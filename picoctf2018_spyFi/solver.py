from pwn import *
import re
import string
from collections import Counter

context.log_level = 'error'
block_len = 32 # for hex
def sendpayload(payload):
	io = remote("2018shell2.picoctf.com", 31123)
	io.recvuntil("report: ")
	io.sendline(payload)
	res = io.recvline()
	res_len = len(res)
	io.close()
	return res,res_len

def toBlocks(data):
	return re.findall("."*block_len,data)

def isdub(arr):
	bbb_enc = "5e6605d02027026603b6f00863d32bc5"
	cont    = Counter(arr)
	try:
		del cont[bbb_enc]
	except:
		pass
	for key in cont:
		if cont[key] > 1:
			return 1
	return 0

	
plaintext =  "ying code is: p"
pad       =  "bbbbbbbbbbbbbbbb"
pad       += "bbbbbbbbbbbbbbbb"
pad       += "bbbbbbbbbbbbbbb"

flag       = "p"
for _ in range(len(pad)):
	for brute_char in string.printable:

		payload = "a" * 11
		payload += plaintext + brute_char
		payload += pad

		data,length = sendpayload(payload)
		blocks = toBlocks(data)

		if isdub(blocks) == 1:
			print "[*] plaintext -> %s " % brute_char

			plaintext  =  plaintext[1::]
			plaintext  += brute_char
			pad    =  pad[1::]
			flag += brute_char
			print "="*30
			print flag
			print payload
			print plaintext
			print "="*30
			break

