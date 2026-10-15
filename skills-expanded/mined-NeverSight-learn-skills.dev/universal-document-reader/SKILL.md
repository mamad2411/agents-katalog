---
name: universal-document-reader
description:
  Converts any document (PDF, DOCX, images, scanned docs) to clean, LLM-friendly text. First step
  before any skill processing. Works for ANY university, ANY document type.
---

# Universal Document Reader & Converter

## Overview

**Base preprocessing skill** — Converts any document format to clean, structured text that LLMs can
process effectively. Must be run BEFORE any other skill (notes, answers, analysis, etc.) when
working with documents.

## Why This Skill Exists

LLMs cannot directly read:

- PDF files (especially scanned/image-based)
- DOCX/DOC files
- Scanned documents (images)
- Handwritten notes (images)
- Protected/encrypted documents

This skill converts them all to clean text first.

---

## Supported Input Formats

| Format                  | Extension                        | Conversion Method         | Notes                        |
| ----------------------- | -------------------------------- | ------------------------- | ---------------------------- |
| **PDF (text-based)**    | `.pdf`                           | `pdftotext` or PyPDF2     | Direct text extraction       |
| **PDF (scanned/image)** | `.pdf`                           | OCR via `tesseract`       | Requires image preprocessing |
| **Word Document**       | `.docx`, `.doc`                  | `pandoc` or `python-docx` | Preserves structure          |
| **Plain Text**          | `.txt`, `.md`                    | Direct read               | No conversion needed         |
| **Images**              | `.png`, `.jpg`, `.jpeg`, `.tiff` | OCR via `tesseract`       | For handwritten/printed text |
| **PowerPoint**          | `.pptx`                          | `pandoc`                  | Extracts slide content       |
| **EPUB**                | `.epub`                          | `pandoc`                  | E-books                      |
| **HTML**                | `.html`, `.htm`                  | `pandoc` or `lynx`        | Web pages                    |

---

## How This Skill Works

1. **User provides**: Document path (local file or URL)
2. **System detects**: File type and format
3. **System converts**: Using appropriate method
4. **System cleans**: Removes noise, normalizes text
5. **System outputs**: Clean, structured text ready for other skills

---

## Conversion Methods

### Method 1: PDF Text Extraction (Linux/Mac)

```bash
# Simple text-based PDF
pdftotext input.pdf output.txt

# With layout preservation
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 10 input.pdf output.txt
```

### Method 2: Python PDF Extraction (supports both pypdf and PyPDF2)

```python
def extract_pdf_text(pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    return '\n'.join(page.extract_text() or '' for page in reader.pages)
```

### Method 3: OCR for Scanned PDFs/Images

```bash
# Convert PDF pages to images first
pdftoppm -png input.pdf output_prefix

# Run OCR on each image
for img in output_prefix-*.png; do
    tesseract "$img" "${img%.png}" -l eng
done

# Combine all text files
cat output_prefix-*.txt > final_output.txt
```

### Method 4: Python OCR (pytesseract)

```python
import pytesseract
from PIL import Image

def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text
```

### Method 5: Word/DOCX Conversion

```bash
# Using pandoc
pandoc input.docx -t plain -o output.txt

# Or with python-docx
```

```python
from docx import Document

def extract_docx_text(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
```

---

## Text Cleaning Pipeline

After extraction, apply these cleaning steps:

```python
import re

def clean_text(text):
    # 1. Remove excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)

    # 2. Remove page numbers/headers/footers (common patterns)
    text = re.sub(r'(?m)^\d+\s*$', '', text)  # Page numbers
    text = re.sub(r'(?m)^Page \d+.*$', '', text)

    # 3. Fix broken words (hyphenation at line breaks)
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)

    # 4. Merge lines that belong together
    lines = text.split('\n')
    merged = []
    for line in lines:
        if merged and not merged[-1].endswith(('.', '!', '?', ':')):
            merged[-1] += ' ' + line.strip()
        else:
            merged.append(line)

    return '\n'.join(merged)
```

---

## Output Format

The converted text is structured as:

```
====================================================
DOCUMENT METADATA
====================================================
Source: [filename]
Pages: [page count]
Converted: [timestamp]
Type: [PDF/DOCX/Image/etc.]
OCR Used: [Yes/No]

====================================================
EXTRACTED TEXT
====================================================

[Clean, structured text content here]

====================================================
END OF DOCUMENT
====================================================
```

---

## Usage Examples

### Example 1: Basic PDF to Text

```
User: "Read this PDF: /path/to/syllabus.pdf"
Skill:
  1. Detects PDF format
  2. Runs pdftotext
  3. Cleans output
  4. Returns structured text
```

### Example 2: Scanned Document

```
User: "Convert this scanned PDF: /path/to/old-notes.pdf"
Skill:
  1. Detects scanned PDF
  2. Converts pages to images
  3. Runs OCR
  4. Cleans and structures output
```

### Example 3: Multi-format Input

```
User: "Process these files: syllabus.pdf, notes.docx, formulae.png"
Skill:
  1. Processes each format appropriately
  2. Combines into single text output
  3. Ready for next skill (notes-generator, etc.)
```

---

## Session Config

This skill integrates with the session config system (`deps/session-profile.json`). Before
executing, check for an existing session profile:

- If `deps/session-profile.json` exists, read `university`, `subject`, `pattern`, and `exam_type`
  fields to auto-configure the skill.
- If the file does not exist, fall back to user-provided context or prompt the user to run
  `setup-exam-prompt` (or `npm run init`) first.
- Session config eliminates redundant context detection — detection happens once and is reused
  across all skill calls.

---

## Integration with Other Skills

After document conversion, pass the text to:

| Next Skill                            | How to Use                                  |
| ------------------------------------- | ------------------------------------------- |
| **universal-notes-generator**         | Feed extracted syllabus/topics              |
| **universal-a-plus-answer-writer**    | Use content for answer generation           |
| **universal-pyq-analyzer**            | Process question papers                     |
| **universal-imp-topics-generator**    | Analyze extracted content                   |
| **universal-flashcard-generator**     | Create flashcards from text                 |
| **universal-formula-sheet-generator** | Extract formulas                            |
| **universal-mcq-practice-generator**  | Generate MCQs from content                  |
| **universal-session-config**          | Read university/department for format hints |

---

## Installation Requirements

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y poppler-utils tesseract-ocr pandoc python3 python3-pip
sudo apt install -y python3-pypdf python3-pytesseract python3-pil python3-docx
```

### Linux (Fedora/RHEL/CentOS)

```bash
sudo dnf install -y poppler-utils tesseract pandoc python3 python3-pip
sudo dnf install -y python3-pypdf python3-pytesseract python3-pillow python3-docx
```

### Linux (Arch/Manjaro)

```bash
sudo pacman -S poppler tesseract tesseract-data-eng pandoc python python-pip
sudo pacman -S python-pypdf python-pytesseract python-pillow
# python-docx is in AUR: yay -S python-docx  (or: pip install python-docx)
```

### Linux (Alpine)

```bash
sudo apk add poppler tesseract-ocr pandoc python3 py3-pip
sudo apk add py3-pypdf py3-pytesseract py3-pillow py3-docx
```

### Linux (openSUSE)

```bash
sudo zypper install poppler-tools tesseract pandoc python3 python3-pip
sudo zypper install python3-pypdf python3-pytesseract python3-pillow python3-docx
```

### macOS

```bash
brew install poppler tesseract pandoc python3
pip3 install pypdf pytesseract Pillow python-docx
```

### Windows (PowerShell Admin)

```powershell
# Option A: winget (built-in Windows 10/11 — recommended)
winget install XP89DCGQ3K6VLD   # poppler (pdftotext)
winget install UBMFFKJRRR9W2K   # tesseract (OCR)
winget install 9NBLGGH4W8GQ     # pandoc
winget install 9PJPW5LDXLZ5     # Python 3
pip install pypdf pytesseract Pillow python-docx

# Option B: Chocolatey
choco install poppler tesseract pandoc python3 -y
pip install pypdf pytesseract Pillow python-docx

# Option C: Scoop
scoop install poppler tesseract pandoc python
pip install pypdf pytesseract Pillow python-docx
```

### Windows (WSL/Ubuntu)

```bash
# Same as Linux Ubuntu/Debian instructions
sudo apt update && sudo apt install -y poppler-utils tesseract-ocr pandoc python3-pip
sudo apt install -y python3-pypdf python3-pytesseract python3-pil python3-docx
```

---

## Prerequisites Check

Before using this skill, verify required tools are installed:

```bash
# Check all dependencies
./scripts/check-deps.sh

# Or manually check:
which pdftotext    # PDF text extraction
which tesseract    # OCR for scanned docs
which pandoc       # Document conversion
python3 -c "import PyPDF2; print('PyPDF2 OK')"
python3 -c "import pytesseract; print('pytesseract OK')"
```

### Auto-Install (Ubuntu/Debian)

```bash
# Install all dependencies at once (system packages preferred)
sudo apt update && sudo apt install -y poppler-utils tesseract-ocr pandoc python3-pip
sudo apt install -y python3-pypdf python3-pytesseract python3-pil python3-docx
```

### Auto-Install (Arch)

```bash
sudo pacman -S poppler tesseract tesseract-data-eng pandoc python python-pip
sudo pacman -S python-pypdf python-pytesseract python-pillow
# python-docx is in AUR: yay -S python-docx
```

### Auto-Install (Fedora)

```bash
sudo dnf install -y poppler-utils tesseract pandoc python3-pip
sudo dnf install -y python3-pypdf python3-pytesseract python3-pillow python3-docx
```

---

## Error Handling

| Error                             | Cause                                | Solution                                              |
| --------------------------------- | ------------------------------------ | ----------------------------------------------------- |
| "PDF is encrypted"                | Password-protected PDF               | Provide password or use decrypted version             |
| "No text extracted"               | Scanned/image PDF                    | Use OCR mode (see Method 3)                           |
| "File not found"                  | Wrong path                           | Check file path, use absolute paths                   |
| "Corrupt file"                    | Damaged document                     | Re-download or get clean copy                         |
| "OCR failed"                      | Poor image quality                   | Improve image quality: contrast, DPI > 300            |
| "pdftotext not found"             | Missing poppler-utils                | `sudo apt install poppler-utils`                      |
| "tesseract not found"             | Missing OCR                          | `sudo apt install tesseract-ocr`                      |
| "pandoc not found"                | Missing converter                    | `sudo apt install pandoc`                             |
| "Permission denied"               | File locked                          | Check file permissions                                |
| "OCR confidence low"              | Poor scan quality (<80%)             | Increase DPI to 300+, adjust contrast/brightness      |
| "OCR language uncertain"          | Mixed language document              | Specify language: `-l eng+hin` for bilingual          |
| "Fatal OCR error"                 | Image corruption or format           | Re-save image as PNG, verify file integrity           |
| "Multi-column garbled"            | PDF has 2+ columns                   | Use `-layout` flag or column-detection OCR mode       |
| "Table structure lost"            | Tabular data extracted as loose text | Use OCR with table recognition, or `camelot`/`tabula` |
| "Image contains only handwriting" | Handwritten notes                    | Use specialized handwriting OCR (e.g., Google Vision) |

---

## Multi-Column PDF Preservation

When processing multi-column PDFs (common in research papers and textbooks), apply these steps:

1. **Detect column layout** — use `pdftotext -layout` which preserves whitespace alignment
2. **Check reading order** — verify extracted text reads left-to-right, top-to-bottom
3. **Column-aware OCR** — for scanned multi-column, use `tesseract --psm 6` (uniform block)
4. **Post-process** — reflow text by detecting short lines that indicate column breaks
5. **Validation** — compare extracted word count against estimated page word count (±10%)

```bash
# Column-aware extraction
pdftotext -layout input.pdf output.txt

# Column-aware OCR (scanned)
tesseract page.png output -l eng --psm 6

# Column-aware OCR with table detection (scanned)
tesseract page.png output -l eng --psm 4
```

If the extracted text has garbled column ordering, fall back to single-column extraction and note to
the user that some interleaving may have occurred.

## Quick Reference

### Linux/macOS

```bash
# Text-based PDF
pdftotext input.pdf output.txt

# Scanned PDF → OCR
pdftoppm -png input.pdf page && tesseract page-1.png output

# DOCX → TXT
pandoc input.docx -t plain -o output.txt

# Image → Text
tesseract image.png output -l eng

# Full pipeline (using wrapper script)
./scripts/process-document.sh input.pdf notes-generator
```

### Windows (PowerShell)

```powershell
# Install tools (pick one)
winget install XP89DCGQ3K6VLD    # pdftotext via winget
winget install UBMFFKJRRR9W2K    # tesseract via winget
winget install 9NBLGGH4W8GQ      # pandoc via winget

# Text-based PDF
pdftotext input.pdf output.txt

# DOCX → TXT
pandoc input.docx -t plain -o output.txt

# Image → Text
tesseract image.png output -l eng

# Or use Python (any OS - no native tools needed)
python -c "from pypdf import PdfReader; open('output.txt','w').write(''.join((p.extract_text() or '') for p in PdfReader('input.pdf').pages))"
```

### Python (Any OS)

```python
from pypdf import PdfReader

# Extract PDF text
reader = PdfReader('input.pdf')
text = ''.join(page.extract_text() or '' for page in reader.pages)
with open('output.txt', 'w') as out:
    out.write(text)
```

> **Note:** `PyPDF2` is deprecated. Use `pypdf` instead (or PyPDF2 if already installed).

---

## Quick Start

### Step 1: Install Dependencies

See the [Installation Requirements](#installation-requirements) section above for full per-OS
instructions (Ubuntu, Fedora, Arch, Alpine, openSUSE, macOS, Windows, WSL).

Quick reference:

```bash
# Linux (Ubuntu/Debian)
sudo apt install -y poppler-utils tesseract-ocr pandoc python3-pip
pip3 install pypdf pytesseract Pillow python-docx

# macOS
brew install poppler tesseract pandoc python3
pip3 install pypdf pytesseract Pillow python-docx

# Windows (PowerShell Admin - winget)
winget install XP89DCGQ3K6VLD UBMFFKJRRR9W2K 9NBLGGH4W8GQ 9PJPW5LDXLZ5
pip install pypdf pytesseract Pillow python-docx
```

### Step 2: Convert a Document

```bash
# Option A: Using wrapper script (recommended)
./scripts/process-document.sh notes.pdf notes-generator

# Option B: Manual conversion
pdftotext notes.pdf notes.txt
# Then use notes.txt with any skill
```

### Step 3: Chain to Any Skill

```bash
# Convert then generate notes
pdftotext syllabus.pdf - | notes-generator

# Convert then create flashcards
pandoc lecture.docx -t plain | flashcard-generator

# Convert then analyze PYQs
pdftotext pyq.pdf - | pyq-analyzer
```

---

## Full Document Pipeline

This skill is Stage 1 of a 3-stage pipeline:

```
Stage 1: PDF/DOCX → TXT    [universal-document-reader]  ← You are here
Stage 2: TXT → MD           [Manual or AI authoring]
Stage 3: MD → PDF           [universal-document-generator / scripts/convert-to-pdf.*]
```

After extracting text with this skill:

1. Structure it into Markdown notes
2. Convert to print-ready PDF using `scripts/convert-to-pdf.py` or `scripts/convert-to-pdf.js`
3. See the `universal-document-generator` skill for full instructions

---

## Integration Workflow

```
┌─────────────────┐
│  User Input     │
│  (PDF/DOCX/etc) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  universal-document-    │
│  reader                 │ ← Stage 1: Convert to clean text
│  (PDF/DOCX → TXT)       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Manual / AI Authoring  │ ← Stage 2: Structure into MD
│  (TXT → MD)             │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  universal-document-    │
│  generator              │ ← Stage 3: Convert to PDF
│  (MD → PDF)             │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│  Print-Ready    │
│  PDF Output     │
└─────────────────┘
```

## Quality Gate

Before passing extracted text to downstream skills, verify:

### OCR Quality Gate

- [ ] OCR confidence score ≥ 80% (use `tesseract page.png output -l eng --psm 6` and check log)
- [ ] No "Fatal OCR error" or "Empty page" warnings in the conversion log
- [ ] At least 50 characters extracted per page (otherwise flag as empty/noise)
- [ ] Language detection: document language matches expected language from session-config
- [ ] Handwriting detected? Flag to user that manual review is needed
- [ ] Multi-column layout handled correctly (reading order verified)
- [ ] Table structures preserved or flagged for manual reconstruction

### General Quality Gate

- [ ] File type is supported (see Supported Input Formats table)
- [ ] Conversion method matches the file type (text PDF → pdftotext, scanned → OCR)
- [ ] Text cleaning pipeline (clean_text function) has been applied
- [ ] Output format matches the DOCUMENT METADATA + EXTRACTED TEXT structure
- [ ] Source filename and conversion timestamp are recorded in metadata
- [ ] If input is a URL, content was successfully fetched before conversion
- [ ] If input is password-protected, user was prompted for password
- [ ] Downstream skill chain is specified (where to send extracted text next)
- [ ] Document type (syllabus, PYQ, notes, reference) is identified for downstream routing

If any check fails, either retry with a different method (e.g., pdftotext -layout → OCR → manual
entry) or report the limitation to the user with suggested fixes.
