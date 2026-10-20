---
name: python-document-pipeline
description: Use when generating PDFs, DOCX, XLSX, or processing documents/images in Python — reportlab, docxtpl, openpyxl, pikepdf, Gotenberg.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [python-essentials, python-django, python-data-pipeline, infra-docker-compose, security]
---

# Python Document Pipeline

**Iron Law: pick the tool for the output, not the language affinity. Don't render HTML-shaped reports with reportlab; don't manipulate PDFs by re-rendering them; don't process 100 MB TIFFs with Pillow.**

**Versions:** reportlab `4.x` · docxtpl `0.19` · docxcompose `1.4` · openpyxl `3.1` · pikepdf `9.x` · pyvips `2.2` · Pillow `11.x` · Gotenberg `8.x` — _Gotenberg 8 ships Chromium 130+ and LibreOffice 24; pyvips needs libvips ≥ 8.15 on the host. pikepdf wraps qpdf 11+ — apt install qpdf in the base image._

## Decision table

| Output                                                                          | Best tool                                                         | When                                                                        |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **PDF (HTML-shaped)** — invoices, reports with CSS, charts via JS               | **Gotenberg 8** (HTTP service, headless Chromium)                 | Anything that already has an HTML template                                  |
| **PDF (code-generated)** — pixel-perfect layouts, tables, vector charts         | **reportlab**                                                     | Old-school layouts, no HTML source, programmatic page math                  |
| **PDF (manipulate existing)** — merge, split, watermark, encrypt, extract pages | **pikepdf**                                                       | Post-processing PDFs from any source                                        |
| **PDF (extract text)**                                                          | **pypdf** (simple) or **pdfplumber** (tables)                     | OCR needs Tesseract — out of scope here                                     |
| **DOCX (templated + merge)** — fill Word templates, combine N outputs           | **docxtpl** + **docxcompose**                                     | Designer-authored templates filled in code, then composed into one document |
| **XLSX (write)**                                                                | **openpyxl** (small/medium) or **xlsxwriter** (streaming, faster) | Multi-sheet reports with formatting                                         |
| **XLSX (read)**                                                                 | **openpyxl** with `read_only=True, data_only=True`                | Stream rows for large workbooks                                             |
| **Image (large, fast)** — multi-megapixel TIFFs, scientific imagery             | **pyvips**                                                        | 10× faster than Pillow on big images, streaming, low memory                 |
| **Image (general)** — thumbnails, format conversion, drawing                    | **Pillow**                                                        | Anything under ~20 MB and not in a tight loop                               |

## Gotenberg 8 — the right tool for HTML-templated PDFs

reportlab on a designer's HTML report is the most common time-waste here. Run Gotenberg as a sidecar, POST the HTML, get a real PDF rendered by Chromium with full CSS/JS.

```yaml
# docker-compose.yml — Gotenberg sidecar. Internal network only, SSRF-narrowed.
services:
  gotenberg:
    image: gotenberg/gotenberg:8.16.0 # pin minor.patch
    restart: unless-stopped
    networks: [internal]
    expose: ["3000"] # NO `ports:` — never publish to host/public
    command:
      [
        "gotenberg",
        "--api-timeout=120s",
        "--chromium-disable-javascript=false",
        "--chromium-allow-list=^https?://(myapp|internal\\.example\\.com).*",
        "--chromium-deny-list=^file://|^https?://(169\\.254\\.169\\.254|metadata\\.google\\.internal|metadata\\.azure\\.com|\\[?fd00:ec2::254\\]?)",
      ]
networks: { internal: { driver: bridge, internal: true } }
```

See `Skill(infra-gotenberg)` for the full hardening reference (auth front-door, sizing, healthcheck).

```python
# Render a Django template to PDF via Gotenberg
import httpx
from django.template.loader import render_to_string

def render_pdf(template: str, ctx: dict, *, timeout: float = 60.0) -> bytes:
    html = render_to_string(template, ctx)
    files = {"files": ("index.html", html.encode("utf-8"), "text/html")}
    data = {"paperWidth": "8.27", "paperHeight": "11.69",       # A4 inches
            "marginTop": "0.4", "marginBottom": "0.4",
            "printBackground": "true", "preferCssPageSize": "true"}  # honor @page in CSS
    with httpx.Client(timeout=timeout) as client:
        r = client.post("http://gotenberg:3000/forms/chromium/convert/html", files=files, data=data)
        r.raise_for_status()
        return r.content
```

Endpoints: `/forms/chromium/convert/{html,url,markdown}`, `/forms/libreoffice/convert` (DOCX/XLSX→PDF), `/forms/pdfengines/merge`. **Never expose Gotenberg publicly** — headless browser with arbitrary-URL fetch = SSRF. See `Skill(security)`.

## reportlab — code-generated PDFs

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_report(path: str, rows: list[tuple]) -> None:
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    flow = [Paragraph("Order summary", styles["Title"])]
    table = Table([["SKU", "Qty", "Total"], *rows], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    flow.append(table)
    doc.build(flow)
```

Use **platypus** (high-level flowables), not the low-level canvas, unless you need pixel positioning. `repeatRows=1` repeats table headers across pages.

## docxtpl + docxcompose — templated DOCX flow

```python
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docxcompose.composer import Composer
from docx import Document

# 1. Fill each section template
sections = []
for ch in chapters:
    tpl = DocxTemplate("templates/chapter.docx")
    tpl.render({"title": ch.title, "rows": ch.rows, "image": InlineImage(tpl, ch.image_path, width=Mm(100))})
    out = io.BytesIO(); tpl.save(out); out.seek(0)
    sections.append(Document(out))

# 2. Compose into one document
master = Document("templates/cover.docx")
composer = Composer(master)
for section in sections:
    composer.append(section)
composer.save("report.docx")
```

**Templates use Jinja syntax** (`{{ var }}`, `{% for %}`) inside Word — designers edit them in Word itself. Images go through `InlineImage` or `tpl.new_subdoc()` for richer-content placeholders. **Style preservation is fragile** — docxcompose copies styles by name; if two source docs define the same style differently, the first wins. **The injection risk is the template file, not the context.** Context values render as strings, not as Jinja sources. The real risk: an attacker-uploaded `.docx` template whose Word XML contains `{% for x in cycler %}…` or `{{ config.items() }}` — that runs at `tpl.render()` time. Mitigations: (1) never accept user-uploaded `.docx` as templates; (2) if you must, parse the XML and reject if any text node contains `{{`/`{%` before passing to `DocxTemplate`; (3) `SandboxedEnvironment` limits attribute access but doesn't block Jinja globals like `lipsum`/`cycler` — it's defense-in-depth, not the primary control.

## openpyxl — XLSX

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb = Workbook(); ws = wb.active; ws.title = "Orders"
ws.append(["SKU", "Qty", "Total"])
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="DDDDDD")
ws.append(["A-1", 3, 99.0])
ws.column_dimensions["A"].width = 14
ws.freeze_panes = "A2"
wb.save("orders.xlsx")
```

Streaming writes for 100k+ rows: `Workbook(write_only=True)` + `WriteOnlyCell`, or `xlsxwriter` with `constant_memory=True` — default openpyxl holds the whole sheet in RAM.

## pikepdf — manipulate existing PDFs

```python
import pikepdf

# Merge
with pikepdf.Pdf.new() as out:
    for path in ["a.pdf", "b.pdf"]:
        with pikepdf.open(path) as src:
            out.pages.extend(src.pages)
    out.save("merged.pdf")

# Watermark every page
with pikepdf.open("in.pdf", allow_overwriting_input=True) as pdf, \
     pikepdf.open("watermark.pdf") as wm:
    stamp = wm.pages[0]
    for page in pdf.pages:
        page.add_overlay(stamp)
    pdf.save("out.pdf")
```

pikepdf wraps qpdf — fast, preserves forms/metadata/signatures. **Never use PyPDF2** (abandoned); use `pypdf` for extraction, pikepdf for manipulation.

## pyvips vs Pillow — image size matters

| Op                  | Pillow            | pyvips             | Verdict         |
| ------------------- | ----------------- | ------------------ | --------------- |
| Thumbnail 5 MB JPEG | 200 ms, 80 MB RAM | 80 ms, 12 MB       | pyvips          |
| Resize 200 MB TIFF  | OOM / 2+ GB       | 600 ms, ~50 MB     | **pyvips only** |
| Draw shapes/text    | trivial           | painful (pipeline) | Pillow          |
| Bulk format convert | linear blocking   | streaming threaded | pyvips          |

```python
import pyvips
img = pyvips.Image.new_from_file("scan.tif", access="sequential")  # streaming
img = img.thumbnail_image(1600)                                    # fits within 1600px
img.write_to_file("thumb.jpg[Q=85,strip]")
```

`access="sequential"` processes one band at a time without materializing — use for any TIFF/PSD over 50 MB. **Image-bomb defense**: untrusted uploads can claim 50,000×50,000 in headers — check `img.width * img.height` before non-streaming ops and reject above a pixel budget. Set `VIPS_BLOCK_UNTRUSTED=1` for user-supplied images.

## Anti-patterns

- HTML reports with reportlab (use Gotenberg); re-rendering a PDF for a watermark (pikepdf overlay)
- Pillow on 100 MB+ images (use pyvips `access="sequential"`); PyPDF2 in new code (use pypdf/pikepdf)
- `wkhtmltopdf` for new projects (dead WebKit, broken CSS3 — use Gotenberg)
- openpyxl default mode for 1M-row exports (RAM blows up — write-only or xlsxwriter); PDF concat by raw bytes (corrupts xref — use pikepdf)
- docxtpl accepting attacker-uploaded `.docx` templates — Jinja in Word XML executes at render time; reject any template whose text nodes contain `{{`/`{%`. For HTML payloads inside trusted templates use `RichText`/`Subdoc`
- Gotenberg exposed publicly — SSRF via `/forms/chromium/convert/url`

## Red flags

| Thought                                    | Reality                                                                   |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| "Hand-render this CSS report in reportlab" | One sprint becomes three — Gotenberg                                      |
| "Pillow is fine for these scans"           | Until the 400 MP drone TIFF                                               |
| "Merge PDFs with pypdf"                    | pikepdf preserves forms/sigs, corrupts less                               |
| "Gotenberg behind nginx is enough"         | If `/forms/chromium/convert/url` is reachable it's an SSRF — lock it down |

## Hand-off

Django integration: `Skill(devkit:python-django)`. Gotenberg sidecar: `Skill(devkit:infra-docker-compose)`. SSRF/upload/signed-URL lockdown: `Skill(devkit:security)`. Data shaping for templates: `Skill(devkit:python-data-pipeline)`.
