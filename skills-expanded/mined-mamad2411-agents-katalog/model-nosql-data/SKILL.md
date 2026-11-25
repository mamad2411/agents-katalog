---
name: model-nosql-data
description: Models data for document, key-value, and wide-column stores access-pattern-first — enumerates queries, then picks partition/sort keys for even distribution, chooses embed-vs-reference per relationship, lays out single-table/aggregate items, denormalizes deliberately with a fan-out path, and avoids hot partitions.
when_to_use: When the datastore is non-relational (DynamoDB, MongoDB, Cassandra/ScyllaDB, Firestore, Bigtable) and you must shape items/documents/rows around queries — picking partition keys, embed vs reference, a single-table model, or a wide-column primary key — before writing the data layer. Distinct from design-relational-schema (normalized tables + joins) and optimize-sql-query (tunes an existing relational query); caching-strategy is a read cache in front of any store, not the store's own model.
---

## When to Use

Reach for this skill when you must **shape the store around its queries**, before any table/collection exists:

- "Design the DynamoDB table(s) for this service"
- "Should this be embedded or a separate collection in MongoDB?"
- "Pick the partition key and clustering columns for this Cassandra table"
- "We're getting hot partitions / throttling on one key — fix the key design"
- "Model a many-to-many (users↔teams, products↔orders) in a store with no joins"
- "Firestore/Bigtable layout for a feed/timeline read"

NOT this skill:
- A normalized schema with joins in a **relational** DB (entities, 3NF, FK/CHECK) → design-relational-schema
- A slow query against an existing **relational** schema → optimize-sql-query
- A read cache (TTL, invalidation, stampede) **in front of** the store → caching-strategy
- Schema *change* safety / locks / rollback on a live table → db-migration-safety
- Append-only event streams + projections as the system of record → design-event-sourcing-cqrs
- Background work / queue semantics → message-queue-jobs

## Steps

1. **Enumerate every access pattern first — this drives 100% of the design. No keys until this table is full.** One row per *operation*, reads and writes. A pattern you forget becomes a full scan in prod.

   | Pattern | R/W | Args (known at call time) | Result shape | Freq | Latency target | Selectivity |
   |---|---|---|---|---|---|---|
   | Get user by id | R | userId | 1 item | very high | <10ms | 1 |
   | List orders for user, newest first | R | userId, limit | N items, sorted | high | <20ms | bounded ~100s |
   | Get order + its line items | R | orderId | 1+M items | high | <20ms | bounded |
   | Create order (+ items, + user counter) | W | order, items | — | med | <30ms | multi-item |

   Rule: **you can only query by what you have in hand.** Every read's *Args* column must become a key or index prefix in step 3. If an Arg isn't a key, that read is a scan — reject the model.

2. **Confirm store-family fit before modeling.** Don't model a graph in a KV store.

   | Family | Pick when | Avoid when | Examples |
   |---|---|---|---|
   | **Document** | nested aggregate read/written as a unit; flexible fields; secondary indexes needed | heavy cross-doc joins; huge fan-out updates of shared data | MongoDB, Firestore |
   | **Wide-column** | massive write volume; time-series/feeds; query = known partition + range scan | ad-hoc queries on non-key columns; multi-key transactions | Cassandra, ScyllaDB, Bigtable |
   | **Key-value / single-table** | every access is by a designed key; you want one round trip per pattern | analytics / unpredictable query shapes | DynamoDB single-table, Redis-as-primary |

   Default for an app backend with a fixed, known pattern set: **document store** unless write volume or strict single-digit-ms-at-scale forces wide-column/DynamoDB.

3. **Design keys for distribution (partition) and range (sort) — distribution is non-negotiable.**
   - **Partition/hash key** = which physical shard. Choose **high-cardinality, evenly-requested** values: `userId`, `tenantId#userId`, `deviceId`. **Never** a low-cardinality or monotonic value (`status`, `country`, `true/false`, a date, an auto-increment) as the sole partition key — that is the #1 hot-partition cause.
   - **Sort/clustering key** = order *within* a partition and enables range/`begins_with` queries: `createdAt`, `ORDER#<ts>`, `<type>#<id>`. Compose it to serve range reads: items sorted newest-first, prefix-filterable.
   - DynamoDB single-table generic keys: `PK` / `SK` plus overloaded `GSI1PK`/`GSI1SK`. Encode the entity type in the key, not a separate column:

     ```
     PK              SK                   GSI1PK        GSI1SK
     USER#u1         PROFILE              —             —              # user profile
     USER#u1         ORDER#2026-06-15#o9  ORDER#o9      STATUS#PAID    # order under user, + lookup by order
     ORDER#o9        ITEM#li1             —             —              # line item under order
     ```
     `Query(PK=USER#u1, SK begins_with ORDER#)` → that user's orders, newest-first, one round trip, no scan.
   - **Bound every partition.** If items-per-partition grows without limit (all events under `PK=GLOBAL`, a celebrity's followers under one key), shard it: suffix `#<bucket 0..N-1>` (write-sharding) and scatter-gather on read, or split the partition by time (`PK=feed#u1#2026-06`).

4. **Embed vs reference — decide per relationship, default to embed for read-together.**

   | Embed (nest inside parent doc/item) | Reference (separate doc/item + id) |
   |---|---|
   | Read together almost always | Accessed independently / by other parents |
   | Child count **bounded & small** (≤ dozens) | Unbounded or large child set |
   | Child owned by exactly one parent | Shared across many parents |
   | Updated together / rarely | High-churn child, low-churn parent (write amplification) |
   | Total well under the item-size limit | Would blow the size limit |

   **Hard ceilings — model to them, not near them:** DynamoDB item **400 KB**; MongoDB document **16 MB**; Cassandra partition keep **< 100 MB / < 100k rows**. Embedding an unbounded array (comments, events, followers) eventually hits the ceiling and turns every append into a full-doc rewrite — **reference those.** Embed `address`, `lineItems` of one order; reference `comments`, `auditEvents`, `members`.

5. **Model M:N and secondary lookups as items/indexes — there are no joins.**
   - **Composite sort key** for one-to-many under a parent: `SK = ORDER#<ts>#<id>`, query by `begins_with(ORDER#)`.
   - **Adjacency list** for M:N in single-table: both directions are items. `PK=USER#u1, SK=TEAM#t1` *and* `PK=TEAM#t1, SK=USER#u1`. Query a user's teams by `PK=USER#u1, begins_with(TEAM#)`; a team's users by the mirror.
   - **GSI / inverted index** to query by a non-key attribute: project `email` into `GSI1PK=EMAIL#<email>` to "get user by email." Each new *read* pattern that doesn't fit the base key = one GSI (DynamoDB) or one secondary index (Mongo/Cassandra), not a scan.
   - Keep GSIs few and purposeful — each is a full extra copy of projected attributes (storage + write cost on every base write).

6. **Denormalize deliberately, and write the path that keeps the copies consistent.** Duplicating data (order carries `userName`, post carries `authorAvatar`) is correct NoSQL — *if* you own the fan-out:
   - **Single write touches multiple items** → use a **transaction** (DynamoDB `TransactWriteItems` ≤ 100 items; Mongo multi-doc txn) so the copies commit atomically.
   - **One source → many copies** (author renames → update 10k posts) → **async fan-out** via a stream (DynamoDB Streams / CDC / outbox), never a synchronous loop on the write path.
   - **Tolerate brief drift** → store a source-of-truth pointer and run **async repair**/reconciliation; never let two copies both claim authority.
   Pick one strategy per duplicated field and write it down — silent divergence is the failure mode.

7. **Time-ordering, TTL, and blob offload.**
   - Newest-first reads: make the sort key descending-friendly (`ORDER#<reverse-ts>` or query with `ScanIndexForward=false`); never client-side sort a scan.
   - Expiring data (sessions, OTPs, ephemeral feeds): set native **TTL** (DynamoDB TTL attribute, Mongo TTL index, Cassandra per-row TTL) — don't run a delete cron.
   - **Large/binary payloads** (images, PDFs, >100 KB blobs): store in object storage (S3/GCS) and keep only the **key/URL + metadata** in the item. Inlining blobs burns item-size budget and read throughput.

8. **Prove no full scans: map each access pattern to exactly one key/index path.** Re-walk the step-1 table; for every row write the resolved access: `Query(PK=…, SK …)` / `GetItem` / `Query(GSI1, …)`. If any row resolves to `Scan` or "filter after fetch on a non-key attribute," the model is incomplete — add a key, GSI, or duplicated item and repeat. A pattern with no index path is a bug, not a tradeoff.

## Common Errors

- **Designing keys before listing access patterns.** Guarantees a missing query path discovered in prod as a scan. Fill the step-1 table first, always.
- **Low-cardinality or monotonic partition key** (`status`, `date`, `true`, auto-increment id). Concentrates traffic on one shard → hot partition + throttling. Use a high-cardinality, evenly-hit key; write-shard or time-bucket if forced.
- **Embedding an unbounded array** (comments/events/followers inside the parent). Hits the 400 KB / 16 MB ceiling and makes every append rewrite the whole doc. Reference it as child items.
- **Modeling relational then "adding NoSQL on top."** Normalized tables + app-side joins = N+1 round trips and scans. Model the aggregate the query needs, even if it duplicates data.
- **A `Filter`/`$match` on a non-key field mistaken for a query.** DynamoDB `FilterExpression` and Mongo filters on un-indexed fields run *after* a scan reads everything — billed and slow. Make the filter field a key/index prefix.
- **Denormalized copy with no fan-out path.** `userName` cached in 10k orders, never updated on rename → permanent stale data. Define transaction / stream fan-out / async repair per duplicated field.
- **One GSI per attribute "just in case."** Each index is a full write-amplifying copy. Add a GSI only for an actual read pattern from step 1.
- **Synchronous fan-out on the write path** (loop updating thousands of copies in the request). Latency spikes and partial failures. Offload to a stream/queue.
- **Unbounded partition growth** (all rows under one `PK`, a whale tenant). Wide-column partition > ~100 MB degrades; DynamoDB throttles the key. Bucket by time or write-shard with a suffix.
- **Blobs inline in the item.** Caps how many items fit per read and wastes throughput. Offload to object storage, keep a pointer.

## Verify

1. **Coverage:** every step-1 access pattern maps to exactly one `Get`/`Query`/index path; **zero** resolve to `Scan` or post-fetch filter on a non-key field.
2. **Distribution:** the partition key is high-cardinality and request-even; no sole partition key is a status/boolean/date/sequence. Estimate items & bytes per hottest partition — under the family ceiling (DynamoDB ~10 GB/partition soft, Cassandra < 100 MB, Mongo doc < 16 MB, DynamoDB item < 400 KB).
3. **Range reads** return already-sorted (sort/clustering key does the ordering); no client-side sort over a fetched set.
4. **Embed/reference** justified per relationship against the step-4 table; no unbounded array embedded; largest realistic item stays well under the limit.
5. **M:N & secondary lookups** each have an explicit path (adjacency item pair, composite SK, or GSI) — confirm both directions of every M:N.
6. **Each denormalized field** names its consistency mechanism (transaction / stream fan-out / async repair); none has two authoritative copies.
7. **Throughput sim:** project read+write units (or ops/s) per partition under peak from step-1 frequencies; confirm no single key exceeds the per-partition limit; write-shard/time-bucket where it does.
8. **TTL** set on every ephemeral entity; **blobs > ~100 KB** offloaded to object storage with only a pointer stored.

Done = every access pattern resolves to a single non-scan key/index path, no partition key is hot or unbounded under projected peak load, every embedded relationship is bounded under the item-size limit, and every denormalized copy has a named write-path keeping it consistent.
