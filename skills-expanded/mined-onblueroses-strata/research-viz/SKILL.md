---
name: research-viz
description: "Build visual artifacts that explain: hand-authored theme-adaptive SVG diagrams for docs, notebooks and READMEs, and interactive localhost viewers for tensors, activations, attention and KV caches. Auto-trigger on: 'diagram this', 'draw how X works', 'architecture picture', 'visualize a tensor', 'attention map'. For plotting data as charts use dataviz instead."
---

# Research Viz

## When to use

Viewers are Python capture then self-contained HTML. Also triggers on: 'figure for the notebook', 'show what the layers are doing', 'KV cache viewer'.

Instruments, not decoration. The goal is a thing you look at to find out what happened, and that you
would trust enough to put a claim on.

Distilled from a measured corpus of viewers and hand-authored SVGs. File and line
references below identify the example implementation within that corpus.

## The stance

Three laws generate almost everything else. Read them before reaching for a chart library.

**1. The browser computes geometry. It never computes a research number.**
Split every viewer in two: `capture_*()` runs the real thing and returns a plain dict; `show_*()`
serves a page that renders that dict. The payload becomes a testable contract, downsampling stays
safe because sampling only affects what is drawn and never what is reported, and you can assert on
the same numbers the page displays without opening a browser.
Named exception: cheap aggregates over already-exact shipped data, computed once and cached. State it
when you take it, because the repo itself violates the absolute form in three places and each one
puts two precisions behind one legend.

**2. A claim belongs in the viewport, not the caption.**
If you would write "the transfer is lossless" under a figure, instead evaluate that predicate in the
capture layer, assert on the field, and render **both** the pass and the fail state as first-class UI.
A badge that can go red is evidence. A sentence cannot fail.

**3. Nothing silently disappears.**
Thresholded-out marks, dropped axes, merged leading dimensions, strided samples: disclose them in the
UI. A viewer that quietly shows you 60% of the data teaches you a false thing with full confidence.

## Pick the diagram type

Route on what the reader is trying to find out, not on the subject matter. These are the four
answers, and picking the wrong one is why most technical figures fail.

| The question behind the request | Type | Shape |
|---|---|---|
| "how does X work", "explain X", "I don't get X" | **Illustrative** | a visual metaphor that carries the intuition; the objects are drawn as what they are |
| "what's the architecture", "show the structure" | **Structural** | containment and adjacency; boxes inside boxes |
| "what are the steps", "walk me through it" | **Flowchart** | sequence, left to right, one path highlighted |
| "how does this number compare" | **Chart** | use `dataviz`, not this skill |

Between illustrative and flowchart, illustrative is the more ambitious choice and usually the right
one for "how does X work". A flowchart tells you the order of operations; an illustration tells you
what the thing *is*, which is what a confused reader is missing.

Then pick how to render it:

| You want to show | Reach for | Why |
|---|---|---|
| A depth × position grid of tokens or labels | CSS grid of `<div>`s | text stays selectable, hit-testing is free, themes retheme automatically |
| An N×N attention map (10k+ cells) | Canvas 2D | DOM dies at this cardinality; accept manual hit-testing and DPR |
| A 3D tensor / weight layout | three.js `InstancedMesh` | one mesh, `setMatrixAt`/`setColorAt`, scales to ~100k voxels |
| A fixed explanatory figure for a doc or notebook | Hand-authored SVG | diffable, themeable, no runtime, renders on GitHub |
| A metric that changes as a job runs | Append-only list + SSE, memoized cards | makes DOM diffing unnecessary rather than fast |

Default to DOM. Reach for canvas only when cardinality forces it: canvas costs you manual text
layout, manual hit testing, manual devicePixelRatio, and it is the one thing a theme change cannot
repaint for free.

## Non-negotiables

These fail silently, which is why they are here rather than in a reference.

- **Canvas and WebGL are palette snapshots.** DOM and SVG retheme for free; immediate-mode marks do
  not. Wire an explicit repaint into the theme toggle or half your viewer keeps yesterday's colors.
- **`InstancedMesh` picking dies when the extent grows.** three.js computes `boundingSphere` lazily
  only when it is `null`, so after changing `count` or any matrix, set `mesh.boundingSphere = null`.
  Otherwise hover and click stop working on newly-extended instances and nothing errors.
- **Scrub NaN/Inf for rendering, keep the raw array for stats.** Two arrays, always. The payload is a
  JS object literal, not `JSON.parse`, so `NaN` parses fine and then poisons every downstream scale
  until the whole view goes neutral.
- **Emit the legend by calling the mark's own color function** at the domain endpoints. Otherwise a
  refactor eventually paints one scale and labels another, and nothing catches it.
- **A ramp's ceiling is a function of what sits on the mark.** Bare cells take `0.06 + 0.88t`; cells
  carrying monospace text need a lower ceiling (~0.75) or the text stops being readable.
- **Theme direction is inverted between the two media.** Interactive viewers here are dark-first
  (`:root` dark, `[data-theme="light"]` override); hand-authored SVGs are light-first (author light
  hex, remap under `prefers-color-scheme: dark`). Know which you are copying before mixing them.
- **Any grid you intend to scroll needs `width: max-content`** on the grid and `overflow-x: auto` on
  a wrapper, or a wide grid compresses to the container and every cell collapses.

## Hand-authored SVG: the one trick worth internalizing

Author every fill in the light palette, then remap the whole file for dark mode with one style block
of attribute selectors. No classes, no dark hex ever written by hand:

```svg
<style>
  @media (prefers-color-scheme: dark) {
    svg { fill: #e5e7eb; }                     /* default-black text */
    [fill="#ffffff"] { fill: #111827; }
    [fill="#1f2937"] { fill: #e5e7eb; }        /* swap pairs are safe: selectors */
    [stroke="#6b7280"] { stroke: #9ca3af; }    /* match attributes, declarations set properties */
  }
</style>
```

Swap pairs do not cascade-loop, because the selector matches the *attribute* while the declaration
sets the *property*. Limits: it cannot reach `style="..."` inline attributes, and gradients need
their stops remapped individually.

**The failure mode is silent and total**: a color you author but forget to map simply never remaps,
so it looks right in light mode and vanishes or glares in dark. Run the bundled linter before
committing any SVG:

```bash
python3 scripts/svg_theme_lint.py doc/img/*.svg
```

It reports every `fill=`/`stroke=` value absent from that file's own style block. This is not
optional hygiene; the playbook this skill came from shipped two "copy me" skeletons that failed
their own linter.

## References

Read the one that matches the task; they do not need to be read together.

| File | When |
|---|---|
| `references/viewer-stack.md` | Building the Python capture/serve layer: shared localhost server, name-as-URL, idempotent notebook re-runs, payload prep |
| `references/svg-diagrams.md` | Drawing a figure: full palette, visual vocabulary, layout grammar, copy-pasteable skeletons |
| `references/design-system.md` | Making it look designed: tokens with real hex, typography scale, spacing, theme mechanism |
| `references/rendering.md` | Canvas grids, sparklines, three.js instancing and log-scaled layout, diff marking, animated wires |

## What not to do

- **No explanatory prose inside the artifact.** Text goes in the surrounding document; the figure
  carries what only a picture can. A diagram with a paragraph in it is a paragraph with decoration.
- **No gradients, drop shadows, blur, glow or neon.** The restraint is the look. They also make an
  SVG harder to theme, because a gradient's stops need remapping individually.
- **No emoji in SVG or HTML marks.** Use CSS shapes or SVG paths; emoji render differently per
  platform and break the typographic scale.
- **Never hardcode a color without deciding its dark-mode fate.** This is the silent one; run the
  linter.
- **Do not draw a cycle as a ring.** Use a stepper, or a linear flow with a return arrow. Rings put
  the entry point nowhere and force the reader to hunt for where to start.
- **Do not cram 6+ components into one figure.** Decompose. Two figures that each land beat one that
  has to be studied.
- **Do not stack visuals back to back.** Prose between them tells the reader what changed.
- **Two figures showing the same thing is a cut, not an addition.** Replace the weaker one; a
  markdown table that a figure now covers in full should go.

## Working rules

- Build the capture layer first and assert on its dict. If you cannot test the numbers without a
  browser, the split in Law 1 is wrong.
- Re-read templates from disk on every call so editing a page costs a cell re-run, not a kernel
  restart.
- Ship the smallest honest thing: a legend, a unit, and a disclosed sampling stride beat another
  panel.
- When a figure and a table show the same thing, deleting the weaker one is the edit.
