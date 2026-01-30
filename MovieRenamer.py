import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

VIDEO_EXTENSIONS = ('.mkv', '.mp4', '.avi', '.mov')
YEAR_REGEX = re.compile(r'(19\d{2}|20\d{2})')


def clean_name(raw_name):
    # Replace dots/underscores with spaces and title-case
    name = raw_name.replace('.', ' ').replace('_', ' ').strip()
    name = re.sub(r'\s+', ' ', name)
    return name.title()


def organize_movie(base_dir, file):
    """
    Organize a single movie file with user input:
    - Detect year
    - Ask user for movie name
    - Create folder and move file
    """
    src = os.path.join(base_dir, file)

    if not os.path.isfile(src):
        return

    if not file.lower().endswith(VIDEO_EXTENSIONS):
        return

    # Detect year
    year_match = YEAR_REGEX.search(file)
    if not year_match:
        print(f"⚠ Year not found in file: {file}")
        return

    year = year_match.group(1)

    # Suggest movie name based on filename (everything before year)
    user_input = input(f"\nMovie found: {file}: ").strip()

    if user_input:
        movie_name = user_input

    if not movie_name:
        print("⚠ Skipping file (no name given).")
        return

    # Create folder
    movie_folder = os.path.join(base_dir, movie_name)
    os.makedirs(movie_folder, exist_ok=True)

    # Rename file
    ext = os.path.splitext(file)[1]
    new_filename = f"{movie_name} ({year}){ext}"
    dst = os.path.join(movie_folder, new_filename)

    if not os.path.exists(dst):
        print(f"MOVING: {file} -> {dst}")
        shutil.move(src, dst)
    else:
        print(f"⚠ File already exists: {dst}")


def main():
    # Hide Tk root window
    root = tk.Tk()
    root.withdraw()

    print("📂 Select movies folder")
    base_dir = filedialog.askdirectory()
    if not base_dir:
        print("❌ No folder selected")
        return

    files = os.listdir(base_dir)
    print(f"\nFound {len(files)} files. Organizing...\n")

    for file in files:
        organize_movie(base_dir, file)

    print("\n✅ All movies organized!")


if __name__ == "__main__":
    main()
