---
name: pdf
description: Use this skill for any work on .pdf files — extract text/tables, OCR scanned PDFs, merge/split/rotate, fill forms, redact sensitive content, encrypt/decrypt, watermark, extract images, manipulate pages. Trigger on any mention of a .pdf filename, "this PDF", "the PDF", or requests to produce, read, modify, secure, or sanitize a PDF. Use for compliance evidence packs (SOC 2, CAIQ, SIG, DPA addenda), redacting customer names/PII before external sharing, OCR on scanned regulatory filings (PR DACO, OCIF, bilingual ES/EN docs), and assembling/splitting PDFs in audit and incident-response chains. ALWAYS use this skill when redaction is requested — visual covering is a security incident; this skill enforces TRUE redaction.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Skill

## Scope and Sibling Boundaries

Use this skill for the **mechanics of .pdf files**. Defer or coordinate when the deliverable shifts:

| If the user wants... | Use |
|---|---|
| .pdf output / read / modify | **this skill** |
| Convert PDF → .docx (Word output) | `docx` (Word is the deliverable) |
| Convert .docx → PDF | **this skill** (PDF is the deliverable) |
| Slides (.pptx output) | `pptx` |
| HTML web presentation | `anthropic-skills:ckmslides` |
| Legal content review of a PDF (find missing clauses, GDPR/HIPAA gaps) | `legal:legal-audit` for content; **this skill** for the file mechanics (extract, redact, re-assemble) |
| Procedure documentation in PDF form | `operations:runbook` for content; **this skill** to render |

When a request mixes content judgment + file mechanics (e.g., "audit this privacy policy PDF and ship a redacted version"), run `legal:legal-audit` for the analysis and use **this skill** for the extraction, redaction, and re-export.

---

## Quick Reference

| Task | Tool | Notes |
|---|---|---|
| Read text | `pdfplumber` / `pdftotext -layout` | Layout flag preserves columns |
| Extract tables | `pdfplumber` → `pandas` | Empty-row guard required |
| OCR scanned PDF | `pdf2image` + `pytesseract` | Use `lang='spa+eng'` for PR bilingual |
| Merge / split / rotate | `pypdf` or `qpdf` | qpdf faster on large files |
| Fill form | see `FORMS.md` | Use AcroForm field updates, not flatten-then-overlay |
| **Redact (TRUE)** | `pymupdf` (`fitz`) `add_redact_annot` + `apply_redactions` | See **Redaction** section — mandatory |
| Encrypt / decrypt | `pypdf` writer.encrypt / `qpdf --decrypt` | AES-256 default |
| Watermark | `pypdf` `merge_page` | Visual only — NOT redaction |
| Extract images | `pdfimages -j` | Poppler |
| Create from scratch | `reportlab` | Use `<sub>`/`<super>` tags, never Unicode subscripts |
| Convert .docx → PDF | `soffice --headless --convert-to pdf` | LibreOffice |

---

## Redaction (HIGH-STAKES — read before any redaction task)

**Visual covering is a security incident.** Drawing a black rectangle over text with `pypdf.merge_page`, ReportLab, or any annotation tool that does not REMOVE the underlying text stream produces a file where the original text is recoverable by:

- Selecting and copying with any PDF reader
- `pdftotext` extraction
- Searching the file
- Copy/paste into a terminal

For a cybersec founder shipping SOC 2 evidence, customer references, incident reports, or DPA addenda, this is a breach. Treat every "redact", "black out", "scrub", "remove", "anonymize", or "sanitize" request as **TRUE redaction required**.

### TRUE Redaction with PyMuPDF (canonical)

```python
import fitz  # pip install pymupdf

doc = fitz.open("incident_report.pdf")

PATTERNS = ["AcmeCorp", "john.doe@acme.com", "192.168.1.42"]

for page in doc:
    for pat in PATTERNS:
        for rect in page.search_for(pat):
            # add_redact_annot marks the area; fill paints the box
            page.add_redact_annot(rect, fill=(0, 0, 0))
    # apply_redactions REMOVES the underlying text/images
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

doc.save("incident_report.redacted.pdf", garbage=4, deflate=True, clean=True)
doc.close()
```

`garbage=4` + `clean=True` rewrites the object stream so nothing orphaned remains. Always use these flags on redacted output.

### Regex / PII redaction

```python
import re, fitz
PII = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),                 # SSN
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),  # email
    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),           # IPv4
]
doc = fitz.open(src)
for page in doc:
    text = page.get_text("text")
    for rx in PII:
        for m in rx.finditer(text):
            for rect in page.search_for(m.group(0)):
                page.add_redact_annot(rect, fill=(0,0,0))
    page.apply_redactions()
doc.save(dst, garbage=4, deflate=True, clean=True)
```

### Mandatory verification step

After redaction, re-extract and grep. If any pattern survives, the redaction failed:

```bash
pdftotext -layout output.redacted.pdf - | grep -iE "acmecorp|john\.doe|192\.168" && echo "LEAK" || echo "clean"
```

For high-sensitivity outputs (incident reports, customer logos, signed contracts), also strip metadata:

```python
doc.set_metadata({})  # before save
```

And flatten any form fields that could carry residual data:

```python
# pdftk input.pdf flatten output flat.pdf   # if pdftk available
```

### What NOT to do

- Do NOT use `page.merge_page(black_box.pdf)` for redaction — text under the box is recoverable.
- Do NOT use ReportLab `c.rect(...)` overlays for redaction — same problem.
- Do NOT use `pypdf` alone for redaction — pypdf has no text-removal primitive.
- Do NOT rely on watermarks, white text, or low-opacity layers — all recoverable.

---

## Reading and Extraction

### Text (layout-aware)

```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

CLI alternative:
```bash
pdftotext -layout input.pdf -
```

### Tables → DataFrame → Excel

```python
import pdfplumber, pandas as pd
frames = []
with pdfplumber.open("caiq.pdf") as pdf:
    for page in pdf.pages:
        for tbl in page.extract_tables() or []:
            if tbl and len(tbl) > 1:
                frames.append(pd.DataFrame(tbl[1:], columns=tbl[0]))
if frames:
    pd.concat(frames, ignore_index=True).to_excel("caiq.xlsx", index=False)
```

If output target is a Word doc, hand off to `docx`. If output is a spreadsheet, hand off to `xlsx`.

### OCR (scanned PDFs, including bilingual ES/EN)

Common in PR for DACO filings, OCIF submissions, court records, scanned contracts.

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path("daco_filing_scanned.pdf", dpi=300)
text = ""
for i, img in enumerate(images, 1):
    # 'spa+eng' handles bilingual Spanish/English documents
    text += f"\n--- Page {i} ---\n"
    text += pytesseract.image_to_string(img, lang="spa+eng")
```

System deps: `tesseract`, `tesseract-data-spa`, `tesseract-data-eng`, `poppler`. For pure English, use `lang="eng"`. For Spanish-only, `lang="spa"`.

### Make a scanned PDF searchable (OCR overlay)

```bash
ocrmypdf -l spa+eng --skip-text input_scanned.pdf output_searchable.pdf
```

Preserves original images and adds a text layer underneath. Use `--redo-ocr` to overwrite an existing bad text layer.

---

## Merge, Split, Rotate, Reorder

### pypdf
```python
from pypdf import PdfReader, PdfWriter
w = PdfWriter()
for f in ["dpa.pdf", "msa.pdf", "sow.pdf"]:
    for p in PdfReader(f).pages:
        w.add_page(p)
with open("evidence_pack.pdf", "wb") as out:
    w.write(out)
```

### qpdf (faster on large files, exact page ranges)
```bash
qpdf --empty --pages dpa.pdf 1-z msa.pdf 1-z sow.pdf 1-z -- evidence_pack.pdf
qpdf input.pdf --pages . 1-5 -- first_five.pdf
qpdf input.pdf output.pdf --rotate=+90:1-z      # rotate all pages 90 CW
```

---

## Forms (compliance use)

For DPA addenda, security questionnaires, CAIQ/SIG, vendor onboarding forms, see `FORMS.md`. Default approach: detect AcroForm fields with `pypdf.PdfReader.get_fields()`, fill via `update_page_form_field_values`, save without flattening unless the recipient requires non-editable output. If the PDF is image-only (scanned, no AcroForm), OCR first then overlay text via `reportlab` at located coordinates — then flatten.

If the form is a Word document being sent as PDF, use `docx` to fill, then convert with `soffice --headless --convert-to pdf`.

---

## Encryption / Decryption

```python
from pypdf import PdfReader, PdfWriter
r = PdfReader("plain.pdf"); w = PdfWriter()
for p in r.pages: w.add_page(p)
w.encrypt(user_password="user", owner_password="owner", algorithm="AES-256")
with open("encrypted.pdf","wb") as f: w.write(f)
```

Decrypt:
```bash
qpdf --password=PASS --decrypt encrypted.pdf decrypted.pdf
```

For SOC 2 evidence shared externally, prefer transport-layer protection (signed URL, secure portal) over PDF passwords — PDF AES is only as strong as the password and gets brute-forced offline.

---

## Watermark (visual only — NOT redaction)

```python
from pypdf import PdfReader, PdfWriter
wm = PdfReader("CONFIDENTIAL.pdf").pages[0]
r = PdfReader("doc.pdf"); w = PdfWriter()
for p in r.pages:
    p.merge_page(wm); w.add_page(p)
with open("watermarked.pdf","wb") as f: w.write(f)
```

Use for "CONFIDENTIAL", "DRAFT", "DO NOT DISTRIBUTE" overlays. Never use for hiding content.

---

## Create PDF from scratch (reportlab)

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()
story = [Paragraph("Incident Report", styles["Title"]), Spacer(1,12),
         Paragraph("CO<sub>2</sub> impact: x<super>2</super>", styles["Normal"])]
SimpleDocTemplate("out.pdf", pagesize=letter).build(story)
```

**Never** use Unicode subscript/superscript chars (₀₁₂, ⁰¹²) — built-in fonts render them as black boxes. Use `<sub>` / `<super>` tags inside `Paragraph`.

---

## Image extraction

```bash
pdfimages -j input.pdf img_   # JPEGs as img_-000.jpg, img_-001.jpg, ...
pdfimages -all input.pdf img_ # original formats
```

---

## Workflow chains (offload patterns)

- **PDF → Word edit cycle**: extract with `pdfplumber`/OCR → hand off to `docx` for the editable Word deliverable.
- **PDF → Slides**: extract → hand off to `pptx` for .pptx deliverable, or `anthropic-skills:ckmslides` for HTML.
- **Legal page audit**: run `legal:legal-audit` on extracted text → use this skill to redact and re-emit the cleaned PDF.
- **Compliance evidence pack**: assemble policies + screenshots + signed contracts via merge → redact customer names → encrypt → ship.
- **Incident report sanitization**: OCR if scanned → TRUE redact PII/IPs/customer identifiers → strip metadata → verify with `pdftotext | grep` → hand off.
- **Runbook PDFs**: build the runbook content via `operations:runbook` → render the deliverable via this skill (reportlab or .docx → PDF).

---

## Pre-ship checklist (any externally shared PDF)

- [ ] Redactions applied via `apply_redactions`, not visual covering
- [ ] `pdftotext output.pdf | grep -iE "<patterns>"` returns nothing
- [ ] Metadata cleared (`set_metadata({})`) if author/title leak matters
- [ ] Form fields flattened if recipient must not edit
- [ ] OCR text layer present if document was scanned (so recipient can search/cite)
- [ ] If encrypted: password sent out-of-band, AES-256, not RC4

---

## Dependencies

```
pip install pypdf pdfplumber pymupdf reportlab pytesseract pdf2image ocrmypdf pandas openpyxl
# system: tesseract tesseract-data-spa tesseract-data-eng poppler qpdf libreoffice
```
