---
name: databricks-lineage
description: This skill enables exploration of Databricks Unity Catalog data lineage. It should be used when tracing data flow between tables, understanding how data assets are connected, finding upstream data sources or downstream consumers, or investigating column-level data dependencies. Complements the databricks-workspace skill for comprehensive data asset exploration.
---

# Databricks Lineage

## Overview

This skill provides workflows for exploring data lineage in Databricks Unity Catalog. It enables tracing data flow at both table and column levels, discovering how data assets are connected across the organization, and understanding dependencies between tables, notebooks, jobs, pipelines, and dashboards.

Use this skill in conjunction with the `databricks-workspace` skill: first use lineage to discover what assets are related, then use workspace to pull the actual code into context.

## Prerequisites

The Databricks CLI must be installed and configured with authentication. Verify setup by running:

```bash
databricks auth profiles
```

The workspace must have Unity Catalog enabled with lineage tracking active.

## Core Operations

### Getting Table Lineage

To retrieve upstream and downstream dependencies for a table:

```bash
python scripts/get_table_lineage.py <catalog>.<schema>.<table>
```

Options:
- `--direction upstream` - Show only data sources
- `--direction downstream` - Show only consumers
- `--json` - Output raw JSON for programmatic use

Example:

```bash
python scripts/get_table_lineage.py main.sales.orders --direction both
```

Output shows:
- **Upstream**: Tables, notebooks, jobs, or pipelines that write to this table
- **Downstream**: Tables, notebooks, jobs, dashboards, or pipelines that read from this table

### Getting Column Lineage

To trace lineage for a specific column:

```bash
python scripts/get_column_lineage.py <catalog>.<schema>.<table> <column_name>
```

Example:

```bash
python scripts/get_column_lineage.py main.sales.orders total_amount --direction upstream
```

This reveals which source columns contribute to a derived column, useful for:
- Understanding data transformations
- Impact analysis before schema changes
- Debugging data quality issues

### Searching and Exploring Lineage

To search for tables and explore their connections:

```bash
python scripts/search_lineage.py <pattern> [--catalog CATALOG] [--depth N]
```

Example:

```bash
python scripts/search_lineage.py customer --catalog main --depth 2
```

This finds tables matching the pattern and explores their lineage graph to the specified depth.

## Workflow: Understanding Data Asset Usage

When asked to understand how a data asset is used across the organization:

1. **Get table lineage** to see direct connections:
   ```bash
   python scripts/get_table_lineage.py catalog.schema.table_name
   ```

2. **Identify notebooks or jobs** from the lineage output that interact with the table

3. **Use databricks-workspace skill** to pull the code into context:
   ```bash
   databricks workspace export /path/to/notebook --format SOURCE
   ```

4. **For deeper analysis**, trace column lineage to understand transformations:
   ```bash
   python scripts/get_column_lineage.py catalog.schema.table_name column_name
   ```

## Workflow: Impact Analysis

Before making schema changes, assess the impact:

1. **Check downstream consumers**:
   ```bash
   python scripts/get_table_lineage.py catalog.schema.table_name --direction downstream
   ```

2. **For column-level changes**, check column dependencies:
   ```bash
   python scripts/get_column_lineage.py catalog.schema.table_name column_to_modify --direction downstream
   ```

3. **Review each affected asset** by pulling its code with the databricks-workspace skill

## Workflow: Data Discovery

To find how data flows through the organization:

1. **Search for tables** related to a domain:
   ```bash
   python scripts/search_lineage.py sales --depth 2
   ```

2. **Explore the lineage graph** to understand the data pipeline architecture

3. **Pull relevant notebooks/scripts** into context using databricks-workspace to understand the transformations

## Direct API Access

For advanced queries, the lineage API can be accessed directly:

```bash
# Table lineage
databricks api GET "/api/2.0/lineage-tracking/table-lineage?table_name=catalog.schema.table&include_entity_lineage=true"

# Column lineage
databricks api GET "/api/2.0/lineage-tracking/column-lineage?table_name=catalog.schema.table&column_name=column"
```

## Lineage Entity Types

Unity Catalog tracks lineage for these entity types:

| Entity | Description |
|--------|-------------|
| TABLE | Unity Catalog managed or external tables |
| NOTEBOOK | Databricks notebooks that read/write data |
| JOB | Scheduled job runs |
| PIPELINE | Delta Live Tables pipelines |
| DASHBOARD | SQL dashboards that query tables |

## Limitations

- Column lineage requires table references (not path-based access)
- UDFs may obscure column-level mappings
- Renamed objects lose historical lineage
- Lineage data is retained for one year on a rolling basis
