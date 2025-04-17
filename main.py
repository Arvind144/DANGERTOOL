from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from pyfiglet import figlet_format
import os
import time
import sys
import requests

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    clear()
    splash = figlet_format("DANGER TOOL", font="slant")
    colors = ["bold red", "bold yellow", "bold green", "bold cyan", "bold magenta"]
    for i in range(10):
        color = colors[i % len(colors)]
        clear()
        console.print(splash, style=color, justify="center")
        time.sleep(0.1)
    time.sleep(0.5)

def pulse_loader():
    loader = ["[cyan]*        ", " [cyan] *       ", "  [cyan]  *     ", "   [cyan]   *   ", "    [cyan]    * ", "     [cyan]     *"]
    for _ in range(2):
        for frame in loader:
            console.print(f"\n\n\n\n{frame}", justify="center")
            time.sleep(0.08)
            clear()

def show_logo():
    logo = figlet_format("DANGER MOD", font="big")
    console.print(logo, style="bold red", justify="center")

# Gradient Function for Text
def gradient_text(text, color1="magenta", color2="cyan"):
    mid = len(text) // 2
    first_half = Text(text[:mid], style=color1)
    second_half = Text(text[mid:], style=color2)
    return first_half + second_half

def welcome_typing():
    console.print(
        Panel(
            gradient_text("Welcome to the DANGER MOD TOOL — Your Ultimate Premium CLI Modder!", color1="bold green", color2="bold cyan"),
            style="bold green",
            padding=(1, 4),
            border_style="bright_magenta",
            box=box.ROUNDED
        )
    )
    time.sleep(1.5)

# New function to check if the user's ID is approved
def check_id_approval(user_id):
    approval_link = "https://raw.githubusercontent.com/Arvind144/telebot/main/approved_ids.txt"  # Replace with actual URL or file that contains approved IDs
    try:
        response = requests.get(approval_link)
        approved_ids = response.text.splitlines()  # Assuming each line is an approved ID
        return user_id in approved_ids
    except Exception as e:
        console.print(f"[bold red]Error: Unable to check approval status. {e}[/bold red]")
        return False

def mod_menu():
    user_id = input("\nEnter your User ID: ").strip()  # Input for the user ID

    # Check if the ID is approved before proceeding
    if not check_id_approval(user_id):
        console.print("[bold red]Your ID is not approved. Access blocked.[/bold red]")
        sys.exit()

    while True:
        clear()
        table = Table(title="[bold green]Select Your MOD Option[/bold green]", box=box.ROUNDED, border_style="cyan")
        table.add_column("Option", justify="center", style="bold white")
        table.add_column("Description", justify="left", style="bold yellow")
        table.add_column("Icon", justify="center")

        menu_options = [
            ("1", "MOD LOBBY", "🎮"),
            ("2", "MOD CAR", "🚗"),
            ("3", "MOD SKIN", "👕"),
            ("4", "ADD CREDIT", "💰"),
            ("5", "MOD GUN", "🔫"),
            ("6", "HIT EFFECT (PAK)", "💥"),
            ("7", "MOD KILLMESSAGE (PAK)", "🎯"),
            ("8", "REPAK (OBB ONLY)", "🔄"),
            ("9", "GUN SIZE FIX", "🔧"),
            ("10", "SKIN SIZE FIX", "🔥"),
            ("11", "EMOTE OBB", "🐒"),
            ("12", "ENTRY EMOTE PAK", "💌"),
            ("13", "CAR SOUNDPAK", "🔊"),
            ("14", "PAK UNPACK REPACK", "💕"),
            ("15", "HEX AND STRING SEARCH", "🔎"),
            ("16", "ID , HEX , NAME", "💥"),
            ("X", "ABOUT TOOL", "💲"),
            ("0", "EXIT", "🙋‍♂️")
        ]

        for opt, desc, icon in menu_options:
            table.add_row(opt, desc, icon)

        console.print(table)

        choice = console.input("\n[bold blue]> Select Option:[/bold blue] ").strip().upper()

        for opt, desc, icon in menu_options:
            if choice == opt:
                clear()
                if opt == "0":
                    console.print("\n[bold red]Exiting...[/bold red]")
                    sys.exit()
                elif opt == "X":
                    console.print(Panel("[bold cyan]Created by DANGER - Premium Modding Tool CLI\nAll rights reserved.[/bold cyan]", title="ABOUT", style="magenta"))
                    console.input("\nPress Enter to return to the menu...")
                    continue
                else:
                    file = get_file_from_option(opt)
                    if file:
                        os.system(f"python {file}")
                    continue
        console.print("[red]Invalid option. Try again![/red]")

def get_file_from_option(opt):
    file_map = {
        "1": "mod_lobby.py",
        "2": "mod_car.py",
        "3": "mod_skin.py",
        "4": "add_credit.py",
        "5": "mod_gun.py",
        "6": "hit_effect.py",
        "7": "mod_killmessage.py",
        "8": "repack.sh",
        "9": "sizfixgun.py",
        "10": "sizefixskin.py",
        "11": "emote.py",
        "12": "entry.py",
        "13": "carsound.py",
        "14": "pak.py",
        "15": "srch.py",
        "16": "idnm.py"
    }
    return file_map.get(opt)

if __name__ == "__main__":
    splash_screen()
    pulse_loader()
    clear()
    show_logo()
    welcome_typing()
    mod_menu()
