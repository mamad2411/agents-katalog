---
name: ship
description: Complete shipping workflow - branch, commit by context, push, and create or update a PR. Also use when the user asks to commit and push or open a pull request from current work.
summary: Ship changes - auto branch if needed, commit files by context, push, and create or update a PR
read_when: User says "ship", "ship this", "ship it", "commit and push", or "create PR"
triggers:
  - ship
  - ship this
  - ship it
  - ready to ship
  - commit and push
  - push this
  - create pr
  - open pr
  - pull request
---

# Ship

Complete shipping workflow in one command.

## What It Does

1. **Branch** - If on main, create feature branch (feat/fix/refactor/docs)
2. **Commit** - Group files by context, commit separately with Conventional Commits
3. **Push** - Push to remote (set upstream if needed)
4. **PR** - Create or update pull request with `gh pr create`

## Partial Modes

Use the same skill for narrower shipping requests:

- **Commit + push only** - if the user explicitly does not want a PR yet
- **PR only** - if commits already exist and the branch just needs a PR
- **Current branch only** - if the user already created the branch manually

## Smart File Grouping

**Group together:**
- Component + test file
- Related functionality

**Commit separately:**
- Config files (package.json, tsconfig.json)
- Documentation (README.md, CHANGELOG.md)
- Dependencies
- Unrelated features

## Commit Message Format

Use Conventional Commits:
```
feat: add user authentication
fix: memory leak in WebSocket handler
refactor: simplify API error handling
docs: update README with setup instructions
chore: update dependencies
```

## Branch Naming

```
feat/description    # New features
fix/description     # Bug fixes
refactor/description # Refactoring
docs/description    # Documentation
```

## Workflow

```bash
# 1. Check branch
current_branch=$(git branch --show-current)
if [ "$current_branch" = "main" ]; then
  # Create feature branch (ask user or auto-generate)
  git checkout -b feat/new-feature
fi

# 2. Group and commit files
# Analyze git status, group by context
# For each group:
#   - Show files + generated message
#   - Ask confirmation
#   - git add <files> && git commit -m "message"

# 3. Push
git push -u origin $(git branch --show-current)

# 4. Create PR
gh pr create --title "..." --body "..." --base main
```

## Options

**Simple:**
```
"ship"
"ship this"
```

**Commit + push only:**
```
"commit and push"
"ship without PR"
```

**PR from current branch:**
```
"create PR"
"open PR for this branch"
```

**Custom branch:**
```
"ship on branch feat/new-feature"
```

## Example

```
User modifies:
  src/Button.tsx
  src/Button.test.tsx
  package.json
  README.md

User: "ship"

Agent:
  ✓ Create feat/add-button (was on main)
  ✓ Commit #1: Button.tsx + test
    "feat: add Button component with tests"
  ✓ Commit #2: package.json
    "chore: add button dependencies"
  ✓ Commit #3: README.md
    "docs: document Button component"
  ✓ Push feat/add-button
  ✓ PR #123 created
  
  https://github.com/user/repo/pull/123
```

---

**One command. Full workflow. Done.**
