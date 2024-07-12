import sys
import os

def load_abbreviations(file_path):
    abbreviations = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    abbreviations[parts[0].upper()] = parts[1]
    except FileNotFoundError:
        print(f"Error: Abbreviations file not found at {file_path}")
        sys.exit(1)
    return abbreviations

def get_expansion(abbreviations, query):
    query = query.upper()
    if query in abbreviations:
        return f"{query}: {abbreviations[query]}"
    else:
        return f"Sorry, I couldn't find an expansion for '{query}'."

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the config directory
    config_dir = os.path.join(script_dir, '../config')
    
    # Construct the full path to the abbreviations.txt file
    abbreviations_file = os.path.join(config_dir, 'abbreviations.txt')
    
    abbreviations = load_abbreviations(abbreviations_file)

    if len(sys.argv) < 2:
        print("Usage: python idkbot_cli.py <abbreviation>")
        sys.exit(1)

    query = sys.argv[1]
    result = get_expansion(abbreviations, query)
    print(result)

if __name__ == "__main__":
    main()
