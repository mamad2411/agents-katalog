---
name: git-worktree-workflow
description: Manage git worktrees for branch isolation. Use when creating feature branches, working on isolated tasks, creating PRs, and cleaning up after merge.
version: 1.0.0
---

# Git Worktree Workflow

## Overview

Manage git worktrees for branch isolation within a single Claude session. Worktrees allow working on a feature branch in a separate directory while keeping the main repo untouched.

## Directory Structure

```
MainProjectDir/
├── ProjectDirApp/      # Main repo (claude runs here)
│   └── .claude/        # Claude settings & rules
└── ProjectWorkTree/    # Worktree (isolated branch work)
    └── .claude -> ../ProjectDirApp/.claude  # Symlinked
```

## Commands Reference

### Create Worktree

```bash
# From main repo directory
git worktree add ../WorktreeName -b branch-name

# Symlink Claude settings
ln -s ../CurrentRepoDir/.claude ../WorktreeName/.claude
```

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
git worktree remove ../WorktreeName
git branch -d branch-name  # Delete local branch
```

## Workflows

### Phase 1: Create Worktree

```
Step 1: Create worktree with new branch
        git worktree add ../WorktreeName -b feature/my-feature

Step 2: Symlink Claude settings
        ln -s "$(basename $(pwd))"/.claude ../WorktreeName/.claude

Step 3: Verify setup
        git worktree list
```

### Phase 2: Work in Worktree

```
Step 1: Work on files in ../WorktreeName/
        Use full paths: ../WorktreeName/src/file.ts

Step 2: Commit changes
        cd ../WorktreeName && git add . && git commit -m "message"

Step 3: Push branch
        cd ../WorktreeName && git push -u origin feature/my-feature
```

### Phase 3: Create PR

```
Step 1: Create pull request
        cd ../WorktreeName && gh pr create --base main --head feature/my-feature

Step 2: Return PR URL to user
        Wait for approval
```

### Phase 4: After Merge - Cleanup

```
Step 1: Return to main repo
        cd back to original repo

Step 2: Pull latest main
        git pull origin main

Step 3: Remove worktree
        git worktree remove ../WorktreeName

Step 4: Delete local branch
        git branch -d feature/my-feature

Step 5: Verify cleanup
        git worktree list
```

## Guidelines

### Do
- Symlink `.claude/` directory - never copy
- Use relative paths for symlinks (`../RepoName/.claude`)
- Cleanup after PR merge (remove worktree + delete branch)
- Work in worktree using full paths from main repo
- Return to main repo before cleanup operations

### Don't
- Copy `.claude/` directory (breaks updates)
- Use absolute paths for symlinks
- Leave worktrees after merge (clutters disk)
- Delete worktree before pushing changes

## Examples

### Example: Feature Development

```bash
# Create
git worktree add ../myapp-auth -b feature/oauth2
ln -s ../myapp/.claude ../myapp-auth/.claude

# Work (edit files in ../myapp-auth/)
cd ../myapp-auth
git add . && git commit -m "feat: add OAuth2 support"
git push -u origin feature/oauth2

# PR
gh pr create --base main --head feature/oauth2 --title "Add OAuth2" --body "..."

# After merge - Cleanup
cd ../myapp
git pull origin main
git worktree remove ../myapp-auth
git branch -d feature/oauth2
```

### Example: Bugfix

```bash
# Create
git worktree add ../myapp-fix -b bugfix/login-issue
ln -s ../myapp/.claude ../myapp-fix/.claude

# Work & PR
cd ../myapp-fix
# ... fix bug, commit, push, create PR ...

# Cleanup after merge
cd ../myapp
git worktree remove ../myapp-fix
git branch -d bugfix/login-issue
```

## Error Handling

### Worktree already exists
```bash
# Check existing worktrees
git worktree list

# Remove if stale
git worktree remove ../WorktreeName --force
```

### Branch already exists
```bash
# Use existing branch instead of -b
git worktree add ../WorktreeName existing-branch
```

### Unmerged changes in worktree
```bash
# Force remove (loses uncommitted changes)
git worktree remove ../WorktreeName --force
```

## Installation

Symlink the helper script (do not copy):

```bash
ln -s /path/to/skills/development/git-worktree-workflow/scripts/worktree.sh .claude/scripts/worktree.sh
```
