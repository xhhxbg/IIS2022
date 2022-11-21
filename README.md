# IIS2022

https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/stack-intro/

# Method 1 ret2text
反编译得到overflow函数中copy字符串距离ebp的长度为0x30
输入'a' * 0x30 + 'b' * 0x08 + 0x000000000040121E 填充
将返回地址修改为 system 指令所在地址

# Method 2 ret2shellcode
通过scanf将copy字符串中填充为shellcode
再通过输入溢出将返回地址替换为country的地址 0x403580 (.bss段)
跳转到 0x403580 后运行机器码
进行system系统调用运行'/bin/sh'

# Method 3 ret3syscall
https://www.dazhuanlan.com/zhjnlb/topics/1242953
ROPgadget --binary bigwork --only "pop|ret" | grep "rax"
未找到 rax 的控制代码

# Method 4 ret2libc
https://cooprint systeml-y.github.io/2019/07/16/linux-pwn-32/
ROPgadget --binary ../src/bigwork --string '/bin/sh'
