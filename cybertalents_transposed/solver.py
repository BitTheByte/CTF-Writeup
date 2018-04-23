import random
def reverse_message(msg):
	msg = msg[-1:] + msg[:-1]
	xmsg = ""
	for i in range(0,21):
		try:
			xmsg += msg[i]
			xmsg += msg[i+21]
		except:
			pass
	msg = xmsg[-1:] + xmsg[:-1]
	return msg
def reverse_loop(msg,perm):
	final = ""
	for x in [7,14,21,28,35,42]:
		block = list(msg[x-7:x])
		if block == []:
			break
		dblock =  [0,0,0,0,0,0,0]
		for i in range(0,len(perm)):
			dblock[perm[i]] = block[i]
		final += ''.join(dblock)
	return final
def decrypt(x,perm):
	enc = x
	for i in xrange(100):
		enc = reverse_message(reverse_loop(enc,perm))
		if i == 99:
			return enc
prev = []
while(1):
	perm = range(7)
	random.shuffle(perm)
	if perm not in prev:
		FLAG = "L{NTP#AGLCSF.#OAR4A#STOL11__}PYCCTO1N#RS.S"
		flag = decrypt(FLAG,perm)
		if "FLAG" == flag[:4]:
			print flag
			break
		prev.append(perm)
