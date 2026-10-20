---
skillx.name: data_cleaning
skillx.purpose: Clean messy tabular datasets (demographic surveys and transaction records) to prepare them for time-series analysis, anomaly detection, and causal inference. Handle duplicates, missing values, inconsistent formatting, outliers, and text processing issues that prevent downstream statistical analysis.
skillx.scope_in: |
  - Deduplication based on logical keys and downstream requirements
  - Missing value handling (drop vs impute) based on column criticality and sample size impact
  - Text processing (extract numbers, clean whitespace, standardize formats)
  - Outlier handling (cap vs remove) based on statistical methods and downstream sensitivity
  - Data type conversions and date parsing for time-series work
  - Ensuring referential integrity across related datasets (e.g., survey IDs linking to transactions)
skillx.scope_out: |
  - Feature engineering or derived variable creation (separate step)
  - Aggregation or reshaping for specific analyses (e.g., DID panel structure)
  - Statistical modeling or causal inference itself
  - Data validation rules or schema enforcement beyond basic type checking
  - Performance optimization for very large datasets (>10M rows)
skillx.requires: |
  - pandas for dataframe operations
  - Understanding of the downstream task to make informed cleaning decisions
  - Knowledge of which columns are critical vs optional for the analysis
  - Sample size considerations (cost of dropping rows vs imputing)
skillx.preferred_tools: |
  - `df.drop_duplicates(subset=...)` for deduplication with logical keys
  - `df.dropna(subset=...)` for critical columns where imputation would harm analysis
  - `df.fillna()` with median/mode for non-critical columns with sufficient independence
  - `sklearn.impute.KNNImputer` when target column values can be inferred from related columns
  - `pd.to_datetime()` with error handling for date columns
  - IQR-based methods (winsorization or removal) for outlier handling
  - String methods (`str.extract()`, `str.strip()`, `str.lower()`) for text cleaning
skillx.risks: |
  - Dropping too many rows due to aggressive missing value or outlier removal can harm sample size and statistical power
  - Imputing critical outcome variables or treatment indicators can introduce bias
  - Removing outliers without understanding if they represent real signal vs noise can distort conclusions
  - Inconsistent cleaning logic between related datasets can break joins (e.g., survey IDs not matching transactions)
  - Over-cleaning can remove legitimate variation needed for causal analysis
  - Text processing that loses semantic information (e.g., extracting only numbers when categories matter)
skillx.examples: |
  Remove duplicates by logical key:
  ```python
  df.drop_duplicates(subset=['customer_id', 'order_date'], keep='first')
  ```

  Drop rows with missing critical identifiers:
  ```python
  df.dropna(subset=['customer_id', 'order_date'], inplace=False)
  ```

  Impute non-critical numerical columns with median:
  ```python
  df['income'].fillna(df['income'].median(), inplace=True)
  ```

  Cap outliers using IQR (winsorization to preserve sample size):
  ```python
  Q1, Q3 = df['amount'].quantile([0.25, 0.75])
  IQR = Q3 - Q1
  lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
  df['amount'] = df['amount'].clip(lower, upper)
  ```
---

# Guidance

## Decision Framework for Cleaning Operations

**Deduplication**: Always check for duplicates first. Examine the data's logical structure and downstream goals:
- For demographic/survey data: typically one row per respondent (duplicate Survey ResponseIDs should be removed)
- For transaction data: multiple transactions per user are legitimate (do NOT remove based on user ID alone)
- Use appropriate subset of columns that define uniqueness for the data type

**Missing Value Strategy**:
1. Assess criticality: Will missing values in this column directly harm downstream analysis performance?
2. Assess cost: How many rows would be lost by dropping vs potential bias from imputing?
3. Decision tree:
   - Critical columns (IDs, dates, outcome variables): drop rows with missingness
   - Non-critical numerical with sufficient independence: impute with median
   - Non-critical categorical with sufficient independence: impute with mode
   - Non-critical with strong relationships to other columns: consider KNN imputation
4. For KNN imputation: only use when you can identify semantically related columns (e.g., income can be inferred from age + education)

**Text Processing**: Preview column values to determine if cleaning is needed:
- Extract numbers from mixed text/number fields if downstream requires numeric values
- Standardize whitespace and case for categorical fields used in joins or grouping
- Remove special characters only if they interfere with analysis (preserve meaning otherwise)

**Outlier Handling**:
1. Understand if outliers represent real signal or data quality issues
2. Assess sample size impact of removal
3. Decision tree:
   - If sample size is large and outliers are clearly erroneous: remove using IQR or Z-score
   - If sample size is precious or outliers might be real: cap using winsorization (IQR method)
   - Default multiplier: 1.5 for IQR, 3.0 for Z-score
4. For causal inference work: be cautious about removing extreme values that may represent legitimate treatment effects

## Implementation Pattern

For complex cleaning pipelines:
1. Read and preview data first (`df.head()`, `df.info()`, `df.describe()`)
2. Check for duplicates and understand their source
3. Identify missing value patterns (`df.isnull().sum()`)
4. Clean in stages: identifiers → critical fields → non-critical fields → outliers
5. Verify referential integrity between related datasets before proceeding to merges
6. Document the number of rows affected by each operation
7. Save cleaned outputs with clear naming (e.g., `survey_cleaned.csv`, not `survey_v2.csv`)

## Common Patterns for This Task Domain

**Survey/Demographic Data**:
- Expect one row per respondent
- Check for duplicate Survey ResponseIDs and remove
- Demographic columns may have missingness requiring imputation
- Verify all IDs follow expected format (e.g., start with 'R_')

**Transaction/Purchase Data**:
- Multiple transactions per user are normal (do NOT deduplicate by user)
- Date columns must be parseable and within expected range
- Price/amount columns should be positive and within reasonable bounds
- Category columns should not have nulls (either drop rows or impute with mode)
- Verify Survey ResponseIDs link to the demographic data

**Cross-Dataset Validation**:
- After cleaning both datasets, verify that transaction IDs exist in demographic data
- Filter transactions to only include users present in cleaned demographics if required for analysis
- Ensure date ranges align with analysis requirements (e.g., 2019-2020 for this task)

# Notes for Agent

1. **Always preview before cleaning**: Use `df.head()`, `df.info()`, `df.describe()`, and `df.isnull().sum()` to understand the data structure and quality issues before applying any cleaning operations.

2. **Document your decisions**: For each cleaning step, note why you chose that approach (e.g., "Dropping rows with missing Category because it's required for downstream aggregation and only affects 7% of data").

3. **Check referential integrity early**: Before proceeding to analysis steps, verify that IDs in transaction data exist in demographic data. This prevents downstream join issues.

4. **Be conservative with outlier removal**: For causal inference tasks, extreme values may represent real effects. Prefer winsorization (capping) over removal unless outliers are clearly data errors.

5. **Validate cleaning results**: After each major operation, check the resulting dataset size and summary statistics to ensure cleaning didn't inadvertently remove too much data or introduce new issues.

6. **Save intermediate outputs**: Write cleaned datasets to the specified output paths as soon as cleaning is complete, before proceeding to analysis steps. This enables inspection and debugging.

7. **Handle date parsing carefully**: Use `pd.to_datetime()` with `errors='coerce'` to identify unparseable dates, then decide whether to drop or fix them. Verify all dates fall within expected ranges for the analysis.

8. **KNN imputation requires setup**: When using KNN imputation, explicitly specify which features to use for inference and ensure they are numeric. Convert categorical features to numeric first if needed.
