# Renamer

A tool for renaming multiple files at once

## Requirements

1. Install the relevant modules from the requirements file by running `pip install -r requirements.txt`
2. Get the directory of the folder the files to be renamed are in

## Usage
Run `python src/main.py`
Write the names of files to be ignored by tool in a `.ignore` file in the directory
- `desktop.ini` and the history JSON files are also auto-ignored.

The tool has 2 main features
1. **Rename**
- The tool renames files in specified directory
- The tool also creates a JSON file named `Folder Name - YYYY-MM-DD HH:MM.json`
2. **Undo/Restore**
- The tool uses previously created JSON files to restore filenames to their previous forms

