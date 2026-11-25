<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xd4y
description: CTF writeups and security challenges by 0xd4y.
---

# Writeups by 0xd4y

Source repository: `/repos/0xd4y`

## Repository Index

- Writeups/Contact/index.md
- Writeups/HackTheBox/index.md
- Writeups/Misc/index.md
- Writeups/Notes/index.md
- Writeups/TryHackMe/index.md
- Writeups/ctf/index.md
- Writeups/images/README.md

## Writeup Content


### File: Writeups/images/README.md

I put all the images I use for the webpages here.



### File: Writeups/Contact/index.md

---
layout: post
title: "Contact"
---

###### Contact

I hope you can learn from reading my writeups! If you have any suggestions or comments, please feel free to contact me: 

## Gmail
<a href = "mailto: 0xd4yWriteups@gmail.com">0xd4yWriteups@gmail.com</a>

## LinkedIn
<a href="https://www.linkedin.com/in/segev-eliezer/">https://www.linkedin.com/in/segev-eliezer/</a>

## HackTheBox Profile
<a href="https://www.hackthebox.eu/profile/140887">https://www.hackthebox.eu/profile/140887</a>

## TryHackMe Profile
<a href="https://tryhackme.com/p/Zezul">https://tryhackme.com/p/Zezul</a>

## Github
<a href="https://github.com/0xd4y">https://github.com/0xd4y</a>



### File: Writeups/HackTheBox/index.md

---
layout: post
title: "HackTheBox Writeups"
---

###### HackTheBox Writeups

### Easy


## Bank

This is a really cool box that has a couple of interesting twists. I go through the unintended solution (the way I went about the machine) and the intended solution. There is a lot to learn here about web security and networking, and I highly encourage you to read this writeup.

<a href="https://0xd4y.github.io/Writeups/HackTheBox/Bank%20Writeup.pdf" class="class2">Bank Writeup</a>


## Bastion

A very realistic box with many things to learn. Misconfigurations can be a dealbreaker when it comes to a certain attack vector. There has always been a conflict between security and convenience, and this box highlights it. I go very in-depth about multiple aspects in this box relating to bastion hosts and credential databases. I hope you learn as much from this writeup as I did from this challenge!

<a href="https://0xd4y.github.io/Writeups/HackTheBox/Bastion%20Writeup.pdf" class="class2">Bastion Writeup</a>

## Love 

This Windows box dealt with exploiting an SSRF vulnerability which allowed for the viewing of a sensitive webpage hosted internally on the target. After exploting a vulnerable version of "voting system" software, a shell as a low-privileged user was returned. Finally, by taking advantage of an HKLM misconfiguration, a shell as the SYSTEM user could be obtained (namely by installing a malicious MSI package).

<a href="https://0xd4y.github.io/Writeups/HackTheBox/Love%20Writeup.pdf" class="class2">Love Writeup</a>

## Writeup

Yes, this box is called Writeup. This box did not have many open ports and even included a DoS protection script to prevent gobusters. The problem is we had to discover certain directories in order to extract essential information about the web server. Come check out my writeup for Writeup, as you will learn a lot about hashes and enumeration.

<a href="https://0xd4y.github.io/Writeups/HackTheBox/Writeup%20Writeup.pdf" class="class2">Writeup Writeup</a>

#### Medium


## Active

This was a fantastic box about the Windows Active Directory service. It showed the importance of managing your passwords in a secure way, as well as having strong passwords that are hard to crack. Something that really makes this box stand out is not so much the vulnerabilities themselves, but rather the reason why they are easily exploitable in the first place. Microsoft essentially made themselves vulnerable, as they spoke a little bit too much on THEIR OWN website! Come check out the writeup to see what I mean.

<a href="https://0xd4y.github.io/Writeups/HackTheBox/Active%20Writeup.pdf" class="class3">Active Writeup</a>

## Writer

This system contained an SQL injection vulnerability which could be leveraged to not only log into an application with admin privileges, but also could be used to read local files on the target. After leaking the source code of the website, an insecure usage of handling files was exploited to get RCE. With a www-data shell on the system, an insecure password of a local user located in the SQL database was cracked. Eventually the system was fully compromised through misconfigurations relating to SMTP and APT.

<a href="https://0xd4y.github.io/Writeups/HackTheBox/Writer%20Writeup.pdf" class="class3">Writer Writeup</a>



### File: Writeups/Misc/index.md

---
layout: post
title: "Miscellaneous Writeups"
---

###### Misc

All writeups not related to TryHackMe or HackTheBox are posted on this page. 

# Pwnable.kr

<a href="http://pwnable.kr/">Pwnable.kr</a> is a website dedicated to providing reverse engineering and binary exploitation challenges at varying difficulties.

## Passcode

scanf() is a function that is widely used in C programs. This binary, which is seemingly secure, made subtle but dangerous programming mistakes that resulted in a security hole through which a user can manipulate memory. Since this binary is dynamically linked, overwriting the GOT entry subsequently forces the program to jump to memory of the attacker's choice when the manipulated function pointer gets called.

<a href="https://0xd4y.github.io/Writeups/Misc/Passcode%20Writeup.pdf" class="class2">Passcode Writeup</a>

# OverTheWire

<a href="https://overthewire.org/wargames/">OverTheWire</a> is a website that contains many different wargames ranging from learning Unix, binary exploitation, scripting, along with many other fun and instructional challenges.

## Narnia

This challenge was about binary exploitation. There were a total of nine binaries which increased in difficulty after each exploit. Common binary exploitation techniques are discussed in this report including ret2libc, shellcode injection, format string exploitation, among others. 

<a href="https://0xd4y.github.io/Writeups/Misc/Narnia%20Writeup.pdf" class="class2">Narnia Writeup</a>

## Behemoth

Behemoth is the sequel to Narnia and is rated to be slightly harder. In comparison to Narnia, it involved more reverse engineering exercises and required more knowledge of C. Each binary contained a different vulnerability ranging from PATH environment variable privilege escalation to buffer overflows, format string exploits, and bypassing shellcode filtering.

<a href="https://0xd4y.github.io/Writeups/Misc/Behemoth%20Writeup.pdf" class="class3">Behemoth Writeup</a>




### File: Writeups/Notes/index.md

---
layout: post
title: "Notes"
---

###### Notes

A collection of some of the notes that I wrote. These notes mainly include topics related to Information Security. 

## AWS - Security Specialty
Notes that I wrote in preparation for the Certified AWS Security - Specialty exam. These notes cover fundamental information about the AWS infrastructure. It is recommended that you install Obsidian and download the zip file instead. This way you can navigate through these notes a lot more quickly.

<a href="https://raw.githubusercontent.com/0xd4y/notes/main/AWS%20-%20Security%20Specialty/AWS%20-%20Security%20Specialty.pdf" class="class1">AWS Security - Specialty Notes</a>
<a href="https://github.com/0xd4y/notes/blob/main/AWS%20-%20Security%20Specialty/AWS-notes.zip" class="class1">AWS Security - Specialty Zip File</a>



### File: Writeups/TryHackMe/index.md

---
layout: post
title: "TryHackMe Writeups"
---

###### TryHackMe Writeups

### Easy

## Archangel
This box is a great introduction to the exploitation of a web server. It involves exploiting a web service through an LFI vulnerability and upgrading that to an RCE exploit via log poisoning. The method of escalating to root privileges is also instructive.

<a href="https://0xd4y.github.io/Writeups/TryHackMe/Archangel%20Writeup.pdf" class="class2">Archangel Writeup</a>

## Avengers

A fun CTF-like box with an easter egg and cool (unintended) foothold. I root this box in a quite unique way, which the author of the box certainly did not intend.

<a href="https://0xd4y.github.io/Writeups/TryHackMe/Avengers%20Writeup%20-%20Unintended%20and%20Secret%20.pdf" class="class2">Avengers Writeup</a>

## Wreath Network

This challenge involved exploiting a vulnerable network of three computers. Two of which were susceptible to exploitations of outdated software. The last machine involved a unique foothold centered around the creation of a malicious image file. I highly encourage you to read this writeup, as I go into detail about how Mimikatz, evil-winrm, and network pivoting work.

<a href="https://0xd4y.github.io/Writeups/TryHackMe/Wreath%20Writeup.pdf" class="class2">Wreath Network Writeup</a>

#### Medium

## Develpy

This box had a fun foothold, and it was a nice little challenge that showed the importance of making your programs secure. I highly recommend you read this writeup, as after exploiting the program, I go over how to patch it to make it more secure.

<a href="https://0xd4y.github.io/Writeups/TryHackMe/Develpy%20Writeup.pdf" class="class3">Develpy Writeup</a>

## Keldagrim

A realistic box. Many things were learned during this challenge, and I highly recommend reading this writeup.

<a href="https://0xd4y.github.io/Writeups/TryHackMe/Keldagrim%20Writeup.pdf" class="class3">Keldagrim Writeup</a>

##### Hard

## PythonPlayground

Python has a lot of features that some people may not know about. In this challenge, it was important to be creative throughout each step of exploitation and piece each compromised puzzle piece together.  

<a href="https://0xd4y.github.io/Writeups/TryHackMe/PythonPlayground%20Writeup.pdf" class="class4">PythonPlayground Writeup</a>



### File: Writeups/ctf/index.md

---
layout: post
title: "CTF Writeups"
---

###### CTF Writeups

Here are a collection of CTF writeups from various tournaments that I have participated in.

# RedPwn

## Ret2The-Unknown 

This challenge was about exploiting a binary via a return-to-libc attack (due to the enabled NX bit). The address of printf was provided to faciliate exploitation, however it was only given after passing in user input. This address could not be used for future execution of the binary due to the presence of ASLR. Nevertheless, despite the presence of the enabled NX bit and ASLR, the binary was vulnerable.

<a href="https://0xd4y.github.io/Writeups/ctf/Ret2The-Unknown%20Writeup.pdf" class="class1">Ret2The-Unknown Writeup</a>

