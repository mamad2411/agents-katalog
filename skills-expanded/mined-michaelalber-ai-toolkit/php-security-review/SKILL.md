---
name: php-security-review
audience: team
description: >
  OWASP-based security review of PHP / Laravel applications. Detects the framework and entry
  points, scans against the OWASP Top 10 (2025) mapped to PHP/Laravel patterns (mass-assignment,
  query injection, Blade XSS, auth/session, file uploads, secrets), and produces a
  manager-friendly executive summary plus a graded technical findings table. Use to audit PHP
  code for vulnerabilities. Do NOT use to grade architecture/structure — use
  php-architecture-checklist.
---

# PHP Security Review

> "Security is not a product, but a process."
> — Bruce Schneier

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` security reviews — same values, language-specific threats.

**Non-Negotiable Constraints:**
1. **Evidence or it is not a finding** — Run the tools; cite `file:line` and the OWASP category
2. **Detect the framework first** — Laravel ships CSRF, hashing, and Blade escaping — confirm they are used, not bypassed, before flagging
3. **Severity reflects exploitability + impact**, not how unusual the pattern looks
4. **Architecture, not here** — Structural/maintainability issues belong to `php-architecture-checklist` — note and route
5. **Federal/gov context → escalate** — If NIST/FIPS/CUI/DOE applies, run `security-review-federal` after this base review

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Validate at boundaries** | Every external input validated and typed at the edge; never trust client data. |
| 2 | **Parameterized queries only** | No string-concatenated SQL; bound parameters everywhere. |
| 3 | **Secrets out of code** | No hardcoded secrets; env / secret-manager; never logged. |
| 4 | **Authn/authz at every boundary** | Authentication and authorization enforced server-side at each trust boundary; deny by default. |
| 5 | **Least privilege & safe defaults** | Minimal permissions; secure defaults; fail closed. |
| 6 | **Protect data in transit & at rest** | No sensitive data (passwords, tokens, PII) in logs; TLS; encryption at rest. |
| 7 | **Dependencies pinned & audited** | Versions pinned; CVE scan in CI; supply chain reviewed. |
| 8 | **Evidence-based, graded findings** | Every finding cites `file:line` + OWASP category + severity; report is graded and manager-readable. |

## Workflow

Shared skeleton: `DETECT → SCAN → EXECUTIVE SUMMARY → GRADED FINDINGS`.

```
DETECT     Framework (Laravel/Symfony/plain + version), entry points (routes, controllers, jobs,
           console commands), and the data stores / external calls in scope.

SCAN       Walk the PHP Threat Checklist below, one OWASP category at a time. Gather evidence:
             composer audit                       # known CVEs in dependencies
             phpstan analyse / psalm --taint-analysis   # taint + static analysis
             grep -rn "DB::raw\|{!! \|unserialize\|env(" app/   # high-signal patterns
           Every issue becomes a finding with file:line, OWASP category, and severity.

EXEC SUMMARY  Manager-friendly: risk grade, count by severity, top 3 risks in plain language.

FINDINGS      Technical table: severity · location · OWASP · finding · remediation.
```

**Load on demand — `references/operating-guide.md`:** PHP Threat Checklist, AI Discipline Rules. Deeper detail: `references/owasp-php-checklist.md`.

## State Block

```
<security-review-state>
language: php
mode: DETECT | SCAN | EXEC-SUMMARY | FINDINGS | COMPLETE
detected: [framework+version | entry points | data stores]
owasp_covered: [A01..A10 progress]
findings: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</security-review-state>
```

## Output Template

Shared across all four security reviews. Executive summary template: [executive summary](references/executive-summary-template.md).

```markdown
## Security Review: [project] (PHP)
**Framework**: [Laravel x/Symfony/plain] | **Scope**: [paths] | **Risk grade**: [A–F]

### Executive Summary (manager-friendly)
[2–3 sentences: overall posture, the most serious risk in plain language, recommended next step.]
Findings: Critical [N] · High [N] · Medium [N] · Low [N]

### Technical Findings
| Severity | Location | OWASP | Finding | Remediation |
|----------|----------|-------|---------|-------------|
| CRITICAL | file:line | A03 | [pattern] | [fix] |

**Top 3 priorities**: 1. … 2. … 3. …
```

Risk grade: **A** no critical/high · **B** no critical, ≤2 high · **C** no critical, multiple high ·
**D** 1+ critical · **F** systemic (injection + secrets in code + broken access control).

## Integration with Other Skills

- **`security-review-federal`** — Federal/gov overlay (NIST 800-53, FIPS, CUI, POA&M) applied on top of this base review.
- **`php-architecture-checklist`** — Companion for structure/maintainability; run first for context.
- **`supply-chain-audit`** — Deeper dependency/CVE and license analysis beyond `composer audit`.
- **`dotnet` / `python` / `rust`-security-review** — Sibling skills sharing this exact Core Values + workflow + output.
