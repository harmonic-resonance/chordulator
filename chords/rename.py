from pathlib import Path

# Get the current directory
current_directory = Path('.')

# Iterate over all .csml files in the directory
for file in current_directory.glob('*.txt'):
    # Check if '-docx' is in the stem of the file name
    new_file_name = f"{file.stem}.csml"
    file.rename(Path(file.parent, new_file_name))

