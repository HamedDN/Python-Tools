import subprocess
import pkg_resources

def update_pip():
    """Update pip to the latest version."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip updated successfully!")
    except Exception as e:
        print(f"Error updating pip: {e}")

def update_packages():
    """Update all installed Python packages to their latest versions."""
    try:
        # Get the list of outdated packages
        outdated_packages = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=freeze"],
            text=True
        ).splitlines()
        
        # Extract package names from the list
        for line in outdated_packages:
            package_name = line.split("==")[0]
            print(f"Updating {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
        
        print("All packages updated successfully!")
    except Exception as e:
        print(f"Error updating packages: {e}")

if __name__ == "__main__":
    import sys
    update_pip()
    update_packages()
