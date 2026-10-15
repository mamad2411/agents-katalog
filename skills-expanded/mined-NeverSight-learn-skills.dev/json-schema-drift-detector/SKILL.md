---
name: json-schema-drift-detector
description: Detects vendor-neutral JSON Schema drift between two versions and produces an actionable change report.
---

## When to invoke
- You maintain APIs/events/config schemas and need to understand what changed between two JSON Schema documents.
- You want a machine-readable summary of breaking vs non-breaking changes.

## Inputs needed
- `--old`: Path to the previous JSON Schema (draft-07 style supported).
- `--new`: Path to the new JSON Schema.
- Optional: `--out`: Path to write a JSON report.

## Workflow
1. Load both schemas.
2. Recursively index fields (JSON Pointer-like paths) for `type`, `required`, `enum`, and object `properties`.
3. Compute added/removed/modified paths.
4. Classify changes:
   - Breaking: removed field, type change, required added, enum narrowed.
   - Non-breaking: added optional field, required removed, enum widened, description/title-only updates.
5. Emit a summary and detailed diff entries.

## Output format
JSON object:
- `summary`: counts for breaking/non_breaking/unknown
- `breaking`: list of change objects
- `non_breaking`: list of change objects
- `unknown`: list of change objects

Each change object includes: `path`, `change_type`, `old`, `new`, `reason`.

## Guardrails
- Do not assume semantic compatibility beyond basic schema keywords; label ambiguous changes as `unknown`.
- Never modify input schemas.
- Treat missing `required` as empty.

## Reference code
Use `json_schema_drift_detector.py`.
