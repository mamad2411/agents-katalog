---
name: persistent-planning
description: "Persistent planning system with 3 markdown files (PLAN.md, PROGRESS.md, CONTEXT.md). Use when starting large features, multi-session work, or complex refactoring. Auto-tracks commits in PROGRESS.md."
user-invocable: false
---

# Persistent Planning System

## Overview

Use 3 persistent markdown files to track plans across sessions:

1. **`thoughts/PLAN.md`** - Active plan
2. **`thoughts/PROGRESS.md`** - Auto-tracked progress (commits)
3. **`thoughts/CONTEXT.md`** - Project context and constraints

## When to Create Plans

- Multi-file features (3+ files)
- Multi-session work
- Complex refactoring
- Architectural changes

## PLAN.md Format

```markdown
# Plan: [Feature Name]

## Goal
What we're building and why.

## Steps
1. [ ] Step one
2. [ ] Step two
3. [ ] Step three

## Constraints
- Must be backward compatible
- Must pass existing tests

## Status
IN PROGRESS | COMPLETED | BLOCKED
```

## CONTEXT.md Format

```markdown
# Project Context

## Architecture Decisions
- Using X because Y
- Chose A over B because C

## Key Files
- src/auth.ts - Authentication logic
- src/api/ - API endpoints

## Known Issues
- Rate limiting not implemented yet
```

## How It Works

- **Session start**: If `thoughts/PLAN.md` exists, it's injected into context
- **After commits**: `thoughts/PROGRESS.md` is auto-updated with commit hash and message
- **Plan completion**: Update PLAN.md status to COMPLETED

## Notes

- Plans are project-local (in the project's `thoughts/` directory)
- PROGRESS.md is append-only (never loses history)
- Add `thoughts/` to `.gitignore` if you don't want plans in version control
