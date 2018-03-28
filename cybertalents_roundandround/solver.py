from z3 import *
flag = [0x726F756E, 0xCABEE660, 0xDDC1997D, 0xAA93C38B, 0x87E21216]

def ROTATE_CHIPHER(txt,key):
	if ( txt > 96 and txt <= 122 ):
		return (txt - 0x61 - key) % 26 + 0x61
	if ( txt <= 64 or txt > 90 ):
		return txt
	return (txt - 0x41 - key) % 26 + 0x41

def encrypt(a1,a2):
	return (a1 << (a2 & 0x1F)) | (a1 >> (-(a2 & 0x1F) & 0x1F))

s =  Solver()
for i in range(0,5):
	s.reset()
	k = BitVec("k",32)
	s.add(	encrypt(k, i) == flag[i])
	s.check()
	k =  int(str(s.model()[k]))
	k = bytearray( ( hex(k).replace("0x","").replace("L","") ).decode("hex") )
	for x in k:
		print chr(ROTATE_CHIPHER(x,i)),


#def decrypt(a1,a2):
#	return (a1 >> (a2 & 0x1F)) | (a1 >> (-(a2 & 0x1F) & 0x1F))
#for i in range(0,5):
#	k =  int(decrypt(flag[i], i))
#	k = bytearray( ( hex(k).replace("0x","").replace("L","") ).decode("hex") )
#	for x in k:
#		print chr(ROTATE_CHIPHER(x,i)),


