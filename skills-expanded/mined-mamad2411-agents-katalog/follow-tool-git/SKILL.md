---
name: follow-tool-git
description: Use git commands per situation
argument-hint: "[scope]"
related:
  - follow-git-flow
  - follow-git-workflows
  - follow-tool-hk
  - follow-tool-moonrepo
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
---

## Goal

Use git in the project correctly and appropriately for the situation

## Scope

Use with every git project, whether local workflow, collaboration, or history investigation

- Latest: `git@2.55.0` (git-for-windows), `simple-git@4.0.1` / `isomorphic-git@1.42.2` / gh CLI `2.101.0` (verified 2026-09-26)
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Setup Repository

> Goal: prepare the repo for use

1. Use `git clone` for an existing repo
2. Use `git init` for a new project
3. Run `git config` to set user, editor, aliases
4. Check `git remote` and `git status`

### 2. Daily Workflow

> Goal: day-to-day work with branches and commits

1. Create a feature branch with `git branch` or `git switch -c`
2. Check `git status` and `git diff` before committing
3. Use `git add` and `git commit` with a clear message
4. Use `git stash` for temporary changes
5. Use `git push` or `git pull` with the remote

### 3. History And Inspection

> Goal: explore history and find the source of problems

1. Use `git log` to view commit history
2. Use `git blame` to find who changed which line
3. Use `git bisect` to find the commit that introduced a bug
4. Use `git reflog` to recover lost references

### 4. Collaboration And Integration

> Goal: work with the team and integrate work

1. Use `git rebase` to keep history linear
2. Use `git merge` to combine branches
3. Use `git cherry-pick` to take a specific commit
4. Use `git revert` to undo a wrong commit
5. Resolve `git conflict` carefully

### 5. Advanced Operations

> Goal: advanced git usage as needed

1. Use `git submodule` for external dependencies
2. Use `git lfs` for large files
3. Use `git tag` to mark releases
4. Set git hooks to check quality before commit — repos with `.moon/workspace.yml` → moon's `vcs.hooks` (see `/follow-tool-moonrepo`); other repos or advanced staged-file linting → `/follow-tool-hk`
5. Use `git worktree` to work on several branches at once
6. cleanup: `git clean -fd` removes untracked files, `git branch -d` deletes merged branches, `git remote prune`/`git fetch --prune` removes stale remote refs

## Rules

### 1. Safety First

- dry-run before rebase, reset, revert that could lose data
- never `--force` on shared branches
- resolve conflicts deliberately — verify before committing

### 2. Clean History

- one commit should do one thing
- write commit messages covering `what` and `why`
- rebase before merge if the team agrees

### 3. Verification

- run tests after rebase/merge/cherry-pick
- keep `git status` clean before pushing
- use `git diff` to review work before committing

- Use `/follow-git-flow` for the branching model
- Use `/follow-git-workflows` for team workflows
- Use `/follow-tool-hk` for git hooks in non-moon repos
- Use `/follow-tool-moonrepo` for `vcs.hooks` in moon repos
- Use `/follow-tool-usage` if needed
- Use `/follow-best-practice` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- git used correctly from daily workflow through advanced operations
- team history never damaged
- problems traceable with the history tools
- repo clean and easy to read
