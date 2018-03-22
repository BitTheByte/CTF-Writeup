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
```python
from z3 import *

USER = bytearray("4dminUser31337")
FORMAT = ""
SERIAL = [ Int('key[%d]' % i) for i in range(0,len(USER)) ]
s = Solver()

for i in range(0,len(USER)):
	s.add( SERIAL[i]  == USER[i] / 2 )
	if USER[i] % 2 == 0:
		FORMAT += "-"
	else:
		FORMAT += "+"
	s.check()
	
print s.model()
```
Solution was
```
key[8] = 57
key[3] = 52
key[0] = 26
key[4] = 55
key[5] = 42
key[6] = 57
key[1] = 50
key[13] = 27
key[7] = 50
key[9] = 25
key[10] = 24
key[2] = 54
key[11] = 25
key[12] = 25
--++-+++-+++++
```
Soo.. :D
```python
key = [None] * 14
key[8] = 57
key[3] = 52
key[0] = 26
key[4] = 55
key[5] = 42
key[6] = 57
key[1] = 50
key[13] = 27
key[7] = 50
key[9] = 25
key[10] = 24
key[2] = 54
key[11] = 25
key[12] = 25
FORMAT = "--++-+++-+++++"
for i in range(len(key)):
	print hex(key[i])[-2:]+FORMAT[i],
```
  
#FLAG = 1a-32-36+34+37-2a+39+32+39-19+18+19+19+1b+


