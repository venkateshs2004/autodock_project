import subprocess
import os
import sys
from visualization import create_html_viewer
from analysis import generate_report
def run_docking():
    # 1. Setup Paths
    base_dir = os.getcwd() # Should be D:\autodock_project
    vina_exe = os.path.join(base_dir, "bin", "vina.exe")
    receptor = os.path.join(base_dir, "data", "prepared", "receptor.pdbqt")
    ligand   = os.path.join(base_dir, "data", "prepared", "ligand.pdbqt")
    output   = os.path.join(base_dir, "data", "results", "output.pdbqt")

    # 2. Check if files exist
    if not os.path.exists(vina_exe):
        sys.exit(f"Error: vina.exe not found at {vina_exe}")
    if not os.path.exists(receptor):
        sys.exit(f"Error: receptor.pdbqt not found at {receptor}")

    # 3. Grid Parameters (1HSG Active Site)
    # These are the numbers your ML model will eventually predict
    center = [144.561, 138.91, 176.753]  # Approximate center of the pocket
    size   = [20.0, 20.0, 20.0]  # Search space dimensions

    # 4. Construct Command
    cmd = [
        vina_exe,
        '--receptor', receptor,
        '--ligand', ligand,
        '--center_x', str(center[0]),
        '--center_y', str(center[1]),
        '--center_z', str(center[2]),
        '--size_x', str(size[0]),
        '--size_y', str(size[1]),
        '--size_z', str(size[2]),
        '--out', output,
        '--exhaustiveness', '8'
    ]

    # 5. Run
    print(f"Running Vina...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✔ Docking Successful!")
            print(f"✔ Output saved to: {output}")
            # Parse the output to find the best affinity
            for line in result.stdout.splitlines():
                if line.strip().startswith('1'):
                    print(f"  Best Affinity: {line.split()[1]} kcal/mol")
                    print("\nGenerating HTML Visualization...")
                    html_path = os.path.join(base_dir, "data", "results", "view_docking.html")
            
                    create_html_viewer(
                        receptor_path=receptor,
                        ligand_path=output,
                        center=center,
                        size=size,
                        output_file=html_path
                    )
                    print(f"Open this file in your browser: {html_path}")
                    generate_report(
                    docking_output_path=output,
                    ligand_input_path=ligand, # We need the input ligand to count atoms
                    output_dir=os.path.dirname(output)
                    )
                    break
        else:
            print("✘ Docking Failed")
            print(result.stderr)
            
    except FileNotFoundError:
        print("✘ System could not find the executable. Check the path to vina.exe")

if __name__ == "__main__":
    run_docking()
