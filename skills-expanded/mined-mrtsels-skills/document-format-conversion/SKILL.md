---
name: document-format-conversion
description: Convert Word (.doc/.docx) to Markdown, Excel (.xlsx) to CSV, PDF to Markdown (text extraction + OCR), and RAR/zip to plain files on macOS. Covers archive prep, encoding issues with Chinese filenames, classification of text vs scanned PDFs, batch OCR with tesseract, table extraction with pdfplumber, file naming conventions, and macOS-specific tooling (textutil, unar, qpdf).
---

# Document Format Conversion (macOS)

Converts Chinese financial/regulatory document bundles: extract archives → clean artifacts → convert formats.

## Zip 创建（中文文件名）

### macOS 自带 `zip` 命令会乱码

macOS 的 `zip`（Info-ZIP 3.0）在打包含中文文件名的文件时，不设置 UTF-8 bit flag，导致解压后文件名变成乱码（如 `备选池` → `�备�?��?池`）。

**可靠方法：用 Python `zipfile` 模块创建**

```python
import zipfile, os

with zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, os.path.dirname(source_dir))
            zf.write(full_path, rel_path)
```

Python 的 `zipfile` 模块正确处理 UTF-8 文件名编码，解压后中文文件名可正常显示。

### 排除特定文件

```python
with zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, start)
            # 排除条件
            if rel_path == '排除的文件名':
                continue
            if f == '.DS_Store':
                continue
            zf.write(full_path, rel_path)
```

## Archive Prep

### Zip (Chinese filenames)

macOS built-in `unzip` frequently fails with **"Illegal byte sequence"** when the archive stores Chinese filenames as UTF-8 bytes without setting the UTF-8 bit flag (common with zips created on macOS or newer tools that write UTF-8 but omit the flag). This is NOT cosmetic — `unzip` refuses to extract entirely.

**Root cause**: The zip spec's general purpose bit 11 signals UTF-8 filenames. When bit 11 is unset, readers assume CP437/OEM encoding. If the actual bytes are UTF-8, macOS `unzip` gets illegal byte sequences and aborts.

**Reliable extraction: read raw bytes from central directory**

The zip's central directory stores the filename as raw bytes. Read those bytes directly, then try multiple decodes:

```python
import struct, os, shutil, zipfile

def extract_zip(src, dst):
    """Extract zip with Chinese filenames, auto-detecting encoding."""
    os.makedirs(dst, exist_ok=True)
    with open(src, 'rb') as f:
        data = f.read()
    
    # Parse central directory
    eocd_sig = b'\x50\x4b\x05\x06'
    eocd_pos = data.rfind(eocd_sig)
    cd_offset = struct.unpack_from('<I', data, eocd_pos + 16)[0]
    
    pos = cd_offset
    while data[pos:pos+4] == b'\x50\x4b\x01\x02':
        fn_len = struct.unpack_from('<H', data, pos + 28)[0]
        extra_len = struct.unpack_from('<H', data, pos + 30)[0]
        raw_name = data[pos+46:pos+46+fn_len]
        total = 46 + fn_len + extra_len + struct.unpack_from('<H', data, pos + 32)[0]
        pos += total
        
        # Try decodes in order: UTF-8 first, then GBK (Windows), then CP437 (fallback)
        for enc in ['utf-8', 'gbk', 'cp437']:
            try:
                decoded = raw_name.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            decoded = raw_name.decode('utf-8', errors='replace')
        
        outpath = os.path.join(dst, decoded)
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with zipfile.ZipFile(src) as zf:
            zinfo = zf.infolist()[i]  # match by order
            # Need to track i — see full script in references/zip-chinese-extraction.md
```

**Full reusable script** in `references/zip-chinese-extraction.md`.

**Quick alternative (when unzip works but garbles):**

```bash
unzip -q "文件名.zip" -d output_dir/
# Then rename manually — but only if unzip didn't crash
```

**Always clean up macOS metadata after extraction:**
```bash
find output_dir -name '__MACOSX' -type d -exec rm -rf {} + 2>/dev/null
find output_dir -name '.~*' -delete
find output_dir -name '.DS_Store' -delete
```

### RAR (macOS)

**Do NOT use pure-Python `rarfile`** for actual extraction — it frequently fails with `BadRarFile: Failed the read enough data` on real archives (RAR v4 Win32).

**Reliable approach:** Install `unar` (The Unarchiver CLI) via Homebrew:

```bash
brew install unar
unar archive.rar -o output_dir/
```

`rarfile` IS useful for **listing** archive contents (works on all RAR versions):
```python
import rarfile
rf = rarfile.RarFile('archive.rar')
print(rf.namelist())
```

## Word → Markdown

### .docx (modern format) → text

Use `python-docx` for structured extraction (paragraphs, tables):
```bash
pip install python-docx
```

For quick text-only conversion on macOS:
```bash
textutil -convert txt file.docx -output /tmp/out.txt
```

### .doc (old binary format) → text

**❗ `python-docx` raises `PackageNotFoundError` on old-format `.doc` files**
This is normal — python-docx only supports .docx (OOXML). Do not chase this error; it is not a broken install.

`textutil` (macOS built-in) is the correct tool:
```bash
textutil -convert txt old.doc -output /tmp/out.txt
```

The output is plain text (no formatting). For Chinese docs, `textutil` handles GBK/UTF-8 correctly.

After getting plain text, structure it into Markdown:
- Identify headings (numerical patterns like `一、`, `（一）`, `1.`)
- Format tables by aligning `|` pipes manually (textutil flattens tables to tab-separated lines)
- Remove duplicate content (textutil sometimes duplicates paragraphs)
- Split into H1/H2/H3 sections based on heading levels

**Batch pattern — mixed PDF + .doc bundles** (e.g. regulatory docs):
```python
import fitz, os, subprocess

base = '/path/to/docs/jul-28-laws'
for f in os.listdir(base):
    path = os.path.join(base, f)
    md = path.rsplit('.', 1)[0] + '.md'
    if f.endswith('.pdf'):
        doc = fitz.open(path)
        lines = [f'<!-- Page {i+1} -->\n{doc[i].get_text()}' for i in range(doc.page_count)]
        doc.close()
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))
    elif f.endswith('.doc') and not f.startswith('~'):
        subprocess.run(['textutil', '-convert', 'txt', path, '-output', md], check=True)
```

Then `rm .gitkeep; git add ; git commit -m "feat: add N docs with OCR markdown"`.

### .docx → Markdown (structured)

For better Markdown output (preserving tables, lists, headings), use `python-docx` to parse the document tree:
```python
from docx import Document
doc = Document('file.docx')
for p in doc.paragraphs:
    if p.style.name.startswith('Heading'):
        level = p.style.name.replace('Heading ', '')
        print(f"{'#'*int(level)} {p.text}")
    else:
        print(p.text)
```

But for simplest workflow, `textutil` to text then manual Markdown formatting is often faster for Chinese regulatory docs with complex table structures.

## Excel → CSV

Use `openpyxl` (always available if pandas is installed):

```python
import csv, openpyxl

wb = openpyxl.load_workbook('file.xlsx', data_only=True)
ws = wb.active

# Find the actual column range (skip empty trailing cols)
max_col = 0
for row in ws.iter_rows():
    for cell in row:
        if cell.value is not None:
            max_col = max(max_col, cell.column)

with open('output.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    for row in ws.iter_rows(min_col=1, max_col=max_col, values_only=True):
        w.writerow(list(row))
```

**Tips:**
- `data_only=True` gives computed values, not formulas
- `utf-8-sig` BOM makes Chinese CSV open correctly in Excel on Windows
- Handle merged cells: only the top-left cell has the value; others are None

## Batch Post-Extraction Cleanup

After unzipping, run these to remove macOS metadata:

```bash
# __MACOSX directories
find . -name '__MACOSX' -type d -exec rm -rf {} + 2>/dev/null

# Temp/lock files from Office
find . -name '.~*' -delete

# .DS_Store
find . -name '.DS_Store' -delete
```

## PDF → Markdown

macOS PDFs fall into four categories: text-extractable, scanned images, mixed-content, or table-heavy. Each needs a different approach.

### Prerequisites

```bash
# Text extraction
pip install pymupdf    # fitz

# OCR for scanned PDFs
brew install tesseract tesseract-lang
pip install pytesseract pdf2image Pillow

# Table extraction
pip install pdfplumber

# Encrypted PDF handling
brew install qpdf
```

### 0. Batch Strategy: Scan → Classify → Route

For bundles of 5+ PDFs, do a single pass to classify ALL files before processing any:

```python
import fitz, os

def classify(path):
    doc = fitz.open(path)
    txt = sum(len(doc[i].get_text()) for i in range(min(3, len(doc))))
    imgs = sum(len(doc[i].get_images()) for i in range(min(3, len(doc))))
    doc.close()
    if txt > 100:
        return "TEXT"
    if txt > 0 and imgs > 0:
        return "MIXED"  # typed doc WITH embedded images/charts
    if imgs > 0:
        return "SCAN"
    return "TEXT"

for p in sorted(pdfs):
    tag = classify(p)
    print(f"[{tag}] {p}")
```

Then dispatch each category in parallel — delegate_task for TEXT PDFs, terminal background for SCAN (slow OCR), direct processing for tables. This cuts total wall-clock time by 3-5x on 30+ files.

### 1. Quick Classification

Check each PDF individually:

```python
import fitz
doc = fitz.open("file.pdf")
p0 = doc[0]
txt = p0.get_text()
imgs = p0.get_images()
print(f"text={len(txt)}B images={len(imgs)}")
doc.close()
```

Decision tree:
- `text > 100B and imgs == 0` → text extraction (fitz) — contracts, performance reports, typed policies
- `text > 0 and imgs > 0` → mixed content — run fitz extraction first; images are often decorative (logos, charts) and OCR adds little value
- `text == 0 and imgs > 0` → scanned document — OCR (tesseract)
- Tabular layout (columns of numbers, accounting codes, few paragraphs) → pdfplumber, then **summarize** (see §4 below)
- Encrypted → try qpdf --decrypt; if fails, skip and report

### 2. Text-Based PDFs (fitz)

Extracts all selectable text per page:

```python
import fitz
doc = fitz.open("file.pdf")
text = []
for i, page in enumerate(doc):
    txt = page.get_text()
    if txt.strip():
        text.append(f"--- Page {i+1} ---\n{txt}")
doc.close()
content = "\n\n".join(text)
with open("file.md", "w") as f:
    f.write(content)
```

### 3. Scanned PDFs (tesseract OCR)

Render each page to image, then OCR:

```python
import fitz, pytesseract, io
from PIL import Image

doc = fitz.open("file.pdf")
pages_text = []
for i in range(len(doc)):
    pix = doc[i].get_pixmap(dpi=250)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    pages_text.append(f"--- Page {i+1} ---\n{text}")
doc.close()

content = "\n\n".join(pages_text)
with open("file.md", "w") as f:
    f.write(content)
```

**Pitfalls:** 300 DPI is ~2x slower than 250 with marginal accuracy gain. Last pages (footnotes, watermarks) OCR poorly. Audit reports (24+p) take ~55-65s each at 250 DPI.

### 4. Table-Heavy PDFs (pdfplumber) → Summarize, Don't Export

For valuation sheets, NAV tables, balance sheets — the user's instruction is:
**"是表格的话总结大致内容"** (tables → summarize; documents → full markdown).

Decision rule:
- Tabular layout?  → extract metadata (date, NAV, totals) + highlight significant rows, write as a short .md summary
- Not tabular? → full text extraction to .md (fitz or OCR as appropriate)

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    p0_text = pdf.pages[0].extract_text()  # meta: dates, NAV
    last_text = pdf.pages[-1].extract_text()  # summary rows
    
    # For redacted valuation data (**** hidden positions):
    sample_pages = [1, 2, len(pdf.pages)-1]
    holdings = set()
    for si in sample_pages:
        page = pdf.pages[si]
        tables = page.extract_tables()
        for t in tables:
            for row in t:
                if len(row) >= 13 and row[12] and '%' in str(row[12]):
                    try:
                        pct = float(row[12].replace('%',''))
                        if pct > 0.5:  # significant holdings
                            holdings.add((row[12], row[1]))
                    except: pass
```

Valuation data is often redacted (`****`) for non-public positions. Market value percentages (`市值占比`) and top-level totals are usually visible.

Write the summary as a structured .md with: ##基本信息 (date, NAV, asset value), ##概览 (row count, page count), ##汇总信息 (balance sheet totals, cash ratio, NAV breakdown), and optionally ##主要持仓 for visible holdings.

### 5. Encrypted PDFs

```bash
for pw in "" "123456" "password" "000000" "111111"; do
  qpdf --decrypt --password="$pw" in.pdf out.pdf && break
done
```

If none work, report and skip.

See `references/pdf-processing-workflow.md` for a full batch-processing example.

## Post-Conversion: File Organization & Cleanup

After converting Office files to md/csv, reorganize the flat directory into a categorized structure.

### Naming Convention for References Directory

Use English lowercase + en-dash naming:
- `company-profiles/` not `公司资料/`
- `a500-index-enhanced-fact-sheet-20260116.csv` not `1-和美水豚中证A500指数增强（要素表）20260116.csv`
- Old/duplicate versions get `-old` suffix: `flexible-hedge-2-fund-contract-old.pdf`

### Category Organization

Numbered prefix directories by category:

```
01-company-profiles/       公司基础资料（营业执照、章程、尽调问卷、财务报表）
02-internal-policies/      公司内部制度（信息披露、风险管理）
03-audit-reports/          审计报告（按年份）
04-fund-contracts/         基金合同（按产品策略）
05-fund-fact-sheets/       产品要素表（xlsx转csv后）
06-valuation-reports/      资产估值表
07-filing-screenshots/     备案类型截图（PNG）
08-performance-attribution/绩效归因报告
```

Move files with `os.rename()` in a Python script — batch all moves to avoid partial state.

### Source File Cleanup

After conversion, delete original Office files when their converted equivalents exist:

- If `file.md` exists, delete `file.doc` / `file.docx`
- If `file.csv` exists, delete `file.xlsx`

This keeps only the portable formats (md/csv) plus native PDFs/PNGs that can't be meaningfully converted.

### Evidence Format Preference

For formal submission packages (asset pool applications, due diligence packets), **deliver evidence files in PDF or DOCX format, not .md**. The .md file is a working copy; the final deliverable must be a proper document format.

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

doc = Document()
style = doc.styles['Normal']
font = style.font
font.name = '仿宋'
font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋')

with open('source.md', 'r', encoding='utf-8') as f:
    for line in f:
        text = line.strip()
        if not text:
            doc.add_paragraph('')
        elif text.startswith('## '):
            p = doc.add_paragraph()
            run = p.add_run(text[3:])
            run.bold = True; run.font.size = Pt(14)
        elif text.startswith('### '):
            p = doc.add_paragraph()
            run = p.add_run(text[4:])
            run.bold = True; run.font.size = Pt(12)
        elif text.startswith('# '):
            p = doc.add_paragraph()
            run = p.add_run(text[2:])
            run.bold = True; run.font.size = Pt(16)
        elif text.startswith('|'):
            continue
        else:
            doc.add_paragraph(text)

doc.save('output.docx')
```

### Numbered Evidence Prefix Scheme

When organizing evidence files for admission conditions, use a hierarchical numbering scheme matching the application form:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `0–` | Cover form (always first) | `0–申请表.docx` |
| `1-1–` | Condition 1, item 1 | `1-1–私募基金管理人公示信息.pdf` |
| `1-2–` | Condition 1, item 2 | `1-2–营业执照副本.pdf` |
| `2–` | Condition 2 (single item) | `2–财务报表.pdf` |
| `3-1-1–` | Condition 3, item 1, file 1 | `3-1-1–对冲1号基金合同.pdf` |
| `3-2-1–` | Condition 3, item 2, file 1 | `3-2-1–对冲1号估值报告.pdf` |
| `5-1–` | Condition 5, item 1 | `5-1–尽调问卷.docx` |

Rules:
- Use en dash (U+2013 `–`) between number and Chinese name, not space or hyphen
- Single-item conditions drop the sub-index: `2–` not `2-1–`
- File references in the application form's evidence column must match the actual filenames
- Keep only application-referenced files; remove stale intermediate artifacts

### Date Directory Convention

Work-in-progress goes in date-stamped directories for chronological sorting:

```
jul-06/      ← leading zero for proper `ls` sorting
jul-07/
aug-01/
```

### Workspace Layout

```
project/
├── AGENTS.md          ← auto-loaded conventions
├── references/        ← raw source materials (gitignored)
├── jul-06/            ← date-stamped working directory
│   └── dux/           ← manager/task subfolder
│       ├── 0–申请表.docx
│       ├── 1-1–*.pdf
│       └── conditions.md  ← condition summary (only doc to keep)
├── tmp/               ← temp files (zip, intermediates; gitignored)
└── .gitignore
```

### Git Push

This user's workflow requires immediate push after any commit (shared repo):

```bash
cd /path/to/project
echo "*.zip\n*.rar\n.DS_Store\n__MACOSX/" > .gitignore
git init
git add -A
git commit -m "feat: initial commit — <description>"
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

Or use `gh repo create <user>/<repo> --private` then `git push`.

See `references/file-org-workflow.md` for a complete end-to-end example from this session (多和美尽调材料, 2026-07-06).

## Running Multi-Line Python

When executing Python across multiple files from the terminal, use heredoc to avoid quoting issues:

```bash
python3 << 'PYEOF'
# multi-line python script here
print('hello')
PYEOF
```

The sandbox `execute_code` tool (which imports `hermes_tools`) may lack some packages (e.g. `rarfile`). Use `terminal()` with heredoc instead.

## Overlap with Other Skills

This skill overlaps with `ocr-and-documents` (PDF extraction) and `github` (git push workflow). Prefer this skill for end-to-end document conversion (archive→extract→convert→organize→push); use `ocr-and-documents` for standalone PDF extraction or marker-pdf workflows.

For filling Word templates (regulatory forms, asset pool applications) based on existing examples, see `references/docx-template-filling.md`.
