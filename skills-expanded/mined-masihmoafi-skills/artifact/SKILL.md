---
name: artifact
description: "Handling rules for visual and document artifacts: PDFs, HTML reports, dashboards, slides and formula rendering. Load when creating, editing, verifying, or opening any of these artifact types."
---

# Artifact

Rules for producing, checking and opening PDFs, HTML reports, slides and formulas. Check every artifact visually before showing it: text visible and legible, consistent, inside its borders.

## Visual design check

Before showing a diagram, chart, slide or report: the primary takeaway is apparent at a glance to its audience; every accent colour carries information; every size or colour difference means something; elements sit on one grid and text aligns to its reading direction (right for Persian); steps and containers have room to breathe.

## PDFs

- For a scanned PDF: run `pdfinfo`, then one `pdftotext -layout` check; if it is empty, render pages with `pdftoppm` to `tmp/pdfs/` and inspect the PNGs at original detail.
- Keep a short inventory: page count, text-extraction result and what the pages contain.
- Stay local; use no online OCR or upload unless the user asks.
- After creating or editing a PDF the user will inspect, render a page to check it, then open it for the user with the environment's opener and confirm the viewer started.

## HTML reports

- After creating or materially editing a user-facing HTML artifact, open it for the user unless they say not to. A screenshot or headless render verifies it; it does not replace opening it.
- Open HTML in Chromium. For a site folder, especially one with assets, scripts or maps, serve it locally: `setsid python3 -m http.server <port> --directory <site-dir> >/tmp/<task>-server.log 2>&1 &`, then open `http://127.0.0.1:<port>/...`. Use `file://` only for a simple standalone page; if Chromium keeps loading, switch to the local server before saying it is open.
- Browser automation and screenshots are costly. Use cheaper local checks unless the UI, formulas or charts are new or materially changed; then do one visual pass before opening.
- Make alternative designs switchable in the HTML rather than describing them in chat.

## Slides and print layout

- For browser-printed HTML slides, do not rely on `.active` styles: print mode often forces every `.slide` to `display:flex`, so put `flex-direction`, `justify-content` and `gap` on the base `.slide` class.
- Check layout by rendering the PDF pages, not by reading extracted text: spot-check the most layout-sensitive pages and make a contact sheet for the whole deck.
- In RTL decks with image and text split layouts, a grid inherits `direction: rtl` and reverses its columns. Set the split container to `direction:ltr` and the text area back to `direction:rtl`.
- For mixed Persian and English slide text, prefer Persian-led phrasing and isolate short English terms; long English-led bullets often render in broken order in PDF.

## Formulas in HTML

- Browsers show raw TeX delimiters (`\(...\)`, `\[...\]`, `$$...$$`) as text unless a renderer or MathML is present.
- In handwritten HTML, write native MathML; Chromium and Firefox render it offline without JavaScript:

```html
<div class="math-display">
  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
    <msub><mi>s</mi><mi>k</mi></msub><mo>=</mo>
    <munderover><mo>&#x2211;</mo><mrow><mi>j</mi><mo>=</mo><mn>0</mn></mrow><mi>k</mi></munderover>
    <msub><mi>p</mi><mi>r</mi></msub><mo>(</mo><msub><mi>r</mi><mi>j</mi></msub><mo>)</mo>
  </math>
</div>
```

Give `.math-display` `direction: ltr` and `overflow: auto` so wide formulas scroll inside RTL pages.


- From Markdown, or when hand-written MathML is too slow for a large document, convert with Pandoc and keep the `.md` beside the `.html`: `pandoc input.md -s --mathml -c style.css -o output.html`.
- MathJax or KaTeX is acceptable only when its script and CSS are included and verified; avoid CDN renderers unless network use is acceptable.
- A plain-text formula is acceptable only when the user does not need typeset math; explain ambiguous notation in words, for example that `G_inverse(s_k)` means the inverse CDF.
- Before delivery, confirm the formulas became MathML with no raw delimiters left, then open the page and check they render as math:

```bash
rg -n '<math' output.html | head
rg -n '\[|\]|\$\$' output.html | head
```
