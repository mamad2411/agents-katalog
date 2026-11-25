---
name: crypto-key-management
description: "Covers cryptography and key management: choosing algorithms (the 2026 floor), PKI and certificates, HSM/KMS, secrets management, and the post-quantum migration (ML-KEM/ML-DSA). Use when the user asks which cipher, hash or key size to use, how to run a PKI or rotate certificates, HSM vs cloud KMS, where to store secrets, crypto-agility, or how to plan a PQC migration."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Cryptography & key management

You rarely implement crypto; you make decisions about it. The failures are never
the math; they're key management, stale algorithms, and rolled-your-own.

## Use, don't invent

- Never design a primitive or a protocol. Use vetted libraries (libsodium, the
  platform's TLS, AWS/GCP/Azure KMS) and standard protocols (TLS 1.3, SSH,
  Signal/MLS). "We wrote our own encryption" is a finding: `report_finding` it.
- Prefer authenticated encryption (AES-GCM, ChaCha20-Poly1305). Encrypt-then-MAC
  only if you must compose; never MAC-then-encrypt or unauthenticated CBC.

## Current algorithm floor (2026)

- Symmetric: **AES-128+ or ChaCha20** (AES-256 for long-life/regulated data).
- Hash: **SHA-256+ / SHA-3**. MD5 and SHA-1 are dead: flag any use.
- Asymmetric (classical): **RSA-3072+** or **ECC P-256/Ed25519**.
- KDF/passwords: **Argon2id** (or scrypt/bcrypt); PBKDF2 only for compat. Never
  a bare hash for passwords (fast hashes fall to GPU cracking).
- TLS: **1.3** preferred, 1.2 floor; disable everything below.
- **APAC pitfall (national crypto):** the AES/RSA/ECC floor above is a Western default.
  **China**'s Commercial Cryptography regime mandates the national **SM2/SM3/SM4/SM9**
  algorithms and **OSCCA/SCA-approved** products for in-country government and many
  regulated systems; foreign crypto faces import/approval limits. Crypto-agility (below)
  is exactly what lets you slot in an SM profile for a China deployment without a rebuild.

## Post-quantum (the live migration: verify, this moves)

- NIST finalized the first PQC standards in Aug 2024: **FIPS 203 (ML-KEM /
  Kyber)** for key exchange, **FIPS 204 (ML-DSA / Dilithium)** and **FIPS 205
  (SLH-DSA / SPHINCS+)** for signatures; **HQC** selected (Mar 2025) as a KEM
  backup and **Falcon (FN-DSA)** as a signature; both still "underway" at NIST
  with no draft FIPS published as of Nov 2026. verify: https://csrc.nist.gov/projects/post-quantum-cryptography
- Migration deadline is set: NIST's transition roadmap (**IR 8547**, final
  27 Oct 2026) deprecates quantum-vulnerable RSA/ECC/DH **after 2030** and
  disallows them **after 2035**; that's the planning horizon for the inventory
  below. US federal
  high-value/high-impact systems move sooner (EO 14412, Jun 2026): PQC key
  establishment by **end-2030**, PQC signatures by **end-2031**.
  verify: https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf
- Threat is **harvest-now-decrypt-later**: long-lived secrets are at risk today.
- Act now: build a **crypto inventory** (where keys/algorithms live), demand
  **crypto-agility** (algorithms swappable, not hard-coded), and deploy **hybrid**
  key exchange (classical + ML-KEM) for data that must stay secret for years.

## Key management (where it actually breaks)

- **Hierarchy:** a root/key-encryption-key protects data-encryption-keys; only
  the KEK lives in the HSM/KMS, DEKs are wrapped (envelope encryption).
- **HSM / KMS:** keep key material in an HSM (on-prem) or cloud KMS; the
  application gets encrypt/decrypt operations, never the raw key. FIPS 140-3
  validation where required.
- **Rotation:** rotate on a schedule and on suspected compromise; design so
  rotation doesn't require re-encrypting everything (rotate the KEK, not every
  DEK). Keep old keys for decrypt-only until data is re-wrapped.
- **Separation of duties:** the people who manage keys ≠ the people who access
  the data. Log every key use (it feeds `load_skill siem-soar`).

## PKI & certificates

- Internal PKI: protect the offline root, issue from intermediates, publish
  CRL/OCSP. Short-lived certs + automation (ACME) beat long-lived + manual.
- **Certificate lifecycle is an outage source**: inventory and auto-renew;
  expired certs cause more downtime than attacks. The CA/Browser Forum schedule
  (ballot SC-081v3) is now in force: public TLS max lifetime **200 days since
  Mar 2026**, 100 days Mar 2027, **47 days Mar 2029**: automate or bleed. verify:
  https://www.cabforum.org/
- mTLS for service-to-service; tie identity to the cert (see `load_skill iam`).

## Secrets management

- No secrets in code, env files, images, or git. Detect leaks with gitleaks /
  trufflehog; if one ships, **rotate it**; masking isn't remediation.
- Use a secrets manager (Vault, cloud secret stores) with short-lived/dynamic
  secrets and tight access policies. Pairs with `load_skill devsecops`.

## Report

- `report_finding` for: weak/deprecated algorithms, hardcoded keys/secrets,
  unauthenticated encryption, missing rotation, self-rolled crypto, no PQC plan
  for long-life data. Map to CWE-327/328/320 and `load_skill control-mapping`.
