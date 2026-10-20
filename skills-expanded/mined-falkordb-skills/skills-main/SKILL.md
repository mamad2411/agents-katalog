---
name: falkordb-skills
description: >
  Practical FalkorDB guidance — Cypher queries, UDF management, Docker
  operations, and data ingestion. Use when writing or reviewing FalkorDB queries, setting up
  FalkorDB containers, working with user-defined functions, or migrating data from other sources.
license: MIT
metadata:
  author: FalkorDB
  version: "1.0"
---

## Conventions

- CLI examples use `redis-cli` unless noted.
- Cypher examples are passed as quoted strings to `GRAPH.QUERY`.
- Use parameterized queries for cache efficiency and safety.

---

## Cypher Skills

### 1) Create nodes and relationships

Create labeled nodes and connect them with properties.

Example:

```bash
redis-cli GRAPH.QUERY social "CREATE (alice:User {id: 1, name: 'Alice', email: 'alice@example.com'})
CREATE (bob:User {id: 2, name: 'Bob', email: 'bob@example.com'})
CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)"
```

### 2) Match patterns and return projections

Match by label/property and return fields.

Example:

```bash
redis-cli GRAPH.QUERY social "MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name"
```

### 3) Use MERGE to avoid duplicate nodes

Use `MERGE` when you want idempotent upserts.

Example:

```bash
redis-cli GRAPH.QUERY social "MERGE (u:User {id: 42})
ON CREATE SET u.name = 'Dana'
ON MATCH SET u.last_seen = timestamp()"
```

### 4) Update and remove properties safely

Use `SET` for updates and set properties to `NULL` to remove them (no `REMOVE` support).

Example:

```bash
redis-cli GRAPH.QUERY social "MATCH (u:User {id: 42})
SET u.email = 'dana@example.com', u.temp = NULL"
```

### 5) Use parameterized queries for cache reuse

Use parameters so the query plan is cached and reused.

Example:

```bash
redis-cli GRAPH.QUERY social "CYPHER name='Alice' MATCH (u:User {name: $name}) RETURN u.id"
```

### 6) Run safe read-only queries

Use `GRAPH.RO_QUERY` for read-only paths; it rejects writes.

Example:

```bash
redis-cli GRAPH.RO_QUERY social "MATCH (u:User) RETURN count(u)"
```

### 7) Inspect query plans before execution

Use `GRAPH.EXPLAIN` to validate plan shape and index usage without executing.

Example:

```bash
redis-cli GRAPH.EXPLAIN social "MATCH (p:Person {age: 30}) RETURN p"
```

### 8) Profile query runtime behavior

Use `GRAPH.PROFILE` to see per-operator runtime and records.

Example:

```bash
redis-cli GRAPH.PROFILE social "MATCH (u:User)-[:FRIENDS_WITH]->(f)
RETURN f.name ORDER BY f.name LIMIT 10"
```

### 9) Create range indexes for exact/range lookups

Use indexes to speed up equality and range predicates.

Example:

```bash
redis-cli GRAPH.QUERY social "CREATE INDEX FOR (p:Person) ON (p.age)"
```

### 10) Verify index usage

Confirm plan uses index scans.

Example:

```bash
redis-cli GRAPH.EXPLAIN social "MATCH (p:Person) WHERE p.age = 30 RETURN p"
```

### 11) Create and query full-text indexes

Use RediSearch-backed full-text indexes for text search.

Example:

```bash
redis-cli GRAPH.QUERY social "CALL db.idx.fulltext.createNodeIndex('Movie', 'title')"
redis-cli GRAPH.QUERY social "CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title"
```

### 12) Create and query vector indexes

Use HNSW vector indexes for ANN search.

Example:

```bash
redis-cli GRAPH.QUERY social "CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding)
OPTIONS {dimension: 768, similarityFunction: 'cosine', M: 32, efConstruction: 200}"

redis-cli GRAPH.QUERY social "CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32([0.1, 0.2, 0.3]))
YIELD node, score RETURN node.name, score"
```

### 13) Manage constraints with awareness of async creation

Create constraints and check status with `db.constraints()`.

Example:

```bash
redis-cli GRAPH.CONSTRAINT CREATE social UNIQUE NODE Person PROPERTIES 1 id
redis-cli GRAPH.QUERY social "CALL db.constraints()"
```

Note: Confirm the exact `GRAPH.CONSTRAINT CREATE` syntax against current docs before use.

### 14) Inspect graphs and memory usage

Use introspection commands for operational visibility.

Example:

```bash
redis-cli GRAPH.LIST
redis-cli GRAPH.INFO social
redis-cli GRAPH.MEMORY USAGE social
```

### 15) Track slow queries

Use slowlog to identify and reset slow queries.

Example:

```bash
redis-cli GRAPH.SLOWLOG social
redis-cli GRAPH.SLOWLOG social RESET
```

### 16) Apply FalkorDB Cypher limitations correctly

Account for known limitations in query design.

Example:

```bash
# Not-equal filters are not index-accelerated
redis-cli GRAPH.QUERY social "MATCH (p:Person) WHERE p.age <> 30 RETURN p"
```

---

## UDF Skills

### 1) Load a JavaScript UDF library

Register UDFs with `falkor.register` in JS.

Example:

```python
from falkordb import FalkorDB

db = FalkorDB(host='localhost', port=6379)
lib = "StringUtils"
script = """
function UpperCaseOdd(s) {
  return s.split('')
    .map((c, i) => i % 2 !== 0 ? c.toUpperCase() : c)
    .join('');
};

falkor.register('UpperCaseOdd', UpperCaseOdd);
"""

db.udf_load(lib, script)
```

### 2) Call a UDF from Cypher

UDFs behave like built-in functions.

Example:

```python
from falkordb import FalkorDB

db = FalkorDB(host='localhost', port=6379)
g = db.select_graph("social")
result = g.query("RETURN StringUtils.UpperCaseOdd('abcdef')").result_set
print(result)
```

### 3) List UDF libraries (with code)

Use `GRAPH.UDF LIST WITHCODE` to audit loaded libraries.

Example:

```bash
redis-cli GRAPH.UDF LIST WITHCODE
```

### 4) Delete or flush UDF libraries

Remove a specific library or flush all.

Example:

```bash
redis-cli GRAPH.UDF DELETE StringUtils
redis-cli GRAPH.UDF FLUSH
```

### 5) Respect UDF limitations

UDFs cannot mutate the graph; they must be pure functions.

Example:

```text
# Use UDFs for transformations only; do not attempt CREATE/SET/DELETE inside JS.
```

---

## Operations Skills (Docker)

### 1) Run FalkorDB with browser for local development

Expose both database and UI ports.

Example:

```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

### 2) Run server-only for production-style usage

Use the server-only image for lean deployments.

Example:

```bash
docker run -p 6379:6379 -it --rm falkordb/falkordb-server:latest
```

### 3) Set authentication using REDIS_ARGS

Pass Redis server flags via environment variables.

Example:

```bash
docker run -p 6379:6379 -p 3000:3000 -it \
  -e REDIS_ARGS="--requirepass yourpassword" \
  --rm falkordb/falkordb:latest
```

### 4) Set module config using FALKORDB_ARGS

Tune module-level settings (threads, timeout, cache size).

Example:

```bash
docker run -p 6379:6379 -p 3000:3000 -it \
  -e FALKORDB_ARGS="THREAD_COUNT 4 TIMEOUT 5000" \
  --rm falkordb/falkordb:latest
```

### 5) Use Docker Compose for repeatable local stacks

Define ports and env vars in a compose file.

Example:

```yaml
services:
  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6379:6379"
      - "3000:3000"
    environment:
      - REDIS_ARGS=--requirepass falkordb
      - FALKORDB_ARGS=THREAD_COUNT 4
```

### 6) Run the browser separately against a server

Use `FALKORDB_URL` to point the browser container to the server.

Example:

```yaml
services:
  falkordb-server:
    image: falkordb/falkordb-server:latest
    ports:
      - "6379:6379"
  falkordb-browser:
    image: falkordb/falkordb-browser:latest
    ports:
      - "3000:3000"
    environment:
      - FALKORDB_URL=redis://falkordb-server:6379
      - FALKORDB_PASSWORD=falkordb
```

---

## Ingestion Skills

### 1) Use Bulk Loader from CSV

Build FalkorDB databases from CSV inputs using the `falkordb-bulk-loader` Python utility.

Example:

```bash
falkordb-bulk-insert social \
  -n Users.csv \
  -N Company Companies.csv \
  -r FRIENDS_WITH friends.csv \
  -u redis://127.0.0.1:6379
```

### 2) Migrate Neo4j to FalkorDB

Extract data from Neo4j to CSV and load it into FalkorDB without APOC.

Example:

```bash
# 1. Extract from Neo4j
python3 neo4j_to_csv_extractor.py \
  --uri neo4j://localhost:7687 \
  --username neo4j \
  --password secret \
  --database movies

# 2. Load into FalkorDB
python3 falkordb_csv_loader.py \
  --config migrate_config.json \
  --dir csv_output
```

### 3) Migrate Neptune to FalkorDB

Convert AWS Neptune Export CSVs and load them into FalkorDB.

Example:

```bash
# 1. Convert Neptune CSVs to FalkorDB format
python3 neptune_to_falkordb_converter.py \
  --input-dir /path/to/neptune/export \
  --output-dir /path/to/falkordb/csvs

# 2. Bulk load the converted files
python3 bulk_load_to_falkordb.py \
  --input-dir /path/to/falkordb/csvs \
  --graph my_graph \
  --host 127.0.0.1 \
  --port 6379
```

### 4) Migrate SQL to FalkorDB

Migrate and continuously sync data from SQL systems (e.g., PostgreSQL) into FalkorDB.

Example:

```bash
# Build the tool
cd PostgreSQL-to-FalkorDB/postgres-to-falkordb
cargo build --release

# Single run
cargo run --release -- --config config.yaml

# Continuous sync
cargo run --release -- --config config.yaml --daemon --interval-secs 60
```
