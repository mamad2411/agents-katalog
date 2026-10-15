---
name: read-pdfs
description: Read, search, summarize, quote, and extract tables from existing PDF files without loading the whole file into context. Use whenever the user wants to read, summarize, search, analyze, or ask questions about a PDF — especially long, large, scanned, or image/figure-heavy ones (reports, papers, contracts, manuals, financial statements, slide decks) — including requests like "read/summarize this PDF", "what does the chart/figure on page N show", or "extract the tables", and any work involving one or more .pdf files even when the user does not say "convert". It works by converting the PDF once into a token-efficient Markdown workspace with page-anchored image placeholders, then rendering only the page(s) needed to see a figure. This reads PDFs that already exist; it does not create, generate, fill, sign, or export PDFs. Prefer it over dumping a PDF into context.
---

# read-pdfs

Read PDFs without burning tokens. A PDF dropped straight into context is expensive and often mostly images. This skill converts a PDF **once** into a Markdown workspace whose text is cheap to read, leaves **placeholders** where images/figures/charts were, and renders **only the page(s)** whose visuals actually matter for the task.

## Mental model

1. **Ingest once** → `pdf_to_markdown.py` builds a workspace folder per PDF (original + `.md` + `manifest.json`).
2. **Read the Markdown** → all text, headings, and tables are there; images appear as placeholder tokens like `🖼 [[fig:p4:1]]`.
3. **Render on demand** → only when the actual pixels of a figure matter, render that one page to a PNG and read it.

The payoff: token cost scales with *what you look at*, not with the size of the PDF.

## Prerequisites

The scripts need `pymupdf4llm` and `pymupdf`. If a run reports a missing module, install them:

```bash
pip install -r requirements.txt
```

`pymupdf4llm` is preferred (it produces structured Markdown and marks image positions). If it is absent the converter falls back to plain-text extraction and says so — still usable, but with less structure.

> **Running the scripts.** Invoke them with the full path to wherever this skill is installed (the bare `scripts/...` form only works when the current directory is the skill root). On Windows/PowerShell, double-quote any path that contains spaces:
>
> ```bash
> python "<skill-dir>/scripts/pdf_to_markdown.py" "path/to/report.pdf"
> ```
>
> After conversion, the exact render command — with absolute paths already filled in — is written into the converted file's front matter; copy it from there rather than reconstructing it.

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Ingest the PDF  (run pdf_to_markdown.py)
- [ ] Step 2: Read the .md    (text, tables, figure index, placeholders)
- [ ] Step 3: Render a page   (only when a visual must be seen, then Read the PNG)
```

### Step 1 — Ingest the PDF

Run the converter on the PDF. It creates a clean workspace folder named after the file:

```bash
python "<skill-dir>/scripts/pdf_to_markdown.py" "path/to/report.pdf"
```

This produces (next to the PDF by default):

```
report/
├── report.pdf        # the original, copied in (workspace is self-contained)
├── report.md         # Markdown + YAML front matter + image placeholders
└── manifest.json     # structured record of what's in the .md vs the original
```

Useful flags: `--out-dir DIR` (put the workspace somewhere else), `--force` (overwrite an existing workspace), `--move` (move the original in rather than copy), `--dpi N` (default render DPI recorded in the front matter). The script prints a JSON summary including the workspace path and the exact render command — keep it.

If the workspace already exists from a previous run, do not re-convert; just read the existing `.md`.

### Step 2 — Read the Markdown

Read `report/report.md`. It opens with front matter (page count, figure/table counts, the render command) and a **"Figure & image index"** table mapping every placeholder to its page and caption. The page body follows, one `## Page N` section per page, with tables rendered as Markdown and visuals shown as inline placeholders.

For most questions — summaries, quotes, table data, "where is X discussed" — the Markdown alone is enough. Answer from it and cite page numbers.

### Step 3 — Render a page only when a visual is needed

When the task genuinely needs to *see* a figure, chart, diagram, photo, or a scanned page (not just its caption), find its placeholder in the `.md`, read the page number from the token, render that page, then Read the resulting PNG:

```bash
python "<skill-dir>/scripts/render_page.py" "path/to/report" 4
```

`render_page.py` accepts a workspace folder (or a direct `.pdf` path) and a 1-based page spec: `4`, `3-5`, `1,4,7`, or `2-3,9`. It writes `report/pages/page-004@150dpi.png`, caches it, and prints the path. Then Read that PNG to view the page.

Only the `p<N>` segment of a token is the page number; the trailing `:n` just disambiguates multiple visuals on the same page. For `[[fig:p4:2]]`, render page **4**.

**Feedback loop:** if fine print or a dense chart is hard to read, re-render at higher resolution with `--dpi 220` (or `300`). For a quick glance, `--dpi 100` is cheaper.

## Placeholders at a glance

- `🖼 [[fig:p4:1]] — image (~300×180) not shown; render page 4 to view.` — an image/figure at that spot on page 4. The caption usually follows on the next line and appears in the figure index.
- `⚠ [[fig:p3:1]] — scanned / image-only page; render page 3 to read.` — little/no extractable text; render to read it.
- Token shape is `[[fig:p<page>:<n>]]`. To list every visual, grep the `.md` for `[[fig:` or read the front-matter figure index.

Full placeholder spec and parsing details: see [references/placeholders.md](references/placeholders.md).

## Tips

- **Multiple PDFs:** convert each into its own workspace (one folder per file). Cross-reference by page.
- **Large PDFs (hundreds of pages):** still convert once; read the `.md` and the figure index, and render pages selectively. Avoid rendering many pages "just in case" — that defeats the purpose.
- **Scanned / image-only PDFs:** the text will be sparse. Render the relevant pages and read them as images. For automated OCR instead of vision, see [references/conversion-internals.md](references/conversion-internals.md).
- **Don't re-dump the PDF:** once a workspace exists, work from the `.md` + targeted renders rather than loading the original PDF into context.

## Reference files

- [references/placeholders.md](references/placeholders.md) — placeholder token format, the figure index, scanned-page markers, and how to find/parse them.
- [references/conversion-internals.md](references/conversion-internals.md) — how conversion works, caption/scanned heuristics and their tunable constants, DPI guidance, OCR, a Playwright-based rendering alternative, and troubleshooting (encrypted/huge PDFs).
