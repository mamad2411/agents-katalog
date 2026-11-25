---
name: profile-dataframe
description: Profiles a pandas DataFrame for dtypes, nulls, outliers and duplicates, then suggests exact pandas fixes for each issue.
disable-model-invocation: true
---

Profile the pandas DataFrame: $ARGUMENTS (a variable, a file that builds it, or a file to load).

1. Find where the frame is created. Write a small script or use the notebook to load it without altering the source. Never modify the original frame; work on `df.copy()`.
2. Print `df.shape`, `df.dtypes`, `df.memory_usage(deep=True)` and `df.isna().mean()` sorted high to low.
3. For object columns, check for numbers or dates stored as strings, mixed case, leading and trailing whitespace, and low cardinality that should be `category`.
4. For numeric columns, find outliers by the 1.5 IQR rule and impossible values. Show `df.describe()`.
5. Count `df.duplicated().sum()`, and also duplicates on the likely key columns.
6. Check index uniqueness and sort order, and datetime columns for time zone and gaps.

Report a table: column, issue, evidence, and a one-line fix such as `df["price"] = pd.to_numeric(df["price"].str.replace("$",""))`. Ask whether to apply fixes into a cleaning function.
