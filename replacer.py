DBGtoLOG = {
    "DBG_ERROR": "LOG_ERROR",
    "DBG_MSG":"LOG_INFO", 
    "DBG_WARNING":"LOG_WARN"
    }

symbolToNew = {
    "%d": "{}",
    "%s": "{}",
    "%u": "{}",
    "%X": "{0:x}",
    "%zu": "{}",
    "%zd": "{}",
    "%zd": "{}",
    "0x%X": "{0:x}"
}
goToNextLine = False
delStartBracket = False

def changeLogger(line):
    for DBGtype in DBGtoLOG:
        if line.find(DBGtype) != -1:
            line = line.replace(DBGtype, DBGtoLOG[DBGtype])
            break
    return line

def checkEnd(line):
    global goToNextLine
    endLine = line.find( ");" )
    if endLine != -1:
        end = line[endLine + 1:]
        line = line[: endLine] + end
        goToNextLine = False
    return line

def changeSymbols(line):
    for oldSymbol in symbolToNew:
        if oldSymbol in line:
            line = line.replace(oldSymbol, symbolToNew[oldSymbol])
    return line

def changeParam(line):
    global goToNextLine
    global delStartBracket
    for DBGtype in DBGtoLOG:
        DBGindex = line.find(DBGtype)
        if DBGindex != -1:
            DBGindex += len(DBGtype)

            if line[DBGindex + 1] == '\n':
                goToNextLine = True
                delStartBracket = False
                return line
            elif line[DBGindex + 1] == '(':
                line = line.replace("(", "", 1)
                delStartBracket = True
                if line.endswith( "(\n" ):
                    goToNextLine = True
                else:
                    line = changeSymbols(line)
                    line = checkEnd(line)
            
    if goToNextLine:
        if not delStartBracket:
            line = line.replace("(", "", 1)
            delStartBracket = True
        line = changeSymbols(line)
        line = checkEnd(line)
    return line