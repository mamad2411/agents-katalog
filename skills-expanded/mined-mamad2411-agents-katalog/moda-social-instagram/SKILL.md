---
name: moda-social-instagram
description: >-
  Instagram creative: feed posts, stories, reel covers, carousels — IG sizes
  and safe areas built in. Stills only; animated → moda-video.
argument-hint: "[what the post/story/carousel is about] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-social-instagram

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
| Feed portrait / carousel slide | 1080×1350 | `carousel` | 4:5 — the IG default; use unless the user says square |
| Feed square | 1080×1080 | `social` | grid-safe; quote cards default here |
| Story / Reel cover | 1080×1920 | `social` | 9:16 vertical |

Safe areas — design full-bleed; only text, logos, CTAs, and focal points must
stay inside:

- Feed/carousel (1080×1350): platform chrome overlays ~60px top, ~50px bottom,
  ~50px top-right — keep essentials in a centered ~960×1200.
- Story/Reel (1080×1920): essentials inside y 250–1670 (username chrome above,
  reply bar below).
- Grid crop: the profile grid shows the center 1:1 — keep the subject of a 4:5
  post inside the middle square.
- Type: body ≈ 45px at 1080w, floor 28px — feed type is read at arm's length;
  cut copy before shrinking below the floor.

## Recipe — single post, story, or quote card

1. `moda canvas create --name "[Topic] — IG" --intent "[one-line brief]" --size 1080x1350 --category social --brand [KIT]` — send the link immediately.
2. Image-led concept? `moda media generate-image --prompt "[hero, in the brand's palette]" --model [MODEL]` for the hero. Type-led is equally strong — state the choice either way.
3. Author the page in ONE apply: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]` (grammar: references/markup.md). Essentials inside the safe area above.
4. `moda canvas screenshot [CANVAS_REF]` — check safe area, type floor, contrast, grid crop; fix and re-screenshot until clean.
5. Deliver: live link + `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [topic]-ig.png`.

## Recipe — carousel (5–8 slides)

1. `moda canvas create --name "[Topic] carousel" --intent "[brief]" --size 1080x1350 --category carousel --brand [KIT]` — link immediately.
2. Lock the system before slide 1: 2–4 colors, exactly two fonts, one grid, one
   repeating motif.
3. Author slide 1 ALONE — the hook: 5–9 words, no logo (branding on slide 1
   reads as an ad). Screenshot and fix until it proves the system.
4. `moda canvas add-pages [CANVAS_REF] --count [N-1]`, then one markup apply per
   slide — vary composition (full-bleed type, number-hero, split, quiet slide,
   pull-quote, photo-led) so adjacent slides never repeat a layout; applies to
   ONE canvas stay serial. The last slide carries the one ask and the brand.
5. Screenshot all pages and judge as a set: brightness spread, motif continuity,
   one stat per slide (oversized numeral, small source footer).
6. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [topic]-carousel.zip`
   — the zip of page images IS the IG carousel deliverable.

## Examples

- "an IG post announcing [Feature]" → single-post recipe, 1080×1350.
- "a quote card from [Person] for Instagram" → single-post recipe, 1080×1080.
- "a 6-slide carousel of [Topic] tips" → carousel recipe.
- "a story for [Event] tomorrow" → single-post recipe at 1080×1920.
- "a poster for Instagram" → this skill at 1080×1350 (platform wins over print
  words; a poster to print is moda-document-print).

## Errors

Any typed error → load moda-core and read its recovery reference.
`invalid_markup`: one page per apply, then re-run; `stale_revision` heals —
re-read and retry once.

## Make it recurring

A series ("every Monday", "tips series") → moda-automate schedules the run;
a winning layout → moda-templates saves it as the team template.

See also: moda-social — formats beyond IG, ad sets, carousel theory ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/instagram.md | more depth: Reels covers, grid strategy, caption handoff |
| references/markup.md | before any markup apply |
| references/design-quality.md | type ladder detail, imagery, shaders, AI-slop list |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
