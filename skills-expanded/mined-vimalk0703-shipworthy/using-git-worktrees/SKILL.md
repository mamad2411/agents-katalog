---
name: using-git-worktrees
description: Create isolated workspaces via git worktrees for parallel development. Safety verification ensures worktree directories are gitignored before use.
invoke_when: Use when working on a separate branch without stashing current work, doing parallel feature development, or when isolation is required for a task.
---

# Using Git Worktrees

## What Are Worktrees?

Git worktrees let you check out multiple branches simultaneously in separate directories. Each worktree has its own working directory but shares the same git history.

## When to Use

- Working on a hotfix while a feature is in progress
- Running tests on one branch while developing on another
- Isolating experimental changes from stable work

## Setup Pattern

### 1. Choose a Worktree Location
Check for project conventions:
- Look for `.worktrees/` directory
- Check CLAUDE.md or architecture.md for guidance
- Default: `.worktrees/` in project root

### 2. Safety Verification
Before creating a worktree:
- Ensure the worktree directory is in `.gitignore`
- If not, add it before proceeding

### 3. Create the Worktree
```bash
git worktree add .worktrees/feature-name -b feature/feature-name
```

### 4. Install Dependencies
Detect project type and install:
- Node.js: `cd .worktrees/feature-name && npm install`
- Python: `cd .worktrees/feature-name && pip install -r requirements.txt`
- Go: `cd .worktrees/feature-name && go mod download`

### 5. Run Baseline Tests
Before starting work, verify the worktree is healthy:
```bash
cd .worktrees/feature-name && npm test
```

## Cleanup

When done with a worktree:
```bash
git worktree remove .worktrees/feature-name
git branch -d feature/feature-name  # if merged
```

## Rules
- Never delete a worktree directory manually — use `git worktree remove`
- Don't modify the same branch from multiple worktrees
- Clean up worktrees when done to avoid confusion
