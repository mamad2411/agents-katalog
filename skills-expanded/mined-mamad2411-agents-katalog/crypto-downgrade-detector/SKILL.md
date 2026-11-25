---
name: crypto-downgrade-detector
description: "Crypto downgrade detector: harvests every weak-algorithm usage (MD5, SHA1, DES, 3DES, RC4, ECB, CBC, deprecated createCipher), modern alternatives (subtle.encrypt, bcrypt, argon2, scrypt, PBKDF2), JWT signing-config (hardcoded-secret vs asymmetric key), cert/key-generation calls, and patch/version-based crypto weakeners (ALLOW_WEAK, --harmony, legacy-crypto). LLM analyses each finding as downgradeable, deprecated, or acceptable and recommends minimum upgrade. Read-only. Audience: Senior. Trigger: /crypto-downgrade"
trigger: /crypto-downgrade
---

## What this is for

Crypto downgrades happen silently: a developer uses `crypto.createCipher('aes-256-cbc', password)` (Node deprecated), signs JWTs with a hardcoded secret instead of an asymmetric key, hashes passwords with MD5, or enables `NODE_OPTIONS=--tls-cipher-list` with weak suites. `security-smell-scanner` flags generic "use modern crypto" - no tool reads the actual algorithm constant and classifies each as downgradeable vs acceptable. This skill catalogs every crypto-relevant statement, and the LLM classifies each by downgrade-type.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/crypto-posture.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **Algorithm downgrade**: is the algorithm deprecated (MD5, SHA1, DES, 3DES, RC4, ECB mode, Node createCipher)? What is the recommended minimum (SHA-256, AES-GCM-256, ChaCha20-Poly1305)?

### Step 6

- **Modern alternative available**: does the code use `crypto.subtle.encrypt`, `bcrypt`, `argon2`, `scrypt`, `PBKDF2`? Are they configured with safe parameters (cost factor, salt length)?

### Step 7

- **JWT signing**: is a hardcoded secret used for HS256/HS384? Should it be RS256/ES256 with a key-management system? Is `jose` or `jsonwebtoken` used?

### Step 8

- **Key generation**: is RSA < 2048 bits, DSA < 2048 bits, or ECDSA with secp256r1 (acceptable) vs secp224r1 (weak)?

### Step 9

- **Config bypass**: are there `ALLOW_WEAK`, `--harmony`, `legacy-crypto`, `NODE_OPTIONS=--tls-cipher-list` toggles that re-enable deprecated algorithms?

### Step 10

- Severity scale: hardcoded-JWT-secret > MD5/SHA1 > DES/RC4 > createCipher > weak RSA key > algorithm-allowlist bypass.

### Step 11

5. Write `crypto-downgrade-report.md` to the working directory.

## Usage

```
/crypto-downgrade                              # interactive
/crypto-downgrade <dir>                        # scan project
/crypto-downgrade -help                        # show usage
```

Returns JSON with `findings[]`:
`{file, line, cryptoType, algorithm, isModern, code}` plus summary counts.
