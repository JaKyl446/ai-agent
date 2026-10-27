import os
import subprocess

from functions.get_files_info import get_valid_target


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        target_valid, target = get_valid_target(working_directory, file_path)

        if not target_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if os.path.islink(target):
            return f'Error: Cannot execute "{file_path}" as it is a symbolic link'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        if not wait_for_review(target, args):
            return (f'Error: Human intervention while trying to execute "{file_path}"')
        
        cmd = ["firejail", "--seccomp", "--net=none", "--quiet", "python", target]
        if type(args) == list and len(args) > 0:
            cmd.extend(args)

        wd_abs = os.path.normpath(os.path.abspath(working_directory))
        proc = subprocess.run(cmd, cwd=wd_abs, capture_output=True, text=True, timeout=30, check=False)
        output = ""
        if proc.returncode != 0:
            output += f"\nProcess exited with code {proc.returncode}"
        if len(proc.stdout) == 0 and len(proc.stderr) == 0:
            output += "\nNo output produced"
        if len(proc.stdout) > 0:
            output += "\nSTDOUT:" + proc.stdout
        if len(proc.stderr) > 0:
            output += "\nSTDERR:" + proc.stderr

        return output
    except Exception as e:
        return(f"Error: executing Python file: {e}")

def wait_for_review(target: str, args: list[str]) -> bool:
    print(f"Calling: {target} with args: {args}")
    cmd = ["kwrite", target]
    proc = subprocess.run(cmd, check=False)
    if proc.returncode == 0:
        return True
    return False

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run the python file from, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of command line arguments passed to the python file (optional)"
                }
            },
        },
    },
}
