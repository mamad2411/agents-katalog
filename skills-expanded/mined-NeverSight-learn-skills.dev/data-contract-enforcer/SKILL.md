---
name: data-contract-enforcer
description: Use to validate dbt models or warehouse tables against a data contract YAML. Checks columns, types, nullability, freshness, row-count bounds, and uniqueness. Emits a CI-friendly report and exits non-zero on violations.
---

# Data Contract Enforcer

## When to invoke
- "Run the data contract for fct_orders before merge."
- "Check the contracts of all models in CI."
- "Validate freshness on dim_users."

## Inputs needed
1. **Contract YAML** — describes expected schema, freshness, and constraints.
2. **Connection** — Snowflake / BigQuery / DuckDB / Postgres (DuckDB used for examples).

## Workflow
1. **Load** the contract.
2. **Inspect** the live table.
3. **Diff** schema (columns + types + nullability).
4. **Run** assertions: freshness, row-count bounds, uniqueness, allowed values.
5. **Report** — Markdown + JSON; exit code 0 (pass) or 1 (violations).

## Contract format
```yaml
table: analytics.fct_orders
owner: data-eng@acme.com
freshness:
  column: created_at
  max_lag_minutes: 120
columns:
  - name: order_id
    type: VARCHAR
    nullable: false
    unique: true
  - name: amount
    type: DECIMAL
    nullable: false
    min: 0
row_count:
  min: 1000
```

## Guardrails
- Default behavior on violation: exit 1, print Markdown report to stdout.
- Never auto-fix the warehouse — only report.
- Treat schema drift as ERROR, freshness lag as WARN unless `strict: true`.

## Reference code
`enforce.py` runs the contract against DuckDB by default; supports a `--dsn` flag for other warehouses via SQLAlchemy.
