---
name: data-pipeline
description: >
  Design, build, and debug data pipelines for ETL/ELT, data ingestion, transformation, and orchestration.
  TRIGGER when: user asks to "build a pipeline", "ETL", "ELT", "data ingestion", "data transformation",
  "orchestrate data", "airflow DAG", "dbt model", "data workflow", "batch processing",
  "streaming pipeline", or "move data from X to Y".
argument-hint: "<source> <destination> [transform_description]"
user-invocable: true
---

# Data Pipeline Builder

You are an expert data engineer. When the user asks you to design, build, or debug a data pipeline, follow this structured process.

## Step 1: Requirements Analysis

| Requirement | Options | Impact |
|-------------|---------|--------|
| Volume | MB, GB, TB, PB | Technology and architecture choice |
| Velocity | Batch (hourly/daily), micro-batch (minutes), real-time (seconds) | Processing framework |
| Variety | Structured, semi-structured, unstructured | Schema handling approach |
| Source(s) | Database, API, file, stream, SaaS | Connector/extractor choice |
| Destination | Data warehouse, data lake, database, API | Loader choice |
| Frequency | One-time, scheduled, event-driven | Orchestration approach |
| Latency SLA | Minutes, hours, next day | Architecture pattern |
| Idempotency | Must be re-runnable without side effects | Design constraint |

## Step 2: Architecture Patterns

### ETL (Extract, Transform, Load)

```
Source --> Extract --> Transform (staging) --> Load --> Destination
```
- Transform happens before loading
- Good for: clean data requirements, limited warehouse compute
- Tools: Python scripts, Spark, custom code

### ELT (Extract, Load, Transform)

```
Source --> Extract --> Load (raw) --> Transform (in warehouse) --> Curated layer
```
- Load raw data first, transform in the warehouse
- Good for: cloud warehouses with cheap compute (BigQuery, Snowflake, Redshift)
- Tools: Fivetran/Airbyte (EL) + dbt (T)

### Streaming

```
Source --> Message Broker --> Stream Processor --> Sink
```
- Continuous processing of events
- Good for: real-time dashboards, alerts, event-driven systems
- Tools: Kafka, Flink, Spark Streaming, Kinesis

### Data Lakehouse

```
Source --> Ingestion --> Bronze (raw) --> Silver (cleaned) --> Gold (aggregated)
```
- Medallion architecture with increasing quality layers
- Good for: mixed workloads (BI + ML), large-scale data
- Tools: Delta Lake, Iceberg, Hudi on Spark/Databricks

## Step 3: Component Design

### Extract Layer

| Source Type | Method | Considerations |
|------------|--------|----------------|
| SQL Database | Full load or CDC (Change Data Capture) | CDC for large tables; use watermark columns |
| REST API | Pagination, rate limiting, retry | Handle 429s, implement exponential backoff |
| Files (S3/GCS) | List + read, event-driven (S3 notification) | Handle late-arriving files |
| Streaming | Consumer group, offset management | At-least-once vs exactly-once semantics |
| SaaS tools | Official connectors (Fivetran, Airbyte) | Check API limits and sync frequency |

### Transform Layer

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| Cleaning | Always | NULL handling, type casting, dedup |
| Filtering | Subset of data needed | WHERE clauses, row-level logic |
| Joining | Enrich with reference data | Lookup tables, dimension joins |
| Aggregation | Summary metrics needed | GROUP BY, window functions |
| Pivoting | Reshape data structure | PIVOT/UNPIVOT, melt/pivot |
| Derivation | Computed columns | Business logic, formulas |
| Validation | Quality gates | Schema checks, range checks, referential integrity |

### Load Layer

| Strategy | Description | Use When |
|----------|-------------|----------|
| Full replace | DROP + recreate | Small tables, no history needed |
| Append | INSERT new rows | Event/log data, immutable records |
| Upsert (MERGE) | INSERT or UPDATE by key | Dimension tables, mutable entities |
| SCD Type 2 | Track historical changes | Need full audit history |
| Partition overwrite | Replace specific partitions | Time-partitioned fact tables |

## Step 4: Orchestration

### DAG Design Principles

```python
# Airflow DAG skeleton
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}

with DAG(
    dag_id="pipeline_name",
    schedule_interval="0 6 * * *",  # Daily at 6 AM UTC
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["production"],
    default_args=default_args,
) as dag:

    extract = PythonOperator(task_id="extract", python_callable=extract_fn)
    transform = PythonOperator(task_id="transform", python_callable=transform_fn)
    validate = PythonOperator(task_id="validate", python_callable=validate_fn)
    load = PythonOperator(task_id="load", python_callable=load_fn)

    extract >> transform >> validate >> load
```

### Orchestration Best Practices

- **Idempotent tasks**: Every task produces the same result if re-run
- **Atomic operations**: Each task either fully succeeds or fully fails
- **Small tasks**: Prefer many small tasks over few large monoliths
- **Parameterized dates**: Use execution_date, never `datetime.now()`
- **Failure handling**: Alert on failure, retry with backoff, skip non-critical tasks
- **Dependency management**: Explicit upstream/downstream; use sensors for external deps

## Step 5: Data Quality Gates

Build quality checks into the pipeline:

| Check | When | Action on Failure |
|-------|------|-------------------|
| Schema validation | After extract | Fail pipeline, alert |
| Row count threshold | After extract | Warn if < expected, fail if zero |
| Null percentage | After transform | Fail if exceeds threshold |
| Uniqueness on keys | Before load | Fail, investigate duplicates |
| Referential integrity | Before load | Warn or fail based on severity |
| Freshness check | After load | Alert if data is stale |
| Value range checks | After transform | Flag anomalous records |
| Reconciliation | After load | Compare source vs destination counts |

### dbt Tests Example

```yaml
# schema.yml
models:
  - name: orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
      - name: customer_id
        tests:
          - relationships:
              to: ref('customers')
              field: customer_id
```

## Step 6: Error Handling and Monitoring

### Error Handling Patterns

- **Dead letter queue**: Route failed records to a separate table for investigation
- **Circuit breaker**: Stop pipeline if error rate exceeds threshold
- **Exponential backoff**: For transient failures (API rate limits, network issues)
- **Partial success**: Process what you can, log failures, continue

### Monitoring Metrics

| Metric | Alert Threshold |
|--------|----------------|
| Pipeline duration | > 2x historical average |
| Row count | < 50% or > 200% of expected |
| Error rate | > 1% of records |
| Data freshness | > SLA window |
| Resource usage | > 80% memory or CPU |

## Step 7: Performance Optimization

- **Partition** source reads by date or key range
- **Parallelize** independent extract tasks
- **Incremental processing**: Only process new/changed data
- **Columnar formats** (Parquet, ORC) for analytical workloads
- **Compression** (gzip, snappy, zstd) for storage and transfer
- **Connection pooling** for database sources
- **Bulk loading** (COPY, bcp, bulk insert) instead of row-by-row

## Quality Checklist

- [ ] Pipeline is idempotent (safe to re-run)
- [ ] All tasks have retry logic with appropriate backoff
- [ ] Data quality checks are in place at each stage
- [ ] Schema changes are detected and handled
- [ ] Logging captures enough detail for debugging
- [ ] Alerts fire on failure, latency, and anomalous row counts
- [ ] Pipeline is parameterized by date (no hardcoded dates)
- [ ] Sensitive data is masked or encrypted in transit and at rest
- [ ] Documentation covers source, transform logic, and destination schema
- [ ] Backfill process is documented and tested

## Edge Cases

- **Schema drift**: Source adds/removes columns; detect and handle gracefully
- **Late-arriving data**: Use watermarks and allow reprocessing windows
- **Duplicate events**: Implement deduplication using unique keys + window
- **API downtime**: Queue requests, implement circuit breaker, retry with backoff
- **Timezone mismatches**: Normalize all timestamps to UTC in the extract layer
- **Very large files**: Stream or chunk processing; do not load entire file into memory
- **Partial failures**: Use checkpointing to resume from last successful record
