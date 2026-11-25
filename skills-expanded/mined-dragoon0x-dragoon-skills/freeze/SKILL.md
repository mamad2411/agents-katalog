---
name: freeze
description: Declare directories that are off-limits to edits. Stores the list in .dragoon/freeze.json. Optionally installs a git pre-commit hook that fails the commit if any frozen path is touched. Subcommands list/add/remove/hook/check. Use when isolating a refactor, locking legacy directories, or onboarding a contributor with limited scope. Run as `node ~/.claude/skills/dragoon/skills/freeze/scripts/freeze.js <subcommand>`.
version: 1.0.0
---

# /freeze

Declare directories off-limits.

## When to use

- During a refactor in one part of the codebase, freeze the rest
- Onboarding a contributor with bounded scope
- Locking legacy directories that nobody should edit

## Commands

```
dragoon freeze list
dragoon freeze add src/legacy --apply
dragoon freeze remove src/legacy --apply
dragoon freeze hook --apply              # writes a pre-commit script
dragoon freeze check                     # CI-friendly check
```

## Enforcement

- by default, dragoon does not block edits at runtime
- with `freeze hook --apply` and a pre-commit symlink, commits to frozen paths fail
- override with `git commit --no-verify` (so the hook is a soft fence, not a wall)
