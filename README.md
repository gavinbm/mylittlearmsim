# lil armsim

A class on machine organization I took last semester used an armv8 simulator to grade our code for quizzes
and I thought it was cool so I decided to give it a shot. It's not the most efficient or robust system but
it's been a fun way to try my hand at writing an "interpreter."

Completed features:
 - arithmetic (add, sub, mul, no div)
 - mov
 - labels, cmp, and branching (cbz/cbnz still work in progress, b, b.gt, b.lt, b.eq, b.ge, b.le) 

Future features (hopefully):
 - str, ldr, and working stack and heap
 - printing and handling strings
 - some css to make it less ugly
