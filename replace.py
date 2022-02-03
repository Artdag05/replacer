
DBGtoLOG = {
    "DBG_ERROR": "LOG_ERROR",
    "DBG_MSG":"LOG_INFO", 
    "DBG_WARNING":"LOG_WARN"
    }
className = "CPAppleDeviceService"
symbolToNew = {
    className + "[%d]::" : "",
    className + "::" : "",
    "%d": "{}",
    "%s": "{}",
    "%u": "{}",
    "__func__" : "__METHOD_NAME__",
    "__FUNCTION__" : "__METHOD_NAME__"
}
filename = "test.cpp"
new_file = ""
findAtNextLine = False
bracketsCount = 0

def checkBracketsCount(line):
    global bracketsCount
    for symbol in line:
        if symbol.find('('):
            bracketsCount += 1
        elif symbol.find(')'):
            bracketsCount -= 1

def changeFuncParametrs(line):
    global findAtNextLine
    for DBGtype in DBGtoLOG:
        foundDBG = line.find(DBGtype)
        if foundDBG != -1:
            foundDBG += len(DBGtype) 
            if line[foundDBG + 1] == '(':              #if func parametrs at the same line
                checkBracketsCount(line)
                line = line[foundDBG + 1].replace('(', '')
                for oldSymbol in symbolToNew:
                    line = line.replace(oldSymbol, symbolToNew[oldSymbol]) 
                if bracketsCount != 0:
                    findAtNextLine = True
            if line[foundDBG + 1] == '\n':
                findAtNextLine = True
    if findAtNextLine:
        for oldSymbol in symbolToNew:
                line = line.replace(oldSymbol, symbolToNew[oldSymbol])
        if bracketsCount == 0:
            findAtNextLine = False
    return line


def changeLogger(line):
    for DBGtype in DBGtoLOG:
        if line.find(DBGtype) != -1:
            line = line.replace(DBGtype, DBGtoLOG[DBGtype])
            break
    return line
            
with open(filename, "r") as file:
    for line in file:
        line = changeFuncParametrs(line)
        line = line.rstrip("\n") #remove '\n' from line.
        line = changeLogger(line)
        new_file += line + '\n'
    
with open(filename, "w") as file:
    file.write(new_file)

