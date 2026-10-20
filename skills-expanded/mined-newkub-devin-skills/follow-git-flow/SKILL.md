---
name: follow-git-flow
description: Set up git flow: integration branch, local hooks, worktree convention, and AGENTS.md update
argument-hint: "[scope]"
related:
  - update-github-metadata
  - update-docs
  - ship
  - report
  - suggest-next-action

---

## Goal

Set up git flow in an existing repo: create the integration branch, configure local hooks, define the worktree convention, update `AGENTS.md`, and set GitHub protection
`/follow-git-flow` never runs `git init`, never runs `git config --global`, and never works on `main`

## Scope

Use first when starting a project or when git flow conventions need a reset
Supports solo and team use by blocking direct pushes to `main` with both local hooks and GitHub protection

If you only need remote GitHub setup → use `/update-github-metadata`
If you only need to create the integration branch → follow the Create Integration Branch steps below

## Execute

### 1. Pre-flight

> Goal: confirm you are in a git repo that has `main`

1. Run `git rev-parse --git-dir`
2. Run `git branch --list main` or `git branch --list master`
3. If there is no `main` or `master` → stop and report
4. Check that `git status --porcelain` is empty
5. If not empty → have the user run `/ship` first

### 2. Determine Integration Branch

> Goal: learn the integration branch name per project conventions

1. Read `AGENTS.md` if it has `### Ship` or `### Ship Flow`
2. If not → ask the user with `/ask-me` or use the default `integration`
3. Record the integration branch name as `<integration-branch>`

### 3. Create Integration Branch

> Goal: make the integration branch ready as the staging/integration branch

1. Check `git branch --list <integration-branch>`
2. If it exists locally → use `git switch <integration-branch>` then go to Ensure Remote
3. If it is not local but exists on the remote → use `git switch -c <integration-branch> origin/<integration-branch>`
4. If neither exists → use `git switch -c <integration-branch> <base-branch>`
5. Run `git push -u origin <integration-branch>` to ensure it exists on the remote

### 4. Setup Local Hooks

> Goal: prevent direct work/push on `main` locally

1. Create the `.githooks/` directory at the root
2. Create `.githooks/pre-commit`:
   ```sh
   #!/bin/sh
   branch=$(git rev-parse --abbrev-ref HEAD)
   if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
     echo "Do not commit directly on main. Use /ship."
     exit 1
   fi
   exit 0
   ```
3. Create `.githooks/pre-push`:
   ```sh
   #!/bin/sh
   while read local_ref local_sha remote_ref remote_sha; do
     if [ "$remote_ref" = "refs/heads/main" ] || [ "$remote_ref" = "refs/heads/master" ]; then
       echo "Direct push to main is not allowed. Use /ship."
       exit 1
     fi
   done
   exit 0
   ```
4. Run `git config --local core.hooksPath .githooks`
5. Run `git config --local core.filemode false` so Windows does not lock the executable bit
6. Run `git update-index --chmod=+x .githooks/pre-commit .githooks/pre-push` to record the executable bit in the git index
7. On Windows, if you do not use Git Bash, verify that `sh.exe` from Git for Windows is on the PATH, or use `.githooks/pre-commit.ps1` / `pre-push.ps1` instead

### 5. Setup Worktree Convention

> Goal: define the worktree layout for issue branches

1. Create the `worktrees/` directory at the root if it does not exist
2. Record the convention: an issue branch named `<integration-branch>/<number>` has its worktree at `worktrees/<integration-branch>-<number>/`
3. Do not create any worktree in this step

### 6. Setup GitHub

> Goal: configure branch protection and GitHub metadata

1. Run `/update-github-metadata` `### 6. Protect Branches` (see `update-github-metadata/references/branch-protection.md`)
2. If `/update-github-metadata` fails → report and stop
3. Confirm that `main` and `<integration-branch>` are protected

### 7. Update AGENTS.md

> Goal: write the ship section into `AGENTS.md`

1. Run `/update-agents-md` so `AGENTS.md` is updated
2. If `AGENTS.md` does not support Thai → write English per the convention

### 8. Report

> Goal: summarize the setup result

1. Use `/report` to summarize: integration branch, hooks, worktree, GitHub protection, AGENTS.md
2. Run `/suggest-next-action`

## Rules

### 1. No Global Git Config

- No `git init`
- No `git config --global`
- `core.hooksPath` must use `--local`

### 2. No Direct main Work

- No commits on `main`
- No direct pushes to `main`
- Local hooks must block both `pre-commit` and `pre-push`

### 3. Branch Naming

- Issue branches use `<integration-branch>/<number>`
- Do not use `issue/<number>` or `feature/*`
- `main` and `<integration-branch>` are the long-lived branches

### 4. Safety

- Check the working tree is clean before setup
- No force push
- Do not overwrite `.github` or `.githooks` without notice
- If `gh` is not available → `/update-github-metadata` will report it

### 5. Idempotent

- Can be re-run without side effects
- If the integration branch already exists → do not recreate it
- If hooks already exist → update only the missing parts
- Use /update-docs if needed


## Expected Outcome

- The integration branch is created from `main` and pushed to the remote
- `.githooks/pre-commit` and `.githooks/pre-push` block `main`
- `core.hooksPath` is set to `.githooks`
- The `worktrees/` directory is ready
- GitHub `main` and `<integration-branch>` are protected
- `AGENTS.md` has a complete `### Ship` or `### Ship Flow` section
- No git init or global config is created
- There is a result report and a next action
