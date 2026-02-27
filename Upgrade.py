import subprocess
import sys
import argparse
import json

def update_pip():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pass

def update_packages(dry_run=False):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            check=True
        )

        outdated_packages = json.loads(result.stdout)

        if not outdated_packages or dry_run:
            return

        for pkg in outdated_packages:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", pkg["name"]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except subprocess.CalledProcessError:
                pass

    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--no-pip', action='store_true')
    args = parser.parse_args()

    if not args.no_pip:
        update_pip()

    update_packages(dry_run=args.dry_run)

if __name__ == "__main__":
    main()