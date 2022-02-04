
from cmath import pi
from inspect import ismethod
from pickle import FALSE


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
            print(line[foundDBG], DBGtype)
            if line[foundDBG + 1] == '(':              #if func parametrs at the same line
                checkBracketsCount(line)
                line = line[foundDBG + 1].replace('(', '')
                for oldSymbol in symbolToNew:
                    line = line.replace(oldSymbol, symbolToNew[oldSymbol]) 
                if bracketsCount != 0:
                    findAtNextLine = True
            elif line[foundDBG + 1] == '\n':
                findAtNextLine = True
    if findAtNextLine:
        for oldSymbol in symbolToNew:
                line = line.replace(oldSymbol, symbolToNew[oldSymbol])
        if bracketsCount == 0:
            findAtNextLine = False
    return line


goToNextLine = False
reverseAtNextLine = False
def removeStrFromLine(line, startPos, endPos, find_symbol):
    isFound = False
    piece = line[line.find(startPos) + 1 : line.find(endPos) + 2]
    print(piece)
    if piece.find(find_symbol) != -1:
        isFound = True
    if isFound:
        line = line.replace(piece, "{} [{}]")
    else:
        line = line.replace(piece, "{}")
    return line, isFound

def reverseSymbolPosition(line):
    tempLine = line[:line.find("\",") + 2]
    quotesPoint = line[line.find("\",") + 2:]
    parametrs = quotesPoint.split(",")

    if parametrs[0] != "__METHOD_NAME__":
        temp = parametrs[0]
        parametrs[0] = parametrs[1]
        parametrs[1] = temp
    tempLine += ",".join(parametrs)
    return tempLine

def atTheSameLine(line):
    global goToNextLine
    global reverseAtNextLine
    if not line.endswith("(\n"):
        for oldSymbol in symbolToNew:
            if oldSymbol in line:
                #delete string
                line, isWrongSymbolFirst = removeStrFromLine(line, "\"", "%s", "[%d]")
                for oldSymbol in symbolToNew:
                        #change symbols
                        line = line.replace(oldSymbol, symbolToNew[oldSymbol])
                if isWrongSymbolFirst:
                    #reverse methods __FIRST__ to __SECOND__ 
                    if not line.endswith("\",\n"): #or not line.endswith("\"\n"):
                        line = reverseSymbolPosition(line) 
                    else:
                        #reverse at the next line
                        reverseAtNextLine = True
                else:
                    goToNextLine = True
                    print("go to angother line")
            
    return line


def changeParam(line):
    global goToNextLine
    global reverseAtNextLine
    for DBGtype in DBGtoLOG:
        indexDBG = line.find(DBGtype)
        if indexDBG != -1:
            indexDBG += len(DBGtype)
            
            if line[indexDBG + 1] == '\n':
                goToNextLine = True

            #func parametrs and DBG_ at the same line
            elif line[indexDBG + 1] == '(':
                line = line.replace("(", "", 1)
                line = atTheSameLine(line)
        
        if goToNextLine:
            line = atTheSameLine(line)
            cppEndLine = line.find( ");" )
            if cppEndLine != -1:
                end = line[cppEndLine + 1:]
                line = line[: cppEndLine] + end
                goToNextLine = False
            for oldSymbol in symbolToNew:
                line = line.replace(oldSymbol, symbolToNew[oldSymbol])
            #don't work correctly
            if reverseAtNextLine:
                pass
                # if not line.endswith("\",\n") or not line.endswith("\"\n"):
                #     if  line.find("__METHOD_NAME__") == -1:
                #         temp = line
                #         line = line.replace(temp, "__METHOD_NAME__")
                #         reverseAtNextLine = FALSE
    return line


def changeLogger(line):
    for DBGtype in DBGtoLOG:
        if line.find(DBGtype) != -1:
            line = line.replace(DBGtype, DBGtoLOG[DBGtype])
            break
    return line
            

filename = "test.cpp"
new_file = ""

with open(filename, "r") as file:
    for line in file:
        line = changeParam(line)
        line = line.rstrip("\n") #remove '\n' from line.
        line = changeLogger(line)
        new_file += line + '\n'
    
with open(filename, "w") as file:
    file.write(new_file)


"""Если название начинается также как и файл,
то
разделить всё на список по пробелу
0 элемент списка - удалить
и вместо него вставить {}
а 
после \", вставить название метода"""