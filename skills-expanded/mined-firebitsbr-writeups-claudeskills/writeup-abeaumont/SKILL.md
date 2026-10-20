<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-abeaumont
description: CTF writeups and security challenges by abeaumont.
---

# Writeups by abeaumont

Source repository: `/repos/abeaumont`

## Repository Index

- ctfs/README.md
- ctfs/codegate-quals-2018/README.md
- ctfs/hackim-2018/README.md
- ctfs/hackit-2019/README.md
- ctfs/plaidctf-2019/README.md
- ctfs/sharif-2018/README.md
- ctfs/swampctf-2019/README.md
- ctfs/swampctf-2019/needle-eyes-apprentice/README.md
- ctfs/sharif-2018/client01/README.md
- ctfs/sharif-2018/el-gamat/README.md
- ctfs/sharif-2018/fhash/README.md
- ctfs/sharif-2018/fifteen-puzzle/README.md
- ctfs/sharif-2018/oss-service-easy/README.md
- ctfs/sharif-2018/oss-service-hard/README.md
- ctfs/plaidctf-2019/docker/README.md
- ctfs/plaidctf-2019/eulernt/README.md
- ctfs/plaidctf-2019/everland/README.md
- ctfs/plaidctf-2019/horst/README.md
- ctfs/hackit-ge-2020/hackit3/README.md
- ctfs/hackit-2019/hackit3/README.md
- ctfs/hackit-2019/hackit5/README.md
- ctfs/hackim-2018/yasc/README.md
- ctfs/codegate-quals-2018/miro/README.md

## Writeup Content


### File: ctfs/README.md

# Writeups and solutions to CTF tasks




### File: ctfs/codegate-quals-2018/README.md

# Solutions to some Codegate Preliminary CTF challenges

You can also check the [official site](https://quals.codegate.kr/),
[CTFtime site](https://ctftime.org/event/542)
and additional [writeups](https://ctftime.org/event/542/tasks/).

This repo contains the following solutions:

* [Miro](miro) (Crypto 404)



### File: ctfs/codegate-quals-2018/miro/README.md

# Miro (crypto 404)

The task consists of two files, [client.py](client.py) and [miro.pcap](miro.pcap).

The python code is a TLS client that connects to a server
and plays a simple maze-like game, with for actions (up, down, left, right).

The problem is that the actions are encoded, and only 2 of them are available:

```python
    if user_input == "u":
        print "Sorry.. Not support function.."
        exit()
    elif user_input == "d":
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        print "Sorry.. Not support function.."
        exit()
```

We don't know how to go up or left and we need those actions to solve the maze.

On the other hand, we have a pcap file with another maze solving session,
so we can check there what the encodings for up and left actions are.
The problem is that, of course, that session is encrypted
and we need to decipher it first.

To do so, we first get the server certificate, either by looking at the pcap file
or connecting to the server (i. e. `openssl s_client -connect ch41l3ng3s.codegate.kr:443`)

From the certificate, we extract both the RSA exponent (e = 65537) and modulus (n = 0x01c20bdc017e3caa3c579b40d439e2ecd70f12c4d7f2764784c95a3fddba00981ba9ce5b227ade47b0a7a0a8acaba4541ab95c52f6b6de3df9ec090c6c356445b21be437abe10214d0b4a398a96743bbf70c864687fb2ec929f01d6edab2d987fe09799ad2204a2704f33061dbf9c2e03b332f0ba1a446644c864a06cd586d480b)

Using [yafu](https://sourceforge.net/projects/yafu/), we factorize it to get `p` and `q`:

```
> yafu factor\(0x01c20bdc017e3caa3c579b40d439e2ecd70f12c4d7f2764784c95a3fddba00981ba9ce5b227ade47b0a7a0a8acaba4541ab95c52f6b6de3df9ec090c6c356445b21be437abe10214d0b4a398a96743bbf70c864687fb2ec929f01d6edab2d987fe09799ad2204a2704f33061dbf9c2e03b332f0ba1a446644c864a06cd586d480b\)


fac: factoring 316033277426326097045474758505704980910037958719395560565571239100878192955228495343184968305477308460190076404967552110644822298179716669689426595435572597197633507818204621591917460417859294285475630901332588545477552125047019022149746524843545923758425353103063134585375275638257720039414711534847429265419
fac: using pretesting plan: normal
fac: no tune info: using qs/gnfs crossover of 95 digits
div: primes less than 10000
fmt: 1000000 iterations
Total factoring time = 1.2601 seconds


***factors found***

P155 = 17777324810733646969488445787976391269105128850805128551409042425916175469483806303918279424710789334026260880628723893508382860291986009694703181381742497
P155 = 17777324810733646969488445787976391269105128850805128551409042425916175469168770593916088768472336728042727873643069063316671869732507795155086000807594027

ans = 1

```

With this, we generate the private key:

```python
from Crypto.PublicKey import RSA

n = 0x01c20bdc017e3caa3c579b40d439e2ecd70f12c4d7f2764784c95a3fddba00981ba9ce5b227ade47b0a7a0a8acaba4541ab95c52f6b6de3df9ec090c6c356445b21be437abe10214d0b4a398a96743bbf70c864687fb2ec929f01d6edab2d987fe09799ad2204a2704f33061dbf9c2e03b332f0ba1a446644c864a06cd586d480bL
e = 65537L
p = 17777324810733646969488445787976391269105128850805128551409042425916175469483806303918279424710789334026260880628723893508382860291986009694703181381742497L
q = 17777324810733646969488445787976391269105128850805128551409042425916175469168770593916088768472336728042727873643069063316671869732507795155086000807594027L

phi = (p - 1) * (q - 1)
d = pow(e, phi - 2, phi)
key = RSA.construct((n, e, d, p, q))
open('priv.key', 'w').write(key.exportKey('PEM'))
```

Adding the generated [private key](priv.key) to Wireshark we can now decipher the session and update the client:

```python
from socket import *
from ssl import *
import time

def recv_until(s, string):
    result = ''
    while string not in result:
        result += s.recv(1)
    return result

client_socket=socket(AF_INET, SOCK_STREAM)
tls_client = wrap_socket(client_socket, ssl_version=PROTOCOL_TLSv1_2, cert_reqs=CERT_NONE)
print tls_client
print tls_client.context.cert_store_stats()

print "[+] Connecting with server.."

tls_client.connect(('ch41l3ng3s.codegate.kr',443))

print "[+] Connect OK"

while 1:
    data = recv_until(tls_client, "Input : ")
    print data
    user_input = raw_input()

    if user_input == "u":
        tls_client.send("9de133535f4a9fe7de66372047d49865d7cdea654909f63a193842f36038d362\n")
    elif user_input == "d":
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        tls_client.send("27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2\n")
    else:
        print "Invalid input!"
        exit()

client_socket.shutdown(SHUT_RDWR)
client_socket.close()
```

That's it, now we can run the [solver.py](solver.py), escape the maze, and get the flag.



### File: ctfs/hackim-2018/README.md

# Solutions to some nullcon HackIM CTF challenges

You can also check the [official site](https://ctf.nullcon.net/),
[CTFtime site](https://ctftime.org/event/566)
and additional [writeups](https://ctftime.org/event/566/tasks/).

This repo contains the following solutions:

* [yasc](yasc) (RE 300)



### File: ctfs/hackim-2018/yasc/README.md

# yasc (RE 300)

The task only provides a [binary file](yasc).

If we analyze or run it, we can see that it reads a input string
and it validates that the input string is the expected one.
If that's the case, it prints the flag.

The input string is composed of 24 blocks where
each block consists in a character and a sequence of numbers.
The length of this sequence of numbers is the index of the block
(that is, from 1 to 24).

That is, if we use `C` for any character and `D` for any digit,
the string has the following format (without spaces):

`C1 D1 C2 D2_1 D2_2 C3 D3_1 D3_2 D3_3 ... C24 D24_1 ... D24_24`

The character of every block is compared against the string `LeIa1SE#g@scn$mrhGipNtl!`,
so that determines what each character is.

For the digits, each block is processed differently.
The xor of all the digits in the sequence is calculated,
resulting in a sequence of 24 integers.

This integers must be a permutation of size 24 of the range [0, 23],
and when used the block's value as an index for the string `LeIa1SE#g@scn$mrhGipNtl!`,
the resulting character must match with the one in the string `SimplestrIngchaL1ENG!@#$`,
indexed by block's number (starting with 0).

If these validations success, both an MD5 and a SHA1 hash is calculated with this information
(for each block, the character and the block value as a 32bit integer).
If the MD5 matches with a predefined hash value,
an encrypted flag is then XORed with the obtained SHA1 to decrypt the flag and print it.

The [solver](solver.py) shows how this process is done.



### File: ctfs/hackit-2019/README.md

# Solutions for Euskal Encounter 2019's Hackit challenges

This repo contains the following solutions:

- [hackit3](hackit3/README.md)
- [hackit5](hackit5/README.md)



### File: ctfs/hackit-2019/hackit3/README.md

# Hackit 3

We are just given a [dump](dump) file.

A file check tells us it's a PCAP file:

```sh
$ file dump
dump: pcap capture file, microsecond ts (little-endian) - version 2.4 (Linux cooked v1, capture length 262144)
```

Checking for strings yields the following result:

```sh
$ strings -12 dump
generic.movementSpeed?
generic.movementSpeed?
```

Opening the file with Wireshark or analyzing it with Scapy we can get some additional relevant information:

```python
>>> x = rdpcap('dump')
>>> x
<dump: TCP:9844 UDP:0 ICMP:0 Other:0>
>>> x[0].dport
25565
```

With both the string and the port used we can deduce it's a Minecraft capture.  
Knowing this, we attempted to use a Minecraft dissector for Wireshark,
but the ones available are too old and don't work properly.

This is quite understandable considering that the Minecraft protocol is rather unstable,
the captured session corresponds to the version 404 of the protocol, which is the current stable one at the time of writing this.

So, we considered using some existing tool unfeasible and just went and learnt about the protocol,
which is quite comprehensibly defined at https://wiki.vg/Protocol

After dealing for a while with both `VarInt` specification and packet format
(according to https://wiki.vg/Protocol#Without_compression, we should only see a single length field,
but we were seeing two of them, as defined in https://wiki.vg/Protocol#With_compression,
even for uncompressed data), we saw that only a reduced subset of the packet types were being used, most notably:

- from client to server:
  - player position
  - player position and look
  - player look
- from server to client:
  - chunk_data
  - unload_chunk

So, basically, client to server communication consists of information about the player and
server to client communication consists of information about the map.

We initially thought the flag could be in the map, so we reversed the server to client communication first.  
After dealing with the chunk format, analyzing their bitmasks, palettes, positions, lights and biomes we realized
there was no simple way to get the flag from there, so we switched to look at the client messages.

After decoding client messages, the position of the player seemed like the most relevant information.
It consists of the 3D coordinates (`X`, `Y`, `Z`, with `Y` being the height)
and a boolean flag indicating whether the player is in the ground.

We saw how the position of the player was continously changing,
so drawing that position seems like a good idea.
Minecraft is 3D though, so we have to consider if we want to draw positions in 3D or use a simpler 2D.

Analyzing the height coord (`Y`), we could see how it barely changed
(it was either `4.0` or `5.0`, unless the player was not in ground),
so we decided to draw it in 2D,
using different colors to indicate player height and whether it was on ground.

We used `pygame` to draw it, resulting in the following image:

![flag](flag.png)

As it can be seen there, the flag is `BLoCkD3f1nEdPr0tOcoL`.

The code we used to get the flag is available at [hackit3.py](hackit3.py).



### File: ctfs/hackit-2019/hackit5/README.md

# Hackit 5

We are just given a [crackme](crackme) file.

```sh
$ file crackme
crackme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, stripped
$ ls -sh crackme
19K crackme
```

So, it seems we have a binary for x86-64 architecture, nothing fancy here.  
Fortunately, it also seems pretty small, so not too much code bloat, hopefully.

If we run the binary (obviously we didn't execute it right away, but it'll serve for illustrative purposes ;),
it kindly reports the proper usage:

```sh
$ chmod a+x crackme
$ ./crackme
Usage: ./crackme <password>
$ ./crackme ifeellucky
Fail!
```

Unsurprisingly, it seems to be the usual crackme, as the name suggests.

The program takes a noticeable time to run:

```sh
$ time ./crackme ifeellucky
Fail!

real	0m0.414s
user	0m0.414s
sys	0m0.000s
```

This suggests that there's quite a bit of logic in that small size.

We also can check what `strings` can tell us:

```
$ strings -8 crackme
[...]
Usage: %s <password>
Success!
E LAKSUERETNUOCN
%tEXtdate:create
2016-03-28T16:11:02+09:00
%tEXtdate:modify
2007-05-15T07:55:53+09:00
tEXtSoftware
www.inkscape.org
[...]
```

Interestingly enough, it seems we should expect to see `Success!` when we guess the correct password,
there's some `EUSKAL ENCOUNTER` text there, and also we seem to have an embedded PNG.

Even if it's not needed to solve the level, we can extract the PNG image with binwalk:

```sh
$ binwalk -D 'png image:png' crackme
```

We can see that it's the euskal encounter logo: ![logo](logo.png).

With all this information, we're ready to reverse the binary.  

The structure in the main function is quite simple and consists in:

- check the number of CLI arguments.
- if there are less than 2 arguments, show usage and finish.
- otherwise, initialize a buffer of size 256B (0x100) with the second argument (the password).
- run a loop 31337 (0x7a69) times, for each loop iteration:
  - traverse an array of items, which consists in a function pointer and 2 arguments
  - for each of the items in the array, call the function with:
    - the buffer (with the password initially)
    - the buffer size (256B)
    - the 2 arguments in the item
    - the loop index
- once the loop is completed, compare the buffer with a hardcoded byte sequence,
  if they match, you guessed the password.

Once the general structure is clear, we need to identify the functions and arguments in the array.  
There are in total 14 elements in the array, but there are only 12 different functions,
since 2 of them are called twice.

Knowing this, it seems pretty clear that those 12 functions will be invertible
and that the task consists in just inverting the code, and using the expected output as our initial input.  
That way, we should get the password as output of our inverted program.

Checking the functions, most of them are simple arithmetic operations.  
In some cases the same function serves for both directions.  
There are some functions that deserve especial mention:

- f1380 uses a multiplication, which means that a modular inverse is needed to reverse it.
  We just bruteforce the value since it's just 8 bits.
- f1450 uses the PNG as a data table. We just extracted the data block to use it.
- f1520 is an example of a function that serves both for direct and invert directions,
  but unfortunately it uses floating point datatypes and operations.
  This means that any precision error will result in an incorrect output,
  so extra care has to be taken with casts and constants.
  In our particular case, using O2 or O3 optimization levels in GCC results in a different constant for `0.1337`,
  which yields an incorrect result. It works just fine without optimizations or using Clang though.
- f1620 has the most complex logic, with some intertwined variables that require especial care to invert.

In order to reverse the functions, the approach we followed is:
- Use a disassembler / decompiler to reverse the logic of the first function.
- Write the code in C.
- Execute both the C written code and the provided `crackme` program
  to verify that both provide the same output given the same input.
  That is, to verify that we have reversed the code correctly.
- Write such function with the logic inverted in C.
- Run the C program calling the first function we have reversed and then the inverted function
  and validate that the output of the program matches the input.
  That is, both the direct and invert functions work and their composition is the identity function.
- Repeat the whole process for all the functions.
- Put both the direct and reverse block in a loop of 31337 and check that it works.
  This should validate that the usage of the loop index argument in the functions is correctly reversed.
  
Once everything above works, we have reversed the whole program and we have its invert,
so we just swich the order of things:
- Use the expected output as input.
- Call the loop in reverse order.
- In every loop interation, we call all the functions in reverse order.
- The output of the program is the password.
- Additionally, we can call the direct code to validate that the end result matches the expected output.

Once this is done, we get the password :)

```sh
$ cc crackme.c -lm
$ ./a.out
R0unD4ndr0UNdth3buff3r
```

You can check the code we built at [crackme.c](crackme.c).



### File: ctfs/hackit-ge-2020/hackit3/README.md

# Hackit 3

This is the last level of the [Gipuzkoa Encounter 14](https://ge14.gipuzkoaencounter.org/) hackit.
The event was transformed into a remote event due to COVID-19 in a rush, yet it went perfectly fine.
Kudos to the organization for the quick and great response!

The challenge consists in just the [cambridge_technology](cambridge_technology) file,
accompanied by the message _To finish, a classic_.
The message already suggests that it's a crackme,
as we'll soon confirm.

## Static analysis

The first thing we do is to check the type of file:

```sh
$ file cambridge_technology
cambridge_technology: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, stripped
```

So, it seems it's an [AArch64](https://en.wikipedia.org/wiki/ARM_architecture#AArch64) binary.

Let's disassemble it and look at the asm code:

![](disassembly.png)

On the top-left window we can see the binary's entry point.
We can see there at `0xa50` how the main function address is taken from the offset `0x11fd8`,
which is shown in the window below pointing to the address `0x810`,
which is the beginning of the text section
and consists in the main function, which contains all the relevant logic of the program.

The first part of the code of the main function is shown in the right window,
and the second part is shown in the bottom-left window.
We can distinguish 4 different parts in the code:

1. Instructions 0x810 - 0x874.
   Initial input/output code (with error handling at 0xa28 - 0xa2c).
   This code prints `Password: ` and reads the password
   to a string of 17 bytes.
   Since strings finish with `0`, it'll be at most 16 byte (128 bits) long.
2. Instructions 0x878 - 0x8a4. Initialization of variables.
   This code initializes `w14` to `0` (`w14` will be the next loop index),
   then it loads the password into the `q0` register (16B).
   It also initializes the registers `q3` to `q7` to some values taken from memory.
3. Instructions 0x8a8 - 0x9b0. The transformation loop.
   This code applies a series of transformations to the register `q0`,
   using helper registers `q1`, `q2` and `w0` to `w13`.
4. Instructions 0x9b4 - 0xa24. Checksum comparison.
   The result of the operations done in the loop is compared against a checksum
   printing a different result depending on the comparison
   (either `FAIL!` or `SUCCESS!`).

### Neon and registers

This code uses ARM's SIMD instruction set, called [Neon](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon/neon-programmers-guide-for-armv8-a/introducing-neon-for-armv8-a/fundamentals-of-armv8-neon-technology).
The way Neon works is pretty simple, but register naming can cause some confusion.
As a quick summary for what we need, [AArch64 has the following registers](https://developer.arm.com/architectures/learn-the-architecture/armv8-a-instruction-set-architecture/registers-in-aarch64-general-purpose-registers):

- 31 general purpose registers, which can be used as 32bit registers (`w0`..`w30`) and 64bit registers (`x0`..`x30`).
- 32 floating-point / SIMD registers (`v0`..`v31`), which can be used as:
  - 8bit registers (`b`yte) (`b0`..`b31`)
  - 16bit registers (`h`alf) (`h0`..`h31`)
  - 32bit registers (`s`ingle) (`s0`..`s31`)
  - 64bit registers (`d`ouble) (`d0`..`d31`)
  - 128bit registers (`q`uad) (`q0`..`q31`)
  Additionally, small registers allow random access, so they can be indexed (e.g. `v0.b[0]..v0.b[15]`).

## Dynamic analysis

Once I understood the overall picture of what the binary did,
I thought that only using static analysis may be too hard,
especially since it was the first time I was reversing code involving Neon,
so the possibility of getting things wrong was pretty high.

### Executing the binary

So, the first step is to actually be able to execute the binary.
We can do this with the almighty [qemu](https://www.qemu.org/),
but we also need a aarch64 libc and loader.

You can get full instructions and the binaries from [this great post](https://ughe.github.io/2018/07/19/qemu-aarch64).

```sh
$ qemu-aarch64 cambridge_technology
Password: AAAAAAAAAAAAAAAA
FAIL!
```

Nice, it seems to work!
Unfortunately, I didn't get the correct password on the first guess... so time for next step.

### Debugging the binary

QEMU includes an option to provide a gdb stub,
so a gdb process can be attached remotely to debug the binary.

```sh
$ qemu-aarch64 -g 1234 cambridge_technology
```

Now we need gdb with aarch64 target support.
Additionally, we'll also use [gef](https://github.com/hugsy/gef)
to help us make debugging a bit easier.

```sh
$ aarch64-linux-gnu-gdb cambridge_technology
```

Once inside `gdb` we set the remote target
and a breakpoint at the beginning of the interesting code,
and continue running the program

```gdb
gef➤ b *0x4000000810
Breakpoint 1 at 0x4000000810
gef➤  target remote 127.0.0.1:1234
Remote debugging using 127.0.0.1:1234
[...]
gef➤  continue
```

When the debugger stops at the breakpoint,
it looks like this:

![](gef.png)

At this point, everything is ready to
actually start reversing the code.

## Reversing the code

The approach I followed to reverse the code was to manually decompile it.
That is, writing a C program with the same logic that produces the same output.
We can confirm that the reversed logic is correct by checking precisely that output match.
In this specific case, after the loop ends we should have the same contents in our output
as we have in the `q0` register.

A decompiler can usually do this step automatically,
but in this case `ghidra` decompiler's output was crap,
I guess it's due to lack of proper support for AArch64 SIMD.

The resulting code looks like this:

```c
#include <stdint.h>
#include <stdio.h>

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

void print(u8 *q) {
  for (int i = 0; i < 0x10; i++) printf("%x ", q[i]);
  printf("\n");
}

int main() {
  u8 q0[0x10], q1[0x10], q2[0x10], q16[0x10];
  u8 q3[0x10] = {0x69, 0x30, 0xfc, 0x30, 0x93, 0x30, 0x68, 0x30, 0xb3, 0x30, 0xa4, 0x30, 0xc3, 0x30, 0x06, 0x26};
  u8 q4[0x10] = {0x4f, 0x7a, 0x84, 0x30, 0x4b, 0x30, 0x58, 0x30, 0x83, 0x30, 0x6a, 0x30, 0x44, 0x30, 0x01, 0xff};
  u8 q5[0x10] = {0xd9, 0x68, 0x1e, 0x88, 0xbe, 0xcf, 0xb6, 0xcf, 0xbc, 0xcf, 0x11, 0xac, 0xe5, 0x9e, 0xbc, 0xcf};
  u8 q6[0x10] = {0xb3, 0xba, 0xfe, 0xca, 0xef, 0xbe, 0xad, 0xde, 0xed, 0xa5, 0x53, 0xd1, 0x37, 0x13, 0xde, 0xc0};
  u8 q7[0x10] = "r4m4nd1mUt3at3!!";
  u32 w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13;
  u8 expected[0x10] = {0x81, 0x0c, 0xff, 0xdf, 0xbf, 0xb9, 0x07, 0xa8, 0xbf, 0x5b, 0xc2, 0x37, 0x7f, 0xcc, 0x6a, 0xbf};
  u8 flag[0x11];
  printf("Password: ");
  fgets(flag, 0x11, stdin);
  for (int i = 0; i < 0x10; i++) q0[i] = flag[i];
  for (int i = 0; i <= 0xc0b1c; i++) {
    // dup    v1.4h,  w14    
    for (int j = 0; j < 4; j++) *((u16 *)q1+j) = i;
    for (int j = 8; j < 0x10; j++) q1[j] = 0;
    // add    v0.16b,  v0.16b,  v7.16b
    for (int j = 0; j < 0x10; j++) q0[j] += q7[j];
    // mul    v1.8h,  v3.8h,  v1.h[0]
    u16 x = *(u16 *)q1;
    for (int j = 0; j < 8; j++) *((u16 *)q1+j) = *((u16 *)q3+j) * x;
    // mul    v0.4s,  v0.4s,  v6.4s
    for (int j = 0; j < 4; j++) *((u32 *)q0+j) *= *((u32 *)q6+j);
    // neg    v0.4s,  v0.4s
    for (int j = 0; j < 4; j++) *((u32 *)q0+j) = ~*((u32 *)q0+j)+1;
    // add    v0.8h,  v0.8h,  v5.8h
    for (int j = 0; j < 8; j++) *((u16 *)q0+j) += *((u16 *)q5+j);
    // mla    v0.8h,  v4.8h,  v1.8h
    for (int j = 0; j < 8; j++) *((u16 *)q0+j) += *((u16 *)q4+j) * *((u16 *)q1+j); 
    // mvn    v0.16b,  v0.16b
    for (int j = 0; j < 16; j++) q0[j] ^= 0xff;
    // mov    d1,  v0.d[0]
    *(u64 *)q1 = *(u64 *)q0, *((u64 *)q1+1) = 0;
    // mov    d0,  v0.d[1]
    *(u64 *)q0 = *((u64 *)q0+1), *((u64 *)q0+1) = 0;
    // trn1   v2.8b,  v1.8b,  v0.8b
    for (int j = 0; j < 16; j += 2) q2[j] = q1[j], q2[j+1] = q0[j];
    // trn2   v0.8b,  v1.8b,  v0.8b
    for (int j = 0; j < 16; j += 2) q0[j] = q1[j+1], q0[j+1] = q0[j+1];
    // stp    d2,  d0,  [sp,  #32]
    // ldr    q0,  [sp,  #32]
    *((u64 *)q0+1) = *(u64 *)q0;
    *(u64 *)q0 = *(u64 *)q2;
    // rev64  v1.4s,  v0.4s
    for (int j = 0; j < 2; j++)
      for (int k = 0; k < 2; k++)
        *((u32 *)q1+j*2+1-k) = *((u32 *)q0+j*2+k);
    // b2,  v1.b[1]
    q2[0] = q1[1];
    for (int j = 1; j < 0x10; j++) q2[j] = 0;
    // mov    b16,  v1.b[0]
    q16[0] = q1[0];
    for (int j = 1; j < 0x10; j++) q16[j] = 0;
    // mov    b0,  v1.b[2]
    q0[0] = q1[2];
    for (int j = 1; j < 0x10; j++) q0[j] = 0;
    // umov   w12,  v1.b[3]
    w12 = q1[3];
    // umov   w11,  v1.b[4]
    w11 = q1[4];
    // umov   w10,  v1.b[5]
    w10 = q1[5];
    // umov   w9,  v1.b[6]
    w9 = q1[6];
    // add    v2.2s,  v2.2s,  v16.2s
    for (int j = 0; j < 2; j++) *((u32 *)q2+j) += *((u32 *)q16+j);
    // umov   w8,  v1.b[7]
    w8 = q1[7];
    // umov   w7,  v1.b[8]
    w7 = q1[8];
    // umov   w6,  v1.b[9]
    w6 = q1[9];
    // umov   w5,  v1.b[10]
    w5 = q1[10];
    // umov   w4,  v1.b[11]
    w4 = q1[11];
    // umov   w3,  v1.b[12]
    w3 = q1[12];
    // umov   w2,  v1.b[13]
    w2 = q1[13];
    // eor    v0.8b,  v2.8b,  v0.8b
    for (int j = 0; j < 0x10; j++) q0[j] ^= q2[j];
    // umov   w1,  v1.b[14]
    w1 = q1[14];
    // umov   w0,  v1.b[15]
    w0 = q1[15];
    // fmov   w13,  s0
    w13 = *(u32 *)q0;
    // mov    v0.16b,  v1.16b
    for (int j = 0; j < 0x10; j++) q0[j] = q1[j];
    // sub    w12,  w12,  w13,  uxtb
    w12 -= w13 & 0xff;
    // mov    v0.b[1],  v2.b[0]
    q0[1] = q2[0];
    // eor    w11,  w12,  w11
    w11 ^= w12;
    // add    w10,  w10,  w11,  uxtb
    w10 += w11 & 0xff;
    // eor    w9,  w10,  w9
    w9 ^= w10;
    // mov    v0.b[2],  w13
    q0[2] = w13;
    // sub    w8,  w8,  w9,  uxtb
    w8 -= w9 & 0xff;
    // eor    w7,  w8,  w7
    w7 ^= w8;
    // mov    v0.b[3],  w12
    q0[3] = w12;
    // add    w6,  w6,  w7,  uxtb
    w6 += w7 & 0xff;
    // eor    w5,  w6,  w5
    w5 ^= w6;
    // sub    w4,  w4,  w5,  uxtb
    w4 -= w5 & 0xff;
    // mov    v0.b[4],  w11
    q0[4] = w11;
    // eor    w3,  w4,  w3
    w3 ^= w4;
    // add    w2,  w2,  w3,  uxtb
    w2 += w3 & 0xff;
    // eor    w1,  w2,  w1
    w1 ^= w2;
    // mov    v0.b[5],  w10
    q0[5] = w10;
    // sub    w0,  w0,  w1,  uxtb
    w0 = (w0 & 0xff) - (w1 & 0xff);
    // mov    v0.b[6],  w9
    q0[6] = w9;
    // mov    v0.b[7],  w8
    q0[7] = w8;
    // mov    v0.b[8],  w7
    q0[8] = w7;
    // mov    v0.b[9],  w6
    q0[9] = w6;
    // mov    v0.b[10],  w5
    q0[10] = w5;
    // mov    v0.b[11],  w4
    q0[11] = w4;
    // mov    v0.b[12],  w3
    q0[12] = w3;
    // mov    v0.b[13],  w2
    q0[13] = w2;
    // mov    v0.b[14],  w1
    q0[14] = w1;
    // mov    v0.b[15],  w0
    q0[15] = w0;
  }
  print(q0);

  for (int i = 0; i < 0x10; i++)
    if (flag[i] != expected[i]) {
      puts("FAIL!");
      return 0;
    }
  puts("SUCCESS!");
}
```

The different parts of the code we discussed above become clear now.
Variables are named after the registers where they are stored
(except for `flag` and `expected` which are stored in the stack).
Inside the loop every operation includes the comment of the assembly code
followed by the equivalent C code.
Additionally, at the end of the processing `q0` register we print
in order to compare with the actual register contents in the debugging session,
this code is not in the original binary, obviously.

The above code is available at [reversed-forward.c](reversed-forward.c).
We can compile and run it to see the actual results of the register
for the input we prefer to provide:

```
> aarch64-linux-gnu-gcc reversed-forward.c
>  qemu-aarch64 ./a.out
Password: AAAAAAAAAAAAAAAA
ea 35 43 d6 1b 47 0 1c 2c a1 c3 59 b2 46 ca 75
FAIL!
```

We can easily confirm with the debug session that the output of the register is the expected one,
so we have correctly reversed what the code does, and we now have it in code form.

If we look the above code in more detail,
we can easily confirm that all the operations are invertible,
so that's what we actually need to do.
If we start with the expected output in `q0` and invert all the operations
we should have the actual password at the end of the process.

We can also notice that the above code can be simplified a bit.
So we can first simplify the code a bit,
now that we can confirm that our simplifications are correct easily.
A simplified version looks like this:

```c
#include <stdint.h>
#include <stdio.h>

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

void print(u8 *q) {
  for (int i = 0; i < 0x10; i++) printf("%x ", q[i]);
  printf("\n");
}

int main() {
  u8 q0[0x10], q1[0x10], q2[0x10];
  u8 q3[0x10] = {0x69, 0x30, 0xfc, 0x30, 0x93, 0x30, 0x68, 0x30, 0xb3, 0x30, 0xa4, 0x30, 0xc3, 0x30, 0x06, 0x26};
  u8 q4[0x10] = {0x4f, 0x7a, 0x84, 0x30, 0x4b, 0x30, 0x58, 0x30, 0x83, 0x30, 0x6a, 0x30, 0x44, 0x30, 0x01, 0xff};
  u8 q5[0x10] = {0xd9, 0x68, 0x1e, 0x88, 0xbe, 0xcf, 0xb6, 0xcf, 0xbc, 0xcf, 0x11, 0xac, 0xe5, 0x9e, 0xbc, 0xcf};
  u8 q6[0x10] = {0xb3, 0xba, 0xfe, 0xca, 0xef, 0xbe, 0xad, 0xde, 0xed, 0xa5, 0x53, 0xd1, 0x37, 0x13, 0xde, 0xc0};
  u8 q7[0x10] = "r4m4nd1mUt3at3!!";
  u8 expected[0x10] = {0x81, 0x0c, 0xff, 0xdf, 0xbf, 0xb9, 0x07, 0xa8, 0xbf, 0x5b, 0xc2, 0x37, 0x7f, 0xcc, 0x6a, 0xbf};
  u8 flag[0x11];
  printf("Password: ");
  fgets(flag, 0x11, stdin);
  for (int i = 0; i < 0x10; i++) q0[i] = flag[i];
  for (int i = 0; i <= 0xc0b1c; i++) {
    for (int j = 0; j < 4; j++) *((u16 *)q1+j) = i;
    for (int j = 8; j < 0x10; j++) q1[j] = 0;
    for (int j = 0; j < 0x10; j++) q0[j] += q7[j];
    u16 x = *(u16 *)q1;
    for (int j = 0; j < 8; j++) *((u16 *)q1+j) = *((u16 *)q3+j) * x;
    for (int j = 0; j < 4; j++) *((u32 *)q0+j) *= *((u32 *)q6+j);
    for (int j = 0; j < 4; j++) *((u32 *)q0+j) = ~*((u32 *)q0+j)+1;
    for (int j = 0; j < 8; j++) *((u16 *)q0+j) += *((u16 *)q5+j);
    for (int j = 0; j < 8; j++) *((u16 *)q0+j) += *((u16 *)q4+j) * *((u16 *)q1+j); 
    for (int j = 0; j < 16; j++) q0[j] ^= 0xff;
    *(u64 *)q1 = *(u64 *)q0, *((u64 *)q1+1) = 0;
    *(u64 *)q0 = *((u64 *)q0+1), *((u64 *)q0+1) = 0;
    for (int j = 0; j < 16; j += 2) q2[j] = q1[j], q2[j+1] = q0[j];
    for (int j = 0; j < 16; j += 2) q0[j] = q1[j+1], q0[j+1] = q0[j+1];
    *((u64 *)q0+1) = *(u64 *)q0, *(u64 *)q0 = *(u64 *)q2;
    for (int j = 0; j < 2; j++)
      for (int k = 0; k < 2; k++)
        *((u32 *)q1+j*2+1-k) = *((u32 *)q0+j*2+k);
    u8 a = q1[0], b = q1[1], c = q1[2];
    b += a;
    c ^= b;
    for (int j = 0; j < 0x10; j++) q0[j] = q1[j];
    q0[1] = b;
    q0[2] = c;
    q0[3] -= c;
    q0[4] ^= q0[3];
    q0[5] += q0[4];
    q0[6] ^= q0[5];
    q0[7] -= q0[6];
    q0[8] ^= q0[7];
    q0[9] += q0[8];
    q0[10] ^= q0[9];
    q0[11] -= q0[10];
    q0[12] ^= q0[11];
    q0[13] += q0[12];
    q0[14] ^= q0[13];
    q0[15] -= q0[14];
  }
  print(q0);
  for (int i = 0; i < 0x10; i++)
    if (q0[i] != expected[i]) {
      puts("FAIL!");
      return 0;
    }
  puts("SUCCESS!");
}
```

This code is available at (reversed-forward-simplified.c)[reversed-forward-simplified.c]
We can confirm that the output haven't changed:

```
> aarch64-linux-gnu-gcc reversed-forward-simplified.c
>  qemu-aarch64 ./a.out
Password: AAAAAAAAAAAAAAAA
ea 35 43 d6 1b 47 0 1c 2c a1 c3 59 b2 46 ca 75
FAIL!
```

The code that inverts the logic looks like this:

```c
#include <stdint.h>
#include <stdio.h>

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

u64 modinv(u64 a, u64 b) {
  u64 b0 = b, t, q;
  u64 x0 = 0, x1 = 1;
  if (b == 1) return 1;
  while (a > 1) {
    q = a / b;
    t = b, b = a % b, a = t;
    t = x0, x0 = x1 - q * x0, x1 = t;
  }
  return x1;
}

int main() {
  u8 q1[0x10], q2[0x10];
  u8 q0[0x11] = {0x81, 0x0c, 0xff, 0xdf, 0xbf, 0xb9, 0x07, 0xa8, 0xbf, 0x5b, 0xc2, 0x37, 0x7f, 0xcc, 0x6a, 0xbf, 0x00};
  u8 q3[0x10] = {0x69, 0x30, 0xfc, 0x30, 0x93, 0x30, 0x68, 0x30, 0xb3, 0x30, 0xa4, 0x30, 0xc3, 0x30, 0x06, 0x26};
  u8 q4[0x10] = {0x4f, 0x7a, 0x84, 0x30, 0x4b, 0x30, 0x58, 0x30, 0x83, 0x30, 0x6a, 0x30, 0x44, 0x30, 0x01, 0xff};
  u8 q5[0x10] = {0xd9, 0x68, 0x1e, 0x88, 0xbe, 0xcf, 0xb6, 0xcf, 0xbc, 0xcf, 0x11, 0xac, 0xe5, 0x9e, 0xbc, 0xcf};
  u8 q6[0x10] = {0xb3, 0xba, 0xfe, 0xca, 0xef, 0xbe, 0xad, 0xde, 0xed, 0xa5, 0x53, 0xd1, 0x37, 0x13, 0xde, 0xc0};
  u8 q7[0x10] = "r4m4nd1mUt3at3!!";
  for (int i = 0xc0b1c; i >= 0; i--) {
    q0[15] += q0[14];
    q0[14] ^= q0[13];
    q0[13] -= q0[12];
    q0[12] ^= q0[11];
    q0[11] += q0[10];
    q0[10] ^= q0[9];
    q0[9] -= q0[8];
    q0[8] ^= q0[7];
    q0[7] += q0[6];
    q0[6] ^= q0[5];
    q0[5] -= q0[4];
    q0[4] ^= q0[3];
    u8 a = q0[0], b = q0[1], c = q0[2];
    q0[3] += c;
    for (int j = 0; j < 0x10; j++) q1[j] = q0[j];
    c ^= b;
    b -= a;
    q1[1] = b;
    q1[2] = c;
    for (int j = 0; j < 2; j++)
      for (int k = 0; k < 2; k++)
        *((u32 *)q0+j*2+1-k) = *((u32 *)q1+j*2+k);
    *(u64 *)q2 = *(u64 *)q0, *(u64 *)q0 = *((u64 *)q0+1);
    for (int j = 0; j < 16; j += 2) q1[j+1] = q0[j], q0[j+1] = q0[j+1];
    for (int j = 0; j < 16; j += 2) q1[j] = q2[j], q0[j] = q2[j+1];
    *((u64 *)q0+1) = *(u64 *)q0, *(u64 *)q0 = *(u64 *)q1;
    for (int j = 0; j < 16; j++) q0[j] ^= 0xff;
    for (int j = 0; j < 4; j++) *((u16 *)q1+j) = i;
    for (int j = 8; j < 0x10; j++) q1[j] = 0;
    u16 x = *(u16 *)q1;
    for (int j = 0; j < 8; j++) *((u16 *)q1+j) = *((u16 *)q3+j) * x;
    for (int j = 0; j < 8; j++) *((u16 *)q0+j) -= *((u16 *)q4+j) * *((u16 *)q1+j);
    for (int j = 0; j < 8; j++) *((u16 *)q0+j) -= *((u16 *)q5+j);
    for (int j = 0; j < 4; j++) *((u32 *)q0+j) = ~*((u32 *)q0+j)+1;
    for (int j = 0; j < 4; j++) *((u32 *)q0+j) *= modinv(*((u32 *)q6+j), 0x100000000);
    for (int j = 0; j < 0x10; j++) q0[j] -= q7[j];
  }
  printf("%s\n", q0);
}
```

This code is available at [reversed.c](reversed.c).
Compiling and running the code we get the valid password:

```sh
$ aarch64-linux-gnu-gcc reversed.c -O3
$ qemu-aarch64 ./a.out
n30nR3d4RM4tur3!
```

We can confirm that it works with the original binary:

```sh
$ qemu-aarch64 cambridge_technology
Password: n30nR3d4RM4tur3!
SUCCESS!
```

Yay!



### File: ctfs/plaidctf-2019/README.md

# Solutions for PlaidCTF 2019 challenges

You can also check the [official site](https://play.plaidctf.com/),
[CTFtime site](https://ctftime.org/event/779)
and additional [writeups](https://ctftime.org/event/743/tasks/).

This repo contains the following solutions:

- [docker](docker/README.md) (Misc 10)
- [Everland](everland/README.md) (Misc 250)
- [Horst](horst/README.md) (Crypto 200)
- [Project Eulernt](eulernt/README.md) (Misc 200)



### File: ctfs/plaidctf-2019/docker/README.md

# docker (misc 10)

The description of the challenge is pretty simple: _docker pull whowouldeverguessthis/public_.

Considering the low score of this chalenge, we assume that it's trivial, so get the image and grep for the flag format:

```sh
$ docker pull whowouldeverguessthis/public
[...]
$ docker images -q whowouldeverguessthis/public
969996089570
$ grep -r PCTF /var/lib//docker/image/overlay2/imagedb/content/sha256/969996089570*
{"architecture":"amd64","config":{"Hostname":"","Domainname":"","User":"","AttachStdin":false,"AttachStdout":false,"AttachStderr":false,"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd":["bash"],"ArgsEscaped":true,"Image":"sha256:476c8b6b6d9fcef1c0e7476342e47ca0b0480e44e5bb42ce94a4cc8415905413","Volumes":null,"WorkingDir":"","Entrypoint":null,"OnBuild":null,"Labels":null},"container":"f785c362a9cfec511ece69829f4bd20a2918a9e291fffe1e19f75485de4cd37b","container_config":{"Hostname":"","Domainname":"","User":"","AttachStdin":false,"AttachStdout":false,"AttachStderr":false,"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd":["/bin/sh","-c","echo \"I'm sorry, but your princess is in another castle\" \u003e /flag"],"ArgsEscaped":true,"Image":"sha256:476c8b6b6d9fcef1c0e7476342e47ca0b0480e44e5bb42ce94a4cc8415905413","Volumes":null,"WorkingDir":"","Entrypoint":null,"OnBuild":null,"Labels":null},"created":"2019-04-12T17:03:47.069664703Z","docker_version":"18.09.2","history":[{"created":"2019-01-22T19:22:38.494832817Z","created_by":"/bin/sh -c #(nop) ADD file:34b9952e66cb98287bc41fab82739375fe6c43f38ed3b893e98a99035b494770 in / "},{"created":"2019-01-22T19:22:38.706883433Z","created_by":"/bin/sh -c #(nop)  CMD [\"bash\"]","empty_layer":true},{"created":"2019-04-12T17:03:46.241744406Z","created_by":"/bin/sh -c echo \"PCTF{well_it_isnt_many_points_what_did_you_expect}\" \u003e /flag"},{"created":"2019-04-12T17:03:47.069664703Z","created_by":"/bin/sh -c echo \"I'm sorry, but your princess is in another castle\" \u003e /flag"}],"os":"linux","rootfs":{"type":"layers","diff_ids":["sha256:743aff3a80526229ca5762b3240e4e506b6b3a61e97accb853707a946a3abb39","sha256:a5fdd7807f999b258a273978509252fcdbb76218e14a01376d5b2ade4798826b","sha256:e958f8e060fc9bb06df3ccb0aff183fa8c549c369536f063d7ea36a617c86564"]}}
```

And we extract the flag from the image: `PCTF{well_it_isnt_many_points_what_did_you_expect}`



### File: ctfs/plaidctf-2019/eulernt/README.md

# Project Eulernt (Misc 200)

We get a python source, [eulernt_6d26d176de9f441923057d2b5c14f126.py](eulernt_6d26d176de9f441923057d2b5c14f126.py) and a host,
`eulernt.pwni.ng:5555`, where that code is running.

Analysing the code we can see that it requests for a number that is both a divisor of _N = 333!_ (333-smooth number) and close to its square root (_sN_),
with an relative error margin of _1e-8_.

We build a solution that just gets the factors of _N_, randomly shuffles them and check if we get any subsequence with a product within the valid range.
We first write it in python ([eulernt.py](eulernt.py)), but since it takes a while, we rewrite it in C++ too ([eulernt.cc](eulernt.cc)).

We then connect to the server and get the flag.

```sh
$ c++ eulernt.cc -lgmp  -lgmpxx -O3
$ ./a.out 
3214724638244592338929574336157302572951323085582819302449269218432782841988198693324942361005598255499445390916417366573442777402935092163167928803153708492324124799012987236567367031831505351605030172818940177625669924447673041630726404543125348067833208617162000948710471059133188661284703535575859200000000000000000000000000000000000000000000000
$ nc eulernt.pwni.ng 5555
Enter number: 3214726332154755748991079128846351062560778451862637883528691274756654374878844647025079591940578176759650427443606854127454330464131553816664001382397024890787110816276254358916583147465182493394800235346889527243496491766897151517308056569578296879300485562874711359654341221896407523796447391678839548240290864168960000000000000000000000000000000
PCTF{R3fr3sh1ngly_Sm00th}
```

So the flag is `PCTF{R3fr3sh1ngly_Sm00th}`.



### File: ctfs/plaidctf-2019/everland/README.md

# Everland (Misc 250)

The challenge provides a source file [everland_19f72e788727d36b0200b0d9507aeb3f.sml](everland_19f72e788727d36b0200b0d9507aeb3f.sml)
and a host `everland.pwni.ng:7772` where the code is running.

Analyzing the code we see that we have a hero and 10 enemies,
they have some health points, strength points, and a set of actions they can execute.
The hero also has a bag with some items.
Some additional items can be collected.
Those items can be used for HP, SP or new actions.


We have to kill them all the enemies and then,
the enemy with higher strength is posessed and we have to kill it too.
Then we get the flag. Easy peasy.

At first glance, winning the fight and getting the flag seems impossible,
but there are several flaws in the program that allow us to win.

## Use recouperate


The enemies use a simple weight function to choose the action they can execute:

```sml
(ms/ts) + 3.0*(mh/th) (* ms = my strength, ts = their strengh, mh = my hp, th = their hp *)
```

From the set of enemy actions, the most effective one is `strike`, which substracts 15HP from the hero.
Executing this continuously, the hero faces a certain death.  
The good news? `(ms/ts)` gets `inf` when `ts = 0` and maximizes the weight,
so once the hero gets 0 strength the first action will be executed, not matter which one is.

This is great, since the first action is `lunge`:

```sml
their_h := 2*(!their_h) div 3; my_h := max(!my_h-10, 0)
```

So, this action will get us killed rather slowly but eventually will kill the enemy itself, nice.
The hero just need to `recouperate` themselves to avoid a certain death:

```sml
my_s := max(!my_s - 20, 0); my_h := (!my_h + 10)
```

This action reduces hero strengh and increases their health, so it fulfills both objectives.

This allows the hero to survive till the posessed enemy.

## Capture and sacrifice

The previous flaw allows the hero to survive till the final enemy, which has a single action, `kill`:

```sml
(* It kills you. You're dead *)
their_h := 0
```

It seems pretty straigthforward, but again, there's a flaw.

The enemies execute their action before the hero in a fight round,
but with the last enemy, the posession itself takes a round.
This means that the hero has a single attack it can use.

Additionally, there's an object called _Sacrifical Net_ that,
when used by the hero, gives them the ability to `capture` an enemy.

When an enemy is captured, we gain an action called `sacrifice`:

```sml
my_h := min((!my_h)+min(!e_h, !my_s*10), player_max);
e_h  := (!e_h-(!my_h)*10);
```

So we just need to have enough health and strength when sacrifying to kill the posessed enemy.

## Get the flag

We connect to the server and follow the previous steps
(`capture`,  then `recouperate` till the last enemy, then `sacrifice`)
and eventually get the flag: `PCTF{just_be_glad_i_didnt_arm_cpt_hook_with_GADTs}`



### File: ctfs/plaidctf-2019/horst/README.md

# Horst (crypto 200)

The challenge provides two files:

- [horst.py](horst.py), containing a permutation based cryptosystem.
- [data.txt](data.txt), containing a couple of _plaintext_ / _ciphertext_ pairs.

As we can see in the python code, the _plaintext_ consists in a pair of permutations.  
Additionally, there's another permutation that acts as a _key_.
The encryption consists in a series repeated operations on the _plaintext_ using the key.
Finally, the _ciphertext_ consists in the resulting permutations,
from which the plaintext can be recovered with the _key_ permutation.

We are provided two _plaintext_ / _ciphertext_ pairs, encrypted with the same _key_,
which is a randomly generated permutation, and not provided.  
We are expected to recover the key, to generate the flag.

Looking at the encryption process we can see that encryption process consists only in three operation rounds,
so it may be feasible to solve it using a solver,
so we create the model and extract the _plaintext_ and _ciphertext_ from the `data.txt` file and add it as the input and constraints.
The final code is available at [horst.pi](horst.pi).

We run it to obtain the key:

```sh
$ picat horst.pi
[59,2,50,29,55,15,43,30,27,6,57,22,7,26,3,35,24,40,53,46,49,10,16,12,41,47,60,11,51,58,4,1,56,28,52,19,39,9,33,36,37,63,14,0,61,13,25,17,8,54,44,34,18,23,48,62,32,42,20,45,31,5,38,21]
```

Once we have the key, we just need to construct the key as specified in the python code:

```sh
$ python2 -c "from horst import Permutation;from hashlib import sha1;print 'The flag is: PCTF{%s}' % sha1(str(Permutation([59,2,50,29,55,15,43,30,27,6,57,22,7,26,3,35,24,40,53,46,49,10,16,12,41,47,60,11,51,58,4,1,56,28,52,19,39,9,33,36,37,63,14,0,61,13,25,17,8,54,44,34,18,23,48,62,32,42,20,45,31,5,38,21]))).hexdigest()";
The flag is: PCTF{69f4153d282560cdaab05e14c9f1b7e0a5cc74d1}
```



### File: ctfs/sharif-2018/README.md

# Solutions to some Sharif 8 CTF challenges

You can also check the [official site](http://ctf.certcc.ir/ctf8/),
[CTFtime site](https://ctftime.org/event/507)
and additional [writeups](https://ctftime.org/event/507/tasks/).

This repo contains the following solutions:

* [OSS Service (Easy)](oss-service-easy) (Crypto 100)
* [ElGamat](el-gamat) (Crypto 200)
* [fHash](fhash) (Crypto 200)
* [OSS Service (Hard)](oss-service-hard) (Crypto 500)
* [Client01](client01) (Forensics 75)
* [Fifteen Puzzle](fifteen-puzzle) (Misc PPC 150)



### File: ctfs/sharif-2018/client01/README.md

# Client01 (forensics 75)

We get a file `client01.tar.gz` with a user home directory.
We do some quick search for anything interesting.

```
> grep -ir flag .
Binary file ./.mozilla/firefox/c3a958fk.default/places.sqlite matches
Binary file ./.mozilla/firefox/c3a958fk.default/secmod.db matches
Binary file ./.cache/thunderbird/5bd7jhog.default/cache2/entries/C972AC86BA22ADBFC038B134C02101C894D0078A matches
Binary file ./.cache/mozilla/firefox/c3a958fk.default/cache2/entries/698AC159A6BCBA0D13FE6F10F1A38E498F826F33 matches
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (B8=imapFlags)(B9=charSetOverride)(BA=charSet)(BB=highestRecordedUID)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (BE=dateReceived)(BF=ProtoThreadFlags)(C0=folderName)(C1=X-GM-MSGID)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (D3=cleanupBodies)(D4=applyToFlaggedMessages)(D5=useServerRetention)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (DA=op)(DB=msgKey)(DC=opFlags)(DD=newFlags)(DE=moveDest)(DF=msgSize)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (88=flags)(89=priority)(8A=label)(8B=statusOfset)(8C=numLines)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (8D=ccList)(8E=bccList)(8F=msgThreadId)(90=threadId)(91=threadFlags)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:  (B2=sortOrder)(B3=viewFlags)(B4=viewType)(B5=sortColumns)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX.msf:    ={"threadCol":{"visible":true,"ordinal":"1"},"flaggedCol":{"visible":true,\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Sent.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Sent.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Templates.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Templates.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Important.msf:  (B8=highestModSeq)(B9=imapFlags)(BA=charSetOverride)(BB=charSet)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Important.msf:  (C3=dateReceived)(C4=ProtoThreadFlags)(C5=X-GM-MSGID)(C6=X-GM-THRID)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Important.msf:  (87=size)(88=flags)(89=priority)(8A=label)(8B=statusOfset)(8C=numLines)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Important.msf:  (8D=ccList)(8E=bccList)(8F=msgThreadId)(90=threadId)(91=threadFlags)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Important.msf:  (B1=MRUTime)(B2=sortType)(B3=sortOrder)(B4=viewFlags)(B5=viewType)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Important.msf:    ={"threadCol":{"visible":true,"ordinal":"1"},"flaggedCol":{"visible":true,\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (B8=columnStates)(B9=highestModSeq)(BA=imapFlags)(BB=charSetOverride)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (C2=gloda-dirty)(C3=ProtoThreadFlags)(C4=X-GM-MSGID)(C5=X-GM-THRID)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (D3=ns:msg:db:table:kind:ops)(D4=op)(D5=msgKey)(D6=opFlags)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (D7=newFlags)(D8=srcFolderURI)(D9=srcMsgKey)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (B5=viewFlags)(B6=viewType)(B7=sortColumns)>
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:  (AA=flag)(AB
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash.msf:    ={"threadCol":{"visible":true,"ordinal":"1"},"flaggedCol":{"visible":true,\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Spam.msf:  (B8=columnStates)(B9=highestModSeq)(BA=imapFlags)(BB=charSetOverride)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Spam.msf:  (88=flags)(89=priority)(8A=label)(8B=statusOfset)(8C=numLines)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Spam.msf:  (8D=ccList)(8E=bccList)(8F=msgThreadId)(90=threadId)(91=threadFlags)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Spam.msf:  (B5=viewFlags)(B6=viewType)(B7=sortColumns)>
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Spam.msf:    ={"threadCol":{"visible":true,"ordinal":"1"},"flaggedCol":{"visible":true,\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Trash:Subject: flag
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Starred.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Starred.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Starred.msf:  (B1=highestModSeq)(B2=imapFlags)(B3=charSetOverride)(B4=charSet)>
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (B8=highestModSeq)(B9=imapFlags)(BA=charSetOverride)(BB=charSet)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (BE=ns:msg:db:table:kind:pending)(BF=dateReceived)(C0=ProtoThreadFlags)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (D0=msgKey)(D1=opFlags)(D2=newFlags)(D3=moveDest)(D4=msgSize)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (88=flags)(89=priority)(8A=label)(8B=statusOfset)(8C=numLines)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (8D=ccList)(8E=bccList)(8F=msgThreadId)(90=threadId)(91=threadFlags)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (B1=MRUTime)(B2=sortType)(B3=sortOrder)(B4=viewFlags)(B5=viewType)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:    ={"threadCol":{"visible":true},"attachmentCol":{"visible":true},"flaggedCo\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail.msf:  (DA=useServerDefaults)(DB=cleanupBodies)(DC=applyToFlaggedMessages)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Drafts.msf:  (B8=highestModSeq)(B9=imapFlags)(BA=charSetOverride)(BB=charSet)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Drafts.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Drafts.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Drafts.msf:  (B1=MRUTime)(B2=sortType)(B3=sortOrder)(B4=viewFlags)(B5=viewType)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/Drafts.msf:    ={"threadCol":{"visible":true},"attachmentCol":{"visible":true},"flaggedCo\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:  (B8=dateReceived)(B9=ProtoThreadFlags)(BA=folderName)(BB=X-GM-MSGID)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:  (C5=replyTo)(C6=sortType)(C7=sortOrder)(C8=viewFlags)(C9=viewType)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:  (86=date)(87=size)(88=flags)(89=priority)(8A=label)(8B=statusOfset)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:  (91=threadFlags)(92=threadNewestMsgDate)(93=children)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:  (B1=highestModSeq)(B2=imapFlags)(B3=charSetOverride)(B4=charSet)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:<(93=flag)>[3:^9A(^95^93)]
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].sbd/All Mail.msf:    ={"threadCol":{"visible":true,"ordinal":"1"},"flaggedCol":{"visible":true,\
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Drafts.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Drafts.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX:Subject: flag
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/[Gmail].msf:  (B8=cleanupBodies)(B9=applyToFlaggedMessages)(BA=useServerRetention)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Archives.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/Archives.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
Binary file ./.thunderbird/5bd7jhog.default/places.sqlite matches
Binary file ./.thunderbird/5bd7jhog.default/calendar-data/local.sqlite matches
./.thunderbird/5bd7jhog.default/blocklist-addons.json:        "why": "Certain versions of this add-on contains an executable that is flagged by multiple tools as malware. Newer versions no longer use it.",
./.thunderbird/5bd7jhog.default/panacea.dat:  (8A=charset)(8B=boxFlags)(8C=hierDelim)(8D=onlineName)(8E=aclFlags)
./.thunderbird/5bd7jhog.default/panacea.dat:  (81=ns:msg:db:table:kind:folders)(82=key)(83=flags)(84=totalMsgs)
Binary file ./.thunderbird/5bd7jhog.default/kinto.sqlite matches
Binary file ./.thunderbird/5bd7jhog.default/secmod.db matches
./.thunderbird/5bd7jhog.default/Mail/Local Folders/Trash.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/Mail/Local Folders/Trash.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
./.thunderbird/5bd7jhog.default/Mail/Local Folders/Trash.msf:  (B8=applyToFlaggedMessages)(B9=useServerRetention)(B2=retainBy)
./.thunderbird/5bd7jhog.default/Mail/Local Folders/Unsent Messages.msf:  (B8=applyToFlaggedMessages)(B9=useServerRetention)
./.thunderbird/5bd7jhog.default/Mail/Local Folders/Unsent Messages.msf:  (84=references)(85=recipients)(86=date)(87=size)(88=flags)(89=priority)
./.thunderbird/5bd7jhog.default/Mail/Local Folders/Unsent Messages.msf:  (8F=msgThreadId)(90=threadId)(91=threadFlags)(92=threadNewestMsgDate)
Binary file ./.thunderbird/5bd7jhog.default/global-messages-db.sqlite matches
./.xsession-errors.old:    'su', (bus_name, flags)))
./.xsession-errors:    'su', (bus_name, flags)))
```

There's clearly something interesting in that output, an mail with `flag` subject:

```
./.thunderbird/5bd7jhog.default/ImapMail/imap.gmail.com/INBOX:Subject: flag
```

We open that inbox file, look for the email and see that it contains a
[link to a file](http://www.filehosting.org/file/details/720884/Ncemd1SxbOVaOrbW/file).

We download the [file](file) open in and see what it seems like a PNG file:

```
00000010: 894e 470d 0a1a 0a00 0000 0d49 4844 5200  .NG........IHDR.
00000010: 0003 e800 0000 c804 0300 0000 89c9 d67c  ...............|
00000020: 0000 001b 504c 5445 0000 00ff ffff 5f5f  ....PLTE......__
...
```

The problem is that the magic value of the file is incorrect
we replace the first byte by a `P` and we can now see the flag:

![the flag](file.png)



### File: ctfs/sharif-2018/el-gamat/README.md

# ElGamat: ElGamal over Matrices (crypto 200)

We are provided with a [cryptosystem scheme spec](ElGamat.pdf),
which consists in getting the discrete logarithm of a matrix.

We are also provided with [a data file](Matrices.txt),
consisting in the modulo `p`, the generator matrix `G`
and the public key matrix `H`.

Finally we have a [flag generator](flag_gen.py) that
once we have the private key (the exponent `α`) gives us the flag.

To get the private key, we look for the jordan blocks of the matrix,
find one that is easily solvable and get alpha:

```sage
#!/usr/bin/sage

def flag_gen(alpha):
	import hashlib
	return 'SharifCTF{%s}' % hashlib.md5(str(alpha).encode()).hexdigest()

p = 1461501637330902918203684832716283019655932542983

G = matrix(GF(p), 5, 5, [
     [1287397632974625907369332145667695136576732725719,  999149001044306271168727399637009399486427921379,   1046504160269652701583906344218556291030141088947,  724446625683754938181565321149725788430461092168,    1071845980147173642753960259602135592110139561915],
     [947603660931904341080240982051313712707367037453,   312289846563741934103580532543082761760226637905,   494739786803547247505263837170488583876166831850,   680540462980071181450018491798299105995449257198,    2602258415762368797405060707505977243346704576],
     [996213673531855992829525358578006610606634622631,   1025711294257038288640877971869685565227647136954,  1432432135773706484846126533752827108541355741973,  1238541870126055576875033883691918425137600727481,   1130938956963588695293783764965618873887596017827],
     [1320933266015680090206505704792362493057963931979,  1151746112645644166669332171392580649376526147475,  117512451110908867093773368598681106589771485221,   78071463743800894350883457304401524272336187149,     350437511649326676405126284689545814008237687775],
     [438339253001275654203062260777687750937184662400,   372483950165136927369598298270629892810999203086,   859008773869616460027135965589262417694174453098,   1174526536643808668299968641952541506024584582818,   13201859260259503932772826643483081858286638179]
    ])

H = matrix(GF(p), 5, 5, [
     [903022231855038558383593109888227525558007552960,   565977275270298825053282757799743346899236483368,   989303675765663596792169321947495382568831693037,   601579288654704389384765634776493921679315260303,    913791750749394879333717884106841876340654737006],
     [1159121456278955861257379214176694847802842944213,  55304385436577133507085707981392660143782780650,    559867756424853909301288957105188829240808301823,   1230859641388132364539374469026906952870988170695,   1423995124592695628047882256427827379994877406997],
     [1125565199147204322161069021173152827232960621114,  1373772036013472137002755957284397215018630262515,  640623873603434273377865546046279663852895430999,   1056809237992218798189986002766547616222871640976,   1426649441470162608512662468308504390861950649943],
     [303729376872199895471546635639837180361513146712,   1163767872227950278851006729914569662442255257700,  1320342731346163804219021270875175061467772367004,  433001013681018647747911760920686992297849343282,    1149024280460224794070159244078925721991430685838],
     [23661702916810298505759145354543089608241235601,    1048655828654821525617176122368805879408325508567,  587846047820504813842423941849757078103027466928,   1338365929525105225695097114139069216753339875455,   1425543850003062038868121400064269552725872690214]
    ])

J, P = G.jordan_form(transformation=True)
I = ~P * H * P
alpha = J[3][3] * I[3][4] / I[4][4]

print flag_gen(alpha)
```

```
> ./matrices.sage
SharifCTF{e61ac2503f2cc2e8385db92afb59aac2}
```



### File: ctfs/sharif-2018/fhash/README.md

# fHash (crypto 200)

The task provides a program, [fHash.py](fHash.py),
that creates a hash from a message and two IVs.

The challenge is to obtain a collision with a different message.

Analyzing the hashing program, the input conssts in:

* The two IVs are 2 bytes hex encoded (strings of length 4)
* The message consists in 8 bytes hex encoded (string of length 16)

The algorithm first splits the message in 4 parts of 2 bytes each
and consists in a round per part (4 rounds in total).

Each round is divided in two parts, one per IV.
Both work the same way:
* Concatenate the IV and the of the message
* Obtain the md5 of the resulting string
* Take the first 2 bytes of the digest, in hex (string of length 4)
* Replace the original IV with the resulting string

Since rounds are independant of each other,
we can focus just on getting just a valid input (2 IVs and message block)
that generate the expected output.
Doing this backward, we can find the initial IVs and message after 4 rounds.

Inside a round the 2 IVs are independant but the message is shared,
so we just look for a pair of first IV + message block
that results in the expected output (next first IV).
When we found this pair, we use the found message and
try to find a second IV that when concatenated with this found message
results in the expected output (next second IV).

Since the outputs we are searching for are rather small (2 bytes each),
it should be pretty easy to find collisions,
so we can efficiently bruteforce a solution, as done by [solver.py](solver.py).



### File: ctfs/sharif-2018/fifteen-puzzle/README.md

# Fifteen Puzzle (misc ppc 150)

We are given [128 _15 puzzle_](puzzles.txt), each providing a bit of the flag.
Each bit is set if the puzzle is solvable and unset otherwise.
The task description also provides a code skeleton of how to generate the flag
from this solvability information.

Each puzzle is solvable if the parity of the inversions of the puzzle
matches with the parity of the row
where the empty square is located (starting with row 1 at the bottom).

So we gather all the pieces together to get the flag:

```python
def is_solvable(puzzle):
    x = [x.strip() for x in ''.join([x.strip()[1:] for x in puzzle]).split('|', 16)[:16]]
    blank = 4 - x.index('') / 4
    x.remove('')
    x = map(int, x)
    inv = 0
    for i in range(15):
        for j in range(i + 1, 15):
            if x[i] > x[j]:
                inv += 1
    return inv % 2 == blank % 2

with open('puzzles.txt') as f:
    lines = f.readlines()
flag = ' '
for i in range(128):
    flag = ('1' if is_solvable(lines[11*i+2:11*i+9:2]) else '0') + flag
print('SharifCTF{%016x}' % int(flag, 2))
```

Running it:

```
> python2 solver.py
SharifCTF{52d3b36b2167d2076b06d8101582b7af}
```



### File: ctfs/sharif-2018/oss-service-easy/README.md

# OSS Service (Easy) (crypto 100)

The task provides a [link](http://ctf.sharif.edu:8086/) where there is
a [file](OSS_Signature.pdf) with the description of
the Ong-Schnorr-Shamir (OSS) signature and the challenge,
which consists in a [known-plaintext attack](https://en.wikipedia.org/wiki/Known-plaintext_attack).
of the signature.

We are also provided a [verifier](verifier.py) to validate the signature.

So we have two equations, `x^2 + k*y^2 = m (mod n)` and `x'^2 + k*y'^2 = m' (mod n)`
where we know `x`, `y`, `x'`, `y'`, `m`, `m'`, `k` and `n`
and we need to generate valid `x''` and `y''` for `x''^2 + k*y''^2 = m * m' (mod n)`

In the 1984 paper _An Efficient Solution of the Congruence x^2 + k*y^2 = m (mod n)_,
Pollard and Schnorr explain that: `(x1^2 + k*y^1)(x^2 + k*y^2) (mod  n)`
can be expressed as `X + k*Y (mod n)` where `X = x1*x2 + k* y1*y2 (mod n)`
and `Y = x1*y2 - y1*x2 (mod n)`.

So we just implement that:

```python
from verify import n, k, m1, x1, y1, m2, x2, y2, public, verify

def mult(x1, y1, x2, y2, k):
    """(x1^2 + ky^1)(x^2 + ky^2)"""

    return (x1 * x2 + k*y1*y2) % n, (x1 * y2 - y1 * x2) % n


x, y = mult(x1, y1, x2, y2, k)
print(verify(public, (m1 * m2) % n, (x, y)))
print('x: {}\ny: {}'.format(x, y))
```

and get the needed parameters:

```
> python solver.py
True
True
True
x: 3228192414578958851010842513154275809496752450843437198583166196901565071578144066800517210864829309956656172864622172889502523814134130877601254638400747755883616155295299435314390972047946113969350548381594633322779945307216665767237995638888452882989503186673207123359630734140939449837354851424900356484212983667331443801108560693455298625538140549843770730178132648956596007707374948190919655158210892858713252214782069457662864873988983041011930880072395421594443371267339482128681654521226571357238152202622389403367075320562466814355917951666554746996134626758309948472069549094989922908904448493268680406656
y: 518211291241825120181140993092343983770941887615321384844260199425792523199755041385119471907237849603159990373526771913427402452760004430627136113781638542767114113264285000466398106908417951520749203743404777034613190657137114341923476307793861309763818494314271906586789936425240207459021063361770273109412368272889165718779882091684440429454382783604840684421214437897887818039810429139216497093192387409059198251459001969178988926945417318424698086613437960638555659525583532581962406409400074841700047111118522735841781583725367240630089427247980009202413865204658013579671962256648081403159372023040686179602
``` 

Submitting the obtained parameters, we get the flag: `SharifCTF{aea9d91c12817a8f5a19b37ee9e1b1d6}`



### File: ctfs/sharif-2018/oss-service-hard/README.md

# OSS Service (Hard) (crypto 500)

The task provides a [link](http://ctf.sharif.edu:8088/) (and a [mirror](http://8088.ctf.certcc.ir/)).

As in a previous [easy](http://ctf.sharif.edu:8086/) task,
we are asked to provide a valid OSS signature on a given message.
The difference is that we don't have any plaintext/ciphertext pair here to use
(so no [known-plaintext attack](https://en.wikipedia.org/wiki/Known-plaintext_attack) in this case.)

The OSS scheme is a cryptosystem proposed by Ong, Schnorr and Shamir
in the 1984 paper _An Efficient Signature Scheme Based on Quadratic Equations_,
based on the difficulty of solving equations of the kind `x^2 + k*y^2 = m (mod n)`,
where `n = p*q`, `m` is the message and `k` is the public key.

In the 1984 paper _An Efficient Solution of the Congruence x^2 + k*y^2 = m (mod n)_,
Pollard and Schnorr describes an algorithm to efficiently forge valid signatures
in the OSS scheme.

An explanation of both the scheme and the algorithm can also be found
[here](https://webcourse.cs.technion.ac.il/236500/Spring2016/ho/WCFiles/cryptanalysis-slides-03-sig-oss.1x1.pdf).

To solve this task we need to implement this algorithm.
We do so at [solver.sage](solver.sage)
and then validate it using the provided [verifier.py](verifier.py).



### File: ctfs/swampctf-2019/README.md

# Solutions for Swamp CTF 2019 challenges

You can also check the [official site](https://play.swampctf.com/),
[CTFtime site](https://ctftime.org/event/779)
and additional [writeups](https://ctftime.org/event/779/tasks/).

This repo contains the following solutions:

* [Needle-Eye's Apprentice](needle-eyes-apprentice) (Misc 495)



### File: ctfs/swampctf-2019/needle-eyes-apprentice/README.md

# Needle-Eye's Apprentice (misc 495)

The challenge provides the file [quadt.out](quadt.out).

Filename suggests a quadtree and description indicates the encoding (_He followed the path laid out for him, always clockwise and ever deeper_).

We write a [quadtree implementation](quadt.py) following the description and write the solution as an image: ![Flag](flag.png)

