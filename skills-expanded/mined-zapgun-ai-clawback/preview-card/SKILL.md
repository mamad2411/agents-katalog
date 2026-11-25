---
name: preview_card
description: Compose a finished run's social SHARE CARD (the chart background + dark scrim + hero headline) and rasterize it to PNG so it can be eyeballed without opening the report GUI in a browser. Use it to check the thing the GUI's client-side PNG actually ships — most importantly, whether the chart lines survive the translucent scrim (a scrim dark enough for the light headline can crush the dark chart lines below the WCAG 1.4.11 3:1 floor, which renders as a near-blank card). Reads a run's summary.json + charts/tokens_saved.bg.svg; writes charts/share_card.svg (always) and charts/share_card.png (best-effort raster).
---

# clawback share-card preview

Run `.skills/scripts/preview_card.sh` from the project root. It composes the exact card
the report GUI would let a user download/post for a run, so you can SEE it
without driving the browser.

```bash
.skills/scripts/preview_card.sh runs/<run>            # -> charts/share_card.{svg,png}
.skills/scripts/preview_card.sh runs/<run> --out /tmp # write the pair elsewhere
```

## What it does

1. `benchmark/bin/preview_card.js --in <run>` reads `summary.json`
   (→ `deriveHeroModel`, the same hero logic the GUI uses) and the bare chart
   `charts/tokens_saved.bg.svg`, encodes the chart as a `data:` URL exactly as
   the GUI does, and writes the composed **`charts/share_card.svg`**
   (chart background → translucent dark scrim → hero headline/sub/tagline).
2. The wrapper then rasterizes that SVG to **`charts/share_card.png`**,
   preferring headless Google Chrome (true 1200×630, renders the nested chart),
   falling back to macOS `qlmanage` Quick Look (offline, but pads to a square —
   the card is the **top 630px**; the white strip below is padding). If neither
   is present it leaves just the SVG with a note to open it in a browser.

## Why SVG, then a best-effort PNG

The shipped share PNG is rasterized **browser-side** from this same SVG
(`share_card.js` `svgToPngBlob`, via canvas). Adding a Node rasterizer would
pull a native dependency the product avoids — so the SVG is the source of truth
and the PNG here is only a convenience for eyeballing. If the lines are crushed
under the scrim in this SVG, they are crushed in the shipped PNG too.

## What to look for

- **Chart lines read?** The two cumulative lines + the shaded wedge should be
  visible behind the headline — that is the whole point of the chart bg. If they
  vanish into the scrim, the scrim is too dark for the line colours (WCAG
  1.4.11 wants ≥3:1 for graphical objects); the fix lives in `share_card.js`
  (`shareCardSvg`) and/or the bare line colours in `benchmark/bin/plot.js`.
- **Headline + sub read?** The percentage, the token sub-line, and the tagline
  must stay legible (≥3:1 large text) — a scrim light enough for the lines can
  in turn wash these out. Both constraints have to hold at once.

## Not shipped

`benchmark/`, `scripts/`, and `.skills/` are dev tooling — none ship in the npm
tarball (`package.json` `files`: `bin, src, README.md, LICENSE`).
