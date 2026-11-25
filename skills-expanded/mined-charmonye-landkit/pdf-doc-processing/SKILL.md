---
name: pdf-doc-processing
description: Use when reading, extracting, summarizing, or converting PDFs related to landscape project documentation, client briefs, reference packs, estimates, contracts, or scanned drawings.
---

# PDF Doc Processing

## Goal

Extract project-useful information from PDFs without losing page references or bloating context.

## Process

1. Identify PDF type: text PDF, scan, drawing, presentation, estimate, contract.
2. If a text layer is available, extract relevant text using available means.
3. If there is no text layer, use OCR/VLM-style processing or work page by page with screenshots/exports.
4. Save the result in the relevant project folder or `91_references` if it is a shared sample.
5. For large PDFs, create a short index: pages, topics, important excerpts, what applies to the project.
6. Do not convert the whole PDF into Markdown unless necessary.

## Extract

- Documentation scope.
- Client requirements.
- Dimensions, areas, quantities.
- Prices and price dates.
- Legal or technical constraints.
- Pages with layout examples.

## Output

- Short summary.
- Table: page -> meaning -> action.
- Requirements to move into brief, documentation, or estimate.
