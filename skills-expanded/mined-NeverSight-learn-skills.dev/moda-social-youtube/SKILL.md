---
name: moda-social-youtube
description: >-
  YouTube art: thumbnails (readable at 320px) and channel banners.
argument-hint: "[what the thumbnail/banner is for] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-social-youtube

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
| Thumbnail | 1280×720 | `social` | judged at ~320px wide — that is the real brief |
| Channel banner | 2560×1440 | `social` | only 1546×423 centred is visible on every device |

- **Thumbnail rules, not preferences**: ≤4 words of on-image text; the subject
  or face fills a third of the frame; one high-contrast focal point; type ≥120px
  at 1280 wide so it survives the shrink. No thin weights, no full sentences.
- **Banner safe core**: everything that must be seen — name, tagline, upload
  cadence, logo — lives inside the centred 1546×423. Decoration extends outward
  into the 2560×1440 field, which desktop shows and phones crop away.

## Recipe — thumbnail

1. `moda canvas create --name "[Episode] — thumb" --intent "[one-line brief]" --size 1280x720 --category social --brand [KIT]` — send the link immediately.
2. Subject first: a photo the user gave you (`moda file upload [photo.jpg]`) or `moda media generate-image --prompt "[subject, high contrast, brand palette]" --model [MODEL]`.
3. Author in ONE apply: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]` — ≤4 words, type ≥120px, one focal point (references/markup.md).
4. **The 320px check** (this recipe's verify twist): `moda canvas screenshot [CANVAS_REF] -o thumb.png`, then judge it at thumbnail scale — a thumbnail that only reads full-size is a failed thumbnail. Fix and re-screenshot.
5. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [episode]-thumb.png`.

## Recipe — channel banner

1. `moda canvas create --name "[Channel] — banner" --intent "[brief]" --size 2560x1440 --category social --brand [KIT]` — link immediately.
2. Author the safe core FIRST — the centred 1546×423 — then extend background,
   texture, and colour outward to the full frame in the same apply.
3. `moda canvas screenshot [CANVAS_REF]`; check that cropping to the core loses
   nothing that carries meaning; fix and re-screenshot.
4. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [channel]-banner.png`.

## Examples

- "a thumbnail for this episode" → thumbnail recipe, judged at 320px.
- "thumbnails for these 3 videos" → run the thumbnail recipe per video, one
  canvas each; the winning layout goes to moda-templates.
- "refresh our channel art" → banner recipe, everything meaningful in the core.
- "a YouTube banner AD" → not channel art: moda-social-ads owns paid formats.

## Errors

Any typed error → load moda-core and read its recovery reference.
Most likely here: type that passes full-size and dies at 320px — shrink the
screenshot before delivering. `stale_revision` heals — retry once.

## Make it recurring

Template-ize the winning thumbnail via moda-templates, then moda-automate the
per-video instance — a thumbnail system beats a thumbnail.

See also: moda-social — other platforms, ad sets, one-off graphics ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/youtube.md | depth: thumbnail composition patterns, banner device crops |
| references/markup.md | before any markup apply |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
