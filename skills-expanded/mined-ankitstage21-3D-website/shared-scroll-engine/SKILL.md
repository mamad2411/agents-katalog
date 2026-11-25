---
name: shared-scroll-engine
description: Owns the shared project scaffold every scroll3d site is built from — the canonical index.html shell, the base.css stylesheet, and choreography.js (scroll-progress calculation, reduced-motion detection, resize/DPR handling, pointer-normalization and color math). Not user-facing, never invoked directly; the technique skills copy these files once per project so they cannot drift apart or ship a shell missing a library tag.
---

# Shared-Scroll-Engine — shared engine utilities

## Scope
This isn't a skill users interact with — it holds the files every project shares,
so the technique skills can't drift apart. Two jobs:

1. **The project scaffold.** `templates/index.html` (the canonical shell) and
   `templates/base.css` (everything not specific to one engine). Whichever
   technique skill runs FIRST copies these once per project; every later skill
   appends into them. There are deliberately no per-skill copies of these files —
   divergent shells were how a project could end up with no Three.js tag, or no
   `choreography.js` tag, purely because of build order.
2. **The shared JS utilities** in `templates/choreography.js`, so engines don't
   independently reimplement the same scroll/pointer math and drift apart over
   time (e.g. one engine's clamp logic getting fixed for an edge case while
   another's doesn't). Any new technique added later should extend this file with
   new shared primitives rather than reimplementing similar math inline.

## The scaffold contract
- `index.html` carries: the Lenis tag, the Three.js tag (pinned to r160 — the last
  release shipping `build/three.min.js`, removed in r161), the cannon-es module
  block, `choreography.js`, every engine `<script>` tag, every `*_SECTIONS`
  registry stub, and one commented example `<section>` per technique.
- The executing skill DELETES the example sections, registry entries and engine
  script tags for techniques the plan doesn't use, rather than each skill shipping
  its own partial shell.
- `base.css` is copied once as the project's `styles.css`; each technique skill then
  APPENDS its own `templates/styles.css` fragment underneath. A fragment on its own
  is not a working stylesheet — it has no `:root`, `.hud`, `.sticky` or `.reveal`
  rules, which is why the base must land first.

## What it provides
- `Choreography.progress(rect, innerHeight)` — the pinned-section scroll
  progress calculation (0 to 1), used identically by scroll-driven engines.
- `Choreography.prefersReducedMotion()` — the single source of truth for
  the reduced-motion check, so every engine checks it the same way.
- `Choreography.capDPR(cap)` — the devicePixelRatio capping logic used by
  every engine's resize handler.
- `Choreography.isInViewport(rect, innerHeight)` — the early-exit check
  used to skip update work for sections far outside the viewport.
- `Choreography.normalizedPointer(event, el)` — normalizes a pointer/mouse
  event's position to `{x, y}` in `[-1, 1]` relative to `el`'s bounding rect
  (or the viewport if `el` is omitted). Used by pointer-driven engines
  (currently pointer-follow-effect) instead of each one recomputing this by hand.
- `Choreography.lerp(a, b, t)` — basic linear interpolation, used for
  damping a value toward a moving target (e.g. easing a camera toward the
  latest pointer position frame over frame) rather than snapping to it.
- `Choreography.interpolateColor(hexA, hexB, t)` — interpolates between two
  hex colors and returns an `rgb(...)` string, `t` in `[0, 1]`. Used for
  scroll-synced background shifts (e.g. video-scroll-effect's `bgFrom`/`bgTo`
  fields on a `descent`-style section).

## Usage
Every engine (`video-scroll-effect.js`, `3d-scene-effect.js`, `pointer-follow-effect.js`,
`click-navigate.js`, `physics-play.js`, `hybrid-2d3d.js`, `cursor-trail.js`, and any
future engine) loads `choreography.js` before itself (`<script src="choreography.js">`
ahead of its own `<script>` tag in `index.html`) and calls into `window.Choreography.*`
instead of reimplementing this math inline.

Every engine also GUARDS on this: if `window.Choreography` is missing at
`DOMContentLoaded` it logs a named console error and bails out instead of throwing a
`TypeError` on the first `Choreography.*` call. A new engine added later must carry the
same guard — a silent throw here takes down every section on the page, not just its own.

## What this never does
- Never renders anything itself — `choreography.js` is pure utility functions only.
- Never makes any engine-specific decisions (frame indices, WebGL scene
  state, camera targets) — those stay in each engine's own JS file.
- Never holds technique-specific CSS. If a rule only applies to one engine's
  wrapper class (`.cinematic`, `.world`, `.parallax`, `.explore`, `.physics`,
  `.hybrid`, `.trail`), it belongs in that skill's fragment, not in `base.css`.

## Files
- `templates/index.html` — the canonical project shell.
- `templates/base.css` — shared base stylesheet, copied once as the project's `styles.css`.
- `templates/choreography.js` — shared scroll/pointer/color utilities.
