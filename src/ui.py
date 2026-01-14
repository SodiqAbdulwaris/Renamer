from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

def display_welcome():
    rprint("[bold blue]Welcome to the Folder-Based File Renamer![/bold blue]")
    rprint("[italic]Renaming files made easy and safe.[/italic]\n")

def display_preview(mapping: list[tuple[str, str]]):
    # Shows preview of renaming

    table = Table(title="Rename Preview")
    table.add_column("Original Name", style="red")
    table.add_column("New Name", style="green")
    
    # Previews summary of renaming of first 3 files and a summary if there are many files, 
    for i, (old, new) in enumerate(mapping):
        if i >= 3:
            break
        table.add_row(old, new)
    
    if len(mapping) > 3:
        remaining = len(mapping) - 3
        table.add_row(f"... and {remaining} more files", "...")

    console.print(table)
    rprint(f"\n[bold yellow]Total files to rename: {len(mapping)}[/bold yellow]")

def display_success(json_path: str):
    rprint(f"\n[bold green]Success! all files have been renamed.[/bold green]")
    rprint(f"History saved to: [underline]{json_path}[/underline]")
