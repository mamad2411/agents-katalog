---
name: sql-sentinel
description: "Audit SQL for the cost & performance anti-patterns that burn warehouse credits. Catches SELECT *, full-table scans, non-sargable predicates, Cartesian joins, NULL-trap NOT IN, and 17 more rules. Scores warehouse health 0-100 and outputs a prioritized cost-reduction plan for BigQuery, Snowflake, Redshift, and Postgres."
category: data
risk: safe
source: self
source_type: self
date_added: "2026-06-26"
author: takeaseat
tags: [sql, bigquery, snowflake, redshift, postgres, data-warehouse, cost, performance, audit, optimization, analytics]
tools: [claude, cursor, codex, gemini, opencode]
license: "MIT"
---

# sql-sentinel

## When to use this skill

Use this skill whenever SQL cost, performance, or warehouse spend matters:
- A user writes or reviews a query for BigQuery, Snowflake, Redshift, Postgres, or Spark SQL.
- A user asks "why is this query so slow?" or "why is my warehouse bill so high?"
- A user is about to promote a dashboard query to production.
- A data engineer wants a second pair of eyes before a code review or a cost-optimization sweep.
- A team is running a "reduce cloud spend" or FinOps initiative.

Warehouse cost bugs are **silent and expensive** — a syntactically valid query that
scans 10x the bytes it needs to, or a cross join that turns a $0.02 query into a $200
query. This skill catches those before they reach production and the invoice.

## How it works

`sql-sentinel` ships a zero-dependency static-analysis engine
(`scripts/sql-sentinel.js`) that:

1. **Splits** a SQL script into statements (honoring single/double/dollar quotes,
   `--`, `/* */`, and `#` comments).
2. **Runs 22 rules** over each statement, each rule a documented cost/performance
   anti-pattern with a `why`, a concrete `fix`, and an `estSavings` estimate.
3. **Scores** warehouse health 0-100 (A-F), weighted by severity (critical 25,
   high 12, medium 5, low 1).
4. **Outputs a prioritized cost-reduction plan** — findings sorted by severity so you
   fix the most expensive problems first.

## Usage

### Programmatic (Node)
```js
const { auditSql } = require('./scripts/sql-sentinel');
const report = auditSql(yourSqlString, { dialect: 'bigquery' });
console.log(report.healthScore);   // 0-100
console.log(report.grade);         // 'A' | 'B' | 'C' | 'D' | 'E' | 'F'
console.log(report.prioritizedPlan); // array, worst-first
```

### CLI
```bash
node scripts/sql-sentinel.js path/to/query.sql        # pretty report
node scripts/sql-sentinel.js path/to/query.sql --json # machine-readable
cat query.sql | node scripts/sql-sentinel.js -        # read from stdin
```

### As a Claude Code skill
Copy this folder into `.claude/skills/` (or your agent's skills directory). When you
ask the agent to "audit this SQL for cost and performance", it will load this skill,
run the engine, and explain the findings with the rule's `why` and `fix`.

## The 22 rules (ruleset v1.0.0)

| Rule | Severity | What it catches |
|---|---|---|
| SQL001 | high | `SELECT *` forces full column scan (50-200x bytes on wide tables) |
| SQL002 | critical | No `WHERE` clause → full table scan |
| SQL003 | high | Leading-wildcard `LIKE '%term'` defeats indexes |
| SQL004 | high | Function wrapping a column (`LOWER(col)`) kills index usage |
| SQL005 | critical | `CROSS JOIN` / comma-join → Cartesian product |
| SQL006 | medium | `SELECT DISTINCT` forces full dedup sort/hash |
| SQL007 | medium | `ORDER BY` without `LIMIT` sorts the full result |
| SQL008 | high | `NOT IN (SELECT ...)` — NULL trap + anti-join hazard |
| SQL009 | medium | Implicit type cast in comparison |
| SQL010 | low | Multiple `OR`s — consider `IN` or `UNION ALL` |
| SQL011 | medium | `COUNT(DISTINCT ...)` — memory-heavy at scale (use HLL) |
| SQL012 | low | `LIMIT` without `ORDER BY` — non-deterministic results |
| SQL013 | medium | Scalar subquery in `SELECT` list (per-row execution risk) |
| SQL014 | medium | 5+ JOINs — broadcast/spill risk |
| SQL015 | high | Fact table (`*_events`/`*_log`) scanned without a partition filter |
| SQL017 | low | String concatenation (`||`/`CONCAT`) in SELECT list |
| SQL018 | medium | Window function `OVER ()` with no `PARTITION` (full sort) |
| SQL020 | critical | `DELETE`/`UPDATE` without `WHERE` — mass data change |
| SQL021 | low | `SELECT *` inside `EXISTS`/`IN` subquery (use `SELECT 1`) |
| SQL022 | medium | `UNION` (not `UNION ALL`) forces implicit dedup |

Every rule's full `why` and `fix` are embedded in the engine output and in
`scripts/sql-sentinel.js`.

## Run the tests
```bash
cd scripts && node test.js    # 26 tests, zero dependencies
```

## Honest limitations

- This is a **static** analyzer. It finds anti-patterns in the *text* of your SQL;
  it does not read your actual query plan, row counts, or warehouse billing. A flagged
  query on a 100-row table is cheap; the same query on a billion-row table is the
  problem the rule exists to prevent. Use your judgement.
- The fact-table heuristic (SQL015) keys off table *names* (`*_events`, `*_log`, etc.)
  and is advisory, not definitive.
- It does not execute SQL — safe to run on any `.sql` file.

## License

MIT — see `LICENSE` in the repo root. The Pro tier adds dialect-specific rules,
unused-column detection, and a CI hook; see the README.
