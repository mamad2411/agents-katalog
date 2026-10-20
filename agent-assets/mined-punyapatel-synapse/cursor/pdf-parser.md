---
description: "Synapse Skill: Extracts text content from PDF files provided as base64 data"
globs:
  - "skills/pdf_parser/**"
alwaysApply: false
---

# Pdf Parser Skill

Extracts text content from PDF files provided as base64 data.

## Skill Location

`skills/pdf_parser/`

## Handlers

| Runtime    | File | Entry Point |
|------------|------|-------------|
| TypeScript | `skills/pdf_parser/index.js` | `export async function handler(params, context)` |
| Python     | `skills/pdf_parser/main.py` | `async def handler(params, context)` |

## Supported Operations

- `extract_text`

## Schema

The full JSON Schema is at `skills/pdf_parser/pdf_parser.skill.json`.

## Example

```json
{
  "operation": "extract_text",
  "data": "<base64-pdf>"
}
```

## Tags

`pdf` · `extract` · `parse` · `text`
