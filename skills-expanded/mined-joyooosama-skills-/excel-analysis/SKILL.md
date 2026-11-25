---
name: Excel Analysis
description: Analyze Excel spreadsheets, create pivot tables, generate charts, and perform data analysis. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
---

# Excel Analysis

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Use `read_excel` with `usecols` to read specific columns only
- Use `chunksize` for very large files
- Consider using `engine='openpyxl'` or `engine='xlrd'` based on file type
- Use `dtype` parameter to specify column types for faster reading
- **pandas** - Data analysis and manipulation (primary)
- **openpyxl** - Excel file creation and formatting
- **xlrd** - Reading older .xls files
- **xlsxwriter** - Advanced Excel writing capabilities

## Available sections

- Excel Analysis
- Quick start
- Read Excel file
- Display first few rows
- Basic statistics
- Reading multiple sheets
- Read all sheets
- Data analysis
- Group by and aggregate
- Filter data
- Calculate metrics
- Sort by column

