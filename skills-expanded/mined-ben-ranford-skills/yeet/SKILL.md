---
name: yeet
description: Create branches, commits, pushes, and draft pull requests with GitHub CLI using strict prerequisites and naming conventions. Use when asked to publish local git changes, open a PR, or run an end-to-end git-to-PR workflow in a repository.
---

# GitHub PR Workflow

Execute this workflow exactly when asked to publish work with `git` + `gh`.

## Prerequisites

1. Run `gh --version`.
2. If `gh` is missing, ask the user to install GitHub CLI and stop.
3. Run `gh auth status`.
4. If not authenticated, ask the user to run `gh auth login`, then re-run `gh auth status`, and stop until that is complete.

## Naming Conventions

1. Branch: `feat/{description}` or `bug/{description}` when starting from `main`, `master`, or repository default branch.
2. Commit message: `{description}` (terse).
3. PR title: Conventional Commits style `type(scope): short summary`.
4. Allowed PR title types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`.
5. Scope is required and should reflect subsystem/team surface (for example: `api`, `web`, `infra`, `auth`).
6. Example PR titles: `fix(auth): handle expired refresh tokens`, `feat(api): add batched export endpoint`.

## Workflow

1. Determine current branch with `git branch --show-current`.
2. If current branch is `main`, `master`, or the default branch, create a branch:
```bash
git checkout -b "feat|bug/{description}"
```
3. If already on a non-default branch, stay on current branch.
4. Confirm status and stage all changes:
```bash
git status -sb
git add -A
```
5. Commit using terse description:
```bash
git commit -m "{description}"
```
6. Run checks if not already run in this session.
7. If checks fail because dependencies/tools are missing, install dependencies and rerun checks once.
8. Push with tracking:
```bash
git push -u origin $(git branch --show-current)
```
9. If push fails due to workflow auth errors, pull from `master` and retry push.
10. Open draft PR using:
```bash
GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)
```
11. Immediately update PR metadata:
```bash
gh pr edit --add-assignee <your github username> --add-label "{label}" --milestone "{milestone}"
```
12. Determine and apply the correct label and milestone for the repository/issue context. If ambiguous, ask the user before editing.
13. Write PR body to a temp markdown file using real newlines (heredoc), then apply it with `--body-file` or `gh pr edit --body-file`.
14. Never pass newline escapes like `\\n` in PR markdown.

## PR Description Requirements

Write detailed markdown prose that includes:

1. The issue.
2. Cause and user impact/effect.
3. Root cause.
4. The fix.
5. Tests/checks used to validate.

Use concrete deltas from the actual diff.
