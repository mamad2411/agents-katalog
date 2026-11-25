---
name: pandas-data-cleaning
description: Cleans messy DataFrames with typed columns, explicit null handling and assertions. Use it when raw CSV or Excel data needs to become trustworthy.
---

# Pandas data cleaning

Every change to the data must be explicit, counted and checked.

## Steps

1. Load with intent: pass `dtype=` for IDs and codes (keep them as strings so leading zeros survive), `parse_dates=` for known dates, and `na_values=` for the file's own null markers such as "N/A" or "-".
2. Look before you fix: `df.info()`, `df.isna().sum()`, `df.nunique()`, and `df.describe(include="all")`. Print the number of rows at the start.
3. Normalize text columns: `.str.strip()`, consistent case, and one canonical spelling map for categories.
4. Convert types explicitly with `pd.to_numeric(errors="coerce")` and `pd.to_datetime(errors="coerce")`, then count what became null and inspect those rows before deciding.
5. Decide each null on purpose: drop, fill with a stated default, or keep as `pd.NA` with a nullable dtype (`Int64`, `string`, `boolean`).
6. Deduplicate on a named key with `drop_duplicates(subset=[...], keep=...)` and say which row wins and why.
7. Finish with assertions: unique key, no nulls in required columns, values inside allowed ranges, expected dtypes.

## Rules

- Never use `inplace=True` or chained assignment. Return a new frame from a pure function.
- Never drop rows silently. Log how many were removed per step.
- Do not guess a date format; use an explicit `format=`.

## Report

Rows in and out, per step counts, columns whose type changed, and any rows set aside for a human to review.
