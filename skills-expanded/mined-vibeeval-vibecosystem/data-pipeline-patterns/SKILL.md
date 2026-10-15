---
name: data-pipeline-patterns
description: ETL/ELT patterns, batch vs streaming, idempotency, data quality framework, and pipeline orchestration
---

# Data Pipeline Patterns

## ETL vs ELT Decision

| Kriter | ETL | ELT |
|--------|-----|-----|
| Transform location | Pipeline'da | Data warehouse'da |
| Data volume | Küçük-orta | Büyük |
| Flexibility | Düşük | Yüksek |
| Cost | Compute-heavy | Storage-heavy |
| Use case | Legacy, compliance | Modern analytics |

## Batch vs Streaming

| Kriter | Batch | Streaming |
|--------|-------|-----------|
| Latency | Dakika-saat | Saniye-milisaniye |
| Complexity | Düşük | Yüksek |
| Cost | Düşük | Yüksek |
| Use case | Reporting, ETL | Real-time alerts, dashboards |
| Tool | Airflow, dbt | Kafka Streams, Flink |

## Idempotency Patterns

```python
# Pattern 1: Upsert
INSERT INTO target (id, name, updated_at)
VALUES (%(id)s, %(name)s, %(ts)s)
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  updated_at = EXCLUDED.updated_at

# Pattern 2: Partition overwrite
DELETE FROM target WHERE partition_date = '2026-03-14';
INSERT INTO target SELECT * FROM staging WHERE partition_date = '2026-03-14';

# Pattern 3: Checkpoint
last_checkpoint = get_checkpoint('pipeline_x')
new_data = source.query(f"WHERE updated_at > '{last_checkpoint}'")
process(new_data)
save_checkpoint('pipeline_x', max(new_data.updated_at))
```

## Data Quality Framework

```python
import pandera as pa

schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, pa.Check.gt(0), nullable=False),
    "email": pa.Column(str, pa.Check.str_matches(r'^.+@.+\..+$')),
    "age": pa.Column(int, pa.Check.in_range(0, 150), nullable=True),
    "created_at": pa.Column(pa.DateTime, pa.Check.less_than_or_equal_to(pd.Timestamp.now()))
})

validated_df = schema.validate(df)  # Fail on invalid data
```

### Quality Dimensions

| Dimension | Kontrol | Tool |
|-----------|---------|------|
| Completeness | NULL ratio < threshold | Great Expectations |
| Accuracy | Value range checks | pandera |
| Freshness | Last update < SLA | Airflow sensor |
| Uniqueness | Duplicate check | SQL DISTINCT |
| Consistency | Cross-table referential integrity | dbt test |

## Pipeline Orchestration

```python
# Airflow DAG
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('daily_etl', schedule='0 6 * * *', catchup=False) as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_fn)
    transform = PythonOperator(task_id='transform', python_callable=transform_fn)
    load = PythonOperator(task_id='load', python_callable=load_fn)
    validate = PythonOperator(task_id='validate', python_callable=validate_fn)

    extract >> transform >> load >> validate
```

## Checklist

- [ ] Pipeline idempotent (rerun safe)
- [ ] Data quality checks her adımda
- [ ] Dead letter queue (failed records)
- [ ] Monitoring + alerting aktif
- [ ] Schema evolution handled
- [ ] Backfill mekanizması var
- [ ] Retry logic (exponential backoff)
- [ ] Data lineage tracked

## Anti-Patterns

- Pipeline'da hardcoded credentials
- Idempotent olmayan transform
- Data quality check'siz load
- Monolithic pipeline (parçala)
- Silent failure (error swallowing)
