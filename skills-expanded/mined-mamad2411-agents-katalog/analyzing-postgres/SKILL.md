---
name: analyzing-postgres
description: PostgreSQL database analysis, performance tuning, and health monitoring. You MUST read this entire skill document before executing any PostgreSQL operations — it contains mandatory workflows, safety constraints, and two-phase execution rules that prevent common errors like hallucinated column names and unsafe queries.
connection_type: postgres
preload: false
---

# Analyzing PostgreSQL

## Discovery

<critical>
**If no `[cached_from_skill:analyzing-postgres:discover]` context exists, run discovery first:**
```bash
bun run ./_skills/connections/postgres/analyzing-postgres/scripts/discover.ts
bun run ./_skills/connections/postgres/analyzing-postgres/scripts/discover.ts --max-tables 100 --sampling true --timeout 120
bun run ./_skills/connections/postgres/analyzing-postgres/scripts/discover.ts --alias prod-db
```
For multi-instance setups, run discovery per-alias. If no alias is provided with multiple instances, the error will list available aliases.
Output is auto-cached.
</critical>

**What discovery provides:**
- Database overview from `get_database_overview()`:
  - `schemas`: List of database schemas
  - `tables`: Tables with names, row counts, sizes, and column information
  - `indexes`: Index information and statistics
  - `relationships`: Foreign key relationships between tables
  - `size_info`: Database and table size metrics
  - `security`: Security score (0-100), superuser count, SSL status, issues and recommendations
  - `performance_hotspots`: Tables with high sequential scans, dead tuples, bloat, or high modification rates

**Discovery options (script defaults, NOT MCP server defaults):**
- `--max-tables N`: Limit tables analyzed (script default: 50, MCP server default: 500)
- `--sampling true`: Use sampling for large tables (script default: false, MCP server default: true)
- `--timeout N`: Timeout in seconds (script default: 60, MCP server default: 300)
- `--alias <name>`: Target a specific postgres instance (required for multi-instance workspaces)

**Why run discovery:**
- Get actual table/column names (never guess - they vary between databases)
- Understand relationships before writing JOINs
- Identify large tables that need sampling
- Know schema structure before executing SQL

**ALWAYS use `format()` for output (40-60% token savings):**
```typescript
import { format } from "@connections/_utils/format";
console.log(format(result)); // CORRECT
console.log(JSON.stringify(result, null, 2)); // WRONG
```

## Two-Phase Execution (MANDATORY)

<critical>
**Discovery and query MUST be separate script executions.**

**Phase 1 - Discovery Script:**
```typescript
const schema = await get_object_details({ schema_name: "public", object_name: "user", object_type: "table" });
console.log(format(schema));
// ⛔ STOP - End script here, read output
```

**[CHECKPOINT: Read output, identify actual column names]**

**Phase 2 - Query Script (NEW execution):**
```typescript
// Use ONLY verified column names from Phase 1
const results = await execute_sql({ sql: `SELECT verified_col FROM ...` });
```

❌ **FORBIDDEN:** `get_object_details()` + `execute_sql()` in same script
</critical>

| Bad ❌ | Good ✅ | Why |
|--------|---------|-----|
| Discovery + query in one script | Two separate scripts | Prevents hallucinated column names |
| Assuming `user_id` exists | Run `get_object_details()` first | Foreign key naming varies |
| `created_at`, `updated_at` | Verify columns exist | May be named differently |
| Writing JOINs without discovery | Discover ALL tables first | Relationships vary |

## Tools (13 total)

**Schema (3):** `list_schemas()`, `list_objects(schema, type?)`, `get_object_details(schema, name, type?)`

**Query (1):** `execute_sql(sql)` - read-only in restricted mode

**Performance (4):**
- `explain_query(sql, analyze?, hypothetical_indexes?)` - CONSTRAINT: `analyze` + `hypothetical_indexes` cannot be used together; `hypothetical_indexes` requires HypoPG extension
- `get_top_queries(sort_by?, limit?)` - default `sort_by: "resources"` (multi-dimensional blend, not just time)
- `analyze_workload_indexes(max_size_mb?, method?)` - analyzes top queries from pg_stat_statements
- `analyze_query_indexes(queries[], max_size_mb?, method?)` - CONSTRAINT: max 10 queries per call

**Health (3):**
- `analyze_db_health(type?)` - accepts comma-separated types (e.g. `"index,vacuum"`)
- `get_blocking_queries()` - works even without active blocking (returns deadlock analysis, contention hotspots, proactive recommendations)
- `analyze_vacuum_requirements()` - 6-phase analysis with severity levels

**Advanced (2):**
- `get_database_overview(max_tables?, sampling_mode?, timeout?)` - includes security score, performance hotspots, relationship mapping
- `analyze_schema_relationships()` - inter-schema dependency analysis with visual representation data

## Quick Patterns

**Discover:**
```typescript
const schemas = await list_schemas();
const tables = await list_objects({ schema_name: "public", object_type: "table" });
const details = await get_object_details({ schema_name: "public", object_name: "users", object_type: "table" });
```

**Top resource-intensive queries (recommended default):**
```typescript
const top = await get_top_queries({ sort_by: "resources" });
// Returns queries consuming >5% of ANY resource dimension (CPU, I/O, WAL, etc.)
```

**Hypothetical Index (requires HypoPG, cannot use with analyze:true):**
```typescript
const baseline = await explain_query({ sql: "SELECT * FROM orders WHERE customer_id = $1" });
const withIndex = await explain_query({
  sql: "SELECT * FROM orders WHERE customer_id = $1",
  hypothetical_indexes: [{ table: "orders", columns: ["customer_id"], using: "btree" }]
});
// Use $1, $2 etc. for parameterized queries (bind variables)
```

**Targeted health check:**
```typescript
const health = await analyze_db_health({ health_type: "index,vacuum,buffer" });
// Only run specific checks instead of "all" to reduce noise
```

**Schema relationships:**
```typescript
const rels = await analyze_schema_relationships();
// Cross-schema FK dependencies, hub tables, isolated schemas
```

## Workflows

**Slow query** (decision tree):
1. `explain_query({ sql, analyze: false })` - get estimated plan
2. If total cost < 1000: query is likely fine, check if issue is elsewhere
3. If cost 1000-50000: `explain_query({ sql, analyze: true })` - get actual timings
4. If cost > 50000 or seq scan on large table: test with `hypothetical_indexes` (requires HypoPG)
5. If index helps: `analyze_query_indexes({ queries: [sql] })` for formal recommendation
6. If no index helps: escalate to query rewrite or schema change

**Workload optimization** (use `resources` sort):
1. `get_top_queries({ sort_by: "resources" })` - find queries consuming >5% of any resource (CPU, buffer reads, dirty pages, WAL)
2. For each flagged query: `explain_query()` to identify bottleneck
3. `analyze_workload_indexes({ method: "dta" })` for index recommendations across workload

**Health check** (targeted deep-dives):
1. `analyze_db_health({ health_type: "all" })` - initial scan
2. Based on findings, deep-dive with targeted tools:
   - Index issues → `analyze_db_health({ health_type: "index" })` shows invalid/duplicate/bloated/unused indexes
   - Vacuum issues → `analyze_vacuum_requirements()` for 6-phase bloat analysis with maintenance commands
   - Connection issues → `analyze_db_health({ health_type: "connection" })` for pool utilization
   - Buffer issues → `analyze_db_health({ health_type: "buffer" })` for cache hit rates (index + table)
   - Replication issues → `analyze_db_health({ health_type: "replication" })` for lag and slot health

**New database assessment:**
1. Run discovery script (auto-calls `get_database_overview()`)
2. Review security score and recommendations from discovery output
3. `analyze_schema_relationships()` - understand cross-schema dependencies
4. `get_top_queries({ sort_by: "resources" })` - identify workload hotspots
5. `analyze_db_health({ health_type: "all" })` - full health scan
6. `analyze_workload_indexes({ method: "dta" })` - index optimization opportunities

**Blocking queries**: `get_blocking_queries()` - run immediately when investigating locks; also useful proactively (returns deadlock stats, contention hotspots, and recommendations even when no active blocking exists)

**Multi-table query**: Phase 1: `get_object_details()` for ALL tables → [CHECKPOINT] → Phase 2: query with verified columns

**Incident triage** (general entry point):
1. `get_blocking_queries()` — check active lock contention first (time-sensitive, always safe)
2. `analyze_db_health({ health_type: "connection,buffer,vacuum" })` — quick health snapshot
3. If slow queries, timeouts, high CPU → follow **Performance incident** below
4. If missing data, wrong counts, usage checks → follow **Data investigation** below
5. If unclear → run both in sequence

**Performance incident:**
1. `get_blocking_queries()` — active locks and deadlock stats
2. `analyze_db_health({ health_type: "connection" })` — connection pool saturation
3. `get_top_queries({ sort_by: "resources" })` — resource-heavy queries
4. For suspect queries: `explain_query({ sql, analyze: false })` — plan without adding load
5. If vacuum/bloat suspected: `analyze_vacuum_requirements()` — maintenance recommendations
6. Report findings with severity and recommended actions

**Data investigation** (usage checks, missing data, verification):
1. Run discovery script if not cached — confirm table names and schema
2. `get_object_details()` for ALL relevant tables — [CHECKPOINT: verify actual column names]
3. `execute_sql()` — query using ONLY verified columns from step 2
4. If investigating relationships: `analyze_schema_relationships()` — FK chains, cascade effects
5. If multi-replica and stale data suspected: `analyze_db_health({ health_type: "replication" })` — check lag
6. Report with evidence (query results, row counts)

## Parameters

**explain_query:**
- `sql` (string) - supports bind variables: `$1`, `$2` for parameterized queries
- `analyze` (bool, default: false) - runs query for real statistics
- `hypothetical_indexes` ([{table, columns, using?}]) - requires HypoPG extension
- CONSTRAINT: `analyze: true` + `hypothetical_indexes` cannot be used together (returns error)

**get_top_queries:**
- `sort_by` (default: `"resources"`) - `resources` uses multi-dimensional blend: includes queries where ANY of 5 fractions (exec time, buffer access, buffer reads, dirty pages, WAL bytes) exceeds 5% of workload total. `total_time` and `mean_time` rank by execution time only
- `limit` (int, default: 10) - only applies to `total_time` and `mean_time` sorts

**analyze_db_health:**
- `health_type` (default: `"all"`) - comma-separated list of checks:
  - `index`: invalid, duplicate, bloated, and unused indexes (4 sub-checks)
  - `connection`: connection count and pool utilization
  - `vacuum`: transaction ID wraparound danger
  - `sequence`: sequences approaching max value
  - `replication`: replication lag and slot health
  - `buffer`: cache hit rates for both indexes and tables (2 sub-checks)
  - `constraint`: invalid (not-validated) constraints
  - `all`: runs all above

**analyze_vacuum_requirements** (6 phases):
1. Vacuum summary: total tables, never-vacuumed count, dead tuples aggregate
2. Table bloat analysis with severity: CRITICAL (>40%), HIGH (>20%), MEDIUM (>10%), LOW (>5%), HEALTHY (<=5%)
3. Autovacuum config: per-table threshold vs actual dead tuples, status (OVERDUE/APPROACHING/HEALTHY)
4. Vacuum performance: counts, modifications per vacuum, time since last vacuum
5. Maintenance recommendations: generates VACUUM FULL, VACUUM, or ANALYZE commands with priority
6. Critical issues: transaction ID wraparound risk (XID age > 1.5B), config tuning suggestions

**analyze_query_indexes:**
- `queries` (string[]) - max 10 queries per call
- `max_index_size_mb` (int, default: 10000)
- `method` ("dta" | "llm", default: "dta")

**analyze_*_indexes:** `method` = dta (Pareto-optimal) | llm

## Safety

| Risk | Operations | Behavior |
|------|------------|----------|
| LOW | `list_*`, `get_object_details`, `explain(analyze:false)`, `get_blocking_queries` | Always safe |
| MEDIUM | `get_database_overview`, `analyze_db_health`, `analyze_schema_relationships` | Use sampling on large DBs |
| HIGH | `explain(analyze:true)` | Check cost first with analyze:false |
| CRITICAL | `execute_sql(INSERT/UPDATE/DELETE/DDL)` | Require confirmation |

## Common Errors

| Error | Fix |
|-------|-----|
| `column X does not exist` | Run `get_object_details()` - never guess column names |
| `relation does not exist` | Refresh table list with `list_objects()` |
| `permission denied` | Use read-only queries |
| `pg_stat_statements not found` | Request DBA to enable extension |
| `timeout` | Reduce scope: `max_tables: 100`, use sampling |
| `HypoPG not installed` | `hypothetical_indexes` requires the HypoPG extension - request DBA to install, or skip hypothetical analysis |
| `Cannot use analyze and hypothetical indexes together` | Remove `analyze: true` when using `hypothetical_indexes` - they are mutually exclusive |
| `up to 10 queries to analyze` | `analyze_query_indexes` accepts max 10 queries - split larger batches into multiple calls |

## Output Format

Present results as a structured report:
```
Analyzing Postgres Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

