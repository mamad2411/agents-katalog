---
name: local-file-manager
description: |
  Main orchestrator for local file editing (PDF, PPTX, DOCX, XLSX). Routes to appropriate
  editor skill based on file type. CRITICAL RULE: NEVER modify original files. Always
  copy to output folder first, then work on the copy. Use this skill when user wants to
  edit local files without Canva API. Does not invoke Canva unless explicitly requested.
---

# Local File Manager Skill

> **QUICK REFERENCE — FILE TYPE ROUTING**
> | File Type | Route to Skill | Utility Script | Sample Script |
> |---|---|---|---|
> | PDF (.pdf) | `local-pdf-editor` | `scripts/local/pdf_utils.py` | `scripts/samples/sample_pdf_edit.py` |
> | PPTX (.pptx) | `local-pptx-editor` | `scripts/local/pptx_utils.py` | `scripts/samples/sample_pptx_edit.py` |
> | DOCX (.docx) | `local-docx-editor` | `scripts/local/docx_utils.py` | `scripts/samples/sample_docx_edit.py` |
> | XLSX (.xlsx) | `local-xlsx-editor` | `scripts/local/xlsx_utils.py` | `scripts/samples/sample_xlsx_edit.py` |
>
> - **Safe copy script**: `scripts/local/safe_copy.py` (ALWAYS copy before editing)
> - **Output folders**: `output/pdf/`, `output/pptx/`, `output/docx/`, `output/xlsx/`
> - **Working folder**: `output/working/` (for intermediate copies)
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)
> - **3-Step workflow**: (1) Copy from `input/` to `output/working/` → (2) Edit the copy → (3) Save to `output/[type]/`

Main orchestrator for all local file editing operations. Routes to appropriate specialized skill based on file type.

## CRITICAL RULE: NEVER MODIFY ORIGINAL FILES

**This is a non-negotiable rule:**

1. **NEVER** edit, modify, or overwrite files in the `input/` folder
2. **NEVER** modify files provided by the user in their original location
3. **ALWAYS** copy the file to `output/` folder first
4. **ALWAYS** work on the copy, not the original
5. **ALWAYS** save results to `output/` folder

### Why This Matters
- User's original files are precious and irreplaceable
- Mistakes happen - modifications should be reversible
- User needs to compare original vs. modified
- Audit trail of what was changed

### Workflow for Every Edit Operation

```
1. User provides file: input/report.pdf

2. COPY to output folder:
   output/working/report_copy.pdf

3. ALL edits happen on the copy

4. Final result saved as:
   output/pdf/report_modified.pdf

5. Original UNTOUCHED:
   input/report.pdf (unchanged)
```

## File Type Routing

| Extension | Skill | Description |
|-----------|-------|-------------|
| `.pdf` | `local-pdf-editor` | PDF manipulation |
| `.pptx`, `.ppt` | `local-pptx-editor` | PowerPoint editing |
| `.docx`, `.doc` | `local-docx-editor` | Word document editing |
| `.xlsx`, `.xls` | `local-xlsx-editor` | Excel spreadsheet editing |

## Standard Workflow

### Step 1: Receive File

User provides a file path. Verify it exists.

```bash
# Check file exists
ls -la "input/user_file.pdf"
```

### Step 2: Create Working Copy

**ALWAYS** copy before any operation:

```bash
# Create working directory
mkdir -p output/working

# Copy original to working directory
cp "input/user_file.pdf" "output/working/user_file_copy.pdf"
```

### Step 3: Route to Appropriate Skill

Based on file extension:
- `.pdf` → Use `local-pdf-editor` skill
- `.pptx` → Use `local-pptx-editor` skill
- `.docx` → Use `local-docx-editor` skill
- `.xlsx` → Use `local-xlsx-editor` skill

### Step 4: Perform Operations on Copy

All scripts receive:
- `--file`: Path to the COPY (not original)
- `--output`: Path in output folder for results

### Step 5: Save Results

Final modified file goes to appropriate output subfolder:
- `output/pdf/` - Modified PDFs
- `output/pptx/` - Modified PowerPoints
- `output/docx/` - Modified Word documents
- `output/xlsx/` - Modified Excel files

## Running Python Scripts (Virtual Environment)

**IMPORTANT**: All Python scripts MUST be run using the virtual environment Python:

```bash
# Windows
.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/document.pdf"

# macOS/Linux
.venv/bin/python scripts/local/safe_copy.py --source "input/document.pdf"
```

**NEVER** use system Python directly. Always use `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux).

## Safe Copy Script

Use this script for all file operations:

```bash
.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/document.pdf"
```

## Directory Structure for Operations

```
10x-Content-Expert/
├── input/                    # User's original files (READ-ONLY)
│   ├── report.pdf           # Original PDF
│   ├── presentation.pptx    # Original PPTX
│   └── document.docx        # Original DOCX
│
├── output/
│   ├── working/             # Temporary working copies
│   ├── pdf/                 # Final modified PDFs
│   ├── pptx/                # Final modified PPTXs
│   ├── docx/                # Final modified DOCXs
│   ├── xlsx/                # Final modified XLSXs
│   └── logs/                # Operation logs
```

## Capabilities

This skill has full access to:
- Web search for researching file format specifications
- Web fetch for getting documentation
- All file operations (read, write, edit)
- Bash for running Python scripts
- All other Claude Code tools as needed

## Todo List Tracking (REQUIRED)

**ALWAYS use the TodoWrite tool** to track progress for file editing tasks:

### When User Requests File Edit:
1. Create todo items for each step
2. Mark items in_progress as you work
3. Mark items completed when done

### Example Todo List for PDF Edit:
```
1. [x] Analyze original PDF structure
2. [x] Create safe working copy
3. [x] Apply requested modifications
4. [x] Verify changes
5. [x] Save to output folder
```

### TodoWrite Format:
```json
[
  {"content": "Create safe working copy", "status": "completed", "activeForm": "Creating safe copy"},
  {"content": "Analyze document structure", "status": "in_progress", "activeForm": "Analyzing structure"},
  {"content": "Apply modifications", "status": "pending", "activeForm": "Applying modifications"},
  {"content": "Save to output folder", "status": "pending", "activeForm": "Saving results"}
]
```

**This gives users visibility into progress and ensures all steps are completed.**

## When to Use This Skill

Use local editing (this skill) when:
- User provides a local file in `input/` folder
- User says "edit this file", "modify my document"
- User wants to update presentations, documents, spreadsheets, PDFs

## Integration with Content Creation

This skill works with content creation skills:
- Use `presentation-content` to generate PPT content/outlines
- Then use `local-pptx-editor` to apply changes to actual PPTX files
- Use `blog-article-writer` for content, then `local-docx-editor` to format
