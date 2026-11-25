---
name: registry-search-table-output
description: Render search results as a fixed-width table with colored type labels.
---

# Registry Search Table Output

Render search results as a fixed-width table with colored type labels.

## When to Use

Use this skill when:

- Working with code in `src/commands/search.ts/`
- User mentions "search"
- User mentions "table"
- User mentions "chalk"
- User mentions "limit"
- User mentions "type"

## Patterns

- chalk-based fixed-width table formatting
- type-aware coloring (agent vs skill)
- limit and type filters via options

## Examples

```
agentsmith search <query> -t agent -l 10
```

## Category

**quality** - Testing, validation, and code quality
