---
name: git-workflow
description: Git workflow patterns — commit messages, branching, PR workflow, and conflict resolution.
---

# Git Workflow — How to Use Git Properly

## Commit Messages

Format: `<type>(<scope>): <description>`

Types:
- `feat` — new feature
- `fix` — bug fix
- `refactor` — code restructuring without behavior change
- `style` — formatting, no code change
- `docs` — documentation only
- `test` — adding or updating tests
- `chore` — maintenance tasks
- `perf` — performance improvement

Examples:
- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null response from payment gateway`
- `refactor(parser): extract validation into separate module`
- `perf(db): add index for user lookup query`

Rules:
- Subject line: imperative mood, no period, max 72 chars
- Body: explain WHAT and WHY, not HOW (the code shows HOW)
- Reference issues: `Closes #123`, `Fixes #456`

## Branching

- `main` — always deployable
- `feat/<name>` — new features
- `fix/<name>` — bug fixes
- `refactor/<name>` — refactoring
- `chore/<name>` — maintenance

Create branch from main, merge back via PR.

## PR Workflow

1. Create branch from main
2. Make changes, commit incrementally
3. Push branch
4. Create PR with description
5. Request review
6. Address feedback
7. Merge (squash for clean history)

## Conflict Resolution

1. `git fetch origin`
2. `git rebase origin/main`
3. Fix conflicts in files
4. `git add <resolved-files>`
5. `git rebase --continue`
6. `git push --force-with-lease`

Never merge main into your branch — rebase instead.

## Interactive Rebase

Clean up commits before PR:
```bash
git rebase -i HEAD~5
# squash, reword, edit commits
git push --force-with-lease
```

## Stashing

```bash
git stash push -m "WIP: login form"
git stash list
git stash pop
```

Stash before switching branches. Pop when you return.
