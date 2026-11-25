---
name: database-connection-pooling
description: Sizes and configures database connection pools, and diagnoses exhausted pools, leaked connections and idle-in-transaction sessions.
---

# Database connection pooling

A pool protects the database. Bigger is rarely better.

## Steps

1. Collect facts: database max connections, number of app instances and workers, pool settings per process, and typical query time. Total possible connections = instances x workers x pool max. Compare to the database limit with headroom for admin and migrations.
2. Size it. A database does best with roughly (cores x 2) + disk spindles active connections. For most apps a pool of 10 to 20 per instance is plenty; if you need more, queries are too slow or transactions too long.
3. Set the pool knobs deliberately: max size, min idle, acquire timeout (fail in a few seconds, not minutes), max connection lifetime (shorter than any proxy or firewall idle timeout), and validation or keepalive.
4. Diagnose exhaustion: log pool wait time and active count. Look at the database view (`pg_stat_activity` or `SHOW PROCESSLIST`) for state, `xact_start` age and the query of sessions that are idle in transaction.
5. Find leaks: connections acquired and not released on error paths. Use the language's scoped form (context manager, try-with-resources, `using`, `defer`) everywhere.
6. Shorten transactions: no HTTP calls, file work or user waits between BEGIN and COMMIT. Set `idle_in_transaction_session_timeout` and a statement timeout.
7. For many instances or serverless, put an external pooler (PgBouncer in transaction mode, or a managed proxy) in front, and check that session features such as prepared statements and advisory locks still work.

## Rules

- Never fix exhaustion by only raising max size.
- Report the arithmetic, not just the numbers.

## Report

The current and proposed settings, the evidence for the cause, and the code fixes.
