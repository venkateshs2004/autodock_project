import os
import py3Dmol

def create_html_viewer(receptor_path, ligand_path, center, size, output_file="view_docking.html"):
    """
    Generates an animated HTML file.
    - Animation: Infinite Loop (reps: 0)
    - Speed: Slow (interval: 1000ms = 1 second per pose)
    """
    
    # 1. Read Data
    with open(receptor_path, 'r') as f:
        receptor_data = f.read()
    with open(ligand_path, 'r') as f:
        ligand_data = f.read()

    # 2. Setup 3D Viewer
    view = py3Dmol.view(width=800, height=600)
    
    # --- LAYER 1: The Protein (Static) ---
    view.addModel(receptor_data, "pdbqt")
    view.setStyle({'model': -1}, {'cartoon': {'color': 'gray'}})
    view.addSurface(py3Dmol.VDW, {'opacity': 0.4, 'color': 'white'}, {'model': -1})

    # --- LAYER 2: The Grid Box (Static) ---
    view.addBox({
        'center': {'x': center[0], 'y': center[1], 'z': center[2]},
        'dimensions': {'w': size[0], 'h': size[1], 'd': size[2]},
        'color': 'yellow',
        'opacity': 0.6,
        'wireframe': True
    })

    # --- LAYER 3: The Docking Results (Animated) ---
    view.addModelsAsFrames(ligand_data, "pdbqt")
    view.setStyle({'model': -1}, {'stick': {'colorscheme': 'magentaCarbon'}})
    
    # --- ANIMATION SETTINGS (CORRECTED) ---
    # loop: 'forward' (plays start to end, then restarts)
    # reps: 0 (Infinite loop)
    # interval: 1000 (1000 milliseconds = 1 second per frame)
    view.animate({'loop': 'forward', 'reps': 0, 'interval': 1000})

    # 3. Finalize
    view.zoomTo({'model': -1})
    
    # Write to HTML
    html_content = view._make_html()
    with open(output_file, "w") as f:
        f.write(html_content)
    
    print(f"✔ Infinite Loop Visualization saved to: {output_file}")