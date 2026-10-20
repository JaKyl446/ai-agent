import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir = os.path.normpath(os.path.join(os.path.abspath(working_directory), directory))
        wd_abs = os.path.normpath(os.path.abspath(working_directory))

        target_dir_valid = os.path.commonpath([wd_abs, target_dir]) == wd_abs

        if not target_dir_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        print("Error: {e}")

    return f'Success: "{directory}" is within the working directory'
