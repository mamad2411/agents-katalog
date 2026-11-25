---
name: fix-bug
description: Diagnose, fix, and validate a reported bug with minimal scoped changes.
---

# Fix Bug

## Procedure

1. Reproduce or isolate the reported behavior.
2. Read the nearest applicable `AGENTS.md`.
3. Load only the relevant `ai-context` files.
4. Identify the root cause before modifying code.
5. Implement the smallest correct fix.
6. Add or update tests when applicable.
7. Run relevant validation.
8. Check for regressions.
9. Report the root cause, changed files, and validation results.

## Rules

- Do not hide symptoms instead of fixing the cause.
- Do not introduce unrelated refactors.
- Do not weaken validation to make tests pass.
- Do not leave TODOs, placeholders, or debugging code.
- Preserve existing architecture and boundaries unless the bug requires a documented change.