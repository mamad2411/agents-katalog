---
name: figma-overlay-check
description: Use when verifying UI fidelity against a Figma design — pixel-perfect walkthroughs, checking whether a page matches the mockup, or when the user mentions "overlay comparison", "design diff", "visual QA", "还原度", "叠图比对". For web projects that can run locally (requires Figma MCP and Playwright MCP).
---

# Figma Overlay Fidelity Check

Core idea: export the Figma design as a PNG, then use Playwright's `browser_evaluate` to inject it **at runtime** as a top-level overlay on the page, combined with pixel diffing for quantified results. Because the injection happens at runtime, **you must not (and need not) modify project source code** — a page refresh clears everything.

## Workflow

```
Task Progress:
- [ ] Step 1: Export the design (mind the 4096px limit)
- [ ] Step 2: Align viewport + height sanity check
- [ ] Step 3: Inject overlay (opacity for coarse pass → difference for fine pass)
- [ ] Step 4: Region cropping + DOM measurement to locate and fix diffs
- [ ] Step 5: Quantify with pixel diff
- [ ] Step 6: Cleanup
```

### Step 1: Export the design

Use Figma MCP `download_assets` (defaultFormat: png) to export the target Frame, save it to `/tmp/figma-overlay/design.png`, and record the Frame's **logical width/height** (e.g. 1400×4283).

**Key gotcha: Figma caps exports at 4096px on the long edge.** Long pages get proportionally downscaled on export (e.g. 1400 wide becomes 1339). Use `file` or `sips` to confirm the actual pixel size and compute the scale factor `scale = exported width / logical width` — you'll need it in Step 5. The overlay itself is unaffected (CSS stretches it back to logical width).

### Step 2: Align viewport + height sanity check

Use `browser_resize` to set the viewport width to the design's logical width (viewport mismatch is the most common source of false positives).

One-line sanity check: `document.body.scrollHeight` should be within a few px of the design's logical height. A large gap means module-level spacing/height bugs — fix the structure first before pixel-level comparison.

### Step 3: Inject the overlay

Ways to make the image accessible to the page, in order of preference:

1. **Dev server static directory** (recommended): copy design.png to something like `public/__figma_overlay.png`, inject `src="/__figma_overlay.png"`, delete the file when done
2. **base64 data URL**: fallback when there's no static directory; note very large images may exceed the evaluate argument size limit

Inject with `browser_evaluate` (disabling animations along the way):

```javascript
() => {
  document.getElementById('__figma_overlay__')?.remove();
  const style = document.createElement('style');
  style.textContent = '* { animation: none !important; transition: none !important; }';
  document.head.appendChild(style);
  const img = document.createElement('img');
  img.id = '__figma_overlay__';
  img.src = '/__figma_overlay.png';
  img.style.cssText =
    'position:absolute;top:0;left:0;width:1400px;' + // ← design's logical width
    'z-index:2147483647;pointer-events:none;opacity:0.5;';
  document.body.appendChild(img);
}
```

Two modes:
- `opacity:0.5`: coarse pass for overall misalignment
- `opacity:1; mix-blend-mode:difference`: fine pass. **The blacker, the closer the match**; bright outlines = position/size offsets; bright solid blocks = color mismatch; "ghosted" text = line-height/font-size mismatch

### Step 4: Locate and fix diffs

Full-page screenshots are too large to inspect details, so combine two techniques:

**Region cropping**: use this skill's `scripts/crop.mjs` to crop suspicious regions out of the difference screenshot for a zoomed-in look:

```bash
node <path-to-this-skill>/scripts/crop.mjs diff.png <x> <y> <w> <h> out.png
```

**DOM measurement**: use `browser_evaluate` + `getBoundingClientRect` to measure absolute coordinates of key elements and compare the numbers directly against node coordinates from Figma metadata — much faster at pinpointing root causes than eyeballing the overlay:

```javascript
() => [...document.querySelectorAll('h2,h3')].map((e) => {
  const r = e.getBoundingClientRect();
  return { text: e.textContent.slice(0, 20), top: r.top + scrollY, left: r.left + scrollX, w: r.width, h: r.height };
})
```

After each fix, refresh the page, re-inject the overlay, and re-check. Loop until the difference screenshot is essentially all black.

Note: Playwright MCP's `browser_take_screenshot` with a filename writes to the **user home directory**, not the project directory.

### Step 5: Quantify with pixel diff

Refresh to remove the overlay, take a full-page screenshot, **resample the screenshot to the exported image's width first** (the scale factor from Step 1), then compare:

```bash
cd /tmp/figma-overlay && npm init -y && npm i pixelmatch pngjs   # first time only
sips --resampleWidth 1339 page.png --out page-resized.png        # 1339 = exported image's actual width
node <path-to-this-skill>/scripts/pixel-diff.mjs design.png page-resized.png diff.png
```

Pass criteria: mismatch < 2% and no large highlighted blocks in the diff image. Scattered highlights from text anti-aliasing and photo edges are acceptable noise.

### Step 6: Cleanup

1. Delete the temporary overlay image from `public/`, refresh and confirm the overlay is gone
2. Confirm no overlay-related code exists in source (this skill never writes source code — if any exists, that's a violation)
3. Clean up `/tmp/figma-overlay/` and screenshot files in the home directory

## Frequent Real-World Diff Causes (check these first)

| Symptom | Root cause | Fix |
|---|---|---|
| Ghosted text drifting down line by line | Figma `normal` line-height ≈ 1.2, Tailwind/browser default is 1.5 | Explicit `leading-[Npx]`, N = the Figma text node's height |
| Photo content misaligned, bright blocks | Code uses `object-cover` center-crop while Figma has the image at exact left/top/width/height inside its container | Absolutely position per the image geometry from `get_design_context` + `max-w-none` |
| Buttons/cards a few px too tall | CSS `border` takes up box size, Figma strokes don't | Reduce padding accordingly when adding borders |
| A whole section shifted by tens of px | Extra/missing padding or gap, or a 0-width decorative node in Figma (inset overflow) mistaken for a spacer | Use DOM measurement to check numbers against Figma coordinates one by one |
| Image assets themselves don't match | Local asset is an old export or cropped from a different source | Re-export from Figma; if instance children can't be exported by id, export the parent instance at 2x and crop programmatically |

## Rules

- **Never write overlay code into project source** (components, layouts, global styles — none of it); always inject at runtime
- Only compare a single page-level Frame, never the whole canvas
- For long pages, anchor the overlay with `position:absolute` to the top of the document so it scrolls with the page
