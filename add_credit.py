import os
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED
from rich.prompt import Prompt

# Permanent paths
SOURCE_DIR = "/storage/emulated/0/FILES_OBB/CREDIT_MOD/dats/"
OUTPUT_DIR = "/storage/emulated/0/FILES_OBB/REPACK_OBB/REPACK/"

# Console for rich output
console = Console()

def read_binary_file(file_path):
    """Reads the content of a binary file."""
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File '{file_path}' not found.")
        return None
    except Exception as e:
        console.print(f"[bold red]An error occurred while reading the file:[/bold red] {e}")
        return None

def write_binary_file(file_path, data):
    """Writes data to a binary file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the output directory exists
        with open(file_path, 'wb') as file:
            file.write(data)
        console.print(f"[bold green]Modified file saved to:[/bold green] {file_path}")
    except Exception as e:
        console.print(f"[bold red]An error occurred while writing to the file:[/bold red] {e}")

def replace_string_in_binary(file_path, old_text, new_text):
    """Replaces a string in a binary file."""
    # Read the binary file
    binary_data = read_binary_file(file_path)
    if binary_data is None:
        return False

    # Convert the strings to bytes
    old_bytes = old_text.encode('utf-8')
    new_bytes = new_text.encode('utf-8')

    # Check if the old text exists in the binary data
    if old_bytes not in binary_data:
        return False

    # Replace the old text with the new text
    new_binary_data = binary_data.replace(old_bytes, new_bytes.ljust(len(old_bytes), b'\x00'))

    # Write the updated binary data to the output directory
    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    write_binary_file(output_file_path, new_binary_data)
    return True

def display_menu():
    """Displays the main menu using a rich table."""
    table = Table(title="DANGER MOD TOOL", box=ROUNDED, style="bold white on blue")
    table.add_column("Option", style="bold green")
    table.add_column("Description", style="cyan")

    table.add_row("1", "MOD CREDIT")
    table.add_row("2", "QUIT")

    console.print(table)

def main():
    while True:
        display_menu()

        choice = Prompt.ask("[bold yellow]Enter your choice (1 or 2):[/bold yellow]").strip()

        if choice == '1':
            text_to_find = Prompt.ask("[bold yellow]Enter the text to find 🔍:[/bold yellow]").strip()
            if not text_to_find:
                console.print("[bold red]Error:[/bold red] Text to find cannot be empty. Please try again.")
                continue

            try:
                dat_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.dat')]
                if not dat_files:
                    console.print("[bold red]No .dat files found in the source directory.[/bold red]")
                    continue

                found = False
                for dat_file in dat_files:
                    file_path = os.path.join(SOURCE_DIR, dat_file)
                    binary_data = read_binary_file(file_path)

                    if binary_data and text_to_find.encode('utf-8') in binary_data:
                        console.print(f"[bold green]Text '{text_to_find}' FOUND[/bold green] in file: {dat_file}")
                        found = True

                        while True:
                            new_text = Prompt.ask("[bold yellow]Enter your new credit text 🔍:[/bold yellow]").strip()
                            if not new_text:
                                console.print("[bold red]Error:[/bold red] New text cannot be empty. Please try again.")
                                continue

                            success = replace_string_in_binary(file_path, text_to_find, new_text)
                            if success:
                                console.print("[bold green]CREDIT SUCCESSFULLY ADDED 💀[/bold green]")
                                break
                            else:
                                console.print("[bold red]An unexpected error occurred while replacing the text. Please try again.[/bold red]")

                if not found:
                    console.print(f"[bold red]Text '{text_to_find}' was NOT FOUND[/bold red] in any .dat file.")

            except Exception as e:
                console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")

        elif choice == '2' or choice.lower() == 'q':  # Added 'q' as a quit option
            console.print("[bold blue]Exiting the program. Goodbye![/bold blue]")
            break

        else:
            console.print("[bold red]Invalid choice. Please enter 1 or 2.[/bold red]")

if __name__ == "__main__":
    main()
