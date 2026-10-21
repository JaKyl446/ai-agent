import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        wd_abs = os.path.normpath(os.path.abspath(working_directory))
        target_valid = os.path.commonpath([wd_abs, target]) == wd_abs

        if not target_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target) or os.path.islink(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return(f"Error: {e}")

    try:
        with open(target, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return(f"Error: {e}")

    return content
