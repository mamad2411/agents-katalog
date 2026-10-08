---
name: local-docx-editor
description: |
  Edit Word documents (DOCX) locally without Canva API. Use this skill when user provides
  a DOCX file and wants to modify content, update formatting, or restructure document.
  Maintains original styles, fonts, spacing, and layout. Does NOT require Canva.
  Output goes to output/ folder. Use for: "edit this document", "update section 3", "change Word file".
---

# Local DOCX Editor Skill

> **QUICK REFERENCE**
> - **Utility script**: `scripts/local/docx_utils.py`
> - **Sample script**: `scripts/samples/sample_docx_edit.py`
> - **Safe copy**: `scripts/local/safe_copy.py`
> - **Output folder**: `output/docx/`
> - **Working folder**: `output/working/`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_docx_edit.py`
> - **3-Step workflow**: (1) Copy from `input/` to `output/working/` → (2) Edit the copy → (3) Save to `output/docx/`
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Edit and manipulate Word documents locally without requiring Canva API.

## CRITICAL: Never Modify Original Files

1. **ALWAYS** copy the original to `output/working/` first
2. **ALL** edits happen on the copy
3. **SAVE** results to `output/docx/`
4. **ORIGINAL** file remains untouched

## When to Use This Skill

Use this skill when:
- User provides a DOCX/DOC file and wants modifications
- Need to update text while maintaining formatting
- Need to add/remove sections
- Need to update tables
- **User has NOT explicitly asked to use Canva**

## Capabilities

### Read Operations
- Extract all text content
- Get document structure (headings, paragraphs)
- Extract images and tables
- Get styles and formatting info

### Write Operations
- Modify text content
- Update tables
- Modify headers/footers
- Apply consistent formatting

### Conversion
- DOCX to PDF
- DOCX to plain text

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
.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/document.docx"
```

### Step 2: Analyze
```bash
.venv\Scripts\python.exe scripts/local/docx_utils.py "output/working/document_copy.docx"
```

### Step 3: Make Modifications

Use docx_utils.py for:
- Find and replace text
- Update specific paragraphs
- Modify table cells

### Step 4: Save Result
Save to `output/docx/document_modified.docx`

## 3-Mode Workflow

### MODE 1: PLAN
- Analyze document structure
- List sections and word counts
- Document proposed changes

### MODE 2: CLARIFY
- Confirm content to modify
- Verify formatting requirements
- Check word count targets

### MODE 3: IMPLEMENT
- Create working copy
- Apply modifications
- Save to output folder

## Maintaining Format Integrity

### Preservation Rules
1. **Styles** - Preserve all named styles
2. **Spacing** - Line and paragraph spacing
3. **Lists** - Bullet and numbering styles
4. **Tables** - Column widths and formatting

## Research Capabilities

This skill can:
- Search for Word document best practices
- Look up python-docx documentation
- Research document formatting standards
- Find solutions to specific challenges

## Available Scripts

- `docx_utils.py` - Core DOCX analysis and manipulation
- `safe_copy.py` - Create working copies safely

## Todo List Tracking (REQUIRED)

**ALWAYS use TodoWrite** to track progress:

```json
[
  {"content": "Create safe working copy", "status": "in_progress", "activeForm": "Creating safe copy"},
  {"content": "Analyze document structure", "status": "pending", "activeForm": "Analyzing document"},
  {"content": "Apply modifications", "status": "pending", "activeForm": "Applying changes"},
  {"content": "Save to output/docx/", "status": "pending", "activeForm": "Saving result"}
]
```

## Output Location

- `output/docx/` - Modified documents
- `output/working/` - Working copies
