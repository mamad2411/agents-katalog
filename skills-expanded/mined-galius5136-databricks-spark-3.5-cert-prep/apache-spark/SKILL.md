---
name: apache-spark
description: "Knowledge base from \"Learning Spark, 2nd Edition\" by Damji, Wenig, Das & Lee. Use when working with Apache Spark / PySpark, preparing for the Databricks Certified Associate Developer for Apache Spark exam, or applying the authors' frameworks for Spark architecture, DataFrame API, Spark SQL, Structured Streaming, tuning, and Datasets."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, framework name, or chapter number]
---

# Learning Spark, 2nd Edition — Knowledge Base
**Authors**: Jules S. Damji, Brooke Wenig, Tathagata Das, Denny Lee | **Chapters**: 12 | **Generated**: 2026-05-24

This skill is tuned for **Databricks Certified Associate Developer for Apache Spark** exam prep — PySpark first, with emphasis on architecture, DataFrame API, Spark SQL, tuning, and Structured Streaming.

## How to Use This Skill

- **Without arguments** — load the Core Frameworks below as a Spark mental model.
- **By topic** — ask about `shuffle partitions`, `broadcast join`, `watermark`, `output modes`, etc. → I find and read the relevant chapter.
- **By chapter number** — ask for `ch07` to load that specific chapter file.
- **Browse** — ask "what chapters do you have?" to see the full index.

When you ask about a topic that's only briefly mentioned in Core Frameworks, I'll read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### Spark in one paragraph
A **unified engine** for large-scale data processing. The **driver** orchestrates **executors** on a cluster; computation is expressed as a **DAG** of **transformations** (lazy) and **actions** (eager). Structured APIs (**DataFrame**, **Dataset**) are optimized by the **Catalyst** optimizer and compiled by **Tungsten** into compact JVM bytecode. The same engine powers batch (Spark SQL), streaming (Structured Streaming), ML (MLlib), and graph (GraphX) workloads.

### Execution hierarchy (memorize for the exam)
**Application** → **Job** (per action) → **Stage** (split at every shuffle/exchange) → **Task** (one per partition, runs on one executor core).

### Lazy evaluation + lineage
Transformations record a **lineage DAG**; actions trigger execution. Lineage = fault tolerance — Spark can rebuild lost partitions by replaying transformations on the source data.

### Narrow vs Wide transformations
**Narrow** (`filter`, `select`, `map`, `union`): 1 input partition → 1 output partition, no shuffle. **Wide** (`groupBy`, `orderBy`, `join`, `distinct`, `repartition`): cross-partition data exchange → stage boundary.

### Deployment modes (exam-critical)
| Mode | Driver | Executor | Cluster Manager |
|---|---|---|---|
| **Local** | single JVM | **same JVM as driver** | host |
| Standalone | any node | each node | any host |
| YARN client | outside cluster | NodeManager | YARN RM + AppMaster |
| YARN cluster | YARN AppMaster | NodeManager | same as YARN client |
| Kubernetes | K8s pod | K8s pod | K8s Master |

Local mode is the **only** mode with driver+executors in one JVM.

### Catalyst optimizer — 4 phases
1. **Analysis** — resolve names via Catalog → AST
2. **Logical optimization** — rule-based + cost-based (predicate pushdown, projection pruning, constant folding)
3. **Physical planning** — choose physical operators
4. **Code generation** — Tungsten whole-stage codegen → compact JVM bytecode

### DataFrame API patterns
```python
# Reader
df = (spark.read.format("csv").schema(schema)
      .option("header", "true").load(path))

# Writer (sample exam Q1)
df.write.mode("overwrite").partitionBy("country").parquet("/data/output")

# Common modifications (exam Sec 3 staple)
df2 = (df.withColumn("state", col("division"))
         .drop("division")
         .withColumnRenamed("mName", "managerName"))

# Drop rows with ANY null
df.na.drop()              # all columns must be non-null
df.na.drop(subset="sqft") # check only one column

# Aggregations
df.groupBy("color").agg(count("*"), approx_count_distinct("user_id"), mean("amount"))

# Joins (inner is default)
a.join(broadcast(b), "key")     # force BHJ
a.join(b, "key", "leftOuter")   # explicit type
```

### Save modes
`overwrite` · `append` · `ignore` · `error`/`errorifexists` (default)

### Spark SQL: temp views
- **Temp view**: `df.createOrReplaceTempView("v")` — session-scoped
- **Global temp view**: `df.createOrReplaceGlobalTempView("v")` — cross-session, query as `global_temp.v`

### Managed vs Unmanaged tables
- **Managed**: Spark owns data + metadata. `DROP TABLE` removes both.
- **Unmanaged**: Spark owns metadata only. `DROP TABLE` removes only metadata.

### Tuning essentials (exam Sec 4)
- **`spark.sql.shuffle.partitions = 200`** (default) — partition count after a wide transformation. **Sample exam Q5** tests this exact fact.
- **`spark.sql.autoBroadcastJoinThreshold = 10 MB`** (default) — BHJ cutoff. `-1` disables.
- **`spark.sql.files.maxPartitionBytes = 128 MB`** — file-read partition size.
- **Executor memory**: 300 MB reserved + 60% execution + 40% storage (defaults; can borrow between exec/storage).
- **Cache vs Persist**: `cache()` = `MEMORY_AND_DISK` (Python) / `MEMORY_ONLY` (Scala). `persist(StorageLevel.X)` for control. **Cache is lazy** — needs an action to materialize.
- **AQE** (`spark.sql.adaptive.enabled`): runtime replanning — coalesces partitions, swaps SMJ→BHJ, handles skew.
- **Repartition (wide)** to grow/balance; **Coalesce (narrow)** to shrink only.

### Join strategies (auto-picked)
| Strategy | Trigger | Cost |
|---|---|---|
| **BHJ** Broadcast Hash Join | one side ≤ 10 MB | no shuffle (fastest) |
| **SMJ** Shuffle Sort Merge Join | both large, equi-join on sortable key | shuffle + sort |
| **SHJ** Shuffle Hash Join | one side fits per partition | shuffle + hash table |
| **BNLJ** Broadcast Nested Loop | small + non-equi join | broadcast + nested loop |
| **Cartesian** | no join condition | quadratic |

### Spark UI
**Port 4040** (driver host). Tabs: Jobs · Stages · Storage · Environment · Executors · SQL · (Structured Streaming in 3.0+).
**Debug signals**: max task time ≫ median → **data skew**; high GC → memory starvation; high shuffle read blocked time → I/O bottleneck.

### Structured Streaming — 5 steps
1. `spark.readStream.format(...)` → source
2. DataFrame transforms (mostly identical to batch)
3. `.writeStream.format(...).outputMode(...)` → sink + mode
4. `.trigger(...).option("checkpointLocation", ...)` → checkpoint required for exactly-once
5. `.start()` → returns `StreamingQuery`

### Streaming output modes
- **append** (default) — only new rows; not allowed for aggregation without watermark
- **complete** — all rows of result table (small aggregates only)
- **update** — only changed rows since last trigger

### Streaming triggers
default (ASAP) · `processingTime="N seconds"` · `once` (one batch, stop) · `continuous` (experimental ms latency)

### Exactly-once requires all three
**Replayable source** + **deterministic compute** + **idempotent sink**

### Watermark pattern (bounds state)
```python
(df.withWatermark("eventTime", "10 minutes")
   .groupBy(window("eventTime", "5 minutes"), key)
   .agg(...))
```
`withWatermark` BEFORE `groupBy`, on the SAME time column. Limits state to `(maxEventTime − delay)`.

### Streaming dedup
```python
df.dropDuplicates("col1", "col2")                                # state unbounded
df.withWatermark("eventTime", "1h").dropDuplicates("id", "eventTime")  # bounded
```

### Stream–stream joins
- **Inner**: watermark + time range condition optional (state unbounded if omitted)
- **Outer**: watermark + time range **mandatory**

### UDFs
**Per-session**, opaque to Catalyst. Prefer built-ins. For Python, use **Pandas UDFs** (`@pandas_udf` decorator, Arrow-backed, vectorized) — much faster than row-by-row.

### Datasets vs DataFrames
**Dataset[T]** = typed; **Scala/Java only**. **DataFrame** = untyped (`Dataset[Row]` in Scala). Python and R get only DataFrame.

---

## ⚠ Gaps vs the 2026 exam

This book was published in 2020. The exam guide (Oct 2025) includes topics added to Spark **after** this book:
- **Spark Connect** (Spark 3.4+, 2023) — client/cluster decoupling. Exam Sec 6.
- **Pandas API on Spark** (`pyspark.pandas`, formerly Koalas, merged Spark 3.2). Exam Sec 7.
- **AQE on by default** in Spark 3.2+ (book shows it as opt-in in 3.0).

For these, supplement with official docs at `spark.apache.org/docs/latest/`.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|---|---|
| [ch01](chapters/ch01-introduction.md) | Introduction — Unified Analytics Engine | Driver/executor/cluster manager, deployment modes, 4 components |
| [ch02](chapters/ch02-getting-started.md) | Downloading and Getting Started | Application→Job→Stage→Task, transformations vs actions, narrow vs wide |
| [ch03](chapters/ch03-structured-apis.md) | Structured APIs (DataFrame & Dataset) | Catalyst 4 phases, schemas (DDL & StructType), columns/rows |
| [ch04](chapters/ch04-sql-builtin-sources.md) | Spark SQL & Built-in Data Sources | Reader/Writer, save modes, managed vs unmanaged, temp views |
| [ch05](chapters/ch05-sql-external-sources.md) | Spark SQL — External Sources | UDFs, Pandas UDFs, JDBC partitioning, joins, window functions |
| [ch06](chapters/ch06-datasets.md) | Spark SQL & Datasets | Encoders, Tungsten off-heap, SerDe cost (Scala/Java) |
| [ch07](chapters/ch07-tuning.md) | **Optimizing & Tuning** | Configs, executor memory, cache/persist, join strategies (BHJ/SMJ), Spark UI |
| [ch08](chapters/ch08-structured-streaming.md) | **Structured Streaming** | 5 steps, output modes, triggers, watermarks, stream joins, exactly-once |
| [ch09](chapters/ch09-reliable-data-lakes.md) | Reliable Data Lakes | Database vs lake vs lakehouse, Delta/Iceberg/Hudi |
| [ch10](chapters/ch10-mllib.md) | Machine Learning with MLlib | Transformer/Estimator/Pipeline, CrossValidator, VectorAssembler |
| [ch11](chapters/ch11-ml-pipelines-deployment.md) | ML Pipelines & Deployment | MLflow, batch/streaming/real-time scoring |
| [ch12](chapters/ch12-epilogue-spark-3.md) | Epilogue — Spark 3.0 | AQE, DPP, SQL join hints, Pandas UDF type hints |

## Topic Index

- **Accumulators** → ch07
- **Actions** → ch02
- **AQE / Adaptive Query Execution** → ch07, ch12
- **Broadcast join** → ch07, ch05
- **Broadcast variables** → ch07
- **Bucketing** → ch07
- **Cache / Persist / StorageLevel** → ch07
- **Catalyst optimizer** → ch03
- **Catalog API** → ch04
- **Checkpoint location** → ch08
- **Coalesce vs Repartition** → ch07
- **Cluster manager** → ch01
- **DataFrame API** → ch03, ch04, ch05
- **DataFrameReader / Writer** → ch04
- **Dataset / Encoders** → ch06
- **Date/time functions** (to_date, date_format, unix_timestamp, year/month/day…) → ch05
- **Deployment modes** → ch01
- **Delta Lake** → ch09
- **Dropna / null handling** → ch04, ch05
- **Dynamic allocation** → ch07
- **Exactly-once** → ch08
- **Execution hierarchy (Job/Stage/Task)** → ch02
- **Explain / query plan** → ch03, ch07
- **JDBC** → ch05
- **Joins (inner, outer, broadcast, etc.)** → ch05, ch07
- **Lazy evaluation** → ch02
- **log4j / Driver / Executor logs** → ch07
- **MLlib / spark.ml** → ch10
- **MLflow** → ch11
- **Output modes (append/complete/update)** → ch08
- **Pandas UDFs** → ch05, ch12
- **Parquet** → ch04
- **Partition / partitioning** → ch01, ch07
- **partitionBy on write** → ch04
- **Repartition** → ch07
- **Save modes** → ch04
- **Schemas (DDL string, StructType)** → ch03
- **Shared variables (broadcast + accumulators)** → ch07
- **Shuffle / shuffle.partitions** → ch07
- **Spark Connect** → not in book (see Gaps above)
- **Spark SQL** → ch04, ch05
- **SparkSession** → ch01, ch04
- **Spark UI** → ch07
- **Stateful streaming / StateStore** → ch08
- **Stream–static / stream–stream joins** → ch08
- **Structured Streaming** → ch08
- **Temp view / global temp view** → ch04
- **Triggers (processingTime, once, continuous)** → ch08
- **Tungsten** → ch03, ch06
- **UDFs** → ch05
- **Watermark** → ch08
- **Window functions** → ch05
- **Whole-stage codegen** → ch03

## Supporting Files

- [glossary.md](glossary.md) — every key term with definition and chapter pointer
- [patterns.md](patterns.md) — concrete techniques: when, how, trade-offs
- [cheatsheet.md](cheatsheet.md) — single-page exam reference + sample-Q answers

---

## Scope & Limits

This skill covers the book "Learning Spark, 2nd Edition" content. For Spark features added after early 2020 (Spark Connect, Pandas API on Spark, newer AQE defaults), consult the official Apache Spark docs. For hands-on practice with PySpark notebooks, use Databricks Community Edition.
