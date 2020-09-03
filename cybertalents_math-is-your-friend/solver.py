from z3 import *

solver = z3.Solver()
password = [BitVec("c_%i" % i ,32)  for i in range(9)]
for char in password:
    solver.add(char >= 0 , char <= 127)

v6 = [0x4F,0x8,0x1D,0x3A,0x51,0x15,0x31,0x7B,0x72]
for i in range(0,3):
    for j in range(0,3):
        v4 = 0
        for k in range(0,3):
            v4 = (password[3 * k + j] * v6[3 * i + k] + v4) % 127
        if i == j:
            solver.add(v4 == 1)
        else:
            solver.add(v4 == 0)

if solver.check() == sat:
    model = solver.model()    
    for char in range(len(password)):
        password[char] = model[password[char]].as_long()
    
    print(''.join([chr(x) for x in password]))

__import__("IPython").embed()
