<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-acciopi
description: CTF writeups and security challenges by acciopi.
---

# Writeups by acciopi

Source repository: `/repos/acciopi`

## Repository Index

- picoCTF2022/picoCTF2022_writeup.md

## Writeup Content


### File: picoCTF2022/picoCTF2022_writeup.md

picoCTF2022
===========

picoCTF 2022 Writeup
----------------------------
This is the writeup of picoCTF 2022.   
(I'm a member of assem. https://github.com/assem2203)

______________

# [Forensics]
 ### #1 Enhance!
Download this image file and find the flag.    
flag hint : (None)
```
 score: 100
 flag : picoCTF{3nh4nc3d_56e87c96}
 solve : $ identify -verbose drawing.flag.svg
```

 ### #3 Lookey here
Attackers have hidden information in a very large mass of data in the past, maybe they are still doing it. Download thr data here.    
flag hint : Download the file and search for the flag based on the known prefix.
 ```
 score: 100
 flag : picoCTF{gr3p_15_@w3s0m3_0abe82b2}
 solve : $ strings anthem.flag.txt | grep -i "pico"
```

 ### #4 Packets Primer
Download the packet capture file and use packet analysis software to find the flag.    
flag hint : Wireshark, if you can install and use it, is probably the most beginner friendly packet analysis software a product.
```
 score: 100
 flag : picoCTF{p4ck37_5h4rk_309456e4}
 solve : [Follow] -> [TCP Stream]
```

 ### #5 Redaction gone wrong
Now you DON’T see me. This report has some critical data in it, some of which have been redacted correctly, while some were not, Can you find an important key that was not redacted properly?    
flag hint : How can you be sure of the redaction?
```
 score: 100
 flag : picoCTF{C4n_Y0u_S33_m3_fully}
 solve : Open file in web browser. Pasted note after drag file.
```

 ### #6 Sleuthkit Intro
DOwnload the disk image and use mmls on it to find the size of the Linux partition. Connect to the remote checker service to check your answer and get the flag. Note: if you are using the webshell, download and extract the disk image into /tmp not your home directory.    
flag hint : (None)
```
 score: 100
 flag : picoCTF{mm15_f7w!}
 solve : $ mmls disk.img
         $ nc saturn.picoctf.net 52279
         $ 202752
```

 ### #7 Sleuthkit Apprentice
Download this disk image and find the flag. Note : if you are using the webshell, download and extract the disk image into /tmp not your home directory.   
flag hint : (None)
```
 score: 200
 flag : picoCTF{by73_5urf3r_11b94644}
 solve : Open FTK Imager in Windows OS. [Partition 3] -> [NONAME] -> [root] -> [root] -> [my_folder] -> [flag.uni.txt]
```

 ### #9 Operation Oni
Download this disk image, find the key and log into the remote machine. Note: if you are using the webshell, download and extract this disk image into /tmp not your home directory. Remote machine : ssh –i key_file –p 57850 ctf-player@saturn.picoctf.net   
flag hint : (None)
```
 score: 300
 flag : picoCTF{k3y_5l3u7h_d6570e30}
 solve : Open FTK Imager in Windows OS. [Partition 2] -> [NONAME] -> [root] -> [root] -> [.ssh], you find private key and public key. And login ssh after extraction files.
        $ ssh -i id_ed25519 -p 57850 ctf-player@saturn.picoctf.net
        $ ls -al
        $ cat flag.txt
```

 ### #11 Operation Orchid
Download this disk image and find the flag. Note: if you are using the webshell, download and extract the disk image into /tmp not your home directory.   
flag hint : (None)
```
 score: 400
 flag : picoCTF{h4un71ng_p457_186cf0da}
 solve : Open FTK Imager in Windows OS. [Partition 3] -> [NONAME] -> [root] -> [root], you find two files. ".ash_history" is command history file and "flag.txt.enc" is encrypted file. You decryption file after read history with extraction files. 
        $ openssl aes256 -d -salt -in flag.txt.enc -out flag.txt -k unbreakablepassword1234567
        $ cat flag.txt
```

______________

