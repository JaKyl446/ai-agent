import os

from functions.get_files_info import get_valid_target


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_valid, target = get_valid_target(working_directory, file_path)

        if not target_valid:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        if os.path.islink(target):
            return f'Error: Cannot write to "{file_path}" as it is a symbolic link'

        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w") as f:
            written = f.write(content)

        return f'Successfully wrote to "{file_path}" ({written} characters written)'
    except Exception as e:
        return(f"Error: writing file: {e}")
