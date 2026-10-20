---
name: sql-performance-tuning
description: Diagnose slow queries; output a ranked tuning report (plan findings, index advice, before/after tests). Use when the user mentions slow query, execution plan, optimize SQL, query tuning, index advice, deadlock, MS-SQL/PostgreSQL/MongoDB performance.
---

# SQL Performance Tuning

Tune like a senior DBA on an air-cargo platform: high-volume event tables (AWB status, flight movements, ULD scans), skewed data (hub stations carry most rows), 24/7 operations. Evidence first, fixes ranked, every change measured.

Writing new queries, schema design, migrations → `database-engineering`. Readability refactors → `refactoring`. Application-code hot loops → `code-performance`.

## Inputs
- Query text (+ the slow parameter values), stored procedure, or ORM-captured SQL
- Execution plan: PostgreSQL `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`, SQL Server actual plan `.sqlplan` XML, Mongo `explain("executionStats")`
- Optional: row counts, index list, stats age, wait stats, `pg_stat_statements` / Query Store output, deadlock graph, Redis `SLOWLOG` / `--bigkeys`, DynamoDB/Cosmos metrics
- Engine and version

Trust in this order: actual plan > measured metrics > estimated plan > the user's description. Never fill gaps with invented numbers.

## Defaults (ask vs assume)
| Setting | Default if not stated | Ask only if |
|---|---|---|
| Engine | Inferred from syntax (`TOP`/`GETDATE()`/`NOLOCK` → SQL Server; `LIMIT`/`::`/`jsonb` → PostgreSQL) | Syntax is ANSI-only and advice differs |
| Version | SQL Server 2022 (compat 160) · PostgreSQL 16 · MongoDB 7 · Redis 7 | A fix is version-gated (PSP, `INCLUDE`, extended stats) |
| Environment | Production, shared, 24/7 | Never assume you may run heavy statements |
| Volume | Large: millions of rows, growing daily | Fix choice flips with volume |
| Target | "Faster" = lower p95 at current concurrency | The user states an SLA |

State engine + version + assumptions in the first line of the answer.

## Routing: read only what the task needs
| Task | Read |
|---|---|
| Any "it's slow" / symptom-first request | `references/playbook.md` |
| SQL Server plans, Query Store, DMVs, waits, sniffing, RCSI, blocking | `references/mssql-performance.md` |
| PostgreSQL EXPLAIN, pg_stat_statements, work_mem, stats, VACUUM, locks | `references/postgresql-performance.md` |
| MongoDB, Redis, DynamoDB / Cosmos DB | `references/nosql-performance.md` |
| Rewriting a query (SARGability, NOT IN, OFFSET, RBAR, DISTINCT) | `references/anti-patterns.md` |
| Report format | `templates/tuning-report-template.md` |

## Steps
1. **Collect evidence.** Query text + slow parameters, actual plan, row counts, stats age, waits, engine + version. List what is missing and give the exact command to get it (see engine reference); do not stop if a partial diagnosis is possible.
2. **Automate the first pass.**
   - Plan file: `python3 scripts/plan_analyzer.py PLAN_FILE [--rows 100000] [--top 5]` (auto-detects PG JSON vs SQL Server XML). Samples: `templates/sample-plan-postgres.json`, `templates/sample-plan-sqlserver.sqlplan`.
   - SQL text: `python3 scripts/sql_lint.py QUERY.sql` (or stdin; copied from database-engineering so this skill is self-contained).
   - Treat both outputs as leads; confirm each finding in the plan/code before reporting it.
3. **Baseline.** Record duration (p50/p95 or several runs), logical reads / buffers, rows, CPU, memory grant / spills, and the plan hash / queryid. Same parameters, warm and cold cache noted.
4. **Diagnose** with `references/playbook.md`: waiting or working? Blocked? Costliest node → first large estimate-vs-actual mismatch (bottom-up) → scans, lookups, spills, loops, conversions.
5. **Rank fixes** in this order and stop when the target is met:
   1. Rewrite (SARGable predicates, types, set-based, keyset paging) — `references/anti-patterns.md`
   2. Index (extend existing before adding; DDL + served query + write/storage cost)
   3. Statistics (update, sample size, extended/filtered stats)
   4. Plan stability (SQL Server PSP / RECOMPILE / Query Store forcing)
   5. Schema (partitioning for pruning/retention, summary tables)
   6. Config / hardware (`work_mem`, MAXDOP, memory, IO) — last, and only with plan evidence
6. **Measurement plan.** For each fix: what to run, which metric must move (reads, time, estimate accuracy, spills gone), test with the slow **and** typical parameters, and how to roll back.
7. **Write the report** with `templates/tuning-report-template.md`; run the self-check.

## Rules
- Never recommend an index without the exact query it serves, the key/INCLUDE order rationale, and its write + storage cost; check for overlapping existing indexes first.
- Missing-index DMV hints and green "missing index" text are **suggestions to verify**, never the answer.
- Never run, or tell the user to run, destructive or heavy statements on production (`DROP`, `DELETE`, `UPDATE`, `ALTER`, index rebuilds, `UPDATE STATISTICS ... FULLSCAN` on huge tables, `EXPLAIN ANALYZE` of DML, `DBCC FREEPROCCACHE`, `VACUUM FULL`) without explicit confirmation; mark them **Heavy** or **Destructive** and give the online / off-peak / staging alternative.
- Always measure before and after with the same parameters; no fix is "done" without the after numbers (or the plan to get them).
- State engine + version; flag version-gated features.
- Do not blame hardware, cloud tier, or "the server" until plans and waits have been read.
- No `NOLOCK` / `READ UNCOMMITTED` as a performance fix; no `OPTION (RECOMPILE)` on high-frequency statements without CPU cost noted.
- Never invent plan output, timings, row counts or gains; label expectations "expected, verify".
- Keep table, column, index and ID names exactly as given.
- Large DML: batch (e.g. 5 000 rows per transaction, keyed loop), never one giant transaction.

## Self-check
- [ ] Engine + version + assumptions in line 1
- [ ] Every finding cites evidence (plan node, metric, wait, or "needs:" plus the command to run)
- [ ] Fixes ranked rewrite → index → stats → config; no hardware blame without plan evidence
- [ ] Every index: DDL, served query, column-order reason, write/storage cost, overlap check
- [ ] Rewrites return the same result set (NULLs, duplicates, order) as the original
- [ ] Heavy/destructive statements flagged with confirmation request and rollback
- [ ] Before/after measurement plan present for each fix
- [ ] No invented numbers

## Output
Return the filled `templates/tuning-report-template.md`: Summary → Evidence → Findings table (# | Severity | Issue | Evidence | Fix | Expected gain | Risk) → rewritten SQL / index DDL → Before/After metrics (baseline filled, after = "to measure") → Rollback → Needs input. For a quick question (one anti-pattern), answer inline with a before/after snippet and the measurement to run.

Test cases for this skill: `evals/test-cases.md` (rerun after every edit).
