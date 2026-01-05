Here is the finalized content, formatted as a clean, copy-pasteable `README.md` file.

```markdown
# Protein-Ligand Interaction Automator

## 📌 Project Overview
This tool automates the structural analysis required for drug discovery. It streamlines the workflow between protein pocket detection and molecular docking, eliminating the need for manual grid box calculation.

**What this project does:**
1.  **Pocket Detection:** Uses **fpocket** to scan the protein surface and identify the most "druggable" binding sites (cavities).
2.  **Automated Grid Box Setup:** Parses the pocket data to automatically calculate the XYZ coordinates and dimensions of the binding site.
3.  **Molecular Docking:** Feeds these coordinates into **AutoDock Vina** to simulate the binding of a ligand (drug) to the protein.

## 🛠️ Prerequisites
To reproduce the results, the following software must be installed on your system.

### 1. System Dependencies (Linux/Ubuntu)
* **fpocket:** For finding protein cavities.
* **AutoDock Vina:** For performing the docking simulation.

```bash
sudo apt-get install fpocket autodock-vina

```

### 2. Python Dependencies

* **Python 3.x**
* **Pandas:** For handling data logs.
* **NumPy:** For coordinate calculations.

```bash
pip install pandas numpy

```

## 📂 Folder Structure

Ensure your project directory is organized as follows before running:

```text
Project_Root/
├── data/
│   ├── protein.pdb       # Target Protein file
│   └── ligand.pdbqt      # Prepared Ligand file
├── src/
│   └── main.py           # Main automation script
└── README.md

```

## 🚀 How to Execute

1. **Prepare Input Files:**
Place your `.pdb` (protein) and `.pdbqt` (ligand) files inside the `data/` folder.
2. **Run the Script:**
Execute the main Python script from your terminal:
```bash
python src/main.py

```


3. **View Results:**
* **Pocket Report:** The script will output the detected pocket parameters from fpocket.
* **Binding Affinity:** Check the generated log file (e.g., `docking_log.txt`) for the **affinity score** (e.g., `-8.5 kcal/mol`).
* **Docked Pose:** The final structure will be saved (e.g., `output_ligand.pdbqt`) for viewing in PyMOL or Chimera.



```

```
