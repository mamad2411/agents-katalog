---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory Selection

Follow this priority order:

### 1. Check Existing Directories

```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory (.worktrees wins if both exist)

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md
```

**If preference specified:** Use it without asking

### 3. Ask User

If no directory exists and no CLAUDE.md preference:
```
No worktree directory found. Where should I create worktrees?
1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global)
```

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify directory is ignored before creating worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:**
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents.

### For Global Directory

No .gitignore verification needed - outside project entirely.

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup

```bash
# Auto-detect and run
if [ -f package.json ]; then npm install; fi
if [ -f pyproject.toml ]; then poetry install; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean.

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping ignore verification | Always use `git check-ignore` |
| Assuming directory location | Follow priority: existing > CLAUDE.md > ask |
| Proceeding with failing tests | Report failures + ask |
| Hardcoding setup commands | Auto-detect from project files |

## Red Flags - STOP

- Create worktree without verifying ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
