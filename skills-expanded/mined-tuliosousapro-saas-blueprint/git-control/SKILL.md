---
name: git-control
description: Standardizes git operations, branch management, and disaster recovery. Use when committing, branching, or resolving conflicts. For commit formatting, see conventional-commits.
---

# Git Control Skill

## When to Use

- Whenever performing version control operations.
- When creating new features, fixing bugs, or managing releases.
- For resolving merge conflicts or recovering from mistakes.

## 1. Core Workflow

### Branching Strategy

- **Main Branch**: Production-ready code only.
- **Feature Branches**: `feat/[feature-name]` for new functionality.
- **Bug Fix Branches**: `fix/[bug-name]` for corrections.
- **Hotfix Branches**: `hotfix/[issue]` for urgent production fixes.

### Staging & Committing

- Always follow the [Conventional Commits](../conventional-commits/SKILL.md) skill.
- Stage only relevant changes: `git add <file>` (avoid `git add .` unless necessary).
- Review changes before committing: `git diff --staged`.

## 2. Common Operations

### Starting Work

```bash
git checkout main
git pull origin main
git checkout -b feat/my-new-feature
```

### Synchronizing

```bash
git fetch --all
git pull origin [branch-name]
git push origin [branch-name]
```

### Merging & Rebasing

- **Merge**: Use for combining long-lived branches.
- **Rebase**: Use to keep feature branches up-to-date with main and maintain a clean history.

  ```bash
  git checkout feat/my-feature
  git rebase main
  ```

## 3. Advanced Git Mastery

### Conflict Resolution

1. Identify files: `git status`.
2. Edit files to resolve `<<<<`, `====`, `>>>>` markers.
3. Stage resolved files: `git add <file>`.
4. Continue: `git commit` or `git rebase --continue`.

### Disaster Recovery

- **Undo last commit (keep changes)**: `git reset --soft HEAD~1`.
- **Undo last commit (discard changes)**: `git reset --hard HEAD~1`.
- **Find lost commits**: `git reflog`.
- **Revert a specific commit**: `git revert <commit-hash>`.

### Stashing

- Save work temporarily: `git stash push -m "work in progress"`.
- Retrieve work: `git stash pop`.

## 4. Quality Gates

- No merge commits on feature branches (prefer rebase).
- Each commit must pass linting and tests.
- Pull requests must be clear and focus on a single objective.
