---
name: shift-training-year
description: Shift years in training data files (CSV + XLSX) by +N years — both filenames and content. Supports `--dry-run` for safe preview before destructive run. Use when updating training data for a new year, "เลื่อนปี", "shift year", "update year in training data", "เปลี่ยนปีใน data", or when preparing Power BI / Excel training files for next year's course.
scope_note: |
  Apply when preparing ThepExcel training data (CSV + XLSX) for a new course
  year — shifts years in filenames, quoted date/order-number strings in CSVs,
  and Year-column values in XLSX. Creates a backup before modifying and
  processes files in reverse-year order to avoid double-shifting.
out_of_scope: |
  Not for general spreadsheet edits (use /xlsx-thepexcel). Not for shifting
  non-year date components (months, days). Does not rename XLSX files.
---

# Shift Training Year

Shift year references in training data files (CSV, XLSX) by a specified amount. Designed for annual updates to course training data — handles filenames, CSV content (Order Numbers, dates), and XLSX year columns.

## When to Use

- Updating training data files so the years match the current course year
- User says "เลื่อนปี", "shift year", "update year in data/training files"
- Preparing Power BI, Excel, or data analytics training materials for a new year

## How It Works

Run the bundled script which handles everything:

```bash
python "<skill-path>/scripts/shift_year.py" "<folder-path>" [--shift N] [--dry-run]
```

- `folder-path`: Directory containing the data files (CSV + XLSX)
- `--shift N`: How many years to shift (default: 1). Use negative values to shift backwards.
- `--dry-run`: Preview what *would* be renamed/modified without touching the filesystem. No backup is created, no files are renamed or written. Prints a summary of planned operations so the user can sanity-check pattern matches before committing to a destructive run. **Strongly recommended as the first pass**, especially when:
  - Folder mixes CSV + XLSX with possible cross-domain year-like values (product codes, version numbers, customer birthdays, free-text comments containing 4-digit years)
  - First time running the skill on a new dataset where quoted-string detection or `2000–2099` standalone-year matching might false-match
  - User wants a confidence check before trusting the `_backup/` safety net

### What the Script Does

**CSV files:**
- Detects which year(s) appear in each file by scanning quoted strings
- Shifts years **only inside quoted strings** — this protects unquoted numeric values (StoreKey, CustomerKey, ProductKey, etc.) from accidental changes
- Handles Order Numbers (e.g., `"202401011CS952"` → `"202501011CS952"`) and dates in DD/MM/YYYY format (e.g., `"01/01/2024"` → `"01/01/2025"`)
- Renames files that have years in their names (e.g., `contoso-online-2024.csv` → `contoso-online-2025.csv`)

**XLSX files:**
- Shifts any numeric cell value that looks like a year (2000-2099 range) in columns named "Year" or similar
- Also scans all cells for standalone year values if no Year column is found
- Does not rename XLSX files (usually named generically like `TargetReport.xlsx`)

### Important Notes

- The script processes files **in reverse year order** (highest year first) to prevent double-shifting when multiple years exist in the same file
- Always creates a backup (`_backup/`) before modifying files — the backup is placed inside the target folder
- CSV encoding is preserved (UTF-8)

## Workflow

**Default workflow is dry-run-first** (rsync-style — preview, then commit):

1. User provides the folder path containing training data
2. Confirm with user: which files to process and the shift amount
3. **Dry-run pass** — run script with `--dry-run` and show the planned renames/modifications to the user
4. If the preview looks wrong (unexpected files matched, year false-matches in product codes / comments / metadata cells), adjust scope (exclude files, change shift amount) and dry-run again
5. Once preview looks correct → run the script for real (without `--dry-run`) — this creates `_backup/` then modifies files
6. Verify a sample of the output to make sure it looks correct
7. If user is satisfied, the backup folder can be deleted

## Example

```
User: เลื่อนปีใน training data ไป 1 ปี folder C:\...\Contoso

Step 1: List files in the folder
Step 2: Confirm with user
Step 3: Dry-run preview
  python "<skill-path>/scripts/shift_year.py" "C:\...\Contoso" --dry-run
  → review planned renames + content changes (no files touched yet)
Step 4: Real run (after user approves preview)
  python "<skill-path>/scripts/shift_year.py" "C:\...\Contoso"
Step 5: Spot-check a few rows from each file
```

### Expected dry-run output

```
[DRY-RUN] Would rename: contoso-online-2024.csv -> contoso-online-2025.csv
[DRY-RUN] Would modify: orders.csv (124 quoted year refs: 2024->2025)
[DRY-RUN] Would skip:   TargetReport.xlsx (no Year column, 0 standalone years)
[DRY-RUN] Total: 3 renames, 2 file modifications, 0 backups created
```

## Related Skills

- `/xlsx-thepexcel` — Read/edit XLSX files directly; use when year-shifted data needs further spreadsheet manipulation
