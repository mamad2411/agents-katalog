---
name: editorial-layout-design
description: "Lay out multi-page documents: grid systems, masters and styles, flowing long copy, tables, footnotes and accessible PDF output."
type: procedural
category: design
domain: design
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - layout a report
  - indesign master pages
  - grid system for magazine
  - flow long text document
  - accessible pdf report
aliases:
  - page-layout
keywords:
  - layout
  - grid
  - editorial
  - magazine
  - masters
  - inDesign
  - scribus
source: custom
enabled: true
---

# Editorial Layout Design

## Purpose

Lay out multi-page documents: grid systems, masters and styles, flowing long copy, tables, footnotes and accessible PDF output.

## When to Use

- A report, book or magazine must be laid out with consistent rhythm across pages.
- Copy will change repeatedly and must reflow without manual fixing.
- The PDF must be accessible and screen-reader friendly.

## When NOT to Use

- The document is a slide deck or dashboard widget.
- A single-page poster with no repeating structure.
- The content is still being written — structure first, layout second.

## Capabilities

- Define a modular grid and map it to master pages.
- Use paragraph and character styles so content drives appearance.
- Handle widows, orphans, hyphenation and footnote placement.
- Export tagged, accessible PDFs with correct reading order.

## Inputs

- Manuscript with heading hierarchy and figure captions.
- Page size, margins, column count and the intended reading distance.
- Print or screen target, plus any accessibility requirement (PDF/UA).

## Workflow

1. Fix the grid: margins, columns, gutters and baseline grid.
2. Create master pages for body, chapter opener and figure page.
3. Map every manuscript element to a named style; nothing gets local formatting.
4. Flow the copy and resolve widows, orphans and awkward breaks manually only at the end.
5. Place figures at final size with captions tied to their anchors.
6. Tag the export, check reading order, then preflight.

## Tools

- indesign
- scribus
- latex
- pandoc
- weasyprint

## Examples

- `A 12-column grid with a 6-column body block gives flexible figure widths without breaking rhythm.`
- `PDF/UA tagging plus alt text on every figure is the difference between a compliant and a decorative report.`

## Safety

- Keep style definitions in the template, not the document, so a second issue reuses them.
- Do not stretch images to fill a frame; crop or re-render them.

## Source

All-Skills canonical library (`skills/design/editorial-layout-design`). First-party skill, maintained in this repository.

## Notes

- Test with the longest heading and the longest word in the manuscript.
- A baseline grid catches misaligned body text before print.
- Pairs with: `typography-and-type-systems`, `print-production-prepress`.
