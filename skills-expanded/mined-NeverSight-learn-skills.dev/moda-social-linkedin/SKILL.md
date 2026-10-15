---
name: moda-social-linkedin
description: >-
  LinkedIn creative: posts, document carousels (exported as ONE multi-page
  PDF), banners, company-page art.
argument-hint: "[what the post/carousel/banner is about] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-social-linkedin

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

| Format | Size | `--category` | Notes |
|---|---|---|---|
| Link/landscape post image | 1200×627 | `social` | the feed default for a link-style post |
| Portrait post image | 1080×1350 | `social` | more feed height; use when the piece is type-led |
| Document-carousel page | 1080×1350 | `carousel` | 6–10 pages; ships as ONE PDF |
| Profile banner | 1584×396 | `social` | the profile photo covers the bottom-left |
| Company page cover | 1128×191 | `social` | very short — a lockup and one line, nothing else |

- Document carousels are read SMALL in the feed: headline-first pages, one idea
  per page, body type no smaller than ~34px at 1080 wide.
- Profile banner: keep the bottom-left quiet, place content center/right (the
  right two-thirds), copy limited to a name/role plus at most one short line.
- Carousel page bottom-center ~60px is overlapped by LinkedIn's own chrome.

## Recipe — document carousel (the signature move)

**A LinkedIn carousel is a document — ONE multi-page PDF, never a zip of
images.** The description promises it; the export step is where it is kept.

1. `moda canvas create --name "[Topic] — LinkedIn doc" --intent "[brief]" --size 1080x1350 --category carousel --brand [KIT]` — send the link immediately.
2. Lock the system first: 2–4 colors, exactly two fonts, one grid, one motif.
3. Author page 1 ALONE — the hook, 5–9 words, no logo: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]`; `moda canvas screenshot [CANVAS_REF]`; fix until it proves the look.
4. `moda canvas add-pages [CANVAS_REF] --count [N-1]`, then one markup apply per page — serial on one canvas. Last page carries the one ask and the brand.
5. `moda canvas screenshot [CANVAS_REF]` in ≤3-page batches; judge as a set.
6. `moda export [CANVAS_REF] --format pdf -o [topic]-linkedin.pdf` — one multi-page PDF. Read `warnings[]` and relay `pdf_links_flattened` honestly (LinkedIn consumes the pages as images anyway).

## Recipe — single post image, banner, or company art

1. `moda canvas create --name "[Topic] — LinkedIn" --intent "[brief]" --size [WxH from the table] --category social --brand [KIT]` — link immediately.
2. Person-first when a name is given (the name is the hero lockup, the company
   supports); company-led only on request: logo + one value prop, no headshots.
3. Author in one apply: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]`.
4. `moda canvas screenshot [CANVAS_REF]` — check the bottom-left avatar zone on a
   banner, contrast and type floor everywhere; fix and re-screenshot.
5. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [topic]-linkedin.png`.

## Examples

- "a LinkedIn carousel about our launch" → document-carousel recipe → ONE PDF.
- "a post image for this announcement" → single recipe at 1200×627.
- "refresh my LinkedIn banner" → single recipe at 1584×396, content center/right.
- "company page cover for [Company]" → single recipe at 1128×191, lockup only.
- "a 10-page LinkedIn doc on [Topic]" → carousel recipe, 10 pages, one PDF.

## Errors

Any typed error → load moda-core and read its recovery reference.
The trap here is exporting a carousel as a zip: png/jpeg multi-page arrives as a
zip, so carousels export `--format pdf`. `stale_revision` heals — retry once.

## Make it recurring

A weekly thought-leadership carousel → moda-automate runs the schedule (the
artifact still routes here); the winning page system → moda-templates.

See also: moda-social — other platforms, ad sets, carousel theory ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/linkedin.md | depth: document-post conventions, banner lockups, feed legibility |
| references/markup.md | before any markup apply |
| references/export.md | PDF vs zip, warnings, pixel ratio |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
