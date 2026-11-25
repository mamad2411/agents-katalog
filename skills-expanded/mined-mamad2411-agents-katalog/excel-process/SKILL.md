---
name: excel-process
description: "Process Excel spreadsheets using command-line tools in the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "📗"
---

# Excel Process

Process Excel files from the shared volume at `{{SHARED_VOLUME}}`.

## Convert to CSV

```bash
# Using ssconvert (gnumeric)
ssconvert {{SHARED_VOLUME}}/input/data.xlsx {{SHARED_VOLUME}}/output/data.csv

# Convert specific sheet
ssconvert --export-type=Gnumeric_stf:stf_csv -S {{SHARED_VOLUME}}/input/data.xlsx {{SHARED_VOLUME}}/output/sheet_%s.csv
```

## Tips for AI Agents

- Convert to CSV first for easier text-based processing.
- `ssconvert` from gnumeric handles .xlsx, .xls, and .ods formats.
- For complex operations, use Python with `openpyxl` or `pandas`.
