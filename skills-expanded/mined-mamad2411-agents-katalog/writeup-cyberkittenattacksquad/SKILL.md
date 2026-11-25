<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cyberkittenattacksquad
description: CTF writeups and security challenges by CyberKittenAttackSquad.
---

# Writeups by CyberKittenAttackSquad

Source repository: `/repos/CyberKittenAttackSquad`

## Repository Index

- writeups/readme.md
- writeups/nuitduhack2016/toil33t.md
- writeups/jcc2016/re/labyrinth/readme.md
- writeups/jcc2016/re/shrek/readme.md
- writeups/jcc2016/nx/hive/readme.md

## Writeup Content


### File: writeups/jcc2016/nx/hive/readme.md

# hive

Hive, aka nx350, was a 350 point network exploitation challenge, the highest point-value nx challenge, and probably endeavor' favorite. Hive was solved by two people, shareef12 and endeavor.

Hive works in two parts. First, you have to successfully authenticate with the hive server. Second, you have to exploit the service. Endeavor did authentication, shareef12 put together the exploit.

## Authentication - *endeavor*

I seem to have misplaced my [binary ninja](http://binary.ninja/) file with all of my comments, so I'll make this writeup based on what I have. I'm also going to walk through my discovery process, instead of cutting straight to the answer.

The binary comes with symbols stripped, and libc (or some equivalent) statically linked in. Finding out, "Where we are in Kansas," was step number one.

I spent some time shooting around the binary, but eventually ended up just running in GDB, breaking, and tracking my way up the callstack.

```
(gdb) r
Starting program: /vagrant/ctf/jcc2016/nx/hive_clean 
The time is: 1463411643, please hurry with authenticating
Please provide your username: ^C
Program received signal SIGINT, Interrupt.
0x000000000043c550 in ?? ()
(gdb) bt
#0  0x000000000043c550 in ?? ()
#1  0x000000000040cdd0 in ?? ()
#2  0x000000000040f3be in ?? ()
#3  0x000000000040a7d4 in ?? ()
#4  0x000000000040a4e6 in ?? ()
#5  0x00000000004010c0 in ?? ()
#6  0x0000000000401047 in ?? ()
#7  0x0000000000402fe0 in ?? ()
#8  0x0000000000400f07 in ?? ()
(gdb) 
```

Several of these functions didn't disassemble in binary ninja, but I took some of these addresses and started hunting around for function preambles in the binary ninja hex view and manually disassembling functions. Eventually I found my way to sub_401058 (that's #5 in our back trace), and this is the function that handles authentication.

Of course, this wasn't the right way to do find this function. The right way to do this would be to start from `_start`, find `main`, and we would have found this function as the second one called. Normally this is what I would have done, but when there are only a few hours left in the CTF and you're desparate for points *sometimes* the decision making progress is a little flawed.

Let's go to `main` and take a look.

![binary ninja main()](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-main.png)

`do_authenticaton` is where our authentication takes place, and `target_function` is where we do our exploitation. I started on `do_authentication`.

About this time shareef12 came on slack and said `!working nx350`, which is our shorthand for announcing what we're working on. We spoke for a few minutes, and agreed shraeef12 would work the exploit and I would work auth.

About 30 minutes later re400, *movfu*, came up, and I switched over to *movfu*, leaving *hive* to shareef12. Shareef12 got a working local exploit in a couple hours, and I came back to finish the authentication.

Diving into the `do_authentication` function.

![binary ninja do_authenicate() 1](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-do_authentication_1.png)
![binary ninja do_authenicate() 2](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-do_authentication_2.png)

This function reads in three strings, a username, password, and token. The username is never used. I wasn't entirely sure what was going on here, so I broke before and after several of these functions, observing arguments going in and either the results or changes to buffers coming out. I have lost most of these comments, but in short for some of these calls I was observing strings going in, and 16-byte hexadecimal strings coming out.

I believed this was an MD5 function, but couldn't quite figure out what was gong on. Eventually I opened up the function now labeled `md5_string`, and the second function in there, `sub_4024d0` sets the `A`, `B`, `C`, `D` MD5 hash primitives. I now knew this `md5_string` function was correct.

![binary ninja md5_string()](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-md5_string.png)
![binary ninja sub_4024d0()](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-sub_4024d0.png)

The problem I was having here was not initially accounting for newlines being appended to the ends of my input strings. Once I understood the case, I could create the MD5 hashes needed, and verified we were using md5 here.

Pseudocode, non-valid C for this function, which is not 100% accurate but more-or-less functionally correct, would be:

```c
do_authenticate (long timestamp) {
    print_string("enter username");
    char pass[64] = get_string();
    print_string("enter password");
    char pass[64] = get_string();
    char * tmp = md5_string(pass, strlen(pass));
    strcpy(pass, tmp);
    print_string("enter token");
    char token[64] = get_string();
    strcat(pass, token);
    tmp = md5_string(pass, strlen(pass));
    strcpy(pass, tmp);
    probable_validate(pass, timestamp);
}
```

Moving forward to the function called `probable_validate`.

![binary ninja probable_validate() 1](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-probable_validate_1.png)
![binary ninja probable_validate() 2](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-probable_validate_2.png)

By setting GDB breakpoints and observing functions, I noticed we first perform some arithmetic over the timestamp, divide the original timestamp by this arithmetic, sprintf the result and `md5_string` it. We then do some permutation over a string pushed onto the stack, and this string looks like an md5 hash. We `strcat` the permutated string and the timestamp md5 hash together, md5 hash those, and compare that to the string we passed into `probable_validate(const char *, long)`.

By setting some breakpoints, we discover what the permutated string is.

```
Starting program: /vagrant/ctf/jcc2016/nx/hive_clean 
The time is: 1463413283, please hurry with authenticating
Please provide your username: user
Please provide your personal password: pass
Please provide an authentication token: token

Breakpoint 1, 0x0000000000401360 in ?? ()
(gdb) x/s $rdi
0x7fffffffe000: "5982aa26412a5dcd5b3d4ec740612d85"
(gdb) x/s $rsi
0x7fffffffdf80: "dbfb89a8706a2f47a30c7b8e49228218"
(gdb) 
```

The permutated string is `"5982aa26412a5dcd5b3d4ec740612d85"`. Pseudocode, non-valid C for this function, which is not 100% accurate but more-or-less functionally correct, would be:

```c
probable_validate (const char * auth_string, long timestamp) {
    long tmp = timestamp;
    do_some_stuff_to_tmp(&tmp);
    tmp = timestamp / tmp;
    char buf[32];
    sprintf(buf, "%d", tmp);
    const char * md5_timestamp = md5_string(buf, strlen(buf));
    char buf[64] = "8215nn59745n8qpq8o6q7rp073945q18";
    permutate_string(buf);
    strcat(buf, md5_timestamp);
    const char * result_hash = md5_string(buf);
    strcpy(buf, result_hash);
    if (strcmp(auth_string, buf)) {
        FAIL();
    }
    else {
        PASS();
    }
}
```

Based off this information, we need our two strings in `do_authentication`, IE the *password* and *token* strings, to be equal to the two strings passed to `strcat` in `probable_validate`. A quick google of the first hash, `5982aa26412a5dcd5b3d4ec740612d85`, returns the string `"5up3rm@n"`. This is our password.

The second string in `probable_validate` is based off a timestamp. Not wanting to bother with reversing the arithmetic taking place, I decided to patch the `hive` binary like so:

1. Nop out the three calls to `get_string` in `do_authentication`.
2. Replace the instruction at `0x40121d` with a jump to some custom assembly which performs a system call to `read`, and reads in a timestamp.
3. Let the original binary perform the arithmetic and hasing over our given timestamp.
4. Drop in some custom assembly at `0x4012bc` and call `puts` over the md5 hash string of our timestamp.
5. Call exit.

This patched binary is available in the `hive_patched` file. The assembly patches are available as comments in `hiveauth.py`.

I could now code out some interaction code in pwnlib, call my patched binary to get the correct timestamp string, and log into the challenge. The below code to authenticate with the server is available in `hiveauth.py`.

```python
def get_timestamp_hash (timestamp) :
    proc = subprocess.Popen('./hive_patched', stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate(struct.pack('<L', timestamp))
    return stdout[-33:]

sh = pwn.process('./hive_clean')

initial = sh.recv(1024)
timestr = re.findall('time is: (.*?),', initial)[0]
print '[+] timestr', timestr
timehash = get_timestamp_hash(int(timestr))
print '[+] timehash', timehash
sh.sendline('username')
sh.sendline('5up3rm@n')
sh.sendline(timehash)
```

This was passed on to shareef12, along with the hive_patched binary, so he could integrate this with his exploit and successfully exploit the remote process.


## Exploitation - *shareef12*

The full exploit is available in `nx350.py`. Perhaps shareef12 will come back at a later time and write up the vulnerability.



### File: writeups/jcc2016/re/labyrinth/readme.md

# labyrinth

Labyrinth was a 300 point re challenge. The binary starts up a bind tcp fork server on port 9999, and the player must solve four consecutive stages to retrieve a zip file, and then decrypt the zip file. Connecting to the server, we're presented with the following prompt:

```
Welcome to the Labyrinth.  If you can navigate the deadly maze and answer the Guardian's riddles you will find the knowledge you seek...
Which direction will you go?
(Enter the numeric value)
1 : Forward
2 : Left
3 : Right
```

Diving into the binary, we find these conditional jumps based on return values from the `check_input` function:

![bn-one](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-one.png)

The `check_input` function ensures our input is either `0x31`, `0x32`, or `0x33`, subtracts `0x30` from the input, and returns. This turns ASCII `'1'` to the byte value `0x1`, and so on. We find the first values needed to continue are: `12113`.

Moving on, we are presented with a question:

```
Welcome to the Labyrinth.  If you can navigate the deadly maze and answer the Guardian's riddles you will find the knowledge you seek...
Which direction will you go?
(Enter the numeric value)
1 : Forward
2 : Left
3 : Right
1
2
1
1
3
You come face to face with a large creature with a squid-like face.
A voice booms within your head!
When referring to computer memory, what does that acronym RAM stand for?
```

Taking a look at the code for these questions, we see we're pulling a pointer to the question from memory.

![bn-two](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-two.png)

Following the pointers....

![bn-three](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-three.png)

![bn-four](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-four.png)

We arrive at the questions and the answers in strings. We code those up in a lookup table so we can solve them:

```
questions_1 = []
questions_1.append(['When referring to computer', 'Random Access Memory'])
questions_1.append(['With over 17 million units', 'Commodore 64'])
questions_1.append(['Who is credited with', 'Charles Babbage'])
questions_1.append(['How many Gigabytes are', '1024'])
questions_1.append(['Crash Override and Acid Burn', 'Hackers'])
questions_1.append(['___ the Planet', 'Hack'])
questions_1.append(['What linux distro', 'Slackware'])
questions_1.append(['Also known as', 'Johnny Long'])
```

The next two stages are identical to the first stage, with the exception that the directions change. The same questions are used.

The fourth stage looks like this:

```
You've done well to make it this far.  To find the knowledge you seek you must answer my final question:
V2hhdCBlbmNvZGluZyBzY2hlbWUgaXMgdGhpcyBxdWVzdGlvbiB1c2luZz8=
```

Decoding the base64, we get the question, "What encoding scheme is this question using?."

If we look at the assembly, we'll see our answer to this question will go through a function called `translatify`, and then a `strncmp` will take place between the result of our translatified string and `"base64"`

![bn-five](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-five.png)

Let's take a look at `translatify`.

![bn-translatify](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-translatify.png)

This just has nope written all over it. We need an input for translatify that will cause the first 6 characters of the output to be base64. Is there another way to solve this without reversing this function?

Why yes, yes there is.

We will nop out all of the socket/fork stuff, nop out stages 1, 2, and 3, nop out some more things, and turn this binary into a simple program that reads in a string, and outputs the result of translatify. We then write up some simple genetic-algorithm-ishy code around this binary, and continually mutate our input until we find one that results in BASE64. Upon observation, we notice that subsequent characters influence the characters preceeding them, and by solving for BASE64 in order, or algorithm improves.

The code to solve for the key is in `gen.py`, and you will need to run it with `lab-solve`, which is our patched binary.

The output will look something like:

```
done with family 0
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
...
done with family 20
3 QmFzwl"{AtHSX*MpTa+
3 QmFzw?"{AbH_X*MpTaU
3 QmFzDP"8m=H@X6DMqaU
3 QmFz@lE{A,H@X%Qpwac
3 QmFzwl"{A1H@XrMpT8P
...
done with family 84
5 YmFzZTaxS!G*G|jCDE%
5 YmFzZTaNMuQjltjg@ES
5 QmFzZTaxIOC)#ezAya7
5 QmFzZTaH8$n8U_U"3]3
```

The numbers on the left represent how many characters we've solved for. Once it hits 6, we have a string which will result in "BASE64" as the output of translatify. We are almost done.

Once we've passed translatify, the remote server will password protect the binary with `keyData`.

![bn-keydata](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-keydata.png)

Running the binary a couple of times we notice that `keyData` will be equal to `BBBBAAAACCCCBASE64` where `BBBB` is the first four characters of the answer to our second question, `AAAA` is the first four character of the answer to our first question, and `CCCC` is the first four characters of the answer to our third question. Keep in mind our inputs will be uppercased by the binary.

We now have everything we need to solve the challenge, retrieve the remote binary, and decrypt it.

Code to solve this challenge is in `labyrinth.py`


### File: writeups/jcc2016/re/shrek/readme.md

# shrek

Shrek was a 250 or 300 point reverse-engineering challenge, I can't remember

I actually have no idea what was in Shrek, or how it was put together. I had some code available for blackbox analyzing challenges like this, and I adpated it for Shrek.

You will need [pintools](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool) installed for this challenge to work, and you will need to build the ManualExamples found in source/tools/ManualExamples. Adjust the paths.

Down at the end where you see `run('flag{_On10ns_aRe_a_ta57y_tR3a7_}' + c)` replace with `run('' + c)`. You'll get the output of each character, and the number of instructions that were executed with that character fed as input.

For example:

```
_ 97162
a 97162
b 97162
c 97162
d 97162
e 97162
f 97172
g 97162
h 97162
i 97162
j 97162
```

We see that ``f`` took more instructions to execute. Our first character is ``f``. We prepend that to our string passed to ``run()`` and solve for the next character.

This process could be automated, but all in all it took about 10-15 minutes to solve the problem manually. It would have taken more time to fix up the code to solve the problem automatically, make sure it worked right, and run the code.

```python
import subprocess
import os

PINTOOLS_PATH = '/home/dev/source/pin-3.0-76991-gcc-linux/'
TOOL_PATH = os.path.join(PINTOOLS_PATH, 'source/tools/ManualExamples/obj-ia32/inscount0.so')
MOVFU_PATH = '/home/dev/ctf/jcc2016/re/shrek'

chars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_+-={}[],./<>?'

def run (s) :
    cmd = [os.path.join(PINTOOLS_PATH, 'pin')]
    cmd += ['-t']
    cmd += [TOOL_PATH]
    cmd += ['--']
    cmd += [MOVFU_PATH]
    cmd += ['"' + s + '"']

    cmd = ' '.join(cmd)

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate(s)

    fh = open('inscount.out', 'rb')
    raw = fh.read()
    fh.close()
    count, n = raw.strip().split(' ')
    return int(n)


for c in chars :
    print c, run('flag{_On10ns_aRe_a_ta57y_tR3a7_}' + c)
```


### File: writeups/nuitduhack2016/toil33t.md

This is a web application which lets us log in using a username, password, and email. Once we login, we are provided with a cookie. We know that AES is being used, but we do not know the encryption mode. The goal is to login in as the administrator.  

One of the main issues when examining cookies is determining if there is any pattern between user input and resulting cookie. Discerning this input-output relationship is closely related to detecting the block cipher mode of operation. 

A method of detecting if an encrypted cookie was created using a weak mode (like ECB) is by solving the longest common substring problem. Usually ECB mode detection is demonstrated visually (https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29), but by computing the longest common substring of data steams you can detect weak cipher modes that preserve structure of the plaintext.

Let's say you have cookies 
* `e04a8615810d47c9feb9ac06df600ff0799a5dc4824d8f51e2a78524b1020705a6eaf0fe5db99c6755c21f277aff95020ea7708a8f28694887deb53b8ecd855ba90ef9d9ab0a1d5913baf5f4c592e484` 
* `32affc73397fb19aa02584ae58303cdb799a5dc4824d8f51e2a78524b1020705a6eaf0fe5db99c6755c21f277aff95020ea7708a8f28694887deb53b8ecd855b52e5c58271840c72e4ef70f717dd31e4` 

Computing the longest common substring gives the longest string that is a substring of two or more strings. This will indicate if there any plaintext data patterns in the ciphertext. 

In this case the longest common substring is `799a5dc4824d8f51e2a78524b1020705a6eaf0fe5db99c6755c21f277aff95020ea7708a8f28694887deb53b8ecd855b`.  

A long common substring tells you that the two encrypted cookies share data and usually means that ECB mode was used. The first cookies was created using the username 'a' and email 'a'. The second cookie was created using email 'b' and username 'b'. 

Looking the html source code of the web page we can find /session decrypts our cookie:

`{
  "email": "a",
  "is_admin": false,
  "show_ad": false,
  "username": "a"
}`  

So we know two pieces of information: 
* The structure of the plain text cookie (determined by /session ) 
* The encrypted cookie was created with AES in ECB mode (determined by longest common substring analysis) 

Once we know this we can mount a cut-paste-and-attack to manipulate the final form of the cookie based on our initial input. We want the cookie to decrypt with "is_admin" set to true.  



### File: writeups/readme.md

# Cyber Kitten Attack Squad Writeups

## Introduction

This repo holds writeups for some of the challenges solved by the CTF team Cyber Kitten Attack Squad (CKAS).

## About CKAS

Some of these writeups follow a narrative, explaining what is going on while we solve challenges. A couple of things about CKAS.

* Our team is small. As of this writing, six people.
* We use [pwntools](http://pwntools.readthedocs.io/en/2.2/) aka pwnlib. This help different people solve different portions of a challenge and quickly pass off work to one another.
* We communicate over slack. If everyone is working, we have two channels for a competition, the *main* channel and the *alternate* channel, so we can work multiple challenges without stepping on one another.
* We announce what we're working on with `!working <challenge_name>` and when we solve a challenge, we announce it with `!solved <challenge_name>`. This helps us ensure we aren't duplicating efforts. We periodically check on who is working on what throughout the CTF.
* We have a standard VM created using vagrant, ensuring everyone has access to a basic set of tools.


