# File-Scanner-And-Copier
File Scanner and Copier is a user-friendly Python application for scanning and organizing files based on their extensions. With an intuitive Tkinter GUI, this tool allows users to specify file types and directories to efficiently locate and copy files.

## Overview

The **File Scanner and Copier** is a Python application designed to scan a specified root folder for files with selected extensions and copy them to a destination folder. The application uses Tkinter for the graphical user interface and supports a variety of file extensions. It provides progress updates and ensures that files with the same name from different folders are handled correctly by organizing them into subfolders named after their original paths.

## Features

- **GUI-Based**: Easy-to-use graphical interface built with Tkinter.
- **Extension Selection**: Choose from a wide range of file extensions to scan for.
- **Progress Tracking**: Real-time progress updates during file scanning and copying.
- **Unique File Handling**: Files with the same name are organized into folders named after their original paths.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

## Installation

### Using the Installer

1. **Download the Installer**

   Download the installer executable from the [Releases](https://github.com/yourusername/file-scanner-copier/releases) page on GitHub.

2. **Run the Installer**

   - **Windows**: Double-click the downloaded `.exe` file and follow the on-screen instructions to install the application.

3. **Launch the Application**

   After installation, you can start the application from your application menu or desktop shortcut.

### Manual Installation For Other OS (Optional)

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Parth4123/File-Scanner-And-Copier
   cd file-scanner-copier

2. **Install Dependencies**
    
    Ensure you have Python 3 installed. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt

3. **Run the Application**

   Start the application by running:
   ```bash
   python FileScannerAndCopier.py

## Usage

1. **Select Source and Destination Folders**

   - Click on the `Browse` button to choose the root folder to scan.
   - Click on the `Browse` button to select the destination folder for copied files.

2. **Choose File Extensions**

   - Select the file extensions you want to scan for by checking the corresponding checkboxes.

3. **Start Scanning and Copying**

   - Click on the `Scan and Copy Files` button to begin the process.
   - The progress bar will update in real-time as files are scanned and copied.

## Customizing File Extensions

You can customize the list of file extensions by modifying the `extensions` list in the `FileScannerAndCopier.py` file. Add or remove file extensions as needed.

```python
 ["*.txt", "*.log", "*.csv", "*.xml", "*.json", "*.db", "*.dbf", "*.sqlite", "*.sql", "*.dat", "*.bin", "*.dmp", "*.pcap", "*.pst", "*.msg", "*.eml", "*.doc", "*.docx", "*.xls", "*.xlsx", "*.pdf", "*.html", "*.htm", "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.mp4", "*.avi", "*.mov", "*.mkv", "*.wav", "*.mp3", "*.flac", "*.dll", "*.exe", "*.bat", "*.sh", "*.py", "*.java", "*.cpp", "*.c", "*.h", "*.pl", "*.rb", "*.php", "*.asp", "*.jsp", "*.cfg", "*.ini", "*.key", "*.pem", "*.crt", "*.csr", "*.p12", "*.pfx", "*.jks", "*.bak", "*.tmp", "*.iso", "*.dmg", "*.tar", "*.gz", "*.zip", "*.rar", "*.7z", "*.dd", "*.e01", "*.aff", "*.s01", "*.000", "*.img"]
    