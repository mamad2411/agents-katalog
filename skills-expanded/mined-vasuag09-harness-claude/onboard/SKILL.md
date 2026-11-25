---
name: onboard
description: Build a fast mental map of an unfamiliar codebase — structure, entry points, data flow, conventions, and where things live. Use when starting work in a new/unfamiliar repo, or to refresh context after time away. Supports maintenance.
---

# /onboard — map the codebase

Goal: understand a codebase enough to work in it, cheaply — without reading everything.

## Do this
1. **Structure first** — read the manifests (package.json / pyproject / README) and the
   top-level tree. Identify the stack, scripts, and entry points.
2. **Use the graph / `mgrep`** (or `Grep`/`Glob` if those are unavailable), not
   brute-force file reads: find the main modules, the
   request/data flow, and the seams (where layers meet).
3. **Conventions** — note the patterns the repo already uses (naming, error handling,
   state management, test layout). Future work must match the grain.
4. **Hot spots** — where is the core logic, where are the tests, where does config live,
   what's the build/run/test command.

## Output — a lean codemap
```
## Stack & run/build/test commands
## Entry points & main flow
## Module map (dir → responsibility)
## Conventions to follow
## Where to add things (tests, config, features)
```

Save it to the session file so later phases don't re-explore. Keep it to one screen.
