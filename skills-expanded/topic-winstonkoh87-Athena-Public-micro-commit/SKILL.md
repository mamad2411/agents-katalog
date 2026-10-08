---
name: micro-commit
description: Enforces strict, atomic commit hygiene. Splits large diffs into logical, revertible units.
argument-hint: "commit <directory>"
allowed-tools:
  - Bash
  - Read
auto-invoke: false
model: default
context_trigger: "commit, git, atomic commit, large diff, split commit, commit hygiene, PR too big"
---

# Micro-Commit Architect

Refuses to allow monolithic "blob" commits. Scans the current git diff and breaks down changes into atomized, logical steps.

## Triggers

"commit changes", "save my work", "micro commit"

## Core Mechanics

1. Runs `git status` and `git diff`.
2. Groups changes by feature, fix, or refactor.
3. Automatically executes individual `git add` and `git commit -m` steps for each logical block.

## Reference Paths

- `.context/memories/protocols/engineering/44-micro-commit-protocol.md`
