---
name: profile
description: "Profile data files — row counts, column types, missing values, duplicates, statistics"
argument-hint: "[dataset-name]"
risk: "safe"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: claude-haiku-4-5-20251001
context: fork
agent: general-purpose
---

# 10x Analyst — Data Profiler

Profile any CSV, Excel, or JSON dataset to understand its structure, quality, and statistics before analysis.

## Overview

Quickly assess data files without running the full pipeline. Reads from `input/<dataset>/`, produces a `data-profile.md` in `output/<dataset>/` with row/column counts, data types, missing values, duplicates, basic statistics, and a quality score.

## When to Use

- User wants to understand a dataset before committing to full analysis
- User asks "what's in this file", "how clean is this data", "describe this dataset"
- First step before running `:analyze` or `:clean`

## Path Resolution

Parse `$ARGUMENTS` to get the dataset name (e.g., `shopify-data`).
- **Input:** `input/<dataset-name>/`
- **Output:** `output/<dataset-name>/`

## Instructions

1. Resolve the dataset name from `$ARGUMENTS` and set paths:
   - Input: `input/<dataset>/`
   - Output: `output/<dataset>/`
2. Find all data files at `input/<dataset>/` using Glob patterns: `input/<dataset>/**/*.csv`, `input/<dataset>/**/*.xlsx`, `input/<dataset>/**/*.xls`, `input/<dataset>/**/*.json`
3. Create output directory: `mkdir -p output/<dataset>`
4. For each file, run this Python script:

```python
import pandas as pd
import os

def profile(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(filepath)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    elif ext == '.json':
        df = pd.read_json(filepath)
    else:
        return None

    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isna().sum().sum()
    quality_score = round((1 - missing_cells / total_cells) * 100, 1) if total_cells > 0 else 0

    print(f"## {os.path.basename(filepath)}")
    print(f"- **Rows:** {len(df):,}")
    print(f"- **Columns:** {len(df.columns)}")
    print(f"- **Duplicates:** {df.duplicated().sum():,}")
    print(f"- **Quality Score:** {quality_score}%")
    print()
    print("| Column | Type | Missing | Missing % | Unique |")
    print("|--------|------|---------|-----------|--------|")
    for col in df.columns:
        missing = df[col].isna().sum()
        missing_pct = round(df[col].isna().mean() * 100, 1)
        unique = df[col].nunique()
        print(f"| {col} | {df[col].dtype} | {missing:,} | {missing_pct}% | {unique:,} |")
    print()

    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) > 0:
        print("| Column | Min | Max | Mean | Median | Std |")
        print("|--------|-----|-----|------|--------|-----|")
        for col in num_cols:
            if not df[col].isna().all():
                print(f"| {col} | {df[col].min():.2f} | {df[col].max():.2f} | {df[col].mean():.2f} | {df[col].median():.2f} | {df[col].std():.2f} |")
        print()
```

5. Write all output to `output/<dataset>/data-profile.md`
6. Present a summary table to the user:

```
| File | Rows | Columns | Quality | Issues |
|------|------|---------|---------|--------|
```

## Examples

```bash
/10x-analyst:profile shopify-data
```

## Limitations

- Does not clean or transform data — use `:clean` for that
- Large files (>500MB) may be slow to profile
- Excel files need `openpyxl` installed

---
*Developed by [10x.in](https://10x.in) | 10x-Analyst v1.0.0*
