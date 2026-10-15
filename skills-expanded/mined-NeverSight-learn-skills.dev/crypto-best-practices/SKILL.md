---
name: crypto-best-practices
description: >
  Cryptographic best practices for secure system design. 
  Use when: choosing encryption algorithms, implementing password hashing, selecting key lengths, 
  using secure random number generation, implementing digital signatures, designing TLS deployments, 
  key management, or avoiding common cryptographic pitfalls.
argument-hint: 'Specify the cryptographic task, e.g. "symmetric encryption for data at rest", "password hashing", "asymmetric signatures for API authentication"'
---

# Cryptographic Best Practices

## ⚠️ Golden Rule

**Use a battle-tested library that handles cryptographic composition correctly for you:**
1. **NaCl** (by Daniel Bernstein)
2. **libsodium** (NaCl fork by Frank Denis)
3. **monocypher** (libsodium fork by Loup Vaillant)

If you use these libraries, most low-level decisions are already made for you. Only continue reading if forced to make your own choices.

---

## 1. Symmetric Encryption

**Decision Tree:**
- Do you have access to a Key Management System (KMS)? → Use KMS
- Otherwise → Use AEAD (Authenticated Encryption with Associated Data)

**Recommended algorithms (in order):**
1. NaCl/libsodium/monocypher default
2. ChaCha20-Poly1305 (faster in software)
3. AES-GCM (industry standard, faster with AES-NI)
4. AES-CTR with HMAC (fast in software)

**❌ Avoid:**
- AES-CBC, AES-CTR alone (must use AEAD)
- Block ciphers with 64-bit blocks (Blowfish, 3DES)
- OFB mode
- RC4 (broken)

**Why AEAD?** Prevents forged ciphertexts. A single byte corruption either fails authentication or reveals nothing.

---

## 2. Symmetric Key Length

**Recommendations for data protection through 2050:**
- **Minimum**: 128 bits
- **Maximum**: 256 bits (no harm in using larger)

| Standard | Recommendation | Notes |
|----------|---|---|
| NIST | 192 bits | Conservative government standard |
| ECRYPT II | 256 bits | Academic consensus, most conservative |
| ANSSI | 128 bits | European standard, adequate |
| IAD-NSA | 256 bits | Highest security requirement |

**If your symmetric key is derived from user input (password):**
- The password must provide **at least as many bits of entropy** as the target key length
- Example: 128-bit AES key needs ≥128 bits of entropy in the password

---

## 3. Symmetric Signatures (HMAC/MAC)

Use when **authenticating but not encrypting** (e.g., API requests, message authentication).

**Recommended algorithms (in order):**

**HMAC variants:**
1. HMAC-SHA-512/256 (truncated SHA-512)
2. HMAC-SHA-512/224 (truncated SHA-512)
3. HMAC-SHA-384
4. HMAC-SHA-224
5. HMAC-SHA-512
6. HMAC-SHA-256

**Alternatives (preferred by cryptographers):**
1. Keyed BLAKE2b
2. Keyed BLAKE2s
3. Keyed SHA3-512
4. Keyed SHA3-256

**❌ Avoid:**
- HMAC-MD5
- HMAC-SHA1
- Custom "keyed hash" constructions
- Complex polynomial MACs
- Encrypted hashes
- CRC

**Implementation tip:** Always use a secure compare function to prevent timing attacks on MAC verification.

---

## 4. Hashing Algorithms

Use when you need **collision-resistant, one-way hashing** (not password hashing — see Section 5).

**Recommended (pick one):**
1. **SHA-2** (SHA-256, SHA-384, SHA-512): Fast, time-tested, industry standard
2. **BLAKE2** (BLAKE2b, BLAKE2s): Faster than SHA-3, SHA-3 finalist
3. **SHA-3** (SHA3-256, SHA3-512): Slowest but industry standard

**❌ Avoid:**
- SHA-1 (collision vulnerabilities proven)
- MD5 (broken)
- MD6
- EDON-R

**Truncation note:** SHA-2 output truncation (e.g., SHA-512/256) sidesteps length extension attacks and is safe.

---

## 5. Random Number Generation

**Rule:** Always use your **operating system's CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator).

| OS | CSPRNG | Usage |
|----|--------|-------|
| Linux / BSD / macOS | `/dev/urandom` | Primary choice |
| Windows | `CryptGenRandom` | Primary choice |

**Important:** `/dev/random` is **NOT** more secure than `/dev/urandom`. They use the same CSPRNG; they differ only in blocking behavior.

**Generate:** 256-bit random numbers as default.

**Fallback (constrained environments only):**
- Use **fast-key-erasure** if you're in embedded firmware where OS RNG unavailable
- Requires careful entropy seeding on each boot (difficult to get right)
- Last resort only

**❌ Avoid:**
- Userspace RNG
- Predictable seeds (`srand(time())`)
- Weak PRNGs for cryptographic use

---

## 6. Password Hashing

Use when storing user passwords in a database.

### Algorithm Selection

**Recommended (in order):**

1. **Argon2id** (winner of Password Hashing Competition)
   - Tune appropriately: sufficient CPU time + RAM allocation
   - Shows no serious weaknesses, well-analyzed

2. **scrypt** (≥16 MB RAM)
   - Sensitive to parameters; can be weaker than bcrypt if misconfigured
   - Time-memory tradeoff attacks possible

3. **bcrypt** (≥cost 5)
   - Use as: `bcrypt(base64(SHA-512(password)))`
   - Mitigates 72-character password limit + leading NULL byte problem

4. **SHA-512-crypt** (≥5,000 rounds)
   - Older but acceptable

5. **SHA-256-crypt** (≥5,000 rounds)

6. **PBKDF2** (≥600,000 rounds per OWASP 2023)
   - Industry standard, but higher iteration count needed

**❌ Avoid:**
- Plaintext passwords
- Naked SHA-2, SHA-1, MD5
- Custom homebrew algorithms
- Any encryption algorithm (for password storage)

### Cost Parameters

| Algorithm | Parameter | Minimum | Recommendation |
|-----------|-----------|---------|---|
| Argon2id | Time cost + Memory cost | - | Tune to CPU/RAM available (≥3s on target hardware) |
| scrypt | N, r, p | N≥16384 | ≥16 MB RAM allocation |
| bcrypt | Cost factor | 5 | 10-12 (tune for ≤100ms latency) |
| SHA-512-crypt | Rounds | 5,000 | 5,000-10,000 |
| SHA-256-crypt | Rounds | 5,000 | 5,000-10,000 |
| PBKDF2 | Iterations | 600,000 | 600,000+ (increase with time) |

---

## 7. Asymmetric Encryption

**Stop using RSA. Use ECC (Elliptic Curve Cryptography).**

**Reasons to prefer ECC:**
- Attacks on RSA proceeding faster than on ECC
- RSA encourages insecure direct encryption (loses forward-secrecy)
- ECC puts security burden on cryptographers (good), not implementors (bad)
- Fewer knobs to turn = fewer mistakes

**If you absolutely must use RSA:**
- Use **RSA-KEM** (not raw RSA encryption)
- But really, use ECC instead

**Recommended approach:**
- Use **NaCl/libsodium/monocypher**, which provide safe ECC-based encryption by default

**❌ Avoid:**
- Raw RSA encryption/decryption
- ElGamal
- OpenPGP, OpenSSL, BouncyCastle for new projects (too many knobs)

---

## 8. Asymmetric Key Length

**For data protection through 2050:**

| Scheme | Minimum | Recommended | Protection |
|--------|---------|---|---|
| ECC/ECDH | 256 bits | 256 bits | ~128-bit symmetric equivalent security |
| RSA/DH Group | 2048 bits | 3072+ bits (if forced) | Equivalent to ~112-bit symmetric |

**Ratios:** ECC 256-bit ≈ RSA 2048-bit in security strength.

**Personal recommendation:**
- **256-bit minimum for ECC/ECDH keys**
- **2048-bit minimum for RSA/DH** (but you shouldn't use RSA)

---

## 9. Asymmetric Signatures

**Deterministic signatures are misuse-resistant.**

**Recommended (in order):**
1. **NaCl/libsodium/monocypher** (handles everything)
2. **Ed25519** (NaCl default, most popular non-Bitcoin signature scheme)
3. **RFC 6979** (deterministic DSA/ECDSA)

**Why deterministic?** Protects against failures like the PlayStation 3 ECDSA flaw, where nonce reuse leaked private keys.

**❌ Avoid:**
- ECDSA (unless using deterministic RFC 6979)
- DSA
- RSA signatures

---

## 10. Diffie-Hellman Key Exchange

**Golden rule:** Don't roll your own encrypted transport. Use **NaCl**.

If you must implement key exchange:

**Recommended (in order):**
1. **NaCl/libsodium/monocypher** (use this!)
2. **Curve25519** (carefully chosen to minimize implementation errors)
3. **2048-bit DH Group #14** (if Curve25519 unavailable)

**Curve25519 is special:** The entire curve was designed to prevent common implementation mistakes.

**Important:** Use an **Authenticated Key Exchange (AKE)** that resists Key Compromise Impersonation (KCI).

**❌ Avoid:**
- NIST curves with ECDH (point validation bugs leak secrets)
- Conventional DH negotiation
- SRP, J-PAKE
- Elaborate key negotiation schemes

---

## 11. Website Security (HTTPS/TLS)

**Recommendation:** Use a **web hosting provider that manages TLS for you** (AWS, Heroku, etc.).

If you self-host:

1. Use **OpenSSL** (not LibreSSL, BoringSSL, BearSSL)
   - OpenSSL is on-the-ball with vulnerability disclosure
   - Others don't justify the added complexity for new projects

2. Use **Let's Encrypt** for certificates
   - Free, automated, and solid
   - Set up cron for regular re-fetches

**Configuration: Hardcode these settings**
- TLS 1.2 or higher (no downgrade negotiation)
- ECDHE cipher suites only (forward secrecy)
- AES-GCM cipher only

**Modern TLS policy example:**
```
ECDHE-ECDSA-AES256-GCM-SHA384:
ECDHE-RSA-AES256-GCM-SHA384:
ECDHE-ECDSA-AES128-GCM-SHA256:
ECDHE-RSA-AES128-GCM-SHA256
```

❌ **Avoid:**
- Default TLS configuration
- Negotiable cipher suites (prevents downgrade attacks)
- Export-grade ciphers (FREAK, Logjam attacks)
- CBC mode ciphers (BEAST, Lucky13, CRIME)

---

## 12. Client-Server Application Security

**Scenario:** Custom transport layer (not browser-based).

**Use TLS because:**
- Many TLS vulnerabilities require browser JavaScript execution
- You control both client and server (no CA risk)
- You can self-sign and ship cert with code
- Standard approach proven at scale

**Why not roll your own?** See Salt Stack's e=1 RSA disaster (RSA with exponent = 1 = encrypted plaintext).

**If implementing custom transport over TLS:**
- Hardcode TLS 1.2+
- ECDHE ciphers only
- AES-GCM only
- No negotiation

---

## 13. Online Backups

**Best practice: Host backups yourself.**

**Recommended approaches (in order):**
1. **OpenZFS** with redundancy + 256-bit checksums (best)
2. **Tarsnap** (cloud-based, encrypted client-side, proven)
3. **Keybase** KBFS (end-to-end encrypted, 250GB free, but closed ecosystem)

**Cloud storage (❌ Avoid):**
- Google, Apple, Microsoft: Trust-based
- Dropbox: Trust-based
- Amazon S3: No end-to-end encryption by default

---

## 14. Hybrid Encryption (Combining Asymmetric + Symmetric)

**When:** Encrypting long messages with public key cryptography.

**Process:**
1. Generate random symmetric key (e.g., 256-bit)
2. Encrypt message with symmetric cipher (AES-GCM)
3. Encrypt symmetric key with asymmetric encryption (Curve25519 / ECC)
4. Send: encrypted key + encrypted message

**NaCl/libsodium/monocypher handle this automatically** in high-level APIs (`crypto_box_easy`).

---

## 15. Common Implementation Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| **Nonce reuse in AEAD** | Leaks auth key, breaks encryption | Generate fresh nonce each time, use AEAD-SIV for nonce-reuse resistance |
| **Timing attacks on MAC** | Attacker forges messages | Use constant-time comparison |
| **Crypto canonicalization bugs** | HMAC input variations leak secrets | Document exact input format, use NaCl |
| **Key derivation from weak passwords** | Weak keys from "secure" storage | Use password hashing (Argon2), sufficient CPU cost |
| **Hot-loading unvalidated keys** | Attacks on ECC points | Use libraries that validate key format |
| **Mixing encryption contexts** | Nonce confusion, key reuse | Unique key + IV per context, use NaCl |

---

## 16. Quick Reference Matrix

| Task | Algorithm | Min Key Size | Library |
|------|-----------|---|---|
| Encrypt data at rest | ChaCha20-Poly1305 or AES-GCM | 256 bits | libsodium |
| Sign API requests | HMAC-SHA-512/256 | 256 bits | libsodium |
| Hash data | SHA-2 or BLAKE2b | N/A | libsodium |
| Generate random ID | OS CSPRNG (`/dev/urandom`) | 256 bits | OS |
| Hash password | Argon2id | Tune time+memory | libsodium |
| Public key encryption | Curve25519 (ECC) | 256 bits | libsodium |
| Digital signature | Ed25519 | 256 bits | libsodium |
| Key exchange | Curve25519 | 256 bits | libsodium |
| Website HTTPS | AES-GCM + ECDHE | 256 bits | OpenSSL + Let's Encrypt |

---

## 17. Decision Flowchart

```
START: I need cryptography

├─ "I should just use NaCl/libsodium/monocypher"
│  └─ STOP ✓ (90% of cases)
│
├─ "I must implement a choice myself"
│  │
│  ├─ Symmetric encryption?
│  │  └─ ChaCha20-Poly1305 or AES-GCM (with AEAD)
│  │
│  ├─ Password storage?
│  │  └─ Argon2id (tune time+memory)
│  │
│  ├─ Message authentication only?
│  │  └─ HMAC-SHA-512/256 or Keyed BLAKE2b
│  │
│  ├─ General hashing?
│  │  └─ SHA-2 or BLAKE2
│  │
│  ├─ Random numbers?
│  │  └─ /dev/urandom (or OS equivalent)
│  │
│  ├─ Public key encryption?
│  │  └─ NaCl curve25519_xsalsa20poly1305
│  │
│  ├─ Digital signatures?
│  │  └─ Ed25519 or NaCl default
│  │
│  ├─ Key exchange?
│  │  └─ Curve25519 (not DH-1024)
│  │
│  └─ Website HTTPS?
│     └─ OpenSSL + Let's Encrypt (ECDHE + AES-GCM)
```

---

## Further Reading

- **[NaCl.cr.yp.to](https://nacl.cr.yp.to/)** — Original library documentation
- **[Latacora Cryptographic Right Answers](http://latacora.singles/2018/04/03/cryptographic-right-answers.html)** — Similar guidance
- **[SafeCurves](https://safecurves.cr.yp.to/)** — Guidance on elliptic curve safety
- **[OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)** — Password hashing standards
- **[Noise Protocol Framework](http://noiseprotocol.org/)** — Authenticated encryption protocol
- **[PASETO](https://github.com/paseto-standard/paseto-spec)** — Secure alternative to JWT
