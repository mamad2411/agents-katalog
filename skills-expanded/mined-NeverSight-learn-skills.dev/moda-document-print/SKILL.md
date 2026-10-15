---
name: moda-document-print
description: >-
  Print pieces: poster, flyer, brochure/trifold, menu, resume, certificate,
  invitation, business card, merch — print sizes, PDF out. A poster/flyer FOR
  a platform → that moda-social child.
argument-hint: "[the piece + what it says] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-document-print

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Sizes and defaults

All `--category prints`; sizes are canvas pixels at the piece's physical intent.

| Piece | Size | Notes |
|---|---|---|
| Flyer / one-sheet | 816×1056 | US-Letter (A4: 794×1123) |
| Poster 18×24in | 1350×1800 | 24×36in → 1800×2700; type scales with the sheet |
| Trifold brochure | 1056×816 × 2 pages | 3 panels per side — imposition in references/print.md |
| Menu | 816×1056 | often 2 pages; keep prices on one grid |
| Resume | 816×1056 | one page unless the user says otherwise |
| Certificate | 1056×816 | landscape Letter |
| Invitation | 525×750 | 5×7in |
| Letterhead | 816×1056 | US-Letter (A4: 794×1123); a small mark up top, body left empty |
| Postcard | 528×384 | 5.5×4in; 2 pages — keep the back's right side clear if it's mailed |
| Business card | 375×225 | 3.5×2in + bleed; 2 pages (front, back) |
| Merch (t-shirt, sticker, mug) | see references/print.md | flat art, no bleed assumptions |

- **A print piece is read up close — pack the page.** Icons, rules, stat rows
  and cards carry structure; a screen-sparse layout looks empty in the hand.
- Keep meaningful content ≥3mm (~12px at Letter scale) off every trimmed edge;
  let backgrounds and colour fields run to the edge.
- A poster or flyer FOR a platform (an Instagram poster) is not this skill — the
  platform child owns the size and safe areas.
- Pixel-only and RGB-only: no CMYK or PDF/X export, no DPI metadata — the print
  shop's preflight converts; say so rather than promising press-ready CMYK. A
  vendor's dieline can't import as locked guides — rebuild it, then delete it
  before export (references/print.md).

## Recipe — one printed piece

1. `moda canvas create --name "[Piece]" --intent "[one-line brief]" --size [WxH from the table] --pages [1 or 2] --category prints --brand [KIT]` — send the link immediately.
2. Read the source with your harness's file-reading tools; scope the piece to one
   dense page (or one page per side) before authoring anything.
3. Imagery: a poster or invitation usually earns a generated hero — `moda media generate-image --prompt "[subject, brand palette]" --model [MODEL]`; a menu or resume is a legitimate type-only piece. State the choice.
4. Author one apply per page/side: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]` (references/markup.md), with the kit's tokens.
5. `moda canvas screenshot [CANVAS_REF]` — check edge clearance, fold panels, type floor, and that nothing critical sits in a trim zone; fix and re-screenshot.
6. `moda export [CANVAS_REF] --format pdf -o [piece].pdf` — the default PDF is vector with selectable text and embedded fonts, crisp at any print scale. Do NOT pass `--flatten` unless the user asks for raster.
7. Read `warnings[]` and relay honestly: `pdf_links_flattened` (links are plain text in print — expected here), `font_substituted` (a face did not embed).

## Recipe — trifold brochure

1. Create TWO landscape Letter pages (1056×816), `--category prints`.
2. Panel order is NOT reading order: outside page is panels 5-6-1, inside page is
   2-3-4 — the imposition map is in references/print.md. Author to the map.
3. Author each side in one apply; keep a ~6px gutter of quiet either side of each
   fold line so no headline lands on a crease.
4. Screenshot, verify panel-by-panel against the reading order, then export PDF.

## Examples

- "a poster for our concert" → single-piece recipe at 18×24in.
- "a trifold brochure for the open house" → trifold recipe, imposed correctly.
- "make my resume look designed" → single-piece recipe at 816×1056, type-only.
- "business cards for the team" → 2 pages (front/back) with bleed, PDF out.
- "a t-shirt for the conference" → merch row: flat art, brand marks at real scale.

## Errors

Any typed error → load moda-core and read its recovery reference.
The trap here is a flattened PDF: the raster default is for screens, so print
exports omit `--flatten`. `stale_revision` heals — re-read and retry once.

## Make it recurring

An event series — a monthly menu, a recurring certificate run — is the cheapest
return reason Moda has: save the proven piece with moda-templates, then let
moda-automate fill in the blanks each cycle.

See also: moda-document — reports, one-pagers, multi-page documents ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/print.md | sizes, bleed, print density, the trifold imposition map, merch |
| references/document-design.md | scope, density, page balance |
| references/export.md | vector vs flattened PDF, warnings |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
