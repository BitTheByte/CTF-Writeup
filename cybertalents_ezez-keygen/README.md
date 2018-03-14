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
s.add(LShR(LShR(0xAAAAAAAAAAAAAAABL * len_input_serial,64),1) + len_input_serial - 3 * LShR(LShR(0xAAAAAAAAAAAAAAABL * len_input_serial,64),1) == 14)
s.add(len_input_serial != 38)
if s.check() == sat:
	print s.model()
```
![IMAGE](https://github.com/BitTheByte/write-ups/blob/master/cybertalents_ezez-keygen/Capturew.PNG?raw=true)  

We still need to find the serial so I looked at ```check_serial``` function
it checks for every 2 chars if there is a "-" or "+" combining this information with the serial length our serial should look like something like this ```AA-AA-AA-AA+AA-AA-AA-AA-AA-AA-AA-AA-AA-AA-``` which every 2 chars converted to hex and multiplicated by 2 and got appended with 0 if there is "-" or 1 if there is "+" 

 looking back to ```check_user``` i saw that the final output of ```check_serial``` should equal to the username
![IMAGE](https://github.com/BitTheByte/write-ups/blob/master/cybertalents_ezez-keygen/Capture22.PNG?raw=true)  
i dont know how to reverse C strtol :) to i decied to write simple C program
```C
#include <stdio.h>
int main(int argc, char **argv)
{
  int i;
  char v2 = "0";
  char v;
  char * ff[] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1A", "1B", "1C", "1D", "1E", "1F", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3A", "3B", "3C", "3D", "3E", "3F", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "4A", "4B", "4C", "4D", "4E", "4F", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "5A", "5B", "5C", "5D", "5E", "5F", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "6A", "6B", "6C", "6D", "6E", "6F", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "7A", "7B", "7C", "7D", "7E", "7F", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "8A", "8B", "8C", "8D", "8E", "8F", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "9A", "9B", "9C", "9D", "9E", "9F", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "AA", "AB", "AC", "AD", "AE", "AF", "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BA", "BB", "BC", "BD", "BE", "BF", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CA", "CB", "CC", "CD", "CE", "CF", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DA", "DB", "DC", "DD", "DE", "DF", "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "EA", "EB", "EC", "ED", "EE", "EF", "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "FF"};
  for (i = 0;i < sizeof(ff);i++){
    v = 2 * strtol(ff[i], 0LL, 16) + v2;
    printf("%s/%d\n",ff[i],v);
  }
  return 0;
}
```
I ran the program two times one with v2="0" and v2="1" and saved the output
Now we only need to find the right value in hex to get the username chars  
using python ```$ python -c "print '4'.encode('hex')"``` i got `34`  
So i wrote python script to handle that for me 
Wait! What about the "+" and "-" .. don't worry i'll tell you remember when you use v2="0" thats mean its "-" and v2="1" it's "+"
```
[!] Values to get 34 (in HEX)
 -> E6-
 -> 1A-
 -> 66-
 -> 9A-
[!] Values to get 64 (in HEX)
 -> B2-
 -> 32-
 -> CE-
 -> 4E-
[!] Values to get 109 (in HEX)
 -> 36+
 -> 49+
[!] Values to get 69 (in HEX)
 -> B4+
 -> 34+
 -> CB+
 -> 4B+
[!] Values to get 110 (in HEX)
 -> 37-
 -> 49-
 -> C9-
 -> B7-
[!] Values to get 55 (in HEX)
 -> 2A+
 -> 55+
 -> AA+
 -> D5+
[!] Values to get 73 (in HEX)
 -> B9+
 -> 39+
 -> C6+
 -> 46+
[!] Values to get 65 (in HEX)
 -> B2+
 -> 32+
 -> CD+
 -> 4D+
[!] Values to get 72 (in HEX)
 -> B9-
 -> 39-
 -> C7-
 -> 47-
[!] Values to get 33 (in HEX)
 -> E6+
 -> 66+
 -> 99+
 -> 19+
[!] Values to get 31 (in HEX)
 -> 67+
 -> E7+
 -> 98+
 -> 18+
[!] Values to get 33 (in HEX)
 -> E6+
 -> 66+
 -> 99+
 -> 19+
[!] Values to get 33 (in HEX)
 -> E6+
 -> 66+
 -> 99+
 -> 19+
[!] Values to get 37 (in HEX)
 -> 64+
 -> E4+
 -> 1B+
 -> 9B+
```

The Final flag range should be   
c_34  = ["E6-","1A-","66-","9A-"]#4  
c_64  = ["B2-","32-","CE-","4E-"]#d  
c_109 = ["36+","49+"]            #m  
c_69  = ["B4+","34+","CB+","4B+"]#i  
c_110 = ["37-,""49-","C9-","B7-"]#n  
c_55  = ["2A+","55+","AA+","D5+"]#u  
c_73  = ["B9+","39+","C6+","46+"]#s  
c_65  = ["B2+","32+","CD+","4D+"]#e  
c_72  = ["B9-","39-","C7-","47-"]#r  
c_33  = ["E6+","66+","99+","19+"]#3  
c_31  = ["67+","E7+","98+","18+"]#1  
c_33  = ["E6+","66+","99+","19+"]#3  
c_33  = ["E6+","66+","99+","19+"]#3  
c_37  = ["64+","E4+","1B+","9B+"]#7  
  
#FLAG = 1A-B2-36+34+37-AA+39+32+B9-99+98+19+19+9B+  
Note that i solved this After the CTF so i don't know the real flag
