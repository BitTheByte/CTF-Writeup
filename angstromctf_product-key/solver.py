from z3 import *

def sumchar(a, a1, a2, a3):
    return sum(a[i] for i in range(a1, a2, a3))
 
 
def swap(a, a1, a2):
    a[a1], a[a2] = a[a2], a[a1]
    return a

s = Solver()
key = [Int('key[%d]' % i) for i in range(6)]
name_ptr = bytearray("Artemis Tosini")
email_ptr = bytearray("artemis.tosini@example.com")
final = [0x7f8, 0x1780, 0xb94, 0x1f8, 0xb4b, 0x11f8]
pad   = [0x77,0x3C,0x1E,0x6B,0x39,0x13,0x22,0x0F,0x24,0x2,0x73,0x59,0x67,0x64,0x21,0x73,0x17,0x1E,0x6D,0x5B,0x4,0x66,0x65,0x51,0x5B,0x43,0x57,0x27,0x0E,0x6A,0x0F,0x6D,0x2F,001,0x48,0x44,0x3B,0x8,0x5E,0x80,0x4E,0x1F,0x27,0x11,0x33,0x46,0x33,0x4A,0x25,0x5E,0x33,0x32,0x28,0x60,0x6E,0x6,0x1F,0x28,0x43,0x7D,0x57,0x32]

v10 = 0
for i in range(0,32-len(email_ptr)):
	email_ptr.append(pad[i])
	v10 += 1

for i in range(0,32-len(name_ptr)):
	name_ptr.append(pad[i + v10])

for i in range(32):
	email_ptr[i] ^= 5
	name_ptr[i] ^= 0xF

for i in range(6):
    v5 = sumchar(email_ptr, 0, 32, i + 2)
    key[i] -= ((sumchar(email_ptr, i + 1, 32, i + 2) * v5) & 0x7fffffff) % 10000
    v6 = sumchar(name_ptr, 0, 32, 2)
    key[i] += 4 * (v6 - sumchar(name_ptr, 1, 32, 2))

swap(key, 3, 4)
swap(key, 2, 5)
swap(key, 1, 5)
swap(key, 2, 3)
swap(key, 0, 5)
swap(key, 4, 5)

for i in range(6):
    key[i] += sumchar(name_ptr, 0, 32, 1)
    key[i] += sumchar(email_ptr, 0, 32, 1)
 
for i in range(6):
    v7 = sumchar(email_ptr, 4 * i, 4 * i + 1, 1)
    key[i] += v7 % sumchar(name_ptr, 4 * i + 2, 4 * i + 3, 1)
 
for i in range(6):
    s.add(final[i] == key[i])
    s.check()
print s.model()

#KEY = 3914-6104-4611-1711-1243-4699

