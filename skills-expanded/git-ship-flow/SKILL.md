---
name: git-ship-flow
description: Safe git workflow for non-developers — init, branch, commit, push, open a PR, and undo mistakes without losing work. Use when the user says "commit this", "push my changes", "make a branch", "open a PR", "I messed up git", "undo my last commit", or is shipping code and doesn't know git well. Don't use for reviewing someone else's PR diff — use github-pr-review.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Git, Version Control, Shipping]
    related_skills: [github-pr-review, changelog-release-notes, bug-triage-protocol, env-secrets-hygiene]
---

# Git Ship Flow

The one safe path through git for people who build with AI and don't want to think about git internals: branch → commit → push → PR, plus the exact undo move for every common mistake. Core promise: with this flow you can always get your work back, and you can never destroy a teammate's.

## When to Use

- User wants to save/ship their changes: "commit this", "push it", "get this on GitHub".
- User is starting a feature and should be on a branch, not `main`.
- Something went wrong: wrong commit message, committed to `main` by accident, need to undo.
- **Not for:** reviewing a PR someone else opened — use `github-pr-review`. Not for writing release notes from history — use `changelog-release-notes`.

## Quick Reference

| Action | Command / Call |
|---|---|
| See where you are | `git status && git branch --show-current` |
| Start a feature branch | `git switch -c feat/short-name` |
| Stage + commit | `git add -A && git commit -m "feat: what changed and why"` |
| Push branch (first time) | `git push -u origin feat/short-name` |
| Open PR (needs `gh`) | `gh pr create --fill` (fallback: push, then open the URL git prints) |
| Safe undo of a pushed commit | `git revert <sha>` |
| Unstage without losing edits | `git restore --staged <file>` |
| Rescue "lost" work | `git reflog` (then `git switch -c rescue <sha>`) |

## Procedure

1. **Precheck** — `command -v git`; then `git status`. If not a repo: `git init` and confirm a `.gitignore` exists (create one covering `.env`, `node_modules/`, `.DS_Store` before the first commit — see `env-secrets-hygiene`). Note the current branch.
2. **Get off main** — if the user is starting new work on `main`/`master`, create a branch first: `git switch -c feat/short-name`. If they already edited files on `main`, no problem — `git switch -c feat/short-name` carries uncommitted changes with them.
3. **Secret scan before staging** — `git diff --stat` to see what's changing, and eyeball for `.env`, keys, or credentials. If anything secret is in the diff, stop and run `env-secrets-hygiene` first.
4. **Commit** — `git add -A && git commit -m "type: summary"`. Message formula: what changed + why, under ~70 chars, e.g. `fix: stop signup form clearing on error`. Success: `git log --oneline -1` shows it.
5. **Push** — `git push -u origin <branch>`. Success: git prints the remote branch and usually a ready-made PR URL.
6. **PR** — `gh pr create --fill` if the GitHub CLI is installed (`command -v gh`); otherwise use the URL from step 5. Title = the commit summary; body = what/why + how you tested.
7. **Undo (only when asked)** — pick from the table below, never guess:

| Situation | Safe move | Why |
|---|---|---|
| Wrong message, not pushed yet | `git commit --amend -m "new msg"` | Rewrites only your local last commit |
| Committed too early, not pushed | `git reset --soft HEAD~1` | Uncommits but keeps every edit staged |
| Bad commit already pushed | `git revert <sha>` | Adds a new "opposite" commit; history stays intact |
| Committed to main by accident | `git switch -c feat/x` then on main `git revert <sha>` | Work lives on the branch; main is cleaned safely |
| Want one file back to last commit | `git restore <file>` | ⚠️ Destroys uncommitted edits to that file — confirm first |

8. **The never rule** — never `git push --force` and never `git reset --hard` on anything pushed or shared. If the user asks for either, explain that `revert` does the job without rewriting shared history, and proceed with force only if they explicitly confirm they understand teammates' work can be lost (`--force-with-lease` at minimum, on their own branch only).

## Output Template

```
## Shipped ✅
Branch: feat/short-name  (from main @ <sha>)
Commit: <sha> — "feat: what changed"
Pushed: yes → origin/feat/short-name
PR: <url>  (or: "run `gh auth login` to open PRs from the terminal")
Undo, if needed: git revert <sha>  (safe — does not rewrite history)
```

## Pitfalls

- **Committed a secret (.env, API key)** — the key is now in history; deleting the file in a new commit does NOT remove it. Recovery: rotate the key immediately, then follow `env-secrets-hygiene` for history cleanup. Rotation first, always.
- **"detached HEAD" panic** — user checked out a sha and thinks work is gone. Recovery: `git switch -c rescue-branch` right there; everything is saved on the new branch.
- **Push rejected (non-fast-forward)** — remote has commits you don't. Recovery: `git pull --rebase origin <branch>`, resolve any conflicts, push again. Never "fix" this with `--force`.
- **Committed to main instead of a branch** — recovery: `git branch feat/x` (bookmarks the work), then `git reset --hard origin/main` ONLY if main was not pushed since — otherwise `git revert` the commits on main and open a PR from `feat/x`.
- **Merge conflict mid-rebase** — files full of `<<<<<<<` markers. Recovery: open each file, keep the correct lines, delete all marker lines, `git add <file>`, `git rebase --continue`. If overwhelmed: `git rebase --abort` returns to the pre-rebase state, nothing lost.

## Verification

- [ ] `git status` is clean (nothing unintentionally uncommitted)
- [ ] Work is on a feature branch, not main (unless user explicitly wanted main)
- [ ] `git log --oneline -3` shows the expected commit(s) with clear messages
- [ ] Branch visible on the remote (push output or `git ls-remote --heads origin <branch>`)
- [ ] No secrets in the diff (`git show --stat HEAD` reviewed)
- [ ] No force-push or hard reset ran without the user's explicit confirmation
