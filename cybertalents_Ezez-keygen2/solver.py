USERNAME = "4dminUser31337"

def getIndex(s,s1):
	for x, i in enumerate(s1):
		if s == i:
			return x

def getBin(a1):
	return format(a1,"b").rjust(4,"0")

def getuser(a1):
	v11 = [0]*len(USERNAME)
	v3 = 0
	for  i in range(0,len(str(a1)),2):
		v1 = getIndex(a1[i], 'AFECWQPXIGJTUBN%')
		v2 = getIndex(a1[i + 1], 'cpqowuejfnvhzbx$')
		v7 = getBin(v1)
		v8 = getBin(v2)
		nptr = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
		  	if ( j & 1 ):
				v3 = v8[j / 2]
			else:
				v3 = v7[j / 2]
			nptr[j] = v3
		nptr = ''.join(str(e) for e in nptr)
		v11[i / 2] = int(nptr, 2)
	return v11


def find(xl):
	r1 = [0x41,0x46,0x45,0x43,0x57,0x51,0x50,0x58,0x49,0x47,0x4a,0x54,0x55,0x42,0x4e,0x25]
	r2 = [0x63,0x70,0x71,0x6f,0x77,0x75,0x65,0x6a,0x66,0x6e,0x76,0x68,0x7a,0x62,0x78,0x24]
	for r_1 in r1:
		for r_2 in r2:
			x =  chr(r_1)+chr(r_2)
			r = x + ("Fq" * (len(USERNAME)-2))
			r = getuser(r)
			if r[0] == ord(xl):
				return x
	return "[00]"

flag = ""
for i in USERNAME:
	flag += find(i)

print "flag{" + flag + "}"
