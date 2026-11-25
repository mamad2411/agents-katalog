---
name: designing-data-storage
description: "File formats and lakehouse table formats for data lakes: Parquet, Arrow, Lance, Zarr, Avro, ORC, Delta Lake, Apache Iceberg, and Apache Hudi. Covers compression, partitioning, ACID transactions, schema evolution, and format selection."
dependsOn:
  - "@building-data-pipelines"
---

# Designing Data Storage

Comprehensive guide to selecting and using modern data storage formats for analytics and machine learning. Covers six file formats (Parquet, Arrow, Lance, Zarr, Avro, ORC) and three lakehouse table formats (Delta Lake, Apache Iceberg, Apache Hudi).

## Table of Contents

- [Quick Format Comparison](#quick-format-comparison)
  - [File Formats](#file-formats)
  - [Lakehouse Table Formats](#lakehouse-table-formats)
- [When to Use Which?](#when-to-use-which)
  - [File Formats](#file-formats-1)
  - [Lakehouse Table Formats](#lakehouse-table-formats-1)
- [Format Selection Matrix](#format-selection-matrix)
- [Detailed Reference Guides](#detailed-reference-guides)
- [Code Examples](#code-examples)
  - [Parquet (Columnar Analytics)](#parquet-columnar-analytics)
  - [Delta Lake (ACID Table Format)](#delta-lake-acid-table-format)
  - [Apache Iceberg (Engine-Agnostic)](#apache-iceberg-engine-agnostic)
  - [Lance (ML-Native)](#lance-ml-native)
  - [Zarr (N-Dimensional Arrays)](#zarr-n-dimensional-arrays)
- [Best Practices](#best-practices)
  - [File Formats](#file-formats-2)
  - [Lakehouse Formats](#lakehouse-formats)
- [Compression Codec Comparison](#compression-codec-comparison)
- [Related Skills](#related-skills)
- [References](#references)

## Quick Format Comparison

### File Formats

| Format | Type | Best For | Compression | Schema Evolution | Random Access |
|--------|------|----------|-------------|------------------|---------------|
| **Parquet** | Columnar | Analytics, data lakes | ✅ (Snappy, Zstd, LZ4) | ✅ (add/drop) | ✅ (row groups) |
| **Arrow/Feather** | Columnar | In-memory, IPC, ML | ✅ (LZ4, Zstd) | Limited | ✅ (record batches) |
| **Lance** | Columnar | ML pipelines, vectors | ✅ (Zstd, LZ4) | ✅ | ✅ (multi-modal) |
| **Zarr** | Chunked arrays | ML, geospatial, N-dim | ✅ (Blosc, gzip) | ✅ (chunks) | ✅ (chunk-level) |
| **Avro** | Row-based | Streaming, Kafka | ✅ (deflate, snappy) | ✅ (full schema) | ❌ (sequential) |
| **ORC** | Columnar | Hive, Hadoop | ✅ (ZLIB, Snappy) | Limited | ✅ (stripe-level) |

### Lakehouse Table Formats

| Feature | Delta Lake | Apache Iceberg | Apache Hudi |
|---------|-----------|----------------|-------------|
| **ACID Transactions** | ✅ | ✅ | ✅ |
| **Time Travel** | ✅ | ✅ | ✅ |
| **Schema Evolution** | ✅ | Advanced (branching) | ✅ |
| **Primary Ecosystem** | Spark/Databricks | Engine-agnostic | Spark (CDC focus) |
| **Write Optimization** | Copy-on-write | CoW, Merge-on-Read | CoW, Merge-on-Read |
| **Python API** | `deltalake` (pure), PySpark | `pyiceberg` (pure) | PySpark only |
| **Best For** | Spark ecosystems | Multi-engine analytics | Change data capture |

## When to Use Which?

### File Formats

**Choose Parquet when:**
- You need broad compatibility (Spark, DuckDB, Polars, pandas)
- Analytics queries with filtering/aggregation
- Data lake storage with partitioning
- Mature ecosystem with best compression support

**Choose Arrow/Feather when:**
- Zero-copy sharing between processes (IPC)
- Fast serialization/deserialization for ML training
- In-memory format persistence
- Need Arrow ecosystem (Kernel, CUDA, etc.)

**Choose Lance when:**
- Machine learning pipelines with embeddings/vectors
- Need multi-modal data (text + images + audio + vectors)
- Versioned datasets with Git-like branching
- Cloud-native (S3/GCS) with no metadata catalog required

**Choose Zarr when:**
- N-dimensional arrays (tensors, satellite imagery, medical scans)
- Chunked, compressed storage for ML
- Parallel reads/writes across chunks
- Cloud-optimized (s3://, gs:// with fsspec)

**Choose Avro when:**
- Streaming to Kafka/Kinesis
- Schema evolution is critical (backward/forward)
- Row-based access pattern
- Need to serialize objects/records

**Choose ORC when:**
- Working primarily with Hive/Hadoop
- Hive ACID transactions
- Legacy big data pipelines

### Lakehouse Table Formats

**Choose Delta Lake when:**
- You're in the Spark/Databricks ecosystem
- Need mature tooling with pure-Python `deltalake` library
- Want simplest time travel and schema evolution

**Choose Apache Iceberg when:**
- You need engine-agnostic tables (Spark, Trino, Flink, DuckDB)
- Advanced schema branching and partition evolution
- Prefer explicit catalog abstraction

**Choose Apache Hudi when:**
- You're building CDC pipelines from Kafka/DB logs
- Need upsert/delete support with streaming
- Low-latency incremental processing

## Format Selection Matrix

| Use Case | Recommended Format | Reason |
|----------|-------------------|--------|
| Data lake analytics | **Parquet** or **Delta Lake** | Mature, partitioning, ecosystem |
| ML training data | **Arrow/Feather** or **Lance** | Zero-copy, vector support |
| Geospatial arrays | **Zarr** | Chunked, N-dimensional, cloud-optimized |
| Streaming/Kafka | **Avro** | Schema evolution, row-based |
| Legacy Hive | **ORC** | Compatibility |
| Feature stores | **Lance** or **Delta Lake** | Versioning, vectors |
| IPC between processes | **Arrow IPC** or **Feather** | Zero-copy, fast |
| Multi-engine analytics | **Apache Iceberg** | Engine-agnostic, catalog flexibility |
| CDC pipelines | **Apache Hudi** | Built for upserts/streaming |
| Quick exports | **Parquet** (Zstd) | Good compression/decompression speed |

## Detailed Reference Guides

### File Format References

- **`references/parquet.md`** - Deep dive on Parquet layout, writer settings, partitioning patterns
- **`references/format-selection-guide.md`** - Comprehensive decision matrix and selection criteria

### Lakehouse Table Format References

- **`references/delta-lake.md`** - Pure-Python API, PySpark integration, time travel, cloud storage
- **`references/iceberg.md`** - Catalog configuration, schema evolution, partition evolution
- **`references/hudi.md`** - CDC patterns, upserts, Copy-on-Write vs Merge-on-Read

## Code Examples

### Parquet (Columnar Analytics)

```python
import polars as pl
import pyarrow.parquet as pq
import pyarrow as pa

# Write with Polars
df = pl.DataFrame({"id": [1, 2, 3], "value": [100.0, 200.0, 150.0]})
df.write_parquet("data.parquet", compression="zstd")

# Write with PyArrow (more control)
table = pa.Table.from_pandas(df)
pq.write_table(
    table,
    "data.parquet",
    compression="ZSTD",
    compression_level=3,
    row_group_size=100000,
    use_dictionary=True
)

# Read with column pruning
df = pl.read_parquet("data.parquet", columns=["id", "value"])

# Dataset scanning with predicate pushdown
lazy_df = pl.scan_parquet("s3://bucket/dataset/**/*.parquet")
result = lazy_df.filter(pl.col("value") > 100).collect()
```

### Delta Lake (ACID Table Format)

```python
from deltalake import DeltaTable, write_deltalake
import pyarrow as pa

# Create Delta table
data = pa.table({
    "id": [1, 2, 3],
    "value": [100.0, 200.0, 150.0],
    "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03"]
})

write_deltalake("data/delta-table", data, mode="overwrite")

# Read with time travel
dt = DeltaTable("data/delta-table")
dt.load_version(1)  # Load specific version
df = dt.to_pandas()

# Upsert (merge)
new_data = pa.table({"id": [2, 4], "value": [250.0, 400.0]})
dt.merge(
    source=new_data,
    predicate="target.id = source.id"
).when_matched_update_all().when_not_matched_insert_all().execute()
```

### Apache Iceberg (Engine-Agnostic)

```python
from pyiceberg.catalog import load_catalog

# Load catalog
catalog = load_catalog("glue", **{
    "type": "glue",
    "s3.region": "us-east-1",
})

# Create and write table
table = catalog.create_table("default.events", schema=schema)
table.append(parquet_data)

# Read with time travel
df = table.scan(
    row_filter="population > 1000000",
    as_of_timestamp="2024-01-01T00:00:00Z"
).to_pandas()
```

### Lance (ML-Native)

```python
import lancedb
import polars as pl

# Create Lance dataset
db = lancedb.connect("./data.lance")
df = pl.DataFrame({
    "id": [1, 2, 3],
    "text": ["Hello", "World", "ML"],
    "vector": [[0.1] * 128, [0.2] * 128, [0.3] * 128]
})

table = db.create_table("my_table", df)

# Vector search
results = table.search([0.1] * 128).limit(5).to_pandas()
```

### Zarr (N-Dimensional Arrays)

```python
import zarr
import numpy as np

# Create chunked, compressed array
z = zarr.open(
    'data.zarr',
    mode='w',
    shape=(1000000, 1000),
    chunks=(10000, 1000),
    dtype='f4',
    compressor=zarr.Blosc(cname='zstd', clevel=3)
)

# Write and read partial (only loads needed chunks)
z[:10000, :] = np.random.rand(10000, 1000).astype('f4')
slice_data = z[5000:6000, :]
```

## Best Practices

### File Formats

1. ✅ **Default to Parquet** - Broadest compatibility, good compression
2. ✅ **Use Arrow/Feather for ML staging** - Zero-copy between frameworks
3. ✅ **Use Lance when vectors are first-class** - No separate vector DB needed
4. ✅ **Use Zarr for N-dim arrays** - Geospatial, video, 3D data
5. ✅ **Compress everything** - Snappy (fast) or Zstd (balanced)
6. ✅ **Partition wisely** - By date/region/tenant to enable pruning
7. ❌ **Don't use Avro for analytics** - No column pruning, row-based
8. ❌ **Don't use ORC unless in Hive/Hadoop world**

### Lakehouse Formats

1. ✅ **Use partitions** - Partition by date/region for predicate pushdown
2. ✅ **Vacuum regularly** - Clean up old files to avoid storage bloat
3. ✅ **Optimize layouts** - Compact small files for better performance
4. ✅ **Catalog choice** - AWS Glue for AWS, Hive for on-prem, REST for SaaS
5. ✅ **Monitor metadata** - Table metadata grows with operations
6. ❌ **Don't vacuum too aggressively** - Keep time travel window
7. ❌ **Don't skip OPTIMIZE** - Small files hurt performance

## Compression Codec Comparison

| Codec | Compression Ratio | Speed | Best For |
|-------|-------------------|-------|----------|
| **Snappy** | Low (~2:1) | ⚡⚡⚡ Fast | Fast analytics, default |
| **Zstd** | Medium-High (~4:1) | ⚡⚡ Fast | General purpose |
| **LZ4** | Low-Medium (~2.5:1) | ⚡⚡⚡ Very fast | Real-time streaming |
| **Gzip** | High (~5:1) | ⚡ Slow | Archival, cold storage |
| **Blosc (zstd)** | Medium | ⚡⚡ | Zarr arrays |

## Related Skills

- `@accessing-cloud-storage` - S3, GCS, Azure authentication and I/O patterns
- `@building-data-pipelines` - ETL patterns using these storage formats
- `@engineering-ai-pipelines` - Vector storage, Lance, embeddings workflows
- `@managing-data-catalogs` - Hive, Glue, REST catalogs for Iceberg

## References

- [Apache Parquet](https://parquet.apache.org/)
- [Apache Arrow](https://arrow.apache.org/docs/format/)
- [Lance Format](https://lancedb.github.io/lancedb/concepts/storage_format/)
- [Zarr Format](https://zarr.readthedocs.io/)
- [Apache Avro](https://avro.apache.org/)
- [Delta Lake](https://docs.delta.io/)
- [Apache Iceberg](https://iceberg.apache.org/)
- [Apache Hudi](https://hudi.apache.org/)
