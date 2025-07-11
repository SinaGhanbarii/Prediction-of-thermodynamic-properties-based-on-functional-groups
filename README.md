# Prediction of Thermodynamic Properties Based on Functional Groups

This repository contains the complete implementation and report of a project conducted for the course **Data Science in Chemical Engineering**, focused on predicting quantum molecular properties from functional group descriptors.

## 📌 Project Objective

To develop and compare classical machine learning models and neural networks for the prediction of 12 quantum chemical properties of small organic molecules using features derived from:
- Functional group counts
- Atomic composition
- Physicochemical and electronic descriptors

The project aims to evaluate the effect of feature engineering and model complexity on predictive performance.

## 🧪 Dataset

- **QM9 Dataset**: Contains ~134,000 small organic molecules with computed quantum mechanical properties.
- A subset of ~10,000 molecules was used.
- SMILES strings were parsed using **RDKit** to extract structural and chemical features.

## 🧰 Methods

### 🔬 Feature Engineering
- Functional group counts (via RDKit Fragment Catalog)
- Atom counts per element
- Physicochemical descriptors: TPSA, MR
- Electronic descriptors: Gasteiger charges
- Shape descriptors: Principal Moments of Inertia (PMI)

### 🤖 Models Trained
- **Classical ML**:
  - Ridge Regression
  - Random Forest
  - Histogram-Based Gradient Boosting
- **Neural Networks**:
  - Feedforward dense architecture with hyperparameter tuning via Keras Tuner
 


## 📓 Notebooks

| Notebook Filename                             | Description                                                  |
|----------------------------------------------|--------------------------------------------------------------|
| `Benchmark After Feature Engineering.ipynb`   | Benchmarking model performance after applying feature engineering |
| `Benchmark Before Feature Engineering.ipynb`  | Benchmarking model performance using raw descriptors          |
| `Classic ML After Feature Engineering.ipynb`  | Classical ML models trained on engineered features            |
| `Classic ML Before Feature Engineering.ipynb` | Classical ML models trained on base descriptors               |
| `Dataset Visualization.ipynb`                | Visual analysis and feature exploration of the dataset        |
| `Functional Groups Extraction.ipynb`         | Functional group counting using RDKit Fragment Catalog        |
| `Neural Network After Feature Engineering.ipynb` | Neural network training and evaluation with engineered features |
| `Neural Network Before Feature Engineering.ipynb` | Neural network performance on unprocessed descriptors         |
| `xyz Decoder.ipynb`                          | Converts `.xyz` molecular files to readable formats (e.g., SMILES) |
| `xyz parser.ipynb`                           | Parses `.xyz` files and extracts necessary molecular details  |


  

## 📊 Results Summary

| Scenario | Avg R² | Avg MAE |
|----------|--------|---------|
| Classical ML (with features) | ~0.906 | ~0.782 |
| Neural Network (with features) | ~0.906 | ~0.782 |

- Feature engineering significantly improved model accuracy.
- Classical models were more interpretable.
- Dipole moment (μ) remained hardest to predict due to geometry dependence.

## 📈 Visualizations & Evaluation
- Model performance plots
- Parity plots
- SHAP analysis for feature importance
- Training history curves (for neural networks)

## 💡 Future Directions

- Include 3D structural descriptors
- Explore Graph Neural Networks (GNNs)
- Apply transfer learning techniques
- Incorporate uncertainty quantification
- Combine domain descriptors with embeddings

## 🛠️ Tools & Libraries

- Python 3.x
- RDKit
- scikit-learn
- XGBoost
- TensorFlow / Keras
- SHAP


