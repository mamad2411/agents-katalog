---
name: celebrant-prompted-print-assets
description: Prompt-led workflow for generating and revising celebrant business cards and DL C-fold trifold brochures directly with image generation/editing after analyzing a client website, assets, and design docs. Use for celebrant print collateral, business cards, brochures, prompt-only image generation, image edits, client revisions, exact 303mm x 216mm bleed artwork, and 97/99/101 or 101/99/97 trifold panels.
---

# Celebrant Prompted Print Assets

Use this skill when the user wants Codex to stay in-chat and produce or revise celebrant print artwork through image editing/generation prompts, rather than relying on the `/Users/jack/tools/celebrant-print-generator` CLI.

The CLI can be used as a reference or fallback, but the default workflow here is: inspect project and existing collateral -> choose the approved/closest visual template -> build a print brief -> edit/remap existing artwork where possible -> use image generation only for missing visuals or tightly scoped edits -> verify dimensions and revisions.

## Non-negotiable template-first rule

Do not use image generation as a blank-canvas redesign tool when an existing approved brochure/card, prior output, or successful client template exists. Most failures come from asking the model to reinvent a layout that was already working.

The successful Alex Real brochure output is the current quality benchmark for all celebrant print work. Future clients should reach the same standard of visual finish: rich but legible panel compositions, no unfinished blank areas, balanced cover/back/inside hierarchy, tasteful layered backgrounds, premium celebrant tone, and contact/QR/badge areas that look intentionally designed. This is a quality benchmark, not a license to copy Alex's brand, copy, photos, logo, colours, or identity.

Priority order for every client:

1. **Approved existing artwork**: use it as the visual source of truth. Preserve composition, palette, typography direction, visual density, logo treatment, image placement, and hierarchy.
2. **Previous output backups**: files like `brochure-side-a-outside.imagegen-before-panel-fix.png`, `brochure-side-b-inside.imagegen-before-panel-fix.png`, `*.before-*.png`, or prior print-output files should be inspected before generating anything new.
3. **Closest successful template**: use successful prior celebrant brochures/cards as strict composition-quality guides. The Alex Real brochure in `/Users/jack/Documents/GitHub/alex-real/print-output/` is the current high-water mark; adapt its polish and design density to the client's own brand.
4. **Image generation**: use only for missing backgrounds/motifs/photos or very localized edits. Full-side regeneration requires explicit user approval or no usable template.

For panel sizing fixes, never regenerate the artwork. Remap/crop/resize the existing raster panels deterministically to the printer guideline geometry and keep the design looking the same.

## Non-negotiable design density

Dead space is a failure condition for celebrant print collateral. Do not leave any panel looking empty, unfinished, or like content was simply placed in the upper half with nothing supporting the rest of the panel.

For every card side and every brochure panel:

- Fill the full panel with an intentional composition: image, tint, texture, floral/botanical illustration, border, quote, service block, contact block, badge/QR area, pattern, or layered background.
- Use quiet space only as breathing room around a clear focal point, never as a large blank zone. If an area is intentionally calm, it still needs subtle visual interest such as a soft gradient, botanical linework, paper texture, translucent image wash, fine border, or oversized cropped motif.
- Each panel should have a top, middle, and bottom visual anchor. A panel with only top-heavy content must be revised before delivery.
- Prefer full-height or large cropped imagery, background washes, ornamental frames, service pills, testimonials, fee blocks, process steps, floral corners, butterflies, vines, or patterned overlays to keep panels visually full while preserving legibility.
- Avoid sparse white cards floating on pale backgrounds unless the card itself contains enough content and the surrounding background has visible brand texture or illustration.
- Do not solve dead space by adding invented claims, fake testimonials, fake prices, fake accreditations, placeholder copy, or irrelevant filler. Use approved content, real assets, generated decorative motifs, or non-text visual structure.
- If there is not enough real copy for a panel, enlarge the image/portrait/logo treatment, introduce a tasteful decorative composition, or split approved content into designed modules.

## Decision rule

- Use this skill for prompt-led generation, direct image edits, and client revision rounds.
- Use `celebrant-print-assets` only when the user explicitly wants the CLI workflow.
- Do not regenerate a whole side for a small revision. Classify revision requests first.

## Exact print specs

Business card:

- Trim: `85mm x 55mm`
- Bleed artwork: `91mm x 61mm`
- Safe zone: important text/logos at least `6mm` inside trim (`9mm` from the full artwork edge including bleed)
- Prompt size target: `1456x976`

DL C-fold trifold brochure:

- Finished trim: `297mm x 210mm` per page, A4 landscape
- Final bleed artwork: `303mm x 216mm`
- Bleed: `3mm` on all outer edges
- Final export target: `3579 x 2551px` at `300 DPI`
- PDF page target: `858.8976377952756 x 612.2834645669292 pt`
- Never use `3579 x 2550px`; the supplied printer PDF's 216mm height rounds to `2551px` at 300 DPI.
- Safe zone: important content at least `12mm` inside trim and away from folds (`15mm` from the full artwork edge including bleed)
- Prompt size target: `3008x2144`

Outside / Side A panels left to right:

1. Fold-in flap: `97mm`
2. Back cover: `99mm`
3. Front cover: `101mm`

Inside / Side B panels left to right:

1. Inside left: `101mm`
2. Inside centre: `99mm`
3. Inside fold-in: `97mm`

Full bleed-sheet columns:

- Treat the printer guideline PDF as the authority. Render it at 300 DPI and derive fold/cut positions from it when supplied.
- For `/Users/jack/Desktop/celebrants-brochure-card-gen/printing-rules-guide/DL Leaflet Artwork Guidelines (4).pdf`, the current validated full-bleed raster columns are:
  - Side A / outside: `1182px / 1169px / 1228px`
  - Side B / inside: `1229px / 1169px / 1181px`
- Do not blindly use `100mm / 99mm / 104mm` or `104mm / 99mm / 100mm` as raster columns. Those are conceptual bleed-sheet widths; the rendered guideline PDF controls the final pixel boundaries.

## Project analysis

Before generating, inspect the project and produce a concise print brief in the response or a local note if useful.

Gather:

- Client/person/business name, role, tagline, contact details, service area, socials
- Services, intro copy, biography, booking copy, testimonials, fees if present
- Brand colours, typography, tone, motifs, visual style, things to avoid
- Asset paths for logos, portraits, badges/accreditations, backgrounds, ceremony photos
- Exact website URL for QR code, if needed

Search likely locations: `src`, `app`, `pages`, `components`, `content`, `public`, `assets`, `docs`, `README`, JSON/YAML/Markdown, and client documents. Use real project evidence; do not invent contact details, accreditations, prices, awards, legal claims, testimonials, or people.

## Generation sequence

Create or revise one output at a time, in this order:

1. Business card front
2. Business card back
3. Brochure Side A / outside
4. Brochure Side B / inside

For each output:

- If an existing approved/template image exists, use edit/remap mode rather than generation mode.
- Preserve approved composition unless the user explicitly asks for a new design.
- Attach relevant references when the tool supports image references.
- Put the most identity-critical reference first: existing artwork/template first for edits, portrait for portrait outputs, logo for logo-only outputs.
- Ask for one flat print artwork only, never a mockup.
- Include the exact trim, bleed artwork, safe zone, panel widths, and panel order.
- State that no crop marks, fold guides, bleed labels, measurement labels, or visible printer marks should appear.
- Require backgrounds and large fills to extend to every artwork edge for bleed.
- Require all important text, logos, QR codes, faces, and badges to stay out of the bleed and away from folds.
- Keep cutter safety visibly generous. Text, logos, faces, QR codes, badges, and fine rules must not sit close to any cut edge or fold line.
- Explicitly require no dead space: each panel/card side must feel complete from top to bottom with a focal point, supporting content, and decorative or image-based visual interest.
- When using AI image generation for artwork, plan deterministic text/vector overlays for exact names, phone numbers, emails, URLs, prices, QR codes, badges, testimonials, and legal/accreditation wording.

## Base prompt frame for new generation only

Use this only when no approved/template artwork exists or the user explicitly requested a new design. For revisions, use the edit prompt below instead.

Use this frame and adapt it to the specific output:

```text
Create [OUTPUT NAME] for a professional UK celebrant.

Print artwork:
- Single flat print artwork, not a mockup.
- Full bleed artwork: [WIDTH] x [HEIGHT].
- Finished trim: [WIDTH] x [HEIGHT].
- Bleed: 3mm on all outer edges.
- Safe zone: keep important text, logos, QR codes, faces, and badge details at least [SAFE] inside trim and away from folds.
- No crop marks, fold guides, labels, measurement text, or printer marks.

Brand:
- Business/name: [BUSINESS]
- Person: [PERSON]
- Role: [ROLE]
- Tagline: [TAGLINE]
- Tone: [TONE]
- Colours: [COLOURS]
- Typography/style: [TYPE]
- Motifs: [MOTIFS]
- Avoid: [AVOID]

Reference use:
- Use supplied logos/portraits/badges/photos only for their intended roles.
- Do not invent people, accreditations, awards, prices, contact details, testimonials, or placeholder text.
- If an APC badge appears, the heading above it must read exactly: "Trained & Certified By".

Composition density:
- No dead space anywhere. Every panel/card side must have a finished top, middle, and bottom composition.
- Keep calm breathing room around important content, but fill quiet areas with subtle brand texture, soft gradients, botanical/floral linework, butterflies, translucent image washes, ornamental borders, service modules, quote blocks, or large cropped motifs.
- Avoid large plain white/cream/lilac zones unless they contain a clear focal point and supporting decorative structure.
- The result should feel premium, full, intentional, and print-designed, not like sparse web content pasted onto a page.
- Quality benchmark: match the polish and completeness of the successful Alex Real brochure while using this client's own identity, palette, copy, and imagery.

Content:
[EXACT COPY AND LAYOUT BY PANEL OR CARD SIDE]

Legibility:
- Prioritize readable real-world print text.
- Ensure every logo/crest/wordmark has strong contrast against its background.
```

## Output-specific layout

Business card front:

- Graphic/typographic brand side only
- Logo or brand mark, business name, tagline
- No portrait, QR, services, testimonial, contact details, or badge
- Fill the card with a complete brand composition: full-bleed colour/texture, floral frame or corner artwork, logo focal point, and balanced bottom detail. Do not leave a plain empty half.

Business card back:

- Name, role, exact contact details, website QR if available
- Key services line
- Portrait if a real portrait reference exists
- Accreditation badge only if supplied
- Balance contact details with portrait, QR, service line, badge, or decorative motif so the side has top, middle, and bottom structure.

Brochure Side A / outside:

- Full bleed artwork `303mm x 216mm`
- Left panel: fold-in flap, `97mm`; intro and services
- Centre panel: back cover, `99mm`; smaller logo, QR, exact contact details, accreditation badge if supplied
- Right panel: front cover, `101mm`; hero cover, prominent logo, business name, tagline
- Follow the active printer guideline PDF for rendered fold/cut positions. For the known DL Leaflet Artwork Guidelines PDF, the final full-bleed raster columns are `1182px / 1169px / 1228px`.
- Left fold-in flap must not be a sparse intro block. Use full-panel image wash, service stack, floral motifs, or quote/content modules to fill the height.
- Centre back cover must treat logo, badge, QR, and contact as a designed vertical composition with background texture or framing. Avoid a small logo/QR floating in empty space.
- Right front cover should be the strongest visual moment: full-bleed image or rich generated artwork, prominent logo/name/tagline, and a bottom anchor such as a strapline panel, border, or floral sweep.

Brochure Side B / inside:

- Full bleed artwork `303mm x 216mm`
- Left panel: inside-left, `101mm`; meet the celebrant and portrait if supplied
- Centre panel: inside-centre, `99mm`; service descriptions
- Right panel: inside-fold-in, `97mm`; what to expect, booking info, testimonial only if real text exists
- Follow the active printer guideline PDF for rendered fold/cut positions. For the known DL Leaflet Artwork Guidelines PDF, the final full-bleed raster columns are `1229px / 1169px / 1181px`.
- Inside-left should make the portrait a major feature if supplied, with biography copy and a bottom anchor such as testimonial, motif, or credential detail.
- Inside-centre should not become an empty list. Use image strips, service cards, ritual blocks, or a modular grid to fill the panel.
- Inside fold-in should combine process/booking/fees/testimonial content with a strong background image or decorative frame so it does not feel like text floating on a blank panel.

## Revision workflow

Before editing generated artwork, classify the revision:

- `Text/QR/logo replacement`: Prefer deterministic overlay or a tightly localized edit. Do not regenerate the full image.
- `Panel sizing / fold geometry`: Deterministically remap the existing raster to the printer guideline positions. Do not ask imagegen to fix geometry.
- `Small visual fix`: Use image editing with the original artwork as the first input. If masks/crops are available, edit only the target region.
- `Structural redesign`: Regenerate only the affected output side, and preserve all approved copy/assets unless the user asks to change them.

For small image edits, use this prompt pattern:

```text
Edit the provided print artwork. Preserve the entire composition, colours, panel layout, typography style, portrait/logo placement, bleed, safe zones, visual density, and all unchanged text exactly as-is. Change only this localized item: [CHANGE]. Do not redesign the artwork. Do not introduce dead space. Do not alter any other panel, image, logo, contact detail, QR code, badge, face, border, background, or decorative element.
```

If the edit tool supports masks, use a mask/crop around only the affected region. If it does not, make the prompt even stricter and warn the user that image edits can still drift.

## Verification

Before final delivery:

- Confirm the requested outputs exist.
- Confirm brochure panel order and sizes are correct.
- Confirm the artwork is full bleed, not a mockup.
- Perform a dead-space audit on every card side and every brochure panel. Reject or revise any panel that has a large blank-looking zone, weak bottom half, top-heavy layout, empty centre, floating card, or pale area with no texture/motif/content.
- Confirm every panel has top, middle, and bottom visual anchors.
- Confirm quiet areas still contain intentional visual interest such as gradient, texture, image wash, floral/botanical linework, border, motif, or designed content module.
- Manually proof every character of names, phone, email, website, QR, badges, and testimonials.
- Check that no text/logos/faces/QR/badges sit in bleed or on folds.
- For paid print, recommend a final deterministic text/vector overlay pass for mission-critical contact details.
