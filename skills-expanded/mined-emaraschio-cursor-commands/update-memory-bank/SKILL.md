---
name: update-memory-bank
description: Sync memory bank with repository state
user-invocable: false
---
## Overview

Sync the memory bank with the current state of the repository and recent agent interactions. Run after significant work sessions, feature completions, or when context has drifted from reality.

## Memory Bank Files

Each file has a distinct responsibility. Update only what changed:

| File | Purpose | Update when... |
|------|---------|----------------|
| `activeContext.md` | Current state, recent commits, active work | After any meaningful commits |
| `progress.md` | Changelog, milestones, statistics | After feature completion |
| `techContext.md` | Tech stack, tools, environment | Tech stack changes |
| `systemPatterns.md` | Coding standards, patterns | New patterns established |
| `projectbrief.md` | Project purpose and scope | Rarely, only on major scope shifts |

## Steps

1. **Gather current state**
   - Run `git log --oneline -15` to capture recent commits
   - Note any new files, commands, or rules added since last update
   - Check `activeContext.md` "Last Updated" date to understand the gap

2. **Update each relevant file**
   - `activeContext.md`: Update "Last Updated" date, "Latest Commits" list, "Recent Focus Areas", and "Cursor Commands Inventory" count if it changed
   - `progress.md`: Add a changelog entry for the current month if work occurred; update statistics if counts changed
   - Other files: Only touch if their specific domain changed

3. **Verify accuracy**
   - Confirm commit hashes and descriptions match `git log` output
   - Remove stale "Active Work Items" that are now complete
   - Ensure statistics (command count, etc.) reflect reality

4. **Commit**
   - Use format: `docs(memory-bank): update memory bank with latest changes`
   - Stage only memory bank files: `git add .cursor/memory-bank/`
   - Push to remote after commit

## Guardrails

- Record only verified state; do not invent commits, files, or statistics.
- Update only the files whose domain changed; leave unchanged files alone.