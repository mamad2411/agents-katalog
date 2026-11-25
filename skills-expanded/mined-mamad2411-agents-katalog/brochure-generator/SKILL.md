---
name: brochure-generator
description: >-
  Create, repair, verify, and export celebrant DL C-fold brochures as
  crop-mark/template proof PDFs with supporting PNG sheets from celebrant website
  GitHub repositories, approved client copy, website assets, and brochure source
  files. Use this whenever the user asks to
  drop into a celebrant site repo and generate a brochure, retrieve the logo,
  include APC accreditation, create a QR code, make a trifold/tri-fold/leaflet,
  produce PNG brochure output, place artwork on a blank print template, check
  crop/bleed/panel widths, fix QR/back-cover issues, or turn website copy and
  assets into brochure artwork, even if they only mention a client name, an
  existing brochure file, or "make the brochure".
---

# Brochure Generator

Use this skill to create or fix professional celebrant brochures where the final
deliverable must include a crop-mark/template proof PDF plus the flat
outside/inside PNG artwork used to build it. The goal is not just a nice-looking
HTML page; the output must produce clean outside/inside PNG artwork with correct
DL C-fold geometry, readable text, truthful client details, APC accreditation
requirements, and a verified PDF proof sitting correctly in the printer crop
template. Do not call a brochure complete if the crop-mark/template PDF is
missing, unverified, or built from an inset proof instead of flat artwork.

## Bundled Resources

Read these only when needed:

- `TEMPLATE.md` - use when starting a fresh brochure HTML file.
- `CHECKLIST.md` - use before final delivery or when fixing an existing brochure.
- `scripts/overlay_brochure_on_template.py` - use when placing finished flat
  artwork PNGs/PDF pages onto blank printer template PNGs and exporting a
  positioned proof PDF.
- `references/dl-cfold-bleed-crop-template.pdf` - use when the user asks for a
  crop-mark proof, grey-box placement proof, or printer template wrapper.
- `assets/APC-seal.png` - fallback Academy of Professional Celebrants badge
  when the source repo does not already contain an approved APC mark.

## Default Output Mode

The crop-mark/template proof PDF is the required final output. PNG sheets are
required supporting artwork, not a replacement for the proof PDF.

Always generate:

- `brochure-<client>-outside.png`
- `brochure-<client>-inside.png`
- `brochure-<client>.html`
- `brochure-<client>-template-proof.pdf`
- `brochure-<client>-template-proof-front-template.png`
- `brochure-<client>-template-proof-back-template.png`

Generate `brochure-<client>.pdf` with `to-pdf.js` when a native master PDF is
also useful, but never treat it as a substitute for the template proof PDF unless
the user explicitly says they do not need the printer-template/crop-mark proof.

The normal completion path is:

1. Export or update flat full-bleed PNG artwork.
2. Overlay those PNGs onto the front/back printer template PNGs.
3. Export the two-page template proof PDF from the composed PNGs.
4. Verify `pdfinfo`, `pdfimages -list`, composed PNG dimensions, and visual
   placement before final response.

## Website Repo Source-Of-Truth Mode

The normal use case is that the user opens or points at a celebrant website
GitHub repo, and that repo is the source of truth for the brochure. Treat the
website repo as the setup: it should provide the logo, brand direction, client
copy, services, contact details, website URL, imagery, and existing site tone.
Do not require the website repo to already contain brochure scripts.

When invoked inside or against a celebrant website repo:

1. Resolve the source repo first, then inspect it before designing.
2. Build a quick source map of the real inputs found on disk: logo, brand
   colours/fonts, name/title, phone, email, area/location, website URL,
   services, bio/about copy, imagery, APC badge, and any existing print assets.
3. Record the file path for every fact or asset that affects the brochure. If a
   required fact is missing, ask the user or omit that element; do not invent it.
4. Use the repo's website design system as the visual base unless the user gives
   a stronger instruction.
5. Use the reliable brochure generator/exporter as tooling when the source repo
   does not contain equivalent scripts.

Search likely source locations:

- `AGENTS.md`, `README*`, `docs/`, project notes, and setup docs.
- `package.json`, framework config, `src/`, `app/`, `pages/`, `components/`,
  `content/`, `data/`, `lib/`, and `config/`.
- `public/`, `assets/`, `src/assets/`, `static/`, `media/`, image folders, and
  favicon/logo folders.
- constants, metadata, schema, SEO, contact, navigation, footer, homepage, about,
  services, and ceremony pages.
- existing `print-output/`, `brochure-materials/`, `output/`,
  `brochure-*.html`, `*-outside.png`, `*-inside.png`, PDFs, cards, and flyers.

Logo handling:

- Prefer the actual logo file from the website repo.
- Prefer transparent PNG/SVG/logo variants for print; create a transparent copy
  only when the source logo has an accidental box/background.
- Use the logo on the front cover and back cover when supplied.

APC badge handling:

- Prefer an APC badge or Academy of Professional Celebrants mark already present
  in the source repo or existing approved collateral.
- If none exists, use bundled
  `/Users/jack/.agents/skills/brochure-generator/assets/APC-seal.png` and place
  it with wording such as `Trained & Certified By`.
- Do not remove the APC badge because the source repo forgot to include it.

QR handling:

- Generate a QR code only when the repo contains a real website URL/domain.
- Prefer an inline SVG QR generated by `qrencode`; avoid browser-time QR
  generation for final output when a static SVG is easy.
- If no real website exists, omit website text, QR code, QR caption, and QR
  libraries completely.

## Template Overlay Workflow

Use this workflow for every completed brochure unless the user explicitly opts
out of crop/template proof output. It also applies when the user already has
finished flat brochure artwork and a blank print template that shows brochure
size, bleed, fold lines, crop marks, or panel guides. This is the "template PNGs
-> place client brochure PNGs on top -> export as PDF" task.

The overlay output is intentionally a PDF proof even though normal brochure
creation is PNG-first.

For this workflow, the composed PNGs are the source of truth. The PDF must be a
simple two-page wrapper around those exact PNG files: page 1 is the composed
front/outside PNG, page 2 is the composed back/inside PNG. Do not rebuild,
rerender, crop, or reposition the artwork separately during PDF creation.

Preferred inputs:

- outside/front-cover template PNG
- inside/back template PNG
- outside/front-cover brochure artwork PNG
- inside/back brochure artwork PNG
- optional original template PDF for exact page size

Prefer flat full-bleed PNG artwork from `to-png.js`. Do not use a proof PDF or a
printer-template PDF as artwork input unless you have confirmed the PDF pages are
art-only and contain no inset margins, crop marks, template border, or safe-zone
guide area. If the PDF already contains margins, first regenerate or extract the
true flat `brochure-<client>-outside.png` and `brochure-<client>-inside.png`
files.

If the finished artwork is a confirmed art-only two-page PDF, use it with
`--art-pdf`. Page 1 maps to the outside/front-cover template. Page 2 maps to the
inside/back template.

For the current supplier files, the naming is easy to confuse:

- `front-templates.png` is the outside/front-cover side: inner flap, back cover,
  front cover.
- `back-templates.png` is the inside/back side: left panel, centre panel, right
  fold-in panel.

Run the bundled script from any working directory:

```bash
python3 /Users/jack/.agents/skills/brochure-generator/scripts/overlay_brochure_on_template.py \
  --front-template "/path/to/front-templates.png" \
  --back-template "/path/to/back-templates.png" \
  --front-art "/path/to/brochure-client-outside.png" \
  --back-art "/path/to/brochure-client-inside.png" \
  --template-pdf "/path/to/brouchure-template.pdf" \
  --out "/path/to/client-brochure-template-proof.pdf"
```

For a two-page finished artwork PDF:

```bash
python3 /Users/jack/.agents/skills/brochure-generator/scripts/overlay_brochure_on_template.py \
  --front-template "/path/to/front-templates.png" \
  --back-template "/path/to/back-templates.png" \
  --art-pdf "/path/to/leaflet.pdf" \
  --template-pdf "/path/to/brouchure-template.pdf" \
  --out "/path/to/client-brochure-template-proof.pdf"
```

The script detects the full-bleed artwork box from the template pixels and
places the artwork on top of the template without manual dragging. On the
supplied `2000 x 1453` template PNGs, the full-bleed box is roughly `50,50` with
about `1900 x 1354` pixels. If detection is ever wrong, rerun with
`--placement x,y,w,h` in template-pixel coordinates.

The script also checks the artwork aspect ratio against the detected placement
box. If it fails, do not force it through. That usually means the input is an
already-inset proof/template PDF, which will place the design inside the red safe
line instead of filling the bleed area.

After overlay export, verify:

```bash
pdfinfo client-brochure-template-proof.pdf
pdfimages -list client-brochure-template-proof.pdf
sips -g pixelWidth -g pixelHeight client-brochure-template-proof-front-template.png
sips -g pixelWidth -g pixelHeight client-brochure-template-proof-back-template.png
```

Expected proof PDF result for the current Affinity template:

- Page count: `2`
- `pdfimages -list` shows one full-page image on each page
- Page size: about `902.898 x 656.283 pt`
- Composed PNGs remain the same size as the template PNGs
- Artwork fills the full-bleed placement box and leaves the outer template/crop
  marks visible

## Global Operating Mode

This is a global user skill, so do not assume the current working directory is
the brochure-generation repo. Separate the source project from the generation
tools.

Resolve the source project in this order:

1. If the user gives a path, use that repo/folder as the source project.
2. If the current working directory is a likely celebrant website repo, use it as
   the source project even if it does not contain brochure scripts.
3. If the user only gives a client name and no usable current repo, use the
   canonical brochure workspace as the source project:
   `/Users/jack/Documents/GitHub/celebrants-brochure-card-gen`.
4. If no source-backed project or supplied files can be found, ask the user for
   the website repo path before generating client-specific facts.

A likely website repo has site/project signals such as `package.json`,
`vite.config.*`, `next.config.*`, `astro.config.*`, `src/`, `app/`, `pages/`,
`public/`, `content/`, client images, site metadata, or existing deployment
docs.

Resolve the generation tools separately:

1. If the source repo contains `to-png.js`, `preflight-brochure.js`, and
   `check-brochure-layout.js`, generate in that repo.
2. Otherwise use the canonical brochure generator tooling at
   `/Users/jack/Documents/GitHub/celebrants-brochure-card-gen`.
3. When generating in the canonical workspace from another website repo, keep the
   website repo as the source of truth. Copy needed print-safe assets into
   `assets/<client>/` or reference them by paths the exporter can resolve. Do not
   treat the canonical workspace's old client data as source truth for a new
   website repo.

Before making a brochure, read source project instructions when they exist:

- `AGENTS.md`
- `docs/celebrant-website-guidelines.md`
- `docs/print-font-strategy.md`
- `brochure-plan.md`
- the relevant website pages, data files, or `assets/<client>/info.md`

If a file is absent, continue using the bundled template and checklist. Do not
block unless the missing file contains the only source for required client data.

## Input Priority

Use approved, source-backed inputs in this order:

1. The celebrant website repo named by the user or active in the current working
   directory: source files, data files, metadata, assets, and existing site copy.
2. Existing approved brochure/card artwork or prior print output.
3. Canonical brief, brochure plan, client `info.md`, supplied copy docs, or
   other approved source files.
4. Approved website design system: colours, typography, imagery, logo, tone.
5. Direct user instructions from the current conversation.

Never invent testimonials, services, locations, websites, religious claims,
certifications, pricing, or client facts to fill space. If a panel feels empty,
increase visual density with layout, type scale, image scale, accreditation
balance, or source-backed copy. Do not pad a sparse panel by simply spreading
small text farther apart or leaving a quiet lower third.

Before writing final brochure copy, check at least the homepage, about/profile,
services/ceremony pages, footer/contact components, site metadata, and any data
or content folders that exist. This is how the skill retrieves the client facts
instead of relying on memory or guessing.

## Preserve Proven Work

Before redesigning, inspect existing collateral outputs and successful prior
client examples in folders such as:

- `print-output/`
- `brochure-materials/`
- `output/`
- `assets/<client>/`
- existing `brochure-*.html`, `*-outside.png`, `*-inside.png`, or PDFs

Do not redesign a brochure just to fix panel sizing, QR codes, contact details,
copy, bleed, or crop marks. Preserve the approved composition when possible and
apply the smallest deterministic fix: CSS geometry correction, text edit, asset
swap, QR replacement, raster remap, or exporter rerun.

The Alex Real brochure at `/Users/jack/Documents/GitHub/alex-real/print-output/`
is a quality benchmark for polish: strong cover, intentional back/contact panel,
balanced inside panels, dense but legible copy, no unfinished blank areas, and
client-specific branding. Use it as a standard, not copied branding.

Before final delivery, visually compare the current flat PNGs and crop-template
proof against Alex Real and at least one relevant generated brochure example
from `/Users/jack/Documents/GitHub/celebrants-brochure-card-gen/`. This is a
hard acceptance check, not optional inspiration. Reject and revise the brochure
if the comparison shows any of these problems:

- body text is noticeably smaller or harder to read than the benchmark examples
- a panel feels empty, unfinished, or padded out with dead space
- contact, QR, APC, logo, or portrait elements look timid or under-scaled
- the design looks like a browser screenshot instead of finished print artwork
- the crop-template proof technically aligns but the brochure itself lacks
  visual weight, hierarchy, or client-specific polish

## Print Geometry

The printer-confirmed DL C-fold dimensions are fixed:

- Finished trim: `297mm x 210mm`
- Full artwork with bleed: `303mm x 216mm`
- Bleed: `3mm` on all outside edges
- CSS page rule: `@page { size: 303mm 216mm; margin: 0; }`
- Expected 300 DPI PNG size: approximately `3579 x 2551 px` per side
- Optional PDF page size, when generated: about `858.898 x 612.283 pt`
- Optional PDF page count, when generated: `2`

Panel widths are asymmetric because the fold-in panel is narrower:

- Side A / outside, left to right: fold-in `97mm`, back `99mm`, front `101mm`
- Side B / inside, left to right: front `101mm`, centre `99mm`, fold-in `97mm`

With outer bleed included, CSS grid columns are:

- Side A: `100mm 99mm 104mm`
- Side B: `104mm 99mm 100mm`

Keep critical content away from cuts and folds:

- Never use less than the repo's `8mm` safe margin for text, logos, QR codes,
  badges, faces, eyes, fine rules, or important decorative marks.
- Prefer `12mm` clearance for critical content where a cut or fold risk exists.
- Only non-critical background colour, texture, image bleed, or decoration should
  enter the bleed area or sit close to folds.

If a printer guideline PDF is supplied, render and measure that specific guide at
300 DPI and treat its actual guide positions as final authority.

## Mandatory Elements

Every brochure must include:

- APC seal or Academy of Professional Celebrants accreditation mark on the back
  cover/contact panel, with wording such as `Trained & Certified By`. Use the
  source repo's badge when present; otherwise use bundled
  `/Users/jack/.agents/skills/brochure-generator/assets/APC-seal.png`.
- Phone, email, and area on the back cover/contact panel.
- Website and QR code only when the source material contains a real website.
- Logo on the front cover and back cover when a logo is supplied.
- Client name and celebrant title on the front cover.
- At least one portrait/personal image inside or on the fold-in panel when a
  suitable portrait is supplied.

Never use placeholder contact content. Do not write `Website to follow`,
`coming soon`, placeholder domains, fake URLs, or `https://[WEBSITE]`. If there
is no real website, omit the website row, QR code, QR caption, and QR library.
Use the freed space to improve APC, contact, logo, or source-backed copy balance.

For QR codes, prefer an inline SVG generated by `qrencode` when available:

```bash
qrencode -t SVG -o assets/<client>/qr-code.svg -l M --svg-path -m 0 'https://example.co.uk'
```

If an existing template already uses `qrcode.js`, that is acceptable during
iteration, but verify the QR renders in the exported PDF/PNG before delivery.

## Cover And Imagery Rules

Do not use a close portrait of the celebrant as the front-cover hero. The
front-cover-to-flap fold can run through the image and split a face. Put
portraits on the inside or fold-in panel unless the user explicitly asks for a
different composition and the fold does not damage the face.

Prefer front-cover imagery that survives folding:

- branded abstract/editorial imagery
- florals, candles, hands, rings, ceremony settings, landscapes
- website mood or parallax imagery
- custom generated scene assets when source imagery is missing

For every portrait/headshot displayed with `object-fit: cover`, set explicit
`object-position`. After exporting PNG previews, visually check that head, hair,
forehead, face, and shoulders are not awkwardly clipped. If they are clipped,
tune `object-position`, change the frame ratio, or pick another image.

Use transparent logos wherever possible. If a supplied logo has an accidental
white or boxed background that clashes with the design, create or use a
transparent version before placing it on coloured or photographic backgrounds.

## Design And Copy Standards

The brochure should feel like a natural print extension of the approved website,
not a generic template.

- Use the website colour system and font direction where practical.
- Define colours as CSS custom properties using hex values.
- Use `mm` for structural print dimensions and `pt` for print text sizing.
- Use British English.
- Avoid religious imagery such as crosses, churches, priests, or explicitly
  religious service framing unless source material and user instructions require
  it.
- Use rich but legible visual density; no panel should look sparse.
- Body text should scale with content volume: light panels often need `12-14pt`,
  moderate panels `11-12pt`, and heavy panels `10-11pt`.
- When a panel has too much empty space, first make the design more readable and
  confident: increase typography size, enlarge meaningful elements such as
  QR/APC/logo/images, tighten weak spacing, or reduce unnecessary copy. Do not
  solve sparse panels by merely distributing the same small text over a taller
  area.
- Check the bottom of every panel in the exported PNG and crop-template proof.
  Excessive empty space at the bottom makes the brochure feel unfinished,
  especially on contact, flap, and step panels. Rebalance the panel before
  delivery.
- If the final proof is viewed at the same size as benchmark brochures and the
  body copy feels small, the task is not complete. Increase type scale, reduce
  unnecessary copy, tighten spacing, enlarge supporting elements, or rebalance
  panels until the brochure reads confidently in print.
- Avoid print-hostile CSS on final print content: unnecessary pseudo-elements,
  clipping tricks, decorative shadows on non-image containers, or wrapper effects
  that create artefacts in Affinity/PDF workflows.

## Standard Workflow

1. Identify the source repo, generation project, client slug, and desired output
   folder.
2. Read source project instructions and inspect the website repo for logo,
   brand, copy, contact details, URL, imagery, APC badge, and existing print
   assets.
3. Build a source map with file paths for the facts/assets used. Ask before
   inventing or filling gaps from guesswork.
4. Inspect existing brochure/output files before changing the design.
5. If starting fresh, read `TEMPLATE.md` and adapt it to the website repo's
   brand and content.
6. Copy or reference needed source assets so the exporter can resolve them,
   including the bundled APC badge only when the repo lacks one.
7. Build or repair the root HTML file, usually `brochure-<client>.html`.
8. Run static and rendered checks.
9. Export flat PNG sheets with `to-png.js`.
10. Visually inspect both PNG sheets before final response.
11. Verify PNG dimensions and image focus/crop quality.
12. Generate the crop-mark/template proof PDF by overlaying the flat PNGs onto
    the front/back printer template PNGs. The PDF must be built from the saved
    composed PNG proofs.
13. Verify the proof PDF with `pdfinfo`, `pdfimages -list`, composed PNG
    dimensions, and visual inspection. Do not call the task complete without
    these crop-template proof checks unless the user explicitly opted out.
14. Compare the rendered proof against Alex Real and at least one relevant
    generator example. Revise if text scale, panel density, or visual hierarchy
    is weaker than the benchmark.
15. Summarise the source repo used, output files, verification commands, and any
    unresolved risks.

## Verification Commands

Run these from the generation project root, not necessarily the source website
repo:

```bash
node preflight-brochure.js brochure-<client>.html
node check-brochure-layout.js brochure-<client>.html
node to-png.js brochure-<client>.html
sips -g pixelWidth -g pixelHeight brochure-<client>-outside.png
sips -g pixelWidth -g pixelHeight brochure-<client>-inside.png
python3 /Users/jack/.agents/skills/brochure-generator/scripts/overlay_brochure_on_template.py \
  --front-template "/path/to/front-templates.png" \
  --back-template "/path/to/back-templates.png" \
  --front-art "brochure-<client>-outside.png" \
  --back-art "brochure-<client>-inside.png" \
  --template-pdf "/Users/jack/.agents/skills/brochure-generator/references/dl-cfold-bleed-crop-template.pdf" \
  --out "brochure-<client>-template-proof.pdf"
pdfinfo brochure-<client>-template-proof.pdf
pdfimages -list brochure-<client>-template-proof.pdf
sips -g pixelWidth -g pixelHeight brochure-<client>-template-proof-front-template.png
sips -g pixelWidth -g pixelHeight brochure-<client>-template-proof-back-template.png
```

Expected core results:

- flat PNG artwork approximately `3579 x 2551 px` at 300 DPI target
- both sides render as complete artwork sheets with no clipped portraits, missing
  logos, sparse panels, overflow, or placeholder contact details
- template proof PDF has `2` pages
- `pdfimages -list` shows one full-page image per page
- composed template PNGs match the template PNG dimensions
- visual inspection confirms artwork fills the full-bleed placement area and
  does not sit inside the red safe line

Optional native master PDF commands:

```bash
node to-pdf.js brochure-<client>.html
pdfinfo brochure-<client>.pdf
```

Expected native master PDF results:

- native PDF page size around `858.898 x 612.283 pt`
- PDF page count `2`
- crop marks outside the artwork box in the exported PDF

If Puppeteer cannot find Chrome, run:

```bash
npx puppeteer browsers install chrome
```

If the user asks for the brochure placed inside the grey box or crop-mark test
template, use `references/dl-cfold-bleed-crop-template.pdf`. Render the template
and brochure at 300 DPI, centre the native-size brochure inside the detected grey
box, and do not scale or stretch the brochure image.

## Final Response Standard

Before answering, double-check the actual files on disk. Mention:

- the source website repo/folder used
- the final outside/inside PNG paths
- the HTML source path
- the PDF path only if a PDF was generated
- which verification commands passed
- any command you could not run, with the reason

Do not call the work finished if you have not inspected the rendered previews or
if a verification command failed without a clear explanation.
