-----

## name: wide-column-stores
description: >
Expert wide-column database design and operations for Cassandra, ScyllaDB, HBase, and
Google Bigtable. Always use this skill when the user mentions Cassandra, CQL, ScyllaDB,
HBase, Bigtable, wide-column, or column-family databases. Also trigger for: designing
partition keys or clustering columns, modeling time-series data at scale, handling
tombstones or compaction, tuning consistency levels, avoiding hot partitions, migrating
from relational to wide-column, writing CQL queries, or building high-throughput
write-heavy workloads. Trigger even if the user just says “NoSQL database for
time-series” or “high write throughput database” — wide-column is often the right answer.
license: MIT
compatibility: opencode
metadata:
audience: developers
category: databases

# Wide-Column Stores

Covers: **Cassandra / ScyllaDB · HBase · Bigtable · Data Modeling · Operations · Performance**

> **Choose your system**: Cassandra/ScyllaDB for leaderless, multi-region, general-purpose. HBase for Hadoop ecosystem integration. Bigtable for managed GCP workloads with minimal ops overhead.

-----

## Core Concepts

Wide-column stores are fundamentally different from relational databases. Internalize these before modeling:

- **Query-first design**: Model your tables around your queries, not your entities. There are no joins.
- **Partition key**: Determines which node holds the data. All rows sharing a partition key are co-located and returned together efficiently.
- **Clustering columns**: Sort order within a partition. Range queries only work on clustering columns, not partition keys.
- **Denormalization is expected**: Duplicate data across tables for different access patterns. Storage is cheap; cross-partition reads are not.
- **Writes are cheap, deletes are expensive**: Deletes create tombstones that linger until compaction. Design to avoid them.

-----

## Cassandra / ScyllaDB

### Data Modeling — Query-First Workflow

Start by listing all queries your application needs, then design one table per query pattern.

```
Application queries:
  Q1. Get all orders for a customer (sorted by date desc)
  Q2. Get orders by status for a given day
  Q3. Get a single order by ID

→ Three tables, one per query.
```

```sql
-- Q1: orders by customer
CREATE TABLE orders_by_customer (
    customer_id  UUID,
    order_date   TIMESTAMP,
    order_id     UUID,
    status       TEXT,
    total        DECIMAL,
    items        LIST<FROZEN<order_item>>,
    PRIMARY KEY (customer_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id ASC)
  AND default_time_to_live = 7776000;  -- 90 days TTL

-- Q2: orders by status + date (compound partition key spreads load)
CREATE TABLE orders_by_status_date (
    status       TEXT,
    order_date   DATE,
    order_id     UUID,
    customer_id  UUID,
    total        DECIMAL,
    PRIMARY KEY ((status, order_date), order_id)
);

-- Q3: single order lookup
CREATE TABLE orders_by_id (
    order_id    UUID PRIMARY KEY,
    customer_id UUID,
    order_date  TIMESTAMP,
    status      TEXT,
    total       DECIMAL
);
```

### Partition Key Design

The partition key is the most consequential modeling decision. A bad partition key causes hot spots — one node overwhelmed while others sit idle.

```sql
-- ❌ Bad: low cardinality — all "PENDING" orders land on one node
PRIMARY KEY (status, order_id)

-- ❌ Bad: unbounded growth — one partition holds all of a user's lifetime data
PRIMARY KEY (user_id, created_at)

-- ✅ Good: bucket by time to bound partition size
PRIMARY KEY ((user_id, bucket), created_at, event_id)
-- where bucket = YYYY-MM or YYYY-WW depending on write volume

-- ✅ Good: compound partition key spreads hot keys
PRIMARY KEY ((region, shard), timestamp, device_id)
-- where shard = device_id % 10  (computed in application)
```

**Partition size rule of thumb**: Keep partitions under 100MB / 100k rows. Use `nodetool tablestats` to check.

### Time-Series Pattern

```sql
-- IoT sensor readings bucketed by day
CREATE TABLE sensor_readings (
    sensor_id   TEXT,
    day         DATE,           -- bucket
    ts          TIMESTAMP,      -- clustering: allows range queries
    value       DOUBLE,
    quality     TINYINT,
    PRIMARY KEY ((sensor_id, day), ts)
) WITH CLUSTERING ORDER BY (ts DESC)
  AND compaction = {
      'class': 'TimeWindowCompactionStrategy',
      'compaction_window_unit': 'DAYS',
      'compaction_window_size': 1
  };

-- Query: last hour of readings for sensor
SELECT * FROM sensor_readings
WHERE sensor_id = 'sensor-42'
  AND day = '2024-03-15'
  AND ts >= '2024-03-15 14:00:00'
  AND ts <= '2024-03-15 15:00:00';
```

### Consistency Levels

```sql
-- Write with quorum, read with quorum = strong consistency
CONSISTENCY QUORUM;
INSERT INTO orders_by_id (order_id, status) VALUES (uuid(), 'PENDING');

-- LOCAL_QUORUM for multi-DC: consistency within local DC only (lower latency)
CONSISTENCY LOCAL_QUORUM;

-- ONE for high-throughput writes where occasional loss is acceptable
CONSISTENCY ONE;
```

|Level         |Writes                |Reads              |Use Case        |
|--------------|----------------------|-------------------|----------------|
|`ONE`         |Fastest, least durable|May return stale   |Metrics, logs   |
|`LOCAL_QUORUM`|Balanced              |Consistent locally |Most OLTP       |
|`QUORUM`      |Slower cross-DC       |Strongly consistent|Financial data  |
|`ALL`         |Slowest               |Guaranteed fresh   |Rarely justified|

### Lightweight Transactions (LWT)

Use sparingly — LWT is 4x slower than regular writes due to Paxos rounds.

```sql
-- Conditional insert (only if not exists)
INSERT INTO users (user_id, email, created_at)
VALUES (uuid(), 'jane@example.com', toTimestamp(now()))
IF NOT EXISTS;

-- Conditional update
UPDATE accounts SET balance = 950.00
WHERE account_id = ? 
IF balance = 1000.00;  -- optimistic lock
```

### Batch Writes

```sql
-- UNLOGGED batch: use only for writes to the SAME partition (atomicity within partition)
BEGIN UNLOGGED BATCH
    INSERT INTO orders_by_customer (customer_id, order_date, order_id, status)
        VALUES (?, ?, ?, ?);
    INSERT INTO orders_by_id (order_id, customer_id, status)
        VALUES (?, ?, ?);
APPLY BATCH;

-- ❌ Never use LOGGED batch across partitions for performance — it's a coordinator bottleneck
```

### CQL Operations

```sql
-- Collections
UPDATE users SET tags = tags + {'vip', 'early-adopter'} WHERE user_id = ?;
UPDATE users SET tags = tags - {'trial'} WHERE user_id = ?;

-- TTL per-row or per-column
INSERT INTO sessions (session_id, user_id, data)
VALUES (?, ?, ?) USING TTL 86400;  -- expires in 24h

-- Counter tables (special type, cannot mix with regular columns)
CREATE TABLE page_views (
    page_id TEXT PRIMARY KEY,
    views   COUNTER
);
UPDATE page_views SET views = views + 1 WHERE page_id = 'home';

-- Materialized views (use with caution — write amplification)
CREATE MATERIALIZED VIEW orders_by_status AS
    SELECT * FROM orders_by_id
    WHERE status IS NOT NULL AND order_id IS NOT NULL
    PRIMARY KEY (status, order_id);
```

-----

## HBase

HBase rows are sorted lexicographically by row key. Design row keys with this in mind.

```java
// Table schema — all "columns" in HBase are actually column qualifiers under a family
// Family: "cf" (column family) — keep families to 1-3, they map to store files
TableDescriptor table = TableDescriptorBuilder
    .newBuilder(TableName.valueOf("events"))
    .setColumnFamily(ColumnFamilyDescriptorBuilder
        .newBuilder(Bytes.toBytes("cf"))
        .setMaxVersions(3)
        .setCompressionType(Compression.Algorithm.SNAPPY)
        .setBloomFilterType(BloomType.ROW)
        .build())
    .build();
admin.createTable(table);

// Row key design: reverse timestamp to get latest-first ordering
// Pattern: <entity_id>~<reverse_timestamp>
long reverseTs = Long.MAX_VALUE - System.currentTimeMillis();
String rowKey = String.format("%s~%016d", userId, reverseTs);

// Write
Put put = new Put(Bytes.toBytes(rowKey));
put.addColumn(CF, Bytes.toBytes("action"), Bytes.toBytes("login"));
put.addColumn(CF, Bytes.toBytes("ip"), Bytes.toBytes("192.168.1.1"));
table.put(put);

// Scan with row key prefix (efficient — uses lexicographic ordering)
Scan scan = new Scan()
    .withStartRow(Bytes.toBytes(userId + "~"))
    .withStopRow(Bytes.toBytes(userId + "~" + "9".repeat(16)))
    .addColumn(CF, Bytes.toBytes("action"))
    .setLimit(100);

ResultScanner scanner = table.getScanner(scan);
for (Result r : scanner) {
    System.out.println(Bytes.toString(r.getValue(CF, Bytes.toBytes("action"))));
}
scanner.close();
```

### HBase Row Key Patterns

```
# ❌ Bad: monotonic timestamp prefix → all writes go to one region (hot spot)
rowKey = timestamp + userId

# ✅ Salt prefix: distribute across N regions
rowKey = (hash(userId) % 16) + "|" + userId + "|" + timestamp

# ✅ Reverse timestamp for latest-first
rowKey = userId + "~" + (Long.MAX_VALUE - timestamp)

# ✅ Composite key for range + entity queries
rowKey = customerId + "#" + orderDate + "#" + orderId
```

-----

## Google Bigtable

Bigtable uses the same model as HBase (it inspired it) but is fully managed on GCP.

```python
from google.cloud import bigtable
from google.cloud.bigtable import column_family, row_filters

client = bigtable.Client(project="my-project", admin=True)
instance = client.instance("my-instance")
table = instance.table("user-events")

# Write
row_key = f"user#{user_id}#{str(int(time.time() * 1000)).zfill(16)}"
row = table.direct_row(row_key)
row.set_cell("events", "action", "purchase", timestamp=datetime.utcnow())
row.set_cell("events", "amount", str(amount), timestamp=datetime.utcnow())
row.commit()

# Read single row
row = table.read_row(row_key.encode())

# Scan with prefix filter (all events for a user)
prefix = f"user#{user_id}#".encode()
rows = table.read_rows(
    filter_=row_filters.RowKeyRegexFilter(prefix + b".*"),
    limit=500
)
for row in rows:
    for cf, cols in row.cells.items():
        for qualifier, cells in cols.items():
            print(qualifier.decode(), cells[0].value.decode())
```

-----

## Anti-Patterns to Avoid

|Anti-Pattern                     |Problem                                     |Fix                                                |
|---------------------------------|--------------------------------------------|---------------------------------------------------|
|Unbounded partition growth       |Partition becomes a hotspot; reads slow down|Bucket by time or hash                             |
|Low-cardinality partition key    |All traffic to one node                     |Add a shard suffix                                 |
|`SELECT *` with `ALLOW FILTERING`|Full table scan, kills performance          |Model a proper table for the query                 |
|Large blobs in cells (>1MB)      |Compaction pressure, slow reads             |Store in object storage; keep reference in DB      |
|Excessive tombstones             |Read performance degrades                   |Use TTL instead of deletes; tune `gc_grace_seconds`|
|Logged batches across partitions |Coordinator bottleneck                      |Use async writes from application layer            |
|Treating wide-column like SQL    |Joins, ad-hoc queries fail                  |Accept denormalization, one table per query        |

-----

## Operations

```bash
# Cassandra nodetool essentials
nodetool status                     # ring health, node states
nodetool tablestats keyspace.table  # partition size, read/write latency
nodetool compactionstats            # pending compactions
nodetool repair keyspace            # anti-entropy repair (run weekly)
nodetool flush                      # force memtable → SSTable

# Find large partitions (Cassandra 4+)
nodetool toppartitions keyspace table 10  # top 10 largest partitions

# Schema inspection
DESCRIBE KEYSPACE my_keyspace;
DESCRIBE TABLE orders_by_customer;

# Performance: tracing a slow query
TRACING ON;
SELECT * FROM orders_by_customer WHERE customer_id = ? LIMIT 10;
TRACING OFF;
```

### Compaction Strategy Selection

|Strategy                                  |Best For                                       |
|------------------------------------------|-----------------------------------------------|
|`SizeTieredCompactionStrategy` (default)  |Write-heavy, general purpose                   |
|`LeveledCompactionStrategy`               |Read-heavy, small SSTables, predictable latency|
|`TimeWindowCompactionStrategy`            |Time-series data with TTL                      |
|`UnifiedCompactionStrategy` (Cassandra 5+)|Modern default, adaptive                       |