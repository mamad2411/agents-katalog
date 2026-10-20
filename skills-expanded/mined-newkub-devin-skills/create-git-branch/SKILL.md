---
name: create-git-branch
description: Create a new git branch the right way
argument-hint: "[branch-name]"
related:
  - cleanup
  - delete
  - ship

---

## Goal

Create a new branch from the correct base, with a sensible name

## Scope

Use before starting a feature, bugfix, hotfix, or experiment

## Execute

### 1. Determine Base

> Goal: Determine Base

1. Identify the default branch (main/master)
2. Check that the base branch is up to date
3. Pull the latest first if needed

### 2. Choose Naming

> Goal: Choose Naming

1. `feature/<ticket>-description`
2. `bugfix/<ticket>-description`
3. `hotfix/description`
4. `experiment/description`
5. Use lowercase, separated by `-`

### 3. Create And Switch

> Goal: Create And Switch

1. `git switch -c <branch>`
2. Verify you are on the correct commit
3. Push upstream with `git push -u origin <branch>`

### 4. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` doesn't pass → report the status

## Rules

- Create from the latest default branch
- Give branches meaningful names
- 1 branch per 1 concern
- Do not create duplicate branches

- Use /cleanup-git-branch if needed
- Use /delete-git-branch if needed

## Expected Outcome

- A new branch exists on the latest base
- The branch name follows convention
- You are now on the new branch
