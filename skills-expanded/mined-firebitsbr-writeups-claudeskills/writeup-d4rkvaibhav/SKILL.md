<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-d4rkvaibhav
description: CTF writeups and security challenges by d4rkvaibhav.
---

# Writeups by d4rkvaibhav

Source repository: `/repos/d4rkvaibhav`

## Repository Index

- IceCTF-2018/README.md
- picoCTF-2018-Writeups/README.md
- picoCTF-2018-Writeups/WEB_EXPLOITATION/A SIMPLE QUESTION/README.md
- picoCTF-2018-Writeups/WEB_EXPLOITATION/BUTTONS/README.md
- picoCTF-2018-Writeups/WEB_EXPLOITATION/Flaskcards Skeleton Key/README.md
- picoCTF-2018-Writeups/WEB_EXPLOITATION/IRISH NAME REPO/README.md
- picoCTF-2018-Writeups/WEB_EXPLOITATION/LOGON/READMe.md
- picoCTF-2018-Writeups/WEB_EXPLOITATION/flaskcards/readme.md
- picoCTF-2018-Writeups/Cryptography/RSAmadlibs/Readme.md
- picoCTF-2018-Writeups/Cryptography/SAFERSA/README.md
- picoCTF-2018-Writeups/Cryptography/Super Safe RSA 2/README.md
- picoCTF-2018-Writeups/Cryptography/Super safe RSA/README.md
- picoCTF-2018-Writeups/Cryptography/blaise/README.md
- picoCTF-2018-Writeups/Cryptography/ceasercipher2/README.md
- picoCTF-2018-Writeups/Cryptography/hertz/README.md
- picoCTF-2018-Writeups/Cryptography/Super Safe RSA 2/rsa-wiener-attack-master/README.md
- IceCTF-2018/Cryptography/README.md
- IceCTF-2018/Miscellaneous/README.md
- IceCTF-2018/Reverse/README.md
- IceCTF-2018/Binary exploit/CAVE-50pts/README.md

## Writeup Content


### File: IceCTF-2018/Binary exploit/CAVE-50pts/README.md

Name of the Question : CAVE 50pts
CATEGORY :BINARY EXPLOITATION

DESCRIPTION (as per the Icectf webste):
You stumbled upon a cave! I've heard some caves hold secrets.. can you find the secrets hidden within its depths?
shout.c

"The file C was also given to US.""

Write up:

(This machine which was given to us was running LINUX Distro)
In the given code we can see that there is a function(void shell()) which is being never called.
This give us the idea that it is clearly concept of "Returned oriented programming (ROP)" we have to fill the buffer follewed by the address of the function (void shell()).
In the function it is seen that a new teriminal shell will be opened when it is called which will have the permission to open  "flag.txt"

so in the gdb using command `info functions`  we find the address of the function shell which was "0x0804850b"
but we have to write it in "Little Endian" because of the current architecture used.

So basically we have to make a segmentation fault and do buffer overflow.We had a chr[16] but we needed a strong nmber to make segfault so we choose 28.

So the final command will be like this to execute the program.

--> ./shout $(python -c `print("A"*28+"\x0b\x85\x04\x08")`)
AFTER OPENING THE FILE FLAG APPEARED : "IceCTF{i_dont_think_caveman_overflowed_buffers}"

Further implementation you can see in the Photo attached!!



### File: IceCTF-2018/Cryptography/README.md

Name of question : DUMBONE

DESCRIPTION (as per the Icectf webste):

I joined a couple of hacking channels on IRC and I started recieving these strange messages. Someone sent me this image. Can you figure out if there's anything suspicous hidden in it?
-----------------------------------------------------------------------------------------------------------------------
Write up:

In this CRYPTO question we had been given 2 things in the picture garfeld.png

First the ciphered text : "IjgJUO{P_LOUV_AIRUS_GYQUTOLTD_SKRFB_TWNKCFT}"

and a key on the top right of the photo

KEY="07271978"

In the python file i have given the code.
In the code it is basically moving backward the current alphabet with the respective number given in the key.

Note: It is only for the alphabets not for the symbols

For example :
	Ijg will be deciphered as below:
	
	'I' : 'I'-0='I'
	'j' : 'j'-7='c'
	'g' : 'g'-2='e'
	

After running the python file the flag appeared :"IceCTF{I_DONT_THINK_GRONSFELD_LIKED_MONDAYS}" 



### File: IceCTF-2018/Miscellaneous/README.md

<b>ANTICAPTCHA</b> : 250 points <br>

<b>Description:</b><br>
Wow, this is a big captcha. Who has enough time to solve this? Seems like a lot of effort to me!


So in this challenge we have been given a lot of questions and by looking at the first time i thought i have to solve all the questions to get the flag and all questions were looking similar either to fing gcd of 2 number or tell the nth word or to tell number is prime or not.

This is the image of the website having questions:

(if you are not able to see image click https://drive.google.com/open?id=1cvXYFnLKrfmjdjefDrDFY7LTksUUKdoi)
<img src="https://drive.google.com/open?id=1cvXYFnLKrfmjdjefDrDFY7LTksUUKdoi" alt="img1"/>

But when i did not answer any question and submitted it, it displayed messages "You got 6 worng!" which gave me a hint that there are only 6 questions that are been evaluating so i once again saaw the questions and then i saw few questions that were completely different so to find these question i used <b>Browser automation using selenium in  python</b>.I have attached a python3 implemention of it.  <b> (File name : sel.py)</b>

(if you are not able to see image click https://drive.google.com/open?id=1np5g02xBMf0sG9t-T2vTGFhJfhyOIDK5)
<img src="https://drive.google.com/open?id=1np5g02xBMf0sG9t-T2vTGFhJfhyOIDK5" alt="img1"/>

![final](https://user-images.githubusercontent.com/43247883/45549101-30c05c80-b844-11e8-9493-b29bd7856613.png)

In the python file i am collecting all question from site 5 times and then found the intersection strings i.e. common questions  that site was generating (collected by refreshing site 5 times)

So the common questions were

[ 'How many planets are between Earth and the Sun? number', 'What year is it? number', 'Who directed the movie Jaws? word', What is the capital of Germany? word', 'What color is the sky? word', 'What is the tallest mountain on Earth? word', 'What is the capital of Hawaii? word', 'How many strings does a violin have? number']

Then i answered the above questions manually and found the flag !!!!! 


<b>IceCTF{ahh_we_have_been_captchured}</b>



### File: IceCTF-2018/README.md

# IceCTF-2018
Writeups of IceCTF 2018



### File: IceCTF-2018/Reverse/README.md

<b>Name of the Question: LOCKED OUT(250)</b><br>
<b>DESCRIPTION<br>
This is a fancy looking lock, I wonder what would happen if you broke it open?</b>
<br>
<br>
In this question we have to crack the password so first i checked the functions in the gdb.The functions were :<br><br>
0x00000590  strcmp@plt<br>
0x000005a0  printf@plt<br>
0x000005b0  strcspn@plt<br>
0x000005c0  free@plt<br>
0x000005d0  fgets@plt<br>
0x000005e0  getegid@plt<br>
0x000005f0  puts@plt<br>
0x00000600  system@plt<br>
0x00000610  strlen@plt<br>
0x00000620  __libc_start_main@plt<br>
0x00000630  __strdup@plt<br>
0x00000640  memfrob@plt<br>
0x00000650  setresgid@plt<br>
0x00000660  __cxa_finalize@plt<br>
0x00000668  __gmon_start__@plt<br>
0x00000670  main

<br>
I noticed that strcmp is used in program so i first searched in the strings of the file but
there was nothing that validates the key.That means it is dynamically generating string and comparing it.
<br>
Then instead of using gdb i used <b>ltrace</b> and saw that in strcmp my string is compared to "aXat9r45UtyMjw4i5Wh8swVWmEg3vAbW" 
<br>

![image](https://user-images.githubusercontent.com/43247883/45688976-6466f380-bb70-11e8-9c02-be785c8ad780.png)

<br>
so first i thought that i have found the password !! but when i entered it in executable file it says key failed!!!!<br>
So i again used ltrace and this time i entered "aXat9r45UtyMjw4i5Wh8swVWmEg3vAbW" in key.Now this time strcmp was returning  : -90 !!
<br>

![image](https://user-images.githubusercontent.com/43247883/45688880-2bc71a00-bb70-11e8-8a97-199505fe5c15.png)


<br>
This resulted that the string is not complete password, there are more letters in it.And -90 indicates the alphabet : Z as it's ascii is 90 so that means our new string is "aXat9r45UtyMjw4i5Wh8swVWmEg3vAbWZ" and again i got some other negative integer in ltrace when i  entered new string.<br>
So i made a python script that collects the integer and add to the string and then again calls the ltrace untill strcmp return 0.<br>

![image](https://user-images.githubusercontent.com/43247883/45689070-9e37fa00-bb70-11e8-81a3-00d249c015cf.png)

<br>
<b>NOTE : YOU CAN FIND THIS PYTHON FILE IN THE SAME REPOSITORY WITH NAME "solution.py"</b><br><br>
So the final String i got was <b>"aXat9r45UtyMjw4i5Wh8swVWmEg3vAbWZaijTWP8"</b>
<br><br>
I entered the String in password and entered the shell.Then opened the flag.txt and got the flag.
<br>
<b>FLAG</b> : IceCTF{you_m3ddling_k1ds}



### File: picoCTF-2018-Writeups/Cryptography/SAFERSA/README.md

Problem Statment:

Now that you know about RSA can you help us decrypt this ciphertext? We don't have the decryption key but something about those values looks funky..


Solution :

In ciphertext file we were given :

	N: 374159235470172130988938196520880526947952521620932362050308663243595788308583992120881359365258949723819911758198013202644666489247987314025169670926273213367237020188587742716017314320191350666762541039238241984934473188656610615918474673963331992408750047451253205158436452814354564283003696666945950908549197175404580533132142111356931324330631843602412540295482841975783884766801266552337129105407869020730226041538750535628619717708838029286366761470986056335230171148734027536820544543251801093230809186222940806718221638845816521738601843083746103374974120575519418797642878012234163709518203946599836959811

	e: 3

	ciphertext (c): 2205316413931134031046440767620541984801091216351222789180582564557328762455422721368029531360076729972211412236072921577317264715424950823091382203435489460522094689149595951010342662368347987862878338851038892082799389023900415351164773 

It is Low public exponent attack.You can find the python script <a href="https://github.com/d4rkvaibhav/PICOCTF-2018/blob/master/Cryptography/SAFERSA/rsa.py">here</a>.

After running python file flag recieved :
	picoCTF{e_w4y_t00_sm411_81b6559f}



### File: picoCTF-2018-Writeups/Cryptography/Super Safe RSA 2/README.md

Proble Statement:

Wow, he made the exponent really large so the encryption MUST be safe, right?! Connect with nc 2018shell2.picoctf.com 29661.

Solution :
I got the following things :

	c: 1778673018511075140350698252891639557906407090250539057221806340768776705763113815373271713598206734943304136885307657644746166557801527614555955063613958550715606102502660768573300084767410478866161295739179626743292839204862654148472896949835346074323716667404949929701903737872090588147698250826373180618

	n: 77531969503748326589677418948315140870584015245386763633241518845356850979564402923266696704186567270006361208862086254527576010412135230279553684940635956656649728134893874567619948675304052482720430367748612708917105846534082863042823913166120865362252479206576942147071396319459112580853771742537940112457

	e: 56172436577459725698934391359139104915041430213184221292301658571726414059411889155782982024019814564512291421932489731563519296372873415080546379424619308859152360214209740169135159761234894923144971372974038021945201954600238994209605035703317119192844975463915465725406543097929017637859019950590916533609



Since e is very large we can crack this using Wiener's attack.I used this repository https://github.com/pablocelayes/rsa-wiener-attack .I made changes in tryhack.py
	
	And got d= 65537

as i got the private key i decoded the message in python3 using :
	
		hex(print(pow(d,c,n))

which resulted 

	0x7069636f4354467b77407463685f793075725f5870306e336e74245f6340723366753131795f353439353632377d	

after converting it resulted:

	picoCTF{w@tch_y0ur_Xp0n3nt$_c@r3fu11y_5495627}


### File: picoCTF-2018-Writeups/Cryptography/Super Safe RSA 2/rsa-wiener-attack-master/README.md

rsa-wiener-attack
=================

A Python implementation of the Wiener attack on RSA public-key encryption scheme.

It uses some results about continued fractions approximations to infer the private key from public key in the cases the encryption exponent is too small or too large.



### File: picoCTF-2018-Writeups/Cryptography/Super safe RSA/README.md

Peoblem Statement:

Dr. Xernon made the mistake of rolling his own crypto.. Can you find the bug and decrypt the message? Connect with nc 2018shell2.picoctf.com 3609.

Solution :
i got the following data :
	
	c: 19474669958697898483768380499982060217038494985407624948963596074034125281014421
	n: 25132405989001317956087767778734083918050854186063214627718037281542891163684097
	e: 65537

Problem Statement(425 points):

Wow, he made the exponent really large so the encryption MUST be safe, right?! Connect with nc 2018shell2.picoctf.com 29661.

Solutions:

I tried all attacks but can't get any result.So in the i used https://www.alpertron.com.ar/ECM.HTM and cracked the factor of n.

After 12 min 55 sec i got the facors :

	158 754754 453572 149934 540516 805858 365529 (39 digits) × 158309 627169 945915 479670 296299 307350 953193 (42 digits)

So we got our p and q

	p=158754754453572149934540516805858365529
	q=158309627169945915479670296299307350953193 
	t=(p-1)*(q-1)
	import gmpy2
	d = gmpy2.invert(e,t)

	# Decryption
	decimalmessage = pow(c,d,n)
	print(decimalmessage)
	hexmessage= hex(decimalmessage)
	print(hexmessage)
	print(hexmessage[2:].decode("hex"))
	print(bytes.fromhex(hexmessage).decode())

Python script <a href="https://github.com/d4rkvaibhav/PICOCTF-2018/blob/master/Cryptography/Super%20safe%20RSA/rsadecrypt.py">here </a>
The program returned the flag:

	picoCTF{us3_l@rg3r_pr1m3$_1335}




### File: picoCTF-2018-Writeups/Cryptography/blaise/README.md

Problem Statement(200 points):

My buddy Blaise told me he learned about this cool cipher invented by a guy also named Blaise! Can you figure out what it says? Connect with nc 2018shell2.picoctf.com 26039.

Tags: Vignere cipher

Solution:
On searching Blaise cipher on google it resulted that it is Vignere cipher which was created by Blaise de Vigenère.On connecting with given service i recieved an encrypted text :

	Yse lncsz bplr-izcarpnzjo dkxnroueius zf g uzlefwpnfmeznn cousex bls ltcmaqltki my Rjzn Hfetoxea Gqmexyt axtfnj 1467 fyd axpd g rptgq nivmpr jndc zt dwoynh hjewkjy cousex fwpnfmezx. Llhjcto'x dyyypm uswy ybttimpd gqahggpty fqtkw debjcar bzrjx, lnj xhizhsey bprk nydohltki my cwttosr tnj wezypr uk ehk hzrxjdpusoitl llvmlbky tn zmp cousexypxz. Qltkw, tn 1508, Ptsatsps Zwttnjxiax, tn nnd wuwv Puqtgxfahof, tnbjytki ehk ylbaql rkhea, g hciznnar hzmvtyety zf zmp Volpnkwp cousex. Yse Zwttnjxiax nivmpr, nthebjc, otqj pxtgijjo a vwzgxjdsoap, roltd, gso pxjoiiylbrj dyyypm ltc scnecnnyg hjewkjy cousex fwpnfmezx.
	Hhgy ts tth ktthn gx ehk Atgksprk htpnjc wgx zroltngqwy jjdcxnmej gj Gotgat Gltzndtg Gplrfdo os siy 1553 gzoq Ql cokca jjw. Sol. Riualn Hfetoxea Hjwlgxz. Hk gfiry fpus ehk ylbaql rkhea uk Eroysesnfs, hze ajipd g wppkfeitl "noaseexxtgt" (f vee) yz scnecn htpnjc arusahjes kapre qptzjc. Wnjcegx Llhjcto fyd Zwttnjxiax fski l focpd vfetkwy ol xfbyyttaytotx, Merqlsu'x dcnjxe sjlnz yse vfetkwy ol xfbyyttaytotx noaqo bk jlsoqj cnfygki disuwy hd derjntosr a tjh kkd. Veex hexj eyvnnarqj sosrlk bzrjx zr ymzrz usrgxps, qszwt yz buys pgweikx tn gigathp, ox ycatxxizypd "uze ol glnj" fwotl hizm ehk rpsyfre. Hjwlgxz's sjehui ehax cewztrki dtxtyg yjnuxney ltc otqj tnj vee. Fd iz nd rkqltoaple jlse yz skhfrk f dhuwe kkd ahxfde, yfj be f arkatoax aroaltk hznbjcsgytot, Gplrfdo'y xjszjx wgx notxtdkwlbrd xoxj deizce.
	Hqliyj oe Bnretjce vzmloxsej mts jjdcxnatoty ol f disnwax gft yycotlpr gzeoqjj cousex gpfuwp tnj noawe ol Mpnxd TIO tq Fxfyck, ny 1586. Lgypr, os ehk 19ys ckseuxd, ehk nyvkseius zf Hjwlgxz's inahkw hay rtsgyerogftki eo Bnretjce. Jfgij Plht ny hox moup Ehk Hzdkgcegppry qlmkseej yse sndazycihzeius my yfjitl ehgy siyyzre mld "olyoxjo tnnd isuzrzfyt itytxnmuznzn gso itxeegi yasjo a xjrrkxdibj lnj jwesjytgwj cousex kzr nnx [Volpnkwp] tntfgn mp hgi yozmtnm yz du bttn ne". pohzCZK{g1gt3w3_n1pn3wd_ax3s7_maj_901j13l1}
	Tnj Gimjyexj nivmpr mftnki l rkuftgytot kzr hjtnm jickueiusllrd dtxtyg. Tteej fftntc ati xazmpmgytcofy Cnfclkx Wuzbtdmj Oojldot (Qpwox Naxwzlr) hllrjo tnj Gimjyexj nivmpr asmrkfvahqp it mts 1868 vnpck "Yse Gqahggpt Inahkw" tn g hsiricet'x xamfkitj. Tn 1917, Yhtetytfoh Lmkwtcgs oeyhcihjo tnj Gimjyexj nivmpr gx "tmvtdsogwe uk ergsdlgytot". Ysiy wppayltoty wgx yoz ipskwgej. Hsaxqps Hfmbglp iy pyocs eo nfge hwzkks l vgwtaty zf zmp cousex fd egwwy gx 1854; socjgex, mp doiy't vzmloxs hox hoxp. Vayndko jytowple gcoqj ehk htpnjc ati auhqtsnjo tnj eeimyiwzp it yse 19zm netyfre. Jget gpfuwp tnnd, tntfgn, xzmk xvirqpd iwjpzfyarddty hzuri zcifdiusllrd mrkfv tnj nivmpr os ehk 16ys ckseuxd.
	Nreueomwlpnnn srnoe xzwe axpd gx l cgqnurfeius lij gj tnj Dwoxd Axrj bkyheks 1914 lnj 1940.
	Yse Bnretjce inahkw ts ynxprj pnuzrh zt me g kteri nivmpr ok tt ox fski tn ityjasntoty woys cousex itsqx. Ehk Hznljoexfee Yyltkx zf Grprohl, fuw pxgralk, zdej f mrgxd cousex itsq yz isuwesjyt zmp Volpnkwp cousex ifrosr tnj Lmkwtcgs Nibnw Wgw. Ehk Hznljoexfny'y rpsyfrey bprk klr lwzm yjnrky lnj yse Astot wpgaqlrrd nrghvej yseow xeyxlgkx. Ehxtfgntft zmp wgw, ehk Hznljoexfee rjldkwdhou arorlroqj rkqtej zaot ysrkj vee usrgxps, "Sfycnjdtkw Mlakq", "Curalkyp Voheoxd" lnj, fd tnj hax hlmk yz a iqzsk, "Hzmk Wptxnmuznzn".
	Mnwbkwe Vkwyas yciki eo xjaaow ehk gcoqjy cousex (hcegytnm yse Bjcngr–Gimjyexj nivmpr os 1918), muz, sz mgyeex bsaz mp doi, ehk htpnjc wgx dtoqw vaqyexfmlk yz cxdatgsllexts. Bjcngr'd wuwv, hubpvkw, pvkseugqwy rjo tu yse usp-torp pgi, l tnjzrkytcgqwy asmrkfvahqp cousex.

SO in the text there is encrypted flag :
	
	pohzCZK{g1gt3w3_n1pn3wd_ax3s7_maj_901j13l1}

As we know that the plaintext start wirh "picoCTF" On decoding online https://www.dcode.fr/vigenere-cipher using the cipher text word "picoCTF".As special characters and number are not encoded in this cipher i got the result :
	
	PICOCTFVGNRCPHRSARNBADEA

then i manually inserted the special characters and numbers and got the flag:
	
	picoCTF{v1gn3r3_c1ph3rs_ar3nt_bad_901e13a1}


### File: picoCTF-2018-Writeups/Cryptography/ceasercipher2/README.md

Problem Statement(250 points):

Can you help us decrypt this message? We believe it is a form of a caesar cipher. You can find the ciphertext in /problems/caesar-cipher-2_3_4a1aa2a4d0f79a1f8e9a29319250740a on the shell server.

Solutions:

The message given was "4-'3evh?'c)7%t#e-r,g6u#.9uv#%tg2v#7g'w6gA".I saw a pattern that if ascii value of given charater is greater than 65 we have to substract 34 to get capital letters and for less than 65 we have to add 60 to get small letters.So i wrote a small piece of code in python3 which you can see below (can also see <a href="https://github.com/d4rkvaibhav/PICOCTF-2018/blob/master/Cryptography/ceasercipher2/script.py"> here</a>) : 

	x="4-'3evh?'c)7%t#e-r,g6u#.9uv#%tg2v#7g'w6gA"
	s=''
	for i in x:
		
		if(ord(i)<=65):
			s+=chr(ord(i)+60)
		else:
			s+=chr(ord(i)-34)
	print(s)

So the decoded text was :

	picoCTF{cAesaR_CiPhErS_juST_aREnT_sEcUrE}




### File: picoCTF-2018-Writeups/Cryptography/hertz/README.md

Problem Statement(150 points):

Here's another simple cipher for you where we made a bunch of substitutions. Can you decrypt it? Connect with nc 2018shell2.picoctf.com 18581.

Solution :
 
 I was given the following ciphertext :

	-------------------------------------------------------------------------------
	wgzivhot ymvm ut jglv achi - tlqtouolougz_wusymvt_hvm_tgcbhqcm_yhaxzqgmtb
	-------------------------------------------------------------------------------
	tohomcj, sclfs qlwr flccuihz whfm avgf oym tohuvymhx, qmhvuzi h qgnc ga
	choymv gz nyuwy h fuvvgv hzx h vhpgv chj wvgttmx. h jmccgn xvmttuziignz,
	lziuvxcmx, nht tltohuzmx imzocj qmyuzx yuf gz oym fucx fgvzuzi huv. ym
	ymcx oym qgnc hcgao hzx uzogzmx:

	-uzovguqg hx hcohvm xmu.

	yhcomx, ym smmvmx xgnz oym xhvr nuzxuzi tohuvt hzx whccmx glo wghvtmcj:

	-wgfm ls, ruzwy! wgfm ls, jgl amhvalc emtluo!

	tgcmfzcj ym whfm agvnhvx hzx fglzomx oym vglzx ilzvmto. ym ahwmx hqglo
	hzx qcmttmx ivhbmcj oyvuwm oym ognmv, oym tlvvglzxuzi chzx hzx oym
	hnhruzi fglzohuzt. oymz, whowyuzi tuiyo ga tomsymz xmxhclt, ym qmzo
	ognhvxt yuf hzx fhxm vhsux wvgttmt uz oym huv, ilvicuzi uz yut oyvgho
	hzx tyhruzi yut ymhx. tomsymz xmxhclt, xutscmhtmx hzx tcmmsj, cmhzmx
	yut hvft gz oym ogs ga oym tohuvwhtm hzx cggrmx wgcxcj ho oym tyhruzi
	ilvicuzi ahwm oyho qcmttmx yuf, mdluzm uz uot cmzioy, hzx ho oym cuiyo
	lzogztlvmx yhuv, ivhuzmx hzx ylmx curm shcm ghr.

	qlwr flccuihz smmsmx hz uztohzo lzxmv oym fuvvgv hzx oymz wgbmvmx oym
	qgnc tfhvocj.

	-qhwr og qhvvhwrt! ym thux tomvzcj.

	ym hxxmx uz h svmhwymvt ogzm:

	-agv oyut, g xmhvcj qmcgbmx, ut oym imzluzm wyvutouzm: qgxj hzx tglc
	hzx qcggx hzx glzt. tcgn fltuw, scmhtm. tylo jglv mjmt, imzot. gzm
	fgfmzo. h cuoocm ovglqcm hqglo oygtm nyuom wgvsltwcmt. tucmzwm, hcc.

	ym smmvmx tuxmnhjt ls hzx ihbm h cgzi tcgn nyutocm ga whcc, oymz shltmx
	hnyucm uz vhso hoomzougz, yut mbmz nyuom ommoy icutomzuzi ymvm hzx oymvm
	nuoy igcx sguzot. wyvjtgtogfgt. ong tovgzi tyvucc nyutocmt hztnmvmx
	oyvgliy oym whcf.

	-oyhzrt, gcx wyhs, ym wvumx qvutrcj. oyho nucc xg zuwmcj. tnuowy gaa
	oym wlvvmzo, nucc jgl?

	ym trussmx gaa oym ilzvmto hzx cggrmx ivhbmcj ho yut nhowymv, ihoymvuzi
	hqglo yut cmit oym cggtm agcxt ga yut ignz. oym sclfs tyhxgnmx ahwm hzx
	tlccmz gbhc egnc vmwhccmx h svmchom, shovgz ga hvot uz oym fuxxcm himt.
	h scmhthzo tfucm qvgrm dlumocj gbmv yut cust.

As the question name tells hertz which means frequency.So we have to do frequency analysis.I decoded it with 

http://crypto.interactive-maths.com/frequency-analysis-breaking-the-code.html and make following substitution

	M H O Z T G C U Y X V L I W S N F Q J A R B D E P K 
	| | | | | | | | | | | | | | | | | | | | | | | | | | 
	e a t n s o l i h d r u g c p w m b y f k v     z

Using the above substitution gave me the flag :

congrats here is your flag - substitution_ciphers_are_solvable_hafdnboesv


	picoCTF{substitution_ciphers_are_solvable_hafdnboesv}


### File: picoCTF-2018-Writeups/README.md

# PICOCTF-2018

<b>Writeups of PICOCTF 2018</b>

Further write ups of different categories wil be added soon.

For cryptography questions  write up:  [Writeup for Crypto](/Cryptography)

For Web questions write up:  [Writeup for web](/WEB_EXPLOITATION	)



### File: picoCTF-2018-Writeups/WEB_EXPLOITATION/A SIMPLE QUESTION/README.md

Problem Statement(600 points):

There is a website running at http://2018shell2.picoctf.com:38834 (link). We need to get into any user for a flag!

Tags : python, sql operator used : "Like"

Solution:

So in this question we have to give the answer but we don't know anything.So i entered "admin" as input which returned "wrong" with a sql statement :

	SQL query: SELECT * FROM answers WHERE answer='admin'

So this gives me a lot of hint to the solution.Next time i entered :
	'Union SELECT  * FROM answers WHERE answer Like '%a%  [ Notice i type (') in starting but not in the end ]

it returned "you are so close"

so i made a python script to find all the alphabet and numbers in the answer.You can find that script <a href="https://github.com/d4rkvaibhav/PICOCTF-2018/blob/master/WEB_EXPLOITATION/A%20SIMPLE%20QUESTION/checkalpha.py">here</a>.
After running the script i got my letters and number it was :  adhinstx14

but it was not ordered so to make it ordered i made changes in my python script.I stored my answer in variable ans.
So ans="adhinstx14" and changes the sql query to 'Union SELECT  * FROM answers WHERE answer Like '"+i+"%" where i are the letters of ans.You can find code <a href="https://github.com/d4rkvaibhav/PICOCTF-2018/blob/master/WEB_EXPLOITATION/A%20SIMPLE%20QUESTION/order.py">here</a>(order.py).

The code outputted tha answer = 41andsixsixths

i submitted the code but it was Wrong!!!

Hmmm.. 
I then realised that the Like opereator does not check the capitalisation so tried  with different capitalisation and got the answer which is : 41AndSixSixths

And i was awarded with flag after entering this.

The flag was :  Your flag is: picoCTF{qu3stions_ar3_h4rd_8f84b784}




### File: picoCTF-2018-Writeups/WEB_EXPLOITATION/BUTTONS/README.md

Problem Name : BUTTONS
Problem statement (250 points):

There is a website running at http://2018shell2.picoctf.com:18342 (link). Try to see if you can push their buttons.

Hints given :

What's different about the two buttons?

Solution:

As i opened the websit a button with tag Push me was there and after pressing the button another window with opened with a hyperlink named as button2 was there but it was not a button.On clicking that i was redirected to some other page with no flag.So using the hint i saw the source code of 2nd page and tried to changed that hyperlink to a button format.

The orignal code was :

<div>
    You did it! Try the next button: <a href="button2.php">Button2</a>
</div>

and i changed it this way using code of button 1 just change the link in button1 source to button2.php: 
<form action="button2.php" method="POST">
    <input type="submit" value="PUSH ME! I am your only hope!"/>
</form> 

and after clicking the button i was awarded with flag :

Well done, your flag is: <b>picoCTF{button_button_whose_got_the_button_25a99f84}</b>






### File: picoCTF-2018-Writeups/WEB_EXPLOITATION/Flaskcards Skeleton Key/README.md

Problem Statement(600 points):

Nice! You found out they were sending the Secret_key: a7a8342f9b41fcb062b13dd1167785f8. Now, can you find a way to log in as admin? http://2018shell2.picoctf.com:53999 (link).

Tags : flask session cookie decode and encode

Solution :

This one redirects to the same website as of the previous flask question <b>Flaskcards</b> but in this they removed the vulnerability in the create card.In the question we were given a secret key.I clicked the admin button but it shows you are not admin.Then i read about the flask secret key and encountered that it is used to encode the cookie.So i checked the session coookie .It was following :

.eJwlT0tqQzEMvIvXWUiWLUu5zEO2JBoCLbyXrErvXpcyq2E-zHyXI8-4Psr9db7jVo6Hl3uR5dnR6szlHO6olgszFukkbVxTW5hxB_DNwbpOFUkKHEgEPah5AO8SqDBbnTUUe8qoqOzTBDjqhm1p1ZVBg7wpmNpoy8qtrOvM4_X1jM-9JzEkw2ivmQJEvF2sY2xGU7WpmEviX-59xfl_gsvPLzCJP70.DqM_4A.iqFjQnY8fW8svj0UMnST-5uQJm8


I decoded online using Flask session cookie decoder(https://www.kirsle.net/wizards/flask-session.cgi) and the decoded part appeared :

{
    "_fresh": true,
    "_id": "8cdf51a2bfcd6edd19afc1fec39b39462f94eaa6500d3940a59b988f3e1713305e34de06f51020b42b2e915f872196dba806e2e2ea42bc2cfe373d490a9a74ca",
    "csrf_token": "f1e8fea3cd6b80336a7469776b83b99498ad8f1a",
    "user_id": "6"
}


So for the admin i have to change the user_id.For admin the user_id should be either 0 or 1. 
I tried to change the user_id to "1" using python code(<a href="https://github.com/d4rkvaibhav/PICOCTF-2018/blob/master/WEB_EXPLOITATION/Flaskcards%20Skeleton%20Key/encode.py">click here for code</a>) and the encoded cookie was as below :

.eJwlT0sKQjEMvEvXLpKmn8TLPNImQREU3tOVeHcrMqthPsy80xa7H5d0fu4vP6XtaumceFpU1DxiWnMzFI2J4ZNkkJSWQ4qrtgpgi4NWGcIc5NiRCKpTMYe2SiDDKHlkF6zBPaM0G8rQPC_okmae4dTJioCK9jI1ndI89tiej5vf155A53CltWYwELXlatL7YjREirAaB_5yr8P3_wlMny8wej-4.DqNCDg.QMUO2oagfXVHopREu5DsIYt4c2w

I changed the value of the session cookie and then clicked again the admin tab. i was awarded with the flag :

Your flag is: <b>picoCTF{1_id_to_rule_them_all_92303c39}</b>



### File: picoCTF-2018-Writeups/WEB_EXPLOITATION/IRISH NAME REPO/README.md

Problem Statement (200 points):

There is a website running at http://2018shell2.picoctf.com:28402 (link). Do you think you can log us in? Try to see if you can login!

Tags : Sql injection

Solution: 

In this we have to log in as admin.Opening the link leads to a website having photos of people.on side menu there is admin login  option.On opening the login page we have to login with username admin but don't know the password so i tried the basic sql injection('or'1'='1) and then i was awarded with flag :

Your flag is: <b>picoCTF{con4n_r3411y_1snt_1r1sh_f58843c5}</b>


### File: picoCTF-2018-Writeups/Cryptography/RSAmadlibs/Readme.md

Problem Statement(250 points):

We ran into some weird puzzles we think may mean something, can you help me solve one? Connect with nc 2018shell2.picoctf.com 40440

Solution:

The output of the terminal when log in to the given service was :

	0x7069636f4354467b64305f755f6b6e30775f7468335f7740795f325f5253405f35643338336531307dL <type 'long'>
	Hello, Welcome to RSA Madlibs
	Keeping young children entertained, since, well, nev3r
	Tell us how to fill in the blanks, or if it's even possible to do so
	Everything, input and output, is decimal, not hex
	#### NEW MADLIB ####
	q : 93187
	p : 94603
	##### WE'RE GONNA NEED THE FOLLOWING ####

So we have to answer some questions to get the flag but in the first line i saw a hexadecimal number.i was curious to know why it is there so i converted it to string and surprisingly it was the flag:

	picoCTF{d0_u_kn0w_th3_w@y_2_RS@_5d383e10}




### File: picoCTF-2018-Writeups/WEB_EXPLOITATION/LOGON/READMe.md

Problem Statement (150 points):

Tags : cookie sniffing

I made a website so now you can log on to! I don't seem to have the admin password. See if you can't get to the flag. http://2018shell2.picoctf.com:6153

Solution :
In this we have to login as admin but we don't know tha password.

When I login with wrong creditentials a window opened with a user and it was written that you are not admin.I again went back to login and tried some sql injection but did not succeded.Then i saw the cookie , there was an admin cookie whose value was false, so using chrome extension (https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) i edit the value of admin cookie to True.

And then flag window appeared with flag : <b>picoCTF{l0g1ns_ar3nt_r34l_82e795f4}<b>




### File: picoCTF-2018-Writeups/WEB_EXPLOITATION/flaskcards/readme.md

Problem Statement (350 points):

We found this fishy website for flashcards that we think may be sending secrets. Could you take a look?

Hints given :

Are there any common vulnerabilities with the backend of the website?
Is there anywhere that filtering doesn't get applied?
The database gets reverted every 2 hours so your session might end unexpectedly. Just make another user

Solution:

We have to login as admin to get the flag.

First we have to make an id with different name than admin.
Then i login with the id we were given tabs like create cards , list cards  ,Admin . When i clicked admin it says "you are not Admin" .

The Create card creates a card with field question and answer.We have to write a question and answer.
So from the website name it could be a flask injection but the problem was where to insert the injection.First i tried {{1+1}} (the flask injection) on the url but i was not succeeded then i tried it in create card and then see the output of it in list card it was "2" . So here is the vulnerability.Then to check the config i write {{config.item()}} and in the result i was provided with a data in which flag was present.

The flag was : picoCTF{secret_keys_to_the_kingdom_e8a55760}
