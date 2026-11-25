---
name: couchbase-magma
description: "Understand and tune the Magma storage engine in Couchbase. Use whenever the user asks about Magma, Magma storage engine, Couchbase storage backend, couchstore vs Magma, 128 vBuckets vs 1024 vBuckets, Magma compaction, Magma memory requirements, Magma disk layout, storage engine selection, when to use Magma vs couchstore, storageBackend bucket setting, numVBuckets bucket setting, or 'which storage engine should I use.' Distinct from couchbase-sizing (which has a brief Magma section in disk.md) — this skill covers Magma behavior, tradeoffs, and tuning in depth. Use proactively when the user is creating new buckets on 8.0 or is investigating storage-related performance issues."
license: MIT
---

# Couchbase Magma Storage Engine

A skill for *understanding and tuning* the Magma storage engine — Couchbase's LSM-tree-based storage backend optimized for large datasets per node.

## When this skill applies

- "Should I use Magma or couchstore for my bucket?"
- "What changed with Magma being the default in 8.0?"
- "What does 128 vBuckets mean vs 1024?"
- "How does Magma handle compaction differently?"
- "How much memory does Magma need?"
- "My write performance is different after upgrading to 8.0"
- "How do I set the storage engine when creating a bucket?"

## Magma vs couchstore at a glance

| | Couchstore (classic) | Magma |
|---|---|---|
| **Architecture** | B-tree per vBucket | LSM-tree per vBucket |
| **Default vBuckets** | 1024 | 128 (8.0 default) |
| **RAM per node minimum** | 100 MB per bucket (min); memory-to-data ratio 10% | 100 MB (128 vBucket) / 1 GiB (1024 vBucket); memory-to-data ratio 1% |
| **Optimized for** | Smaller datasets, high read ratio | Large datasets (>100M docs/node), high write rate |
| **Write performance** | Good at low-moderate write rates | Better at sustained high write rates (LSM absorbs bursts) |
| **Read performance** | Excellent (direct B-tree lookup) | Good (may require multi-level lookup on cold data) |
| **Compaction** | Explicit compaction cycle | Continuous background compaction (no manual trigger needed) |
| **Disk space efficiency** | Good after compaction | Good continuously (LSM merges in background) |
| **Available** | CE and EE | EE only |

## When to use Magma

Use Magma when:
- Dataset exceeds ~100M documents per node
- Write rate is high and sustained (> 50K writes/sec per node)
- Memory is constrained (Magma's minimum per-bucket RAM is lower)
- You're using fullEviction (Magma pairs well with fullEviction's design)

Stick with couchstore when:
- Dataset is small-to-medium (< 50M documents per node)
- Read performance is critical and the working set fits in RAM
- You're on Community Edition
- You need to stay on 1024 vBuckets for an existing operational reason

## vBucket count: 128 vs 1024

**1024 vBuckets (couchstore default):**
- Original Couchbase vBucket count
- Higher parallelism for large clusters (more vBuckets = finer-grained distribution)
- Higher memory overhead per bucket (1024 vBucket metadata structures)
- Required for compatibility with older SDK versions

**128 vBuckets (Magma 8.0 default):**
- Lower memory footprint (128 vBucket structures vs 1024)
- Sufficient parallelism for most cluster sizes (128 is still well-distributed across 3-10 nodes)
- Not compatible with SDK versions that require 1024 vBuckets (check your SDK matrix)

**vBucket count is set at bucket creation and cannot be changed.** Plan before creating buckets in production.

## Setting storage engine and vBucket count

Via the Couchbase UI (Create Bucket → Advanced Settings) or via REST / MCP:

```python
admin_bucket_create(
    name="my-bucket",
    ram_quota_mb=4096,
    storage_backend="magma",    # "couchstore" or "magma"
    num_vbuckets=128,           # 128 or 1024
    cluster="prod"
)
```

On 8.0 EE, omitting these parameters creates a Magma 128-vBucket bucket (the new default). On 7.x or CE, the default is couchstore 1024 vBuckets.

## Magma compaction

Couchstore uses explicit compaction cycles — compaction runs periodically (configurable) and reclaims disk space from deleted/updated documents. Between compaction runs, disk usage grows.

Magma uses continuous background compaction (LSM tree merging). There's no "compaction running" spike — disk usage stays relatively stable. The tradeoff: Magma has slightly higher write amplification than couchstore (each write may trigger a background merge operation).

You can still trigger manual compaction on a Magma bucket, but it's usually not necessary. If you're monitoring disk usage, don't be surprised that Magma doesn't show the sawtooth pattern that couchstore compaction creates.

## Memory requirements

**Couchstore bucket minimum:** 100 MB per bucket per node. Couchstore has a minimum memory-to-data ratio of ~10% (working set expected to fit largely in RAM).

**Magma bucket minimum:**
- 128-vBucket Magma: 100 MB per bucket per node
- 1024-vBucket Magma: 1 GiB per bucket per node (higher due to vBucket metadata)

Magma has a minimum memory-to-data ratio of ~1% — e.g. a node holding 5 TiB in a Magma bucket must allocate at least ~51 GiB RAM for that bucket. This 10:1 difference in the required memory-to-data ratio is Magma's core advantage for large, memory-constrained datasets.

The 128-vBucket default in 8.0 is partly motivated by this: smaller memory footprint makes Magma practical for memory-constrained deployments.

## Migration between storage engines

You cannot change the storage engine of an existing bucket in place. Options:

1. **Create new bucket + migrate data:** create a Magma bucket alongside the existing couchstore bucket, use XDCR or cbimport/cbexport to copy data, then cut over. See `couchbase-migration-execution` for migration patterns.
2. **Backup + restore:** backup the couchstore bucket with cbbackupmgr, create a new Magma bucket, restore into it.

Plan migration during a maintenance window. For large datasets, the copy process can take hours.

## Related skills

- `couchbase-sizing` — Magma sizing formulas and disk planning
- `couchbase-upgrade` — 8.0 default change to Magma and its impact on bucket creation scripts
- `couchbase-migration-execution` — migrating data between storage engines
