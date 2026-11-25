---
name: documents-master
description: Master hub for Document, media & file generation. Use to generate documents and media: DOCX, PDF, PPTX, XLSX, Markdown, diagrams, images, and pro technical documentation/docs sites. For full AI video creation (Veo, Kling, Remotion, ffmpeg, social export) use video-ai-master. Bundles 21 specialized skills. Use for documents; use video-ai-master for video.
---

# Document & file generation — Master Hub

Use to generate documents and files: DOCX, PDF, PPTX, XLSX, Markdown, diagrams, images.

## How to use this hub

This single skill bundles **all 21 documents skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **video-production-pro** — Condensed AI video reference. **For full workflows use `video-ai-master`** (10 skills: prompts, APIs, storyboard, avatars, export).  
  → `skills/video-production-pro/GUIDE.md`
- **documentation-pro** ⭐ — Professional technical documentation: the Diátaxis framework (tutorial/how-to/reference/explanation), docs-as-code tooling (Docusaurus/Mintlify/MkDocs), OpenAPI API reference, README/ADR/runbook structures, and writing style. Use for docs sites, API docs, and developer guides.  
  → `skills/documentation-pro/GUIDE.md`
- **anthropic-doc-coauthoring** — Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This ...  
  → `skills/anthropic-doc-coauthoring/GUIDE.md`
- **anthropic-docx** — Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produ...  
  → `skills/anthropic-docx/GUIDE.md`
- **anthropic-pdf** — Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, r...  
  → `skills/anthropic-pdf/GUIDE.md`
- **anthropic-pptx** — Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text fro...  
  → `skills/anthropic-pptx/GUIDE.md`
- **anthropic-xlsx** — Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., ...  
  → `skills/anthropic-xlsx/GUIDE.md`
- **blastum-docx** — Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional document...  
  → `skills/blastum-docx/GUIDE.md`
- **blastum-markdown-exporter** — Convert markdown files to DOCX, PPTX, XLSX, PDF, PNG, HTML, IPYNB, CSV, JSON, XML, LaTeX, and extract code blocks. Use when exporting or converting markdown to other document formats.  
  → `skills/blastum-markdown-exporter/GUIDE.md`
- **blastum-markdown-to-confluence** — Upload markdown files directly to Confluence using REST API. Use when creating or updating Confluence pages from markdown documents.  
  → `skills/blastum-markdown-to-confluence/GUIDE.md`
- **blastum-markdown-to-pdf** — Convert markdown files to styled PDFs using pandoc and WeasyPrint with CSS. Use when exporting markdown documents to PDF with custom styling.  
  → `skills/blastum-markdown-to-pdf/GUIDE.md`
- **blastum-mermaid-diagrams** — Create software diagrams using Mermaid syntax. Use when users need to create, visualize, or document software through diagrams including class diagrams (domain modeling, object-oriented design), se...  
  → `skills/blastum-mermaid-diagrams/GUIDE.md`
- **blastum-pptx** — Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layo...  
  → `skills/blastum-pptx/GUIDE.md`
- **blastum-xlsx** — Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, ....  
  → `skills/blastum-xlsx/GUIDE.md`
- **exporting-to-png** — Export code, terminal output, diagrams, or UI components to PNG images using headless browser rendering or CLI tools.  
  → `skills/exporting-to-png/GUIDE.md`
- **generating-images** — >-  
  → `skills/generating-images/GUIDE.md`
- **sentry-doc-coauthoring** — Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This ...  
  → `skills/sentry-doc-coauthoring/GUIDE.md`
- **sentry-presentation-creator** — Create data-driven presentation slides using React, Vite, and Recharts with Sentry branding. Use when asked to "create a presentation", "build slides", "make a deck", "create a data presentation", ...  
  → `skills/sentry-presentation-creator/GUIDE.md`
- **pdf-pro-documents** ⭐ — Produce professional, structured, accessible PDFs: engine decision matrix (Puppeteer/Playwright HTML→PDF, @react-pdf/renderer, WeasyPrint, Typst, LaTeX, pdf-lib), typographic hierarchy, paginating tables, TOC, running headers/footers + page numbers, branding, embedded fonts + Arabic/RTL shaping, PDF/A archival & PDF/UA tagging, merge/split/stamp/watermark, fillable forms, encryption/permissions.  
  → `skills/pdf-pro-documents/GUIDE.md`
- **excel-pro-spreadsheets** ⭐ — Build professional, organized Excel workbooks: library matrix (ExcelJS / SheetJS / openpyxl / XlsxWriter), multi-sheet financial-model layout (assumptions→calcs→outputs), number/date/currency formats, named ranges, data validation/dropdowns, conditional formatting, cross-sheet formulas, tables, charts, freeze panes, protection, CSV/formula-injection security, streaming for large data, Arabic/RTL direction.  
  → `skills/excel-pro-spreadsheets/GUIDE.md`
- **contracts-pro** ⭐ — Engineer professional contracts: full anatomy (parties→signatures→schedules), versioned clause library + templating (docxtemplater / JSON→DOCX/PDF) with variables and conditional clauses, versioning/redlines, e-signature integration (DocuSign/Dropbox Sign) with webhook + document integrity, UAE/GCC bilingual Arabic/English + RTL. Engineering guidance, not legal advice — recommends lawyer review.  
  → `skills/contracts-pro/GUIDE.md`

## Pairs well with

**`video-ai-master`** — dedicated hub for AI video generation, editing, and platform export.

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
