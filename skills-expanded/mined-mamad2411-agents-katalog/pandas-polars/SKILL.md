---
name: "pandas-polars"
description: "Pandas and Polars data manipulation: filtering, groupby, joins, time series, performance optimization"
---

# Pandas / Polars Skill

## When to activate
- Cleaning, transforming, or aggregating tabular data in Python
- Merging, joining, or reshaping DataFrames
- Writing data validation or quality checks
- Converting between formats (CSV, Parquet, JSON, Excel)
- Profiling or exploring a new dataset
- Optimizing slow Pandas code for large datasets
- Migrating Pandas code to Polars for performance

## When NOT to use
- SQL in a database (push transformations to the database when data is already there)
- Spark/distributed computing (use PySpark skill for datasets > available RAM)
- dbt models (SQL-based transformations in a warehouse)
- NumPy array operations on non-tabular data

## Instructions

### Pandas — performance rules
```python
import pandas as pd
import numpy as np

# Never use iterrows() — vectorize instead
# Bad:
for idx, row in df.iterrows():
    df.at[idx, 'tax'] = row['price'] * 0.2

# Good:
df['tax'] = df['price'] * 0.2

# Use .loc for label-based access, .iloc for position-based
# Never chain without assignment — causes SettingWithCopyWarning
df.loc[df['status'] == 'active', 'flag'] = True

# Categorical dtype for low-cardinality string columns (massive memory saving)
df['country'] = df['country'].astype('category')

# Downcasting numeric types to reduce memory
df['quantity'] = pd.to_numeric(df['quantity'], downcast='integer')
df['price'] = pd.to_numeric(df['price'], downcast='float')
```

### Pandas — aggregation and groupby
```python
# Groupby with multiple aggregations
summary = (
    df.groupby(['region', 'category'])
    .agg(
        total_revenue=('revenue', 'sum'),
        order_count=('order_id', 'nunique'),
        avg_order_value=('revenue', 'mean'),
    )
    .reset_index()
    .sort_values('total_revenue', ascending=False)
)
```

### Pandas — merging
```python
# Always specify how= explicitly — never rely on default (inner)
result = pd.merge(
    orders,
    customers,
    on='customer_id',
    how='left',      # explicit
    validate='m:1',  # validates cardinality — raises if violated
    suffixes=('_order', '_customer')
)
```

### Polars — when to use instead of Pandas
Use Polars when:
- Dataset > 1M rows (Polars is 5–100x faster for many operations)
- You need lazy evaluation (query optimization before execution)
- Parallelism matters (Polars uses all CPU cores by default)

```python
import polars as pl

# Lazy API — queries are optimized before execution
result = (
    pl.scan_parquet("orders.parquet")   # Lazy scan — no data loaded yet
    .filter(pl.col("status") == "completed")
    .group_by(["region", "category"])
    .agg([
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("order_id").n_unique().alias("order_count"),
        pl.col("revenue").mean().alias("avg_order_value"),
    ])
    .sort("total_revenue", descending=True)
    .collect()   # Execute now
)
```

### Polars — expressions (no chained indexing)
```python
# Polars: no SettingWithCopyWarning, no chained indexing
df = df.with_columns([
    (pl.col("price") * 0.2).alias("tax"),
    pl.col("name").str.to_uppercase().alias("name_upper"),
    pl.when(pl.col("quantity") > 10)
      .then(pl.lit("bulk"))
      .otherwise(pl.lit("standard"))
      .alias("order_type"),
])
```

### Data validation pattern
```python
def validate_orders(df: pd.DataFrame) -> None:
    assert df['order_id'].notna().all(), "order_id has nulls"
    assert df['order_id'].is_unique, "order_id has duplicates"
    assert (df['amount'] >= 0).all(), "amount has negative values"
    assert df['status'].isin(['pending', 'completed', 'cancelled']).all(), "invalid status values"
    assert pd.to_datetime(df['created_at'], errors='coerce').notna().all(), "created_at has invalid dates"
```

### Format conversion
```python
# Read
df = pd.read_parquet("data.parquet", columns=['id', 'name', 'amount'])  # Column selection at read time
df = pd.read_csv("data.csv", dtype={'id': str}, parse_dates=['created_at'])

# Write — always use Parquet over CSV for large datasets
df.to_parquet("output.parquet", index=False, compression='snappy')
```

## Example

**User:** Clean a raw orders CSV: fix dtypes, remove duplicates, handle nulls, add derived columns (revenue_after_tax, order_size_bucket), and output a validated Parquet file.

**Expected output:**
- Read with explicit `dtype=` and `parse_dates=`
- Drop duplicate `order_id` rows (keep last)
- Fill nulls: `quantity` → 0, `discount` → 0.0, drop rows where `customer_id` is null
- Derive: `revenue_after_tax = price * quantity * (1 - discount) * 0.8`
- Bucket: `order_size_bucket` = 'small'/<100, 'medium'/100–1000, 'large'/>1000
- Validate with assertions before write
- Write to Parquet with snappy compression

---
