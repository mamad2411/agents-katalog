---
name: analyzing-cassandra
description: |
  Use when working with Cassandra — apache Cassandra keyspace analysis,
  compaction strategies, repair status, nodetool operations, and cluster health
  monitoring.
connection_type: cassandra
preload: false
---

# Cassandra Analysis Skill

Analyze and optimize Cassandra clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated keyspace/table names and schema errors.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Cluster overview
nodetool status
nodetool describecluster

# 2. List keyspaces
cqlsh -e "DESCRIBE KEYSPACES;"

# 3. List tables in a keyspace
cqlsh -e "USE my_keyspace; DESCRIBE TABLES;"

# 4. Get table schema (never assume column names)
cqlsh -e "DESCRIBE TABLE my_keyspace.my_table;"

# 5. Sample data to confirm column names
cqlsh -e "SELECT * FROM my_keyspace.my_table LIMIT 5;"
```

**Phase 1 outputs:**
- Cluster topology and node states
- List of keyspaces with replication strategies
- Table schemas with actual column names and types

### Phase 2: Analysis (only after Phase 1)

Only reference keyspaces, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core CQL query runner — always use this
cql_exec() {
    local query="$1"
    cqlsh ${CASSANDRA_HOST:-localhost} ${CASSANDRA_PORT:-9042} -e "$query"
}

# Nodetool helper
nt_cmd() {
    nodetool -h ${CASSANDRA_HOST:-localhost} "$@"
}
```

## Anti-Hallucination Rules

- **NEVER reference a keyspace** without confirming it exists via `DESCRIBE KEYSPACES`
- **NEVER reference a table** without confirming it via `DESCRIBE TABLES` in the keyspace
- **NEVER reference column names** without seeing them in `DESCRIBE TABLE`
- **NEVER assume replication factor** — always check keyspace definition
- **NEVER assume compaction strategy** — always check table definition

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, DESCRIBE, nodetool status/info/tablestats/tpstats
- **FORBIDDEN**: DROP, TRUNCATE, ALTER, INSERT, UPDATE, DELETE, nodetool decommission/removenode/repair without explicit user request
- **ALWAYS add `LIMIT`** to SELECT queries — tables can have billions of rows
- **NEVER** run `SELECT *` without LIMIT on production
- **Use `nodetool tablestats`** instead of COUNT(*) for row counts

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Node Status ==="
nt_cmd status

echo ""
echo "=== Cluster Info ==="
nt_cmd describecluster

echo ""
echo "=== Gossip Info ==="
nt_cmd gossipinfo | head -60

echo ""
echo "=== Thread Pool Stats ==="
nt_cmd tpstats | head -30
```

### Keyspace & Table Analysis

```bash
#!/bin/bash
KEYSPACE="${1:-my_keyspace}"

echo "=== Keyspace Definition ==="
cql_exec "DESCRIBE KEYSPACE $KEYSPACE;"

echo ""
echo "=== Table Stats ==="
nt_cmd tablestats "$KEYSPACE" | grep -E "Table:|Space used|Number of|Compaction|Read Latency|Write Latency|Bloom filter"
```

### Compaction & Repair Status

```bash
#!/bin/bash
echo "=== Active Compactions ==="
nt_cmd compactionstats

echo ""
echo "=== Compaction History (last 10) ==="
nt_cmd compactionhistory | head -20

echo ""
echo "=== Repair Status ==="
nt_cmd netstats | grep -A5 "Repair"

echo ""
echo "=== Pending Tasks ==="
nt_cmd tpstats | grep -E "Pending|Blocked"
```

### Performance Analysis

```bash
#!/bin/bash
KEYSPACE="${1:-my_keyspace}"
TABLE="${2:-my_table}"

echo "=== Table Stats: $KEYSPACE.$TABLE ==="
nt_cmd tablestats "$KEYSPACE.$TABLE"

echo ""
echo "=== Partition Distribution ==="
nt_cmd tablehistograms "$KEYSPACE.$TABLE"

echo ""
echo "=== Tombstone Warnings ==="
grep -i "tombstone" /var/log/cassandra/system.log 2>/dev/null | tail -10

echo ""
echo "=== Dropped Messages ==="
nt_cmd tpstats | grep -E "Dropped"
```

### SSTable Analysis

```bash
#!/bin/bash
KEYSPACE="${1:-my_keyspace}"
TABLE="${2:-my_table}"

echo "=== SSTable Count & Size ==="
nt_cmd tablestats "$KEYSPACE.$TABLE" | grep -E "SSTable count|Space used|Compaction strategy"

echo ""
echo "=== Estimated Partitions ==="
nt_cmd tablestats "$KEYSPACE.$TABLE" | grep -E "partitions|cells"

echo ""
echo "=== Read/Write Latency ==="
nt_cmd tablestats "$KEYSPACE.$TABLE" | grep -E "latency|count"
```

## Output Format

Present results as a structured report:
```
Analyzing Cassandra Report
══════════════════════════
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

- **Tombstone accumulation**: Deletes create tombstones that slow reads — check tombstone count in tablestats
- **Wide partitions**: Partitions over 100MB cause GC pressure — check partition size histograms
- **Consistency level**: QUORUM requires RF/2+1 nodes — know your replication factor before choosing CL
- **Repair neglect**: Unrepaired data leads to inconsistency — check `nodetool netstats` for repair status
- **Hot partitions**: Uneven data distribution causes hotspots — check partition size distribution
- **COUNT(*) is expensive**: It scans the entire table — use `nodetool tablestats` for estimated counts
- **Materialized views**: MVs can cause write amplification — check for MV-related latency
