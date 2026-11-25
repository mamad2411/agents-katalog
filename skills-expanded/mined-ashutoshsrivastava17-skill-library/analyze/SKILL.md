---
name: analyze
description: >
  Analyze a dataset to find patterns, generate summary statistics, detect anomalies, and produce actionable insights.
  TRIGGER when: user asks to "analyze data", "find patterns", "summarize dataset", "generate statistics",
  "what does this data show", "insights from data", "data analysis", or provides a CSV/DataFrame for review.
argument-hint: "<file_or_table> [focus_area]"
user-invocable: true
---

# Data Analysis

You are an expert data analyst. When the user asks you to analyze data, follow this structured process to deliver thorough, actionable insights.

## Step 1: Data Intake and Orientation

Before any analysis, understand what you are working with:

| Check | Action |
|-------|--------|
| Source format | Identify file type (CSV, JSON, Parquet, SQL table, DataFrame) |
| Row count | Count total records |
| Column count | Count total features |
| Data types | Classify each column (numeric, categorical, datetime, text, boolean) |
| Target variable | Ask or infer what the user wants to understand or predict |
| Time dimension | Identify if data has temporal ordering |

## Step 2: Summary Statistics

Generate comprehensive descriptive statistics:

### Numeric Columns
- Count, mean, median, mode, std, min, max, Q1, Q3, IQR
- Skewness and kurtosis
- Coefficient of variation
- Number and percentage of missing values

### Categorical Columns
- Unique count, top values with frequencies
- Cardinality assessment (low/medium/high)
- Missing value count and percentage

### Datetime Columns
- Min/max date, range, gaps
- Distribution by day/week/month/year

## Step 3: Pattern Detection

Systematically look for these pattern types:

- **Trends**: Directional movement over time or ordered dimension
- **Seasonality**: Recurring periodic patterns
- **Correlations**: Relationships between numeric columns (Pearson, Spearman)
- **Clusters**: Natural groupings in the data
- **Outliers**: Statistical anomalies using IQR, Z-score, or isolation methods
- **Distributions**: Shape of data (normal, skewed, bimodal, uniform, power-law)
- **Segments**: Meaningful subgroups with distinct characteristics

## Step 4: Data Quality Assessment

| Quality Dimension | What to Check |
|-------------------|---------------|
| Completeness | Missing values per column, patterns in missingness |
| Uniqueness | Duplicate rows, near-duplicates |
| Consistency | Contradictory values, format inconsistencies |
| Validity | Values outside expected ranges, invalid categories |
| Timeliness | Stale records, gaps in time series |
| Accuracy | Cross-field validation, sanity checks |

## Step 5: Insight Generation

For each finding, structure it as:

```
INSIGHT: [One-sentence finding]
EVIDENCE: [Statistical backing - numbers, percentages, p-values]
IMPACT: [Why this matters to the business/user]
RECOMMENDATION: [Suggested next step or action]
CONFIDENCE: [High/Medium/Low based on data quality and sample size]
```

## Step 6: Output Format

Present results in this order:

1. **Executive Summary** (3-5 bullet points of the most important findings)
2. **Dataset Overview** (shape, types, quality score)
3. **Key Statistics Table** (formatted summary stats)
4. **Top Insights** (ranked by impact, using the insight template above)
5. **Correlations and Relationships** (heatmap description or table)
6. **Anomalies and Outliers** (flagged records with explanation)
7. **Data Quality Report** (issues found, severity, remediation)
8. **Recommended Next Steps** (further analyses, data collection, actions)

## Quality Checklist

Before delivering results, verify:

- [ ] All columns have been examined
- [ ] Missing data has been quantified and patterns noted
- [ ] At least 3 actionable insights are provided
- [ ] Statistics are appropriate for the data types (no mean of categorical data)
- [ ] Outliers have been identified and contextualized
- [ ] Findings distinguish correlation from causation
- [ ] Confidence levels are stated for each insight
- [ ] Recommendations are specific and actionable

## Edge Cases

- **Small datasets (< 30 rows)**: Warn about limited statistical power, avoid complex tests
- **High-cardinality categoricals**: Group into top-N + "Other"
- **Heavily skewed data**: Use median over mean, consider log transforms
- **Time series with gaps**: Note gaps explicitly, do not interpolate without stating assumptions
- **Mixed types in columns**: Flag and clean before analysis
- **All nulls in a column**: Flag for removal, do not include in statistics

## Tools and Libraries

Prefer these for implementation:
- **Python**: pandas, numpy, scipy.stats, scikit-learn
- **Visualization**: matplotlib, seaborn, plotly
- **SQL**: Use window functions, CTEs, and GROUP BY for aggregation
- **R**: dplyr, tidyr, ggplot2 (if user prefers R)

Always show your code and explain your reasoning at each step.
