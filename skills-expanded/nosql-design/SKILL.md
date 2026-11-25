---
name: nosql-design
description: Designs and reviews MongoDB, DynamoDB and Redis usage from access patterns - keys and indexes, query shapes, hot partitions, document and item size limits, atomic updates, transactions, TTLs, Redis data structures, eviction and persistence. Use when choosing a key or index, writing NoSQL queries, debugging slow or expensive MongoDB, DynamoDB or Redis operations, or deciding whether NoSQL fits at all.
license: MIT
---

# NoSQL Design

NoSQL stores are fast only for the queries they were designed for. Write down every access pattern first, then design keys and indexes so each one is a direct lookup or an indexed range read. If the access patterns are unknown, ad-hoc, or heavy on joins and reporting, recommend a relational database instead.

## When to use

- Designing collections, tables or key layouts in MongoDB, DynamoDB or Redis (or compatible stores such as Valkey).
- A NoSQL query is slow, scans too much, or costs too much read/write capacity.
- Hot partitions or shards, throttling, memory pressure or evictions in Redis.
- Choosing between NoSQL and a relational database for a new feature.

Not for: the embed-vs-reference and single-table basics (covered in the database-schema-design skill's `references/nosql-modeling.md`), or using Redis purely as a cache layer (use caching-strategies).

## Workflow

1. **Fill in the access-pattern worksheet** ([references/access-pattern-worksheet.md](references/access-pattern-worksheet.md)): every read and write, its inputs, result size, frequency and consistency need.
2. **Check fit** with the table below. If several "choose relational" rows apply, say so before designing.
3. **Design keys and indexes** so every pattern maps to one of: get by key, query a key range, or an index lookup. Write the mapping into the worksheet.
4. **Check limits**: document/item size, partition throughput, array growth, memory.
5. **Verify with the store's tools**: `explain("executionStats")` in MongoDB, consumed capacity in DynamoDB (`ReturnConsumedCapacity`), `SLOWLOG` and `--bigkeys` in Redis.
6. **Get confirmation** before running anything destructive on shared data (dropping indexes or collections, `FLUSHALL`, mass deletes, table deletion).

## NoSQL or relational?

| Choose NoSQL when | Choose relational (for example PostgreSQL, possibly with JSON columns) when |
|---|---|
| Access patterns are known and few | Queries are ad-hoc or change often |
| Most reads fetch one entity or one key range | You need joins across many entity types |
| Scale or latency needs exceed one relational node | Data fits comfortably on one well-tuned server |
| The data is naturally a document, a key or a time series | Many-to-many relationships are central |
| Single-item atomicity is enough | Business operations must be atomic across many entities |
| | Analysts need SQL over the live data |

## MongoDB

**Indexes and queries**

- Build compound indexes with the **ESR rule**: fields matched by **E**quality first, then fields you **S**ort on, then fields filtered by **R**ange (`$gt`, `$lt`, `$in` with many values).
- Check every important query with `db.orders.find(q).sort(s).explain("executionStats")`: a `COLLSCAN` stage, or `totalDocsExamined` much larger than `nReturned`, means the index doesn't fit the query.
- A query is **covered** (answered from the index alone) when the filter and projection use only indexed fields and `_id` is excluded from the projection.
- Partial indexes (`partialFilterExpression`) index only the documents a query targets, such as `{ status: "open" }`.
- TTL indexes (`{ expireAfterSeconds: N }` on a date field) delete expired documents in the background; deletion is not immediate.
- Every index slows writes and uses memory. Remove unused ones (`$indexStats` shows usage).

**Writes and consistency**

- Use update operators for atomic single-document changes: `$inc`, `$set`, `$push` with `$each` and `$slice` to keep an array capped. Never read, modify in code, and write the whole document back.
- Single-document writes are atomic. Multi-document transactions exist but cost more and have time and size limits; prefer designs where one operation updates one document.
- Use `writeConcern: { w: "majority" }` for data you cannot lose, and a matching read concern when reads must see committed data.
- Enforce required fields and types with `$jsonSchema` validation on the collection, and business uniqueness with unique indexes.

**Scale**

- Avoid unbounded arrays and huge documents (hard limit 16 MB; performance suffers far earlier).
- `$lookup` is a join. If a hot path needs it, the model probably needs embedding or a copied field.
- Shard key: high cardinality, evenly spread writes, and present in most queries. A monotonically increasing key (timestamp, ObjectId) sends all inserts to one shard; use a hashed or compound key instead.

## DynamoDB

**Keys and reads**

- Every pattern should be a `GetItem` or a `Query` on the table or an index. `Scan` reads the whole table and is for rare batch jobs only.
- `FilterExpression` is applied **after** items are read: you still pay for every item the key condition matched. Push selectivity into the key or an index.
- `Query` returns results in pages (up to 1 MB per page). Always loop on `LastEvaluatedKey`.
- Strongly consistent reads (`ConsistentRead: true`) work on the table and local secondary indexes, not on global secondary indexes.
- Sparse indexes: a GSI includes only items that have its key attributes. Use this for "items in state X" queries.

**Writes**

- Use conditional writes for invariants: `attribute_not_exists(PK)` for create-only, `version = :expected` for optimistic locking, `stock >= :qty` for reservations.
- Use update expressions for atomic changes (`SET #c = #c + :one`, `ADD`), not read-modify-write.
- `BatchWriteItem` and `BatchGetItem` can return `UnprocessedItems` / `UnprocessedKeys`. Retry those with backoff, or data is silently dropped.
- `TransactWriteItems` gives all-or-nothing across items, at higher cost. Check current item-count limits in the docs.

**Throughput**

- Hot partitions throttle no matter how much table capacity you have. Spread hot keys (add a random or computed suffix and query the shards in parallel), and avoid low-cardinality partition keys such as a status or a date.
- On-demand capacity suits spiky or unknown traffic; provisioned with auto scaling is cheaper for steady load.
- Item size limit is 400 KB. Store large blobs in object storage and keep a pointer.
- Use TTL for expiring items; deletion happens in the background, so filter expired items in reads if exactness matters.

## Redis

Pick the data structure by the operation you need:

| Need | Structure | Key commands |
|---|---|---|
| Cache a value, counter, flag | String | `SET key val EX 300`, `INCR`, `SET ... NX` |
| Object with fields | Hash | `HSET`, `HGET`, `HINCRBY` |
| Queue / recent items | List | `LPUSH`, `RPOP`, `LTRIM` to cap length |
| Unique members, membership test | Set | `SADD`, `SISMEMBER`, `SCARD` |
| Leaderboard, priority, time-ordered index | Sorted set | `ZADD`, `ZRANGE ... BYSCORE`, `ZRANGE ... REV` (replaces the deprecated `ZREVRANGE`), `ZREMRANGEBYSCORE` |
| Durable event log with consumer groups | Stream | `XADD`, `XREADGROUP`, `XACK`, `XAUTOCLAIM` |
| Fire-and-forget notifications | Pub/Sub | `PUBLISH`, `SUBSCRIBE` (messages are lost if no subscriber is connected) |

Rules:

- **Never run `KEYS` in production**: it blocks the server while it walks every key. Use `SCAN` with `MATCH` and `COUNT`. Same caution for other O(N) commands on big keys (`HGETALL`, `SMEMBERS`, `LRANGE 0 -1`). Delete big keys with `UNLINK`, not `DEL`.
- Set a TTL on everything that is not meant to live forever. Namespace keys (`app:env:entity:id`).
- **Memory limits**: set `maxmemory` and choose `maxmemory-policy` on purpose. The default `noeviction` makes writes fail when memory is full; `allkeys-lru` or `allkeys-lfu` suit a pure cache; `volatile-*` policies evict only keys with a TTL.
- **Persistence**: RDB snapshots lose writes since the last snapshot; AOF with `appendfsync everysec` loses about one second. If Redis holds data you can't rebuild, configure persistence and replication deliberately and test recovery. Otherwise treat it as a cache.
- Find problems with `redis-cli --bigkeys`, `redis-cli --memkeys`, `SLOWLOG GET 20` and `INFO memory`.
- Use pipelining to batch many commands in one round trip; use `MULTI`/`EXEC` or a Lua script when several commands must apply together.
- In Redis Cluster, multi-key commands need all keys in the same hash slot; use hash tags (`{user:42}:cart`, `{user:42}:profile`).
- Simple locks: `SET lock:job token NX PX 30000`, and release only if the value still matches your token (a short Lua compare-and-delete). Such locks are best-effort; for correctness-critical mutual exclusion, also use a fencing token or a database constraint.

## Anti-patterns

- **Designing the schema before listing the queries.**
- **Scans and filters doing the job of a key**: DynamoDB `Scan` + `FilterExpression`, MongoDB queries without a supporting index.
- **Low-cardinality partition or shard keys** (status, country, today's date) causing hot partitions.
- **Unbounded arrays** in MongoDB documents and unbounded lists or sets in Redis.
- **Ignoring `UnprocessedItems`** in DynamoDB batch writes.
- **Redis as the only copy of important data** without tested persistence.
- **`KEYS *` in application code or scripts against production.**
- **Picking NoSQL for a reporting-heavy, join-heavy domain.**

## Done when

- Every access pattern in the worksheet maps to a key lookup, key range or index, with no scans on hot paths.
- `explain`, consumed-capacity or `SLOWLOG` output confirms the important queries behave as designed.
- Keys spread load evenly; item, document and collection sizes stay bounded.
- Invariants are enforced with atomic operators, conditional writes, unique indexes or schema validation.
- Redis has `maxmemory`, an eviction policy, TTLs and a persistence decision that matches what it stores.

## References

- [references/access-pattern-worksheet.md](references/access-pattern-worksheet.md) — read at the start of any NoSQL design or review: the worksheet template with a worked example for MongoDB and DynamoDB.
