---
name: typst-renderer
description: "Compile structured resume JSON into single-page PDF using Typst templates. Handles template selection, JSON-to-Typst conversion, compilation, and auto-fit logic. The LLM never needs to worry about formatting, fonts, spacing, or page limits - Typst templates handle all layout automatically."
---

# Typst Renderer - JSON to PDF Resume Compilation

A tool skill for compiling structured resume content (JSON) into professional single-page PDFs using Typst templates with automatic page fitting.

## Overview

This skill provides the rendering pipeline for Rescume v2.0. It takes structured JSON content from the content-generator agent and produces a perfectly formatted single-page PDF resume using Typst templates.

**Key principle:** The LLM is a content writer, not a layout engineer. This skill handles ALL formatting decisions.

## Quick Reference

| Task | Script |
|------|--------|
| List available templates | `list_templates.py` |
| Compile JSON to PDF | `compile.py content.json template-name output.pdf` |
| Convert JSON to Typst data | `json_to_typst.py content.json data.typ` |
| Validate PDF output | `validate_pdf.py output.pdf` |

## Core Features

### 1. Automatic Page Fitting (Auto-Fit)

The renderer automatically adjusts font size to ensure content fits on exactly 1 page:

- Start at default size (11pt)
- If content overflows, reduce font by 0.5pt steps
- Stop at minimum size (9pt)
- If still overflows, report to coordinator for content trimming

**Result:** Guaranteed single-page output or clear feedback for content adjustment.

### 2. Template Support

Multiple professional templates available:
- **basic-resume**: Clean, ATS-friendly single-column
- **modern-resume**: Modern design with color accents

Templates are Typst files with consistent data schema.

### 3. Deterministic Rendering

Same content + same template = same PDF every time.
No LLM guessing about layout.

## Available Scripts

### list_templates.py

List all available Typst templates with metadata.

**Usage:**
```bash
python scripts/list_templates.py
```

**Output:**
```json
[
  {
    "name": "basic-resume",
    "description": "Clean, ATS-friendly single-column resume template",
    "preview": "templates/basic-resume/preview.pdf",
    "default_font": "New Computer Modern",
    "default_font_size": "11pt",
    "min_font_size": "9pt"
  }
]
```

### compile.py

Main compilation script - handles full pipeline.

**Usage:**
```bash
python scripts/compile.py <content.json> <template-name> <output.pdf>
```

**Example:**
```bash
python scripts/compile.py resume_content.json basic-resume final_resume.pdf
```

**What it does:**
1. Loads JSON content
2. Converts to Typst data format
3. Injects into selected template
4. Compiles with Typst CLI
5. Checks page count
6. If > 1 page, reduces font and recompiles
7. Returns success or overflow error

**Output:**
```json
{
  "success": true,
  "pages": 1,
  "font_size_used": 10.5,
  "output_path": "final_resume.pdf",
  "compilation_time_ms": 187
}
```

Or if overflow:
```json
{
  "success": false,
  "status": "overflow",
  "pages": 1.2,
  "min_font_reached": 9.0,
  "recommendation": "Reduce content by approximately 2-3 bullet points"
}
```

### json_to_typst.py

Convert structured JSON content to Typst data declarations.

**Usage:**
```bash
python scripts/json_to_typst.py <content.json> <output.typ>
```

**Input (content.json):**
```json
{
  "header": {
    "name": "Andy Wen",
    "email": "andy@example.com",
    "phone": "(555) 123-4567"
  },
  "experience": [
    {
      "company": "Tech Corp",
      "role": "Engineer",
      "dates": "2020-Present",
      "bullets": ["Built scalable systems"]
    }
  ]
}
```

**Output (data.typ):**
```typst
#let resume-data = (
  header: (
    name: "Andy Wen",
    email: "andy@example.com",
    phone: "(555) 123-4567",
  ),
  experience: (
    (
      company: "Tech Corp",
      role: "Engineer",
      dates: "2020-Present",
      bullets: ("Built scalable systems",),
    ),
  ),
)
```

### validate_pdf.py

Validate PDF output (page count, readability).

**Usage:**
```bash
python scripts/validate_pdf.py <output.pdf>
```

**Output:**
```json
{
  "valid": true,
  "pages": 1,
  "readable": true,
  "file_size_kb": 45.2
}
```

## JSON Content Schema

The expected JSON schema for resume content (from content-generator):

```json
{
  "header": {
    "name": "string (required)",
    "location": "string (optional)",
    "email": "string (optional)",
    "phone": "string (optional)",
    "linkedin": "string (optional)",
    "github": "string (optional)",
    "website": "string (optional)"
  },
  "summary": "string (optional)",
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "dates": "string",
      "gpa": "string (optional)",
      "details": ["string"]
    }
  ],
  "experience": [
    {
      "company": "string",
      "role": "string",
      "location": "string (optional)",
      "dates": "string",
      "bullets": ["string"]
    }
  ],
  "projects": [
    {
      "name": "string",
      "subtitle": "string (optional)",
      "dates": "string (optional)",
      "bullets": ["string"]
    }
  ],
  "skills": {
    "languages": ["string"],
    "frameworks": ["string"],
    "tools": ["string"],
    "concepts": ["string"]
  }
}
```

## Auto-Fit Algorithm

```
1. font_size = 11pt (default)
2. Compile resume with font_size
3. Count pages in output PDF
4. If pages == 1:
     SUCCESS - return PDF
5. Else if pages > 1 and font_size > 9pt:
     font_size -= 0.5pt
     Go to step 2
6. Else:
     OVERFLOW - return error with recommendations
```

**Performance:** Each compile ~50ms, max 5 iterations = ~250ms total

## Integration with Rescume Workflow

In the main rescume coordinator skill (Phase 2):

```
Step 4: Content Generation
  → content-generator outputs content.json

Step 5: Typst Compilation (USE THIS SKILL)
  → User selects template (or default)
  → Call: compile.py content.json basic-resume output.pdf
  → If success: Proceed to Step 6
  → If overflow: Ask LLM to trim content, recompile

Step 6: Quality Check
  → hr-critic evaluates content (from JSON, not PDF)
  → If quality issues: Revise JSON, recompile

Step 7: Deliver PDF
```

## Instructions for LLM

When using this skill:

1. **Never worry about formatting** - that's handled by Typst templates
2. **Never count words or characters** - auto-fit handles page fitting
3. **Never think about fonts, spacing, or layout** - templates handle all of that
4. **Focus purely on content quality** - write compelling, tailored bullets
5. **If overflow reported** - simply reduce content volume (remove 2-3 bullets or shorten descriptions)

Your job is to generate great resume content as JSON. This skill makes it look professional.

## Error Handling

All scripts return proper exit codes:
- `0`: Success
- `1`: Compilation failed (Typst error)
- `2`: File not found
- `3`: Invalid JSON schema
- `4`: Overflow at minimum font size

Check results:
```bash
python scripts/compile.py content.json basic-resume output.pdf && echo "Success!" || echo "Failed"
```

## Dependencies

- **Typst CLI** (system binary): Must be installed and in PATH
- **pdfplumber** (Python): `pip install pdfplumber`
- **Python 3.8+**: Standard library (subprocess, json, pathlib)

## File Structure

```
typst-renderer/
├── SKILL.md                    (this file)
└── scripts/
    ├── compile.py              # Main compilation orchestrator
    ├── json_to_typst.py        # JSON → Typst converter
    ├── validate_pdf.py         # PDF validation
    └── list_templates.py       # Template listing
```

Templates live in: `/Users/andy/.claude/skills/rescume/templates/`

## Testing

Test the complete pipeline:
```bash
# 1. Create test content
echo '{"header":{"name":"Test User","email":"test@example.com"},"experience":[{"company":"Test Co","role":"Engineer","dates":"2020-Present","bullets":["Built things"]}],"skills":{"languages":["Python"]}}' > test_content.json

# 2. Compile
python scripts/compile.py test_content.json basic-resume test_output.pdf

# 3. Validate
python scripts/validate_pdf.py test_output.pdf
```

## Notes

- Compilation is fast (~50-200ms total with auto-fit)
- Templates use fallback fonts for maximum compatibility
- All PDFs are US Letter size, single page
- ATS-friendly - no complex graphics or unusual formatting
- Works offline - no external API calls needed
