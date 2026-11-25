<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-combustiblelemonsctf
description: CTF writeups and security challenges by CombustibleLemonsCTF.
---

# Writeups by CombustibleLemonsCTF

Source repository: `/repos/CombustibleLemonsCTF`

## Repository Index

- CTCTF-2015-writeups/README.md
- CTCTF-2015-writeups/1023megabytes/README.md
- CTCTF-2015-writeups/8675309/README.md
- CTCTF-2015-writeups/caesar-the-flag/README.md
- CTCTF-2015-writeups/capture-the-logo/README.md
- CTCTF-2015-writeups/dbftbs-djqifs/README.md
- CTCTF-2015-writeups/faulty-qr/README.md
- CTCTF-2015-writeups/hello-ctctfer/README.md
- CTCTF-2015-writeups/his-name-is-jay-mo/README.md
- CTCTF-2015-writeups/javatar/README.md
- CTCTF-2015-writeups/just-keep-going/README.md
- CTCTF-2015-writeups/kelvins-corner/README.md
- CTCTF-2015-writeups/kelvins-favorite-colors/README.md
- CTCTF-2015-writeups/keyboard/README.md
- CTCTF-2015-writeups/legend-of-twerkopter/README.md
- CTCTF-2015-writeups/lucass-note/README.md
- CTCTF-2015-writeups/patience/README.md
- CTCTF-2015-writeups/they-said-easyctf-was-easy/README.md
- CTCTF-2015-writeups/this-problem-is-3-hard-3-me/README.md
- CTCTF-2015-writeups/uninteresting-gif/README.md
- CTCTF-2015-writeups/vulnerable-server/README.md

## Writeup Content


### File: CTCTF-2015-writeups/1023megabytes/README.md

# CTCTF 2015: 1023megabytes

### Problem

**Points**: 45

**Description**: 

> My name is Michael Zhang.

**Hint**: 

None given.

### Solution

By associating Michael Zhang with the Donut Mafia, we found this [site](https://www.classy.org/fundraise?fcid=407177). The flag is in the page source.

Note: **nobody** likes recon.

Fun fact: the string in the curly brackets of the flag is the MD5 hash for `lol`.

**Flag**: `flag{9cdfb439c7876e703e307864c9167a15}`

### Other Resources

* None.



### File: CTCTF-2015-writeups/8675309/README.md

# CTCTF 2015: 8675309

### Problem

**Points**: 70

**Description**: 

> 84433 33355524 444777794466683399877775554445533844 4447777

**Hint**: 

> Numbers... phone numbers?

### Solution

Many of the digits in the numbers we were given repeat, some of them up to four times. If we separate them, we get this: 

```
8:44:33 333:555:2:4 444:7777:9:44:666:8:33:99:8:7777:555:444:55:33:8:44 444:7777
```

Perhaps this is an encoding scheme where each group of digits represents a word? Fortunately, this is where the hint about the phone numbers becomes useful. Phone keypads map characters to digits so that you can have phone numbers with words in them to make them more memorable, like `555-NOPE`, which translates to `555-6673`.

The repeated digits represent what position on that key the letter is. That is, for the `1` button, `1` would map to `A`, `11` would map to `B`, and `111` would map to `C`. If we apply this decoding algorithm to the phone numbers, we get a message: `THE FLAG ISWHOTEXTSLIKETH IS`.

**Flag**: `WHOTEXTSLIKETHIS`

### Other Resources

* None.



### File: CTCTF-2015-writeups/README.md

# CTCTF 2015 Writeups

We are the `CombustibleLemons` ([Jonathan Lee](https://github.com/jonathanlee1), [Tim Cyrus](https://github.com/tcyrus)) from [TJHSST](http://activities.tjhsst.edu/csc/).

If you are in a hurry, then here are the [flags](flags.json).

Here are writeups for [CTCTF 2015](http://ctctf.io/), a jeopardy-style computer security competition where teams obtain flags from challenges and submit them to the website for points.

`>>> Happy hacking`

| Challenge Name                                              | Points | Status    |
|-------------------------------------------------------------|--------|-----------|
| [Hello CTCTFer](hello-ctctfer)                              | 5      | Completed |
| [Caesar the Flag](caesar-the-flag)                          | 10     | Completed |
| [Kelvin's Corner](kelvins-corner)                           | 15     | Completed |
| [Dbftbs Djqifs](dbftbs-djqifs)                              | 20     | Completed |
| [His name is Jay Mo](his-name-is-jay-mo)                    | 25     | Completed |
| [They said EasyCTF was Easy](they-said-easyctf-was-easy)    | 25     | Completed |
| [Fautly QR](faulty-qr)                                      | 30     | Completed |
| [Keyboard](keyboard)                                        | 35     | Completed |
| [Patience](patience)                                        | 35     | Completed |
| [Javatar](javatar)                                          | 40     | Completed |
| [Kelvin's Favorite Colors](kelvins-favorite-colors)         | 40     | Completed |
| [1023megabytes](1023megabytes)                              | 45     | Completed |
| [Capture the Logo](capture-the-logo)                        | 45     | Completed |
| [Just Keep Going](just-keep-going)                          | 50     | Completed |
| [Legend of Twerkopter](legend-of-twerkopter)                | 50     | Completed |
| [Uninteresting gif](uninteresting-gif)                      | 60     | Completed |
| [Vulnerable Server](vulnerable-server)                      | 60     | Completed |
| [8675309](8675309)                                          | 70     | Completed |
| [This problem is 3 hard 3 me!](this-problem-is-3-hard-3-me) | 70     | Completed |
| [Lucas's Note](lucass-note)                                 | 75     | Completed |



### File: CTCTF-2015-writeups/caesar-the-flag/README.md

# CTCTF 2015: Caesar the Flag

### Problem

**Points**: 10

**Description**: 

> Csbjogvdl jt bo ftpufsjd qsphsbnnjoh mbohvbhf opufe gps jut fyusfnf njojnbmjtn. Uif mbohvbhf dpotjtut pg pomz fjhiu tjnqmf dpnnboet boe bo jotusvdujpo qpjoufs. Ju jt eftjhofe up dibmmfohf boe bnvtf qsphsbnnfst, boe xbt opu nbef up cf tvjubcmf gps qsbdujdbm vtf. Ju xbt dsfbufe jo 1993 cz Vscbo Nümmfs. Bozxbzt, uif gmbh jt tufq_ju_vq

**Hint**: 

None given.

### Solution

As the title suggests, the problem description is the ciphertext of a [cipher](http://en.wikipedia.org/wiki/Caesar_cipher) where each letter is shifted by `n` positions. For example, if `n = 1`, then "A" would become "B," "B" would become "C," and so on. Because the letters loop around, there are only 25 possibilities in the solution space, making this cipher very easy to crack. Only one of them is likely to contain English.

Using [this tool](http://rumkin.com/tools/cipher/caesar.php), we got the flag when `n = 25`.

**Flag**: `step_it_up`

### Other Resources

* None.



### File: CTCTF-2015-writeups/capture-the-logo/README.md

# CTCTF 2015: Capture the Logo

### Problem

**Points**: 45

**Description**: 

![](logo.jpg)

**Hint**: 

> Hint

### Solution

This JPG file can be scanned for additional hidden files by using the [`binwalk`](http://binwalk.org/) utility.

```
[!] binwalk logo.jpg

DECIMAL     HEX         DESCRIPTION
-------------------------------------------------------------------------------------------------------
12          0xC         TIFF image data, big-endian
205         0xCD        LZMA compressed data, properties: 0x04, dictionary size: 16777216 bytes, uncompressed size: 805371904 bytes
5351        0x14E7      LZMA compressed data, properties: 0x0C, dictionary size: 33554432 bytes, uncompressed size: 61503 bytes
88772       0x15AC4     Zip archive data, at least v2.0 to extract, compressed size: 6699, uncompressed size: 7418, name: "steg1.png"  
95587       0x17563     End of Zip archive 

```

That ZIP file looks interesting. We opened the file up in the [`Bless`](http://home.gna.org/bless/) hex editor, selected the range between `0x15AC4` and `0x17562` bytes, inclusive, and copied the selected data into a new file.

![](bless.png)

Extracting this ZIP file gave us one PNG file named `steg1.png`, which contains the flag.

![](steg1.png)

**Flag**: `that_stego_wasnt_too_difficult_was_it`

### Other Resources

* None.



### File: CTCTF-2015-writeups/dbftbs-djqifs/README.md

# CTCTF 2015: Dbftbs Djqifs

### Problem

**Points**: 20

**Description**: 

> Kyv wcrx zj trgklivu_kyv_wcrx

**Hint**: 

> Step it up

### Solution

The hint is the same as the flag from last time. Therefore, the cipher used to encode the flag is probably the Caesar cipher (again). [Decoding](http://rumkin.com/tools/cipher/caesar.php) this ciphertext when `n = 9` gives the message `The flag is captured_the_flag`.

Alternatively, instead of solving the challenge the boring way, you might have noticed that `Kyv wcrx zj` looks a lot like `The flag is`. Making the necessary substitutions, you would have gotten `The flag is *a*t**e*_the_flag`. Then, you could have searched `/usr/share/dict/words` with grep: 

```
[!] sudo grep --ignore-case "^.a.t..e.$" /usr/share/dict/words
Castries
Martinez
bantered
baptized
baptizes
bartered
battened
battered
cactuses
cantered
captives
captured

[ . . . additional output redacted . . . ]
```

**Flag**: `captured_the_flag`

Fun fact: the problem title is "Caesar Cipher" with `n = 25`.

### Other Resources

* None.



### File: CTCTF-2015-writeups/faulty-qr/README.md

# CTCTF 2015: Faulty QR

### Problem

**Points**: 30

**Description**: 

![](QRCode.png)

**Hint**: 

> What do you know about QR codes?

### Solution

QR codes are two-dimensional matrices that hold information much like barcodes do. The edges of this QR code have been cropped off, making it impossible for a device to scan it. Our own human brains, however, can extrapolate from the data on the edge of the image to detect the colors of the squares that should exist there.

Although there are probably more clever solutions, the image was small enough that we were able to reconstruct the below QR code using [GIMP](http://www.gimp.org/) and to scan it to get the flag.

![](QRFixed.png)

**Flag**: `QRsAreTooEasyToFix`

### Other Resources

* [ISO/IEC 18004](https://www.iso.org/obp/ui/#iso:std:iso-iec:18004:ed-3:v1:en), the technical specifications of QR codes



### File: CTCTF-2015-writeups/hello-ctctfer/README.md

# CTCTF 2015: Hello CTCTFer

### Problem

**Points**: 5

**Description**: 

> Complete a survey for free points and feedback: Link to Survey

**Hint**: 

> It's free. No strings attached.

### Solution

Just do [this survey](https://jaymo1.typeform.com/to/qvMXQx).

**Flag**: `hello_ctctf`

### Other Resources

* None.



### File: CTCTF-2015-writeups/his-name-is-jay-mo/README.md

# CTCTF 2015: His name is Jay Mo

### Problem

**Points**: 25

**Description**: 

None given.

**Hint**: 

> unitedjaymo

### Solution

This is a recon problem of Jay Mo, one of the organizers of this competition. If we google his online handle, `unitedjaymo`, we get his personal website, GitHub, and Twitter, among other things. His website turns up nothing of interest with regard to finding the flag, but his GitHub profile turns up [two suspicious commits](https://github.com/unitedjaymo/unitedjaymo.github.io/commits?author=unitedjaymo) named "This isn't CSS" and "His name is Jay Mo."

In the commit "[His name is Jay Mo](https://github.com/unitedjaymo/unitedjaymo.github.io/commit/8a69038b9219a379519e65924f25da8033e94bb3)," which is the name of this challenge, we can see that he added a CSS comment containing the flag in the source of `index.html`.

**Flag**: `that's_my_name`

### Other Resources

* None.



### File: CTCTF-2015-writeups/javatar/README.md

# CTCTF 2015: Javatar

### Problem

**Points**: 40

**Description**: 

> C++, JavaScript, Python, Java. Long ago four languages worked together then, everything changed when annoying developers started complaining. Only the Javatar can master all four languages.
Javatar

**Hint**: 

> Check out jd-gui

### Solution

Java, unlike other languages, is very friendly towards decompilers, such as [`jd-gui`](http://jd.benow.ca/), which is mentioned in the hint. After we downloaded `jd-gui` as well as some graphics libraries needed to run it, we got [this source](Javatar.java): 

```java
import java.io.PrintStream;

public class Javatar
{
  public static void main(String[] paramArrayOfString)
  {
    String str1 = "KYLIIWIBTKEQAAAOAW";
    String str2 = "PEQVVNRSAHFJKVWTLR";
    String str3;
    int i;
    if (paramArrayOfString[0].equals("WHOISTHEJAVATAR")) {
      str3 = "";
      for (i = 0; i < str1.length(); i++) {
        if (i % 2 == 0) str3 = str3 + str1.charAt(i); else
          str3 = str3 + str2.charAt(i);
      }
      System.out.println(str3);
    }
    else
    {
      str3 = "";
      for (i = 0; i < str1.length(); i++) {
        if (i % 2 != 0) str3 = str3 + str1.charAt(i); else
          str3 = str3 + str2.charAt(i);
      }
      System.out.println(str3);
    }
  }
```

A complete understanding of the program is not even necessary to solve this challenge. We got the flag by running the code in the `if` block by passing in `WHOISTHEJAVATAR` as the first additional argument.

```
[!] mv Javatar.class JavatarOriginal.class
[!] javac Javatar.java
[!] java Javatar WHOISTHEJAVATAR
KELVINISTHEJAVATAR
```

Note: We had to store the original `Javatar.class` in `JavatarOriginal.class` and to recompile the program because of conflicting Java versions.

**Flag**: `KELVINISTHEJAVATAR`

### Other Resources

* None.



### File: CTCTF-2015-writeups/just-keep-going/README.md

# CTCTF 2015: Just Keep Going

### Problem

**Points**: 50

**Description**: 

> Just keep going…  
> persevere.txt  
> Rot13->b64->repeat, should be automated for good results.

**Hint**: 

> nope

### Solution

The problem description tells us exactly how to reverse the contents of the file. [`This file`](persevere.txt) contains the output of `base64`, which makes binary data safe to export as ASCII text, and `rot13`, which is just the Caesar cipher with `n = 13`. However, instead of automation, we just copied and pasted a long chain of commands and pipes and then adjusted it until we got the flag.

```
[!] cat persevere.txt | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d | rot13 | base64 -d
```

**Flag**: `isnt_automation_great`

### Other Resources

* None.



### File: CTCTF-2015-writeups/kelvins-corner/README.md

# CTCTF 2015: Kelvin's Corner

### Problem

**Points**: 15

**Description**: 

> Kelvin just created his personal website. See if there's anything suspicious!  
> Kelvin's Website

**Hint**: 

> Try viewing the page source

### Solution

The hint explicitly says to look at the [page](http://ctctf.io/problem_data/Kelvin/website.html)'s source, which is the raw HTML that specifies how the page should be formatted. In Chrome, we can view the [page source](website.html) using <kbd>CTRL</kbd>+<kbd>U</kbd> (or <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>J</kbd>, which opens up the developer console).

The flag is in the comment, which is marked with `<!--` and `-->`, after the image element.

**Flag**: `don't_take_food`

### Other Resources

* [HTML Tutorial](http://www.w3schools.com/html/)



### File: CTCTF-2015-writeups/kelvins-favorite-colors/README.md

# CTCTF 2015: Kelvin's Favorite Colors

### Problem

**Points**: 40

**Description**: 

> Frogs are known to have excellent eyesight. Being a designer, Kelvin the Frog also has excellent taste for colors. Here's a list of his favorite colors.

**Hint**: 

> What does the # do?

### Solution

Ordinarily, the `#` would signal that the following characters were part of a hexadecimal RGB color code. Each color in the code, red, green, and blue, would be assigned an integer value from `0` to `255`, or `0` to `FF` in hexadecimal. For example, the first color, `#466c61`, has a red value of `70`, a green value of `108`, and a blue value of `97`.

However, in this case, the hexadecimal values in the text file also represent an ASCII string. Using Python, you can merge the hexadecimal strings as one and decode it as ASCII.

```python
[!] python3
Python 3.3.2+ (default, Feb 28 2014, 00:52:16) 
[GCC 4.8.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> hexed = ''
>>> with open('colors.txt', 'r') as f:
...     for line in f:
...             hexed += line.strip()[1:]
... 
>>> hexed
'466c61673a2020746861745f7761735f657a'
>>> import binascii
>>> binascii.unhexlify(hexed.encode('utf-8'))
b'Flag:  that_was_ez'
```

**Flag**: `that_was_ez`

### Other Resources

* None.



### File: CTCTF-2015-writeups/keyboard/README.md

# CTCTF 2015: Keyboard

### Problem

**Points**: 35

**Description**: 

> ZY DHPUKYEHAURP, A JBSJKZKBKZYY DZURQH ZJ A TQKRYF YW QYDYFZYE SP MRZDR BYZKJ YW UVAZYKQOK AHQ HQUVADQF MZKR DZURQHKQOK, ADDYHFZYE KY A HQEBVAH JPJKQT; KRQ "BYZKJ" TAP SQ JZYEVQ VQKKQHJ (KRQ TYJK DYTTYY), UAZHJ YW VQKKQHJ, KHZUVQKJ YW VQKKQHJ, TZOKBHQJ YW KRQ ASYNQ, AYF JY WYHKR. WYH KRQ WVAE, ZK'J CQQUZKDVQAY

**Hint**: 

> Keyboard... substitution?

### Solution

This is essentially a substitution cipher challenge. To make things easier, we used [quipquip](http://quipqiup.com/), which analyzes which English words could possibly make up the ciphertext. The highest ranked solution for this ciphertext was: 

> IO CRYPTOGRAPHY, A SUBSTITUTIOO CIPHER IS A METHOD OF EOCODIOG BY WHICH UOITS OF PLAIOTEXT ARE REPLACED WITH CIPHERTEXT, ACCORDIOG TO A REGULAR SYSTEM; THE 'UOITS' MAY BE SIOGLE LETTERS (THE MOST COMMOO), PAIRS OF LETTERS, TRIPLETS OF LETTERS, MIXTURES OF THE ABOVE, AOD SO FORTH. FOR THE FLAG, IT'S ~EEPITCLEAO

The last sentence, `FOR THE FLAG, IT'S ~EEPITCLEAO`, is what we are looking for. However, the most glaring error for the whole text is that the `N`s were incorrectly interpreted as `O`s. The last sentence is now `FOR THE FLAG, IT'S ~EEPITCLEAN`. We inferred that the `~` is probably a `K`, which gives us the flag.

**Flag**: `KEEPITCLEAN`

### Other Resources

* None.



### File: CTCTF-2015-writeups/legend-of-twerkopter/README.md

# CTCTF 2015: Legend of Twerkopter

### Problem

**Points**: 50

**Description**: 

> Take a look at Kelvin's newest app:  
> Twerkopter.xap

**Hint**: 

> What's a XAP file?

### Solution

XAP files are standalone files for distributing software on Windows Phones. However, they are essentially specialized ZIP files, much like DOCX and JAR files. All of these formats share the same magic numbers as the ZIP file format.

After extracting the contents of `Twerkopter.xap`, we looked through the plaintext files and stumbled across the flag in a comment on the last line of [`WMAppManifest.xml`](Twerkopter/WMAppManifest.xml).

**Flag**: `XAP_for_XNA`

### Other Resources

* None.



### File: CTCTF-2015-writeups/lucass-note/README.md

# CTCTF 2015: Lucas's Note

### Problem

**Points**: 75

**Description**: 

>   
> note.txt

**Hint**: 

> lucas is a pretty cool dude

### Solution

Lucas numbers are part of a recursive integer sequence where `L_n = L_{n - 1} + L_{n - 2}`; this is essentially a Fibonacci sequence with different seed values. Instead of starting with `0` and `1`, Lucas numbers start with `2` and `1`, giving us the sequence `2, 1, 3, 4, 7, 11, 18, 29, . . . `.

What does this have to do with the flag and the file of text that we got? Well, suppose that you combined the characters whose indices were Lucas numbers. We wrote [this program](lucas.py) to do that.

**Flag**: `LUCASNUMBERSAREPRETTYCOOL`

### Other Resources

* None.



### File: CTCTF-2015-writeups/patience/README.md

# CTCTF 2015: Patience

### Problem

**Points**: 35

**Description**: 

![](patience.gif)

**Hint**: 

> Sometimes the obvious isn't the answer

### Solution

One's first instinct would be to scan this barcode. However, this image is a GIF (Graphics Interchange Format), which means that it can handle animation. The program displaying the GIF would draw several, successive still frames to create the illusion of motion. We used [this tool](http://ezgif.com/split) to separate this GIF into its frames. At the very end is the 100th frame, which contains the flag: 

![](frame_099.gif)

**Flag**: `not_the_barcode`

### Other Resources

* None.



### File: CTCTF-2015-writeups/they-said-easyctf-was-easy/README.md

# CTCTF 2015: They said EasyCTF was Easy

### Problem

**Points**: 25

**Description**: 

![](easysteg.jpg)

**Hint**: 

> Hint

### Solution

As in any forensics challenge, we ran this image through the `strings` command, which grabs the printable fragments of the file and writes them to standard output. Most of the output is part of the image and irrelevant, but, hidden at the very end, is the flag.

```
[!] strings easysteg.jpg 
Exif
Adobe Photoshop CS6 (Windows)
2015:03:01 19:37:51
Adobe_CM
Adobe
b34r
7GWgw
AQaq"
dEU6te

[ . . . output condensed . . . ]

yl}~+#
G*  a
He43
h@4 
}e7^
file.headers.are.important......flag:this_steg_was_waaay_too_easy_to_find
```

**Flag**: `this_steg_was_waaay_too_easy_to_find`

### Other Resources

* None.



### File: CTCTF-2015-writeups/this-problem-is-3-hard-3-me/README.md

# CTCTF 2015: This problem is 3 hard 3 me!

### Problem

**Points**: 70

**Description**: 

> written by Michael Zhang.  
> 27623b1c6b18181fed122b113027111f  
> flag: cbcb381b203b232233cbcb  

**Hint**: 

> It's not a hash. Don't try to brute-force crack it, because even if you get something, it'll be totally unrelated to the flag.

[Additional hints](https://gist.github.com/failedxyz/86a5f50becdf0d6de7db): 

> this translates roughly to "not a hash lol  " (notice the spaces)  
> 321a124c274c702739704c181a184c4

> Hint 2 for 3 hard: it's based on ASCII.

> base 16, base 2, base 3

### Solution

The solution was surprisingly simple.

The first two hints tell us that each byte (i.e. two hexadecimal digits) translates to a character in the original message. However, the encoding scheme is not ASCII: 

```python
[!] python3
Python 3.3.2+ (default, Feb 28 2014, 00:52:16) 
[GCC 4.8.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import binascii
>>> binascii.unhexlify(b'cbcb381b203b232233cbcb')
b'\xcb\xcb8\x1b ;#"3\xcb\xcb'
```

The last hint was the most important. Somehow, we have to use "base 16, base 2, base 3," in that order. Well, the encoded flag is already in hexadecimal, so the "base 16" must mean that we have to convert each character into base 10. Anything in base 2 is valid in base 3, so we can convert each character now in base 10 to "base 2," and then interpret that base 2 string as "base 3."

[Here](solution.py) is the program that we wrote up to get the flag. This is the program's output: 

> Message: ĀϏţuϫlly౼TĒRńĀRy  
> Flag: ஃஃşpóţ÷öňஃஃ

Fun fact: the hexadecimal string that we got in the first hint translates to `ŇoT˽Ā˽НĀŠН˽lol˽`.

Side note: we never got points for this because the scoring system was broken the whole time. To the developers: maybe you should have used [picoCTF's CTF platform](https://github.com/picoCTF/picoCTF-Platform-1), which "has been tested extensively on Ubuntu 12.04 LTS?" Just a thought.

**Flag**: `ஃஃşpóţ÷öňஃஃ`

### Other Resources

* None.



### File: CTCTF-2015-writeups/uninteresting-gif/README.md

# CTCTF 2015: Uninteresting gif

### Problem

**Points**: 60

**Description**: 

![](uninteresting_gif.gif)

**Hint**: 

> Hint

### Solution

Seems like a plain black GIF with some random noise in it, right? Nope. At the very bottom is what appears to be a fragment of a barcode. We split the GIF into its frames using [this tool](http://ezgif.com/split), then converted the first frame into the [PPM image format](http://en.wikipedia.org/wiki/Netpbm_format), which lists its colors values in ASCII and for which I had already written [a library](imagelib.py). Then, we ran [this program](solution.py) on it, converted `tmp.ppm` into PNG, and then scanned it using [this](http://online-barcode-reader.inliteresearch.com/).

```
[!] convert -compress None frames/frame_000.gif barcode.ppm
[!] python3 solution.py 
Reading image from barcode.ppm . . . 
Image dimensions: 300 x 629 pixels
Writing image to tmp.ppm . . . 
[!] convert tmp.ppm tmp.png
```

Here was the original barcode: 

![](tmp.png)

Note: beware of mixing up which stripes were black and white, which we did initially.

**Flag**: `useless_fact_the_1st_barcode_scanned_was_for_gum`

### Other Resources

* None.



### File: CTCTF-2015-writeups/vulnerable-server/README.md

# CTCTF 2015: Vulnerable Server

### Problem

**Points**: 60

**Description**: 

> written by Michael Zhang.  
> http://vulnserver-failedxyz.c9.io/

**Hint**: 

> You might want to look up SQL injection.

### Solution

For this problem, the flag is the `admin`'s password. When we deliberately enter a wrong password, we get: 

```
Nope. SELECT * FROM users WHERE username='admin' AND password='notpassword'
```

Because there is no filtering in place, we can alter the query and the conditions to get a binary outcome to deduce the password. Here is the necessary algorithm: 

1. Loop over all of the valid characters (i.e. the alphanumeric characters as well as the underscore).
2. Given a current character of the loop, create a query that tests whether the username is `admin` and whether the password starts with the current password plus the current character.
3. Send the query to the server.
4. If the query returns a success, then add the current character to the current password, and go back to step 1 to start over the loop.
5. Otherwise, continue to the next character at step 2.
6. If there are no more characters to loop over, then you have the full password.

We wrote [this script](client.py) to automate the guessing process. 

**Flag**: `i_h0pe_u_didnt_do_this_manually_lol`

### Other Resources

* [SQL tutorial](http://www.w3schools.com/sql/)
* [An overview of SQL injection](https://docs.google.com/presentation/d/1Zj3qMvDRBEnnh9EFyEf0bUgSTc6g2o0ZxGm6QdHTE4o/edit)

