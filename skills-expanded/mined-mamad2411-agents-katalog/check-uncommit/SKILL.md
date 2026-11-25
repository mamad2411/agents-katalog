---
name: check-uncommit
description: Scan all git repos on the machine for uncommitted changes (modified, staged, untracked)
argument-hint: "[path]"
related:
  - list-projects-git-in-drive-d
  - git-commit
  - check-unpush
  - report

---

## Goal

Scan git repositories across the whole machine (or a given path) for uncommitted changes: modified, staged, and untracked files — so no work is left sitting there forgotten instead of committed

## Scope

- Use when you want to audit every repo for work that has not been committed yet
- Default scope: every repo found on the machine via `/list-projects-git-in-drive-d`, or the given path
- Combined scan: run `/check-uncommit` + `/check-unpush` with the same `path` (e.g. `D:\`) and merge into one per-repo table with columns `No.`, `Project`, `Path`, `Uncommit`, `Unpush`, `Status` to see which repo needs commit, push, or sync
- Read-only: reports status only — never commits or modifies anything

## Execute

### 1. Collect Repositories

> Goal: know which repos to scan

1. Take `path` from the argument — default: scan every drive via `/list-projects-git-in-drive-d`
2. Find directories containing `.git` (including worktrees and submodules)
3. Skip bare repos and cache directories

### 2. Check Working Tree Status

> Goal: count uncommitted changes per repo

1. Run `git -C <repo> status --porcelain` for each repo
2. Classify: `staged` (index), `modified` (unstaged), `untracked` (`??`)
3. Count files per category
4. Check `git -C <repo> stash list` for leftover stashes

### 3. Assess Severity

> Goal: rank the repos most at risk of losing work

1. Flag `high` if the repo has untracked files that look like source code, or staged changes left sitting for a long time
2. Flag `medium` if it has modified files but everything is tracked
3. Flag `low` if there are only untracked build artifacts (from `.gitignore` patterns)
4. Combine with `/check-unpush` results when run together — repos that are both uncommitted and unpushed are the most at risk

### 4. Report

> Goal: summarize the repos with pending work

1. Build a `/report` with columns: `No.`, `Repo`, `Path`, `Staged`, `Modified`, `Untracked`, `Stashes`, `Severity`
2. Sort severity high → low
3. Recommend `/git-commit` or `/git-commit selected-files` per repo with pending work

## Rules

### 1. Read-Only

- Never commit, stash, or modify the working tree
- Report only — the user chooses the action

### 2. Performance

- Limit scan depth and skip directories such as `node_modules` and `.git` internals
- With many repos → run in parallel or report in streaming fashion

### 3. Accuracy

- Use `git status --porcelain` only — never guess from file timestamps
- Note detached HEAD and merge/rebase in progress in the report

- Use /list-projects-git-in-drive-d if needed
- Use /check-unpush if needed
- Use /git-commit if needed

## Expected Outcome

- A list of every repo with uncommitted changes, with a full breakdown
- Severity flags to prioritize the repos most at risk of losing work
- Ready to hand off to `/git-commit` per repo
