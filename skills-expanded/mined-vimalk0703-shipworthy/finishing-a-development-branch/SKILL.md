---
name: finishing-a-development-branch
description: 5-step branch completion workflow — verify tests, determine base branch, present merge options, execute, and clean up.
invoke_when: Use when finishing a feature branch, merging completed work, or when the user says they are done with a branch.
---

# Finishing a Development Branch

## The 5-Step Completion Workflow

### Step 1: Verify Everything Passes
Before any merge activity:
- Run the full test suite — ALL tests must pass
- Run the build — zero errors
- Run the linter — zero errors
- This is non-negotiable. Do NOT skip to step 2 with failing tests.

### Step 2: Determine the Base Branch
- Check what branch this was branched from
- Usually `main` or `develop`
- Verify the base branch is up to date: `git fetch origin`
- Check for conflicts: `git diff main...HEAD`

### Step 3: Present Options
Tell the user their options:
1. **Merge commit**: `git merge --no-ff` (preserves branch history)
2. **Squash merge**: `git merge --squash` (clean single commit)
3. **Rebase and merge**: `git rebase main` then fast-forward merge
4. **Create PR**: push and create a pull request for review

Recommend based on:
- Single logical change → squash
- Multiple meaningful commits → merge commit
- Needs review → PR

### Step 4: Execute
Carry out the user's chosen strategy. If creating a PR, use `gh pr create` with a clear title and description.

### Step 5: Clean Up
After successful merge:
- Delete the local branch: `git branch -d feature/branch-name`
- Delete the remote branch (if applicable): `git push origin --delete feature/branch-name`
- Remove worktree (if used): `git worktree remove .worktrees/branch-name`
- Verify main is clean: `git checkout main && git pull && npm test`
