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

        cmd = ["python", target]
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
