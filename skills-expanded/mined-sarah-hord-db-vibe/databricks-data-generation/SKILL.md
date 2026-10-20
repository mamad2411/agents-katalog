---
name: databricks-data-generation
description: "Generate realistic synthetic data for demos and testing across retail, healthcare (incl. clinical trials), financial, IoT, manufacturing, supply chain, oil & gas, and gaming industries using Polars + Mimesis (local/UC) or dbldatagen (Connect/notebooks)."
argument-hint: "[industry] [--rows N] [--catalog NAME] [--schema NAME]"
audience: external
---

> **This skill is self-contained.** All tier definitions, code patterns, and reference files are documented below. Do not search the filesystem or spawn agents to find additional files. Catalog and schema are **always user-supplied** — never default to any value. If the user hasn't provided them, ask. For any UC write, **always create the schema if it doesn't exist** before writing data.

# Synthetic Data Generator

Generate realistic synthetic data for demos, proof-of-concepts, and testing.

## Three-Tier Architecture

| Tier  | Volume                   | Engine                                                                                     | Output                                                                           | Dependencies                                                                    |
| ----- | ------------------------ | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **1** | <500K rows               | Polars + NumPy + Mimesis                                                                   | `./output/{industry}/` (local parquet) **or** UC Delta tables via Connect bridge | `polars`, `numpy`, `mimesis` (+ `databricks-connect` for UC write)              |
| **2** | 500K-5M rows             | **dbldatagen + Connect** (primary) or Polars + NumPy + Mimesis → Connect (when Mimesis PII needed) | Unity Catalog Delta tables                                                       | `dbldatagen`, `databricks-connect` or `polars`, `numpy`, `mimesis`, `databricks-connect` |
| **3** | >5M rows or UDF features | dbldatagen (notebooks — full feature set)                                                  | Unity Catalog Delta tables                                                       | `dbldatagen` (pre-installed in DBR)                                             |

> **Key design:** For Tier 2, **dbldatagen works over Databricks Connect + serverless** for all Catalyst-safe features (`values=`, `weights=`, `minValue`/`maxValue`, `expr=`, `begin`/`end`, `percentNulls=`, `omit=True`). Only UDF-dependent features (`text=mimesisText()`, `distribution=Gamma/Beta`, `.withConstraint()`, `template=` with UDF patterns) require Tier 3 notebooks. Polars + NumPy + Mimesis remains an alternative Tier 2 engine when rich PII or statistical distributions are needed locally.

### Decision Tree

- Wants local parquet, <500K rows, no UC needed → **Tier 1** (Polars + NumPy + Mimesis → local parquet)
- Wants UC Delta tables, <500K rows → **Tier 1 + UC write** (Polars + NumPy + Mimesis → Connect bridge to UC)
- Wants UC Delta tables, 500K-5M rows → **Tier 2** (dbldatagen + Connect — primary)
- Wants UC Delta tables but needs Mimesis PII or NumPy statistical distributions → **Tier 2** (Polars + NumPy + Mimesis → Connect write)
- Wants >5M rows, streaming, CDC, or UDF features (`mimesisText`, `distribution=`, `.withConstraint()`) → **Tier 3** (dbldatagen in notebook)
- Explicitly asks for Polars/local/offline → **Tier 1**
- Explicitly asks for notebook → **Tier 3**

> **Trigger phrases for UC write:** "save to Unity Catalog", "write to UC", "I need this in UC", "save to Delta tables", `--catalog NAME`. When any of these are present, use the Connect bridge pattern even for small datasets.

## Invocation

When invoked with arguments (`/databricks-data-generation $ARGUMENTS`):

| Argument         | Position | Example                                                     | Default                      |
| ---------------- | -------- | ----------------------------------------------------------- | ---------------------------- |
| Industry         | `$0`     | `retail`, `healthcare`, `financial`, `iot`, `manufacturing`, `supply_chain`, `oil_gas`, `gaming`, `clinical_trials` | _(prompt user)_              |
| `--rows N`       | flag     | `--rows 100000`                                             | `10000`                      |
| `--tier N`       | flag     | `--tier 2`                                                  | Auto from row count          |
| `--catalog NAME` | flag     | `--catalog main`                                            | _(ask user if not provided)_ |
| `--schema NAME`  | flag     | `--schema retail`                                           | _(ask user if not provided)_ |

### Examples

- `/databricks-data-generation retail --rows 50000` → Tier 1 local parquet
- `/databricks-data-generation retail --rows 10000 --catalog demo` → Tier 1 + UC write via Connect bridge
- `/databricks-data-generation healthcare --rows 500000 --catalog demo` → Tier 2 UC Delta
- `/databricks-data-generation iot --rows 10000000 --tier 3` → Recommend Tier 3 notebook
- `/databricks-data-generation supply_chain --rows 1000 --catalog demo` → 6-table supply chain dataset
- `/databricks-data-generation oil_gas --tier 3` → ARPS decline curves in notebook
- `/databricks-data-generation gaming --rows 5000000 --tier 3` → Hash-based login events (notebook only)
- `/databricks-data-generation clinical_trials --rows 5000 --catalog demo` → 5-table clinical trials variant
- "generate 10K healthcare rows and save to Unity Catalog" → Tier 1 + UC write

When invoked without arguments, use the Decision Tree to determine tier and prompt for industry, catalog, and schema.

## Generation Plan (Required Before Code Generation)

**Before generating any code, ALWAYS present a Generation Plan for user approval.**

After determining tier, industry, row count, and output destination from the user's request and the Decision Tree, present a plan in this format:

### Plan Template

```
## 📋 Generation Plan: {Industry}

**Tier:** {N} | **Engine:** {engine_name} | **Seed:** 42
**Compute:** {`None (local only)` or `Serverless (via Databricks Connect)`}
**Output:** {`./output/{industry}/` or `{catalog}.{schema}.*`}
**Run command:** `uv run --with {deps} script.py`

---

### {table_name} — {row_count:,} rows

| Column | Type | Generation | Notes |
|---|---|---|---|
| {col} | {type} | {method} | {nulls, weights, FK, distribution, etc.} |

*(repeat for each table)*

### Relationships
- `{child_table}.{fk_col}` → `{parent_table}.{pk_col}`

---

**Options:**
- "looks good" → generate the full dataset
- "sample" → generate 100 rows per table as a preview first
- or request changes (e.g., "drop the inventory table", "change rows to 50K", "add a discount_pct column")
```

### Plan Rules

1. **Never skip the plan** — always present it before writing code, even for simple requests
2. **Full column detail** — list every column per table with type, generation method, and parameters (null rates, value weights, FK targets, distributions, date ranges)
3. **Source from skill content** — use the Industry Quick Reference tables and reference generator scripts already in this skill for column definitions; adapt for user overrides
4. **Wait for explicit approval** — do not generate code until the user says "looks good", "go", "yes", or similar
5. **Handle modifications** — if the user changes anything, update the plan and re-present the modified version
6. **Sample mode** — when the user says "sample", generate a 100-row-per-table version, display `print(df.head(20))` for each table, then ask "Generate the full dataset?" before proceeding to the real run
7. **Preserve plan as code comments** — when generating the final script, include a header comment summarizing the approved plan (tables, row counts, output destination) for session continuity
8. **Serverless acknowledgment** — when the plan uses Databricks Connect (Tier 1+UC, Tier 2, or Tier 3 with Connect), the `Compute: Serverless` line alerts the user that serverless compute will be used; do not proceed until the user acknowledges this as part of their plan approval

## Running Generated Scripts

This skill has **no `pyproject.toml`** — scripts are standalone reference implementations.
Always use `uv run --with` to supply dependencies at execution time:

```bash
# Tier 1 — local parquet only
uv run --with polars --with numpy --with mimesis scripts/my_script.py

# Tier 1 + UC write — Polars generates locally, Connect bridge writes to UC
uv run --with polars --with numpy --with mimesis --with "databricks-connect>=16.4,<17.0" scripts/my_script.py

# Tier 2 (dbldatagen) — generate via Connect + serverless, write to UC
uv run --with "databricks-connect==16.2.*" --with dbldatagen --with jmespath --with pyparsing scripts/my_script.py

# Tier 2 (Polars alternative) — Polars generates locally, Connect writes to UC
uv run --with polars --with numpy --with mimesis --with "databricks-connect>=16.4,<17.0" scripts/my_script.py
```

> **Do NOT** use `uv add`, `uv pip install`, or `pip install` — there is no project venv to install into.
> **Tier 3** (dbldatagen in notebooks) is for >5M rows or UDF features — no local execution needed.

### Environment Check

> Databricks profile: !`databricks auth profiles 2>/dev/null | head -5 || echo "No profiles configured — Tier 1 (local) only"`

## Quick Start: Tier 1 (Polars + NumPy + Mimesis)

Fast local generation — no Spark session, no JVM, no Databricks Connect required. NumPy vectorizes all randomness; Mimesis pools ~1K unique values then NumPy samples at array speed.

```python
import numpy as np
import polars as pl
from mimesis import Generic
from mimesis.locales import Locale

rng = np.random.default_rng(42)
g = Generic(locale=Locale.EN, seed=42)
rows = 10_000

# Pool-and-sample: generate ~1K unique Mimesis values, then NumPy picks from pool
pool = min(1_000, rows)
_first = np.array([g.person.first_name() for _ in range(pool)])
_last = np.array([g.person.last_name() for _ in range(pool)])

start = np.datetime64("2020-01-01")
span = (np.datetime64("2024-12-31") - start).astype(int)

_tier_w = np.array([50, 30, 15, 5], dtype=np.float64)

customers = pl.DataFrame({
    "customer_id": np.arange(1_000_000, 1_000_000 + rows),
    "first_name": _first[rng.integers(0, pool, size=rows)],
    "last_name": _last[rng.integers(0, pool, size=rows)],
    "loyalty_tier": rng.choice(
        ["Bronze", "Silver", "Gold", "Platinum"],
        size=rows, p=_tier_w / _tier_w.sum()),
    "signup_date": start + rng.integers(0, span + 1, size=rows).astype("timedelta64[D]"),
})
customers.write_parquet("output/retail/customers.parquet")
print(customers.head())
```

See [polars-generation-guide.md](references/polars-generation-guide.md) for full patterns (distributions, nulls, FKs, derived columns).

## Quick Start: Tier 1 + UC Write (Polars → Connect Bridge)

Same Polars + NumPy + Mimesis generation as Tier 1, but writes to Unity Catalog via the Connect bridge. Use this when the user asks to **save to Unity Catalog** for datasets <500K rows.

```python
import numpy as np
import polars as pl
from mimesis import Generic
from mimesis.locales import Locale
from databricks.connect import DatabricksSession

rng = np.random.default_rng(42)
g = Generic(locale=Locale.EN, seed=42)
rows = 10_000

pool = min(1_000, rows)
_first = np.array([g.person.first_name() for _ in range(pool)])
_last = np.array([g.person.last_name() for _ in range(pool)])

start = np.datetime64("2020-01-01")
span = (np.datetime64("2024-12-31") - start).astype(int)
_tier_w = np.array([50, 30, 15, 5], dtype=np.float64)

# --- Generate with Polars + NumPy + Mimesis (same as Tier 1) ---
customers = pl.DataFrame({
    "customer_id": np.arange(1_000_000, 1_000_000 + rows),
    "first_name": _first[rng.integers(0, pool, size=rows)],
    "last_name": _last[rng.integers(0, pool, size=rows)],
    "loyalty_tier": rng.choice(
        ["Bronze", "Silver", "Gold", "Platinum"],
        size=rows, p=_tier_w / _tier_w.sum()),
    "signup_date": start + rng.integers(0, span + 1, size=rows).astype("timedelta64[D]"),
})

# --- Write to Unity Catalog via Connect bridge ---
CATALOG = "my_catalog"  # ← replace with user-supplied catalog
SCHEMA = "retail"  # ← replace with user-supplied schema

spark = DatabricksSession.builder.serverless().getOrCreate()

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

spark_df = spark.createDataFrame(customers.to_pandas())
(spark_df.write.format("delta")
 .mode("overwrite")
 .option("overwriteSchema", "true")
 .saveAsTable(f"{CATALOG}.{SCHEMA}.customers"))

print(f"Wrote {spark.table(f'{CATALOG}.{SCHEMA}.customers').count():,} rows")
spark.stop()
```

Run: `uv run --with polars --with numpy --with mimesis --with "databricks-connect>=16.4,<17.0" script.py`

## Quick Start: Tier 2 (dbldatagen + Connect → UC)

dbldatagen generates data via Databricks Connect + serverless compute using Catalyst-safe features. All standard features work — only UDF-dependent features (mimesisText, distributions, constraints) require notebooks.

### Setup

```bash
databricks configure  # DEFAULT profile, auto-discovered
```

### Primary Pattern: dbldatagen + Connect

```python
from databricks.connect import DatabricksSession
import dbldatagen as dg
from pyspark.sql.types import StringType, IntegerType, FloatType, DecimalType, TimestampType

spark = DatabricksSession.builder.serverless().getOrCreate()

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

customers = (
    dg.DataGenerator(sparkSession=spark, name="customers", rows=1_000_000, partitions=10)
    .withIdOutput()
    .withColumn("first_name", StringType(), values=FIRST_NAMES, random=True)
    .withColumn("last_name", StringType(), values=LAST_NAMES, random=True)
    .withColumn("email", StringType(),
        expr="lower(concat(first_name, '.', last_name, cast(id % 1000 as string), '@example.com'))",
        baseColumns=["first_name", "last_name"])
    .withColumn("age", IntegerType(), minValue=18, maxValue=85, random=True)
    .withColumn("lifetime_value", DecimalType(12, 2), minValue=0, maxValue=50000, random=True)
    .withColumn("loyalty_tier", StringType(),
                values=["Bronze", "Silver", "Gold", "Platinum"],
                weights=[50, 30, 15, 5])
    .withColumn("signup_ts", TimestampType(),
                begin="2020-01-01 00:00:00", end="2024-12-31 23:59:59",
                interval="1 day", random=True)
    .withColumn("is_active", "boolean", expr="rand() < 0.85")
    .withColumn("percent_nulls_email", StringType(), percentNulls=0.05,
                values=FIRST_NAMES, random=True, omit=True)
    .build()
)

customers.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("my_catalog.retail.customers")  # ← replace with user-supplied catalog.schema
spark.stop()
```

See [dbldatagen-connect-patterns.md](references/dbldatagen-connect-patterns.md) for the full validated pattern reference.

### Alternative Pattern: Polars + NumPy + Mimesis → Connect

Use this when you need rich Mimesis PII (realistic names, emails, addresses) or NumPy statistical distributions (`rng.gamma`, `rng.beta`):

```python
import numpy as np
import polars as pl
from mimesis import Generic
from mimesis.locales import Locale
from databricks.connect import DatabricksSession

rng = np.random.default_rng(42)
g = Generic(locale=Locale.EN, seed=42)
rows = 100_000

pool = min(1_000, rows)
_first = np.array([g.person.first_name() for _ in range(pool)])
_last = np.array([g.person.last_name() for _ in range(pool)])
_email = np.array([g.person.email() for _ in range(pool)])
_tier_w = np.array([50, 30, 15, 5], dtype=np.float64)

customers = pl.DataFrame({
    "customer_id": np.arange(1_000_000, 1_000_000 + rows),
    "first_name": _first[rng.integers(0, pool, size=rows)],
    "last_name": _last[rng.integers(0, pool, size=rows)],
    "email": _email[rng.integers(0, pool, size=rows)],
    "lifetime_value": np.round(rng.gamma(2.0, 2.0, size=rows) * 2500, 2),
    "loyalty_tier": rng.choice(
        ["Bronze", "Silver", "Gold", "Platinum"],
        size=rows, p=_tier_w / _tier_w.sum()),
})

spark = DatabricksSession.builder.serverless().getOrCreate()
spark_df = spark.createDataFrame(customers.to_pandas())
(spark_df.write.format("delta")
 .mode("overwrite")
 .option("overwriteSchema", "true")
 .saveAsTable("my_catalog.retail.customers"))  # ← replace with user-supplied catalog.schema
```

### UC Provisioning

**The catalog must already exist** — create via Databricks UI or ask a workspace admin. Check schema existence before creating:

```python
spark.sql("CREATE SCHEMA IF NOT EXISTS my_catalog.retail")  # ← replace with user-supplied catalog.schema
```

For SDK-based provisioning, see `scripts/utils/uc_setup.py`.

## Quick Start: Tier 3 (dbldatagen in Notebooks — Full Feature Set)

Use Tier 3 for >5M rows **or** when you need UDF-dependent features that don't work over Connect:

- `text=mimesisText(...)` — requires mimesis on workers
- `distribution=Gamma/Beta/Normal` — requires dbldatagen classes to deserialize on workers
- `.withConstraint()` — Connect Column type mismatch
- `template=` with UDF patterns

```python
# In a Databricks notebook — full dbldatagen feature set available
import dbldatagen as dg
from utils.mimesis_text import mimesisText

customers = (
    dg.DataGenerator(spark, rows=10_000_000, partitions=100, randomSeed=42)
    .withColumn("customer_id", "long", minValue=1_000_000, uniqueValues=10_000_000)
    .withColumn("first_name", "string", text=mimesisText("person.first_name"))
    .withColumn("last_name", "string", text=mimesisText("person.last_name"))
    .withColumn("lifetime_value", "decimal(12,2)", minValue=0, maxValue=50000,
                distribution=dg.distributions.Gamma(shape=2.0, scale=2.0))
    .withColumn("loyalty_tier", "string",
                values=["Bronze", "Silver", "Gold", "Platinum"],
                weights=[50, 30, 15, 5])
    .build()
)
customers.write.format("delta").mode("overwrite").saveAsTable("catalog.schema.customers")
```

See [dbldatagen-guide.md](references/dbldatagen-guide.md) for the full API.

## Schema Introspection & Generation

Use `DataAnalyzer` to introspect existing Unity Catalog tables and generate matching synthetic data:

```python
from dbldatagen import DataAnalyzer

analyzer = DataAnalyzer(spark, "prod.sales.customers")
summary_df = analyzer.summarizeToDF()
display(summary_df)

code = analyzer.scriptDataGeneratorFromData()
print(code)  # Copy-paste and refine
```

See [schema-introspection-patterns.md](references/schema-introspection-patterns.md) for complete workflows.

## Key Capabilities

- [CDC Patterns](references/cdc-patterns.md) — APPEND/UPDATE/DELETE operations for pipeline demos
- [Data Quality Injection](references/data-quality-patterns.md) — Nulls, duplicates, late-arriving data
- [Streaming Patterns](references/streaming-patterns.md) — Real-time data with `withStreaming=True`
- [Medallion Architecture](references/medallion-patterns.md) — Bronze/Silver/Gold with UC Volumes
- [Multi-Table Patterns](references/multi-table-patterns.md) — FK consistency, cardinality control
- [Seasonality Patterns](references/seasonality-patterns.md) — Monthly/weekly/campaign time patterns
- [ML Feature Patterns](references/ml-feature-patterns.md) — Drift simulation, label imbalance, feature arrays
- [Schema Introspection](references/schema-introspection-patterns.md) — DataAnalyzer for UC table -> synthetic data
- [Time-Series Patterns](references/time-series-patterns.md) — Temporal data patterns

## Output Destinations

| Tier            | Pattern                 | Code                                                          |
| --------------- | ----------------------- | ------------------------------------------------------------- |
| **1** local     | Polars + NumPy → parquet | `df.write_parquet("output/{industry}/{table}.parquet")`       |
| **1 + UC**      | Polars + NumPy → Connect bridge | `spark.createDataFrame(df.to_pandas()).write...saveAsTable()` |
| **2** primary   | dbldatagen → UC         | `spec.build().write...saveAsTable()`                          |
| **2** alt       | Polars → Connect        | Same as Tier 1 + UC                                           |
| **3** notebook  | dbldatagen → UC         | `df.write.format("delta")...saveAsTable()`                    |
| **3** streaming | writeStream             | `df.writeStream.format("delta")...toTable()`                  |
| **2/3** saveAsDataset | OutputDataset → path | `spec.saveAsDataset(dataset=OutputDataset(location=...))` |

All UC writes use `.mode("overwrite").option("overwriteSchema", "true")`. See Quick Start sections for full examples.

> **saveAsDataset:** For writing to UC Volume paths or file locations, use `OutputDataset` from `dbldatagen.config`. This writes to a *path* (not a table name). For UC managed tables, continue using `.build()` + `.saveAsTable()`. See [dbldatagen-guide.md](references/dbldatagen-guide.md#outputdataset--saveasdataset) for details.

## Reading Generated Data

| Data Location            | Read With              | Why                                           |
| ------------------------ | ---------------------- | --------------------------------------------- |
| **Local parquet files**  | **Polars**             | Fast, zero-JVM, works without a Spark session |
| **Unity Catalog tables** | **Databricks Connect** | Requires UC access via `DatabricksSession`    |

```python
# Local parquet -> Polars (never use spark.read.parquet on local paths)
import polars as pl
customers = pl.read_parquet("output/retail/customers.parquet")

# Unity Catalog -> Databricks Connect
customers = spark.table("demo.retail.customers")
```

## Code Generation Guidelines

### Polars + NumPy + Mimesis (Tier 1, Tier 1 + UC, and Tier 2 alternative)

- Use `rng = np.random.default_rng(seed)` for all randomness; seed `Generic(seed=N)` for Mimesis
- Use **pool-and-sample** for Mimesis: create ~1K unique values, then `rng.integers()` to sample
- Use `rng.choice(values, size=rows, p=weights/weights.sum())` for weighted categorical columns
- Use `rng.gamma()`, `rng.beta()`, `rng.normal()`, `rng.exponential()` for distributions
- Use `np.datetime64` + `rng.integers().astype("timedelta64[D]")` for dates/timestamps
- Use `pl.when(...).then(None).otherwise(pl.col(...))` for null injection (post-DataFrame)
- Use `pl.format("PREFIX-{}", pl.col(...))` for string formatting, then `.drop()` temp columns
- FK ranges must match parent table ranges
- Use `df.with_columns(...)` for derived columns
- **UC write trigger:** When the user says "save to Unity Catalog", "write to UC", or provides `--catalog`, add the Connect bridge after Polars generation — even for small datasets
- UC write pattern: `spark.createDataFrame(df.to_pandas())` then `.saveAsTable()`
- Always use `.option("overwriteSchema", "true")` when writing to existing UC tables
- For UC writes, always check/create schema before writing: `spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")`

### dbldatagen (Tier 2 — Connect + Serverless)

- Import convention: `import dbldatagen as dg`
- Always set `partitions` explicitly (Connect can't read `defaultParallelism`)
- Use `partitions = max(4, rows // 100_000)` as a guideline
- Timestamps require `"YYYY-MM-DD HH:MM:SS"` format for `begin`/`end`
- Use `.build()` + `.saveAsTable()` for UC managed tables; use `saveAsDataset(OutputDataset(...))` for Volume paths and file locations
- Catalyst-safe features only: `values=`, `weights=`, `minValue`/`maxValue`, `expr=`, `baseColumns=`, `begin`/`end`/`interval`, `percentNulls=`, `omit=True`, `.withIdOutput()`, `random=True`
- Use `omit=True` for intermediate columns
- FK ranges must match parent table ranges (e.g., child `maxValue=customer_count`)
- For UC writes, always check/create schema before writing: `spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")`
- See [dbldatagen-connect-patterns.md](references/dbldatagen-connect-patterns.md) for full reference

### dbldatagen (Tier 3 — notebooks, full feature set)

- Same import convention and partitioning as Tier 2
- Additional features available: `text=mimesisText()`, `distribution=Gamma/Beta/Normal`, `.withConstraint()`, `template=` with UDF patterns
- Use `saveAsDataset(OutputDataset(...))` for declarative output to Volume paths; use `.build()` + `.saveAsTable()` for UC managed tables
- Use Tier 3 when you need these UDF-dependent features or >5M rows
- For UC writes, always check/create schema before writing: `spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")`

## Industry Quick Reference

See [industry-quick-reference.md](references/industry-quick-reference.md) for table summaries across all 9 industries (retail, healthcare, financial, IoT, manufacturing, supply chain, oil & gas, gaming, clinical trials) and `references/industry-patterns/` for complete column-level schemas.

## Multi-Table Generation (Spark)

```python
from dbldatagen import Datasets

ds = Datasets(spark)
customers_df = ds.getTable("multi_table/sales_order", "customers", numCustomers=10000)
orders_df = ds.getTable("multi_table/sales_order", "orders", numOrders=100000)
```

See [dbldatagen-guide.md](references/dbldatagen-guide.md) for all built-in dataset providers.

## Common Issues

See [troubleshooting.md](references/troubleshooting.md) for dependency errors, Connect issues, FK mismatches, and performance guidance.

## Supporting Files

Claude should read these files when deeper context is needed for a user's request.

### Scripts (Reference Implementations)

These are **not importable modules** — Claude reads them for patterns and adapts inline.

| File                                         | When to Read                                                                  |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| `scripts/generators/polars/retail.py`        | Tier 1 retail data (customers, products, transactions, line_items, inventory) |
| `scripts/generators/polars/healthcare.py`    | Tier 1 healthcare data (patients, encounters, claims)                         |
| `scripts/generators/polars/financial.py`     | Tier 1 financial data (accounts, trades, transactions)                        |
| `scripts/generators/polars/iot.py`           | Tier 1 IoT data (devices, sensor_readings, events, telemetry)                 |
| `scripts/generators/polars/manufacturing.py` | Tier 1 manufacturing data (equipment, sensor_data, maintenance_records)       |
| `scripts/generators/polars/cdc.py`           | Tier 1 CDC batch generation for any industry                                  |
| `scripts/generators/retail.py`               | Tier 3 retail data (dbldatagen, notebooks only)                               |
| `scripts/generators/healthcare.py`           | Tier 3 healthcare data (dbldatagen, notebooks only)                           |
| `scripts/generators/financial.py`            | Tier 3 financial data (dbldatagen, notebooks only)                            |
| `scripts/generators/iot.py`                  | Tier 3 IoT data (dbldatagen, notebooks only)                                  |
| `scripts/generators/manufacturing.py`        | Tier 3 manufacturing data (dbldatagen, notebooks only)                        |
| `scripts/generators/supply_chain.py`         | Tier 3 supply chain data — 6 tables (dbldatagen, notebooks only)             |
| `scripts/generators/oil_gas.py`              | Tier 3 oil & gas data — ARPS decline curves (dbldatagen, notebooks only)     |
| `scripts/generators/gaming.py`               | Tier 3 gaming login events — hash-based IDs (dbldatagen, notebooks only)     |
| `scripts/generators/clinical_trials.py`      | Tier 3 clinical trials data — 5 tables (dbldatagen, notebooks only)          |
| `scripts/generators/cdc.py`                  | Tier 3 CDC batch generation (dbldatagen, notebooks only)                      |
| `scripts/utils/mimesis_text.py`              | MimesisText PyfuncTextFactory pattern (**notebook only**)                     |
| `scripts/utils/introspect.py`                | Generate data matching an existing UC table                                   |
| `scripts/utils/output.py`                    | write_delta, write_medallion, write_to_volume patterns                        |
| `scripts/utils/local_output.py`              | Tier 1/2 local file output utilities (parquet/CSV)                            |
| `scripts/utils/uc_setup.py`                  | SDK-based UC provisioning                                                     |

### Reference Documents

| Document                                                                        | When to Read                                                     |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [polars-generation-guide.md](references/polars-generation-guide.md)             | Tier 1 patterns: Polars + Mimesis, distributions, nulls, FKs     |
| [generator-api.md](references/generator-api.md)                                 | Available generators, function signatures, default row counts    |
| [examples.md](references/examples.md)                                           | End-to-end examples (local Polars, Connect, notebook, streaming) |
| [dbldatagen-guide.md](references/dbldatagen-guide.md)                           | Deep dbldatagen API (constraints, distributions, templates)      |
| [mimesis-guide.md](references/mimesis-guide.md)                                 | Mimesis provider reference, locale support, PyfuncTextFactory    |
| [databricks-connect-guide.md](references/databricks-connect-guide.md)           | Connect setup, pure PySpark fallbacks                            |
| [dbldatagen-connect-patterns.md](references/dbldatagen-connect-patterns.md)     | Validated dbldatagen + Connect + serverless patterns             |
| [cdc-patterns.md](references/cdc-patterns.md)                                   | CDC batch generation, Volume landing zones                       |
| [data-quality-patterns.md](references/data-quality-patterns.md)                 | Null injection, duplicates, late-arriving data                   |
| [streaming-patterns.md](references/streaming-patterns.md)                       | Rate sources, withStreaming, checkpoint management               |
| [medallion-patterns.md](references/medallion-patterns.md)                       | Bronze/Silver/Gold with UC Volumes                               |
| [multi-table-patterns.md](references/multi-table-patterns.md)                   | FK consistency, cardinality control                              |
| [seasonality-patterns.md](references/seasonality-patterns.md)                   | Monthly/weekly/campaign time patterns                            |
| [ml-feature-patterns.md](references/ml-feature-patterns.md)                     | Drift simulation, label imbalance, feature arrays                |
| [schema-introspection-patterns.md](references/schema-introspection-patterns.md) | DataAnalyzer workflows                                           |
| [time-series-patterns.md](references/time-series-patterns.md)                   | Temporal data, sine waves, fault injection                       |
| [troubleshooting.md](references/troubleshooting.md)                             | Dependency errors, Connect issues, FK mismatches, performance    |

### Industry Patterns

| Document                                                          | Tables Covered                                           |
| ----------------------------------------------------------------- | -------------------------------------------------------- |
| [retail.md](references/industry-patterns/retail.md)               | customers, products, transactions, line_items, inventory |
| [healthcare.md](references/industry-patterns/healthcare.md)       | patients, encounters, claims + clinical_trials variant (5 additional tables) |
| [financial.md](references/industry-patterns/financial.md)         | accounts, trades, transactions                           |
| [iot.md](references/industry-patterns/iot.md)                     | devices, sensor_readings, events, telemetry              |
| [manufacturing.md](references/industry-patterns/manufacturing.md) | equipment, sensor_data, maintenance_records              |
| [supply_chain.md](references/industry-patterns/supply_chain.md)   | products, distribution_centers, stores, orders, inventory_snapshots, shipments |
| [oil_gas.md](references/industry-patterns/oil_gas.md)             | well_headers, daily_production, type_curves              |
| [gaming.md](references/industry-patterns/gaming.md)               | login_events                                             |


### JSON Schemas

`assets/schemas/` contains 28 JSON schema files (one per table across all 8 industries/variants) documenting column names, types, generation hints, and constraints.
