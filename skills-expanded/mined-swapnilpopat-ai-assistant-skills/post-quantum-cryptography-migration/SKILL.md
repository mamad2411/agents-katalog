---
name: post-quantum-cryptography-migration
description: Plan and execute the migration from classical public-key cryptography (RSA, ECDSA, ECDH, DH) to NIST-standardized post-quantum algorithms (FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA, draft FIPS 206 FN-DSA), defending against harvest-now-decrypt-later (HNDL) attacks and meeting CNSA 2.0, BSI, ANSSI, and EU CRA expectations. Use when inventorying cryptographic dependencies, selecting hybrid schemes, building a crypto-agility layer, or estimating PQC migration effort.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Post-Quantum Cryptography Migration

Plan and execute a defensible transition from classical asymmetric cryptography to NIST-standardized post-quantum algorithms before a cryptographically relevant quantum computer (CRQC) — or, more urgently, before the data you transmit today is decrypted in 5–15 years by an adversary already storing it.

## Context

You are a senior cryptography engineer guiding $ARGUMENTS through PQC migration. NIST finalized the first three standards in August 2024 (FIPS 203, 204, 205) and a fourth (FIPS 206 / FN-DSA) in 2026; the US NSA's CNSA 2.0 mandates PQC for National Security Systems on a 2025–2033 timeline; CISA, NSA, and NIST jointly published the *Quantum-Readiness* roadmap urging every organization to start with a cryptographic inventory now. The threat is asymmetric and immediate: any TLS, VPN, S/MIME, code-signing, or document-encryption traffic an adversary captures today can be decrypted later if it relied on RSA / ECDH for key establishment — this is the **Harvest Now, Decrypt Later (HNDL)** attack.

## Domain Context

- **NIST PQC standards (finalized 2024–2026)**:
  - **FIPS 203 — ML-KEM** (Module-Lattice Key Encapsulation, ex-Kyber). Replaces RSA-OAEP / ECDH for key establishment. Parameter sets: ML-KEM-512 / 768 / 1024.
  - **FIPS 204 — ML-DSA** (Module-Lattice Digital Signatures, ex-Dilithium). General-purpose signature replacement for RSA / ECDSA. Parameter sets: ML-DSA-44 / 65 / 87.
  - **FIPS 205 — SLH-DSA** (Stateless Hash-Based Signatures, ex-SPHINCS+). Conservative, hash-only signatures — large but the safest long-term bet for code/firmware signing. SHA2/SHAKE × small/fast variants.
  - **FIPS 206 — FN-DSA** (FFT over NTRU lattices, ex-Falcon). Compact lattice signatures; trickier to implement safely (floating-point side channels).
  - **HQC** — selected March 2025 as a code-based KEM backup to ML-KEM (different mathematical assumption).
- **Stateful hash-based signatures (already standardized)**: **LMS** (NIST SP 800-208), **XMSS** (RFC 8391) — usable today for firmware signing where state can be managed.
- **CNSA 2.0 (US NSA, 2022 → enforced 2033)**: ML-KEM-1024, ML-DSA-87, SLH-DSA-256, AES-256, SHA-384/512. Software/firmware signing must be PQC by **2025**; new equipment by **2027**; full transition by **2033**.
- **Hybrid schemes**: combine a classical and a post-quantum primitive so a break in either one is not fatal during transition. **TLS 1.3 hybrid KEM**: `X25519MLKEM768` (IETF draft `draft-kwiatkowski-tls-ecdhe-mlkem`, deployed by Cloudflare, Google, Apple, AWS in 2024–2025). **Hybrid signatures**: composite (concatenated) or chained per IETF `draft-ietf-lamps-pq-composite-sigs`.
- **HNDL — Harvest Now, Decrypt Later**: nation-state adversaries are widely assumed to be storing encrypted internet traffic now. Anything encrypted today with RSA-2048 / P-256 ECDH and required to remain confidential past ~2035 is already at risk.
- **Crypto-agility**: software architecture property — algorithms can be swapped per-protocol-version, per-tenant, or per-policy without code rewrites.
- **Cryptographic Bill of Materials (CBOM)**: CycloneDX 1.6 extension cataloguing cryptographic primitives, key sizes, certificates, and protocols in your stack.

## Stack Baseline (2026)

| Layer | Recommended |
| --- | --- |
| TLS | OpenSSL 3.5 (native ML-KEM hybrid), BoringSSL, rustls 0.23+, Go 1.24 (`X25519MLKEM768` default in 1.24) |
| TLS hybrid KEM | `X25519MLKEM768` (Cloudflare / Chrome / Edge default 2025) |
| SSH | OpenSSH 9.9+ (`mlkem768x25519-sha256` default 2026) |
| VPN | WireGuard PQ wrappers, IPsec via IKEv2 hybrid (RFC 9370), OpenVPN PQC plugins |
| PKI / certificates | Composite ML-DSA + ECDSA certs (IETF draft, supported by EJBCA 8+, smallstep, AWS Private CA roadmap) |
| Code / firmware signing | SLH-DSA (long-term assets) or LMS/XMSS (existing stateful HSMs); cosign roadmap PQC 2026 |
| Document encryption | S/MIME 4.x with ML-KEM (LAMPS WG drafts), age PQC fork |
| HSM / KMS | Thales Luna 7+, Entrust nShield 13+, AWS KMS hybrid roadmap, GCP Cloud HSM, Azure Managed HSM PQC preview |
| Library | liboqs / Open Quantum Safe (research / interop), `pqcrypto` (Rust), BouncyCastle 1.79+ (Java), Cryptography 44+ (Python via Rust backend) |
| CBOM tooling | CycloneDX 1.6 CBOM, `cbomkit` (IBM), `pqc-scanner` |

## When to Use This Skill

- Producing the **cryptographic inventory** required by NSM-10 / CNSA 2.0 / NIS2 / EU CRA
- Designing a new protocol, API, signing system, or PKI that must remain secure for 10+ years
- Evaluating whether to enable hybrid TLS in front-of-house load balancers or an internal mTLS mesh
- Choosing between ML-DSA, SLH-DSA, and (eventually) FN-DSA for a signing use-case
- Briefing leadership on PQC migration cost, risk, and timeline
- Responding to a customer security questionnaire asking about quantum-readiness

## Prerequisites

1. **Asset inventory**: every system that uses, generates, or verifies asymmetric keys (TLS endpoints, VPNs, SSH bastions, PKI CAs, code-signing pipelines, S/MIME, JWT issuers, document encryption, blockchain wallets, IoT device identity)
2. **Data-lifetime classification**: for each encrypted channel/dataset, how long must it remain confidential? > ~10 years → high HNDL exposure
3. **Vendor / platform map**: which crypto is *yours* to swap, and which is provided by browsers, OSes, HSMs, cloud KMS, third-party SaaS — a vendor-pressure list
4. **Compliance drivers**: CNSA 2.0 deadlines (if US gov / DoD adjacent), CRA, NIS2, sector-specific (finance, health, telecom)
5. **Performance budget**: ML-KEM is comparable to ECDH; ML-DSA signatures and public keys are 2–10× larger than ECDSA — measure real impact in TLS handshake size, JWT length, certificate chain growth

## Instructions

### 1. Build the Cryptographic Bill of Materials (CBOM)

Discover every use of asymmetric crypto. Sources:

- Source code scan: `cbomkit`, `pqc-scanner`, `semgrep` rules for `RSA`, `ECDSA`, `Ed25519`, `DH`, `crypto/rsa`, `org.bouncycastle.crypto.RSAEngine`, etc.
- Network scan of TLS endpoints: `testssl.sh`, `tlsx`, `qualys SSL Labs` (records cipher suites + key sizes)
- Certificate inventory: pull from ACM, Let's Encrypt, internal CA, mTLS service mesh — record signature algorithm and key type
- HSM / KMS inventory: AWS KMS keys, GCP KMS, Azure Key Vault, on-prem HSMs — list `KeyUsage`, `KeySpec`
- Code-signing identities: Authenticode certs, Apple notarization keys, GPG keys, Sigstore Fulcio root, container signing keys
- Protocols in use: TLS, SSH, IPsec, S/MIME, SAML/JWT, OIDC, JWS, COSE, mTLS, WireGuard, OpenPGP

Output: a CycloneDX 1.6 CBOM JSON listing each primitive, where used, owner, data-lifetime, and HNDL exposure rating.

### 2. Triage by HNDL exposure and CNSA 2.0 deadline

Priority 1 (act in 2026):

- Long-lived confidential data flowing over TLS (financial, health, defense, M&A, source code, customer PII with > 10-year retention)
- Code-signing / firmware-signing root keys (whatever you sign now must be verifiable by quantum-era clients)
- Root and intermediate CAs you control (cert lifetimes 10–25 years)

Priority 2 (2027–2028):

- Authentication signatures (JWTs, SAML, mTLS) — not HNDL-vulnerable but CNSA mandates
- VPN / IPsec
- Document encryption and S/MIME

Priority 3 (when downstream support catches up):

- Constrained IoT devices (memory / power constraints — wait for ML-KEM-512 / SLH-DSA-128f optimizations)
- Blockchain / wallet signing (ecosystem-wide change required)

### 3. Choose algorithms per use-case

| Use case | Recommended PQC | Notes |
| --- | --- | --- |
| Key establishment in TLS / VPN / mTLS | ML-KEM-768 (or -1024 for CNSA 2.0) | Use **hybrid** `X25519MLKEM768` during transition |
| General-purpose signatures | ML-DSA-65 (or -87 for CNSA 2.0) | Composite with ECDSA P-256 / P-384 during transition |
| Code & firmware signing (long-lived) | SLH-DSA (SHA2-128s/192s/256s) | Larger sigs, slower, but most conservative — break only if SHA-256 breaks |
| Existing stateful HSM firmware signing | LMS or XMSS | Already standardized (NIST SP 800-208); state must be managed |
| Compact signatures (constrained or bandwidth-limited) | FN-DSA (FIPS 206) | Once FIPS 206 finalised; implement only with vetted constant-time libraries |
| Backup KEM (algorithm diversity) | HQC (NIST 2025 selection) | Different math from ML-KEM; use as second choice in dual-KEM designs |

Avoid: **non-standardized** PQC (anything not in the NIST FIPS series or LMS/XMSS) for production-confidentiality use. Research libraries (liboqs) are appropriate for interop testing only.

### 4. Build a crypto-agility layer

Refactor so algorithm choice is configuration, not code:

- **Protocol negotiation**: TLS 1.3 already negotiates; ensure your stack accepts new groups via config, not recompile
- **Application-layer crypto**: introduce an interface (`Signer`, `KemEncapsulator`, `Verifier`) implemented by a `crypto-suite` config object naming the algorithm; never hard-code RSA/ECDSA in business code
- **Multi-algorithm certificates**: composite (concatenated) certs allow simultaneous classical + PQ signatures during transition; consumers verify whichever they support
- **Key-rotation runbooks**: every key has a documented rotation procedure including algorithm change, dual-use overlap, and revocation
- **CBOM-as-code**: regenerate CBOM in CI; alert on regressions (a developer adding a fresh `RSA.generate(2048)` should fail the build)

### 5. Roll out hybrid TLS first

Lowest-risk win — no migration cost for clients that don't support PQC, immediate HNDL protection for those that do.

```nginx
# OpenSSL 3.5 / nginx 1.27+
ssl_conf_command Groups X25519MLKEM768:X25519:secp256r1;
ssl_protocols TLSv1.3;
```

```go
// Go 1.24+ — X25519MLKEM768 is in the default group list
import "crypto/tls"
cfg := &tls.Config{
    MinVersion:   tls.VersionTLS13,
    CurvePreferences: []tls.CurveID{tls.X25519MLKEM768, tls.X25519, tls.CurveP256},
}
```

Validate with `openssl s_client -connect host:443 -groups X25519MLKEM768 -tls1_3` and watch for `Negotiated TLS1.3 group: X25519MLKEM768`.

Measure: handshake size grows by ~1.1 KB; CDN edge POPs and most modern browsers absorb this fine; legacy MTU-constrained networks (some IoT, some satellite) may need adjustment.

### 6. PKI: composite certificates and parallel hierarchies

Two viable patterns:

- **Composite certificates** (LAMPS WG draft): single cert, two signatures (e.g., ECDSA + ML-DSA). Verifier uses whichever it supports; composite is broken only if **both** are broken.
- **Parallel PKI**: stand up a parallel ML-DSA root, issue dual end-entity certs, transition consumers gradually. Higher operational burden but cleaner separation.

Plan for **certificate-chain growth**: an ML-DSA-65 leaf + intermediate + root chain can reach ~14 KB versus ~3 KB ECDSA. Measure TLS record limits, JWT header sizes, X.509 storage in databases.

### 7. Code-signing — start now

The artifacts you sign in 2026 are the artifacts a quantum-equipped attacker would forge in 2035. Move signing roots to **SLH-DSA** (or LMS/XMSS) **today** for any artifact with a multi-year lifetime — firmware, OS images, container base images, package-manager root keys.

- Generate PQC root in HSM / KMS that supports it (Thales Luna 7.13+, Entrust nShield 13+, or air-gapped tooling)
- Co-sign current artifacts: classical + PQC signature attached side-by-side
- Add PQC verification path to bootloaders / package managers / installers; ship verifier updates ahead of the cutover
- Plan public root distribution (browser / OS truststore inclusion) — this is a multi-year process

### 8. Track standards & ecosystem

PQC is moving fast. Subscribe to:

- NIST PQC project page and `pqc-forum` mailing list
- IETF working groups: TLS, LAMPS, JOSE, COSE, CFRG
- CISA Quantum-Readiness updates
- BSI (Germany), ANSSI (France), NCSC (UK) guidance for sector-specific deadlines
- Vendor roadmaps for AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault, Cloudflare, Akamai, Fastly, Microsoft, Apple, Google PKI

Re-baseline your CBOM at least quarterly; update algorithm choices as standards stabilize.

## Common Pitfalls

| Pitfall | Why it fails | Fix |
| --- | --- | --- |
| "We'll wait until quantum computers exist" | HNDL is happening now; data lifetime > breach horizon | Prioritize confidential long-lived channels in 2026 |
| Pure-PQ cutover with no hybrid | Any flaw in a brand-new algorithm or implementation = downtime | Use hybrid (classical + PQ) during transition |
| Hard-coding RSA / ECDSA in application crypto | No agility; PQC swap requires code rewrite per call site | Introduce a `Signer`/`Kem` interface with config-driven algorithm |
| Choosing FN-DSA before vetted constant-time impls | Floating-point side channels are subtle and have already produced real-world breaks | Default to ML-DSA; only adopt FN-DSA where compactness is essential and the impl is audited |
| Ignoring certificate / handshake size growth | Surprise TLS failures behind MTU-limited paths or in size-capped JWTs | Measure handshake + chain size at the edge before rollout |
| Trying to PQC-encrypt everything in one quarter | Coordination failures across teams; broken interop | Phase by HNDL exposure; hybrid TLS first; signing second |
| Using research libraries (liboqs) in production | Non-FIPS, evolving APIs, no support contract | Use only NIST-validated libraries (OpenSSL 3.5 PQ provider, BoringSSL, BoringCrypto, vendor HSMs) |

## Output Format

Produce a **PQC Migration Plan**:

```markdown
# Post-Quantum Cryptography Migration Plan: <org / product>

## 1. Cryptographic Bill of Materials (CBOM summary)
- Inventory totals per primitive (RSA-2048, ECDSA-P256, Ed25519, DH-2048, ...)
- Top 10 systems by HNDL exposure (data-lifetime × volume × confidentiality)

## 2. HNDL risk assessment
| System | Channel | Algorithm | Data lifetime | HNDL rating |

## 3. Algorithm selection per use-case
| Use case | Today | Hybrid (transition) | Target PQC |

## 4. Phased roadmap
- Phase 0 (Q1–Q2 2026): CBOM, crypto-agility refactor, PQC root generation
- Phase 1 (Q3–Q4 2026): Hybrid TLS at edge, public-facing endpoints
- Phase 2 (2027): Internal mTLS, VPN, SSH; PQC code-signing rollout
- Phase 3 (2028–2030): PKI re-issuance, S/MIME, document encryption
- Phase 4 (≤ 2033): CNSA 2.0 / regulatory deadline compliance

## 5. Compliance mapping
- CNSA 2.0, NIST SP 800-131A, EU CRA, NIS2, sector regs

## 6. Risks & dependencies
- Vendor PQC roadmap blockers
- HSM / KMS support gaps
- Bandwidth / size impacts measured

## 7. Governance
- CBOM regenerated in CI
- Quarterly standards review
- Crypto-board sign-off on algorithm changes
```

## Worked Example

**Subject**: Mid-size financial-services SaaS, EU + US customers, regulatory data-retention 10 years.

CBOM highlights:

- 312 TLS endpoints (RSA-2048 / ECDSA-P256, mostly via Let's Encrypt + AWS ACM)
- 4 internal CAs (RSA-4096 root, 12-year lifetime — already in HNDL window)
- 1 firmware-signing key (ECDSA-P384) — embedded HSM in 200K hardware tokens deployed
- mTLS service mesh (Istio + SPIRE), ECDSA-P256
- JWT signing: RS256 (RSA-2048)

Plan:

| Phase | Action | Deadline |
| --- | --- | --- |
| 0 | Refactor JWT / mTLS issuance behind a `Signer` interface; CBOM in CI | Q1 2026 |
| 1 | Enable `X25519MLKEM768` on AWS ALB + Cloudflare front; measure handshake size impact | Q2 2026 |
| 1 | Stand up parallel ML-DSA-65 internal CA; dual-issue mTLS certs in service mesh | Q3 2026 |
| 2 | Move JWT signing to ML-DSA-65 (composite with RS256 during 6-mo overlap) | Q4 2026 |
| 2 | Generate SLH-DSA-192s firmware-signing root in HSM; ship co-signed firmware updates so deployed tokens learn to verify PQC | 2027–2028 |
| 3 | Re-issue customer-facing certs with composite ML-DSA + ECDSA when public CAs offer them | 2028 |
| 4 | Decommission RSA / ECDSA-only paths | by 2031 |

Critical risks: firmware-signing migration is the **longest pole** (must reach deployed devices); start in Q3 2026 to leave field-update headroom.

## Decision Framework

- **Is this data confidential beyond 2035?** If yes, it is HNDL-exposed today. Move key-establishment to hybrid PQC this year.
- **Does CNSA 2.0 / a sector regulator apply?** Treat the regulator's deadline as immovable; back-plan from it.
- **Pure PQ or hybrid?** Hybrid until you have at least one full annual review cycle of running PQ in production and ecosystem maturity is high. Default 2026 answer is **hybrid**.
- **ML-DSA vs SLH-DSA for signatures?** ML-DSA for everyday (smaller, faster). SLH-DSA for long-lived roots and anything that **must** survive a hypothetical lattice break.
- **Composite vs parallel certs?** Composite is operationally simpler (one cert, one chain); parallel allows independent lifecycle. Pick composite unless you have a specific lifecycle reason.
- **Should we adopt FN-DSA?** Only if signature size is critical and you have audited constant-time implementations on your platform.
- **Is liboqs OK?** For interop testing yes; for production confidentiality no — wait for FIPS-validated builds.

## Authoritative References

- NIST FIPS 203 (ML-KEM): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf
- NIST FIPS 204 (ML-DSA): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf
- NIST FIPS 205 (SLH-DSA): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf
- NIST IR 8547 — Transition to PQC standards: https://csrc.nist.gov/pubs/ir/8547/ipd
- NIST SP 800-208 (LMS/XMSS): https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-208.pdf
- NSA CNSA 2.0: https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF
- CISA / NSA / NIST Quantum-Readiness factsheet: https://www.cisa.gov/resources-tools/resources/quantum-readiness-migration-post-quantum-cryptography
- IETF `draft-kwiatkowski-tls-ecdhe-mlkem` (X25519MLKEM768): https://datatracker.ietf.org/doc/draft-kwiatkowski-tls-ecdhe-mlkem/
- IETF `draft-ietf-lamps-pq-composite-sigs`: https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/
- BSI Migration to Post-Quantum Cryptography: https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Crypto/Migration_to_Post_Quantum_Cryptography.pdf
- CycloneDX 1.6 CBOM: https://cyclonedx.org/capabilities/cbom/
- Cloudflare PQC deployment notes: https://blog.cloudflare.com/pq-2024/
- Open Quantum Safe (liboqs): https://openquantumsafe.org/
