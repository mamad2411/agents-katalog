---
name: validate-dita-topic
description: Validates a DITA 1.3 topic file against structural and semantic rules derived from the official DITA 1.3 DTDs. Use this skill when you need to check a concept, task, reference, troubleshooting, glossentry, or base topic for missing required elements, incorrect nesting, duplicate IDs, malformed conref/keyref, or shortdesc quality issues. Returns structured JSON with errors and warnings.
compatibility: Python 3.9+. No third-party dependencies. Reads DTDs from dtd/ for reference only; validation is rule-based (not DTD-driven at runtime).
---

## Overview

Validates a DITA 1.3 XML topic and returns a JSON report listing all errors and warnings.

## Usage

```bash
# Validate a file
python scripts/validate_dita_topic.py path/to/topic.dita

# Pipe XML directly
cat topic.dita | python scripts/validate_dita_topic.py -

# Enforce a specific topic type (fails if root element doesn't match)
python scripts/validate_dita_topic.py topic.dita concept
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

Exit code is `0` when `is_valid` is `true`, `1` otherwise.

## Rules applied

See [references/RULES.md](references/RULES.md) for the full rule catalogue.

Key rules per type:

| Type | Required body | Key extra rules |
|---|---|---|
| concept | `<conbody>` | No task/ref elements inside conbody |
| task | `<taskbody>` | Each `<step>` needs `<cmd>`; singletons enforced |
| reference | `<refbody>` | `<property>` row quality checks |
| troubleshooting | `<troublebody>` | At least one `<troubleSolution>` |
| glossentry | *(n/a)* | `<glossterm>` and `<glossdef>` required |

## Common edge cases

- A topic with a valid root but no `@id` → Error (not Warning)
- `<shortdesc>` containing `<p>` or other block elements → Warning
- `@conref` without a `#` fragment separator → Error
- Duplicate `@id` values → Error (only first occurrence is valid)
- `<steps>` with more than 10 `<step>` children → Warning (split recommended)
