---
name: google-sheets
description: Create and manage Google Sheets spreadsheets. Create new sheets with headers, move to folders, read and update data. Use when user asks to create a Google Sheet, spreadsheet, tracker, or mentions Google Sheets.
---

# Google Sheets Skill

Create and manage Google Sheets spreadsheets via the Sheets API.

## Quick Start

```bash
# Create new spreadsheet with headers
uv run scripts/create.py --title "My Tracker" --headers "Date,Task,Status,Notes"

# Append rows to existing spreadsheet
uv run scripts/append.py --id "SPREADSHEET_ID" --data "2024-01-15,Review docs,Done"

# Update specific cells
uv run scripts/update.py --id "SPREADSHEET_ID" --range "B2" --value "In Progress"

# Import CSV to new spreadsheet
uv run scripts/csv_import.py --file "data.csv" --title "Imported Data" --headers

# Manage sheets within a spreadsheet
uv run scripts/sheets.py --id "SPREADSHEET_ID" --duplicate "Template" --as "January"
```

## Available Operations

| Operation | Script | Description |
|-----------|--------|-------------|
| Create | `create.py` | Create new spreadsheet with headers |
| Append | `append.py` | Add rows to end of sheet |
| Update | `update.py` | Update specific cells or ranges |
| CSV Import | `csv_import.py` | Import CSV files to Google Sheets |
| Sheets | `sheets.py` | Add, duplicate, rename, delete sheets |

---

## CREATE - New Spreadsheet

Create a new Google Spreadsheet with optional headers and folder placement.

```bash
# Basic with headers
uv run scripts/create.py --title "My Tracker" --headers "Date,Task,Status,Notes"

# In specific folder (nested paths supported)
uv run scripts/create.py --title "Habit Tracker" --headers "Date,Training,Meditation" --folder "Projects/Tracking"

# From JSON definition
uv run scripts/create.py --title "Project Plan" --json '{"headers": ["Task", "Owner", "Due Date"]}'

# Custom first sheet name
uv run scripts/create.py --title "Budget 2025" --headers "Date,Category,Amount" --sheet "January"
```

**Arguments:**
- `--title` / `-t` (required) - Spreadsheet name
- `--headers` / `-H` - Comma-separated header names
- `--folder` / `-f` - Google Drive folder path
- `--sheet` / `-s` - First sheet name (default: Sheet1)
- `--json` / `-j` - JSON config with headers

---

## APPEND - Add Rows

Append rows to the end of an existing sheet.

```bash
# Single row (comma-separated)
uv run scripts/append.py --id "SPREADSHEET_ID" --data "Value1,Value2,Value3"

# Multiple rows (JSON array)
uv run scripts/append.py --id "SPREADSHEET_ID" --json '[["Row1A","Row1B"],["Row2A","Row2B"]]'

# Specific sheet
uv run scripts/append.py --id "SPREADSHEET_ID" --sheet "Sheet2" --data "A,B,C"

# Works with URLs too
uv run scripts/append.py --id "https://docs.google.com/spreadsheets/d/ABC123/edit" --data "New,Row,Data"
```

**Arguments:**
- `--id` / `-i` (required) - Spreadsheet ID or URL
- `--sheet` / `-s` - Target sheet name (default: Sheet1)
- `--data` / `-d` - Comma-separated values for single row
- `--json` / `-j` - JSON array for multiple rows

---

## UPDATE - Modify Cells

Update specific cells or ranges with new values.

```bash
# Single cell
uv run scripts/update.py --id "SPREADSHEET_ID" --range "A1" --value "Hello"

# Single row
uv run scripts/update.py --id "SPREADSHEET_ID" --range "A1:C1" --data "Val1,Val2,Val3"

# Multiple cells (2D array)
uv run scripts/update.py --id "SPREADSHEET_ID" --range "A1:B2" --json '[["A","B"],["C","D"]]'

# Specific sheet
uv run scripts/update.py --id "SPREADSHEET_ID" --range "Sheet2!A1" --value "Updated"

# Raw input (no formula parsing)
uv run scripts/update.py --id "SPREADSHEET_ID" --range "A1" --value "=SUM(B:B)" --raw
```

**Arguments:**
- `--id` / `-i` (required) - Spreadsheet ID or URL
- `--range` / `-r` (required) - A1 notation (e.g., "A1", "Sheet1!A1:C3")
- `--value` / `-v` - Single cell value
- `--data` / `-d` - Comma-separated values for single row
- `--json` / `-j` - JSON 2D array
- `--raw` - Use RAW input (no formula parsing)

---

## CSV IMPORT - Import CSV Files

Convert local CSV files to Google Sheets.

```bash
# Create new spreadsheet from CSV
uv run scripts/csv_import.py --file "data.csv" --title "Imported Data"

# With header formatting
uv run scripts/csv_import.py --file "leads.csv" --title "Leads" --headers

# To specific folder
uv run scripts/csv_import.py --file "data.csv" --title "Data" --folder "Projects" --headers

# Append to existing spreadsheet (new sheet)
uv run scripts/csv_import.py --file "data.csv" --id "SPREADSHEET_ID" --sheet "ImportedData"
```

**Arguments:**
- `--file` / `-f` (required) - Path to CSV file
- `--title` / `-t` - New spreadsheet title (creates new)
- `--id` / `-i` - Existing spreadsheet ID (appends to it)
- `--sheet` / `-s` - Target sheet name (default: Sheet1)
- `--folder` - Google Drive folder path
- `--headers` - Format first row as headers (bold, blue, frozen)

---

## SHEETS - Sheet Management

Manage sheets within a spreadsheet (add, duplicate, rename, delete).

```bash
# List all sheets
uv run scripts/sheets.py --id "SPREADSHEET_ID" --list

# Add new blank sheet
uv run scripts/sheets.py --id "SPREADSHEET_ID" --add "NewSheet"

# Duplicate existing sheet (great for templates!)
uv run scripts/sheets.py --id "SPREADSHEET_ID" --duplicate "Template" --as "January"

# Rename a sheet
uv run scripts/sheets.py --id "SPREADSHEET_ID" --rename "OldName" --as "NewName"

# Delete a sheet
uv run scripts/sheets.py --id "SPREADSHEET_ID" --delete "OldSheet"

# Delete without confirmation
uv run scripts/sheets.py --id "SPREADSHEET_ID" --delete "OldSheet" --force
```

**Arguments:**
- `--id` / `-i` (required) - Spreadsheet ID or URL
- `--list` / `-l` - List all sheets
- `--add` / `-a` - Name for new blank sheet
- `--duplicate` / `-d` - Source sheet to copy
- `--rename` - Sheet to rename
- `--as` - New name (required with --duplicate or --rename)
- `--delete` - Sheet to delete
- `--force` / `-f` - Skip delete confirmation

---

## First-Time Setup

This skill uses the shared Google OAuth integration:

```bash
uv run ~/.claude/plugins/cache/riccardovandra/cc-plugin-productivity-suite/integrations/google/scripts/oauth_setup.py --add-scope spreadsheets --add-scope drive
```

See the plugin README for full setup instructions.

## Activation Triggers

- "create google sheet", "make a spreadsheet"
- "add rows to spreadsheet", "append data"
- "update spreadsheet", "modify cells"
- "import csv to sheets", "convert csv"
- "duplicate sheet", "add new sheet"
- "google sheets", "spreadsheet"

## URL/ID Flexibility

All scripts accept either:
- Spreadsheet ID: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`
- Full URL: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`
