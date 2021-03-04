from reg import *

fin = open("input.txt").read().strip("\n").splitlines()
# Storing all labels and line numbers in input
getLabels(fin)

# counter to stop infinite loops
prog_stop = 0
# iterate, translate, and execute each line of input
i = 0
while i < len(fin):
    prog_stop += 1
    if prog_stop > 500:
        print("infinite loop")
        break
        # set registers back to 0, clear flash, give error message
        # and re-render the site
        #resetReg(Reg)
        #session.pop('_flashes', None)
        #flash("you've created an infinite loop! D:")
        #return render_template("home.html", oldcode=oldcode)
    # if line is empty, increment i and skip it
    if fin[i] == "":
        i += 1
        continue
    # parse the line into a list of string lists where
    # first element is the instruction and the others are the
    # corresponding arguments/operands for the instruction
    parsed = parse(fin[i])
    print(parsed)
    # storing instruction into ins var for easier comparisons/use
    ins = parsed[0]

    # checks instruction and passes args to appropriate function
    # stored in the asm dict
    if ":" in ins:
        i += 1
        continue
    if ins in asm and len(parsed) > 3:
        asm[ins](parsed[1], parsed[2], parsed[3])
    elif ins in asm and len(parsed) <= 3:
        asm[ins](parsed[1], parsed[2])

    elif ins in "b|b.eq|b.gt|b.lt|b.le|b.ge|b.ne|cbz|cbz|bl".split("|"):
        if "cbz" in ins:
            if Reg[parsed[1]] == 0:
                i = Labels[parsed[2]]
        elif "cbnz" in ins:
            if Reg[parsed[1]] != 0:
                i = Labels[parsed[2]]
        elif "bl" in ins:
            Reg["lr"] = i # store line number ("address") of next instruction
            i = Labels[parsed[1]] # branch to the label
        else:
            if "b." in ins:
                flagCode = parsed[0][2:4]
                if Flags[flagCode]:
                    i = Labels[parsed[1]]
            else:
                if parsed[1].lower() == "lr": # branch to lr
                    i = Reg["lr"]
                else:
                    i = Labels[parsed[1]]
    # throw error message if non-supported instruction is given
    else:
        print("bad ins")
        break
        #flash(f"Uh Oh! Instruction on line {i + 1} isn't supported!")
        #render_template("home.html", oldcode=oldcode)
    # iteration
    i += 1

print(Reg)
print(Flags)
