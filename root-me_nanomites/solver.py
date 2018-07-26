from z3 import *

check_list = [0x0B,0x6E,0x42,0x14,0x54,0x34,0x1D,0x6E,0x4A,0x26,0x36,0x30,0x2F,0x6D,0x30,0x38,0x58,0x31,0x41,0x74,0x41,0x4A,0x6A,0x65,0x53,0x5F,0x33,0x5C,0x49,0x33,0x65,0x34,0x37,0x6E,0x64,0x73,0x77,0x79,0x66]

user_input = [BitVec('k[%d]'%i,32) for i in range(12+1)]
s = Solver()
for i in range(len(user_input)):
	s.add(user_input[i] < 0x100 , user_input[i] > 0x20)

for i in range(12+1):
	s.add( check_list[3 * i + 1 + i % 2] == user_input[i] )
flag = ""
if s.check() == sat:
	u = s.model()
	for i in range(len(u)):
		aq = s.model()[user_input[i]]
		aq = int(str(aq))
		flag += chr(aq)
print flag
