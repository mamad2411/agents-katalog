---
name: local-pdf-editor
description: |
  Edit PDF files locally without Canva API. Use this skill when user provides a PDF file
  and wants to modify content, extract text, merge/split pages, or update specific sections.
  Maintains original formatting, spacing, fonts, and layout. Does NOT require Canva.
  Output goes to the output/ folder. Use for: "edit this PDF", "change page 15", "update text in PDF".
---

# Local PDF Editor Skill

> **QUICK REFERENCE**
> - **Scripts**: `scripts/local/pdf_utils.py`, `scripts/local/safe_copy.py`
> - **Sample script**: `scripts/samples/sample_pdf_edit.py`
> - **Output**: `output/pdf/`
> - **Working dir**: `output/working/`
> - **Python**: `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (Mac/Linux)
> - **Step 1**: `.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/file.pdf"`
> - **Step 2**: `.venv\Scripts\python.exe scripts/local/pdf_utils.py "output/working/file_copy.pdf"`
> - **Step 3**: Edit the copy, save to `output/pdf/`

Edit and manipulate PDF files locally without requiring Canva API.

## CRITICAL: Never Modify Original Files

1. **ALWAYS** copy the original to `output/working/` first
2. **ALL** edits happen on the copy
3. **SAVE** results to `output/pdf/`
4. **ORIGINAL** file remains untouched

## When to Use This Skill

Use this skill when:
- User provides a PDF file and wants modifications
- Need to extract text from PDF
- Need to merge or split PDF pages
- Need to update specific content while maintaining layout
- **User has NOT explicitly asked to use Canva**

## Capabilities

### Read Operations
- Extract text from PDF (all pages or specific)
- Extract images from PDF
- Get PDF metadata (pages, size, fonts)
- Analyze PDF structure

### Write Operations
- Modify text content (maintaining layout)
- Add/remove pages
- Merge multiple PDFs
- Split PDF into separate files
- Add watermarks or headers/footers

### Conversion
- PDF to DOCX (for easier editing)
- PDF to images (PNG/JPG)
- PDF to text
- DOCX back to PDF

## Running Python Scripts (Virtual Environment)

**IMPORTANT**: Always use the virtual environment Python:

```bash
# Windows
.venv\Scripts\python.exe scripts/local/script_name.py

# macOS/Linux
.venv/bin/python scripts/local/script_name.py
```

## Workflow for Content Modification

### Step 1: Create Safe Copy
```bash
.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/document.pdf"
```

### Step 2: Analyze the PDF
```bash
.venv\Scripts\python.exe scripts/local/pdf_utils.py "output/working/document_copy.pdf"
```

### Step 3: For Text Modifications
```bash
# Convert to DOCX for easier editing
.venv\Scripts\python.exe scripts/local/pdf_to_docx.py --file "output/working/document_copy.pdf"

# Make modifications to the DOCX

# Convert back to PDF
.venv\Scripts\python.exe scripts/local/docx_to_pdf.py --file "output/working/document_copy.docx" --output "output/pdf/document_modified.pdf"
```

## 3-Mode Workflow

### MODE 1: PLAN
- Analyze the PDF structure
- Document current state (pages, content)
- List proposed changes
- Identify what will NOT change

### MODE 2: CLARIFY
- Confirm which content to modify
- Ask about formatting preferences
- Verify output requirements

### MODE 3: IMPLEMENT
- Create working copy
- Make modifications
- Save to output folder
- Report results

## Research Capabilities

This skill can:
- Search the web for PDF manipulation techniques
- Look up PDF format specifications
- Research best practices for maintaining formatting
- Find solutions to specific PDF challenges

## Available Scripts

- `pdf_utils.py` - Core PDF analysis and manipulation
- `safe_copy.py` - Create working copies safely

## Todo List Tracking (REQUIRED)

**ALWAYS use TodoWrite** to track progress:

```json
[
  {"content": "Create safe working copy", "status": "in_progress", "activeForm": "Creating safe copy"},
  {"content": "Analyze PDF structure", "status": "pending", "activeForm": "Analyzing PDF"},
  {"content": "Apply modifications", "status": "pending", "activeForm": "Applying changes"},
  {"content": "Save to output/pdf/", "status": "pending", "activeForm": "Saving result"}
]
```

## Output Location

All modified files saved to:
- `output/pdf/` - Modified PDFs
- `output/working/` - Intermediate files
