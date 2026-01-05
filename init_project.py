import os
import urllib.request
import sys

# --- CONFIGURATION ---
FOLDERS = [
    r"bin",
    r"src",
    r"data\raw",
    r"data\prepared",
    r"data\results"
]

# Stable URLs from the official AutoDock Vina repository (Development branch)
URLS = {
    "receptor.pdbqt": "https://raw.githubusercontent.com/ccsb-scripps/autodock_vina/develop/example/1hsg/receptor.pdbqt",
    "ligand.pdbqt": "https://raw.githubusercontent.com/ccsb-scripps/autodock_vina/develop/example/1hsg/ligand.pdbqt"
}

def create_structure():
    print("--- Creating Directory Structure ---")
    for folder in FOLDERS:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"✔ Created/Verified: {folder}")
        except OSError as e:
            print(f"✘ Error creating {folder}: {e}")

    # Create empty __init__.py in src to make it a package
    with open(r"src\__init__.py", "w") as f:
        pass

def download_data():
    print("\n--- Downloading Sample Data (1HSG) ---")
    target_dir = r"data\prepared"
    
    for filename, url in URLS.items():
        destination = os.path.join(target_dir, filename)
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, destination)
            # Verify file isn't empty (common issue with bad URLs)
            if os.path.getsize(destination) < 100:
                print(f"⚠ Warning: {filename} seems too small. The URL might be broken.")
            else:
                print(f"✔ Success: {destination}")
        except Exception as e:
            print(f"✘ Failed to download {filename}: {e}")
            print(f"  -> Please download manually from: {url}")

if __name__ == "__main__":
    create_structure()
    download_data()
    print("\n--- Setup Complete ---")
    print("Next Step: Download 'vina.exe' and place it in the 'bin' folder.")