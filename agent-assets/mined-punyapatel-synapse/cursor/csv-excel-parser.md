---
description: "Synapse Skill: Parses and generates CSV/Excel data from structured input"
globs:
  - "skills/csv_excel_parser/**"
alwaysApply: false
---

# Csv Excel Parser Skill

Parses and generates CSV/Excel data from structured input.

## Skill Location

`skills/csv_excel_parser/`

## Handlers

| Runtime    | File | Entry Point |
|------------|------|-------------|
| TypeScript | `skills/csv_excel_parser/index.js` | `export async function handler(params, context)` |
| Python     | `skills/csv_excel_parser/main.py` | `async def handler(params, context)` |

## Supported Operations

- `parse`
- `generate`

## Schema

The full JSON Schema is at `skills/csv_excel_parser/csv_excel_parser.skill.json`.

## Example

```json
{
  "operation": "parse",
  "data": "name,age\\nAlice,30",
  "format": "csv"
}
```

## Tags

`csv` · `excel` · `parse` · `spreadsheet`
