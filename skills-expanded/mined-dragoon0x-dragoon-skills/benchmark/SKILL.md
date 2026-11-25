---
name: benchmark
description: Snapshot codebase metrics (file count, total lines, /critique scores) for trend tracking. Subcommands capture/list/compare/show. Snapshots stored as JSON in .dragoon/benchmarks/. Use to track design quality and codebase growth over time. Run as `node ~/.claude/skills/dragoon/skills/benchmark/scripts/benchmark.js <subcommand>`.
version: 1.0.0
---

# /benchmark

Track codebase metrics over time.

## When to use

- Weekly snapshot to watch trends
- Before/after a refactor
- The user says "track quality", "are we improving"

## Commands

```
dragoon benchmark capture          # take a snapshot
dragoon benchmark list             # list snapshots
dragoon benchmark compare          # compare latest two
dragoon benchmark show 2026-04     # show one matching prefix
```
