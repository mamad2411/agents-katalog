---
name: exploratory-data-analysis
description: Use when starting on a new dataset, before modeling, or when asked to "explore", "profile", "understand", or "summarize" data. Covers structured EDA, distributions, correlations, target leakage checks, and visualization.
---

# Exploratory Data Analysis (EDA)

## Overview

EDA is the disciplined first pass over a dataset: understand shape, types, distributions, missingness, relationships, and red flags **before** writing a single model. Skipping it is the #1 cause of silent modeling failures (leakage, broken splits, garbage features).

## When to use

- A new dataset just landed.
- You're asked to "look at", "profile", "explore", or "summarize" data.
- A model underperforms and you need to understand the inputs.

## Workflow

Follow this order. Do not jump to modeling until every step is answered.

1. **Shape & types** — rows, columns, dtypes, memory. Are numeric columns actually numeric?
2. **Missingness** — per-column null counts and patterns (MCAR/MAR/MNAR). Is missingness itself predictive?
3. **Target analysis** — distribution of the target (class balance / skew). This decides metrics and resampling.
4. **Univariate** — distributions of each feature (histograms, value counts, describe()).
5. **Bivariate** — feature vs target relationships; correlation matrix for numeric.
6. **Leakage scan** — features too perfectly correlated with the target, IDs, timestamps, or post-outcome columns.
7. **Cardinality & outliers** — high-cardinality categoricals, extreme values.

## Reference snippet

```python
import pandas as pd

df = pd.read_csv("data.csv")

# 1. Shape & types
print(df.shape)
print(df.dtypes.value_counts())
print(df.memory_usage(deep=True).sum() / 1e6, "MB")

# 2. Missingness
miss = df.isna().mean().sort_values(ascending=False)
print(miss[miss > 0])

# 3. Target (classification example)
print(df["target"].value_counts(normalize=True))

# 4-5. Numeric summary + correlations with target
num = df.select_dtypes("number")
print(num.describe().T)
print(num.corr()["target"].sort_values(ascending=False))

# 6. Leakage red flag: |corr| ~ 1.0 with target
corr_t = num.corr()["target"].drop("target").abs()
print("LEAKAGE SUSPECTS:", corr_t[corr_t > 0.95].index.tolist())
```

For a fast automated first look, `ydata-profiling` (`ProfileReport(df)`) or `df.describe(include="all")` is acceptable — but never let a tool replace the manual leakage scan.

## Pitfalls

- **Profiling on the full dataset then splitting.** EDA that informs feature choices must be done on the **training split only**, or you leak test information.
- **Ignoring class imbalance.** A 99/1 split makes accuracy meaningless — note it now so you pick the right metric later.
- **Treating IDs as features.** Order IDs, row indices, and hashes correlate with the target by accident.
- **Trusting `.corr()` for non-linear / categorical relationships.** Use mutual information or grouped means for those.

## Hand-off

Output of EDA should be: a short written summary (shape, target balance, top missing columns, leakage suspects, candidate features) that downstream steps (data-cleaning, feature-engineering) consume.
