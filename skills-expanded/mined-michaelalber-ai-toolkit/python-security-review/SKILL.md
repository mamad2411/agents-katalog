---
name: python-security-review
audience: team
description: >
  OWASP-based security review of Python apps (FastAPI, Django, Flask). Detects framework and
  entry points, scans the OWASP Top 10 (2025) mapped to Python patterns (injection, insecure
  deserialization, SSTI, secrets, auth), runs bandit and pip-audit for evidence, and emits an
  exec summary plus graded findings. Use to audit Python for vulnerabilities. Not for
  architecture grading (python-architecture-checklist).
---

# Python Security Review

> "Security is not a product, but a process."
> — Bruce Schneier

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` security reviews — same values, language-specific threats.

**Non-Negotiable Constraints:**
1. **Evidence or it is not a finding** — Run bandit/pip-audit; cite `file:line` and the OWASP category
2. **Detect the framework first** — Django escapes templates and ships CSRF; FastAPI validates via Pydantic — confirm these are used, not bypassed, before flagging
3. **Severity reflects exploitability + impact**, not how unusual the pattern looks
4. **Architecture, not here** — Structural/maintainability issues belong to `python-architecture-checklist` — note and route
5. **Federal/gov context → escalate** — If NIST/FIPS/CUI/DOE applies, run `security-review-federal` after this base review

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Validate at boundaries** | Every external input validated and typed at the edge (Pydantic/serializers); never trust client data. |
| 2 | **Parameterized queries only** | No f-string / `%`-formatted SQL; bound parameters or the ORM everywhere. |
| 3 | **Secrets out of code** | No hardcoded secrets; env / secret-manager; never logged. |
| 4 | **Authn/authz at every boundary** | Authentication and authorization enforced server-side at each trust boundary; deny by default. |
| 5 | **Least privilege & safe defaults** | Minimal permissions; secure defaults; fail closed. |
| 6 | **Protect data in transit & at rest** | No sensitive data (passwords, tokens, PII) in logs; TLS; encryption at rest. |
| 7 | **Dependencies pinned & audited** | Versions pinned; `pip-audit` in CI; supply chain reviewed. |
| 8 | **Evidence-based, graded findings** | Every finding cites `file:line` + OWASP category + severity; report is graded and manager-readable. |

## Workflow

Shared skeleton: `DETECT → SCAN → EXECUTIVE SUMMARY → GRADED FINDINGS`.

```
DETECT     Framework (FastAPI/Django/Flask + version), entry points (routes, views, tasks, CLIs),
           and the data stores / external calls in scope.

SCAN       Walk the Python Threat Checklist below, one OWASP category at a time. Gather evidence:
             bandit -r <pkg>            # static security analysis
             pip-audit                  # known CVEs in dependencies
             grep -rn "yaml.load(\|shell=True\|format(.*SELECT" <pkg>
           Every issue becomes a finding with file:line, OWASP category, and severity.

EXEC SUMMARY  Manager-friendly: risk grade, count by severity, top 3 risks in plain language.

FINDINGS      Technical table: severity · location · OWASP · finding · remediation.
```

**Load on demand — `references/operating-guide.md`:** Python Threat Checklist, AI Discipline Rules. Deeper detail: `references/owasp-python-checklist.md`.

## State Block

```
<security-review-state>
language: python
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
## Security Review: [project] (Python)
**Framework**: [FastAPI/Django/Flask] | **Scope**: [paths] | **Risk grade**: [A–F]

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
- **`python-architecture-checklist`** — Companion for structure/maintainability; run first for context.
- **`supply-chain-audit`** — Deeper dependency/CVE and license analysis beyond `pip-audit`.
- **`dotnet` / `php` / `rust`-security-review** — Sibling skills sharing this exact Core Values + workflow + output.
