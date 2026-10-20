---
name: Global Agent Behavior
alwaysApply: true
description: General behavior rules for all coding workspaces.
---

# Global Agent Behavior

## Core behavior

- Follow the user's current scope exactly.
- Do not add features that were not requested.
- Do not reopen completed work unless the user explicitly asks.
- Do not repeat already agreed scope back to the user unnecessarily.
- Prefer small, targeted changes over broad rewrites.
- Preserve existing architecture unless there is a clear defect.
- When uncertain, inspect the existing code before proposing new files.
- Do not create parallel systems when an existing module can be extended.

## Communication

- Be direct and concise.
- State what changed, what was tested, and what remains open.
- Do not over-explain obvious steps.
- Do not claim something is done unless code/tests confirm it.
- If a task is blocked, name the exact blocker.

## Scope control

Before changing code, identify:

1. Existing relevant files
2. Existing conventions
3. Minimal change needed
4. Tests affected

Do not start unrelated refactors.
