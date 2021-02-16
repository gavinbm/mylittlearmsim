# Dict to hold pseudo registers, defaulted to 0 for simplicity
Reg = {"x0":0,"x1":0,
       "x2":0,"x3":0,
       "x4":0,"x5":0,
       "x6":0,"x7":0,
       "x8":0,"x9":0,
       "sp":0}

'''origValues = {"x0":0,"x1":0,
              "x2":0,"x3":0,
              "x4":0,"x5":0,
              "x6":0,"x7":0,
              "x8":0,"x9":0,
              "sp":0}'''

# Dict to hold Flags that are used for cmp and branching
Flags = {"eq":False,
         "gt":False,
         "lt":False,
         "ne":False}

# Dict to hold all labels and their corresponding line numbers
Labels = {}

''' Move Instruction '''
def mov(dest, data):
    dest = dest.replace(" ", "").replace(",", "")
    data = data.replace(" ", "").replace(",", "")
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

''' Arithmetic Instructions '''
def add(dest, op1, op2):
    dest = dest.replace(" ", "").replace(",", "")
    x = op1.replace(" ", "").replace(",", "")
    y = op2.replace(" ", "").replace(",", "")
    if dest in Reg:
        if op1 in Reg:
            x = Reg[op1]
        if op2 in Reg:
            y = Reg[op2]
        Reg[dest] = int(x) + int(y)
    else:
        print("invalid dest")

def mul(dest, op1, op2):
    dest = dest.replace(" ", "").replace(",", "")
    x = op1.replace(" ", "").replace(",", "")
    y = op2.replace(" ", "").replace(",", "")
    if dest in Reg:
        if op1 in Reg:
            x = Reg[op1]
        if op2 in Reg:
            y = Reg[op2]
        Reg[dest] = int(x) * int(y)
    else:
        print("invalid dest")

def sub(dest, op1, op2):
    dest = dest.replace(" ", "").replace(",", "")
    x = op1.replace(" ", "").replace(",", "")
    y = op2.replace(" ", "").replace(",", "")
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
    parsed = [x for x in line.split(" ") if x != ""]
    for i in range(0, len(parsed)):
        # comment handling
        if "@" in parsed[i]:
            parsed[i] = ""
        else:
            parsed[i] = parsed[i].replace(" ", "").replace(",", "").replace("#", "")
    return parsed

''' Get Labels '''
def getLabels(inputFile):
    for k in range(0, len(inputFile)):
        tmp = parse(inputFile[k])
        if ":" in tmp[0]:
            Labels[tmp[0][:-1]] = k
