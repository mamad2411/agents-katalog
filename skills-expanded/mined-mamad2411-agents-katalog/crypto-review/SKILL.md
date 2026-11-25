---
name: crypto-review
description: Review a cryptography choice — encryption at rest/in transit, key management + rotation, algorithm/mode selection, and common foot-guns (IV reuse, ECB, home-rolled crypto).
---

# crypto-review

> Don't invent crypto, and don't configure it from a blog post. Use vetted primitives at safe defaults, and put the hard problem — key management — at the center, not the algorithm.

## When to use

- Choosing or reviewing how data is encrypted, signed, hashed, or how keys are managed.
- A design mentions encryption and you need to confirm it's not subtly broken.
- A workflow invokes `polymath-security:crypto-review`.

Not this when: you are designing auth tokens/sessions (`auth-design`) or doing a general code review (`owasp-review`). This focuses on the cryptographic choices and key lifecycle.

## Inputs

- What's being protected (data at rest, in transit, secrets, passwords), against whom, and any compliance requirement.

## Procedure

1. **Encryption in transit**: TLS 1.2+ (prefer 1.3), strong cipher suites, valid certs with rotation/automation, HSTS; mTLS for service-to-service where warranted. No plaintext internal hops "because it's internal".
2. **Encryption at rest**: use authenticated encryption (AES-GCM or ChaCha20-Poly1305); never ECB; never reuse a nonce/IV with the same key; envelope-encrypt with a KMS-managed data key.
3. **Key management — the core**: keys in a KMS/HSM, never in code/config/repo; separate keys per purpose/environment; define rotation cadence and how rotation re-wraps data; least-privilege key access; audit key use. Most "encryption" failures are key-handling failures.
4. **Hashing & passwords**: passwords with a memory-hard KDF (argon2id/scrypt/bcrypt) + per-user salt — never fast hashes (MD5/SHA-1/unsalted SHA-256). Integrity with SHA-256+/HMAC.
5. **Randomness**: cryptographically secure RNG for keys/tokens/IVs/salts — never `rand()`/`Math.random`.
6. **Signatures/certs** where authenticity matters; pin algorithms; reject downgrade.
7. **Flag the foot-guns**: home-rolled crypto, deprecated algorithms (DES/RC4/MD5/SHA-1), ECB mode, static IVs, hardcoded keys, missing rotation, secrets in logs.
8. **Crypto-agility**: version the scheme so an algorithm can be retired without a data-loss event.

## Output

- A one-page review: in-transit + at-rest schemes (algorithm/mode), the key-management lifecycle (storage, separation, rotation, access), password/hashing approach, RNG check, the foot-gun findings, and a crypto-agility note.

## Quality bar

- Only vetted primitives at safe defaults; authenticated encryption for data at rest; no ECB / nonce reuse.
- Keys live in a KMS/HSM with stated rotation and least-privilege access — never in the repo.
- Passwords use a memory-hard salted KDF; CSPRNG used for all secrets/IVs.
- Deprecated algorithms and home-rolled crypto are flagged.
