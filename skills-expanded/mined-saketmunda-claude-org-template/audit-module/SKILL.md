# skills/audit-module/SKILL.md
# Slash command: /audit-module [path or module name]
# Trigger: User types /audit-module to inspect a specific file, directory, or module

---

## What This Does

Runs a structured 10-point audit on any module, file, or directory. Produces a findings table and a verdict. No code is written — this is read-only analysis.

Useful before: starting a refactor, reviewing inherited code, onboarding to a new module, or deciding whether a module needs extraction.

---

## When to Use

- Before extracting or refactoring a module
- When a module is flagged as high-risk in a sprint plan
- Periodic health checks on core modules
- Onboarding: understand an unfamiliar module fast

---

## The 10-Point Audit

Run each check and record findings:

```
## Module Audit — [path] — [date]

| # | Check | Status | Findings |
|---|---|---|---|
| 1 | Test coverage | PASS / WARN / FAIL | [coverage % or "no tests found"] |
| 2 | Rule compliance | PASS / WARN / FAIL | [which rules are violated, if any] |
| 3 | Layer violations | PASS / WARN / FAIL | [e.g. "handler calls DB directly"] |
| 4 | Error handling | PASS / WARN / FAIL | [silent catches, missing error types] |
| 5 | Logging | PASS / WARN / FAIL | [console.log present, missing log calls] |
| 6 | Security surface | PASS / WARN / FAIL | [unvalidated inputs, hardcoded secrets] |
| 7 | N+1 / query patterns | PASS / WARN / FAIL | [N+1 loops, missing indexes referenced] |
| 8 | Type safety | PASS / WARN / FAIL | [any types, missing interfaces] |
| 9 | Dead code | PASS / WARN / FAIL | [unused exports, commented-out blocks] |
| 10 | Complexity | PASS / WARN / FAIL | [functions >50 lines, nesting >3 deep] |

**Overall:** HEALTHY / NEEDS ATTENTION / REFACTOR RECOMMENDED

### Summary
[2–3 sentences. What this module does. What its biggest risks are. Recommended next action.]

### Recommended Actions
| Priority | Action | Effort |
|---|---|---|
| HIGH | Add tests — currently at 0% | Medium |
| MEDIUM | Break handler into service layer | High |
| LOW | Remove 3 commented-out functions | Low |
```

---

## Audit Definitions

**PASS** — Meets the project standard (from relevant rules/ file)
**WARN** — Below standard but not critically broken — file as tech debt
**FAIL** — Actively harmful — fix before adding new features to this module

---

## Refusal Triggers

- Path doesn't exist — report and stop
- Module is a test file — redirect: "Use /audit-module on the source file, not the test"
- Request to fix findings during this audit — this skill is read-only. File the recommendations; use `/new-feature` or `/sprint` to action them.

---

## Notes

This audit is a snapshot, not a guarantee. It reads static code — it cannot catch runtime bugs, performance issues under load, or race conditions. Use it to inform planning, not to certify production readiness.
