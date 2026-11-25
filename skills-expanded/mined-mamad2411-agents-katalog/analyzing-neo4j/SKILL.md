---
name: analyzing-neo4j
description: |
  Use when working with Neo4J — neo4j graph database analysis, index management,
  Cypher query optimization, APOC utilities, and cluster health monitoring.
connection_type: neo4j
preload: false
---

# Neo4j Analysis Skill

Analyze and optimize Neo4j graph databases with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated label/relationship names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Database overview
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" "CALL db.labels() YIELD label RETURN label;"

# 2. Relationship types
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" "CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType;"

# 3. Property keys
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" "CALL db.propertyKeys() YIELD propertyKey RETURN propertyKey;"

# 4. Schema overview
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" "CALL db.schema.visualization();"

# 5. Sample nodes per label
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" "MATCH (n:MyLabel) RETURN n LIMIT 3;"
```

**Phase 1 outputs:**
- Node labels and relationship types
- Property keys in use
- Sample nodes to understand actual properties

### Phase 2: Analysis (only after Phase 1)

Only reference labels, relationship types, and properties confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Cypher runner — always use this
neo4j_query() {
    local query="$1"
    cypher-shell -u "${NEO4J_USER:-neo4j}" -p "${NEO4J_PASSWORD}" \
        -a "${NEO4J_URI:-bolt://localhost:7687}" \
        --format plain "$query"
}

# HTTP API alternative
neo4j_http() {
    local query="$1"
    curl -s -u "${NEO4J_USER:-neo4j}:${NEO4J_PASSWORD}" \
        -H "Content-Type: application/json" \
        -d "{\"statements\":[{\"statement\":\"$query\"}]}" \
        "http://${NEO4J_HOST:-localhost}:7474/db/neo4j/tx/commit"
}
```

## Anti-Hallucination Rules

- **NEVER reference a node label** without confirming via `db.labels()`
- **NEVER reference a relationship type** without confirming via `db.relationshipTypes()`
- **NEVER reference property names** without seeing them in `db.propertyKeys()` or sample nodes
- **NEVER assume index names** — always check with `SHOW INDEXES`
- **NEVER guess constraint names** — always verify with `SHOW CONSTRAINTS`

## Safety Rules

- **READ-ONLY ONLY**: Use only MATCH, RETURN, CALL (read procedures), EXPLAIN, PROFILE
- **FORBIDDEN**: CREATE, DELETE, DETACH DELETE, MERGE, SET, REMOVE, DROP without explicit user request
- **ALWAYS add `LIMIT`** to MATCH queries — graphs can have millions of nodes
- **Use `EXPLAIN`** before running expensive traversals
- **Use `PROFILE`** sparingly — it executes the query and captures runtime stats

## Common Operations

### Graph Overview

```bash
#!/bin/bash
echo "=== Neo4j Version ==="
neo4j_query "CALL dbms.components() YIELD name, versions RETURN name, versions;"

echo ""
echo "=== Node Counts by Label ==="
neo4j_query "CALL db.labels() YIELD label CALL { WITH label CALL db.stats.retrieve('GRAPH COUNTS') YIELD nodeCount RETURN nodeCount } RETURN label, nodeCount;" 2>/dev/null || \
neo4j_query "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY count DESC;"

echo ""
echo "=== Relationship Counts ==="
neo4j_query "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY count DESC;"

echo ""
echo "=== Database Size ==="
neo4j_query "CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Store sizes') YIELD attributes RETURN attributes;" 2>/dev/null || echo "JMX not available"
```

### Index Management

```bash
#!/bin/bash
echo "=== Existing Indexes ==="
neo4j_query "SHOW INDEXES YIELD name, type, state, populationPercent, labelsOrTypes, properties RETURN name, type, state, populationPercent, labelsOrTypes, properties ORDER BY labelsOrTypes;"

echo ""
echo "=== Constraints ==="
neo4j_query "SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties RETURN name, type, labelsOrTypes, properties;"

echo ""
echo "=== Index Usage (via query plan) ==="
neo4j_query "EXPLAIN MATCH (n:MyLabel {myProp: 'value'}) RETURN n;"
```

### Query Performance Analysis

```bash
#!/bin/bash
echo "=== Active Queries ==="
neo4j_query "CALL dbms.listQueries() YIELD queryId, username, query, elapsedTimeMillis, status RETURN queryId, username, substring(query, 0, 80) AS query_preview, elapsedTimeMillis, status ORDER BY elapsedTimeMillis DESC;" 2>/dev/null || echo "listQueries not available in this edition"

echo ""
echo "=== Query Plan Analysis ==="
# Replace with actual query from Phase 1 discovery
neo4j_query "PROFILE MATCH (n:MyLabel)-[:MY_REL]->(m) RETURN n, m LIMIT 100;"

echo ""
echo "=== Transaction Status ==="
neo4j_query "CALL dbms.listTransactions() YIELD transactionId, username, currentQueryId, elapsedTimeMillis, status RETURN transactionId, username, currentQueryId, elapsedTimeMillis, status;" 2>/dev/null
```

### APOC Utilities

```bash
#!/bin/bash
echo "=== APOC Version ==="
neo4j_query "RETURN apoc.version();" 2>/dev/null || echo "APOC not installed"

echo ""
echo "=== Graph Stats via APOC ==="
neo4j_query "CALL apoc.meta.stats() YIELD labelCount, relTypeCount, nodeCount, relCount, propertyKeyCount RETURN labelCount, relTypeCount, nodeCount, relCount, propertyKeyCount;" 2>/dev/null

echo ""
echo "=== Schema via APOC ==="
neo4j_query "CALL apoc.meta.schema() YIELD value RETURN value;" 2>/dev/null
```

## Output Format

Present results as a structured report:
```
Analyzing Neo4J Report
══════════════════════
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

- **Unbounded traversals**: `MATCH (a)-[*]->(b)` can explode on large graphs — always bound depth with `[*1..3]`
- **Cartesian products**: Multiple disconnected MATCH patterns create cartesian products — always connect patterns
- **Missing indexes**: Label+property scans without indexes cause full scans — check `SHOW INDEXES`
- **Eager operations**: Some operations (e.g., COLLECT before DELETE) load everything into memory — use `EXPLAIN` to check for Eager operators
- **PROFILE vs EXPLAIN**: PROFILE executes the query; EXPLAIN only plans it — use EXPLAIN first on production
- **Property existence**: Properties are optional in Neo4j — always handle NULL/missing properties
