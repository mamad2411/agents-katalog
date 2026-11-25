---
name: spark-3.5-updates
description: "Knowledge base for Spark 3.1→3.5 updates not covered by the Learning Spark 2nd Ed book. Use for: (A) Pandas UDF and Arrow APIs (exam Sec 7 obj 2 'Create and invoke Pandas UDF'); (B) new built-in functions added in 3.3-3.5 (exam Sec 3); (C) AQE evolution post-3.0 — default-on, new sub-configs, SMJ→SHJ conversion (exam Sec 4). NOT covered here: Pandas API on Spark (see skill pandas-on-spark), Spark Connect (see skill spark-connect), AQE 3.0 baseline (see apache-spark ch07/ch12)."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic A/B/C, function name, or chapter]
---

# Spark 3.1 → 3.5 Updates — Exam-Prep Knowledge Base
**Anchor**: Spark **3.5** | **Chapters**: 3 | **Generated**: 2026-05-24

> **Scope**: only what changed BETWEEN the Damji book (Spark 3.0 baseline) AND Spark 3.5. Anything Spark 4.x is flagged ⚠️.
>
> **Topics covered**:
> - **A**: Pandas UDF type hints + Pandas Function APIs + Arrow Python UDF — Sec 7 obj 2
> - **B**: New built-in functions added in Spark 3.3-3.5 — Sec 3 supplement
> - **C**: AQE evolution vs Spark 3.0 baseline — Sec 4 supplement
>
> **Cross-references** (don't expand here):
> - **Pandas API on Spark** (`pyspark.pandas`) → skill `pandas-on-spark`
> - **Spark Connect** → skill `spark-connect`
> - **AQE 3.0 baseline + Spark UI** → `apache-spark/chapters/ch07-tuning.md`
> - **Spark 3.0 epilogue / Catalyst** → `apache-spark/chapters/ch12-epilogue-spark-3.md`

## How to Use This Skill

- **Without arguments** — load the Core Frameworks below.
- **By topic letter** — A (Pandas UDF), B (functions), C (AQE).
- **By chapter** — `ch01`, `ch02`, `ch03`.

---

## Core Frameworks & Mental Models

### Topic A — Pandas UDF (Sec 7 obj 2)

**Pandas UDF** = vectorized Python UDF using Arrow as transport between JVM and Python. Spark 3.0+ uses Python type hints; legacy `PandasUDFType` (book Damji ch.5) is deprecated.

#### The 4 type-hint shapes
| # | Type hint | Use |
|---|---|---|
| 1 | `pd.Series, ... -> pd.Series` | Series-to-Series scalar |
| 2 | `Iterator[pd.Series] -> Iterator[pd.Series]` | Iterator scalar (per-worker state) |
| 3 | `Iterator[Tuple[pd.Series, ...]] -> Iterator[pd.Series]` | Iterator multi-Series |
| 4 | `pd.Series, ... -> Any` | Grouped aggregate / window |

#### Pandas Function APIs (whole DataFrame, not column)
- `df.mapInPandas(func, schema)` — iterator pd.DataFrame → iterator pd.DataFrame
- `df.groupby(k).applyInPandas(func, schema)` — one pd.DataFrame per group
- `df.groupby(k).cogroup(other.groupby(k)).applyInPandas(func, schema)` — two pd.DataFrames per cogroup

#### Arrow Python UDF (Spark 3.5+)
```python
@udf(returnType="int", useArrow=True)   # row-by-row, Arrow transport
def f(s): return len(s)
```
- `useArrow=True/False/None`. `None` → fall back to `spark.sql.execution.pythonUDF.arrow.enabled`
- Better type coercion than default pickled UDF; still row-by-row (not vectorized)

#### Legacy → modern (Damji book mapping)
| Legacy | Modern |
|---|---|
| `PandasUDFType.SCALAR` | type hint #1 |
| `PandasUDFType.SCALAR_ITER` | type hint #2 |
| `PandasUDFType.GROUPED_AGG` | type hint #4 |
| `PandasUDFType.GROUPED_MAP` | `groupby().applyInPandas` (not `@pandas_udf`) |

### Topic B — New functions 3.3 → 3.5 (Sec 3)

**Filtered, exam-curated set** (full table in `cheatsheet.md` and ch02). Highlights:

- **Array** (3.4+): `array_append`, `array_insert`, `array_compact`, `array_sort(comparator)`, `array_prepend` (3.5)
- **Array** (3.3): `array_size`, `try_element_at`
- **String** (3.3): `contains`, `startswith`, `endswith`, `ilike`, `to_number`
- **String** (3.4): `split_part`, `regexp_count`, `regexp_substr`, `mask`
- **Date/time** (3.3): `timestampadd`, `timestampdiff`, `convert_timezone`, `make_date`
- **Aggregate** (3.4): `median`, `mode`, `any_value`, `percentile_cont`, `percentile_disc`
- **Aggregate** (3.3): `max_by`, `min_by`, `array_agg`
- **Misc**: `equal_null` (3.4), `unpivot`/`melt` (3.4), `DataFrame.offset` (3.5), `assertDataFrameEqual` (3.5)

### Topic C — AQE delta vs 3.0 (Sec 4)

Read `apache-spark/chapters/ch07-tuning.md` and `ch12-epilogue-spark-3.md` first for the 3.0 baseline.

#### Big-picture delta
| | Spark 3.0 (book) | Spark 3.5 |
|---|---|---|
| `spark.sql.adaptive.enabled` default | **false** (opt-in) | **true** (since 3.2 — SPARK-33679) |
| Runtime join switches | SMJ → BHJ | + **SMJ → ShuffledHashJoin** (3.2) |
| DPP × AQE | separate | fully compatible (3.2) |

#### Key new configs (exam-worthy)
- `spark.sql.adaptive.enabled` — **true** by default since 3.2
- `…coalescePartitions.parallelismFirst` — **true** by default (3.2); ⚠ silently ignores `advisoryPartitionSizeInBytes`
- `…coalescePartitions.minPartitionSize` — 1 MB default (3.2)
- `…maxShuffledHashJoinLocalMapThreshold` — 0 default; >0 enables SMJ→SHJ (3.2)
- `…autoBroadcastJoinThreshold` (AQE-specific) — overrides static for runtime decisions (3.2)
- `…forceOptimizeSkewedJoin` — false default; force skew handling even with extra shuffle (3.3)
- `…rebalancePartitionsSmallPartitionFactor` — 0.2 default; merge tiny fragments after skew splitting (3.3)
- `…optimizer.excludedRules` — disable AQE rules by name (3.1)
- `…customCostEvaluatorClass` — pluggable cost evaluator (3.2)

#### Top exam pitfalls
1. `parallelismFirst=true` (3.2 default) **ignores** `advisoryPartitionSizeInBytes`.
2. AQE on by default since 3.2 means upgrade silently enables it.
3. SMJ → SHJ is a **new** join switch (3.2), distinct from SMJ → BHJ (3.0).

---

## Exam Sec coverage mapping

| Topic | Exam section | Status |
|---|---|---|
| Pandas UDF + Function APIs + Arrow UDF | **Sec 7 obj 2** | ✅ this skill |
| New built-in functions 3.3-3.5 | Sec 3 supplement | ✅ this skill |
| AQE evolution | Sec 4 supplement | ✅ this skill |
| AQE 3.0 baseline | Sec 4 | → `apache-spark` ch07/ch12 |
| Pandas API on Spark | Sec 7 obj 1 | → skill `pandas-on-spark` |
| Spark Connect | Sec 6 | → skill `spark-connect` |
| All other DataFrame/SQL/Streaming/Architecture | Sec 1-5 | → skill `apache-spark` |

---

## Chapter Index

| # | Title | Topic | Focus |
|---|---|---|---|
| [ch01](chapters/ch01-pandas-udf-and-arrow.md) | Pandas UDF & Arrow APIs | A | 4 type hints, Pandas Function APIs, Arrow Python UDF, legacy mapping |
| [ch02](chapters/ch02-new-builtin-functions.md) | New Built-in Functions 3.3-3.5 | B | ~25 functions, version-tagged, with purpose |
| [ch03](chapters/ch03-aqe-delta-vs-3.0.md) | AQE Delta vs Spark 3.0 | C | New configs, SMJ→SHJ, parallelismFirst gotcha |

## Topic Index

### Topic A (Pandas UDF / Arrow)
- `@pandas_udf` → ch01
- `@udf(useArrow=True)` (Spark 3.5+) → ch01
- 4 type-hint shapes → ch01
- `applyInPandas` / `mapInPandas` / `cogroup().applyInPandas` → ch01
- `PandasUDFType` (legacy) → ch01
- Arrow batch size config → ch01
- `selfDestruct` (3.2+) → ch01

### Topic B (new functions)
- Array: `array_append/insert/compact/sort/prepend/size`, `try_element_at`, `array_agg` → ch02
- String: `contains/startswith/endswith/ilike`, `to_number`, `split_part`, `regexp_*`, `mask` → ch02
- Date/time: `timestampadd/diff`, `convert_timezone`, `make_date` → ch02
- Aggregate: `median`, `mode`, `any_value`, `percentile_cont/disc`, `max_by/min_by`, `histogram_numeric` → ch02
- Misc: `equal_null`, `unpivot/melt`, `DataFrame.offset` (3.5), `assertDataFrameEqual` (3.5), `map_contains_key` → ch02

### Topic C (AQE)
- `spark.sql.adaptive.enabled` default change → ch03
- `parallelismFirst` gotcha → ch03
- `forceOptimizeSkewedJoin` → ch03
- `maxShuffledHashJoinLocalMapThreshold` → ch03
- SMJ → SHJ runtime conversion → ch03
- AQE × DPP compatibility → ch03
- `excludedRules` / `customCostEvaluatorClass` → ch03
- Local Shuffle Reader → ch03

## Supporting Files
- [glossary.md](glossary.md) — terms version-tagged
- [patterns.md](patterns.md) — concrete patterns: migrate legacy, choose UDF kind, AQE config sanity checks
- [cheatsheet.md](cheatsheet.md) — single-page exam reference

## Sources used

Topic A:
- https://spark.apache.org/docs/3.5.7/api/python/user_guide/sql/arrow_pandas.html (primary)
- https://spark.apache.org/docs/3.5.7/api/python/reference/pyspark.sql/api/pyspark.sql.functions.pandas_udf.html
- https://spark.apache.org/docs/3.5.7/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udf.html

Topic B:
- https://spark.apache.org/releases/spark-release-3-5-0.html
- https://spark.apache.org/releases/spark-release-3-4-0.html
- https://spark.apache.org/releases/spark-release-3-3-0.html
- https://spark.apache.org/docs/3.5.7/sql-ref-functions-builtin.html (referenced for cross-checking)

Topic C:
- https://spark.apache.org/docs/3.5.7/sql-performance-tuning.html (master AQE config doc)
- https://www.databricks.com/blog/2021/10/19/introducing-apache-spark-3-2.html (SPARK-33679)

> To regenerate local snapshots: fetch each URL above and extract the relevant sections (the chapter files in `chapters/` synthesize them).

---

## Scope & Limits

This skill is calibrated for the exam objectives **not covered** by the Damji book due to its 2020 publication anchored on Spark 3.0. For everything book-covered, see `apache-spark`. For Pandas API on Spark or Spark Connect, see the dedicated skills.
