---
name: mobile-owasp-masvs
description: Aligning a mobile app against the OWASP Mobile Application Security Verification Standard (MASVS v2). Use as a review rubric and as the source of truth for which controls apply.
---

# OWASP MASVS Alignment

## Instructions

MASVS v2 is the de-facto standard for mobile app security. Use it as a verification checklist, not as a wish list — not every control applies to every app.

### 1. The Eight Groups (MASVS v2)

| Group | Scope |
| ----- | ----- |
| **MASVS-STORAGE** | Sensitive data at rest. |
| **MASVS-CRYPTO** | Cryptography usage. |
| **MASVS-AUTH** | Authentication and session management. |
| **MASVS-NETWORK** | Network communication. |
| **MASVS-PLATFORM** | Platform interaction (IPC, WebViews, permissions). |
| **MASVS-CODE** | Code quality and update hygiene. |
| **MASVS-RESILIENCE** | Reverse-engineering and tampering resistance. |
| **MASVS-PRIVACY** | Privacy of user data. |

Adopted in v2: RESILIENCE and PRIVACY are now explicit groups.

### 2. Pick a Profile

MASVS defines **profiles**, not a monolith:

- **L1 (baseline)** — every mobile app.
- **L2 (defense-in-depth)** — apps handling sensitive data (banking, health, enterprise).
- **R (resilience)** — apps at material risk of client-side attacks (DRM, gambling, premium content).

A SaaS productivity app may be L1. A consumer bank is L2 + R. Document which profile applies per app and per feature.

### 3. Control Mapping to Practical Skills

| MASVS group | Map to skill |
| ----------- | ------------ |
| STORAGE | [secure-storage](../../storage/secure-storage/SKILL.md), [keystore-keychain](../../storage/keystore-keychain/SKILL.md), [encrypted-databases](../../storage/encrypted-databases/SKILL.md) |
| CRYPTO | [keystore-keychain](../../storage/keystore-keychain/SKILL.md) |
| AUTH | [oauth-mobile](../../auth/oauth-mobile/SKILL.md), [token-storage](../../auth/token-storage/SKILL.md), [biometric-auth](../../auth/biometric-auth/SKILL.md), [mfa-on-mobile](../../auth/mfa-on-mobile/SKILL.md) |
| NETWORK | [tls-pinning](../../network/tls-pinning/SKILL.md), [mitm-prevention](../../network/mitm-prevention/SKILL.md), [api-abuse-protection](../../network/api-abuse-protection/SKILL.md) |
| PLATFORM | [mitm-prevention](../../network/mitm-prevention/SKILL.md) (WebView / deep links), [secrets-management](../../secrets/secrets-management/SKILL.md) |
| CODE | [code-obfuscation](../../code/code-obfuscation/SKILL.md), [dependency-scanning](../dependency-scanning/SKILL.md) |
| RESILIENCE | [anti-tampering](../../code/anti-tampering/SKILL.md), [root-jailbreak-detection](../../code/root-jailbreak-detection/SKILL.md) |
| PRIVACY | [privacy-by-design](../../privacy/privacy-by-design/SKILL.md), [consent-management](../../privacy/consent-management/SKILL.md), [gdpr-mobile](../../compliance/gdpr-mobile/SKILL.md) |

### 4. Practical Verification — Quick Wins

Run these on every release:

- **Static**: MobSF (open source) on the APK / IPA. Triage the findings — not every "HIGH" matters for your profile.
- **Dependency**: see [dependency-scanning](../dependency-scanning/SKILL.md).
- **Dynamic**: run against Frida / Objection to validate root / debugger / pinning controls in a lab.
- **Binary**: `apkanalyzer`, `otool -L`, `strings` — sanity-check that no hardcoded secrets slipped in.

```bash
# Example: fail CI if an expected-stripped symbol is present
if unzip -p app-release.aab AndroidManifest.xml | grep -i "DEBUG"; then
  echo "Debug symbol shipped in release bundle" && exit 1
fi
```

### 5. Evidence Package Per Release

For L2 / R apps, produce a short evidence bundle:

- Which profile applies.
- Which MASVS controls are in scope, and which skill / test proves each.
- Exceptions, with a rationale and expiry date.
- Sign-off from engineering + security owner.

This pays for itself on the first audit, SOC 2 report, or App Store rejection.

### 6. What MASVS Does Not Cover

- Server-side authorization (covered by OWASP ASVS + API Security Top 10).
- Business-logic fraud (rate limits, anomaly detection).
- Supply-chain compromise of build tooling (covered by SLSA / in-toto).

Don't pretend MASVS compliance covers these — it doesn't.

### 7. Keep Up With the Standard

MASVS v2 is stable but the **MASTG** (Mobile Application Security Testing Guide) is updated continuously. Subscribe to releases; controls are refined as platforms change (e.g., iOS Privacy Manifests, Android 14 photo picker).

### 8. Using MASVS With AI Agents

When reviewing a PR, prompt the agent:

> "Walk through this diff against MASVS-STORAGE and MASVS-NETWORK. List any control where you would fail or need more info."

Agents with these skills produce useful, specific findings — not generic "consider security" comments.

## Checklist

- [ ] A profile (L1 / L2 / R) is documented per app and per feature.
- [ ] Each in-scope MASVS control maps to a specific skill or test.
- [ ] MobSF (or equivalent) runs on every release build and findings are triaged.
- [ ] Dynamic tests (Frida, Objection) verify resilience controls for R-profile features.
- [ ] Binary sanity checks run in CI (no hardcoded secrets, no debug symbols).
- [ ] Release produces an evidence bundle for L2 / R apps.
- [ ] MASTG updates are reviewed at least quarterly.
