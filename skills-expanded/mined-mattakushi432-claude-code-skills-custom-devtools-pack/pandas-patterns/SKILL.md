---
name: pandas-patterns
description: "When to activate: pandas, DataFrame operations, data wrangling, CSV/Excel, groupby, merge, performance optimization"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: data
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Pandas Patterns

## Core Best Practices

### Prefer vectorized operations over loops
```python
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

# Bad: Python loop
results = []
for _, row in df.iterrows():
    results.append(row["price"] * row["quantity"])
df["total"] = results

# Good: vectorized
df["total"] = df["price"] * df["quantity"]

# Good: apply for complex per-row logic (still ~10x slower than vectorized)
df["category"] = df["value"].apply(lambda x: "high" if x > 100 else "low")

# Best: use np.where for conditional logic
df["category"] = np.where(df["value"] > 100, "high", "low")
```

### Use appropriate data types
```python
# Reduce memory: use categorical for low-cardinality strings
df["status"] = df["status"].astype("category")

# Downcast numeric types
df["count"] = pd.to_numeric(df["count"], downcast="integer")

# Check memory usage
df.info(memory_usage="deep")
df.memory_usage(deep=True).sum() / 1e6  # MB
```

### Chaining with method chaining
```python
result = (
    df
    .query("status == 'active' and value > 0")
    .assign(
        full_name=lambda d: d["first_name"] + " " + d["last_name"],
        value_log=lambda d: np.log1p(d["value"]),
    )
    .groupby("category")["value"]
    .agg(["mean", "std", "count"])
    .rename(columns={"mean": "avg", "std": "std_dev", "count": "n"})
    .sort_values("avg", ascending=False)
)
```

## GroupBy Patterns
```python
# Aggregation
summary = df.groupby("category").agg(
    total_revenue=("price", "sum"),
    avg_price=("price", "mean"),
    n_items=("id", "count"),
    unique_customers=("customer_id", "nunique"),
).reset_index()

# Transform (preserves original index/shape)
df["category_avg"] = df.groupby("category")["price"].transform("mean")

# Apply for complex group operations
def normalize(group: pd.DataFrame) -> pd.DataFrame:
    group["normalized"] = (group["value"] - group["value"].mean()) / group["value"].std()
    return group

df = df.groupby("category", group_keys=False).apply(normalize)
```

## Merge / Join Patterns
```python
# Validate join keys (prevents silent data loss)
merged = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="left",
    validate="m:1",  # many orders to one customer
    indicator=True,  # adds _merge column for debugging
)

# Check for unexpected non-matches
unmatched = merged[merged["_merge"] != "both"]
if len(unmatched) > 0:
    logger.warning(f"{len(unmatched)} orders have no matching customer")
```

## Anti-Patterns
- `iterrows()` / `itertuples()` in performance-sensitive code
- Chained assignment: `df["a"]["b"] = val` → use `df.loc[mask, col] = val`
- `object` dtype for numeric-looking columns (use `pd.to_numeric`)
- Reading entire large CSV into memory (use `chunksize` or Polars)
- Missing `validate=` in merges (silent data duplication)
