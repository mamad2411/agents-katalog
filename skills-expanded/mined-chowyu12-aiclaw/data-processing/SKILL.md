---
name: Data Processing
description: Import, clean, transform, analyze, and export CSV/JSON/Excel data. Use code_interpreter with read/write for end-to-end data pipelines; split large workloads with sub_agent when useful.
---

# Data Pipeline (data-pipeline)

Act as a data engineering specialist. When the user provides data files or a processing request, write and run code to complete the pipeline.

## Workflow

1. **Understand the data**: use `read` to inspect the first rows and learn the schema.
2. **Confirm the goal**: clarify the requested cleaning, transformation, analysis, merge, or export.
3. **Write the script**: use `code_interpreter` to run Python for the data processing task.
4. **Validate results**: show a sample of the processed output for confirmation.
5. **Export files**: use `write` to save the final output in the requested format.

## Large Workloads

For multiple files or multi-dimensional analysis, use `sub_agent` to process independent parts in parallel:

```text
sub_agent(prompt: "Read sales_2024.csv, calculate monthly sales totals, and return JSON.")
sub_agent(prompt: "Read users.csv, group users by region, calculate active rate, and return JSON.")
```

The parent Agent should collect results, run cross-analysis, and produce the final report.

## Common Tasks

### Data Cleaning

- Deduplication, missing-value handling, and type conversion
- Outlier detection and handling
- Field normalization, including dates and encodings

### Data Transformation

- CSV, JSON, and Excel conversion
- Field mapping, splitting, and merging
- Pivoting and aggregation

### Statistical Analysis

- Descriptive statistics such as mean, median, standard deviation, and percentiles
- Grouped statistics and cross-tab analysis
- Trend analysis and year-over-year / period-over-period comparisons

### Visualization

- Generate charts with matplotlib or plotly via `code_interpreter`
- Produce statistical summaries and reports

## Coding Guidelines

- Prefer Python with pandas.
- Add validation steps for row count, column count, and missing-value statistics.
- Read large files in chunks to avoid memory pressure.
- Print samples and summary statistics before final export.
