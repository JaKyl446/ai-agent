from functions.write_file import write_file

wd = "calculator"
files = [
    ("lorem.txt", "wait, this isn't lorem ipsum"),
    ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("/tmp/temp.txt", "this should not be allowed"),
]

for f, c in files:
    result = write_file(wd, f, c)
    print(result)
