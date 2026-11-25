---
name: pdf-to-readable-markdown
description: "Extract + manually format Chinese law PDFs to readable markdown."
version: 0.1.0
author: Hermes
platforms: [macos]
tags: [PDF, Markdown, Chinese, OCR, Formatting]
---

# PDF → Readable Markdown

Extract text from Chinese law/regulation PDFs and `.doc` files, then manually format into readable markdown with proper heading hierarchy. Does NOT handle scanned-image PDFs (use `vision_analyze` per-page instead). Uses `textutil` (macOS) for old-format `.doc` files.

## When to Use

- User provides PDFs of laws, regulations, or official documents
- User says "OCR into markdown" or "转成 markdown"
- User provides `.doc` files (old Word format)
- User asks to "排版" or "format" extracted text

## Prerequisites

- PyMuPDF (`fitz`): `pip install pymupdf` (for PDF text extraction)
- `textutil`: macOS built-in (for `.doc` → `.txt` conversion)
- `python-docx`: for `.docx` files (pip install python-docx)

## Quick Reference

| Step | Tool | Command |
|------|------|---------|
| Check PDF type | `terminal` | `python3 -c "import fitz; ... get_text()"` |
| Extract PDF text | `terminal` or `execute_code` | `fitz.open().page_count; doc[i].get_text()` |
| Convert .doc | `terminal` | `textutil -convert txt -output out.txt input.doc` |
| Format manually | `write_file` | Rewrite the whole file with `#` headings and `**第X条**` |
| Verify | `terminal` | `grep -c "Page\|MERGEFORMAT" *.md` |

## Procedure

### 1. Check if PDF is text-based or scanned

```python
import fitz
doc = fitz.open("文件.pdf")
text = doc[0].get_text()
print(f"Pages: {doc.page_count}, text_len: {len(text)}")
doc.close()
# text > 0 → proceed with extraction
# text ≈ 0 → use vision_analyze per-page
```

### 2. Extract text

**For text-based PDFs**, use `execute_code` or `terminal` with PyMuPDF:

```python
import fitz
doc = fitz.open("input.pdf")
lines = []
for i in range(doc.page_count):
    lines.append(f"<!-- Page {i+1} -->")
    lines.append(doc[i].get_text())
doc.close()
# Write to .md file
with open("output.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
```

**For `.doc` files** (old Word format), use macOS `textutil`:

```bash
textutil -convert txt -output /tmp/output.txt input.doc
```

Then move the result: `mv /tmp/output.txt docs/target/output.md`

**For `.docx` files**, use `python-docx`:

```python
from docx import Document
doc = Document("input.docx")
text = "\n".join(p.text for p in doc.paragraphs)
```

### 3. Format manually with `write_file`

Read the extracted text, then rewrite the whole file. Follow these rules:

**Remove PDF artifacts:**
- `<!-- Page N -->` markers — delete
- Repeated page headers (e.g. `国家金融监督管理总局规章\n国家金融监督管理总局发布\n- N -`) — delete
- `PAGE  \* MERGEFORMAT N` footers — delete
- Trailing spaces on every line — strip

**Add title:**
```markdown
# 信托公司管理办法

> 国家金融监督管理总局令2025年第8号，自2026年1月1日起施行
```

**Heading mapping:**

| Source text | Markdown |
|---|---|
| `第一章 总则` | `## 第一章 总则` |
| `第一节 委托人` | `### 第一节 委托人` |
| `第一条 ...` | `**第一条**　...` (bold article number only) |
| `一、总体要求` | `## 一、总体要求` |
| `（一）回归信托本源` | `### （一）回归信托本源` |
| `1. 家族信托。` | `**1. 家族信托。**` (bold item number + name) |

**Paragraph joining** (critical — do NOT automate):
- Group text by blank lines (each group = one paragraph)
- Within a group, join all lines into one paragraph (PDF breaks lines mid-sentence)
- Short lines (`第一章 总则`, `一、总体要求`) stay on their own as headings
- Inline section markers like `第二节受托人` at end of an article → split into standalone heading

**Lists:**
- `（一）` / `（二）` items → keep as bullet list, indented
- Long list items with broken lines → join into one line first, then format

### 4. Verify

```bash
# No remaining page artifacts
grep -c "<!-- Page\|MERGEFORMAT\|Page \d" *.md
# Should return 0 for all files (or 1 if "Page" appears in reference links)

# Check heading hierarchy
grep -n "^#" 文件.md
```

## Pitfalls

- **Never use a script to auto-join Chinese lines.** Chinese has no word boundaries. A script will merge "2001年4月28日" with "中华人民共和国信托法" because neither line has sentence-ending punctuation. Manual per-paragraph editing is the only reliable approach.
- **`（一）` can be both a heading and inline text.** In the same document, `（一）` might start a section (→ `###`) or be a list item within an article (→ stay as text). Manually distinguish.
- **`.doc` is NOT `.docx`.** `python-docx` only reads `.docx` (OOXML format). Old-format `.doc` files need `textutil` on macOS, or LibreOffice on Linux.
- **Some PDFs have blank lines embedded mid-paragraph.** These aren't real paragraph breaks — they're page-break artifacts. The second-pass manual edit catches these.
- **Don't forget the `.doc` original.** Keep the original `.doc`/`.pdf` alongside the `.md`. The user may have placed these for reference.
- **Git workflow (yuecai project only):** Every file change → `git add <specific path>` + `git commit` + `git push`. Never `git add .`.

## Verification

Open the formatted file and read the first page — it should be clean text with proper headings. Then run:

```bash
grep -c "<!-- Page" *.md          # expect 0
grep -n "^#" 文件.md              # expect # → ## → ###, no jumps
```
