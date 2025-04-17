import os
import time
import re

# ---------- UTILITY FUNCTIONS ----------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title():
    print("\n⚡ HEX DATA EXTRACTOR ⚡")
    print("══════════════════════════════════════════════")

def typing_effect(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

# ---------- ADVANCED CONVERTER FUNCTION ----------
def advanced_converter():
    while True:
        clear_screen()
        display_title()
        print("\n🔧 ADVANCED DECIMAL-HEX CONVERTER 🔧")
        print("══════════════════════════════════════════════")
        print("\nEnter decimal values (separated by spaces), or 'back' to return:")
        
        try:
            input_values = input("> ").strip().lower()
            if input_values == "back":
                return
            
            if not input_values:
                raise ValueError
            
            decimals = input_values.split()
            
            print("\n══════════════════════════════════════════════")
            print("Conversion Results:")
            print("══════════════════════════════════════════════\n")
            
            for decimal in decimals:
                if not re.match(r'^\d+$', decimal):
                    print(f"❌ Invalid decimal value: {decimal}\n")
                    continue
                
                try:
                    decimal_int = int(decimal)
                    hex_value = format(decimal_int, '08X')
                    
                    # Split into byte pairs and reverse order
                    byte_pairs = [hex_value[i:i+2] for i in range(0, len(hex_value), 2)]
                    reversed_hex = ''.join(byte_pairs[::-1])
                    formatted_hex = ''.join([f'\\x{pair}' for pair in byte_pairs[::-1]])
                    print()
                    print(f"Id: {decimal}")
                    print(f"Hex: {reversed_hex}")  # Little-endian
                    
                except Exception as e:
                    print(f"❌ Error converting {decimal}: {str(e)}\n")
                    
        except ValueError:
            print("\n❌ No valid input provided!")
        
        input("\nPress Enter to continue...")

# ---------- DATA EXTRACTION FUNCTION ----------
def extract_data(items, dump_file, mode, operation_mode):
    # Initialize all mapping dictionaries
    id_map = {}          # Hex -> ID
    name_map = {}        # ID -> Name
    hex_map = {}         # ID -> Hex
    name_to_id_map = {}  # Name -> ID
    name_to_hex_map = {} # Name -> Hex

    # Read Dump File
    typing_effect("\nLoading Skin Data...", 0.02)
    try:
        with open(dump_file, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(" | ")
                if len(parts) >= 3:
                    _id, hex_code, name = parts[0], parts[1], parts[2]
                    id_map[hex_code] = _id
                    name_map[_id] = name
                    hex_map[_id] = hex_code
                    name_to_id_map[name.lower()] = _id
                    name_to_hex_map[name.lower()] = hex_code
    except Exception:
        print("\n❌ Error Loading dump.txt!")
        return []

    result = []
    
    if operation_mode == "pairs":
        for item1, item2 in items:
            if mode == 1:  # Hex to ID
                id1 = id_map.get(item1, "Not Found")
                id2 = id_map.get(item2, "Not Found")
                result.append(f"{id1},{id2}")
            elif mode == 2:  # ID to Name
                name1 = name_map.get(item1, "Not Found")
                name2 = name_map.get(item2, "Not Found")
                result.append(f"\033[92m✨ \033[91;1m{name1}\033[0m \033[38;5;208m»\033[0m ➡️ \033[38;5;14m»\033[0m \033[92;3m{name2}\033[0m ✨\033[0m")
            elif mode == 3:  # ID to Hex
                hex_val1 = hex_map.get(item1, "Not Found")
                hex_val2 = hex_map.get(item2, "Not Found")
                result.append(f"{hex_val1},{hex_val2}")
            elif mode == 4:  # Hex to Name
                id1 = id_map.get(item1, "Not Found")
                id2 = id_map.get(item2, "Not Found")
                name1 = name_map.get(id1, "Not Found")
                name2 = name_map.get(id2, "Not Found")
                result.append(f"\033[92m✨ \033[91;1m{name1}\033[0m \033[38;5;208m»\033[0m ➡️ \033[38;5;14m»\033[0m \033[92;3m{name2}\033[0m ✨\033[0m")
            elif mode == 5:  # Name to ID
                id1 = name_to_id_map.get(item1.lower(), "Not Found")
                id2 = name_to_id_map.get(item2.lower(), "Not Found")
                result.append(f"{id1},{id2}")
            elif mode == 6:  # Name to Hex
                hex1 = name_to_hex_map.get(item1.lower(), "Not Found")
                hex2 = name_to_hex_map.get(item2.lower(), "Not Found")
                result.append(f"{hex1},{hex2}")
    else:  # single mode
        for item in items:
            if mode == 1:  # Hex to ID
                id_val = id_map.get(item, "Not Found")
                result.append(f"{id_val}")
            elif mode == 2:  # ID to Name
                name = name_map.get(item, "Not Found")
                result.append(f"\033[92m✨ \033[91;1m{item}\033[0m → \033[92;3m{name}\033[0m ✨\033[0m")
            elif mode == 3:  # ID to Hex
                hex_val = hex_map.get(item, "Not Found")
                result.append(f"{hex_val}")
            elif mode == 4:  # Hex to Name
                id_val = id_map.get(item, "Not Found")
                name = name_map.get(id_val, "Not Found")
                result.append(f"\033[92m✨ \033[91;1m{item}\033[0m → \033[92;3m{name}\033[0m ✨\033[0m")
            elif mode == 5:  # Name to ID
                id_val = name_to_id_map.get(item.lower(), "Not Found")
                result.append(f"{id_val}")
            elif mode == 6:  # Name to Hex
                hex_val = name_to_hex_map.get(item.lower(), "Not Found")
                result.append(f"{hex_val}")
    return result

# ---------- FILE READING FUNCTIONS ----------
def read_pairs_with_sections(file_path):
    sections = {}
    current_section = None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("----") and stripped.endswith("----"):
                    current_section = stripped.strip("-").strip()
                    sections[current_section] = []
                elif ',' in stripped:
                    parts = stripped.split(',')
                    if len(parts) == 2:
                        if current_section is None:
                            current_section = "DEFAULT"
                            sections[current_section] = []
                        sections[current_section].append((parts[0].strip(), parts[1].strip()))
    except Exception:
        print("\n❌ Error Loading input file!")
        return None
    return sections

def read_singles_with_sections(file_path):
    sections = {}
    current_section = None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("----") and stripped.endswith("----"):
                    current_section = stripped.strip("-").strip()
                    sections[current_section] = []
                else:
                    if current_section is None:
                        current_section = "DEFAULT"
                        sections[current_section] = []
                    sections[current_section].append(stripped)
    except Exception:
        print("\n❌ Error Loading input file!")
        return None
    return sections

# ---------- BASIC CONVERTER FUNCTION ----------
def basic_converter():
    input_file = "/storage/emulated/0/FILES_OBB/ID,NAME,HEX/input.txt"
    dump_file = "/storage/emulated/0/FILES_OBB/ID,NAME,HEX/dump.txt"

    while True:
        clear_screen()
        display_title()
        
        # Operation mode selection
        print("\nChoose Operation Mode:")
        print("1. Single Item Mode")
        print("2. Pair Mode")
        print("3. Back to Main Menu")
        
        try:
            operation_choice = int(input("\nEnter choice (1-3): ").strip())
            if operation_choice == 3:
                return
            elif operation_choice not in [1, 2]:
                raise ValueError
        except ValueError:
            print("\n❌ Invalid Input! Please try again.")
            time.sleep(1)
            continue
        
        operation_mode = "single" if operation_choice == 1 else "pairs"
        
        # Read input file based on operation mode
        if operation_mode == "pairs":
            sections = read_pairs_with_sections(input_file)
        else:
            sections = read_singles_with_sections(input_file)
            
        if sections is None:
            time.sleep(2)
            continue

        # Display conversion mode options
        clear_screen()
        display_title()
        print("\nChoose Conversion Mode:")
        print("1. Hex to ID")
        print("2. ID to Name")
        print("3. ID to Hex")
        print("4. Hex to Name")
        print("5. Name to ID")
        print("6. Name to Hex")
        print("7. Back")
        
        try:
            mode = int(input("\nEnter mode (1-7): ").strip())
            if mode == 7:
                continue
            if mode not in range(1, 7):
                raise ValueError
        except ValueError:
            print("\n❌ Invalid Input! Please try again.")
            time.sleep(1)
            continue

        # Process and display results
        clear_screen()
        display_title()
        print("\n══════════════════════════════════════════════")
        print("Output:")
        print("══════════════════════════════════════════════\n")

        for section, items in sections.items():
            print(f"---- {section} ----")
            print(f"Total Count: {len(items)}\n")
            output_lines = extract_data(items, dump_file, mode, operation_mode)
            
            if mode in [2, 4]:  # Fancy output modes
                counter = 1
                for line in output_lines:
                    print(f"{counter}. {line}\n")
                    counter += 1
            else:  # Plain output modes
                for line in output_lines:
                    print(line)
        
        print("\n══════════════════════════════════════════════")
        input("\nPress Enter to continue...")

# ---------- MAIN EXECUTION ----------
def main():
    while True:
        clear_screen()
        display_title()
        
        # Main menu selection
        print("\nMAIN MENU:")
        print("1. Basic Converter (Single/Pair Mode)")
        print("2. Advanced Decimal-Hex Converter")
        print("3. Exit")
        
        try:
            main_choice = int(input("\nEnter choice (1-3): ").strip())
            if main_choice == 3:
                print("\nGoodbye! 👋")
                return
            elif main_choice == 1:
                basic_converter()
            elif main_choice == 2:
                advanced_converter()
            else:
                raise ValueError
        except ValueError:
            print("\n❌ Invalid Input! Please try again.")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()
