*NOTE : FUNCTIONS NAME ARE RENAMED YOUR DISASSEMBLED BINARY WONT LOOK LIKE MINE*  
First, i noticed that the program need 2 inputs  
[*] USERNAME, SERIAL  
Using IDA we got the User which is "4dminUser31337" (Without quotes)  

![IMAGE](https://github.com/BitTheByte/write-ups/blob/master/cybertalents_ezez-keygen/Capture.PNG?raw=true)


The goal is clear we need a valid serial  
by looking to ```main``` function I know that I had to pass the first and second if statement
The first one was easy since it only checking for the length of username and serial  
we have some limits now .. the username need to be less that 30 char. which is okay our ```4dminUser31337``` is only 14 char next the serial need to be less than 100 char which we don't know yet :)  
The second if checks if the length of the serial equal the length of the username but it looks complicated so I wrote a python script using z3 to find the right numbers to satisfy the conditions .. which is [42] Cool ha? we now know the length of the serial  
```python
from z3 import *
s = Solver()
len_input_serial = BitVec("serial_len",128)
s.add(LShR(LShR(0xAAAAAAAAAAAAAAAB * len_input_serial,64),1) + len_input_serial - 3 * LShR(LShR(0xAAAAAAAAAAAAAAAB * len_input_serial,64),1) == 14)
s.add(len_input_serial != 38)
if s.check() == sat:
	print s.model()
```
![IMAGE](https://github.com/BitTheByte/write-ups/blob/master/cybertalents_ezez-keygen/Capturew.PNG?raw=true)  

We still need to find the serial so I looked at ```check_serial``` function
it checks for every 2 chars if there is a "-" or "+" combining this information with the serial length our serial should look like something like this ```AA-AA-AA-AA+AA-AA-AA-AA-AA-AA-AA-AA-AA-AA-``` which every 2 chars converted to hex and multiplicated by 2 and got appended with 0 if there is "-" or 1 if there is "+" 

 looking back to ```check_user``` i saw that the final output of ```check_serial``` should equal to the username
![IMAGE](https://github.com/BitTheByte/write-ups/blob/master/cybertalents_ezez-keygen/Capture22.PNG?raw=true)  
using this python script
```
from itertools import chain, product
def bruteforce(charset, maxlength):
    return (''.join(candidate)
    	for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in xrange(2, maxlength + 1)))
hex_n =  list(bruteforce('0123456789ABCDEF', 2))
username = "4dminUser31337"

for lc in username:
	l = lc.encode("hex")
	if l[0] in list("abcdef"): 
		l=int(l,16)
	elif len(l) > 1:
		if l[1] in list("abcdef"):
			l=int(l,16)
	for h in hex_n:
		strol = hex(2 * int(h,16)).replace("0x","")
		if len(strol) == 3: strol=strol[1:]
		if strol[0] in list("abcdef"): 
			strol=int(strol,16)
		elif len(strol) > 1:
			if strol[1] in list("abcdef"):
				strol=int(strol,16)
		strol_n = str(int(strol) + 0)
		strol_p = str(int(strol) + 1)

		if strol_n == str(l):
			print "{} --> {} from {}".format(lc,strol_n ,h+ "-")
		if strol_p == str(l):
			print "{} --> {} from {}".format(lc,strol_p ,h+ "+")

```
i got ..
```
4 --> 34 from 1A-
4 --> 34 from 9A-
d --> 64 from 32-
d --> 64 from B2-
m --> 109 from 36+
m --> 109 from B6+
i --> 69 from 34+
i --> 69 from B4+
n --> 110 from 37-
n --> 110 from B7-
U --> 55 from 2A+
U --> 55 from AA+
s --> 73 from 39+
s --> 73 from B9+
e --> 65 from 32+
e --> 65 from B2+
r --> 72 from 39-
r --> 72 from B9-
3 --> 33 from 19+
3 --> 33 from 99+
1 --> 31 from 0F+
1 --> 31 from 18+
1 --> 31 from 8F+
1 --> 31 from 98+
3 --> 33 from 19+
3 --> 33 from 99+
3 --> 33 from 19+
3 --> 33 from 99+
7 --> 37 from 1B+
7 --> 37 from 9B+
```

The Final flag range should be known
```
4 = [1A-,9A-]
d = [32-,B2-]
m = [36+,B6+]
i = [34+,B4+]
n = [37-,B7-]
U = [2A+,AA+]
s = [39+,B9+]
e = [32+,B2+]
r = [39-,B9-]
3 = [19+,99+]
1 = [0F+,18+]
1 = [8F+,98+]
3 = [19+,99+]
3 = [19+,99+]
7 = [1B+]
7 = [9B+]
```
  
#FLAG = 1A-32-36+34+37-2A+39+32+39-19+0F+8F+19+19+1B+9B+  
Note that i solved this After the CTF so i don't know the real flag
