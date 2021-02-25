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
 - labels, cmp, and branching (b, b.gt, b.lt, b.eq, b.ge, b.le) (*cbz/cbnz still WiP)
 - comments get removed and don't mess up code execution

Sample Program:
This shows some of every complete feature listed above.
Finds the x0th fibonacci number and moves it into x0

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
 
Future features (hopefully):
 - str, ldr, svc, and working stack and heap
 - adds, subs, and (bitwise) instructions
 - printing and handling strings
 - animated visual for stack changes
 - some css to make it less ugly
