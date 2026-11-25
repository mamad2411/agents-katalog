---
name: hybrid-2d3d
description: Executes ONE section of a site plan handed to it by site-planner, using a flat editorial 2D layout (real headline/paragraph/stats, normal document flow) with a smaller embedded Three.js object as an inline visual — NOT a full-bleed pinned scene like the other real-time techniques. Does NOT decide site structure or content depth — site-planner owns those decisions. Trigger only via site-planner's hand-off, or directly if the user explicitly asks for a hybrid/editorial 2D-and-3D layout by name.
---

# Hybrid-2D3D — editorial layout with an inline 3D object

## What this actually is (read first)
Every other technique in this plugin is a full-bleed pinned scroll-jacked or
cursor-jacked moment. This one is deliberately the opposite: a normal, flat editorial
section — real headline, paragraph, stat row, standard document flow, no
`position:sticky`, no multi-`vh` scroll runway — with a smaller Three.js canvas
embedded inline as a hero visual next to the copy. It reads as "an article page with a
3D object in it," not "an immersive 3D moment." Use it to break up a site that would
otherwise be wall-to-wall full-bleed sections, or for content-dense sections where
readable, scannable copy matters more than spectacle.

Stack: **HTML + CSS + JS + Three.js** (CDN, zero build step) + `choreography.js`.

## Scope — this skill does NOT decide
This skill executes a section (or sections) from a site plan produced by
site-planner. It does not decide overall site structure or content depth. If
invoked without a plan, ask for a `content_brief`, `motion`, and `palette` for the
section being built — do not invent a full multi-section site yourself.

## Asset needs
No image/video generation needed — the embedded object is built procedurally, same
approach as 3d-scene-effect Step 2 (simple, iconic silhouettes read better at the smaller
size this technique renders at than intricate detail would).

## Prerequisites
- No external API/credits needed — Three.js is CDN-loaded.
- This skill installed at `${CLAUDE_PLUGIN_ROOT}/skills/hybrid-2d3d/`.

## THE PIPELINE — executes one plan section

### 1. Read the section spec
Take the section's `motion`, `content_brief`, and the site's `palette` from the plan.
Write real headline/paragraph/stat copy from `content_brief` — this section is
copy-forward, more so than the full-bleed techniques where copy is a few punchy
overlay lines.

### 2. Build the inline 3D object
Model the subject procedurally (same primitive-geometry approach as 3d-scene-effect),
favoring simple iconic silhouettes — the canvas here is a bounded, fixed-aspect-ratio
box (e.g. `aspect-ratio: 1`), not a full-viewport stage, so detail reads smaller.

### 3. Drive the object: idle rotation, optional pointer-tilt
- Auto-rotate continuously (`group.rotation.y += delta` each frame) — this is the
  section's baseline motion and works identically for every visitor regardless of
  device or input capability. Pause the rAF loop via
  `window.Choreography.isInViewport` when the section scrolls off-screen.
- Optionally, layer a mild pointer-tilt on top using
  `window.Choreography.normalizedPointer`/`lerp` when
  `(hover: hover) and (pointer: fine)` matches — this is a progressive enhancement
  only. Because idle rotation alone already makes the section work everywhere, there
  is no fallback-pose gotcha to handle here (unlike pointer-follow-effect): with or without
  a fine pointer, or with `prefers-reduced-motion` set, simply skip the extra tilt and
  the base idle rotation still renders something meaningful. Skip the idle rotation
  itself too under `prefers-reduced-motion` — freeze at a single static pose, same
  principle as every other engine.

### 4. Build this section from templates/
- **Project scaffold (once per site, whichever skill runs FIRST):** copy
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/index.html`,
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/base.css` (as the project's `styles.css`),
  and `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/choreography.js` into the project.
  There is no per-skill `index.html` any more — the shell is shared so a project
  can never end up missing the Three.js / cannon-es / choreography tags just
  because of which technique happened to be built first.
- **This skill's own files (every time this skill runs):** copy
  `templates/hybrid-2d3d.js` into the project, and APPEND `templates/styles.css`
  (a fragment, not a full stylesheet) to the project's `styles.css`.
- If the project already has the scaffold, do not overwrite it — subsequent
  sections append into what is already there.
- Register this section in a `HYBRID_SECTIONS` entry:
  `{ section:"#<section-id>", motion:"<motion>", palette:{...} }`.
- **Class contract** the engine depends on (rename these and it silently does nothing):
  - each section: a `.hybrid` section containing a `.hybrid-grid` with `.hybrid-copy`
    (flat text content) and `.hybrid-stage` (a `<canvas>`, fixed aspect ratio)
  - **no `.sticky` wrapper** — that's the structural signal this section is NOT
    full-bleed/pinned; adding one here is a bug, not a stylistic choice
  - text content uses `.reveal` (fade-up-on-enter) and `.stat`/`.stat-num` — the same
    generic IntersectionObserver-driven classes used sitewide — NOT `.reveal-line`,
    since this section isn't scroll-progress-driven
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
- Size the renderer to the `.hybrid-stage` element's bounding box, not the viewport —
  this canvas is bounded, unlike every other engine's full-bleed canvas.
- Pause the rAF loop when off-screen (`Choreography.isInViewport`) — an idle-rotating
  object still costs a render per frame even though nothing scroll/pointer-driven is
  happening, so don't let it run forever on a section nobody's looking at.

## Known gotchas
- Don't reuse `.sticky`/`position:sticky` here even though every other engine does —
  it's the one deliberate structural exception, and `build-reviewer` checks for it.
- Keep the object simple — at this canvas size (roughly a card, not a viewport),
  intricate geometry just reads as noise; the silhouette needs to be legible small.
- If adding the optional pointer-tilt, damp it more subtly than pointer-follow-effect's
  full-scene version (this is a small inline accent, not the section's main draw) —
  a small rotation offset (a few degrees) reads better than a dramatic camera swing.

## Files
- `templates/hybrid-2d3d.js` — editorial grid layout + inline auto-rotating Three.js object.
- `templates/styles.css` — `.hybrid` CSS fragment, appended to the project's `styles.css`.
- Project shell (`index.html`, `base.css`, `choreography.js`): `shared-scroll-engine/templates/`.
