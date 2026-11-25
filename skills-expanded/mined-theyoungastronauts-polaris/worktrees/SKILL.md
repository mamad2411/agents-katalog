---
name: worktrees
description: "Set up git worktrees for working on multiple independent features in parallel."
disable-model-invocation: true
---

# Using Git Worktrees for Parallel Development

> Inspired by [obra/superpowers](https://github.com/obra/superpowers), adapted for feature-based workflow.

## Overview

Git worktrees let you have multiple branches checked out simultaneously in separate directories. Each worktree is a full working copy with its own branch, dependencies, and state.

## When to Use

- Working on multiple **independent** features at the same time on an existing project
- Need to switch between unrelated tickets without stashing or losing context
- Want isolated workspaces so parallel features don't interfere with each other

## When NOT to Use

- **Initial MVP builds** — work directly on main, there's nothing to protect yet
- **Single features** — a regular branch is simpler and sufficient
- **Sequential phases that build on each other** — just commit on main or merge between phases

## Setup Flow

### 1. Verify Clean State

Before creating any worktrees, verify the source branch is clean:

```bash
# Ensure we're on the base branch (usually main or develop)
git checkout main
git pull origin main

# Verify clean working tree
git status --porcelain
# If not clean: stash or commit before proceeding
```

### 2. Choose Worktree Location

Worktrees are created as sibling directories to the repo within the project root. Example with two features in flight:

```
~/prj/my-project/
  api/                     # git repo (main branch)
  api-notifications/       # worktree (feature/notifications branch)
  api-billing/             # worktree (feature/billing branch)
  web/                     # git repo (main branch)
  web-notifications/       # worktree (feature/notifications branch)
```

Naming convention: `{repo-name}-{feature-name}` for clarity.

### 3. Create Worktree

```bash
# From the repo root
REPO_NAME=$(basename $(pwd))
FEATURE="notifications"

git worktree add "../${REPO_NAME}-${FEATURE}" -b "feature/${FEATURE}"
```

### 4. Install Dependencies

After creating a worktree, detect the project type and install dependencies:

```bash
cd "../${REPO_NAME}-${FEATURE}"

# Python
if [ -f "pyproject.toml" ]; then
  poetry install 2>/dev/null || pip install -e ".[dev]" 2>/dev/null
elif [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi

# Node.js
if [ -f "package-lock.json" ]; then
  npm ci
elif [ -f "yarn.lock" ]; then
  yarn install --frozen-lockfile
elif [ -f "pnpm-lock.yaml" ]; then
  pnpm install --frozen-lockfile
elif [ -f "package.json" ]; then
  npm install
fi

# Flutter/Dart
if [ -f "pubspec.yaml" ]; then
  flutter pub get
fi
```

### 5. Verify Clean Baseline

Run the test suite to confirm everything passes before making changes. This is critical — if tests fail before you start, you know it's not your fault.

```bash
# Python/Django
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
  pytest --tb=short -q
fi

# Node.js/Next.js
if [ -f "package.json" ]; then
  npm test -- --watchAll=false 2>/dev/null || npx jest --passWithNoTests 2>/dev/null
fi

# Flutter
if [ -f "pubspec.yaml" ]; then
  flutter test
fi
```

**If tests fail:** Report the failures. Ask whether to proceed anyway or investigate first. Do not silently continue with a broken baseline — that makes verification meaningless later.

**If tests pass:** Report readiness:

```
✓ Worktree ready: ../api-notifications
  Branch: feature/notifications
  Base: main (abc1234)
  Tests: 47 passing, 0 failures
  Ready for development
```

### 6. Install Skills (if using Polaris)

```bash
# From the worktree directory
polaris project --profile django-api
```

### 7. Generate VS Code Workspace

Generate a `.code-workspace` file so all active worktrees are accessible from a single VS Code window.

```bash
# From the project root (parent of repos)
PROJECT_DIR=$(pwd)

cat > "${PROJECT_DIR}/dev.code-workspace" << EOF
{
  "folders": [
    { "path": "api", "name": "API (main)" },
    { "path": "api-notifications", "name": "API - Notifications" },
    { "path": "api-billing", "name": "API - Billing" },
    { "path": "web", "name": "Web (main)" },
    { "path": "web-notifications", "name": "Web - Notifications" }
  ],
  "settings": {}
}
EOF
```

Only include folders that exist. Update this file as worktrees are created and removed.

Open with:

```bash
code "${PROJECT_DIR}/dev.code-workspace"
```

The sidebar shows each worktree as a labeled root with separate SCM panels per worktree.

## Working in Worktrees

### Switching Between Features

Each worktree is a regular directory. Switch between them like any other project:

```bash
cd ../api-notifications   # work on notifications
cd ../api-billing         # switch to billing
cd ../api                 # back to main
```

### Committing and PRs

Commits in a worktree happen on that worktree's branch. Normal git workflow applies:

```bash
git add .
git commit -m "feat(notifications): add push notification service"
git push origin feature/notifications
gh pr create --title "feat: add push notifications" \
  --body "Implements notification service and delivery queue."
```

## Cleanup

After a feature is merged and the PR is closed:

```bash
# From the main repo
git worktree remove ../api-notifications
git branch -d feature/notifications  # delete local branch
git worktree prune
```

## Listing Active Worktrees

```bash
git worktree list
# /home/tyler/prj/my-project/api                    abc1234 [main]
# /home/tyler/prj/my-project/api-notifications       def5678 [feature/notifications]
# /home/tyler/prj/my-project/api-billing              ghi9012 [feature/billing]
```

## Cross-Repo Worktrees

For features that span both backend and frontend repos:

```bash
# From the project root (~/prj/my-project/)
cd api
git worktree add ../api-notifications -b feature/notifications

cd ../web
git worktree add ../web-notifications -b feature/notifications
```

Then generate a single workspace file covering both repos and their worktrees (see step 7 above).

## Common Issues

**"fatal: is already checked out"** — You're trying to create a worktree for a branch that's already checked out somewhere. Use a new branch name.

**Shared node_modules/venv** — Each worktree has its own working directory but shares `.git`. Dependency directories (`node_modules`, `.venv`, `build/`) are per-worktree and need separate installs.

**IDE confusion** — Use the generated `.code-workspace` file to open all worktrees in a single VS Code window with proper isolation. Avoid opening worktrees individually within the same window without a workspace file.
