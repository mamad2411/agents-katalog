---
name: scanned-pdf-ocr
description: OCR scanned PDF documents to Markdown using PyMuPDF (fitz) + pytesseract, with 250-300 DPI rendering and chi_sim+eng language support.
---

# Scanned / Text / Table PDF → Markdown

Extract content from Chinese + English PDFs into Markdown files, one `.md` per `.pdf`, saved alongside the original. Routes each PDF to the best extraction strategy automatically.

## Classification First

Before extracting, classify each PDF by sampling the first 2-3 pages:

```python
doc = fitz.open(path)
total_text = sum(len(doc[i].get_text()) for i in range(min(3, len(doc))))
total_imgs = sum(len(doc[i].get_images()) for i in range(min(3, len(doc))))
has_text = total_text > 50
```

| Signal | Classification | Tool |
|--------|---------------|------|
| `text > 50B` | Text-based PDF (contracts, typed docs) | `fitz.Page.get_text()` |
| `text == 0` and `imgs > 0` | Scanned / image-only PDF | `tesseract` OCR (see below) |
| `text == 0` and `imgs == 0` | Encrypted or corrupted | `doc.needs_pass` check |
| Dense numeric columns, financial tables | Table-heavy PDF | `pdfplumber.extract_tables()` |

Also check `doc.needs_pass` — encrypted PDFs cannot be extracted without the correct password (empty password typically fails).

## Prerequisites

```bash
pip install PyMuPDF pytesseract Pillow
# tesseract itself + Chinese language pack
brew install tesseract tesseract-lang
tesseract --list-langs    # verify chi_sim is listed
```

## Table Extraction (pdfplumber)

For financial tables (valuation sheets, NAV reports, level-4 account breakdowns), `pdfplumber` produces structured tables that `fitz.get_text()` can't preserve.

```python
import pdfplumber

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                # process cells
```

### Strategy for table-heavy PDFs

- Extract header meta (fund name, date, NAV) from page 1 via `extract_text()`
- Sum rows across all pages for a size estimate
- Check last page for summary/total rows
- Write a summary `.md` with key figures, not the full table dump
- Chinese financial valuation tables often have redacted data (`****`) — note this in the summary

**Vision-analyze shortcut for key financial pages**: For audit reports with 资产负债表, 利润表, and 现金流量表 (typically just 3-6 pages), skip tesseract OCR entirely. Instead:

**Vision-Only Extraction（全页 vision 替代方案）**: 当文档为产品手册、培训PPT等含大量图表的扫描件时，不要默认跑 tesseract。改为全 vision 流程：提取所有页为PNG（`fitz.Page.get_pixmap(dpi=200)`），逐页用 `vision_analyze` 工具提取文字，整理为结构化 md。比 tesseract 准确得多，尤其适合图表/表格/多列布局。≤24 页均适用。
1. Render the specific pages with `doc[i].get_pixmap(dpi=250)` and save as PNG
2. Use `vision_analyze` tool on each page with a targeted question asking for the specific figures you need (e.g. "extract 营业收入, 营业成本, 净利润 for 2025 and 2024")
3. This is faster (~1s/page vs ~3s/page for tesseract) and produces much cleaner table extraction — vision models understand Chinese financial table layout inherently, whereas tesseract garbles aligned columns

This works best for 10-30 page documents where only 3-6 pages contain the data you actually need.

## Core Technique

For each page of the PDF:
1. **Render** as image at **250-300 DPI** via `fitz.Page.get_pixmap(dpi=DPI)`
2. **Load** into PIL `Image` from PNG bytes
3. **OCR** with `pytesseract.image_to_string(img, lang='chi_sim+eng')`

## Script Pattern

```python
import fitz
from PIL import Image
import pytesseract
import io, os

DPI = 300

def ocr_pdf(pdf_path, md_path):
    doc = fitz.open(pdf_path)
    if doc.needs_pass:
        raise ValueError(f"Encrypted PDF: {pdf_path}")
    
    pages = []
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=DPI)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        if not text.strip():
            text = "[OCR: page is blank]\n"
        pages.append(f"--- 第{i+1}页 ---\n{text}")
    
    doc.close()
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pages))
```

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| **Encrypted PDF** | Check `doc.needs_pass` before processing. Empty password seldom works — ask the user for the actual password. |
| **Blank / image-only pages** | `image_to_string` returns `""` — detect and insert a placeholder so page count stays aligned. |
| **Conda auto-activates** | In `terminal(background=true)`, the shell may activate conda, shadowing the system Python. Use the **full path** to the correct Python (e.g. `/usr/local/bin/python3 script.py`). |
| **Large PDF (>30 pages)** | Run in background (`notify_on_complete=True`) — each page takes ~2-3 s at 300 DPI. |
| **OCR quality on tables** | Tesseract handles tables poorly. For financial reports with dense tables, consider **200-250 DPI** (faster) + post-process alignment with regex. **Better alternative: use vision_analyze on rendered key pages** — vision models extract Chinese financial tables much more accurately than tesseract (see "Vision-analyze shortcut" above). |
| **chi_sim_vert** | If the PDF contains vertical Chinese text (e.g. traditional calligraphy / seals), also pass `chi_sim_vert` in the lang string. |
| **Image-overlay PDFs (text layer + background images)** | 中信证券 绩效报告 format: the PDF has text content (column labels, disclaimers, formulas) but the actual data cells (numbers, percentages) are rendered in embedded chart/table images. `get_text()` returns ~7KB of headers and notes but ZERO data values. **Classification trap**: `text > 50B` and `imgs > 0` — looks like a text PDF, but all the numbers are in images. Fix: after classifying as TEXT, spot-check by searching for actual data values (year dates, fund codes) in the extracted text. If headers but no data values appear, fall back to rendering pages at 200 DPI and using `vision_analyze`. The key data page is usually page index 2 (0-based) containing 基本信息 + 业绩表现 + 绩效指标 tables. |
| **Redacted financial data** | Chinese fund valuation tables commonly mask position-level data with `****`. Only summary rows (totals, NAV, cash ratio) survive. Note this in the output — don't interpret `****` as missing data.
| **Tunnel vision on one document type** | When searching for specific data, don't fixate on audit reports. Fundraising plans, strategy targets, and AUM projections live in 尽调问卷 (DOCX), not audit PDFs. Always list ALL files in the directory first and search every type. See `references/chinese-audit-report-extraction.md` for the document-type-to-data map.

## Output Format

Each `.md` uses page-delimited sections:

```
--- 第1页 ---
<OCR text of page 1>

--- 第2页 ---
<OCR text of page 2>
```

Saved as `{same-dir-as-pdf}/{same-basename}.md`.

## Batch Processing (30+ PDFs)

When processing a large directory of PDFs (e.g. fund due diligence packs), run a **classification pass first** to decide extraction strategy for each file:

```python
import fitz, os

def classify(pdf_path):
    doc = fitz.open(pdf_path)
    total_text = sum(len(doc[i].get_text()) for i in range(min(3, len(doc))))
    total_imgs = sum(len(doc[i].get_images()) for i in range(min(3, len(doc))))
    doc.close()
    if total_text > 50:  return "TEXT"
    if total_imgs > 0:   return "SCAN"
    return "ENCRYPTED"
```

Print a table: `classify | pages | text | strategy | size | first-N chars` — use this to spot outliers (encrypted PDFs, unexpectedly large files) before any processing starts.

**Batch dispatch strategy:**
- **TEXT PDFs** (contracts, policies, typed docs): extract with `fitz.get_text()` — ~0.1s/page. Run sequentially, write `.md` alongside each `.pdf`.
- **SCAN PDFs** (audits, licenses, articles): OCR via `fitz.render + tesseract` — ~2-3s/page. Run in background or via `delegate_task`.
- **TABLE PDFs** (valuation sheets, NAV reports): use `pdfplumber` to extract tables + write summary `.md`.
- **ENCRYPTED**: skip with a note that the password is needed.

**OCR quality check**: After batch processing, spot-check by reading the first 10 and last 10 lines of each scanned `.md`. If excessive garbage, try 300 DPI or `chi_sim` only (less English in these docs).

## Post-Extraction Text Cleanup (Text-Based PDFs)

Text-based PDFs (`fitz.get_text()`) retain page-level artifacts and column-width line breaks. After extraction, pass the output through a cleanup pipeline.

### ⚠️ Automated Heuristics Are Not Reliable (User Preference)

Automated line-joining heuristics produce characteristic errors that require human editorial judgment to fix. The user has explicitly rejected code-based reflow in favor of **manual section-by-section formatting** for Chinese legal/regulatory documents.

**Known failure modes of automated joining:**

| Failure | Example | Cause |
|---------|---------|-------|
| **Section header merged with text** | "二、明确信托业务分类标准和要求信托公司应当以信托目的" | Section heading and following paragraph lack a blank line between them in PDF extraction |
| **Title page elements merged** | "中华人民共和国主席 江泽民２００１年４月２８日" | Two separate lines joined because neither ends with sentence-ending punctuation |
| **Inline section headers** | "解任受托人。第二节受托人" | Section heading (第二节) embedded at end of preceding article, no newline in source |
| **List item numbering lost** | "（五）不得利用..." → "不得利用..." | Number lost when preceding line was treated as end of sentence |
| **Sub-item indent collapsed** | "（一）..." | Leading whitespace stripped, list structure lost |

### Manual Formatting Workflow (Preferred)

For Chinese laws, regulations, and policy documents, format **section by section by hand** rather than with scripts:

1. **Strip page artifacts** — `<!-- Page N -->`, `PAGE \* MERGEFORMAT`, standalone `- N -`, repeated page headers like "国家金融监督管理总局规章 / 发布 / - N -"
2. **Add title** — `# 文件名` at top with a `> subtitle` line for doc number and effective date
3. **Identify and mark headings** with proper `#` hierarchy:
   - `##` for chapters: "第一章 总则", "第二章 信托的设立"
   - `###` for sections: "第一节 委托人", "第二节 受托人"
   - `**第X条**` for articles — bold the article number, then the text
   - `####` for deep attachment sub-headings
4. **Join broken paragraph lines** — within a single article/paragraph, remove line breaks inserted by PDF column wrapping
5. **Keep section boundaries** — NEVER join a heading line with its following paragraph text
6. **Handle inline section headers** — detect patterns like "。第二节受托人" and split into separate heading
7. **Format lists** — use proper markdown list syntax for sub-items: `（一）`, `（二）`, `1.`, `2.`
8. **Preserve reference links** at the end (URLs to official publication pages)

### Heading Hierarchy for Chinese Legal Documents

```
# Law/Regulation Title
> Document number, effective date

## Chapter heading (第一章 总则)

### Section heading (第一节 委托人)

**Article number**　Article text...

#### Deep sub-heading (for attachments) **(一) 资产服务信托**

**Bold sub-item**　Sub-item description...

Markdown list for sub-articles:
（一）item one
（二）item two
```

### Common Artifacts

| Artifact | Example | Action |
|----------|---------|--------|
| **Page markers** | `<!-- Page N -->` | Delete |
| **Repeated page headers** | "国家金融监督管理总局规章 / 发布 / - N -" | Delete (3 lines every page) |
| **Standalone page numbers** | "`- 1 -`" on its own line | Delete |
| **Word footer artifacts** | `PAGE  \* MERGEFORMAT 1` | Delete |
| **Broken lines within paragraphs** | "防\n范风险" → "防范风险" | Join (remove the embedded newline) |
| **Inline section headers** | "。第二节受托人" | Split into `### 第二节 受托人` on its own line |

### Step-by-Step Session Pattern

For each file in a batch:

1. `git restore --source=<original-commit>` the raw OCR output to ensure clean starting state
2. Read the entire file
3. Write the formatted version, section by section
4. `git add && git commit -m "docs: format <filename> with headings" && git push`

**Do not** attempt to script this — every document has unique structure (inline headings, table attachments, preamble formats) that heuristics cannot reliably handle.

## References

- `references/chinese-audit-report-extraction.md` — structured pattern for extracting financial data (营收/成本/利润/资产负债) from Chinese audit reports using vision_analyze instead of tesseract for tables. Includes report page layout, multi-year comparison, and fund-due-diligence-specific pitfalls (营业成本 = 0 for advisory firms, negative equity signals, etc.).

## See Also

- `scripts/batch-classify.py` — classification-first batch processor for 30+ PDF directories
