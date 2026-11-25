---
name: pdf-table-parser
description: Safely read and parse complex tables from local PDF files. Extracts structured tabular data without executing any embedded scripts or macros. Pure local file operation.
---

# PDF Table Parser SOP

Safely read and parse complex tables from local PDF files. Extracts structured tabular data without executing any embedded scripts or macros. Pure local file operation.

## When to Use

- Keywords: pdf, table, parser, data-extraction, local

## Required Parameters

- **file_path** (string): Local path to the PDF file

## Optional Parameters

- **pages** (string): Page range to parse, e.g. '1-3' or 'all' (default: all)
- **output_format** (string): Output format: json, csv, or markdown (default: json)
- **merge_cells** (boolean): Whether to merge spanning cells (default: True)

## Output

- **tables** (array): Array of extracted tables, each containing rows and columns
- **page_count** (number): Number of pages processed
- **table_count** (number): Total number of tables found

## Security

- Sandbox level: strict
- Max execution time: 120000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `validate_file` -> 9 steps -> Exit: `return_result`, `abort_not_pdf`, `abort_too_large`
