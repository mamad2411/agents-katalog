---
name: react-security-review
audience: team
description: >
  OWASP-based security review of React/TypeScript front-ends. Detects framework (Vite/CRA/Next),
  entry points, and data flows; scans the OWASP Top 10 (2025) mapped to React client-side risks
  (raw-HTML XSS, URL/protocol injection, bundled secrets, insecure token storage, dependency
  CVEs, missing CSP, open redirects); emits an exec summary plus graded findings. Use to audit
  React for vulnerabilities. Not for architecture grading (react-architecture-checklist).
---

# React Security Review

> "Security is not a product, but a process."
> — Bruce Schneier

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` / `react` security reviews — same values, language-specific threats.

> **Grounding note:** the knowledge base has no React corpus. Use `collection="internal"` for OWASP,
> `collection="javascript"` for JS/TS specifics, and `collection="ui_ux"` for safe-by-default UI; cite
> **react.dev** and the OWASP cheat sheets as the React authority. Never invent a `react` collection.

**Non-Negotiable Constraints:**
1. **Evidence or it is not a finding** — Run the tools; cite `file:line` and the OWASP category
2. **Detect the framework first** — React escapes JSX by default and Next.js adds headers/CSP options — confirm the safe defaults are used, not bypassed, before flagging
3. **Client guards are UX, not security** — A hidden admin route is never a control; the finding is the *missing server-side check*, not the visible button
4. **Severity reflects exploitability + impact**, not how unusual the pattern looks
5. **Architecture, not here** — Structural/maintainability issues belong to `react-architecture-checklist` — note and route
6. **Federal/gov context → escalate** — If NIST/FIPS/CUI/DOE applies, run `security-review-federal` after this base review

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Validate at boundaries** | Every external input (URL params, `postMessage`, API responses) validated/typed before use; never trust client-controlled data — even your own API's response shapes. |
| 2 | **No raw HTML from untrusted data** | Output is escaped by default (JSX does this); the raw-HTML escape hatch is sanitized or never fed user data. |
| 3 | **Secrets out of the bundle** | No API keys/tokens in client code; only intentionally-public `VITE_`/`NEXT_PUBLIC_` values shipped; everything else stays server-side. |
| 4 | **Authn/authz is server-enforced** | The client never *decides* authorization — it only reflects it. Route guards are UX, not security; the API enforces. |
| 5 | **Least privilege & safe defaults** | Minimal scopes; safe link/target defaults; fail closed on missing data. |
| 6 | **Protect data in transit & at rest** | TLS only; tokens in memory or httpOnly cookies, not `localStorage`; no PII/tokens in logs or analytics. |
| 7 | **Dependencies pinned & audited** | Lockfile committed; `npm audit` / Snyk in CI; transitive CVEs reviewed (the npm tree is deep). |
| 8 | **Evidence-based, graded findings** | Every finding cites `file:line` + OWASP category + severity; report is graded and manager-readable. |

## Workflow

Shared skeleton: `DETECT → SCAN → EXECUTIVE SUMMARY → GRADED FINDINGS`.

```
DETECT     Framework (Vite/CRA/Next + React version), entry points (routes, forms, `postMessage`/
           `iframe`, external script tags), and the APIs / storage the app talks to.

SCAN       Walk the React Threat Checklist below, one OWASP category at a time. Gather evidence:
             npm audit --omit=dev                       # known CVEs in the dependency tree
             npx eslint . --plugin security             # eslint-plugin-security + jsx-a11y
             grep -rn "dangerously" src/                 # raw-HTML escape hatch usage
             grep -rn "localStorage\|sessionStorage" src/ # token storage
             grep -rn "VITE_\|NEXT_PUBLIC_\|process.env" src/ # secrets exposed to the bundle
           Every issue becomes a finding with file:line, OWASP category, and severity.

EXEC SUMMARY  Manager-friendly: risk grade, count by severity, top 3 risks in plain language.

FINDINGS      Technical table: severity · location · OWASP · finding · remediation.
```

**Load on demand — `references/operating-guide.md`:** React Threat Checklist, AI Discipline Rules. Deeper detail: `references/owasp-react-checklist.md`.

## State Block

```
<security-review-state>
language: react
mode: DETECT | SCAN | EXEC-SUMMARY | FINDINGS | COMPLETE
detected: [framework+version | entry points | apis/storage]
owasp_covered: [A01..A10 progress]
findings: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</security-review-state>
```

## Output Template

Shared across all security reviews. Executive summary template: [executive summary](references/executive-summary-template.md).

```markdown
## Security Review: [project] (React)
**Framework**: [Vite/CRA/Next + React x] | **Scope**: [paths] | **Risk grade**: [A–F]

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
**D** 1+ critical · **F** systemic (unsanitized raw HTML + secrets in bundle + client-only authz).

## Integration with Other Skills

- **`security-review-federal`** — Federal/gov overlay (NIST 800-53, FIPS, CUI, POA&M) applied on top of this base review.
- **`react-architecture-checklist`** — Companion for structure/maintainability; run first for context.
- **`supply-chain-audit`** — Deeper dependency/CVE and license analysis beyond `npm audit` (the npm tree is the largest attack surface here).
- **`dotnet` / `python` / `php` / `rust`-security-review** — Sibling skills sharing this exact Core Values + workflow + output.
