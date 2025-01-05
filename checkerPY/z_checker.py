import os
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_file_hash(file_path):
    """Returns the SHA256 hash for the specified file."""
    hash_algo = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def get_file_hash_with_path(file_path):
    """Returns a tuple (file path, hash) for the specified file."""
    return file_path, get_file_hash(file_path)

def get_folder_hashes(folder_path):
    """Returns a dictionary with file hashes in the specified folder and its subdirectories."""
    file_hashes = {}
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(get_file_hash_with_path, file_path))
        
        for future in as_completed(futures):
            file_path, file_hash = future.result()
            file_hashes[file_path] = file_hash

    return file_hashes

def save_hashes_to_file(hashes, file_path):
    """Saves the dictionary of hashes to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(hashes, f, indent=4, ensure_ascii=False)

def load_hashes_from_file(file_path):
    """Loads the dictionary of hashes from a JSON file, if it exists."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def compare_hashes(old_hashes, new_hashes):
    """Compares old and new hashes and returns the changes."""
    changes = {'modified': {}, 'added': {}, 'deleted': {}}

    for file_path, new_hash in new_hashes.items():
        if file_path in old_hashes:
            if old_hashes[file_path] != new_hash:
                changes['modified'][file_path] = {'old': old_hashes[file_path], 'new': new_hash}
        else:
            changes['added'][file_path] = new_hash

    for file_path in old_hashes:
        if file_path not in new_hashes:
            changes['deleted'][file_path] = old_hashes[file_path]

    return changes

def pretty_print_changes(changes, root_path):
    """Nicely formats and prints changes with relative paths."""
    has_changes = any(changes.values())
    if not has_changes:
        print("No changes detected.\n")
        return

    change_messages = {
        'modified': "modified",
        'added': "added",
        'deleted': "deleted"
    }

    for change_type, message in change_messages.items():
        if changes[change_type]:
            print(f"{message.capitalize()} files:")
            for file_path in changes[change_type]:
                relative_path = os.path.relpath(file_path, root_path)
                print(f"  {relative_path} ({message})")
            print()

def main():
    """Main function to execute the program."""
    if not os.path.exists('path.txt'):
        print("File path.txt does not exist.\n")
        return

    with open('path.txt', encoding='utf-8') as file:
        folder_path = file.read().strip()

    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.\n")
        return

    hash_file_path = 'hashes.json'

    old_hashes = load_hashes_from_file(hash_file_path)
    new_hashes = get_folder_hashes(folder_path)
    changes = compare_hashes(old_hashes, new_hashes)
    
    pretty_print_changes(changes, folder_path)

    # Save hashes only if there were changes
    if any(changes.values()):  # Check for changes
        save_hashes_to_file(new_hashes, hash_file_path)

if __name__ == "__main__":
    main()
