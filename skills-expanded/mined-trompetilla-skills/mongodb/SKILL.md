---
name: MongoDB
description: Design schemas, write queries, and configure MongoDB for consistency and performance.
metadata: {"clawdbot":{"emoji":"🍃","requires":{"anyBins":["mongosh","mongo"]},"os":["linux","darwin","win32"]}}
---

## Schema Design Decisions

- Embed when data is queried together and doesn't grow unboundedly
- Reference when data is large, accessed independently, or many-to-many
- Arrays that grow infinitely = disaster—document size limit 16MB; use bucketing pattern
- Denormalize for read performance, accept update complexity—no JOINs means duplicate data

## Array Pitfalls

- Arrays > 1000 elements hurt performance—pagination inside documents is hard
- `$push` without `$slice` = unbounded growth; use `$push: {$each: [...], $slice: -100}`
- Multikey indexes on arrays: index entry per element—can explode index size
- Can't have multikey index on more than one array field in compound index

## $lookup Is Not a JOIN

- `$lookup` performance degrades with collection size—no index usage on foreign collection (until 5.0)
- One `$lookup` per pipeline stage—nested lookups get complex and slow
- Consider embedding or application-side joins for frequent lookups
- `$lookup` with pipeline (5.0+) can filter before joining—massive performance improvement

## Index Strategy

- ESR rule for compound indexes: Equality fields first, Sort fields next, Range fields last
- MongoDB doesn't do efficient index intersection—single compound index often better than multiple
- Only one text index per collection—plan carefully; use Atlas Search for complex text
- TTL index for auto-expiration: `{createdAt: 1}, {expireAfterSeconds: 86400}`

## Aggregation Pipeline

- Stage order matters: `$match` and `$project` early to reduce documents flowing through
- `$match` at start can use indexes; `$match` after `$unwind` or `$lookup` cannot
- `allowDiskUse: true` for large aggregations—without it, 100MB memory limit per stage
- `$facet` for multiple aggregations in one query—but all facets process same documents

## Consistency & Transactions

- Default read/write concern not fully consistent—`{w: "majority", readConcern: "majority"}` for strong consistency
- Multi-document transactions since 4.0—but add latency and lock overhead; design to minimize
- Single-document operations are atomic—exploit this by embedding related data
- `retryWrites: true` in connection string—handles transient failures

## ObjectId Behavior

- Contains timestamp: `ObjectId.getTimestamp()`—can extract creation time
- Roughly time-ordered—can sort by `_id` for creation order
- Not random—predictable if you know creation time and machine; don't rely on for security
- 12 bytes: 4 timestamp + 5 random + 3 counter

## Explain & Performance

- `explain("executionStats")` shows actual execution—not just plan
- Look for `COLLSCAN`—means no index used; add appropriate index
- `totalDocsExamined` vs `nReturned`—ratio should be close to 1; otherwise index missing
- Covered queries: `IXSCAN` + `"totalDocsExamined": 0`—all data from index

## Document Size

- 16MB max per document—plan for this; use GridFS for large files
- BSON overhead: field names repeated per document—short names save space at scale
- Nested depth limit 100 levels—rarely hit but exists

## Read Preferences

- `primary` for strong consistency; `secondaryPreferred` for read scaling with eventual consistency
- Stale reads on secondaries—replication lag can be seconds
- `nearest` for lowest latency—but may read stale data
- Write always goes to primary—read preference doesn't affect writes

## Common Mistakes

- Treating MongoDB as "schemaless"—still need schema design; just enforced in app
- Not adding indexes—scans entire collection; every query pattern needs index
- Giant documents via array pushes—hit 16MB limit or slow BSON parsing
- Ignoring write concern—data may appear written but not persisted/replicated
