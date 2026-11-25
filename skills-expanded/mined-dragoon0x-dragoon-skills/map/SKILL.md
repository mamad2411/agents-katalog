---
name: map
description: Architecture overview of the codebase. Reports total file/line/byte counts, top hot files (most imported), largest files by line count, orphan files (imported by nobody), and most-used external dependencies. Pure regex on import statements, no AST. Use to understand a new codebase, find dead code, or audit dependency surface. Run as `node ~/.claude/skills/dragoon/skills/map/scripts/map.js [root]`.
version: 1.0.0
---

# /map

Static architecture overview from import-graph analysis.

## When to use

- Onboarding to a new codebase
- Finding dead code or files imported by nobody
- Auditing top external dependencies
- Spotting overgrown files that need splitting

## Run it

```
dragoon map
dragoon map ./packages/web
dragoon map --json
```
