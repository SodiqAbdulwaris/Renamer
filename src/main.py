import sys
import time
from pathlib import Path
from rich.prompt import Prompt

sys.path.append(str(Path(__file__).parent))

from renamer import get_files, generate_rename_mapping, perform_rename, perform_restore
from utils import validate_path, save_history
from ui import display_welcome, display_preview, display_success, console

def main():
    display_welcome()

    # 1. Get Folder Path
    while True:
        folder_str = Prompt.ask("[bold]Enter the folder path[/bold]")
        try:
            folder_path = validate_path(folder_str)
            break
        except (FileNotFoundError, NotADirectoryError) as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    # 1.5 Select Mode
    mode = Prompt.ask("[bold]Select Mode[/bold]", choices=["Rename", "Undo/Restore"], default="Rename")

    if mode in ["Undo/Restore", "Undo", "Restore"]:
        # Undo Flow

        # Look for json files
        json_files = list(folder_path.glob("*.json"))
        if not json_files:
            console.print("[bold red]No history JSON files found in this folder.[/bold red]")
            return

        console.print("[bold]Available History Files:[/bold]")
        for i, f in enumerate(json_files, 1):
            console.print(f"{i}. {f.name}")
        
        choice = Prompt.ask("Select a file number", choices=[str(i) for i in range(1, len(json_files)+1)])
        selected_json = json_files[int(choice)-1]
        
        perform_restore(folder_path, selected_json)
        return

    # Rename Flow (Default)
    # 2. Get Files
    files = get_files(folder_path)
    if not files:
        console.print("[bold red]No files found in the directory (or all ignored).[/bold red]")
        return
    
    console.print(f"[green]Found {len(files)} files to rename.[/green]")

    # 3. Get General Title
    general_title = Prompt.ask("[bold]Enter the general title[/bold] (e.g. 'Networking 101')")
    
    # 4. Generate Mapping
    mapping = generate_rename_mapping(files, general_title)
    
    # 5. Preview
    display_preview(mapping)
    
    # 6. Proceed automatically (with a safety pause)
    console.print("\n[bold yellow]Proceeding with rename in 3 seconds... (Press Ctrl+C to cancel)[/bold yellow]")
    try:
        for i in range(3, 0, -1):
            console.print(f"{i}...")
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold red]Operation cancelled by user.[/bold red]")
        sys.exit(0)

    # 7. Rename
    perform_rename(folder_path, mapping)
    
    # 8. Save History
    json_path = save_history(folder_path, mapping, general_title)
    
    # 9. Success
    display_success(str(json_path))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
        sys.exit(0)
