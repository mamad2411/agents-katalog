-----

## name: wrangling
description: >
Expert data wrangling, cleaning, and transformation using pandas, polars, and SQL.
Always use this skill when the user needs to: clean messy or raw data, reshape DataFrames
(pivot, melt, stack, unstack), join or merge datasets, handle missing values or duplicates,
parse dates/strings/JSON columns, normalize or encode features, fix data types, wrangle
CSVs/Excel/JSON/Parquet files, or prepare data for analysis or machine learning.
Trigger for any task involving “dirty data”, “data prep”, “ETL”, “munging”, “transform”,
“reshape”, or “combine datasets” — even if the user doesn’t say “wrangling” explicitly.
license: MIT
compatibility: opencode
metadata:
audience: data-analysts
category: data-science

# Data Wrangling

Covers the full wrangling lifecycle: **inspect → clean → reshape → merge → validate → export**.

-----

## 1. Inspect First

Always understand the data before touching it.

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

# Shape and types
print(df.shape)           # (rows, cols)
print(df.dtypes)
print(df.info())

# Missing values — count and percentage
missing = pd.DataFrame({
    "count": df.isnull().sum(),
    "pct": (df.isnull().sum() / len(df) * 100).round(1)
}).query("count > 0").sort_values("pct", ascending=False)
print(missing)

# Distributions and outliers
print(df.describe(include="all"))

# Duplicate rows
print(f"Duplicates: {df.duplicated().sum()}")

# Cardinality of categoricals
for col in df.select_dtypes("object"):
    print(f"{col}: {df[col].nunique()} unique — {df[col].value_counts().head(3).to_dict()}")
```

-----

## 2. Cleaning

### Missing Values

```python
# Strategy depends on column type and missingness rate:

# Drop rows where key columns are null
df = df.dropna(subset=["id", "date"])

# Fill with a sensible default
df["category"] = df["category"].fillna("Unknown")
df["quantity"] = df["quantity"].fillna(0)

# Forward/back fill (time series)
df["price"] = df["price"].ffill().bfill()

# Fill numerics with median (robust to outliers)
df["income"] = df["income"].fillna(df["income"].median())

# Interpolate (smooth numeric gaps)
df["sensor_reading"] = df["sensor_reading"].interpolate(method="linear")
```

### Data Types

```python
# Parse dates — always specify format for speed and correctness
df["created_at"] = pd.to_datetime(df["created_at"], format="%Y-%m-%d", errors="coerce")

# Numeric coercion — errors="coerce" turns unparseable values into NaN
df["amount"] = pd.to_numeric(df["amount"].str.replace("[$,]", "", regex=True), errors="coerce")

# Categoricals save memory on low-cardinality string columns
df["status"] = df["status"].astype("category")

# Boolean from string
df["is_active"] = df["is_active"].map({"true": True, "false": False, "1": True, "0": False})
```

### String Cleaning

```python
# Normalize text
df["name"] = df["name"].str.strip().str.title()
df["email"] = df["email"].str.lower().str.strip()

# Extract structured parts
df["domain"] = df["email"].str.split("@").str[1]
df["area_code"] = df["phone"].str.extract(r"\((\d{3})\)")

# Remove noise
df["notes"] = df["notes"].str.replace(r"[^\w\s]", "", regex=True)

# Standardize inconsistent values
replacements = {"NY": "New York", "N.Y.": "New York", "new york": "New York"}
df["state"] = df["state"].replace(replacements)

# Fuzzy deduplication (install: pip install thefuzz)
from thefuzz import process
canonical = ["New York", "Los Angeles", "Chicago"]
df["city_clean"] = df["city"].apply(
    lambda x: process.extractOne(x, canonical)[0] if pd.notna(x) else x
)
```

### Duplicates

```python
# Exact duplicates
df = df.drop_duplicates()

# Duplicates on key columns only — keep most recent
df = df.sort_values("updated_at", ascending=False)
df = df.drop_duplicates(subset=["customer_id"], keep="first")

# Find which rows are duped (for inspection before dropping)
dupes = df[df.duplicated(subset=["order_id"], keep=False)]
```

-----

## 3. Reshaping

### Pivot & Melt

```python
# Wide → long (melt): great for plotting and tidy analysis
long = pd.melt(
    df,
    id_vars=["country", "category"],
    value_vars=["2021", "2022", "2023"],
    var_name="year",
    value_name="revenue"
)

# Long → wide (pivot): great for comparison tables
wide = df.pivot_table(
    index="country",
    columns="year",
    values="revenue",
    aggfunc="sum",
    fill_value=0
)
wide.columns = [f"rev_{c}" for c in wide.columns]  # flatten MultiIndex
wide = wide.reset_index()
```

### Stack / Unstack (MultiIndex)

```python
# Stack columns into rows
stacked = wide.set_index("country").stack().reset_index()
stacked.columns = ["country", "year", "revenue"]

# Unstack index level into columns
unstacked = df.set_index(["country", "year"])["revenue"].unstack("year")
```

### Explode Nested Data

```python
# JSON column → rows
import json
df["tags"] = df["tags"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df_exploded = df.explode("tags")

# Nested dict column → separate columns
df = pd.concat([df.drop("metadata", axis=1),
                df["metadata"].apply(pd.Series)], axis=1)
```

-----

## 4. Merging & Joining

```python
# Standard join — always specify how= explicitly, never rely on default
merged = pd.merge(orders, customers, on="customer_id", how="left")

# Multiple keys
merged = pd.merge(sales, targets,
                  left_on=["region", "year"],
                  right_on=["territory", "fiscal_year"],
                  how="inner")

# Diagnose join quality immediately after merging
total = len(merged)
matched = merged["customer_name"].notna().sum()
print(f"Match rate: {matched}/{total} ({matched/total:.1%})")

# Concatenate (stack rows from multiple frames)
combined = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# Anti-join: rows in left NOT in right
not_matched = orders[~orders["customer_id"].isin(customers["customer_id"])]
```

**Common join bugs to check:**

- Mismatched dtypes on join keys (`int` vs `str`) → always align before merging
- Leading/trailing whitespace in string keys → `.str.strip()` both sides
- Case differences → `.str.lower()` both sides
- Duplicate keys causing row explosion → `df.duplicated(subset=["key"]).sum()` before merging

-----

## 5. Feature Engineering

```python
# Date decomposition
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.day_name()
df["is_weekend"] = df["date"].dt.dayofweek >= 5
df["days_since_signup"] = (pd.Timestamp.today() - df["signup_date"]).dt.days

# Binning
df["age_band"] = pd.cut(df["age"], bins=[0,18,35,65,120],
                        labels=["minor","young_adult","adult","senior"])
df["income_quartile"] = pd.qcut(df["income"], q=4, labels=["Q1","Q2","Q3","Q4"])

# Multi-condition segmentation (cleaner than nested np.where)
conditions = [
    df["income"] > 100_000,
    df["income"] > 50_000,
]
choices = ["Premium", "Standard"]
df["segment"] = np.select(conditions, choices, default="Basic")

# Window / rolling calculations
df = df.sort_values(["customer_id", "date"])
df["7d_rolling_avg"] = (df.groupby("customer_id")["spend"]
                          .transform(lambda x: x.rolling(7, min_periods=1).mean()))
df["pct_change"] = df.groupby("customer_id")["spend"].pct_change()
df["rank_in_group"] = df.groupby("region")["sales"].rank(method="dense", ascending=False)
```

-----

## 6. Groupby & Aggregation

```python
# Simple aggregation
summary = df.groupby("region").agg(
    total_sales=("sales", "sum"),
    avg_order=("order_value", "mean"),
    order_count=("order_id", "count"),
    unique_customers=("customer_id", "nunique")
).reset_index()

# Multiple aggregations per column
summary = df.groupby("category").agg({"price": ["min","max","mean"], "qty": "sum"})
summary.columns = ["_".join(c) for c in summary.columns]  # flatten MultiIndex

# Transform (returns same-length Series, great for adding group stats back)
df["pct_of_region"] = df["sales"] / df.groupby("region")["sales"].transform("sum")
df["region_avg"] = df.groupby("region")["sales"].transform("mean")
```

-----

## 7. Validation

Always validate after transformation — never assume it worked.

```python
def validate(df, name="DataFrame"):
    issues = []
    if df.isnull().any().any():
        issues.append(f"Nulls in: {df.columns[df.isnull().any()].tolist()}")
    dupes = df.duplicated().sum()
    if dupes:
        issues.append(f"{dupes} duplicate rows")
    for col in df.select_dtypes("number"):
        if (df[col] < 0).any():
            issues.append(f"Negative values in '{col}'")
    if issues:
        print(f"⚠️  {name} issues:\n" + "\n".join(f"  - {i}" for i in issues))
    else:
        print(f"✅  {name} looks clean ({len(df):,} rows, {len(df.columns)} cols)")
    return len(issues) == 0

validate(df, "cleaned_orders")
```

-----

## 8. Reading & Writing Files

```python
# CSV with explicit types — avoids silent type inference errors
df = pd.read_csv("data.csv",
    dtype={"zip_code": str, "id": str},
    parse_dates=["created_at", "updated_at"],
    na_values=["N/A", "na", "--", ""])

# Excel — specific sheet, skip header rows
df = pd.read_excel("report.xlsx", sheet_name="Sales", skiprows=2, usecols="A:F")

# Parquet — columnar, fast, preserves dtypes (prefer over CSV for large data)
df.to_parquet("clean_data.parquet", index=False)
df = pd.read_parquet("clean_data.parquet", columns=["id","date","amount"])

# JSON with nested records
df = pd.json_normalize(records, record_path=["items"], meta=["order_id", "customer"])

# Chunked reading for large files
chunks = []
for chunk in pd.read_csv("huge.csv", chunksize=100_000):
    chunk = chunk[chunk["status"] == "active"]  # filter early
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)
```

-----

## Polars (Fast Alternative for Large Data)

Use Polars when pandas is slow (>1M rows) or you need lazy evaluation.

```python
import polars as pl

df = pl.read_csv("data.csv")

# Lazy evaluation — builds a query plan, executes only on .collect()
result = (
    pl.scan_csv("large_data.csv")
    .filter(pl.col("status") == "active")
    .with_columns([
        pl.col("amount").cast(pl.Float64),
        pl.col("date").str.to_date("%Y-%m-%d"),
        (pl.col("revenue") / pl.col("revenue").sum()).alias("pct_of_total"),
    ])
    .group_by("region")
    .agg([
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("customer_id").n_unique().alias("customers"),
    ])
    .sort("total_revenue", descending=True)
    .collect()
)
```

-----

## Quick Reference: Common Fixes

|Problem                             |Fix                                                                   |
|------------------------------------|----------------------------------------------------------------------|
|Mixed date formats                  |`pd.to_datetime(df["d"], infer_datetime_format=True, errors="coerce")`|
|`$1,234.56` as string               |`.str.replace("[$,]","",regex=True)` → `pd.to_numeric()`              |
|Column names with spaces            |`df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")`|
|Inconsistent booleans               |`.map({"yes":True,"no":False,"1":True,"0":False})`                    |
|Exploding row count after join      |Check for dupe keys: `df.duplicated(subset=["key"]).sum()`            |
|Object column that should be numeric|`pd.to_numeric(df[col], errors="coerce")`                             |
|Memory issues on large CSV          |Use `dtype=` to avoid float64 defaults; use Parquet; use Polars       |