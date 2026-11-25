---
name: security-review-federal
audience: team
description: >
  Federal/government security overlay applied ON TOP OF a base language security review
  (dotnet/python/php/rust/react/vue). Language-agnostic: adds NIST SP 800-53 control mapping, FIPS
  140-2/3 crypto compliance (per-language crypto table), CUI handling, EO 14028 supply-chain
  requirements, and DOE Order 205.1B; emits POA&M-ready findings with FIPS 199 impact levels.
  Use for federal/DOE/DOD/national-lab systems. Not standalone — run the matching
  <lang>-security-review FIRST; this overlay maps and extends it.
---

# Security Review — Federal Overlay

> "Compliance is the floor, not the ceiling."
> — NIST Cybersecurity Framework guidance

## Core Philosophy

This is a **language-agnostic federal overlay**, not a standalone review. It assumes the OWASP Top 10
baseline has already been covered by a base `<lang>-security-review` (`.NET` / `Python` / `PHP` / `Rust` / `React` / `Vue`)
and adds the regulatory, cryptographic, and procedural requirements of U.S. federal systems —
particularly DOE and national-laboratory environments.

**Non-negotiables:**
1. **Base review first, always.** Run the matching `<lang>-security-review`; OWASP coverage is a prerequisite. A federal review that skips the baseline is incomplete.
2. **NIST SP 800-53 Rev 5 is the framework.** Every finding maps to a control family (AC, IA, SC, AU, SI, …).
3. **Compliance is legally binding.** FISMA, FIPS, EO 14028 — gaps can revoke an ATO. Findings are POA&M entries, not suggestions.

## Workflow

Shared skeleton: `CONFIRM BASE → MAP → ASSESS → REPORT`.

```
CONFIRM BASE   Verify a base <lang>-security-review ran and its findings are available. If not, run it first.

MAP            Map every base finding to its NIST SP 800-53 control family (references/nist-800-53-mapping.md).
               Assign a FIPS 199 impact level (Low/Moderate/High) by data sensitivity.

ASSESS         Apply the four federal dimensions below; each gap is a new finding with a control ID.

REPORT         Emit the POA&M (references/poam-template.md) + federal executive summary with impact levels.
```

## Federal Dimensions

| Dimension | What to verify | Control family |
|---|---|---|
| **NIST 800-53 mapping** | Every finding cites the control it violates; missing controls flagged | AC · IA · SC · AU · SI · CM |
| **FIPS 140-2/3 crypto** | Only FIPS-validated modules/algorithms for security functions (per-language table below); no MD5/SHA1/DES; approved RNG | SC-13 |
| **CUI handling** | CUI not in logs, dev/test data, or error output; encrypted in transit (TLS 1.2+) and at rest; access-controlled (references/cui-handling.md) | MP · SC · AC |
| **EO 14028 supply chain** | SBOM produced; dependencies provenance-checked; signed artifacts | SR · SA |
| **DOE Order 205.1B** | DOE cybersecurity program requirements where applicable (references/doe-cybersecurity.md) | PM |

### FIPS 140-2/3 crypto — per-language approved usage

| Language | Use (FIPS-validated) | Avoid for security functions |
|----------|----------------------|------------------------------|
| **.NET** | CNG / `System.Security.Cryptography` in FIPS mode; `Aes`, `SHA256+`, `RandomNumberGenerator` | `MD5`, `SHA1`, `DES`, `RNGCryptoServiceProvider` deprecated paths |
| **Python** | `cryptography` in FIPS mode; `hashlib` SHA-256+; `secrets`/`os.urandom` | `hashlib.md5/sha1` for security, `random` for tokens |
| **PHP** | `openssl_*` with AES-GCM, `sodium_*`, `password_hash` (Argon2id) | `md5`, `sha1`, `mcrypt`, `mt_rand`/`uniqid` |
| **Rust** | `ring` / `rustls` / `aws-lc-rs` (FIPS module); `sha2`, `getrandom` | custom crypto, `md5`/`sha1` crates for security |
| **React / Vue (TS)** | Do crypto **server-side** behind FIPS-validated TLS; `crypto.getRandomValues` / Web Crypto only for non-secret nonces; tokens in httpOnly cookies | any client-side encryption/hashing as a security control, `Math.random` for tokens, secrets shipped in the bundle (`VITE_`/`NEXT_PUBLIC_`/`NUXT_PUBLIC_`) |

Deeper FIPS module/algorithm detail: [fips crypto requirements](references/fips-crypto-requirements.md).

## Output Template

Federal executive templates: [federal executive templates](references/federal-executive-templates.md).

```markdown
## Federal Security Review — [System]
**Base review**: [<lang>-security-review, date] · **Categorization (FIPS 199)**: [Low/Moderate/High]
**Frameworks**: NIST SP 800-53 Rev 5 · FIPS 140-2/3 · EO 14028 · DOE 205.1B

### Executive Summary
[Posture vs ATO. The most serious compliance gap in plain language. Recommendation.]

### POA&M (Plan of Action & Milestones)
| ID | Weakness | NIST Control | Severity | Impact | Remediation | Milestone |
|----|----------|--------------|----------|--------|-------------|-----------|
| P-01 | [finding] | SC-13 | High | Moderate | [fix] | [date] |
```

Full POA&M format: [poam template](references/poam-template.md).

## AI Discipline Rules

- **Never run alone.** If no base `<lang>-security-review` has been performed, run it first — this overlay maps and extends it; it does not replace OWASP coverage.
- **Every finding gets a control ID.** "Weak crypto" is not a federal finding; "SC-13 violation: SHA1 used for token signing at `auth.py:88`" is.
- **FIPS is about validated modules, not just strong algorithms.** AES in a non-validated library is still a FIPS gap in a federal context.
- **CUI is the high-stakes data class.** Treat any CUI in logs, test fixtures, or error output as a Critical finding.

## Integration with Other Skills

- **`dotnet` / `python` / `php` / `rust` / `react` / `vue`-security-review** — The required base review this overlay extends; run one first.
- **`supply-chain-audit`** — SBOM / provenance / CVE depth for the EO 14028 dimension.
