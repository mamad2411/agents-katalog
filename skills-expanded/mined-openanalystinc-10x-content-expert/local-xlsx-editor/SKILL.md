---
name: local-xlsx-editor
description: |
  Edit Excel spreadsheets (XLSX) locally without Canva API. Use this skill when user provides
  an XLSX file and wants to modify data, update formulas, or change formatting.
  Maintains original formulas, formatting, and structure. Does NOT require Canva.
  Output goes to output/ folder. Use for: "edit this spreadsheet", "update cell A5", "change Excel data".
---

# Local XLSX Editor Skill

> **QUICK REFERENCE**
> - **Utility script**: `scripts/local/xlsx_utils.py`
> - **Sample script**: `scripts/samples/sample_xlsx_edit.py`
> - **Safe copy**: `scripts/local/safe_copy.py`
> - **Output folder**: `output/xlsx/`
> - **Working folder**: `output/working/`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_xlsx_edit.py`
> - **3-Step workflow**: (1) Copy from `input/` to `output/working/` → (2) Edit the copy → (3) Save to `output/xlsx/`
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Edit and manipulate Excel spreadsheets locally without requiring Canva API.

## CRITICAL: Never Modify Original Files

1. **ALWAYS** copy the original to `output/working/` first
2. **ALL** edits happen on the copy
3. **SAVE** results to `output/xlsx/`
4. **ORIGINAL** file remains untouched

## When to Use This Skill

Use this skill when:
- User provides an XLSX/XLS file and wants modifications
- Need to update cell values or formulas
- Need to add/remove rows or columns
- **User has NOT explicitly asked to use Canva**

## Capabilities

### Read Operations
- Read cell values and formulas
- Get sheet names and structure
- Extract data ranges
- Analyze formulas

### Write Operations
- Update cell values
- Modify formulas
- Add/remove rows and columns
- Add/copy/delete sheets

### Conversion
- XLSX to CSV
- CSV to XLSX

## Running Python Scripts (Virtual Environment)

**IMPORTANT**: Always use the virtual environment Python:

```bash
# Windows
.venv\Scripts\python.exe scripts/local/script_name.py

# macOS/Linux
.venv/bin/python scripts/local/script_name.py
```

## Workflow

### Step 1: Create Safe Copy
```bash
.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/data.xlsx"
```

### Step 2: Analyze
```bash
.venv\Scripts\python.exe scripts/local/xlsx_utils.py "output/working/data_copy.xlsx"
```

### Step 3: Make Modifications

Use xlsx_utils.py for:
- Update specific cells
- Find and replace
- Modify ranges

### Step 4: Save Result
Save to `output/xlsx/data_modified.xlsx`

## 3-Mode Workflow

### MODE 1: PLAN
- Analyze spreadsheet structure
- List sheets and data ranges
- Document proposed changes

### MODE 2: CLARIFY
- Confirm cells to modify
- Verify formula handling
- Check formatting requirements

### MODE 3: IMPLEMENT
- Create working copy
- Apply modifications
- Save to output folder

## Formula Handling

- Formulas automatically recalculate when referenced cells change
- Relative references adjust when rows/columns added
- Named ranges maintained

## Research Capabilities

This skill can:
- Search for Excel best practices
- Look up openpyxl documentation
- Research spreadsheet formulas
- Find solutions to specific challenges

## Available Scripts

- `xlsx_utils.py` - Core XLSX analysis and manipulation
- `safe_copy.py` - Create working copies safely

## Todo List Tracking (REQUIRED)

**ALWAYS use TodoWrite** to track progress:

```json
[
  {"content": "Create safe working copy", "status": "in_progress", "activeForm": "Creating safe copy"},
  {"content": "Analyze spreadsheet structure", "status": "pending", "activeForm": "Analyzing spreadsheet"},
  {"content": "Apply modifications", "status": "pending", "activeForm": "Applying changes"},
  {"content": "Save to output/xlsx/", "status": "pending", "activeForm": "Saving result"}
]
```

## Output Location

- `output/xlsx/` - Modified spreadsheets
- `output/working/` - Working copies
