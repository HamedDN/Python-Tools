import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

class FileOrganizer:
    def __init__(self, source_dir, film_name):
        self.source_dir = source_dir
        self.film_name = film_name
        self.target_dir = os.path.join(source_dir, film_name)

        # Supports: S01E02, S1E2, S01 E02, S01-E02
        self.pattern = re.compile(r'S(\d+)[\s._-]*E(\d+)', re.IGNORECASE)
        self.supported_extensions = ('.mkv', '.srt')

        os.makedirs(self.target_dir, exist_ok=True)

    def process_files(self):
        for root, _, files in os.walk(self.source_dir):
            # Do not scan inside target folder
            if os.path.abspath(root).startswith(os.path.abspath(self.target_dir)):
                continue

            for file in files:
                if not file.lower().endswith(self.supported_extensions):
                    continue

                match = self.pattern.search(file)
                if not match:
                    continue   # 👈 IMPORTANT: ignore unrelated files

                season, episode = match.groups()

                ext = os.path.splitext(file)[1].lower()

                if ext == '.srt':
                    new_name = f"{self.film_name} S{season} E{episode} (subtitle){ext}"
                else:
                    new_name = f"{self.film_name} S{season} E{episode}{ext}"

                season_folder = os.path.join(self.target_dir, f"S{season}")
                os.makedirs(season_folder, exist_ok=True)

                src = os.path.join(root, file)
                dst = os.path.join(season_folder, new_name)

                if not os.path.exists(dst):
                    shutil.move(src, dst)

    def clean_empty(self):
        for root, dirs, _ in os.walk(self.source_dir, topdown=False):
            for d in dirs:
                folder = os.path.join(root, d)
                if folder != self.target_dir and not os.listdir(folder):
                    os.rmdir(folder)


def main():
    root = tk.Tk()
    root.withdraw()

    print("📂 Select parent folder (example: D:\\N)")
    source_dir = filedialog.askdirectory()

    if not source_dir:
        print("❌ No folder selected")
        return

    film_name = input("🎬 Enter series name: ").strip()

    if not film_name:
        print("❌ Series name empty")
        return

    organizer = FileOrganizer(source_dir, film_name)

    organizer.process_files()

    organizer.clean_empty()

    print("\n✅ DONE")

if __name__ == "__main__":
    main()