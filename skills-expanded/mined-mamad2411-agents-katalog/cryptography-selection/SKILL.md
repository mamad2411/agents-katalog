---
name: cryptography-selection
description: Select and parameterize cryptographic primitives correctly for confidentiality, integrity, authentication, and signatures — symmetric (AES-GCM, AES-GCM-SIV, ChaCha20-Poly1305, XChaCha20-Poly1305), KEMs and key-exchange (ECDH X25519, ML-KEM hybrid), signatures (Ed25519, ECDSA, ML-DSA), password / key derivation (Argon2id, scrypt, HKDF), MACs (HMAC-SHA256, KMAC), and emerging post-quantum primitives (NIST FIPS 203/204/205). Use when designing any encryption, signing, hashing, or key-exchange flow, or when reviewing existing crypto for misuse.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Cryptography Selection

Select the right cryptographic primitive, mode, parameter, and library for the job — and just as importantly, refuse the dozen wrong-but-superficially-attractive options that line up next to it. Cryptographic mistakes are typically silent (the code runs, returns plausible-looking ciphertext) and catastrophic (every record encrypted under the broken construction is decryptable forever).

## Context

You are a senior cryptography reviewer working on $ARGUMENTS. Most production crypto bugs are not novel cryptanalysis — they are reused IVs, missing authentication, AES-CBC without HMAC, MD5 password hashes, hard-coded keys, custom-built protocols, and post-quantum risk being ignored. Your job is to pick well-vetted primitives, use them through high-level "misuse-resistant" APIs (libsodium, AWS Encryption SDK, Tink, age, ML-KEM hybrids), and document parameter choices so the next engineer cannot quietly weaken them.

## Domain Context

- **Confidentiality**: only intended recipients can read the data
- **Integrity**: any modification is detectable
- **Authenticity**: the message provably came from the claimed sender
- **AEAD (Authenticated Encryption with Associated Data)**: combines confidentiality + integrity in one primitive — the **only** correct choice for symmetric encryption in 2026
- **KEM (Key Encapsulation Mechanism)**: modern replacement vocabulary for "asymmetric encryption used for key exchange" — ML-KEM, RSA-KEM, ECIES
- **Forward secrecy**: compromise of long-term keys does not expose past sessions (ECDHE, X3DH, hybrid X25519+ML-KEM)
- **Post-quantum (PQC)**: NIST FIPS 203 (ML-KEM) for key establishment, FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA) for signatures, FIPS 206 (FN-DSA) for compact signatures
- **HNDL (Harvest Now, Decrypt Later)**: any long-lived confidential data encrypted today with classical-only key exchange will be decryptable when a CRQC arrives — start hybrid PQC for HNDL-relevant channels in 2026 (see `post-quantum-cryptography-migration` skill)
- **Crypto-agility**: algorithm choice expressed in configuration, not code, so primitives can be swapped without refactoring

## Stack Baseline (2026)

| Need | Recommended primitive | Recommended library |
| --- | --- | --- |
| Symmetric encryption (single-key-per-message OK) | AES-256-GCM, ChaCha20-Poly1305 | libsodium, Tink, AWS Encryption SDK, age |
| Symmetric encryption (random nonces / many messages per key) | **AES-256-GCM-SIV** or **XChaCha20-Poly1305** (192-bit nonce) | libsodium, RustCrypto `aes-gcm-siv` |
| Disk / volume encryption | XTS-AES-256 (LUKS2, BitLocker, FileVault) | OS-native |
| Streaming / large payloads | Encrypted chunking (libsodium `secretstream`, age, Tink streaming AEAD) | libsodium, Tink |
| Key wrapping / envelope encryption | AES-KW, AWS/GCP/Azure KMS Encrypt/Decrypt, HashiCorp Vault Transit | KMS / HSM |
| Key derivation from a high-entropy secret | HKDF-SHA-256 / SHA-512 | libsodium, RustCrypto `hkdf` |
| Key derivation from a password | **Argon2id** (preferred), scrypt (legacy compat), PBKDF2-HMAC-SHA-256 ≥ 600K iters (FIPS only) | libsodium, `argon2-cffi`, `node-argon2` |
| MAC (separate from encryption) | HMAC-SHA-256, KMAC-256 | RustCrypto `hmac`, libsodium |
| Hash (general) | SHA-256 / SHA-512, SHA-3, BLAKE3 | OS / language stdlib |
| Hash (collision-resistance critical) | SHA-256 minimum; SHA-3 if regulatory | stdlib |
| Signatures (modern default) | **Ed25519** | libsodium, RustCrypto `ed25519-dalek` |
| Signatures (NIST / FIPS environments) | ECDSA P-256 / P-384 (SHA-256/384), RSA-PSS 3072+ | OpenSSL 3.x, BoringSSL |
| Signatures (long-lived: code/firmware) | **SLH-DSA (FIPS 205)** or LMS / XMSS (NIST SP 800-208) | OpenSSL 3.5+, vendor HSM |
| Signatures (everyday PQC + crypto-agility) | **ML-DSA (FIPS 204)**, hybrid composite with Ed25519 / ECDSA | OpenSSL 3.5+, BoringSSL, BouncyCastle 1.79+ |
| Key exchange (TLS / VPN / mTLS) | X25519 with **hybrid `X25519MLKEM768`** (TLS 1.3) | OpenSSL 3.5+, Go 1.24+, rustls 0.23+ |
| Random | OS CSPRNG: `getrandom(2)`, `BCryptGenRandom`, `arc4random_buf`, `crypto.randomBytes`, `secrets.token_bytes` | OS / stdlib |
| Format / envelope | **age** (file encryption), **JOSE** (JWS/JWE for tokens), **COSE** (CBOR), **PASETO v4** (better-than-JWT alternative) | `age`, `jose`, PyJWT, paseto |

## When to Use This Skill

- Designing any new encryption, signing, hashing, or key-exchange flow
- Reviewing a security-impacting PR that touches `crypto.*`, `cipher`, `hash`, `sign`, `verify`, `kdf`, `pbkdf2`, `Argon2`, `MessageDigest`, `BCrypt`, `KMS`
- Selecting a library, format (JOSE vs PASETO, age vs PGP), or HSM/KMS
- Updating a system in scope of CNSA 2.0 / NIS2 / EU CRA / FIPS 140-3 / PCI 4.0
- Migrating off RSA / ECDSA / SHA-1 / 3DES / MD5 / unsalted hashes

## Prerequisites

1. **Threat model**: who is the adversary, what is their capability (passive on-the-wire, active MITM, server compromise, nation-state, future CRQC), and what are they after?
2. **Data sensitivity & lifetime**: short-lived session token vs. PHI retained 30 years — drives PQC timing
3. **Compliance scope**: FIPS 140-3, CNSA 2.0, PCI 4.0, NIS2, sector regs — narrows the algorithm allow-list
4. **Performance budget**: throughput, latency, memory, embedded / mobile constraints
5. **Operational envelope**: KMS / HSM available? rotation cadence? air-gapped?
6. **Library / language constraints**: vetted stdlib options vs. third-party

## Instructions

### 1. Decide the AEAD construction first

For symmetric encryption, the answer in 2026 is always an AEAD (Authenticated Encryption with Associated Data). Choose by **nonce strategy**:

| Situation | AEAD |
| --- | --- |
| Counter-managed nonce, no nonce reuse possible | AES-256-GCM (12-byte nonce) or ChaCha20-Poly1305 |
| Random nonces from many writers, or > ~2^32 messages per key | **AES-256-GCM-SIV** (nonce-misuse-resistant) or **XChaCha20-Poly1305** (192-bit random nonce) |
| Long streams / files | libsodium `secretstream`, age, Tink streaming AEAD |
| Disk volumes | XTS-AES-256 |

**Never** select AES-CBC, AES-CTR, AES-ECB, or unauthenticated stream ciphers. If a library forces them on you, wrap with HMAC-SHA-256 (Encrypt-then-MAC) and review the construction — but prefer switching libraries.

### 2. Use envelope encryption with KMS

For data at rest in a real production system:

1. Generate a **DEK** (data encryption key) per object/row/file with the OS CSPRNG.
2. Encrypt data with the DEK using AES-256-GCM (or GCM-SIV / XChaCha).
3. **Wrap** the DEK with a **KEK** managed in AWS KMS / GCP KMS / Azure Key Vault / Vault Transit / HashiCorp Vault.
4. Store ciphertext + wrapped DEK + KMS key id + algorithm version side-by-side.
5. Rotate the KEK (KMS handles transparently); on read, ask KMS to unwrap.

This pattern gives you per-object keys, automatic KEK rotation, no plaintext keys in your code, and an audit trail.

### 3. Key exchange & TLS — go hybrid PQC at the edge

For TLS 1.3, default the supported groups to **`X25519MLKEM768:X25519:secp256r1`** (OpenSSL 3.5+, Go 1.24+, BoringSSL, rustls 0.23+). This adds ~1 KB to handshakes but provides immediate HNDL protection for any client that supports it, costs nothing for clients that don't.

For other key-establishment surfaces (mTLS, IPsec, SSH 9.9+ with `mlkem768x25519-sha256`, WireGuard PQ wrappers): same approach — **hybrid** until ecosystem maturity is conclusive (likely 2027–2028).

For application-layer KEMs (file encryption to a recipient, end-to-end messaging): use vetted constructions (`age` with X25519 recipients, libsodium sealed boxes); avoid raw RSA-OAEP designs.

See `post-quantum-cryptography-migration` for the full roadmap.

### 4. Signatures: pick by lifetime and ecosystem

| Use case | Pick |
| --- | --- |
| Modern app, full control over verifier | **Ed25519** — small keys, fast, no parameter footguns |
| FIPS / CNSA / vendor environment | ECDSA P-256 (SHA-256), RSA-PSS-3072+ (avoid PKCS#1 v1.5) |
| Crypto-agility into PQ era | **ML-DSA-65** (composite with Ed25519 / ECDSA during transition) |
| Long-lived code or firmware signing | **SLH-DSA** or LMS/XMSS (stateful, NIST SP 800-208) |
| Compact PQ signatures (constrained bandwidth) | FN-DSA — only with audited constant-time impls |

Never sign with raw RSA/ECDSA over `MD5` or `SHA-1`. Never use `RSASSA-PKCS1-v1_5` for new systems — use **RSA-PSS**. Never roll your own signature scheme.

### 5. Hashing & MACs

- **General-purpose hash**: SHA-256 (or SHA-512 on 64-bit hot paths) is fine. SHA-3 / BLAKE3 if you have a specific reason.
- **Collision-critical**: ≥ SHA-256. **Never** MD5 or SHA-1 anywhere a collision matters (signing, dedup, content-addressed storage).
- **MAC**: HMAC-SHA-256 (or KMAC-256 for SHA-3 ecosystems). Never use a plain hash as a MAC (`H(key || msg)` — vulnerable to length-extension).
- **Constant-time comparison** of MACs / tokens: `crypto.timingSafeEqual`, `hmac.compare_digest`, `subtle.ConstantTimeCompare`. Never `==` on a secret.

### 6. Password & key derivation

| Input | Use |
| --- | --- |
| User password | **Argon2id** (m=64 MiB, t=3, p=1 baseline; tune to ~250 ms on target hardware) |
| User password (FIPS-only environment) | PBKDF2-HMAC-SHA-256, ≥ 600,000 iterations (OWASP 2023 floor) |
| Already-high-entropy shared secret (DH output, KMS-derived) | HKDF-SHA-256 with non-empty `info` and `salt` |
| Many derived sub-keys from one master | HKDF-Expand with distinct `info` per purpose |
| Disk encryption from passphrase | scrypt (LUKS2 default) or Argon2id (LUKS2 newer) |

Always store hashed passwords with their algorithm + parameters embedded (`$argon2id$v=19$m=65536,t=3,p=1$...$...`) so you can up-shift parameters over time.

Check passwords against breach lists (Have I Been Pwned k-Anonymity API) at set/change time. Refuse the top-100K most-common passwords regardless of length. Length minimum 12 (NIST SP 800-63B Rev 4); no rotation requirement; allow ≥ 64 char passphrases; allow all printable Unicode.

### 7. Tokens, JWTs, and the "JWT-vs-PASETO" question

JWTs are deeply foot-gunny: algorithm-confusion (`alg=none`), key-confusion (HMAC verifier accepts RSA public key as HMAC key), expiry not enforced, etc.

- If you must use JWT: pin `alg` server-side (never trust the header), use **EdDSA / Ed25519** or **ES256**, **never** `HS256` for cross-service tokens, set `exp`/`nbf`/`iat`/`aud`/`iss`, validate them rigorously, prefer signed JWS (not encrypted JWE).
- Better default in 2026: **PASETO v4** (Ed25519 / XChaCha20-Poly1305) — no algorithm header, no negotiation, no curve confusion.
- For long-lived service identity: SPIFFE JWT-SVIDs.
- Never put secrets *in* a JWT (signed ≠ encrypted) unless you also use JWE — and even then prefer keeping secrets on the server.

### 8. Randomness

The only correct sources are OS CSPRNGs:

- Python: `secrets.token_bytes`, `secrets.token_urlsafe`
- Node: `crypto.randomBytes`, `crypto.randomUUID`
- Go: `crypto/rand` (never `math/rand` for security)
- Java: `SecureRandom.getInstanceStrong()` or just `new SecureRandom()` on Linux (uses `getrandom`)
- Rust: `rand::rngs::OsRng` or `getrandom` crate
- Browser: `window.crypto.getRandomValues`, `crypto.subtle`

Never seed your own RNG for security tokens. Never generate "random" values from time, PID, or `Math.random`.

### 9. Crypto-agility

Express algorithm choice as configuration (a `crypto-suite` name → primitive set). Version every ciphertext with the suite id so future you can roll forward. Wrap primitives behind interfaces (`Signer`, `KemEncapsulator`, `Verifier`, `AEADCipher`); never let business logic call `RSA.generate(2048)` directly. Maintain a Cryptographic Bill of Materials (CBOM) generated in CI.

### 10. Code-review red flags

A 5-second scan of any crypto PR — flag every one of these:

- `MD5`, `SHA1`, `DES`, `3DES`, `RC4` anywhere
- `AES.MODE_CBC` / `AES.MODE_ECB` / `AES.MODE_CTR` without an explicit MAC
- `pickle.loads`, `yaml.load` (without `SafeLoader`), `eval`, `exec` on data adjacent to crypto
- Hard-coded keys, IVs, salts, or "test" credentials
- `Math.random`, `random.random`, `time.time` used to generate tokens
- `==` comparing a secret, MAC, or token
- `HS256` JWT used between services
- `weights_only=False` on `torch.load`, `trust_remote_code=True` on Hugging Face loaders (adjacent supply-chain concern)
- Custom padding, custom modes, custom signature schemes
- "We'll add MFA / authentication / encryption later"

## Common Pitfalls

| Pitfall | Why it fails | Fix |
| --- | --- | --- |
| Reused GCM nonce | Two messages under same key+nonce → recover plaintext + forge | Counter nonce, or AES-GCM-SIV / XChaCha20-Poly1305 |
| Encrypt-only with AES-CBC, no MAC | Padding-oracle / bit-flip attacks | Use AEAD (GCM, ChaCha20-Poly1305) |
| RSA-PKCS#1 v1.5 for signatures or encryption | Bleichenbacher and adjacent oracles | RSA-PSS for signatures, RSA-OAEP for encryption — or move to ECDH/Ed25519 |
| MD5 / SHA-1 / unsalted SHA-256 for passwords | Brute-forceable with commodity GPU | Argon2id |
| `HS256` JWT shared between services | Any service that verifies can also forge; algorithm-confusion possible | Asymmetric (EdDSA / ES256) or PASETO v4 |
| Comparing tokens with `==` | Timing side-channel | Constant-time comparison (`hmac.compare_digest`) |
| Keys in env vars / Git / `secrets.yaml` | Trivial exfil; rotation impossible | KMS / Vault, envelope encryption, OIDC federation |
| Pre-image of "we encrypt at rest" using ECB | Patterns visible in ciphertext (the famous Tux image) | AEAD as above |
| Custom protocol "because we know what we're doing" | History suggests otherwise | Use a vetted standard (TLS, Noise, MLS, age, libsodium) |
| Ignoring HNDL for long-lived confidential data | Captured today, decrypted in 2035 | Hybrid PQC (`X25519MLKEM768`) for TLS now |

## Output Format

A **Cryptography Selection Decision Record**:

```markdown
# Cryptography Decision Record: <feature / system>

## 1. Threat model summary
- Adversary capability, data sensitivity, data lifetime, compliance scope

## 2. Selected primitives
| Need | Algorithm | Parameters | Library | Crypto-suite id |

## 3. Key management
- DEK / KEK strategy, KMS, rotation cadence, audit logging

## 4. Crypto-agility
- Suite versioning, migration path, CBOM coverage

## 5. PQ readiness
- Hybrid in scope? roadmap reference

## 6. Compliance mapping
- FIPS 140-3 / CNSA 2.0 / PCI 4.0 / NIS2 / sector

## 7. Review evidence
- Fuzz / KAT / interop tests, third-party crypto review (if any)
```

## Worked Example

**Requirement**: encrypt customer PII at rest, store in Postgres, retain 10 years (GDPR + sector reg). Long-lived → HNDL relevant.

| Decision | Choice | Rationale |
| --- | --- | --- |
| Symmetric algo | AES-256-GCM-SIV | DEK reused across rows; nonce-misuse resistance avoids catastrophe if an ORM regenerates a row |
| Key strategy | Envelope: per-row DEK wrapped by AWS KMS KEK | Audit trail, automatic KEK rotation, IAM-controlled use |
| Field hashing for search | HMAC-SHA-256 with a separate KMS-managed key | Searchable equality without exposing plaintext |
| Password column for portal users | Argon2id m=64MiB t=3 p=1 | OWASP 2023 baseline; tuned to ~250 ms |
| Backups | KMS-encrypted snapshots + offsite copy with separate KEK | Cross-region, key-isolated |
| Transport | TLS 1.3, supported groups `X25519MLKEM768:X25519:secp256r1` on the API gateway | HNDL protection now |
| Crypto-suite version | `pii-v1 = aesgcmsiv-256 + kms-v1 + argon2id-r1 + tls13-mlkem` | Stamped into every ciphertext |
| PQ roadmap | Migrate `pii-v1 → pii-v2` adding ML-KEM data-key wrapping when AWS KMS adds PQC support (target 2027) | Tracked in CBOM |

## Decision Framework

- **Counter-managed nonce or random nonce?** Counter → GCM. Random or distributed writers → GCM-SIV / XChaCha20-Poly1305.
- **JWT or PASETO?** New system, full control: PASETO v4. Existing JWT ecosystem: lock down to EdDSA, never `HS256` between services, validate everything explicitly.
- **Ed25519 or ECDSA P-256?** Ed25519 unless you must comply with FIPS / CNSA — then ECDSA.
- **AES or ChaCha?** AES-GCM(-SIV) on platforms with AES-NI; ChaCha20-Poly1305 on platforms without (mobile, embedded). Both are fine choices.
- **Roll-your-own KDF or HKDF?** HKDF, every time.
- **Encrypt with KMS directly or envelope?** Envelope. KMS direct-encrypt has a 4 KB ciphertext limit and burns API calls.
- **PQC now or later?** Hybrid PQ for any TLS / VPN / mTLS in front of long-lived confidential data — start in 2026. Pure PQ — wait for ecosystem maturity.

## Authoritative References

- NIST SP 800-175B (Cryptographic Standards): https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-175B.pdf
- NIST SP 800-131A Rev 3 (Algorithm Transitions): https://csrc.nist.gov/pubs/sp/800/131/a/r3/final
- NIST SP 800-63B Rev 4 (Authentication / passwords): https://pages.nist.gov/800-63-4/sp800-63b.html
- NIST FIPS 197 (AES): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
- NIST SP 800-38D (GCM): https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf
- RFC 8452 (AES-GCM-SIV): https://www.rfc-editor.org/rfc/rfc8452
- RFC 8439 (ChaCha20-Poly1305): https://www.rfc-editor.org/rfc/rfc8439
- RFC 5869 (HKDF): https://www.rfc-editor.org/rfc/rfc5869
- RFC 9106 (Argon2): https://www.rfc-editor.org/rfc/rfc9106
- RFC 8032 (Ed25519): https://www.rfc-editor.org/rfc/rfc8032
- NIST FIPS 203 / 204 / 205 (PQC): https://csrc.nist.gov/projects/post-quantum-cryptography
- OWASP Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- libsodium documentation: https://doc.libsodium.org/
- Google Tink: https://developers.google.com/tink
- AWS Encryption SDK: https://docs.aws.amazon.com/encryption-sdk/
- PASETO specification: https://github.com/paseto-standard/paseto-spec
- age encryption: https://age-encryption.org/
- Real-World Cryptography (Wong, 2021); Serious Cryptography (Aumasson, 2024 2nd ed.): book-length treatments
