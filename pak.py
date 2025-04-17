#!/data/data/com.termux/files/usr/bin/python3

import requests, sys

try:
    user_id = input("ENTER YOUR USER ID: ").strip()
    approved_ids = requests.get("https://raw.githubusercontent.com/Arvind144/telebot/main/approved_ids.txt").text.splitlines()
    if user_id not in approved_ids:
        print("Access Denied: Tu approved user nahi hai.")
        sys.exit()
except Exception as e:
    print("Approval check failed:", e)
    sys.exit()

import os
import shutil
import subprocess
from pathlib import Path
import time
import random

# Define color codes for terminal output
class Colors:
    NOCOLOR = '\033[0m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    ORANGE = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    LIGHTGRAY = '\033[0;37m'
    DARKGRAY = '\033[1;30m'
    LIGHTRED = '\033[1;31m'
    LIGHTGREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    LIGHTBLUE = '\033[1;34m'
    LIGHTPURPLE = '\033[1;35m'
    LIGHTCYAN = '\033[1;36m'
    WHITE = '\033[1;37m'

# --- (baaki ka tera pura original code yahin se chalu hai, bilkul waise hi) ---


def print_new_banner():
    """Print the banner using toilet, figlet, and pv for a dynamic effect."""
    # Clear the screen
    os.system('clear')

    # Use toilet, figlet, and pv to display the banner
    os.system('toilet -f term -F border --gay "   𝗣𝗔𝗞𝗧𝗢𝗢𝗟  " | pv -qL 9500')
    os.system('toilet -f term --gay "   𝗢𝗪𝗡𝗘𝗥 : @PhantomSkins. " | pv -qL 9500')
    os.system('toilet -f term --gay "   𝗨𝗡𝗣𝗔𝗖𝗞 𝗚𝗔𝗠𝗘_𝗣𝗔𝗧𝗖𝗛 𝗕𝗢𝗧𝗛 𝗖𝗛𝗨𝗡𝗞/𝗡𝗢𝗡_𝗖𝗛𝗨𝗡𝗞 " | pv -qL 9500')        
    os.system('toilet -f term -F border --gay "   𝗖𝗛𝗢𝗢𝗦𝗘 𝗢𝗣𝗧𝗜𝗢𝗡 😉 " | pv -qL 9500')

# Define paths
dark_pak_dir = Path("/storage/emulated/0/DANGER/UNPACK_REPACK")
paks_dir = dark_pak_dir / "PAKS"
unpack_repack_dir = dark_pak_dir / "UNPACK"

# Ensure directories exist
paks_dir.mkdir(parents=True, exist_ok=True)
unpack_repack_dir.mkdir(parents=True, exist_ok=True)

# Define paths for DARKSIDE executable (Termux home path)
executable_script = Path.home() / "DANGER" / "dist"

def unpakgamepach1(selected_file, chunk_mode=False):
    """Unpack the selected .pak file and create repack and result folders."""
    pak_name = selected_file.stem  # Get the name of the .pak file without extension
    unpack_dir = unpack_repack_dir / pak_name / "unpack"
    repack_dir = unpack_repack_dir / pak_name / "repack"
    result_dir = unpack_repack_dir / pak_name / "result"

    # Create necessary directories
    unpack_dir.mkdir(parents=True, exist_ok=True)
    repack_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    # Define a blocklist of files to skip during extraction
    BLOCKLIST = [
        "0014e550.dat",
        "004e0030.dat",
        "004ef820.dat",
        "004b9ea0.125",
        "004d0860.dat",
        "004c1440.dat",
        "0023c320.dat",
        "001e7ef0.uasset",
        "00133910.lua",
        "000f9090.lua",
        "05ba510.uasset",       
    ]

    print(f"{Colors.CYAN}Unpacking {selected_file.name} to {unpack_dir}...{Colors.NOCOLOR}")

    # Run the unpacking process
    if chunk_mode:
        # Use chunk mode with -c 65536
        subprocess.run([str(executable_script), "-a", "-c", "65536", str(selected_file), str(unpack_dir)])
    else:
        # Use non-chunk mode
        subprocess.run([str(executable_script), "-a", str(selected_file), str(unpack_dir)])

    # Remove blocked files from the unpack directory
    for file in unpack_dir.glob("*"):
        if file.name in BLOCKLIST:
            file.unlink()  # Delete the blocked file

    print(f"{Colors.GREEN}Unpacking completed! Files are saved in {unpack_dir}.{Colors.NOCOLOR}")
    time.sleep(5)  # Wait for 5 seconds before returning to the main menu

def repakgamepach1(selected_file, chunk_mode=False):
    """Repack edited files while keeping the original .pak file unchanged."""
    pak_name = selected_file.stem
    repack_dir = unpack_repack_dir / pak_name / "repack"
    result_dir = unpack_repack_dir / pak_name / "result"

    if not repack_dir.exists():
        print(f"{Colors.RED}No edited files found in {repack_dir}.{Colors.NOCOLOR}")
        return

    print(f"{Colors.CYAN}Repacking {selected_file.name} while keeping the original file safe...{Colors.NOCOLOR}")

    # Ensure result directory exists
    result_dir.mkdir(parents=True, exist_ok=True)

    # Paths
    original_pak_file = paks_dir / selected_file.name
    copied_pak_file = repack_dir / selected_file.name
    result_pak_file = result_dir / selected_file.name

    # Step 1: Copy original .pak to repack folder
    shutil.copy2(original_pak_file, copied_pak_file)
    print(f"{Colors.LIGHTBLUE}Copied {selected_file.name} to repack folder.{Colors.NOCOLOR}")

    # Step 2: Run repacking using the copied file in repack/
    if chunk_mode:
        # Use chunk mode with -c 65536
        subprocess.run([str(executable_script), "-a", "-r", "-c", "65536", str(copied_pak_file), str(repack_dir)])
    else:
        # Use non-chunk mode
        subprocess.run([str(executable_script), "-a", "-r", str(copied_pak_file), str(repack_dir)])

    # Step 3: Move repacked .pak to result folder
    if copied_pak_file.exists():
        shutil.move(copied_pak_file, result_pak_file)
        print(f"{Colors.GREEN}Repacking completed! Modified .pak file saved in {result_pak_file}.{Colors.NOCOLOR}")
    else:
        print(f"{Colors.RED}Repacking failed! No file was created in {result_dir}.{Colors.NOCOLOR}")
        return

    # Step 4: Delete copied .pak from repack folder
    if copied_pak_file.exists():
        copied_pak_file.unlink()
        print(f"{Colors.ORANGE}Temporary file deleted from repack folder.{Colors.NOCOLOR}")

    time.sleep(5)  # Wait for 5 seconds before returning to the main menu

def unpak_all_paks(chunk_mode=False):
    """Unpack all .pak files in the PAKS directory."""
    pak_files = list(paks_dir.glob("*.pak"))
    if not pak_files:
        print(f"{Colors.RED}No .pak files found in {paks_dir}.{Colors.NOCOLOR}")
        return

    print(f"{Colors.CYAN}Unpacking all .pak files in {paks_dir}...{Colors.NOCOLOR}")
    for selected_file in pak_files:
        unpakgamepach1(selected_file, chunk_mode)
    print(f"{Colors.GREEN}All .pak files have been unpacked!{Colors.NOCOLOR}")
    time.sleep(5)  # Wait for 5 seconds before returning to the main menu

def unpakgamepach(chunk_mode=False):
    """Prompt user to select a .pak file to unpack."""
    pak_files = list(paks_dir.glob("*.pak"))
    if not pak_files:
        print(f"{Colors.RED}No .pak files found in {paks_dir}.{Colors.NOCOLOR}")
        return

    print(f"{Colors.CYAN}Available .pak files:{Colors.BLUE}")
    for i, file in enumerate(pak_files):
        print(f"{i + 1}: {file.name}")

    try:
        choice = int(input(f"{Colors.YELLOW}Please select a file to unpack: {Colors.NOCOLOR}")) - 1
        if 0 <= choice < len(pak_files):
            selected_file = pak_files[choice]
            unpakgamepach1(selected_file, chunk_mode)
        else:
            print(f"{Colors.RED}Invalid selection.{Colors.NOCOLOR}")
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.NOCOLOR}")

def repakgamepach(chunk_mode=False):
    """Prompt user to select a .pak file to repack."""
    pak_files = list(paks_dir.glob("*.pak"))
    if not pak_files:
        print(f"{Colors.RED}No .pak files found in {paks_dir}.{Colors.NOCOLOR}")
        return

    print(f"{Colors.CYAN}Available .pak files:{Colors.NOCOLOR}")
    for i, file in enumerate(pak_files):
        print(f"{i + 1}: {file.name}")

    try:
        choice = int(input(f"{Colors.YELLOW}Please select a file to repack: {Colors.NOCOLOR}")) - 1
        if 0 <= choice < len(pak_files):
            selected_file = pak_files[choice]
            repakgamepach1(selected_file, chunk_mode)
        else:
            print(f"{Colors.RED}Invalid selection.{Colors.NOCOLOR}")
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.NOCOLOR}")

def main_menu(chunk_mode=False):
    """Main loop to provide options to the user."""
    while True:
        print_new_banner()
        # Use toilet for menu options
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟭] 𝗨𝗡𝗣𝗔𝗞"])
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟮] 𝗨𝗡𝗣𝗔𝗞 𝗔𝗟𝗟"])
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟯] 𝗥𝗘𝗣𝗔𝗞"])
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟰] 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗢𝗗𝗘 𝗦𝗘𝗟𝗘𝗖𝗧𝗜𝗢𝗡"])
        choice = input(f"{Colors.YELLOW}PLEASE CHOOSE: {Colors.NOCOLOR}")

        if choice == "1":
            unpakgamepach(chunk_mode)
        elif choice == "2":
            unpak_all_paks(chunk_mode)
        elif choice == "3":
            repakgamepach(chunk_mode)
        elif choice == "4":
            print(f"{Colors.GREEN}Returning to mode selection...{Colors.NOCOLOR}")
            break
        else:
            print(f"{Colors.RED}Invalid option. Try another one.{Colors.PURPLE}")

def main():
    """Main loop to select mode (NON_CHUNK or CHUNK)."""
    while True:
        print_new_banner()
        # Use toilet for mode selection options
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟭] 𝗡𝗢𝗡_𝗖𝗛𝗨𝗡𝗞"])
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟮] 𝗖𝗛𝗨𝗡𝗞"])
        subprocess.run(["toilet", "-f", "term", "--gay", "𝟯] 𝗘𝗫𝗜𝗧"])
        choice = input(f"{Colors.YELLOW}PLEASE CHOOSE: {Colors.NOCOLOR}")

        if choice == "1":
            main_menu(chunk_mode=False)
        elif choice == "2":
            main_menu(chunk_mode=True)
        elif choice == "3":
            print(f"{Colors.GREEN}Exiting...{Colors.NOCOLOR}")
            break
        else:
            print(f"{Colors.RED}Invalid option. Try another one.{Colors.PURPLE}")

if __name__ == "__main__":
    main()