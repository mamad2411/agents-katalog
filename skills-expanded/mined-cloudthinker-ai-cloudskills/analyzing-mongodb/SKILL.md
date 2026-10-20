---
name: analyzing-mongodb
description: |
  Use when working with Mongodb — mongoDB database analysis, performance tuning,
  query optimization, and health monitoring. Covers collection analysis, index
  recommendations, aggregation pipelines, replica set health, Atlas cluster
  management, and slow query investigation.
connection_type: mongodb
preload: false
---

# MongoDB Analysis Skill

Analyze and optimize MongoDB databases with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated collection names and schema errors.**

### Phase 1: Discovery (ALWAYS run first)

```javascript
// Run this discovery script first — NEVER skip
// Connect: mongosh "$MONGODB_URI" --quiet --eval "..."

// 1. List databases and sizes
db.adminCommand({ listDatabases: 1, nameOnly: false })
   .databases
   .forEach(d => print(d.name, d.sizeOnDisk));

// 2. List collections in target database
use targetDb;
db.getCollectionNames().forEach(c => {
    const stats = db[c].stats();
    print(c, stats.count, stats.storageSize, stats.totalIndexSize);
});

// 3. Sample schema (never assume field names)
db.collectionName.findOne();
db.collectionName.aggregate([{ $sample: { size: 5 } }]);
```

**Phase 1 outputs:**
- List of databases and sizes
- List of collections with document counts
- Sample documents to understand actual field names

### Phase 2: Analysis (only after Phase 1)

Only reference collections, databases, and field names confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core MongoDB query runner — always use this
mongo_eval() {
    local db="$1"
    local script="$2"
    mongosh "$MONGODB_URI/$db" --quiet --eval "$script"
}

# Atlas CLI helper (if Atlas connection available)
atlas_cmd() {
    atlas "$@" --projectId "$MONGODB_ATLAS_PROJECT_ID" --output json
}
```

## Anti-Hallucination Rules

- **NEVER reference a collection by name** without confirming it exists via `db.getCollectionNames()`
- **NEVER reference a field name** in queries without seeing it in a sample document
- **NEVER assume index names** — always list indexes via `db.collection.getIndexes()`
- **NEVER assume Atlas cluster names** — always run `atlas clusters list` first
- **ALWAYS use `--quiet` flag** with mongosh to suppress connection banners

## Safety Rules

- **READ-ONLY ONLY**: Use only find, aggregate, explain, stats, currentOp, serverStatus
- **FORBIDDEN**: insertMany, updateMany, deleteMany, drop, dropDatabase, createIndex without explicit user request
- **ALWAYS add `.limit()`** to find queries — default cap at 100 documents
- **NEVER** run `db.collection.find()` without a limit on large collections
- **Use explain()** before running expensive aggregations on large collections

## Common Operations

### Database Health Overview

```bash
#!/bin/bash
echo "=== MongoDB Server Status ==="
mongo_eval admin "
    const s = db.serverStatus();
    print('Version:', s.version);
    print('Uptime (hours):', Math.round(s.uptime/3600));
    print('Connections active:', s.connections.current);
    print('Connections available:', s.connections.available);
    print('Ops/sec inserts:', s.opcounters.insert);
    print('Ops/sec queries:', s.opcounters.query);
    print('Ops/sec updates:', s.opcounters.update);
    print('Mem resident MB:', s.mem.resident);
    print('Mem virtual MB:', s.mem.virtual);
"

echo ""
echo "=== Replica Set Status ==="
mongo_eval admin "
    try {
        const rs = rs.status();
        rs.members.forEach(m => print(m.name, m.stateStr, m.health, m.optimeDate));
    } catch(e) { print('Not a replica set'); }
"

echo ""
echo "=== Databases ==="
mongo_eval admin "
    db.adminCommand({listDatabases:1}).databases
      .sort((a,b) => b.sizeOnDisk - a.sizeOnDisk)
      .forEach(d => print(d.name, Math.round(d.sizeOnDisk/1024/1024) + 'MB'));
"
```

### Collection Analysis

```bash
#!/bin/bash
DB_NAME="${1:-myDatabase}"

echo "=== Collections in $DB_NAME ==="
mongo_eval "$DB_NAME" "
    db.getCollectionNames().forEach(c => {
        const stats = db[c].stats({scale: 1024*1024});
        print(c, stats.count + ' docs', Math.round(stats.storageSize) + 'MB data', Math.round(stats.totalIndexSize) + 'MB indexes');
    });
" | sort -t' ' -k3 -rn | head -20

echo ""
echo "=== Indexes per Collection ==="
mongo_eval "$DB_NAME" "
    db.getCollectionNames().forEach(c => {
        const idxs = db[c].getIndexes();
        print(c + ': ' + idxs.length + ' indexes');
        idxs.forEach(i => print('  -', JSON.stringify(i.key), i.unique ? '[UNIQUE]' : ''));
    });
"
```

### Slow Query Analysis

```bash
#!/bin/bash
DB_NAME="${1:-myDatabase}"
SLOW_MS="${2:-100}"

echo "=== Slow Query Log (>=${SLOW_MS}ms) ==="
mongo_eval "$DB_NAME" "
    db.system.profile.find(
        { millis: { \$gte: ${SLOW_MS} } },
        { ns: 1, op: 1, millis: 1, command: 1, ts: 1 }
    )
    .sort({ millis: -1 })
    .limit(20)
    .forEach(q => {
        print(q.ts.toISOString().substr(0,19),
              q.op,
              q.ns,
              q.millis + 'ms',
              JSON.stringify(q.command || {}).substr(0,100));
    });
" 2>/dev/null || echo "Profiler not enabled. Enable with: db.setProfilingLevel(1, {slowms: ${SLOW_MS}})"

echo ""
echo "=== Currently Running Operations ==="
mongo_eval admin "
    db.currentOp({ active: true, secs_running: { \$gte: 1 } })
      .inprog
      .forEach(op => print(op.opid, op.secs_running + 's', op.op, op.ns, JSON.stringify(op.command || {}).substr(0,80)));
"
```

### Index Effectiveness Analysis

```bash
#!/bin/bash
DB_NAME="$1"
COLLECTION="$2"

if [ -z "$DB_NAME" ] || [ -z "$COLLECTION" ]; then
    echo "Usage: $0 <database> <collection>"
    exit 1
fi

echo "=== Index Usage Stats for $DB_NAME.$COLLECTION ==="
mongo_eval "$DB_NAME" "
    // Index access stats (requires MongoDB 3.2+)
    db['$COLLECTION'].aggregate([
        { \$indexStats: {} }
    ]).forEach(i => {
        print(i.name, 'accesses:', i.accesses.ops, 'since:', i.accesses.since.toISOString().substr(0,10));
    });
"

echo ""
echo "=== Unused Indexes (0 accesses) ==="
mongo_eval "$DB_NAME" "
    db['$COLLECTION'].aggregate([{ \$indexStats: {} }])
        .toArray()
        .filter(i => i.accesses.ops == 0 && i.name != '_id_')
        .forEach(i => print('UNUSED:', i.name, JSON.stringify(i.key)));
"

echo ""
echo "=== Collection Size vs Index Size ==="
mongo_eval "$DB_NAME" "
    const s = db['$COLLECTION'].stats({scale: 1024*1024});
    print('Documents:', s.count);
    print('Data size:', Math.round(s.size) + 'MB');
    print('Storage size:', Math.round(s.storageSize) + 'MB');
    print('Index size:', Math.round(s.totalIndexSize) + 'MB');
    print('Index ratio:', Math.round(s.totalIndexSize/s.size*100) + '%');
"
```

### Query Performance with explain()

```bash
#!/bin/bash
DB_NAME="$1"
COLLECTION="$2"

echo "=== Query Plan Analysis ==="
mongo_eval "$DB_NAME" "
    // ALWAYS use explain() before running expensive queries on large collections
    db['$COLLECTION'].find({ /* your filter here */ })
        .explain('executionStats')
        .executionStats
        |> ({
            nReturned: @.nReturned,
            executionTimeMs: @.executionTimeMillis,
            docsExamined: @.totalDocsExamined,
            keysExamined: @.totalKeysExamined,
            indexUsed: @.executionStages?.inputStage?.indexName || 'COLLSCAN'
        })
        |> print(JSON.stringify(@, null, 2));
" 2>/dev/null

# Simpler version for older mongosh
mongo_eval "$DB_NAME" "
    const plan = db['$COLLECTION'].find({}).explain('executionStats');
    const stats = plan.executionStats;
    print('Docs examined:', stats.totalDocsExamined);
    print('Docs returned:', stats.nReturned);
    print('Exec time ms:', stats.executionTimeMillis);
    print('Stage:', plan.queryPlanner.winningPlan.stage);
    if (plan.queryPlanner.winningPlan.inputStage) {
        print('Index used:', plan.queryPlanner.winningPlan.inputStage.indexName || 'NONE (COLLSCAN)');
    }
"
```

### Atlas Cluster Management (if Atlas connection)

```bash
#!/bin/bash
echo "=== Atlas Clusters ==="
atlas clusters list 2>/dev/null | jq -r '.[] | "\(.name)\t\(.stateName)\t\(.mongoDBVersion)\t\(.providerSettings.instanceSizeName)"' || echo "Atlas CLI not configured"

echo ""
echo "=== Atlas Metrics (last 1h) ==="
CLUSTER_NAME=$(atlas clusters list 2>/dev/null | jq -r '.[0].name' || echo "")
if [ -n "$CLUSTER_NAME" ]; then
    atlas metrics process "$CLUSTER_NAME" \
        --granularity PT1M --period P1H \
        --type CONNECTIONS --type OPCOUNTER_CMD \
        2>/dev/null | jq -r '.measurements[] | "\(.name): \(.dataPoints[-1].value // 0)"'
fi
```

### Aggregation Pipeline Examples

```bash
#!/bin/bash
DB_NAME="$1"
COLLECTION="$2"

echo "=== Document Count by Date (last 30 days) ==="
mongo_eval "$DB_NAME" "
    // Adapt date field name based on Phase 1 discovery
    db['$COLLECTION'].aggregate([
        {
            \$match: {
                createdAt: { \$gte: new Date(Date.now() - 30*24*60*60*1000) }
            }
        },
        {
            \$group: {
                _id: { \$dateToString: { format: '%Y-%m-%d', date: '\$createdAt' } },
                count: { \$sum: 1 }
            }
        },
        { \$sort: { _id: -1 } },
        { \$limit: 30 }
    ]).forEach(r => print(r._id, r.count));
" 2>/dev/null || echo "Adjust date field name after Phase 1 discovery"
```

## Output Format

Present results as a structured report:
```
Analyzing Mongodb Report
════════════════════════
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

- **Schema assumptions**: MongoDB is schema-flexible — never assume field names without sampling documents
- **Missing `--quiet`**: Without `--quiet`, mongosh outputs connection banners that corrupt script output
- **Large `.find()` without limit**: Always add `.limit(N)` — collections can have millions of documents
- **`explain()` on production**: Use `explain('queryPlanner')` for plan-only (no execution); `explain('executionStats')` runs the query
- **Replica set reads**: Prefer `readPreference: 'secondaryPreferred'` for analytics to avoid impacting primary
- **Aggregation memory**: Default 100MB memory limit per stage — add `{ allowDiskUse: true }` for large aggregations
- **Timezone handling**: ISODate stores in UTC — always convert user-specified times to UTC before querying
- **Atlas vs self-hosted**: Atlas has different metric APIs than `db.serverStatus()` — check connection type in Phase 1
