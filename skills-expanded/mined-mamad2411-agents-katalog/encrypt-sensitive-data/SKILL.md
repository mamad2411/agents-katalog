---
name: encrypt-sensitive-data
description: Encrypts sensitive data at rest, in transit, and per-field using AEAD-only ciphers (AES-256-GCM or ChaCha20-Poly1305 — never ECB, never unauthenticated CBC, never raw RSA) — envelope encryption where a KMS-held KEK wraps a per-record/per-tenant DEK, per-column field encryption for PII with deterministic-vs-randomized chosen per query need, strict unique-nonce/IV discipline (random 96-bit or counter, NEVER reused under one key), AAD binding ciphertext to its context (tenant/row id), versioned keys + rotation that re-wraps DEKs without re-encrypting data, TLS 1.2+/1.3 with mTLS and modern cipher suites, and — critically — passwords are HASHED with argon2id/bcrypt, NOT encrypted. Distinct from secrets-management (stores the app secrets/keys this skill consumes) and map-privacy-data-gdpr (the legal PII/erasure obligations encryption helps satisfy).
when_to_use: You must protect sensitive data — encrypting PII/PHI/card data at rest, a per-column/field-level encryption scheme, envelope encryption with a KMS (AWS KMS/GCP KMS/Vault Transit), key rotation, choosing a cipher/mode/nonce strategy, enforcing TLS/mTLS, or hashing passwords. Distinct from secrets-management (storing and injecting the KEKs/API keys/credentials — that skill provisions the keys; this one uses them to encrypt data) and map-privacy-data-gdpr (the legal classification/erasure/residency duties that encryption and crypto-shredding help you meet).
---

## When to Use

Reach for this skill when the task is making sensitive *data* cryptographically protected — at rest, in transit, or field-by-field:

- "Encrypt SSNs / card numbers / health records / PII columns in the database"
- "Set up envelope encryption with AWS KMS / GCP KMS / Vault Transit (DEK + KEK)"
- "Rotate our encryption keys" / "we need versioned keys without re-encrypting everything"
- "Which cipher/mode — is AES-CBC okay? do we need a separate MAC? what nonce?"
- "Enforce TLS 1.3 / mutual TLS between services with modern cipher suites"
- "Are we storing passwords correctly?" (hash, don't encrypt)
- "Make a user's data unrecoverable on account deletion" (crypto-shredding)

NOT this skill:
- Storing/injecting the KEKs, API keys, DB creds, and `.env` material this skill *consumes* → secrets-management (it provisions and rotates the secrets; this skill encrypts data *with* them)
- The legal side — what counts as PII/PHI, lawful basis, right-to-erasure, data residency → map-privacy-data-gdpr (this skill is the *technical control*, e.g. crypto-shredding, that satisfies those duties)
- TLS *termination/cert issuance* at the edge proxy, ACME, SNI routing → configure-dns-tls and configure-reverse-proxy-lb (this skill covers the cipher-suite/mTLS *policy*, not cert plumbing)
- Browser security response headers (HSTS, CSP) → configure-security-headers-csp (HSTS *enforces* HTTPS; this skill is the transport crypto itself)
- Login sessions, JWT signing/verification, token rotation → auth-jwt-session (signatures/JWE are adjacent but that owns session lifecycle)
- Identifying the threats/attacker model that justify these controls → threat-model-stride
- A broad security pass over a diff → security-review (this skill is the deep crypto specialist it defers to)

## Steps

1. **Classify data first, then pick the protection tier — encryption is not the answer to everything.** Three distinct goals need three different tools:

   | Goal | Use | NEVER |
   |---|---|---|
   | Verify a credential later (passwords) | **slow password hash** (argon2id) — one-way | encrypt; never decrypt a password |
   | Protect data you must read back (PII, PHI, PAN, tokens) | **AEAD encryption** + KMS envelope | reversible "encoding", base64, ROT |
   | Integrity/origin without secrecy | HMAC-SHA-256 / signature | "encrypt to authenticate" |
   | Index/search without revealing value | HMAC-based blind index or deterministic enc | plaintext index column |

   Encrypting a password is a **bug**, not a feature: anything reversible means an attacker (or insider) with the key gets every plaintext password.

2. **Use AEAD ciphers only. Banned modes are non-negotiable.** Authenticated Encryption with Associated Data gives confidentiality *and* tamper-detection in one primitive:

   | Use this | Why |
   |---|---|
   | **AES-256-GCM** | hardware-accelerated (AES-NI), NIST-approved, ubiquitous KMS support |
   | **ChaCha20-Poly1305** | faster on CPUs without AES-NI (mobile/ARM), constant-time by design |
   | **AES-256-GCM-SIV / XChaCha20-Poly1305** | nonce-misuse-resistant / 192-bit nonce — prefer when you can't guarantee unique 96-bit nonces |

   | Banned | Why it's broken |
   |---|---|
   | **ECB** | identical plaintext blocks → identical ciphertext (the "ECB penguin"); leaks structure |
   | **CBC/CTR without a MAC** | unauthenticated → padding-oracle (CBC) & bit-flipping attacks; ciphertext is malleable |
   | **Raw RSA / RSA-PKCS#1v1.5 enc** | use RSA-OAEP, or better ECIES/hybrid; never "RSA the whole payload" |
   | DES/3DES/RC4/MD5/SHA-1 | broken/deprecated |

   Don't hand-roll "AES + separate HMAC" (encrypt-then-MAC) unless you must — get the construction order wrong and you reintroduce the oracle. Use a vetted library: **libsodium** (`crypto_aead_*` / `secretbox`), **Go** `crypto/cipher` GCM or `nacl/secretbox`, **Python** `cryptography` `AESGCM`/`ChaCha20Poly1305` (not the low-level `Cipher` API), **Java** `javax.crypto` GCM or Google **Tink**, **Rust** `aes-gcm`/`chacha20poly1305` RustCrypto crates, **Node** `crypto.createCipheriv('aes-256-gcm', …)` + `getAuthTag()`. **Tink/libsodium are the senior default** — they pick safe modes and manage nonces for you.

3. **Nonce/IV discipline: unique per (key, message), forever. This is the #1 way AEAD fails.** GCM with a **repeated nonce under the same key is catastrophic** — it leaks the XOR of plaintexts *and* the authentication key (forgery). Rules:
   - 96-bit (12-byte) nonce for GCM. Either **random** from a CSPRNG (`os.urandom`/`crypto.randomBytes`/`getrandom`) or a **monotonic counter** — never both, never `0`, never a timestamp, never reuse.
   - Random 96-bit nonces are safe only up to **~2³² messages per key** (birthday bound). High-volume? Rotate the DEK sooner, or use **XChaCha20-Poly1305 (192-bit nonce)** / **AES-GCM-SIV** which tolerate accidental reuse.
   - **Store the nonce alongside the ciphertext** (it's not secret) — typical record = `version ‖ nonce ‖ ciphertext ‖ tag`.
   - Don't derive the nonce from the plaintext or a non-unique field. Don't reuse one nonce across a re-encrypt.

4. **Bind ciphertext to its context with AAD (Associated Data).** AEAD lets you authenticate (not encrypt) extra context — pass the **row id / tenant id / column name / key version** as AAD. This stops an attacker from copying a valid ciphertext from row A into row B (ciphertext substitution): decryption of B fails because the AAD no longer matches. AAD must be reconstructible at decrypt time from the record's own metadata.

5. **Envelope encryption: a KMS-held KEK wraps per-record/per-tenant DEKs. Never encrypt bulk data directly with the KMS key.** The pattern that scales and rotates cleanly:

   ```
   1. KMS.GenerateDataKey(KeyId=KEK, KeySpec=AES_256)
        → returns { Plaintext DEK, Encrypted DEK (wrapped by KEK) }
   2. Encrypt your data locally with the plaintext DEK (AES-256-GCM, fresh nonce)
   3. Store: encrypted_dek ‖ key_version ‖ nonce ‖ ciphertext ‖ tag
   4. ZERO the plaintext DEK from memory immediately after use
   5. Decrypt: KMS.Decrypt(encrypted_dek) → plaintext DEK → local AEAD decrypt
   ```

   - **KEK** lives in **AWS KMS / GCP KMS / Azure Key Vault / Vault Transit / an HSM** and *never leaves it* — KMS does the wrap/unwrap, your app never sees KEK bytes. **DEK** is short-lived in app memory, zeroed after use.
   - Granularity: **per-tenant or per-record DEK** for crypto-shredding (delete the DEK → that data is gone). Per-row is most flexible; cache the unwrapped DEK briefly (e.g. LRU with TTL) to avoid a KMS call per row.
   - Tools: AWS **KMS** + the **AWS Encryption SDK** (handles the envelope + nonce for you), GCP **KMS**, HashiCorp **Vault Transit** (`vault write transit/encrypt/...` — Vault holds the key, returns ciphertext), or **Tink**'s `KmsEnvelopeAead`. Prefer these over rolling your own envelope.

6. **Per-field/column encryption for PII — choose deterministic vs randomized by query need.** Application-layer (encrypt before the DB sees it) beats trusting only DB-native TDE, because TDE protects the *disk file*, not a SQL-injection or a DBA reading rows.

   | Mode | Same plaintext → | Lets you | Cost |
   |---|---|---|---|
   | **Randomized** (fresh nonce) | different ciphertext | only decrypt-then-use | leaks nothing; **default for PII** |
   | **Deterministic** (synthetic IV / SIV) | same ciphertext | equality lookup, joins, unique constraint | leaks equality (which rows share a value) |

   For *searchable* encryption use a **blind index**: store `HMAC-SHA256(key, normalize(value))` in a separate indexed column and query by that, keeping the value column randomized-encrypted. Don't reach for order-preserving/fully-homomorphic encryption (leaky / impractical) unless you truly understand the tradeoff. Postgres `pgcrypto` is fine for small cases but does *application-visible* keys in SQL logs — prefer encrypting in the app. **Don't encrypt a column you need range-query or `LIKE` on** without redesigning the access pattern first.

7. **Passwords: hash with a memory-hard KDF, salted and parameterized — never encrypt, never plain SHA-256.** Use:

   | Algorithm | Params (2025 baseline) |
   |---|---|
   | **argon2id** (first choice) | m=19–64 MiB, t=2–3, p=1; OWASP min m=19 MiB,t=2,p=1 |
   | **scrypt** | N=2^17, r=8, p=1 (or N=2^15 for lighter) |
   | **bcrypt** (legacy/compat) | cost ≥ 12; **pre-hash with SHA-256 + base64** if password may exceed 72 bytes (bcrypt silently truncates) |

   - A **per-password random salt** is mandatory (the libraries generate and embed it in the encoded hash — `$argon2id$v=19$m=...`). No global "pepper-as-salt".
   - **Pepper** (optional, defense-in-depth) = a secret key *not* in the DB; either HMAC the password before hashing or keep it in a KMS/HSM. Store the pepper in secrets-management, never beside the hash.
   - **Never** use fast hashes (MD5, SHA-1, SHA-256, SHA-512) bare for passwords — GPUs do billions/sec. **Never** encrypt passwords (reversible = breach of all of them).
   - Verify in **constant time** (the KDF's `verify`/`checkpw` does this); re-hash on login if cost params have since increased.

8. **TLS in transit: 1.2 minimum, 1.3 preferred; modern cipher suites; mTLS for service-to-service.**
   - **Versions:** disable SSLv3/TLS 1.0/1.1 entirely. Allow **TLS 1.2 + 1.3**; prefer 1.3 (1-RTT, AEAD-only, forward-secret by construction).
   - **TLS 1.2 cipher suites** (AEAD + ECDHE forward secrecy only): `ECDHE-ECDSA-AES128-GCM-SHA256`, `ECDHE-RSA-AES256-GCM-SHA384`, `ECDHE-*-CHACHA20-POLY1305`. **No** CBC suites, no static RSA key exchange, no `NULL`/`RC4`/`3DES`/`EXPORT`. TLS 1.3 only offers AEAD suites, so the choice is made for you.
   - Mozilla SSL Config "**Intermediate**" is the safe default; "Modern" = TLS 1.3-only. Verify with **`testssl.sh`** or SSL Labs (target **A/A+**). Enable **HSTS** at the edge (handoff to configure-security-headers-csp).
   - **mTLS** for internal/service-to-service: both sides present certs; pin to your CA, short-lived certs (SPIFFE/SVID, Istio, Linkerd, or a service-mesh issuer). Validate the **full chain + SAN**, not just "a cert was presented."
   - **Never disable cert verification** (`verify=False`, `rejectUnauthorized:false`, `InsecureSkipVerify:true`) outside a throwaway test — it silently turns TLS into plaintext-to-anyone.

9. **Key rotation with versioned keys — rotate the KEK cheaply, re-wrap DEKs, lazy-re-encrypt data.** Store a **`key_version`** with every ciphertext so multiple key generations coexist:
   - **KEK rotation** (cheapest, do on schedule, e.g. annually or per policy): KMS rotates the KEK; you **re-wrap each DEK** (decrypt-unwrap with old, wrap with new). Bulk data is *untouched* — that's the whole point of envelope encryption.
   - **DEK rotation:** generate a new DEK, **re-encrypt the affected records lazily** (on next write, or a background backfill) and bump `key_version`. Keep old key versions readable until backfill completes, then retire.
   - **On compromise:** rotate immediately and force re-encryption; **crypto-shred** by destroying a DEK to make its data permanently unrecoverable (the GDPR-erasure trick — handoff to map-privacy-data-gdpr).
   - Decrypt path must **dispatch on the stored `key_version`**; never assume "current key." Keep a registry of retired versions for audit.

10. **Operational hygiene — the parts that get forgotten.** Generate all keys/nonces/salts from a **CSPRNG** (`os.urandom`, `crypto.randomBytes`, `getrandom(2)`, `SecureRandom`) — never `Math.random`/`rand()`/`mt19937`. **Zero plaintext keys** from memory after use where the language allows (Go `defer` wipe, Rust `zeroize`, libsodium `sodium_memzero`). Don't log plaintext, keys, or full ciphertext. Encrypt **backups and replicas** too (same KMS). Use **constant-time comparison** for MACs/tags/tokens (`hmac.compare_digest`, `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`) — `==` leaks via timing. Run a **`security-review`** over the crypto diff before shipping.

## Common Errors

- **Encrypting passwords instead of hashing.** Reversible = one key compromise dumps every password. Fix: argon2id/bcrypt, one-way (step 7).
- **Plain/fast hash for passwords** (`SHA256(password)`, unsalted MD5). GPUs crack billions/sec; rainbow tables for unsalted. Fix: memory-hard KDF with per-password salt.
- **ECB mode / unauthenticated CBC.** ECB leaks structure; CBC-without-MAC → padding oracle, malleable ciphertext. Fix: AEAD (AES-GCM/ChaCha20-Poly1305) only.
- **Nonce/IV reuse under one key (GCM).** Catastrophic — leaks plaintext XOR *and* the auth key (forgeries). Fix: unique nonce per message; XChaCha20/GCM-SIV if you can't guarantee it (step 3).
- **Hardcoded / static IV** (`iv = new byte[12]` all zeros). Same as reuse. Fix: fresh CSPRNG nonce per encryption, stored with ciphertext.
- **Encrypting bulk data directly with the KMS/KEK.** Throughput and cost explode; no clean rotation. Fix: envelope — KEK wraps per-record DEK (step 5).
- **No AAD binding.** Valid ciphertext copy-pasted between rows/tenants decrypts fine. Fix: pass row/tenant/version as AAD (step 4).
- **No key version on ciphertext.** Rotation becomes a flag-day re-encrypt-everything. Fix: store `key_version`, dispatch decryption on it (step 9).
- **Plaintext DEK left in memory / logged.** Heap dump or log leak = game over. Fix: zero after use; never log keys/plaintext/tags.
- **`Math.random()` / `rand()` for keys, nonces, or salts.** Predictable → forgeable. Fix: CSPRNG only.
- **Disabling TLS verification** (`verify=False`, `InsecureSkipVerify`, `rejectUnauthorized:false`). Silent MITM. Fix: validate chain + SAN; only bypass in isolated tests.
- **Weak TLS** (TLS 1.0/1.1, CBC suites, static RSA, RC4/3DES). Fix: TLS 1.2+/1.3, AEAD+ECDHE suites; verify with testssl.sh.
- **`==` on MACs/tags/tokens.** Timing side-channel. Fix: constant-time comparison.
- **Roll-your-own crypto / `Cipher` low-level API.** Easy to misorder encrypt-then-MAC, mishandle padding. Fix: libsodium / Tink / AWS Encryption SDK.
- **Deterministic encryption on high-cardinality PII you didn't mean to.** Leaks equality patterns. Fix: randomized by default; deterministic/blind-index only where a query needs it (step 6).

## Verify

1. **No banned modes/algorithms:** grep the diff for `ECB`, `AES/CBC` without an accompanying MAC, `DES`, `RC4`, `MD5`/`SHA1` on secrets, raw RSA encrypt — zero hits. All symmetric encryption is AES-GCM / ChaCha20-Poly1305 (AEAD).
2. **Passwords are hashed, not encrypted:** grep finds argon2id/bcrypt/scrypt on the password path and **no** encrypt/decrypt of passwords; salts are per-password (encoded in the hash); cost params meet the step-7 baseline.
3. **Nonce uniqueness:** confirm every encryption draws a fresh CSPRNG nonce (or a guaranteed-unique counter); no static/zero IV; nonce stored with ciphertext. For high volume, DEK rotation or a nonce-misuse-resistant mode is in place.
4. **Envelope encryption holds:** bulk data is encrypted with a DEK, the DEK is wrapped by a KMS-held KEK that never leaves KMS, plaintext DEK is zeroed after use, and a `key_version` is stored per record.
5. **AAD binds context:** moving a valid ciphertext from one row/tenant to another **fails** decryption (AAD mismatch).
6. **Rotation works without re-encrypting everything:** rotating the KEK re-wraps DEKs only; old `key_version` ciphertext still decrypts; a DEK-destroy crypto-shreds its records (they become permanently undecryptable).
7. **TLS posture:** `testssl.sh <host>` / SSL Labs returns **A/A+** — TLS 1.2+ only, AEAD+forward-secret suites, no CBC/RC4/3DES; mTLS validates the full chain + SAN; no `verify=False`/`InsecureSkipVerify` in non-test code.
8. **Randomness + timing:** all keys/nonces/salts come from a CSPRNG (no `Math.random`/`rand`); MAC/tag/token comparisons are constant-time.
9. **Tamper detection:** flipping one ciphertext byte makes decryption **fail** (auth tag rejects it) rather than returning garbage plaintext.

Done = sensitive data is encrypted with AEAD under unique nonces, bulk data uses KMS envelope encryption with versioned, rotatable keys and context-binding AAD, passwords are hashed with argon2id/bcrypt (never encrypted), PII fields are randomized-encrypted (deterministic/blind-index only where a query demands it), transport is TLS 1.2+/1.3 with modern suites and mTLS where needed, and all keys/nonces/salts come from a CSPRNG with constant-time tag checks — all proven by checks 1–9, with `security-review` run over the crypto diff.
