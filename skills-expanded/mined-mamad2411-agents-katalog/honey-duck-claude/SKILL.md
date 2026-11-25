# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Optional: Enable persistent run history (copy .env.example to .env)
cp .env.example .env

# Start Dagster UI (dg CLI - modern replacement for dagster CLI)
uv run dg dev

# With custom port for frontend compatibility
uv run dg dev -p 3003

# Run tests
uv run pytest

# Type checking
uv run ty check src/ cogapp_libs/

# Build docs
uv run mkdocs serve  # Local preview at http://localhost:8000
uv run mkdocs build  # Build static site to site/
```

## dg CLI Commands

```bash
# List all definitions (assets, jobs, resources, etc.)
uv run dg list defs

# Run a specific pipeline
uv run dg launch --job <job_name>

# Available jobs (7 total):
uv run dg launch --job processors_pipeline    # Original processor classes
uv run dg launch --job polars_pipeline        # Pure Polars
uv run dg launch --job duckdb_pipeline        # Pure DuckDB SQL
uv run dg launch --job duckdb_soda_pipeline   # DuckDB + Soda validation
uv run dg launch --job polars_fs_pipeline     # Polars variant
uv run dg launch --job polars_ops_pipeline    # Graph-backed ops
uv run dg launch --job polars_multi_pipeline  # Multi-asset pattern

# Run all pipelines (for testing)
for job in processors_pipeline polars_pipeline duckdb_pipeline duckdb_soda_pipeline polars_fs_pipeline polars_ops_pipeline polars_multi_pipeline; do
  uv run dg launch --job $job
done
```

## Structure

```
src/honey_duck/
├── __init__.py           # Package metadata
├── components/           # Dagster component registry
└── defs/                 # Organized by technology
    ├── definitions.py    # Combined Dagster Definitions (6 jobs)
    ├── harvest/          # dlt ingestion layer
    │   ├── sources.py    # dlt source configuration
    │   └── assets.py     # dagster-dlt asset wrapper
    ├── original/         # Original implementation (processor classes)
    │   └── assets.py     # Transform/output using processor classes
    ├── polars/           # Pure Polars implementations
    │   ├── assets.py     # Split intermediate steps for observability
    │   ├── assets_fs.py  # Variant with different group
    │   ├── assets_ops.py # Graph-backed assets with ops
    │   └── assets_multi.py # Multi-asset pattern
    ├── duckdb/           # Pure DuckDB SQL implementation
    │   └── assets.py     # SQL queries for transforms
    ├── duckdb_soda/      # DuckDB + Soda with column lineage
    │   ├── assets.py     # Cleaner DuckDB patterns + lineage examples
    │   └── checks.py     # Soda data quality checks
    └── shared/           # Shared resources and utilities
        ├── resources.py  # ConfigurableResource classes
        ├── constants.py  # Business constants (thresholds, tiers)
        ├── schemas.py    # Pandera validation schemas
        ├── helpers.py    # STANDARD_HARVEST_DEPS constant
        ├── jobs.py       # Job definitions (6 jobs)
        └── checks.py     # Asset checks (Pandera + quality)

cogapp_libs/              # Utilities (simulates external package)
├── dagster/              # Dagster helpers
│   ├── __init__.py       # Exports write_json_output, track_timing, etc.
│   ├── io.py             # DuckDBPandasPolarsIOManager (unused)
│   ├── helpers.py        # track_timing, add_dataframe_metadata, etc.
│   ├── io_managers.py    # JSONIOManager, ElasticsearchIOManager
│   └── components/       # Dagster Components for YAML config
│       └── elasticsearch.py  # ElasticsearchIOManagerComponent
└── processors/           # DataFrame processors
    ├── pandas/           # PandasReplaceOnConditionProcessor
    ├── polars/           # PolarsFilterProcessor, PolarsStringProcessor
    └── duckdb/           # DuckDBJoinProcessor, DuckDBWindowProcessor

data/
├── input/                # Source CSV files
├── output/               # Final outputs (JSON files per implementation)
├── storage/              # IO manager intermediate storage (Parquet)
└── harvest/              # dlt raw Parquet data + pipeline state

dagster_home/             # Dagster persistence directory
```

## Key Patterns

**Asset graph** (7 parallel implementations sharing harvest layer):

```
                      ┌──→ sales_transform ──→ sales_output (original)
                      ├──→ sales_joined_polars ──→ sales_transform_polars ──→ sales_output_polars
dlt_harvest_* (shared)├──→ sales_transform_duckdb ──→ sales_output_duckdb
                      ├──→ sales_transform_soda ──→ sales_output_soda (with column lineage)
                      ├──→ sales_transform_polars_fs ──→ sales_output_polars_fs
                      ├──→ sales_transform_polars_ops ──→ sales_output_polars_ops
                      └──→ sales_pipeline_multi ──→ sales_output_polars_multi
                      (same pattern for artworks with more intermediate steps in polars)
```

**Implementations** (7 total, ordered by performance):
1. **polars** - Pure Polars with eager DataFrames (polars/assets.py) - fastest
2. **duckdb** - Pure DuckDB SQL queries (duckdb/assets.py) - fastest
3. **duckdb_soda** - DuckDB + Soda with column lineage (duckdb_soda/assets.py) - demonstrates lineage
4. **polars_multi** - Multi-asset pattern for tightly coupled steps (polars/assets_multi.py)
5. **polars_fs** - Polars variant, same logic different group (polars/assets_fs.py)
6. **polars_ops** - Graph-backed assets with ops for detailed observability (polars/assets_ops.py)
7. **original** - Processor classes (original/assets.py) - slowest due to abstraction overhead

**Jobs** (7 total):
- `processors_pipeline` - Original implementation with processor classes
- `polars_pipeline` - Pure Polars with intermediate step assets
- `duckdb_pipeline` - Pure DuckDB SQL
- `duckdb_soda_pipeline` - DuckDB + Soda with column lineage and example values
- `polars_fs_pipeline` - Polars variant
- `polars_ops_pipeline` - Graph-backed assets (ops)
- `polars_multi_pipeline` - Multi-asset pattern

**ConfigurableResource Pattern**:
All path configuration uses Dagster's ConfigurableResource for runtime injection:
- `PathsResource` - harvest_dir, data_dir
- `OutputPathsResource` - output paths per implementation
- `DatabaseResource` - DuckDB database path

**IO Managers**:
- `io_manager` (default): PolarsParquetIOManager - stores Polars DataFrames as Parquet
- `pandas_io_manager`: DuckDBPandasIOManager - stores Pandas DataFrames in DuckDB
- `parquet_path_io_manager`: ParquetPathIOManager - passes file paths (not data) for DuckDB pipelines

**Storage pattern**:
- Harvest layer: dlt writes Parquet to `data/harvest/raw/`
- Transform/output layers: Parquet files in `data/storage/`
- Final outputs: JSON files in `data/output/`
- Pandas pipeline: DuckDB tables (exception, uses pandas_io_manager)

**Output dependency ordering**:
Sales outputs depend on artworks outputs (`deps=["artworks_output_*"]`) to ensure
deterministic asset ordering for consistent JSON output. This is a workaround for
non-deterministic parallel execution in Dagster.

## Adding New Assets

1. Add asset function in appropriate technology folder:
   - `defs/polars/assets.py` for Polars implementations
   - `defs/duckdb/assets.py` for DuckDB implementations
   - `defs/original/assets.py` for processor-based implementations
2. Import `STANDARD_HARVEST_DEPS` from `defs/shared/helpers.py`
3. Decorate with `@dg.asset(kinds={"polars"}, group_name="...", deps=STANDARD_HARVEST_DEPS)`
4. Inject resources: `paths: PathsResource`, `output_paths: OutputPathsResource`
5. Add rich metadata via `context.add_output_metadata()`
6. Add to `definitions.py` assets list

## Adding New dlt Sources

1. Add resource to `defs/harvest/sources.py` honey_duck_source function
2. Asset key will be auto-generated as `dlt_harvest_{name}`
3. Data written to `data/harvest/raw/{name}/`

## Polars Best Practices

**Consolidate `with_columns` chains** - Multiple expressions in a single `with_columns` run in parallel:
```python
# ✅ GOOD - parallel execution
result = df.with_columns(
    pl.col("a").alias("x"),
    pl.col("b").alias("y"),
    pl.col("c").str.to_uppercase(),
)

# ❌ BAD - sequential execution
result = df.with_columns(pl.col("a").alias("x"))
result = result.with_columns(pl.col("b").alias("y"))
```

**Use `sort_by` inside aggregations** - `sort()` before `group_by()` doesn't guarantee order within groups:
```python
# ✅ GOOD - sorted within each group
result = df.group_by("id").agg(
    pl.struct("a", "b").sort_by("a").alias("items")
)

# ❌ BAD - sort order not preserved after group_by
result = df.sort("a").group_by("id").agg(pl.struct("a", "b").alias("items"))
```

**Prefer semi-joins over `is_in()`** - Avoids early materialization:
```python
# ✅ GOOD - stays lazy
result = sales.join(artworks.select("id"), on="id", how="semi")

# ❌ BAD - forces collect of ids
result = sales.filter(pl.col("id").is_in(artworks["id"]))
```

## Visualization Helpers

Add charts and tables to Dagster asset metadata:

```python
from cogapp_libs.dagster import altair_to_metadata, table_preview_to_metadata

# Bar chart (Altair via Polars .plot)
chart = df.plot.bar(x="category", y="count")
context.add_output_metadata(altair_to_metadata(chart, "distribution_chart"))

# Markdown table preview
context.add_output_metadata(
    table_preview_to_metadata(df.head(5), "preview", "Top 5 Results")
)
```

## ParquetPathIOManager

For DuckDB-native pipelines where data never materializes as Python DataFrames, use
`ParquetPathIOManager` to pass file paths between assets instead of data.

```python
from cogapp_libs.dagster import ParquetPathIOManager

# In definitions.py:
defs = dg.Definitions(
    resources={
        "parquet_path_io_manager": ParquetPathIOManager(
            base_dir="data/transforms"
        ),
    },
)
```

**How it works:**
1. Asset writes parquet directly via DuckDB `COPY ... TO` or `.write_parquet()`
2. Asset returns the path string (not a DataFrame)
3. IO manager stores the path in a small `.path` file
4. Downstream asset receives the path string
5. Downstream uses `FROM 'path'` or `read_parquet(path)` in SQL

```python
@dg.asset(io_manager_key="parquet_path_io_manager")
def sales_transform_soda(context, paths, database, sales_raw, ...) -> str:
    output_path = paths.transforms_dir / "sales.parquet"
    with duckdb.connect(database.db_path) as conn:
        # Register views and transform via SQL
        conn.sql("...").write_parquet(str(output_path))
    return str(output_path)  # Return path, not DataFrame

@dg.asset(io_manager_key="parquet_path_io_manager")
def sales_output_soda(context, paths, database, sales_transform_soda: str) -> str:
    # sales_transform_soda is the path string, not data
    with duckdb.connect(database.db_path) as conn:
        result = conn.sql(f"SELECT * FROM '{sales_transform_soda}'")
        # ...process and write output
```

**Benefits:**
- Memory efficient: Data stays in DuckDB, never loads into Python
- Clean SQL: Use `FROM 'path'` instead of registering DataFrames
- Soda compatible: Checks receive paths to validate parquet directly

## Soda Data Quality Checks

The DuckDB+Soda pipeline uses [Soda Core v4](https://docs.soda.io/) for data quality validation.
Soda validates parquet files directly via DuckDB SQL - no data loads into Python memory.

**Installation:**
```bash
pip install -i https://pypi.cloud.soda.io/simple soda-duckdb>=4
```

**Contract YAML files** define expected schema and quality rules:

```yaml
# contracts/sales_transform.yml
dataset: sales_transform
schema:
  - name: sale_id
    data_type: integer
    checks:
      - type: no_missing_values
      - type: no_duplicate_values
  - name: sale_price
    data_type: decimal
    checks:
      - type: no_missing_values
  - name: artist_name
    data_type: varchar
```

**Blocking checks** prevent downstream assets from running if validation fails:

```python
from dagster import asset_check, AssetCheckResult

@dg.asset_check(asset=sales_transform_soda, blocking=True)
def check_sales_transform_soda(
    context: dg.AssetCheckExecutionContext,
    sales_transform_soda: str,  # Receives path from ParquetPathIOManager
) -> dg.AssetCheckResult:
    """Validate against Soda contract. Blocks sales_output_soda if failed."""
    return _run_soda_check_v4(
        parquet_path=sales_transform_soda,
        table_name="sales_transform",
        contract_path=CONTRACTS_DIR / "sales_transform.yml",
        context=context,
    )
```

**How Soda validation works:**
1. Asset check receives parquet path (not data)
2. Creates temp DuckDB data source config pointing to parquet
3. Runs `verify_contract_locally()` - all validation happens in SQL
4. Returns pass/fail with metadata (checks passed/failed, execution time)

**Metadata emitted:**
- `contract`: Contract file name
- `checks_passed`: Number of passing checks
- `checks_failed`: Number of failing checks
- `record_count`: Row count (via DuckDB)
- `execution_time_ms`: Validation duration
- `errors`: Detailed error messages (if any)

## Column Lineage with Example Values

The DuckDB+Soda pipeline (`defs/duckdb_soda/`) demonstrates column-level lineage tracking with
example values, making data flow visible in both Dagster UI and our custom frontend.

### How It Works

Each asset emits two metadata entries:
- `dagster/column_lineage` - Dagster's native column lineage format (shows in UI catalog)
- `lineage_examples` - JSON dict mapping column names to formatted example values

### Defining Column Lineage (DSL)

Use `build_lineage()` for transform assets that join multiple sources:

```python
from cogapp_libs.dagster.lineage import build_lineage, passthrough_lineage
import dagster as dg

SALES_RAW = dg.AssetKey("dlt_harvest_sales_raw")
ARTWORKS_RAW = dg.AssetKey("dlt_harvest_artworks_raw")
ARTISTS_RAW = dg.AssetKey("dlt_harvest_artists_raw")

# Transform: joins multiple sources
SALES_TRANSFORM_LINEAGE = build_lineage(
    passthrough={
        "sale_id": SALES_RAW,
        "artwork_id": SALES_RAW,
        "title": ARTWORKS_RAW,
    },
    rename={
        "artwork_year": (ARTWORKS_RAW, "year"),
        "list_price_usd": (ARTWORKS_RAW, "price_usd"),
    },
    computed={
        "price_diff": [(SALES_RAW, "sale_price_usd"), (ARTWORKS_RAW, "price_usd")],
    },
)

# Output: columns pass through from single source
SALES_OUTPUT_LINEAGE = passthrough_lineage(
    source=dg.AssetKey("sales_transform_soda"),
    columns=["sale_id", "title", "artist_name", "pct_change"],
    renames={"price_difference": "price_diff"},
)
```

### Usage in Assets

Use helper functions for streamlined metadata collection:

```python
from cogapp_libs.dagster.lineage import (
    collect_parquet_metadata,
    collect_json_output_metadata,
    register_harvest_views,
)

@dg.asset(kinds={"duckdb", "parquet"}, group_name="soda", io_manager_key="parquet_path_io_manager")
def sales_transform_soda(context, duckdb, paths, output_paths) -> str:
    start = time.perf_counter()
    output_path = Path(output_paths.transforms_soda_dir) / "sales.parquet"

    with duckdb.get_connection() as conn:
        # Single-line view registration
        register_harvest_views(conn, paths.harvest_dir, ["sales", "artworks", "artists"])
        conn.sql(SALES_TRANSFORM_SQL).write_parquet(str(output_path), compression="zstd")

        # Collect all metadata in one call
        collect_parquet_metadata(
            context, conn, str(output_path),
            lineage=SALES_TRANSFORM_LINEAGE,
            stats_sql=f"SELECT count(*) AS record_count FROM '{output_path}'",
            example_id=("sale_id", 2),
            elapsed_ms=(time.perf_counter() - start) * 1000,
        )

    return str(output_path)

@dg.asset(io_manager_key="parquet_path_io_manager")
def sales_output_soda(context, duckdb, sales_transform_soda: str, output_paths) -> str:
    with duckdb.get_connection() as conn:
        # ... write JSON output ...
        collect_json_output_metadata(
            context, conn,
            input_path=sales_transform_soda,
            output_path=output_paths.sales_soda,
            lineage=SALES_OUTPUT_LINEAGE,
            example_id=("sale_id", 2),
            example_renames={"price_difference": "price_diff"},
            extra_metadata={"record_count": count},
        )
    return sales_transform_soda
```

### Value Formatting

`get_example_row()` automatically formats values for readability:
- Large numbers: `$86,300,000` → `$86.3M`
- Thousands: `$1,500` → `$1.5K`
- Negatives: `-$560,000` → `-$560K`
- Floats: `123.45` → `$123.45`
- Others: Converted to string

### Frontend Integration

The lineage page (`frontend/src/app/lineage/`) fetches examples via GraphQL:

```graphql
query AllLineageQuery {
  assetsOrError {
    ... on AssetConnection {
      nodes {
        assetMaterializations(limit: 1) {
          metadataEntries {
            ... on TableColumnLineageMetadataEntry {
              lineage { columnName, columnDeps { assetKey, columnName } }
            }
            ... on JsonMetadataEntry { jsonString }  # lineage_examples
          }
        }
      }
    }
  }
}
```

The UI shows:
- Asset selector with lineage-enabled assets
- Column table with example values
- Visual lineage diagram: Source → Target → Downstream
- Example values at each step for the same record (e.g., Day Dream sale)

## Known Limitations

**Graph-backed ops** (`defs/polars/assets_ops.py`): Individual ops within a @graph_asset
cannot receive ConfigurableResource injection. These ops use a module-level
`_DEFAULT_HARVEST_DIR` constant. This is a Dagster limitation - ops don't participate
in resource injection the way assets do.

**Op dependency wiring**: Ops that read from harvest files must declare `ins={"_dep": dg.In(Nothing)}`
and receive a Nothing-typed input in the graph to ensure they wait for harvest to complete.
Without this, ops can execute in parallel before their data dependencies exist.
