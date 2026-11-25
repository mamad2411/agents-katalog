---
name: cursor-trail
description: Executes ONE section of a site plan handed to it by site-planner, using a canvas-2D particle system that trails the cursor — atmospheric/decorative, not a product-showcase technique like the other real-time engines. Scroll still pins the section and drives overlay copy; cursor position drives the particles. Does NOT decide site structure or content depth — site-planner owns those decisions. Trigger only via site-planner's hand-off, or directly if the user explicitly asks for cursor-trailing particles by name.
---

# Cursor-Trail — canvas-2D particle-trail execution engine

## What this actually is (read first)
A lightweight canvas-2D particle system (no WebGL/Three.js needed — this is decorative
motion, not geometry) where particles spawn at the cursor position and drift/fade,
leaving a trail as the visitor moves their mouse. Scroll still pins the section and
drives the `.reveal-line` overlay copy exactly like video-scroll-effect/3d-scene-effect;
cursor position only drives the particle layer. Best for atmospheric/mood sections
(brand moments, section transitions) rather than sections that need to communicate
product specifics.

Stack: **HTML + CSS + JS (canvas 2D)** + `choreography.js`. No Three.js needed.

## Scope — this skill does NOT decide
This skill executes a section (or sections) from a site plan produced by
site-planner. It does not decide overall site structure or content depth. If
invoked without a plan, ask for a `content_brief` and `palette` for the section being
built — do not invent a full multi-section site yourself.

## Asset needs
None — this is a pure particle effect, no image/video generation involved.

## Prerequisites
- No external API/credits needed, no external CDN dependency beyond `choreography.js`.
- This skill installed at `${CLAUDE_PLUGIN_ROOT}/skills/cursor-trail/`.

## THE PIPELINE — executes one plan section

### 1. Read the section spec
Take the `content_brief` and the site's `palette` from the plan. Write this section's
overlay copy from `content_brief` — don't reuse generic placeholder text.

### 2. Build a fixed-size particle pool
Pre-allocate `particleCount` (default 150) particle objects up front in a plain array —
`{ x, y, vx, vy, life, maxLife }` — and never grow that array at runtime. This is the
one hard rule of this engine: don't `push`/`splice` particle objects inside the render
loop, or per-frame garbage collection stutters the whole page. Cycle through the pool
round-robin (or respawn the oldest-dead one) each time a new particle needs to spawn.

### 3. Wire cursor-driven spawning + ambient fallback
- On `pointermove` within the section (gated behind
  `matchMedia("(hover: hover) and (pointer: fine)")`, same as pointer-follow-effect):
  respawn 1-3 pool particles per event at the cursor position with a small randomized
  velocity, reusing `window.Choreography.normalizedPointer` to get the position.
- No fine pointer, or `prefers-reduced-motion` set: don't wire the listener at all —
  instead spawn/drift particles ambiently (gentle randomized motion, no cursor
  dependency) so touch-device and reduced-motion visitors still see a populated,
  alive-looking canvas rather than an empty one.
- Every frame: advance each live particle's position/opacity by its age, draw it, and
  let it "die" (become eligible for respawn) once its `life` exceeds `maxLife`.

### 4. Build this section from templates/
- **Project scaffold (once per site, whichever skill runs FIRST):** copy
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/index.html`,
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/base.css` (as the project's `styles.css`),
  and `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/choreography.js` into the project.
  There is no per-skill `index.html` any more — the shell is shared so a project
  can never end up missing the Three.js / cannon-es / choreography tags just
  because of which technique happened to be built first.
- **This skill's own files (every time this skill runs):** copy
  `templates/cursor-trail.js` into the project, and APPEND `templates/styles.css`
  (a fragment, not a full stylesheet) to the project's `styles.css`.
- If the project already has the scaffold, do not overwrite it — subsequent
  sections append into what is already there.
- Register this section in a `TRAIL_SECTIONS` entry:
  `{ section:"#<section-id>", palette:{...}, particleCount:150 }`.
- **Class contract** the engine depends on (rename these and it silently does nothing):
  - each section: a `<canvas>` inside `.sticky`, wrapped by a `.trail` section with the
    config's id
  - `.reveal-line` + `data-in`/`data-out` — same scroll-driven overlay-copy contract as
    video-scroll-effect/3d-scene-effect
- If this is the first section being built for this project (nav bar doesn't exist yet
  in index.html), generate the `.hud-nav` links from the full `plan.sections` list's
  `id`/`nav_label` pairs before proceeding to this section's own content.

### 5. Deploy to Cloudflare Pages + write out to connected folder
(Same as the other engines' final step — runs once, after all sections from the plan,
across every technique in use, are in the same project.)
- Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` as environment variables.
- Load credentials first: `set -a && source .env && set +a`.
- Deploy: `npx wrangler pages deploy <project-dir> --project-name=<slug> --branch=main`.
- Confirm the live URL loads before telling the user it's ready.
- Always write out to the connected folder regardless of deploy success.

## Engine rules
- Cap pixel ratio via `window.Choreography.capDPR()`, same as the other engines.
- Scroll-driven overlay update (`.reveal-line` opacity) hooks into an existing
  `window.__lenis` instance if present, else falls back to its own rAF loop against
  native scroll — same coexistence pattern as 3d-scene-effect/pointer-follow-effect.
- Particle rendering runs on its own rAF loop independent of scroll, gated only by
  `Choreography.isInViewport` so it doesn't burn CPU off-screen.

## Known gotchas
- The fixed-size pool is the main trap — if particle objects are created inside the
  per-frame draw function instead of pre-allocated once, this looks fine at first and
  then stutters increasingly as the browser's GC struggles to keep up. `build-reviewer`
  checks for this pattern.
- Keep `particleCount` modest (100-200) — a canvas-2D particle system with thousands of
  live particles is still real per-frame draw-call cost.
- Same headless-screenshot limitation as the other engines: verify live in a real
  browser with actual cursor movement, not just via automated screenshot tools.

## Files
- `templates/cursor-trail.js` — canvas-2D particle pool + scroll-driven overlay.
- `templates/styles.css` — `.trail` CSS fragment, appended to the project's `styles.css`.
- Project shell (`index.html`, `base.css`, `choreography.js`): `shared-scroll-engine/templates/`.
