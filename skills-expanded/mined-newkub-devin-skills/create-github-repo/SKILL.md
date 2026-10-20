---
name: create-github-repo
description: Publish a local project that has no remote to a new GitHub repository
argument-hint: "[repo-name]"
related:
  - git-commit
  - git-push
  - update-gitignore

---

## Goal

Publish a local project that has no remote to a new GitHub repository

## Scope

- Works with the current directory, whether or not it already has `.git`
- Creates a new GitHub repo, adds a remote, commits, and pushes
- Does not cover repos that already have a remote (see `/git-push`)

## Execute

### 1. Validate Local Directory

> Goal: Check the state of the local repo before doing anything

1. Confirm you are in a project directory
2. Run `git status` if `.git` exists to see the state
3. If a remote already exists, stop and tell the user to use `/git-push`
4. Take `repo-name` from the argument, or fall back to the current folder name
5. Take visibility from the argument (default `--private`)

### 2. Initialize Git Repository

> Goal: The local directory has `.git`

1. If there is no `.git`, run `git init`
2. If there is no `.gitignore`, create a basic `.gitignore` suited to the project type
3. Run `git branch -M main`

### 3. Create GitHub Repository

> Goal: There is a remote repository on GitHub

1. Check `gh auth status`; if not logged in, stop and tell the user to run `gh auth login`
2. Run `gh repo create <repo-name> --<visibility>`
3. Extract the repo URL from the output
4. Run `git remote add origin <repo-url>`

### 4. Commit And Push

> Goal: All code is committed and pushed to the remote

1. Follow `/git-commit-and-push` to commit and push the changes
2. If `git-commit-and-push` fails → check `git status` and `git log`, then retry up to 1 time

### 5. Verify

> Goal: Confirm the repo is ready to use

1. Check that `git status` is clean
2. Run `gh repo view <repo-name> --json url,defaultBranchRef --jq .url`
3. Use `/open-web` to open the repo URL

## Rules

### 1. Repository Name

- Default to the current folder name
- If an argument is provided, use the argument instead
- Do not use names with special characters or spaces

### 2. Initial State

- If there are no commits yet, let `git-commit-and-push` handle the first commit
- If there are files that should be ignored, fix `.gitignore` before staging
- Do not run `git add .` directly; let `git-commit` handle staging

### 3. Safety

- Check `gh auth status` first
- Never force push
- If the repo already has a remote, stop and tell the user to use `/git-push`

- Use /update-gitignore if needed

## Expected Outcome

- The local project has `.git` and the `origin` remote
- The GitHub repository is created with the specified visibility
- All files are committed and pushed
- The repo page can be opened in a browser
