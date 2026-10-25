import os


def get_valid_target(wd:str, path: str) -> tuple[bool, str]:
    target = os.path.normpath(os.path.join(os.path.abspath(wd), path))
    wd_abs = os.path.normpath(os.path.abspath(wd))
    target_valid = os.path.commonpath([wd_abs, target]) == wd_abs
    return (target_valid, target)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_valid, target = get_valid_target(working_directory, directory)

        if not target_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return(f"Error: {e}")

    ls = os.listdir(target)
    out = []
    for f in ls:
        p = target + "/" + f
        try:
            out.append(f"- {f}: file_size={os.path.getsize(p)} bytes, is_dir={os.path.isdir(p)}")
        except Exception as e:
            return(f"Error: {e}")
    return "\n".join(out)

    return f'Success: "{directory}" is within the working directory'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
