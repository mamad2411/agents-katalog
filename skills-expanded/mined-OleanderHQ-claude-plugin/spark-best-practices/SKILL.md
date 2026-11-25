---
name: spark-best-practices
description: >-
  General Apache Spark best practices for scalable, maintainable DataFrame
  jobs: avoid driver materialization, reduce shuffle, join efficiently, and
  cache carefully. Use when optimizing Spark performance, reviewing PySpark
  jobs, or writing new DataFrame pipelines.
---

# Spark Best Practices

Use this skill for general Apache Spark guidance when optimizing performance, reliability, and maintainability.

## 1) Keep execution distributed

- Avoid `collect()`, `toPandas()`, and large `take()` in core data paths.
- Materialize to driver memory only for very small control outputs (metrics, IDs, summaries).
- Keep heavy transformation and write paths in Spark DataFrame execution.

## 2) Prefer DataFrame APIs to Python loops

- Use Spark SQL/DataFrame functions so Catalyst can optimize execution plans.
- Avoid row-by-row Python logic when equivalent DataFrame expressions exist.
- Keep transformations declarative and composable.

## 3) Reduce shuffle cost

- Project and filter early to reduce data volume before joins/aggregations.
- Repartition intentionally before heavy joins/writes.
- Use `coalesce` when reducing output partitions.
- Watch for skewed keys and apply skew mitigation.

## 4) Use efficient joins

- Broadcast small dimension tables when appropriate.
- Align join key types and null handling before joins.
- Validate expected join cardinality to avoid explosive outputs.

## 5) Cache only reused intermediates

- Cache/persist DataFrames only when reused across multiple downstream actions.
- Unpersist promptly when no longer needed.
- Consider checkpointing for very long lineage plans.

## 6) Write in table-friendly layouts

- Prefer columnar formats (Parquet/Delta/Iceberg) when possible.
- Partition by bounded-cardinality business keys.
- Avoid small file explosion; compact files when needed.

## 7) Be explicit with schema and quality

- Define schemas explicitly where practical.
- Normalize data types across sources before joins/unions.
- Handle null semantics intentionally in filters, joins, and aggregations.

## 8) Observe and verify

- Use `explain()` and execution metrics/logs to inspect physical plans and shuffle boundaries.
- Track row counts and key metrics at major steps.
- Compare runtime and output quality after each optimization pass.

## 9) Set Structured Streaming checkpoints

Every Structured Streaming query needs a stable checkpoint location. The
checkpoint stores progress metadata and, for stateful queries such as windows,
state-store data that Spark needs to recover correctly.

Use shared storage for cluster runs, not local `/tmp`, because executors must be
able to see the same checkpoint path.

oleander provides `spark.oleander.app.state.dir` as a shared application state
directory that users can use for streaming checkpoints.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, window

spark = SparkSession.builder.appName("message-counts").getOrCreate()

state_dir = spark.conf.get("spark.oleander.app.state.dir", "").strip()
checkpoint = f"{state_dir.rstrip('/')}/public-stream/checkpoints/message-counts"

events = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "messages")
    .load()
)

counts = (
    events.selectExpr("CAST(value AS STRING) AS body", "timestamp AS event_time")
    .withWatermark("event_time", "1 minute")
    .groupBy(window(col("event_time"), "1 minute"))
    .agg(count("*").alias("message_count"))
)

query = (
    counts.writeStream
    .format("console")
    .outputMode("append")
    .option("checkpointLocation", checkpoint)
    .start()
)

query.awaitTermination()
```
