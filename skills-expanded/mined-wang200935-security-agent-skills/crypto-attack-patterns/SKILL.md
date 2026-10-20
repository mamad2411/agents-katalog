---
name: crypto-attack-patterns
description: Solve CTF cryptography challenges by mapping challenge artifacts to attack
  patterns, tooling, and reusable exploit workflows across classical crypto, XOR/stream
  ciphers, block modes, hashes/MACs, RSA, ECC, lattices, PRNGs, encodings, and protocol
  mistakes.
version: 1.2.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- cryptography
- crypto-attacks
- rsa
- ecc
- lattices
- xor
- hash
- prng
related_skills:
- cryptography-fundamentals
---

# CTF Cryptography

## Purpose

Use this skill when the user wants to solve, train for, or build knowledge around **CTF cryptography challenges**. This is different from production crypto guidance: CTF crypto is about recognizing intentionally broken assumptions, deriving an attack, scripting it quickly, and recovering a flag.

The goal is to make Hermes strong at:
- recognizing challenge families from source/output/artifacts
- choosing the likely attack path fast
- writing Python/Sage/Z3 scripts to recover plaintext/key/flag
- explaining the vulnerability in a writeup-quality way
- preserving newly learned tricks back into this skill

## First Response Workflow for Any CTF Crypto Challenge

1. **Inventory artifacts**
   - source code? parameters? ciphertext? public key? oracle endpoint? samples? multiple messages?
   - exact challenge category: classical, encoding, XOR, block cipher, hash/MAC, RSA, ECC, lattice, PRNG, protocol, side-channel.
2. **Extract mathematical objects**
   - integers: `n, e, c, p, q, phi, d`
   - curves: `p, a, b, G, Q, order`
   - block data: mode, IV/nonce, tag, padding, repeated blocks
   - hashes/MACs: construction, secret-prefix/suffix, digest size, salt
   - PRNG: seed source, state size, output truncation
3. **List obvious smells**
   - small exponent, reused nonce, repeated XOR key, known plaintext, deterministic encryption, textbook RSA, missing padding, ECB, CBC bit flipping, CTR nonce reuse, bad RNG, custom hash, custom curve, small subgroup.
4. **Try low-cost checks first**
   - decode layers, factor small `n`, gcd across moduli, repeated blocks, XOR frequency, Fermat close primes, small roots, Wiener/Boneh-Durfee hints, invalid curve/singular curve, MT19937 state recovery.
5. **Script reproducibly**
   - keep all constants in one file
   - assert intermediate equations
   - print candidate plaintexts and score them
   - for oracle challenges, implement a cached, retrying oracle wrapper before the exploit loop
   - for PRNG challenges, identify exact generator, output width, truncation, and whether outputs are consecutive
6. **Produce final writeup**
   - bug → attack idea → math derivation → exploit script → flag

## Core Attack Taxonomy

### Classical and encoding
- Caesar/Vigenere/Affine/substitution/transposition
- Bacon, Morse, Polybius, rail fence
- base encodings, hex/base64/base32/ascii85, URL, JWT, PEM, ASN.1
- frequency analysis, crib dragging, known plaintext

### XOR and stream ciphers
- single-byte XOR by frequency score
- repeating-key XOR by normalized Hamming distance
- many-time pad / CTR nonce reuse via pairwise XOR and crib dragging
- LFSR / Berlekamp-Massey
- RC4 bias or key scheduling mistakes

### Block cipher modes
- ECB repeated-block detection and cut-and-paste
- CBC padding oracle
- CBC bit flipping when IV/ciphertext malleable
- CTR/GCM nonce reuse recovering keystream or breaking authentication assumptions
- weak/custom padding

### Hashes and MACs
- length extension: MD5/SHA1/SHA256 secret-prefix MAC
- weak compare/timing leaks
- hash collision puzzle, truncated digest brute force
- custom Merkle-Damgard misuse
- HMAC vs `hash(secret || msg)` confusion

### RSA
- textbook RSA no padding
- small public exponent / Hastad broadcast
- common modulus
- shared prime across moduli via gcd
- Fermat factorization for close primes
- Wiener attack for small `d`
- partial key exposure / Coppersmith small roots
- low-entropy messages / stereotyped plaintext
- parity/LSB oracle and Bleichenbacher-style padding oracle
- CRT faults leaking factor via `gcd(s^e - m, n)`
### RSA
- textbook RSA no padding
- small public exponent / Hastad broadcast
- common modulus
- shared prime across moduli via gcd
- Fermat factorization for close primes
- Wiener attack for small `d`
- partial key exposure / Coppersmith small roots
- low-entropy messages / stereotyped plaintext
- parity/LSB oracle and Bleichenbacher-style padding oracle
- CRT faults leaking factor via `gcd(s^e - m, n)`
- XOR exponent fault (d XOR random row): when n is NOT given and a "bundle" encodes a helper value (base) via subset sums, first try the direct dual-LLL base recovery documented in `references/easyfault-solved-workflow.md`: build `L1 = {u : u·vals1 = 0 mod mod1}`, LLL it, then compute `base = -(u·vals0)/(u·bias0) mod mod0`. This solved the EasyFAULT instance in seconds and avoids 2^192 search. If direct recovery does not apply, fall back to the older oracle notes in `references/rsa-fault-xor-missing-modulus.md`. ⚠️ Pitfall: single-set/CRT zero-vector counts can be tautological as discriminators; verify any candidate by reconstructing rows and completing the fault attack.
- **q = p²+1 with hidden modulus (N·s output)** : when `q = p**2 + 1` (composite, always even) and output gives N multiplied by another random prime s (hiding N), the flag can be decrypted using only p·(p²+1) as modulus — r is irrelevant if the flag is small enough (< 1536 bits). The challenge reduces to finding p³+p as a divisor of the obfuscated K = N·s. See `references/rsa-psq-plus-one-hidden-modulus.md`.\n- **N · getPrime(k) — multi-instance GCD attack**: when a challenge outputs `K = N * getPrime(k)` (N hidden behind a random k-bit factor), and the CTF platform allows re-generating instances (re-download, press Start, or the API returns new values each call), collect **two or more K values**. Since s₁ ≠ s₂ are independent primes, `gcd(K₁, K₂) = N`. This is often the INTENDED solution — the extra factor is a red herring that collapses with multiple instances. **Check the Network tab (F12)** for API endpoints returning fresh challenge outputs. Single-instance ECM/Coppersmith on K is a trap; if you're stuck after 30+ minutes, re-read the challenge page for instance regeneration hints. See `references/rsa-psq-plus-one-hidden-modulus.md`.

### ECC
- invalid curve attack
- small subgroup / missing point validation
- nonce reuse in ECDSA/Schnorr
- biased/partial nonce lattice attacks
- anomalous curves, singular curves
- Pohlig-Hellman when group order is smooth
- wrong curve parameters or reused `k`

### Lattices and algebra
- LLL/Coppersmith for small roots
- Hidden Number Problem for biased nonces
- approximate common divisor
- subset sum/knapsack low density
- **subset sum basis recovery**: when a secret (e.g. `base`) is encoded as subset sums of unknown coefficients across multiple sets sharing the same underlying rows, statistical tests (GCD of differences, convex hull vertex count, pairwise ratio analysis, magnitude bounds) are WORTHLESS — the encoded values are indistinguishable from random for any candidate. Only lattice reduction (LLL/BKZ) can recover the coefficients and the secret. SageMath or fpylll is mandatory.
  - **count_zero_st oracle**: for the RSA-fault bundle pattern (see `references/rsa-fault-xor-missing-modulus.md`), build the lattice L = L_0 ∩ L_1, embed basis vectors as (w, s, t) in Z^74, LLL, and count vectors with s=t=0. Random bases give 1-3; correct base gives ~38-42. This oracle enables iterative search for the secret base. A reusable implementation is at `scripts/bundle_oracle.py` — takes a base hex string and an output.txt path, prints the oracle score.
- LWE-style packed payloads: infer serialization/layout and source constants before launching generic CVP/LLL
- **FHE/KSK key recovery from evaluation keys**: when a TFHE-like challenge provides BSK/KSK (evaluation keys) but not the secret key, recover lvl0 from KSK j=2 samples reduced modulo 2^40 — the message term `s_i*2^40` vanishes mod 2^40, giving clean LWE with known messages. Alternatively, combine j=1 and j=2 KSK samples via `y' = b1 - b2*2^12` to eliminate the unknown `s_i` entirely, yielding LWE with noise ~2^31 mod 2^64 (ratio 2^-33). Once lvl0 is recovered, lvl1 follows trivially from KSK j=1 entries (signal 2^52 vs noise 2^19). See `references/fhe-ksk-key-recovery.md`.
  - ⚠️ **Noise amplification pitfall**: Gaussian elimination mod composite modulus (2^k) or mod a prime near q DESTROYS the signal for binary-secret LWE — the matrix inverse amplifies noise to uniform random. Real-valued least-squares with RDF only works for entries ≤40 bits. LLL/BKZ lattice reduction is REQUIRED for this problem class; Gaussian elimination and plain real-valued solves are traps.

### PRNG and randomness
- time-seeded RNG brute force
- Python `random` / MT19937 state recovery
- LCG parameter/state recovery
- modulo bias and insufficient entropy
- nonce/key generation from predictable values

### Protocol/oracle challenges
- chosen plaintext/ciphertext oracle
- padding oracle
- format oracle
- signature oracle with malleability
- JWT/JOSE alg confusion, `none`, weak HMAC secret
- TLS/certificate toy mistakes in CTF form

### FHE / TFHE challenges (key recovery & statistical bypass)
- **Statistical LWE bypass for binary secrets**: When you need to produce valid LWE ciphertexts decrypting to chosen messages WITHOUT knowing the binary secret, exploit the known dimension. Set `a = [x, x, ..., x, 0, ..., 0]` (mostly constant value `x`, ≤ max_allowed zeros). Then `<a, s> ≈ x · k/2` with error ≤ `x · (3√k/2 + excluded_zeros)`. If error << Δ/2, encryption works without key recovery. See `references/statistical-lwe-bypass-binary-secret.md`. ✓ Solved R3CTF 2026 "Encrypted Activation".
- **KSK key recovery from evaluation keys**: When KSK j=2 samples are reduced modulo 2^40, the lvl1-bit message term `s_i·2^40` vanishes, giving pure LWE for lvl0 recovery. Alternatively, combine j=1 and j=2 via `y' = b1 - b2·2^12 mod 2^64` to eliminate s_i completely (noise ~2^31, ratio 2^-33). See `references/fhe-ksk-key-recovery.md`.
- ⚠️ **Pitfall**: Gaussian elimination mod composite/power-of-2 or mod a prime near q DESTROYS binary-secret LWE signal — matrix inverse amplifies noise uniformly. Real-valued LS (RDF) only works for entries ≤40 bits. LLL/BKZ lattice reduction is REQUIRED for key recovery, but even LLL on 1245-dim lattice is too slow (>10 min). Try the statistical bypass FIRST.
- **BSK linear system**: BSK contains ~318K equations (622 rows × 512 coefficients) for 1646 unknowns (622 lvl0 + 1024 lvl1) with noise 2^12. RealField(100+) solve is slow (5 rows in 17s) and may still fail due to condition number.

## Default Tooling

Python packages commonly useful:
```bash
python3 -m pip install --user pycryptodome gmpy2 sympy z3-solver pwntools factordb-python libnum fastecdsa ecdsa primefac
```

### factordb.com — Partial Factorization Lookup

Before spending hours on ECM/lattice attacks, ALWAYS query factordb.com for the challenge modulus or derived numbers. Many CTF challenges reuse numbers that have been partially factored by other participants.

```bash
# Query factordb API
curl -s "http://factordb.com/api?query=<number>" | python3 -m json.tool
# Status: "FF" (fully factored), "CF" (composite factors known), "C" (composite, unknown)
```

factordb may have partial factorizations even for large numbers (4000+ bits). Each found prime factor q of p²+1 gives a constraint p ≡ sqrt(-1) mod q, narrowing p via CRT.

### GMP-ECM on macOS

Homebrew does NOT have gmp-ecm (the `ecm` formula is a CD compression tool). Compile from source:

```bash
# Requires: brew install gmp autoconf automake libtool
cd /tmp
# Use a GitHub mirror (Inria GitLab requires auth)
curl -L -o ecm.tar.gz "https://github.com/sethtroisi/gmp-ecm/archive/refs/heads/master.tar.gz"
tar xzf ecm.tar.gz && cd gmp-ecm-main

# Fix macOS endian issue: resume.c uses Linux-specific htole32/le32toh
cat > endian_compat.h << 'EOF'
#ifdef __APPLE__
#include <machine/endian.h>
#include <libkern/OSByteOrder.h>
#define htole32(x) OSSwapHostToLittleInt32(x)
#define htole64(x) OSSwapHostToLittleInt64(x)
#define le32toh(x) OSSwapLittleToHostInt32(x)
#define le64toh(x) OSSwapLittleToHostInt64(x)
#endif
EOF
sed -i '' '1s/^/#include "..\/endian_compat.h"\n/' resume.c

autoreconf -i
./configure --with-gmp=$(brew --prefix gmp)
make -j4
# Binary at ./ecm
```

Usage:
```bash
# Pollard p-1 (faster, works if factor-1 is smooth):
./ecm -pm1 10000000 < number.txt

# ECM (general elliptic curve):
./ecm -c 100 -one 1000000 < number.txt  # B1=1M, 100 curves
./ecm -c 50 -one 3000000 < number.txt   # B1=3M, ~40-digit factors
```
Per-curve time on 4000-bit numbers: B1=1M ~40s, B1=3M ~140s. Finding 35-digit factors needs ~20 hours; 40-digit factors need ~12 days.

### jvdsn/crypto-attacks — Coppersmith Factorization with Partial p

```bash
git clone https://github.com/jvdsn/crypto-attacks.git
# Key functions:
#   attacks/factorization/coppersmith.py  → factorize_p(N, partial_p, beta, epsilon)
#   shared/partial_integer.py            → PartialInteger.from_lsb/blocks/middle
```

**Usage for recovering p from K when partial bits known**:
```python
from attacks.factorization.coppersmith import factorize_p
from shared.partial_integer import PartialInteger

partial_p = PartialInteger.from_lsb(512, p_mod_M, M_bitlength)
result = factorize_p(K, partial_p, beta=0.13, epsilon=0.1)
if result:
    p, cofactor = result
```

**Pitfall**: The modulus must be an integral domain (prime). Using composite K directly can fail with `inverse of Mod(...) does not exist`. Workaround: use the largest partially-factored cofactor (e.g., K divided by known small factors) as the modulus. For q=p²+1 patterns, use K/(2·4001·109976715073) = ~4044 bits rather than full K.

### defund/coppersmith Library

```bash
git clone https://github.com/defund/coppersmith.git
# Usage: load('coppersmith.sage'); small_roots(f, bounds, m=1, d=None)
```

**Critical pitfall**: The library requires the base ring to be an **integral domain** (prime modulus). Using `Integers(K)` with composite K fails with `"self must be an integral domain."` For problems needing a composite modulus, build the lattice manually or use a known prime factor as the modulus.

**Bounds**: For bivariate polynomial `f(x,y) = y*(x^2+1) - K` with root (p, p·r·s): X=2^513, Y=2^3073, K=2^4096. At boundary X²Y=K, standard lattice with m=4, d=3 finds only trivial relations. Larger shift parameters (m≥6, d≥5) or BKZ with block_size≥40 may be needed.

### SageMath
- lattice/LLL/Coppersmith
- elliptic curves
- polynomial arithmetic over finite fields

### factordb.com — First-Line Factorization Resource

**Always check factordb.com FIRST** before attempting local factorization of large numbers. It is often pre-populated with partial factorizations from other CTF participants.

```bash
# Query via API (returns JSON with status and known factors)
curl -s "http://factordb.com/api?query=$NUMBER" | python3 -m json.tool
# Status: FF = fully factored, CF = composite with partial factors, C = composite, P = prime

# Submit for ECM factorization via web UI:
# http://factordb.com/index.php?query=$NUMBER → click "Factorize!"
# Quick ECM (~30s) finds factors up to ~40 digits
```

factordb is critical for CTF crypto because:
- Challenge numbers (n, c, K, etc.) are often submitted by other participants
- Even partial factorizations reveal small factors that give modular constraints
- For RSA with q=p²+1, factors of p²+1 give p mod q_i via p² ≡ -1 mod q_i

The `factordb-python` pip package provides a Python API but may not be installed; `curl` + API is more reliable.

### CTFd API — Challenge Metadata & Flag Submission

For CTFd-hosted challenges, use the API with a token (from challenge page → F12 → Network → Authorization header):

```bash
TOKEN="ctfd_xxx"
HOST="https://ctf.example.com"

# List all challenges (includes solves count, score dynamics)
curl -skL -H "Authorization: Token $TOKEN" "$HOST/api/v1/challenges"

# Get challenge details (description, hints, files, connection info, solves)
curl -skL -H "Authorization: Token $TOKEN" "$HOST/api/v1/challenges/$ID"

# Submit a flag
curl -skL -X POST -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"challenge_id":12,"submission":"AIS3{flag}"}' \
  "$HOST/api/v1/challenges/attempt"
```

**Pitfall**: Some CTFd endpoints (hints, solves, submissions) require session auth, not just token auth. The token-only endpoints are challenges list, challenge details, and flag submission.

### GMP-ECM — Quick Timing Reference

| B1 | Time/curve (4044-bit) | Finds factors up to | Expected time for one factor |
|------|------|------|------|
| 50k | ~2s | ~20 digits | Minutes |
| 250k | ~13s | ~30 digits | ~20 min (30 curves) |
| 1M | ~47s | ~35 digits | ~20 hours |
| 3M | ~140s | ~40 digits | Days |
| 11M | ~8 min | ~45 digits | Weeks |

Timings from Apple M-series (ARM64) with GMP 6.3.0. Scale linearly with number bit-length.

### GMP-ECM — macOS Compilation (Apple Silicon)

GMP-ECM is essential for finding medium-sized factors (20-50 digits) of large CTF numbers. Homebrew does NOT have a formula for it.

```bash
# 1. Ensure GMP is installed (Homebrew)
brew install gmp

# 2. Clone from GitHub mirror (Inria GitLab requires auth)
cd /tmp
curl -L -o ecm.tar.gz "https://github.com/sethtroisi/gmp-ecm/archive/refs/heads/master.tar.gz"
tar xzf ecm.tar.gz
cd gmp-ecm-main

# 3. Fix macOS endian headers — resume.c uses Linux <endian.h>
cat > ../endian_compat.h << 'EOF'
#ifndef ENDIAN_COMPAT_H
#define ENDIAN_COMPAT_H
#ifdef __APPLE__
#include <machine/endian.h>
#include <libkern/OSByteOrder.h>
#define htole16(x) OSSwapHostToLittleInt16(x)
#define htole32(x) OSSwapHostToLittleInt32(x)
#define htole64(x) OSSwapHostToLittleInt64(x)
#define le16toh(x) OSSwapLittleToHostInt16(x)
#define le32toh(x) OSSwapLittleToHostInt32(x)
#define le64toh(x) OSSwapLittleToHostInt64(x)
#endif
#endif
EOF
sed -i '' '1s/^/#include "..\/endian_compat.h"\n/' resume.c

# 4. Build
autoreconf -i
./configure --with-gmp=$(brew --prefix gmp)
make -j4
# Binary at ./ecm

# 5. Usage
echo "$NUMBER" | ./ecm -c 30 -one 250000     # 30 curves, B1=250k, stop on factor
# B1=50k (2s/curve): finds ~20-digit factors
# B1=250k (12s/curve): finds ~30-digit factors
# B1=1M (40s/curve): finds ~35-digit factors (expected ~20h for one 35-digit factor)
```

**Pitfall**: Homebrew's `ecm` formula is the "Error Code Modeler" CD tool — NOT GMP-ECM. Do not install it.

**CRITICAL workflow rule**: Never start ECM or other factorization runs expected to take more than a few minutes without explicit user consent. Many users reject multi-hour/day background computations. Always present the time estimate and ask first. "Just running it" for 5 days without asking will cause frustration.

SageMath installation on macOS (Apple Silicon):
```bash
# conda-forge (works; pip install sagemath-standard FAILS with primecountpy)
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh -o /tmp/miniforge.sh
bash /tmp/miniforge.sh -b -p ~/miniforge3
~/miniforge3/bin/conda install -y -c conda-forge sage singular
# Run with: PATH=~/miniforge3/bin:$PATH ~/miniforge3/bin/sage script.sage
# Note: SageMath startup takes ~60s. Use background processes with generous timeouts.
```

**SageMath 10.9 (Python 3.14) breaking changes:**
- `block_matrix(ring, [[A, B]], nrows=2)` → removed `nrows`/`ncols` parameters. Use nested lists: `block_matrix(ring, [[A], [B]])` for vertical, `block_matrix(ring, [[A, B]])` for horizontal stacking. Alternatively use `.stack()` and `.augment()` methods.
- `random.seed(Integer(n))` → Python 3.14 rejects SageMath Integer as seed. Use `random.seed(int(n))`.
- `float(Rational).__format__` → SageMath Rational doesn't support `:.3f` format. Cast with `float()` first.
- `BKZ(block_size=40, fp='rr')` → crashes on macOS with `"fplll: Missing precision for BKZ with floating point type mpfr"`. Use lower block_size or default params.
- `matrix.right_kernel()` → parameter changed in 10.9. Use `matrix.right_kernel()` (no arguments) or `matrix.T.kernel()`.
- The `tqdm` package: `sage -pip install tqdm` (installs to `~/.sage/local/bin`).

Useful commands/tools:
- `python3` for most exploit scripts
- `sage` for lattice/ECC algebra
- `openssl asn1parse` for cert/ASN.1/PEM
- `xxd`, `file`, `strings` for artifact inspection
- CyberChef manually for quick encoding hypotheses

## Practical Solving Checklist

- [ ] Preserve raw artifacts exactly; do not accidentally alter bytes via Unicode handling.
- [ ] Convert between bytes/int carefully: `long_to_bytes`, `bytes_to_long`, endianness.
- [ ] Try decoding/format detection before heavy math.
- [ ] For RSA, always inspect `n` bit length, `e`, gcd with known moduli, close primes, small `c`, and padding absence.
- [ ] For RSA with `q = p**2 + 1` (composite, always even): decrypt using only p·(p²+1) as modulus — r is irrelevant if flag < 1536 bits. Find p²+1 factors via factordb; each factor q_i gives p ≡ sqrt(-1) mod q_i. Accumulate constraints; use Coppersmith when enough bits are known.\n- [ ] **N·getPrime(k) — multi-instance check FIRST**: If output is `N * getPrime(k)` (N hidden behind a random k-bit factor), re-download or re-generate the challenge before attempting ECM/Coppersmith. `gcd(K₁, K₂) = N` when s₁ ≠ s₂. Check the F12 Network tab for API calls returning fresh outputs. Single-instance attacks are a trap for this pattern. **Pitfall**: some CTF platforms use per-user fixed instances — all re-downloads return the same K. In that case, multi-instance GCD won't work. Move to single-instance attacks.\n- [ ] **Search persistently before giving up**: When stuck on a hard challenge, use TinyFish/web_search, check CTFtime, HackMD, GitHub, CryptoHack, and the challenge author's blog for writeups. Exhaust ALL search angles before concluding the problem is unsolvable. The user expects aggressive online research, not premature surrender.\n- [ ] For RSA where n is hidden (output gives n·s) and only ONE instance is available: K/c ≠ s (N/c varies, c is random in [0,N-1]). K/c ≈ 2s on average. Instead factor K via factordb to recover p through constraints.\n- [ ] **m mod small factors**: If p²+1 has known small prime factors q₁, q₂, ..., compute c mod qᵢ = m^e mod qᵢ, solve for m mod qᵢ (by discrete log or brute force if qᵢ is small), then CRT constraints on m. With enough factors (product > m), recover m directly without finding p. This is an alternative to the p-recovery path.
- [ ] For XOR/stream, check repeated nonce/key and crib-drag with expected flag format.
- [ ] For block modes, identify mode, IV, nonce, tag, block size, repeated blocks, and oracle behavior.
- [ ] For hash/MAC, identify whether it is HMAC or naive secret-prefix/suffix.
- [ ] For ECC signatures, inspect repeated `r` or biased `k`.
- [ ] For PRNG, identify language/library and seed source.
- [ ] Turn each insight into an assertion in the script.

## Flag-Oriented Heuristics

Most CTF flags look like `flag{...}`, `ctf{...}`, `HTB{...}`, `picoCTF{...}`, etc. Use this as a crib, but do not overfit; some tasks hide compressed data, images, or nested encodings.

## Safety Boundary

This skill is for educational CTF and authorized challenge environments. Do not use it to attack real services or recover secrets from systems without permission. When an oracle endpoint is provided by a CTF challenge, rate-limit and script responsibly.

## Reference Files

- `references/attack-taxonomy.md` — detailed pattern-to-attack map
- `references/rsa-playbook.md` — RSA CTF decision tree and formulas
- `references/ecc-playbook.md` — ECC/signature CTF attacks
- `references/symmetric-hash-prng-playbook.md` — XOR, block modes, hashes, MACs, and PRNGs
- `references/lattice-playbook.md` — when to use LLL/Coppersmith/HNP
- `references/oracle-attacks-playbook.md` — CBC padding oracle, RSA parity/Bleichenbacher-style oracles, compression oracles, signature/decryption oracle discipline
- `references/rsa-fault-xor-missing-modulus.md` — RSA fault attack with XOR-ed exponent, missing n, and subset-sum-encoded helper value (EasyFAULT pattern)
- `references/easyfault-solved-workflow.md` — solved EasyFAULT workflow: direct dual-LLL base recovery, embedding/flatter kernel split, gcd recovery of hidden `n`, unimodular non-kernel bit selectors, and write-up screenshot guidance.
- `references/easyfault-techniques-tried.md` — detailed catalog of techniques tried and failed on the EasyFAULT challenge (session reference)
- `references/easyrsa-p2plus1-family.md` — RSA with q=p²+1, N·s output, and hidden modulus via extra 512-bit factor (EasyRSA 2026 pattern)
- `references/easyrsa-p2plus1-family.md` — RSA with q=p²+1, N·s output, hidden modulus via extra 512-bit factor. Attack path: factordb → CRT constraints → Coppersmith. Pitfall: ECM too slow for 4044-bit composites. (EasyRSA 2026 pattern)
- `references/number-theory-toolbox.md` — gcd/CRT/integer roots/modular equations/discrete-log triage/GF(2) algebra quick reference
- `references/reversing-packed-python-crypto.md` — packed Python/Nuitka crypto challenge triage: extract inner payloads, scan ELF constants blobs when PE-focused tools fail, mine constants, and reconstruct source-guided solvers
- `references/packed-nuitka-lwe-payload-notes.md` — session-derived notes for BDRW/EasyPAINT-style Nuitka GUI crypto with packed 32x32 LWE-like payloads, constants recovered so far, and reporting discipline when no flag is recovered yet
- `references/rsa-psq-plus-one-hidden-modulus.md` — RSA with q=p²+1 (composite, always even), hidden modulus via N·s multiplication, decryption without r when flag < 1536 bits
- `references/fhe-ksk-key-recovery.md` — TFHE/FHE CTF challenges: recovering secret keys from KSK evaluation keys via message-vanishing modulus reduction and combined-sample elimination

## Scripts

- `scripts/xor_toolkit.py` — single-byte XOR, repeating-key XOR helpers, Hamming distance, scoring
- `scripts/rsa_ctf_toolkit.py` — common RSA checks and attacks: integer roots, gcd factors, Fermat, common modulus helper
- `scripts/prng_toolkit.py` — LCG modulus/parameter recovery plus MT19937 untemper/state-clone helpers
- `scripts/oracle_skeleton.py` — cached/retrying HTTP oracle wrapper skeleton for adaptive oracle exploits
- `scripts/bundle_oracle.py` — count_zero_st oracle for RSA-fault bundle pattern (EasyFAULT-style). Takes base hex + output.txt, returns oracle score (1-3 = wrong, 38-42 = correct). Requires fpylll.

## Practical lesson: The universal LS trap for binary LWE

When attacking binary-secret LWE key-recovery, the first instinct is Gaussian
elimination or least-squares. **This always fails** for nontrivial parameters.

**Why**: matrix `A` (m×n) with entries up to q has inverse entries ≈ O(q).
Multiplying `A^{-1} * noise` amplifies each noise sample to O(q·σ)·√n.
After modular reduction, result is uniformly random — the binary signal is lost.

**Tested failure modes** (R3CTF 2026 session, n=622, q∈[2^24,2^64], σ∈[2^19,2^31]):
| Method | Speed | Result |
|--------|-------|--------|
| Mod-q Gaussian elimination | instant | noise→uniform, lvl0=0/622 correct |
| Mod-prime (~2^64) elimination | ~2s | noise→uniform, solution random |
| RealField(500) LS | >10min | times out |
| RealField(80) LS (6842×1646) | >3min | times out |
| RDF LS (scipy, mod 2^24) | 0.1s | x≈0±0.17, lvl0=0 ones, verify 0% |
| RDF LS (Sage, mod 2^40) | 0.7s | x≈0±0.05, all binary-but-wrong |
| scipy.sparse LSQR (BSK, 1866×1646) | 1.3s | lvl1=0, residual 1e20, verify 0% |
| Greedy coordinate descent | 60s | stuck at 8 bits, local minimum |
| **LLL primal (1245-dim)** | **5-10min** | **only viable approach** |

**Takeaway**: for binary LWE with parameters above toy scale, skip all
linear-algebra solvers and go straight to LLL/BKZ lattice reduction.
The intermediate approaches waste hours.  See `references/fhe-ksk-key-recovery.md`.

**Exception**: if entries are ≤40 bits AND n ≤ 100, RDF may work.  For larger
n or 64-bit entries, precision loss from condition number is fatal.

## Practical lesson: LWE-style packed payload triage

For source-guided LWE-style CTF apps, infer the serialized layout from file length before attacking the lattice. A magic like `BDRW` followed by `0x00000200` can mean an 8-byte header plus a 512-byte encrypted/ciphertext area, with the remaining bytes holding matrix/product values. Check exact decompositions such as `remaining = (DIM*DIM + DIM) * LWE_VALUE_BYTES`; for example, `17416 = 8 + 512 + (32*32 + 32)*16` strongly suggests `DIM=32` and 128-bit LWE values. Do not launch generic high-dimensional CVP/LLL before recovering constants from the app; first identify `DIM`, modulus `q`, value byte order, secret distribution, error distribution, and whether the secret is a binary canvas vector or password-derived vector.

Workflow discipline from a failed EasyPAINT attempt: if the user asks for the correct flag, do not keep reporting partial progress as if it were useful completion. Use summaries only when forced by tool/context limits; otherwise continue reversing/solving until the flag is recovered and verified. For packed Python crypto, exact source-level derivation functions (`derive_secret`, `build_matrix`, `derive_message_vector`, stream cipher) matter more than speculative linear algebra. If direct matrix inversion over likely moduli produces random-looking vectors, treat that as evidence the equation/PRNG derivation is still missing, not as a solve path.

For EasyPAINT/BDRW-style Nuitka crypto, do not stop at inferring an LWE-shaped `enc.bin` layout from file size. Parse the Nuitka DataComposer constants blob to recover source-level function metadata first. In particular, if `app.py`, `derive_secret`, `derive_message_vector`, `build_matrix`, `stream_xor_encrypt`, `PASSWORD_SHA256`, and alphabet constants appear in the constants blob but have no normal binary xrefs, reconstruct the DataComposer chunks (`name\0 + uint32_le(part_len) + uint16_le(count) + tagged constants`) and use those constants/code-object specs to derive the true equations before launching LLL/Z3/subset attacks.

When a recovered app constant includes a huge prime modulus (for example a 257-bit `Q`) but the serialized matrix and product values are all much smaller (for example 128-bit), treat that size mismatch as a first-class clue: the file may store PRNG/hash-derived limbs, use a smaller effective modulus such as `P=257`, or defer reduction to runtime. Do not assume a textbook LWE modulus just because a `Q` constant exists. First recover `DIM`, `P/Q`, byte order, secret distribution, error distribution, and whether the secret is a binary canvas vector or password-derived vector, then choose Z3/subset/lattice accordingly.

## Practical lesson: repeating-key XOR implementation

For repeating-key XOR, use normalized Hamming distance to estimate key size, transpose bytes by key position, then solve each column as single-byte XOR with English/flag scoring. In practice, guessed keys may appear as repeated multiples such as `RAVENRAVEN`; reduce to the smallest repeating period when reporting.

Portable Python pitfall: on this Mac, `python3` may be 3.9; avoid requiring `int.bit_count()` in reusable CTF solvers. Use `bin(x).count("1")` or a compatibility helper for popcount.

## Practical lessons: picoCTF-style crypto batch solves

- **Batch solver orchestration**: do not run every challenge solver in one unguarded script when one path may be expensive (e.g. RSA factoring). Provide per-challenge CLI entry points or run quick solvers first, and put long factoring attempts behind explicit arguments/timeouts so a slow RSA task does not hide fast flags from LFSR/AES/custom-cipher tasks.
- **Multi-prime close-prime RSA**: if `n` appears to be a product of more than two nearby primes, run close-factor / Fermat-style splitting until all factors are found. For RSA with factors `p_i`, compute `phi = Π(p_i - 1)`, `d = inverse(e, phi)`, then decrypt. Do not assume exactly two primes. If generic `sympy.factorint` stalls, switch to targeted Pollard Rho/Fermat/root-neighborhood scanning or external tools rather than blocking the batch.
- **LFSR-derived AES keys**: when source gives LFSR state/taps but orientation is ambiguous, brute force the small convention space before overengineering: shift direction (`left/right`), output bit (`msb/lsb`), tap index base (`0/1`), and bit packing (`MSB-first/LSB-first`). Score AES decryptions by flag prefix and printable plaintext. If no candidate appears, inspect source for output-before/after-clock, Fibonacci vs Galois update, mode/IV, and whether the feedback bit rather than state bit is emitted.
- **AES without SubBytes becomes linear**: if custom AES removes the nonlinear S-box but keeps ShiftRows/MixColumns/AddRoundKey, model it as an affine/linear transform. With one known plaintext/ciphertext pair, derive `E_K(0) = C_known XOR E_0(P_known)`, then recover another plaintext via `P = D_0(C_target XOR E_K(0))`. This is faster than attempting key recovery.

## Practical lesson: OpenJDK Preferences altBase64 / UTF-16BE encodings

When a challenge points at `java.util.prefs.FileSystemPreferences` / `Base64.byteArrayToAltBase64`, treat the ciphertext as **OpenJDK Preferences alternate Base64**, not standard Base64. The process is usually:

1. Remove the leading `_` added by `dirName()`.
2. Decode with Java's alternate alphabet:
   ```text
   !"#$%&'(),-.:;<>@[]^`_{|}~abcdefghijklmnopqrstuvwxyz0123456789+?
   ```
3. Interpret the decoded bytes as **UTF-16BE** if the source used `byteArray(String)` / `nodeName()`.
4. If direct UTF-16BE output is partly garbled but contains obvious structure, inspect for **bit misalignment** before abandoning the route. A practical probe is to shift the full decoded bitstream by 0..15 bits and rescore for printable ASCII / leetspeak / flag markers. In one solved challenge, a **10-bit right shift** realigned the stream and exposed a readable flag-like message plus a nested standard Base64 tail.
5. After realignment, look for a **second encoding layer** such as standard Base64, especially when the plaintext visibly contains `[A-Za-z0-9+/=]` runs.

Reusable heuristic: when a custom alphabet decode yields many UTF-16 words that are multiples of `0x40`, that often means the payload is structurally correct but shifted; `word >> 6` or whole-bitstream offset scans can reveal the intended text.

Additional pitfall from a solved variant: do **not** trust an apparent printable prefix after altBase64 decode. One challenge produced leading printable garbage (`plfanz...`) in the first few decoded words, while the real message appeared only after skipping several 16-bit words and applying `word >> 6` to the remainder. If the decoded stream contains a plausible flag body but the prefix looks wrong, treat the early words as framing/junk and rescore later offsets before submitting.

Source-guided triage rule from this solve: when the challenge hands you exact library symbols (`dirName()`, `byteArrayToAltBase64()`, `byteArray(nodeName)`), prefer reconstructing the **precise upstream transform** over generic decode brute force. The winning path came from reading what each Java function implied about prefixing, alphabet choice, and string-to-bytes encoding; only after that should you enumerate alignment fixes.

Verification rule from this solve: separate **recovered payload**, **candidate flag wrapper**, and **human interpretation**. In this family the decoded payload may contain readable taunts, nested Base64, or strings that look like a flag namespace. Record them as separate layers and verify each layer independently instead of collapsing them too early into a single guessed final flag.

Submission discipline for this family: if the recovered plaintext contains a nested standard-Base64-looking tail (for example `V2VsbCBkb29p`), do **not** silently normalize it into a more English-looking phrase (`Well done`) unless the challenge or an independent derivation proves that transformation is required. Preserve the **literal decoded output** as the primary candidate, then test variants systematically in this order: raw recovered text, raw text with the nested Base64 left intact, and only then a second-layer-decoded form. Apparent wrappers such as `plfanzen{...}` should also be treated as hypotheses, not facts, unless the platform or challenge explicitly states that flag format.

## Practical lesson: SageMath 10.9 `block_matrix` API change

SageMath 10.9 removed the `nrows`/`ncols` keyword arguments from `block_matrix`. Older lattice-attack code using `block_matrix(ring, [[...]], nrows=2)` must be updated to use nested list structure:

```python
# Old (broken in Sage 10.9):
block_matrix(GF(3), [[P3, -V3*P3]], nrows=2)
# New (Sage 10.9+):
block_matrix(GF(3), [[P3], [-V3*P3]])      # vertical stack
block_matrix(GF(3), [[A, B]])               # horizontal stack
block_matrix(GF(3), [[A, B], [C, D]])       # 2×2 block
```

This affects many lattice-attack implementations from papers (e.g., Coron et al. 2020 multivariate HSSP) and CTF writeups.

## Practical lesson: EasyFAULT-style small-bias non-discrimination

When a challenge uses small bias/perturbation values (e.g., 12-bit bias vs 256-bit modulus), the single-set orthogonal lattice `[I_m, h; 0, mod]` will produce identical zero-vector counts (typically 38-42 for m=72, n=32 HSSP) for ALL candidate bases — correct and incorrect. This is because the bias perturbation Δ·bias only affects the lower ~204 bits of 511-bit CRT values; LLL sees the identical top bits and finds the same structure.

**Symptom**: LLL gives 39-42 zero vectors for every candidate base. The lattice approach appears to "always work."

**Fix**: Use the intersection of TWO lattices (one per modulus) with exact-integer constraints (the s=t=0 condition in the 74-dim embedding). Only the correct base gives both lattices the same kernel structure, yielding 38-42 intersection vectors. Wrong bases give 1-3. A reusable implementation is at `scripts/bundle_oracle.py`.

**Also fails**: CRT-combining the two sets into a single modulus — same non-discrimination issue (perturbation confined to low bits).

**Two-stage search strategy** (practical for bundle-oracle based base recovery):
- **Stage 1 — LLL screening** (~0.17s/base): Run the intersection oracle with LLL instead of BKZ. Wrong bases score 0-4. Bases scoring ≥6 are candidates.
- **Stage 2 — BKZ-45 verification** (~0.39s/base): Verify top LLL candidates with full BKZ-45. Only BKZ-45 gives reliable scores (38-42 for correct, 2-3 for wrong).
- Overall speed: ~6 evals/sec (LLL) with selective BKZ verification. With 2+ parallel processes: ~12-18 evals/sec.
- Pitfall: LLL sometimes gives inflated scores (observed 10 for a wrong base); always BKZ-verify before claiming success.

**BKZ block_size speed comparison** (fpylll 0.6.4, system Python on macOS):
| Block size | Time | Stability |
|-----------|------|-----------|
| BKZ-20 | 0.22s | Unstable (0-3 for wrong bases) |
| BKZ-25 | 0.23s | Unstable (0-4) |
| BKZ-30 | 0.25s | Stable (3) |
| BKZ-40 | 0.38s | Stable (2-3) |
| BKZ-45 | 0.39s | Stable (2-3) |
Use BKZ-30+ for stable oracle scores. Lower block sizes produce inconsistent results. For the TWO-STAGE approach, use LLL for screening (BKZ not needed for wrong-base discrimination).

**Also fails — Gradient descent**: Minimizing `(w·vals0)(w·bias1) - (w·vals1)(w·bias0)` with Adam/sgd always converges to trivial solutions where w·bias0 ≈ 0 or w·bias1 ≈ 0. The zero-set is 70-dimensional and GD cannot escape to the true 40-dim ker(X^T) subspace. Adding a regularizer to maximize b²+d² doesn't help — the gradient conflict cannot be balanced.

**Also fails — Multivariate HSSP attack** (Coron et al. 2020): The standard implementation requires m ≥ n(n+3)/2 ≈ 560 samples for n=32. The EasyFAULT challenge only provides m=72. Step 1 (orthogonal lattice) runs but step 2 (GF(3) eigenspace) fails because the kernel matrix has 488+ dimensions instead of the required n=32. The `tl2cents/Implementation-of-Cryptographic-Attacks` multivariate_attack function will fail silently on undersized input.

**Also fails — Polynomial GCD / determinant approach**: For the correct base, `det_{j,k}(base) = (vals0_j+base·bias0_j)·(vals1_k+base·bias1_k) - (vals1_j+base·bias1_j)·(vals0_k+base·bias0_k)` is NOT zero modulo M. The algebraic cancellation `(X_j·c0)·(X_k·c1) - (X_j·c1)·(X_k·c0) = 0` only works BEFORE modular reduction. Since vals are already reduced modulo their respective primes, the determinant is nonzero (confirmed experimentally on synthetic data). Do NOT attempt this approach — it's a trap that looks mathematically promising but fails on modularly-reduced values.

**Also fails — Low-bit enumeration**: Testing all 2^12 values of base mod 4096 via DP subset-sum check gives ALL 4096 candidates passing — the DP is too weak to discriminate. The subset sum structure modulo 2^12 is preserved for all bases.

**Working verification — Nguyen-Stern OL Attack** (✓ discriminates correct vs wrong bases):
The full Nguyen-Stern orthogonal lattice attack (two-step: LLL on kernel → right_kernel + BKZ → solve_right) produces a definitive boolean result. For m=72, n=32 HSSP with CRT-combined modulus: correct base → True, wrong base → False. Speed: ~0.3s/check in SageMath (similar to bundle oracle). However, this is a VERIFICATION method, not a base-recovery method — it still requires the base as input.

**Nguyen-Stern vs Multivariate HSSP**: The Nguyen-Stern algorithm needs only m ≥ 2n samples (64 for n=32). The optimized multivariate attack (Coron et al. 2020) needs m ≥ n(n+3)/2 ≈ 560. For low-m challenges like EasyFAULT (m=72), only Nguyen-Stern can verify; the multivariate attack's GF(3) eigenspace step fails because ker(E) has 488+ dimensions instead of n=32. The `tl2cents` notebook explicitly notes: "In the Nguyen-Stern algorithm, we only need about m = 2n hidden subset and samples to solve, but the optimized algorithm needs at least m = n²/2."

**C·h tautology pitfall**: Checking whether C·h ≡ 0 mod M (where C is the orthogonal lattice basis) is TAUTOLOGICAL — C is built from vectors satisfying w·h ≡ 0 mod M by construction, so C·h=0 for ALL bases. Do NOT use this as a discriminator. It's equivalent to the count-of-zero-vectors test.

## Maintenance Rule

After solving any CTF crypto challenge, patch this skill with the reusable pattern if:
- the trick was not already listed
- a script needed a non-obvious fix
- a tool/library behaved differently on this machine
- the writeup revealed a better decision tree
