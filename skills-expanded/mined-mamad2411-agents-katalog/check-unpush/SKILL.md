---
name: check-unpush
description: Scan all git repos on the machine for unpushed commits and branches without an upstream
argument-hint: "[path]"
related:
  - list-projects-git-in-drive-d
  - git-push
  - refactor-commit
  - check-uncommit
  - report

---

## Goal

Scan git repositories across the whole machine (or a given path) for commits not yet pushed, branches without an upstream, and repos whose remote is missing — so work that is committed but not yet backed up is not lost

## Scope

- Use when you want to audit every repo for commits that have not reached a remote
- Default scope: every repo found on the machine via `/list-projects-git-in-drive-d`, or the given path
- Combined scan: run `/check-uncommit` + `/check-unpush` with the same `path` (e.g. `D:\`) and merge into one per-repo table with columns `No.`, `Project`, `Path`, `Uncommit`, `Unpush`, `Status` to see which repo needs commit, push, or sync
- Read-only: reports status only — never pushes or changes remote config

## Execute

### 1. Collect Repositories

> Goal: know which repos to scan

1. Take `path` from the argument — default: scan every repo from `/list-projects-git-in-drive-d`
2. Skip repos with no remote (empty `git remote`) but flag them as `no-remote`
3. Skip bare repos

### 2. Check Ahead/Behind Status

> Goal: count unpushed commits per branch

1. Run `git -C <repo> status -sb` looking for `[ahead N]` / `[behind M]`
2. Run `git -C <repo> log '@{u}..HEAD' --oneline` for commits not yet pushed (when an upstream exists)
3. Count the ahead number for every branch: `git -C <repo> for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads`

### 3. Detect Orphan Branches

> Goal: find branches without an upstream

1. Find local branches whose `%(upstream)` is empty — their commits have never been pushed
2. Find branches whose upstream points at a deleted remote branch (`[gone]`)
3. Check remote reachability (`git ls-remote --heads` with a short timeout) — flag `unreachable` when the remote is dead

### 4. Report

> Goal: summarize the repos whose work is not yet backed up

1. Build a `/report` with columns: `No.`, `Repo`, `Branch`, `Ahead`, `Behind`, `Upstream`, `Status`
2. Status: `unpushed`, `no-upstream`, `gone`, `no-remote`, `unreachable`, `clean`
3. Sort the most `unpushed` first
4. Recommend `/git-push` per repo/branch that needs pushing — when the unpushed commits are messy, recommend `/refactor-commit` before pushing

## Rules

### 1. Read-Only

- Never push, fetch, or change remote config
- Report only — the user chooses the action

### 2. No Network Surprise

- `git status` and `for-each-ref` use local data — no network needed
- Run `git ls-remote` only when remote reachability must be verified, with a short timeout
- When offline → report from local tracking info and state that the remote was not verified

### 3. Accuracy

- Count commits from `@{u}..HEAD`, never by guessing
- Keep `ahead` (extra commits locally) and `behind` (extra commits on the remote) clearly separate

- Use /list-projects-git-in-drive-d if needed
- Use /check-uncommit if needed
- Use /git-push if needed
- Use /refactor-commit if needed

## Expected Outcome

- A list of repos/branches with unpushed commits, with exact counts
- Branches without an upstream and repos with a missing remote are identified
- Ready to hand off to `/git-push` per repo
