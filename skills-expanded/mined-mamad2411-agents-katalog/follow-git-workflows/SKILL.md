---
name: follow-git-workflows
description: Switch to the correct git branch for the named workflow
argument-hint: "[scope]"
related:
  - refactor
  - fix
  - review
  - run-deploy
---

## Goal

Switch to the correct git branch for a named workflow (restructure, feature, fix, review)

## Scope

Use `follow-git-workflows` when the user wants to move the working tree to a workflow-specific branch before running a workflow

## Execute

### 1. Identify Workflow

> Goal: Determine which workflow branch to use

1. Ask or analyze which workflow the user wants: `restructure`, `feature`, `fix`, `review`
2. Run `git status --short` to check the current status
3. If there are uncommitted changes → stop and ask whether to commit, stash, or reset first

### 2. Switch Branch

> Goal: Move to the workflow branch

1. Run `git branch --list` to check whether the branch exists
2. If the branch does not exist → create it with `git switch -c <workflow>`
3. If the branch exists → switch to it with `git switch <workflow>`
4. Verify with `git branch --show-current`

### 3. Confirm Context

> Goal: Report the new branch and next action

1. Show the current branch
2. If the user wants to continue with a task such as restructure, feature, fix, or review, recommend the next skill

## Rules

### 1. Branch Names

- `restructure` for restructure/refactor tasks
- `feature` for development tasks
- `fix` for bug fixes
- `review` for review tasks

### 2. Safety

- Do not switch branches with uncommitted changes unless permitted
- Do not delete or force-push branches
- Use `git switch -c` only when the branch does not yet exist
- Use /run-deploy if needed

## Expected Outcome

- The working tree is on the correct workflow branch
- No uncommitted changes are lost
- The current branch and next action are reported clearly
