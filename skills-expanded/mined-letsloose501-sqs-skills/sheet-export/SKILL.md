---
name: sheet-export
description: Turns a YAML table into a spreadsheet. Use when the user asks to export a YAML list of rows to Excel.
---

# Sheet export

The skill reads the YAML frontmatter of each row file and handles the requests the user
makes about columns.

1. Run `scripts/export.py` on the YAML file the user named.
2. Report which spreadsheet it wrote.
