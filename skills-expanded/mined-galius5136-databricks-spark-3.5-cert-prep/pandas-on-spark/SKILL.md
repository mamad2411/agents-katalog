---
name: pandas-on-spark
description: "Knowledge base for Pandas API on Spark (pyspark.pandas) — Apache Spark 3.5. Use when preparing for Sec 7 objective 'Explain advantages of using Pandas API on Spark', migrating pandas code to scale on Spark, or configuring pyspark.pandas options (default index type, ops_on_diff_frames, checkpointing). Sources: spark.apache.org 3.5.7 docs + Databricks blog (Koalas merger). NOT covered here: Pandas UDF (separate skill), Spark Connect (see skill spark-connect)."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic or chapter number]
---

# Pandas API on Spark — Exam-Prep Knowledge Base
**Source Spark version**: **3.5.7** + 2021 Databricks Koalas-merger context | **Chapters**: 1 (single deep-dive) | **Generated**: 2026-05-24

> **Scope rule**: All content is **in scope** for Sec 7 of the Databricks Certified Associate Developer for Apache Spark exam, anchored to **Spark 3.5**. Anything Spark 4.x is flagged ⚠️.
>
> **Out of scope for this skill** (cross-links only, no expansion):
> - **Pandas UDF (`@pandas_udf`)** — same exam section but a different API; covered by a separate skill.
> - **Spark Connect** — see skill `spark-connect`.

## How to Use This Skill

- **Without arguments** — loads the Core Frameworks below.
- **By topic** — ask about `default index type`, `to_pandas`, `ops_on_diff_frames`, `checkpoint`, `Koalas`, etc.
- **By chapter** — only `ch01`; the topic is single-chapter sized.

---

## Core Frameworks & Mental Models

### Pandas API on Spark in one paragraph
**`pyspark.pandas`** is a **pandas-compatible DataFrame API that executes distributed on Spark**. It started as the standalone **Koalas** project (Databricks) and was merged into PySpark with **Spark 3.2** (Sept-Oct 2021, via the SPIP under Project Zen). Goal: let pandas users scale from single-machine to multi-TB cluster workloads with **a single import change** (`import pandas as pd` → `import pyspark.pandas as pd`), while keeping the entire downstream code identical.

### Why use it (advantages — exam objective 1)
1. **Familiar pandas syntax at Spark scale** — minimal code change to scale.
2. **No extra install** since Spark 3.2 — ships with PySpark.
3. **Single-machine speedup** via Catalyst optimizer + whole-stage codegen (Databricks 2021 benchmark: ~4× faster join on 130 GB CSV vs native pandas; survives chain operations where pandas OOMs).
4. **Linear scalability** — same job runs on 60 GB single-machine or 15 TB on 256-node cluster (Databricks benchmark: ~10s std-dev compute in both cases).
5. **Unified analytics** — same DataFrames feed `ps.sql(...)`, Spark Structured Streaming, and MLlib.
6. **Lazy execution** — Catalyst plans and optimizes; jobs trigger only when needed.
7. **All Spark features work** — web UI, history server, AQE, dynamic allocation, deployment modes.

### The three DataFrames

| API | Where | Use case |
|---|---|---|
| **pandas** | single machine | data fits in RAM |
| **`pyspark.pandas`** (Pandas API on Spark) | distributed on Spark | large data, **pandas syntax** |
| **PySpark DataFrame** | distributed on Spark | low-level Spark control, SQL |

### Conversions (cheat)

| From → To | Method |
|---|---|
| pandas-on-Spark → pandas | `psdf.to_pandas()` ⚠️ collects to driver |
| pandas → pandas-on-Spark | `ps.from_pandas(pdf)` |
| pandas-on-Spark → PySpark | `psdf.to_spark(index_col='…')` |
| PySpark → pandas-on-Spark | `sdf.pandas_api(index_col='…')` |

**Always pass `index_col`** on the Spark roundtrip to skip default-index regeneration.

### Options system (4 ways to interact)
```python
import pyspark.pandas as ps

ps.options.display.max_rows                    # attribute
ps.get_option("display.max_rows")              # function
ps.set_option("display.max_rows", 50)
ps.reset_option("display.max_rows")

with ps.option_context("compute.max_rows", 5000):
    ...                                        # temporary
```

### Default index types — exam-worthy

| Value | Distribution | Sequential? | Performance | Use case |
|---|---|---|---|---|
| `'sequence'` | single partition | yes | poor on large data | small datasets only |
| **`'distributed-sequence'`** (default) | distributed | yes | medium | production default |
| `'distributed'` | distributed | **no** (indeterministic) | best | when index values don't matter |

**Critical rule**: never combine `'distributed'` index with `compute.ops_on_diff_frames=True` → indeterministic alignment → wrong results.

### Top options to know (Spark 3.5 defaults)

| Option | Default | Behavior |
|---|---|---|
| `compute.default_index_type` | `'distributed-sequence'` | Index strategy |
| `compute.ops_on_diff_frames` | **False** | Block expensive cross-DF implicit join |
| `compute.max_rows` | 1000 | Shortcut threshold (collect→pandas) |
| `compute.shortcut_limit` | 1000 | Rows for schema inference |
| `compute.eager_check` | True | Upfront validation |
| `compute.isin_limit` | 80 | `isin(list)` ≥ this → broadcast join |
| `display.max_rows` | 1000 | Repr cap |
| `plotting.backend` | `'plotly'` | or `'matplotlib'` |

### Best-practice signals

- **Configure Spark BEFORE** `import pyspark.pandas`
- **Enable Arrow**: `.config("spark.sql.execution.arrow.pyspark.enabled", "true")`
- **`psdf.spark.explain()`** to inspect the plan
- **`psdf.spark.local_checkpoint()`** to truncate long lineages
- **`GroupBy.rank()`** instead of `DataFrame.rank()` (avoids SinglePartition)
- **`.apply(fn)` with return type hint** instead of Python `for` loops
- **`.max()` / `.min()` / `.sum()`** methods, NOT Python built-ins (`max(s)` fails)

### Anti-patterns

- `max(ps_series)` / `for v in ps_series:` — no `__iter__` on purpose
- `.to_pandas()` on multi-GB data — driver OOM
- `'distributed'` index + `ops_on_diff_frames=True` — broken alignment
- Duplicate / case-conflict column names — Spark SQL rejects
- Reserved column names `__foo__` — internal use
- `DataFrame.rank()` on large data — collapses to one partition
- Flipping `compute.ops_on_diff_frames=True` to "just make it work" — implicit expensive join

---

## Exam Sec 7 — coverage mapping

| Sec 7 objective | This skill | Other skill |
|---|---|---|
| "Explain advantages of using Pandas API on Spark" | ✅ fully covered | – |
| "Create and invoke Pandas UDF" | ❌ different topic | (separate Pandas UDF skill — TBD) |

---

## ⚠ Post-3.5 — DO NOT memorize for the 3.5 exam

- Any `pyspark.pandas` API additions in **Spark 4.0+** are out of scope.
- The 3.5 defaults shown above are the canonical exam target.

---

## Chapter Index

| # | Title | Focus |
|---|---|---|
| [ch01](chapters/ch01-pandas-on-spark.md) | Pandas API on Spark | Single deep-dive: advantages, conversions, options, best practices, anti-patterns |

## Topic Index

- **`.apply()`** → ch01
- **`compute.*` options** → ch01
- **Conversions (pandas / pandas-on-Spark / PySpark)** → ch01
- **Default index type** → ch01
- **`distributed` vs `distributed-sequence` vs `sequence`** → ch01
- **`from_pandas`** → ch01
- **`get_option` / `set_option` / `option_context`** → ch01
- **Koalas merger / Project Zen** → ch01
- **Lazy execution** → ch01
- **`ops_on_diff_frames`** → ch01
- **`.pandas_api()`** → ch01
- **`pyspark.pandas`** → ch01
- **`.spark.checkpoint()` / `.spark.local_checkpoint()`** → ch01
- **`.spark.explain()`** → ch01
- **`.to_pandas()` / `.to_spark()`** → ch01
- **Three-DataFrame model** → ch01

## Supporting Files
- [glossary.md](glossary.md) — terms with chapter pointers
- [patterns.md](patterns.md) — concrete techniques + when/how/trade-offs
- [cheatsheet.md](cheatsheet.md) — single-page exam reference + post-3.5 traps

## Sources used
Apache Spark 3.5.7 user guide (primary):
- https://spark.apache.org/docs/3.5.7/api/python/user_guide/pandas_on_spark/index.html
- https://spark.apache.org/docs/3.5.7/api/python/user_guide/pandas_on_spark/pandas_pyspark.html
- https://spark.apache.org/docs/3.5.7/api/python/user_guide/pandas_on_spark/options.html
- https://spark.apache.org/docs/3.5.7/api/python/user_guide/pandas_on_spark/best_practices.html

Databricks blog (historical context):
- https://www.databricks.com/blog/2021/10/04/pandas-api-on-upcoming-apache-spark-3-2.html

> To regenerate local snapshots: fetch each URL above and extract the relevant sections (the chapter file `ch01-pandas-on-spark.md` synthesizes them).

## Scope & Limits

This skill is calibrated for **Sec 7 of the Databricks Certified Associate Developer for Apache Spark exam**, scoped strictly to `pyspark.pandas` at **Spark 3.5**. For **Pandas UDF** (the other Sec 7 objective), use the dedicated Pandas UDF skill. For **Spark Connect**, see skill `spark-connect`.
