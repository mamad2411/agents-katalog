---
name: document-design
description: Production-grade editorial document styling, publication design, 60-30-10 color harmony, Edward Tufte table rules, typographic measure, modern Web-to-PDF Playwright pipeline, and Word/PowerPoint recipes.
category: "08 - Productivity & Office Documents"
tags:
  - agent-skill
  - documents
  - typography
  - publication
  - stage-8
aliases:
  - document-design
  - publication-design
  - editorial-design
  - tufte-tables
---

# Document Design: Editorial Styling & Publication Engineering

Use this skill when designing, authoring, or styling formal reports, whitepapers, executive briefs, legal contracts, publication-ready PDFs, Word (`docx`) documents, and presentation decks (`powerpoint`). This skill elevates ordinary technical deliverables into timeless, publication-grade editorial documents inspired by classic Swiss typography and Edward Tufte's information design principles.

---

## The 60-30-10 Document Color Harmony

Most digital documents suffer from blinding pure white canvases (`#FFFFFF`) and harsh pure black ink (`#000000`), causing eye fatigue and looking like raw unstyled drafts. Master publication design follows the **60-30-10 harmony**:

```
┌─────────────────────────────────────────────────────────────┐
│ 60% Canvas Ground: Warm Ivory / Parchment (#FAF9F6)         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 30% Structural Ink: Deep Charcoal (#141413 / #1A1C1E) │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ 10% Intentional Accent: Terracotta (#C96442)    │  │  │
│  │  │ (Focal Anchors, Rule Lines, Key Metrics)        │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Color Specification Breakdown

1. **60% Canvas / Background — Warm Ivory / Parchment (`#FAF9F6` or `#F7F6F2`):**
   - Soft, glare-reducing, tactile paper warmth.
   - Provides organic depth without dulling readability.
2. **30% Structure & Typography — Deep Warm Charcoal (`#141413` or `#1A1C1E`):**
   - **Never use pure black (`#000000`) on white.**
   - Headings & Primary Ink: `#141413` (rich, warm black).
   - Secondary Text & Metadata: `#52524E` (neutral charcoal).
   - Hairline Rules & Dividers: `#E8E6DC` (subtle parchment border).
3. **10% Strategic Accent — Pick ONE purposeful hue per document:**
   - **Terracotta Warmth (`#C96442`):** Editorial, architectural, warm and authoritative.
   - **Scholarly Navy (`#1E3A8A` or `#1D2D44`):** Financial, institutional, analytical.
   - **Imperial Burgundy (`#722F37` or `#800020`):** Legal, formal, executive.

---

## Edward Tufte's Table Rules (Zero Chartjunk)

Tables are instruments for reasoning about numbers. Default spreadsheet grids surround numbers in dense cages of black gridlines that distract the human eye. Edward Tufte’s table doctrine mandates:

1. **Zero Vertical Lines:**
   - **Completely eliminate all vertical column borders.** White space alone must separate columns.
2. **Three Horizontal Hairlines Only (`#E8E6DC` or 0.5pt):**
   - Top Table Rule (above header).
   - Under-Header Rule (separating column labels from data).
   - Bottom Table Rule (anchoring the bottom of the table).
   - *Optional:* Extremely subtle hairlines for total/summary rows only.
3. **Right-Aligned Tabular Numbers:**
   - Numeric columns must always be **right-aligned**.
   - Use monospace numbers or CSS `font-variant-numeric: tabular-nums` to ensure decimals line up in a vertical column for effortless scanning.
4. **Header-Data Alignment Parity:**
   - Column headers must match the alignment of the data beneath them:
 - Left-aligned text Left-aligned header.
 - Right-aligned numbers Right-aligned header.
 - Centered icons/status Centered header.
5. **Units in Header, Not Cells:**
   - State currency and units in the header once (e.g., `Revenue ($M)` or `Latency (ms)`), leaving cells clean (e.g., `12.4`, `18.1` instead of `$12.4M`, `$18.1M`).

```html
<!-- Tufte Editorial Table Blueprint -->
<table class="tufte-table">
  <thead>
    <tr>
      <th class="text-left">Initiative</th>
      <th class="text-left">Lead Author</th>
      <th class="text-right">Allocation ($K)</th>
      <th class="text-right">ROI (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="text-left">Design System Overhaul</td>
      <td class="text-left">Sarah Chen</td>
      <td class="text-right tabular-nums">420.0</td>
      <td class="text-right tabular-nums">+142.5</td>
    </tr>
    <tr>
      <td class="text-left">Web-to-PDF Engine</td>
      <td class="text-left">Marcus Vance</td>
      <td class="text-right tabular-nums">180.0</td>
      <td class="text-right tabular-nums">+88.0</td>
    </tr>
  </tbody>
</table>

<style>
.tufte-table {
  width: 100%;
  border-collapse: collapse;
  font-family: inherit;
  border-top: 1px solid #E8E6DC;
  border-bottom: 1px solid #E8E6DC;
}
.tufte-table th {
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 8px 12px;
  border-bottom: 1px solid #E8E6DC;
  color: #141413;
}
.tufte-table td {
  padding: 10px 12px;
  border: none;
  color: #2A2A28;
}
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
```

---

## Editorial Typographic Scale & Measure

Reading comfort depends on the harmonious interaction of typeface, optical size, leading (line height), and measure (line length).

### 1. Typographic Hierarchy
- **Headings & Titles:** Editorial Serif (`Georgia`, `Cambria`, `Charter`, or `Source Serif Pro`) with **font weight 500 (Medium)**. Never use heavy bold 800+ for editorial serif headings; let size provide the hierarchy.
- **Body Text:** Clean, legible sans-serif (`system-ui`, `SF Pro`, `Inter`, `Helvetica Neue`) at `10.5pt`–`11.5pt` (`15px`–`17px`).
- **Code & Metadata:** Muted Monospace (`JetBrains Mono`, `SF Mono`, `Fira Code`) at `0.88em`.

### 2. The Measure Rule (55–75 Characters)
- **Line Length (Measure):** The optimal reading measure is **55 to 75 characters per line** (including spaces).
  - In CSS: `max-width: 65ch` or `max-width: 38rem` (~600px).
  - Too long (>85 chars): The reader's eye loses tracking when returning to the left edge.
  - Too short (<45 chars): The rhythm breaks with frequent hyphenation or awkward line breaks.
- **Line Height (Leading):**
  - Body Text: `1.45` to `1.6` for effortless line transitions.
  - Headings: `1.15` to `1.25` to keep multi-line titles tightly bound.

---

## Modern Web-to-PDF Pipeline (Playwright & CSS Paged Media)

Legacy PDF generators (`wkhtmltopdf`, basic headless scripts) produce ugly breaks and distorted margins. The modern publication standard writes documents in **HTML5 + Tailwind CSS** with **CSS Paged Media**, compiled via **Playwright**.

### 1. CSS Paged Media Standard Stylesheet

```css
@page {
  size: A4 portrait;
  margin: 20mm;
  @top-right {
    content: "Confidential & Proprietary";
    font-family: sans-serif;
    font-size: 8pt;
    color: #888884;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: sans-serif;
    font-size: 8pt;
    color: #888884;
  }
}

@media print {
  html, body {
    background-color: #FAF9F6 !important;
    color: #141413 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  /* Page break controls */
  .page-break {
    page-break-after: always;
    break-after: page;
  }

  .avoid-break {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  h1, h2, h3 {
    break-after: avoid;
    page-break-after: avoid;
  }

  table, figure, .callout-box {
    break-inside: avoid;
    page-break-inside: avoid;
  }
}
```

### 2. Playwright Automated Rendering Commands

```bash
# Direct CLI rendering via Playwright
npx playwright pdf document.html document.pdf \
  --paper-format A4 \
  --margin-top 20mm \
  --margin-bottom 20mm \
  --margin-left 20mm \
  --margin-right 20mm \
  --print-background
```

```python
# Programmatic Python Playwright generation
from playwright.sync_api import sync_playwright

def render_publication_pdf(html_file: str, output_pdf: str) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_file}")
        page.emulate_media(media="print")
        page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
            display_header_footer=False
        )
        browser.close()
```

---

## Word (`docx`) Production Recipes

When generating native Microsoft Word documents, adhere to these styling rules in both `docx-js` (Node/TypeScript) and `python-docx` (Python):

### 1. Typography & Spacing Rules
- **Line Spacing:** `276` dxa (approx. `1.15`x) in docx-js / `line_spacing = 1.15` in python-docx.
- **Paragraph Spacing:** `after: 120` dxa (6pt), `before: 0`.
- **Heading Spacing:** `before: 280` dxa (14pt), `after: 80` dxa (4pt).
- **Hairline Borders:** `0.5pt` (`#E8E6DC`) top and bottom; zero vertical borders.
- **Cell Shading:** Warm tint background fill (`#FAF6F0`).

### 2. `docx-js` Recipe (Node / TypeScript)
```typescript
import { Table, TableRow, TableCell, BorderStyle, WidthType, ShadingType } from "docx";

const tufteTable = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: {
    top: { style: BorderStyle.SINGLE, size: 4, color: "E8E6DC" },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: "E8E6DC" },
    left: { style: BorderStyle.NONE },
    right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.NONE },
    insideVertical: { style: BorderStyle.NONE },
  },
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "E8E6DC" } },
          shading: { fill: "FAF6F0", type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 160, right: 160 },
          children: [/* Header text */],
        }),
      ],
    }),
  ],
});
```

### 3. `python-docx` Recipe (Python)
```python
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_editorial_document(filename: str):
    doc = docx.Document()
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # A4
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.787)  # 20mm
    section.bottom_margin = Inches(0.787)
    section.left_margin = Inches(0.787)
    section.right_margin = Inches(0.787)

    # Document body style: Georgia, 10.5pt, 1.15 line spacing, 6pt after
    style = doc.styles["Normal"]
    style.font.name = "Georgia"
    style.font.size = Pt(10.5)
    style.font.color.rgb = RGBColor(0x14, 0x14, 0x13)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

    # Tufte Table with 3 horizontal hairlines (#E8E6DC)
    table = doc.add_table(rows=3, cols=3)
    table.autofit = False

    # Apply 3 horizontal hairlines via XML
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # Under-header rule & warm shading on header row
    for cell in table.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        under_header = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(under_header)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FAF6F0"/>')
        tcPr.append(shd)

    doc.save(filename)
```

---

## Presentation Decks (`powerpoint`)

For widescreen slide decks that command attention without looking like corporate bullet lists:

1. **Aspect Ratio:** Strictly **16:9 Widescreen** (13.333" × 7.5").
2. **Headlines:** Minimum **28pt–36pt** with high contrast; summarize the core conclusion in the title.
3. **Card-Based Stat Callouts:**
   - **Metric Figure:** 40pt–56pt bold in Accent Terracotta (`#C96442`).
   - **Unit / Label:** 12pt uppercase tracked subtitle in Muted Charcoal (`#52524E`).
4. **Negative Space:** Reserve at least 35% of the slide area as empty canvas to ensure the focal point stands out effortlessly.

### `python-pptx` Recipe (Editorial Slide Layout)
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

slide = prs.slides.add_slide(prs.slide_layouts[6])

# Headline: 32pt bold charcoal
title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.2))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Q3 Infrastructure Velocity Increased by 142%"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = RGBColor(0x14, 0x14, 0x13)

# Card-based Stat Box: 52pt Terracotta metric + 11pt tracking label
stat_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(3.5), Inches(2.0))
stf = stat_box.text_frame
p1 = stf.paragraphs[0]
p1.text = "142.5%"
p1.font.size = Pt(52)
p1.font.bold = True
p1.font.color.rgb = RGBColor(0xC9, 0x64, 0x42)  # Terracotta accent

p2 = stf.add_paragraph()
p2.text = "NET EFFICIENCY ROI GAIN"
p2.font.size = Pt(11)
p2.font.bold = True
p2.font.color.rgb = RGBColor(0x52, 0x52, 0x4E)  # Muted charcoal
```

---

## Callout Boxes (Architectural Accents)

Important takeaways, warnings, and executive notes should use restrained architectural callout boxes:

- **Left Border:** `3pt` (or `border-l-4`) solid Terracotta (`#C96442`).
- **Background Fill:** 4% warm tint (`#FAF6F0` or `rgba(201, 100, 66, 0.04)`).
- **Internal Padding:** `12pt`–`16pt` (`p-4` or `p-5`).
- **Corner Radius:** Square (`0px`) or subtle (`rounded-r-md`).
- **Micro-Heading:** Small uppercase bold label in accent color (`font-bold text-xs uppercase tracking-wider text-[#C96442]`).

### HTML / Tailwind Callout Component
```html
<div class="callout-box" style="border-left: 4px solid #C96442; background: #FAF6F0; padding: 14px 18px; border-radius: 0 6px 6px 0; margin: 20px 0;">
  <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #C96442; margin-bottom: 6px;">
    Executive Finding
  </div>
  <p style="margin: 0; font-size: 14px; line-height: 1.55; color: #141413;">
    All migration targets achieved zero table locks and sub-10ms query execution across 42 million production records.
  </p>
</div>
```

### `python-docx` Callout Box Function
```python
def add_callout_box(doc, title: str, text: str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)

    # 3pt (sz=24) Left Border in Terracotta, none for others
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="C96442"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    # Shading: 4% warm tint #FAF6F0
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FAF6F0"/>')
    tcPr.append(shd)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(title.upper() + "\n")
    run_t.font.bold = True
    run_t.font.size = Pt(9)
    run_t.font.color.rgb = RGBColor(0xC9, 0x64, 0x42)

    run_b = p.add_run(text)
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(0x14, 0x14, 0x13)
```

---

## 🔗 Connected Skills
- [[Skills/docx/SKILL|docx]] — สร้างและจัดการเอกสาร Word (.docx) ตามข้อกำหนดสไตล์
- [[Skills/pdf/SKILL|pdf]] — จัดการ ตัด รวม และตรวจสอบไฟล์ PDF
- [[Skills/powerpoint/SKILL|powerpoint]] — ออกแบบและสร้างสไลด์นำเสนอ PowerPoint 16:9
- [[Skills/xlsx/SKILL|xlsx]] — จัดรูปแบบตารางคำนวณและข้อมูลตัวเลขก่อนนำเสนอ
- [[Skills/ocr-and-documents/SKILL|ocr-and-documents]] — สกัดข้อมูลจากเอกสารเดิมมาจัดรูปแบบใหม่
- [[Skills/claude-design/SKILL|claude-design]] — เชื่อมต่อการออกแบบ UI และ Digital Artifacts สู่เอกสารจริง
- [[Skills/playwright-cli/SKILL|playwright-cli]] — เรนเดอร์ HTML สู่ PDF ระดับสิ่งพิมพ์ผ่าน CLI
- [[Skills/verification-before-completion/SKILL|verification-before-completion]] — ตรวจสอบความถูกต้องและสัดส่วนก่อนส่งมอบ

<!-- v1.1.0 synchronized: 2026-09-29 -->
