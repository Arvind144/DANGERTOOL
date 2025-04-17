import os
import shutil
import json
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

CONFIG_FILE = r"/storage/emulated/0/FILES_OBB/HEX AND STRING SEARCH/directory_config.json"
DEFAULTS_FILE = r"/storage/emulated/0/FILES_OBB/HEX AND STRING SEARCH/defaults.txt"  # using a plain text file for input directories

# ============================
# Defaults Text Handling
# ============================
def load_default_inputs():
    """Load the predefined input directories from defaults.txt."""
    if os.path.exists(DEFAULTS_FILE):
        with open(DEFAULTS_FILE, 'r', encoding="utf-8") as f:
            # Each non-empty line is a directory
            return [line.strip() for line in f if line.strip()]
    return []

def save_default_inputs(inputs_list):
    """Save the predefined input directories to defaults.txt."""
    with open(DEFAULTS_FILE, 'w', encoding="utf-8") as f:
        f.write("\n".join(inputs_list))

# ============================
# Config Handling for Output Folder
# ============================
def load_saved_folders():
    """
    Load the saved output folder from directory_config.json.
    If the file does not exist, is empty, or is malformed, return None.
    """
    if os.path.exists(CONFIG_FILE) and os.stat(CONFIG_FILE).st_size != 0:
        try:
            with open(CONFIG_FILE, 'r', encoding="utf-8") as config:
                data = json.load(config)
                return data.get("output_folder", None)
        except json.JSONDecodeError:
            return None
    return None

def save_folder_paths(output_folder):
    """Save the output folder to the config file."""
    with open(CONFIG_FILE, 'w', encoding="utf-8") as config:
        json.dump({"output_folder": output_folder}, config)

# ============================
# Utility Functions
# ============================
def clean_hex_input(hex_value):
    """Remove spaces from hex input and validate it."""
    hex_value = hex_value.replace(" ", "").lower()  # Remove spaces and convert to lowercase
    if all(c in "0123456789abcdef" for c in hex_value):
        return hex_value
    else:
        raise ValueError("❌ Invalid hex input. Only hexadecimal characters (0-9, a-f) are allowed.")

def create_search_output_folder(search_input, output_folder):
    """
    Create a new subfolder in the output directory for the given search input.
    The search_input is truncated to a maximum of 15 characters.
    If the folder exists, append a serial number.
    """
    # Sanitize search_input for folder name (remove spaces, replace with underscore) and truncate to 15 characters
    folder_base = search_input.strip().replace(" ", "_")[:15]
    base_path = os.path.join(output_folder, folder_base)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        return base_path
    else:
        i = 1
        new_folder = f"{base_path}_{i}"
        while os.path.exists(new_folder):
            i += 1
            new_folder = f"{base_path}_{i}"
        os.makedirs(new_folder)
        return new_folder

# ============================
# Search Functions
# ============================
def search_string_in_files(string_value, folder_path, main_output_folder, search_output_folder):
    """
    Search all files in folder_path for a decoded string.
    Matching files are copied to search_output_folder.
    Log results to the global results.txt in main_output_folder and print them.
    """
    results = []
    log_file_path = os.path.join(main_output_folder, "results.txt")
    header = f"🔎 Searching for string: {string_value} 🚀\n"
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(header)
    print(Fore.CYAN + header.strip() + Style.RESET_ALL)

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        data = file.read()
                        decoded_text = data.decode(errors="ignore")
                        if string_value in decoded_text:
                            results.append(file_path)
                            shutil.copy(file_path, search_output_folder)
                            position = decoded_text.find(string_value)
                            message = f"📄 Match found in: {os.path.basename(file_path)} at position: {position} 🎉\n"
                            with open(log_file_path, "a", encoding="utf-8") as log_file:
                                log_file.write(message)
                            print(Fore.GREEN + message.strip() + Style.RESET_ALL)
                except Exception as e:
                    error_msg = f"⚠️ Error processing file {file_path}: {e}\n"
                    with open(log_file_path, "a", encoding="utf-8") as log_file:
                        log_file.write(error_msg)
                    print(Fore.RED + error_msg.strip() + Style.RESET_ALL)
    return results

def search_hex_in_files(hex_values, folder_path, main_output_folder, search_output_folder, mode):
    """
    Search for hex patterns in files.
    
    mode 1: File matches if ANY hex value is found.
    mode 2: File matches only if ALL hex values are found.
    
    Matching files are copied to search_output_folder.
    Results are logged in the main_output_folder's results.txt and printed to the terminal.
    """
    hex_values = [clean_hex_input(hv) for hv in hex_values]
    hex_bytes_list = [bytes.fromhex(hv) for hv in hex_values]
    results = []
    log_file_path = os.path.join(main_output_folder, "results.txt")
    header = f"\n🔍 Searching for hex values: {', '.join(hex_values)} 💥\n"
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(header)
    print(Fore.CYAN + header.strip() + Style.RESET_ALL)
    
    input_folder_abs = os.path.abspath(folder_path)
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        data = file.read()
                        # Determine matches
                        if mode == 1:
                            matches = {}
                            for hex_bytes in hex_bytes_list:
                                count = data.count(hex_bytes)
                                if count > 0:
                                    matches[hex_bytes.hex()] = count
                        elif mode == 2:
                            if all(data.count(hex_bytes) > 0 for hex_bytes in hex_bytes_list):
                                matches = {hex_bytes.hex(): data.count(hex_bytes) for hex_bytes in hex_bytes_list}
                            else:
                                matches = {}
                        if matches:
                            results.append({"file": file_path, "matches": matches})
                            shutil.copy(file_path, search_output_folder)
                            file_dir = os.path.abspath(os.path.dirname(file_path))
                            # Get relative directory (if any)
                            relative_dir = os.path.relpath(file_dir, input_folder_abs)
                            subfolder_line = f"📂 Inside the subfolder: {relative_dir}\n" if relative_dir != "." else ""
                            message = f"📄 Found in: {os.path.basename(file_path)}\n" + subfolder_line
                            for hex_val, count in matches.items():
                                message += f"🔷 Hex: {hex_val}\n"
                                message += f"🧮 Total occurrences: {count}\n"
                            message += "✨ Done! ✨\n\n"
                            with open(log_file_path, "a", encoding="utf-8") as log_file:
                                log_file.write(message)
                            print(Fore.GREEN + message.strip() + Style.RESET_ALL)
                except Exception as e:
                    error_msg = f"⚠️ Error processing file {file_path}: {e}\n"
                    with open(log_file_path, "a", encoding="utf-8") as log_file:
                        log_file.write(error_msg)
                    print(Fore.RED + error_msg.strip() + Style.RESET_ALL)
    return results

# ============================
# Main Function
# ============================
def main():
    run_count = 1
    while True:
        # Header UI
        print(Fore.MAGENTA + "═════════════════════════════════════════════════════════" + Style.RESET_ALL)
        print(Fore.GREEN + "        Hex and String Search Tool 🔎🚀✨" + Style.RESET_ALL)
        print(Fore.MAGENTA + "═════════════════════════════════════════════════════════" + Style.RESET_ALL)
        
        # --- Select Input Directory ---
        default_inputs = load_default_inputs()
        print(Fore.CYAN + "\nAvailable Input Directories:" + Style.RESET_ALL)
        if default_inputs:
            for idx, inp in enumerate(default_inputs, start=1):
                print(Fore.YELLOW + f"{idx}. {inp}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "No predefined input directories found." + Style.RESET_ALL)
        print(Fore.YELLOW + "0. Enter a new input directory" + Style.RESET_ALL)
        
        try:
            choice = int(input(Fore.YELLOW + "Select an input directory by number: " + Style.RESET_ALL).strip())
        except ValueError:
            print(Fore.RED + "❌ Invalid choice. Exiting." + Style.RESET_ALL)
            return
        
        if choice == 0:
            new_input = input(Fore.YELLOW + "Enter the full path to the new input directory: " + Style.RESET_ALL).strip()
            if not os.path.isdir(new_input):
                print(Fore.RED + "❌ Invalid directory. Exiting." + Style.RESET_ALL)
                return
            default_inputs.append(new_input)
            save_default_inputs(default_inputs)
            input_folder = new_input
        elif 1 <= choice <= len(default_inputs):
            input_folder = default_inputs[choice - 1]
        else:
            print(Fore.RED + "❌ Invalid choice. Exiting." + Style.RESET_ALL)
            return
    
        # --- Get Output Folder (ask only once) ---
        saved_output_folder = load_saved_folders()
        if saved_output_folder:
            print(Fore.YELLOW + f"\n💾 Saved output folder: {saved_output_folder}" + Style.RESET_ALL)
            use_saved = input(Fore.YELLOW + "Do you want to use this folder? (y/n): " + Style.RESET_ALL).strip().lower()
            if use_saved == "y":
                output_folder = saved_output_folder
            else:
                output_folder = input(Fore.YELLOW + "Enter the path to the output folder: " + Style.RESET_ALL).strip()
        else:
            output_folder = input(Fore.YELLOW + "Enter the path to the output folder: " + Style.RESET_ALL).strip()
        if not os.path.isdir(output_folder):
            print(Fore.RED + "❌ Invalid output folder. Exiting." + Style.RESET_ALL)
            return
        save_folder_paths(output_folder)
    
        # Ensure a single results.txt in the main output folder
        results_log = os.path.join(output_folder, "results.txt")
        if not os.path.exists(results_log):
            with open(results_log, "w", encoding="utf-8") as f:
                f.write("📜 Search Results Log\n\n")
    
        # --- Select Search Option ---
        print(Fore.CYAN + "\nSelect an option:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. Search for a single hex value in files" + Style.RESET_ALL)
        print(Fore.CYAN + "2. Search for multiple hex values (any match) in files" + Style.RESET_ALL)
        print(Fore.CYAN + "3. Search for multiple hex values (all match in one file) in files" + Style.RESET_ALL)
        print(Fore.CYAN + "4. Search for a string in files" + Style.RESET_ALL)
        option = input(Fore.YELLOW + "Enter your choice (1, 2, 3, or 4): " + Style.RESET_ALL).strip()
    
        # --- Determine search term, log header, and create a new search output folder ---
        if option == "1":
            hex_value = input(Fore.YELLOW + "Enter the hex value to search for (e.g., 'd837af41'): " + Style.RESET_ALL).strip()
            search_term = clean_hex_input(hex_value)
            # Log custom header
            with open(results_log, "a", encoding="utf-8") as f:
                f.write(f"\n{'-'*20} SEARCH RESULT {run_count} FOR VALUE: {search_term} {'-'*20}\n\n")
            search_output_folder = create_search_output_folder(search_term, output_folder)
            search_hex_in_files([hex_value], input_folder, output_folder, search_output_folder, mode=1)
        elif option == "2":
            hex_values = input(Fore.YELLOW + "Enter multiple hex values separated by commas (e.g., 'd837af41, aa55bb66'): " + Style.RESET_ALL).strip().split(',')
            search_term = "_".join([clean_hex_input(hv) for hv in hex_values])
            with open(results_log, "a", encoding="utf-8") as f:
                f.write(f"\n{'-'*20} SEARCH RESULT {run_count} FOR VALUE: {search_term} {'-'*20}\n\n")
            search_output_folder = create_search_output_folder(search_term, output_folder)
            search_hex_in_files(hex_values, input_folder, output_folder, search_output_folder, mode=1)
        elif option == "3":
            hex_values = input(Fore.YELLOW + "Enter multiple hex values separated by commas (e.g., 'd837af41, aa55bb66'): " + Style.RESET_ALL).strip().split(',')
            search_term = "_".join([clean_hex_input(hv) for hv in hex_values])
            with open(results_log, "a", encoding="utf-8") as f:
                f.write(f"\n{'-'*20} SEARCH RESULT {run_count} FOR VALUE: {search_term} {'-'*20}\n\n")
            search_output_folder = create_search_output_folder(search_term, output_folder)
            search_hex_in_files(hex_values, input_folder, output_folder, search_output_folder, mode=2)
        elif option == "4":
            string_value = input(Fore.YELLOW + "Enter the string to search for: " + Style.RESET_ALL).strip()
            search_term = string_value.strip().replace(" ", "_")
            with open(results_log, "a", encoding="utf-8") as f:
                f.write(f"\n{'-'*20} SEARCH RESULT {run_count} FOR VALUE: {search_term} {'-'*20}\n\n")
            search_output_folder = create_search_output_folder(search_term, output_folder)
            search_string_in_files(string_value, input_folder, output_folder, search_output_folder)
        else:
            print(Fore.RED + "❌ Invalid choice. Exiting." + Style.RESET_ALL)
            return
    
        run_count += 1  # increment run counter after a successful search run
    
        # --- Ask the user if they want to perform another search ---    
        repeat = input(Fore.YELLOW + "\nDo you want to search for more? (y/n): " + Style.RESET_ALL).strip().lower()
        if repeat != "y":
            print(Fore.YELLOW + "Exiting the search tool. Goodbye!" + Style.RESET_ALL)
            break
        print("\n" + "="*60 + "\n")  # Visual separator before restarting the process
    
if __name__ == "__main__":
    main()
