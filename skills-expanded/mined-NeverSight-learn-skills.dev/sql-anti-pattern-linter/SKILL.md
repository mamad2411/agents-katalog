---
name: sql-anti-pattern-linter
description: Vendor-neutral skill to lint SQL text for common anti-patterns and output actionable findings.
---

## When to invoke
- You want a lightweight, fast static check on SQL before review.
- You suspect performance issues from patterns like `SELECT *` or non-sargable filters.

## Inputs needed
- `--sql_file`: Path to a `.sql` file.
- `--out_json`: Path to write findings as JSON.

## Workflow
1. Read SQL text.
2. Run heuristic rule checks (regex-based):
   - `SELECT *`
   - `WHERE` clause using functions on indexed-looking columns (e.g., `LOWER(col)=...`)
   - Leading wildcard `LIKE '%foo'`
   - `OR` chains on same column
   - Implicit joins via comma in `FROM a, b`
   - `NOT IN (subquery)` null-trap risk
   - Missing `WHERE` on `UPDATE`/`DELETE`
3. Emit findings with rule id, severity, message, and line number when detectable.

## Output format
JSON with:
- `file`
- `findings[]`: `{rule_id, severity, message, line}`

## Guardrails
- Not a full SQL parser; results are best-effort.
- Do not auto-rewrite queries without human review.

## Reference code
- `sql_anti_pattern_linter.py`
