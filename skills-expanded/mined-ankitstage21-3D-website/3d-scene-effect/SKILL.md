---
name: 3d-scene-effect
description: Executes ONE section of a site plan handed to it by site-planner, using real-time WebGL (Three.js) rather than frame-scrub video. Builds a procedurally modeled or abstract 3D scene that responds to scroll position — camera orbit, morphing geometry, particle effects. No AI video/image generation needed; the "3D" comes from actual geometry and lighting, not footage. Does NOT decide site structure or content depth — site-planner owns those decisions. Trigger only via site-planner's hand-off, or directly if the user explicitly asks for real 3D/WebGL by name.
---

# 3D-Scene-Effect — real-time WebGL execution engine

## What this actually is (read first)
Unlike video-scroll-effect (canvas image-sequence scrub from a generated video), this
builds an actual **Three.js scene** — real geometry, real materials, real lighting —
that responds to scroll position in real time. No footage to generate, no frames to
extract. This suits abstract/procedural subjects well (geometric products, tech/SaaS,
anything where photorealism isn't the point) and is a good fallback when video
generation isn't available.

Stack: **HTML + CSS + JS + Three.js** (loaded from CDN, zero build step).

## Scope — this skill does NOT decide
This skill executes a section (or sections) from a site plan produced by
site-planner. It does not decide overall site structure or content depth.
If invoked without a plan, ask for a `content_brief`, `motion`, and `palette`
for the section being built — do not invent a full multi-section site yourself.

## Handling a single static image as input (no video, no AI generation)
When a section's only available asset is one static photo (no video clip, no
Higgsfield access), do NOT treat this the same as a photorealistic-footage
section — texture-map the photo onto real 3D geometry instead, so scroll-driven
camera movement reads as genuine 3D parallax rather than a flat pan/zoom.

- Map the image onto a `THREE.PlaneGeometry` (or a slightly curved/beveled plane
  for more dimensionality) as its material's texture map.
- Drive the CAMERA around this textured plane using scroll progress — tilt,
  orbit partially, dolly in/out, shift perspective — rather than moving/zooming
  the image itself. Real 3D camera movement around a flat plane still reads as
  meaningfully more three-dimensional than a 2D zoompan, because parallax and
  perspective shift are genuinely present.
- Add subtle depth cues to sell the effect: a soft drop shadow beneath the
  plane, slight ambient occlusion at the plane edges, or a very slight
  perspective distortion — these are cheap and meaningfully improve the
  illusion of depth from a single flat image.
- This mode requires zero credits and zero video generation — it's the
  fallback that should be offered whenever a user has photos but no video and
  no working Higgsfield access, instead of routing that section to
  video-scroll-effect's flat frame-scrub (which has no real motion to work with
  from a single image).


## Prerequisites
- No external API/credits needed — Three.js is CDN-loaded, geometry is built in code.
- This skill installed at `${CLAUDE_PLUGIN_ROOT}/skills/3d-scene-effect/`.

## THE PIPELINE — executes one plan section

### 1. Read the section spec
Take the section's `motion`, `content_brief`, and the site's `palette` from the plan
handed off by site-planner.

### 2. Model the subject procedurally
Build the 3D subject from primitive geometries (boxes, cylinders, spheres, extrusions,
lathes) combined and styled to suggest the product — this doesn't need to be a precise
model, it needs to read clearly at a glance while scrolling. Favor:
- Simple, iconic silhouettes over intricate detail (detail gets lost during motion anyway)
- Materials that match the palette (metalness/roughness for product realism, or flat/
  toon-shaded for a more abstract, brand-forward look)
- Consistent lighting: 2-3 lights (key + rim + fill) rather than relying on ambient alone

### 3. Drive the scene from scroll position
Use the section's `motion` value to decide the camera/geometry behavior:
- **orbit/turntable** — camera orbits the subject as scroll progress goes 0→1
- **fly-through** — camera moves through/past the subject along a path
- **morph/reveal** — geometry itself deforms, assembles, or explodes apart with scroll
- **abstract drift** — particles or abstract forms drift/rotate, decoupled from a literal subject
- If `motion` doesn't match any of these, implement something in the same spirit rather
  than forcing it into one of the above.
- Drive updates from scroll progress the same way video-scroll-effect does: pin the section
  (`position:sticky`), compute `progress = clamp(-rect.top / (rect.height - innerH), 0, 1)`,
  and map that to camera/geometry state every frame.

### 4. Build this section from templates/
- **Project scaffold (once per site, whichever skill runs FIRST):** copy
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/index.html`,
  `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/base.css` (as the project's `styles.css`),
  and `${CLAUDE_PLUGIN_ROOT}/skills/shared-scroll-engine/templates/choreography.js` into the project.
  There is no per-skill `index.html` any more — the shell is shared so a project
  can never end up missing the Three.js / cannon-es / choreography tags just
  because of which technique happened to be built first.
- **This skill's own files (every time this skill runs):** copy
  `templates/3d-scene-effect.js` into the project, and APPEND `templates/styles.css`
  (a fragment, not a full stylesheet) to the project's `styles.css`.
- If the project already has the scaffold, do not overwrite it — subsequent
  sections append into what is already there.
- Register this section the same way video-scroll-effect registers scrub sections, so both
  skills' sections can coexist on one page without conflicting engines.
- Write this section's copy from its `content_brief`.
- If this is the first section being built for this project (nav bar doesn't
  exist yet in index.html), generate the `.hud-nav` links from the full
  `plan.sections` list's `id`/`nav_label` pairs before proceeding to this
  section's own content.

### 5. Deploy to Cloudflare Pages + write out to connected folder
(Same as video-scroll-effect's Step 7/7b — runs once, after all sections from the plan,
whether built by video-scroll-effect, 3d-scene-effect, or both, are in the same project.)
- Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` as environment variables.
- Load credentials first: `set -a && source .env && set +a`.
- Deploy: `npx wrangler pages deploy <project-dir> --project-name=<slug> --branch=main`.
- Confirm the live URL loads before telling the user it's ready.
- Always write out to the connected folder regardless of deploy success.

## Engine rules
- Cap pixel ratio (`Math.min(devicePixelRatio, 2)`) to avoid tanking performance on
  high-DPI displays.
- Dispose of geometries/materials/textures on section teardown if the page has many
  sections — don't leak WebGL contexts.
- Throttle scroll-driven updates via requestAnimationFrame, same pattern as
  video-scroll-effect's engine — never recompute scene state directly inside a raw
  scroll event handler.
- Respect `prefers-reduced-motion`: freeze the camera/geometry at a single static
  pose instead of animating, same principle as video-scroll-effect's E3 fix.

## Known gotchas
- Procedural geometry can look cheap if lighting is flat — always use at least a key
  + rim light, never pure ambient-only.
- Too much geometric complexity kills scroll framerate — favor fewer, well-lit shapes
  over dense detail.
- Same headless-screenshot limitation as video-scroll-effect: verify live in a real
  browser, not just via automated screenshot tools, since WebGL canvases often don't
  capture correctly in headless contexts.

## Files
- `templates/3d-scene-effect.js` — Three.js scene + scroll driver.
- `templates/styles.css` — `.world` CSS fragment, appended to the project's `styles.css`.
- Project shell (`index.html`, `base.css`, `choreography.js`): `shared-scroll-engine/templates/`.