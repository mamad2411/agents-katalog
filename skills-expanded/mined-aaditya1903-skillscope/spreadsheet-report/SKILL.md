---
name: spreadsheet-report
description: Build formatted spreadsheet reports with computed columns, summary rows and charts. Use when someone needs an .xlsx workbook produced from tabular data rather than a document or slide deck.
license: MIT
compatibility: Requires a spreadsheet library capable of writing .xlsx.
allowed-tools: Read Write Bash
metadata:
  category: documents
---

# Spreadsheet report

Produce a workbook from tabular input, keeping the raw data on its own sheet so
the derived figures can always be traced back.

## When to use this

Use this skill when the deliverable is a spreadsheet file. Prefer a document
skill when the deliverable is prose, and a slide skill when it is a deck.

## Steps

1. Read the source rows and record the column types you inferred.
2. Write the untouched rows to a `data` sheet.
3. Add computed columns on a `report` sheet that reference the `data` sheet.
4. Add a summary block with totals and per-group subtotals.
5. Add one chart per requested comparison.

## Checks

- Every derived cell references a source cell rather than a pasted value.
- Numeric formats are set explicitly, including currency and percentage.
- The workbook opens without repair prompts.
