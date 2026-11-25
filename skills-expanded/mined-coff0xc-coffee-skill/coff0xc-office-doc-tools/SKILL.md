---
name: coff0xc-office-doc-tools
description: "Use when the user requests formal Office or file-based deliverables: PPT PPTX PowerPoint slides deck, DOCX Word redline comments, PDF read create review render, Excel XLSX CSV workbook chart formula table export. Requires editable files and render/OOXML/formula/format checks. Manual trigger: Use coff0xc-office-doc-tools."
---

# coff0xc-office-doc-tools

<!-- skill-id: cs-odt-9c3a15f7 -->

## Quick Rules (read this first for everyday tasks)
> **[Files first]** First confirm input/output file types, editability, original preservation, target audience, and delivery path.
> **[Structure gate]** For PPT, check narrative and visual system; for Excel, check data shape/formulas/charts; for DOCX/PDF, check styles, comments, pagination, and render evidence.
> **[Verification evidence]** Open the structure when it can be opened, render/screenshot when it can be rendered; say so explicitly when something cannot be verified.
> **[PPT rewrite]** When rewriting a defense deck from a paper/report DOCX + old PPTX, read `references/pptx-defense-rewrite.md`; do not get stuck on Presentations path version mismatches.
> **[Hard boundary]** Confirm first for uploading to external services, overwriting originals, accepting all revisions, and handling customer/private/contract/financial data.

Follow this section first for ordinary Office file tasks; expand the full gates only for artifact quality eval, formal release, or complex cross-file delivery.

## Capability
Office document-tool capability for formal file delivery in PowerPoint, Word, PDF, and Excel/CSV. It is not about "writing a paragraph"; it is about turning content into files other people can open, edit, review, print, and keep using.

This skill fits when the user says "make me a PPT / edit a DOCX / check a PDF / process an Excel file / produce a deliverable file." It puts artifact quality first: the file must exist, the content must be right, the formatting must hold, the formulas must compute, and the layout must have been looked at — completion must not be claimed on text guesswork alone.

## What It Can Deliver
- Editable `.pptx` decks: page structure, charts, tables, images, narrative logic, export checks, and preview QA.
- Editable `.docx` documents: reports, proposals, SOPs, contract drafts, comments, revisions, tables, table of contents, headers/footers, metadata cleanup recommendations.
- `.pdf` reading, review, generation, or checks: page rendering, text extraction, layout issues, page numbers, tables, images, and citation checks.
- `.xlsx` / `.csv` / `.tsv` workbooks: data cleaning, formulas, pivot/summary, charts, dashboards, conditional formatting, validation columns, and exported files.
- Delivery notes: final file path, verification method, reasons something was not verified, residual risk, and suggested manual review points.

## What Input It Can Take
- Existing PPTX, DOCX, PDF, XLSX, CSV, TSV, Markdown, images, screenshots, tables exported from web pages.
- Text outlines, meeting notes, report drafts, audit findings, experiment data, financial/operations data, brand requirements, or template files provided by the user.
- Comment requirements, rewrite requirements, format requirements, target audience, page limits, print/presentation/archive use.
- Multiple source files, e.g. "organize the PDF data into Excel, then make a one-page PPT summary."

## Safe-Use Boundaries
- Local, reversible, checkable file creation, editing, conversion, analysis, and format cleanup can be done directly.
- Do not upload user documents to external services, call paid generation/conversion services, or publish or send files unless the user explicitly confirms.
- For content containing personal information, customer data, contracts, finance, medical, identity information, or internal material, confirm de-identification, retention scope, and output directory first.
- Do not fabricate sources, signatures, seals, audit conclusions, legal opinions, financial authenticity, or official certification.
- When editing existing files, preserve the original by default and output a new file; confirm before batch overwriting, deleting, accepting all revisions, clearing comments, or removing watermarks.
- By default only local, reversible, verifiable low-risk work; confirm first for anything involving production, credentials, payment, remote writes, deletion, publishing, or permission changes.

## Why You Can Trust It
- File deliverables require an evidence chain of "file exists + content checked + visual/structural verification."
- PPT/DOCX/PDF quality cannot be judged from text extraction alone; layout work needs render or preview checks.
- Excel/XLSX cannot be judged by surface formatting alone; key formulas, reference ranges, error values, and chart sources must be checked.
- Editing existing files follows a minimal-change principle: preserve structure, styles, and the original file, and avoid untraceable overwrites.
- Final replies distinguish "verified," "could not be verified," and "needs manual review," and never present checks that were not run as passed.

## Typical Usage
```text
Use coff0xc-office-doc-tools to turn this Markdown into an editable PPTX with charts, narrative logic, and preview verification.
Use coff0xc-office-doc-tools to add comments and revisions to this DOCX without overwriting the original, then render-check the layout.
Use coff0xc-office-doc-tools to turn this CSV into a formatted Excel workbook with formulas, charts, and a formula error scan.
Use coff0xc-office-doc-tools to review this PDF report for layout, missing pages, broken tables, and export-ready issues.
```

## Runtime / Tool Fallback
For Office tasks, prefer plugins or MCP tools already loaded in the current session instead of hardcoded version paths.

- PPT/PPTX: prefer `presentations:Presentations`; if the path/version does not match, switch to the workspace dependency loader, Office tools, or a local OOXML/Python/JS generation path instead of repeatedly guessing plugin directories.
- DOCX: prefer `documents:documents` or Office document tools; when rendering is unavailable, do a structural check and state explicitly that visual QA is not done.
- Excel/XLSX/CSV: prefer `spreadsheets:Spreadsheets` or Office spreadsheet tools; when a full Excel engine is unavailable, only claim formula/structure checks within the supported scope.
- PDF: prefer PDF rendering/page checks; text extraction alone does not prove the layout passed.

If the goal is a formal defense PPT, thesis defense, project defense, graduation project, or "rewrite the PPT from the DOCX and old PPTX," read `references/pptx-defense-rewrite.md`.

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
