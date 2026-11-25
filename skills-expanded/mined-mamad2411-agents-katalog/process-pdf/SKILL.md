---
name: process-pdf
description: Handles full PDF lifecycle — extracts text/tables, merges/splits, rotates, watermarks, fills forms, encrypts/decrypts, and OCRs scanned pages.
when_to_use: When the user needs to work with a PDF file: pull out text or tables, fill a PDF form, merge or split pages, add a watermark, rotate/encrypt, or OCR a scanned document into searchable text.
---

## When to Use

Reach for this skill when the task touches a `.pdf` and falls into one of five families. Classify first — the family decides the library, not the other way around:

| Family | Trigger phrases | Primary lib |
|---|---|---|
| **extract-text** | "pull text", "get the content", "read the PDF" | `pdfplumber` (layout) / `pypdf` (fast plain) |
| **extract-table** | "get the table", "rows/columns", "to CSV/DataFrame" | `camelot` (ruled) / `pdfplumber` (no rules) |
| **form-fill** | "fill this form", "set field X", "AcroForm" | `pypdf` AcroForm |
| **merge-split / transform** | "combine", "split pages 3-7", "rotate", "watermark", "encrypt/decrypt" | `pypdf` |
| **OCR** | "scanned", "image-only", "make it searchable", text layer empty | `ocrmypdf` (wraps tesseract) |

If the request mixes families (e.g. "OCR then extract the tables"), run OCR first to produce a text layer, then re-classify the output as a normal PDF.

## Steps

1. **Probe the source before doing anything.** Open it and check three things: is it encrypted, how many pages, and does a text layer exist.
   ```python
   from pypdf import PdfReader
   r = PdfReader("in.pdf")
   print("encrypted:", r.is_encrypted, "pages:", len(r.pages))
   sample = (r.pages[0].extract_text() or "").strip()
   print("has_text_layer:", bool(sample))
   ```
   - `is_encrypted` True and you have the password → `r.decrypt(pw)`. No password → stop and ask; do not guess.
   - `has_text_layer` False on a content page → this is a **scanned PDF**. Jump to step 6 (OCR) before extraction.

2. **extract-text path.** For reading order / clean prose use `pdfplumber`; it respects layout and gives word coordinates.
   ```python
   import pdfplumber
   with pdfplumber.open("in.pdf") as pdf:
       text = "\n".join(p.extract_text() or "" for p in pdf.pages)
   ```
   Need bounding boxes (redaction, positional logic) → use `page.extract_words()` / `page.chars` for `x0,x1,top,bottom`. Use `pypdf`'s `extract_text()` only when you need speed and don't care about column order — it interleaves multi-column layouts.

3. **extract-table path.** Branch on whether the table has visible borders:
   - **Ruled lines present** → `camelot` lattice (needs Ghostscript installed):
     ```python
     import camelot
     tables = camelot.read_pdf("in.pdf", pages="1-end", flavor="lattice")
     tables[0].df.to_csv("out.csv", index=False)
     print(tables[0].parsing_report)   # check 'accuracy' and 'whitespace'
     ```
   - **No borders (whitespace-aligned)** → `camelot` flavor `"stream"`, or `pdfplumber`'s `page.extract_tables()` with explicit `table_settings={"vertical_strategy":"text","horizontal_strategy":"text"}`.
   - Always validate `tables[0].parsing_report["accuracy"]`; below ~80 means the flavor is wrong — switch lattice↔stream before trusting the rows.

4. **form-fill path.** First **dump the real field names** — they are rarely what the user assumes, and a typo silently writes nothing.
   ```python
   from pypdf import PdfReader, PdfWriter
   fields = PdfReader("form.pdf").get_fields()
   print({k: f.get("/FT") for k, f in fields.items()})  # /Tx text, /Btn checkbox, /Ch choice
   ```
   Then write, preserving the appearance stream so values render:
   ```python
   w = PdfWriter(clone_from="form.pdf")
   for page in w.pages:
       w.update_page_form_field_values(page, {"full_name": "ACME", "agree": "/Yes"},
                                       auto_regenerate=False)
   with open("filled.pdf", "wb") as fh: w.write(fh)
   ```
   - Checkboxes/radios take the **export value** (often `/Yes`, `/On`, or a custom string), not `True`. Read it from the field's `/_States_` (via `fields[name]`) if unsure.
   - "Flatten" / "make it non-editable" requested → set `NameObject("/Ff")` or use a flatten pass; after flattening, fields are baked in and `get_fields()` returns nothing — that's expected.

5. **merge-split / transform path** (all `pypdf`, page indices are **0-based**):
   - Merge: `PdfWriter()` + `w.append("a.pdf"); w.append("b.pdf")`.
   - Split pages 3–7 (human 1-based) → indices `2..6`: `for i in range(2,7): w.add_page(reader.pages[i])`.
   - Rotate: `page.rotate(90)` (clockwise, multiples of 90).
   - Watermark/stamp: render the watermark to its own one-page PDF (`reportlab`), then `content_page.merge_page(watermark_page)` over each page.
   - Encrypt: `w.encrypt("userpw", algorithm="AES-256")`. Decrypt: `reader.decrypt(pw)` then re-write the pages out.

6. **OCR path (scanned / empty text layer).** Don't hand-roll tesseract page-by-page — `ocrmypdf` adds an invisible text layer while keeping the original image, which is what "searchable PDF" means.
   ```bash
   ocrmypdf -l eng --rotate-pages --deskew --optimize 1 in.pdf out_ocr.pdf
   ```
   - `--force-ocr` when there's a partial/garbage text layer you want to replace; `--redo-ocr` to re-OCR cleanly; `--skip-text` to OCR only the image-only pages.
   - Multi-language → `-l eng+tha` (the matching tesseract language packs must be installed).
   - After it finishes, feed `out_ocr.pdf` back into step 2/3 for actual extraction.

7. **Always verify** (next section) before declaring done.

## Common Errors

- **`PdfReadError` / garbage output on an encrypted file.** Source is encrypted — `reader.is_encrypted` is True. `decrypt(pw)` first. An empty-string password is common for "owner-locked, no open password" files: try `reader.decrypt("")`.
- **`extract_text()` returns `""` or only whitespace.** No text layer = scanned/image PDF. This is not a bug to work around with regex; route to OCR (step 6). Extracting harder will not conjure text that isn't there.
- **Form fill "succeeds" but the PDF shows blanks.** Either (a) field name typo — you wrote to a key that doesn't exist (dump names in step 4), or (b) the viewer didn't regenerate appearances. Set `auto_regenerate=False` and write via `clone_from`/`PdfWriter`, not by mutating the reader.
- **Checkbox stays unchecked despite setting it `True`.** Checkboxes need the export value (`"/Yes"` etc.), not a boolean. Pull the valid state from the field.
- **Camelot finds zero tables or shredded rows.** Wrong `flavor`. `lattice` needs visible ruling lines; `stream` is for whitespace-separated tables. Also: `lattice` requires **Ghostscript** on the system — a missing-Ghostscript failure looks like "no tables found", not an import error.
- **Merged/rotated output drops form fields or annotations.** Plain page-copy loses interactive objects. Use `PdfWriter.append()` (carries annotations) and `clone_from` to preserve AcroForm structure.
- **Off-by-one page ranges.** User says "pages 3–7" (1-based, inclusive); `pypdf`/`pdfplumber` are 0-based. Map to indices `2..6`, i.e. `range(2, 7)`.
- **OCR raises `PriorOcrFoundError`.** A text layer already exists. Use `--force-ocr`, `--redo-ocr`, or `--skip-text` per the intent in step 6.

## Verify

Never trust the write — re-open the output and assert against the goal:

- **Any transform (merge/split/rotate):** re-open output, assert `len(PdfReader("out.pdf").pages)` equals the expected page count; spot-check `page.rotation` after a rotate.
- **Text extraction:** confirm non-empty output and that a known anchor string from the document is present; flag if length is suspiciously short for the page count (likely a missed OCR case).
- **Table extraction:** check `parsing_report["accuracy"] >= 80`, and that column count and a known header row match the source; eyeball the first and last data row.
- **Form fill:** re-read with `get_fields()` and assert each target field's `/V` equals the value you set (and the right export value for checkboxes). If you flattened, instead confirm the rendered values are visible in a render.
- **Encrypt:** re-open and assert `is_encrypted` is True and the correct password decrypts; **decrypt:** assert `is_encrypted` is False on output.
- **OCR:** re-run the step-1 probe on the output — `has_text_layer` must now be True and `extract_text()` must return real words from a previously-image page.
