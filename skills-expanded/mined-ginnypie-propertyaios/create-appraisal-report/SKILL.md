---
name: create-appraisal-report
description: Use to turn a property address into a beautifully designed appraisal-report PDF. Runs the property-appraisal analysis, then renders it in a chosen brand theme (66days | harbour | noir). Trigger on "make an appraisal report", "appraisal PDF", "valuation report for an address".
---

# Skill — Create Appraisal Report (themed PDF)

Turns an address into a polished, downloadable appraisal-report PDF. Same layout every
time (cover · summary · comparables with a value number-line), swappable design theme.

**Stage:** 2 — Package · **Reads from:** property-appraisal output · **Writes:** a PDF

---

## What it is / is NOT
- A presentation layer over the `property-appraisal` skill — indicative, comparable-sales based.
- NOT a certified valuation. The report carries that disclaimer; keep it.
- Never invents comps, prices or dates. Every figure comes from `property-appraisal`
  (which uses only supplied or genuinely looked-up sold data).

## Inputs
- **Address** (required).
- **Theme** (optional, default `66days`): `66days` (crimson/cream), `harbour` (navy/teal),
  `noir` (charcoal/oxblood), or any file in the bundled `report-assets/themes/` folder.
- **Client name / purpose** (optional).

## Steps

1. **Run the appraisal.** Invoke the `property-appraisal` skill for the address. This
   produces the value range, subject attributes, and the comparable-sales table — the
   real, sourced data. Do not proceed with invented numbers.

2. **Gather images — REQUIRED, do not skip.** Every comparable and the subject MUST
   have a real photo URL, or the report renders with empty grey boxes. Reliable method:
   for each property, open its Domain property-profile page. The URL pattern is
   `https://www.domain.com.au/property-profile/` followed by the address as a slug —
   number-street-suburb-state-postcode, e.g. `9-grimes-place-davidson-nsw-2085`. On that
   page take the `og:image` meta URL — that is the hero listing photo (a
   `rimh2.domainstatic.com.au/...` link). realestate.com.au (`i2.au.reastatic.net`) and
   agent-site photos work too. Use your web/fetch tool to read the page and copy the
   `og:image`. Put one URL in each comp's `image` field and in the top-level `image`
   (subject). The renderer downloads and inlines them (jpeg/png/webp all handled). If a
   property genuinely has no photo, use its street-view or leave it as an empty string —
   but never leave the whole set empty. Public listing photos, for research ID only.

3. **Write a data file.** Copy `report-assets/example-11-apollo.json` and fill it with the
   appraisal output: `address`, `date`, value fields, subject summary, an array of
   `reasoning` paragraphs (simple emphasis markup is allowed), and the `comparables` array
   (each: ref, address, beds/baths/cars, price, date, relation = Comparable | Superior |
   Inferior, image; mark the anchor comp with `"anchor": true`).

4. **Render.** The renderer is bundled inside this skill, in the `report-assets/` folder
   next to this SKILL.md. Save your data file there (for example `report.json`), then run:
   ```bash
   cd "$(dirname "$0")/report-assets"
   python3 render.py report.json --theme 66days --out ./appraisal.pdf
   ```
   Swap `report.json`, the `--theme` value, and the `--out` path for your own. The script
   ALWAYS writes a fully self-contained `.html` first (every image + font embedded), then,
   **only if** Chrome / Chromium / Edge is already installed, auto-prints the matching PDF.
   The HTML is the real deliverable — it looks identical to the PDF and needs nothing else.

   **Do NOT install a browser, Playwright, Chromium, wkhtmltopdf, or any other engine.**
   If none is found the script says so and stops after the HTML — that is the expected,
   successful outcome, not an error. Downloading a browser is slow and unnecessary.

5. **Deliver — works on any OS.** Save the `.html` (and the `.pdf` if one was produced)
   somewhere the person can find it — their Documents folder, or the folder they ran this
   from. Then tell them: **open the `.html` in any web browser and choose Print → Save as
   PDF.** That Print-to-PDF option is built into every browser on Windows, macOS and Linux
   (Chrome, Edge, Firefox, Safari) — no software to install. The fonts and property photos
   are already embedded, so the printed PDF is pixel-identical to the report.

## Adding a person / brand
Drop a new token file in `report-assets/themes/` (copy an existing one, change the
`:root` values + font import). It is instantly selectable via the `--theme` flag.

## Files (all bundled in report-assets/)
- `render.py` — the renderer
- `master.template.html` — layout (has the theme slot)
- `report.body.template.html` — tokenized body
- `themes/` — the designs (66days, harbour, noir)
- `example-11-apollo.json` — worked example (11 Apollo Quay)

## Disclaimer
Indicative appraisal for research and preparation only — not a certified valuation. A
valuation for lending, purchase, sale, tax (CGT), legal or family-law purposes must be
prepared by a Certified Practising Valuer (CPV / API) or RICS registered valuer.
