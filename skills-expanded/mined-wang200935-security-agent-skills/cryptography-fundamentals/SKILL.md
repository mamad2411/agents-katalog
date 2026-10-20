---
name: cryptography-fundamentals
description: Build and maintain deep cryptography knowledge for Hermes, covering foundations,
  primitives, protocols, standards, post-quantum migration, and applied engineering
  checklists. Use when the user asks about cryptography, encryption, signatures, key
  exchange, TLS, password hashing, PKI, zero-knowledge, MPC, homomorphic encryption,
  or post-quantum crypto, or when Hermes should deepen and solidify cryptography knowledge
  into reusable notes.
version: 1.5.0
license: MIT
metadata:
  hermes_origin: import
tags:
- cryptography
- security
- encryption
- signatures
- pki
- pqc
- protocols
related_skills: []
---

# Cryptography

## Overview

Use this skill to answer cryptography questions rigorously and to keep Hermes' cryptography knowledge durable instead of ad hoc. The skill turns broad crypto requests into a structured workflow: classify the problem, anchor on authoritative standards and textbooks, explain the security goal and threat model, and distinguish mathematical soundness from engineering safety.

This skill is for *real cryptography*, not vague "military-grade encryption" language. It prefers precise statements like confidentiality, integrity, authenticity, key establishment, forward secrecy, misuse resistance, side-channel resistance, and post-quantum migration readiness.

## When to Use

Use this skill when the user asks about:
- symmetric encryption, AEAD, MACs, hashes, KDFs, RNGs
- public-key encryption, signatures, PKI, certificates, key exchange
- TLS, JOSE/JWT/JWE/JWS, password storage, secret management
- elliptic-curve crypto, lattice crypto, hash-based signatures
- zero-knowledge, threshold crypto, MPC, FHE/HE
- long-term crypto knowledge-base expansion and standards-anchored research curation
- cryptographic standards selection, algorithm migration, or crypto review
- post-quantum cryptography and transition planning
- building or solidifying long-term cryptography knowledge inside Hermes

Do not use this skill for purely legal/policy crypto questions unless technical mechanism selection is involved.

## Core Principle

Always answer crypto questions in this order:
1. **Goal** — what property is required: confidentiality, integrity, authenticity, non-repudiation, key establishment, privacy, anonymity, verifiability, or availability?
2. **Threat model** — attacker capabilities, deployment constraints, data lifetime, performance, hardware assumptions.
3. **Primitive/protocol class** — AEAD vs signature vs KEM vs PAKE vs ZK proof, etc.
4. **Standard/authority** — NIST, RFC/IETF, CFRG, textbook, or well-established library guidance.
5. **Engineering risks** — key lifecycle, randomness, nonce reuse, side channels, downgrade risks, metadata leakage, implementation maturity.

## Fast Taxonomy

### 1. Secret-key primitives
- **Block ciphers**: AES
- **Stream ciphers**: ChaCha20
- **Authenticated encryption**: AES-GCM, ChaCha20-Poly1305, AES-GCM-SIV, XChaCha20-Poly1305
- **MACs**: HMAC, CMAC, Poly1305
- **Hashes/XOFs**: SHA-2, SHA-3, SHAKE, BLAKE2/3
- **KDFs**: HKDF, scrypt, Argon2, PBKDF2
- **RNG/DRBG**: system CSPRNG, NIST DRBG families

### 2. Public-key primitives
- **Key establishment**: (EC)DH, X25519/X448, ML-KEM
- **Encryption/KEM**: RSA-OAEP, ECIES-family, HPKE, ML-KEM
- **Signatures**: Ed25519/Ed448, ECDSA, RSA-PSS, ML-DSA, SLH-DSA
- **PKI**: X.509, certificate validation, revocation, trust stores

### 3. Advanced cryptography
- **ZK**: Sigma protocols, SNARKs, STARKs, Bulletproofs
- **Threshold / MPC**: DKG, threshold signatures, garbled circuits, secret sharing
- **Privacy tech**: PIR, anonymous credentials, mixnets, group signatures
- **Homomorphic encryption**: Paillier, BFV, BGV, CKKS, TFHE

## Recommended Canon by Priority

Read and cite from these first:
1. **Boneh & Shoup, _A Graduate Course in Applied Cryptography_** — broad modern foundation; browser-verified table of contents includes secret-key crypto, public-key crypto, signatures, elliptic curves, lattice/post-quantum crypto, zero-knowledge, AKE, threshold crypto, and MPC.
2. **NIST Cryptographic Standards and Guidelines** — standards hub covering block ciphers, signatures, hashes, key management, randomness, lightweight crypto, threshold crypto, privacy-enhancing crypto, and post-quantum crypto.
3. **NIST SP 800-175B Rev.1** — high-level mechanism-selection guidance for using cryptographic standards.
4. **NIST PQC standards (2024)**:
   - **FIPS 203** — ML-KEM
   - **FIPS 204** — ML-DSA
   - **FIPS 205** — SLH-DSA
5. **Core protocol RFCs** — TLS 1.3 and related RFCs when protocol-level guidance is needed.

Detailed study notes live in the reference files bundled with this skill.

## Default Research Workflow

When deepening Hermes knowledge on any crypto topic:

1. **Classify the topic** using the taxonomy above.
2. **Anchor on authority**:
   - theory → Boneh & Shoup
   - U.S. standards / implementation guidance → NIST
   - Internet protocol behavior → RFC / IETF / CFRG
3. **Capture exact claims** with publication name, year, and what it standardizes.
4. **Separate levels**:
   - primitive security claim
   - protocol composition claim
   - operational deployment guidance
5. **Write reusable notes**, not one-off answers. Prefer:
   - definition
   - what problem it solves
   - what it does *not* solve
   - standard choices
   - failure modes / misuse traps
   - migration / interoperability notes
6. **If comparing algorithms**, score along:
   - security assumption
   - quantum vulnerability
   - misuse resistance
   - performance / ciphertext size / key size
   - standardization status
   - library maturity
7. **If giving implementation guidance**, always recommend vetted libraries and protocols over custom crypto.
8. **When possible, prove behavior with runnable labs** in `references/practical-labs.md` and the bundled `scripts/` tools instead of only describing expected outcomes.
9. **For protocol or product reviews**, load `references/modern-protocol-design.md` and `references/key-management-and-secrets.md`, then run `scripts/crypto_design_review.py` on any available design text to catch common red flags before writing the final assessment.

## Default Applied Guidance

### For data in transit
- Prefer **TLS 1.3** with modern library defaults.
- Avoid inventing new secure-channel protocols.

### For application payload encryption
- Prefer **AEAD**.
- Default shortlist: **AES-256-GCM**, **ChaCha20-Poly1305**.
- Consider misuse-resistant variants like **AES-GCM-SIV** when nonce management is risky.

### For password storage
- Prefer **Argon2id**.
- Accept **scrypt** if Argon2id unavailable.
- Use **PBKDF2** mainly for compatibility constraints, not as first choice.

### For signatures
- Prefer protocol/ecosystem defaults.
- Modern app-level default shortlist: **Ed25519** or **RSA-PSS** depending on interoperability requirements.
- For PQ migration, track **ML-DSA** and hybrid deployments.

### For key agreement / KEM
- Current default shortlist: **X25519** for classical ecosystems, **ML-KEM** for PQ migration planning, often in **hybrid** combinations during transition.

### For randomness
- Use OS CSPRNGs.
- Never design your own RNG.

## Common Crypto Review Questions

When reviewing a design, explicitly answer:
- What are the assets and attacker goals?
- Are confidentiality and authenticity both required?
- Is nonce uniqueness guaranteed?
- How are keys generated, stored, rotated, revoked, and destroyed?
- Is the design relying on unauthenticated encryption anywhere?
- Does metadata remain exposed even if payload is encrypted?
- Are passwords hashed with a memory-hard KDF?
- Are certificates and hostnames validated correctly?
- Is there a post-quantum migration requirement due to long-lived secrets or harvest-now-decrypt-later risk?
- Is any custom cryptographic construction being proposed that should be rejected in favor of standards?

## Common Pitfalls

1. **Confusing encryption with authentication.** Encryption alone does not prove who sent the message or whether it was modified.
2. **Using raw primitives directly.** Prefer complete constructions/protocols like AEAD, HPKE, TLS, age, Signal, libsodium sealed boxes.
3. **Nonce/IV misuse.** Reuse can catastrophically break schemes like GCM.
4. **Weak password storage.** Fast hashes like SHA-256 are not password hash functions.
5. **Rolling custom crypto.** Novel constructions are almost always a red flag.
6. **Ignoring side channels and key lifecycle.** Sound math is not enough.
7. **Treating PQC as optional for long-lived secrets.** Harvest-now-decrypt-later matters.
8. **Using cryptography to solve authorization problems.** Crypto protects data; it does not replace access-control design.

## Reference Files

- `references/core-canon.md` — authoritative study canon and reading order
- `references/topic-map.md` — concept graph / roadmap of the field
- `references/pqc-and-standards.md` — NIST standards snapshot and migration view
- `references/applied-checklists.md` — practical selection and review checklists
- `references/standards-and-protocol-anchors.md` — browser/terminal-verified standards and RFC anchors for applied crypto answers
- `references/domain-deep-dives.md` — durable topic coverage across encryption, PKI, password hashing, ZK, MPC, HE, and migration
- `references/advanced-comparison-maps.md` — decision tables for ZK, MPC, threshold crypto, HE, and PQ transition tradeoffs
- `references/crypto-engineering-playbooks.md` — reusable applied playbooks for password storage, PKI review, protocol composition, PQ migration, and privacy tech selection
- `references/modern-protocol-design.md` — protocol design hierarchy, composition rules, HPKE/TLS guidance, replay resistance, and review template
- `references/key-management-and-secrets.md` — key lifecycle, envelope encryption, multi-tenant keying, secret storage, JWT/JWKS pitfalls, and incident response questions
- `references/practical-labs.md` — executable local labs for AEAD, signatures (Ed25519 + RSA-PSS), HKDF, password KDF (scrypt + Argon2id), X25519 key exchange, certificate-chain validation, and HPKE-style composition
- `references/research-program.md` — ongoing agenda for continuously deepening Hermes cryptography knowledge

## Scripts

- `scripts/crypto_design_review.py` — lightweight text scanner for crypto-design smells such as ECB/CBC-without-MAC, raw RSA, SHA password hashing, naive MACs, weak RNGs, and JWT validation pitfalls

## Verification Checklist

- [ ] Identified the exact security property needed
- [ ] Named the primitive/protocol class correctly
- [ ] Anchored advice to a standard, RFC, or textbook
- [ ] Distinguished theory from deployment guidance
- [ ] Called out misuse and side-channel risks
- [ ] Avoided recommending custom cryptography unless the task is research
