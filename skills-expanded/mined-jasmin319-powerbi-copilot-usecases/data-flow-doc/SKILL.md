---
name: data-flow-doc
description: |
  Transforms a Power BI dataflow JSON export (model.json-style "raw data" file)
  into a Word document (.docx) that matches a fixed reference structure exactly —
  title block, table of contents, and the seven sections System Overview, Source
  Systems, Table Catalog (a classification + column profile per query), Core
  Business Logic, Recommended Relationships, Key Figures, and Data Governance Notes.
  Use when the user asks to "document the data flow", "turn this dataflow JSON into
  the documentation", "generate the data flow Word doc", "create the technical data
  flow documentation", "document the Power BI dataflow", "Datenfluss dokumentieren",
  or uploads a dataflow / raw-data JSON and asks for the formatted Word document.
  Do NOT use for slide decks (use pptx), a spreadsheet data dictionary (use xlsx),
  a prose document that is not this dataflow documentation (use docx directly), a
  status update (use stakeholder-comms), or live Power BI querying (use PBI tools).
cowork:
  category: writing
  icon: Flowchart
---

# Data Flow Documentation (JSON → Word)

Takes a Power BI **dataflow JSON export** and produces a Word document that
reproduces the exact structure of the bundled reference document
(`references/reference-document.docx`). Same sections, same tables, same headers
every time — only the content changes with the input.

## Overview

The input is a Power BI dataflow / "raw data" JSON (fields like `name`,
`version`, `culture`, `modifiedTime`, `pbi:mashup.queriesMetadata`,
`pbi:mashup.document`, and `entities[]` with `attributes`). The skill parses it and
builds a `.docx` in the fixed "Business and Technical Documentation" format:
a title block, a table of contents, and seven numbered sections — including one
Heading-2 block per query with a 15-row classification profile and a full
column/data-type table. The layout never varies; it mirrors the reference file.

## When to Use

- The user uploads a Power BI dataflow / raw-data JSON and wants the Word doc
- The user asks to (re)generate the business-and-technical documentation for a dataflow
- A dataflow changed and its documentation needs to be produced in the same format

## When NOT to Use

- **Slides** about the dataflow → use `pptx`
- **A spreadsheet** data dictionary or plain column list → use `xlsx`
- **A prose document that is not this dataflow documentation** (memo, SOP, letter)
  → use `docx` directly
- **A status update / leadership summary** → use `stakeholder-comms`
- **Live analysis** of a Power BI semantic model or report → use the Power BI tools

## Quick Start

```
User: (uploads dataflow.json) "Turn this into the data flow documentation"
1. Find the JSON: Glob input/**/*.json; read it with a code tool.
2. Read references/reference-structure.md (the exact layout spec) and, if useful,
   open references/reference-document.docx to mirror styling.
3. Parse the JSON: metadata, queriesMetadata (order matters), entities/attributes,
   refresh policies, and the M `document` text.
4. Invoke the built-in `docx` skill to build the file section by section, matching
   the reference structure exactly.
5. Run the fidelity checklist, save to output/, and confirm the file exists.
```

## Core Instructions

### Step 1: Locate and load the input JSON
- `Glob input/**/*.json` (also check the workspace root and any `<attached_files>`).
- Parse with a code tool — never eyeball a large JSON. Capture: `name`,
  `description`, `version`, `culture`, `modifiedTime`; each query in
  `pbi:mashup.queriesMetadata` (`queryId`, `queryName`, `loadEnabled`) **in export
  order**; each `entities[]` item (`name`, `description`, `pbi:refreshPolicy`,
  `attributes[]` = `name` + `dataType`); and the M `pbi:mashup.document` text.
- If no JSON is found, ask the user to attach the dataflow export. If a JSON is
  found but cannot be parsed, say so plainly and ask them to re-attach — never
  substitute sample data.

### Step 2: Load the structure spec
- Read `references/reference-structure.md` — it defines every section, table,
  column header, and the fixed 15 classification labels, in order.
- The output must match it exactly. When unsure about styling, open
  `references/reference-document.docx` as the visual ground truth.

### Step 3: Separate extracted facts from inferred content
- **Extracted (state as fact):** all metadata, query IDs, load flags, source
  objects/CSVs, refresh policy, and every column + data type.
- **Inferred (hedge, never assert):** Type, Granularity, Primary/foreign keys,
  Business purpose, Use-for, Special logic, Usage notes, recommended relationships,
  key figures, governance notes. Mirror the reference doc's hedging language —
  "Presumably…", "Business-inferable:", "recommended", "Not included in export".
  Base inferences only on what the data supports; do not invent column names,
  systems, or values.

### Step 4: Build the document with the `docx` skill
- Emit, in order: Title block + metadata table → Table of Contents →
  1. System Overview → 2. Source Systems → 3. Table Catalog (per-query Heading 2 +
  15×2 classification table + "Technical Structure" + Column/Data-type table) →
  4. Core Business Logic → 5. Recommended Relationships → 6. Key Figures →
  7. Data Governance Notes → closing "Quality check:" line.
- Use tables with the exact headers from the spec. Compute any counts (queries,
  entities, columns) with a code tool — do not count by hand.

### Step 5: Verify and deliver
- Run the **fidelity checklist** at the end of `reference-structure.md`
  (one block per query, both tables present, all 7 sections, hedging preserved).
- Save to `output/` as `<dataflow-name>-business-and-technical-documentation.docx`.
- Confirm with `Glob output/**/*` before telling the user it's ready.

## Output

- **Format:** Word document (`.docx`) in `output/`
- **Structure:** identical to `references/reference-document.docx` — Title + TOC +
  the 7 numbered sections, with a classification and column table per query
- **Tone:** precise and technical; inferred content explicitly hedged
- **Completeness:** every query in `queriesMetadata` documented, in export order

## Guardrails

- **Match the reference structure exactly** — never drop, reorder, or rename the
  sections, tables, or column headers defined in `reference-structure.md`.
- **Never fabricate facts** — system names, endpoints, column names, keys, or
  values. Extracted content comes straight from the JSON; inferred content is
  hedged ("Presumably", "recommended", "Not included in export").
- **Document every query**, in `queriesMetadata` export order, each with both its
  classification table and its column/data-type table.
- **Retrieve before asking** — locate and parse the JSON yourself; ask the user
  only if no dataflow JSON can be found.
- **Fail honestly** — if the JSON can't be read, say so and ask for a re-attach;
  do not produce a document from placeholder or sample data.
- **Confirm the file exists** in `output/` before announcing completion.
