---
description: "Synapse Skill: Audits HTML for frontend performance issues: blocking scripts, lazy loading, DOM size, inline styles"
globs:
  - "skills/performance_auditor/**"
alwaysApply: false
---

# Performance Auditor Skill

Audits HTML for frontend performance issues: blocking scripts, lazy loading, DOM size, inline styles.

## Skill Location

`skills/performance_auditor/`

## Handlers

| Runtime    | File | Entry Point |
|------------|------|-------------|
| TypeScript | `skills/performance_auditor/index.js` | `export async function handler(params, context)` |
| Python     | `skills/performance_auditor/main.py` | `async def handler(params, context)` |

## Supported Operations

- `analyze`

## Schema

The full JSON Schema is at `skills/performance_auditor/performance_auditor.skill.json`.

## Example

```json
{
  "operation": "analyze",
  "html": "<html><head><script src=\"app.js\"></script></head></html>"
}
```

## Tags

`performance` · `audit` · `speed` · `optimization`
