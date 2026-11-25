---
name: openai-spreadsheet
description: Creating, editing, analyzing, or formatting spreadsheets (`.xlsx`, `.csv`, `.tsv`) using Python (`openpyxl`, `pandas`), ensuring formula integrity and visual polish.
allowed-tools:
- Bash
- Read
- Grep
- Glob
- Write
- Edit
metadata:
  version: 0.2.0
  category: Data Processing
---
# Spreadsheet Management

## Quick Start
```python
import pandas as pd
from openpyxl import Workbook
# Read CSV and write to styled XLSX
df = pd.read_csv('data.csv')
df.to_excel('output.xlsx', index=False)
```

## Workflow
1. **Analyze**: Confirm file type (.xlsx, .csv, .tsv) and goals (create, edit, analyze, visualize).
2. **Execute**: Use `openpyxl` for .xlsx layout/formatting and `pandas` for data analysis.
3. **Validate**: Verify formulas, references, and styles; ensure no broken links.
4. **Review**: Render to PDF/PNG for visual check if system tools (`soffice`, `pdftoppm`) are available.
5. **Finalize**: Save artifacts to `output/spreadsheet/` and clean up `tmp/` files.

## Rules & Constraints
- **RULE-1**: Use formulas for derived values; NEVER hardcode results that should be dynamic.
- **RULE-2**: Preserve existing formatting and styles exactly when modifying existing workbooks.
- **RULE-3**: Cite all data sources using plain text URLs or cell comments for inputs.
- **RULE-4**: Openpyxl does not evaluate formulas; results will only calculate when opened in Excel/Sheets.

## When to Use
- Building new workbooks with complex formulas and structured layouts.
- Analyzing tabular data (pivots, aggregates) or visualizing with charts.
- Modifying financial models (LBO, DCF, 3-statement) while maintaining integrity.

## When NOT to Use
- Simple text editing that doesn't require tabular structure.
- Large-scale database operations where a SQL database would be more appropriate.

## References
- [Skill Manual](references/openai-spreadsheet-manual.md)
- [Openpyxl Examples](references/examples/openpyxl/)
