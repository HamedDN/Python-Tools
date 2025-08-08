import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from ctypes import windll, Structure, c_ulong, byref
import sys

# Define the structure for window composition attributes
class ACCENTPOLICY(Structure):
    _fields_ = [("nAccentState", c_ulong), ("nFlags", c_ulong), ("nColor", c_ulong), ("nAnimationId", c_ulong)]

# Set the window style to glassmorphism effect
def set_glassmorphism_style(window):
    accent = ACCENTPOLICY(3, 0, 0, 0)
    accent_struct_size = sys.getsizeof(accent)
    user32 = windll.user32
    user32.SetWindowCompositionAttribute(window.winfo_id(), byref(accent), accent_struct_size)

class FileOrganizer:
    def __init__(self, directory, film_name):
        self.directory = directory
        self.film_name = film_name
        self.pattern = r'S(\d+)\s*E(\d+)'

    def move_files_from_subfolders(self):
        for root, dirs, files in os.walk(self.directory):
            for dir in dirs:
                subfolder_path = os.path.join(root, dir)
                for root_sub, dirs_sub, files_sub in os.walk(subfolder_path):
                    for file in files_sub:
                        source_path = os.path.join(root_sub, file)
                        destination_path = os.path.join(self.directory, file)
                        shutil.move(source_path, destination_path)

    def rename_files(self):
        files = [f for f in os.listdir(self.directory) if f.endswith('.mkv') or f.endswith('.srt') or f.endswith('.sub')]

        for file in files:
            name, extension = os.path.splitext(file)
            match = re.search(self.pattern, name)
            if match:
                season = match.group(1)
                episode = match.group(2)

                if file.endswith('.srt'):
                    new_file_name = f'{self.film_name} S{season} E{episode} (subtitle){extension}'
                elif file.endswith('.mkv'):
                    new_file_name = f'{self.film_name} S{season} E{episode}{extension}'
                else:
                    continue

                source_path = os.path.join(self.directory, file)
                destination_path = os.path.join(self.directory, new_file_name)

                if not os.path.exists(destination_path):
                    os.rename(source_path, destination_path)
                else:
                    continue

    def organize_files(self):
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

        for file in files:
            name, extension = os.path.splitext(file)
            match = re.search(self.pattern, name)
            if match:
                season = match.group(1)
                episode = match.group(2)
                season_folder = os.path.join(self.directory, f'S{season}')
                if not os.path.exists(season_folder):
                    os.makedirs(season_folder)
                source_path = os.path.join(self.directory, file)
                destination_path = os.path.join(season_folder, file)
                shutil.move(source_path, destination_path)

    def rename_folder(self):
        base_dir = os.path.dirname(self.directory)
        new_folder_name = os.path.join(base_dir, self.film_name)
        try:
            shutil.move(self.directory, new_folder_name)
        except:
            pass

    def delete_empty_folders(self):
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for dir in dirs:
                folder_path = os.path.join(root, dir)
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)

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

    file_organizer = FileOrganizer(directory, film_name)

    file_organizer.move_files_from_subfolders()
    file_organizer.rename_files()
    file_organizer.organize_files()
    file_organizer.delete_empty_folders()
    file_organizer.rename_folder()

    messagebox.showinfo("Success", "File organization completed successfully")

# Window setup
root = tk.Tk()
root.geometry("400x200")
root.configure(bg="#FFFFFF")

# Apply glassmorphism effect
set_glassmorphism_style(root)

# Directory label and entry
directory_label = tk.Label(root, text="Directory:")
directory_label.pack()
directory_entry = tk.Entry(root, width=40)
directory_entry.pack()

# Browse button
browse_button = tk.Button(root, text="Browse", command=browse_directory, bg="#8CA8D1", fg="#FFFFFF")
browse_button.pack(pady=10)

# Film name label and entry
film_name_label = tk.Label(root, text="Film Name:")
film_name_label.pack()
film_name_entry = tk.Entry(root, width=40)
film_name_entry.pack()

# Start button
start_button = tk.Button(root, text="Start", command=start_file_organizer, bg="#8CA8D1", fg="#FFFFFF")
start_button.pack(pady=10)

root.mainloop()