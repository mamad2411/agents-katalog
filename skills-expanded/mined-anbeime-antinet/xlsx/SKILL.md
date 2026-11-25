---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When working with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
license: MIT
---

# Excel Skill for Antinet

This skill provides comprehensive Excel file operations for the Antinet intelligent knowledge management system.

## Features

- Create and edit Excel files with formulas
- Format cells (colors, fonts, alignment)
- Generate multi-sheet workbooks
- Export four-color cards to Excel
- Create data visualization charts
- Formula recalculation support

## Integration with Antinet

This skill is specifically designed for:
- Exporting analysis reports with four-color cards (🔵🟢🟡🔴)
- Creating structured data analysis workbooks
- Generating team collaboration templates
- Preserving formulas for dynamic updates

## Usage

See `excel_exporter.py` for the main export functionality.

## Requirements

- openpyxl >= 3.1.0
- pandas >= 2.0.0
- LibreOffice (optional, for formula recalculation)
