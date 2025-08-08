import os
import re
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from ctypes import windll, Structure, c_ulong, byref

# --- Windows Glassmorphism Effect ---
class ACCENTPOLICY(Structure):
    _fields_ = [
        ("nAccentState", c_ulong),
        ("nFlags", c_ulong),
        ("nColor", c_ulong),
        ("nAnimationId", c_ulong)
    ]

def set_glassmorphism_style(window):
    accent = ACCENTPOLICY(3, 0, 0, 0)
    accent_struct_size = sys.getsizeof(accent)
    user32 = windll.user32
    user32.SetWindowCompositionAttribute(window.winfo_id(), byref(accent), accent_struct_size)

# --- File Organizer Logic ---
class FileOrganizer:
    def __init__(self, directory, film_name):
        self.directory = directory
        self.film_name = film_name
        self.pattern = r'S(\d+)\s*E(\d+)'
        self.supported_extensions = ('.mkv', '.srt', '.sub')

    def move_files_from_subfolders(self):
        """Move all files from subfolders to the main directory."""
        for root, dirs, _ in os.walk(self.directory):
            for dir in dirs:
                subfolder_path = os.path.join(root, dir)
                for _, _, files_sub in os.walk(subfolder_path):
                    for file in files_sub:
                        src = os.path.join(subfolder_path, file)
                        dst = os.path.join(self.directory, file)
                        shutil.move(src, dst)

    def rename_files(self):
        """Rename .mkv, .srt, and .sub files to a standard format."""
        files = [f for f in os.listdir(self.directory)
                 if f.endswith(self.supported_extensions)]
        for file in files:
            name, ext = os.path.splitext(file)
            match = re.search(self.pattern, name)
            if not match:
                continue
            season, episode = match.groups()
            if ext == '.srt':
                new_name = f'{self.film_name} S{season} E{episode} (subtitle){ext}'
            elif ext == '.mkv':
                new_name = f'{self.film_name} S{season} E{episode}{ext}'
            else:
                continue
            src = os.path.join(self.directory, file)
            dst = os.path.join(self.directory, new_name)
            if not os.path.exists(dst):
                os.rename(src, dst)

    def organize_files(self):
        """Move files into season folders."""
        files = [f for f in os.listdir(self.directory)
                 if os.path.isfile(os.path.join(self.directory, f))]
        for file in files:
            name, _ = os.path.splitext(file)
            match = re.search(self.pattern, name)
            if not match:
                continue
            season = match.group(1)
            season_folder = os.path.join(self.directory, f'S{season}')
            os.makedirs(season_folder, exist_ok=True)
            src = os.path.join(self.directory, file)
            dst = os.path.join(season_folder, file)
            shutil.move(src, dst)

    def rename_folder(self):
        """Rename the main folder to the film name."""
        base_dir = os.path.dirname(self.directory)
        new_folder = os.path.join(base_dir, self.film_name)
        try:
            shutil.move(self.directory, new_folder)
        except Exception:
            pass

    def delete_empty_folders(self):
        """Delete any empty folders."""
        for root, dirs, _ in os.walk(self.directory, topdown=False):
            for dir in dirs:
                folder_path = os.path.join(root, dir)
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)

# --- GUI Functions ---
def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(tk.END, directory)

def start_file_organizer():
    directory = directory_entry.get()
    film_name = film_name_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory path")
        return
    if not film_name:
        messagebox.showerror("Error", "Film name cannot be empty")
        return
    organizer = FileOrganizer(directory, film_name)
    organizer.move_files_from_subfolders()
    organizer.rename_files()
    organizer.organize_files()
    organizer.delete_empty_folders()
    organizer.rename_folder()
    messagebox.showinfo("Success", "File organization completed successfully")

# --- GUI Setup ---
root = tk.Tk()
root.geometry("400x200")
root.configure(bg="#FFFFFF")
set_glassmorphism_style(root)

# Directory input
tk.Label(root, text="Directory:").pack()
directory_entry = tk.Entry(root, width=40)
directory_entry.pack()
tk.Button(root, text="Browse", command=browse_directory, bg="#8CA8D1", fg="#FFFFFF").pack(pady=10)

# Film name input
tk.Label(root, text="Film Name:").pack()
film_name_entry = tk.Entry(root, width=40)
film_name_entry.pack()

# Start button
tk.Button(root, text="Start", command=start_file_organizer, bg="#8CA8D1", fg="#FFFFFF").pack(pady=10)

root.mainloop()