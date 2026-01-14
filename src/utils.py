import os
import json
from datetime import datetime
from pathlib import Path

def validate_path(path_str: str) -> Path:
    # Validates if the given path string exists and is a directory.

    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"The path '{path_str}' does not exist.")
    if not path.is_dir():
        raise NotADirectoryError(f"The path '{path_str}' is not a directory.")
    return path

def save_history(folder: Path, mapping: list[tuple[str, str]], general_title: str) -> Path:
    # Saves the rename history to a JSON file in the folder.
    # Format: "Folder Name - YYYY-MM-DD_HH:MM.json"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    folder_name = folder.name
    json_filename = f"{folder_name} - {date_str}.json"
    json_path = folder / json_filename

    history_data = {
        "folder": str(folder),
        "date": datetime.now().isoformat(),
        "general_title": general_title,
        "renames": [
            {"Prev Name": old, "New Name": new}
            for old, new in mapping
        ]
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=4)
    
    return json_path


def update_ignore_file(folder: Path, newly_created_files: list[str]):
   
    ignore_path = folder / ".ignore"
    existing_lines = set()
    if ignore_path.exists():
        try:
            with open(ignore_path, 'r', encoding='utf-8') as f:
                existing_lines = {line.strip() for line in f if line.strip()}
        except Exception:
            pass
    
    # Adds desktop.ini and .ignore file to ignore file
    items_to_ensure = {"desktop.ini", ".ignore"}
    items_to_ensure.update(newly_created_files)
    
    # Determine what to append
    to_append = []
    for item in items_to_ensure:
        if item not in existing_lines:
            to_append.append(item)
            
    if to_append:
        try:
            with open(ignore_path, 'a', encoding='utf-8') as f:
                if ignore_path.exists() and ignore_path.stat().st_size > 0:
                     f.write("\n")
                for item in to_append:
                    f.write(f"{item}\n")
        except Exception as e:
            print(f"Warning: Could not update ignore file: {e}")
