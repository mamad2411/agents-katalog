---
description: "Synapse Skill: Generates cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512) and UUIDs"
globs:
  - "skills/hash_generator/**"
alwaysApply: false
---

# Hash Generator Skill

Generates cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512) and UUIDs.

## Skill Location

`skills/hash_generator/`

## Handlers

| Runtime    | File | Entry Point |
|------------|------|-------------|
| TypeScript | `skills/hash_generator/index.js` | `export async function handler(params, context)` |
| Python     | `skills/hash_generator/main.py` | `async def handler(params, context)` |

## Supported Operations

- `hash`
- `uuid`

## Schema

The full JSON Schema is at `skills/hash_generator/hash_generator.skill.json`.

## Example

```json
{
  "operation": "hash",
  "data": "Hello World",
  "algorithm": "sha256"
}
```

## Tags

`hash` · `crypto` · `uuid` · `checksum`
