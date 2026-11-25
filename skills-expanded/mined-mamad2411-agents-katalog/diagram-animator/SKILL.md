---
name: diagram-animator
description: Turn a static diagram into an animated, step-through walkthrough — a self-contained HTML file where each numbered step draws its arrow, highlights the components involved, dims everything else, and narrates what is happening, with play/pause and step navigation. Also exports GIF, MP4, and per-step PNG stills. Use this whenever the user wants a diagram animated, brought to life, made interactive, walked through, or explained step by step; whenever they share an architecture, flow, sequence, network, pipeline, or process diagram (SVG, Mermaid, Graphviz/DOT, or PNG) and want to show how it works rather than just how it looks; and whenever they ask for an animated version of a diagram for a deck, demo, doc, README, or Slack. Trigger on "animate this diagram", "can you make this move", "step through this architecture", "animated version of this flow", "show the request path", or a diagram plus any mention of walkthrough, explainer, or narration.
---

# Diagram Animator

Static architecture diagrams show *what exists*. They are bad at showing *what
happens*, because every arrow is drawn simultaneously and the reader has no idea
where to start. This skill converts a diagram into a sequenced walkthrough: one
step at a time, the relevant arrow draws itself, the components involved light
up, everything else recedes, and a caption explains the mechanism.

The output is a single self-contained HTML file. No build step for the viewer, no
external requests, works offline, survives being emailed. Optional GIF / MP4 /
PNG exports come from the same source.

## The pipeline

```
source diagram ──▶ layered SVG ──▶ steps.json ──▶ build.py ──▶ flow.html
                       │                                          │
                  (the real work)                        export_frames.js
                                                                  │
                                                     gif · mp4 · per-step stills
```

The engine (`assets/engine.js`) is already written and general. Do not rewrite
it per diagram — the per-diagram work is grouping the SVG and authoring the
steps. That split is what keeps this cheap to run repeatedly.

## Workflow

### 1. Get a vector source

Ask for the SVG before settling for a raster. Most diagrams that arrive as a PNG
were exported from something, and the quality gap is large enough that one
round-trip is worth it. If the chat uploader rejects a `.svg` attachment as an
unprocessable image, suggest renaming it to `.svg.txt`, connecting the containing
folder, or pasting the source inline.

For Mermaid, Graphviz, or a raster fallback, read `references/inputs.md` — it
covers rendering to SVG and mapping the generated ids onto the scheme below.

### 2. Restructure the SVG into layers

Read `references/grouping.md` before doing this. The essential rule: every
independently dimmable unit becomes its own `<g class="layer" id="...">`, and
those groups are **flat siblings**, never nested — nesting multiplies opacity, so
a highlighted box inside a dimmed panel can never brighten.

Flows get `id="f1".."fN"` on the group and `id="p1".."pN"` on the geometry inside.
The number circle and its digit go in a `<g class="badge">`.

Geometry is never modified. The animation is purely additive, so the static
diagram still renders identically.

Verify before moving on:

```bash
python scripts/check_layers.py diagram.svg
```

It catches nested layers, ungrouped elements that will never dim, duplicate ids,
and flows missing their geometry — all of which are invisible until you watch the
result and something looks broken.

### 3. Author the steps

Write `steps.json` per `references/steps-schema.md`. Each step names the flow,
the layers to keep bright, an accent color matching that arrow, a short tag, a
title, and a caption.

The captions are the deliverable. The animation is a delivery mechanism for an
explanation — if the caption only restates the arrow's own label, the whole thing
is decoration. Read the diagram closely enough to say what actually happens at
each hop: the protocol, the claim being checked, the component doing the work,
what would break without it. Where the diagram states a design property
("no standing privileges", "unchanged from reference arch"), work out which step
earns it and say so there.

Two things to get right, because they are the most common mistakes:

- **Focus the containing panel alongside an inner box.** Highlighting `g-oauth`
  without `g-vault-shell` leaves a bright box floating on an invisible panel.
- **Match each step's `color` to its arrow's stroke.** The engine paints five
  things from that one value; a mismatch shows up everywhere at once.

### 4. Build

```bash
python scripts/build.py \
  --svg diagram.svg --steps steps.json --out flow.html \
  --title "..." --footer "..."
```

Options: `--theme light`, `--theme-file brand.css`, `--no-chrome` (autoplay-only,
for screen recording or embedding), `--scrub` (timeline slider), `--strict`.
See `references/theming.md`.

### 5. Verify in a browser — always

An animation that throws on step 4 looks fine in step 1. Load it headless, check
for console errors, and screenshot a few steps to confirm the dimming and
highlighting land where intended:

```bash
node scripts/export_frames.js flow.html out/ --stills
```

Then actually look at the stills. Check that focused regions read clearly against
the dimmed background, that no element stayed bright because it was left out of a
layer, and that captions fit their box without overflowing.

### 6. Deliver

Send `flow.html` with `SendUserFile`. A step-through diagram is something people
reopen and share, so also persist it with `create_artifact` when a desktop is
connected.

If the user wants stills, a GIF, or an MP4 — for a deck, a README, or Slack,
where HTML will not embed — see **Exports** below.

## Exports

`scripts/export_frames.js` drives the built HTML through its own timeline and
screenshots deterministically. This works because `engine.js` models the entire
animation as a pure function of a scalar time value, so seeking to *t* always
produces the identical frame regardless of machine speed.

```bash
# per-step PNGs (overview, one per step, complete)
node scripts/export_frames.js flow.html out/ --stills --scale 2

# looping GIF — Slack, README, chat
node scripts/export_frames.js flow.html out/ --gif --fps 18 --gif-width 1100

# video — much smaller and sharper than GIF, and it has a scrub bar
node scripts/export_frames.js flow.html out/ --mp4 --fps 30   # web, Slack, PowerPoint
node scripts/export_frames.js flow.html out/ --mov --fps 30   # QuickTime, Keynote, Final Cut

# everything
node scripts/export_frames.js flow.html out/ --stills --gif --mp4 --mov
```

Requires `playwright` (node) and, for GIF/video, `ffmpeg`. Without ffmpeg the raw
frames are still written and can be encoded later.

### Picking a format

| Want | Use |
|---|---|
| Someone can click through at their own pace | the HTML — always ship this |
| Plays inline in Slack, GitHub, chat | `--gif` |
| Deck, email, DM, anywhere with a player | `--mp4` |
| macOS-native — QuickTime, Keynote, Final Cut | `--mov` |
| Will be re-edited or re-encoded downstream | `--prores` (large; ProRes 422 HQ) |
| Slides, print, a doc | `--stills --scale 2` |

`--mov` and `--mp4` are the same H.264 encode in different containers. The MOV
wrapper matters because some macOS apps refuse to preview an `.mp4` inline, and
Keynote handles `.mov` more predictably.

Notes that save a re-run:

- GIFs of a full 7-step sequence get large. Keep `--fps` at 15–20 and
  `--gif-width` at ~1100, or send a video instead where the destination allows it.
- Video wants `--fps 30`; GIF does not benefit past ~20 and just gets heavier.
- `--no-chrome` at build time gives cleaner exports — playback controls are not
  useful in a video. `export_frames.js` hides them anyway, but building without
  them also reclaims the vertical space.
- Even dimensions and `yuv420p` are non-negotiable for H.264 that opens in
  QuickTime and Preview; the script enforces both. An odd width produces a file
  that plays in VLC and nowhere else, which is a miserable thing to debug.
- Stills at `--scale 2` are the right choice for slides and print.

## Files

```
assets/
  engine.js        timeline engine — seekable, deterministic; do not rewrite per diagram
  engine.css       chrome + dim/highlight/glow states, all themable via CSS vars
  template.html    placeholder shell that build.py fills
scripts/
  build.py         inline SVG + steps + engine → one self-contained HTML
  check_layers.py  pre-flight the restructured SVG (run before building)
  export_frames.js deterministic stills / GIF / MP4 capture
references/
  grouping.md      how to restructure an SVG into layers — read before step 2
  steps-schema.md  the steps.json format, field by field
  inputs.md        Mermaid, Graphviz, and PNG-fallback paths
  theming.md       themes, CSS variable knobs, no-chrome and scrub variants
  themes/light.css light theme
examples/
  steps.example.json  a complete 7-step config from a real architecture diagram
```

## Scaling the effort

A 3-step process diagram is a fifteen-minute job: group, write three captions,
build, check. A 12-step architecture diagram with nested panels needs real care
in the grouping pass, and the captions become genuine technical writing.

Where the diagram covers a domain with established mechanics — an auth flow, a
deployment pipeline, a consensus protocol — the captions are much better when
they name the actual mechanism rather than paraphrasing the boxes. If something
in the diagram is unfamiliar or the terminology is ambiguous, ask rather than
guess: a confidently wrong caption is worse than a plain one, because the
animation lends it authority.
