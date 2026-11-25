---
name: refactor-safe-diff
description: >-
  Use when refactoring, renaming, or restructuring code where behavior must stay
  the same, or when the user asks for minimal/surgical changes. Not for greenfield
  features or intentional behavior changes unless listed.
---

# Refactor-safe diff

## Rules

1. **Smallest diff** that achieves the goal — no drive-by formatting, renames, or "while we're here" features.
2. **Do not change behavior** unless explicitly requested; list behavior changes if unavoidable.
3. Touch only files required for the task; avoid moving files unless asked.
4. Preserve public APIs (exports, prop names) unless migration is in scope.
5. Run through affected call sites — no broken imports.

## Process

1. State what will change and what will **not** change.
2. Refactor in steps: extract → wire → delete old (if safe).
3. Keep tests/flows working: auth, payments, critical paths unchanged.

## Verify

After each step:

- TypeScript compiles (no new errors introduced).
- Critical flows still work in chat preview (auth, primary action, payment if applicable).
- Imports and exports resolved; no broken references left behind.

## Output

When done, summarize:

- Files changed (count and names).
- Behavior preserved confirmation.
- Follow-up risks or deferred cleanup (if any).

## Avoid

- Renaming entire codebase conventions in one pass.
- Swapping libraries (SWR → React Query) without explicit ask.
- Deleting code paths you did not verify unused.
- Bundling unrelated bug fixes into the same refactor PR.
