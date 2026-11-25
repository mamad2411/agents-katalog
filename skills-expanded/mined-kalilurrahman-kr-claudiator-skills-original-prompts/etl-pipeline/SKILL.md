---
name: etl-pipeline
description: Design extract-transform-load pipelines for data warehousing. Outputs data sources, transformations, quality checks, scheduling, and monitoring.
argument-hint: [data sources, transformation requirements, destination]
allowed-tools: Read, Write, Bash
---

# ETL Pipeline Design

Design production-ready ETL (Extract-Transform-Load) pipelines that move data from sources to destinations reliably. Not basic SQL queries — orchestration, incremental loading, data quality, schema evolution, and monitoring.

## Process

1. **Map data sources.** Databases, APIs, files, streams.
2. **Define transformations.** Cleaning, enrichment, aggregation, joins.
3. **Design schema.** Fact tables, dimensions, slowly changing dimensions (SCD).
4. **Plan incremental loading.** Full refresh vs delta loads, watermarking.
5. **Add quality checks.** Schema validation, null checks, range checks, uniqueness.
6. **Set up orchestration.** Scheduling, dependencies, retries.
7. **Monitor.** Data freshness, row counts, failed jobs, SLA violations.

## Output Format

### ETL Pipeline: [Pipeline Name]

**Sources:** 3 (PostgreSQL, S3, REST API)  
**Destination:** Snowflake Data Warehouse  
**Schedule:** Daily at 2 AM UTC  
**Load Type:** Incremental (last 24 hours)  
**Orchestration:** Apache Airflow  
**Expected Duration:** 45 minutes  
**Data Volume:** 10M rows/day  

---

## Pipeline Architecture

```
[PostgreSQL]  ─┐
               │
[S3 CSV]      ─┼─→ [Extract] → [Transform] → [Load] → [Snowflake]
               │      ↓            ↓            ↓
[REST API]    ─┘   [Staging]  [Quality]   [Final Tables]
                     Area       Checks
```

---

## Incremental Loading Pattern

```python
def extract_incremental(table_name):
    # Get last successful watermark
    watermark = get_last_watermark(table_name)
    
    query = f"""
        SELECT * FROM {table_name}
        WHERE updated_at > %(watermark)s
        ORDER BY updated_at ASC
    """
    
    conn = psycopg2.connect(DATABASE_URL)
    df = pd.read_sql(query, conn, params={'watermark': watermark})
    
    # Save to staging
    df.to_parquet(f's3://staging/{table_name}/{date}.parquet')
    
    # Update watermark only after successful load
    if len(df) > 0:
        new_watermark = df['updated_at'].max()
        save_watermark(table_name, new_watermark)
    
    return len(df)
```

---

## Data Quality Framework

```python
class DataQuality Check:
    def __init__(self, df, table_name):
        self.df = df
        self.table_name = table_name
        self.errors = []
    
    def check_schema(self, expected_columns):
        """Validate column presence and types"""
        missing = set(expected_columns) - set(self.df.columns)
        if missing:
            self.errors.append(f"Missing columns: {missing}")
    
    def check_nulls(self, non_null_columns):
        """Ensure critical columns have no nulls"""
        for col in non_null_columns:
            null_count = self.df[col].isnull().sum()
            if null_count > 0:
                self.errors.append(f"{col} has {null_count} nulls")
    
    def check_range(self, column, min_val=None, max_val=None):
        """Validate numeric ranges"""
        if min_val is not None:
            invalid = (self.df[column] < min_val).sum()
            if invalid > 0:
                self.errors.append(f"{column} has {invalid} values < {min_val}")
    
    def check_row_count(self, expected_min, expected_max):
        """Validate row count is within expected range"""
        count = len(self.df)
        if count < expected_min or count > expected_max:
            self.errors.append(f"Row count {count} outside [{expected_min}, {expected_max}]")
    
    def check_duplicates(self, key_columns):
        """Check for duplicates on key"""
        dupes = self.df.duplicated(subset=key_columns).sum()
        if dupes > 0:
            self.errors.append(f"{dupes} duplicate records on {key_columns}")
    
    def run_all_checks(self):
        """Run all checks and raise if any fail"""
        if self.errors:
            raise DataQualityError(f"Quality checks failed for {self.table_name}: {self.errors}")
        return True
```

## Rules

- Incremental loading is mandatory for tables > 10M rows — full refresh is too slow.
- Every pipeline must have data quality checks before loading to destination.
- Watermarks must be updated atomically after successful load.
- Failed jobs must retry 3 times before alerting.
- Data freshness SLA must be monitored (alert if > 2 hours old).
- Use SCD Type 2 for dimensions where history matters.
- Every transformation must be idempotent.
- Staging area is mandatory — never load directly from source to destination.
- Monitor row counts daily — alert if deviation > 20% from average.
- Pipeline duration must be tracked — alert if runtime exceeds 2x expected.
