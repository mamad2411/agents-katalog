---
name: moda-social-ads
description: >-
  Static ads: platform-native single ads and multi-size display banner sets
  (IAB) — one message across sizes, exported together.
argument-hint: "[the offer + where it runs] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-social-ads

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

The IAB core set (`--category web-ads`), plus any size the user names:

| Size | Role | Notes |
|---|---|---|
| 300×250 | medium rectangle | the workhorse — design the MASTER here |
| 728×90 | leaderboard | hostile: one line, logo, CTA — nothing else |
| 160×600 | skyscraper | vertical stack, CTA at the bottom |
| 300×600 | half page | the roomy one; the master usually scales here first |
| 320×50 | mobile banner | hostile: type only, 4–6px off every edge |
| 970×250 | billboard | the only size with room for imagery |

Platform-native single ads (`--category web-ads` or `social`): IG story ad
1080×1920 (bottom reserved from y 1400 for CTA chrome), Facebook feed ad
1200×628, IG feed ad 1080×1080 or 1080×1350.

Craft, in one pass: the Rule of One — one audience, one promise, one ask.
Hierarchy is hook → brand → CTA, with brand and CTA both visible; the CTA is
button-shaped and the highest-contrast element ("See the demo", never "Learn
more"). Keep type and CTA 8–10px off every edge — networks add a border at
serve time. Photography rarely survives these sizes: prefer solid colour,
gradients, shapes, type, and generated patterns.

## Recipe — the size set (master first)

1. `moda canvas create --name "[Campaign] — ads" --intent "[the one promise]" --size 300x250 --category web-ads --brand [KIT]` — send the link immediately.
2. Design and APPROVE the master on page 1: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]`, then `moda canvas screenshot [CANVAS_REF]`. Do not adapt anything until the master is right.
3. `moda canvas add-pages [CANVAS_REF] --count 1 --size 728x90` — one page per size, repeated for each size in the set.
4. Re-COMPOSE each size (never squash): one markup apply per page, serial on the
   one canvas — the same message, re-laid for the shape. Check the two hostile
   sizes (728×90, 320×50) first; they break layouts before the others do.
5. `moda canvas screenshot [CANVAS_REF]` in ≤3-page batches; judge the set for
   one voice, one CTA, one brand presence.
6. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [campaign]-ads.zip`
   — multi-page png arrives as a zip: the set ships together, one file for the
   trafficker.

## Recipe — one platform-native ad

1. `moda canvas create --name "[Campaign] — [placement]" --intent "[the one promise]" --size [WxH] --category web-ads --brand [KIT]` — link immediately.
2. Write the idea in one sentence first: "For [audience], [brand] is the
   [category] that [single claim]." Kill every secondary message.
3. Author in ONE apply; keep the CTA inside the placement's chrome-free zone.
4. `moda canvas screenshot [CANVAS_REF]` — squint test: blurred, does it still
   show what it is for and where the eye lands? Fix, re-screenshot.
5. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [campaign]-[size].png`.

## Examples

- "banner ads in the standard sizes" → size-set recipe, IAB core, one zip.
- "an Instagram ad for the spring sale" → platform-native recipe at 1080×1350.
- "just a 728×90 and a 300×250" → size-set recipe with those two pages only.
- "an animated banner ad" → not this skill: load moda-video (motion wins).

## Errors

Any typed error → load moda-core and read its recovery reference.
`stale_revision` is likeliest here (many pages, many applies): applies to one
canvas stay SERIAL — a parallel batch shares one revision pin and loses.

## Make it recurring

A campaign refresh on a cadence → moda-automate; the approved size-set skeleton
→ moda-templates, so the next campaign starts at step 4.

See also: moda-social — organic posts, carousels, one-off graphics ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/ads.md | depth: IAB set, per-size composition patterns, CTA and stopping power |
| references/markup.md | before any markup apply |
| references/export.md | zip semantics, pixel ratio, warnings |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
