---
name: git-workflow
description: Guide safe commits, branches, pushes, and pull requests while preserving uncommitted work.
category: development
aliases:
- git
- commit
- conventional-commits
- push
triggers:
- Commit this
- Open a PR
- Push my branch
- Use a conventional commit message
- Sign my commits
keywords:
- git
- commit
- pr
- push
- branch
- conventional
- signed
- hook
- changelog
dependencies:
- git
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- git-workflow
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- commit
- development
- git
- push
- workflow
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Git Workflow

## Purpose
Wrap the local Git cycle (stage â†’ commit â†’ push â†’ PR) into a single, opinionated
operation. The skill enforces **conventional commits**, optional GPG/SSH signing,
and assembles a useful PR body from the commit log and any issue context.

## When to Use
- The user is ready to commit and push a change
- The user wants a PR opened against `main` / `develop`
- The user wants a clean, conventional commit message generated from a diff

## When NOT to Use
- The repo explicitly forbids conventional commits
- The user wants to amend a public commit
- The user wants to force-push to a protected branch

## Capabilities
- Run `git status`, `git diff --staged`, `git log -n 5` to summarize state
- Stage interactively (`git add -p`) or via glob
- Generate a conventional commit message from the diff
- Sign the commit (GPG or SSH) if configured
- Push the current branch, setting upstream
- Open a PR via `gh pr create` with a body assembled from:
  - the commit log,
  - any linked issue (`Closes #123`),
  - a checklist (tests, docs, changelog),
  - a one-line risk note.

## Inputs
- `mode`: `commit` | `pr` | `commit-and-pr` (default `commit-and-pr`)
- `type` (optional): `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`
- `scope` (optional): the affected area (`auth`, `cli`, `docs`)
- `sign` (default: `auto` — sign if configured)
- `draft` (default `false`)

## Workflow
1. **Inspect** the working tree (`status`, `diff --stat`, `diff --staged`).
2. **Confirm scope** — show the staged changes and ask the user to confirm.
3. **Build the message** — `type(scope): subject` from the diff, body from
   meaningful hunks, footer for `BREAKING CHANGE` and `Closes #â€¦`.
4. **Commit** with `--signoff` (DCO) and signing per `sign`.
5. **Push** the current branch with `--set-upstream`.
6. **Open PR** with `gh pr create --fill --body <body>` (or `--draft`).

## Tools
- `git`
- `gh` (for PR creation; gracefully skip if not installed)
- `commitlint` (optional, in pre-commit hook)

## Examples
**User:** "Commit and open a PR for the auth refactor."
**Response:** Staged: 4 files. Commit: `refactor(auth): split user/session tables`.
Pushed to `feat/auth-split`. PR opened: <url>. Checklist: tests âœ“, docs âœ—, changelog âœ—.

**User:** "Make a chore commit for the dep bump."
**Response:** Staged: `package.json`, `package-lock.json`. Commit:
`chore(deps): bump left-pad to 1.3.0`. Pushed. No PR opened (branch is up to date).

## Safety
- Never `--force` push without explicit `--force-with-lease` confirmation
- Never amend a commit already pushed
- Never skip a pre-commit hook with `--no-verify` unless explicitly asked
- Default to draft PR for first-time contributors on a new branch

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
