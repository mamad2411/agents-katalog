---
name: elementary-data-quality
description: >
  Configure Elementary anomaly detection for dbt on Microsoft Fabric. Use when
  placing data quality tests by medallion layer, setting up volume or column
  anomalies, or configuring timestamp_column. Also use when debugging silent
  test failures or choosing severity levels.
tools: Read, Write, Edit, Glob, Grep, Bash
type: platform
domain: Elementary data observability
version: 1.0.0
---

# Elementary on Fabric -- Practitioner Patterns

Hard-to-find patterns for running Elementary data quality tests on dbt-fabric. Focuses on what Claude consistently gets wrong: the two-component architecture, silent failures from missing `timestamp_column`, test placement by medallion layer, and Fabric compatibility constraints.

## Two-Component Architecture

Elementary has two distinct components. Claude frequently confuses them or assumes they are one thing.

| Component | What it is | How it runs | What it produces |
|---|---|---|---|
| **dbt package** (`elementary-data/elementary`) | dbt tests + macros that collect metrics | `dbt test` / `dbt build` | Results stored in `elementary` schema tables inside your warehouse |
| **`edr` CLI** (`elementary-data/edr`) | Python CLI that reads collected results | `edr report` / `edr send-report` | HTML report, Slack/email alerts |

### Key distinction

- The **dbt package** runs inside your dbt project. It defines test types (`volume_anomalies`, `column_anomalies`, etc.) and writes results to Elementary's internal tables in your warehouse.
- The **`edr` CLI** is a separate Python tool. It reads the results tables and generates reports or sends alerts. It never runs dbt tests itself.

### What this means on Fabric

- `dbt test --select tag:elementary` runs all Elementary tests via the dbt-fabric adapter. Results land in the Elementary schema tables.
- `edr report` connects to your Fabric warehouse (same `profiles.yml`) and reads those tables to generate an HTML report.
- If `edr` fails but `dbt test` works, the problem is in the reporting layer, not your tests.
- If `dbt test` passes but anomalies are not detected, the problem is test configuration (usually missing `timestamp_column`).

### Anti-pattern: installing `edr` when you only need tests

You do not need `edr` installed to run Elementary tests. The dbt package alone handles test execution and result collection. Only install `edr` when you need HTML reports or alert delivery.

## Quick Reference

### Test placement by medallion layer

| Layer | Tests | Why |
|---|---|---|
| **Bronze** (raw ingestion) | `schema_changes_from_baseline`, `volume_anomalies` | Catch upstream schema drift and missing loads before transformation |
| **Silver** (staging/intermediate) | `column_anomalies`, `all_columns_anomalies`, `freshness_anomalies` | Catch data quality issues after initial cleaning |
| **Gold** (marts) | `exposure_schema_validity`, `dimension_anomalies`, `volume_anomalies` | Protect consumer-facing data and BI tool contracts |

### Why this ordering matters

- **Bronze gets schema tests** because upstream sources change without warning. `schema_changes_from_baseline` catches added/removed/retyped columns before they break downstream models.
- **Bronze gets volume tests** because ingestion pipelines (dlt, ADF) can silently produce empty loads. `volume_anomalies` with `fail_on_zero: true` catches these immediately.
- **Silver gets column anomalies** because this is where data is cleaned and typed. Column-level monitors (nulls, distinct count, min/max) catch issues in the cleaned data, not the messy raw data.
- **Gold gets exposure tests** because mart schemas are contracts with BI tools and downstream consumers. `exposure_schema_validity` ensures your exposures match what the models actually produce.

### The `timestamp_column` problem

**This is the single most common Elementary misconfiguration.** Without `timestamp_column`, anomaly detection tests still run and pass, but they compare total table metrics instead of time-bucketed metrics. This means:

- Anomalies are detected only when the cumulative total drifts, which may take days or weeks
- Recent spikes or drops are averaged out by historical data
- The test appears to work but provides almost no value

**Always set `timestamp_column`** at the model level for any model with anomaly detection tests:

```yaml
models:
  - name: stg_stripe__payments
    config:
      elementary:
        timestamp_column: "created_at"
    tests:
      - elementary.volume_anomalies
      - elementary.freshness_anomalies
    columns:
      - name: amount
        tests:
          - elementary.column_anomalies:
              column_anomalies:
                - zero_count
                - null_count
```

**How to identify the right `timestamp_column`:**
- Use the column that represents when the row was created or last updated
- For event tables: the event timestamp (`event_at`, `created_at`)
- For dimension tables: the last modified timestamp (`updated_at`, `modified_at`)
- For tables with no natural timestamp: use `_dlt_load_id` (if loaded via dlt) or consider whether anomaly detection is appropriate at all

### Debugging silent anomaly detection failures

When `dbt test` passes but anomalies go undetected:

1. **Check `timestamp_column`** -- missing = comparing totals, not time buckets
2. **Check `training_period`** -- default is 14 days. If your table has less than 14 days of data, every bucket looks anomalous (or none do). Set `training_period` to match your data history.
3. **Check `time_bucket`** -- default is daily. Hourly data with daily buckets smooths out intra-day anomalies. Weekly patterns need `seasonality: day_of_week`.
4. **Check `anomaly_sensitivity`** -- default is 3 (standard deviations). Lower to 2 for stricter detection. Raise to 4 if too many false positives.
5. **Check the Elementary results tables** -- query `elementary_test_results` in your warehouse to see what metrics were collected and what thresholds were computed.

## Severity Progression Strategy

### Start with `warn`, promote to `error`

New anomaly detection tests should always start with `severity: warn`:

```yaml
tests:
  - elementary.volume_anomalies:
      timestamp_column: "created_at"
      config:
        severity: warn
```

**Why:**
- Anomaly tests need a baseline period (training data) to establish normal ranges
- During the first 1-2 weeks, the model is learning what "normal" looks like
- `severity: error` during this period causes `dbt build` failures on legitimate data
- `severity: warn` logs the anomaly without failing the DAG

**Promotion timeline:**
1. **Week 0**: Deploy with `severity: warn`. Run `dbt build` daily.
2. **Week 1-2**: Review warnings in Elementary report (`edr report`). Tune `anomaly_sensitivity` if too noisy.
3. **Week 2+**: Promote to `severity: error` for tests that have stable baselines.

### Exception: `fail_on_zero`

`volume_anomalies` with `fail_on_zero: true` should use `severity: error` from day one. A table with zero rows is always wrong -- no baseline needed:

```yaml
tests:
  - elementary.volume_anomalies:
      fail_on_zero: true
      config:
        severity: error
```

## Volume Anomalies -- Deep Patterns

### `fail_on_zero` for critical tables

Tables that should never be empty (active customer tables, daily fact tables, reference dimensions):

```yaml
models:
  - name: fct_daily_orders
    config:
      elementary:
        timestamp_column: "order_date"
    tests:
      - elementary.volume_anomalies:
          fail_on_zero: true
          anomaly_direction: drop  # only alert on fewer rows, not more
          config:
            severity: error
```

### Spike vs drop detection

By default, `anomaly_direction: both` alerts on unusual increases AND decreases. Override when you have asymmetric concerns:

- **`drop`** for tables where fewer rows = problem (transaction tables, event logs)
- **`spike`** for tables where sudden growth = problem (error logs, staging tables that should be stable)
- **`both`** for tables where any volume change is suspicious (reference/dimension tables)

### Training and detection periods on Fabric

Fabric data warehouses often have less historical data than Snowflake/BigQuery (newer platform, smaller retention windows). Adjust accordingly:

```yaml
tests:
  - elementary.volume_anomalies:
      timestamp_column: "loaded_at"
      training_period:
        period: day
        count: 21  # 3 weeks, not the default 14 days
      detection_period:
        period: day
        count: 2   # check last 2 days
      time_bucket:
        period: day
        count: 1
```

## Column Anomalies -- Choosing Monitors

### Default monitors vs explicit selection

If you omit `column_anomalies`, Elementary runs ALL default monitors for the column type. This is noisy and slow. **Always specify monitors explicitly:**

```yaml
columns:
  - name: email
    tests:
      - elementary.column_anomalies:
          column_anomalies:
            - missing_count
            - missing_percent
          timestamp_column: "created_at"
  - name: revenue
    tests:
      - elementary.column_anomalies:
          column_anomalies:
            - min
            - max
            - zero_count
          timestamp_column: "transaction_date"
```

### Monitor selection by column type

| Column type | Recommended monitors | Why |
|---|---|---|
| String (names, emails) | `missing_count`, `min_length`, `max_length` | Catch null injection and truncation |
| Numeric (amounts, counts) | `min`, `max`, `zero_count`, `null_count` | Catch out-of-range values and unexpected zeros |
| Categorical (status, type) | `null_count`, `distinct_count` | Catch new/dropped categories |
| Date/timestamp | `null_count` via `freshness_anomalies` | Catch missing timestamps; use `freshness_anomalies` instead of `column_anomalies` for dates |
| ID columns | `null_count`, `distinct_count` | Catch deduplication failures |

### `all_columns_anomalies` -- when to use

Use `all_columns_anomalies` only on silver models with <20 columns. It runs default monitors on every column, which is:
- Expensive on wide tables (Fabric compute cost adds up)
- Noisy on columns with legitimate variability
- Useful as a broad sweep when you don't yet know which columns matter

For production gold models, always use targeted `column_anomalies` with explicit monitor lists.

## Schema Tests

### `schema_changes_from_baseline` -- the bronze guardian

This test compares the current table schema against a baseline defined in your YAML. **Critical for bronze tables** where upstream sources can change without warning:

```yaml
models:
  - name: raw_stripe_payments
    columns:
      - name: id
        data_type: varchar
      - name: amount
        data_type: decimal
      - name: currency
        data_type: varchar
      - name: created_at
        data_type: datetime2
      - name: status
        data_type: varchar
    tests:
      - elementary.schema_changes_from_baseline:
          fail_on_added: true    # new columns = potential PII leak
          enforce_types: true    # type changes = downstream cast failures
          config:
            severity: error      # schema drift is always an error
```

### Fabric data type mapping

When defining baseline columns, use Fabric/T-SQL data types:

| Common type | Fabric type | Note |
|---|---|---|
| String | `varchar` or `nvarchar` | Fabric often uses `varchar(max)` |
| Integer | `int` or `bigint` | |
| Decimal | `decimal(p,s)` | Specify precision and scale |
| Timestamp | `datetime2` | Not `timestamp` (which is a row version type in T-SQL) |
| Boolean | `bit` | T-SQL has no native boolean |
| Date | `date` | |

### `exposure_schema_validity` -- protecting BI contracts

Place on gold models that feed BI tools:

```yaml
models:
  - name: fct_weekly_revenue
    tests:
      - elementary.exposure_schema_validity:
          config:
            severity: error
```

This test requires exposures to be defined in your dbt project. It validates that the model's actual schema matches what the exposure declares. If a column is renamed or dropped, this test fails before the BI dashboard breaks.

## Fabric Compatibility

### No official Elementary adapter for Fabric

Elementary does not ship a Fabric-specific adapter. It works on Fabric through the dbt-fabric adapter's compatibility with standard dbt test interfaces and the tsql-utils package.

**What works:**
- All Elementary test types (anomaly, schema, volume) run via `dbt test`
- Results are stored in Elementary's internal tables (created by `dbt run --select elementary`)
- `edr` CLI can connect to Fabric warehouse to generate reports

**What to watch for:**
- Elementary's internal macros may generate SQL that assumes Postgres/Snowflake functions. If a test fails with a SQL syntax error, check the generated SQL in `target/compiled/` for non-T-SQL syntax.
- `datetime2` precision differences: Fabric uses `datetime2(6)` by default. Elementary's time bucketing works with this, but custom `where_expression` filters that compare timestamps may need explicit `CAST`.
- Elementary's `freshness_anomalies` uses `DATEDIFF` internally. On Fabric, this works natively (T-SQL has `DATEDIFF`), but the date part names must match T-SQL conventions.

### Required packages

```yaml
# packages.yml
packages:
  - package: elementary-data/elementary
    version: [">=0.16.0", "<0.17.0"]
  - package: dbt-msft/tsql_utils
    version: [">=0.10.0", "<0.11.0"]
```

After adding the elementary package:
```bash
dbt deps
dbt run --select elementary  # creates Elementary internal tables
dbt test --select tag:elementary  # runs Elementary tests
```

### Project configuration

```yaml
# dbt_project.yml
models:
  elementary:
    +schema: "elementary"  # isolate Elementary tables in their own schema
```

## Anti-Patterns

What Claude consistently gets wrong with Elementary on Fabric:

- **Missing `timestamp_column`** -- anomaly tests pass but detect nothing useful. Always set it.
- **Confusing dbt package with `edr` CLI** -- "install Elementary" can mean two different things. The dbt package is for tests; `edr` is for reports.
- **Running all default monitors** -- omitting `column_anomalies` parameter runs all monitors on the column. This is slow and noisy. Be explicit.
- **`severity: error` on day one** -- new anomaly tests have no baseline. They will fail on legitimate data during the training period.
- **Wrong test at wrong layer** -- `schema_changes_from_baseline` on gold is overkill (you control the schema). `column_anomalies` on bronze is noisy (raw data is messy by nature).
- **Assuming Elementary handles alerting** -- the dbt package only collects results. You need `edr` or a separate process to generate reports and send alerts.
- **Using `timestamp` type in schema baseline** -- on Fabric, `timestamp` is a row version type, not a datetime. Use `datetime2`.
- **Not running `dbt run --select elementary` first** -- Elementary needs its internal tables created before tests can store results. This is a one-time setup step that Claude often omits.

## Reference Files

For deeper guidance on specific patterns:

- **[references/test-catalog.md](references/test-catalog.md)** -- Full test type catalog with configuration examples, parameters, and Fabric-specific notes for every Elementary test type.
- **[references/layer-strategy.md](references/layer-strategy.md)** -- Detailed test placement strategy by medallion layer with complete YAML examples for bronze, silver, and gold models.
- **[references/evaluations.md](references/evaluations.md)** -- Evaluation scenarios for testing whether the skill produces correct Elementary guidance.
