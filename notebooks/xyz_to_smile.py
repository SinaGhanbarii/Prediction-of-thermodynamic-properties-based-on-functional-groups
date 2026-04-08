# Import necessary libraries
import tarfile
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import logging
from rdkit import Chem
import tempfile
import uuid

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# keep only the 12 targets we care about
PROP_LABELS = [
    "mu", "alpha",                  # dipole moment (D), polarizability (Å³)
    "homo", "lumo", "gap",          # orbital energies (Ha) and gap (Ha)
    "r2",                           # <R²> (a₀²)
    "zpve",                         # zero‑point vibrational energy (Ha)
    "U0", "U", "H", "G",            # energies / enthalpy / free energy (Ha)
    "Cv"                            # heat capacity (cal mol‑¹ K‑¹)
]

# Ignore Rotational constants
IGNORED = 3                         # rotA, rotB, rotC

# Function to parse a single QM9 .xyz file and extract SMILES and desired properties
def parse_qm9_xyz(xyz_path: str | Path) -> dict:
    """ 
    Read one QM9‑style .xyz file and return:
        {
            'index' : 3895,
            'smiles': 'O=C1C=CON=N1',
            'props' : {label: value, …}   # the 12 targets (rotA/B/C omitted)
        }
    """
    lines = Path(xyz_path).read_text().splitlines()  # read text file and split into lines

    # ── header ──────────────────────────────────────────────────────────────
    n_atoms = int(lines[0])                 # sanity‑check only 
    header_parts = lines[1].split('\t') # split header line by tab 

    # “gdb 3895” → tag = 'gdb', idx = 3895
    tag, idx = header_parts[0].split()      # extract tag and index of the molecule
    idx = int(idx)

    # Skip the first three values, then take the next 12
    start = 1 + IGNORED                    # 1 = first value column after “gdb idx”
    end   = start + len(PROP_LABELS)
    prop_values = list(map(float, header_parts[start:end]))     # convert to float
    props = dict(zip(PROP_LABELS, prop_values))                 # create a dictionary with labels as keys

    # ── comment block ───────────────────────────────────────────────────────
    smiles = lines[-2].split('\t')[0]      # first token on the penultimate line

    return {"index": idx, "smiles": smiles, "props": props}

# Function to process a .tar.gz file containing QM9 .xyz files and save the dataset to a CSV file
def process_tar_gz(tar_path: str | Path, output_csv: str | Path) -> None:
    """
    Process a .tar.gz file containing QM9 .xyz files and save the dataset to a CSV.

    Args:
        tar_path: Path to the .tar.gz file.
        output_csv: Path to save the output CSV file.
    """
    records = []        # Preallocate a list to store records
    # Create a temporary directory for processing
    temp_dir = Path(tempfile.gettempdir()) / f"qm9_processing_{uuid.uuid4()}"

    try:
        # Create temporary directory
        temp_dir.mkdir(parents=True, exist_ok=True)

        with tarfile.open(tar_path, "r:gz") as tar:
            # Find all .xyz files in the tar archive
            xyz_files = [member for member in tar.getmembers() if member.name.endswith(".xyz")]
            logger.info(f"Found {len(xyz_files)} .xyz files in {tar_path}")

            for member in tqdm(xyz_files, desc="Processing .xyz files"):
                try:
                    # Extract the file from the tar archive
                    f = tar.extractfile(member)
                    if f is None:
                        logger.warning(f"Could not extract {member.name}")
                        continue

                    # Use unique temporary file name
                    temp_xyz = temp_dir / f"{uuid.uuid4()}.xyz"
                    content = f.read().decode("utf-8")
                    temp_xyz.write_text(content)

                    result = parse_qm9_xyz(temp_xyz)
                    if result:
                        # Ensure the result contains the expected keys
                        record = {"index": result["index"], "smiles": result["smiles"]}
                        record.update(result["props"])
                        records.append(record)
                    else:
                        logger.warning(f"Skipping {member.name}: Parsing failed")

                    # Clean up temporary file
                    temp_xyz.unlink()
                except Exception as e:
                    logger.error(f"Error processing {member.name}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Error opening tar file {tar_path}: {e}")
        return
    finally:
        # Clean up temporary directory
        try:
            for temp_file in temp_dir.glob("*.xyz"):
                temp_file.unlink()
            temp_dir.rmdir()
        except Exception as e:
            logger.warning(f"Error cleaning up temporary directory {temp_dir}: {e}")

    if records:
        df = pd.DataFrame(records)
        columns = ["index", "smiles"] + PROP_LABELS
        df = df[columns]
        df = df.sort_values("index")
        df.to_csv(output_csv, index=False)
        logger.info(f"Saved dataset with {len(df)} records to {output_csv}")
    else:
        logger.warning("No valid records processed.")

if __name__ == "__main__":
    tar_path = "dataset.tar.gz"  # Your provided file
    output_csv = "qm9_dataset.csv"  # Output CSV file
    process_tar_gz(tar_path, output_csv)