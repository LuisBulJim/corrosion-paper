# Corrosion Detection Project

This repository contains research and code for detecting corrosion in different environments (aerial and aquatic) using machine learning and deep learning techniques. The project involves dataset visualization, preprocessing, model training (specifically using Ultralytics models), and logical ensembles.

## 📂 Repository Structure

The project is organized into sequential notebooks and support directories:

*   **Data Analysis & Preprocessing**
    *   `0.1Visualización_dataset.ipynb`: Initial exploration and visualization of the dataset.
    *   `0.Tratamiento_dataset_acuatico.ipynb`: Specific preprocessing steps for aquatic environment datasets.

*   **Model Training**
    *   `1.Entrenamiento_Corrosion_Aereo.ipynb`: Training models on aerial corrosion data.
    *   `2.Entrenamiento_corrosion_acuatico_KFold.ipynb`: Training on aquatic data using K-Fold Cross Validation.
    *   `3.Entrenamiento_Corrosion_Mixto.ipynb`: Training models on a combined dataset (mixed environments).

*   **Evaluation & Results**
    *   `4.Comparacion_Modelos.ipynb`: Comparative analysis of the trained models.
    *   `5.Ensemble_Logico.ipynb`: Implementation of logical ensemble methods to improve detection accuracy.
    *   `6.Visualizacion_Resultados.ipynb`: Visualization of the final predictions and results.

*   **Configuration & Dependencies**
    *   `pyproject.toml`: Project configuration and dependency definition (managed by `uv`).
    *   `uv.lock`: Lockfile ensuring reproducible dependency versions.
    *   `modelos_entrenados/`: Directory containing trained model artifacts.
    *   `runs/`: Logs and outputs from model training runs.

## 🚀 Getting Started

This project uses **[uv](https://github.com/astral-sh/uv)** for fast and reliable dependency management.

### Prerequisites

*   Python 3.12+
*   `uv` (Universal Python Package Installer)

### Installation

1.  **Install `uv`** (if you haven't already):
    ```bash
    # On Linux/macOS
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    # Or via pip
    pip install uv
    ```

2.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd Articulo-Corrosion
    ```

3.  **Sync Dependencies**:
    Initialize the environment and install all required packages defined in `pyproject.toml`.
    ```bash
    uv sync
    ```
    This will create a hidden `.venv` directory with the exact environment needed.

4.  **Setup Jupyter Kernel**:
    Register the environment as a Jupyter kernel so you can use it within the notebooks.
    ```bash
    uv run python -m ipykernel install --user --name=articulo-corrosion --display-name "Python (Articulo Corrosion)"
    ```

### Usage

1.  Launch Jupyter Lab or Notebook:
    ```bash
    uv run jupyter lab
    # or just open your preferred IDE (VS Code, Cursor, etc.)
    ```
2.  Open any `.ipynb` file.
3.  **Important**: Ensure the kernel is set to **"Python (Articulo Corrosion)"**.
