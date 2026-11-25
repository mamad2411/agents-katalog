<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cryptanalyse
description: CTF writeups and security challenges by Cryptanalyse.
---

# Writeups by Cryptanalyse

Source repository: `/repos/Cryptanalyse`

## Repository Index

- writeups/README.md
- writeups/2020-insomnihack-teaser/crypto-OutOfTheSbox/README.md
- writeups/2019-RITSEC/crypto-RageDelete/README.md

## Writeup Content


### File: writeups/2019-RITSEC/crypto-RageDelete/README.md

# Rage Delete - Crypto 500 - 10 solves

RITSEC 2019

### Challenge description

```
Help!!! Our Crypto guy left in a furious rage and deleted our company private key and part of our signatures! We use that key to sign all of our important documents and such. This should be enough information for you to figure it out:

Curve: NIST256P
HASH: SHA256
Generator X: 48439561293906451759052585252797914202762949526041747995844080717082404635286
Generator Y: 36134250956749795798585127919587881956611106672985015071877198253568414405109
Group Order: 115792089210356248762697446949407573529996955224135760342422259061068512044369
Point X: 62642270921362628024101430148161419180734994811675578761489832783807341294140
Point Y: 620508080568073990375228521563014425211330352832293590138091382461067773777

I was also told the following gobblygook may be helpful.

-----BEGIN PUBLIC KEY----- 
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEin5E1fIJtTJ4ICIZ4leN0kT+QguW 
zDv6xizjvWTqcjwBXzHz49NVqrXR1Be16ceYRgtW7iGx1ifF135T0E1HUQ==
-----END PUBLIC KEY-----

Also so you can see some examples of our signatures... he always was yelling something about incrementing a value.

Message 1: "We are not uncertain with the vote." 
Signature 1: (5469004757321565031662176892324365988603823594146568468219498508892601371422, 79937836276667565200355044792462693868454270095571952117096182814592269649296)

Message 2: "We are uncertain with the vote." 
Signature 2: (???, 30705201908992384075889316247635358307738190041386759684653850381547740770548)

The flag is the private key in decimal.

Author: cictrone
```

### Analysis

The challenge shows a misuse of ECDSA signature scheme, when nonces are not correctly chosen. The typical case would be a nonce reuse, however, here the description suggests that the nonce is actually a counter.

Since we have two signatures, this means that `k` is used as nonce for message `m1` and `k+1` for message `m2`. 

Also, we are only given a partial for the second signature, but we can recover it based on the counter assumption for the nonce and the public details of the curve (`NIST256p`).

### Solution

```python
import ecdsa
from gmpy2 import invert as mod_inv
import random
from hashlib import sha256

def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1
    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #
    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in xrange(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)

        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def get_y(x):
	y = (pow(x, 3) + a*x + b) % p
	y = modular_sqrt(y, p)
	assert pow(y, 2) % p == (pow(x, 3) + a*x + b) % p
	return y

C = ecdsa.NIST256p
G = C.generator
N = C.order

m1 = "We are not uncertain with the vote."
m2 = "We are uncertain with the vote."

h1 = int(sha256(m1.encode()).hexdigest(), 16)
h2 = int(sha256(m2.encode()).hexdigest(), 16)

a = C.curve.a()
b = C.curve.b()
p = C.curve.p()

#########################################
### Data from the challenge
#########################################

## Data: signature for m1
r1 = 5469004757321565031662176892324365988603823594146568468219498508892601371422
s1 = 79937836276667565200355044792462693868454270095571952117096182814592269649296

## Data: partial signature for m2
s2 = 30705201908992384075889316247635358307738190041386759684653850381547740770548

## Data: Verifying key
pubkey = open("pub.key").read()
vk = ecdsa.VerifyingKey.from_pem(pubkey)
P = vk.pubkey.point
assert pow(P.y(), 2) % p == (pow(P.x(), 3) + a*P.x() + b) % p

#########################################
### Recover the incomplete signature
#########################################

## Verify m1 and signature (r1, s1)
s1_inv = mod_inv(s1, N)
u1 = (h1*s1_inv) % N
u2 = (r1*s1_inv) % N
T1 = u1 * G + u2 * P
assert T1.x() == r1

for kG in [
	ecdsa.ellipticcurve.Point(C.curve, r1,   get_y(r1)   ),
	ecdsa.ellipticcurve.Point(C.curve, r1, (-get_y(r1))%p),
]:
	Q = kG + G # Move to second nonce
	r2 = Q.x() # Recover r2 
	## Verify m2 and signature (r2, s2)
	s2_inv = mod_inv(s2, N)
	v1 = (h2*s2_inv) % N
	v2 = (r2*s2_inv) % N
	T2 = v1 * G + v2 * P
	if T2.x() == r2:
		break

## Verify m2 and signature (r2, s2)
s2_inv = mod_inv(s2, N)
u1 = (h2*s2_inv) % N
u2 = (r2*s2_inv) % N
T2 = u1 * G + u2 * P
assert T2.x() == r2

#########################################
### Key recovery by solving the system
###	      k  * s_1 = h_1  +  s * r_1
###	   (k+1) * s_2 = h_2  +  s * r_2
#########################################

r1_inv = mod_inv(r1, N)
r2_inv = mod_inv(r2, N)
k = (h1*r1_inv - h2*r2_inv + s2*r2_inv) * mod_inv(s1*r1_inv - s2*r2_inv, N) % N
d = (s1 * k - h1) * mod_inv(r1, N) % N

#########################################
### Check correctness
#########################################

kG = k*G
r = kG.x() % N
s = mod_inv(k, N)*(h1 + d*r) % N
assert (r, s) == (r1, s1)

kG = (k+1)*G
r = kG.x() % N
s = mod_inv(k+1, N)*(h2 + d*r) % N
assert (r, s) == (r2, s2)

#########################################
### Output
#########################################

print("Nonce:       {}".format(k))
print("Signing key: {}".format(d))

# Nonce:       7800010500099000107000320001190009700011500032000104000101000114000101
# Signing key: 51385391163632633269999983613639213146659943335057127399923324554652318101330
```

Output:

```
Nonce:       7800010500099000107000320001190009700011500032000104000101000114000101
Signing key: 51385391163632633269999983613639213146659943335057127399923324554652318101330
```



### File: writeups/2020-insomnihack-teaser/crypto-OutOfTheSbox/README.md

# Ouf of the Sbox - Crypto 500 - 14 solves

Insomni'hack Teaser 2020

### Challenge description

```
Rijndael is too mainstream, so we went custom.
This should work out of the box and be unbreakable!

Authors: pwndawan & nico
```

Attached file: `out_of_the_sbox.zip`

### Offline Analysis

The Python source code attached to the challenge described a custom cipher that has the following properties (`des.py`):

* 64-bit blocks,
* 48-bit keys,
* 7-round balanced Feistel structure (two 32-bit branches),
* The F-function of the Feistel network is word-based:
	* Four key bytes are XORed to the 4-bytes input,
	* Four round-dependent Sboxes are applied to the 4 bytes,
	* The bytes are rotated by one position.

F-function:

```
(x0, x1, x2, x3) -> (S1[x1 + k1], S2[x2 + k2], S3[x3 + k3], S0[x0 + k0])
```

Cryptographically speaking, one can already pinpoints several weaknesses:

* There are only 7 rounds.
* The Sboxes chosen are linearly weak (the maximal biais is significantly high)
* There is no key schedule: the 6 bytes of the master key `k0 || k1 || k2 || k3 || k4 || k5` are used to construct the seven 32-bit subkeys:
	* `k2 || k3 || k4 || k5`
	* `k0 || k1 || k2 || k3`
	* `k4 || k5 || k0 || k1`
	* `k2 || k3 || k4 || k5`
	* `k0 || k1 || k2 || k3`
	* `k4 || k5 || k0 || k1`
	* `k2 || k3 || k4 || k5`
* There are only three difference subkeys `RK0`, `RK1` and `RK2`, which are used in a cyclic way.

### Online Analysis

Upon connection to the remote service, we are given 50,000 known plaintexts. I believe that the authors of the challenge wanted the solution to implement an attack based on linear cryptanalysis, relying on the very strong linear approximations existing in the Sboxes.

### Solution

The solution given below:

* does not implement a linear attack,
* is **independent of the choice of the Sboxes**,
* only requires **2 known plaintext/ciphertext pairs**.

The first pair is denoted `(P, C)` and will be used for the key recovery, while the second `(P', C')` is denoted and will only be used to filter out wrong key candidates by trial encryption of `P'`.

By guessing completely 32 bits of the master key (i.e., `k2 || k3 || k4 || k5`), one can partially encrypt and decrypt `P` and `C` to peel of the first and the last rounds. So we end up with a 5-round Feistel cipher where we also know partial subkey. We only have to recover the missing 16 bits of the master key.

To do this, we propagate the known information from the plaintext and the subkeys inwards, and simarly backwards from the ciphertext side. Since there are only five rounds, one can deduce a candidate value for `k0` as:

```
k0 = state[4][2] ^ invS_4_1[ state[4][5] ^ state[5][1] ]
```

where `state[r][i]` contains the `i`-th byte of the internal state after `r+1` rounds, and `invS_4_1` is the inverse of the Sbox `S[4][1]`.

We can the proceed similarly to derive a candidate for `k1`:

```
k1 = state[1][3] ^ invS_2_0[ state[0][2] ^ state[2][2] ]
```

Overall the pseudo code of the attack is:

```
For each value of (k2, k3, k4, k5)
    - Determine k0
    - Determine k1
    - If Encrypt(P', (k0, k1, k2, k3, k4, k5)) == C':
    	- Return k0, k1, k2, k3, k4, k5
```

Therefore the cost of the attack is equivalent to `2**32` encryptions, requires 2 KP, and has negligibly memory complexity.

Code of the attack is attached (`attack.c`).

#### Flag

`INS{W3ll_m4ybe_cust0m_5B0Xes_4re_no7_a_g0od_1dea!}`


### File: writeups/README.md

# Some CTF write-ups

