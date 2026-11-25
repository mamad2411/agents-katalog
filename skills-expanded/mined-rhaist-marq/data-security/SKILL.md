---
name: data-security
description: "Covers data-centric security architecture: a classification scheme people actually use, DLP and its limits, encryption at rest/in transit/in use, tokenization vs encryption, key separation, retention, and APAC data-localization pitfalls. Use when the user asks how to classify or protect sensitive data, whether DLP will work, tokenize vs encrypt (e.g. card or PII data), design data retention, or handle data residency."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Data security architecture

Protect the data, not just the perimeter around it, because the perimeter is
gone (SaaS, BYOD, third-party processors). Everything here depends on one thing
you must do first: **know what data you have and where it flows** (data discovery
and a data map / RoPA). You cannot classify or protect what you can't see.

## Classification scheme that people actually use

The failure mode is a 6-tier taxonomy nobody applies. Use **4 tiers, max**, named
for handling consequences not abstractions:

| Tier             | Examples                                              | Handling rule                                                               |
| ---------------- | ----------------------------------------------------- | --------------------------------------------------------------------------- |
| **Public**       | Marketing, published docs                             | No controls; just integrity (don't let it be tampered).                     |
| **Internal**     | Org charts, internal wikis                            | Default for everything; SSO-gated, not shared externally.                   |
| **Confidential** | Customer PII, source code, contracts                  | Encrypt, access on need-to-know, DLP-monitored, logged.                     |
| **Restricted**   | Secrets, regulated data (PHI, cardholder, auth creds) | Strongest: tokenize/encrypt, JIT access, key-separated, narrow legal basis. |

Rules that make it stick:

- **Sensible default** (Internal) so unlabeled data isn't unprotected.
- Classify by the **most sensitive element** in a dataset; one SSN makes the table Restricted.
- Map tier -> _handling matrix_ (storage, transit, sharing, retention): the tier
  is useless without the "so therefore you must" actions next to it.
- Auto-classify where possible (DLP/cloud-native classifiers, Microsoft Purview), but the data
  _owner_ accepts the label. Labels drive DLP policy and encryption automatically.
- Regulated categories ride on top: cross-link `load_skill privacy-eu`: GDPR
  "special category" data and PCI cardholder data force the Restricted handling
  regardless of your internal label.

## DLP and its hard limits

DLP enforces the handling matrix by inspecting data in three places:

- **Network DLP**: egress inspection (email, web uploads). Blind to TLS it can't
  break; useless against personal devices/networks.
- **Endpoint DLP**: agent watches copy/USB/print/upload on managed devices. Blind
  on unmanaged/BYOD.
- **Cloud DLP / CASB / DSPM**: scans SaaS + cloud stores (S3, OneDrive, Snowflake),
  the place most data now actually lives. This is where to invest in 2026.

**Limits (set expectations honestly):**

- DLP catches **accidental/sloppy** leaks well; a motivated insider defeats it
  (photograph the screen, retype, steganography, personal device).
- It is **content-pattern-bound**: strong on regex-able data (card/SSN), weak on
  unstructured IP ("the secret recipe").
- High false-positive tax; start in **monitor/log mode**, tune, then enforce on the
  highest tiers only. A DLP rolled out in block mode on day one gets disabled by week two.
- It does **not** replace access control or encryption: it's the detective layer
  over them. Treat DLP findings as signal into `load_skill incident-response-leadership`.

## Encryption: at rest, in transit, in use

| State          | Protects against                            | Standard                                         | Catch                                                                                                                            |
| -------------- | ------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **At rest**    | Stolen disk/backup/DB file                  | AES-256 (XTS for disk, GCM for records)          | Transparent disk/DB encryption protects a _powered-off_ disk only; a live app/DB sees plaintext. Doesn't stop a compromised app. |
| **In transit** | Network sniffing / MITM                     | **TLS 1.3** (1.2 floor; kill TLS 1.0/1.1, SSLv3) | Internal/east-west traffic too, not just edge. mTLS for service-to-service.                                                      |
| **In use**     | Cloud host/hypervisor/insider w/ RAM access | **Confidential computing** (TEEs)                | Newer, perf overhead, attestation complexity.                                                                                    |

**Encryption in use / confidential computing** (verify, fast-moving):

- VM-level TEEs are the current shape: **AMD SEV-SNP** and **Intel TDX** encrypt
  guest RAM against the hypervisor/host; older Intel SGX was process-enclave only.
- TDX uses AES-256, SEV-SNP AES-128 for memory encryption; both add **remote
  attestation** so you prove the workload ran in a genuine TEE before releasing secrets.
- Use it for: regulated/multi-tenant cloud workloads, sensitive AI/ML on shared infra,
  "we don't trust the cloud operator" threat models. Verify current support per cloud:
  https://docs.cloud.google.com/confidential-computing/confidential-vm/docs/confidential-vm-overview
- Post-quantum: at-rest data with long secrecy lifetimes is the "harvest-now-decrypt-
  later" target: start planning PQC migration; cross-link `load_skill crypto-key-management`.

## Tokenization vs encryption: pick deliberately

- **Encryption**: reversible with a key; ciphertext is mathematically derived from
  the plaintext. Right for data you must process/decrypt at scale.
- **Tokenization**: replace the value with a random token; real value lives in a
  separate **token vault**. There is no key in the data path to steal; the token is
  meaningless without vault access.
- Use **tokenization** to pull systems out of compliance scope: tokenized PAN means
  the app/DB never holds cardholder data, so it falls out of PCI-DSS scope. Same play
  for SSNs in analytics. Format-preserving tokens keep schemas intact.
- Use **encryption** when you need the real value back in many places (DB-level,
  field-level encryption). Tokenization scales worse (vault is a bottleneck/SPOF) but
  shrinks scope better.

## Key separation (the rule that makes encryption real)

Encryption at rest is theater if the key sits next to the data. Enforce:

- **Keys in a KMS/HSM**, separated from the ciphertext, with their own access policy.
- The DB admin who can read the encrypted store must **not** also hold the decryption
  key (separation of duties). Envelope encryption: data key wraps data, KEK wraps data key.
- Rotation, escrow, dual-control, key-deletion-as-crypto-shredding: all live in the
  sibling skill: `load_skill crypto-key-management`. This skill defines _when_ to
  encrypt; that one defines _how to run the keys_.

## Data lifecycle & retention

- **Minimize at intake**: the cheapest data to protect is the data you never collected
  (GDPR data-minimization; cross-link `load_skill privacy-eu`).
- **Retention schedule per classification**: define max retention; default-delete, don't
  default-keep. "Keep everything forever" is unmanaged liability + bigger breach blast radius.
- **Defensible deletion**: automated expiry, documented, including backups and
  derived/replicated copies (the data lake and the SaaS export, not just the primary).
- **Crypto-shredding**: for distributed/immutable stores, destroy the key to render
  data unrecoverable when physical deletion is impractical.
- Lifecycle stages to control: create/classify -> store -> use -> share -> archive ->
  destroy. Each tier gets stricter rules at every stage.

## APAC data-localization pitfall (where EU/US instincts break)

An EU/US team assumes SCCs/adequacy (EU) or one global datastore (US) travels
everywhere. It doesn't: residency is a per-dataset design input in APAC:

- **China** (PIPL/DSL/CSL) gates personal-data export behind a **CAC security
  assessment**, an **SCC filing**, or **certification**, chosen by volume (security
  assessment at >1M individuals or ≥10k sensitive; <100k non-sensitive exempt since
  the 2024 relaxation; the 100k to 1M band takes SCCs or certification). Full per-country
  detail and clocks: `load_skill privacy-apac`. "Important data" may not leave at all without assessment.
- **India** (DPDP Rules 2025) is permissive by default (a **blocklist** model, transfer
  allowed unless the government restricts a country), **but** sector rules override:
  RBI forces payment data to stay in-country, SEBI/IRDAI add their own localization.
- **Indonesia** and others layer sector localization on top of the general privacy law.
- The lesson: the general privacy regime and the sector localization mandate are
  **separate obligations**: meet both, map residency per dataset, and don't assume a
  transfer mechanism that works for the EU covers China or a regulated Indian workload.
