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
                        # set registers back to 0, clear flash, give error message
                        # and re-render the site
                        resetReg(Reg)
                        session.pop('_flashes', None)
                        flash("you've created an infinite loop! D:")
                        return render_template("home.html", oldcode=oldcode)
                    # parse the line into a list of strings
                    parsed = parse(fin[i])
                    # first entry of parsed will be arm instruction
                    ins = parsed[0]

                    # checks instruction and passes args to appropriate function
                    # stored in the asm dict
                    print(parsed)
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
                            Reg["lr"] = i + 1
                            k = Labels[parsed[1]]

                        else:
                            if "b." in ins:
                                flagCode = parsed[0][2:4]
                                if Flags[flagCode]:
                                    i = Labels[parsed[1]]
                            else:
                                i = Labels[parsed[1]]
                    # throw error message if non-supported instruction is given
                    else:
                        flash(f"Uh Oh! Instruction on line {i + 1} isn't supported!")
                        render_template("home.html", oldcode=oldcode)
                    # iteration
                    i += 1
                flash(beautify(Reg))
                return render_template("home.html", oldcode=oldcode)
        # reset the reg values and reload the page
        elif request.form["reset"] == "reset":
            resetReg(Reg)
            session.pop('_flashes', None)
            redirect(url_for("sim"))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
