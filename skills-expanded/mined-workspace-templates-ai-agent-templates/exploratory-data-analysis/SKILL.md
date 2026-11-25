---
name: exploratory-data-analysis
description: Profiles a new dataset, finds quality problems and summarizes findings with plots. Use it before modeling or reporting on data you have not seen yet.
---

# Exploratory data analysis

Understand the data before drawing a conclusion from it. Report what you saw, separate from what you suspect.

## Steps

1. State the unit of a row ("one order line", "one user per day") and the target question. If you cannot name the row unit, find out before going on.
2. Inspect structure: row and column counts, dtypes, memory, a random sample of 10 rows (not just `head`), and the date range if any.
3. Check quality: nulls per column as a percentage, duplicate rows and duplicate keys, constant columns, impossible values (negative ages, future dates), and inconsistent categories.
4. Describe each numeric column: min, quartiles, max, skew, and outliers by the 1.5 IQR rule. Draw a histogram or box plot for the important ones.
5. Describe categoricals: cardinality, top values, and rare levels. Use a bar chart for the leading categories.
6. Look at relationships: a correlation matrix for numerics, group means against the target, and a time series plot for anything dated. Remember correlation is not cause.
7. Check for leakage: any column that would not exist at prediction time.
8. Save plots to `eda/` as PNG files with titles and axis labels.

## Rules

- Never modify the source data; work on a copy.
- Report numbers with their denominators.

## Report

Open with the 3 findings that change what you will do next, then data quality problems ranked by impact, then plots with one sentence each, then open questions.
