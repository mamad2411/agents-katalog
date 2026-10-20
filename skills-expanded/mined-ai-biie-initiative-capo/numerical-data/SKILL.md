---
name: numerical-data-processing
description: >
  Generic biological numerical data processing skill. Loads tabular datasets,
  validates numeric feature and target columns, applies minimal safe preprocessing,
  computes required statistics before modeling, and returns reproducible,
  split-aware, leakage-checked outputs suitable for standard ML pipelines.

  Use this skill when the user asks to:
  (1) Prepare biological or medical numerical data for training or evaluation
  (2) Clean, inspect, validate, filter, impute, or normalize tabular measurements
  (3) Produce feature matrices and targets for classification or regression
license:
metadata:
  version: "0.1"
user-invokable: true
compatibility: >
  Works offline. Uses local tabular parsing and pandas-based preprocessing only.
---

# Numerical Data Processing

Process biological or medical tabular numerical datasets into clean, reproducible, model-ready tables.

Supported use cases include biomarker prediction, diagnosis classification, assay readout modeling, risk prediction, omics-derived tabular features, phenotype prediction, and other biology tasks where the inputs are already numerical or should become numerical with simple coercion.

Stay generic by default. Do not apply disease-specific, assay-specific, or model-specific assumptions unless the user or dataset clearly requires them.

## When to use

Use this skill when the task involves:
- preparing tabular numerical data for training or fine-tuning
- cleaning biological feature matrices before modeling
- validating feature columns, targets, splits, ids, or group columns
- handling missing values, impossible values, duplicates, or leakage risks
- standardizing mixed tabular inputs into one normalized dataset

## What this skill must do

This skill must:
1. load supported tabular inputs
2. select only requested feature columns and target columns when provided
3. coerce feature columns to numeric safely
4. coerce the target column to the expected type safely
5. compute statistics before declaring readiness
6. preserve row alignment between features and targets
7. handle missing values with simple, explicit, reproducible rules
8. detect leakage risks such as duplicate rows or group overlap across splits
9. emit cleaned artifacts plus a manifest and warnings

This skill must not:
- silently use columns outside the requested feature set
- silently change target semantics
- silently create train/val/test splits unless explicitly requested
- silently drop rows without reporting counts
- add unnecessary feature engineering
- declare the dataset ready without reporting statistics

## Supported inputs

- CSV
- TSV
- Parquet
- JSON records
- Hugging Face datasets containing tabular columns

## Expected inputs

The skill may receive:
- a pandas DataFrame
- a path to a tabular file
- a dataset identifier plus a split
- an explicit list of feature columns
- a target column
- optional id, split, and group columns

## Normalized schema

Normalize data into a table with these columns or roles when possible:

- `sample_id`: stable row identifier if available
- `split`: split name if present
- `group`: grouping variable for leakage checks if present
- `feature_*`: selected numerical input columns
- `target`: cleaned target column
- additional metadata columns preserved only if useful for audit or leakage checks

## Required preprocessing

Apply these defaults unless the user requested otherwise.

### 1) Table normalization
- load the dataset into pandas
- lowercase column names only if renaming is allowed; otherwise preserve original names and track canonical aliases separately
- strip surrounding whitespace from column names
- resolve duplicate column names with a warning
- preserve original row index until final output

### 2) Column selection
- if `feature_columns` is provided, use only the intersection with existing columns
- if some requested feature columns are missing, report them explicitly
- if no requested feature columns remain, return an empty feature table aligned to the filtered target
- never pull in extra columns just because they look useful
- if `target_column` is missing, return a hard error

### 3) Numeric coercion
For every selected feature column:
- apply numeric coercion using:
  - `pd.to_numeric(X[col], errors="coerce")`
- preserve the column as a pandas Series in a DataFrame
- do not one-hot encode
- do not create interactions
- do not bin values unless explicitly requested

For the target column:
- apply numeric coercion using:
  - `pd.to_numeric(y, errors="coerce")`
- drop rows where the target is missing after coercion
- keep `X` and `y` aligned after filtering

### 4) Missing-value handling
Use simple, safe rules:
- never impute the target
- for feature columns:
  - if a column is entirely missing after coercion, fill with `0.0` only if returning a usable matrix is required and report this clearly
  - otherwise impute missing values with the column median
- report missingness counts before and after imputation
- never use target-aware imputation
- do not use KNN, iterative imputation, or model-based imputation unless explicitly requested

### 5) Impossible-value handling
Check for values that are numerically valid but biologically implausible or structurally suspicious.

Use this rule:
- only recode suspicious values to missing if the feature meaning strongly justifies it
- examples include measurements recorded as `0` when `0` is not physiologically possible
- do not apply such recoding to all columns by default
- require either:
  - explicit user instruction, or
  - strong dataset evidence from column meaning and summary statistics

When applied:
- convert those values to missing before imputation
- report exactly which columns were affected and how many rows changed

### 6) Duplicate handling
- detect exact duplicate rows across all selected columns
- detect duplicate sample ids if an id column exists
- do not drop duplicates silently
- report duplicate counts
- only remove duplicates if explicitly requested or clearly required by the downstream task

### 7) Split and group handling
If a split column exists:
- use it as provided
- normalize obvious aliases only when unambiguous:
  - `validation` -> `val`
  - `dev` -> `val`
- do not reshuffle or recreate splits unless explicitly requested

If a group column exists:
- check whether groups overlap across splits
- warn if the same group appears in multiple splits

## Required statistics

Return these at minimum.

### Dataset statistics
- total rows before filtering
- total rows after target filtering
- total selected feature columns
- list of missing requested feature columns
- dtype summary for selected columns
- null counts per selected feature column before imputation
- null counts per selected feature column after imputation
- exact duplicate row count

### Feature statistics
For each selected feature column:
- non-null count
- missing count
- min
- median
- mean
- max
- standard deviation
- count of zeros
- count of negative values
- count of non-finite values if present before cleanup

### Target statistics
- non-null count
- missing count after coercion
- unique values
- class counts for classification targets
- prevalence for binary targets

### Split statistics
If split exists, report per split:
- row count
- target class counts if classification
- feature missingness summary
- duplicate count within split if checked

### Group leakage statistics
If group exists, report:
- number of unique groups
- groups appearing in more than one split
- count of affected rows

## Required validations

Do not mark the dataset ready if any of the following holds:
- the target column is missing
- all target values are missing after coercion
- no valid feature columns remain after selection
- all selected feature columns are entirely missing after coercion and no fallback policy is allowed
- target semantics are ambiguous for the intended task
- severe split or group leakage is detected and not acknowledged

Return a warning-heavy result in these cases.

## Task-type handling

Infer or accept one of:
- `binary_classification`
- `multiclass_classification`
- `regression`
- `unknown`

Use these rules:
- if target has exactly two numeric values after filtering, binary classification is allowed
- if target has more than two discrete integer-like values, multiclass classification may be allowed
- if target is continuous, regression may be allowed
- if unclear, report `unknown` and do not force a task type

## Output artifacts

Produce these artifacts when possible:
- cleaned feature table: CSV or Parquet
- cleaned target table or Series export: CSV or Parquet
- stats report: JSON or Markdown
- manifest: JSON with inputs, selected columns, transforms, and warnings

The manifest should include:
- input source names
- selected feature columns
- missing requested feature columns
- selected target column
- task type guess
- preprocessing steps applied
- rows removed at each stage
- columns imputed
- warnings generated

## Output format

Return a result with this exact structure.

**Numerical Data Processing Result**
- inputs_detected:
  - source: …
  - format: …
  - revision/hash: …
- schema:
  - feature_columns_requested: […]
  - feature_columns_used: […]
  - feature_columns_missing: […]
  - target_column: …
  - id_column: …
  - split_column: …
  - group_column: …
  - inferred_task_type: …
- stats_report:
  - n_rows_raw: …
  - n_rows_after_target_filter: …
  - feature_dtype_summary: …
  - feature_missingness_before: …
  - feature_missingness_after: …
  - feature_summary_stats: …
  - target_summary: …
  - duplicate_summary: …
  - per_split_summary: …
  - group_leakage_summary: …
- cleaned_dataset:
  - x_shape: …
  - y_shape: …
  - imputation_applied: …
  - impossible_value_rules_applied: …
  - filtering_applied: …
- artifacts:
  - feature_table: …
  - target_table: …
  - stats_report: …
  - manifest: …
- warnings:
  - …
- next_step:
  1. …
  2. …
  3. …

## Exact implementation cues

When writing preprocessing code, do the following in order:

1. create `valid_feature_columns = [c for c in feature_columns if c in df.columns]`
2. create `X = df.loc[:, valid_feature_columns].copy()`
3. create `y = df[target_column]`
4. convert every feature column with:
   - `X[col] = pd.to_numeric(X[col], errors="coerce")`
5. convert target with:
   - `y = pd.to_numeric(y, errors="coerce")`
6. create a valid-target mask:
   - `valid_y_mask = y.notna()`
7. filter both:
   - `X = X.loc[valid_y_mask].copy()`
   - `y = y.loc[valid_y_mask].copy()`
8. compute feature missingness
9. optionally recode clearly impossible values to missing only when justified
10. impute feature missing values columnwise using median
11. keep `X` as a pandas DataFrame
12. keep `y` as a pandas Series
13. return `(X, y)`

## Error patterns

Prefer these exact messages when applicable.

- `ERROR: target column is missing`
- `ERROR: all target values are missing after numeric coercion`
- `ERROR: no requested feature columns were found`
- `ERROR: no usable feature columns remain after preprocessing`
- `ERROR: inferred task type is ambiguous`
- `WARNING: some requested feature columns are missing`
- `WARNING: feature columns contain high missingness`
- `WARNING: exact duplicate rows detected`
- `WARNING: duplicate sample ids detected`
- `WARNING: groups overlap across splits`
- `WARNING: suspicious impossible values were recoded to missing`

## Commands

Use simple commands only when execution is required and the environment supports them.

```bash
python script.py --input data.csv --target outcome --features age bmi glucose
````

```bash
python - <<'PY'
import pandas as pd

df = pd.read_csv("data.csv")
X = df[["feature1", "feature2"]].copy()
for col in X.columns:
    X[col] = pd.to_numeric(X[col], errors="coerce")
y = pd.to_numeric(df["target"], errors="coerce")
mask = y.notna()
X = X.loc[mask].copy()
y = y.loc[mask].copy()
for col in X.columns:
    X[col] = X[col].fillna(X[col].median())
PY
```

Do not mention extra tools, package managers, or framework-specific workflows unless they are already required by the user's environment.

## Production constraints

Always respect these:

* prefer deterministic preprocessing
* preserve target semantics
* never hide dropped-row counts
* never use columns outside the requested feature set
* never claim the data is ready without reporting statistics
* keep artifacts small, standard, and inspectable
* default to CSV, Parquet, JSON, and Markdown outputs
* avoid unnecessary feature engineering
* avoid unnecessary exploration or extra processing passes
* do not invent project conventions or hidden biological assumptions

## Internal flow

1. detect input format
2. load data
3. select requested columns
4. coerce features and target to numeric
5. filter rows with missing target
6. compute statistics
7. recode clearly impossible values only if justified
8. impute feature missing values with medians
9. validate alignment and readiness
10. emit cleaned artifacts and warnings

## Guardrails

Do not:

* add unnecessary requirements
* assume disease-specific rules for all datasets
* impute targets
* normalize, scale, or rebalance unless explicitly requested
* introduce broad feature engineering
* use the target to engineer features
* expand the workflow beyond what is needed to make the dataset usable

