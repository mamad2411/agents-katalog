<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xpanic
description: CTF writeups and security challenges by 0xPanic.
---

# Writeups by 0xPanic

Source repository: `/repos/0xPanic`

## Repository Index

- Writeups/auctf2020/README.md
- Writeups/utctf2019/README.md
- Writeups/utctf2020/README.md

## Writeup Content


### File: Writeups/auctf2020/README.md

![Description](/auctf2020/img/description.png)

Clicking the link took me to the default apache page, so I decided to go straight into gobuster to find other pages.

![Gobuster](/auctf2020/img/gobuster.png)

First time I ran it the /cgi-bin/ directory stood out to me, so I ran it again on that directory and discovered the scriptlet file located within.

![Scriptlet](/auctf2020/img/whoami.png)

This appears to be a bash script that just runs whoami. Since this is bash, let's try exploiting shellshock. (cgi-bin + ctf - user input = shellshock)

To begin, I intercepted the request firefox was making to the script in burpsuite

![Burp1](/auctf2020/img/burp1.png)

And then hitting ctrl + R to send it to the repeater to make things eaiser.
![Burp2](/auctf2020/img/burp2.png)

To test for shellshock, we can replace the user agent string with `() { :;}; echo; echo vulnerable` . If the response from the server contains the word `vulnerable`, we have a hit.

And it did.
![Burp3](/auctf2020/img/burp3.png)

My home network wouldn't allow me to catch a reverse shell, but burpsuite is all the shell I need at this point. After some poking around, I found something interesting at / (full path for ls was required)

![Burp3](/auctf2020/img/binls.png)

catting the file revealed hex data
![Burp3](/auctf2020/img/bincat.png)

So I threw that into cyberchef and decoded from hex. After decoding that cyberchef was nice enough to point out that this was gzipped data and just handed me the flag.
![Burp3](/auctf2020/img/cyberchef.png)

Success! This was a really fun challenge.




### File: Writeups/utctf2019/README.md

````
Our once-venerable president has committed the unspeakable crime of dine-and-dashing the pizza during
our own club meetings. He's on the run as we speak, but we're not sure where he's headed.

Luckily, he forgot that we had planted a packet sniffer on his laptop, and we were able to retrieve
the following capture when we raided his apartment:

https://storage.googleapis.com/utctf/capture.pcapng

He's too smart to email his plans to himself, but I'm certain he took them with him somehow. Can you 
help us figure out which country he's fleeing to?
````

This challenge consisted of a PCAP containing a large amount of USB packets.
![Wireshark](/utctf2019/img/wireshark.png)
This writeup describes in detail how to extract
these keystrokes from the file: https://medium.com/@ali.bawazeeer/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4

After following the steps to get the keystrokes extracted, I ran a slightly modified version of the script shown in the linked
writeup.

````
newmap = {
 2: "?",
 4: "a",
 5: "b",
 6: "c",
 7: "d",
 8: "e",
 9: "f",
 10: "g",
 11: "h",
 12: "i",
 13: "j",
 14: "k",
 15: "l",
 16: "m",
 17: "n",
 18: "o",
 19: "p",
 20: "q",
 21: "r",
 22: "s",
 23: "t",
 24: "u",
 25: "v",
 26: "w",
 27: "x",
 28: "y",
 29: "z",
 30: "1",
 31: "2",
 32: "3",
 33: "4",
 34: "5",
 35: "6",
 36: "7",
 37: "8",
 38: "9",
 39: "0",
 40: "Enter",
 41: "esc",
 42: "del",
 43: "tab",
 44: " ",
 45: "-",
 47: "[",
 48: "]",
 55: ".",
 56: "/",
 57: "CapsLock",
 79: "RightArrow",
 80: "LetfArrow"
 }

myKeys = open('hexoutput.txt')
i = 1
for line in myKeys:
    bytesArray = bytearray.fromhex(line.strip())
 #print "Line Number: " + str(i)
    for byte in bytesArray:
        if byte != 0:
            keyVal = int(byte)
 
            if keyVal in newmap:
                print newmap[keyVal]
            else:
                print "No map found for this value: " + str(keyVal)
 
    i+=1
````
after running the script and replacing newline chars with spaces, I got the following output:

`g p g g     - c   f f l l a a g g s g s . p p n n g Enter u t ? ? n ? ? o ? ? t ? f l a g ? ? [ ? t r y ? ? - ? h a a r r d e e r r ? ? ] ? Enter u t ? ? n ? ? o ? ? t ? f l a g ? ? [ ? t r y ? ? - ? h a r d e e r r ? ? ] ? Enter c p   f l a g g s s . p n g . g p g   / m e d i a / u s s e e r e r / ? ? u ? ? s ? ? b ? / Enter`

After removing dupicate characters and figuring out that consecutive question marks corresponds to the shift key being pressed, 
I was able to deduce what was being ran, the important parts being:
`gpg -c flags.png
utNOTflag{try_harder}`

So now I had to find a GPG file in the pcap and decode it with the discovered password. Finding the GPG file wasn't difficult
since it was the largest packet in the pcap:

![gpg packet in wirehsark](/utctf2019/img/gpgpacket.png)

After extracting the gpg file and running the command, I was able to decode the message:

![Decoded gpg](/utctf2019/img/data.png)

It's a file. After redirecting the decoded message to an empty file and running `file` on it, I was able to determine it was a PNG. Opening it revealed the following:

![image in GPG file](/utctf2019/img/theimage.png)

Which is not very useful, so I opened it up with stegsolve.jar and started flipping through different planes until finding:

![flag](/utctf2019/img/stegsolve.png)



### File: Writeups/utctf2020/README.md

# spooky store
```
It's a simple webpage with 3 buttons, you got this :)
```
Visiting this page revealed a website with 3 clickable buttons that displayed a location's latitute and longitute
![Page](/utctf2020/img/xxe1.png)

Intercepting the request in burpsuite revealed that the POST request is using XML
![POST Request](/utctf2020/img/xxe2.png)

Let's try modifying the post request to be a simple XXE payload to print /etc/passwd (this is the typical payload example that you will find with a google search)


![XXE](/utctf2020/img/xxe3.png)

This worked and printed /etc/passwd, which included the flag

![FLAG](/utctf2020/img/xxe4.png)


# epic admin pwn
```
this challenge is epic i promise
```
For this challenge we are presented with a simple login screen

![Login](/utctf2020/img/sqli1.png)

Start off by trying sql injection to login with user Admin and password 'or '1' ='1 is successful

![Login](/utctf2020/img/sqli2.png)

This gives us a static page, which is basically a dead end. Let's try using sqlmap to try and get something more out of the database.

To do this we intercept the login request in burpsuite and save it to a file called post.txt

![Login](/utctf2020/img/sqli3.png)

From here we run sqlmap. Normally I would use --sql-shell, but that wasn't working so I tried --dump instead.

![Login](/utctf2020/img/sqli4.png)

This successfully dumps the database, which included the flag.

