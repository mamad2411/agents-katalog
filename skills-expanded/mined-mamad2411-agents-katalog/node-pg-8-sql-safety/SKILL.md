---
name: node-pg-8-sql-safety
description: Reviews Node pg 8.x SQL safety, parameterization, dynamic SQL allowlists, sensitive database command usage, and database credential exposure.
license: MIT
compatibility: Node applications using Node pg 8.x and PostgreSQL.
---

# Node pg 8 SQL Safety

This skill guides security review for handwritten SQL in Node `pg` 8.x codebases.

## When to Use

Use this skill when the task involves:

- reviewing SQL injection risks
- converting concatenated SQL to parameterized SQL
- validating dynamic sort/filter/identifier logic
- reviewing database access logs and errors
- checking least-privilege role usage
- reviewing direct `psql`, migration, or database maintenance commands
- enabling MCP database tools

## Security Requirements

- Parameterize values.
- Allowlist dynamic identifiers.
- Keep database credentials out of source, shell history, logs, and hook output.
- Prefer least-privilege database users.
- Avoid data-changing MCP or direct database commands unless explicitly requested and reviewed.
- Treat production database access as sensitive, even for read-only queries.
- Redact values in logs and error messages.
- Review all `RETURNING *` and `SELECT *` usage for exposure.
- Ensure authorization predicates are in SQL, not only in caller code.

## Workflows

Use `workflows/sql-security-review-workflow.md` for SQL security reviews.

## Resources

Use `resources/security-checklist.md` during review.

## Examples

Use `examples/sql-injection-refactor-example.md` when replacing unsafe dynamic SQL.

## Scripts

Run scripts with `--help` before manual use. Antigravity hooks call these scripts automatically through `hooks.json`.

- `scripts/guard-pg-run-command.py`
- `scripts/review-pg-tool-use.py`
