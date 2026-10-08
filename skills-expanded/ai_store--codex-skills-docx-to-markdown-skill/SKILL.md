---
name: tm:docx
metadata: version: 1.00
description: Create, edit, analyze .docx Word documents. Use for document creation, tracked changes, comments, formatting preservation, text extraction, template modification.
license: MIT
---

# DOCX Creation, Editing, and Analysis

## Overview

User may ask you to create, edit, or analyze the contents of a .docx file. A .docx file is essentially a ZIP archive containing XML files and other resources that you can read or edit.

## Setup & Dependencies
See [references/setup.md](references/setup.md) for installation instructions.

## Workflow Decision Tree

### Reading/Analyzing Content
Use "Text extraction" or "Raw XML access" sections below

### Creating New Document
Use "Creating a new Word document" workflow with **docx-js**

### Converting Markdown to Word
Use "Converting Markdown to Word" workflow with **pypandoc**

### Editing Existing Document
Use "Editing an existing Word document" workflow

## Reading and Analyzing Content

### Quick Convert to Markdown (Recommended)
Convert document to markdown for easy reading by AI agents:

```bash
# Basic conversion (accepts all tracked changes)
python scripts/docx_to_md.py document.docx output.md

# Show tracked changes (insertions/deletions marked)
python scripts/docx_to_md.py document.docx output.md --track-changes

# Output to stdout (for piping) (or --reject to show original)
python scripts/docx_to_md.py document.docx
```

### Text Extraction with Pandoc
`pandoc --track-changes=all document.docx -o output.md`

### Raw XML Access
For comments, complex formatting, document structure, unpack the document:
`python scripts/unpack.py <office_file> <output_directory>`

Key files: `word/document.xml` (content), `word/comments.xml` (comments), `word/styles.xml` (styles).

## Creating a New Word Document

Use **docx-js** library.
1. **READ DOCUMENTATION**: [references/docx-js-guide.md](references/docx-js-guide.md)
2. Create JS/TS file using Document, Paragraph, TextRun.
3. Export using Packer.toBuffer().

## Converting Markdown to Word

Convert markdown files to Word documents using **pypandoc** (already available in this skill).

### Basic Conversion

```bash
# Simple conversion
python scripts/md_to_docx.py document.md output.docx

# With custom styling template
python scripts/md_to_docx.py document.md output.docx --reference-doc template.docx

# With table of contents
python scripts/md_to_docx.py document.md output.docx --toc

# With numbered sections
python scripts/md_to_docx.py document.md output.docx --number-sections

# Combine options
python scripts/md_to_docx.py document.md output.docx --reference-doc template.docx --toc --number-sections
```

### Supported Markdown Features

**Formatting:**
- Headings (# ## ###)
- **Bold** and *italic* text
- Lists (ordered and unordered)
- `Code blocks` and inline code
- Links and images
- Tables
- Blockquotes

**Reference Document (Template):**
When you provide a `--reference-doc`, pypandoc uses the styles from that Word template. This is useful for:
- Corporate branding (fonts, colors)
- Custom heading styles
- Page layout (margins, headers/footers)
- Consistent formatting across documents

**When to Use:**
- ✅ Converting markdown documentation to Word format
- ✅ Creating Word documents from markdown reports
- ✅ Batch conversion of markdown files
- ✅ Applying consistent styling via templates
- **CRITICAL**: Do NOT create new python scripts, have to use existing scripts in the ./scripts/ folder.

**When NOT to Use:**
- ❌ Need precise OOXML control → Use docx-js or OOXML editing
- ❌ Need track changes → Use redlining workflow
- ❌ Complex document structures → Create from scratch with docx-js

### Advanced: Markdown with Track Changes

For converting markdown that includes track change markers to Word documents with native track changes.

**Markdown Track Change Syntax:**
```markdown
**text**         → Insertion (appears as tracked insertion in Word)
~~text~~         → Deletion (appears as tracked deletion in Word)  
*[SOW-ID Rxx.x]* → Comment with SOW reference
```

**Usage:**

```bash
# Apply changes to existing document
python scripts/md_to_docx_tracked.py changes.md updated.docx --base original.docx

# Create new document with track changes
python scripts/md_to_docx_tracked.py changes.md output.docx

# Custom author name
python scripts/md_to_docx_tracked.py changes.md output.docx --author "John Doe"
```

**Example Markdown:**
```markdown
# Document Updates

The system now supports **multi-channel notifications** *[HUBSOW-1530 R24.10]*
for customer communications.

~~The old postal-only system~~ has been replaced with flexible delivery options.

Key features include **email**, **SMS**, and **postal letter** delivery.
```

**Platform Support:**
- **Windows**: Uses `win32com.client` for native track changes (recommended)
- **macOS/Linux**: Uses `python-docx` with formatting markers (limited support)

**Dependencies:**
- Windows: `pip install pywin32`
- Other platforms: `pip install python-docx`

**When to Use:**
- ✅ Converting markdown analysis reports to Word with tracked changes
- ✅ Applying SOW requirements to existing documents
- ✅ Creating review documents with change history
- ✅ Collaborative document editing workflows

**Limitations:**
- Deletions require existing text in base document
- Complex nested changes may need manual review
- python-docx has limited track changes support (uses formatting instead)

## Editing an Existing Word Document

For editing existing documents with tracked changes and comments:

1. **READ DOCUMENTATION**: [references/ooxml-guide.md](references/ooxml-guide.md)
2. **Unpack**: `python scripts/unpack.py document.docx ./unpacked`
3. **Edit**: Create/run Python script using `DocxEditor` class (see `scripts/docx_editor.py`)
4. **Pack**: `python scripts/pack.py ./unpacked output.docx`

### Redlining Workflow (Tracked Changes)

1. **Get markdown**: `pandoc --track-changes=all document.docx -o current.md`
2. **Identify changes**: Review and plan.
3. **Unpack**: `python scripts/unpack.py document.docx ./unpacked`
4. **Implement changes**: Use `DocxEditor` class.
5. **Pack**: `python scripts/pack.py ./unpacked output.docx`

## Converting Documents to Images

1. Convert to PDF: `soffice --headless --convert-to pdf document.docx`
2. PDF to JPEG: `pdftoppm -jpeg -r 150 document.pdf page`
