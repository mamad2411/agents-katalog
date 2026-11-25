---
name: image
description: >
  Recreate a single flat image as one self-contained HTML page, verified by
  rendering it and comparing to the image — no capture, no DOM, no HTML input.
  Use when the user hands you just a picture (a screenshot, a poster, an
  Instagram/carousel slide, a graphic, a UI mock) and wants it rebuilt, cloned,
  copied or "made into HTML" — "clone this image", "copy this poster", "turn
  this screenshot into a page", "recreate this" — with nothing but the image to
  work from. This is the right skill precisely when there is no capture session
  (no pages.json, no source.html, no computed.json). If a real capture session
  exists, prefer clone:html or clone:react instead — they measure per-box
  against the DOM, which this cannot. Best on flat, mostly-typographic graphics;
  photographs and complex illustrations inside the image become placeholders.
---

# clone:image — one picture → one verified HTML page

**In:** a single image file (whatever the user attached).
**Out:** `apps/<name>/index.html`, a self-contained page that renders to look
like the image, checked by rendering it at the image's exact pixel size and
comparing the two pictures.

There is no DOM here and no per-box oracle. The entire check is _does my render
look like the picture_ — a whole-image compare you read with your own eyes and
iterate against. That is enough for flat graphics, which is what this is for.

## Setup

```
mkdir -p apps/<name>
cp <the image> apps/<name>/ref.png
```

Read `ref.png` and note its pixel size (also `python3 -c "from PIL import Image;
print(Image.open('apps/<name>/ref.png').size)"`). That size **is** your canvas.

## Author `apps/<name>/index.html`

**Start from the template** — copy `template.html` (next to this file) to
`apps/<name>/index.html` and set `--w` / `--h` to the image's pixel size. It is
one self-contained file (inline `<style>`, no external requests, no build) whose
job is a **fixed design canvas that fits any screen**: you author at exact pixels
inside `.stage`, and a five-line script scales the stage to fit whatever viewport
it is opened in — a phone, a laptop, a 4K monitor — with no scrollbar. `render.py`
sets the viewport to the canvas size, so the render is always at scale 1 and stays
pixel-exact; the scaling only ever kicks in for a humqan viewer. Do not size the
`body` or drop the wrapper — a raw fixed-px body overflows every screen smaller
than the image, which is the whole thing this avoids.

- **Author inside `.stage`, in px.** Everything is `position:absolute` (or flow)
  in CSS px equal to the image's pixels. `.stage` is already the exact canvas.
- **Rebuild, don't slice.** Text is text, boxes are `div`s, highlights are
  background colours, gradients are CSS gradients. Never embed a crop of `ref.png`
  as an `<img>` — if the render only matches because it _contains_ the reference,
  you have cloned nothing.
- **Measure the geometry, don't guess it.** Eyeballing positions is how a clone
  ends up subtly wrong everywhere. Read the pixels: a coloured block's exact
  rect, a rule's y and width, the background colour — a few lines of PIL over
  `ref.png` gives you real numbers to author against. On the confidence poster,
  scanning for bright-yellow rows gave every highlight box to the pixel; that is
  the difference between "roughly there" and right.
- **Fonts: identify by side-by-side, and webfonts DO load here.** Do not settle
  for a generic stack — a wrong font makes every letter width wrong and the whole
  thing reads off. Crop the reference word, render 4–6 candidates at matched
  size, screenshot, and _look_: is it a slab serif (flat serifs — Bitter, Roboto
  Slab), an old-style serif (pointed, some contrast — Noto Serif), a grotesque?
  Pick the match, load it with a Google Fonts `<link>` (they load in this headless
  renderer — verified), and weight it to match (these graphics run heavy, 700–900).
  Fall back to a system stack only when nothing fits.
- **Rebuild texture in CSS too.** Paper grain, noise, a gradient wash — an SVG
  `feTurbulence` data-URI background is real texture, not a slice of the reference.
  A flat fill where the original has grain is a visible miss.
- **What CSS genuinely can't rebuild is the ONE exception.** A photograph or a
  detailed illustration (the man at the podium, a product photo) is not
  reconstructable. If it sits on the page background (no frame), just leave the
  background showing through and say the illustration is omitted — a grey slab is
  its own wrong. If it has a distinct frame/fill, a neutral block in its dominant
  colour is fine. Either way, do not grind the loop trying to converge on it.

## The loop

```
python3 .claude/skills/clone/skills/image/render.py apps/<name>
```

It writes `render.png`, `sbs.png` (reference | render), `diff.png` (where they
disagree lights up) and prints one `match %`.

**The `match %` is NOT a pass gate — your eyes on `sbs.png` are.** It is a whole-
image pixel diff, so it rewards a flat wrong fill that happens to average out and
punishes _correct_ texture that can't align pixel-for-pixel: adding real paper
grain to the confidence poster dropped it from 53% to 26% while the clone got
better. A high number can hide a wrong font; a low one can sit under a faithful
clone. Use it only as a regression tripwire between two edits (did this help or
hurt), never as "done".

1. **Read `overlay.png` first, then `sbs.png`.** The overlay is a 50% blend, so
   anything off in position or size **ghosts** (doubles) — a side-by-side hides
   exactly that. Ghosting that drifts left-to-right along a line means the text
   is the wrong width (size or letter-spacing); a uniform double means it is
   shifted. Name the biggest discrepancy from the overlay.
2. **For text, measure both ink boxes and correct — don't nudge blind.** A few
   lines of PIL give the black-text bounding box in `ref.png` and in
   `render.png`; the deltas (dLeft, dTop, dWidth) are the exact edit: dWidth
   drives font-size (or letter-spacing when the height already matches), dTop the
   `top`, dLeft the `left`. This converges a headline to ~2px in two cycles
   instead of ten blind ones. Decouple the pieces — draw the measured highlight
   rectangle as its own div and position the word over it — so you can move the
   text without the box shifting.
3. **Fix one thing with `Edit`, re-render, re-read the overlay.** Repeat until
   the overlay stops ghosting — not until a number crosses a threshold. Residual
   ghosting that is only a faint outline is the substitute font's letterforms,
   not a geometry error; that is your floor unless you find a closer font.

Stop when the only differences left are the placeholders (photos/illustrations)
and sub-pixel noise. Report the final `match %`, the match by eye, and every box
you placed as a placeholder with the reason.

## Not this skill

- A **capture session** (pages.json + DOM) → `clone:html` / `clone:react`; they
  measure per box, which is strictly better when the DOM exists.
- **Behaviour** (hover, focus, keyboard, a live component) isn't in a flat image
  and can't be cloned from one — capture it and use `clone:react`.
