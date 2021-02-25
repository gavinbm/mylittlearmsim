# lil armsim

A class on machine organization I took last semester used an armv8 simulator to grade our code for quizzes
and I thought it was cool so I decided to give it a shot. It's not the most efficient or robust system but
it's been a fun way to try my hand at writing an "interpreter."

NOTE: The local testing folder only exists for me to run the simulator in a terminal to make print statements
      easier to read and so I don't have to start a flask server everytime I want to test something

Completed features:
 - arithmetic (add, sub, mul, no div)
 - mov
 - labels, cmp, and branching (b, b.gt, b.lt, b.eq, b.ge, b.le) (*cbz/cbnz still WiP)

Future features (hopefully):
 - str, ldr, svc, and working stack and heap
 - printing and handling strings
 - animated visual for stack changes
 - some css to make it less ugly
