---
name: fabric-cli-lakehouse
description: Fabric CLI lakehouse operations — create lakehouses, inspect table schemas, load data into tables, optimize and vacuum tables, and run table maintenance jobs. Use when working with .Lakehouse items and Delta tables via the fab CLI.
allowed-tools: "Bash(uv run *), Bash(fab *), Bash(cat *), Bash(grep *), Read, Write, Edit, Glob"
user-invocable: false
metadata:
  author: accelerate-data
---

# Fabric CLI — Lakehouse & Table Operations

Complete reference for managing lakehouses and Delta tables via `fab` CLI.

## Execution Pattern

```bash
uv run --env-file .env fab <command>
```

## Lakehouse Management

### List Lakehouses

```bash
# All items in workspace
uv run --env-file .env fab ls ws1.Workspace

# Detailed
uv run --env-file .env fab ls ws1.Workspace -l
```

### Create a Lakehouse

```bash
# Basic
uv run --env-file .env fab create ws1.Workspace/lh1.Lakehouse

# With schema support enabled
uv run --env-file .env fab create ws1.Workspace/lh1.Lakehouse -P enableSchemas=true
```

### Check Existence

```bash
uv run --env-file .env fab exists ws1.Workspace/lh1.Lakehouse
```

### Get Lakehouse Details

```bash
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse -v
```

### Delete a Lakehouse

```bash
uv run --env-file .env fab rm ws1.Workspace/lh1.Lakehouse -f
```

## Table Schema Inspection

Inspect the schema of Delta tables within a lakehouse:

```bash
# Must specify the full path to a specific table (not just the schema)
uv run --env-file .env fab table schema ws1.Workspace/lh1.Lakehouse/Tables/dbo/customer_data
```

> **Note:** You must point to a specific table, not just the schema directory. `fab table schema .../Tables/dbo` will fail — use `fab table schema .../Tables/dbo/table_name`.

**Supported item types for schema inspection:**

| Type | Extension |
|------|-----------|
| Lakehouse | `.Lakehouse` |
| Warehouse | `.Warehouse` |
| Mirrored Database | `.MirroredDatabase` |
| SQL Database | `.SQLDatabase` |
| Semantic Model | `.SemanticModel` (requires enablement) |
| KQL Database | `.KQLDatabase` (requires enablement) |

### List Tables

```bash
# List tables in a lakehouse
uv run --env-file .env fab ls ws1.Workspace/lh1.Lakehouse/Tables

# List tables in a specific schema
uv run --env-file .env fab ls ws1.Workspace/lh1.Lakehouse/Tables/dbo

# List warehouse tables
uv run --env-file .env fab ls ws1.Workspace/wh1.Warehouse/Tables/dbo
```

## Load Data into Tables

Load CSV or Parquet files from OneLake into Delta tables.

> **Note:** `table load` is **not supported in schema-enabled Lakehouses** (created with `-P enableSchemas=true`).

### CSV Loading

```bash
# Load from a folder of CSVs
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/customer_data --file ws1.Workspace/lh1.Lakehouse/Files/csv/customers

# Load a single CSV (append mode)
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/sales_data --file ws1.Workspace/lh1.Lakehouse/Files/csv/daily_sales.csv --mode append

# Custom CSV format (no header, semicolon delimiter)
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/product_catalog --file ws1.Workspace/lh1.Lakehouse/Files/custom_csv --format "format=csv,header=false,delimiter=';'"
```

### Parquet Loading

```bash
# Load from a folder of Parquet files
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/analytics_data --file ws1.Workspace/lh1.Lakehouse/Files/parquet/events --format format=parquet --mode append

# With extension filter
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/processed_data --file ws1.Workspace/lh1.Lakehouse/Files/parquet/processed --format format=parquet --extension '.parquet'
```

### Load Flags

| Flag | Purpose | Values |
|------|---------|--------|
| `--file` | Source file/folder path in OneLake | OneLake path |
| `--mode` | Write mode | `overwrite` (default), `append` |
| `--format` | File format specification | `format=csv`, `format=parquet` + options |
| `--extension` | Filter source files by extension | `.csv`, `.parquet` |

### CSV Format Options

| Option | Purpose | Example |
|--------|---------|---------|
| `format` | File format | `csv` |
| `header` | Has header row | `true`, `false` |
| `delimiter` | Column separator | `,`, `;`, `\t` |

## Table Optimization

Optimize Delta table file layout for query performance:

```bash
# Basic optimization (compacts small files)
uv run --env-file .env fab table optimize ws1.Workspace/lh1.Lakehouse/Tables/sales_data

# With V-Order and Z-Order indexing
uv run --env-file .env fab table optimize ws1.Workspace/lh1.Lakehouse/Tables/customer_transactions --vorder --zorder customer_id,transaction_date
```

### Optimization Flags

| Flag | Purpose |
|------|---------|
| `--vorder` | Apply V-Order optimization (Fabric-specific, improves read performance) |
| `--zorder` | Apply Z-Order indexing on specified columns (comma-separated) |

## Table Vacuum

Remove old files no longer referenced by the Delta log:

```bash
# Default vacuum (7-day retention)
uv run --env-file .env fab table vacuum ws1.Workspace/lh1.Lakehouse/Tables/transaction_history

# Custom retention (48 hours)
uv run --env-file .env fab table vacuum ws1.Workspace/lh1.Lakehouse/Tables/temp_processing_data --retain_n_hours 48
```

### Vacuum Flags

| Flag | Purpose | Default |
|------|---------|---------|
| `--retain_n_hours` | Retention period in hours | 168 (7 days) |

## Table Maintenance via Jobs

Run table maintenance as background jobs:

```bash
# Optimize via job
uv run --env-file .env fab job run ws1.Workspace/lh1.Lakehouse -i '{"tableName": "orders", "optimizeSettings": {"vOrder": true, "zOrderBy": ["account_id"]}}'

# Vacuum via job
uv run --env-file .env fab job run ws1.Workspace/lh1.Lakehouse -i '{"tableName": "orders", "vacuumSettings": {"retentionPeriod": "7.01:00:00"}}'
```

**Job input JSON formats:**

Optimize:
```json
{
  "tableName": "orders",
  "optimizeSettings": {
    "vOrder": true,
    "zOrderBy": ["account_id", "order_date"]
  }
}
```

Vacuum:
```json
{
  "tableName": "orders",
  "vacuumSettings": {
    "retentionPeriod": "7.01:00:00"
  }
}
```

## Table Help

```bash
uv run --env-file .env fab table -h
```

## Query Lakehouse Tables via SQL Endpoint

The `fab` CLI does not have a built-in SQL query command. To query lakehouse tables, use `pyodbc` with Azure AD token auth against the SQL endpoint:

```bash
# Environment variables needed
LAKEHOUSE_SQL_ENDPOINT=your-endpoint.datawarehouse.fabric.microsoft.com
LAKEHOUSE_DATABASE=your_lakehouse
```

Use a helper script with `pyodbc` for token-based auth. Note: `sqlcmd` ODBC does not support token auth properly (throws "Argument too long" for tokens > 128 chars).

## Practical Tips

- **Get lakehouse ID:** `uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse -f -q "id"`
- **Describe available commands:** `uv run --env-file .env fab desc .Lakehouse` shows all supported operations (includes `table load`, `table optimize`, `table schema`, `table vacuum`, `job run`, etc.)
- **Lakehouse does NOT support:** `cp`, `export`, `import` at the item level (use OneLake paths for file operations within the lakehouse)

## Direct API Access

For advanced operations not covered by CLI commands:

```bash
# List lakehouses via REST API
uv run --env-file .env fab api -X get workspaces/<workspace-id>/lakehouses

# Create lakehouse via REST API
uv run --env-file .env fab api -X post workspaces/<workspace-id>/lakehouses -i '{"displayName": "my_lakehouse"}'

# List OneLake files via storage API
uv run --env-file .env fab api -A storage ws1.Workspace/lh1.Lakehouse/Files?resource=filesystem&recursive=false

# Get ACL permissions on OneLake paths
uv run --env-file .env fab acl ls ws1.Workspace/lh1.Lakehouse/Files
```

## Common Patterns

### Load CSV then verify

```bash
# Upload CSV to OneLake
uv run --env-file .env fab cp ./data/customers.csv ws1.Workspace/lh1.Lakehouse/Files/csv/customers.csv

# Load into table
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/customers --file ws1.Workspace/lh1.Lakehouse/Files/csv/customers.csv

# Verify schema
uv run --env-file .env fab table schema ws1.Workspace/lh1.Lakehouse/Tables/dbo/customers
```

### Optimize after bulk load

```bash
# Load data
uv run --env-file .env fab table load ws1.Workspace/lh1.Lakehouse/Tables/events --file ws1.Workspace/lh1.Lakehouse/Files/parquet/events --format format=parquet --mode append

# Optimize for query performance
uv run --env-file .env fab table optimize ws1.Workspace/lh1.Lakehouse/Tables/events --vorder --zorder event_date
```

## Common Issues

| Issue | Fix |
|-------|-----|
| `table schema` returns nothing | Table may not exist yet — load data first |
| Load fails with format error | Ensure `--format` uses `key=value` pairs: `format=csv,header=true` |
| Vacuum removes too much | Increase `--retain_n_hours` (default is 168 = 7 days) |
| Z-Order columns invalid | Columns must exist in the table schema |
| Permission denied on table ops | Verify `FAB_TOKEN` has write access to the lakehouse |
| Schema not visible | Ensure lakehouse has `enableSchemas=true` if using custom schemas |
