#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time

console = Console()

# ------------------------------------------------------------------------
# 1. Define your directories
# ------------------------------------------------------------------------
CAR_SOUND_DIR = r"/storage/emulated/0/FILES_OBB/CAR SOUND"
REPACK_DIR    = r"/storage/emulated/0/DANGER/UNPACK/game_patch_3.7.0.19759/repack"

# Name of the single file inside CAR_SOUND_DIR (adjust as needed)
FILE_NAME = None  # or "somefile.obb"

def copy_file_to_repack():
    """
    Copies the single file from CAR_SOUND_DIR to REPACK_DIR.
    If FILE_NAME is not specified, it will automatically pick the first file it finds.
    """
    # Make sure REPACK_DIR exists
    Path(REPACK_DIR).mkdir(parents=True, exist_ok=True)

    source_dir = Path(CAR_SOUND_DIR)
    if FILE_NAME is None:
        # Grab the first file in the directory
        all_files = list(source_dir.iterdir())
        if not all_files:
            console.print("[bold red]No files found in CAR SOUND directory![/bold red]")
            return None
        source_file = all_files[0]
    else:
        source_file = source_dir / FILE_NAME

    # Destination
    dest_file = Path(REPACK_DIR) / source_file.name

    console.print(Panel(f"Copying [cyan]{source_file.name}[/cyan] to REPACK folder...", title="Copying", expand=False))
    shutil.copy2(source_file, dest_file)
    console.print(Panel(f"[green]Copied successfully![/green]", title="Success", expand=False))
    return dest_file


def read_pairs_from_input():
    """
    Reads multiple lines of input from the user in the format: ID1,ID2
    Ends when user types 'q' or 'Q'.
    Returns a list of (ID1, ID2) tuples.
    """
    pairs = []
    console.print(Panel("Enter pairs of IDs (ID1,ID2). Type 'q' to finish.", title="Input", expand=False))
    while True:
        line = console.input("> ")
        line = line.strip()
        if line.lower() == 'q':
            break
        if ',' in line:
            # Split by comma
            parts = line.split(',')
            if len(parts) == 2:
                ID1, ID2 = parts[0].strip(), parts[1].strip()
                pairs.append((ID1, ID2))
            else:
                console.print("[red]Invalid format. Please enter in format: ID1,ID2[/red]")
        else:
            console.print("[red]Invalid format. Please enter in format: ID1,ID2 or 'q' to quit.[/red]")
    return pairs


def find_long_hex_offset(file_bytes, id_str):
    """
    Finds the offset of the 'long hex' region corresponding to the given ID.
    The ID is ASCII-encoded with a null terminator (8 bytes total),
    and the 'long hex' is defined as 12 bytes starting from that offset.

    Returns (offset, long_hex_bytes).
    If not found, returns (None, None).
    """
    # ID in ASCII plus null terminator
    id_bytes = id_str.encode('ascii') + b'\x00'
    offset = file_bytes.find(id_bytes)
    if offset == -1:
        return None, None

    # We assume we want 12 bytes total from this offset:
    #   8 bytes (the ID + \x00) + 4 extra bytes
    end_offset = offset + 12
    if end_offset > len(file_bytes):
        return None, None  # Not enough data

    long_hex_bytes = file_bytes[offset:end_offset]
    return offset, long_hex_bytes


def replace_long_hex(file_bytes, id_str, new_long_hex):
    """
    Finds the offset of the 'long hex' for id_str in file_bytes,
    then replaces those 12 bytes with new_long_hex.

    Returns the old long hex if successful, or None if not found.
    """
    offset, old_long_hex = find_long_hex_offset(file_bytes, id_str)
    if offset is None:
        return None
    file_bytes[offset:offset+12] = new_long_hex
    return old_long_hex


def hex_to_str(byte_data):
    """Convert a bytes object to a spaced-hex string for logging."""
    return " ".join(f"{b:02X}" for b in byte_data)


def main():
    console.print(Panel("[bold green]Skin Modding Script[/bold green]", title="Welcome", expand=False))

    # 1) Copy file
    dest_file = copy_file_to_repack()
    if not dest_file:
        console.print("[red]Aborting because file copy failed or no source file was found.[/red]")
        return

    # 2) Read pairs of IDs from user
    pairs = read_pairs_from_input()
    if not pairs:
        console.print("[red]No pairs entered. Exiting.[/red]")
        return
    
    # 3) Open the file in memory
    console.print(Panel(f"Reading file [cyan]{dest_file.name}[/cyan] in binary...", title="Reading", expand=False))
    with open(dest_file, "rb") as f:
        file_bytes = bytearray(f.read())

    # 4) Prepare a table to log changes
    table = Table(title="Hex Replacement Log", show_lines=True)
    table.add_column("Pair (ID1, ID2)", justify="left", style="bold cyan")
    table.add_column("Old LongHex (ID1)", justify="left", style="yellow")
    table.add_column("New LongHex (from ID2)", justify="left", style="green")

    # 5) Process each pair
    for (ID1, ID2) in pairs:
        # Get the 'long hex' from ID2
        offset_2, long_hex_2 = find_long_hex_offset(file_bytes, ID2)
        if offset_2 is None:
            console.print(f"[red]Could not find ID2 '{ID2}' in file. Skipping pair ({ID1}, {ID2}).[/red]")
            continue

        # Replace the 'long hex' of ID1 with that from ID2
        old_long_hex_1 = replace_long_hex(file_bytes, ID1, long_hex_2)
        if old_long_hex_1 is None:
            console.print(f"[red]Could not find ID1 '{ID1}' in file. Skipping pair ({ID1}, {ID2}).[/red]")
            continue

        # Log in table
        table.add_row(
            f"{ID1}, {ID2}",
            hex_to_str(old_long_hex_1),
            hex_to_str(long_hex_2),
        )

    # 6) Write changes back to the file
    with open(dest_file, "wb") as f:
        f.write(file_bytes)

    # 7) Display the log table
    console.print(Panel("[green]Processing complete![/green] Here is the log of all changes:", title="Success", expand=False))
    console.print(table)
    console.print("[bold green]All done![/bold green]")


if __name__ == "__main__":
    main()
