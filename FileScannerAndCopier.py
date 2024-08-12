import os
import fnmatch
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from threading import Thread

def scan_and_copy_files(root_folder, extensions, destination_folder, progress_callback):
    matched_files = []
    scanned_files_count = 0
    copied_files_set = set()
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    total_files = 0
    # First pass to count total files
    for root, dirs, files in os.walk(root_folder):
        for extension in extensions:
            for filename in fnmatch.filter(files, extension):
                total_files += 1

    # Second pass to scan and copy files
    scanned_files_count = 0
    for root, dirs, files in os.walk(root_folder):
        for extension in extensions:
            for filename in fnmatch.filter(files, extension):
                full_file_path = os.path.join(root, filename)
                if not os.path.isfile(full_file_path):  # Ensure it's a file
                    continue
                
                # Count the file and add it to the list
                matched_files.append(full_file_path)
                scanned_files_count += 1

                # Update progress
                progress_callback(scanned_files_count, total_files)
                
                # Create a relative path based on the root_folder and replace slashes with underscores
                relative_path = os.path.relpath(root, root_folder)
                safe_relative_path = relative_path.replace(os.sep, '_')
                dest_folder = os.path.join(destination_folder, safe_relative_path)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                    
                dest_file_path = os.path.join(dest_folder, filename)
                # Ensure unique filename in the destination folder
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_file_path):  # Check if the file already exists
                    dest_file_path = os.path.join(dest_folder, f"{base}_{counter}{extension}")
                    counter += 1

                try:
                    shutil.copy(full_file_path, dest_file_path)
                    copied_files_set.add((full_file_path, dest_file_path))  # Add to set of copied files
                except Exception as e:
                    print(f"Error copying {filename}: {e}")

    copied_files_count = len(copied_files_set)  # Count unique copied files
    return scanned_files_count, copied_files_count, copied_files_set

def update_progress_bar(value, total_files, progress_bar, progress_label):
    if total_files > 0:
        progress_bar['maximum'] = total_files
        progress_bar['value'] = value
        progress_label.config(text=f"Progress: {int((value/total_files)*100)}%")
        loading_screen.update_idletasks()
    else:
        progress_bar['maximum'] = 1
        progress_bar['value'] = 1
        progress_label.config(text="Progress: 100%")
        loading_screen.update_idletasks()

def start_scan():
    root_folder = root_folder_entry.get()
    destination_folder = destination_folder_entry.get()
    
    if not root_folder or not destination_folder:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    extensions = extension_selector.get_selected_extensions()

    if not extensions:
        messagebox.showerror("Error", "Please select at least one extension")
        return

    def update_progress(value, total_files):
        update_progress_bar(value, total_files, progress_bar, progress_label)

    def scan_thread():
        scanned_files_count, copied_files_count, copied_files = scan_and_copy_files(
            root_folder, extensions, destination_folder, update_progress)
        loading_screen.destroy()
        if copied_files_count > 0:
            messagebox.showinfo("Success", f"Copied {copied_files_count} files to {destination_folder}")
        else:
            messagebox.showinfo("No Files Found", "No files matching the specified extensions were found.")

    # Create and display the loading screen
    global loading_screen
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Loading...")
    loading_screen.geometry("350x150")
    tk.Label(loading_screen, text="Scanning and copying files, please wait...", padx=20, pady=20).pack()
    progress_bar = ttk.Progressbar(loading_screen, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(padx=20, pady=10)
    progress_label = tk.Label(loading_screen, text="Progress: 0%")
    progress_label.pack(pady=10)

    # Start scanning in a new thread to keep the GUI responsive
    scan_thread = Thread(target=scan_thread)
    scan_thread.start()

class ExtensionSelector:
    def __init__(self, parent, options):
        self.parent = parent
        self.options = options
        self.selected_extensions = []

        self.frame = tk.Frame(parent)
        self.frame.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        self.frame.grid_columnconfigure(0, weight=1)

        self.button = tk.Button(self.frame, text="Select Extensions", command=self.open_dropdown, width=20)
        self.button.pack(pady=5)

        self.selected_label = tk.Label(self.frame, text="Selected Extensions: None")
        self.selected_label.pack(pady=5)

    def open_dropdown(self):
        self.dropdown_window = tk.Toplevel(self.parent)
        self.dropdown_window.title("Select Extensions")
        self.dropdown_window.geometry("400x400")  # Adjusted size for better visibility

        self.listbox_frame = tk.Frame(self.dropdown_window)
        self.listbox_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=15)  # Increased height
        for ext in self.options:
            self.listbox.insert(tk.END, ext)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Add "Select All" button
        select_all_button = tk.Button(self.dropdown_window, text="Select All", command=self.select_all)
        select_all_button.pack(pady=5)

        apply_button = tk.Button(self.dropdown_window, text="Apply", command=self.apply_selection)
        apply_button.pack(pady=10)

    def select_all(self):
        self.listbox.select_set(0, tk.END)

    def apply_selection(self):
        selected_indices = self.listbox.curselection()
        self.selected_extensions = [self.listbox.get(i) for i in selected_indices]
        self.update_selected_label()
        self.dropdown_window.destroy()

    def update_selected_label(self):
        if self.selected_extensions:
            # Truncate the list of selected extensions if it's too long
            if len(self.selected_extensions) > 5:
                extensions_text = ', '.join(self.selected_extensions[:5]) + ' ...'
            else:
                extensions_text = ', '.join(self.selected_extensions)
        else:
            extensions_text = "None"
        self.selected_label.config(text=f"Selected Extensions: {extensions_text}")

    def get_selected_extensions(self):
        return self.selected_extensions

# GUI Setup
root = tk.Tk()
root.title("File Scanner and Copier")
root.geometry("600x300")
root.resizable(False, False)  # Make the window non-resizable

# Set the icon for the main window
icon_path = 'icon.ico'  # Replace with the path to your icon file
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Main frame for alignment
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Root Folder
tk.Label(main_frame, text="Root Folder:", anchor="e").grid(row=0, column=0, padx=10, pady=10, sticky="e")
root_folder_entry = tk.Entry(main_frame, width=50)
root_folder_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(main_frame, text="Browse", command=lambda: root_folder_entry.insert(0, filedialog.askdirectory())).grid(row=0, column=2, padx=10, pady=10)

# Destination Folder
tk.Label(main_frame, text="Destination Folder:", anchor="e").grid(row=1, column=0, padx=10, pady=10, sticky="e")
destination_folder_entry = tk.Entry(main_frame, width=50)
destination_folder_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(main_frame, text="Browse", command=lambda: destination_folder_entry.insert(0, filedialog.askdirectory())).grid(row=1, column=2, padx=10, pady=10)

# Extension Selector
extension_options = ["*.txt", "*.log", "*.csv", "*.xml", "*.json", "*.db", "*.dbf", "*.sqlite", "*.sql", "*.dat", "*.bin", "*.dmp", "*.pcap", "*.pst", "*.msg", "*.eml", "*.doc", "*.docx", "*.xls", "*.xlsx", "*.pdf", "*.html", "*.htm", "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.mp4", "*.avi", "*.mov", "*.mkv", "*.wav", "*.mp3", "*.flac", "*.dll", "*.exe", "*.bat", "*.sh", "*.py", "*.java", "*.cpp", "*.c", "*.h", "*.pl", "*.rb", "*.php", "*.asp", "*.jsp", "*.cfg", "*.ini", "*.key", "*.pem", "*.crt", "*.csr", "*.p12", "*.pfx", "*.jks", "*.bak", "*.tmp", "*.iso", "*.dmg", "*.tar", "*.gz", "*.zip", "*.rar", "*.7z", "*.dd", "*.e01", "*.aff", "*.s01", "*.000", "*.img"] # Add more extensions as needed
extension_selector = ExtensionSelector(main_frame, extension_options)

# Start Button
tk.Button(main_frame, text="Start Scan", command=start_scan, width=20).grid(row=4, column=1, pady=20)

root.mainloop()
