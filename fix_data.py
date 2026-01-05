import os
import urllib.request
import ssl

# Bypass SSL errors that sometimes happen on Windows
ssl._create_default_https_context = ssl._create_unverified_context

# --- WORKING BACKUP URLs ---
# Using a stable GitHub example repository that hosts pre-prepared PDBQT files
BASE_URL = "https://raw.githubusercontent.com/sha256feng/Autodock-vina-example/master/"
FILES = {
    "receptor.pdbqt": BASE_URL + "pocket.pdbqt",    # The protein pocket
    "ligand.pdbqt":   BASE_URL + "ligand-b.pdbqt"   # The drug molecule
}

def download_fix():
    target_dir = os.path.join("data", "prepared")
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"--- Downloading to {target_dir} ---")
    
    for local_name, url in FILES.items():
        save_path = os.path.join(target_dir, local_name)
        print(f"Downloading {local_name}...")
        
        try:
            urllib.request.urlretrieve(url, save_path)
            size = os.path.getsize(save_path)
            if size > 100:
                print(f"✔ Success! ({size} bytes)")
            else:
                print(f"⚠ Warning: File {local_name} is empty. The link might be dead.")
        except Exception as e:
            print(f"✘ Failed: {e}")

if __name__ == "__main__":
    download_fix()
    print("\nReady to dock. Run: python src/docking.py")