<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ashutosh1206
description: CTF writeups and security challenges by ashutosh1206.
---

# Writeups by ashutosh1206

Source repository: `/repos/ashutosh1206`

## Repository Index

- Crypto-CTF-Writeups/README.md
- Crypto-CTF-Writeups/2018/README.md
- Crypto-CTF-Writeups/2018/noxCTF/Decryptor/README.md
- Crypto-CTF-Writeups/2018/noxCTF/Trinity/README.md
- Crypto-CTF-Writeups/2018/noxCTF/WTF/README.md
- Crypto-CTF-Writeups/2018/hxp-CTF/daring/README.md
- Crypto-CTF-Writeups/2018/VolgaCTF-Quals/Nonsense/README.md
- Crypto-CTF-Writeups/2018/Tokyo-Westerns/Revolutional-Secure-Angou/README.md
- Crypto-CTF-Writeups/2018/Swamp-CTF/Locked-Dugeons-2/README.md
- Crypto-CTF-Writeups/2018/Pragyan-CTF/RSA's-Quest/README.md
- Crypto-CTF-Writeups/2018/N1CTF/RSA_Padding/README.md
- Crypto-CTF-Writeups/2018/Midnight-CTF-Quals/hm4c/README.md
- Crypto-CTF-Writeups/2018/Insomni'Hack-Teaser/Rule86/README.md
- Crypto-CTF-Writeups/2018/HackIT-CTF/Into-the-Darkness/README.md
- Crypto-CTF-Writeups/2018/Codegate-CTF-Preliminary/RSAbaby/README.md
- Crypto-CTF-Writeups/2018/ACEBEAR-Security-Contest/CNVService/README.md
- Crypto-CTF-Writeups/2017/MeePwn-CTF/Simpler-Than-RSA/README.md
- Crypto-CTF-Writeups/2017/Hack.lu-CTF/prime-enigma/README.md
- Crypto-CTF-Writeups/2017/CSAW-CTF-Quals/BabyCrypt/README.md
- Crypto-CTF-Writeups/2017/ASIS-CTF-Quals/DLP/README.md
- Crypto-CTF-Writeups/2017/ASIS-CTF-Finals/Gracias/README.md

## Writeup Content


### File: Crypto-CTF-Writeups/2017/ASIS-CTF-Finals/Gracias/README.md

# Gracias (Crypto, 287p)

```
Some people think that combination of cryptographic systems will definitely improve the security. That’s your turn to prove them wrong.
```

In this task, we get [encryption script](gracias.py) to exploit upon.
The task is not really difficult as it looks like. The challenge is to break the given multi-prime based RSA encryption.

A few steps in the encryption: 
1. Private and Public keys are generated using the same function `make_pubpri(nbit)` 
    a. The function generates primes `p` , `q` and `r` like conventional RSA encryption
    b. Along with public keys `n` and `e`, the function also generates a 2*nbit safe prime number `a` and another number `g` following the criteria given below
    c. So, the public key actually contains `n`, `e`, `a`, `g` and the private key contains `n`, `d`, `a`, `g`
2. The encryption function `encrypt(m, pub)` works as follows:
    a. Using the public key generated in Step-1, it generates two numbers k and K as `k = getRandomRange(2, a)` and `K = pow(g, k, a)`
    b. Now, instead of encrypting the message `m` using the public keys, it does the following operation to get ciphertext `c1` and `c2`:
        (i) `c1, c2 = pow(k, e, n), (m * K) % a`
    c. Returns `c1` and `c2` as ciphertext

The attack on this will work as follows:
1. Using `c1`, `e` and `n`, get the value of `k` 
2. Calculate `K` using `k` generated in Step-1
3. Finally calculate message `m` as `m = (c2 * (k^(-1) mod n)) mod n`

A direct Wiener's Attack will not work in this case since it doesn't exactly follow the criteria of `d` being less than `N^(1/4)`.

You can check this variant of Wiener Attack which works when the size of `d` is just a few bits greater than `N^(1/4)`. Paper on a variant of Wiener Attack [here](https://www.math.tugraz.at/~cecc08/abstracts/cecc08_abstract_20.pdf).

Conclusion from the paper which is significant for exploit of this challenge:
1. Along with d being the denominator of the convergent of the continued fraction of (e/n), the decryption exponent can also be written in the form:
    a. `d = r*q(m+1) + s*q(m)`

Here q(m+1) and q(m) are the (m+1)th and mth denominators of the convergents of the continued fraction of (e/n) respectively.

This is a script implementing the above conclusion:

```python
def wiener(e, n):
	m = 12345
	c = pow(m, e, n)
	q0 = 1

	list1 = continued_fraction(Integer(e)/Integer(n))
	conv = list1.convergents()
	for i in conv:
		k = i.numerator()
		q1 = i.denominator()

		for r in range(20):
			for s in range(20):
				d = r*q1 + s*q0
				m1 = pow(c, d, n)
				if m1 == m:
					return d
		q0 = q1
```
which will give us the decryption exponent:

`d = 100556095937036905102538523179832446199526507742826168666218687736467897968451`

Then we can write the following code to get the flag: 
```python
from Crypto.Util.number import *
 
k = pow(c1, d, n)
K = pow(g, k, a)
print long_to_bytes(c2 * inverse(K, a) % a)
```

This gives us the flag: `ASIS{Wiener_at7ack_iN_mUlt1_Prim3_RSA_iZ_f34sible_t0O!}`

If you want to check how I approached the challenge in detail, checkout my blog [here](https://masterpessimistaa.wordpress.com/2017/11/24/asis-finals-ctf-2017-gracias-writeup/).
The complete exploit script [here](exploit.py)





### File: Crypto-CTF-Writeups/2017/ASIS-CTF-Quals/DLP/README.md

# DLP

Challenge Points: 158

Ciphertext is generated as following:
```python
def encrypt(nbit, msg):
    msg = bytes_to_long(msg)
    p = getPrime(nbit)
    q = getPrime(nbit)
    n = p*q
    s = getPrime(4)
    enc = pow(n+1, msg, n**(s+1))
    return n, enc
```  
  
We know that enc = (n+1)<sup>msg</sup> mod n<sup>s+1</sup>  
Thus, according to Binomial Theorem we can write:  
The expansion of (n+1)<sup>msg</sup> is as follows:  
![equation](https://latex.codecogs.com/png.latex?\small&space;{msg\choose&space;0}n^{msg}&space;&plus;&space;{msg\choose&space;1}n^{msg-1}&space;&plus;&space;{msg\choose&space;2}n^{msg-2}&space;&plus;&space;...&space;&plus;&space;{msg\choose&space;msg-1}n&space;&plus;&space;{msg\choose&space;msg}n^{0})  
And so we can also write,  
![equation](https://latex.codecogs.com/png.latex?\small&space;({msg\choose&space;0}n^{msg-2}&space;&plus;&space;{msg\choose&space;1}n^{msg-3}&space;&plus;&space;...&space;&plus;&space;{msg\choose&space;msg-2})n^2&space;&plus;&space;{msg\choose&space;msg-1}n&space;&plus;&space;{msg\choose&space;msg}n^{0})  
Which can be written as,  
![equation](https://latex.codecogs.com/png.latex?\small&space;(x)n^2&space;&plus;&space;mn&space;&plus;&space;1) where,  
![equation](https://latex.codecogs.com/png.latex?\small&space;x&space;=&space;{msg\choose&space;0}n^{msg-2}&space;&plus;&space;{msg\choose&space;1}n^{msg-3}&space;&plus;&space;...&space;&plus;&space;{msg\choose&space;msg-2})  
If we take the above result and **divide it with n^2**, the following can be written: ![equation](https://latex.codecogs.com/png.latex?\small&space;xn^2&space;&plus;&space;mn&space;&plus;&space;1&space;\equiv&space;mn&plus;1&space;\pmod&space;{n^2})  
Since, n<sup>s+1</sup> is always greater than and divisible by n<sup>2</sup>, we can now calculate the message `msg` as:  
![equation](https://latex.codecogs.com/png.latex?\small&space;enc&space;\equiv&space;(n&plus;1)^{msg}&space;\pmod&space;{n^{s&plus;1}})  
![equation](https://latex.codecogs.com/png.latex?\small&space;enc&space;\equiv&space;(msg*n&space;&plus;&space;1)&space;\pmod&space;{n^2})  
Therefore,  
![equation](https://latex.codecogs.com/png.latex?{m&space;=&space;\frac{(enc\mod&space;n^2)&space;-&space;1}{n}}) 
  
Surprisingly, this is the single line exploit to the challenge: 
```python
hex(int((enc%n^2-1)/n))[2:].replace("L","").decode("hex")
```





### File: Crypto-CTF-Writeups/2017/CSAW-CTF-Quals/BabyCrypt/README.md

# BabyCrypt (Crypto, 350)

This challenge was a bit overrated, there were no complications in the challenge, as you will see when we discuss the writeup.

In this challenge, we are supposed to get the flag which is present in the server. The server has an input-output program running, which gives AES-ECB encryption of the input given to it. The encryption takes place as follows: 
1. Takes the input from the user
2. Appends `secret` (which is the flag here) to the input
3. Pads to make it a multiple of blocksize
4. Encrypts the resultant string using AES in ECB mode
5. Gives the ciphertext as the output

As you can see, we are only in control of the input which we are supposed to give to the server. Using the input that we give, we need to get the `secret` which is the flag.
Let us have a look at how the blocks are divided when we send an input of size equal to the blocksize (16 in this case): 
```
        1st Block | 2nd Block | 3rd Block | ...
        Input     | Secret    | secret+padding ...
```
The first block contains 16 bytes of our input, which is known to us. When we send an input of size one less than the blocksize, then the block division is as follows:
```
        1st Block | 2nd Block    | 3rd Block | ...
        x         | Secret[1:17] | secret[17:]+padding ...
```
Here `x = 15 bytes input + 1 byte secret`.
We know the first 15 bytes of block #1, we can simply brute force 256 possibilities of the 16th byte in block #1 by checking the corresponding ciphertexts of block #1.

![picture](https://i.imgur.com/bta3KOp.png)

For the second byte we send 14 random bytes + 1 byte of secret(we got from previous step) as the input to the server and then brute force for 2nd byte of secret which again has 256 possibilties. We keep on continuing this process to get each byte of the secret and finally get the flag:

![picture2](https://i.imgur.com/BFvygKf.png)

Flag: `flag{Crypt0_is_s0_h@rd_t0_d0...}`

In case you want to know how I approached the problem in detail, checkout my blogpost [here](https://amritabi0s.wordpress.com/2017/09/18/csaw-quals-2017-babycrypt-writeup/).
Check my complete exploit script for this challenge [here](exploit.py).



### File: Crypto-CTF-Writeups/2017/Hack.lu-CTF/prime-enigma/README.md

# Prime Enigma
  
**Challenge Points**: 50(+ 100)  
  
**Challenge Description**: Hey there fellow lizard how nice of you to drop by! Did you know those filthy humans really think that some numbers have special meanings? Seven, 13 and for some strange reason even 9000. Go and show them that a good prime does not make a secure cryptosystem!  
  
The following encryption is taking place:  
```python
g = 5
d = key
m = int(flag.encode('hex'), 16) % p

B = pow(g, d, p)  # Equation-1
k = pow(A, d, p)  # Equation-2
c = k * m % p     # Equation-3
```
Values p, A, g, B, c are known.  
**Encryption System**: ElGamal  
  
Prerequisites:  
1. Cyclic Groups
2. Discrete Logarithm Problem
3. Basic Number Theory
In case you are interested in understanding the exploit, but don't have much knowledge about Cyclic Groups and DLP, you can read about it here on my blog post: [Cyclic Groups, DLP and Baby Step Giant Step Algorithm](https://masterpessimistaa.wordpress.com/2018/01/14/dlp-and-baby-step-giant-step-algorithm/).
  
The entire exploit summed up:
1. We need to calculate the value of `d` by solving `Equation-1`
2. Calculate `k` using the value of `d` obtained from Step-1 in order to solve `Equation-2`
3. Calculate m = c * mod_inv(k, p) using the value of `k` obtained from Step-2 in order to solve `Equation-3`

**Solving Step-1**:  
We know from the property of Cyclic Groups that ![equation](https://latex.codecogs.com/png.latex?g^{|G|}&space;\equiv&space;1&space;\mod&space;p), where `|G|` is the cardinality/order of the Cyclic Group `G`. Cardinality i.e. the number of elements in the Cyclic Group, in this case, is `p-1`. Therefore we can write: ![equation](https://latex.codecogs.com/png.latex?g^{p-1}&space;\equiv&space;1&space;\mod&space;p) which is also known as [Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem).  
  
Note that B = p-1, which makes solving DLP a lot easier. We can now write:  
![equation](https://latex.codecogs.com/png.latex?p-1\equiv&space;g^d&space;\mod&space;p)  
which can also be written as:  
![equation](https://latex.codecogs.com/png.latex?g^d\equiv&space;-1&space;\mod&space;p)  
Upon squaring, we have:  
![equation](https://latex.codecogs.com/png.latex?g^{2d}\equiv&space;1&space;\mod&space;p)  
Comparing the above equation with ![equation](https://latex.codecogs.com/png.latex?g^{p-1}&space;\equiv&space;1&space;\mod&space;p), we can write:  
**d = (p-1)/2**   
  
**Solving Step-2**:  
Simple compute: ![equation](https://latex.codecogs.com/png.latex?k&space;=&space;A^d&space;\mod&space;p)  
  
**Solving Step-3**:  
Simply compute: ![equation](https://latex.codecogs.com/png.latex?m&space;=&space;ck^{-1}&space;\mod&space;p)  
  
Checkout the entire exploit script [here](exploit.py)



### File: Crypto-CTF-Writeups/2017/MeePwn-CTF/Simpler-Than-RSA/README.md

# Simpler Than RSA
  
Challenge Points: 100  
  
We are given an encryption script [simple.py](simple.py). Values of n, g, h are public other than the ciphertext. The following function is used to generate values for the challenge:  
![picture](https://i.imgur.com/0QUHha4.png)  
The encryption function:  
![picture](https://i.imgur.com/ORlFqDf.png)  
As we can see, the ciphertext for each character in the plaintext is generated separately. For the `ith` byte of message we can write the corresponding ciphertext as:  
![equation](https://latex.codecogs.com/gif.latex?c_i=((g^{m_i}\mod&space;n)*(h^{r}\mod&space;n))\mod&space;n)  
Given: ![equation](https://latex.codecogs.com/gif.latex?h=g^{n}\mod&space;n)  
We can now write:  
![equation](https://latex.codecogs.com/gif.latex?c_i=((g^{m_i}\mod&space;n)*(g^{nr}\mod&space;n))\mod&space;n)  
which gives us ![equation](https://latex.codecogs.com/gif.latex?c_i=g^{m_i&plus;nr}\mod&space;n)  
Since n=p*p*q,  
![equation](https://latex.codecogs.com/gif.latex?c_i=g^{m_i&plus;p^{2}qr}\mod&space;n)  
Raising both sides by (p-1)*(q-1), we have:  
![equation](https://latex.codecogs.com/gif.latex?c_i^{(p-1)*(q-1)}\mod&space;n=g^{(m_i&plus;p^{2}qr)*(p-1)*(q-1)}\mod&space;n)  
![equation](https://latex.codecogs.com/gif.latex?c_i^{(p-1)*(q-1)}\mod&space;n=g^{(m_i*(p-1)*(q-1))&plus;(p*(p-1)*(q-1)*nr)}\mod&space;n)  
Since phi(n) = p*(p-1)*(q-1),  
![equation](https://latex.codecogs.com/gif.latex?c_i^{(p-1)*(q-1)}\mod&space;n=(g^{(m_i*(p-1)*(q-1))}*g^{nr\phi(n)})\mod&space;n)  
Euler's theorem states that when GCD(a, n) == 1: ![equation](https://latex.codecogs.com/gif.latex?a^{\phi(n)}\equiv1\mod&space;n)  
We can now write,  
Equation(a): ![equation](https://latex.codecogs.com/gif.latex?c_i^{(p-1)*(q-1)}\mod&space;n=g^{m_i*(p-1)*(q-1)}.1\mod&space;n)  
We have now eliminated `r` from the equation, let us first get the factors of n, trying it on [factordb.com](factordb.com) gives us the factors as:  
```
    p = 1057817919251064684989791981
    q = 1103935256393984899021164397
```  
Now that we have the factors, we can use Equation(a) to get solution for each ciphertext byte. For each byte, we just have to check for 256 possibilities of corresponding message byte and a total of 54*256 brute-force checks to get the flag(We already know the other values in Equation(a): p,q,ciphertext byte). The exploit:  
```python
list1 = open("enc.txt",'r').read()[1:-2]
list1 = list1.split(",")
list1 = [int(i[:-1]) for i in list1]
list1 = [pow(i, (p-1)*(q-1), n) for i in list1]
msg = ""
for i in list1:
	for j in range(1, 256):
		if pow(g, j*(p-1)*(q-1), n) == i:
			msg += chr(j)
	print msg
```  
This gives us the flag: MeePwnCTF{well_is_fact0rizati0n_0nly_w4y_to_s0lve_it?}  
Check out the entire exploit script [here](exploit.py)




### File: Crypto-CTF-Writeups/2018/ACEBEAR-Security-Contest/CNVService/README.md

# CNVService
  
**Challenge Points**: 856  
  
**Challenge Description**:   
  
Check out my writeup for this challenge on my blog [here](https://masterpessimistaa.wordpress.com/2018/01/31/cnvservice-acebear-ctf-2018-writeup/)  




### File: Crypto-CTF-Writeups/2018/Codegate-CTF-Preliminary/RSAbaby/README.md

# RSAbaby
The idea behind the challenge involved knowledge of basic Number Theory which was pretty cool.  
  
We are given a couple of parameters and an encryption script which is used for encrypting the message. Everything in the script works normally except the `GenerateKeys` function:  
![picture](https://i.imgur.com/RdXt8bo.png)  
There is are two extra variables other than the regular public key parameters whose values are known: `g` and `h`  
  
I think the challenge creators left two different intentional vulnerabilities- one was bit by bit decryption and the other was a simple application of number theory. We discuss exploiting `g` using simple yet interesting application of number theory  

## The exploit
We know that:  
![equation](https://latex.codecogs.com/gif.latex?g=d*(p-0xdeadbeef))  
![equation](https://latex.codecogs.com/gif.latex?eg=ed*(p-0xdeadbeef))  
![equation](https://latex.codecogs.com/gif.latex?2^{eg}=2^{ed*(p-0xdeadbeef)})  
![equation](https://latex.codecogs.com/gif.latex?2^{eg}\mod&space;n=2^{ed*(p-0xdeadbeef)}\mod&space;n)  
Thus we can write,  
![equation](https://latex.codecogs.com/gif.latex?2^{ed*(p-0xdeadbeef)}=2^{(1&plus;k\phi(n))*(p-0xdeadbeef)})  
![equation](https://latex.codecogs.com/gif.latex?2^{(1&plus;k\phi(n))*(p-0xdeadbeef)}=(2*2^{k\phi(n)})^{(p-0xdeadbeef)})  
![equation](https://latex.codecogs.com/gif.latex?(2*2^{k\phi(n)})^{(p-0xdeadbeef)}=2^{(p-0xdeadbeef)}*2^{k*\phi(n)*(p-0xdeadebeef)})  
We know from Euler's Theorem that when GCD(a, n) == 1:  
![equation](https://latex.codecogs.com/gif.latex?a^{\phi(n)}\equiv1\mod&space;n)  
![equation](https://latex.codecogs.com/gif.latex?2^{(p-0xdeadbeef)}*2^{k*\phi(n)*(p-0xdeadebeef)}\equiv2^{p-0xdeadebeef}*1\mod&space;n)  
![equation](https://latex.codecogs.com/gif.latex?2^{eg}\mod&space;n=2^{p-0xdeadbeef}\mod&space;n)  
![equation](https://latex.codecogs.com/gif.latex?2^{eg}*2^{0xdeadbeef}\mod&space;n=2^{p}\mod&space;n)  
We know from Fermat's Little Theorem that when GCD(a, p) == 1:  
![equation](https://latex.codecogs.com/gif.latex?a^{p}\equiv&space;a\mod&space;p)  
We can now write:  
![equation](https://latex.codecogs.com/gif.latex?2^{eg}*2^{0xdeadbeef}\mod&space;n=(kp&plus;2)\mod&space;n)  
Thus,  
![equation](https://latex.codecogs.com/gif.latex?2^{eg}*2^{0xdeadbeef}-2\mod&space;n=kp\mod&space;n)  
will be a factor of the RSA modulus N.  
We can easily get one of the factors of N as p = GCD(2^(eg + 0xdeadbeef) mod N - 2, N) and q = N/p  

## Exploit script
Checkout the complete exploit script [here](exploit.py)


### File: Crypto-CTF-Writeups/2018/HackIT-CTF/Into-the-Darkness/README.md

# Into The Darkness

Detailed explanation coming soon I hope :P  

Exploit script for this challenge: [exploit.py](exploit.py)  
  
If you want to know CBC Bit Flipping attack, read about it here: https://masterpessimistaa.wordpress.com/2017/05/03/cbc-bit-flipping-attack/  

Similar Challenges:
1. CTFZone CTF Quals 2018: [USSH-3.0](https://masterpessimistaa.wordpress.com/2018/07/23/exploiting-cookie-auth-mechanism-ctfzone-ussh-3-0-write-up/)
2. ACEBEAR CTF 2018: [CNVService](https://masterpessimistaa.wordpress.com/2018/01/31/cnvservice-acebear-ctf-2018-writeup/)
  

tl;dr chained CBC Bit Flipping Attack


### File: Crypto-CTF-Writeups/2018/Insomni'Hack-Teaser/Rule86/README.md

# Rule86
  
**Points**: 78  
  
**Description**: Kevin is working on a new synchronous stream cipher, but he has been re-using his key.
  
Check out my writeup for this challenge [here](https://masterpessimistaa.wordpress.com/2018/01/23/rule86-insomnihack-teaser-2018-writeup/)  
Other write-ups using z3 to solve the challenge: [https://ctftime.org/writeup/8563](https://ctftime.org/writeup/8563)  


### File: Crypto-CTF-Writeups/2018/Midnight-CTF-Quals/hm4c/README.md

# Hm4c
  
**Challenge Points**: 50  
  
**Challenge Description**: Some n00b implemented a HMAC, I'm sure you can pwn it  
  
We are given [hm4c.py](hm4c.py) running on `crypto.midnightsunctf.se` and port number `31337`. The script basically generates a custom HMAC of `FLAG` + (`input` that we give to it). This is how the HMAC is generated:  
![Picture1](Pictures/Picture1.png)  
As we can see, the server returns the SHA256 hash of `(FLAG ^ input) + input`. This is what makes this challenge vulnerable to Bit by Bit Decryption, let us see how:  
1. To get the SHA256 of FLAG we just send base64 encoded string of `\x00` as the output will be SHA256((FLAG ^ 0) + 0) = SHA256(FLAG)
2. Starting from LSB, we analyse the value returned by the function when the last bit of our input is **1**
   - If the last bit of FLAG is 1 then the last bit of `(FLAG ^ input) + input` will be `(1 ^ 1) + 1 = 0 + 1 = 1` which is the same as the last bit of the FLAG and hence the HMAC won't change.
   - If the last bit of FLAG is not 1, then the last bit of `(FLAG ^ input) + input` will be `(0 ^ 1) + 1 = 10`; although the last bit is same here again, but notice that one bit of just before the last bit has changed and hence the HMAC will change.
3. Now, we can use the same concept to get every bit of FLAG as follows:
   - Send 1, 2, 4, 8, ..., 2**`i` as an input and check if the the output for each input matches with the SHA256 of FLAG obtained in Step-1.
     - If it matches, then the `i`th bit of FLAG is 1, otherwise it is 0
  
  

I wrote the following python implementation of the exploit:  
```python
flag = ""
r = process("./hm4c.sh")
r.recvline().replace("\n","")
for i in range(256):
	r.recvline().replace("\n","")
	r.recvline().replace("\n","")
	r.recvline().replace("\n","")
	r.sendline("1")
	r.recvline().replace("\n","")

	r.sendline(int_to_base64(1<<i))
	recvd = r.recvline().replace("\n","")
	if int(recvd) == base_hash:
		flag += "1"
	else:
		flag += "0"

flag = flag[::-1]
print "[+] Got the flag: ", long_to_bytes(int(flag,2))
```
Check out the entire exploit script [here](exploit.py)  




### File: Crypto-CTF-Writeups/2018/N1CTF/RSA_Padding/README.md

# RSA_Padding

**Challenge points**: 303  
  
**Challenge Description**: babyRSA  
  
There are two steps involved in the challenge:
1. Proof of Work
2. RSA encryption using user defined padding

## Proof of Work
We are given with the following condition to bypass as PoW:  
![picture](Pictures/pow.png)  
There is not much to explain here, wrote the following script to bypass the above conditions:
```python
from pwn import *
import hashlib
import string
from Crypto.Util.number import *
 
r = remote("47.75.39.249",'23333')
 
r.recvline()
str1 = r.recvline().strip()
print "condition: ", str1
 
prepend = str1[8:14]
sha_end = str1[len(str1)-15:len(str1)-10]
 
for i in string.letters + string.digits:
    for j in string.letters + string.digits:
        for k in string.letters + string.digits:
            for l in string.letters + string.digits:
                var = hashlib.sha256(prepend + i + j + k + l).hexdigest()[:5]
                if var == sha_end:
                    print "gotit!"
                    print "happening: ", r.recvline()
                    r.recvline()
                    r.sendline(i + j + k + l)
                    print r.recvuntil("want?\n\n")
                    r.interactive()
                    r.sendline("1")
                    print r.recvall()
                    exit()
                    break
print "Failed!"
```
  
## Message encryption using padded RSA
Upon successful validation of PoW, we are given a choice to select:  
![picture](Pictures/server.png)  
1. get code
2. get message

We first select "get code" and get the source code of the encryption:  
```python
#!/usr/bin/env python3
# -*- coding=utf-8 -*-
 
from Crypto.Util.number import getPrime, GCD, bytes_to_long
from hashlib import sha256
import random
import signal
import sys, os
 
signal.alarm(20)
 
m = b"xxxxxxxxxxxxxx"
n = 21727106551797231400330796721401157037131178503238742210927927256416073956351568958100038047053002307191569558524956627892618119799679572039939819410371609015002302388267502253326720505214690802942662248282638776986759094777991439524946955458393011802700815763494042802326575866088840712980094975335414387283865492939790773300256234946983831571957038601270911425008907130353723909371646714722730577923843205527739734035515152341673364211058969041089741946974118237091455770042750971424415176552479618605177552145594339271192853653120859740022742221562438237923294609436512995857399568803043924319953346241964071252941
e = 3
 
def proof():
    strings = "abcdefghijklmnopqrstuvwxyzWOERFJASKL"
    prefix = "".join(random.sample(strings, 6))
    starwith = str(random.randint(10000, 99999))
    pf = """
sha256("%s"+str).hexdigest().startswith("%s") == True
Please give me str
"""%(prefix, starwith)
    print(pf)
    s = input().strip()
    if sha256((prefix+s).encode()).hexdigest().startswith(starwith):
        return True
    else:
        return False
 
def cmd():
    help = """
1. get code
2. get flag
Please tell me, what you want?
"""
    while True:
        print(help)
        c = input().strip()
        if c == "1":
            return True
        elif c == "2":
            return False
        else:
            print("Enter Error!")
 
def main():
    if not proof():
        print("Check Failed!")
        return
    welcom()
    if cmd():
        f = open("file.py")
        print(f.read())
        return
    mm = bytes_to_long(m)
    assert pow(mm, e) != pow(mm, e, n)
    sys.stdout.write("Please give me a padding: ")
    padding = input().strip()
    padding = int(sha256(padding.encode()).hexdigest(),16)
    c = pow(mm+padding, e, n)
    print("Your Ciphertext is: %s"%c)
 
if __name__ == '__main__':
    main()
```

From the code we observe the following:

1. When we select “get flag” option, the server encrypts the contents of flag file by padding it with sha256 of the string that we wish to give and then encrypting it using public key exponent e = 3 and a different modulus n (public) generated each time. This is where the vulnerability lies in the code.
2. Returns the ciphertext

Mathematically the encryption happens as follows:  
c = (m + sha256(pad))^3 % n  
Note that m^3 > n  

### The vulnerability
Allowing user controlled padding exposes the challenge to the attack described below  

### The exploit
Note that the server appends sha256 of the input to the message before encryption.  
  
First, we send ‘2’ as an input to the server and get the ciphertext:  
```python
c1 = 14550589053226237723784378782911157204367764723816957959635387925652898370034365455451983914571405062459535687617841302966938233065296973978472553109061974458935966754832788411876301179210585984208608247433383774246743661884093657109502619626436726032508763685599880808525861655167503719155953736308920858354069083437923495143680174206534169208623366776314544036377265501358254923029291010047210371394197963442022610746743020719292018028518885149189744832788117626194748311114409968846879212425054195323473068436359069318372735069308398135560733890706617536127579272964863500568572120716434126233695562326533941909353
```  
The following computation happens when we send the input as ‘2’:  
1. hash1 = int(sha256('2').hexdigest(), 16)
2. c1 = pow(m + hash1, e, n)
  
  

Next, send '1' as an input to the server and get the ciphertext:  
```python
c2 = 14550589053226237723784378782911157204367764723813789158271625147472004207734354619642445255036997940341703539883653916130592718879734436263217819317202435434496341973502556894834798718992952369685841347018901038478081710519253844078907000973324354805502890255414196801758171762906898874914776720897920729518384393581853690034053515213192846817920534901501370942556249012415259244063185938984570137371682805276444650716010228924732495062415330875872004691866847132147232457398743319930259327973290858489741376000333603734294893832124907092640953321640151851853501528390729805151850605432707293088635480863375398001441
```  
The following computation happens when we send the input as ‘1’:  
1. hash2 = int(sha256('1').hexdigest(), 16)
2. c2 = pow(m + hash2, e, n)
  
  

Now that we have values of hash1(or h1), hash2(or h2), c1 and c2, we can use them to get m. Let us see how:  
![picture](Pictures/1.gif)  
![picture](Pictures/2.gif)  
![picture](Pictures/3.gif)  
![picture](Pictures/4.gif)  
![picture](Pictures/5.gif)  
![picture](Pictures/6.gif)  
![picture](Pictures/7.gif)  
![picture](Pictures/8.gif)  
where a = 3, b = 3*(h1 + h2), c = (h1^2 + h1*h2 + h2^2) – x  
  
I wrote the following code to implement the above calculation and get the flag:  
```python
import hashlib
import gmpy2
from Crypto.Util.number import *

hash1 = int(hashlib.sha256('2').hexdigest(), 16)
hash2 = int(hashlib.sha256('1').hexdigest(), 16)
diff = hash1 - hash2
print "diff: ", diff

# M1 = M2 + diff
n = 21727106551797231400330796721401157037131178503238742210927927256416073956351568958100038047053002307191569558524956627892618119799679572039939819410371609015002302388267502253326720505214690802942662248282638776986759094777991439524946955458393011802700815763494042802326575866088840712980094975335414387283865492939790773300256234946983831571957038601270911425008907130353723909371646714722730577923843205527739734035515152341673364211058969041089741946974118237091455770042750971424415176552479618605177552145594339271192853653120859740022742221562438237923294609436512995857399568803043924319953346241964071252941L
e = 3

c1 = 14550589053226237723784378782911157204367764723816957959635387925652898370034365455451983914571405062459535687617841302966938233065296973978472553109061974458935966754832788411876301179210585984208608247433383774246743661884093657109502619626436726032508763685599880808525861655167503719155953736308920858354069083437923495143680174206534169208623366776314544036377265501358254923029291010047210371394197963442022610746743020719292018028518885149189744832788117626194748311114409968846879212425054195323473068436359069318372735069308398135560733890706617536127579272964863500568572120716434126233695562326533941909353
c2 = 14550589053226237723784378782911157204367764723813789158271625147472004207734354619642445255036997940341703539883653916130592718879734436263217819317202435434496341973502556894834798718992952369685841347018901038478081710519253844078907000973324354805502890255414196801758171762906898874914776720897920729518384393581853690034053515213192846817920534901501370942556249012415259244063185938984570137371682805276444650716010228924732495062415330875872004691866847132147232457398743319930259327973290858489741376000333603734294893832124907092640953321640151851853501528390729805151850605432707293088635480863375398001441
assert c2 < n
assert c1 < n
assert c1 > c2
res = (c1 - c2) / (hash1 - hash2)

a = 3
b = 3*(hash1 + hash2)
c = (hash1**2 + hash1*hash2 + hash2**2) - res
assert b**2 - 4*a*c >= 0

det = gmpy2.iroot(b**2 - 4*a*c, 2)
#Result of the above operation
det = 895117860555194221639962847152553327251877885494596369020458400464169641215830527612022789636620223733091925404109820014339798528983673228478908782900199621057014409705139235003835944181120537080102658020544028036693589036615231884111568905196654L
sol1 = (det - b)/(2*a)
print long_to_bytes(sol1)
```  
Running the above exploit script gives us: Welcom to Nu1L CTF, Congratulations, You get flag, and flag is **N1CTF{f7efbf4e5f5ef78ca1fb9c8f5eb02635}**. Check out the entire exploit [here](exploit.py)   





### File: Crypto-CTF-Writeups/2018/Pragyan-CTF/RSA's-Quest/README.md

# RSA's Quest
  
**Challenge Points**: 200  
  
**Challenge Description**: Rivest comes up with an encryption, and Shamir creates a service for decrypting any cipher text encrypted using Rivests’s encryption. Adleman is asked to decrypt a specific ciphertext, but he is not able to do so directly through Shamir’s service. Help him out.  
  
Check out my writeup for this challenge on my blog [here](https://masterpessimistaa.wordpress.com/2018/03/04/pragyan-ctf-rsas-quest/)  



### File: Crypto-CTF-Writeups/2018/README.md

# 2018 Crypto Writeups

Writeups of the following challenges from CTFs:  

| S.No. | CTF name                                             | Challenge-Name                                          | Points | Vulnerability/Concept   | Level of Difficulty |
|-------|:----------------------------------------------------:|:-------------------------------------------------------:|:------:|:-----------------------:|:-------------------:|
| 1     | [Insomni'hack teaser](https://ctftime.org/event/545) | [Rule86](Insomni'Hack-Teaser/Rule86/)                   | 78     | Number Theory/z3        |                     |
| 2     | [ACEBEAR Security Contest](https://ctftime.org/event/564) | [CNVService](ACEBEAR-Security-Contest/CNVService/) | 856    | CBC-Bit Flipping Attack |                     |
| 3     | [Codegate Preliminary](https://ctftime.org/event/542)| [RSAbaby](Codegate-CTF-Preliminary/RSAbaby/)            | 349    | Euler's Thm + FLT on RSA|                     |
| 4     | [Pragyan CTF](https://ctftime.org/event/581)         | [RSA's Quest](Pragyan-CTF/RSA's-Quest/)                 | 200    | Chosen Ciphertext Attack|                     |
| 5     | [N1CTF](https://ctftime.org/event/584)               | [Baby N1ES](N1CTF/baby_N1ES/)                           | 85     | Feistel Network Reverse |                     |
| 6     | [N1CTF](https://ctftime.org/event/584)               | [RSA Padding](N1CTF/RSA_Padding/)                       | 303    | Franklin Reiter's related message attack |    |
| 7     | [b00t2root'18](https://ctftime.org/event/589)        | [RSA-2](b00t2root'18/RSA-2/)                            | 200    | Franklin Reiter's related message attack |    |
| 8     | [Volga CTF Quals](https://ctftime.org/event/539/tasks/) | [Nonsense](VolgaCTF-Quals/Nonsense/)                 | 200    | Number Theory           |                     |
| 9     | [Swamp CTF](https://ctftime.org/event/590)           | [Locked-Dungeons-2](Swamp-CTF/Locked-Dugeons-2/)        | 498    | CBC-Bit Flipping Attack |                     |
| 10    | [Midnight Sun CTF Quals](https://ctftime.org/event/595)| [Hm4c](Midnight-CTF-Quals/hm4c/)                      | 50     | Bit by Bit decryption   |                     |
| 11    | [Meepwn CTF Quals](https://ctftime.org/event/625)    | [Bazik](Meepwn-CTF-Quals/bazik/)                        | 100    | Coppersmith's Stereotyped |                   |
| 12    | [Tokyo Westerns CTF](https://ctftime.org/event/651)  | [Revolutional-Secure-Angou](Tokyo-Westerns/Revolutional-Secure-Angou)| nil | Number Theory + RSA |               |
| 13    | [noxCTF](https://ctftime.org/event/671)              | [WTF](noxCTF/WTF/)                                      | 742    | Wiener's Attack         |                     |
| 14    | [noxCTF](https://ctftime.org/event/671)              | [Trinity](noxCTF/Trinity/)                              | 794    | Hastad's Broadcast Attack |                   |
| 15    | [noxCTF](https://ctftime.org/event/671)              | [Decryptor](noxCTF/Decryptor/)                          | 447    | Chosen Ciphertext Attack |                    |
| 16    | [HackIT CTF](https://ctftime.org/event/672)          | [Into The Darkness](HackIT-CTF/Into-the-Darkness/)      | 862    | CBC Bit Flipping Attack |                     |
| 17   | [HITCON CTF](https://ctftime.org/event/669) | [Lost-Key](HITCON-CTF/Lost-Key/) | 257 | LSByte Oracle Attack |   |
| 18   | [CSAW CTF Finals](https://ctftime.org/event/696) | [Disastrous Security](CSAW-Finals/DisastrousSecurity) | 400 | Breaking MTRNG to get `k` and forge DSA |        |
| 19   | [Hxp CTF](https://ctftime.org/event/647) | [Daring](hxp-CTF/daring/) | 105 | Weak padding + Number Theory + small RSA exponent |        |



### File: Crypto-CTF-Writeups/2018/Swamp-CTF/Locked-Dugeons-2/README.md

# Locked-Dungeons-2
  
**Challenge Points**: 498  
  
**Challenge Description**: The Dungeon Keeper learned from its mistake. This next lock is protected by even stronger encryption. We’re so close to the final level…there has to be a way in.  
  
Encryption Script [here](enter_the_dungeon2.py)  
Check out my writeup for this challenge on my blog [here](https://masterpessimistaa.wordpress.com/2018/04/03/swamp-ctf-2018-locked-dungeons-2-write-up/)  



### File: Crypto-CTF-Writeups/2018/Tokyo-Westerns/Revolutional-Secure-Angou/README.md

# Revolutionary Secure Angou

**Challenge Points**:  
  
**Challenge Description**: [No Description]

In this challenge, we are given an encryption script written in ruby that encrypts the flag using RSA. We are also given the [public key](publickey.pem) and [ciphertext](flag.encrypted). Let us analyse the encryption script first:  

```ruby
require 'openssl'

e = 65537
while true
  p = OpenSSL::BN.generate_prime(1024, false)
  q = OpenSSL::BN.new(e).mod_inverse(p)
  next unless q.prime?
  key = OpenSSL::PKey::RSA.new
  key.set_key(p.to_i * q.to_i, e, nil)
  File.write('publickey.pem', key.to_pem)
  File.binwrite('flag.encrypted', key.public_encrypt(File.binread('flag')))
  break
end
```
As you can see, private key parameters are not generated as they are supposed to be. Specifically, although `p` is a pseudo-random prime generated using OpenSSL, but `q` is generated as ![picture](Pictures/1.gif). Looks fishy! Also, there are no other suspicious lines of code as everything else looks fine. So now we know where we have to focus to find the exploit!  
  
We want to find someway to get the value of `p`, and we can use the equation for `q` to get this. Let us see how:  
![picture](Pictures/2.gif)  
In the above equation, `k` is the multiplier. Now, if we multiply the above equation with `q` on both sides, we will have:  
![picture](Pictures/3.gif)  
We know that n = p*q, hence the simplification above.  
  
Great, now we have a simple quadratic equation, to get the value of `q`, knowing the value of `e` and `n`. Although, we don't know the value of `k`, we can brute-force the value of `k`. To solve the above quadratic equation:  
![picture](Pictures/4.gif)  
So as per the above formula, there are two possible values of `q`; but we can remove the negative sign since `q` is very large and cannot be less than one. This gives us:  
![picture](Pictures/5.gif)  
  
To get the value of `q`, iterate check for every value of `k`, if ![picture](Pictures/6.gif) is a perfect square. If it does, then we have got the value of `q`! I implemented this using the following script:  
```python
for k in range(1, 1000000):
        # Checking for perfect equare
	if gmpy2.iroot(1+4*e*n*k, 2)[1] == True:
                # Calculating q
		q = (1 + int(gmpy2.iroot(1+4*e*n*k, 2)[0]))/(2*e)
		if n % q == 0:
			factor = q
			print k
			break
```
This gave me the value of `q` as: 117776309990537864360810812340917258096636219871129327152749744175094693075913995854147376703562090249517854407162616412941789644355136574651545193852293544566513866746012759544621873312628262933928953504305148673201262843795559879423287920215664535429854303448257904097546288383796049755601625835244054479553  
  
Now that we have `q`, we can calculate `p` and hence the private key to get the flag:  
```python
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import gmpy2

key = RSA.importKey(open("publickey.pem").read())
n = key.n
e = key.e
print n
print e

for k in range(1, 1000000):
	if gmpy2.iroot(1+4*e*n*k, 2)[1] == True:
		q = (1 + int(gmpy2.iroot(1+4*e*n*k, 2)[0]))/(2*e)
		if n % q == 0:
			factor = q
			print k
			print "q: ", q
			break
ct = open("flag.encrypted").read()
ct = bytes_to_long(ct)
p = n/factor
phin = (p-1)*(q-1)
d = inverse(e, phin)
print long_to_bytes(pow(ct, d, n))
```
  
Ran the above script and got the flag as: **TWCTF{9c10a83c122a9adfe6586f498655016d3267f195}** !
  
You can check out the exploit script here- [exploit.py](exploit.py)  


### File: Crypto-CTF-Writeups/2018/VolgaCTF-Quals/Nonsense/README.md

# Nonsense
  
**Challenge Points**: 200  
**Challenge Description**: We've intercepted several consecutive signatures. Take everything you need and find the secret key. Send it to us in hex.  
  
We are given [task.py](task.py) as the script used to sign data.  
Following are the public parameters: `g`, `y`, `p`, `q`, `a`, `b`, `m`, `message`
  
Following is the code for signing data:  
![picture1](Pictures/Picture1.png)  
Particularly, the above function has a vulnerability: `k` is being generated using LCG when it is supposed to be generated using a secure algorithm. This is how two values of `k` are being used to sign different messages:  
![picture2](Pictures/Picture2.png)  
And the LCG:  
![picture3](Pictures/Picture3.png)  
  
## The Exploit
Since we have signatures of two messages whose nonces (ie. `k`) are generated using LCG, we can write:  
![picture4](Pictures/Picture4.png)  
![picture5](Pictures/Picture5.png)  
We know from LCG that  
![picture6](Pictures/Picture6.png)  
Note that values of `m` and `q` are the same, we can then write s2 as:  
![picture7](Pictures/Picture7.gif)  
Multiplying both sides by their respective `k`, we have:  
![picture8](Pictures/Picture8.gif)  
![picture9](Pictures/Picture9.gif)  
Multiplying the above equation with s1, we have:  
![picture10](Pictures/Picture10.gif)  
Arranging the terms we get `x` as:  
![picture11](Pictures/Picture11.gif)  
  
I wrote the following script [exploit.py](exploit.py) to implement the above exploit:  
```python
import hashlib
from Crypto.Util.number import *

# Signature function body variables
g = 88125476599184486094790650278890368754888757655708027167453919435240304366395317529470831972495061725782138055221217302201589783769854366885231779596493602609634987052252863192229681106120745605931395095346012008056087730365567429009621913663891364224332141824100071928803984724198563312854816667719924760795
y = 18433140630820275907539488836516835408779542939919052226997023049612786224410259583219376467254099629677919271852380455772458762645735404211432242965871926570632297310903219184400775850110990886397212284518923292433738871549404880989194321082225561448101852260505727288411231941413212099434438610673556403084
p = 89884656743115795425395461605176038709311877189759878663122975144592708970495081723016152663257074178905267744494172937616748015651504839967430700901664125135185879852143653824715409554960402343311756382635207838848036159350785779959423221882215217326708017212309285537596191495074550701770862125817284985959
q = 1118817215266473099401489299835945027713635248219

# LCG parameters
a = 3437776292996777467976657547577967657547
b = 828669865469592426262363475477574643634
m = 1118817215266473099401489299835945027713635248219

assert m == q

msg1 = "VolgaCTF{nKpV/dmkBeQ0n9Mz0g9eGQ==}"
h1 = int(hashlib.md5(msg1).hexdigest(), 16)
msg2 = "VolgaCTF{KtetaQ4YT8PhTL3O4vsfDg==}"
h2 = int(hashlib.md5(msg2).hexdigest(), 16)

r1 = 1030409245884476193717141088285092765299686864672
r2 = 403903893160663712713225718481237860747338118174

s1 = 830067187231135666416948244755306407163838542785
s2 = 803753330562964683180744246754284061126230157465

inv1 = inverse(s2*a*r1 - s1*r2, q)
x = ((s1*h2 - s1*s2*b - s2*a*h1)*inv1) % q
print hex(x)[2:].replace("L","")
```
Got the secret key (in hex) as: **9d529e2da84117fe72a1770a79cec6ece4065212**


### File: Crypto-CTF-Writeups/2018/hxp-CTF/daring/README.md

# Daring

**Challenge Points**:

**Challenge Description**: We encrypted our flag, but we lost the keys. Can you help?

This was a simple yet a very tricky challenge made by `yyyyyyy` aimed at testing your basics. In this challenge you are given a small script:

```python
#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Counter
from Crypto.PublicKey import RSA

flag = open('flag.txt', 'rb').read().strip()

key = RSA.generate(1024, e=3)
open('pubkey.txt', 'w').write(key.publickey().exportKey('PEM').decode() + '\n')
open('rsa.enc', 'wb').write(pow(int.from_bytes(flag.ljust(128, b'\0'), 'big'), key.e, key.n).to_bytes(128, 'big'))

key = SHA256.new(key.exportKey('DER')).digest()
open('aes.enc', 'wb').write(AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(flag))
```

If you analyse the script carefully, you will notice that the same flag is encrypted in two independent ways:
1. The flag is padded with `\x00` (null byte) to make the plaintext of size 128 bytes and then encrypted using the public key where `e = 3`
2. SHA256 of the private key of used for encryption using RSA is calculated, the result of which is then used as a symmetric key to encrypt the `unpadded` flag using AES in CTR mode.

Some observations:
1. We all know that `e = 3` is vulnerable to root attacks, but here in our challenge, since the flag is padded with null bytes to make it of size 128 bytes, the root attack won't work since `pt`^3 > `n` (`pt` is the padded plaintext and `n` is the RSA modulus) and hence will wrap around while calculating the ciphertext.
2. When some plaintext is encrypted in CTR mode, remember that the ciphertext size is exactly of the same size as plaintext, since CTR mode is similar to a stream cipher.

Based on the above observations, we will try to move ahead:
1. Size of ciphertext of AES encrypted flag is 43 bytes. This implies that the original size of the flag is 43 bytes.
2. From (1), we can say that:
   + plaintext = flag + '\x00'\*(128-43) = flag + '\x00'\*85
   + ciphertext ![picture](Pictures/1.gif)
   + ciphertext ![picture](Pictures/2.gif)

To get **flag<sup>3</sup> % n**, we can compute:  
  
![picture](Pictures/3.gif)

and get the value of `x` = flag<sup>3</sup> % n


Probably **flag<sup>3</sup> > n**, since flag is of 43 bytes. But we can write:
1. x = flag<sup>3</sup> % n
2. flag<sup>3</sup> = x + k*n

So, now if we add multiples of `n` to `x` and check if the resultant value is a perfect cube, we can get the flag by taking the cube root. This part of the challenge is similar to Iowe challenge from CSAW CTF Qualifiers 2018: https://ctftime.org/task/6668

I wrote the following script to solve the challenge:  
```python
#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Counter
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
import gmpy2

pubkey = RSA.importKey(open("pubkey.txt").read())
e = pubkey.e
n = pubkey.n
rsa_enc = int.from_bytes(open("rsa.enc","rb").read(), 'big')

assert GCD(2, n) == 1
# 680 * 3 = 2040
inv = pow(inverse(2, n), 2040, n)
aes_enc = open("aes.enc","rb").read()

# From here we get the size of the actual flag
assert len(aes_enc) == 43
print(int.from_bytes(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa".ljust(128,b'\0'), 'big') == int.from_bytes(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 'big') << 680)

rsa_enc = rsa_enc*inv % n
for i in range(1000):
    ans = gmpy2.iroot(rsa_enc + i*n, 3)[1]
    if ans == True:
        print("Gotit", i)
        pt = int(gmpy2.iroot(rsa_enc + i*n, 3)[0])
        print(pt.to_bytes(43, 'big'))
        break
```
Exploit script here: [exploit.py](exploit.py)



### File: Crypto-CTF-Writeups/2018/noxCTF/Decryptor/README.md

# Decryptor

**Challenge Points**: 447  
  
**Challenge Description**: I created this nice decryptor for RSA ciphertexts, you should try it out!
  

Chosen Ciphertext Attack on RSA unpadded encryption. Similar challenge writeup: https://masterpessimistaa.wordpress.com/2018/03/04/pragyan-ctf-rsas-quest/  
  
Full exploit script for this challenge:  
```python 
from pwn import *
from Crypto.Util.number import *

r = remote("chal.noxale.com","4242")
r.recvline().strip()

N = 140165355674296399459239442258630641339281917770736077969396713192714338090714726890918178888723629353043167144351074222216025145349467583141291274172356560132771690830020353668100494447956043734613525952945037667879068512918232837185005693504551982611886445611514773529698595162274883360353962852882911457919
e = 65537
c = 86445915530920147553767348020686132564453377048106098831426077547738998373682256014690928256854752252580894971618956714013602556152722531577337080534714463052378206442086672725486411296963581166836329721403101091377505869510101752378162287172126836920825099014089297075416142603776647872962582390687281063434

chosen_ct = (c * pow(2, e, N)) % N
r.sendline(hex(chosen_ct)[2:].replace("L",""))

_pt = int(r.recvline().strip(), 16)
print long_to_bytes(_pt/2)
```

Running this script gives us the flag: **noxCTF{0u7sm4r73d}**
  


### File: Crypto-CTF-Writeups/2018/noxCTF/Trinity/README.md

# Trinity

**Challenge Points**: 794  
  
**Challenge Description**: Neo, you are the chosen one. The only person who can make sense of these numbers. Do it.
  

You might want to see our approach for solving [WTF](../WTF/) before moving further in this writeup (Guessing work in this challenge is related to `WTF` challenge).  
  
In this challenge, we get three ciphertext-modulus pairs:  
```
N = 331310324212000030020214312244232222400142410423413104441140203003243002104333214202031202212403400220031202142322434104143104244241214204444443323000244130122022422310201104411044030113302323014101331214303223312402430402404413033243132101010422240133122211400434023222214231402403403200012221023341333340042343122302113410210110221233241303024431330001303404020104442443120130000334110042432010203401440404010003442001223042211442001413004
c = 310020004234033304244200421414413320341301002123030311202340222410301423440312412440240244110200112141140201224032402232131204213012303204422003300004011434102141321223311243242010014140422411342304322201241112402132203101131221223004022003120002110230023341143201404311340311134230140231412201333333142402423134333211302102413111111424430032440123340034044314223400401224111323000242234420441240411021023100222003123214343030122032301042243


N = 302240000040421410144422133334143140011011044322223144412002220243001141141114123223331331304421113021231204322233120121444434210041232214144413244434424302311222143224402302432102242132244032010020113224011121043232143221203424243134044314022212024343100042342002432331144300214212414033414120004344211330224020301223033334324244031204240122301242232011303211220044222411134403012132420311110302442344021122101224411230002203344140143044114
c = 112200203404013430330214124004404423210041321043000303233141423344144222343401042200334033203124030011440014210112103234440312134032123400444344144233020130110134042102220302002413321102022414130443041144240310121020100310104334204234412411424420321211112232031121330310333414423433343322024400121200333330432223421433344122023012440013041401423202210124024431040013414313121123433424113113414422043330422002314144111134142044333404112240344


N = 332200324410041111434222123043121331442103233332422341041340412034230003314420311333101344231212130200312041044324431141033004333110021013020140020011222012300020041342040004002220210223122111314112124333211132230332124022423141214031303144444134403024420111423244424030030003340213032121303213343020401304243330001314023030121034113334404440421242240113103203013341231330004332040302440011324004130324034323430143102401440130242321424020323
c = 10013444120141130322433204124002242224332334011124210012440241402342100410331131441303242011002101323040403311120421304422222200324402244243322422444414043342130111111330022213203030324422101133032212042042243101434342203204121042113212104212423330331134311311114143200011240002111312122234340003403312040401043021433112031334324322123304112340014030132021432101130211241134422413442312013042141212003102211300321404043012124332013240431242
```

This looks like we need to do Hastad's Broadcast Attack with e=3, you can read about it in Crypton [here](https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Hastad-Broadcast). But the moduli looked somewhat strange to me; also the attack did not work on these moduli. All the numbers only contained digits from `0` to `4`. So they can be base-5 numbers.  
  
I converted them back to base-10 (decimal) numbers, implemented the attack using p4-team's [crypto-commons](https://github.com/p4-team/crypto-commons/blob/master/crypto_commons/rsa/rsa_commons.py) library code and got the flag!  
  
```python
from crypto_commons.generic import long_to_bytes
from crypto_commons.rsa.rsa_commons import hastad_broadcast

n1 = "331310324212000030020214312244232222400142410423413104441140203003243002104333214202031202212403400220031202142322434104143104244241214204444443323000244130122022422310201104411044030113302323014101331214303223312402430402404413033243132101010422240133122211400434023222214231402403403200012221023341333340042343122302113410210110221233241303024431330001303404020104442443120130000334110042432010203401440404010003442001223042211442001413004"
c1 = "310020004234033304244200421414413320341301002123030311202340222410301423440312412440240244110200112141140201224032402232131204213012303204422003300004011434102141321223311243242010014140422411342304322201241112402132203101131221223004022003120002110230023341143201404311340311134230140231412201333333142402423134333211302102413111111424430032440123340034044314223400401224111323000242234420441240411021023100222003123214343030122032301042243"

n2 = "302240000040421410144422133334143140011011044322223144412002220243001141141114123223331331304421113021231204322233120121444434210041232214144413244434424302311222143224402302432102242132244032010020113224011121043232143221203424243134044314022212024343100042342002432331144300214212414033414120004344211330224020301223033334324244031204240122301242232011303211220044222411134403012132420311110302442344021122101224411230002203344140143044114"
c2 = "112200203404013430330214124004404423210041321043000303233141423344144222343401042200334033203124030011440014210112103234440312134032123400444344144233020130110134042102220302002413321102022414130443041144240310121020100310104334204234412411424420321211112232031121330310333414423433343322024400121200333330432223421433344122023012440013041401423202210124024431040013414313121123433424113113414422043330422002314144111134142044333404112240344"

n3 = "332200324410041111434222123043121331442103233332422341041340412034230003314420311333101344231212130200312041044324431141033004333110021013020140020011222012300020041342040004002220210223122111314112124333211132230332124022423141214031303144444134403024420111423244424030030003340213032121303213343020401304243330001314023030121034113334404440421242240113103203013341231330004332040302440011324004130324034323430143102401440130242321424020323"
c3 = "10013444120141130322433204124002242224332334011124210012440241402342100410331131441303242011002101323040403311120421304422222200324402244243322422444414043342130111111330022213203030324422101133032212042042243101434342203204121042113212104212423330331134311311114143200011240002111312122234340003403312040401043021433112031334324322123304112340014030132021432101130211241134422413442312013042141212003102211300321404043012124332013240431242"

n1 = int(n1, 5)
n2 = int(n2, 5)
n3 = int(n3, 5)
c1 = int(c1, 5)
c2 = int(c2, 5)
c3 = int(c3, 5)

print(long_to_bytes(hastad_broadcast([(c1, n1), (c2, n2), (c3, n3)])))
```
Got the flag on running the above script: **noxCTF{D4mn_y0u_h4s74d_wh47_4_b100dy_b4s74rd!}**  


### File: Crypto-CTF-Writeups/2018/noxCTF/WTF/README.md

# WTF

**Challenge Points**: 742  
  
**Challenge Description**: Um uhhhhhhhhh WTF IS THIS?! I give up. Now you try to solve this.  
  
*Disclaimer*: Guessing involved in this challenge, so proceed at your own risk
  
In this challenge we are given N, e, c like every other RSA challenge, except for the fact that the values are encoded using some weird encoding technique. Googling about it leads to nothing, here are the public key values and ciphertext  

```
N = "lObAbAbSBlZOOEBllOEbblTlOAbOlTSBATZBbOSAEZTZEAlSOggTggbTlEgBOgSllEEOEZZOSSAOlBlAgBBBBbbOOSSTOTEOllbZgElgbZSZbbSTTOEBZZSBBEEBTgESEgAAAlAOAEbTZBZZlOZSOgBAOBgOAZEZbOBZbETEOSBZSSElSSZlbBSgbTBOTBSBBSOZOAEBEBZEZASbOgZBblbblTSbBTObAElTSTOlSTlATESEEbSTBOlBlZOlAOETAZAgTBTSAEbETZOlElBEESObbTOOlgAZbbOTBOBEgAOBAbZBObBTg"
e = "lBlbSbTASTTSZTEASTTEBOOAEbEbOOOSBAgABTbZgSBAZAbBlBBEAZlBlEbSSSETAlSOlAgAOTbETAOTSZAZBSbOlOOZlZTETAOSSSlTZOElOOABSZBbZTSAZSlASTZlBBEbEbOEbSTAZAZgAgTlOTSEBEAlObEbbgZBlgOEBTBbbSZAZBBSSZBOTlTEAgBBSZETAbBgEBTATgOZBTllOOSSTlSSTOSSZSZAgSZATgbSOEOTgTTOAABSZEZBEAZBOOTTBSgSZTZbOTgZTTElSOATOAlbBZTBlOTgOSlETgTBOglgETbT"
c = "SOSBOEbgOZTZBEgZAOSTTSObbbbTOObETTbBAlOSBbABggTOBSObZBbbggggZZlbBblgEABlATBESZgASBbOZbASbAAOZSSgbAOZlEgTAlgblBTbBSTAEBgEOEbgSZgSlgBlBSZOObSlgAOSbbOOgEbllAAZgBATgEAZbBEBOAAbZTggbOEZSSBOOBZZbAAlTBgBOglTSSESOTbbSlTAZATEOZbgbgOBZBBBBTBTOSBgEZlOBTBSbgbTlZBbbOBbTSbBASBTlglSEAEgTOSOblAbEgBAbOlbOETAEZblSlEllgTTbbgb"
```

Looking at such a big value of `e`, it had to be Wiener's Attack or it's variant. But we cannot move further without decoding the values.  
  

The part below is purely guessing  

So, one of my teammates suggested looking at the distinct characters in the encoded strings. Here are the distinct characters present in the encoded strings:  
> ['A', 'b', 'E', 'g', 'l', 'O', 'S', 'B', 'T', 'Z']

10 distinct characters, 10 digits in decimal system. So, each character represents a digit. But how do we map them?  
> 'O' --> 0  
> 'l' --> 1  
> 'Z' --> 2  
> 'E' --> 3  
> 'A' --> 4  
> 'S' --> 5  
> 'b' --> 6  
> 'T' --> 7  
> 'B' --> 8  
> 'g' --> 9  

Now, there is nothing significant left in the challenge, all that is left is to implement a simple Wiener's Attack, for which I wrote a sage/python implementation and got the flag:  
```python
from sage.all import *
from Crypto.Util.number import *

def mapping(str1):
    for i in str1:
        if i not in "AbEglOSBTZ":
            print i
    str1 = str1.replace("O", '0')
    str1 = str1.replace("l", '1')
    str1 = str1.replace("Z", '2')
    str1 = str1.replace("E", '3')
    str1 = str1.replace("A", '4')
    str1 = str1.replace("S", '5')
    str1 = str1.replace("b", '6')
    str1 = str1.replace("T", '7')
    str1 = str1.replace("B", '8')
    str1 = str1.replace("g", '9')
    return str1

def wiener(e, n):
    m = 12345
    c = pow(m, e, n)
    lst = continued_fraction(Integer(e)/Integer(n))
    conv = lst.convergents()
    for i in conv:
        k = i.numerator()
        d = int(i.denominator())
        try:
            m1 = pow(c, d, n)
            if m1 == m:
                print "[*] Found d: ", d
                return d
        except:
            continue
    return -1

N = "lObAbAbSBlZOOEBllOEbblTlOAbOlTSBATZBbOSAEZTZEAlSOggTggbTlEgBOgSllEEOEZZOSSAOlBlAgBBBBbbOOSSTOTEOllbZgElgbZSZbbSTTOEBZZSBBEEBTgESEgAAAlAOAEbTZBZZlOZSOgBAOBgOAZEZbOBZbETEOSBZSSElSSZlbBSgbTBOTBSBBSOZOAEBEBZEZASbOgZBblbblTSbBTObAElTSTOlSTlATESEEbSTBOlBlZOlAOETAZAgTBTSAEbETZOlElBEESObbTOOlgAZbbOTBOBEgAOBAbZBObBTg"
e = "lBlbSbTASTTSZTEASTTEBOOAEbEbOOOSBAgABTbZgSBAZAbBlBBEAZlBlEbSSSETAlSOlAgAOTbETAOTSZAZBSbOlOOZlZTETAOSSSlTZOElOOABSZBbZTSAZSlASTZlBBEbEbOEbSTAZAZgAgTlOTSEBEAlObEbbgZBlgOEBTBbbSZAZBBSSZBOTlTEAgBBSZETAbBgEBTATgOZBTllOOSSTlSSTOSSZSZAgSZATgbSOEOTgTTOAABSZEZBEAZBOOTTBSgSZTZbOTgZTTElSOATOAlbBZTBlOTgOSlETgTBOglgETbT"
c = "SOSBOEbgOZTZBEgZAOSTTSObbbbTOObETTbBAlOSBbABggTOBSObZBbbggggZZlbBblgEABlATBESZgASBbOZbASbAAOZSSgbAOZlEgTAlgblBTbBSTAEBgEOEbgSZgSlgBlBSZOObSlgAOSbbOOgEbllAAZgBATgEAZbBEBOAAbZTggbOEZSSBOOBZZbAAlTBgBOglTSSESOTbbSlTAZATEOZbgbgOBZBBBBTBTOSBgEZlOBTBSbgbTlZBbbOBbTSbBASBTlglSEAEgTOSOblAbEgBAbOlbOETAEZblSlEllgTTbbgb"
N = int(mapping(N))
e = int(mapping(e))
c = int(mapping(c))

d = wiener(e, N)
print long_to_bytes(pow(c, d, N))
```
In case you want to learn Wiener's Attack, you can learn about it on Crypton [here](https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Wiener).  
  
Running this script gives us the flag as: **noxCTF{RSA_1337_10rd}**.


### File: Crypto-CTF-Writeups/README.md

# Crypto-CTF-Writeups
Writeups to Crypto Challenges in CTFs

