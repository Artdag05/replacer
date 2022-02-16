import os
from replacer import* 

def filter(files):
    result = list()
    for file in files:
        if file.endswith(".cpp"):
            result.append(file)
    return result

dirname = input("Enter dir name location: ")
files = filter(os.listdir(dirname))

for file in files:
    filename = os.path.join(dirname, file)
    new_file = ""

    with open(filename, "r") as file:
        for line in file:
            line = changeParam(line)
            line = line.rstrip("\n")
            line = changeLogger(line)
            new_file += line + '\n'
        
    with open(filename, "w") as file:
        file.write(new_file)

