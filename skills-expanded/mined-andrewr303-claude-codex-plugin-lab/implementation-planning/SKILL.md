---
name: implementation-planning
description: Use to turn an approved brief or known change into a falsifiable implementation plan with risks, files, and checks named before edits.
---

# Implementation Planning

Plans are contracts for verification, not narrative.

## Required Shape

```md
Stage 1: Source-of-truth discovery
- Files/sources:
- Artifact:
- Pass check:
- Risk:

Stage 2: Design and risk gate
- Decision:
- Approval needed:
- Failure modes:

Stage 3: Implementation
- Files:
- Patch strategy:
- Acceptance checks:

Stage 4: Verification and skeptic pass
- Commands:
- Runtime/render checks:
- Counterexample search:

Stage 5: Handoff
- Verified:
- Not verified:
- Resume point:
```

## Rules

- Every stage must produce a checkable artifact.
- Name the first check that could invalidate the plan.
- Keep edits scoped to existing ownership boundaries.
- For UI work, include desktop and mobile verification.
- For data/auth/money/legal/production boundaries, require approval before mutation.
- For ML work, lock evaluation before iteration.

## Good Plan Items

- Include file paths, commands, and acceptance criteria.
- Separate build/lint/type checks from behavior checks.
- Include rollback or recovery where risk is high.

