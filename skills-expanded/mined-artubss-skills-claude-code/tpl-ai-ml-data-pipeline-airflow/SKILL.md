---
name: tpl-ai-ml-data-pipeline-airflow
description: Template do pack (ai-ml/08-data-pipeline-airflow.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/08-data-pipeline-airflow.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Data Pipeline with Apache Airflow 2.9

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/08-data-pipeline-airflow.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Orchestration:** Apache Airflow 2.9 (Celery executor)
- **Language:** Python 3.12
- **Metadata DB:** PostgreSQL 16
- **Data Storage:** AWS S3 (data lake) + Parquet via pandas/polars
- **Workers:** Celery + Redis broker
- **Secrets:** Airflow Connections (UI) + environment variables
- **Deployment:** Docker Compose (dev) / Helm on Kubernetes (prod)

---

## PROJECT STRUCTURE
```
airflow/
├── dags/
│   ├── etl_customers.py          # Customer data pipeline
│   ├── ml_feature_refresh.py     # ML feature computation
│   ├── daily_report.py           # Business report generation
│   └── utils/
│       ├── s3.py                 # S3 helper operators
│       ├── notifications.py      # Slack/email alerts
│       └── quality.py            # Data quality checks
├── plugins/
│   └── operators/
│       └── postgres_upsert.py   # Custom operator
├── tests/
│   └── test_etl_customers.py    # DAG unit tests
├── Dockerfile
└── docker-compose.yml
```

---

## ARCHITECTURE RULES
1. **DAG = orchestration only** — no data processing logic in the DAG file itself; delegate to functions/operators.
2. **Task atomicity** — each task can succeed/fail independently and be retried safely (idempotent).
3. **XCom sparingly** — XCom for IDs/paths only (< 1KB); never pass dataframes via XCom.
4. **Connections via Airflow UI or env vars** — never hardcode DB strings, S3 keys in DAG files.
5. **Backfill strategy defined upfront** — `catchup=True` only if historical backfill is intended; default `catchup=False`.
6. **SLA miss = alert, not failure** — SLAs send notifications but don't fail the DAG; failures are separate.
7. **Test DAGs without Airflow** — pure Python unit tests on all task functions; `dag.test()` for integration.
8. **Dynamic tasks for fan-out** — `@task.expand` / XCom-driven dynamic task generation instead of branching.

---

## DAG STRUCTURE EXAMPLE

```python
# dags/etl_customers.py
from __future__ import annotations
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.models import Variable
import logging

logger = logging.getLogger(__name__)

default_args = {
    "owner":             "data-team",
    "retries":           2,
    "retry_delay":       timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay":   timedelta(minutes=30),
    "email_on_failure":  True,
    "email_on_retry":    False,
    "email":             ["data-team@company.com"],
}

@dag(
    dag_id="etl_customers",
    description="Extract customers from Postgres, transform, load to S3 data lake",
    schedule="0 2 * * *",      # 2 AM UTC daily
    start_date=datetime(2024, 1, 1),
    catchup=False,             # Don't backfill historical runs
    max_active_runs=1,         # Prevent overlapping runs
    default_args=default_args,
    tags=["etl", "customers", "daily"],
    doc_md="""
### Customer ETL
Extracts daily customer snapshot, runs quality checks, loads to S3 as Parquet.
SLA: Must complete by 4 AM UTC.
Owner: #data-team Slack channel.
    """,
    sla_miss_callback=lambda *args: notify_slack_sla_miss(*args),
)
def etl_customers():

    @task(task_id="extract_customers")
    def extract() -> str:
        """Extract from Postgres, upload raw CSV to S3. Returns S3 path."""
        import pandas as pd
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from utils.s3 import upload_to_s3

        hook = PostgresHook(postgres_conn_id="postgres_prod")  # From Airflow Connections
        df = hook.get_pandas_df("""
            SELECT customer_id, email, created_at, plan, mrr
            FROM customers
            WHERE updated_at >= CURRENT_DATE - 1
        """)

        logger.info(f"Extracted {len(df)} customer records")

        # Push path, not data
        s3_path = f"raw/customers/{datetime.utcnow().strftime('%Y/%m/%d')}/customers.parquet"
        upload_to_s3(df, bucket="my-data-lake", key=s3_path)

        return s3_path   # XCom: just the path string

    @task(task_id="data_quality_check")
    def quality_check(s3_path: str) -> str:
        """Validate data quality. Fails task if critical checks fail."""
        import pandas as pd
        from utils.s3 import read_from_s3
        from utils.quality import run_quality_suite

        df = read_from_s3(bucket="my-data-lake", key=s3_path)
        report = run_quality_suite(df, suite_name="customers")

        if not report.success:
            critical_failures = [c for c in report.results if c.severity == "critical" and not c.passed]
            if critical_failures:
                raise ValueError(f"Critical quality checks failed: {[c.name for c in critical_failures]}")

        return s3_path

    @task(task_id="transform_customers")
    def transform(s3_path: str) -> str:
        """Apply business transformations. Write to curated zone."""
        import polars as pl
        from utils.s3 import read_from_s3_polars, upload_polars_to_s3

        df = read_from_s3_polars(bucket="my-data-lake", key=s3_path)

        transformed = (
            df
            .with_columns([
                pl.col("email").str.to_lowercase().alias("email_normalized"),
                pl.col("mrr").cast(pl.Float64),
                (pl.col("mrr") * 12).alias("arr"),
            ])
            .filter(pl.col("customer_id").is_not_null())
        )

        curated_path = s3_path.replace("raw/", "curated/").replace(".parquet", "_curated.parquet")
        upload_polars_to_s3(transformed, bucket="my-data-lake", key=curated_path)

        return curated_path

    @task(task_id="load_to_warehouse")
    def load(curated_path: str) -> None:
        """Load to data warehouse (Redshift/BigQuery/Snowflake)."""
        from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
        from utils.s3 import get_s3_url

        hook = RedshiftSQLHook(redshift_conn_id="redshift_prod")
        s3_url = get_s3_url(bucket="my-data-lake", key=curated_path)

        hook.run(f"""
            COPY customers_staging
            FROM '{s3_url}'
            IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3Role'
            FORMAT PARQUET;

            BEGIN;
            DELETE FROM customers WHERE customer_id IN (SELECT customer_id FROM customers_staging);
            INSERT INTO customers SELECT * FROM customers_staging;
            TRUNCATE TABLE customers_staging;
            COMMIT;
        """)

    # Task dependencies (linear pipeline)
    raw_path = extract()
    validated_path = quality_check(raw_path)
    curated_path = transform(validated_path)
    load(curated_path)

etl_customers()
```

---

## DYNAMIC TASK GENERATION

```python
# dags/ml_feature_refresh.py — process N tables dynamically
from __future__ import annotations
from airflow.decorators import dag, task

FEATURE_TABLES = ["orders", "sessions", "events", "products"]

@dag(schedule="@hourly", catchup=False, tags=["ml", "features"])
def ml_feature_refresh():

    @task
    def get_tables_to_process() -> list[str]:
        """Could query a config table or return static list."""
        return FEATURE_TABLES

    @task
    def compute_features(table_name: str) -> dict:
        logger.info(f"Computing features for {table_name}")
        # ... feature computation logic ...
        return {"table": table_name, "rows_processed": 1000}

    @task
    def summarize_runs(results: list[dict]) -> None:
        total = sum(r["rows_processed"] for r in results)
        logger.info(f"Feature refresh complete. Total rows: {total}")

    tables = get_tables_to_process()
    results = compute_features.expand(table_name=tables)   # Fan-out!
    summarize_runs(results)

ml_feature_refresh()
```

---

## XCOM LIMITS + RULES
```
XCom storage limit: 48KB (SQLite) / 1GB (PostgreSQL with blob)

✅ Pass via XCom:
  - File paths: "s3://bucket/path/file.parquet" (< 200 chars)
  - IDs: "job-123", "batch-abc"
  - Small counts/stats: {"rows": 1000, "errors": 5}

❌ Never pass via XCom:
  - DataFrames (any size)
  - File contents
  - Large JSON objects (> 10KB)
  - Database connections

Pattern: Tasks write to S3/DB, pass only the path/key via XCom.
```

---

## CONNECTION SECRETS

```bash
# Add connections via environment variables (no UI clicks in CI/CD)
# Format: AIRFLOW_CONN_{UPPER_CONN_ID}=connection-uri

export AIRFLOW_CONN_POSTGRES_PROD="postgresql://user:pass@rds-host:5432/mydb"
export AIRFLOW_CONN_REDSHIFT_PROD="redshift+psycopg2://user:pass@endpoint:5439/mydb"
export AIRFLOW_CONN_AWS_DEFAULT="aws://:@?region_name=us-east-1"  # Uses IAM role

# Or via Airflow Secrets Backend (Secrets Manager):
# In airflow.cfg:
# [secrets]
# backend = airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
# backend_kwargs = {"connections_prefix": "airflow/connections"}
```

---

## SLA MISS ALERT

```python
# dags/utils/notifications.py
from airflow.models import TaskInstance, DagRun
from airflow.utils.email import send_email
import requests

SLACK_WEBHOOK = Variable.get("SLACK_WEBHOOK_URL", default_var=None)

def notify_slack_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    if not SLACK_WEBHOOK:
        return
    msg = f":warning: SLA Miss: `{dag.dag_id}` — Tasks: {[t.task_id for t in task_list]}"
    requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=5)
```

---

## DAG UNIT TESTS

```python
# tests/test_etl_customers.py
import pytest
from airflow.models import DagBag

def test_dag_loads_without_errors():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    dag = dagbag.get_dag("etl_customers")
    assert dag is not None
    assert len(dagbag.import_errors) == 0

def test_dag_task_count():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    dag = dagbag.get_dag("etl_customers")
    assert len(dag.tasks) == 4   # extract, quality_check, transform, load

def test_dag_schedule():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    dag = dagbag.get_dag("etl_customers")
    assert dag.schedule_interval == "0 2 * * *"
    assert dag.catchup is False
```
