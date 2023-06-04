import re
import string
import base64



asm = open('ch30.asm','r').readlines()

def asmflit(s):
	s  = s.split(',')
	s = s[1]
	s = s.translate( None, string.whitespace )
	if ';' in s:
		s = s.split(";")[0]
	if 'h' in s:
		s = s.replace("h","")
	try:
		int(s,16)
	except:
		return "NOT_HEX"
	return f'0x{s}'
def getData(asm,i='linux'):
	MOV_INS   = []
	XOR_INS   = []
	if i == 'linux':
		CMP_RBP_EAX_REGEX = re.compile('                cmp     eax, \[rbp-8\]')
		MOV_RBP_REGEX 	  = re.compile('                mov     dword ptr \[rbp-8\], (.*?)')
		XOR_EAX_REGEX 	  = re.compile('                xor     eax, (.*?)')
		XOR_AL_REGEX  	  = re.compile('                xor     al, (.*?)')
	if i == 'windows':
		CMP_RBP_EAX_REGEX = re.compile('                cmp     eax, \[ebp\+var_8\]')
		MOV_RBP_REGEX 	  = re.compile('                mov     \[ebp\+var_8\], (.*?)')
		XOR_EAX_REGEX 	  = re.compile('                xor     eax, (.*?)')
		XOR_AL_REGEX  	  = re.compile('                xor     al, (.*?)')

	for i in asm:
		MOV 	= MOV_RBP_REGEX.match(i)
		XOR 	= XOR_AL_REGEX.match(i)
		XOR_EAX = XOR_EAX_REGEX.match(i)
		CMP 	= CMP_RBP_EAX_REGEX.match(i)

		if MOV != None:
			val = asmflit(i)
			if val != "NOT_HEX":
				MOV_INS.append(val)
		if XOR != None:
			val = asmflit(i)
			if val != "NOT_HEX":
				XOR_INS.append(val)
		if XOR_EAX != None:
			val = asmflit(i)
			if val != "NOT_HEX":
				XOR_INS.append(val)
		if CMP != None:
			if len(MOV_INS) > len(XOR_INS):
				XOR_INS.append("0x00")

	return MOV_INS,XOR_INS


data = getData(asm,'linux')
mov=  data[0]
xor=  data[1]
output  = ""
for i in xrange(len(mov)):
	output += chr( (int(mov[i],16) ^ int(xor[i],16)))
output = base64.b64decode(output)
open("win.exe","wb").write(output)

print "[!] Decoded ch30 to win.exe"
print "[!] Get ASM from ida and rename it to ch30_win.asm"
raw_input("[#] Press enter when you ready!")

asm = open('ch30_win.asm','r').readlines()
data = getData(asm,'windows')
mov=  data[0]
xor=  data[1]
output  = ""
for i in xrange(len(mov)):
	output += chr( (int(mov[i],16) ^ int(xor[i],16)))
print output
raw_input('[!] Finished')
