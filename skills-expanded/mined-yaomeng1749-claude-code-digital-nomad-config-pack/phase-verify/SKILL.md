---
name: phase-verify
description: Phase D of the solution-design workflow: perform final implementation verification with code review, security review, E2E checks, optional multi-model review, and PR preparation.
origin: ECC automation-pack
---

# Phase Verify

Use this skill when the user asks for `/phase-verify`, final verification after executing a plan, pre-PR verification, or multi-model final review.

## Purpose

Confirm that the executed solution is correct, safe, tested, and ready to hand off.

## Workflow

1. Inspect the full diff and compare it to the validated plan.
2. Run code review, language-specific review, and security review.
3. Use external model review when available and useful.
4. Run E2E checks for user-facing flows.
5. Run final verification before completion:
   - tests pass
   - no accidental artifacts
   - no secrets
   - docs updated where needed
6. Prepare commit and PR material when requested.

## Output

Use this shape:

```text
FINAL VERDICT: PASS | FAIL
Code Review: PASS | FAIL
Security: PASS | FAIL
Cross-Model: PASS | FAIL | SKIPPED
E2E: PASS | FAIL | SKIPPED
PR: <url or not created>
```

End with `PHASE_VERIFY_PASS` or `PHASE_VERIFY_FAIL`.
