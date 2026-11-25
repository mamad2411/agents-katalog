---
name: lake-catalog
description: >-
  Engine-agnostic oleander lake catalog conventions: catalog.namespace.table
  naming, hierarchy, and catalog-qualified reads/writes without raw storage
  paths. Use when naming tables, choosing namespaces, or referencing the
  lake catalog from Spark, Polars, SQL, or another engine.
---

# oleander Lake Catalog

Use this skill when reading from or writing to the oleander lake catalog from Spark, Polars, SQL, or another engine.

## Catalog hierarchy

Tables are addressed as `catalog.namespace.table`:

- **catalog**: always `oleander` for the managed Lakekeeper-backed catalog
- **namespace**: a logical grouping (e.g., `default`, `san_francisco`, `my_org`)
- **table**: the table name

By default, `default` and `telemetry` namespaces are available out of the box. The `telemetry` namespace contains oleander-managed data you can query directly (for example `oleander.telemetry.run_events`, `oleander.telemetry.traces`, and `oleander.telemetry.logs`).

These tables are partitioned on their time column and are reachable over MCP with `query_run` — see the `lake-query` skill.

Examples:

```bash
oleander.default.sf_311
oleander.san_francisco.district_stats
oleander.my_namespace.results
```

## Referencing tables

Always use fully qualified table names through the engine's catalog integration. Do not build raw storage paths such as S3 URIs when reading or writing Iceberg tables.

Good patterns:

- read `oleander.default.sf_311` through your engine's catalog-aware table API
- write results to `oleander.my_namespace.results`

Avoid:

- hardcoding storage locations like `s3://.../warehouse/...`
- bypassing the catalog when the engine supports catalog-qualified reads and writes

Using the catalog name keeps Iceberg metadata, lineage, and table semantics consistent across engines.

## Engine-specific read/write syntax

This skill defines the shared catalog rules. Engine-specific syntax and operational advice should live in engine-specific skills.

Use companion skills when available:

- Spark: see `spark-lake-catalog` for `spark.table(...)`, write modes, and caching guidance
- Other engines: keep the same table naming and catalog-reference rules, but use that engine's native API

## Namespace conventions

- Use lowercase, underscore-separated names for namespaces and tables.
- Keep the namespace tied to the domain or data source, not the job name.
- Avoid deeply nested namespaces; one level is usually sufficient.

## Portability checklist

- Use `catalog.namespace.table` names everywhere user input, docs, and examples refer to tables.
- Pass table names as configuration when practical so jobs are reusable across namespaces.
- Keep engine-specific read/write code separate from shared catalog conventions.
