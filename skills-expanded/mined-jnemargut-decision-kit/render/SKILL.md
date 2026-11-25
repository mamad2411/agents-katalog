---
name: render
description: Render a local HTML or SVG file to a PNG and look at it. Use before showing the user any HTML artifact, decision page, mockup, report, chart, or SVG asset — and whenever a layout, chart, or visual needs checking rather than assuming it worked.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *), Read
---

# Look at it before they do

You cannot see HTML by reading it. Source is not pixels. Render it, Read the PNG, then decide.

```
${CLAUDE_SKILL_DIR}/scripts/render.sh <file.html|file.svg> [out.png]
```

Flags: `--full` (whole page), `--mobile` (390px), `--width N`, `--height N`, `--check`.
It prints the PNG path. **Then Read that path** — you read images natively, so this closes the loop.

## When to run it

Before `open`-ing anything, and before telling the user an artifact is ready. Also any time you've
written a chart, meter, grid, or diagram by hand — those are where silent breakage lives.

## Which renderer you get

The script picks the first that works and tells you when it had to compromise.

| Available | What happens |
|---|---|
| **playwright** | Preferred. Honours any viewport width, real full-page capture. |
| **Chrome/Chromium/Edge/Brave only** | Works at 1400px and any width **≥ 500px**. Below that see the warning below. |
| **Neither** | Exits non-zero and says so. Read the CSS and markup carefully instead — do not silently skip the check, and never claim an artifact looks right if you never saw it. |

**The 500px floor.** Headless Chrome silently clamps its viewport to a 500px minimum, in both
`--headless` and `--headless=new`. With Chrome only, `--mobile` therefore renders at 500px, not 390,
and the script says so on stderr. **Do not read the result as a responsive bug.** Confirm any
suspected overflow with `--check`, which compares `clientWidth` against `scrollWidth` — if they are
equal there is nothing to fix. For genuine narrow-viewport work:
`pip install playwright && playwright install chromium`.

`--check` itself needs Chrome (it uses `--dump-dom`), and says so if Chrome is missing.

## What to check

Binary questions, not ratings. "Is X true" is signal; "rate this 1–10" is noise.

1. **Did every element actually paint?** Bars, meters, fills, charts, borders, backgrounds. An
   element that computes to zero height renders as nothing and reads as "clean design."
2. **Is anything clipped, overlapping, or overflowing** its container?
3. **Do sibling cards or columns align**, or does one have a dead zone of whitespace?
4. **Is text legible** at real size — contrast, and nothing truncated mid-word?
5. **Did images and fonts load**, or are there broken boxes and fallback serif?
6. **Does it look finished**, or does it look like a first draft you'd be embarrassed to send?

Fix what fails, re-render, look again. Two or three passes converges; guessing does not.

## The bug class this exists to catch

A real one, found across five shipped pages: progress bars marked up as
`<span class="track"><span class="fill" style="width:82%"></span></span>` with CSS
`.fill { height: 100% }`. Spans are inline boxes — `height` does nothing on them, so every bar
rendered as an empty grey track. The page looked fine. The data was invisible.

**`display: block` on the fill fixed all fifty.**

The lesson generalises: percentage heights, flex children, absolutely positioned overlays and
grid alignment all fail *quietly*. Reading the CSS would not have caught it. Looking did.
