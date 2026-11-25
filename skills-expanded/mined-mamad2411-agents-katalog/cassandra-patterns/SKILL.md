---
name: cassandra-patterns
description: "When to activate: Cassandra, CQL, partition key, wide row, Cassandra cluster, eventual consistency, Scylla"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: databases
  language: sql
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Cassandra Patterns

## Data Modeling — Query-First Design

```cql
-- Design tables around access patterns, NOT entities
-- Access pattern: "Get all messages for a conversation, ordered by time"
CREATE TABLE messages_by_conversation (
  conversation_id UUID,
  sent_at         TIMEUUID,     -- time-ordered UUID for clustering
  sender_id       UUID,
  body            TEXT,
  is_deleted      BOOLEAN,
  PRIMARY KEY (conversation_id, sent_at)
) WITH CLUSTERING ORDER BY (sent_at DESC)
  AND compaction = {'class': 'TimeWindowCompactionStrategy',
                    'compaction_window_size': '1',
                    'compaction_window_unit': 'DAYS'};

-- Access pattern: "Get user profile by user_id"
CREATE TABLE users (
  user_id   UUID PRIMARY KEY,
  name      TEXT,
  email     TEXT,
  settings  MAP<TEXT, TEXT>
);

-- Access pattern: "Find user by email" — denormalize!
CREATE TABLE users_by_email (
  email     TEXT PRIMARY KEY,
  user_id   UUID,
  name      TEXT
);
```

## Partition Key Design

```cql
-- BAD: low cardinality partition key → hot partition
CREATE TABLE events (day DATE, time TIMEUUID, data TEXT,
  PRIMARY KEY (day, time));  -- all events on same day → one node

-- GOOD: add bucket to distribute load
CREATE TABLE events (
  day    DATE,
  bucket INT,     -- hash(user_id) % 100
  time   TIMEUUID,
  data   TEXT,
  PRIMARY KEY ((day, bucket), time)
) WITH CLUSTERING ORDER BY (time DESC);

-- Composite partition key prevents single-node hotspot
CREATE TABLE sensor_data (
  sensor_id   TEXT,
  year_month  TEXT,     -- '2024-01' — limit partition size
  recorded_at TIMEUUID,
  value       DOUBLE,
  PRIMARY KEY ((sensor_id, year_month), recorded_at)
);
```

## CQL Queries

```cql
-- Always specify partition key in WHERE
SELECT * FROM messages_by_conversation
WHERE conversation_id = 550e8400-e29b-41d4-a716-446655440000
  AND sent_at > minTimeuuid('2024-01-01 00:00:00+0000')
LIMIT 50;

-- Batch (only for related partitions — not performance tool!)
BEGIN BATCH
  INSERT INTO users (user_id, name, email) VALUES (uuid(), 'Alice', 'a@b.com');
  INSERT INTO users_by_email (email, user_id, name) VALUES ('a@b.com', uuid(), 'Alice');
APPLY BATCH;

-- Lightweight transaction (compare-and-set)
INSERT INTO users (user_id, email) VALUES (uuid(), 'a@b.com') IF NOT EXISTS;
UPDATE users SET name = 'Alice' WHERE user_id = ? IF name = 'old_name';

-- TTL on individual columns or rows
INSERT INTO sessions (session_id, data) VALUES (?, ?) USING TTL 86400;
UPDATE users USING TTL 3600 SET reset_token = ? WHERE user_id = ?;
```

## Consistency Levels

```python
from cassandra.cluster import Cluster, ConsistencyLevel
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import SimpleStatement

cluster = Cluster(
    ['node1', 'node2', 'node3'],
    load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='us-east-1')
)
session = cluster.connect('myapp')

# Quorum reads/writes (strong consistency, tolerates minority failure)
stmt = SimpleStatement(
    "SELECT * FROM users WHERE user_id = %s",
    consistency_level=ConsistencyLevel.LOCAL_QUORUM
)
rows = session.execute(stmt, [user_id])

# ONE for high-throughput writes (eventual consistency)
write_stmt = SimpleStatement(
    "INSERT INTO events (id, data) VALUES (%s, %s)",
    consistency_level=ConsistencyLevel.ONE
)
```

## Anti-Patterns to Avoid

- `ALLOW FILTERING` → full partition scan, never in production
- `SELECT COUNT(*)` on large tables → very slow
- Unbounded partition size (cap at ~100k rows or 100MB per partition)
- Secondary indexes on high-cardinality columns
- Large `IN` lists on partition keys → fan-out across nodes
- Batch for performance (batches = coordinator load, use async writes instead)
