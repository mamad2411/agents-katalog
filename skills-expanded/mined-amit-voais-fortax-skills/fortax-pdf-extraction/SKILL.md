---
name: fortax-pdf-extraction
description: Read documents and pull their figures into a checkable sheet - text and tables from PDFs (26AS, AIS, GST ledgers and challans, bank statements, notices, invoices, annual reports) with pdfplumber, OCR for scans, and a long-screenshot method for pages too tall for one image (a web page in any browser or screenshot tool, or a tall PDF / image file) that reads in overlapping slices and stitches on the overlap so no digit is lost. Also answers "what is this, what does it say" about an open page, file or pasted text strictly from its own words, with the dates, amounts and actions and where each is printed. Typical asks - "is PDF se table nikalo", "26AS ka data Excel me do", "ye notice kya keh raha hai", "ye kya hai samjhao", "isme kya likha hai", "screenshot se figures padho".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "pdfplumber techniques and examples adapted from claude-office-skills/skills, https://github.com/claude-office-skills/skills (MIT); overlapping long-screenshot capture and stitch-on-the-overlap technique adapted from agent-vision-toolkit, https://github.com/Anionex/agent-vision-toolkit (MIT)"
---

# Read a document and extract its figures

Three jobs, one discipline: **every figure you report comes from the document's own text or image,
with where it is printed, and you say how you read it.** Text beats pixels; a downloaded file beats a
screenshot; a rupee figure you are not sure of is a blocker, not a footnote.

1. **Read what is open** — the CA points at a page, file or pasted text and asks what it is or says.
2. **Extract from a PDF** — tables and figures into a sheet (pdfplumber; OCR for scans).
3. **Read a long page** — too tall for one screenshot; overlapping slices, stitched on the overlap.

## Part 1 — read what is open

"Ye kya hai", "samjhao", "isme kya likha hai", "what does this say", "is there anything I need to do".

### Step 1 — find the thing, then read it

| It is | Read it with |
|---|---|
| A page open in the browser | your browser tool's page-text / accessibility read (Claude in Chrome, a Playwright/browser MCP, the Codex browser). If you have none, ask the CA to save the page as PDF or paste the text |
| A file the CA named or dropped in the folder | read the file; for a PDF use Part 2 |
| A scan, a photo, or a PDF with no text layer | OCR (Part 2), or read the image in slices (Part 3) |
| Text pasted into the chat | the text itself |

If you cannot tell which one they mean, ask in one line: "The GST page that is open, or the PDF you added
for Sharma Traders?" Do not guess.

If the text cannot be read, say exactly that. **Never describe a document you have not read.**

### Step 2 — identify it from its own words

Say what the document is using what is printed on it: title, form number, issuing authority, reference
number, date. If none is present, say what it appears to be and why.

A notice headed "Form ASMT-10" is an ASMT-10. A page on `services.gst.gov.in` titled "Track Application
Status" is that page. Do not name a form, section, scheme or deadline that does not appear in the text.

### Step 3 — pull out what matters

```
What it is
<one line, from the document's own heading and issuer>

Who it concerns
<the client, GSTIN / PAN / CIN as printed, and the other party or authority>

What it asks for or decides
<plain language, two to four lines>

Dates
| What | Date | Where it says so |

Money
| What | Amount | Where it says so |

What the client has to do
- <each action, with its deadline if the document gives one>

Unclear or missing
- <anything illegible, cut off, or referred to but not attached>
```

"Where it says so" is a page and paragraph, a clause number, or a field label. Every date and every
amount has one.

### Step 4 — hand off if it needs more

- A contract or agreement that needs judging, not just reading: `fortax-contract-review`.
- A tax notice that needs a reply: `fortax-notice-reply`.
- A question about what the law says: `fortax-knowledge-base`.
- A deadline the CA wants tracked: offer it; do not add it to any calendar yourself.

### Rules

- **Only the text.** No figure, date or reference that is not in the document.
- **Quote, do not paraphrase, anything the client will act on:** a due date, an amount demanded, a
  reference number.
- **Say how you read it:** page text, file text, OCR or image. An image-read figure is marked
  `[read from scan — check]`.
- **Hinglish is fine** if the CA wrote in it. Quoted text stays in the document's language.

## Part 2 — extract from a PDF

`pip install pdfplumber` (and `pillow` for images). pdfplumber gives character-level positions, table
detection and visual debugging. Write the Python, run it, and write the output next to the PDF.

### First: does it have text?

```python
import pdfplumber
with pdfplumber.open("26AS_ABCDE1234F_2025-26.pdf") as pdf:
    print(len(pdf.pages), pdf.metadata)
    print(repr((pdf.pages[0].extract_text() or "")[:500]))
```

- Text comes back -> use the methods below.
- Empty or garbage -> it is a scan. OCR it: `ocrmypdf in.pdf out.pdf` (adds a text layer; needs
  Tesseract) then use pdfplumber on `out.pdf`; or `pytesseract` on page images. Or read the page images
  in slices (Part 3). OCR digits are marked `[OCR — check]` and every total is re-added.
- Password-protected (bank statements, 26AS/AIS downloads): ask the CA to open it and save an
  unprotected copy (Print -> Save as PDF). Never ask for, guess, type or store the password.
- A download in a better format exists (Excel of the bank statement, JSON/Excel of 2B, text/Excel of
  26AS/AIS): ask for that instead. A downloaded file beats any extraction.

### Structure

```
PDF document
  metadata (title, author, creation date)
  pages[]
    chars (each character with position, font, size)
    words, lines, rects, curves, images
  outline (bookmarks)
```

### Text

```python
with pdfplumber.open(path) as pdf:
    text = pdf.pages[0].extract_text()
    full = "".join((p.extract_text() or "") + "\n" for p in pdf.pages)

    page = pdf.pages[0]
    layout_text = page.extract_text(layout=True, x_tolerance=3, y_tolerance=3)   # keeps columns aligned
    words = page.extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False)
    for w in words:
        print(w["text"], w["x0"], w["top"])
    for c in page.chars[:20]:
        print(c["text"], c["x0"], c["top"], c["fontname"], c["size"])
```

### Tables

```python
with pdfplumber.open(path) as pdf:
    page = pdf.pages[0]
    for table in page.extract_tables():
        for row in table:
            print(row)

    settings = {
        "vertical_strategy": "lines",      # or "text" for tables without ruling lines
        "horizontal_strategy": "lines",
        "snap_tolerance": 3, "join_tolerance": 3, "edge_min_length": 3,
        "min_words_vertical": 3, "min_words_horizontal": 1,
        "intersection_tolerance": 3, "text_tolerance": 3,
    }
    tables = page.extract_tables(settings)

    for t in page.find_tables():           # locate without extracting
        print(t.bbox)                      # (x0, top, x1, bottom)
        data = t.extract()
```

Bank statements and 26AS usually have no vertical lines: try `"text"` strategies, or crop to the table
area and split columns by the x positions of the header words.

### Visual debugging

```python
im = page.to_image(resolution=150)
im.draw_rects(page.words)
im.save("debug_words.png")
im.reset()
im.debug_tablefinder()
im.save("debug_tables.png")
```

Look at the debug image before tuning settings.

### Crop, filter by position or font

```python
cropped = page.crop((0, 120, page.width, page.height - 60))   # (x0, top, x1, bottom): drop header/footer
text, tables = cropped.extract_text(), cropped.extract_tables()

def within(obj, bbox):
    x0, top, x1, bottom = bbox
    return obj["x0"] >= x0 and obj["x1"] <= x1 and obj["top"] >= top and obj["bottom"] <= bottom

bold = "".join(c["text"] for c in page.chars if "Bold" in c["fontname"])
large = [c for c in page.chars if c["size"] > 14]

half = page.width / 2                                  # two-column layout
left, right = page.crop((0, 0, half, page.height)), page.crop((half, 0, page.width, page.height))
```

### Clean Indian figures

```python
import re
def to_amount(s):
    """'1,23,456.78' -> 123456.78; '1,234.00 Dr' -> -1234.0; '(500.00)' -> -500.0; '' -> None"""
    if s is None:
        return None
    t = str(s).strip()
    neg = t.endswith(("Dr", "DR")) or (t.startswith("(") and t.endswith(")")) or t.startswith("-")
    t = re.sub(r"[^\d.]", "", t)
    if not t:
        return None
    v = float(t)
    return -v if neg else v

GSTIN = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b")
PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
DATE = re.compile(r"\b\d{2}[-/.](?:\d{2}|[A-Za-z]{3})[-/.]\d{2,4}\b")   # 31-03-2026, 31-Mar-2026
```

Whether Dr means negative depends on the document (a bank statement's Dr is a withdrawal); state the sign
convention in the output. Keep identifiers (GSTIN, PAN, TAN, challan and account numbers) as text.

### All tables to one checkable workbook

```python
import pdfplumber, pandas as pd

def pdf_tables_to_xlsx(pdf_path, xlsx_path):
    frames = []
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, 1):
            for tno, table in enumerate(page.extract_tables(), 1):
                if not table or len(table) < 2:
                    continue
                rows = [[(c or "").strip() for c in r] for r in table]
                df = pd.DataFrame(rows[1:], columns=rows[0])
                df["Source"] = f"{pdf_path} p{pno} t{tno}"
                frames.append(df)
    with pd.ExcelWriter(xlsx_path) as xw:
        for i, df in enumerate(frames, 1):
            df.to_excel(xw, sheet_name=f"Table_{i}", index=False)
    return frames
```

Headers repeated on every page: detect and drop them, then concatenate into one table.

### Invoice fields (a GST invoice)

```python
def extract_invoice(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
    out = {"gstins": GSTIN.findall(text), "invoice_no": None, "date": None, "total": None}
    m = re.search(r"Invoice\s*(?:No\.?|Number|#)\s*:?\s*([A-Za-z0-9/\-]+)", text, re.I)
    out["invoice_no"] = m.group(1) if m else None
    m = DATE.search(text)
    out["date"] = m.group(0) if m else None
    m = re.search(r"(?:Grand\s+)?Total\s*(?:Amount)?\s*:?\s*(?:Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)", text, re.I)
    out["total"] = to_amount(m.group(1)) if m else None
    return out
```

The first GSTIN is not always the supplier — check the label next to it. Recompute the invoice total from
the taxable value and tax lines; if it does not agree with the printed total, report both.

### Prove the extraction

- Re-add every column that has a printed total, with code; **if your total does not match the
  document's, you have misread something** — fix it before reporting, and never adopt the printed total
  over your rows.
- Row counts: pages x rows per page vs rows extracted.
- Bank statements: opening + credits - debits = closing, and the running balance on every row (or run
  the statement through `fortax-bank-statement-to-books`, which proves it).
- Spot-check three random rows against the page image.

### Limitations

- Scanned / image PDFs need OCR first; complex layouts need tuning per document; some encryption types
  are not supported; embedded fonts can garble text (check against the image); no PDF editing.

## Part 3 — read a long page without losing a figure

One screenshot of a tall page gets scaled down before it is read, and small digits are the first thing
to go. On a 26AS, a GST cash ledger, a bank statement or a multi-page notice, a lost digit is the whole job.

### Step 1 — text first, always

- **Web page:** read the page text with your browser tool first. If the figures are there, you are done.
- **Download:** if the page offers a PDF, Excel or JSON, have it downloaded into the client folder (the CA
  confirms the download) and read the file.
- **PDF already given:** Part 2.

Only when the content is drawn (a canvas chart, an image-only scan, a viewer that blocks selection) go
to pixels.

### Step 2a — capture a web page in overlapping screens (any screenshot tool)

1. Scroll to the top; take a screenshot.
2. Scroll down by about **80% of the viewport height**, so each screen shares a band with the previous.
   Use whatever your tool has: a scroll action with an amount, the Page Down key (check the overlap —
   some pages scroll a full screen), or run `window.scrollBy(0, Math.round(innerHeight * 0.8))`.
3. Screenshot again. Repeat until the page stops moving: the scroll position does not change, or
   `scrollY + innerHeight >= document.documentElement.scrollHeight`.
4. Tables inside their own scrolling panel: scroll that panel, not the window.
5. Zoom into a region (if your tool can) where digits are small, rather than shrinking the whole page.

If the tool has no scroll or screenshot, ask the CA to save the page as PDF ("Print -> Save as PDF")
and use Part 2 / Step 2b.

### Step 2b — a tall image or PDF file

Cut it into overlapping slices with the bundled script, then read each slice:

```bash
python3 scripts/slice_tall_image.py "<Client>/<FY>/ITR/26AS_ABCDE1234F.pdf" --dpi 200 --height 1400 --overlap 200
python3 scripts/slice_tall_image.py long_screenshot.png --out slices/
```

It writes `<stem>_p<page>_s<slice>.png` and prints each slice's pixel range. Raise `--dpi` for small
print; keep the overlap at least two table rows high.

Say how many screens or slices you took. If a page needs more than about twelve, it is too long to read
this way reliably — get a download, or tell the CA which section you covered.

### Step 3 — read each piece as its own document

One screen or slice at a time; write down what you found before moving on. Do not hold six images in
your head and summarise at the end. For each piece record: the section or period it covers, the rows
with their figures, and running totals if shown.

### Step 4 — stitch on the overlap, not on faith

- Join consecutive pieces by matching the rows that appear in both. That shared band is the proof the
  join is correct.
- A row that appears in two pieces is **one** row. Deduplicate on its identifiers (invoice number, challan
  number, date plus amount), never on position.
- If the overlap shows nothing in common, a screen is missing. Go back and capture it.
- Where the page prints a total, recompute it from your rows with code. If it does not match, you misread
  something. Do not report until it ties, and never quietly adopt the page's total.

### Step 5 — say how you read it

State: read from the page text, from a downloaded file, from OCR, or from N screenshots / slices. Where a
figure was unclear, mark it `[UNCLEAR — confirm on screen]` rather than guessing a digit.

### Scans and photographs

The same discipline applies to a long scanned document. Work page by page, not a summary of the whole
file. For a photograph of a document, check extracted fields against what else you have: name against
PAN, the PAN inside the GSTIN (characters 3-12) against the client's PAN, the period against the folder.

## Output

Into the client folder next to the source (e.g. `<Client>/<FY>/ITR/26AS_ABCDE1234F_2025-26_extract.xlsx`):

- The extracted table(s) with a `Source` column naming the page (and screen or slice) of every row.
- The totals recomputed by formula, beside the printed totals, with a check cell.
- A short note: how it was read, sign conventions, anything unclear.
- For screenshot or slice reads, the images alongside so the CA can check any row against what you saw.

## Credit

pdfplumber techniques adapted from claude-office-skills/skills (MIT). The overlapping-capture and
stitch-on-the-overlap method is adapted from the long-screenshot OCR method in
agent-vision-toolkit by Anionex (MIT); no code from that project is used. Notices are in the
`LICENSE-THIRD-PARTY-*.txt` files. Changed by Fortax: Indian documents and figure formats, proof checks,
tool-neutral capture, the slicing script, and the read-what-is-open method.
