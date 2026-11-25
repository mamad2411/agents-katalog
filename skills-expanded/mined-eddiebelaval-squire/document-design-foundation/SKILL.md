---
name: Document Design Foundation
slug: document-design-foundation
description: Shared design system, CSS standards, and operational workflow for all document generation skills
category: document-creation
complexity: intermediate
version: "2.0.0"
author: "ID8Labs"
triggers:
  - "create document"
  - "generate document"
  - "make a document"
tags:
  - documents
  - design-system
  - foundation
  - css
  - styling
---

# Document Design Foundation


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

This is the shared design system for all document generation in Claude Code. Every document skill (PDF, Report, Word, Presentation, Spreadsheet) references this foundation for consistent, professional output.

## The Golden Rule

**When the user asks you to create a document, YOU create it. Do not write a program that creates it.**

- Generate a beautifully styled HTML file directly using the Write tool
- Save it to the project directory or `~/Development/artifacts/` if no project context
- Open it in the browser if the user wants to preview
- Convert to PDF via puppeteer only if the user specifically needs a .pdf file
- Convert to .docx only if the user specifically needs a Word file

## Operational Workflow

```
User says "create a report" or "make a PDF" or "generate a document"
                    |
                    v
    1. Determine document type and content
    2. Choose the right template (see Document Types below)
    3. Write a single, self-contained HTML file using the design system below
    4. Save to appropriate location
    5. If user needs .pdf: convert via puppeteer script
    6. If user needs .docx: generate via docx library
    7. Tell the user where the file is
```

## Design System

### Color Palette

```
Primary:        #1a1a2e     (deep navy - headings, primary text)
Secondary:      #16213e     (dark blue - subheadings)
Accent:         #0f3460     (medium blue - links, highlights)
Accent Light:   #e8f0fe     (pale blue - backgrounds, cards)
Success:        #0d7c3d     (green - positive metrics)
Warning:        #b45309     (amber - caution)
Danger:         #b91c1c     (red - negative metrics, alerts)
Neutral 50:     #fafafa     (near white - page background)
Neutral 100:    #f5f5f5     (light gray - card backgrounds)
Neutral 200:    #e5e5e5     (border gray)
Neutral 400:    #a3a3a3     (muted text)
Neutral 600:    #525252     (body text)
Neutral 800:    #262626     (strong text)
Neutral 900:    #171717     (headings)
```

### Typography

```css
/* Font stack - no external dependencies */
--font-heading: 'Georgia', 'Times New Roman', serif;
--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
--font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;

/* Scale */
--text-xs: 0.75rem;      /* 12px - captions, footnotes */
--text-sm: 0.875rem;     /* 14px - secondary text */
--text-base: 1rem;       /* 16px - body */
--text-lg: 1.125rem;     /* 18px - lead paragraphs */
--text-xl: 1.25rem;      /* 20px - section heads */
--text-2xl: 1.5rem;      /* 24px - major sections */
--text-3xl: 1.875rem;    /* 30px - page titles */
--text-4xl: 2.25rem;     /* 36px - cover titles */

/* Line height */
--leading-tight: 1.25;
--leading-normal: 1.6;
--leading-relaxed: 1.75;
```

### Base HTML Template

Every document starts with this skeleton. Copy and customize.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{DOCUMENT_TITLE}}</title>
  <style>
    /* ========== RESET ========== */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* ========== BASE ========== */
    html {
      font-size: 16px;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      color: #525252;
      line-height: 1.6;
      background: #fafafa;
    }

    /* ========== DOCUMENT CONTAINER ========== */
    .document {
      max-width: 820px;
      margin: 0 auto;
      background: #ffffff;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    .document-body {
      padding: 3rem 3.5rem;
    }

    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4 {
      font-family: Georgia, 'Times New Roman', serif;
      color: #1a1a2e;
      line-height: 1.25;
    }

    h1 {
      font-size: 2.25rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }

    h2 {
      font-size: 1.5rem;
      font-weight: 600;
      margin-top: 2.5rem;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid #e5e5e5;
    }

    h3 {
      font-size: 1.125rem;
      font-weight: 600;
      margin-top: 1.75rem;
      margin-bottom: 0.75rem;
      color: #16213e;
    }

    p {
      margin-bottom: 1rem;
      color: #525252;
    }

    .lead {
      font-size: 1.125rem;
      color: #525252;
      line-height: 1.75;
      margin-bottom: 1.5rem;
    }

    .subtitle {
      font-size: 1rem;
      color: #a3a3a3;
      font-weight: 400;
      margin-bottom: 2rem;
    }

    .muted { color: #a3a3a3; }
    .small { font-size: 0.875rem; }
    strong { color: #262626; }

    /* ========== COVER / HEADER ========== */
    .cover {
      padding: 4rem 3.5rem 3rem;
      border-bottom: 3px solid #1a1a2e;
    }

    .cover h1 {
      font-size: 2.5rem;
      margin-bottom: 0.25rem;
    }

    .cover .subtitle {
      font-size: 1.125rem;
      margin-bottom: 0;
    }

    .meta-row {
      display: flex;
      gap: 2rem;
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid #e5e5e5;
      font-size: 0.875rem;
      color: #a3a3a3;
    }

    .meta-row span { display: inline-flex; align-items: center; gap: 0.35rem; }

    /* ========== KPI / METRIC CARDS ========== */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin: 1.5rem 0 2rem;
    }

    .kpi-card {
      padding: 1.25rem;
      border-radius: 8px;
      background: #f5f5f5;
      border: 1px solid #e5e5e5;
    }

    .kpi-card .label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #a3a3a3;
      margin-bottom: 0.35rem;
    }

    .kpi-card .value {
      font-size: 1.75rem;
      font-weight: 700;
      color: #1a1a2e;
      font-family: Georgia, serif;
    }

    .kpi-card .change {
      font-size: 0.8rem;
      margin-top: 0.25rem;
    }

    .kpi-card .change.up { color: #0d7c3d; }
    .kpi-card .change.down { color: #b91c1c; }
    .kpi-card .change.neutral { color: #a3a3a3; }

    /* ========== TABLES ========== */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-size: 0.9rem;
    }

    thead th {
      text-align: left;
      padding: 0.75rem 1rem;
      background: #1a1a2e;
      color: #ffffff;
      font-weight: 600;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    thead th:first-child { border-radius: 6px 0 0 0; }
    thead th:last-child { border-radius: 0 6px 0 0; }

    tbody td {
      padding: 0.65rem 1rem;
      border-bottom: 1px solid #e5e5e5;
      color: #525252;
    }

    tbody tr:hover { background: #fafafa; }
    tbody tr:nth-child(even) { background: #fafafa; }
    tbody tr:nth-child(even):hover { background: #f0f0f0; }

    /* ========== CALLOUT / HIGHLIGHT BOXES ========== */
    .callout {
      padding: 1.25rem 1.5rem;
      border-radius: 8px;
      margin: 1.5rem 0;
      border-left: 4px solid;
    }

    .callout.info    { background: #e8f0fe; border-color: #0f3460; }
    .callout.success { background: #ecfdf5; border-color: #0d7c3d; }
    .callout.warning { background: #fffbeb; border-color: #b45309; }
    .callout.danger  { background: #fef2f2; border-color: #b91c1c; }

    .callout .callout-title {
      font-weight: 700;
      font-size: 0.875rem;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      margin-bottom: 0.35rem;
    }

    .callout.info .callout-title    { color: #0f3460; }
    .callout.success .callout-title { color: #0d7c3d; }
    .callout.warning .callout-title { color: #b45309; }
    .callout.danger .callout-title  { color: #b91c1c; }

    /* ========== LISTS ========== */
    ul, ol {
      margin: 1rem 0 1.5rem 1.5rem;
      line-height: 1.8;
    }

    li { margin-bottom: 0.35rem; }
    li::marker { color: #a3a3a3; }

    /* ========== SECTION DIVIDER ========== */
    hr {
      border: none;
      border-top: 2px solid #e5e5e5;
      margin: 2.5rem 0;
    }

    /* ========== FOOTER ========== */
    .document-footer {
      padding: 1.5rem 3.5rem;
      border-top: 1px solid #e5e5e5;
      font-size: 0.8rem;
      color: #a3a3a3;
      display: flex;
      justify-content: space-between;
    }

    /* ========== STATUS BADGES ========== */
    .badge {
      display: inline-block;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .badge.green  { background: #ecfdf5; color: #0d7c3d; }
    .badge.yellow { background: #fffbeb; color: #b45309; }
    .badge.red    { background: #fef2f2; color: #b91c1c; }
    .badge.blue   { background: #e8f0fe; color: #0f3460; }
    .badge.gray   { background: #f5f5f5; color: #525252; }

    /* ========== PROGRESS BAR ========== */
    .progress-bar {
      width: 100%;
      height: 8px;
      background: #e5e5e5;
      border-radius: 4px;
      overflow: hidden;
    }

    .progress-bar .fill {
      height: 100%;
      border-radius: 4px;
      background: #0f3460;
      transition: width 0.3s;
    }

    /* ========== TWO-COLUMN LAYOUT ========== */
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      margin: 1.5rem 0;
    }

    /* ========== PRINT STYLES ========== */
    @media print {
      body { background: white; }
      .document { box-shadow: none; max-width: none; }
      .document-body { padding: 2cm 2.5cm; }
      .cover { padding: 3cm 2.5cm 2cm; }
      h2 { page-break-after: avoid; }
      table, .kpi-grid { page-break-inside: avoid; }
      .callout { page-break-inside: avoid; }
      .document-footer { position: fixed; bottom: 0; width: 100%; }
      @page { margin: 0; size: A4; }
    }
  </style>
</head>
<body>
  <div class="document">

    <!-- COVER -->
    <div class="cover">
      <h1>{{TITLE}}</h1>
      <p class="subtitle">{{SUBTITLE}}</p>
      <div class="meta-row">
        <span>Prepared by {{AUTHOR}}</span>
        <span>{{DATE}}</span>
        <span>{{LABEL}}</span>
      </div>
    </div>

    <!-- BODY -->
    <div class="document-body">
      {{CONTENT}}
    </div>

    <!-- FOOTER -->
    <div class="document-footer">
      <span>{{ORGANIZATION}} &middot; Confidential</span>
      <span>{{DATE}}</span>
    </div>

  </div>
</body>
</html>
```

## Document Types and When to Use Each

| User Request | Output Format | Template Focus |
|---|---|---|
| "create a report" | HTML file | Cover + KPI cards + sections + tables |
| "make a PDF" | HTML file (print to PDF) | Same as report, with print styles |
| "write a proposal" | HTML file | Cover + executive summary + sections + callouts |
| "generate an invoice" | HTML file | Header + line items table + totals |
| "create a one-pager" | HTML file | Compact layout, KPI grid, key points |
| "make a dashboard" | HTML file | KPI grid + charts + status badges |
| "write documentation" | Markdown file | Standard markdown (no HTML needed) |
| "create a Word doc" | .docx via docx library | Use Word Document Creator skill |
| "make a spreadsheet" | .xlsx via exceljs | Use Spreadsheet Builder skill |
| "create a presentation" | .pptx via pptxgenjs | Use Presentation Maker skill |

## Content Quality Standards

### Structure
- **Every document needs a clear hierarchy:** Title > Subtitle > Section heads > Body
- **Lead with the conclusion.** Executive summary or BLUF (Bottom Line Up Front) first, supporting detail after.
- **Use data over prose.** KPI cards, tables, and charts communicate faster than paragraphs.
- **End with action.** Recommendations, next steps, or a clear call to action.

### Writing
- **Be specific.** "Revenue increased 23% MoM" not "Revenue showed strong growth."
- **Use active voice.** "The team shipped 4 features" not "4 features were shipped."
- **Keep paragraphs short.** 2-4 sentences max. White space is a feature.
- **Numbers get formatted.** Currency: $1,234.56. Percentages: 23.4%. Dates: April 15, 2026.

### Visual
- **Do not overcrowd.** One idea per section. Generous margins and spacing.
- **Tables over bullet lists** when data has 2+ dimensions.
- **Use callout boxes sparingly.** One per major section at most.
- **Status badges** for at-a-glance state (On Track, At Risk, Blocked).

## PDF Conversion (When Needed)

If the user specifically needs a .pdf file, convert the HTML:

```javascript
const puppeteer = require('puppeteer');

async function htmlToPdf(htmlPath, pdfPath) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' }
  });
  await browser.close();
}
```

Run this as a one-shot script, not a project scaffold:

```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto('file://INPUT_PATH', { waitUntil: 'networkidle0' });
  await page.pdf({ path: 'OUTPUT_PATH', format: 'A4', printBackground: true, margin: { top: '0', right: '0', bottom: '0', left: '0' } });
  await browser.close();
  console.log('PDF saved.');
})();
"
```

## Component Library

These are copy-paste patterns for common elements. Use them inside the base template.

### KPI Card
```html
<div class="kpi-card">
  <div class="label">Total Revenue</div>
  <div class="value">$142,500</div>
  <div class="change up">+12.3% vs last month</div>
</div>
```

### Callout Box
```html
<div class="callout info">
  <div class="callout-title">Key Finding</div>
  <p>Customer retention improved 8% after implementing the new onboarding flow.</p>
</div>
```

### Status Badge
```html
<span class="badge green">On Track</span>
<span class="badge yellow">At Risk</span>
<span class="badge red">Blocked</span>
<span class="badge blue">In Review</span>
```

### Progress Bar
```html
<div class="progress-bar">
  <div class="fill" style="width: 72%"></div>
</div>
```

### Data Table
```html
<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Current</th>
      <th>Previous</th>
      <th>Change</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Revenue</td>
      <td>$142,500</td>
      <td>$126,900</td>
      <td><span class="badge green">+12.3%</span></td>
    </tr>
  </tbody>
</table>
```

## File Naming and Location

- **Project context exists:** Save to project root or `docs/` or `reports/` directory
- **No project context:** Save to `~/Development/artifacts/{project-or-topic}/`
- **Filename pattern:** `{type}-{subject}-{date}.html` (e.g., `report-q1-revenue-2026-04-15.html`)
- **PDF companion:** Same name with `.pdf` extension alongside the `.html`
