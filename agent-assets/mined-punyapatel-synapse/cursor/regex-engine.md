---
description: "Synapse Skill: Tests, matches, replaces and extracts text using regular expressions"
globs:
  - "skills/regex_engine/**"
alwaysApply: false
---

# Regex Engine Skill

Tests, matches, replaces and extracts text using regular expressions.

## Skill Location

`skills/regex_engine/`

## Handlers

| Runtime    | File | Entry Point |
|------------|------|-------------|
| TypeScript | `skills/regex_engine/index.js` | `export async function handler(params, context)` |
| Python     | `skills/regex_engine/main.py` | `async def handler(params, context)` |

## Supported Operations

- `test`
- `match`
- `replace`
- `extract`

## Schema

The full JSON Schema is at `skills/regex_engine/regex_engine.skill.json`.

## Example

```json
{
  "operation": "match",
  "pattern": "\\d+",
  "text": "abc 123 def 456",
  "flags": "g"
}
```

## Tags

`regex` · `pattern` · `match` · `replace`
