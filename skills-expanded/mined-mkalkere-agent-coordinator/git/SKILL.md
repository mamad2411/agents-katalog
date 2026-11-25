---
name: git
description: Git operations - branch, commit, push, merge
uses: []
requires:
  tools: [git]
---

# Git Operations

## When to Use

Any time you need to interact with git version control.

## Core Operations

### Check Status

```bash
git status
git branch --show-current
git log --oneline -5
```

### Create Feature Branch

Pattern: `<type>/<issue>-<description>`

```bash
git checkout main
git pull
git checkout -b feat/123-add-feature
```

Types:
- `feat/` - new feature
- `fix/` - bug fix
- `docs/` - documentation
- `refactor/` - code refactor
- `test/` - tests

### Stage Changes

**Never use `git add .` or `git add -A`** - always stage specific files:

```bash
git add path/to/file1.py path/to/file2.py
```

Or use interactive staging:
```bash
git add -p
```

### Commit

Format: `type(scope): description`

```bash
git commit -m "$(cat <<'EOF'
type(scope): short description

Longer explanation if needed.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Push

```bash
git push -u origin <branch-name>
```

### Switch Branches

```bash
git checkout <branch>
git checkout main && git pull
```

### Merge (local)

```bash
git checkout main
git merge <feature-branch>
git push
git branch -d <feature-branch>
```

## Safety Rules

1. **Never commit to main/master directly**
2. **Never force push to shared branches**
3. **Never use `git add .`** - stage specific files
4. **Always pull before starting work**
5. **Run tests before committing**

## Pre-Commit Checklist

Before every commit:
1. `git branch --show-current` - verify not on main
2. Run project linter/formatter
3. Run tests
4. `git diff --staged` - review what you're committing
5. Stage specific files only

## Completion

Git operation is complete when:
- Changes are committed (if committing)
- Changes are pushed (if pushing)
- Working directory is clean or intentionally dirty
