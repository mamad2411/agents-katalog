---
name: qa-audit
description: "Use when performing a quality audit, security review, or robustness check. Covers XSS/innerHTML scanning, rule compliance verification, race condition analysis, config schema validation, and documentation drift detection. Produces a severity-classified report (Critical/High/Medium/Low)."
disable-model-invocation: true
---

# QA-Audit

<!-- SETUP: Fill in [FILL: ...] placeholders to match your project. -->

> Systematic full-scope quality audit for `[FILL: main-source-file]` and its config ecosystem.

## Overview

This skill performs a comprehensive code quality audit covering security, robustness, rule compliance, and documentation drift. It produces a structured report with findings classified by severity.

## Scope Options

Ask user for scope before starting:

| Scope | Coverage |
| --- | --- |
| **Source-only** | Main source file |
| **Config-included** | Source + all config files |
| **Full Scope Paranoid** | Source + Config + Agent Rules + Docs (recommended, default) |

**Key requirements:**
1. Read ALL source lines — no skipping
2. Check ALL rule files listed below
3. Report findings with exact line numbers and the specific rule violated
4. Save report as `docs/QA-AUDIT-{YYYY-MM-DD}.md`
5. **No fixes until user approves** — audit is read-only first

---

## When to Use

- **Periodic audits** — after major features or before releases
- **Security review** — when checking for XSS, injection, or unsafe data flows
- **Post-refactor verification** — when code changed significantly
- **Rule compliance check** — when verifying code follows all project conventions
- **Documentation drift detection** — when code values may have changed without updating docs
- **Pre-release quality gate** — as part of the release-readiness workflow

## The 9-Phase Process

| Phase | Focus | Output |
| --- | --- | --- |
| 0 | **Baseline** — Run `npm test` and config/asset verification | Green baseline confirmed |
| 1 | **Source Full Read** — Every line of the main source file | Zone-by-zone understanding |
| 2 | **Rule Compliance** — Compare code against ALL rule files | Rule violation findings |
| 3 | **Config Verification** — Schema conformity, cross-references | Schema/data integrity findings |
| 4 | **Security Scan** — innerHTML/XSS, forbidden APIs | Security findings |
| 5 | **Edge-Case & Robustness** — Race conditions, error propagation, guards | Robustness findings |
| 6 | **Documentation Drift** — Code IST vs. documented SOLL values | Drift findings |
| 7 | **Classification & Report** — Severity assignment, structured audit document | `QA-AUDIT-{date}.md` |
| 8 | **Fix Planning** — Risk per finding, fix order, verification plan | Fix roadmap |

## Severity Definitions

| Severity | Criteria | Examples |
| --- | --- | --- |
| **CRITICAL** | Security vulnerability or data loss risk | XSS via innerHTML, credential exposure |
| **HIGH** | Functional bug affecting users | UI freeze, broken navigation, lost state |
| **MEDIUM** | Rule violation, robustness gap, doku drift | Missing guard, wrong value in docs |
| **LOW** | Code hygiene, dead code, inconsistency | Unused variable, redundant style |

## Key Checks (Quick Reference)

### Security

- All `innerHTML` with config-/runtime-derived text uses a safe escaping function
- No `eval()`, `Function()`, `document.write()`, `postMessage`, `localStorage`
- [FILL: Project-specific security check]

### Rule Compliance

- [FILL: Rule 1 — e.g. "touch-action: manipulation on every interactive element"]
- [FILL: Rule 2 — e.g. ":hover only inside @media (hover: hover) and (pointer: fine)"]
- [FILL: Rule 3 — e.g. "All config uses IIFE + Object.freeze"]
- Relative paths only — no leading `/` or `./` (if applicable)

### Robustness

- [FILL: Race condition check 1]
- [FILL: Error propagation check]
- Compatibility guard covers all required APIs

### Documentation Drift

- [FILL: Key value that must match across all rule files]
- Immutable contract IDs are unchanged

## Rule Files to Check (ALL of these)

| File | Key sections |
| --- | --- |
| `AGENTS.md` | Coding Rules, Immutable Contract |
| `CLAUDE.md` | Critical Constraints, Do NOT |
| `.github/copilot-instructions.md` | Always Do, Never Do |
| `.agent/rules/coding-standards.md` | Rules, conventions |
| [FILL: additional rule files] | [FILL: scope] |

## Report Output

Save to: `docs/QA-AUDIT-{YYYY-MM-DD}.md`

Update `docs/QA-CHECKLIST.md` if new check categories are discovered.

## Full Procedure

→ See `.agent/workflows/qa-audit.md` for the complete step-by-step guide.

→ For Claude Code users: use the `/qa-audit` slash command.
