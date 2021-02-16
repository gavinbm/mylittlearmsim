from flask import Flask, flash, redirect, url_for, render_template, request, session
from reg import *
#from main import *

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.secret_key = "howdy"

@app.route("/", methods=["GET", "POST"])
def sim():
	if request.method == "POST":
		# if the user assembles their code
		if "assemble" in request.form:
			if request.form["assemble"] == "assemble":
				fin = request.form["input"].splitlines()
				# Storing all labels and line numbers in input.txt
				getLabels(fin)

				# iterate, translate, and execute each line of code
				# from input
				i = 0
				while i < len(fin):
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
				flash(Reg)
				return render_template("home.html")
		# reset the reg values and reload the page
		elif request.form["reset"] == "reset":
			for key in Reg:
				Reg[key] = 0
				redirect(url_for("sim"))

	return render_template("home.html")

if __name__ == "__main__":
	app.run(debug = True)
