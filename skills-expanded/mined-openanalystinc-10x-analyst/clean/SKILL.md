---
name: clean
description: "Clean and transform data files — fix types, handle missing values, remove duplicates"
argument-hint: "[dataset-name]"
risk: "safe"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: claude-haiku-4-5-20251001
context: fork
agent: general-purpose
---

# 10x Analyst — Data Cleaner

Clean and transform raw data files into analysis-ready datasets.

## Overview

Automated data cleaning pipeline: parse dates, convert currencies, standardize column names, handle missing values, remove duplicates. Reads from `input/<dataset>/`, outputs cleaned files to `output/<dataset>/cleaned-data/`.

## When to Use

- User says "clean this data", "fix this dataset", "prepare this for analysis"
- Data has known quality issues (missing values, wrong types, duplicates)
- Before running `:analyze` manually on pre-cleaned data

## Path Resolution

Parse `$ARGUMENTS` to get the dataset name.
- **Input:** `input/<dataset-name>/`
- **Output:** `output/<dataset-name>/cleaned-data/`

## Instructions

1. Resolve the dataset name from `$ARGUMENTS` and set paths
2. Find all data files at `input/<dataset>/` using Glob
3. Create output directory: `mkdir -p output/<dataset>/cleaned-data`
4. For each file, apply these cleaning steps in Python:

```python
import pandas as pd
import re
import os

def clean_file(filepath, output_dir):
    ext = os.path.splitext(filepath)[1].lower()
    basename = os.path.basename(filepath)

    if ext == '.csv':
        df = pd.read_csv(filepath)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    elif ext == '.json':
        df = pd.read_json(filepath)
    else:
        return

    original_rows = len(df)

    # 1. Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r'[^a-z0-9]+', '_', regex=True).str.strip('_')

    # 2. Drop exact duplicates
    df.drop_duplicates(inplace=True)

    # 3. Parse date columns (columns with 'date', 'time', 'created', 'updated' in name)
    date_cols = [c for c in df.columns if any(kw in c for kw in ['date', 'time', 'created', 'updated'])]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # 4. Convert currency strings to float
    for col in df.select_dtypes(include='object').columns:
        sample = df[col].dropna().head(20).astype(str)
        if sample.str.match(r'^\$?[\d,]+\.?\d*$').mean() > 0.5:
            df[col] = df[col].astype(str).str.replace(r'[$,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 5. Handle missing values
    for col in df.columns:
        missing_pct = df[col].isna().mean()
        if missing_pct > 0.5:
            df.drop(columns=[col], inplace=True)
        elif missing_pct > 0:
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna('Unknown', inplace=True)

    # 6. Save cleaned file
    output_path = os.path.join(output_dir, basename)
    if ext == '.json':
        df.to_json(output_path, orient='records', indent=2)
    else:
        df.to_csv(output_path, index=False)

    cleaned_rows = len(df)
    print(f"{basename}: {original_rows} -> {cleaned_rows} rows ({original_rows - cleaned_rows} removed)")
```

5. Write a cleaning summary to `output/<dataset>/cleaning-log.md`
6. Present results table:

```
| File | Original Rows | Cleaned Rows | Removed | Actions Taken |
|------|--------------|-------------|---------|---------------|
```

## Examples

```bash
/10x-analyst:clean shopify-data
```

## Limitations

- Aggressive missing value handling: >50% missing columns are dropped
- Currency detection is heuristic-based — may miss non-US formats
- Does not handle multi-sheet Excel files (reads first sheet only)

---
*Developed by [10x.in](https://10x.in) | 10x-Analyst v1.0.0*
