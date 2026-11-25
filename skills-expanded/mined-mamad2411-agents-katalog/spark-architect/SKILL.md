---
name: spark-architect
description: Expert guidance for developing PySpark jobs in the flights-analytics-prod project. Use when creating or modifying Bronze-to-Silver or Silver-to-Gold Spark jobs to ensure compliance with partitioning and logging standards.
---

# Spark Architect Skill

This skill ensures all PySpark jobs follow the `flights-analytics-prod` standards for Dataproc optimization, partitioning, and error handling.

## Core Workflows

### 1. Job Scaffolding
Every new job **MUST** use the standard `get_spark_session()` and logging configuration.
- **Reference**: Use [pyspark-template.py](assets/pyspark-template.py) for the basic structure.

### 2. Standard References
Refer to these for specific implementation details:
- **Global Standards**: [global-standards.md](references/global-standards.md) (Naming, logging, constants)
- **Optimization**: [optimization.md](references/optimization.md) (Partitioning, file sizing, session configuration)

### 3. Data Lake Lifecycle
- **Bronze -> Silver**: Enforce schema (Parquet), deduplicate, and write to `gs://flights-silver-flights-analytics-prod`.
- **Silver -> Gold**: Business aggregates, enrichments, and write to `gs://flights-gold-flights-analytics-prod`.

## Quality Standards
- **Repartitioning**: Data **must** be repartitioned before writing to GCS to avoid small files.
- **Column Naming**: All columns **must** be `snake_case`.
- **Error Handling**: Use `try...except` and log exceptions with `exc_info=True`.
- **Immutability**: Transformation steps **must** create new DataFrames.
