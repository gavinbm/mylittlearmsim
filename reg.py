from flask import Flask, flash, redirect, url_for, render_template, request, session

# Dict to hold pseudo registers, defaulted to None to represent garbage values
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

''' Move, Load, and Store Instructions '''
def mov(dest, data):
    if "x" in data:
        Reg[dest] = Reg[data]
    elif "x" not in data:
        Reg[dest] = int(data)
    elif dest not in Reg:
        flash("Too bad! That destination doesn't exist!")
        return render_template("home.html")

# stores the src value into the stack at the set increment
# checks if user is reaching out of range of the stack
# Throws error if the user goes past the stack
def store(src, sp, placeInStack):
    placeInStack = int(int(placeInStack)/4)

    if placeInStack >= len(Reg["sp"]):
        flash("Oh no! You've reached past the stack pointer!")
        return render_template("home.html")

    if src not in Reg:
        flash("Too bad! The source register doesn't exist!")
        return render_template("home.html")
    else:
        Reg["sp"][placeInStack] = Reg[src]

# loads desired value from the stack list
# checks for invalid inputs/calls and throws errors accordingly
def ldr(dest, src, placeInStack):
    placeInStack = int(int(placeInStack)/4)

    if dest in Reg and placeInStack < len(Reg["sp"]):
        Reg[dest] = Reg["sp"][placeInStack]

    elif dest not in Reg:
        flash("Error! Invalid destination register!")
        return render_template("home.html")

    elif placeInStack >= len(Reg["sp"]):
        flash("Oh no! You've reached past the stack pointer!")
        return render_template("home.html")

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
        flash("Whoops! Theres an uninitialized register in a cmp instruction!")
        return render_template("home.html")
    Flags["eq"] = x == y
    Flags["lt"] = x < y
    Flags["gt"] = x > y
    Flags["ne"] = x != y
    Flags["ge"] = x >= y
    Flags["le"] = x <= y

''' Arithmetic Instructions '''
# performs addition of immediates or register values
# also used to shrink the stack
def add(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        if dest == "sp":
            op2 = int(op2)
            if int(op2/4) != len(Reg["sp"]):
                flash("Darn! You've got to reset the stack!")
                return render_template("home.html")
            else:
                Reg["sp"] = []
                return
        if op1 in Reg:
            x = Reg[op1]
        if op2 in Reg:
            y = Reg[op2]
        if x == None or y == None:
            flash("Whoops! Theres an uninitialized register in an add instruction!")
            return render_template("home.html")
        Reg[dest] = int(x) + int(y)
    else:
        print("invalid dest")

# performs multiplication
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
                flash("Whoops! Theres an uninitialized register in a mul instruction!")
                return render_template("home.html")
            Reg[dest] = int(x) * int(y)
    else:
        print("invalid dest")

# performs subtraction and grows the stack
def sub(dest, op1, op2):
    dest = dest
    x = op1
    y = op2
    if dest in Reg:
        # using sub to grow the stack
        if dest == "sp":
            op2 = int(op2)
            if op2 % 4 == 0:
                Reg["sp"] = [None] * int(op2/4)
            else:
                flash("Shucks! You have to grow the stack in multiples of 4!")
                return render_template("home.html")
        else:
            if op1 in Reg:
                x = Reg[op1]
            if op2 in Reg:
                y = Reg[op2]
            if x == None or y == None:
                flash("Whoops! Theres an uninitialized register in a sub instruction!")
                return render_template("home.html")
            Reg[dest] = int(x) - int(y)
    else:
        print("invalid dest")

# dict to store all function calls and tie them to appropriate user input
asm = {"mov":mov, "cmp":cmp, "add":add, "sub":sub, "mul":mul, "str":store, "ldr":ldr}

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
        registers[key] = None
    registers["sp"] = []
