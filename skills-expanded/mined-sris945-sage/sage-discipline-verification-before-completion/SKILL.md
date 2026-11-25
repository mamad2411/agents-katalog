---
name: sage-discipline-verification-before-completion
description: SAGE — no success claims until you have run the verification command in this turn and read the output.
---

# SAGE discipline — Verification before completion

## Purpose

In **SAGE**, “done” means **verified with evidence from a command you ran in this session**, not memory or hope.

**Core rule:** Evidence before claims. Always.

## Iron law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the full check in this message chain, you may not say tests pass, build is clean, or the bug is fixed.

## Gate (every time)

1. **Identify** the command that proves the claim (tests, lint, typecheck, build).
2. **Run** it completely (not a subset unless the claim is explicitly scoped).
3. **Read** stdout/stderr and exit code.
4. **State** the result with a short quote or counts from output.
5. **Only then** use language like “passes”, “complete”, “fixed”.

## Common mistakes

| Bad | Good |
|-----|------|
| “Should work now” | Paste or summarize the command you ran and its result |
| “Tests should pass” | “Ran `pytest -q` → N passed, 0 failed” |
| Trusting a prior agent message | Re-run verification yourself |

## Cross-links

- After verification, align claims with **sage:discipline:test-driven-development** for new behavior.
