---
tags: [backend, mongodb, compound, index, esr, rule]
name: mongodb-compound-index-esr-rule
description: Order MongoDB compound-index fields as Equality → Sort → Range so the query planner keeps a tight IXSCAN and avoids in-memory sorts.
trigger: Designing or reviewing MongoDB compound indexes; slow queries with COLLSCAN or in-memory sort; index field ordering disputes.
source_project: lucida-domain-apm
version: 1.0.0
category: backend
---

# MongoDB Compound Index — ESR Rule

Order fields as **E**quality → **S**ort → **R**ange.

- **Equality** — fields filtered with `=`
- **Sort** — fields used in `sort()`
- **Range** — fields with `<`, `>`, `between`, or `$in` over a large set

## Why

MongoDB consumes the index left-to-right. Equality fields narrow the scan to a contiguous key range; sort fields let the engine return results without an in-memory sort; range fields expand the scan and must come last — placing them earlier forces a wider scan and may break sort usage.

## Steps

1. List the query's predicates; classify each field as equality, sort, or range.
2. Build the index in ESR order. Drop fields that don't participate.
3. Remove dead indexes whose key prefix is covered by the new one (left-prefix rule).
4. Verify with `db.<coll>.find(...).explain("executionStats")`: want `IXSCAN` and `nReturned ≈ totalDocsExamined`, with no `SORT` stage.

## Example

```java
@CompoundIndexes({
    @CompoundIndex(name = "tenant_service_time",
                   def = "{tenantId:1, serviceId:1, startTime:-1, duration:1}")
    // E: tenantId, serviceId     S: startTime (desc)     R: duration
})
```

## Counter / Caveats

- Sort direction: MongoDB can scan an index backwards, so an ASC query on a DESC index still works — *position* matters more than direction.
- `$in` with a small list behaves like equality; large `$in` lists are range-like.
- Partial indexes and `hint()` can invalidate this reasoning — always re-check with `explain()`.
- A compound index satisfying ESR for one query may be wrong for a sibling query — index per workload, not per table.
