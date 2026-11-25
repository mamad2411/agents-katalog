---
name: device-fingerprint-ethics
description: >
  Ethical and legal limits for device fingerprinting in owned fraud/security systems:
  purpose limitation, data minimization, transparency, retention, consent/legitimate interest
  analysis, user controls, accuracy/bias, and safer alternatives (WebAuthn, device binding
  keys, risk scores). Use when browser fingerprinting, canvas/audio fingerprint, fraud device
  graph, cross-site tracking risk, or privacy review of fingerprint SDKs — not for building
  covert cross-site trackers or bypassing user consent for ads.
---

# Device Fingerprint Ethics

## Scope And Authorization

- **In scope:** Fraud, security, and product analytics systems **you operate**, with legal/privacy counsel involvement where required.
- **Out of scope:** Deploying fingerprinting to track people across unrelated sites without basis; selling fingerprint graphs; evading browser anti-tracking for adtech abuse.
- Prefer privacy-by-design reviews before enabling new signals (canvas, WebGL, fonts, sensors).
- Redact raw fingerprints and user identifiers in tickets; restrict who can export device graphs.
- Pair with `device-binding-tokens` for security binding, `captcha-bypass-research` only for authorized bot research, and `code-quality-standards`.

## When To Use

- Introducing or expanding device fingerprinting for account takeover / payment fraud.
- Privacy impact assessment (PIA/DPIA-style) of a fingerprint SDK.
- Responding to “is this GDPR/CCPA compliant?” product questions (with counsel).
- Replacing invasive fingerprinting with cryptographic device binding where possible.
- Reviewing retention, sharing, and cross-product linkage of device IDs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cryptographic token–device bind | `device-binding-tokens` |
| Bot/CAPTCHA control research | `captcha-bypass-research` (authorized) |
| ATO methodology | `account-takeover-methodology` |
| Cookie/session security | session/cookie skills |
| Ad tracking growth hacks | **Do not use this library for that** |
| Code quality baseline | `code-quality-standards` |

## Ethical principles

| Principle | Application to fingerprinting |
| --- | --- |
| Purpose limitation | Collect for fraud/security (stated); do not silently reuse for ads/profiling |
| Data minimization | Prefer coarse risk scores over raw canvas hashes stored forever |
| Transparency | Privacy policy + in-product notice where required; no dark patterns |
| User control | Appeals, logout-all, delete/export where law requires; avoid inescapable lock-in |
| Proportionality | Higher friction only for higher risk events |
| Security of processing | Protect fingerprint DBs— they are identifying |
| Non-discrimination | Monitor false positives harming cohorts (shared devices, VPNs, accessibility) |
| Vendor diligence | SDK data flows, subprocessors, default sharing off |

## Workflow

### 1. Confirm purpose and legal basis

1. Write a one-page purpose statement: e.g. “Reduce ATO and payment fraud on first-party properties.”
2. Involve privacy/legal for lawful basis (consent vs legitimate interest varies by jurisdiction and use).
3. Explicitly list **non-purposes** (no resale, no cross-site ads).
4. Success: approved purpose, retention, and sharing matrix before code ships.

### 2. Inventory signals and vendors

| Signal | Entropy / invasiveness | Notes |
| --- | --- | --- |
| User-Agent, timezone, language | Medium | Easy to spoof; still identifying with others |
| Canvas/WebGL/audio | High | Sensitive; browser may brand/noise |
| Installed fonts, plugins | High | Stability vs privacy tension |
| IP / ASN / geo | Medium | Often already logged; handle carefully |
| Hardware attestation / App Attest | High trust, better integrity | Prefer for mobile when available |
| Cookie + account id | Account-scoped | Prefer first-party session continuity |

```bash
# Owned web app — find fingerprint SDKs
rg -n "fingerprint|FingerprintJS|visitorId|canvas.*toDataURL|clientjs|threatmetrix|device.?id" .
```

1. Map every egress of fingerprint data to vendors.
2. Kill dead scripts still collecting.

### 3. Minimize and segregate

1. Store **hashed/salted** device keys with per-org salt; avoid exporting raw component vectors widely.
2. Separate fraud store from marketing analytics; different access controls.
3. Retention: e.g. 30–180 days for raw components; longer only for confirmed fraud cases with policy.
4. Do not join fingerprint to sensitive categories (health, precise geo) without heightened review.

### 4. Prefer less invasive security controls

| Goal | Prefer | Fingerprint role |
| --- | --- | --- |
| Prove same install | Secure enclave key / `device-binding-tokens` | Optional secondary |
| Prove human | Proof-of-work carefully, WebAuthn, challenge | Risk input only |
| New device login | MFA step-up | Risk score trigger |
| Session theft | Short tokens, binding, reuse detection | Soft anomaly signal |

1. Document residual false positive rate and support playbooks (shared family computer, privacy browsers).

### 5. Transparency, UX, and fairness

1. Align privacy policy with actual signals and vendors.
2. Security challenges should explain “unusual login” without exposing other users’ data.
3. Measure challenge rates by browser, OS, locale—investigate bias (e.g. Tor/Firefox users blocked en masse).
4. Provide human review path for locked accounts.

### 6. Technical safeguards

1. First-party collection on your sites/apps only unless multi-product contract allows and discloses.
2. CSP and script inventory so third parties cannot inject extra fingerprinting.
3. Rate-limit and authz APIs that return device-linkage (prevent graph abuse by insiders).
4. Encryption at rest; audit logs for bulk exports.

### 7. Review cadence and hand off

1. Annual DPIA-style review or on vendor/SDK major change.
2. Incident plan: fingerprint DB leak → force step-up, rotate salts, notify per law.
3. Engineering standards: no new signal without privacy checklist ticket.
4. Apply `code-quality-standards` to instrumentation code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Purpose | Fraud on first-party | Silent ad graph enrichment |
| Storage | Score + hashed id, short TTL | Forever raw canvas dumps |
| Security bind | Cryptographic device keys | Fingerprint as only auth factor |
| Vendor | Contractual no-resale, DPA | Random npm tracker |
| UX | Challenge + support path | Permanent ban on privacy browser |
| Transparency | Accurate policy | Hidden SDK farm |

## Output Checklist

- [ ] Purpose and non-purposes written; legal/privacy consulted as required
- [ ] Signal and vendor inventory complete
- [ ] Minimization, hashing, retention configured
- [ ] Segregation from marketing analytics
- [ ] Alternatives (binding, MFA, WebAuthn) evaluated
- [ ] Transparency/UX/fairness measures documented
- [ ] Access control and export audit on device graph
- [ ] Incident response for graph leak
- [ ] Review date scheduled
- [ ] Engineering checklist for new signals

## Rules

- Security use does not automatically justify unbounded tracking.
- Do not use this skill to design covert cross-site advertising fingerprints.
- Prefer cryptographic device binding over sticky passive fingerprints when the goal is token theft resistance.
- Protect fingerprint datasets like identity data.
- Coordinate with counsel for jurisdiction-specific obligations; this skill is operational ethics, not legal advice.
