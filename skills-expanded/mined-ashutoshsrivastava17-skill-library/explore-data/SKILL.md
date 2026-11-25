---
name: explore-data
description: >
  Explore and profile a dataset to understand its shape, types, distributions, quality, and suitability for analysis.
  TRIGGER when: user asks to "explore data", "profile data", "describe dataset", "data overview",
  "what's in this data", "data quality check", "EDA", "exploratory data analysis", or "understand this dataset".
argument-hint: "<file_or_table>"
user-invocable: true
---

# Data Exploration and Profiling

You are an expert data analyst performing exploratory data analysis (EDA). When the user asks you to explore or profile a dataset, follow this structured process.

## Step 1: First Look

Perform these checks immediately upon receiving data:

```python
# Standard first-look commands
df.shape                    # (rows, columns)
df.dtypes                   # Column types
df.head(10)                 # First 10 rows
df.tail(5)                  # Last 5 rows
df.sample(5)                # Random sample
df.info(memory_usage="deep") # Memory and type summary
df.columns.tolist()         # All column names
```

### Initial Report Template

```
DATASET: <name or filename>
SHAPE: <rows> rows x <columns> columns
MEMORY: <size in MB>
SOURCE: <file path, table name, or URL>
DATE RANGE: <if temporal data exists>
```

## Step 2: Column Classification

Classify every column into one of these types:

| Type | Detection Rule | Example |
|------|---------------|---------|
| Numeric continuous | float, many unique values | revenue, temperature |
| Numeric discrete | int, few unique values | count, rating (1-5) |
| Categorical low-cardinality | string/int, < 20 unique values | status, country |
| Categorical high-cardinality | string, 20-1000 unique | city, product_name |
| Identifier | unique per row or nearly | id, email, UUID |
| Datetime | date/timestamp type or parseable string | created_at, date |
| Boolean | 2 unique values | is_active, has_paid |
| Text / free-form | string, high uniqueness, variable length | description, comment |
| Constant | 1 unique value | unused columns |
| JSON / nested | contains structured sub-data | metadata, properties |

## Step 3: Univariate Analysis

### For Each Numeric Column

| Statistic | Value |
|-----------|-------|
| Count | N (non-null) |
| Missing | N (% of total) |
| Mean | X |
| Median | X |
| Std Dev | X |
| Min | X |
| Q1 (25%) | X |
| Q3 (75%) | X |
| Max | X |
| IQR | Q3 - Q1 |
| Skewness | X (> 1 or < -1 = highly skewed) |
| Kurtosis | X (> 3 = heavy tails) |
| Zeros | N (% of total) |
| Negatives | N (% of total) |
| Distinct | N |

### For Each Categorical Column

| Statistic | Value |
|-----------|-------|
| Count | N (non-null) |
| Missing | N (%) |
| Unique | N |
| Top value | X (frequency, %) |
| Top 5 values | X1 (n%), X2 (n%), ... |
| Bottom 5 values | X1 (n%), X2 (n%), ... |
| Entropy | X (measure of uniformity) |

### For Each Datetime Column

| Statistic | Value |
|-----------|-------|
| Min date | X |
| Max date | X |
| Range | X days/months/years |
| Granularity | second / minute / hour / day / month |
| Gaps | List any gaps in expected frequency |
| Timezone | X or None |

## Step 4: Missing Data Analysis

### Missing Data Report

```
| Column | Missing Count | Missing % | Pattern |
|--------|--------------|-----------|---------|
| col_a  | 0            | 0.0%      | Complete |
| col_b  | 150          | 15.0%     | MCAR    |
| col_c  | 300          | 30.0%     | MAR     |
```

### Missingness Patterns
- **MCAR** (Missing Completely at Random): No pattern, random absence
- **MAR** (Missing at Random): Correlates with other observed variables
- **MNAR** (Missing Not at Random): Related to the missing value itself

### Actions
- < 5% missing: Safe to drop or simple impute (mean/median/mode)
- 5-30% missing: Investigate pattern; use appropriate imputation
- > 30% missing: Consider dropping column; document if kept
- Patterned missingness: Flag for domain expert review

## Step 5: Data Quality Assessment

| Check | Method | Flag If |
|-------|--------|---------|
| Duplicates | `df.duplicated().sum()` | Any exact duplicates |
| Near-duplicates | Fuzzy matching on key columns | High similarity score |
| Constant columns | `df.nunique() == 1` | Always true |
| High-null columns | null% > 50% | Review for removal |
| Type mismatches | Numeric stored as string | Any occurrence |
| Outliers | IQR method: < Q1-1.5*IQR or > Q3+1.5*IQR | Count per column |
| Invalid values | Domain checks (negative age, future dates) | Any occurrence |
| Inconsistent categories | Case/spelling variations ("US", "us", "USA") | Any occurrence |
| PII detection | Pattern match (email, phone, SSN) | Flag for privacy review |

## Step 6: Bivariate Quick Scan

If the dataset has a clear target variable, compute:

- **Numeric vs numeric**: Correlation matrix (Pearson + Spearman)
- **Numeric vs categorical**: Group-by means and box plots
- **Categorical vs categorical**: Contingency table, Cramer's V
- **Any vs target**: Mutual information score

### Correlation Flags
- |r| > 0.8: Strong correlation (potential multicollinearity)
- |r| > 0.95: Near-perfect correlation (likely redundant columns)
- Report top 10 strongest correlations

## Step 7: Output Report

Structure the exploration report as:

1. **Dataset Card** (name, shape, source, date range, memory)
2. **Column Inventory** (table of all columns with type, nulls, uniques)
3. **Key Statistics** (summary stats for numeric and categorical)
4. **Missing Data Report** (table with counts, percentages, patterns)
5. **Data Quality Flags** (duplicates, outliers, inconsistencies)
6. **Distribution Notes** (skewed columns, bimodal, uniform)
7. **Preliminary Correlations** (top relationships found)
8. **Recommendations** (what to clean, transform, or investigate next)

## Quality Checklist

- [ ] Every column has been classified and profiled
- [ ] Missing data is quantified with percentages
- [ ] Duplicates have been checked
- [ ] Data types are correct (no numbers stored as strings)
- [ ] Outliers are identified with counts
- [ ] PII columns are flagged
- [ ] At least one visualization per data type (histogram, bar chart, etc.)
- [ ] Recommendations for next steps are provided

## Edge Cases

- **Very wide data (100+ columns)**: Group by prefix, profile in batches, focus on non-null columns
- **Very long data (10M+ rows)**: Sample for profiling (1% or 100K rows), note sampling
- **All-null columns**: Flag and recommend removal
- **Mixed-type columns**: Attempt coercion, flag failures
- **Encoded data**: Detect base64, URL-encoded, or hashed columns
- **Nested JSON columns**: Flatten one level and profile sub-fields
