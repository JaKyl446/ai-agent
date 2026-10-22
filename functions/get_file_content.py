import os

from config import MAX_CHARS
from functions.get_files_info import get_valid_target


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_valid, target = get_valid_target(working_directory, file_path)

        if not target_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target) or os.path.islink(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return(f"Error: reading file: {e}")

    return content
