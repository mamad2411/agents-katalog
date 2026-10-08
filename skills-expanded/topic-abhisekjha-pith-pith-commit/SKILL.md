---
name: pith-commit
description: >
  One-shot commit message generator. Conventional Commits format, subject ≤50 chars.
  Use when writing a git commit message for staged changes. Does not persist.
---

Conventional Commits. Subject ≤50 chars. Imperative mood.

```
type(scope): subject

Why: [reason, only when non-obvious from the diff]
```

## Types

| Type | When |
|------|------|
| `feat` | new capability |
| `fix` | bug correction |
| `refactor` | restructure without behavior change |
| `perf` | measurable performance improvement |
| `test` | add or fix tests only |
| `docs` | documentation only |
| `chore` | tooling, deps, config — no prod code |
| `ci` | CI/CD pipeline changes |
| `build` | build system changes |

## Rules

- Subject: imperative. "add" not "added" or "adds". ≤50 chars. Hard limit.
- Scope: component or file affected. Optional but preferred. Lowercase.
- Body (`Why:`): only when the reason is non-obvious from subject + diff. Skip for trivial changes.
- Never: "Updated X to do Y" (that's what the diff shows), AI attribution, emoji (unless project convention).
- Breaking changes: add `!` after type. `feat(api)!: change response shape`

## Examples

Good:
```
fix(auth): correct token expiry unit comparison
Why: exp is Unix seconds, Date.now() is ms — check always evaluated false
```

```
feat(payments): add Stripe webhook signature verification
```

```
refactor(db): extract query builders into repository layer
```

Bad:
```
Fixed the authentication middleware to properly handle token expiration by comparing the values in the correct units so that users can actually log in now
```

One-shot. Does not persist.
