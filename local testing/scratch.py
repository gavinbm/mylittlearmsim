from reg import *

fin = open("input.txt").read().strip('\n').splitlines()
print(f"before\n{Reg}")

# Storing all labels and line numbers in input.txt
getLabels(fin)
# iterate, translate, and execute each line of code
# from input
i = 0
while i < len(fin):
    parsed = parse(fin[i])
    ins = parsed[0]
    #print(parsed)
    print(Labels)
    # handle moving values
    if "mov" in ins:
        dest = parsed[1]
        op1 = parsed[2]
        mov(dest, op1)
    # handle arithmetic
    elif "add" in ins:
        dest = parsed[1]
        op1 = parsed[2]
        op2 = parsed[3]
        add(dest, op1, op2)
    elif "sub" in ins:
        dest = parsed[1]
        op1 = parsed[2]
        op2 = parsed[3]
        sub(dest, op1, op2)
    elif "mul" in ins:
        dest = parsed[1]
        op1 = parsed[2]
        op2 = parsed[3]
        mul(dest, op1, op2)
    # handle comparisons
    elif "cmp" in ins:
        dest = parsed[1]
        op1 = parsed[2]
        cmp(dest, op1)
    # handle branching
    elif "b" in ins:
        if "cbz" in ins or "cbnz" in ins:
            dest = parsed[1]
            cmp(dest, "x8")
            if "cbz" in ins and Flags["eq"] == True:
                i = k
            elif "cbnz" in ins and Flags["eq"] == False:
                i = k
        else:
            if "b." in ins:
                flagCode = parsed[0][2:4]
                if Flags[flagCode]:
                    i = Labels[parsed[1]]
            else:
                i = Labels[parsed[1]]
    # handle storing to stack

    # iteration
    i += 1

print(f"after\n{Reg}")
