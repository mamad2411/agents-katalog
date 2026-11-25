# office/xlsx-toolkit — skill payload

> Machine-readable contract: [`../xlsx-toolkit.manifest.json`](../xlsx-toolkit.manifest.json).

## What this skill does

Read, write, analyse and chart Excel workbooks. Wraps `openpyxl` for
structured cell access and `pandas` for tabular analysis. A single
`operation` parameter routes to:

- `read_range` — return cell values from `Sheet!A1:D20` style ranges.
- `write_range` — write a 2D array of values into a range.
- `add_chart` — insert a bar/line/pie chart over a data range.
- `evaluate_formulas` — open with the calc engine, return computed values.
- `list_sheets` — sheet names + dimensions, useful for orientation.

## When to use it

- The user uploaded a workbook and wants it summarised or transformed.
- You need to fill a templated workbook (e.g. budget template).
- You need to extract a specific named range for downstream processing.

## When **not** to use it

- The data is CSV or Parquet — pandas directly is lighter weight.
- The workbook is a financial model with macros — macros are not executed.
- The user wants a *report* (narrative + charts together) — use
  `office/docx-toolkit` or `office/pptx-toolkit` and embed the chart.

## Determinism and risk

Determinism: **high** for read/write; **medium** for formula evaluation
(depends on the engine). Risk: **low** — no external side effects.

## How it composes

`spreadsheet.analyse` is a common upstream step for `office/pptx-toolkit`
(chart-in-deck), `office/docx-toolkit` (table-in-report), and any
finance reconciliation skill that consumes structured tables.
