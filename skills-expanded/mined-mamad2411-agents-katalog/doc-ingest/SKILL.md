---
name: doc-ingest
description: "Read existing documents (PDF, Word, PowerPoint, Excel, HTML) and convert them into clean Markdown/plain text the agent can reason over: extract text, ingest a file, summarize a document. Use whenever the user wants to READ, extract, ingest, transcribe, or summarize the contents of an existing file (not create one)."
license: MIT (Code Buddy original skill)
nativeEngine:
  triggers:
    - extract text
    - convert to markdown
    - to markdown
    - markdown
    - ingest
    - read this file
    - read document
    - summarize
    - résume
    - résumé
    - extrais
    - transcribe
    - ocr
---

# Ingest existing documents into Markdown / text

Turn a document the user already has (PDF, Word, PowerPoint, Excel, HTML) into
clean Markdown or plain text so you can quote, summarize, or transform it. This
is the **read** counterpart to the create skills (`xlsx`/`docx`/`pptx`/`pdf`).

Work **one visible step at a time** and verify before reporting.

## Two backends — prefer the lean one
- **Lean (always available, no extra install):** the bundled libraries
  `pypdf`, `python-docx`, `python-pptx`, `openpyxl` read the common Office/PDF
  formats with `python3 -c "import pypdf, docx, pptx, openpyxl"`. Use this path
  by default.
- **Rich (optional, `prepare:python:extras`):** `markitdown` adds HTML, images
  (OCR), EPUB, ZIP and more, and emits tidy Markdown directly. Only reach for it
  when the lean path can't read the format.

## Workflow (one step at a time)
1. **Identify** the file and its type (extension).
2. **Extract**: run a short Python script (heredoc via the `bash` tool) that
   reads the file with the matching library and prints — or writes — Markdown/text.
3. **Verify**: assert the output is non-empty (e.g. `assert len(text) > 0`) and
   print a length + first lines so the extraction is visibly correct.
4. **Report**: the extracted text (or the saved `.md` path) and a one-line summary.

## Lean extraction (covers PDF / Word / PowerPoint / Excel)
```bash
python3 - "$FILE" <<'PY'
import sys, os
src = sys.argv[1]
ext = os.path.splitext(src)[1].lower()

def pdf(p):
    from pypdf import PdfReader
    return "\n\n".join((pg.extract_text() or "") for pg in PdfReader(p).pages)

def docx(p):
    import docx
    d = docx.Document(p)
    return "\n".join(par.text for par in d.paragraphs)

def pptx(p):
    from pptx import Presentation
    out = []
    for i, sl in enumerate(Presentation(p).slides, 1):
        out.append(f"## Slide {i}")
        for sh in sl.shapes:
            if sh.has_text_frame:
                out.append(sh.text_frame.text)
    return "\n".join(out)

def xlsx(p):
    from openpyxl import load_workbook
    wb = load_workbook(p, data_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(f"## {ws.title}")
        for row in ws.iter_rows(values_only=True):
            out.append(" | ".join("" if c is None else str(c) for c in row))
    return "\n".join(out)

handlers = {".pdf": pdf, ".docx": docx, ".pptx": pptx, ".xlsx": xlsx}
fn = handlers.get(ext)
if not fn:
    sys.exit(f"Lean path can't read {ext}; enable the rich backend (prepare:python:extras) for markitdown.")
text = fn(src)
assert text and text.strip(), "extraction produced no text"
print(f"[{len(text)} chars]")
print("\n".join(text.splitlines()[:40]))
PY
```

## Rich backend (markitdown — optional)
```bash
python3 - <<'PY'
try:
    from markitdown import MarkItDown
except ModuleNotFoundError:
    raise SystemExit(
        "markitdown not installed. Run `npm run prepare:python:extras` in cowork/ "
        "to add the optional ingestion backend (HTML, images/OCR, EPUB, ...)."
    )
md = MarkItDown()
res = md.convert("INPUT_PATH")
assert res.text_content, "markitdown produced no content"
print(res.text_content[:4000])
PY
```

## Notes
- Never invent content — only report what the extractor returned.
- For large files, summarize after extraction rather than dumping everything.
- To then *produce* a new document from what you read, hand off to the
  `xlsx`/`docx`/`pptx`/`pdf` create skills.
