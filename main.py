from replacer import*

filename = "test.cpp"
new_file = ""

with open(filename, "r") as file:
    for line in file:
        line = changeFuncParametrs(line)
        line = line.rstrip("\n") #remove '\n' from line.
        line = changeLogger(line)
        new_file += line + '\n'
    
with open(filename, "w") as file:
    file.write(new_file)