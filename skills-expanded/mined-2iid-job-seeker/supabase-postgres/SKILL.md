---
name: supabase-postgres
description: "Postgres PERFORMANCE reference: EXPLAIN plans, index selection, connection pooling, locking, VACUUM and bloat, and the SQL patterns behind them. A reference corpus, not a playbook — it is cited by this project's own skills and is deliberately not auto-invoked."
license: MIT
vendored_from: supabase/agent-skills
---

> **VANTRY DEFERENCE HEADER — read this before the upstream text below.**
>
> This is vendored third-party reference material. Where it touches an area this project already governs, the
> project's playbook wins and this file is the reference it reaches for:
>
> | area | who owns it here |
> |---|---|
> | authorization correctness, and its **executed allow AND deny tests** | `skills/rls-policy` |
> | any DDL against a live table — constraints, indexes, column changes | `skills/safe-migration` |
> | deciding whether to optimize at all (**a budget before an optimization**) | `skills/perf-profile` |
> | scheduled and queued work (`pg_cron`, `pgmq`) | `skills/background-job` |
> | rewriting existing rows, `pg_restore`, imports | `skills/data-backfill` |
> | the audit row, and the transaction it belongs to | `skills/audit-log` |
>
> Upstream's own description claimed to cover "RLS policies **and the tests that verify them**". It ships no
> tests. The claim is removed above; `rls-policy` is where that requirement lives.
>
> **Four of its rules are weaker than this project's.** They are listed in `CONFLICTS.md` beside this file,
> with the safe form for each. Read that file before following any DDL example below.

# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples:

```
references/query-missing-indexes.md
references/query-partial-indexes.md
references/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

## References

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
