---
name: doc-normalizer
description: Convert non-Markdown documents (docx, xlsx, pptx, html, pdf) to Markdown before AI processing
model: none
token_budget: {input: 0, output: 0}
---

# Doc Normalizer Skill

**Purpose:** Ensure agents always receive **plain-text Markdown** regardless of the source format the user provides. This skill is a **pre-processing gate** — it runs before any story-generator, prd-gap-analyzer, or other skill that expects Markdown input.

## When to invoke

Invoke this skill automatically (without asking) whenever the user provides or references a file whose extension is NOT `.md`:

| Extension | Source |
|-----------|--------|
| `.docx` | Word document — PRD, spec, meeting notes |
| `.xlsx` / `.xls` | Excel — requirements matrix, test plan, roadmap |
| `.pptx` | PowerPoint — design deck, stakeholder presentation |
| `.html` / `.htm` | Web page, exported Confluence/Notion page |
| `.pdf` | Design brief, contract, scanned spec |

## Invocation (CLI)

```bash
# Single file
sdlc doc convert ./docs/prd-draft.docx

# Directory (converts all supported formats inside)
sdlc doc convert ./uploads/

# Custom output dir
sdlc doc convert ./prd.pdf --output-dir ./stories/source/
```

Output is written to `.sdlc/import/<filename>.extracted.md` (default).

## Invocation (AI chat / agent)

When a user uploads or pastes a path to a non-Markdown file:

1. Run `sdlc doc convert <path>` (or `python3 scripts/doc-to-md.py <path>`).
2. Read the resulting `.extracted.md` file.
3. Continue with the intended skill (e.g. `prd-gap-analyzer`, `story-generator`).

Do **not** attempt to parse binary file content directly from a chat attachment. Always extract first.

## Dependencies

Libraries are installed **automatically** by `./setup.sh` and `bootstrap-sdlc-features.sh` (best-effort, non-fatal). No manual step is required after initial setup.

To install manually (e.g. on a new machine without re-running setup):

```bash
pip install pypdf pdfplumber mammoth python-docx openpyxl python-pptx \
            beautifulsoup4 html2text trafilatura
```

All libraries are optional per format; the script degrades gracefully if one is missing.

To skip the automatic install during setup: set `SDL_SKIP_DOC_LIBS=1` before running `./setup.sh`.

## Output contract

The extracted `.md` file:
- Starts with `<!-- source: <filename> ... -->` provenance comment.
- Uses ATX Markdown headings (`#`, `##`, …) where the source had structure.
- Tables from spreadsheets are rendered as GitHub Flavored Markdown tables.
- Slide decks: one `## Slide N: <title>` section per slide.
- PDFs: one `<!-- page N -->` comment per page boundary.

## Guardrails

- Files larger than 10 MB are rejected; split before converting.
- Macro-enabled Office files (`.xlsm`, `.docm`) are treated as read-only data; macros are never executed.
- Scanned (image-only) PDFs produce empty or minimal output — advise the user to OCR first if text extraction is empty.
- Never commit raw binary files to the repo; commit only the extracted `.md`.

## Related

- `skills/shared/prd-gap-analyzer/` — consumes the extracted Markdown.
- `skills/shared/story-generator/` — ingests the normalized text to build Master Stories.
- `rules/ask-first-protocol.md` — ask before overwriting an existing `.extracted.md`.
- `scripts/doc-to-md.py` — implementation.
- `cli/lib/executor.sh` (`cmd_doc`) — `sdlc doc convert` entry point.
