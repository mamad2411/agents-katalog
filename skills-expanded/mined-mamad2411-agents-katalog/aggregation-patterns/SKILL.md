---
name: aggregation-patterns
description:
  This skill should be used when writing MongoDB aggregation pipelines, using $lookup, $group,
  $merge, or optimizing pipeline performance. It provides pipeline stage ordering rules, $lookup vs
  app-side join guidance, $facet patterns, $merge for materialized views, pipeline optimization
  techniques, and $out vs $merge comparisons.
version: 0.1.0
---

# Aggregation Patterns Skill

This skill defines the conventions, rules, and best practices for MongoDB aggregation pipelines.
Apply these rules when writing new pipelines, reviewing existing pipelines, or optimizing
aggregation performance.

---

## Table of Contents

1. [Pipeline Stage Ordering Rules](#pipeline-stage-ordering-rules)
2. [$lookup vs App-Side Joins](#lookup-vs-app-side-joins)
3. [$facet Patterns](#facet-patterns)
4. [$merge for Materialized Views](#merge-for-materialized-views)
5. [$out vs $merge](#out-vs-merge)
6. [Pipeline Optimization Rules](#pipeline-optimization-rules)
7. [Common Aggregation Patterns](#common-aggregation-patterns)

---

## Pipeline Stage Ordering Rules

### Rule PO-1: $match Must Be the First Stage

Always place `$match` as the first stage in the pipeline. This filters documents early, reducing the
workload for all subsequent stages. When `$match` is the first stage, it can use indexes.

```javascript
// CORRECT — $match first, uses index on { status: 1, orderDate: 1 }
db.orders.aggregate([
  {
    $match: { status: 'completed', orderDate: { $gte: ISODate('2024-01-01') } },
  },
  { $group: { _id: '$customerId', total: { $sum: '$amount' } } },
  { $sort: { total: -1 } },
  { $limit: 100 },
]);
```

```javascript
// WRONG — $match after $group (processes entire collection first)
db.orders.aggregate([
  {
    $group: {
      _id: { customerId: '$customerId', status: '$status' },
      total: { $sum: '$amount' },
    },
  },
  { $match: { '_id.status': 'completed' } },
  // By now, ALL orders have been grouped — waste of resources
]);
```

When multiple `$match` conditions exist, split them if an early `$match` can reduce the dataset
significantly:

```javascript
// CORRECT — split $match: index-supported filter first
db.orders.aggregate([
  { $match: { status: 'completed' } }, // Uses index
  { $lookup: { from: 'customers' /* ... */ } },
  { $match: { 'customer.tier': 'premium' } }, // Post-lookup filter
]);
```

### Rule PO-2: $project Before $group

Reduce document size before grouping to minimize memory consumption during the `$group` stage.

```javascript
// CORRECT — project only needed fields before $group
db.orders.aggregate([
  { $match: { status: 'completed' } },
  { $project: { customerId: 1, amount: 1, orderDate: 1 } },
  {
    $group: {
      _id: '$customerId',
      totalAmount: { $sum: '$amount' },
      orderCount: { $sum: 1 },
    },
  },
]);
```

```javascript
// WRONG — $group receives full documents (50+ fields each)
db.orders.aggregate([
  { $match: { status: 'completed' } },
  // No projection — all fields flow into $group
  {
    $group: {
      _id: '$customerId',
      totalAmount: { $sum: '$amount' }, // Only uses 2 fields
      orderCount: { $sum: 1 },
    },
  },
  // Memory wasted holding 48 unused fields per document
]);
```

### Rule PO-3: $sort + $limit Must Be Adjacent

When sorting and limiting results, place `$sort` immediately before `$limit`. MongoDB optimizes this
combination by only tracking the top N documents during sorting, dramatically reducing memory usage.

```javascript
// CORRECT — adjacent $sort + $limit (optimized)
db.products.aggregate([
  { $match: { status: 'active' } },
  { $group: { _id: '$category', avgPrice: { $avg: '$price' } } },
  { $sort: { avgPrice: -1 } },
  { $limit: 10 },
  // MongoDB only tracks top 10 during sort
]);
```

```javascript
// WRONG — stage between $sort and $limit
db.products.aggregate([
  { $match: { status: 'active' } },
  { $group: { _id: '$category', avgPrice: { $avg: '$price' } } },
  { $sort: { avgPrice: -1 } },
  { $addFields: { rank: 'top' } }, // Breaks sort+limit coalescing
  { $limit: 10 },
  // MongoDB must sort ALL groups before limiting
]);
```

### Rule PO-4: $match + $sort Uses Compound Indexes

When `$match` is followed by `$sort` at the pipeline start, and a compound index covers both, the
operation is fully index-supported.

```javascript
// Given index: { status: 1, createdAt: -1 }

// CORRECT — $match + $sort uses the compound index
db.orders.aggregate([
  { $match: { status: 'completed' } },
  { $sort: { createdAt: -1 } },
  { $limit: 50 },
]);
// IXSCAN: no in-memory sort needed
```

```javascript
// WRONG — $sort on an unindexed field
db.orders.aggregate([
  { $match: { status: 'completed' } },
  { $sort: { total: -1 } }, // No index covers status + total sort
  { $limit: 50 },
  // In-memory sort of potentially millions of documents
]);
```

### Rule PO-5: Avoid $unwind on Large Arrays

`$unwind` creates one document per array element. Prefer array operators (`$filter`, `$map`,
`$reduce`, `$size`) when possible.

```javascript
// CORRECT — use $filter instead of $unwind + $match + $group
db.orders.aggregate([
  { $match: { customerId: ObjectId('...') } },
  {
    $addFields: {
      electronicItems: {
        $filter: {
          input: '$items',
          as: 'item',
          cond: { $eq: ['$$item.category', 'electronics'] },
        },
      },
    },
  },
  { $match: { 'electronicItems.0': { $exists: true } } },
]);
```

```javascript
// WRONG — $unwind for simple filtering
db.orders.aggregate([
  { $match: { customerId: ObjectId('...') } },
  { $unwind: '$items' }, // 50 items = 50 docs
  { $match: { 'items.category': 'electronics' } },
  {
    $group: {
      // Regroup back
      _id: '$_id',
      items: { $push: '$items' },
      orderDate: { $first: '$orderDate' },
    },
  },
]);
```

When `$unwind` is necessary, use `preserveNullAndEmptyArrays`:

```javascript
// CORRECT — preserve documents with missing/empty arrays
{ $unwind: { path: "$tags", preserveNullAndEmptyArrays: true } }

// WRONG — silently drops documents without tags
{ $unwind: "$tags" }
```

### Rule PO-6: Limit Documents Before Expensive Stages

Place `$limit` (or additional `$match`) before expensive stages like `$lookup`, `$graphLookup`, or
complex `$addFields`.

```javascript
// CORRECT — limit before $lookup
db.orders.aggregate([
  { $match: { status: 'completed' } },
  { $sort: { orderDate: -1 } },
  { $limit: 100 }, // Process only 100 orders
  {
    $lookup: {
      from: 'customers',
      localField: 'customerId',
      foreignField: '_id',
      as: 'customer',
    },
  },
]);
```

```javascript
// WRONG — $lookup on entire result set, then limit
db.orders.aggregate([
  { $match: { status: 'completed' } },
  {
    $lookup: {
      // Looks up ALL completed orders
      from: 'customers',
      localField: 'customerId',
      foreignField: '_id',
      as: 'customer',
    },
  },
  { $sort: { orderDate: -1 } },
  { $limit: 100 }, // Wasted lookup on 99,900+ docs
]);
```

---

## $lookup vs App-Side Joins

### Rule LK-1: Use $lookup for Same-Database, Small-to-Medium Joins

`$lookup` is efficient when:

- Both collections are in the same database
- The foreign field is indexed
- The result set is manageable (not millions of joined documents)

```javascript
// CORRECT — $lookup for order + customer join (same DB, indexed)
db.orders.aggregate([
  {
    $match: { status: 'completed', orderDate: { $gte: ISODate('2024-01-01') } },
  },
  { $limit: 100 },
  {
    $lookup: {
      from: 'customers',
      localField: 'customerId',
      foreignField: '_id',
      as: 'customer',
    },
  },
  { $unwind: '$customer' },
  {
    $project: {
      orderDate: 1,
      total: 1,
      'customer.name': 1,
      'customer.email': 1,
    },
  },
]);
```

### Rule LK-2: Use App-Side Joins for Cross-Database or Large Datasets

When joining across databases, services, or when the joined collection is very large, perform the
join in application code.

```javascript
// CORRECT — app-side join for large datasets
const orders = await db
  .collection('orders')
  .find({ customerId: customerId })
  .sort({ orderDate: -1 })
  .limit(10)
  .toArray();

const productIds = [...new Set(orders.flatMap((o) => o.items.map((i) => i.productId)))];

const products = await db
  .collection('products')
  .find({ _id: { $in: productIds } })
  .project({ name: 1, price: 1, image: 1 })
  .toArray();

const productMap = new Map(products.map((p) => [p._id.toString(), p]));

const enrichedOrders = orders.map((order) => ({
  ...order,
  items: order.items.map((item) => ({
    ...item,
    product: productMap.get(item.productId.toString()),
  })),
}));
```

### Rule LK-3: Always Index the Foreign Field

The `foreignField` in `$lookup` must be indexed. Without an index, MongoDB performs a collection
scan for every input document.

```javascript
// CORRECT — ensure index exists before using $lookup
db.products.createIndex({ sku: 1 });

db.orders.aggregate([
  {
    $lookup: {
      from: 'products',
      localField: 'items.sku',
      foreignField: 'sku', // Indexed field
      as: 'productDetails',
    },
  },
]);
```

```javascript
// WRONG — $lookup on unindexed foreign field
// products.sku has no index
db.orders.aggregate([
  {
    $lookup: {
      from: 'products',
      localField: 'items.sku',
      foreignField: 'sku', // No index = collection scan per document
      as: 'productDetails',
    },
  },
]);
// With 10,000 orders and 50,000 products: 10,000 * 50,000 comparisons
```

### Rule LK-4: Use Pipeline $lookup for Complex Conditions

When join conditions are more complex than equality, use the pipeline form.

```javascript
// CORRECT — pipeline $lookup with conditions and projection
db.orders.aggregate([
  { $match: { status: 'completed' } },
  {
    $lookup: {
      from: 'reviews',
      let: { orderId: '$_id', custId: '$customerId' },
      pipeline: [
        {
          $match: {
            $expr: {
              $and: [{ $eq: ['$orderId', '$$orderId'] }, { $eq: ['$customerId', '$$custId'] }],
            },
          },
        },
        { $match: { rating: { $gte: 4 } } },
        { $project: { rating: 1, comment: 1 } },
        { $limit: 3 },
      ],
      as: 'topReviews',
    },
  },
]);
```

### Rule LK-5: $lookup + $unwind Coalescing

When `$lookup` is immediately followed by `$unwind` on the same field, MongoDB optimizes this into a
single stage internally. Leverage this pattern.

```javascript
// CORRECT — coalesced $lookup + $unwind
db.orders.aggregate([
  { $match: { status: 'completed' } },
  {
    $lookup: {
      from: 'customers',
      localField: 'customerId',
      foreignField: '_id',
      as: 'customer',
    },
  },
  { $unwind: '$customer' }, // Coalesced with $lookup by optimizer
]);
```

---

## $facet Patterns

### Rule FC-1: Use $facet for Multiple Analyses on the Same Data

`$facet` runs multiple sub-pipelines on the same input documents, avoiding multiple passes over the
data.

```javascript
// CORRECT — multiple analyses in one query
db.products.aggregate([
  { $match: { status: 'active' } },
  {
    $facet: {
      priceDistribution: [
        {
          $bucket: {
            groupBy: '$price',
            boundaries: [0, 25, 50, 100, 250, Infinity],
            output: { count: { $sum: 1 } },
          },
        },
      ],
      topCategories: [
        { $group: { _id: '$category', count: { $sum: 1 } } },
        { $sort: { count: -1 } },
        { $limit: 5 },
      ],
      overallStats: [
        {
          $group: {
            _id: null,
            totalProducts: { $sum: 1 },
            avgPrice: { $avg: '$price' },
            medianPrice: {
              $median: { input: '$price', method: 'approximate' },
            },
          },
        },
        { $project: { _id: 0 } },
      ],
    },
  },
]);
```

```javascript
// WRONG — three separate queries for the same data
const priceDistribution = await db.products.aggregate([...]).toArray();
const topCategories = await db.products.aggregate([...]).toArray();
const overallStats = await db.products.aggregate([...]).toArray();
// Three passes over the collection vs one with $facet
```

### Rule FC-2: Use $facet for Paginated Results with Count

Get paginated data and total count in a single query.

```javascript
// CORRECT — pagination with $facet
db.products.aggregate([
  { $match: { category: 'electronics', status: 'active' } },
  {
    $facet: {
      metadata: [{ $count: 'total' }],
      data: [
        { $sort: { createdAt: -1 } },
        { $skip: 20 }, // Page 3, 10 per page
        { $limit: 10 },
        { $project: { name: 1, price: 1, rating: 1 } },
      ],
    },
  },
  { $unwind: '$metadata' },
  {
    $addFields: {
      total: '$metadata.total',
      page: 3,
      pageSize: 10,
      totalPages: { $ceil: { $divide: ['$metadata.total', 10] } },
    },
  },
  { $project: { metadata: 0 } },
]);
```

### Rule FC-3: $facet Limitations

- Sub-pipeline output capped at 16 MB per facet (BSON document limit)
- Cannot nest `$facet` inside `$facet`
- Cannot use `$out` or `$merge` inside `$facet`
- All sub-pipelines share the same input documents
- 100 MB memory limit applies to the entire stage

```javascript
// WRONG — $out inside $facet
db.orders.aggregate([
  {
    $facet: {
      summary: [
        { $group: { _id: '$status', count: { $sum: 1 } } },
        { $out: 'orderSummary' }, // ERROR: cannot use $out in $facet
      ],
    },
  },
]);
```

---

## $merge for Materialized Views

### Rule MV-1: Use $merge for Incremental Materialized Views

`$merge` enables incremental updates to materialized views by upserting results into a target
collection.

```javascript
// CORRECT — incremental daily stats materialized view
db.orders.aggregate([
  {
    $match: {
      orderDate: {
        $gte: ISODate('2024-03-15T00:00:00Z'),
        $lt: ISODate('2024-03-16T00:00:00Z'),
      },
      status: 'completed',
    },
  },
  {
    $group: {
      _id: {
        date: { $dateToString: { format: '%Y-%m-%d', date: '$orderDate' } },
        category: '$category',
      },
      revenue: { $sum: '$total' },
      orderCount: { $sum: 1 },
      avgOrderValue: { $avg: '$total' },
    },
  },
  {
    $merge: {
      into: 'dailyCategoryStats',
      on: '_id',
      whenMatched: 'replace',
      whenNotMatched: 'insert',
    },
  },
]);
```

### Rule MV-2: Use $merge with Custom Pipeline for Complex Updates

When a simple merge/replace is not sufficient, use a pipeline in `whenMatched`.

```javascript
// CORRECT — accumulate totals across runs
db.orders.aggregate([
  { $match: { processedAt: { $exists: false } } },
  {
    $group: {
      _id: '$customerId',
      newOrders: { $sum: 1 },
      newRevenue: { $sum: '$total' },
    },
  },
  {
    $merge: {
      into: 'customerLifetimeStats',
      on: '_id',
      whenMatched: [
        {
          $set: {
            totalOrders: { $add: ['$$ROOT.totalOrders', '$$new.newOrders'] },
            totalRevenue: { $add: ['$$ROOT.totalRevenue', '$$new.newRevenue'] },
            lastUpdated: new Date(),
          },
        },
      ],
      whenNotMatched: 'insert',
    },
  },
]);
```

### Rule MV-3: Create Indexes on Materialized View Collections

Materialized view collections are query targets. Always create indexes suited to the expected read
patterns.

```javascript
// CORRECT — indexes on the materialized view
db.dailyCategoryStats.createIndex({ '_id.date': -1 });
db.dailyCategoryStats.createIndex({ '_id.category': 1, revenue: -1 });
```

### Rule MV-4: Schedule Materialized View Updates

Use Atlas Triggers, cron jobs, or application schedulers to refresh materialized views regularly.

```javascript
// CORRECT — scheduled refresh with timestamp tracking
const lastRun = await db.collection('jobState').findOne({ jobId: 'dailyStatsRefresh' });

const startFrom = lastRun?.lastProcessedDate || new Date('2024-01-01');
const now = new Date();

db.orders.aggregate([
  { $match: { orderDate: { $gte: startFrom, $lt: now } } },
  // ... pipeline ...
  { $merge: { into: 'dailyCategoryStats', on: '_id', whenMatched: 'replace' } },
]);

await db
  .collection('jobState')
  .updateOne(
    { jobId: 'dailyStatsRefresh' },
    { $set: { lastProcessedDate: now } },
    { upsert: true }
  );
```

---

## $out vs $merge

### Rule OM-1: Prefer $merge Over $out

`$merge` is the modern, flexible replacement for `$out`. Use `$out` only when you need atomic full
collection replacement.

| Feature                  | $out              | $merge                   |
| ------------------------ | ----------------- | ------------------------ |
| Replaces target entirely | Yes (atomic)      | No (per-document upsert) |
| Same database required   | Yes (before 4.4)  | No                       |
| Sharded target support   | No                | Yes                      |
| Incremental updates      | No                | Yes                      |
| Custom merge behavior    | N/A               | merge/replace/keep/fail  |
| Pipeline on match        | N/A               | Yes                      |
| Use case                 | Full refresh only | Most materialized views  |

```javascript
// CORRECT — $merge for daily updates (incremental)
db.events.aggregate([
  { $match: { date: { $gte: yesterday, $lt: today } } },
  { $group: { _id: '$eventType', count: { $sum: 1 } } },
  {
    $merge: {
      into: 'dailyEventStats',
      on: '_id',
      whenMatched: 'merge',
      whenNotMatched: 'insert',
    },
  },
]);
```

```javascript
// WRONG — $out for incremental updates (destroys all existing data)
db.events.aggregate([
  { $match: { date: { $gte: yesterday, $lt: today } } },
  { $group: { _id: '$eventType', count: { $sum: 1 } } },
  { $out: 'dailyEventStats' }, // REPLACES entire collection with 1 day's data!
]);
```

### Rule OM-2: Use $out for Full Snapshot Reports

`$out` is appropriate when you need a complete, consistent snapshot that atomically replaces the
previous version.

```javascript
// CORRECT — $out for weekly full report
db.orders.aggregate([
  { $match: { orderDate: { $gte: weekStart, $lt: weekEnd } } },
  {
    $group: {
      _id: { category: '$category', status: '$status' },
      count: { $sum: 1 },
      revenue: { $sum: '$total' },
    },
  },
  { $sort: { revenue: -1 } },
  { $out: 'weeklyReport' },
  // Atomically replaces the entire weeklyReport collection
]);
```

### Rule OM-3: Warn Before Using $out

Always warn the user before executing a pipeline with `$out`, because it replaces the entire target
collection. Lost data cannot be recovered without a backup.

```text
WARNING: This pipeline uses $out which will REPLACE the entire
"weeklyReport" collection.
  Current document count: 1,247
  After $out: Only new pipeline results will exist
  Previous data will be permanently deleted.

  To proceed, confirm "yes". To use incremental updates instead,
  switch to $merge.
```

---

## Pipeline Optimization Rules

### Rule OPT-1: Use explain() to Verify Index Usage

```javascript
// CORRECT — always check execution plan
db.orders.explain('executionStats').aggregate([
  {
    $match: {
      status: 'completed',
      orderDate: { $gte: ISODate('2024-01-01') },
    },
  },
  { $group: { _id: '$customerId', total: { $sum: '$amount' } } },
]);

// Key metrics to check:
// - winningPlan.stage: "IXSCAN" (good) vs "COLLSCAN" (bad)
// - totalKeysExamined should be close to nReturned
// - executionTimeMillis should be acceptable for your SLA
```

### Rule OPT-2: Use allowDiskUse Sparingly

`allowDiskUse: true` enables spilling to disk when a stage exceeds the 100 MB memory limit. Use it
only when necessary, as it significantly slows execution.

```javascript
// CORRECT — allowDiskUse with awareness
db.largeCollection.aggregate(
  [
    { $match: { status: 'active' } },
    { $group: { _id: '$region', total: { $sum: '$amount' } } },
    { $sort: { total: -1 } },
  ],
  { allowDiskUse: true }
  // NOTE: This pipeline may use disk for sort. Consider adding an index
  // on { status: 1, region: 1 } to avoid disk usage.
);
```

### Rule OPT-3: Avoid Unnecessary $unwind + $group Cycles

The pattern `$unwind` -> process -> `$group` (to reconstitute) is expensive. Use array operators
instead.

```javascript
// CORRECT — $reduce for array computation
db.orders.aggregate([
  {
    $addFields: {
      totalValue: {
        $reduce: {
          input: '$items',
          initialValue: NumberDecimal('0'),
          in: {
            $add: ['$$value', { $multiply: ['$$this.price', '$$this.qty'] }],
          },
        },
      },
    },
  },
]);

// WRONG — $unwind + $group for the same computation
db.orders.aggregate([
  { $unwind: '$items' },
  {
    $group: {
      _id: '$_id',
      totalValue: { $sum: { $multiply: ['$items.price', '$items.qty'] } },
      // Must $first every other field to reconstitute the document
      customerId: { $first: '$customerId' },
      orderDate: { $first: '$orderDate' },
      status: { $first: '$status' },
    },
  },
]);
```

### Rule OPT-4: Use $sample for Testing on Large Collections

When developing pipelines against large collections, use `$sample` to test with a subset.

```javascript
// CORRECT — test pipeline with sample
db.largeCollection.aggregate([
  { $sample: { size: 1000 } }, // Random 1000 documents
  // ... rest of pipeline for testing ...
]);
```

### Rule OPT-5: Avoid Repeated Pipeline Execution

If the same aggregation is needed multiple times, consider:

1. Materialized views with `$merge` for periodic refresh
2. Caching the results in application code
3. Creating a dedicated summary collection

```javascript
// CORRECT — materialized view refreshed on schedule
// Run nightly:
db.orders.aggregate([
  { $match: { orderDate: { $gte: lastRefresh } } },
  { $group: { _id: '$category', revenue: { $sum: '$total' } } },
  { $merge: { into: 'categoryRevenue', on: '_id', whenMatched: 'replace' } },
]);

// Application reads from materialized view (fast):
const revenue = await db.collection('categoryRevenue').find().toArray();
```

---

## Common Aggregation Patterns

### Top N Per Group

```javascript
// CORRECT — top 3 products per category
db.sales.aggregate([
  {
    $group: {
      _id: { category: '$category', product: '$productName' },
      revenue: { $sum: '$amount' },
    },
  },
  { $sort: { '_id.category': 1, revenue: -1 } },
  {
    $group: {
      _id: '$_id.category',
      topProducts: {
        $topN: {
          n: 3,
          sortBy: { revenue: -1 },
          output: { product: '$_id.product', revenue: '$revenue' },
        },
      },
    },
  },
]);
```

### Running Totals with Window Functions

```javascript
// CORRECT — running total and 7-day moving average (MongoDB 5.0+)
db.dailySales.aggregate([
  { $match: { storeId: 'store-001' } },
  { $sort: { date: 1 } },
  {
    $setWindowFields: {
      partitionBy: '$storeId',
      sortBy: { date: 1 },
      output: {
        runningTotal: {
          $sum: '$revenue',
          window: { documents: ['unbounded', 'current'] },
        },
        movingAvg7Day: {
          $avg: '$revenue',
          window: { range: [-6, 'current'], unit: 'day' },
        },
      },
    },
  },
]);
```

### Pivot / Crosstab

```javascript
// CORRECT — monthly sales pivoted by region
db.sales.aggregate([
  { $match: { year: 2024 } },
  {
    $group: {
      _id: { region: '$region', month: '$month' },
      total: { $sum: '$amount' },
    },
  },
  {
    $group: {
      _id: '$_id.region',
      monthlySales: { $push: { month: '$_id.month', total: '$total' } },
    },
  },
  {
    $project: {
      region: '$_id',
      sales: {
        $arrayToObject: {
          $map: {
            input: '$monthlySales',
            as: 'm',
            in: { k: { $toString: '$$m.month' }, v: '$$m.total' },
          },
        },
      },
    },
  },
]);
```

### Time-Based Gap Filling (MongoDB 5.1+)

```javascript
// CORRECT — hourly event counts with gap filling
db.events.aggregate([
  {
    $match: {
      timestamp: {
        $gte: ISODate('2024-03-15T00:00:00Z'),
        $lt: ISODate('2024-03-16T00:00:00Z'),
      },
    },
  },
  {
    $group: {
      _id: { $dateTrunc: { date: '$timestamp', unit: 'hour' } },
      count: { $sum: 1 },
    },
  },
  {
    $densify: {
      field: '_id',
      range: {
        step: 1,
        unit: 'hour',
        bounds: [ISODate('2024-03-15T00:00:00Z'), ISODate('2024-03-16T00:00:00Z')],
      },
    },
  },
  {
    $fill: {
      output: { count: { value: 0 } },
    },
  },
  { $sort: { _id: 1 } },
]);
```

### Multi-Level Grouping with Subtotals

```javascript
// CORRECT — hierarchy: region > city with $facet
db.sales.aggregate([
  { $match: { year: 2024 } },
  {
    $facet: {
      byCity: [
        {
          $group: {
            _id: { region: '$region', city: '$city' },
            revenue: { $sum: '$amount' },
          },
        },
        { $sort: { '_id.region': 1, revenue: -1 } },
      ],
      byRegion: [
        {
          $group: {
            _id: '$region',
            revenue: { $sum: '$amount' },
            cityCount: { $addToSet: '$city' },
          },
        },
        { $addFields: { cityCount: { $size: '$cityCount' } } },
        { $sort: { revenue: -1 } },
      ],
      grandTotal: [
        {
          $group: {
            _id: null,
            totalRevenue: { $sum: '$amount' },
            orderCount: { $sum: 1 },
          },
        },
        { $project: { _id: 0 } },
      ],
    },
  },
]);
```

### Ranking with Window Functions

```javascript
// CORRECT — rank employees by salary within department
db.employees.aggregate([
  {
    $setWindowFields: {
      partitionBy: '$department',
      sortBy: { salary: -1 },
      output: {
        departmentRank: { $rank: {} },
        denseRank: { $denseRank: {} },
        percentileRank: {
          $documentNumber: {},
        },
      },
    },
  },
  { $match: { departmentRank: { $lte: 5 } } },
]);
```

### Union Multiple Collections

```javascript
// CORRECT — combine data from multiple collections
db.activeOrders.aggregate([
  {
    $project: {
      orderId: '$_id',
      source: { $literal: 'active' },
      total: 1,
      date: '$orderDate',
    },
  },
  {
    $unionWith: {
      coll: 'archivedOrders',
      pipeline: [
        {
          $project: {
            orderId: '$_id',
            source: { $literal: 'archived' },
            total: 1,
            date: '$orderDate',
          },
        },
      ],
    },
  },
  { $sort: { date: -1 } },
  { $limit: 100 },
]);
```

### Conditional Aggregation

```javascript
// CORRECT — conditional grouping with $switch
db.orders.aggregate([
  {
    $addFields: {
      sizeBucket: {
        $switch: {
          branches: [
            { case: { $lt: ['$total', 50] }, then: 'small' },
            { case: { $lt: ['$total', 200] }, then: 'medium' },
            { case: { $lt: ['$total', 1000] }, then: 'large' },
          ],
          default: 'enterprise',
        },
      },
    },
  },
  {
    $group: {
      _id: '$sizeBucket',
      count: { $sum: 1 },
      revenue: { $sum: '$total' },
      avgValue: { $avg: '$total' },
    },
  },
  { $sort: { revenue: -1 } },
]);
```
