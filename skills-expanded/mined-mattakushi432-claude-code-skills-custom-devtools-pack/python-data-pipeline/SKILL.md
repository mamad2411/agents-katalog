---
name: python-data-pipeline
description: "When to activate: ETL, data pipeline, Prefect, Airflow, DLT, Polars, batch processing, data quality"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: data
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python Data Pipeline Patterns

## Polars (Faster pandas alternative)
```python
import polars as pl
from pathlib import Path

# Lazy evaluation (builds execution plan, runs on collect())
result = (
    pl.scan_csv("data/*.csv")
    .filter(pl.col("status") == "active")
    .with_columns([
        pl.col("price").cast(pl.Float64),
        (pl.col("price") * pl.col("quantity")).alias("revenue"),
        pl.col("date").str.to_date("%Y-%m-%d"),
    ])
    .group_by(["category", "date"])
    .agg([
        pl.sum("revenue").alias("total_revenue"),
        pl.count("id").alias("n_orders"),
        pl.mean("price").alias("avg_price"),
    ])
    .sort("total_revenue", descending=True)
    .collect()
)

# Write
result.write_parquet("output/revenue_by_category.parquet")
result.write_csv("output/revenue_by_category.csv")
```

## Prefect Flows
```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
    retries=3,
    retry_delay_seconds=60,
)
def extract(source_url: str) -> pl.DataFrame:
    return pl.read_csv(source_url)

@task
def transform(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(pl.col("amount") > 0).with_columns(
        pl.col("date").str.to_date()
    )

@task
def load(df: pl.DataFrame, target: str) -> None:
    df.write_parquet(target)

@flow(name="daily-revenue", log_prints=True)
def daily_revenue_pipeline(date: str) -> None:
    raw = extract(f"s3://data/{date}/orders.csv")
    clean = transform(raw)
    load(clean, f"s3://warehouse/{date}/revenue.parquet")

if __name__ == "__main__":
    daily_revenue_pipeline("2024-01-01")
```

## Data Quality Checks
```python
import great_expectations as gx

def validate_orders(df: pl.DataFrame) -> bool:
    # Convert to pandas for GX compatibility
    pandas_df = df.to_pandas()
    
    validator = gx.from_pandas(pandas_df)
    
    results = [
        validator.expect_column_values_to_not_be_null("order_id"),
        validator.expect_column_values_to_be_between("amount", min_value=0),
        validator.expect_column_values_to_be_in_set("status", ["pending", "complete", "cancelled"]),
        validator.expect_column_to_exist("created_at"),
    ]
    
    failed = [r for r in results if not r.success]
    if failed:
        logger.error("Data quality check failed: %s", failed)
        return False
    return True
```

## Chunked Processing for Large Files
```python
def process_large_csv(path: Path, chunk_size: int = 100_000) -> pl.DataFrame:
    results = []
    
    for chunk in pl.read_csv_batched(path, batch_size=chunk_size):
        processed = transform_chunk(chunk)
        results.append(processed)
    
    return pl.concat(results)
```
