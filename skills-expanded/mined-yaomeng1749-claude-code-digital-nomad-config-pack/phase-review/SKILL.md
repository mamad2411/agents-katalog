---
name: phase-review
description: Phase 5 of the software delivery workflow: perform code quality, language-specific, security, and optional multi-model review on the current change set before shipping.
origin: ECC automation-pack
---

# Phase Review

Use this skill when the user asks for `/phase-review`, code review phase, multi-model review, Santa Loop review, or pre-ship review of a change set.

## Purpose

Find correctness, security, maintainability, and integration risks before release.

## Workflow

1. Inspect the diff and recent commits.
2. Review in parallel where possible:
   - general correctness and maintainability
   - security and privacy
   - language/framework-specific risks
3. If external model CLIs are available and appropriate, run an independent review:
   - `codex review --uncommitted`, `codex review --base main`, or `codex review --commit HEAD`
   - fallback to another configured reviewer such as Gemini
4. Merge findings from internal and external reviews.
5. Classify issues by severity.
6. Fix critical and high-confidence defects, then re-run review or targeted verification.
7. Stop after 3 review-fix rounds unless the user requests more.

## Output

Use this shape:

```text
REVIEW VERDICT: PASS | FAIL
General Review: PASS | FAIL
Security Review: PASS | FAIL
Language Review: PASS | FAIL
External Review: PASS | FAIL | SKIPPED
Issues:
- ...
```

End with `PHASE_REVIEW_PASS` or `PHASE_REVIEW_FAIL`.
