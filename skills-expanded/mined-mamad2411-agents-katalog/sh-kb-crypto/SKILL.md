---
name: sh-kb-crypto
description: "Knowledge base for finding cryptographic failures - weak hashing/encryption, insecure randomness, hardcoded/static keys and IVs, ECB mode, missing integrity, and predictable tokens. Use when hunting crypto misuse. CWE-327/328/330/326/916, OWASP A02:2021-Cryptographic Failures."
---

# Cryptographic Failures - Hunter Knowledge Base

Broken or misused cryptography: weak algorithms, predictable randomness, static keys/IVs, missing
integrity, or protecting nothing (plaintext). Impact depends on what the crypto was meant to protect.

## What to hunt
- **Weak/broken algorithms** (CWE-327/328): `MD5`/`SHA1` for passwords or signatures, `DES`/`3DES`/`RC4`,
  fast hashes for password storage (should be argon2/bcrypt/scrypt/PBKDF2).
- **Insecure randomness** (CWE-330/338): `Math.random()`, `random.random()`/`random.randint`, `rand()`,
  `java.util.Random`, time-seeded RNG used for tokens/session ids/password-reset/OTP/nonces/keys.
- **Static/hardcoded key or IV** (CWE-321/329): fixed AES key/IV in source; reused nonce; predictable salt.
- **ECB mode** (CWE-327): `AES/ECB` leaks plaintext patterns.
- **Missing integrity / unauthenticated encryption**: CBC without a MAC (padding-oracle risk); encrypt
  without authenticate; not using AEAD (AES-GCM/ChaCha20-Poly1305).
- **Bad TLS/cert handling**: disabled verification (`verify=False`, `rejectUnauthorized:false`,
  `InsecureSkipVerify:true`, trust-all TrustManager/HostnameVerifier).
- **Weak KDF params**: low PBKDF2 iterations, no salt.

## Sinks (grep targets)
`md5(|sha1(|MD5|SHA1|DES|RC4|Math.random|random\.(random|randint|choice)|util.Random|AES/ECB|ECB|
verify=False|rejectUnauthorized|InsecureSkipVerify|createCipher\(|PBKDF2.*iterations|IV\s*=`.
Look near "password", "token", "key", "encrypt", "sign", "session".

## Detection recipe
1. Grep the patterns above; for each, determine **what is being protected** and the **threat model**.
2. Password storage: which hash + salt + params? Token generation: which RNG? Encryption: algorithm, mode,
   key/IV source, integrity?
3. Confirm the weakness is used on security-relevant data (a non-security CRC/`md5` for a cache key is fine).

## PoC / evidence
- The code using the weak primitive at `file:line`. For randomness: show tokens derive from a predictable
  RNG (attacker can predict/brute future values). For static key: show the literal key/IV.
- Padding oracle / ECB: describe the exploit conditions; a full oracle PoC is usually `needs-runtime`.

## False-positive filters
- MD5/SHA1 used for **non-security** purposes (ETags, cache keys, dedup checksums) - not a finding.
- CSPRNG in use: `secrets`/`os.urandom` (Python), `crypto.randomBytes` (Node), `SecureRandom` (Java),
  `crypto/rand` (Go). Password hashing via argon2/bcrypt/scrypt with salt.
- AEAD (AES-GCM/ChaCha20-Poly1305) or encrypt-then-MAC; per-message random IV/nonce; keys from a KMS/secret
  manager. TLS verification enabled (the insecure flags are dev-only and not shipped).

## CWE / OWASP / severity
CWE-327/328/330/338/321/326/916, CWE-295 (cert validation). OWASP A02:2021. Forgeable tokens / broken auth
crypto / disabled TLS verification -> **high/critical**; weak-but-limited -> medium.

## Chaining hints
Predictable reset/session tokens -> `auth` account takeover; static JWT/HMAC key -> forge tokens; disabled
TLS verification -> MITM -> credential capture; weak password hash + a `secrets`/`sqli` DB dump -> mass
credential cracking.

## Mitigation
Use argon2/bcrypt/scrypt (salted) for passwords; CSPRNG for all tokens/keys/IVs; AES-GCM or
ChaCha20-Poly1305 (AEAD) with per-message nonces; keys from a KMS/secret manager, never hardcoded; enforce
TLS certificate verification; drop MD5/SHA1/DES/RC4/ECB for security purposes.
