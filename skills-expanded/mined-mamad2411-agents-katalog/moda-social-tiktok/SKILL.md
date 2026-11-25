---
name: moda-social-tiktok
description: >-
  TikTok stills: video covers and photo-mode posts — 9:16 sizing and safe
  areas.
argument-hint: "[what the cover/photo post is about] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-social-tiktok

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
| Cover frame / photo-mode page | 1080×1920 | `social` | 9:16 — everything on TikTok is this size |
| Photo-mode set | 1080×1920 × N | `carousel` | one page per photo; ships as a zip of pngs |

Safe areas — design full-bleed; only text, logos, CTAs, and focal points stay
inside:

- **Post**: UI covers top y 0–190, the right icon rail x 900–1080 (y 190–1780),
  and the caption band y 1780–1920. Safe zone **x 120–840, y 252–1742**.
- **Ad**: extra CTA chrome — bottom reserved from y 1400. Safe zone **x 120–840,
  y 252–1280**. Assume a normal post unless the user says ad.
- Cover frames are also shown as a small grid tile on the profile: the subject
  and any title must survive at ~1/6 scale.
- Type: body ≈ 48px at 1080 wide, floor 32px — vertical video is read in motion.

This skill owns the STILL: the cover frame and photo-mode pages. An actual
TikTok video is moda-video (render format wins over platform).

## Recipe — cover frame or single photo-mode page

1. `moda canvas create --name "[Topic] — TikTok" --intent "[one-line brief]" --size 1080x1920 --category social --brand [KIT]` — send the link immediately.
2. Image-led? `moda media generate-image --prompt "[subject, brand palette]" --model [MODEL]` for the backdrop; type-led is equally strong.
3. Author in ONE apply: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]` — title inside x 120–840, y 252–1742 (references/markup.md).
4. `moda canvas screenshot [CANVAS_REF]` — check the right rail and caption band are clear, then judge the title at tile scale; fix and re-screenshot.
5. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [topic]-tiktok.png`.

## Recipe — photo-mode set

1. `moda canvas create --name "[Topic] — photo set" --size 1080x1920 --category carousel --brand [KIT]` — link immediately.
2. Prove page 1 alone (author → screenshot → fix) before adding pages: it sets
   the system every later page repeats — 2–4 colors, two fonts, one motif.
3. `moda canvas add-pages [CANVAS_REF] --count [N-1]`, then one markup apply per
   page, serial on the one canvas; vary composition so neighbours differ.
4. `moda canvas screenshot [CANVAS_REF]` in ≤3-page batches; judge as a set.
5. `moda export [CANVAS_REF] --format png --pixel-ratio 2 -o [topic]-tiktok.zip`
   — the zip of page images IS the photo-mode deliverable.

## Examples

- "a cover for our new TikTok" → cover recipe at 1080×1920.
- "a 5-photo TikTok post about [Topic]" → photo-mode set, 5 pages, zip.
- "a TikTok ad still" → cover recipe with the ad safe zone (bottom clear from y 1400).
- "make the TikTok video itself" → not this skill: load moda-video.

## Errors

Any typed error → load moda-core and read its recovery reference.
Most likely here: text drifting under the right rail — re-screenshot after every
fix. `stale_revision` heals — re-read and retry once.

## Make it recurring

A cover-frame series on a posting cadence → moda-automate; the proven cover
layout → moda-templates, so every upload starts from the winner.

See also: moda-social — other platforms, carousel theory, one-off graphics ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/tiktok.md | depth: safe-area map, cover-vs-photo craft, tile-scale legibility |
| references/markup.md | before any markup apply |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
