from functions.run_python_file import run_python_file

wd = "calculator"
files = [
    ("main.py", None),
    ("main.py", ["3 + 5"]),
    ("tests.py", None),
    ("../main.py", None),
    ("nonexistent.py", None),
    ("lorem.txt", None),
]

for e, a in files:
    print(run_python_file(wd, e, a))
