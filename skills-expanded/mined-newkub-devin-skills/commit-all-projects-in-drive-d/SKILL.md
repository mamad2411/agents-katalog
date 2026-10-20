---
name: commit-all-projects-in-drive-d
description: Commit uncommitted changes across all drive-D git repos via check-uncommit + git-commit per repo
argument-hint: "[filter]"
allowed-tools:
  - exec
  - read
  - grep
  - find_file_by_name
  - ask_user_question
related:
  - list-projects-git-in-drive-d
  - check-uncommit
  - git-commit
  - check-secrets
  - push-all-projects-in-drive-d
  - report
  - ask-me
  - suggest-next-action
---

## Goal

Safely commit uncommitted changes in every git project under `D:\` — scan with `/check-uncommit` first, then commit per repo via `/git-commit` without destroying pending work

## Scope

Use when you want to commit pending work in every repo under `D:\` in one pass. Supports a `filter` by name/keyword — excludes push (continue with `/push-all-projects-in-drive-d`) and does not modify any files beyond committing

## Execute

### 1. List Target Projects

> Goal: Identify the projects to commit

1. If the user provides a `filter` → run `/search-project-in-drive-d <filter>` to narrow the projects
2. If not provided → run `/list-projects-git-in-drive-d` for the full list
3. Verify the list has at least 1 project; if none → stop and report

### 2. Check Uncommit Per Project

> Goal: Keep only repos with pending work

1. Run `/check-uncommit` on every project in the list — using `git -C <repo> status --porcelain`
2. Skip clean repos — no staged/modified/untracked files
3. Flag repos with an in-progress `merge`/`rebase`, a detached HEAD, or staged secret-suspect files — set them aside for the report and do not commit
4. Show the list of repos to commit with file counts per type

### 3. Confirm Commit Plan

> Goal: The user picks the scope and message strategy before work starts

1. Ask the user with `/ask-me`:
   - `all` — commit every dirty repo (default)
   - `select` — the user selects which repos to commit
   - `dry-run` — show the commit plan without committing
2. Ask for the message strategy: let `/git-commit` generate a conventional message per repo (default) or use one shared message for all repos
3. If the user does not answer → stop and report — never commit without confirmation

### 4. Commit Each Project

> Goal: Commit every selected repo

1. Loop sequentially through the list — one repo at a time so each message matches that repo's context
2. Run `/git-commit` per repo — let that skill handle staging, message, and hooks
3. If a repo has risky files (`.env`, credentials, large binaries) → run `/check-secrets` first, then skip + flag if anything is found
4. If a pre-commit hook fails → record the error and skip that repo — never use `--no-verify` without permission
5. If more than 5 independent repos → optionally use `/use-subagents` to split per repo, then merge the reports

### 5. Verify

> Goal: Confirm no pending work is left

1. Re-run `/check-uncommit` on the repos that were committed
2. Repos still dirty → identify the cause (hook fail, skipped, secrets flag)

### 6. Report Summary

> Goal: Summarize the commit results

1. Use `/report` with columns: `No.`, `Project`, `Path`, `Files`, `Commit`, `Status`
2. Status: `committed`, `clean`, `skipped`, `error`, `flagged`
3. Report the count of each status
4. Run `/suggest-next-action` — recommend `/push-all-projects-in-drive-d` if any repos are committed but not yet pushed

## Rules

### 1. Drive D Scope Only

- Work only under paths starting with `D:\` or `/mnt/d` (WSL)
- Do not touch other drives without permission
- Verify the drive letter before every execution

### 2. Confirm Before Commit

- Always pass `/ask-me` confirmation before committing — show the plan with a dry run first
- Never commit repos with a pending merge/rebase, a detached HEAD, or a secrets flag
- Never `--no-verify` unless the user explicitly allows it

### 3. Per-Repo Context

- Commit messages must come from that repo's actual diff — never reuse one generic message for all repos unless the user says so
- Use conventional commits following that repo's style (check the latest `git log`)

### 4. No Push

- This skill only commits — no push, no pull, no fetch
- If a push is needed, continue with `/push-all-projects-in-drive-d`

### 5. Idempotency

- Re-running never creates empty commits — clean repos are always skipped

- Use /check-unpush if needed
- Use /refactor-commit if needed

## Expected Outcome

- Every dirty repo under `D:\` is committed with a message matching its context (or skipped with a reason)
- No secrets or risky pending work gets committed accidentally
- A summary report of every repo's status with a pointer to `/push-all-projects-in-drive-d`
