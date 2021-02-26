from flask import Flask, flash, redirect, url_for, render_template, request, session
from reg import *

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.secret_key = "armsimweb"

@app.route("/", methods=["GET", "POST"])
def sim():
    if request.method == "POST":
        # if the user assembles their code
        if "assemble" in request.form:
            if request.form["assemble"] == "assemble":
                oldcode = request.form["input"]
                fin = oldcode.strip("\n").splitlines()
                # Storing all labels and line numbers in input
                getLabels(fin)

                # counter to stop infinite loops
                prog_stop = 0
                # iterate, translate, and execute each line of input
                i = 0
                while i < len(fin):
                    prog_stop += 1
                    if prog_stop > 500:
                        resetReg(Reg)
                        flash("you've created an infinite loop! D:")
                        return render_template("home.html", oldcode=oldcode)
                    parsed = parse(fin[i])
                    ins = parsed[0]
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
                    if "b" in ins:
                        if "cbz" in ins:
                            if Reg[parsed[1]] == 0:
                                i = Labels[parsed[2]]
                        elif "cbnz" in ins:
                            if Reg[parsed[1]] != 0:
                                i = Labels[parsed[2]]
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
                flash(beautify(Reg))
                return render_template("home.html", oldcode=oldcode)
        # reset the reg values and reload the page
        elif request.form["reset"] == "reset":
            resetReg(Reg)
            redirect(url_for("sim"))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
