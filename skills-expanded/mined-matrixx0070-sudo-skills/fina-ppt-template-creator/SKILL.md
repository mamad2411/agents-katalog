---
name: fina-ppt-template-creator
version: 1.0.0
description: Builds a reusable, on-brand PowerPoint master and layout set for finance decks, defining slide layouts, color palette, typography, placeholders, and standardized exhibit zones for tables and charts with accessible contrast.
author: matrixx0070
tags: [finance, powerpoint, template, slide-master, branding, typography, accessibility, exhibits]
capabilities: []
---

# Finance PowerPoint Template Creator

## When to use
Use this when you need a firm- or team-standard PowerPoint template: a slide master, layout set, color and type spec, and standard exhibit zones that every finance deck will inherit. This is the one-time (or periodic) infrastructure build that makes fina-pptx-author fast and fina-ib-check-deck's formatting checks trivially pass.

**Not for:** authoring deck content (use fina-pptx-author), refreshing an existing deck's data (use fina-deck-refresh), or proofing a finished deck (use fina-ib-check-deck). The template holds no analysis; numbers come from fina-comps-analysis, fina-dcf-model, and fina-3-statement-model at authoring time.

## Method
1. **Define the brand system.** You lock the primary, secondary, and accent colors with exact hex values, the typeface family with weights, and the logo lockups; everything downstream references these tokens, not ad-hoc values.
2. **Set the grid and safe zones.** You establish a column grid, margins, and the footer/footnote/source band so every layout aligns to the same skeleton. Decision point: if the deck will be printed and projected, you set the aspect ratio to 16:9 and confirm margins survive both; if it is board-book print only, you may set 4:3 — pick one and state it.
3. **Build the slide master.** You define master-level elements once — footer text field, page-number field, confidentiality legend, logo position, and default text styles — so they propagate to every layout.
4. **Create the layout inventory.** You build the standard layouts: title/cover, section divider, one-message content, exhibit (table), exhibit (chart), full-bleed chart, two-up comparison, and appendix.
5. **Place typed placeholders.** You add placeholders for action title, body, exhibit area, source line, and page number with correct text styles, so authors fill content without touching formatting.
6. **Design the exhibit zones.** You define a table zone (header row style, banding, number alignment, decimal conventions) and a chart zone (plot area, legend position, axis styles, data-label defaults) as reusable standards.
7. **Verify accessibility and contrast.** Decision point: if any text-on-fill pair fails a 4.5:1 contrast ratio (3:1 for large text), you adjust the palette or restrict that color to non-text use before shipping the template.
8. **Document and hand off.** You write the reuse rules — what is editable, what is locked, how to update the master — and hand the template to fina-pptx-author as the authoring base.

## Example
You build "Firm Finance Master 16:9." You lock navy `#0B2545` (primary), slate `#5C6B7A` (secondary), and gold `#C6A15B` (accent, non-text only — it fails 4.5:1 on white). Type is a single sans family: 28pt semibold for action titles, 12pt for body, 9pt for source lines, all left-aligned to a 12-column grid with a 0.4" footer band. You create nine layouts including an exhibit-table layout whose header row is navy-on-white 10pt bold with right-aligned numerals to one decimal for multiples, and an exhibit-chart layout with legend-right and horizontal gridlines only. You confirm navy-on-white measures 12.6:1 and slate-on-white 4.9:1 (both pass); gold is restricted to rules and accents. You document that titles and body are editable, master chrome is locked, and hand off to fina-pptx-author.

## Pitfalls
- **Hard-coded formatting.** Letting authors style text directly instead of via placeholders guarantees drift; put every style on the master and lock chrome.
- **Failing contrast.** Brand accent colors often fail text contrast; test every text-on-fill pair and restrict weak colors to rules and fills.
- **Missing footnote band.** A template with no dedicated source zone teaches authors to skip sourcing; bake a source line into every exhibit layout so fina-ib-check-deck passes.
- **Aspect-ratio afterthought.** Switching 4:3 to 16:9 late reflows every exhibit; decide the ratio first and build to it.
- **Too many layouts.** A sprawling layout set nobody understands leads to off-template slides; keep a tight, named inventory.
- **Unaligned number columns.** Center-aligned numerals or inconsistent decimals make tables unreadable; standardize right-aligned numerals with per-metric decimal rules.

## Output format
```
TEMPLATE SPEC — Firm Finance Master (16:9)
COLORS   primary #0B2545 | secondary #5C6B7A | accent #C6A15B (non-text) | ink #1A1A1A | rule #D9DEE3
TYPE     Family: <sans>  | Title 28 semibold | Head 14 bold | Body 12 | Source 9 | all left-aligned
GRID     12 col, 0.5" margins, footer band 0.4"

LAYOUTS
1 Cover        [logo][title][subtitle][project code][date][confidentiality]
2 Section      [section no][section title]
3 Content      [action title][body / bullets][source][page#]
4 Exhibit-Table[action title][table zone][source][page#]
5 Exhibit-Chart[action title][chart zone][source][page#]
6 Full-bleed   [chart zone full][floating title][source]
7 Two-up       [action title][left zone][right zone][source][page#]
8 Appendix     [action title][flexible zone][source][page#]

CONTRAST  navy/white 12.6:1 PASS | slate/white 4.9:1 PASS | gold text FAIL -> non-text only
LOCKED    master chrome, footer, page#, legend    EDITABLE  title, body, exhibit content
```

## Reference

### Layout inventory
| # | Layout | Purpose | Key placeholders |
| --- | --- | --- | --- |
| 1 | Cover / title | Deck opener | Logo, title, subtitle, project code, date, legend |
| 2 | Section divider | Break between sections | Section number, section title |
| 3 | Content | One-message text slide | Action title, body, source, page# |
| 4 | Exhibit (table) | Tabular data | Action title, table zone, source, page# |
| 5 | Exhibit (chart) | Single chart | Action title, chart zone, source, page# |
| 6 | Full-bleed chart | Dominant visual | Full chart zone, floating title, source |
| 7 | Two-up comparison | Side-by-side | Action title, left zone, right zone, source |
| 8 | Appendix | Supporting detail | Action title, flexible zone, source, page# |

### Master-element checklist
| Element | Requirement |
| --- | --- |
| Footer band | Footer text + confidentiality legend on every non-cover layout |
| Page number | Auto field, consistent position |
| Logo lockup | Fixed position and clear space |
| Source line | Present in every exhibit layout |
| Text styles | Title/head/body/source defined at master level |
| Confidentiality | Legend field driven by master |

### Color and type spec
| Token | Value | Use |
| --- | --- | --- |
| Primary | Deep brand color (e.g., navy) | Titles, header rows, key accents |
| Secondary | Neutral (e.g., slate) | Body emphasis, secondary series |
| Accent | Bright color | Rules and fills only if it fails text contrast |
| Ink | Near-black | Body text |
| Rule | Light gray | Table lines, gridlines |
| Title / Head / Body / Source | Descending sizes, one family | Text hierarchy |

### Exhibit-zone conventions
| Zone | Standard |
| --- | --- |
| Table header | Primary fill, white bold, left for labels / right for numbers |
| Table body | Right-aligned numerals; decimals per metric class (x to 1dp, % to 1dp) |
| Table banding | Subtle alternate-row shading or none; consistent |
| Chart plot | Horizontal gridlines only; no chart junk |
| Chart legend | Fixed position (right or bottom), consistent across deck |
| Data labels | On for key series, off for dense series; consistent decimals |

### Reuse and handoff rules
| Rule | Detail |
| --- | --- |
| Editable vs locked | Content placeholders editable; master chrome locked |
| Update path | Change once on master; layouts inherit |
| Naming | `Firm Finance Master <ratio> v<N>` |
| Handoff | Template is the authoring base for fina-pptx-author |
| Accessibility gate | No text on a fill below 4.5:1 (3:1 for large text) |
