---
name: etl-lineage-explainer
description: Vendor-neutral skill for extracting and summarizing table-level lineage from SQL-based ETL jobs.
---

## When to invoke
- You have a folder of SQL files (or a single SQL script) that implements ETL/ELT.
- You need a quick, readable lineage view: sources → targets, plus joins/filters hints.
- You want a lightweight, vendor-neutral approximation (not a full SQL parser).

## Inputs needed
- Path to one SQL file or a directory containing `.sql` files.
- (Optional) Output path for a JSON summary.

## Workflow
1. Read each SQL file and strip comments.
2. Identify common ETL patterns:
   - `INSERT INTO <target> ... FROM <source>`
   - `CREATE TABLE <target> AS SELECT ... FROM <source>`
   - `CREATE VIEW <target> AS SELECT ... FROM <source>`
3. Extract:
   - Target object name
   - Source object names from `FROM` and `JOIN`
   - File name where found
4. Produce a consolidated lineage graph:
   - Targets with their sources
   - Reverse index: source → downstream targets
5. Emit both a human-readable markdown summary and machine-readable JSON.

## Output format
- JSON with:
  - `edges`: list of `{source, target, file}`
  - `targets`: `{target: {sources: [...], files: [...]}}`
  - `sources`: `{source: {targets: [...], files: [...]}}`
- Markdown summary printed to stdout.

## Guardrails
- Best-effort parsing only; do not claim completeness.
- Avoid inferring schema ownership or PII.
- Treat quoted identifiers and database-specific syntax conservatively.

## Reference code
- `etl_lineage_explainer.py`
