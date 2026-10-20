---
name: data-platform-orchestrator
description: "Orchestrates the complete lifecycle of a data platform: from database architecture and schema migration to dbt/Dataform transformations, quality validation, and final analysis. Ensures data integrity, cost-optimization, and high-performance pipelines. Keywords: data-platform, data-engineering, dbt, bigquery, dataform, data-quality, spark, database-migration, sql-pro."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# Data Platform Orchestrator - End-to-End Data Engineering

This skill orchestrates the complex sequence of steps required to build, deploy, and maintain a production-grade data platform. It ensures that data moves from source to insight with high integrity, optimized performance, and clear lineage.

## When to Use
Use this skill when building new data pipelines, migrating existing databases, setting up dbt/Dataform transformation layers, or performing deep-dive data analysis on large-scale datasets.

## The Orchestrated Workflow
This skill executes the following phases in sequence:

### Phase 1: Architecture & Schema Design
1. **Database Architecture**: Invoke `database-architect` to define the high-level data layer (SQL/NoSQL selection, normalization strategies).
2. **Schema Design**: Invoke `database-schema-designer` to create specific tables, views, and indexes.
3. **Migration Planning**: Invoke `database-migration` to plan the zero-downtime transition of data from source to target.

### Phase 2: Transformation & Engineering
4. **ETL/ELT Implementation**: Invoke `dbt-bigquery` or `dataform-bigquery` to build the transformation logic.
5. **Spark Optimization**: If dealing with massive scale, invoke `spark-optimization` to tune partitioning and memory.
6. **Notebook Guidance**: Use `notebook-guidance` to structure interactive exploration or prototyping notebooks.

### Phase 3: Quality & Validation
7. **Data Quality Framework**: Invoke `data-quality-frameworks` to establish data contracts and validation rules.
8. **Verification**: Use `sql-pro` to verify the correctness of the output against expected results.

### Phase 4: Analysis & Insights
9. **Data Science Analysis**: Invoke `data-scientist` for advanced statistical modeling and predictive analysis.
10. **Final Review**: Use `notebook-guidance` to structure the final findings into a readable report.

## Freedom Calibration & Constraints
- **Constraint Level: High**
  - **Rigidity**: The order of phases (Architecture -> Engineering -> Quality) is mandatory to prevent "building on sand."
  - **Freedom**: The specific SQL queries, dbt models, and Spark configurations are left to the engineer's judgment within the scope of the chosen architecture.

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** skip quality checks | Deploying data pipelines without automated validation leads to downstream "silent" failures. | Integrate `data-quality-frameworks` into every pipeline. |
| **NEVER** bypass schema design | Creating tables without a formal schema design leads to technical debt and slow queries. | Always start with `database-schema-designer`. |
| **NEVER** ignore cost | Building expensive queries/pipelines without considering BigQuery/Spark costs. | Use `spark-optimization` and `sql-pro` to audit costs. |

## Verification
1. A production-ready database schema is defined and migrated.
2. dbt/Dataform models are implemented and validated.
3. Data quality tests pass for all critical fields.
4. A final analysis report or dashboard is produced.
