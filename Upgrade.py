import subprocess
import sys
import argparse

def update_pip():
    """Update pip to the latest version."""
    print("Checking pip version...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,  # Suppress verbose output
            stderr=subprocess.PIPE
        )
        print("✅ pip updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error updating pip: {e}")
    except Exception as e:
        print(f"❌ Unexpected error updating pip: {e}")

def update_packages(dry_run=False):
    """
    Update all installed Python packages to their latest versions.
    
    Args:
        dry_run: If True, only list packages that would be updated without updating
    """
    try:
        # Get the list of outdated packages
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse JSON output (more reliable than parsing freeze format)
        import json
        outdated_packages = json.loads(result.stdout)
        
        if not outdated_packages:
            print("✅ All packages are up to date!")
            return
        
        print(f"Found {len(outdated_packages)} outdated packages:")
        for pkg in outdated_packages:
            print(f"  • {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        
        if dry_run:
            print("\nDry run complete. No packages were updated.")
            return
        
        # Update packages
        success_count = 0
        fail_count = 0
        
        for pkg in outdated_packages:
            package_name = pkg['name']
            print(f"\nUpdating {package_name}...")
            
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE
                )
                print(f"  ✅ {package_name} updated successfully")
                success_count += 1
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Failed to update {package_name}: {e}")
                fail_count += 1
        
        print(f"\n📦 Update complete: {success_count} updated, {fail_count} failed")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting outdated packages: {e}")
    except json.JSONDecodeError:
        print("❌ Error parsing pip output")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Update pip and Python packages")
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be updated without actually updating')
    parser.add_argument('--no-pip', action='store_true',
                       help='Skip updating pip itself')
    
    args = parser.parse_args()
    
    if not args.no_pip:
        update_pip()
        print()  # Empty line for separation
    
    update_packages(dry_run=args.dry_run)

if __name__ == "__main__":
    main()