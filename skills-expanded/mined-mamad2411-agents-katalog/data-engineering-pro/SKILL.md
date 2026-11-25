---
name: data-engineering-pro
description: "ETL pipelines, data warehousing, streaming, orchestration, quality, governance. Use when designing or reviewing data pipelines."
---

# Data Engineering Pro

## Purpose

Build production data pipelines: batch and streaming ETL, data warehouse modeling, orchestration, data quality, and governance.

## When to Use

**Use this when:**
- Designing or reviewing batch ETL pipelines, data warehouse models, or dbt transformation layers
- Setting up orchestration with Airflow, Prefect, or Dagster for scheduled data workflows
- Building streaming ingestion with Kafka, Kinesis, or Pub/Sub feeding a warehouse or lake

**Use this ESPECIALLY when:**
- The pipeline handles PII and must redact or mask data before it reaches non-production environments
- SLA breaches on data freshness would have downstream business impact (dashboards, ML features, billing)
- You are migrating from ad-hoc scripts to a versioned, tested, incrementally-loaded warehouse model

**Don't skip when:**
- Source schemas are owned by another team and may evolve without notice — data contracts and schema evolution handling are required
- The raw layer is being reused by multiple downstream consumers and breaking changes have no rollback path
- Data quality failures in the past have gone undetected until users reported incorrect numbers

## Core Patterns

### 1. Pipeline Architecture

```
[Sources] → [Ingestion] → [Stage] → [ODS] → [DW] → [Marts] → [Consumption]
   │            │            │         │       │        │          │
  APIs        Kafka      S3/GCS    Snowflake  dbt    Views/APIs   BI tools
  DBs         Kinesis     Raw       Bronze  Silver  Gold    Dashboards
  Events      Pub/Sub    Landing    Deduped  Modeled Aggregated  Notebooks
```

### 2. dbt Modeling

```sql
-- models/staging/stg_projects.sql
-- Stage: raw → cleaned, typed, renamed
WITH source AS (
    SELECT * FROM {{ source('raw', 'projects') }}
),
renamed AS (
    SELECT
        id,
        name,
        description,
        owner_id,
        created_at::timestamp AS created_at,
        updated_at::timestamp AS updated_at,
        _loaded_at
    FROM source
    WHERE _deleted = false
)
SELECT * FROM renamed

-- models/marts/dim_projects.sql
-- Mart: business-facing dimension
SELECT
    p.id AS project_id,
    p.name AS project_name,
    p.description,
    u.name AS owner_name,
    u.department,
    p.created_at,
    CASE
        WHEN COUNT(t.id) = 0 THEN 'no_tasks'
        WHEN SUM(CASE WHEN t.status = 'done' THEN 1 ELSE 0 END) = COUNT(t.id) THEN 'complete'
        ELSE 'in_progress'
    END AS project_status
FROM {{ ref('dim_projects') }} p
LEFT JOIN {{ ref('dim_users') }} u ON p.owner_id = u.user_id
LEFT JOIN {{ ref('fact_tasks') }} t ON p.project_id = t.project_id
GROUP BY 1, 2, 3, 4, 5, 6
```

### 3. Orchestration (Airflow)

```python
# dags/project_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

with DAG(
    'project_pipeline',
    schedule='0 3 * * *',   # Daily at 3 AM
    catchup=False,
    max_active_runs=1,
) as dag:
    extract = PythonOperator(
        task_id='extract_projects',
        python_callable=extract_from_api,
    )

    load_raw = SnowflakeOperator(
        task_id='load_raw_projects',
        sql='COPY INTO raw.projects FROM @stage/projects/',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --models marts',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --models marts',
    )

    alert_on_failure = SlackWebhookOperator(
        task_id='alert_on_failure',
        slack_webhook_conn_id='slack_alerts',
        message='Pipeline failed: {{ dag.dag_id }}',
        trigger_rule='one_failure',
    )

    extract >> load_raw >> dbt_run >> dbt_test
    [extract, load_raw, dbt_run, dbt_test] >> alert_on_failure
```

### 4. Data Quality

```yaml
# tests/data_quality.yml
version: 2
models:
  - name: dim_projects
    columns:
      - name: project_id
        tests:
          - unique
          - not_null
      - name: project_name
        tests:
          - not_null
          - length_greater_than: 0
      - name: created_at
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_in_type: timestamp
  - name: fact_tasks
    columns:
      - name: task_id
        tests:
          - unique
          - not_null
          - relationships:
              to: ref('dim_projects')
              field: project_id
      - name: estimated_hours
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000
```

### 5. Streaming (Kafka)

```python
# Kafka producer
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode(),
    acks='all',                  # Wait for all replicas
    retries=3,
    max_in_flight_requests_per_connection=1,
)

producer.send('project-events', {
    'event_type': 'project_created',
    'project_id': str(project.id),
    'user_id': str(project.owner_id),
    'timestamp': datetime.utcnow().isoformat(),
})
producer.flush()
```

### Checklist

- [ ] Source data versioned (immutable raw layer)
- [ ] dbt tests on every model (not_null, unique, relationships)
- [ ] Airflow alerting on failure (Slack/PagerDuty)
- [ ] Backfill strategy documented (catchup, rerun)
- [ ] Data contract between source and consumers
- [ ] PII columns tagged and redacted in non-production
- [ ] Incremental models for large tables
- [ ] Data retention policy documented
- [ ] Schema evolution handled (additive changes)

## Related Skills

- **ai-ml-pro** — feature store design, training data pipelines, and model evaluation datasets that sit downstream of your warehouse
- **backend-senior-engineer** — application-side event emission and change-data-capture patterns that are the source of record for your pipelines
- **observability-pro** — pipeline run metrics, SLA alerting, and data-freshness dashboards fed by your orchestration layer
- **cloud-security-auditor** — IAM roles for Snowflake, BigQuery, S3, and Kafka; encryption-at-rest and in-transit for sensitive data stores
- **security-reviewer** — PII classification, column-level masking policies, and access control in the warehouse
- **test-engineer** — dbt test strategy, Great Expectations suites, and pipeline integration tests against staging data
- **devops-release-engineer** — CI/CD for dbt model promotion, Airflow DAG deployment, and infrastructure-as-code for the data platform
- **performance-engineer** — query optimization, partition pruning, incremental materialization strategies, and Kafka consumer lag tuning

