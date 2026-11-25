---
name: spark-lineage
description: >-
  Preserves connected OpenLineage for oleander Spark jobs by avoiding
  collect()/toPandas() between read and write, and using env vars for
  runtime config. Use when lineage looks disconnected, jobs split after
  collect(), or rewriting Spark pipelines for continuous lineage.
---

# oleander Spark Lineage

Use this skill when Spark lineage in oleander looks disconnected or when rewriting Spark jobs to preserve connected lineage.

## Lineage context

Key behavior from oleander Spark/OpenLineage integrations:

- `collect()` is a Spark action that materializes data into driver memory.
- After `collect()`, execution is regular Python in-memory logic, not distributed Spark DataFrame execution.
- Spark can treat "read + collect" and "write from memory" as separate jobs.
- The OpenLineage Spark integration may not connect those phases as one continuous lineage path.

## Recommended lineage-safe pattern

Prefer this shape for connected lineage:

1. `df = spark.table(...)`
2. chain DataFrame transforms (`select`, `withColumn`, `join`, aggregate)
3. finalize with `df.write(...)`

If `collect()` is required, keep it for small side-effects or reporting, not as the core bridge between read and write.

## Rewrite checklist

When fixing lineage gaps:

1. Find points where data leaves Spark (`collect`, `toPandas`, driver loops).
2. Move transformation logic back into DataFrame expressions whenever possible.
3. Keep read-transform-write in one Spark flow.
4. Ensure final writes are Spark writes (`df.write...`), not Python-memory writes.
5. Re-run and confirm lineage graph connectivity and Spark job boundaries.

## Environment variables

Use env vars for runtime configuration, not transformation logic.

- Provide safe defaults: `os.getenv("VAR", "default")`
- Validate required env vars at startup and fail early with clear errors.
- Keep env-driven behavior small and explicit (names, toggles, destinations).

Example pattern:

```python
import os

job_name = os.getenv("NAME", "default-service")
output_catalog = os.getenv("OUTPUT_CATALOG", "oleander.sf")
```
