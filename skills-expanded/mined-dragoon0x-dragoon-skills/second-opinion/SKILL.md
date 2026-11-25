---
name: second-opinion
description: Build a structured packet to paste into another model or share with a colleague. Includes branch, head, recent commits, and optional file contents (max 5 files, 200 lines each). dragoon does NOT call other models for you - this is the prompt you copy. Use when stuck on an approach, considering tradeoffs, or wanting external review. Run as `node ~/.claude/skills/dragoon/skills/second-opinion/scripts/second-opinion.js "<topic>" [--file path]`.
version: 1.0.0
---

# /second-opinion

The packet you paste into the other model.

## When to use

- Stuck on an approach
- Choosing between two designs
- Want external review without writing the prompt from scratch

## Includes automatically

- git branch + head
- last 10 commits
- attached file contents (with --file)

## Run it

```
dragoon second-opinion "is this useEffect logic right" --file src/Hook.tsx --apply
dragoon second-opinion "should we cache this in memory or redis" --apply
```
