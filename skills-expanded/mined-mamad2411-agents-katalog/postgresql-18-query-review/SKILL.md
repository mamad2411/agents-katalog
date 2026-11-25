---
name: postgresql-18-query-review
description: Reviews PostgreSQL 18 SQL for correctness, performance, indexes, EXPLAIN plans, lock behavior, transaction impact, and safe schema inspection. Use when a task mentions SQL review, queries, indexes, query plans, EXPLAIN, slow queries, locks, foreign keys, lookup columns, or MCP schema inspection.
license: MIT
compatibility: PostgreSQL 18 release line; scripts require bash and git for changed-file hook scans.
---

# PostgreSQL 18 Query Review

Use this skill for SQL correctness review, index review, query plan review, lock behavior, and performance-sensitive query design.

## Start Here

1. Confirm the target is PostgreSQL 18.
2. Identify whether the query is read path, write path, report, migration, queue, or admin SQL.
3. Gather SQL text, bind values, schema, indexes, row counts, and representative data distribution.
4. Prefer PostgreSQL 18 `EXPLAIN` evidence for performance claims.
5. Use supporting files:
   - `resources/query-review-checklist.md`
   - `resources/index-review-guide.md`
   - `resources/mcp-toolbox-readonly-policy.md`
   - `examples/explain-review-template.md`
6. Run scripts with `--help` before using them:
   - `scripts/postgresql-18-index-required-check.sh`

## Review Principles

- Check correctness before performance.
- Require deterministic ordering for pagination, tests, exports, and user-visible result order.
- Avoid `SELECT *` in application-facing stable APIs.
- Review transaction scope and lock behavior for write queries.
- Tie index proposals to concrete predicates, joins, ordering, uniqueness, or operational behavior.
- Avoid redundant indexes and low-value indexes that add write amplification.
- Treat `EXPLAIN (ANALYZE)` on mutating SQL as dangerous unless explicitly approved.

## Workflows

Use `workflows/query-review-workflow.md` for SQL and index review.

## Expected Output

For query review tasks, provide:

- Correctness findings.
- Lock and transaction behavior.
- Index review.
- `EXPLAIN` interpretation when available.
- Recommendation with risks and validation steps.
