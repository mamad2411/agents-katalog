---
name: cleanup-branches-merged
description: Delete all local and remote branches merged into main, with a dry run first
argument-hint: "[base-branch] [--remote]"
related:
  - ask-me
  - cleanup-git-branch
  - report
  - run-clean
  - run-cleanup
---

## Goal

Delete branches already merged into the base branch (default `main`) — both local and remote — with a dry run and confirmation before any real deletion

## Scope

- Merged local branches: `git branch --merged <base>`
- Merged remote branches, or PR-closed ones, when `--remote` is given
- Skip: the base branch, the current branch, and protected branches (`main`, `develop`, `release/*` per convention)
- Destructive: always requires a dry run + user confirmation
- To delete just one specific branch, or an abandoned (unmerged) branch, use `/cleanup-git-branch` instead

## Execute

### 1. Survey Branches

> Goal: gather all branches and their status

1. `git fetch --prune` to sync the latest remote refs
2. `git branch --merged <base>` to find merged local branches
3. With `--remote`: `git branch -r --merged <base>` to find merged remote branches
4. Cross-check GitHub: branches whose PRs were closed/merged, via `gh pr list --state merged`

### 2. Build Deletion List

> Goal: build the list of branches that are safe to delete

1. Skip: the base branch, the current checkout, and protected patterns (`main`, `master`, `develop`, `release/*`, `hotfix/*`)
2. Flag branches that are merged but have unmerged commits on their remote counterpart
3. Flag branches that are merged but still have an open PR — it could be reopened
4. Keep only: merged + no open PR + not protected

### 3. Dry-Run Report

> Goal: show what will be deleted before doing it

1. Report via `/report` with columns: `No.`, `Branch`, `Local/Remote`, `Merged Into`, `Last Commit`, `Safe`
2. State the total count and the skipped branches, each with its reason
3. Always wait for user confirmation via `/ask-me` before deleting

### 4. Delete

> Goal: delete as confirmed

1. Local: `git branch -d <branch>` (safe delete — refuses unmerged branches)
2. Remote: `git push origin --delete <branch>` only for what the user confirms
3. If `-d` fails → never force `-D` on your own — report it and let the user decide

### 5. Report Result

> Goal: summarize what was deleted and what remains

1. Result table: deleted, skipped, failed, each with its reason
2. `git branch` + `git remote prune origin` to confirm everything is clean

## Rules

### 1. Confirmation Required

- Never delete any branch without a dry-run report and user confirmation
- Use `-d` (safe), not `-D` (force), unless the user explicitly says so

### 2. Protect Critical Branches

- The base branch, the current branch, and protected patterns must never appear in the deletion list
- Branches with an open PR or unmerged commits must be flagged, not deleted

### 3. Sync First

- Always `fetch --prune` first — stale refs make the list wrong
- Perform remote deletions only when the user passes `--remote` and confirms
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- Merged branches deleted safely, both local and remote (when selected)
- Protected and open-PR branches left untouched
- A deleted/skipped report with complete reasons
