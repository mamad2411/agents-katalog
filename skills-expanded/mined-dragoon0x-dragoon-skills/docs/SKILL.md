---
name: docs
description: Detect drift between markdown docs (README, docs/) and the actual codebase. Catches references to npm scripts that don't exist, scoped dependencies not in package.json, file paths in backticks that don't resolve on disk, and undocumented npm scripts. Use to audit documentation hygiene before a release or after a major refactor. Exits non-zero on findings. Run as `node ~/.claude/skills/dragoon/skills/docs/scripts/docs.js`.
version: 1.0.0
---

# /docs

Detects drift between your documentation and your code.

## When to use

- Auditing docs before a release
- After a major refactor that may have invalidated examples
- The user says "check docs", "audit the README", "find stale references"

## Rules

- `docs-001` npm scripts referenced in docs that don't exist (`medium`)
- `docs-002` scoped dependencies referenced that aren't installed (`low`)
- `docs-003` file paths in backticks that don't exist on disk (`medium`)
- `docs-004` npm scripts that aren't documented anywhere (`low`)

Each finding includes the markdown file, line, column, snippet, message, and a fix.

## Run it

```
dragoon docs                       # all severities
dragoon docs --severity medium     # focus on the actionable ones
dragoon docs --json                # CI mode
```

## Exit codes

- `0` no drift
- `1` drift detected
- `2` bad usage
