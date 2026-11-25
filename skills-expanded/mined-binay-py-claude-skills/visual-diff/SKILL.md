---
name: visual-diff
description: Before/after visual regression for websites. Screenshots pages at desktop (1366 wide) and mobile (390x844) in a headless Chromium with animations frozen, then compares two sets pixel by pixel and writes an HTML report with before/after/diff images, % of pixels changed and boxes around the changed regions; exits 1 when a page changes more than a threshold. Use before and after a CSS refactor, dependency upgrade, redesign or deploy to catch unintended layout or style changes, or when asked "did my change break how anything looks?". Pairs with site-qa.
---

# visual-diff

`scripts/visual-diff.mjs` is zero-dependency Node 22+. It starts its own headless Chrome / Edge / Brave / Chromium with a temporary profile (never the user's browser or logins) and closes it when done. Set `BROWSER=/path/to/chrome` if none is found. PNG decoding and diffing are done in plain Node, so there is nothing to install.

```
# 1. baseline before the change
node visual-diff.mjs capture https://example.com /pricing /about --out vd/before --full
# 2. after the change (same flags)
node visual-diff.mjs capture https://example.com /pricing /about --out vd/after --full
# 3. compare
node visual-diff.mjs compare vd/before vd/after --out vd/report        # exit 1 if any page > 0.5 %

# or in one step: first run creates the baseline, later runs capture to vd/runs/<time>/ and compare
node visual-diff.mjs run http://localhost:5173 /pricing --baseline vd/baseline --full
```

Capture options:
- `--full` full-page screenshot (page is scrolled first so lazy images load; capped at 16000 px tall). Without it, only the first screen.
- `--hide ".clock, .ad-slot, canvas"` hides dynamic regions (`visibility:hidden`, so layout does not move).
- `--wait 1500` extra ms after the page is quiet (default 500). `--viewports desktop` or `mobile` to do only one.
- Paths like `/about` resolve against the first URL. In Git Bash, `/about` is rewritten by MSYS; the script undoes that (a one-letter path like `/p` comes back as `/p/`), or write `about` without the slash.

Compare options: `--threshold 0.5` (% of pixels, per screenshot) and `--tolerance 16` (per-channel 0-255 difference ignored, to skip antialiasing noise).

What it does to make two runs comparable: emulates `prefers-reduced-motion: reduce`, injects `*{animation:none;transition:none;caret-color:transparent}`, waits for network quiet, `document.fonts.ready` and every `<img>` to load and decode, pauses videos at 0, blurs the focused element, scrolls to the top.

## Outputs
- capture dir: `<page>__desktop.png`, `<page>__mobile.png` (mobile is 2x, so 780 px wide), `manifest.json` (url, viewport, size, HTTP status). Pages are matched between runs by name + viewport.
- report dir: `index.html` (summary table, then before / after / diff side by side, most-changed first), `report.json`, `<page>__<viewport>__diff.png`.
- Terminal: one line per screenshot with % changed, region count, largest region and size change.

## Reading the results
- Open `index.html` and LOOK at the diff column. Magenta = changed pixels on a faded copy of the new screenshot, orange boxes = changed regions. Box coordinates are screenshot pixels (mobile is 2x CSS pixels).
- A small change that stays in place (a button color) gives a small % and one tight box. In testing, a button color change was 0.43 % desktop / 1.42 % mobile with a box exactly around the button.
- If something changes height, everything below it moves, so the whole lower page turns magenta and the screenshot height changes ("size 1366x1021 -> 1366x1101"). Look at the topmost box: that is where the shift starts.
- `ok (small change, under threshold)` means some pixels changed but less than `--threshold`. Still glance at it.
- `MISSING in current` fails the run. `new (no baseline)` does not.
- When a change is intended, make the current capture the new baseline (copy the folder over the baseline).

## Limits
- Only CSS animations are frozen. JavaScript-driven motion (WebGL/three.js canvases, scroll-reveal effects, typing effects, carousels, random content) can still differ between runs. Hide those regions with `--hide`. On https://binay.codes (three.js page) two unchanged full-page runs differed by 0.01 % desktop / 0.03 % mobile; with `--hide canvas` mobile was 0.00 % and the leftover 0.11 % desktop was a JS scroll-reveal.
- Comparing captures made with different flags (`--full` vs not, different `--hide`) prints a warning; the result is not meaningful.
- Screenshots from different machines or browser versions differ in font rendering. Take baseline and current on the same machine.
- It does not log in, click, or fill forms. Pages behind auth or reached through interaction are not covered.
- Pixel diff, not perceptual: a 1 px layout shift near the top can produce a large % even if the page looks the same.
