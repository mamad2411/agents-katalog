---
name: sql-optimization-patterns
description: Safe SQL query diagnosis, EXPLAIN analysis, index and rewrite recommendations, and database health or security reviews for PostgreSQL, MySQL, and MariaDB. Use when Codex needs to investigate slow queries, interpret execution plans, review index design, run periodic performance checks, or propose low-risk optimization steps before any database change.
---

# SQL Optimization Protocol

Systematic, safe optimization of SQL queries on live systems. This is an operational protocol with a reference library. You already know SQL — this tells you how to operate without breaking things, and gives you ready-to-use templates so you don't generate common patterns from scratch.

This protocol is tool-agnostic. Execute discovery and diagnostic queries through whatever SQL interface is available (MCP database tools, CLI clients, application connections, ORMs). Adapt query syntax to your execution context but never skip the protocol steps.

### Integration with MCP Toolbox for Databases

Google's open-source [MCP Toolbox for Databases](https://googleapis.github.io/genai-toolbox/getting-started/introduction/) is an industry-standard MCP server that handles database connectivity, connection pooling, authentication, and exposes prebuilt tools for 50+ database engines. When available in the agent's environment, it serves as the **execution layer** for this skill.

**How they relate:** This skill is the decision-making protocol (what to do, when, and safely); the Toolbox is the execution interface (how to reach the database). The Toolbox provides atomic operations — `postgres-list-tables`, `postgres-list-query-stats`, `postgres-list-locks`, `mysql-get-query-plan`, etc. — useful for quick Phase 0/1 lookups. This skill provides what the Toolbox does not: risk classification, safety gates, business context requirements, EXPLAIN interpretation, fix patterns, multi-query impact analysis, security auditing, rollback protocols, and structured delivery.

**When the Toolbox is available:**
- Use its prebuilt tools for quick atomic lookups during Phase 0 (engine detection) and Phase 1 (schema discovery).
- For comprehensive diagnostics (health checks, index audits, security audits, performance reviews), prefer this skill's `scripts/` — they produce multi-section structured output that Toolbox's atomic tools don't replicate.
- The Toolbox handles connection management and auth; this skill handles the intelligence layer on top.

**When the Toolbox is NOT available:**
- Execute queries through whatever SQL interface exists (psql, mysql CLI, application DB connection, other MCP database tools).
- The protocol remains the same regardless of execution interface. Script coverage may vary by engine version, enabled extensions, and metadata privileges, so always read the header notes in the selected script.

**Reference library** (load only what the current phase needs):
- `references/discovery-queries.md` — Phase 1 & 3: schema, index health, write pressure, co-resident query templates
- `references/explain-cheatsheet.md` — Phase 2: plan node lookup, red flags, metric interpretation
- `references/fix-patterns.md` — Phase 3: ready-to-adapt SQL for common root causes
- `references/monitoring-queries.md` — Periodic reviews: top queries, table health, unused indexes, sessions

**Diagnostic scripts** (self-contained, L0 read-only — run as-is against the target database, subject to engine-specific extension and privilege notes in each file):
- `scripts/postgresql/health-check.sql` | `scripts/mysql/health-check.sql` | `scripts/mariadb/health-check.sql` — Full database health snapshot: sizes, bloat/cache, connections, locks, replication
- `scripts/postgresql/index-audit.sql` | `scripts/mysql/index-audit.sql` | `scripts/mariadb/index-audit.sql` — Unused, duplicate, overlapping/redundant, invalid or missing candidate indexes; write overhead
- `scripts/postgresql/security-audit.sql` | `scripts/mysql/security-audit.sql` | `scripts/mariadb/security-audit.sql` — Role privileges, cross-database access, public exposure, SECURITY DEFINER risks, SSL, RLS coverage where applicable
- `scripts/postgresql/performance-review.sql` | `scripts/mysql/performance-review.sql` | `scripts/mariadb/performance-review.sql` — Top queries, scan patterns, temp spill, config review, view candidates

**How to use scripts:** Identify the engine in Phase 0, then run the appropriate script through the available SQL interface. Do not use the MySQL scripts against MariaDB or vice versa. Scripts produce labeled sections (`section` column) — parse the output and feed findings into the protocol phases. Scripts never modify data.

**Validation notes for release quality:**
- The scripts and examples were checked against a lab harness using modern PostgreSQL and MySQL with BIRD real-world schemas.
- MariaDB now has dedicated scripts because several MySQL metadata assumptions do not hold on MariaDB.
- Some outputs are intentionally heuristic review candidates, especially duplicate/overlap index detection and view-candidate suggestions.
- Authentication posture, extension availability, and metadata visibility are environment-specific; treat missing sections as a coverage limitation, not as proof that the system is healthy.
- `laboratory/` in this repository is for local testing and validation only. It is not part of the installable skill and should not be copied into Codex's skills directory.

## Trigger Conditions

Activate when:
- A query is reported slow or timing out
- A periodic performance review is requested
- Schema or index design advice is needed
- An EXPLAIN plan needs interpretation
- N+1, pagination, or aggregation problems are suspected
- A database health check or security audit is requested
- Index audit or cleanup is needed

### Phase Routing

Not every request needs the full protocol. Route by request type:

| Request Type | Phases Required | References / Scripts to Load | Example |
|-------------|----------------|------------------------------|---------|
| Explain a plan | 0, 2 | explain-cheatsheet | "What does this EXPLAIN output mean?" |
| Read-only diagnosis | 0, 1, 2 | discovery-queries, explain-cheatsheet | "Why is this query slow?" |
| Fix proposal | 0, 1, 2, 3, 4, 5 | discovery-queries, explain-cheatsheet, fix-patterns | "Fix this slow query" |
| Periodic review | 0, 1 (batch), 2 (batch), 3, 5 | scripts/health-check + performance-review + index-audit, fix-patterns | "Monthly performance review" |
| Index design advice | 0, 1, 2B, 3 | discovery-queries, scripts/index-audit, fix-patterns | "Should I add an index for X?" |
| Health check | 0 | scripts/health-check | "How's the database doing?" |
| Security review | 0 | scripts/security-audit | "Audit database security" |
| Index audit | 0, 1 | scripts/index-audit | "Find unused or redundant indexes" |

When in doubt, run all phases. The cost of extra diagnosis is low; the cost of a wrong change is high.

## Risk Levels

Classify every action before executing it. Never escalate without explicit user approval.

| Level | Type | Examples | Reversibility | Requirement |
|-------|------|----------|---------------|-------------|
| L0 | Read-only inspection | EXPLAIN, schema queries, pg_stat_*, SHOW INDEX | None / safe | Proceed freely |
| L1 | Advisory (no DB change) | Query rewrite suggestions, app-code changes | N/A | Proceed freely |
| L2 | Additive DDL | CREATE INDEX, CREATE VIEW, CREATE MATERIALIZED VIEW | DROP reverses it, but creation may lock/load | User approval before execution |
| L3 | Mutative DDL | ALTER TABLE, DROP INDEX, repartition, REINDEX | Difficult/impossible to undo cleanly | User approval + rollback plan required |
| L4 | DML / Data mutation | UPDATE, DELETE, bulk migration, VACUUM FULL | Data loss possible | User approval + backup confirmation + staging validation required |

**Hard rules:**
- If you cannot classify an action's risk level, stop and ask.
- **EXPLAIN ANALYZE must only be used on SELECT statements.** For DML (INSERT, UPDATE, DELETE), EXPLAIN ANALYZE *executes* the statement — this means data modification. Use plain EXPLAIN (without ANALYZE) to inspect DML plans, or test DML on staging.
- **Never modify diagnostic scripts before execution.** The scripts in `scripts/` are validated L0 artifacts. If a script needs adaptation, copy and present the modified version for user approval before running — do not alter and execute in one step.

## Escalation & Stop Conditions

**Stop and escalate to the user when ANY of these are true:**

- Root cause is ambiguous after plan analysis (multiple plausible explanations)
- Business context is missing or unclear and the fix depends on it
- The EXPLAIN plan does not improve after applying a proposed fix
- You encounter engine behavior you cannot explain confidently
- The change would affect more than 3 tables or indexes
- Write-side impact cannot be estimated (no stats, no baseline)
- The query involves security-sensitive data (PII, financial, auth) and you're unsure about access patterns
- You are about to propose a second L2+ change to the same table in the same session
- You discover your connection has higher privileges than expected (e.g., superuser when only read access was stated)
- The target table has triggers or foreign key cascades that amplify the impact of a proposed change
- You are connected to a different database or schema than intended

**How to escalate:** State what you know, what you don't know, and what decision you need the user to make. Never fill gaps with assumptions.

## Protocol Phases

### Phase 0: Environment & Scope Lock

Before any diagnosis, establish these facts. Do not assume — query or ask.

**Required context (non-negotiable):**

1. **Engine & version** — PostgreSQL/MySQL/MariaDB + version number. Behavior differs.
2. **Environment type** — Production / staging / replica / local dev. This determines what you can run.
3. **Connection role** — Read-only? Read-write? Admin? Use least privilege possible.
4. **The problem statement** — Specific query, observed latency, expected latency, when it started.

**Verify environment programmatically — do not rely solely on user assertion:**
```sql
-- PostgreSQL: confirm primary vs. replica
SELECT pg_is_in_recovery();  -- true = replica, false = primary

-- MySQL: confirm replica status
SHOW REPLICA STATUS;  -- non-empty = replica

-- MariaDB:
SHOW SLAVE STATUS;  -- non-empty = replica (MariaDB <10.5 syntax)
```
If connected to production, verify the connection role cannot execute DDL. If it can, flag this as a security concern and refuse L2+ operations regardless of user approval.

**Environment constraints:**

| Environment | EXPLAIN | EXPLAIN ANALYZE (SELECT only) | DDL | DML |
|-------------|---------|-------------------------------|-----|-----|
| Production | Yes | Only with timeout guard | No — use staging first | No |
| Replica | Yes | Yes (read-only) | No | No |
| Staging | Yes | Yes (with timeout guard) | Yes (with approval) | Yes (with approval) |
| Local dev | Yes | Yes | Yes | Yes |

**Reminder: EXPLAIN ANALYZE executes the statement.** Only use it on SELECT queries. For INSERT/UPDATE/DELETE, use plain EXPLAIN.

**Timeout guard (always use in production/staging):**
```sql
-- PostgreSQL: wrap in transaction with timeout
BEGIN;
SET LOCAL statement_timeout = '3s';
EXPLAIN (ANALYZE, BUFFERS) <SELECT query>;
ROLLBACK;

-- MySQL: set session limit (NOTE: max_execution_time applies to SELECT only)
SET SESSION max_execution_time = 3000;
EXPLAIN ANALYZE <SELECT query>;  -- MySQL 8.0.18+
-- MySQL has no equivalent transaction-based guard for EXPLAIN ANALYZE.
-- If you need to analyze a DML plan on MySQL, use plain EXPLAIN (no ANALYZE).
```

### Phase 1: Context Acquisition

**You must understand the database and the business context before proposing any change.** Skipping this phase is how optimizations break systems silently.

#### 1A. Schema & Index Discovery (L0 — run freely)

Gather the structure around the target query's tables: columns, types, constraints, foreign keys, existing indexes, table size, and row estimates.

**Use templates from:** `references/discovery-queries.md` → Schema Discovery + Index Health sections.

#### 1B. Business Context (ask the user — never guess)

Before optimizing, understand WHY the query exists:

- **What operation does this serve?** (API endpoint, report, background job, migration)
- **What are the correctness requirements?** (Exact results? Approximate OK? Strong consistency needed?)
- **Are there SLA/latency targets?** (p99 < 200ms? Batch job must finish in < 1h?)
- **What writes hit the same tables?** (Adding an index speeds reads but slows every INSERT/UPDATE)
- **Are other queries/processes dependent on the same indexes or lock patterns?**
- **Is the data distribution uniform or skewed?** (A few users with millions of rows will behave differently)

**If the user cannot answer these questions, flag this as a risk.** Optimizing without business context means you're guessing.

### Phase 2: Diagnosis

Now analyze the problematic query.

#### 2A. Plan Analysis (L0)

Run EXPLAIN (not ANALYZE in production without timeout guard). Read the plan bottom-up.

**Use:** `references/explain-cheatsheet.md` for node types, metric interpretation, and red flags.

**Focus on these five signals:**

1. **Scan type on each table** — Sequential scan on a large table is the most common problem.
2. **Join strategy** — Nested loops with large outer sets are expensive. Hash/merge joins for large-large joins.
3. **Row estimate accuracy** — If estimated rows differ from actual by 10x+, statistics are stale or the planner is misled.
4. **Sort/temp operations** — Disk sorts, temp tables, and filesorts indicate memory pressure or missing indexes.
5. **Filter vs. Index Cond** — Rows filtered *after* fetch (Filter) waste I/O. Rows filtered *during* fetch (Index Cond) are efficient.

#### 2B. Root Cause Classification

Categorize the problem before proposing solutions:

| Root Cause | Signal | Typical Fix |
|-----------|--------|-------------|
| Missing index | Seq Scan / type=ALL on large table | Add targeted index (L2) |
| Wrong index chosen | Index scan but wrong index, or low selectivity | Composite/partial/covering index (L2) |
| Stale statistics | Row estimates wildly off | ANALYZE the table (L0-L1) |
| N+1 pattern | Many identical queries with different params | App-level: batch/JOIN (L1) |
| Expensive sort/temp | Sort node with disk spill, Using filesort | Index to support ORDER BY, or LIMIT push (L1-L2) |
| Large OFFSET pagination | Offset grows, query slows linearly | Cursor-based pagination (L1) |
| Correlated subquery | SubPlan executing per-row | Rewrite as JOIN/CTE/window (L1) |
| Lock contention | Not a plan issue — query waits, not runs | Investigate pg_stat_activity / SHOW PROCESSLIST (L0) |
| Over-fetching | SELECT * with unused columns | Select only needed columns (L1) |
| Implicit type cast | Index not used despite existing | Fix type mismatch in WHERE clause (L1) |

### Phase 3: Solution Design

#### Mandatory constraints for every proposed change:

1. **Minimal intervention** — The smallest change that solves the problem. Don't refactor a schema to fix a missing index.
2. **One change at a time** — Propose changes individually so impact is measurable.
3. **Write-side impact assessment** — Every index you add slows writes. Quantify: how write-heavy is the table? How large is the index?
4. **No semantic changes** — The optimized query MUST return identical results. If it doesn't, it's not an optimization, it's a rewrite that needs business validation.
5. **Engine-specific annotation** — If a solution is PostgreSQL-only or MySQL-only, say so explicitly.

#### Solution ranking (prefer top of list):

1. **L1 — Query rewrite** (no DB change): Fix app query, add proper WHERE, eliminate N+1, cursor pagination
2. **L1 — Statistics refresh**: ANALYZE the relevant tables
3. **L2 — Add index**: Targeted index for the specific query pattern
4. **L2 — Covering index / partial index**: When a basic index isn't enough
5. **L3 — Schema change**: Only when structural problems prevent optimization
6. **L3 — Partitioning / materialized views**: For truly large-scale problems

**Use templates from:** `references/fix-patterns.md` — grab the pattern matching the root cause, adapt to the target schema.

#### Multi-Query Impact Analysis (mandatory for L2+)

Before proposing any DDL change, assess collateral impact on other queries that touch the same tables.

**Why this matters:** Adding an index to speed up one SELECT can degrade a high-throughput INSERT path. Dropping an "unused" index might break a query that only runs monthly. Changing a column type can invalidate every query that touches it.

**Required steps:**

1. **Identify co-resident queries** — What other queries read from or write to the affected tables? Ask the user or use templates from `references/discovery-queries.md` → Co-Resident Query Detection.
2. **Classify write pressure** — Is this table write-heavy? Use templates from `references/discovery-queries.md` → Write Pressure Analysis.
3. **Check index overlap** — Does a similar index already exist? Would a composite index serve both the new and existing queries?
4. **Document co-impact** — In the delivery output, list other queries that will be affected (positively or negatively) by the proposed change.

**If co-resident query impact cannot be assessed, flag this explicitly in the delivery and recommend staging validation.**

#### DDL Safety & Lock Awareness (L2-L3)

Every DDL operation has lock implications. Know them before proposing.

**PostgreSQL:**
| Operation | Lock Level | Blocks Writes? | Blocks Reads? | Safe Alternative |
|-----------|-----------|----------------|---------------|-----------------|
| CREATE INDEX | ShareLock | Yes | No | CREATE INDEX CONCURRENTLY |
| CREATE INDEX CONCURRENTLY | ShareUpdateExclusiveLock | No | No | — (can fail, leaves invalid index) |
| ALTER TABLE ADD COLUMN (with default) | AccessExclusiveLock | Yes | Yes | PG 11+: no rewrite for non-volatile defaults |
| ALTER TABLE ALTER TYPE | AccessExclusiveLock | Yes | Yes | No safe shortcut — schedule maintenance window |
| DROP INDEX | AccessExclusiveLock | Yes | Yes | DROP INDEX CONCURRENTLY |
| REINDEX | ShareLock | Yes | No | REINDEX CONCURRENTLY (PG 12+) |
| VACUUM FULL | AccessExclusiveLock | Yes | Yes | Regular VACUUM (non-blocking) |

**MySQL/InnoDB:**
| Operation | Online DDL? (8.0+) | Blocks Writes? | Notes |
|-----------|-------------------|----------------|-------|
| ADD INDEX | Yes (ALGORITHM=INPLACE) | Brief lock at start/end | Monitor with `SHOW PROCESSLIST` |
| DROP INDEX | Yes | Brief lock | — |
| ADD COLUMN | Depends on position and type | Check version docs | ALGORITHM=INSTANT for trailing nullable columns (8.0.12+) |
| MODIFY COLUMN type | Usually requires rebuild | Yes during rebuild | Test on staging first |

**Pre-DDL checklist (mandatory for all L2+ operations):**
- **Verify no other DDL is in progress** on the target table. For replicated environments, confirm you are connected to the primary and assess replication lag impact.
- **Estimate index size:** Will it fit in available memory? Disk budget?
- **Check for long-running transactions:** A long-running transaction can block DDL that needs AccessExclusiveLock. Check `pg_stat_activity` / `SHOW PROCESSLIST` for old transactions before running DDL.
- **Concurrent CREATE INDEX failure (PostgreSQL):** If it fails, an invalid index remains. Check with `SELECT indexrelid::regclass, indisvalid FROM pg_index WHERE NOT indisvalid;` and drop invalid indexes before retrying. Note: `CREATE INDEX CONCURRENTLY` and `DROP INDEX CONCURRENTLY` cannot run inside a transaction — rollback must be a separate statement.
- **Backup verification for L3-L4:** Before executing any non-reversible change, confirm that a recent backup exists and has been tested. "Staging validation mandatory" is not sufficient if no backup is available.

#### Context Freshness Gate (mandatory before executing L2+)

Before executing any approved L2+ change, verify that your schema understanding is still current. Migrations, other team members, or automated processes may have changed the schema since your initial discovery.

**Quick freshness check:**
```sql
-- PostgreSQL: verify table structure hasn't changed
SELECT column_name, data_type FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = '<table>'
ORDER BY ordinal_position;

-- Compare index list to what you recorded in Phase 1A
SELECT indexname FROM pg_indexes WHERE tablename = '<table>';
```

**If the schema has changed since Phase 1:** Stop. Re-run Phase 1A on the affected tables. Your analysis may be invalidated.

#### Rollback Specification (mandatory for L2+)

Every L2+ proposal must include a complete, tested rollback block. Not a description — the exact SQL.

**Format:**
```
ROLLBACK PLAN:
  Condition: [when to trigger rollback — e.g., "write latency exceeds 2x baseline"]
  Command:
    <exact SQL to reverse the change>
  Verification:
    <query to confirm rollback succeeded>
  Notes: [any caveats — e.g., "CONCURRENTLY cannot run in a transaction"]
```

**L3-L4 operations that cannot be cleanly rolled back** (ALTER COLUMN TYPE, data migrations, DROP COLUMN) must be flagged with: `ROLLBACK: NOT CLEANLY REVERSIBLE — requires backup restore or forward-fix. Staging validation mandatory.`

### Phase 4: Validation

**Never declare success without evidence.**

#### 4A. Plan Comparison (before vs. after)

Show the EXPLAIN output for both the original and optimized query side by side. Key metrics to compare:

- Scan type changed (Seq Scan → Index Scan)
- Estimated cost reduced
- Actual time reduced (if ANALYZE is safe to run)
- Row estimates closer to reality
- Sort/temp operations eliminated

#### 4B. Semantic Equivalence Check

The optimized query must return identical results to the original. Use the appropriate verification method:

**Method 1 — Row count match (minimum bar):**
```sql
SELECT COUNT(*) FROM (<original_query>) AS orig;
SELECT COUNT(*) FROM (<optimized_query>) AS optim;
```

**Method 2 — Set difference (strong verification):**
```sql
-- PostgreSQL: should return zero rows
(<original_query> EXCEPT <optimized_query>)
UNION ALL
(<optimized_query> EXCEPT <original_query>);
```

**Method 3 — Row hash (for large result sets):**
```sql
-- PostgreSQL:
SELECT md5(string_agg(row_hash, ',' ORDER BY row_hash))
FROM (SELECT md5(CAST(ROW(col1, col2, col3) AS TEXT)) AS row_hash FROM (<query>) q) t;
```

**Edge cases to spot-check:**
- NULL handling (IS NULL vs = NULL, COALESCE behavior)
- Empty result sets (no rows should not become one row with NULLs after aggregation change)
- Ordering (if ORDER BY is specified, verify order is preserved)
- Floating-point precision (SUM/AVG on floats — compare with tolerance)

**If results differ in ANY way, the optimization is WRONG. Stop and investigate.**

#### 4C. Write Impact Verification (for L2+ changes)

If you added an index or changed schema, verify writes are not degraded unacceptably:
- INSERT/UPDATE/DELETE timing on the affected table
- Compare to pre-change baseline

### Phase 5: Delivery

#### For real-time troubleshooting, deliver:

```
PROBLEM: [one-line description]
ENVIRONMENT: [engine, version, env type]
ROOT CAUSE: [classification from Phase 2B]
TABLES INVOLVED: [with row counts and sizes]

CURRENT PLAN (summary):
  [key nodes, scan types, costs, actual times if available]

PROPOSED FIX:
  Risk Level: [L0-L4]
  Change: [exact SQL or code change]
  Expected Impact: [what changes in the plan]
  Write Overhead: [if applicable]
  Co-Query Impact: [other queries affected, positively or negatively]

ROLLBACK PLAN:
  Condition: [when to trigger]
  Command: [exact SQL]
  Verification: [confirmation query]

VALIDATION:
  [before/after plan comparison]
  [semantic equivalence confirmation]
  [write impact check if applicable]

CHANGE RECORD:
  Date: [timestamp]
  Table(s): [affected tables]
  Change Type: [L-level + description]
  Reason: [root cause reference]
  Applied By: [agent session / user]
  Status: [proposed | approved | applied | rolled back]
```

#### For periodic reviews, deliver:

Use `references/monitoring-queries.md` to gather data, then format:

```
REVIEW PERIOD: [date range]
ENVIRONMENT: [engine, version]

TOP QUERIES BY IMPACT:
  1. [query fingerprint] — mean: Xms, calls: Y, total: Zs
     Status: [needs optimization / acceptable / regression from last review]

RECOMMENDATIONS (prioritized):
  1. [change] — Risk: LX — Expected gain: X%
     Co-Query Impact: [assessment]
     Rollback: [command]
  2. ...

INDEX HEALTH:
  Unused indexes (candidates for removal): [list with sizes]
  Missing index candidates: [list with justification]

RISKS & NOTES:
  [anything the reviewer should know]

NEXT REVIEW: [suggested date]
```

## Boundaries — What This Skill Does NOT Do

- **Does not execute L2+ changes autonomously.** Always presents for user approval.
- **Does not redesign schemas.** Schema design is a business decision. This skill optimizes within existing structure.
- **Does not execute server configuration changes.** It may surface configuration risks in review output, but changing `work_mem`, `shared_buffers`, `innodb_buffer_pool_size`, and similar settings requires infrastructure-owner review.
- **Does not replace load testing.** EXPLAIN estimates are not production benchmarks.
- **Does not guess business logic.** If the purpose of a query is unclear, asks.
- **Does not proceed when uncertain.** See Escalation & Stop Conditions.
