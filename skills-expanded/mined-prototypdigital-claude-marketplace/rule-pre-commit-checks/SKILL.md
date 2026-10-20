---
name: pre-commit-checks
description: Run formatter, linter, and build checks before every commit.
---

# Pre-commit checks

**Why:** Commits that fail formatting, lint, or build turn into red CI runs and noisy follow-up "fix lint" commits; catching them locally keeps history clean and the branch mergeable.

Before committing any changes, verify the workspace is clean and CI-ready. This is a non-negotiable gate — back it with a pre-commit hook (e.g. husky + lint-staged) or required CI checks, since prose alone won't catch every commit.

## Required steps

1. Run the project formatter on all modified files (e.g. `prettier --write`).
2. Run the linter and fix any new warnings introduced by the changes.
3. Verify the build passes (`tsc --noEmit`, `npm run build`, or equivalent).
4. Never commit files that have unresolved diagnostics, type errors, or lint failures.

## Scope

This applies to every commit — feature work, refactors, docs, config changes. No exceptions.
If a formatter or linter config exists in the project, respect it. If `.prettierignore` or `.eslintignore` excludes certain paths, do not force-format those paths.

## Examples

```sh
# BAD — committing without running any checks
git add src/api/orders.ts
git commit -m "feat: add order cancellation"
→ unformatted code, type error, and lint warning committed

# GOOD — all checks pass before committing
prettier --write src/api/orders.ts
eslint src/api/orders.ts --fix
tsc --noEmit
git add src/api/orders.ts
git commit -m "feat(orders): add cancellation endpoint"
```
