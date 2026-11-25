---
name: threejs-prototype-starter
description: Create and iterate simple playable Three.js prototypes with index.html, separate ESM JavaScript modules, and adaptive desktop/mobile controls. Use when Codex is asked to quickly prototype a Three.js game/mechanic/visual idea, scaffold a minimal playable browser prototype, add PC keyboard/mouse/gamepad controls, add mobile/Cordova touch controls, keep code lightweight, or prepare an early prototype that can later work with localization and threejs-steam-shipper Steam/web/mobile export skills. Delegates mechanical coding, parallel lanes and image generation to Gemini via the agy CLI, keeping design and hard problems on Fable/Opus.
---

# Three.js Prototype Starter

## Goal

Create a tiny playable Three.js prototype quickly, without overengineering. Start with `index.html` and separate ESM modules, keep the code easy to iterate, and leave a clean path toward `$threejs-localize` and `$threejs-steam-shipper` Steam/web/mobile exports if the idea becomes serious.

## Who Does The Work — Model & Labor Routing

This skill is an **orchestrator**. Most of the typing is delegated; you keep the
judgment. Route by *kind of thinking required*, never by convenience.

| Work | Engine | How |
|---|---|---|
| Art direction, core-loop design, architecture, scope cuts, ambiguous briefs, "why is this not fun" | **Fable 5** (plan) → **Opus 5** (execute) | Stay in Claude. Do not delegate. |
| Genuinely hard implementation — novel math, tricky shader, perf mystery, a bug with no diagnosis | **Opus 5** | Stay in Claude. |
| Scaffolding, ESM module wiring, controls layer, UI text extraction, refactors, renames, boilerplate, config, test scaffolds, doc sync, format passes | **Gemini via `agy`** | `~/Projects/ClaudeHQ/scripts/hq agy "<task>" --dir <project>` |
| Broad parallel work — several independent modules, asset manifests, content data, QA sweeps | **Gemini teamwork** | `agy` + `define_subagent` / `invoke_subagent` / `/teamwork-preview` |
| Concept art, placeholder sprites, style search, asset generation | **Gemini `generate_image`** | via `agy`; see Image Lane below |
| Video / motion reference | **Gemini on the web** | see Video Lane below |

**Never delegate to Sonnet or Haiku.** Where a smaller Claude tier would have been
used, use Gemini through `agy` instead — it is subscription-billed, runs headless, and
is stronger than a downgraded Claude tier for mechanical work.

**Do not ration Gemini.** Quota fear is not a reason to keep work in-house. Run
several `agy` lanes in parallel, spawn subagent teams freely, regenerate images until
the style is right. Default to `gemini-3.8-flash-medium` with `--effort medium` (task-type levels in global/model-routing.md; never Argon), which is what the
wrapper already does. Never use the Gemini 3 series. Rerun a lane that comes back wrong,
incomplete or invented at `gemini-3.8-flash-high`/`high`, then Haiku, then Sonnet. Reserve throttling for actual rate-limit errors, and when one
hits, back off that lane rather than abandoning the delegation.

### The one rule delegation does not buy you

`agy` output is a **claim, not evidence**. Every delegated task ends with you running
`git diff` / reading the file / loading the page. A report saying "done and verified"
counts for nothing until the disk agrees. Delegated runs write their report to
`docs/runs/<YYYY-MM-DD-HHMM>-<slug>.md` inside the project — read it, then verify it.

### Splitting work so parallelism actually pays

Measured on an equivalent prototype: one focused pass took 18 minutes; the same
content split across 19 packages and 14 agents took 5 hours. The loss was interface
discovery — packages waited to learn each other's shapes, and two invented conflicting
schemas for the same object.

So: **parallelize on axes that do not share an interface.** Art, content data, QA and
research never wait on each other. The core loop does. Give every delegated lane an
explicit file-ownership line — "write only under `public/assets/` and `src/art.js`;
if another file needs changing, report instead of editing" — and keep `src/scene.js`
and `src/main.js` single-owner while the loop is still being found.

### Image Lane

Concept frames and placeholder sprites go through Gemini's `generate_image`, not
hand-drawn canvas fills, whenever the brief has an art direction:

- **Style search:** one scene, ten genuinely different styles — not ten tints of one.
  The scene must be the game's most intense *moment*, framed like an in-game frame
  (camera, composition, HUD margins). A menu or victory screen is the wrong frame.
- **Aspect ratio** follows the shot: `16:9` in-game, `3:2` or `1:1` for cards/portraits.
- **Lock the style** by passing the chosen frame back as an `ImagePaths` reference on
  every later generation. Keep the style block byte-identical — one reworded adjective
  splits the set in two.
- **Rejects are per-asset**, never per-set: regenerate only the bad id, adding one
  sentence about what was wrong (`too dark`, `reads as a rock not a tent`). The old
  file stays until the new one lands, so the prototype never renders broken.
- Sprites stay textured quads. Regenerating art is cheap; substituting primitives for
  a sprite game is not — it changes the read of the whole game.

### 3D Lane — image, then model, then animation

Sprites remain the default; this lane opens **only when the brief asks for 3D in
words**. img2threejs existing is not a reason to turn a sprite game into a 3D one.

When the brief is 3D, the chain runs:

```
Gemini generate_image  →  reference frame  →  img2threejs  →  TS factory  →  live in scene
```

- **The reference frame is of the object, not the game.** Clean background, silhouette
  readable: three-quarter view for props, T/A-pose for characters. This is the one
  place where an in-game frame is the wrong frame.
- **`img2threejs` returns code, not assets** — a `createXModel(): THREE.Group`
  TypeScript factory plus an `ObjectSculptSpec` JSON. Readable, diffable, and
  animation-ready: it hands you a pivot/socket hierarchy you can rig. That is the
  whole reason to prefer it over a pile of primitives, which you cannot rig.
- **Wire the factory into `src/`,** not `public/assets/` — its output is source. The
  placeholder contract still holds: a primitive stands in until the factory lands.
- **Hero objects only.** Sculpting every piece of scene litter this way blows the
  prototype budget. Use it for the thing the player looks at.
- Not installed? The `img2threejs-setup` skill handles the checkout and the
  Claude/Antigravity symlinks. The sculpt pipeline is deterministic and mechanical —
  **delegate it to Gemini via `agy`**; keep only the acceptance call in Claude.
- **Limit:** one image cannot reveal hidden geometry, so the result is approximate,
  characters most of all. The tool flags its own confidence and inferred regions —
  carry those flags into the handoff instead of swallowing them.

### Video Lane

Neither Antigravity nor `agy` has a text-to-video engine. When the brief needs motion
reference or a trailer-style clip, open Gemini **on the web** in the browser and drive
it there — same account, same subscription, video models available. Keep the same
style block and reference frame you locked in the image lane.

For motion *inside* the prototype, do not go to video at all: Three.js plus Web Audio
gives you the real thing, and a running scene answers the design question better than
a rendered clip ever will.

## Before You Scaffold — Read The Brief, Do Not Assume

Three.js is the *renderer*, not the art direction. Never infer a 3D game from
the fact that this skill is Three.js.

1. **Sprites are the default. 3D must be asked for in words.**
   Build meshes/3D geometry **only** when the brief explicitly says so — "3D
   models", "meshes", "glTF/FBX assets", "3D characters", "full 3D". If the
   brief does not say that, the prototype is a **sprite** game, even when the
   space it renders is three-dimensional (Necrobeat is 3D space, sprite
   actors). A brief that is silent about art style is a sprite brief: assume
   sprites and keep going — do not ask, and do not reach for primitives.
2. **Sprite game means textured quads, not boxes.**
   Textured quads / `THREE.Sprite` / billboards, orthographic or perspective
   camera as the view demands. Boxes, spheres and capsules are NOT an
   acceptable stand-in for sprites — they change the whole read of the game.
   Explicit sprite cues to honour when present: "2D", "2.5D", "top-down",
   "isometric", "cutout sprites", "hand-painted", "pixel art", "sprite-only",
   or named sprite resolutions (e.g. `64x64`).
3. **Placeholder art still has to be the right kind of art.** For a sprite
   game, generate placeholder sprite textures (canvas-drawn or generated
   images) instead of substituting primitives.
4. **Show concept art first when the brief has an art direction section.**
   Produce concept frames through the Image Lane above (Gemini `generate_image`
   via `agy`) and confirm the look with the user *before* writing gameplay code.
   Wiring a whole prototype in the wrong visual language wastes the run. Do not
   block on it: fire the style search, then keep writing the core loop while it
   renders.

## Default Shape

Use this structure for new prototypes:

```text
target-project/
  index.html
  package.json
  vite.config.js
  src/
    main.js
    scene.js
    input.js
    ui.js
    styles.css
  public/
    assets/
```

This is intentionally small:

- `index.html` only loads `src/main.js`.
- JavaScript files use ESM imports/exports.
- Vite handles dev server and production `dist/`.
- `vite.config.js` uses `base: './'` so future Electron/Steam packaging can load assets from `file://`.
- Input uses one gameplay intent shape (`moveX`, `moveY`, `action`) while `input.js` chooses keyboard/mouse/gamepad or mobile touch controls from device capability and target.
- UI text lives in `ui.js` constants/functions first, so `$threejs-localize` can later extract it cleanly.

## Workflow

1. **Scaffold if needed.**

   ```bash
   node <skill>/scripts/scaffold-threejs-prototype.mjs <target-project> --name "Prototype Name"
   ```

   The script creates missing files only. It does not overwrite existing prototype code.

2. **Implement the idea — delegate the typing, keep the loop.**
   Hand the scaffold, the input layer, the UI shell and any later refactor to
   `agy` (parallel lanes where the files do not overlap). Write `scene.js` and
   the core update loop yourself while those run — that is the part that has to
   stay in one head. Verify every delegated lane with `git diff` before building
   on it.
   - Put renderer/camera/bootstrap in `main.js`.
   - Put scene objects and update loop logic in `scene.js`.
   - Put keyboard, pointer/touch, and gamepad state in `input.js`.
   - Put DOM labels/buttons/help text in `ui.js`.
   - Put CSS in `styles.css`.
   - Keep scene code platform-agnostic: consume `input.state.moveX`, `input.state.moveY`, and action flags instead of checking `window`, `cordova`, keyboard keys, or touch state inside gameplay.

3. **Keep iteration fast.**
   - Prefer one playable mechanic over menus, settings, save systems, assets, or polish.
   - Use primitives and simple materials before importing models.
   - Add only the controls needed to test the idea.
   - Keep functions small and obvious; avoid frameworks until the prototype earns them.

4. **Run locally.**

   ```bash
   npm install
   npm run dev
   ```

   If another server is already running, use Vite's next available port.

5. **Make it future-compatible.**
   - Use relative asset URLs and `public/assets/`.
   - Keep player-facing text centralized in `ui.js` or a small object, not scattered across render code.
   - Avoid build-only or draft files under `public/`.
   - Keep source code clean enough that `$threejs-localize` can scan it and `$threejs-steam-shipper` can build/package `dist/` for Steam, web, or Cordova mobile.
   - Add target override query params for QA when useful: `?controls=desktop`, `?controls=touch`, `?controls=gamepad`.
   - For Cordova/mobile, use touch controls, safe-area CSS, pause/resume hooks, and real-device checks before treating the prototype as shippable.
   - For PC/Steam/web desktop, keep keyboard/mouse usable and poll the Gamepad API when a controller is connected.

6. **Check controls on target devices.** Load `references/adaptive-controls.md` before adding or changing controls. Verify desktop keyboard/mouse, optional gamepad, mobile browser touch, and Cordova touch behavior according to the target the user wants to build.

7. **When the prototype grows.** Load `references/grow-up-path.md` before restructuring toward a bigger app/game. Move deliberately: introduce folders, state management, asset pipelines, localization, and Steam/web/mobile packaging only when the prototype needs them.

## Compatibility

This skill works standalone. It does not require `$threejs-localize` or `$threejs-steam-shipper`.

If those skills are later used:

- `$threejs-localize` can extract UI strings from `src/ui.js`.
- `$threejs-steam-shipper` can run the Vite production build and copy `dist/` into `buildable/steam-electron/web/`, `buildable/web/dist/`, or `buildable/mobile-cordova/www/`.
- `base: './'` avoids common Electron `file://`, static subfolder, and Cordova `www/` asset path failures.
- The adaptive input layer lets each export target use the right controller without changing gameplay code: PC uses keyboard/mouse/gamepad, mobile/Cordova uses touch controls.

## References

- Read `references/prototype-pattern.md` for file responsibilities and anti-overengineering rules.
- Read `references/adaptive-controls.md` before implementing controls for PC, web, mobile browser, or Cordova.
- Read `references/grow-up-path.md` before turning a prototype into a more serious project.
