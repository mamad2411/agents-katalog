---
name: analyzing-vitess
description: |
  Use when working with Vitess — vitess tablet health, VSchema management,
  resharding status, VReplication workflows, and cluster topology.
connection_type: vitess
preload: false
---

# Vitess Analysis Skill

Analyze and optimize Vitess clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated keyspace/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List cells
vtctldclient GetCellInfoNames

# 2. List keyspaces
vtctldclient GetKeyspaces

# 3. Get keyspace info
vtctldclient GetKeyspace my_keyspace

# 4. List tablets
vtctldclient GetTablets --keyspace my_keyspace

# 5. Get VSchema (table routing)
vtctldclient GetVSchema my_keyspace

# 6. List shards
vtctldclient FindAllShardsInKeyspace my_keyspace
```

**Phase 1 outputs:**
- Cells, keyspaces, and shards
- Tablet list with types and health
- VSchema with table definitions

### Phase 2: Analysis (only after Phase 1)

Only reference keyspaces, shards, and tables confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core vtctldclient helper — always use this
vtctl() {
    vtctldclient --server "${VTCTLD_SERVER:-localhost:15999}" "$@"
}

# VTGate SQL helper
vt_query() {
    local query="$1"
    mysql -h "${VTGATE_HOST:-localhost}" -P "${VTGATE_PORT:-15306}" \
        -u "${VTGATE_USER:-}" -e "$query"
}
```

## Anti-Hallucination Rules

- **NEVER reference a keyspace** without confirming via `GetKeyspaces`
- **NEVER reference table names** without checking VSchema or running `SHOW TABLES` via VTGate
- **NEVER assume shard names** — always get from `FindAllShardsInKeyspace`
- **NEVER guess tablet aliases** — always list via `GetTablets`
- **NEVER assume VIndex types** — always check VSchema

## Safety Rules

- **READ-ONLY ONLY**: Use only Get*, Find*, SELECT, SHOW commands
- **FORBIDDEN**: ApplySchema, ApplyVSchema, Reshard, MoveTables without explicit user request
- **ALWAYS verify tablet health** before querying specific tablets
- **Use VTGate** for queries — never query tablets directly unless debugging

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cells ==="
vtctl GetCellInfoNames

echo ""
echo "=== Keyspaces ==="
for KS in $(vtctl GetKeyspaces); do
    echo "--- $KS ---"
    vtctl GetKeyspace "$KS" | jq '{name, keyspace_type, durability_policy}'
done

echo ""
echo "=== Tablets ==="
vtctl GetTablets | jq -r '.[] | "\(.tablet.alias.cell)/\(.tablet.alias.uid)\t\(.tablet.keyspace)\t\(.tablet.shard)\t\(.tablet.type)\t\(.state)"'
```

### Tablet Health Analysis

```bash
#!/bin/bash
KEYSPACE="${1:-my_keyspace}"

echo "=== Tablet Health for $KEYSPACE ==="
vtctl GetTablets --keyspace "$KEYSPACE" | jq '.[] | {alias: "\(.tablet.alias.cell)/\(.tablet.alias.uid)", type: .tablet.type, shard: .tablet.shard, hostname: .tablet.hostname, state: .state}'

echo ""
echo "=== Shard Info ==="
vtctl FindAllShardsInKeyspace "$KEYSPACE" | jq '.shards | to_entries[] | {shard: .key, primary_alias: .value.primary_alias, is_primary_serving: .value.is_primary_serving}'

echo ""
echo "=== Replication Status ==="
for TABLET in $(vtctl GetTablets --keyspace "$KEYSPACE" | jq -r '.[] | "\(.tablet.alias.cell)-\(.tablet.alias.uid)"'); do
    echo "--- $TABLET ---"
    vtctl GetReplicationStatus "$TABLET" 2>/dev/null
done
```

### VSchema & Routing Analysis

```bash
#!/bin/bash
KEYSPACE="${1:-my_keyspace}"

echo "=== VSchema ==="
vtctl GetVSchema "$KEYSPACE" | jq '{tables: (.tables | keys), vindexes: (.vindexes | keys)}'

echo ""
echo "=== Routing Rules ==="
vtctl GetRoutingRules | jq '.'

echo ""
echo "=== Shard Routing ==="
vtctl GetShardRoutingRules 2>/dev/null | jq '.'
```

### VReplication & Resharding Status

```bash
#!/bin/bash
echo "=== Active VReplication Workflows ==="
vtctl GetWorkflows my_keyspace | jq '.workflows[]? | {name, state, source, target, max_v_replication_lag}'

echo ""
echo "=== Reshard Status ==="
vtctl Reshard --target-keyspace my_keyspace status 2>/dev/null || echo "No active reshard"

echo ""
echo "=== MoveTables Status ==="
vtctl MoveTables --target-keyspace my_keyspace status 2>/dev/null || echo "No active MoveTables"
```

## Output Format

Present results as a structured report:
```
Analyzing Vitess Report
═══════════════════════
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

- **Scatter queries**: Queries without VIndex-routable WHERE clauses scatter to all shards — very expensive
- **VSchema misconfig**: Missing VIndex definitions cause scatter queries — always verify VSchema
- **Primary tablet failover**: Monitor primary tablet health — failover causes brief unavailability
- **Resharding in progress**: Active resharding adds replication lag — monitor VReplication lag
- **Schema changes**: Use Vitess schema management (ApplySchema) — direct DDL can cause inconsistency
- **Cross-shard joins**: Vitess does not support cross-shard joins natively — plan VSchema accordingly
