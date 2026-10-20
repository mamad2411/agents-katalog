---
name: analyzing-planetscale
description: |
  Use when working with Planetscale — planetScale branch management, deploy
  requests, schema analysis, query insights, and database health.
connection_type: planetscale
preload: false
---

# PlanetScale Analysis Skill

Analyze and optimize PlanetScale databases with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated database/branch names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List organizations
pscale org list

# 2. List databases
pscale database list --org "$PS_ORG"

# 3. List branches
pscale branch list "$DB_NAME" --org "$PS_ORG"

# 4. Get schema
pscale shell "$DB_NAME" "$BRANCH" --org "$PS_ORG" -e "SHOW TABLES;"

# 5. Describe table (never assume column names)
pscale shell "$DB_NAME" "$BRANCH" --org "$PS_ORG" -e "DESCRIBE my_table;"
```

**Phase 1 outputs:**
- Organizations and databases
- Branches with status
- Table schemas with confirmed column names

### Phase 2: Analysis (only after Phase 1)

Only reference databases, branches, and tables confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core PlanetScale CLI helper — always use this
ps_cmd() {
    pscale "$@" --org "${PS_ORG}" --format json 2>/dev/null
}

# PlanetScale SQL runner
ps_query() {
    local db="$1" branch="$2" query="$3"
    pscale shell "$db" "$branch" --org "${PS_ORG}" -e "$query"
}

# PlanetScale API helper
ps_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer ${PS_TOKEN}" \
        "https://api.planetscale.com/v1/organizations/${PS_ORG}/$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a database** without confirming via `pscale database list`
- **NEVER reference a branch** without confirming via `pscale branch list`
- **NEVER reference table names** without running `SHOW TABLES` on the branch
- **NEVER assume column names** — always run `DESCRIBE` first
- **NEVER guess deploy request IDs** — always list them first

## Safety Rules

- **READ-ONLY ONLY**: Use only list, show, shell (SELECT only), audit-log commands
- **FORBIDDEN**: branch delete, database delete, deploy-request create/deploy without explicit user request
- **ALWAYS use the correct branch** — production vs development branches have different data
- **Verify branch status** before running queries

## Common Operations

### Database Overview

```bash
#!/bin/bash
echo "=== Databases ==="
ps_cmd database list | jq '.[] | {name, region, plan, state, created_at}'

echo ""
echo "=== Branches ==="
DB_NAME="${1:-my_database}"
ps_cmd branch list "$DB_NAME" | jq '.[] | {name, production: .production, ready, schema_last_updated_at}'

echo ""
echo "=== Database Schema ==="
ps_query "$DB_NAME" main "SHOW TABLES;"
```

### Deploy Request Analysis

```bash
#!/bin/bash
DB_NAME="${1:-my_database}"

echo "=== Open Deploy Requests ==="
ps_cmd deploy-request list "$DB_NAME" | jq '[.[] | select(.state == "open")] | .[] | {number, branch, state, created_at, deployment}'

echo ""
echo "=== Recent Deploys ==="
ps_cmd deploy-request list "$DB_NAME" | jq '[.[] | select(.state == "complete")] | sort_by(.closed_at) | reverse | .[0:10] | .[] | {number, branch, state, closed_at}'

echo ""
echo "=== Schema Diff ==="
BRANCH="${2:-dev}"
pscale branch diff "$DB_NAME" "$BRANCH" --org "$PS_ORG" 2>/dev/null
```

### Query Insights

```bash
#!/bin/bash
DB_NAME="${1:-my_database}"

echo "=== Query Statistics ==="
ps_query "$DB_NAME" main "SELECT query_pattern, count_star, sum_timer_wait, avg_timer_wait, sum_rows_examined, sum_rows_sent FROM performance_schema.events_statements_summary_by_digest ORDER BY sum_timer_wait DESC LIMIT 15;" 2>/dev/null

echo ""
echo "=== Slow Queries ==="
ps_query "$DB_NAME" main "SELECT DIGEST_TEXT, COUNT_STAR, AVG_TIMER_WAIT/1000000000 as avg_ms, SUM_ROWS_EXAMINED, SUM_ROWS_SENT FROM performance_schema.events_statements_summary_by_digest WHERE AVG_TIMER_WAIT > 1000000000 ORDER BY AVG_TIMER_WAIT DESC LIMIT 10;" 2>/dev/null
```

### Schema Analysis

```bash
#!/bin/bash
DB_NAME="${1:-my_database}"
BRANCH="${2:-main}"

echo "=== Table Sizes ==="
ps_query "$DB_NAME" "$BRANCH" "SELECT table_name, table_rows, ROUND(data_length/1024/1024, 2) as data_mb, ROUND(index_length/1024/1024, 2) as index_mb, ROUND((data_length + index_length)/1024/1024, 2) as total_mb FROM information_schema.tables WHERE table_schema = DATABASE() ORDER BY data_length + index_length DESC;"

echo ""
echo "=== Indexes ==="
ps_query "$DB_NAME" "$BRANCH" "SELECT table_name, index_name, column_name, seq_in_index, non_unique FROM information_schema.statistics WHERE table_schema = DATABASE() ORDER BY table_name, index_name, seq_in_index;"
```

## Output Format

Present results as a structured report:
```
Analyzing Planetscale Report
════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Branch isolation**: Development branches have separate data — queries on dev branch do not reflect production
- **Deploy requests**: Schema changes require deploy requests — direct DDL on production branches is blocked
- **Foreign keys**: PlanetScale does not support foreign key constraints at the database level — enforce in application
- **Connection strings**: Each branch has its own connection string — do not mix
- **Boost queries**: PlanetScale Boost caches results — invalidation timing matters
- **Row limits**: Free tier has row limits — check plan quotas
