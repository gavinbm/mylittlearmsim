# Dict to hold pseudo registers, defaulted to 0 for simplicity
Reg = {"x0":None,"x1":None,
       "x2":None,"x3":None,
       "x4":None,"x5":None,
       "x6":None,"x7":None,
       "x8":None,"x9":None,
       "lr":None,"sp":[]}

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
regex = ",#[]"

''' Move Instruction '''
def mov(dest, data):
    if "x" in data:
        Reg[dest] = Reg[data]
    elif "x" not in data:
        Reg[dest] = int(data)
    elif dest not in Reg:
        print("Invalid input")

def str(src, sp, placeInStack):
    placeInStack = int(int(placeInStack)/8)

    if placeInStack >= len(Reg["sp"]):
        print("out of range")
        return
    if src not in Reg:
        print("invalid src")
        return
    else:
        Reg["sp"][placeInStack] = Reg[src]

def ldr(dest, src, placeInStack):
    placeInStack = int(int(placeInStack)/8)

    if dest in Reg and placeInStack < len(Reg["sp"]):
        Reg[dest] = Reg["sp"][placeInStack]
    elif dest not in Reg:
        print("invalid dest")
    elif placeInStack >= len(Reg["sp"]):
        print("target out of range")

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
    if x == None or y == None:
        print("uninitialized register")
        return
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
        if x == None or y == None:
            print("uninitialized register")
            return
        Reg[dest] = int(x) + int(y)
    else:
        print("invalid dest")

def mul(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        if dest == "sp":
            print("invalid ins")
        else:
            if op1 in Reg:
                x = Reg[op1]
            if op2 in Reg:
                y = Reg[op2]
            if x == None or y == None:
                print("uninitialized register")
                return
            Reg[dest] = int(x) * int(y)
    else:
        print("invalid dest")

def sub(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        # using sub to grow the stack
        if dest == "sp" and int(op2) % 8 == 0:
            Reg["sp"] = [None] * int(int(op2)/8)
        elif op2 % 8 != 0:
            print("must be multiple of 8")
        else:
            if op1 in Reg:
                x = Reg[op1]
            if op2 in Reg:
                y = Reg[op2]
            if x == None or y == None:
                print("uninitialized register")
                return
            Reg[dest] = int(x) - int(y)
    else:
        print("invalid dest")

# dict to store all function calls and tie them to appropriate user input
asm = {"mov":mov, "cmp":cmp, "add":add, "sub":sub, "mul":mul, "str":str, "ldr":ldr}

''' check for NULL registers '''
def checkNone(register):
    if Reg[register] == None:
        return False
    else:
        return True

''' Parsing '''
# takes in a string (line) removes non-alphanumeric chars and puts valid strings
# into a list. first entry of list will be the instruction, the others will be
# the corresponding arguments
def parse(line):
    for char in line:
        if char in regex:
            line = line.replace(char, "")
    parsed = [x for x in line.split(" ") if x != "" and "@" not in x]
    return parsed

''' Get Labels '''
# fills Labels dict with every label in the user input, labels are keys, line
# numbers are values
def getLabels(inputFile):
    for k in range(0, len(inputFile)):
        tmp = parse(inputFile[k])
        if tmp == []:
            continue
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
