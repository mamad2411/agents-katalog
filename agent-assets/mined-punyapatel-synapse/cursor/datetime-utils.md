---
description: "Synapse Skill: Parses, formats, converts timezones and calculates differences between dates"
globs:
  - "skills/datetime_utils/**"
alwaysApply: false
---

# Datetime Utils Skill

Parses, formats, converts timezones and calculates differences between dates.

## Skill Location

`skills/datetime_utils/`

## Handlers

| Runtime    | File | Entry Point |
|------------|------|-------------|
| TypeScript | `skills/datetime_utils/index.js` | `export async function handler(params, context)` |
| Python     | `skills/datetime_utils/main.py` | `async def handler(params, context)` |

## Supported Operations

- `now`
- `format`
- `diff`
- `convert_tz`

## Schema

The full JSON Schema is at `skills/datetime_utils/datetime_utils.skill.json`.

## Example

```json
{
  "operation": "now",
  "timezone": "Asia/Kolkata"
}
```

## Tags

`date` · `time` · `timezone` · `format`
