---
name: smol-map
description: Build or incrementally update the project codemap at .smol/. Run when starting on a new project, or after large refactors.
---

# /smol-map

Delegate to the `mapper` agent.

Steps:
1. Check whether `.smol/codemap.json` exists.
2. If no → `mapper` runs `init`.
3. If yes → `mapper` runs `update`.
4. `mapper` then fills any new or changed `codemap.md` templates.
5. Report: how many folders mapped / refreshed, how many files indexed.
