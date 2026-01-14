import os
import math
import json
from pathlib import Path
from natsort import natsorted

def get_files(folder: Path) -> list[Path]:
    # Returns a sorted list of files in the folder (ignoring subdirectories).
    
    files = [f for f in folder.iterdir() if f.is_file()]
    
    # Check for ignore file
    ignore_file = '.ignore'
    ignored_names = set(ignore_file) # Always ignore the ignore file itself
    ignored_names.add('desktop.ini') # Ignore "desktop.ini"

    # Read the ignore file content
    ignore_path = folder / ignore_file
    if ignore_path.exists():
        try:
            with open(ignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    name = line.strip()
                    if name and not name.startswith('#'):
                        ignored_names.add(name)
        except Exception as e:
            print(f"Warning: Could not read ignore file {ignore_file}: {e}")

    # Log/print what is being ignored might be useful, but let's just filter.
    filtered_files = []
    for f in files:
        if f.name in ignored_names:
            continue
        # Also ignore history files (pattern check) to prevent renaming "Name - Date.json"
        if f.suffix == '.json' and ' - 20' in f.name:
            continue
        filtered_files.append(f)

    # Sort NATURALLY by filename not LEXICOGRAPHICALLY
    filtered_files = natsorted(filtered_files, key=lambda f: f.name)
    return filtered_files

def generate_rename_mapping(files: list[Path], general_title: str) -> list[tuple[str, str]]:    
    # Generates a mapping of (original_name, new_name).

    total_files = len(files)
    if total_files == 0:
        return []

    # Calculate padding width
    padding = max(2, len(str(total_files))) # 100 files -> "100" -> 3 0s for the padding 
    
    mapping = []
    
    for index, file_path in enumerate(files, start=1):
        original_name = file_path.name
        extension = file_path.suffix
        new_name = f"{general_title} - {str(index).zfill(padding)}{extension}"
        mapping.append((original_name, new_name))
    return mapping

def perform_rename(folder: Path, mapping: list[tuple[str, str]]):
    # Renames the files in the folder based on the mapping.
    
    for old_name, new_name in mapping:
        old_path = folder / old_name
        new_path = folder / new_name
        
        # Skip if name hasn't changed
        if old_path == new_path:
            continue
            
        try:
            old_path.replace(new_path)
        except OSError as e:
            print(f"Error renaming {old_name} -> {new_name}: {e}")

def perform_restore(folder: Path, json_path: Path):
    # Restores filenames based on the history log.
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading history file: {e}")
        return

    renames = data.get("renames", [])
    if not renames:
        print("No rename history found in this file.")
        return

    print(f"Restoring {len(renames)} files...")
    
    success_count = 0
    fail_count = 0

    for item in renames:
        current_name = item["New Name"]
        original_name = item["Prev Name"]
        
        current_path = folder / current_name
        original_path = folder / original_name
        
        if not current_path.exists():
            print(f"Skipping: {current_name} (File not found)")
            fail_count += 1
            continue
            
        try:
            current_path.replace(original_path)
            success_count += 1
        except OSError as e:
            print(f"Error restoring {current_name} -> {original_name}: {e}")
            fail_count += 1
            
    print(f"\nRestore complete. Restored: {success_count}, Failed: {fail_count}")
