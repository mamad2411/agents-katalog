---
name: dev-mysql
description: MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends.
metadata:
  origin: ECC
---

# MySQL Patterns

Use this skill when working on MySQL or MariaDB schema design, migrations,
slow-query investigation, queue-style transactions, connection pools, or
production database configuration. Prefer exact version checks before applying a
feature-specific pattern because MySQL and MariaDB have diverged in several SQL
details.

## Activation

- Designing MySQL or MariaDB tables, indexes, and constraints
- Reviewing migrations before they run on large production tables
- Debugging slow queries, lock waits, deadlocks, or connection exhaustion
- Adding keyset pagination, upserts, full-text search, JSON columns, or queues
- Configuring application connection pools, read replicas, TLS, or slow logs

## Version Check

Start by identifying the engine and version:

```sql
SELECT VERSION();
SHOW VARIABLES LIKE 'version_comment';
```

Keep MySQL and MariaDB guidance separate when syntax differs:

- MySQL documents row aliases as the replacement for `VALUES(col)` in
  `ON DUPLICATE KEY UPDATE`; `VALUES(col)` is deprecated there.
- MariaDB documents `VALUES(col)` as the supported way to reference inserted
  values in `ON DUPLICATE KEY UPDATE`; use it for cross-engine compatibility.
- `SKIP LOCKED` is appropriate for queue-like work only. It skips locked rows
  and can return an inconsistent view, so do not use it for general accounting
  or integrity-sensitive reads.

## Topic Map

Load the reference file that matches the task before writing SQL or config:

| Task | Reference |
| --- | --- |
| Table design, column types, composite indexes, `EXPLAIN` review | `references/schema-and-indexing.md` |
| Upserts, keyset pagination, JSON columns, full-text search | `references/query-patterns.md` |
| Transactions, locking order, deadlocks, `SKIP LOCKED` queues | `references/transactions.md` |
| Application connection pools (SQLAlchemy, mysql2), pool sizing | `references/connection-pools.md` |
| Slow-log setup, `PROCESSLIST`, replicas, `my.cnf` starting points | `references/operations.md` |
| Users, grants, TLS, least-privilege review | `references/security.md` |

## Anti-Patterns

| Anti-Pattern | Risk | Better Pattern |
| --- | --- | --- |
| `SELECT *` in hot paths | Over-fetching and brittle clients | Select explicit columns |
| Deep `OFFSET` pagination | Linear scans and slow pages | Keyset pagination |
| No index on foreign-key joins | Slow joins and lock-heavy deletes | Index FK columns intentionally |
| Long transactions | Lock waits and large undo history | Commit small units of work |
| Direct DML against `mysql.user` | Grant-table corruption risk | Use `CREATE USER`, `ALTER USER`, `DROP USER` |
| Application user with admin grants | High blast radius | Least-privilege runtime user |
| Pool recycle above `wait_timeout` | Stale pooled connections | Recycle below timeout and pre-ping |
| Replica reads after writes | Stale user-facing state | Pin read-after-write flows to primary |

## Output Expectations

When this skill is used for review, return:

1. Engine/version assumptions.
2. Highest-risk correctness, lock, security, and migration issues.
3. Exact SQL or code changes for the safe path.
4. Validation plan: `EXPLAIN`, migration dry run, lock/deadlock check, and
   rollback criteria.
5. Any MySQL/MariaDB syntax differences that affect the recommendation.

## Related

- Skill: `postgres-patterns` - PostgreSQL-specific schema and query patterns
- Skill: `database-migrations` - migration planning and rollout safety
- Skill: `backend-patterns` - API and service-layer patterns
- Skill: `security-review` - secret handling, auth, and least privilege
- Agent: `database-reviewer` - broader database review workflow
