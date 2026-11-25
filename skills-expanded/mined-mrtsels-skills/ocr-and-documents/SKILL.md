---
name: ocr-and-documents
description: Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill.
version: 2.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [powerpoint]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

### ⚠️ pypdf / PyMuPDF Failure Modes

**`Resource deadlock avoided`**: pypdf and PyMuPDF can fail with this error when the file is held open by another process (e.g., browser preview, macOS Quick Look). Workarounds:
- Copy the file to `/tmp/` first, then extract
- Use browser-based extraction (see fallback below)
- Close the file in the other application

### ⚠️ Unicode Math in Modern PDFs (e.g., CambriaMath, Latin Modern)

Many modern PDFs (especially from PowerPoint/Word → PDF) embed math using Unicode
private-use characters from fonts like CambriaMath. PyMuPDF extracts these as raw
Unicode — they are NOT LaTeX. Example: `𝑝(𝜃|𝒟) ∝ 𝑝(𝒟|𝜃)𝑝(𝜃)` instead of
$p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta)p(\theta)$.

**How to detect this:**
```python
import pymupdf
doc = pymupdf.open("lecture.pdf")
text = doc[0].get_text()
# Look for private-use Unicode chars (U+E000–U+F8FF) or math Unicode blocks
has_unicode_math = any(0x1D400 <= ord(c) <= 0x1D7FF for c in text)
print("Has Unicode math:", has_unicode_math)
```

**If the PDF is text-based (no scanned images) — prefer PyMuPDF over Marker:**
- PyMuPDF is instant; Marker times out on CPU-only machines (~5min for one page)
- Unicode math is actually preserved — you just need to convert it to LaTeX
- See the `latex-ocr-guide` skill for the Unicode → LaTeX conversion workflow

**If the PDF is scanned (empty text via PyMuPDF) — use Marker:**
- Marker needs GPU or very long CPU time; warn the user about this
- CPU timeout is not a failure of the PDF — it is expected on CPU-only systems

### ⚠️ Network/Install Failures: Use Browser as Fallback

When pip installs, uv tool installs, or Docker pulls time out (slow/unreliable network):
1. Open the PDF in a browser: `browser_navigate(url="file:///absolute/path/to/document.pdf")`
2. Extract text via browser console: `browser_console(expression="document.body.innerText")`
3. This works for both local files (`file://`) and URLs (arxiv PDF, WeChat articles, etc.)

This fallback also works when local PDF tools fail due to file locks or dependency issues.

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)

---

## Quick PDF Text Edits (nano-pdf)

For small text changes in PDFs — titles, dates, typos, client names — use `nano-pdf`:

```bash
uv pip install nano-pdf

nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results'"
nano-pdf edit report.pdf 3 "Update the date to February 2026"
nano-pdf edit contract.pdf 2 "Change 'Acme Corp' to 'Acme Industries'"
```

Page numbers may be 0-based or 1-based depending on version — retry with ±1 if the edit hits the wrong page. The tool uses an LLM under the hood; verify output PDF after editing.
