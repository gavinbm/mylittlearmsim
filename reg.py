# Dict to hold pseudo registers, defaulted to 0 for simplicity
Reg = {"x0":0,"x1":0,
       "x2":0,"x3":0,
       "x4":0,"x5":0,
       "x6":0,"x7":0,
       "x8":0,"x9":0,
       "sp":0}

# Dict to hold Flags that are used for cmp and branching
Flags = {"eq":False,
         "gt":False,
         "lt":False,
         "ne":False,
         "ge":False,
         "le":False}

# Dict to hold all labels and their corresponding line numbers
Labels = {}

'''basic regex for removing non-essential characters from each line.
   removes commas and # so instructions can be passed into
   the appropriate functions
'''
regex = ",#"

''' Move Instruction '''
def mov(dest, data):
    if "x" in data:
        Reg[dest] = Reg[data]
    elif "x" not in data:
        Reg[dest] = int(data)
    elif dest not in Reg:
        print("Invalid input")

''' conditional and branching instructions '''
def cmp(op1, op2):
    if "x" in op1:
        op1 = op1.replace(" ", "").replace(",", "")
        x = Reg[op1]
    else:
        x = int(op1)
    if "x" in op2:
        op2 = op2.replace(" ", "").replace(",", "")
        y = Reg[op2]
    else:
        y = int(op2)
    Flags["eq"] = x == y
    Flags["lt"] = x < y
    Flags["gt"] = x > y
    Flags["ne"] = x != y
    Flags["ge"] = x >= y
    Flags["le"] = x <= y

''' Arithmetic Instructions '''
def add(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        if op1 in Reg:
            x = Reg[op1]
        if op2 in Reg:
            y = Reg[op2]
        Reg[dest] = int(x) + int(y)
    else:
        print("invalid dest")

def mul(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        if op1 in Reg:
            x = Reg[op1]
        if op2 in Reg:
            y = Reg[op2]
        Reg[dest] = int(x) * int(y)
    else:
        print("invalid dest")

def sub(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        if op1 in Reg:
            x = Reg[op1]
        if op2 in Reg:
            y = Reg[op2]
        Reg[dest] = int(x) - int(y)
    else:
        print("invalid dest")

''' Parsing '''
def parse(line):
    for char in line:
        if char in regex:
            line = line.replace(char, "")
    parsed = [x for x in line.split(" ") if x != "" and "@" not in x]
    return parsed

''' Get Labels '''
def getLabels(inputFile):
    for k in range(0, len(inputFile)):
        tmp = parse(inputFile[k])
        if ":" in tmp[0]:
            Labels[tmp[0].replace(":", "")] = k

''' Reset register values to 0 '''
def resetReg(registers):
    for key in registers:
        registers[key] = 0

''' Format Registers for Site '''
def beautify(regDict):
    res = ""
    for register in regDict:
        res += register + ": " + str(regDict[register]) + " "
    return res
