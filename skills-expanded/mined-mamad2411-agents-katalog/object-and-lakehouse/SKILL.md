---
name: object-and-lakehouse
description: >
  Object storage and analytical table formats — S3/GCS/Azure Blob, MinIO, Parquet, and
  Iceberg/Delta. Carries: why Parquet beats CSV for anything you'll read twice (columnar, predicate
  pushdown, compression, typed schema), partitioning and the small-files problem that eventually
  bites every lake, table formats for ACID + schema evolution + time travel over object storage,
  compaction, lifecycle rules and storage classes, and **presigned URLs scoped and short-lived,
  buckets never public**. Load when choosing a storage layout, writing or reading Parquet, setting
  up a lake or lakehouse, tuning slow analytical reads, or handing someone a file. Triggers: S3,
  GCS, Azure Blob, MinIO, object storage, bucket, parquet, arrow, iceberg, delta lake, hudi,
  lakehouse, partitioning, small files, compaction, columnar, predicate pushdown, presigned URL,
  storage class, lifecycle policy, data lake, time travel, schema evolution. Dataset provenance and
  versioning are `datasets` + `data-dvc`; bucket IAM is the cloud skills; warehouse SQL is `sql`.
---

# object-and-lakehouse — cheap storage that stays queryable

**Pinned:** pyarrow, duckdb, polars, minio — unpinned · authored 2026-07 · run `/skill-update
object-and-lakehouse` once the stack is chosen.

> On-demand: load this when data lands in object storage or needs to be read back efficiently.
> *Which* dataset version a run used is `datasets` + `data-dvc`; bucket policies and IAM are the
> cloud skills; querying a warehouse is `sql`. Canon: `security.md` `S7` (egress — a bucket is an
> external destination), `platform-security.md` `P5`/`P11`, `data-governance.md` `D9`/`D10`.

## When this applies

Choosing a storage layout. Reading or writing Parquet. Setting up a lake. Diagnosing slow analytical
reads. Handing someone a file.

## Object storage is not a filesystem

The mental model that prevents most mistakes:

- **Flat key space.** "Directories" are a prefix convention. Listing a prefix is an API call whose
  cost scales with the number of objects — this is why small files hurt.
- **Objects are immutable.** There is no append and no partial write; you replace the whole object.
- **Eventually consistent listings**, even where reads are strongly consistent. A just-written object
  may not appear in a listing immediately.
- **You pay per request as well as per byte.** A million small reads costs real money on top of the
  storage.
- **Versioning is your undo.** Turn it on for anything that matters (`S8` — an agent mistake should
  be reversible, not archaeological), and pair it with a lifecycle rule so old versions expire.

## Parquet, not CSV

For anything read more than once:

| | CSV | Parquet |
|---|---|---|
| Layout | Row-oriented text | **Columnar binary** |
| Schema | None — types re-inferred every read, inconsistently | Embedded and typed |
| Size | Baseline | Typically 5–10× smaller |
| Reading one column | Reads everything | Reads that column only |
| Filtering | Scan everything | **Predicate pushdown** via row-group statistics |

```python
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# Write partitioned, with a row group size that suits your read pattern
pq.write_to_dataset(table, root_path="s3://bucket/events/",
                    partition_cols=["dt"], compression="zstd")

# Read only the columns and partitions you need — the rest is never fetched
dataset = ds.dataset("s3://bucket/events/", format="parquet", partitioning="hive")
df = dataset.to_table(filter=(ds.field("dt") == "2026-07-25"),
                      columns=["user_id", "latency_ms"]).to_pandas()
```

**Compression:** `zstd` is the sensible default (better ratio than snappy, still fast). `snappy` when
decompression speed dominates. **Row group size** matters: too small and you lose columnar benefit
and statistics get noisy; ~128MB is a reasonable starting point.

For local analytics over Parquet, **DuckDB reads it directly from object storage** and will handle
more than people expect — often the right answer before reaching for a cluster.

## Partitioning, and the small-files problem

Partition on the column you **filter by most**, usually date. Hive-style (`dt=2026-07-25/`) is widely
understood by readers.

**The failure every lake eventually hits:** partitioning too finely — by hour, then by tenant, then
by type — produces millions of tiny files. Listing dominates, per-request costs dominate, query
planning dominates, and the "fast" columnar format is slower than the CSV it replaced.

- Aim for files in the **100MB–1GB** range.
- If a streaming writer produces small files, **compaction is a scheduled job**
  (`workflow-orchestration`), not an aspiration.
- Don't partition on high-cardinality columns. Use them for sorting within a file instead — row-group
  statistics then give you pushdown without the file explosion.

## Table formats — when a directory of Parquet isn't enough

Parquet is a *file* format. **Iceberg** and **Delta Lake** are *table* formats layered over it,
adding a metadata layer that buys:

- **ACID transactions** — concurrent writers without corrupting readers.
- **Schema evolution** — add, drop, and rename columns safely, including rename, which a bare
  directory cannot do.
- **Time travel** — query the table as of a timestamp or snapshot. Genuinely useful for reproducing
  a training run's exact input (`model-governance.md` `M2`) and for recovering from a bad write.
- **Partition evolution** (Iceberg) — change the partitioning without rewriting history.
- **Efficient upserts and deletes** — including the deletes canon `D10` requires, which a plain
  Parquet directory makes painful.

Take a table format when you have concurrent writers, evolving schemas, or a deletion obligation.
Skip it for write-once immutable exports, where a partitioned Parquet directory is simpler and
sufficient.

**Time travel is not a backup and not deletion.** Snapshots expire on a retention policy, and a
deleted row remains readable in older snapshots until they do — so a deletion request means
`DELETE` *plus* snapshot expiry (`D10`).

## Lifecycle and cost

Storage tiers trade retrieval latency and cost for storage cost. Set lifecycle rules **when the
bucket is created**, not after the bill:

- Hot → infrequent-access after ~30 days · archive after ~90 · delete at the retention limit (`D6`).
- **Expire old object versions and incomplete multipart uploads.** Abandoned multipart uploads are
  invisible in listings and billed indefinitely — a genuinely common surprise line item.
- Archive tiers have retrieval *latency* (minutes to hours) and retrieval *cost*. Don't archive
  something a pipeline reads.

## Security

- **Buckets are never public** (`S7`, `S8`). Block public access at the account level so a single
  misconfigured bucket policy can't override it. `guard-iac.py` blocks the shapes it can see.
- **Presigned URLs are scoped and short-lived** — the narrowest operation, one object, minutes not
  days. A presigned URL is a bearer credential in a link, and links get forwarded and logged.
- **Encryption at rest and in transit** (`D9`), including for the archive tiers.
- **Access logging on** for buckets holding project data (`P9`) — you cannot investigate an access
  you didn't record.
- Sending data to a bucket is **egress** (`S7`): it is publishing, governed by the data policy,
  whoever owns the account.

## Gotchas

- **CSV for anything reread.** Types drift between reads and nobody notices until a model does.
- **`SELECT *` over a lake.** Columnar storage's whole benefit is not reading columns you don't need.
- **Partitioning by a high-cardinality column.** The small-files problem, arriving fast.
- **No compaction job.** Streaming ingest without one degrades continuously until someone
  investigates a "slow query" that is actually a listing problem.
- **Trusting listing consistency** immediately after a write.
- **A lifecycle rule that archives data a pipeline reads**, discovered as a mysterious timeout.
- **Deleting the source row and considering it deleted** — canon `D10`: the Parquet file, the
  snapshot, and any derived index still hold it.
