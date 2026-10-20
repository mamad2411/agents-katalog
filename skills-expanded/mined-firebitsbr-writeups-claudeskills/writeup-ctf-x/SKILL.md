<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ctf-x
description: CTF writeups and security challenges by ctf-x.
---

# Writeups by ctf-x

Source repository: `/repos/ctf-x`

## Repository Index

- ctfx-problems-2016/README.md
- ctfx-problems-2016/web/north_korea-50/deploy/README.md
- ctfx-problems-2016/web/harambehub-100/deploy/README.md
- ctfx-problems-2016/crypto/blocky-200/README.md
- ctfx-problems-2016/crypto/little_crypto_gambler-150/README.md
- ctfx-problems-2016/crypto/little_crypto_gambler-150/deploy/README.md
- ctfx-problems-2016/crypto/customauth-100/deploy/README.md
- ctfx-problems-2016/binary/dat_boinary-250/deploy/README.md

## Writeup Content


### File: ctfx-problems-2016/README.md

# CTF(x) 2016
Splash site: https://ctf-x.github.io

CTF(X) problem statements, files, and writeups


CTFTime link: https://ctftime.org/event/348



### File: ctfx-problems-2016/binary/dat_boinary-250/deploy/README.md

# Deploy Instructions
* cd into directory
* `docker build -t ctfx/datboi .`
* `docker run -p <host port>:1337 -d ctfx/datboi`



### File: ctfx-problems-2016/crypto/blocky-200/README.md

# Blocky Writeup

We are provided with [blocky.py](https://github.com/bobacadodl/ctfx-problems/blob/master/crypto/blocky-200/blocky.py) and the encrypted flag.


Upon examination of the code, this is a block cipher with a block size of 5. 

We know that flag starts with 'ctf(', so we can generate 256 possibilities for the Initialization Vector.

We then reverse the encryption algorithm in z3, and try decrypting the 2nd block with all the IV possibilties. 
Only 1 results in a seemingly legitimate ascii printable decryption, so we know the correct IV
Then simply decrypt each block with that initialization vector

See [blocky_sol.py](https://github.com/bobacadodl/ctfx-problems/blob/master/crypto/blocky-200/blocky_sol.py) for code



### File: ctfx-problems-2016/crypto/customauth-100/deploy/README.md

# Deploy Instructions
* cd into directory
* `docker build -t ctfx/customauth .`
* `docker run -p <host port>:3000 -d ctfx/customauth`



### File: ctfx-problems-2016/crypto/little_crypto_gambler-150/README.md

# Little Crypto Gambler Writeup

The pseudorandom numbers are generated using a Linear Congruential Generator, with the parameters m,a,c,s being randomly generated.

There are several fast ways to crack them based on only a few outputs. One way to do this can be found here: http://security.stackexchange.com/a/4306


Bet 1 ~7 times and calculate the LCG parameters, then calculate the next number and bet everything.

[Solution code](https://github.com/bobacadodl/ctfx-problems/blob/master/crypto/little_crypto_gambler-150/gamble_solution.py)



### File: ctfx-problems-2016/crypto/little_crypto_gambler-150/deploy/README.md

# Deploy Instructions
* cd into directory
* `docker build -t ctfx/lcg .`
* `docker run -p <host port>:3001 -d ctfx/lcg`



### File: ctfx-problems-2016/web/harambehub-100/deploy/README.md

# Deploy Instructions
* cd into directory
* `docker build -t ctfx/harambehub .`
* `docker run -p <host port>:8080 -d ctfx/harambehub`



### File: ctfx-problems-2016/web/north_korea-50/deploy/README.md

# Deploy Instructions
* cd into directory
* `docker build -t ctfx/northkorea` .`
* `docker run -p <host port>:3000 -d ctfx/northkorea`

