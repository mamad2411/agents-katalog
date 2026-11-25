---
name: rust-security-review
audience: team
description: >
  OWASP-based security review of Rust apps with a memory-safety `unsafe` audit. Detects crates,
  async runtime, and entry points, scans the OWASP Top 10 (2025) mapped to Rust patterns
  (injection, unsafe-block memory safety, panic/DoS, deserialization, crypto, secrets), runs
  cargo-audit and cargo-deny for evidence, and emits an exec summary plus graded findings. Use
  to audit Rust for vulnerabilities. Not for architecture grading (rust-architecture-checklist).
---

# Rust Security Review

> "Security is not a product, but a process."
> — Bruce Schneier

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` security reviews — same values, language-specific threats.

**Non-Negotiable Constraints:**
1. **Evidence or it is not a finding** — Run cargo-audit/cargo-deny; cite `file:line` and the OWASP category
2. **`unsafe` is the security surface** — Memory safety holds only outside `unsafe`; audit every block for a correct `// SAFETY:` invariant — a missing or wrong one is Critical
3. **`panic` on input is a DoS finding**, not just a robustness nit, in a service that must stay up
4. **Architecture, not here** — Ownership/trait/structure issues belong to `rust-architecture-checklist` — note and route
5. **Federal/gov context → escalate** — If NIST/FIPS/CUI/DOE applies, run `security-review-federal` after this base review

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Validate at boundaries** | Every external input validated and typed at the edge (serde + validation); never trust client data. |
| 2 | **Parameterized queries only** | No `format!`-built SQL; `sqlx`/`diesel` bound parameters everywhere. |
| 3 | **Secrets out of code** | No hardcoded secrets; env / secret-manager; never logged (beware `Debug` on secret structs). |
| 4 | **Authn/authz at every boundary** | Auth middleware / extractors server-side at each trust boundary; deny by default. |
| 5 | **Least privilege & safe defaults** | Minimal permissions; secure defaults; fail closed. |
| 6 | **Protect data in transit & at rest** | No sensitive data (passwords, tokens, PII) in logs; TLS (`rustls`); encryption at rest. |
| 7 | **Dependencies pinned & audited** | `cargo audit` + `cargo deny` in CI; supply chain reviewed. |
| 8 | **Evidence-based, graded findings** | Every finding cites `file:line` + OWASP category + severity; report is graded and manager-readable. |

## Workflow

Shared skeleton: `DETECT → SCAN → EXECUTIVE SUMMARY → GRADED FINDINGS`.

```
DETECT     Crates (web framework, DB driver, crypto), async runtime, and entry points (handlers, FFI,
           CLI). Enumerate every `unsafe` block — it is the memory-safety attack surface.

SCAN       Walk the Rust Threat Checklist below, one OWASP category at a time. Gather evidence:
             cargo audit                 # RustSec CVEs
             cargo deny check            # licenses, bans, advisories
             grep -rn "unsafe \|\.unwrap()\|\.expect(\|format!(.*SELECT\|transmute" src/
           Every issue becomes a finding with file:line, OWASP category, and severity.

EXEC SUMMARY  Manager-friendly: risk grade, count by severity, top 3 risks in plain language.

FINDINGS      Technical table: severity · location · OWASP · finding · remediation.
```

**Load on demand — `references/operating-guide.md`:** Rust Threat Checklist, AI Discipline Rules. Deeper detail: `references/owasp-rust-checklist.md`, `references/unsafe-audit-guide.md`.

## State Block

```
<security-review-state>
language: rust
mode: DETECT | SCAN | EXEC-SUMMARY | FINDINGS | COMPLETE
detected: [crates | runtime | entry points | unsafe_blocks:N]
owasp_covered: [A01..A10 progress]
findings: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</security-review-state>
```

## Output Template

Shared across all four security reviews.

```markdown
## Security Review: [crate] (Rust)
**Runtime**: [Tokio/async-std] | **unsafe blocks**: [N] | **Risk grade**: [A–F]

### Executive Summary (manager-friendly)
[2–3 sentences: overall posture, the most serious risk in plain language, recommended next step.]
Findings: Critical [N] · High [N] · Medium [N] · Low [N]

### Technical Findings
| Severity | Location | OWASP | Finding | Remediation |
|----------|----------|-------|---------|-------------|
| CRITICAL | file:line | A04 | [pattern] | [fix] |

### `unsafe` Audit
| Location | SAFETY comment | Quality | Risk |
|----------|----------------|---------|------|

**Top 3 priorities**: 1. … 2. … 3. …
```

Risk grade: **A** no critical/high · **B** no critical, ≤2 high · **C** no critical, multiple high ·
**D** 1+ critical · **F** systemic (unjustified `unsafe` + injection + secrets in code).

## Integration with Other Skills

- **`security-review-federal`** — Federal/gov overlay (NIST 800-53, FIPS, CUI, POA&M) applied on top of this base review.
- **`rust-architecture-checklist`** — Companion for structure/maintainability (also audits `unsafe` for correctness); run first for context.
- **`supply-chain-audit`** — Deeper dependency/CVE and license analysis beyond `cargo audit`.
- **`dotnet` / `python` / `php`-security-review** — Sibling skills sharing this exact Core Values + workflow + output.
