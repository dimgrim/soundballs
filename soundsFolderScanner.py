import os
import json
import sys

def scan_sounds_folder(sounds_path):
    """
    Scan the sounds folder and create a structured dictionary of its contents.
    """
    result = {
        "note_folders": [],
        "note_files": {},
        "background_files": []
    }
    
    # Get all items directly inside the sounds folder
    try:
        items = os.listdir(sounds_path)
    except PermissionError:
        print(f"Error: Permission denied to access '{sounds_path}'.")
        return None
    
    # Process each item inside the sounds folder
    for item in sorted(items):
        item_path = os.path.join(sounds_path, item)
        
        if os.path.isdir(item_path):
            if item.lower() == "background":
                # This is the background folder - add its contents to background_files
                print(f"  Found background folder: {item}")
                try:
                    for file in sorted(os.listdir(item_path)):
                        file_path = os.path.join(item_path, file)
                        if os.path.isfile(file_path) and file.lower().endswith('.wav'):
                            result["background_files"].append(file)
                            print(f"    Added background file: {file}")
                except PermissionError:
                    print(f"  Warning: Permission denied to read folder '{item}'")
            else:
                # This is a note folder
                print(f"  Found note folder: {item}")
                result["note_folders"].append(item)
                
                # Get all wav files inside this subfolder
                wav_files = []
                try:
                    for file in sorted(os.listdir(item_path)):
                        file_path = os.path.join(item_path, file)
                        if os.path.isfile(file_path) and file.lower().endswith('.wav'):
                            wav_files.append(file)
                except PermissionError:
                    print(f"  Warning: Permission denied to read folder '{item}'")
                    continue
                
                if wav_files:
                    result["note_files"][item] = wav_files
                    print(f"    Found {len(wav_files)} note files")
        
        elif os.path.isfile(item_path) and item.lower().endswith('.wav'):
            # This is a wav file directly in the sounds folder root
            print(f"  Found root background file: {item}")
            result["background_files"].append(item)
    
    return result

def main():
    """Main function to run the script."""
    print("Sounds Folder Scanner")
    print("=" * 50)
    
    # Get the current directory (where the script is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sounds_path = os.path.join(current_dir, "sounds")
    
    print(f"Script location: {current_dir}")
    print(f"Looking for sounds folder at: {sounds_path}")
    print()
    
    # Check if the sounds folder exists
    if not os.path.exists(sounds_path) or not os.path.isdir(sounds_path):
        print(f"❌ Error: Could not find 'sounds' folder at: {sounds_path}")
        print("   Make sure:")
        print("   1. You have a folder named 'sounds' in the same directory as this script")
        print("   2. The 'sounds' folder contains your piano/, bells/, background/ folders and WAV files")
        print()
        print(f"Current directory contents:")
        for item in sorted(os.listdir(current_dir)):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
        
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Scan the folder
    print(f"\nScanning contents of 'sounds' folder...")
    folder_data = scan_sounds_folder(sounds_path)
    
    if folder_data is None:
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Save JSON in the same directory as the script (next to the sounds folder)
    output_path = os.path.join(current_dir, "sounds.json")
    
    # Write to JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(folder_data, json_file, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully created sounds.json at: {output_path}")
        print(f"\nSummary:")
        print(f"  - Note folders: {', '.join(folder_data['note_folders'])}")
        
        total_note_files = sum(len(files) for files in folder_data['note_files'].values())
        print(f"  - Total note files: {total_note_files}")
        
        for folder, files in folder_data['note_files'].items():
            print(f"    • {folder}: {len(files)} files")
        
        print(f"  - Background files: {len(folder_data['background_files'])}")
        if folder_data['background_files']:
            print(f"    Files: {', '.join(folder_data['background_files'])}")
        
    except Exception as e:
        print(f"\n❌ Error writing JSON file: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\nDone! Press Enter to exit.")
    input()

if __name__ == "__main__":
    main()
