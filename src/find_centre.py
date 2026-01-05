import os

def get_center_from_pdbqt(file_path):
    x_coords = []
    y_coords = []
    z_coords = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # PDBQT columns: X is 30-38, Y is 38-46, Z is 46-54
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    x_coords.append(x)
                    y_coords.append(y)
                    z_coords.append(z)
                except ValueError:
                    continue

    if not x_coords:
        return None

    avg_x = sum(x_coords) / len(x_coords)
    avg_y = sum(y_coords) / len(y_coords)
    avg_z = sum(z_coords) / len(z_coords)

    return [round(avg_x, 3), round(avg_y, 3), round(avg_z, 3)]

if __name__ == "__main__":
    # Point this to your prepared receptor
    receptor_path = os.path.join("data", "prepared", "receptor.pdbqt")
    
    center = get_center_from_pdbqt(receptor_path)
    
    if center:
        print("-" * 30)
        print(f"Receptor Found at: {receptor_path}")
        print(f"CALCULATED CENTER: {center}")
        print("-" * 30)
        print("Update your src/docking.py with these coordinates!")
    else:
        print("Error: Could not read atoms from file.")