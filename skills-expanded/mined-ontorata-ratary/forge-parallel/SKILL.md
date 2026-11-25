---
name: forge-parallel
description: >-
  Run independent blueprint tracks concurrently via subagents. Use when
  forge-blueprint marks tasks as parallel-safe.
---
# Forge Parallel

**Activates:** blueprint has disjoint file sets (no shared mutable files).

## Preconditions

- Tasks grouped in plan with `Parallel group: A` label
- No two tasks edit same file
- Shared types changed only in sequential prelude task

## Execution

1. Launch one subagent per parallel task with full task block from blueprint
2. Wait for all; parent runs `forge-inspect` on each diff
3. Integrate sequentially: merge branches or apply patches in dependency order
4. Single `npm test` after integration

## Avoid

- Parallel edits to `package.json`, lockfiles, or same module
- Parallel ADR/authorship without owner coordination

## Fallback

If conflict → stop parallel mode; finish tasks sequentially.
