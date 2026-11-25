---
name: pdf-parse
description: >-
  Extract text and structure from PDF files into Markdown or plain text.
  Selects the right tool automatically: xberg for machine-readable PDFs (fast,
  Rust core, no ML overhead), marker-pdf for scanned or image-heavy PDFs
  (OCR + layout detection). Includes tool installation, update, and cleanup.
  Use before any task that requires reading PDF content.
metadata:
  version: "0.2.0"
---

# PDF Parsing

Dual-path extraction pipeline. Selects tool based on PDF type.

## Tool overview

| Tool | Best for | Backend | Install |
|---|---|---|---|
| **xberg** | Machine-readable PDFs | pdfium + Rust | `brew install xberg-io/tap/xberg` |
| **marker-pdf** | Scanned / image PDFs | ML OCR + layout | `uvx marker-pdf` |
| **pdftotext** | Fallback (text-only) | poppler | system package |

## Step 1 — Ensure tools are installed

### xberg

```bash
# Check
xberg --version

# Install (macOS)
brew tap xberg-io/tap
brew install xberg


# Install (Linux / no brew)
# Download binary from https://github.com/xberg-io/xberg/releases
# or via Docker: docker pull ghcr.io/xberg-io/xberg:latest
```

### marker-pdf

marker-pdf is invoked via `uvx` — no persistent install needed.

```bash
# Verify uvx is available
uvx --version

# Test marker-pdf is resolvable
uvx marker-pdf --version
```

If `uvx` is missing, install uv first: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### pdftotext (fallback)

```bash
# macOS
brew install poppler

# Debian/Ubuntu
apt-get install poppler-utils
```

## Step 2 — Detect PDF type

```bash
# xberg detect — confirms file is a valid PDF (returns MIME type only)
xberg detect "<path/to/file.pdf>"

# To distinguish machine-readable vs scanned, use pdfinfo
pdfinfo "<path/to/file.pdf>"
```

**Known limitation:** `xberg detect` returns `application/pdf` for all PDFs — it does NOT distinguish machine-readable from scanned. Use it only to confirm the file is a valid PDF.

**Decision rule:**

- pdfinfo shows `Pages: N` and text content present (non-zero `Characters:`) → Step 3A (xberg)
- pdfinfo shows `Characters: 0` or < 100 → Step 3B (marker-pdf, likely scanned)
- xberg unavailable → Step 3B (marker-pdf) or Step 3C (pdftotext fallback)
- Neither tool available → Step 3C (pdftotext fallback)

## Step 3 — Extract

### 3A — Machine-readable PDF → xberg

**Warning:** xberg writes WARN-level log lines to **stdout**, not stderr. Using `>` redirection captures them inside the output file. Always use `--output` to avoid polluted Markdown.

```bash
# Markdown output (default, RAG-friendly)
xberg extract "<path/to/file.pdf>" --content-format markdown --output "<output/file.md>"

# JSON output (structured tree)
xberg extract "<path/to/file.pdf>" --content-format json --output "<output/file.json>"

# With page markers (useful for large PDFs — adds <!-- page N --> separators)
xberg extract "<path/to/file.pdf>" --content-format markdown --page-markers true --output "<output/file.md>"

# Batch extraction
xberg batch "<input_dir/" --content-format markdown --output-dir "<output_dir/"

# If --output is unavailable and stdout redirect is the only option, strip WARN lines after:
xberg extract "<path/to/file.pdf>" --content-format markdown > /tmp/raw.md
grep -v '^WARN' /tmp/raw.md > "<output/file.md>"
```

### 3B — Scanned / image PDF → marker-pdf

```bash
# Standard scanned PDF
uvx marker-pdf marker_single "<path/to/file.pdf>" --output_dir "<output_dir/"

# Academic paper — LLM-enhanced (best quality, slower, requires OPENAI_API_KEY or compatible)
uvx marker-pdf marker_single "<path/to/file.pdf>" --use_llm --force_ocr --output_dir "<output_dir/"

# Force OCR without LLM
uvx marker-pdf marker_single "<path/to/file.pdf>" --force_ocr --output_dir "<output_dir/"

# Large scanned PDF — split by page range to avoid OOM
uvx marker-pdf marker_single "<path/to/file.pdf>" --page_range "0-49" --output_dir "<output_dir/part1/"
uvx marker-pdf marker_single "<path/to/file.pdf>" --page_range "50-99" --output_dir "<output_dir/part2/"
```

marker-pdf produces a subdirectory per document containing `<slug>.md` and images.

### 3C — Fallback → pdftotext

```bash
pdftotext "<path/to/file.pdf>" "<output/file.txt>"

# Preserve layout (tables, columns)
pdftotext -layout "<path/to/file.pdf>" "<output/file.txt>"
```

## Step 4 — Verify output

```bash
# Quick sanity check — word count and line count
wc -w -l "<output/file.md>"

# Check for garbled content (non-UTF8 sequences)
file "<output/file.md>"
```

If word count is suspiciously low (< 200 words for a multi-page PDF), retry with the other tool path.

## Tool maintenance

### Update xberg

```bash
brew upgrade xberg-io/tap/xberg
xberg --version
```

### Update marker-pdf

uvx always pulls the latest version on first invocation per session. To force refresh of cached venv:

```bash
uvx --reinstall marker-pdf marker_single --version
```

### Update pdftotext

```bash
# macOS
brew upgrade poppler

# Debian/Ubuntu
apt-get upgrade poppler-utils
```

### Diagnose xberg

```bash
xberg doctor
```

Reports missing system deps (tesseract, pdfium), OCR language packs, and version info.

### Clean xberg cache

```bash
# Show cache stats
xberg cache stats

# Clear all cached extractions
xberg cache clear

# Clear cache for one file
xberg cache clear "<path/to/file.pdf>"
```

### Uninstall

```bash
# xberg
brew uninstall xberg

# marker-pdf (no persistent install — clear uvx cache)
uvx cache clean marker-pdf
# or wipe all uvx caches
rm -rf "$(uvx env --path 2>/dev/null || echo ~/.cache/uv/tool-environments)"
```

## Quick decision table

| Scenario | Command |
|---|---|
| Machine-readable PDF → Markdown | `xberg extract file.pdf --content-format markdown --output file.md` |
| Scanned PDF, no LLM | `uvx marker-pdf marker_single file.pdf --force_ocr --output_dir out/` |
| Academic paper, best quality | `uvx marker-pdf marker_single file.pdf --use_llm --force_ocr --output_dir out/` |
| Large PDF (> 100 pages), machine-readable | `xberg extract --content-format markdown --page-markers true --output file.md` then split by `<!-- page N -->` markers |
| Large scanned PDF | marker-pdf with `--page_range` in chunks |
| CI / no ML deps allowed | `xberg extract` only |
| Fallback / minimal env | `pdftotext file.pdf out.txt` |
