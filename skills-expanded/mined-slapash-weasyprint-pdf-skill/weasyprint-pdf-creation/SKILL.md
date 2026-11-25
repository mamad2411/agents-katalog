---
name: weasyprint-pdf-creation
description: Use when creating designed PDFs from owned HTML/CSS templates with WeasyPrint. Covers invoice/report/proposal/brief/receipt/statement templates, render scripts, example galleries, font guidance, and QA checks for page size, warnings, overflow, extraction, and visual layout.
version: 1.0.0
author: Omar Benaidy + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pdf, weasyprint, html, css, invoices, reports, documents, artifacts]
    related_skills: [claude-design, nano-pdf]
---

# WeasyPrint PDF Creation

## Overview

Use this skill to create polished PDFs from source-controlled HTML/CSS templates. The core workflow is:

```text
HTML template + print CSS + data → WeasyPrint → PDF → QA → publish/share
```

This is for **new PDFs you own**: invoices, reports, proposals, briefs, statements, one-page docs, printable guides, and template-driven business documents.

Do **not** use this as the default for editing arbitrary existing PDFs or capturing JavaScript-heavy webpages. See the decision table below.

## When to Use

Use this skill when the user asks to:

- create an invoice, report, proposal, brief, contract-style doc, handout, or printable PDF
- make a reusable PDF template from HTML/CSS
- generate a better-looking PDF than a markdown/export default
- publish a PDF preview for review on an artifact shelf/static host
- test whether a designed document survives print/PDF rendering

Do not use this skill for:

- editing text in an existing PDF → use nano-pdf/PyMuPDF
- OCR/extracting text from scans → use OCR/document extraction tooling
- screenshots or JS-rendered dashboards → use Playwright/Chromium
- raw programmatic vector drawing → consider ReportLab/SVG/PyMuPDF

## Decision Table

| Need | Tool |
|---|---|
| New designed invoice/report/doc from template | WeasyPrint |
| Existing PDF text edit | nano-pdf / PyMuPDF |
| JS-heavy webpage or dashboard to PDF | Playwright/Chromium |
| Extract/OCR a PDF | OCR/document tools |
| Low-level PDF surgery/merge/split | pikepdf / PyMuPDF |

## Recommended Repo Shape

```text
pdf-project/
  templates/
    invoice.html
    report.html
    proposal.html
    one-page-brief.html
    receipt.html
    statement.html
  styles/
    print.css
  data/
    sample-invoice.json
    sample-report.json
    sample-proposal.json
  scripts/
    render_pdf.py
    qa_pdf.py
  outputs/
    .gitkeep
  examples/
    index.html
    invoice.pdf
    invoice.png
  docs/
    pdf-qa.md
    template-rules.md
  fonts/
    README.md
  requirements.txt
  README.md
```

Keep templates boring to run and tasteful to look at:

- semantic HTML
- print-first CSS
- no required JavaScript
- local assets/fonts where possible
- data injection separated from layout
- source-controlled sample JSON
- deterministic generated output

## Install

### Python venv

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m weasyprint --info
```

`requirements.txt` minimum:

```text
weasyprint==68.1
Jinja2>=3.1
pypdf>=5.0
```

### Debian/Ubuntu native dependencies

For most modern Debian/Ubuntu hosts:

```bash
sudo apt-get update
sudo apt-get install -y \
  python3-pip \
  libpango-1.0-0 \
  libpangoft2-1.0-0 \
  libharfbuzz-subset0 \
  fontconfig \
  fonts-dejavu-core
```

## Template Rules

### CSS

Use `@page` and print media deliberately:

```css
@page { size: A4; margin: 0; }
@media print {
  body { background: white; }
  .page { width: 210mm; height: 297mm; overflow: hidden; }
  .no-print { display: none; }
}
```

Prefer:

- `mm` for page canvas and key print spacing
- CSS grid/table for stable document layout
- `font-variant-numeric: tabular-nums` for money and IDs
- explicit column widths for invoice tables
- reserved space for stamps/badges/decorative elements
- wrapping rules for long strings like IBANs, emails, IDs

Avoid or verify carefully:

- absolute positioning near content
- unsupported browser-only CSS
- fancy effects like `box-shadow`, `filter`, `mix-blend-mode`
- JS-only chart/render flows
- content that fits only because sample text is short

### HTML

Use semantic blocks and stable classes:

```html
<section class="page invoice">
  <header class="invoice-header">...</header>
  <section class="invoice-meta">...</section>
  <table class="line-items">...</table>
  <section class="payment-box">...</section>
</section>
```

For long values:

```css
.long-value { overflow-wrap: anywhere; }
.amount { white-space: nowrap; text-align: right; }
```

## Render Script Pattern

Use a small Python script so rendering is repeatable and testable.

```python
from pathlib import Path
import argparse, json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

parser = argparse.ArgumentParser()
parser.add_argument('--template', required=True)
parser.add_argument('--data', required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args()

template_path = Path(args.template)
data = json.loads(Path(args.data).read_text())

env = Environment(
    loader=FileSystemLoader(str(template_path.parent)),
    autoescape=select_autoescape(['html', 'xml'])
)
html = env.get_template(template_path.name).render(**data)
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
HTML(string=html, base_url=str(template_path.parent.resolve())).write_pdf(args.out)
```

## QA Checklist

Run all of these before calling a PDF done.

### 1. WeasyPrint warning check

```bash
python scripts/render_pdf.py --template templates/invoice.html --data data/sample-invoice.json --out outputs/invoice.pdf 2> outputs/weasyprint.log
test ! -s outputs/weasyprint.log
```

Warnings often reveal unsupported CSS or broken assets. Fix them unless they are intentionally harmless and documented.

### 2. PDF metadata/page check

```bash
pdfinfo outputs/invoice.pdf | grep -E 'Pages|Page size|PDF version'
```

Expected A4:

```text
Page size: 595.276 x 841.89 pts (A4)
```

### 3. Text extraction smoke test

```bash
pdftotext outputs/invoice.pdf - | grep -E 'Invoice|Total|Payment'
```

This catches invisible text, missing content, and many accidental blank-page failures.

### 4. Browser preview

Open the HTML preview and check console errors. For artifact shelf/static hosting:

```bash
artifact add-dir my-pdf-lab ./public --title "PDF Lab" --type site --tag artifact
curl -fsSI https://artifacts.example.com/artifacts/my-pdf-lab/
```

### 5. Visual/overlap check

Inspect the rendered HTML/PDF visually. Focus on:

- totals and money columns
- payment boxes
- long IDs/IBAN/email fields
- stamps/badges
- footer spacing
- page breaks
- table rows at page boundaries

If the user reports overlap, do not hand-wave it. Re-check with browser/vision and redesign the cramped area.

## Publishing Pattern

For review, publish a static folder containing previews and PDFs:

```text
public/
  index.html
  invoice.html
  invoice.pdf
  report.html
  report.pdf
```

Then:

```bash
artifact add-dir pdf-lab public --title "PDF Lab" --type site --tag artifact
curl -fsSI https://artifacts.omarbenaidy.com/artifacts/pdf-lab/
```

If using a different environment, any static host works: GitHub Pages, Cloudflare Pages, Netlify, nginx, S3, etc.

## Font Guidance

Fonts affect pagination and overflow. For reproducible PDFs:

- define an explicit font stack
- bundle or install production fonts
- avoid relying on macOS-only fonts unless the renderer runs on macOS
- re-run QA after font changes
- keep `fonts/README.md` updated with chosen fonts and licenses

## Common Pitfalls

1. **Treating browser CSS support as WeasyPrint CSS support.** WeasyPrint is excellent for print CSS, but not a full Chrome clone. Generate once early and read warnings.

2. **Decorative absolute positioning over real content.** Stamps, blobs, and badges need reserved layout space. If they float over payment/totals/footer, they will overlap with real data.

3. **Long values in single-line fields.** IBANs, addresses, emails, and invoice references need `overflow-wrap:anywhere` or stacked layout.

4. **Accidental extra blank pages.** Fixed `min-height:297mm` plus padding/content can overflow. In print mode, use `height:297mm`, controlled padding, and inspect page count with `pdfinfo`.

5. **Unpinned renderer versions.** Rendering can change across WeasyPrint versions. Pin the version and re-check golden PDFs after upgrades.

6. **Unpinned fonts.** Missing or different fonts change layout. Install known fonts and avoid relying on system-specific typography.

7. **Screenshot-only QA.** Screenshots are secondary. Check logs, page count, extracted text, browser console, and actual PDF availability.

## Verification Checklist

- [ ] WeasyPrint version pinned
- [ ] Native dependencies/fonts installed and documented
- [ ] Render command is repeatable
- [ ] Render log has zero unexpected warnings
- [ ] `pdfinfo` page count/size is expected
- [ ] `pdftotext` finds key content
- [ ] Browser preview has no console errors
- [ ] Visual QA checks totals/payment/footer/page breaks
- [ ] Public/review links return 200 when publishing is requested
