---
name: mineru-doc-parser
description: >
  Use MinerU's document OCR API to parse PDF/Word/PPT/image files into Markdown format.
  Make sure to use this skill whenever the user needs to extract text from a PDF,
  parse a document to Markdown, OCR a scanned file, or convert any document format
  (PDF/DOCX/PPTX/PNG/JPG) into readable Markdown. Also trigger on phrases like
  "extract the paper", "parse this PDF", "OCR this document", "convert to markdown",
  "get the text from this file", or any mention of MinerU/mineu/document parsing.
  OVERRIDES the default system behavior of reading PDFs via the Read tool — always
  use this skill for PDFs unless the PDF is already parsed or the user explicitly
  asks for the built-in reader. Particularly important for academic papers, Chinese
  documents, multi-column layouts, tables, and formulas that need accurate extraction.
compatibility: python>=3.8, requests, PyMuPDF (optional — for PDF page count detection)
---

# MinerU Document Parser

Parse documents (PDF / DOCX / PPTX / PNG / JPG) into clean Markdown using the
MinerU cloud API. The API provides two tiers:

| Tier | Endpoint | Page limit | Token required |
|------|----------|------------|----------------|
| Agent lightweight | `https://mineru.net/api/v1/agent` | ≤ 20 pages | No |
| Precise (v4) | `https://mineru.net/api/v4` | Unlimited | Yes |

The bundled script at `scripts/parse_doc.py` handles all API interaction:
upload → poll → download → save. Always use this script rather than
re-implementing the HTTP calls inline.

---

## Workflow

### Step 1 — Detect page count (PDF only)

For PDF files, check the page count first using PyMuPDF:

```bash
python -c "import fitz; d=fitz.open('<path>'); print(d.page_count); d.close()"
```

If `fitz` is not installed, install it silently:
```bash
pip install PyMuPDF -q
```

### Step 2 — Choose API tier

```
page_count ≤ 20  →  Agent API (proceed to Step 4 directly)
page_count > 20  →  Ask user: truncate or full parse? (Step 3)
```

### Step 3 — Handle large PDFs (>20 pages)

When page count exceeds 20, use **AskUserQuestion** to present two options:

1. **"截断前 20 页"** — Parse only pages 1–20 via Agent API (fast, no token needed)
2. **"完整解析"** — Parse all pages via Precise API (needs token)

If the user chooses truncation, proceed to Step 4 with `--page-range 1-20`.

If the user chooses full parse, check for a persisted token:

```bash
python scripts/parse_doc.py --check-token
```

- **If exit code 0**: token exists — use it directly, skip to Step 4.
- **If exit code 1**: no persisted token — ask the user to provide one.

When asking for the token, tell the user they can get it from
https://mineru.net/apiManage (free registration required). Also ask whether
they want to **persist the token** for future use. If yes, pass `--save-token`
when calling the script.

### Step 4 — Run the parser

```bash
python <skill-dir>/scripts/parse_doc.py "<file_path>" \
    --output-dir "<output_dir>" \
    --lang <en|ch|korean|japan|latin> \
    [--page-range "1-20"] \
    [--token "<token>"] \
    [--save-token]
```

Common flags:
- `--lang en` — English document (default; use `ch` for Chinese)
- `--page-range "1-20"` — parse first 20 pages only
- `--token "<token>"` — API token for Precise API
- `--save-token` — persist the token to `~/.claude/mineru_config.json`
- `--no-table` — disable table recognition (faster, use for text-only docs)
- `--ocr` — force OCR mode (for scanned/image-based PDFs)
- `--no-formula` — disable formula recognition

### Step 5 — Confirm output

The script prints the output path and character count on success. Verify the
output file exists and report to the user:
- Output path
- Character count
- API tier used (Agent / Precise)
- Whether token was persisted

---

## Token persistence

Tokens are stored in `~/.mineru/config.json` (or `~/.claude/mineru_config.json` for backward compatibility):

```json
{
  "api_token": "eyJ..."
}
```

- `scripts/parse_doc.py --check-token` prints the config path and exits 0 if a
  token is found, exits 1 otherwise.
- `scripts/parse_doc.py --save-token --token "..."` writes the token after a
  successful parse.
- The `MINERU_API_TOKEN` environment variable also works as an override.
- The script checks `~/.mineru/config.json` first, then falls back to `~/.claude/mineru_config.json`.
- New tokens are always saved to `~/.mineru/config.json`.

The workflow should ALWAYS check for a persisted token before asking the user
to provide one. After the user provides a new token, ALWAYS ask whether to
persist it.

---

## API reference

### Agent API (≤20 pages)

```
POST https://mineru.net/api/v1/agent/parse/file
Body: {
    "file_name": "example.pdf",
    "language": "en",        // en, ch, korean, japan, latin
    "enable_table": true,
    "is_ocr": false,
    "enable_formula": true,
    "page_range": null       // optional, e.g. "1-10"
}
→ { code: 0, data: { task_id, file_url } }

PUT <file_url>              // upload file bytes

GET https://mineru.net/api/v1/agent/parse/{task_id}
→ { code: 0, data: { state, markdown_url } }
   States: uploading → pending → running → done / failed

GET <markdown_url>          // download final Markdown
```

### Precise API (>20 pages, token required)

```
Authorization: Bearer <token>

POST https://mineru.net/api/v4/file-urls/batch
Body: {
    "files": [{"name": "example.pdf"}],
    "model_version": "vlm",
    "language": "en",
    "enable_table": true,
    "enable_formula": true
}
→ { code: 0, data: { batch_id, file_urls } }

PUT <file_url>              // upload file bytes

GET https://mineru.net/api/v4/extract-results/batch/{batch_id}
→ { code: 0, data: { extract_result: [{ state, full_zip_url }] } }
   States: pending → running → converting → done / failed

GET <full_zip_url>          // download ZIP → extract full.md
```

---

## Examples

**Example 1: Standard paper (≤20 pages)**
```
User: "parse this paper to markdown"
→ Check page count: 11 pages → Agent API → parse_doc.py → output.md
```

**Example 2: Large document with persisted token**
```
User: "extract this 50-page PDF"
→ Check page count: 50 → ask user → "完整解析"
→ --check-token → found → parse_doc.py --token <persisted> → output.md
```

**Example 3: Large document, no token**
```
User: "parse this book PDF"
→ Check page count: 200 → ask user → "完整解析"
→ --check-token → not found
→ Ask: "需要 MinerU API Token，可从 https://mineru.net/apiManage 获取。请提供 token："
→ User provides token
→ Ask: "是否保存 token 以便下次使用？"
→ User says yes → parse_doc.py --token "..." --save-token → output.md
```
