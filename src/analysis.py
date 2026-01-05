import os
import re
import pandas as pd
import matplotlib.pyplot as plt

def parse_vina_output(filepath):
    """
    Parses the PDBQT output to extract Binding Affinities and Mode Numbers.
    """
    modes = []
    affinities = []
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('REMARK VINA RESULT'):
                # Line format: REMARK VINA RESULT:    -8.681      0.000      0.000
                parts = line.split()
                affinity = float(parts[3])
                affinities.append(affinity)
                modes.append(len(affinities)) # Mode 1, Mode 2, etc.
                
    return modes, affinities

def count_heavy_atoms(ligand_path):
    """
    Counts non-hydrogen atoms in the ligand input file to calculate Ligand Efficiency.
    """
    count = 0
    with open(ligand_path, 'r') as f:
        for line in f:
            # Check for atom lines (HETATM or ATOM)
            if line.startswith("HETATM") or line.startswith("ATOM"):
                # Simple check: If element is not Hydrogen
                # PDBQT element is usually near the end or we check the atom name
                atom_name = line[12:16].strip()
                if not atom_name.startswith('H'):
                    count += 1
    return max(count, 1) # Avoid division by zero

def generate_report(docking_output_path, ligand_input_path, output_dir):
    """
    Main function to generate CSV and PNG report.
    """
    print(f"--- Generating Analysis Report ---")
    
    # 1. Extract Data
    modes, affinities = parse_vina_output(docking_output_path)
    atom_count = count_heavy_atoms(ligand_input_path)
    
    if not modes:
        print("✘ No docking results found to analyze.")
        return

    # 2. Calculate Metrics (Data Science Part)
    # Ligand Efficiency (LE) approx = (-Affinity) / Heavy_Atoms
    # (Simplified version for this project)
    le_scores = [(-score / atom_count) for score in affinities]

    # 3. Create DataFrame
    df = pd.DataFrame({
        'Mode': modes,
        'Affinity (kcal/mol)': affinities,
        'Heavy Atoms': [atom_count] * len(modes),
        'Ligand Efficiency': le_scores
    })

    # 4. Save to CSV
    csv_path = os.path.join(output_dir, "docking_report.csv")
    df.to_csv(csv_path, index=False)
    print(f"✔ CSV Report saved: {csv_path}")

    # 5. Generate Plot (Visualization Part)
    plt.figure(figsize=(8, 5))
    plt.bar(modes, affinities, color='skyblue', edgecolor='black')
    plt.xlabel('Binding Mode (Rank)')
    plt.ylabel('Binding Affinity (kcal/mol)')
    plt.title(f'Docking Profile (Best: {affinities[0]} kcal/mol)')
    plt.gca().invert_yaxis() # Invert Y axis because more negative is better
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plot_path = os.path.join(output_dir, "docking_plot.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"✔ Performance Graph saved: {plot_path}")
    print("-" * 30)