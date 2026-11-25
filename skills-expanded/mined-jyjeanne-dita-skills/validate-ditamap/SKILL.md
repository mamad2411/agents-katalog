---
name: validate-ditamap
description: Validates a DITA 1.3 map file against structural rules derived from the DITA 1.3 map DTD. Use this skill when you need to check topicref completeness (href or keyref required), key uniqueness, collection-type values, reltable structure, nesting depth, or broken reference patterns. Returns structured JSON with errors and warnings.
compatibility: Python 3.9+. No third-party dependencies. File-system href resolution requires all referenced .dita files to be present relative to the map file.
---

## Overview

Validates a DITA 1.3 `<map>` file and returns a JSON report listing errors and warnings.

## Usage

```bash
# Validate a map file
python scripts/validate_ditamap.py path/to/map.ditamap

# Pipe XML directly (href resolution disabled in pipe mode)
cat map.ditamap | python scripts/validate_ditamap.py -

# Exit code: 0 = valid, 1 = invalid
```

## Output schema

```json
{
  "is_valid": true,
  "errors": [
    { "element": "string", "rule": "string", "message": "string", "line": 0 }
  ],
  "warnings": [
    { "element": "string", "rule": "string", "message": "string", "line": 0 }
  ]
}
```

## Rules applied

See [references/RULES.md](references/RULES.md) for the full rule catalogue.

| Category | Key rules |
|---|---|
| Root | `<map>` required; `@id` recommended |
| topicrefs | `href` or `keyref` required on every `<topicref>` |
| Keys | `keys` values must be unique across the map |
| Collection-type | Must be `unordered`, `sequence`, `choice`, or `family` |
| Nesting | Warn if depth > 5 |
| Reltable | All `<relrow>` cells must match the number of `<relcolspec>` columns |

## Common edge cases

- A `<topicref>` with only `@keys` and no `href`/`keyref` → Warning (it's a valid key-only definition via `<keydef>` but unusual on plain `<topicref>`)
- `<navref>` does not require `href` or `keyref` — not flagged
- Nested maps (`<mapref>`) are noted but not recursively validated in single-file mode
