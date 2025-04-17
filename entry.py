import os
import shutil
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

# Configuration
SOURCE_DIR = r"/storage/emulated/0/FILES_OBB/ENTRY EMOTE"
REPACK_DIR = r"/storage/emulated/0/DANGER/UNPACK_REPACK/UNPACK/game_patch_3.7.0.19773/repack/"
FILENAME = "0026e939.dat"  # Replace with actual filename

def copy_file_to_repack():
    source_path = os.path.join(SOURCE_DIR, FILENAME)
    destination_path = os.path.join(REPACK_DIR, FILENAME)
    
    try:
        shutil.copy(source_path, destination_path)
        return True
    except Exception as e:
        print(f"[bold red]❌ Error copying file:[/] {str(e)}")
        return False

def modify_hex_values(file_path, hex_pairs):
    console = Console()
    log_table = Table(title="Modification Log", show_header=True, header_style="bold magenta")
    log_table.add_column("Original Hex", style="cyan")
    log_table.add_column("New Hex", style="green")
    log_table.add_column("Offset", style="yellow")
    log_table.add_column("Status", style="bold")

    try:
        with open(file_path, "rb+") as f:
            content = f.read()
            
            for original_hex, new_hex in hex_pairs:
                original_bytes = bytes.fromhex(original_hex)
                new_bytes = bytes.fromhex(new_hex)
                
                offset = content.find(original_bytes)
                if offset == -1:
                    log_table.add_row(
                        original_hex,
                        new_hex,
                        "[red]Not found[/]",
                        "⚠️  Skipped"
                    )
                    continue
                
                # Perform replacement
                f.seek(offset)
                f.write(new_bytes)
                log_table.add_row(
                    original_hex,
                    new_hex,
                    f"0x{offset:X}",
                    "✅ Success"
                )
                
            console.print(Panel.fit(log_table, title="Modification Results"))
            
    except Exception as e:
        print(f"[bold red]❌ Error modifying file:[/] {str(e)}")

def main():
    console = Console()
    
    # Display header (FIXED THIS SECTION)
    console.print(Align.center(Panel(
        " HEX MODIFICATION TOOL ",
        title="🚀 Skin Modding Assistant",
        subtitle="Made with ❤️ by Chetan",
        border_style="bold blue",
        expand=False  # Moved to correct parameter
    )))
    
    # Copy file first
    if not copy_file_to_repack():
        return

    # Get hex pairs from user
    console.print("\n[bold yellow]Enter hex pairs in format 'original,new' (one per line)[/]")
    console.print("[italic]Type 'q' on a new line to finish input:[/]\n")
    
    hex_pairs = []
    while True:
        user_input = Prompt.ask(
            f"[cyan]{'▶'*(len(hex_pairs)+1)}[/]",
            console=console,
            default=""
        ).strip()
        
        if user_input.lower() == 'q':
            break
            
        if not user_input:
            continue
            
        parts = user_input.split(',')
        if len(parts) != 2:
            console.print(f"[bold red]⚠️  Invalid format:[/] {user_input}")
            continue
            
        hex1, hex2 = parts[0].strip(), parts[1].strip()
        if not all(c in '0123456789abcdefABCDEF' for c in hex1+hex2):
            console.print(f"[bold red]⚠️  Invalid hex:[/] {user_input}")
            continue
            
        hex_pairs.append((hex1, hex2))
        
    # Process modifications
    if hex_pairs:
        modify_hex_values(os.path.join(REPACK_DIR, FILENAME), hex_pairs)
    else:
        console.print("[bold yellow]⚠️  No valid hex pairs entered, no changes made[/]")
    
    # Final message
    console.print("\n[bold green]🎉 All operations completed![/]")
    console.print(f"Modified file saved to: [italic]{REPACK_DIR}[/]")

if __name__ == "__main__":
    main()
