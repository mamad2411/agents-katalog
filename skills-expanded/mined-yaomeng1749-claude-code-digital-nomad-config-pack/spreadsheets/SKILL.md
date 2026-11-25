---
name: spreadsheets
description: "Generate and edit spreadsheets. Outputs CSV, TSV, or Excel-compatible HTML tables. Use when user says 'make spreadsheet', 'create table', 'generate CSV', '做表格', '导出数据', or needs structured tabular data output."
---

# Spreadsheet Generator

Generate structured tabular data as CSV files or HTML tables that can be opened in Excel/Google Sheets.

## Usage

`/spreadsheets <description of data needed>`

## Output Formats

### CSV (default)
- File: `output/<name>.csv`
- UTF-8 with BOM (for Excel compatibility with CJK characters)
- Proper quoting for fields containing commas or newlines

### HTML Table (for rich formatting)
- File: `output/<name>.html`
- Styled table that can be copy-pasted into Google Sheets or Excel
- Includes headers, formatting, and conditional styling

## Capabilities

1. **Data generation**: Create structured datasets from descriptions
2. **Data transformation**: Reshape, pivot, aggregate existing data
3. **Template creation**: Budget templates, project trackers, comparison matrices
4. **Analysis tables**: Summary statistics, comparison tables, decision matrices

## Template Types

- **Comparison matrix**: Feature × product comparison
- **Project tracker**: Task, owner, status, deadline, priority
- **Budget template**: Category, planned, actual, variance
- **Decision matrix**: Option × criteria with weighted scoring
- **Data dictionary**: Field name, type, description, example
- **Timeline/Gantt**: Task, start, end, dependencies, status

## Rules

- Always include a header row
- Use consistent date formats (YYYY-MM-DD)
- Quote strings containing special characters
- Add UTF-8 BOM for CSV files with CJK characters
- Create the output directory if it doesn't exist
