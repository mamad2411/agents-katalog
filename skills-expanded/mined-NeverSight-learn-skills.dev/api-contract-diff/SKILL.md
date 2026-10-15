---
name: api-contract-diff
description: Vendor-neutral skill to compare two OpenAPI 3 specifications and produce a structured contract change report with breaking-change detection.
---

## When to invoke
- When you need to assess API changes between two versions of an OpenAPI 3.x spec.
- When you need to flag likely breaking changes (removed paths, removed operations, removed/changed required request fields, response schema removals).

## Inputs needed
- `--old`: Path to the older OpenAPI 3 JSON file.
- `--new`: Path to the newer OpenAPI 3 JSON file.
- Optional `--out`: Path to write a JSON report.

## Workflow
1. Load both OpenAPI documents (JSON).
2. Extract operations indexed by `(path, method)`.
3. Compare:
   - Added/removed paths and operations.
   - Parameter additions/removals (path/query/header).
   - Request body requiredness and JSON schema required properties.
   - Response status codes present/removed.
4. Label changes as `breaking`, `non_breaking`, or `unknown_risk`.

## Output format
JSON with:
- `summary`: counts of breaking/non-breaking/unknown.
- `breaking_changes`: list of items with `kind`, `location`, and `details`.
- `non_breaking_changes`: list of items.
- `unknown_risk_changes`: list of items.

## Guardrails
- Do not assume semantic meaning beyond what is expressed in OpenAPI.
- Mark schema-type changes as `unknown_risk` unless clearly breaking (e.g., removed required property).
- Prefer false positives over false negatives for breaking changes.

## Reference code
- `api_contract_diff.py`
