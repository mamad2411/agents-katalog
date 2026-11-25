<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gatewaydiscord
description: CTF writeups and security challenges by GatewayDiscord.
---

# Writeups by GatewayDiscord

Source repository: `/repos/GatewayDiscord`

## Repository Index

- WriteUps/README.md
- WriteUps/Affinity CTF Lite 2020/README.md
- WriteUps/Affinity CTF Lite 2020/Crypto/Shifter_Salad_solution.md
- WriteUps/Affinity CTF Lite 2020/Crypto/crypto.md
- WriteUps/Affinity CTF Lite 2020/Stego/Stego.md
- WriteUps/Affinity CTF Lite 2020/Web/Catch Me If You Can/writeup.md
- WriteUps/Affinity CTF Lite 2020/Reverse Engineering/Magic Word/Magic_Word.md
- WriteUps/Affinity CTF Lite 2020/Forensics/Lost Head/aether_writeup.md
- WriteUps/Affinity CTF Lite 2020/Forensics/Lost Head/lost_head.md

## Writeup Content


### File: WriteUps/Affinity CTF Lite 2020/README.md

<center>
<b>Gateway participated and got to 23rd place in Afffinity CTF Lite 2020 out of 690 CTF teams.</b>
<br>
<br>
</center>

![img](https://i.imgur.com/CR9Pxhu.png)




### File: WriteUps/README.md

# WriteUps
CTF write ups for CTFs Gateway's team has participated in.

Currently we have write ups on challenges we did on Affinity CTF Lite 2020




### File: WriteUps/Affinity CTF Lite 2020/Crypto/Shifter_Salad_solution.md

# Shifter Salad 
Cryptography 10 pts -> Solve by Sarastro.

This CTF is one of the easier CTFs that AFFINITY CTF has presented in its crypto session CTF panel. The name itself suggest that its a shifter and by the challenge we see that we need to find a cipher and decipher it. 
Shifter + Salad + Cipher is only meant to be a Caeasers Cipher. 

A shifter is really what the name suggests. It shifts the letters. You have a certain pattern or a shift of numbers starting from a specific point and working towards that number in an upper or lesser context. Affecting the cipher will 
get you to the plaintext. 

*AGHFXK{5ai5b1cee10z}* - cipher text. 

Since AGHFXK is not the default flag format ( AFFCTF ) we can decipher that right away.


A = A = 0 shiftes ( no changes )

F = G --> F in the alphabet is 7th and G is sixth while F is 6th. Following the previous shift and pattern we see that this one is subtracted with -1. So this would be G-1 or 7-1 = 6 or F ( In the A1Z26 alphabet cipher )

F = H --> H is 8th in the alphabet. Following the pattern from previous : 0, -1, this would be -2 and that would be -- > H-2 or 8-2 = 6 or F. 

So far so good.

C = F --> F-3 or 6-3 = 3 or C

X = T --> X-4 or 24-4 = 20  or T

You can do K for yourself.


We clearly saw the pattern. Each letter gets subtracted by -1,-2,.. as it goes when converted to the alphabetic value of itself. 

Now a problem, what to do with the numbers that are found in there, since we do not have to turn them into letters or subtitute them you can leave them be and focus on the letters.

AFFCTF{aibceez} . Now you have 2 ways to go about this,either go manually and extract each one or write a script. I will show you both ways.

![image](https://user-images.githubusercontent.com/74470185/99503638-bdb05480-297e-11eb-93fc-525488931aef.png)

### MANUALLY

A = A-6 = 1(first in the alphabet) - 6 = -5, hmm what do we do here? What would be the -1th letter. The letter -1 from A or the last letter in the alphabet Z. = Z-5 = 26-5 = 21 or U

I = I-7 = 9-7 = 2 or B

B = B-8 = 2-8 = -6 = Z-6 = 20 or T

C = C-9 = 3-9 = -6 = Z-6 = 20 or T

E = E-10 = 5-10 = -5 = Z-5 = 21 = U

E = E-11 = 5-11 = -6 = Z-6 = T

Z = Z-12 = 26-12 = 14 = N


We got UBTTUN. Some may already see it but if you do not circle back to when I said leave the numbers outside since we cannot do anything with them. Let's plock them in here

```AFFCTF{5UB5T1TUT10N}```

### SCRIPT

Using a script you will save some time but it's an equally good option.

```python
def cipher(symbol, shift): #cipher for alphabet and shift alphabet can be changed
    LETTERS = 'abcdefghijklmnopqrstuvwxyz'

    if symbol in LETTERS:
        num = LETTERS.find(symbol)
        num = num + shift
        if num >= len(LETTERS):
            num = num - len(LETTERS)
            return LETTERS[num]
        elif num < 0:
            num = num + len(LETTERS)
            return LETTERS[num]
        else:
            return LETTERS[num]
    return symbol


enc = 'aibceez' # cipher

dec = [] # stored string

cnt = -6 #count as we started from 0 with the AFFCTF
for c in enc:

    dec.append(cipher(c, cnt)) # Append to the end result with cypher. Sends the shift and symbol
    cnt -= 1

print("".join(dec))

```

#### Conclusion

This CTF is very beginner friendly and a good learning experience!



### File: WriteUps/Affinity CTF Lite 2020/Crypto/crypto.md

Crypto Challenges at Affinity CTF Lite 2020



### File: WriteUps/Affinity CTF Lite 2020/Forensics/Lost Head/aether_writeup.md

# Aether Plane Take off
Forensics 724 pts -> Solve by Sarastro.

Even though they classified it under Forensics I still think it falls under a different branch. The Aether Plane Take Off challenge is the highest ranking challenge but it's really easy if u have experience or just get lucky.

## Forensic Enumeration
Now since it is a forensics challenge we thought we would need to check the file, analyze it hard, binwalk it and others but upon doing every enumeration we could, we just found out it is a normal .wav file.

We ploncked it Sonic Visualier to check the frequency waves as well to see if there are any hidden messages but still nothing. 

We continued analyzing it to see if we could get anything from it and upon seeing the waves, running it through frequency analyzers and similar wave enumeration methods, we got that the message is PSK encrypted.

Eventually getting EssexPSK, a PSK and RTTY reciever that decodes a message, we worked our way towards the flag.

Downloading it we came across a problem. It only read through the microphone, so we made a vbcable virtual connection for my headset to act as a microphone in the program. We also had to change up the frequency a bit to match the RX return value.

![Screenshot_1](https://user-images.githubusercontent.com/74470185/99834180-77681a80-2b63-11eb-909e-af67a9c8f5c6.png)

Ran it and got the flag!



### File: WriteUps/Affinity CTF Lite 2020/Forensics/Lost Head/lost_head.md

Solution by 0xSagacity: https://0xsagacity.github.io/affinity-lost-head.html



### File: WriteUps/Affinity CTF Lite 2020/Reverse Engineering/Magic Word/Magic_Word.md

Solution By 0xsagacity, Our team member: https://0xsagacity.github.io/affinity-magic-word.html



### File: WriteUps/Affinity CTF Lite 2020/Stego/Stego.md

Stego Challenges at Affinity CTF Lite 2020



### File: WriteUps/Affinity CTF Lite 2020/Web/Catch Me If You Can/writeup.md

Full writeup here: https://medium.com/@0x0elliot/ocr-challenge-catch-me-if-you-can-affinity-ctf-lite-2020-28cb9329690a

