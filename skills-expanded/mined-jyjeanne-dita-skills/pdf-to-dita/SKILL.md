---
name: pdf-to-dita
description: Converts a PDF document into a complete DITA 1.3 guide by running a 5-stage automated pipeline: PDF text extraction, topic chunking, validation, best-practices optimization, and full-guide review. Use this skill when you need to migrate legacy PDF documentation into structured DITA XML, bootstrap a DITA project from an existing PDF manual, or verify the quality of the generated DITA output. Integrates with validate-dita-topic, validate-ditamap, dita-best-practices, and review-dita-guide.
compatibility: Python 3.9+. Stage 1 requires pdfplumber (pip install pdfplumber). Stages 2–5 use stdlib only and call the existing dita-skills validator scripts.
---

## Overview

`pdf-to-dita` orchestrates a five-stage pipeline that transforms any PDF into a well-structured DITA 1.3 guide, validates every generated file, applies best-practices fixes, and produces a consolidated quality report.

```
PDF  →  [1] Extract  →  [2] Chunk  →  [3] Validate  →  [4] Optimize  →  [5] Review
         extracted.json   topics/*.dita  validation_       optimization_    review_
                          root.ditamap   report.json       report.json      report.json
```

---

## Pipeline stages

### Stage 1 — Extract (`extract_pdf.py`)

Reads the PDF with **pdfplumber** and produces a structural JSON document.

- Detects heading levels from font-size ratios (body text = most common size; ratio ≥ 1.15 → heading).
- Preserves paragraphs, ordered/unordered lists, and tables.
- Outputs `extracted.json` with a nested `sections` tree.

```bash
python pdf-to-dita/scripts/extract_pdf.py input.pdf > extracted.json
```

**Output excerpt:**
```json
{
  "source": "/abs/path/input.pdf",
  "title":  "Getting Started Guide",
  "pages":  42,
  "sections": [
    {
      "level": 1,
      "title": "Installation",
      "content": [
        {"type": "paragraph", "text": "This guide covers..."},
        {"type": "list", "ordered": true, "items": ["Download the package", "Run setup.sh"]}
      ],
      "subsections": []
    }
  ]
}
```

---

### Stage 2 — Chunk (`chunk_to_dita.py`)

Converts the extracted JSON into DITA 1.3 XML topics and a root `ditamap`.

**Topic-type heuristics:**

| Signal | Assigned type |
|--------|--------------|
| Title matches action verbs (configure, install, create, …) | `task` |
| Title matches (reference, parameters, api, settings, …) | `reference` |
| Content has ≥ 3 ordered-list items | `task` |
| Table headers include `name`, `parameter`, `property` | `reference` |
| Default | `concept` |

**Output structure:**
```
output_dir/
├── root.ditamap
└── topics/
    ├── installation.dita        (task)
    ├── configuration-options.dita (reference)
    └── overview.dita             (concept)
```

```bash
python pdf-to-dita/scripts/chunk_to_dita.py extracted.json ./output --map-title "My Guide"
```

---

### Stage 3 — Validate (`validate_output.py`)

Calls `validate_dita_topic.py` and `validate_ditamap.py` on every generated file.

```bash
python pdf-to-dita/scripts/validate_output.py ./output
```

**Output excerpt:**
```json
{
  "summary": {
    "total_files": 8, "valid": 7, "invalid": 1,
    "total_errors": 2, "total_warnings": 5
  },
  "files": [
    { "file": "topics/installation.dita", "is_valid": true, "errors": [], "warnings": [] }
  ]
}
```

---

### Stage 4 — Optimize (`optimize_dita.py`)

Calls `best_practices.py` on each topic, auto-fixes common violations, then re-validates.

**Auto-fixes applied:**

| Violation | Fix |
|-----------|-----|
| `missing-shortdesc` | Inserts `<shortdesc>` from first sentence of first paragraph |

Remaining errors and warnings after auto-fix are reported but not auto-corrected (require human review).

```bash
python pdf-to-dita/scripts/optimize_dita.py ./output
```

---

### Stage 5 — Review (`review_dita_guide.py`)

Runs the full hierarchical guide review via `review-dita-guide`, traversing the generated map → topics and checking for:
- Missing href targets
- Duplicate topic `@id` values across the guide
- Cross-file structural issues

```bash
python review-dita-guide/scripts/review_dita_guide.py ./output/root.ditamap --best-practices
```

---

## Running the full pipeline

```bash
# Full pipeline (all 5 stages)
python pdf-to-dita/scripts/pipeline.py input.pdf ./output

# With custom map title
python pdf-to-dita/scripts/pipeline.py input.pdf ./output --map-title "My Product Guide"

# Skip Stage 5 for faster iteration
python pdf-to-dita/scripts/pipeline.py input.pdf ./output --skip-review

# Resume from extracted JSON (skip PDF re-extraction)
python pdf-to-dita/scripts/pipeline.py --from-json extracted.json ./output

# Full verbose report
python pdf-to-dita/scripts/pipeline.py input.pdf ./output --format full
```

**Summary report output:**
```json
{
  "overall": "ok",
  "output_dir": "./output",
  "stages": [
    { "stage": "extract",  "status": "ok", "elapsed_s": 3.2 },
    { "stage": "chunk",    "status": "ok", "elapsed_s": 0.4 },
    { "stage": "validate", "status": "warnings", "elapsed_s": 1.1 },
    { "stage": "optimize", "status": "ok", "elapsed_s": 1.3 },
    { "stage": "review",   "status": "ok", "elapsed_s": 2.0 }
  ],
  "validation":   { "total_files": 8, "valid": 8, "total_errors": 0, "total_warnings": 3 },
  "optimization": { "total_topics": 7, "fixes_applied": 4, "remaining_errors": 0 },
  "review":       { "maps": 1, "topics": 7, "errors": 0, "warnings": 3 }
}
```

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | All stages succeeded, no validation errors |
| `1` | Validation errors found (DITA invalid) |
| `2` | Pipeline failure (PDF read error, missing dependency) |

---

## Integration with other skills

| Skill | Role in pipeline |
|-------|-----------------|
| `validate-dita-topic` | Stage 3 — validates each generated `.dita` |
| `validate-ditamap`    | Stage 3 — validates the generated `root.ditamap` |
| `dita-best-practices` | Stage 4 — detects and auto-fixes best-practice violations |
| `review-dita-guide`   | Stage 5 — cross-guide structural review |
| `generate-dita-topic` | Reference — topic templates match Stage 2 output format |
| `generate-ditamap`    | Reference — map template matches Stage 2 output format |
| `refactor-dita-content` | Post-pipeline — split oversized topics, add conref |

---

## Installation

```bash
# Required for Stage 1 (PDF extraction)
pip install pdfplumber

# Or install with the project optional dependency group
pip install "dita-skills[pdf]"
```

---

## Common issues

| Problem | Cause | Fix |
|---------|-------|-----|
| All topics are `concept` | PDF uses uniform font size (no headings detected) | Increase `--heading-ratio` threshold or pre-process PDF |
| Empty `<steps>` in task topics | Steps detected but content was plain text | Manually convert paragraphs to `<cmd>` elements |
| `KeyError: 'DITA_OT_DIR'` in review stage | DITA-OT not configured | Set `DITA_OT_DIR` env var or skip review with `--skip-review` |
| `ImportError: pdfplumber` | pdfplumber not installed | `pip install pdfplumber` |
| Garbled text from scanned PDF | PDF contains images, not selectable text | Run OCR first (e.g., `ocrmypdf input.pdf ocr_output.pdf`) |
| Short-desc truncated mid-word | First sentence > 50 words | Manually edit `<shortdesc>` after pipeline run |

---

## See also

- `validate-dita-topic` — standalone topic validation
- `validate-ditamap` — standalone map validation
- `dita-best-practices` — standalone best-practices analysis
- `review-dita-guide` — full hierarchical guide review
- `refactor-dita-content` — improve reuse and modularity of generated topics
