---
name: sheet-export
description: Turns a YAML table into a spreadsheet. Use when the user asks to export a YAML list of rows to Excel.
compatibility: Needs Python 3.9+ with pandas installed.
---

# Sheet export

Needs these packages, once:

```bash
pip install openpyxl pyyaml
```

1. Run `scripts/export.py` on the YAML file the user named, to turn it into a spreadsheet.
2. For a chart of the rows, run `scripts/chart.py` - it runs under `uv run`, which reads
   its own dependencies from the script.
3. Report which spreadsheet it wrote. The layout rules for the Excel file are in
   [references/layout.md](references/layout.md).
