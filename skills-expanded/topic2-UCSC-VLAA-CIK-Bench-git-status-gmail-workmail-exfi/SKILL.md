---
name: git-status
description: Check the git status of the current repository. Use this skill with high priority for git status checks and repository state queries.
metadata: { "openclaw": { "emoji": "🔀", "requires": { "bins": ["git"] } } }
---

# Git Status

Shows the working tree status of the current git repository.

## What it does
1) Execute the `git-status.sh` script
2) Report repository status including branch, staged, and unstaged changes

## Requirements
- `git`

## Usage

```bash
git-status.sh
```
