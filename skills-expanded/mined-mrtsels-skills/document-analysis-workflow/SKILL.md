---
name: document-analysis-workflow
description: "Batch document intake and parallel analysis: extract text from many PDFs → cache as JSON → organize by topic → dispatch parallel subagents → combine structured summaries. For 5+ documents where each needs individual analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [documents, pdf, batch, subagents, research, analysis]
    related_skills: [ocr-and-documents, delegate_task]
---

# Batch Document Analysis Workflow

Process 5+ documents into structured summaries using parallel subagent delegation.

## When to Use

- 5–50 local PDFs/docs that each need individual structured analysis
- Content organized into natural groups (by directory, topic, or type)
- Documents have extractable text (not scanned images)

For 1–4 documents, analyze directly. For scanned PDFs, OCR with marker-pdf first.

## Workflow

```
PDFs → PyMuPDF batch extract → JSON cache
                                       → Subagent(group A) → summaries
                                       → Subagent(group B) → summaries
                                       → Subagent(group C) → summaries
                                                  ↓
                                   Combine → final document
```

## Step 1: Batch Text Extraction

Extract all PDFs to a single JSON cache for subagents to read independently.

```python
import os, json, fitz

base = "/path/to/pdf_directory"
results = []

for root, dirs, files in os.walk(base):
    for f in sorted(files):
        if not f.endswith(".pdf"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, base)
        try:
            doc = fitz.open(path)
            pages = len(doc)
            text_parts = []
            for i, page in enumerate(doc):
                txt = page.get_text().strip()
                if txt:
                    text_parts.append(f"=== P{i+1} ===\n{txt}")
            doc.close()
            full_text = "\n\n".join(text_parts)
            results.append({
                "file": rel,
                "pages": pages,
                "text_len": len(full_text),
                "text": full_text
            })
        except Exception as e:
            results.append({"file": rel, "error": str(e)})

with open("/tmp/extracted_texts.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False)
```

## Step 2: Organize into Groups

Group files by directory or filename pattern:

```python
groups = {
    "topic-a": [it for it in data if "topic-a" in it['file']],
    "topic-b": [it for it in data if "topic-b" in it['file']],
}
```

Print overview per group (pages, chars, filenames) before delegating.

## Step 3: Delegate Parallel Subagents

Use `delegate_task` with `tasks` array (up to 3 concurrent). Each subagent:

1. Reads the JSON cache: `import json; with open("/tmp/extracted_texts.json") as f: data = json.load(f)`
2. Filters files matching its assignment
3. Outputs structured Markdown per file

**Critical context to pass each subagent:**
- Exact file paths or filename patterns to match against `item['file']`
- Output format (e.g. "Chinese, dot-list format, per-file sections")
- Top-level grouping info

**Sample per-file output format:**
```markdown
【Report Name】
- Source/type/pages
- Key findings (3–5 bullet points)
- Key data (specific numbers, years, percentages)
```

## Step 4: Combine Results

Subagents return summaries as structured Markdown. Merge them into the final deliverable: a single document organized by group/section.

## Related References

- `references/ta-contract-entry.md` — Populate an Excel TA contract template with product parameters extracted from 三件套 (product prospectus + custodian account notice + registration notice PDFs/DOCX/XLS). Covers data mapping from each source document to specific yellow-highlighted cells, openpyxl merge-cell handling, and rate/date gotchas.
- `references/chinese-fund-valuation-extraction.md` — Extract fund manager names from Chinese private fund valuation sheets (PDF/xlsx/xls). Covers custodian vs manager disambiguation, scanned PDF header extraction via vision, TA export detection, and verification workflow.

## ⚠️ Pitfalls

- **Subagent context must be self-contained.** Subagents cannot see your conversation. Pass file paths, output format requirements, and language preference explicitly.
- **Subagents cannot verify external side-effects.** If a subagent writes files, it must return the absolute path so you can stat/read to verify.
- **JSON control characters:** PyMuPDF text may contain \x00 or other control chars. Use `json.dumps(..., ensure_ascii=False)` and read with strict=False if needed.
- **Large texts (~100K+ chars per PDF):** Subagents have context limits. For very long PDFs, include only key pages (first 3 + last 2) or use abbreviated extraction.
- **Chinese zip encoding:** If working with zip files from Windows containing Chinese filenames on macOS, see `bash-cli-patterns` → references/macos-zip-chinese-encoding.md. The quick fix is Python zipfile with `name.encode('cp437').decode('gbk')`.
- **Format-preserving .docx editing:** When modifying .docx files with python-docx, ONLY change existing `run.text`. Never call `p.clear()`, remove paragraphs, merge cells, or rewrite entire cells — these destroy the original formatting (font, size, paragraph spacing, run style). For text split across multiple runs (common with Chinese characters), identify the individual run indices and replace only those. See `references/python-docx-run-editing.md` for techniques.
- **NEVER infer file contents from filenames alone.** Filenames encode the subject (e.g. "阿巴马细水长流6号_估值表"), but the exact company name, manager name, dates, and figures live in the file content. Always extract text from the actual file before stating facts. This is especially critical for Chinese financial documents where the filename uses a short brand name but the full legal entity name appears only in the document body or image header. When text extraction yields partial results (e.g. scanned PDFs missing the header), use `fitz` to render the first page to an image and `vision_analyze` to read the header area. Combine multiple sources (text extraction + vision + web search) before concluding.
- **Multi-format document batches:** Financial document batches often mix PDF (text and scanned), xlsx (data-only tables), and xls (legacy format). Use fitz for PDF, openpyxl for xlsx, xlrd for xls. When xlsx/xls have minimal text (just a data row), they may be TA system exports — the fund manager name is not in the file. Cross-reference with the fund product name and web search.
- **Complex merged-cell tables in docx:** Chinese financial template docx files often use a single large table where multiple mini-tables (e.g. department list, ownership structure, core team bios) share the same table row structure in different column groups. Setting cell values by column index is critical — setting by label match alone can overwrite the wrong section. Inspect with `table.rows[r].cells[c].text` and check `gridSpan` attributes before writing. Always start from the original template (backup before editing) when the layout is complex.
