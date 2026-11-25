---
name: document-analysis
description: >
  This skill should be used when the user asks to "convert documents to markdown",
  "turn these PDFs into markdown", "ingest these files for analysis", "markitdown
  this folder", "extract text from these docs", "prep documents for the
  document-analysis pipeline", or any request to convert PDF / Word / PowerPoint /
  Excel / HTML / CSV / JSON / XML / EPub files into clean Markdown. It wraps
  Microsoft's MarkItDown with batch folder conversion, YAML frontmatter, a
  hash-based manifest for idempotent re-runs, per-file error isolation, and
  optional LLM image descriptions + OCR via the team OpenRouter key. It is the
  ingestion front-end of the document-analysis project.
version: 0.1.0
---

# document-analysis — document → Markdown ingestion

Convert documents into LLM-friendly Markdown using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown), with the workflow MoxyWolf needs wrapped around it. This is the `document-analysis` plugin; MarkItDown is the underlying conversion tool it wraps. This is the **ingestion stage** of the document-analysis pipeline: raw documents in, structured Markdown (with provenance) out, ready for downstream chunking, synthesis, and analysis.

MarkItDown preserves document *structure* (headings, lists, tables, links) rather than visual fidelity. The output is meant to be read by text-analysis tools, not to look pixel-identical to the source.

## Commands

| Command | What it does |
|---------|-------------|
| `/markitdown-setup` | Install MarkItDown + the document-set extras + `markitdown-ocr` + `openai` in the sandbox; report `ffmpeg`/`exiftool` availability; resolve the OpenRouter key. Run once per session before converting. |
| `/markitdown-convert` | Convert a single file or a whole folder into a mirrored Markdown tree, with frontmatter, a manifest, and optional LLM/OCR. |
| `/extract-terms` | Extract glossary/definition terms from converted Markdown into a lexicon `/glossary-promote` package (for lexicon-workbench's importer). Thin wrapper over the `document-analysis` repo's extractor. |

The `markitdown-*` commands drive `scripts/convert.py` (conversion). `/extract-terms` wraps the `document-analysis` repo's `docanalysis` package (the same code GitHub Actions runs) — see DR-003.

## Supported formats (document set)

PDF, Word (`.docx`), PowerPoint (`.pptx`), Excel (`.xlsx`, `.xls`), HTML, CSV, TSV, JSON, XML, plain text, Markdown, EPub. See `references/formats-and-extras.md` for the format ↔ dependency map. Audio transcription, YouTube, and Outlook are *not* installed by default — add those extras on demand if a corpus needs them.

## Environment

Conversion runs in the **Cowork bash sandbox** (Python 3.10+, verified). `/markitdown-setup` installs:

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]' markitdown-ocr openai --break-system-packages
```

Notes the setup command surfaces:

- **`ffmpeg`** is present in the sandbox (only matters if audio extras get added later).
- **`exiftool`** is absent — only affects image EXIF metadata, not document conversion.
- The `mammoth` console script installs to `~/.local/bin`, which may warn it's not on PATH. Harmless — the driver calls the Python API, not the console script.
- A benign `onnxruntime cpuid_info` warning prints on import. Ignore it.

## The sandbox / host path gotcha (read before running)

`scripts/convert.py` takes **explicit absolute `--input` and `--out` paths**, and the *command* resolves the correct sandbox mount at runtime — never hardcode a session path inside the script.

- The document-analysis repo on the host is `~/GitHub/document-analysis`. In the sandbox it appears under `/sessions/<session>/mnt/GitHub/document-analysis`. Discover it at runtime: `ls -d /sessions/*/mnt/GitHub/document-analysis`.
- Default output target is a `sources-md/` tree inside that repo, with the manifest (`.markitdown-manifest.json`) alongside.
- Uploaded files the user wants converted live under the session `uploads/` mount; resolve that the same way.

## Output contract

For every converted file the driver writes `<out>/<mirrored-relative-path>.md` containing:

1. **YAML frontmatter** — `source_file`, `source_type`, `sha256`, `bytes`, `converted_at` (Pacific), `converter`, `converter_version`, `ocr`, `llm_model`, `title`. Schema in `references/frontmatter-schema.md`. This makes outputs first-class citizens for Obsidian and the research-pipeline.
2. **The Markdown body** from MarkItDown.

It also maintains `.markitdown-manifest.json` in the output root: source path, sha256, status, timestamp, and the conversion settings (`ocr`, `llm_model`, `converter_version`) per file. On re-run, a file is **skipped only when both its source bytes and the effective conversion settings are unchanged** — so flipping on `--use-llm` later actually re-OCRs previously text-only files instead of silently skipping them, and a markitdown version bump triggers re-conversion. `--force` overrides regardless. This keeps re-converting a growing corpus cheap without the stale-skip trap.

Per-file failures are isolated: a corrupt or unsupported file is recorded in the manifest with its error and the batch continues. Each file also has a conversion **timeout** (`--timeout`, default 300s; `0` disables) so one hung document or stalled vision call can't freeze the whole batch — a timeout is recorded as a per-file error like any other. The final report lists converted / skipped / failed counts and every failure reason.

## LLM image descriptions + OCR

With `--use-llm`, the driver points an OpenAI-compatible client at OpenRouter (`https://openrouter.ai/api/v1`) using the team key, sets `enable_plugins=True`, and passes `llm_client` + `llm_model`. That gives two things:

- **Image descriptions** for images embedded in PPTX/images (MarkItDown's native LLM hook).
- **Embedded-image OCR** in PDF/DOCX/PPTX/XLSX via the `markitdown-ocr` plugin — scanned pages and image-heavy decks produce real text instead of blanks.

Key resolution order: `OPENROUTER_API_KEY` in the environment, else the `--openrouter-env` file (the team key lives at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/openrouter.env`). Default model is `openai/gpt-4o` (override with `--llm-model` or `MARKITDOWN_LLM_MODEL`). If no key resolves, the driver warns and falls back to text-only rather than failing.

For high-fidelity PDF beyond LLM-OCR, MarkItDown also supports Azure Document Intelligence — out of scope here, noted in `references/formats-and-extras.md`.

## Downstream handoff

This skill's job ends at clean, provenance-stamped Markdown in `document-analysis/sources-md/`. From there the document-analysis pipeline (chunking, synthesis, analysis — separate plugins/code in the `document-analysis` repo) takes over. Don't analyze content here; convert and hand off.

## What this skill does not do

- **No content analysis or summarization** — ingestion only.
- **No writes to `.git/`** and no commits — converting documents is a data operation, not a repo operation. If outputs land in a git repo, the human commits them (or a separate session does), per the team commit norm.
- **No host execution** — everything runs in the sandbox; the `codex`/host concerns of other plugins don't apply.
