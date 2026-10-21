from functions.get_file_content import get_file_content

wd = "calculator"
files = ["lorem.txt", "main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]

for f in files:
    result = get_file_content(wd, f)
    if not 'truncated' in result:
        print(result)
    else:
        print(f"{f} length: {len(result)}")
        print(f"{f} truncated: {'truncated' in result}")
