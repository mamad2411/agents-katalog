---
name: documents-core
description: "Shared reference for the documents cluster: the editable-source vs rendered-artifact decision every task turns on, the format→tool matrix (DOCX/PDF/PPTX/XLSX/diagram), the ingest (OCR/NotebookLM) and publish (Mintlify/changelog) paths, and the fidelity/round-trip guardrails. USE WHEN choosing how to create, edit, extract from, or render a document — the conventions every documents spoke shares."
cluster: documents
version: 1.0.0
---

# Documents Core

Shared model for the `documents` cluster. Every spoke either keeps a file **editable** or turns
it into a **rendered artifact** — get that call right first and the tool choice follows. Keep the
matrix below consistent so no spoke contradicts another.

## 1. The defining decision: editable source vs rendered artifact

A document is processed in one of two modes, and the mode is a one-way door:

```
Editable source  ──(render)──>  Rendered artifact
  (OOXML, openpyxl,                (Playwright PDF, OCR'd text,
   .drawio XML, .md)                flattened PDF, GIF)
  round-trippable, diff-able        pixel/print fidelity, terminal — you can't edit back
```

- **Editable** — work in the native structured format (DOCX OOXML, XLSX cells+formulas, PPTX
  OOXML, `.drawio` XML, Markdown). Structure, tracked changes, and formulas survive; the file
  can be re-opened and re-edited. Default here.
- **Rendered** — produce a fixed output for delivery or print (HTML→PDF via Playwright, a
  flattened/filled PDF, OCR text from a scan, a GIF of a diagram). High fidelity, but the
  source structure is gone — treat it as terminal.

**Rule:** stay editable as long as the user might edit again; only render at the **last** step,
and state it when you do. Keep the original; write the render **alongside**, never over it.

## 2. Format → tool matrix

| Format / task | Spoke | Editable path | Rendered path |
|---|---|---|---|
| Word (DOCX) | `documents` → `docx/` | docx-js create · OOXML edit · tracked changes | export/convert to PDF |
| PDF (office) | `documents` → `pdf/` | reportlab create · pypdf merge/split · pdfplumber extract · forms fill | flatten / fill-and-flatten |
| PDF (quick NL edit) | `nano-pdf` | natural-language page ops | — |
| PowerPoint (PPTX) | `documents` → `pptx/` | html2pptx · OOXML edit · templates | thumbnail grid / images |
| Excel (XLSX) | `documents` → `xlsx/` | openpyxl + **formulas** · recalc.py | — |
| Consulting report | `documents` (ConsultingReport) | structured HTML | **Playwright PDF** (A4, TOC, headers) |
| Scanned PDF → data | `deepread-ocr` | — | OCR text + structured data **with confidence flags** |
| Corpus → notebook/podcast | `notebooklm` | sources/notebook | briefing / audio artifact |
| Docs site | `mintlify` | MDX pages + nav config | published site |
| Release notes | `changelog-generator` | Markdown changelog | — |
| draw.io diagram | `drawio-diagrams-enhanced` | `.drawio` XML | exported image |
| Mermaid → motion | `mermaid-to-gif` | `.mmd` / fenced block | **GIF** |

## 3. Ingest path (document → data)

- **OCR first, never blind.** Scanned or image-only PDFs go through `deepread-ocr`, which scores
  confidence and flags low-quality regions — surface those flags; don't pass OCR text downstream
  as if it were clean.
- **Synthesize after.** Once you have text, `notebooklm` turns a corpus into a notebook,
  briefing, or podcast. Typical chain: `deepread-ocr` → `notebooklm`.

## 4. Publish path (docs about the work)

- **`mintlify`** builds and maintains the documentation **site** (MDX pages, navigation, API refs).
- **`changelog-generator`** turns git history into user-facing release notes.
  These narrate the project; they don't process arbitrary user files — keep them distinct from the
  office-format engine.

## 5. Fidelity & conventions

- **XLSX:** always use Excel **formulas**, never hardcode computed values; run `recalc.py` after
  create/edit; deliver zero formula errors; follow input/formula/link color coding.
- **DOCX:** use the redlining (tracked-changes) workflow for review; mark only what changes,
  preserve RSIDs; verify by converting to Markdown.
- **PPTX:** web-safe fonts only; generate a thumbnail grid to visually verify before delivery.
- **PDF:** pick the library by job — pypdf (structure), pdfplumber (text/tables), reportlab
  (create); `nano-pdf` for quick NL edits; flatten only at the end.
- **Diagrams:** keep the `.drawio`/`.mmd` source in the repo; the image/GIF is the render.

## 6. Shared guardrails

- **Preserve the source**: stay in the editable format; render only at the last step and say so.
- **Render is one-way**: never overwrite the original with its rendered output.
- **No fabricated values**: formulas compute (XLSX); OCR confidence is shown, not hidden.
- **No silent flattening**: don't drop tracked changes, form fields, or layers without stating it.
- **Right tool per format**: follow the matrix above; don't reach for a generic converter when a
  format-native spoke exists.
- **Diagram-as-code**: source diagrams live as text (`.drawio` XML / Mermaid); export is derived.
