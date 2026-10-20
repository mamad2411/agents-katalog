---
description: Check a rendered ad is technically correct — every format, safe zones, fonts, claims. Reports, doesn't fix
argument-hint: [ad slug, empty for the current one]
---

Verify an ad renders correctly. **Report what's wrong; don't fix it** — that's
`/adjust`. Don't grade the design either; that's `/critique`.

Target: **$ARGUMENTS** — if empty, use the ad this conversation has been working
on, or the only folder in `ads/`. Ask if it's ambiguous.

## 1. Get current pixels

Source edited by hand is the normal case here, so `out/` is usually stale.
**Re-render unless you know the output is current** — verifying last week's PNG
proves nothing. Follow `/render`, including its stale-`brand.css` check.

For motion, don't sit through a full encode to check a layout:

```bash
node .claude/skills/critique-ad/scripts/frames.mjs ads/<slug> --at 0,4,8 --thumb
```

## 2. Look at every format

`Read` each exported PNG — **every format in `ad.config.json`, not just the
first.** The whole point of this project's layout rules is that one source
survives several ratios, and the failure always shows up in the one you skipped.

## 3. Technical checklist

Run against the image, not the source:

| | Fails when |
|---|---|
| **Every format exported** | `out/` is missing one listed in `ad.config.json` |
| **Safe zones** | Content sits under platform chrome. Judge from the render — `.ad-safe` being in the markup proves nothing |
| **Ratio integrity** | A layout tuned at one ratio grew a dead band or overflowed at another |
| **Type didn't reflow badly** | Headline over 3 lines, a line breaking to one orphan word, text clipped by a container |
| **Fonts loaded** | Glyphs are the fallback face — check shapes against the brand's display font, not just that text is present |
| **Images loaded** | A photo is missing, stretched, or cropped through its subject |
| **Contrast** | Muted or scrimmed text illegible on its actual ground |
| **Claims** | Every number, price, rating or quote on screen traces to the brief, the brand file, or the product. Anything else is a defect, not a detail |
| **Motion** | Frame 0 is a legible ad; no frozen `<video>`; the last frame rests on CTA and brand |
| **Determinism** | Nothing in the timeline reads `Math.random()`, `Date.now()`, or rAF state |

## 4. Verdict

Lead with **pass / issues found**, then the issues ranked by cost, each with the
format it appears in and what you saw:

```
9x16 — headline overflows .ad-safe by ~30px at the bottom; the CTA sits under
the Reels chrome band. 1x1 is clean.
```

Where a fault is in shared behaviour rather than this ad — a `runtime/` rule
losing a specificity fight — say so, because the fix belongs in `runtime/` and
affects every ad.

Then offer `/adjust` to fix, or `/critique` if the ad is technically sound and
the open question is whether it's any good.
