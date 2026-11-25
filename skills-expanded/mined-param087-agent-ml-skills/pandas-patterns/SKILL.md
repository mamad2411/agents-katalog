---
name: pandas-patterns
description: Use when writing or reviewing pandas code. Covers idiomatic, vectorized, memory-efficient patterns; avoiding SettingWithCopyWarning, chained indexing, and slow apply loops.
---

# Pandas Patterns

## Overview

Most pandas pain comes from three things: chained indexing, row-wise `apply`, and ignoring dtypes/memory. This skill encodes the idioms that keep pandas correct and fast.

## When to use

- Writing data-wrangling code.
- Code is slow, leaks memory, or throws `SettingWithCopyWarning`.
- Reviewing someone's pandas for correctness.

## Core rules

1. **Assign with `.loc`, never chained.**
   ```python
   df.loc[df["age"] > 30, "segment"] = "senior"   # correct
   # df[df["age"] > 30]["segment"] = "senior"      # WRONG: SettingWithCopyWarning, no-op risk
   ```
2. **Vectorize instead of `apply(axis=1)`.** Row-wise apply is a Python loop.
   ```python
   df["bmi"] = df["weight"] / df["height"] ** 2          # fast
   # df.apply(lambda r: r.weight / r.height**2, axis=1)  # 100x slower
   ```
3. **Use `np.select` / `np.where` for conditional columns.**
   ```python
   import numpy as np
   df["tier"] = np.select(
       [df.spend > 1000, df.spend > 100],
       ["gold", "silver"],
       default="bronze",
   )
   ```
4. **Downcast dtypes** to cut memory: `category` for low-cardinality strings, `int32`/`float32` where safe.
   ```python
   df["country"] = df["country"].astype("category")
   ```
5. **Prefer `merge` over loops for joins**, and validate join cardinality:
   ```python
   df = orders.merge(users, on="user_id", how="left", validate="m:1")
   ```

## Performance toolkit

- `df.groupby(..., observed=True).agg(...)` — `observed=True` avoids exploding categorical combinations.
- `pd.eval` / `df.query()` for large boolean filters.
- Read big files in chunks (`chunksize=`) or switch to **Polars/DuckDB** when pandas is the bottleneck.
- `df.pipe(fn)` to compose transformations without intermediate variables.

## Method chaining (readable + copy-safe)

```python
result = (
    df
    .query("status == 'active'")
    .assign(revenue=lambda d: d.qty * d.price)
    .groupby("region", observed=True)
    .agg(total=("revenue", "sum"))
    .reset_index()
)
```

## Pitfalls

- **`inplace=True`** rarely saves memory and breaks chaining — avoid it.
- **Iterating with `iterrows`** — almost always replaceable with vectorization or `itertuples`.
- **Floating-point group keys** — round or use integer/category keys.
- **Silent dtype upcasts** (int → float when NaN appears) — use nullable `Int64` if you must keep integers.

## Hand-off

Clean, vectorized transformations that downstream skills (feature-engineering, model-evaluation) can run quickly on full datasets.
