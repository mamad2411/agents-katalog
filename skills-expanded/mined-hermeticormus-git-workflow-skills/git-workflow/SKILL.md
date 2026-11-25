---
name: git-workflow
description: A git workflow for reviewable changes. Start from fresh main, branch with intent, commit in logical units, write conventional-commit messages, push, and open a reviewable PR. Use when starting a change, committing work, or opening a pull request.
license: MIT
---

# Git Workflow

A git workflow for any change that will be reviewed. Sloppy git history is unreviewable and unrevertable; these habits keep it legible so review is fast and reverts are surgical.

**Tradeoff**: this biases toward small commits and small PRs. For a one-line typo fix, use judgment.

## 1. Start fresh

Branch from an up-to-date `main`. A branch cut from stale `main` carries conflicts you did not write.

```bash
git checkout main
git pull origin main
git status   # confirm a clean tree before branching
```

## 2. Branch with intent

```bash
git checkout -b feature/order-export-csv
git checkout -b fix/session-refresh-null
git checkout -b chore/bump-eslint-9
```

Prefixes: `feature/`, `fix/`, `chore/`, `docs/`, `refactor/`, plus a short hyphenated slug. The name states what the branch does without reading the diff.

## 3. Commit in logical units

One idea per commit. If the message needs "and," it is two commits.

```bash
git add -p              # split a dirty tree into logical hunks
git diff --staged       # read what you are about to commit
git commit -m "feat(orders): add CSV export for order history"
```

Atomic commits are what make a branch revertable: a clean revert of one commit undoes exactly one idea.

## 4. Write conventional-commit messages

`type(scope): description` in the subject line.

- `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Imperative mood, no trailing period, under ~72 characters.
- Add a body after a blank line explaining why, not what.

## 5. Push and open a reviewable PR

```bash
git push -u origin feature/order-export-csv
```

A reviewable PR does one thing, stays small, and has a description stating what changed, why, and how it was verified.

## 6. Keep it reviewable

Answer review feedback with new commits, not rewritten history on a branch others read. Keep the branch current with `main` so the diff stays honest about what it changes.

---

See full content, worked examples, and install options at https://github.com/HermeticOrmus/git-workflow-skills.
