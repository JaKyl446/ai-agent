from functions.get_files_info import get_files_info

wd = "calculator"
dirs = [".", "pkg", "/bin", "../"]

for d in dirs:
    print(f"\nResult for '{d}' directory:")
    print(get_files_info(wd, d))


