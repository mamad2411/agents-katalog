---
name: ra-fieldwork
description: >
  Handles the manual, repetitive, copy-paste-transfer labour of research work — the unglamorous fieldwork that would otherwise be done by hand.
  Use this skill for: extracting structured information from PDFs into a new or existing Excel file; transferring data between Excel files (e.g. supplemental material → working database); building codebooks or data dictionaries; constructing literature matrices or extraction databases; cross-checking two sources for consistency (citations, variables, entries); auditing lists for missing items; simplifying academic text into structured plain-language output.
  Trigger on casual phrasing too: "pull this from the PDF", "add this to my Excel", "build me a table from these papers", "check if these match", "make a codebook", "organise this into a database".
  Part of the research-assistant skill family. Domain-agnostic: works for the user's own research, thesis reviews, RA work, or any external project.
---

# RA Fieldwork

A skill for handling the manual, repetitive organisational work of research: extracting, organising, transferring, checking, and simplifying structured information across documents and files.

---

## When this skill applies

Load this skill for any task involving:

- **PDF → Excel extraction**: pulling structured fields from one or many PDFs into a spreadsheet
- **Excel → Excel transfer**: copying data from a supplemental or external file into the user's working file, respecting its existing schema
- **Database / matrix construction**: building a literature matrix, screening database, or extraction table from scratch
- **Codebook / data dictionary creation**: generating variable descriptions, value labels, and notes from a dataset or variable list
- **Cross-checking / auditing**: verifying that two sources are consistent (e.g. citations ↔ reference list, variables ↔ codebook, entries ↔ protocol)
- **Simplification / translation**: converting academic or technical text into plain structured output (e.g. for extraction forms, lay summaries, Substack posts)

---

## Core principles

1. **Schema-first**: Always establish what fields to extract before extracting. If the user provides an existing Excel, read its column headers and sheet structure first — map extracted data to that schema, do not invent new columns unless explicitly asked.
2. **Sample before scale**: For multi-document jobs, extract 1–2 items first, confirm the mapping looks right, then proceed with the full set.
3. **Explicit about gaps**: If a field cannot be found in the source, write `N/A` or leave blank — never fabricate or infer values without flagging it.
4. **Preserve existing structure**: When writing to an existing Excel, never reformat, rename, or reorder existing columns. Append new rows cleanly.
5. **Domain-agnostic**: Never assume field names, research area, or document type. Follow the user's schema or ask for it.

---

## Workflow by task type

### PDF → Excel extraction

1. **Establish schema**
   - If the user provides an existing Excel: read its headers and first few rows to understand the structure.
   - If no Excel exists: ask the user what fields to extract, or infer from context (e.g. for a lit review: Author, Year, Title, Journal, N, Method, Key findings, Notes).
   - Confirm the schema with the user before extracting.

2. **Read the PDF(s)**
   - Use the `pdf-reading` skill for all PDF access (text extraction, table extraction, rasterization for visual pages, OCR for scans).
   - For a single PDF: extract all relevant fields in one pass.
   - For multiple PDFs: loop through them, extracting one row per document (or one row per unit as defined by the schema).

3. **Map to schema**
   - Match extracted content to the confirmed column headers.
   - Mark missing fields as `N/A`.
   - If a field is ambiguous (e.g. two possible values), note both and flag for the user.

4. **Write to Excel**
   - Use the `xlsx` skill for all Excel read/write operations.
   - If writing to an existing file: `load_workbook`, find the last populated row, append new rows.
   - If creating a new file: build headers from the schema, then populate rows.
   - Always run `recalc.py` if the file contains formulas.

5. **Confirm and deliver**
   - Show the user a preview of the first 3–5 rows extracted.
   - Note any fields that were missing or ambiguous.
   - Present the output file.

---

### Excel → Excel transfer (supplemental → working file)

1. Read the source file (supplemental material) to understand its structure.
2. Read the destination file to understand its schema.
3. Map source columns to destination columns — ask the user to confirm the mapping if it is non-obvious.
4. Append or update rows in the destination file, preserving all existing formatting and formulas.
5. Flag any rows that couldn't be mapped cleanly.

---

### Codebook / data dictionary

1. Read the dataset (Excel or CSV) to get variable names, types, and value ranges.
2. For each variable, generate: variable name, label (plain-language description), type (numeric/string/date), value labels (if categorical), notes.
3. Output as a new Excel sheet or file with one row per variable.
4. Ask the user to review and annotate — offer to iterate.

---

### Literature matrix / extraction database

1. Establish the extraction schema (ask for it or infer from document type).
2. Extract one row per document from the provided PDFs or from uploaded data.
3. Organise into a clean Excel matrix.
4. For systematic review work: flag screened-out items separately with reason.

---

### Cross-checking / auditing

1. Load both sources (e.g. citation list from text + reference list from bibliography).
2. Identify: items in source A missing from source B, items in source B missing from source A, mismatches (same item, different details).
3. Output a structured report: matched ✓, missing from A, missing from B, mismatches.
4. Deliver as inline markdown table or Excel, per user preference.

---

### Simplification / translation

1. Identify the target audience and output format (plain text, extraction field, lay summary, structured table).
2. Rewrite or restructure the source content accordingly.
3. For extraction tasks: output directly into the relevant schema field.

---

## Dependencies

This skill delegates to:
- **`pdf-reading` skill** (`/mnt/skills/public/pdf-reading/SKILL.md`) — for all PDF access
- **`xlsx` skill** (`/mnt/skills/public/xlsx/SKILL.md`) — for all Excel read/write operations

Read those skills before starting any task that involves their respective file types.

---

## Output defaults

| Task | Default output |
|---|---|
| PDF extraction | `.xlsx` file, one row per document |
| Excel transfer | Updated version of the destination `.xlsx` |
| Codebook | New sheet in existing `.xlsx`, or new `.xlsx` |
| Literature matrix | New `.xlsx` |
| Cross-check | Inline markdown table + optional `.xlsx` |
| Simplification | Inline text or into the relevant Excel cell |

---

## Edge cases to handle explicitly

- **Scanned PDFs**: rasterize pages and use vision extraction; note lower confidence
- **Tables embedded in PDFs**: use `pdfplumber` table extraction; rasterize if garbled
- **Supplemental Excel inside a PDF**: extract with `pdfdetach`, then treat as Excel → Excel transfer
- **Existing Excel with merged cells or complex formatting**: read structure carefully before writing; never break merges
- **Multiple documents, varying structure**: establish a common schema upfront; use `N/A` for fields not present in all documents
- **Large batches (10+ PDFs)**: confirm schema on first 2, then proceed; report summary of gaps at the end
