# lil armsim

This is officially LIVE at https://mylittlearmsim.com/

A class on machine organization I took last semester used an armv8 simulator to grade our code for quizzes
and I thought it was cool so I decided to give it a shot. It's not the most efficient or robust system but
it's been a fun way to try my hand at writing an "interpreter."

NOTE: The local testing folder only exists for me to run the simulator in a terminal to make print statements
      easier to read and so I don't have to start a flask server everytime I want to test something

Completed features:
 - arithmetic (add, sub, mul, no div)
 - mov
 - labels, cmp, and branching (cbz, cbnz, bl, b, b.gt, b.lt, b.eq, b.ge, b.le)
 - grow, shrink, str, and ldr the stack pointer (str/ldr don't work with other registers, just sp)
 - comments (single-line, denoted by "@") get removed and don't mess up code execution

Sample Programs:
These will show most of the features that are completed thus far.

1) finds the x0th fibonacci number (edit line 2 to change which one) iteratively
```assembly
main:
      mov x0, 10
      mov x1, #1
      mov x2, #1
      mov x3, #0
      START:
            cmp x0, x1
            b.gt LOOP
            b.eq END
      LOOP:
            add x4, x2, x3
            mov x3, x2
            mov x2, x4
            add x1, x1, #1
            b START
      END:
            mov x0, x4
 ```
2) example of how to use bl and branch with lr (conditions not supported)
```assembly
mov x1, 2
.here:
    mov x0, x1
    bl .there
    add x1, x1, 10
    b .end
.there:
    mov x1, 5
    b lr
.end:
```
3) example of using the stack to str/ldr values
```assembly
sub sp, sp, 16
mov x1, 1
str x1, [sp, 8]
ldr x0, [sp, 8]
add sp, sp, 16
```
Future features (hopefully):
 - str/ldr for registers other than sp
 - svc, more robust stack, and heap limits
 - adds, subs, and (bitwise) instructions
 - printing and handling strings
 - animated visual for stack changes
 - recursion
 - some css to make it less ugly

# Making Your Own
I made this using flask and python 3.8.6, reg.py holds all the ARM-esque logic like registers, labels, functions, etc.
views.py has one view in it, sim, which gets code from the textarea in templates/home.html and uses
the parsing function from reg.py to parse the code and call the right functions from reg.py

The site is hosted on a Linode server running Ubuntu 20.04 LTS and I'm using Nginx and uWSGI to actually
get HTTP requests to the app. Basic tutorial on setting that up [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)
