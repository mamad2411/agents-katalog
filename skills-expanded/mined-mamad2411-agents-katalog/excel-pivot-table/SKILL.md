---
name: excel-pivot-table
description: Design Excel pivot tables, spreadsheet summaries, grouping fields, calculated measures, slicers, and pivot-style analysis layouts.
---

# excel-pivot-table

## Purpose

Turn tabular data into a pivot-style summary that is easy to review or build in Excel.

## Workflow

1. Identify source columns, row grain, target question, measures, dimensions, and filters.
2. Choose rows, columns, values, filters, slicers, and calculated measures.
3. Define aggregation rules such as sum, count, average, min, max, distinct count, or rate.
4. Add layout, sorting, subtotal, and formatting guidance.
5. Provide a CSV/Markdown fallback if spreadsheet tooling is unavailable.

## Required Checks

- Do not assume hidden columns or clean data.
- Do not mix incompatible grains in one measure.
- Mark formulas and calculated fields clearly.

## Output

Return pivot specification, summary table, calculated fields, layout notes, and data-quality checks.
