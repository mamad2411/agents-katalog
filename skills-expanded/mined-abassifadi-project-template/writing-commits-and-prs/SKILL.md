---
name: writing-commits-and-prs
description: Writes Conventional Commits messages and pull request descriptions from staged changes or a branch diff, and splits work into small reviewable commits. Use when committing, opening or describing a pull request, writing a changelog entry, or when the user asks for a commit message.
argument-hint: "[commit|pr]"
metadata:
  role: senior-developer
  version: "1.0"
---

# Writing commits and pull requests

## Commits — Conventional Commits 1.0

Format:

```
<type>(<optional scope>): <imperative summary, ≤ 72 chars, no period>

<body: what and WHY, wrapped at 72 chars. Not how — the diff shows how.>

<footer: BREAKING CHANGE: ..., Refs: #123, Co-authored-by: ...>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
A breaking change adds `!` after the type/scope (`feat(api)!: ...`) and a `BREAKING CHANGE:` footer.

**Examples**

Input: added JWT login endpoint and token middleware
```
feat(auth): add JWT-based login

Sessions were stored in memory and lost on every deploy. Tokens let
any instance validate a request without shared state.

Refs: #214
```

Input: dates in reports shifted by one day for users west of UTC
```
fix(reports): format dates in the user's time zone

Dates were rendered from UTC midnight, so users in negative offsets
saw the previous day.
```

## Commit hygiene

1. Inspect first: `git status`, `git diff --staged`. Never commit secrets, build output, or unrelated files.
2. One logical change per commit; each commit builds and passes tests.
3. Separate refactors, formatting, and behavior changes into different commits.
4. If the staged diff mixes concerns, propose a split (`git add -p`) before writing the message.

## Pull requests

Keep PRs small (aim < 400 changed lines). Template:

```markdown
## What
<one-paragraph summary of the change>

## Why
<problem, link to issue/ADR>

## How
<key design decisions, alternatives rejected>

## Testing
<commands run, new tests, manual steps, screenshots for UI>

## Risk & rollout
<blast radius, feature flag, migration, rollback plan>

## Checklist
- [ ] Tests added/updated
- [ ] Docs/changelog updated
- [ ] No breaking change (or documented above)
```

Title follows the commit format (`feat(scope): ...`) so squash-merges produce a clean history.
