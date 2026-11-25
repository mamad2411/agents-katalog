---
name: render-incident-report-image
description: Render a verbose monospace "incident report" PNG tuned for reading on an iPhone 13 mini in a Pushover notification (72-column wrap, dark theme, green headings, no horizontal cut-off, unlimited scrollable height). Use when the user wants a detailed text briefing/report rendered as an image to attach to a push notification, or asks for a Pushover-friendly report image. TRIGGERS - render report, incident report image, pushover briefing image, report png.
---

# render-incident-report-image

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Render a clean monospace report PNG via the TS core `pushover_core.ts render` (Satori → vector SVG → @resvg/resvg-js → PNG).

## Device-calibrated facts (verified on a physical iPhone 13 mini, 2026-05-30)

- **72-column hard wrap** is comfortably legible inline without pinch-zoom (40/56/72 all tested; 72 confirmed fine).
- Pushover **fits images to width** — it never crops horizontally. Earlier "right-edge trimmed" images were a _renderer_ bug (no wrapping), not Pushover.
- **No practical pixel-height ceiling**: a 30,000 px-tall image scrolls/zooms fine, far under the **5 MB** attachment cap → render the whole report in one tall image, never paginate.
- **Auto-fit width (2026-06-01)**: 72 cols is the **MAX wrap**, not a fixed canvas width. The canvas is sized to the _longest actual line_ (`maxChars × 18px advance + 48px pad`, monospace ⇒ exact/deterministic), so short reports don't waste right-margin whitespace — Pushover scales the snug image up, rendering text larger. (e.g. a 43-char digest: 1344 → 822 px, ~1.6× bigger on screen.) No image post-processing needed.

## Usage

```bash
env -u HTTPS_PROXY -u HTTP_PROXY bun "$(cc-plugin-root pushover-commander)/skills/_lib/pushover_core.ts" render \
  --in report.txt --out /tmp/report.png            # or: cat report.txt | bun .../pushover_core.ts render --out /tmp/report.png
# then attach with send-notification --attach /tmp/report.png
```

## Line markup (first 2 chars)

| Prefix | Style              |
| ------ | ------------------ |
| `#`    | heading (green)    |
| `!`    | subheading (amber) |
| `>`    | accent (cyan)      |
| `.`    | dim/muted          |
| (none) | body (light grey)  |

Wrapping is **word-aware** (greedy, `fold -s` semantics): lines break at spaces and
NEVER mid-word. Only a single token that ALONE exceeds the column width (paths,
hashes, URLs) is hard-broken so nothing overflows the canvas. Lines already within
the width keep their exact spacing (aligned tables stay aligned). Greedy is the
correct algorithm for left-aligned monospace — Knuth-Plass optimizes _justified_
paragraphs and adds nothing to ragged-right fixed-width text.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the PNG render with correct word-wrap and no horizontal cut-off at the target device width?** If text overflowed, fix the wrap/width.
2. **Did the Satori to resvg pipeline complete without error?** A blank or partial image means a rendering regression to fix.

Only update if the issue is real and reproducible — not speculative.
