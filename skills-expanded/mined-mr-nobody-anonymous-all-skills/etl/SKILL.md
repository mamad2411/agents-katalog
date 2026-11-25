---
name: etl
description: "Extract, Transform, Load architecture, batch extraction, schema validation, idempotent upserts, and dead-letter queues"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/etl/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# ETL Pipeline Architecture

## Scope
ETL (Extract, Transform, Load) pipelines extract raw operational data from disparate sources, transform it according to business and analytical logic, and load clean tabular structures into target warehouses.

## Architectural Principles & Invariants
- **Idempotency & Replayability**: Every pipeline run for a given time partition $[t_1, t_2]$ must yield identical state, regardless of rerun count. Implement via staging tables and atomic swaps:
  ```sql
  MERGE INTO analytics.fact_orders t
  USING staging.orders_stg s ON t.order_id = s.order_id
  WHEN MATCHED THEN UPDATE SET ...
  WHEN NOT MATCHED THEN INSERT ...;
  ```
- **Schema Validation & Dead-Letter Queues (DLQ)**: Malformed rows failing type casting or schema contracts are directed to quarantine dead-letter sinks without halting pipeline execution.
- **Incremental Extraction (CDC / Watermarking)**: Querying source tables using high-watermark timestamps: `WHERE updated_at > :last_watermark`.

## Tools & Standards
- **Tools**: Apache Airflow, dbt, Apache Spark, Singer, Airbyte.
