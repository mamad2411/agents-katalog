---
description: Summarize an ad for delivery — what it is, what shipped, which claims it makes, what's still open
argument-hint: [ad slug, empty for the current one]
---

Summarize an ad for handoff. **Read-only** — change nothing, render nothing, fix
nothing. If something needs doing, name it and stop.

Target: **$ARGUMENTS** — if empty, use the ad this conversation has been working
on, or the only folder in `ads/`. Ask if it's ambiguous.

## 1. Gather

From the ad itself, not from memory of the conversation:

- `ad.config.json` — type, brand, formats, duration, fps
- `index.html` / `ad.css` — the on-screen copy and the layout approach
- `out/manifest.json` — what was actually exported, and when
- The campaign brief and `campaign.md` it came from, if it came from one

If `out/` is missing or older than the source, say the export is stale rather
than reporting files that don't reflect the current ad.

## 2. Report

- **What it is** — type, angle, formats, brand, placement
- **The creative** — the headline, the CTA, and the one idea it carries. Quote
  the copy that's actually on screen
- **Files** — what's in `out/`, which formats, rendered when
- **Claims on screen** — every number, price, rating or quote, and where each
  one came from. If something has no source, that's the headline of this report,
  not a footnote
- **Placeholders** — anything visibly fake standing in for proof
- **Open** — what's stale, untested, or assumed. Per-ratio rules for formats not
  in the config are untested by definition; say so

## 3. One honest note

End with the weakest thing about the creative — the hook, the CTA, the fact that
it's carrying placeholder art, a photo that argues against the angle. One
sentence, specific.

A report that reads as uniformly positive is not a report. If the ad is genuinely
solid, say which single element is carrying it and what would break first.
