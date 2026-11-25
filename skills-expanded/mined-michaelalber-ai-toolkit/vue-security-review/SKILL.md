---
name: vue-security-review
audience: team
description: >
  OWASP-based security review of Vue/TypeScript front-ends. Detects framework (Vite/Vue
  CLI/Nuxt), entry points, and data flows; scans the OWASP Top 10 (2025) mapped to Vue
  client-side risks (raw-HTML XSS via v-html, URL/protocol injection, bundled secrets,
  insecure token storage, dependency CVEs, missing CSP, open redirects, router guard
  bypass); emits an exec summary plus graded findings. Use to audit Vue for
  vulnerabilities. Not for architecture grading (vue-architecture-checklist).
---

# Vue Security Review

> "Security is not a product, but a process."
> — Bruce Schneier

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` / `react` / `vue` security reviews — same values, language-specific threats.

> **Grounding note:** the knowledge base has a Vue 2/3 corpus under `collection="javascript"`. Use
> `collection="internal"` for OWASP and `collection="ui_ux"` for safe-by-default UI; cite **vuejs.org**
> and the OWASP cheat sheets as the Vue authority. Never invent a `vue` collection.

**Non-Negotiable Constraints:**
1. **Evidence or it is not a finding** — Run the tools; cite `file:line` and the OWASP category
2. **Detect the framework first** — Vue escapes interpolation by default and Nuxt adds headers/CSP options — confirm the safe defaults are used, not bypassed, before flagging
3. **Client guards are UX, not security** — A `beforeEnter`/`beforeEach` route guard is never a control; the finding is the *missing server-side check*, not the visible redirect
4. **Severity reflects exploitability + impact**, not how unusual the pattern looks
5. **Architecture, not here** — Structural/maintainability issues belong to `vue-architecture-checklist` — note and route
6. **Federal/gov context → escalate** — If NIST/FIPS/CUI/DOE applies, run `security-review-federal` after this base review

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Validate at boundaries** | Every external input (route params, `postMessage`, API responses) validated/typed before use; never trust client-controlled data — even your own API's response shapes. |
| 2 | **No raw HTML from untrusted data** | Output is escaped by default (Vue's mustache interpolation and `:text` do this); `v-html` is sanitized or never fed user data. |
| 3 | **Secrets out of the bundle** | No API keys/tokens in client code; only intentionally-public `VITE_`/`VUE_APP_` values shipped; everything else stays server-side. |
| 4 | **Authn/authz is server-enforced** | The client never *decides* authorization — it only reflects it. Vue Router navigation guards are UX, not security; the API enforces. |
| 5 | **Least privilege & safe defaults** | Minimal scopes; safe link/target defaults; fail closed on missing data. |
| 6 | **Protect data in transit & at rest** | TLS only; tokens in memory or httpOnly cookies, not `localStorage`; no PII/tokens in logs or analytics. |
| 7 | **Dependencies pinned & audited** | Lockfile committed; `npm audit` / Snyk in CI; transitive CVEs reviewed (the npm tree is deep). |
| 8 | **Evidence-based, graded findings** | Every finding cites `file:line` + OWASP category + severity; report is graded and manager-readable. |

## Workflow

Shared skeleton: `DETECT → SCAN → EXECUTIVE SUMMARY → GRADED FINDINGS`.

```
DETECT     Framework (Vite/Vue CLI/Nuxt + Vue version), entry points (routes, forms, `postMessage`/
           `iframe`, external script tags), and the APIs / storage the app talks to.

SCAN       Walk the Vue Threat Checklist below, one OWASP category at a time. Gather evidence:
             npm audit --omit=dev                       # known CVEs in the dependency tree
             npx eslint . --plugin security               # eslint-plugin-security + vuejs-accessibility
             grep -rn "v-html" src/                        # raw-HTML escape hatch usage
             grep -rn "localStorage\|sessionStorage" src/ # token storage
             grep -rn "VITE_\|VUE_APP_\|process.env" src/ # secrets exposed to the bundle
           Every issue becomes a finding with file:line, OWASP category, and severity.

EXEC SUMMARY  Manager-friendly: risk grade, count by severity, top 3 risks in plain language.

FINDINGS      Technical table: severity · location · OWASP · finding · remediation.
```

**Load on demand — `references/operating-guide.md`:** Vue Threat Checklist, AI Discipline Rules. Deeper detail: `references/owasp-vue-checklist.md`.

## State Block

```
<security-review-state>
language: vue
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
## Security Review: [project] (Vue)
**Framework**: [Vite/Vue CLI/Nuxt + Vue x] | **Scope**: [paths] | **Risk grade**: [A–F]

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
**D** 1+ critical · **F** systemic (unsanitized `v-html` + secrets in bundle + client-only authz).

## Integration with Other Skills

- **`security-review-federal`** — Federal/gov overlay (NIST 800-53, FIPS, CUI, POA&M) applied on top of this base review.
- **`vue-architecture-checklist`** — Companion for structure/maintainability; run first for context.
- **`supply-chain-audit`** — Deeper dependency/CVE and license analysis beyond `npm audit` (the npm tree is the largest attack surface here).
- **`dotnet` / `python` / `php` / `rust` / `react`-security-review** — Sibling skills sharing this exact Core Values + workflow + output.
