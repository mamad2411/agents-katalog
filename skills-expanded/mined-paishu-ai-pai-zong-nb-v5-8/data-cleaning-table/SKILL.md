---
name: data-cleaning-table
description: Clean and normalize tables, CSV data, spreadsheet columns, dates, categories, duplicates, missing values, and analysis-ready datasets.
---

# data-cleaning-table

## Purpose

Prepare messy tabular data for analysis, reporting, charts, or import.

## Workflow

1. Identify source format, target schema, required fields, and downstream use.
2. Normalize headers, dates, numbers, currencies, categories, casing, and identifiers.
3. Detect duplicates, missing values, impossible values, and inconsistent units.
4. Produce a cleaned table or cleaning plan depending on available tooling.
5. Record assumptions and unresolved rows.

## Required Checks

- Do not silently drop rows.
- Do not overwrite source data unless explicitly requested.
- Preserve an exception list for uncertain transformations.

## Output

Return cleaned table or transformation plan, data-quality issues, exception rows, and validation checks.
