import os
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress

console = Console()

def dynamic_extract_index(data, marker_pos):
    start = marker_pos - 11
    if start < 1:
        return None
    for pos in range(start, 0, -1):
        if data[pos] != 0:
            if pos - 1 < 0:
                return None
            extracted = data[pos-1:pos+1]
            if extracted[0] == 0:
                extracted = extracted[1:2] + extracted[0:1]
            return (pos - 1, extracted)
    return None

def search_hex_occurrences(file_path, hex_bytes):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except Exception as e:
        console.print(f"❌ [red]Error reading {file_path}: {e}[/]")
        return []
    
    occurrences = []
    start = 0
    while True:
        pos = data.find(hex_bytes, start)
        if pos == -1:
            break
        marker_pos = data.rfind(b'\xff\xff\xff', 0, pos)
        if marker_pos != -1:
            res = dynamic_extract_index(data, marker_pos)
            if res:
                start_pos, index_bytes = res
                occurrences.append((start_pos, index_bytes))
        start = pos + 1
    return occurrences

def find_hex_index_any_file(hex_bytes, exclude_files):
    for fname in os.listdir("."):
        if fname in exclude_files or not os.path.isfile(fname):
            continue
        occurrences = search_hex_occurrences(fname, hex_bytes)
        if occurrences:
            return occurrences[0][1]
    return None

def main():
    # Setup directories
    emote_dir = r"/storage/emulated/0/FILES_OBB/EMOTE"
    repack_dir = r"/storage/emulated/0/FILES_OBB/REPACK_OBB/REPACK"
    
    # Copy files from EMOTE to REPACK
    if os.path.exists(repack_dir):
        shutil.rmtree(repack_dir)
    shutil.copytree(emote_dir, repack_dir)
    os.chdir(repack_dir)
    
    # Create EMOTE TOOL banner
    banner = Panel(
        Text(" EMOTE TOOL ", style="bold white on purple", justify="center"),
        title=":rocket: Skin Modding Utility",
        subtitle="Made with :heart: by Chetan",
        border_style="magenta",
        expand=False
    )
    console.print(banner, justify="center")
    
    console.print(f"[green]📂 Files copied to:[/] [cyan]{repack_dir}[/]")

    # Input pairs
    console.print("\n[yellow]Paste all hex pairs (hex1,hex2) below. Enter 'q' on a new line to process:[/]")
    pairs = []
    while True:
        line = input("  ➤ ").strip()
        if line.lower() == 'q':
            break
        if not line:
            continue
        parts = line.split(',')
        if len(parts) == 2:
            hex1, hex2 = parts[0].strip(), parts[1].strip()
            if len(hex1) % 2 == 0 and len(hex2) % 2 == 0:
                pairs.append((hex1, hex2))
    
    if not pairs:
        console.print("\n[yellow]⚠️ No valid pairs entered. Exiting...[/]")
        return

    # Processing
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Processing pairs...", total=len(pairs))
        changelog = []

        for hex1, hex2 in pairs:
            progress.update(task, description=f"[cyan]Processing {hex1} → {hex2}[/]")
            
            try:
                hex1_bytes = bytes.fromhex(hex1)
                hex2_bytes = bytes.fromhex(hex2)
            except ValueError as e:
                console.print(f"  ⚠️ [red]Error parsing hex: {e}[/]")
                continue

            # Find all hex1 occurrences
            hex1_occurrences = []
            for fname in os.listdir("."):
                if fname.endswith(".py") or fname == "changelog.txt" or not os.path.isfile(fname):
                    continue
                occurrences = search_hex_occurrences(fname, hex1_bytes)
                for pos, idx in occurrences:
                    hex1_occurrences.append((fname, pos, idx))

            if not hex1_occurrences:
                continue

            # Find hex2's index
            hex2_idx = find_hex_index_any_file(hex2_bytes, {"changelog.txt"})
            if not hex2_idx:
                continue

            # Replace occurrences
            for fname, pos, old_idx in hex1_occurrences:
                if not os.access(fname, os.W_OK):
                    continue
                try:
                    with open(fname, "rb+") as f:
                        f.seek(pos)
                        f.write(hex2_idx)
                    changelog.append(
                        f"In {fname}: Replaced [cyan]{hex1}[/] (index: {old_idx.hex().upper()}) with [magenta]{hex2}[/]'s index ({hex2_idx.hex().upper()}) at position {pos}"
                    )
                except Exception as e:
                    console.print(f"  ⚠️ Error modifying {fname}: {e}")

            progress.advance(task)

    # Create changelog
    if changelog:
        console.print("\n✅ [green]Modding complete![/]")
        changelog_path = os.path.join(repack_dir, "changelog.txt")
        
        # Create styled changelog table
        table = Table(title=":page_facing_up: Modification Log", show_lines=True)
        table.add_column("File", style="cyan")
        table.add_column("Details", style="magenta")
        
        for entry in changelog:
            parts = entry.split(": ", 1)
            table.add_row(parts[0], parts[1])
        
        console.print(table)
        
        with open(changelog_path, "w", encoding="utf-8") as f:
            for entry in changelog:
                f.write(entry + "\n")
        console.print(f"📝 Changelog saved to: [cyan]{changelog_path}[/]")
    else:
        console.print("\n:no_entry_sign: No modifications were made")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Process interrupted by user[/]")
