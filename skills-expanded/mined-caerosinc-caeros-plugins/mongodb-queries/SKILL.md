---
name: mongodb-queries
description: Write and tune MongoDB reads and writes, CRUD operators, aggregation pipelines, indexes, and explain plans. Use when the user is querying MongoDB, building a pipeline, or debugging a slow query.
---

# MongoDB Queries

Works the same in mongosh, drivers, and the MongoDB MCP server tools
(`find`, `aggregate`, `count`, `insert-many`, `update-many`, `delete-many`).

## CRUD essentials

```js
db.users.insertOne({ email: "a@b.co", plan: "free", createdAt: new Date() })
db.users.find({ plan: "pro" }, { email: 1, _id: 0 }).sort({ createdAt: -1 }).limit(20)
db.users.updateOne({ _id: id }, { $set: { plan: "pro" }, $inc: { logins: 1 } })
db.users.updateOne({ email: "a@b.co" }, { $setOnInsert: { createdAt: new Date() } }, { upsert: true })
db.users.deleteMany({ deactivatedAt: { $lt: cutoff } })
```

- Operators to reach for: `$in`, `$gte`/`$lte`, `$exists`, `$regex` (anchor with
  `^` or it cannot use an index), `$elemMatch` for matching one array element
  against multiple conditions, `$push`/`$pull`/`$addToSet` for array writes.
- `updateMany` with `$set` never replaces the document; a bare replacement doc
  in `replaceOne` does. Mixing them is the classic data-loss mistake.
- Bulk writes: `db.coll.bulkWrite([...], { ordered: false })` keeps going past
  individual failures and is much faster than looped single writes.

## Aggregation pipelines

Stage order matters: filter early, project late.

```js
db.orders.aggregate([
  { $match: { status: "paid", createdAt: { $gte: since } } },   // uses indexes
  { $group: { _id: { m: { $dateTrunc: { date: "$createdAt", unit: "month" } } },
              revenue: { $sum: "$total" }, n: { $count: {} } } },
  { $sort: { "_id.m": 1 } },
])
```

- Joins: `$lookup` (+ `$unwind` if you need one row per match). Prefer a
  pipeline-form `$lookup` with its own `$match` to limit joined docs.
- `$facet` runs sub-pipelines in one pass (results + total count for paging).
- `$project`/`$addFields` for reshaping; `$replaceRoot` to promote a subdoc.
- Memory: stages are capped at 100MB; add `{ allowDiskUse: true }` for big
  sorts/groups, but treat that as a smell, usually a missing index or filter.

## Indexes

```js
db.orders.createIndex({ userId: 1, createdAt: -1 })
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 })    // TTL
db.users.createIndex({ email: 1 }, { unique: true })
db.events.createIndex({ type: 1 }, { partialFilterExpression: { archived: false } })
```

- Compound index field order: **ESR** (Equality first, Sort second, Range last).
  `{ userId: 1, createdAt: -1 }` serves `userId = X ORDER BY createdAt DESC`.
- A query can generally use one index (plus `$or` branches). An index on
  `{ a: 1, b: 1 }` covers prefix queries on `a` alone, not `b` alone.
- Indexes cost writes and RAM: drop unused ones
  (`db.coll.aggregate([{ $indexStats: {} }])` shows usage counts).

## explain

```js
db.orders.find({ userId: u }).sort({ createdAt: -1 }).explain("executionStats")
```

Read it in this order:

1. `winningPlan`: `COLLSCAN` means no usable index; `IXSCAN` names the index.
2. A `SORT` stage means the sort was in memory; fix with an index matching the
   sort order.
3. `executionStats.totalDocsExamined` vs `nReturned`: a large ratio means the
   index is not selective enough (or filters run after the fetch).

## Gotchas

- `_id` is immutable; ObjectId embeds a timestamp
  (`ObjectId().getTimestamp()`), so `_id` sorts roughly by insert time.
- Comparing against `null` matches both null values and missing fields; use
  `$type` or `$exists` to tell them apart.
- Dates: store BSON `Date`, never strings; string dates break range queries
  and `$dateTrunc`.
- Case-insensitive matching: use a collation
  (`{ collation: { locale: "en", strength: 2 } }`) with a matching index, not
  `$regex` with `i` (which scans).
