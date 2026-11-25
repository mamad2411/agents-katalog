---
name: wrangle-tabular-data
description: Cleans, transforms, joins, reshapes, and aggregates tabular data (CSV/Parquet/DataFrames) with pandas, handling missing values, type coercion, dedup, and time-series resampling.
when_to_use: When the user needs to clean or transform a dataset in code — fix missing/dirty values, coerce types, dedup, join/merge tables, pivot/melt/reshape, group-and-aggregate, or resample a time series, typically producing a cleaned CSV/DataFrame for downstream use.
---

## When to Use

Use this when transforming a dataset **in code** and emitting a cleaned artifact (CSV/Parquet/DataFrame) for a downstream step.

Triggers: fix missing/dirty values, coerce dtypes, dedup, join/merge tables, pivot/melt/reshape, groupby-aggregate, rolling/window, or resample a time series.

Not this skill:
- Producing a formatted `.xlsx` for a human to open → use **build-spreadsheet** (this skill is a code-level transform, the output is data not presentation).
- Only inspecting/summarizing a dataset without changing it → use **profile-dataset** (transform vs. inspect).

## Steps

1. **Load with explicit dtypes — never trust the inferrer.**
   - CSV: `pd.read_csv(path, dtype={...}, parse_dates=[...], na_values=["", "NA", "null", "-", "N/A"], keep_default_na=True)`. Pass `dtype=str` for ID/code/zip columns to stop them becoming floats (`007` → `7.0`, leading zeros gone forever).
   - Parquet: `pd.read_parquet(path)` already carries a schema — read it, don't re-coerce blindly.
   - Capture `df.shape` and `df.dtypes` immediately; these are the baseline for the transformation log.

2. **Diagnose before touching anything.** Run `df.isna().sum()`, `df.nunique()`, and `df.dtypes`. For each `object` column you expect numeric/date, check why it's `object` (usually one stray non-numeric value or a thousands separator). Decide the strategy per column up front — do not clean ad hoc.

3. **Coerce types deliberately.**
   - Numeric: `pd.to_numeric(s, errors="coerce")` then inspect the new NaNs (those are your dirty rows — log how many). Strip `$`, `,`, `%` first: `s.str.replace(r"[,$%]", "", regex=True)`.
   - Datetime: `pd.to_datetime(s, errors="coerce", utc=True)` — force UTC so you never carry tz-naive timestamps into a resample/merge. If source is local time, localize then convert.
   - Categorical: convert low-cardinality string columns with `.astype("category")` (memory + faster groupby).

4. **Clean values.**
   - Missing: pick per column — `dropna(subset=[...])` for required keys, `fillna(value)` for known defaults, `ffill`/`bfill` only for ordered/time-series data. State which strategy and why in the log. Never blanket `fillna(0)` across the frame.
   - Strings: `s.str.strip()`, normalize case (`.str.lower()`), collapse whitespace (`.str.replace(r"\s+", " ", regex=True)`) before dedup/join — invisible trailing spaces silently break key matches.
   - Outliers: only act if asked; clip (`.clip(lower, upper)`) or flag, don't silently drop.

5. **Dedup with intent.** `df.duplicated(subset=[keys]).sum()` first to know the count. Then `df.drop_duplicates(subset=[keys], keep="first")`. Choosing `keep` matters when non-key columns differ — sort first if "latest wins" (`sort_values("ts").drop_duplicates(subset=keys, keep="last")`).

6. **Merge/join — always validate cardinality.** Use `validate=` to make pandas raise on a bad assumption: `df.merge(other, on="id", how="left", validate="m:1")`. Options: `1:1`, `1:m`, `m:1`, `m:m`. After merge, assert row count didn't explode (`assert len(out) <= len(left) * expected`). Check `indicator=True` to count unmatched keys (`how="left"` + `_merge == "left_only"`).

7. **Reshape.**
   - Long→wide: `df.pivot_table(index=..., columns=..., values=..., aggfunc=...)` (use `pivot_table` not `pivot` so duplicate index/column pairs aggregate instead of raising).
   - Wide→long: `df.melt(id_vars=[...], value_vars=[...], var_name=..., value_name=...)`.
   - Aggregate: `df.groupby(keys, dropna=False).agg(out_col=("src", "func"))` — named aggregation keeps column names clean; `dropna=False` so NaN keys aren't silently dropped.
   - Window: sort by the order column first, then `.rolling(window)` / `.expanding()` / `.shift()`.

8. **Time-series resample.** Index must be a tz-aware DatetimeIndex (`df.set_index("ts")`). Then `df.resample("1h").agg(...)` (downsample) or `.resample("1min").interpolate()` / `.asfreq()` (upsample). Per-group: `df.groupby("id").resample("1D").sum()`. Confirm the freq string is right (`"h"`, `"D"`, `"W"`, `"M"`, `"MS"` differ).

9. **Big files — stay in memory budget.**
   - Read in chunks: `for chunk in pd.read_csv(path, chunksize=500_000): ...` and reduce per chunk.
   - Set `dtype` + `category` at read time (biggest single win).
   - Select columns with `usecols=[...]` — never load columns you won't use.
   - If pandas still won't fit, switch the load+filter step to `pyarrow`/`polars` and hand a smaller frame back to pandas.

10. **Output + transformation log.** Write the artifact (`to_parquet` preferred — preserves dtypes; `to_csv(index=False)` if a CSV is required). Then emit a short log: rows in→out, columns dropped/added, dtype changes, NaNs coerced, duplicates removed, join match rate. This is the deliverable's audit trail, not optional.

## Common Errors

- **Silent 1:many join blow-up.** A left join on a non-unique right key multiplies rows. Symptom: output row count jumps, later aggregates double-count. Fix: always pass `validate="m:1"` (or the correct cardinality) so pandas raises instead of silently fanning out.
- **Mixed-type column read as `object`.** One `"N/A"` in a numeric column makes the whole column `object`; arithmetic then fails or coerces weirdly. Fix: `pd.to_numeric(errors="coerce")` and inspect the produced NaNs.
- **Leading zeros / big-int IDs corrupted on load.** `read_csv` infers `int64`/`float64` and drops leading zeros or rounds 19-digit IDs. Fix: `dtype=str` for any code/ID/zip/phone column.
- **Tz-naive timestamps breaking resample/merge.** Mixing naive and aware datetimes raises or aligns wrong across DST. Fix: `utc=True` on every `to_datetime`; localize source local-time explicitly.
- **`pivot` raising on duplicates.** `df.pivot` errors on duplicate index/column pairs. Fix: use `pivot_table` with an explicit `aggfunc`.
- **`groupby` silently dropping NaN keys.** Default `dropna=True` makes rows with NaN group keys vanish from the result. Fix: `groupby(..., dropna=False)` when NaN is a real category.
- **`fillna`/`ffill` on unsorted data.** Forward-fill before sorting propagates the wrong value. Fix: `sort_values` by the order/time column before any fill or rolling op.
- **Chained-assignment / `SettingWithCopyWarning`.** Edits on a slice don't stick. Fix: operate on `.copy()` or use `.loc[mask, col] = ...`.

## Verify

- Row count: `len(out)` matches expectation (joins didn't explode, dedup removed the diagnosed count, filters dropped what you intended).
- Dtypes: `out.dtypes` are final (no stray `object` where numeric/datetime expected); IDs still strings with leading zeros intact.
- Keys: `out.duplicated(subset=keys).sum() == 0` after dedup; join match rate logged (unmatched-key count is acceptable and known, not surprising).
- No accidental NaN: `out.isna().sum()` only shows NaNs you chose to keep.
- Time series: index is tz-aware DatetimeIndex, no gaps/duplicates in the resampled frequency.
- Round-trip: re-read the written artifact and confirm `shape` + `dtypes` survive (Parquet keeps them; CSV will re-infer — re-pass `dtype` if the CSV is the handoff format).
- Transformation log exists and reconciles in→out counts.
