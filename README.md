# checkerPY

`checkerPY` is a Python program designed to monitor changes in files within a directory by computing and comparing their SHA256 hashes. It can detect modifications, additions, and deletions of files. This is useful for tracking changes in a directory over time.

## Features

- **Hash Computation**: Calculates SHA256 hashes of files in a directory and its subdirectories.
- **Change Detection**: Compares current file hashes with previously saved hashes to detect modifications, additions, and deletions.
- **Persistent Storage**: Saves and loads file hashes to and from a JSON file for persistent monitoring.
- **Change Reporting**: Provides a human-readable report of detected changes with relative paths.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kapitoshka1337/checkerPY.git
    cd checkerPY
    ```

2. Ensure you have Python 3.6+ installed.

## Usage

1. Create a text file named `path.txt` in the same directory as the script. This file should contain the absolute path of the directory you want to monitor.

    ```text
    /absolute/path/to/your/directory
    ```

2. Run the script:

    ```bash
    python checkerPY.py
    ```

3. The script will read the path from `path.txt`, compute file hashes, compare them with previously saved hashes (if any), and print out the changes. If changes are detected, it will update the `hashes.json` file with the new hashes.

## Functions

- **`get_file_hash(file_path)`**: Returns the SHA256 hash of a file specified by `file_path`.
- **`get_file_hash_with_path(file_path)`**: Returns a tuple containing the file path and its SHA256 hash.
- **`get_folder_hashes(folder_path)`**: Computes and returns a dictionary of file paths and their hashes for all files in the specified folder and its subdirectories.
- **`save_hashes_to_file(hashes, file_path)`**: Saves the dictionary of file hashes to a JSON file specified by `file_path`.
- **`load_hashes_from_file(file_path)`**: Loads and returns the dictionary of file hashes from a JSON file specified by `file_path`. Returns an empty dictionary if the file does not exist.
- **`compare_hashes(old_hashes, new_hashes)`**: Compares old and new file hashes and returns a dictionary of changes, including modified, added, and deleted files.
- **`pretty_print_changes(changes, root_path)`**: Nicely formats and prints the detected changes with relative paths.

## Example Output

```
Modified files:
  relative/path/to/modified/file.txt (modified)

Added files:
  relative/path/to/new/file.txt (added)

Deleted files:
  relative/path/to/deleted/file.txt (deleted)
```

## Notes

- Ensure `path.txt` is correctly configured with a valid directory path.
- The `hashes.json` file will be created or updated in the same directory as the script.
- To ignore certain files or directories, you may need to modify the script to add filtering logic.

## Contributing

Feel free to fork the repository and submit pull requests. Ensure that your contributions follow the coding style and pass any existing tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
