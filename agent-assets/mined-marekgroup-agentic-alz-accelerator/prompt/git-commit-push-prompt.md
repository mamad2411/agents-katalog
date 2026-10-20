---
agent: orchestrator
description: "Commit staged changes and push to remote"
---

# Git Commit & Push

Commit and push the current changes with a conventional commit message.

## Process

1. Run `git status` to see what changed
2. Stage all changes: `git add -A`
3. Write a conventional commit message:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `refactor:` for restructuring
   - `docs:` for documentation
   - `chore:` for maintenance
4. Commit and push

## Conventional Commit Format

```
<type>(<scope>): <short description>

<body — what changed and why>
```

Example: `feat(agents): add governance discovery prompt and instructions`
