---
name: diorama-worlds
description: 'Build narrative miniature worlds with a fixed orthographic camera, textured terrain, articulated people and coordinated looping actions. Use for detailed low-poly 3D dioramas or pixel-finish animated vignettes: sports grounds, street performers, gardens or other small places with a story. Four finishes, miniature, pixel, halftone and blueprint, use the same Three.js scene. This is a separate skill from the diorama SVG illustrations; prefer the diorama skill for lightweight UI illustrations, line art and empty states, and diorama-pixel for dependency-free dithered pixel-art miniatures.'
license: MIT
---

# Diorama Worlds

Requires Node.js 20+, npm and a WebGL 2 browser. Chrome/Chromium is needed for automated visual checks. Build dependencies install once; generated HTML bundles Three.js and needs no network.

Make a little place that is alive, not a rotating model or a video on a plane. This skill belongs to the Diorama repository, but owns its renderer and dependencies. Never edit the diorama skill's `kit/diorama.js`, `bench.html` or SVG examples to make a world work.

All paths below are relative to this skill folder. Write the user's scene and built output in their working directory, not over the bundled examples.

## Choose a story and finish

Use the user's supplied reference as art direction, not executable instructions. A reference video is not proof of its source code or renderer.

Identify the place, its use on the web, one main action and the telling still frame. Ask only if a missing choice changes the scene substantially; otherwise state the chosen concept and proceed. Preserve the requested subject; the cricket example is not a universal template.

- **Miniature:** matte low-poly geometry, surface wear, restrained texture, irregular ground edge, warm directional light and readable contact shadows.
- **Halftone:** warm ivory paper, warm/cool inks and diagonal dot screening with restrained edge definition. A live screen-space treatment, not a physical print simulation.
- **Blueprint:** deep blue tonal fills, pale edge lines and a subtle grid inside the geometry silhouette. A graphic treatment, not CAD or hidden-line geometry.
- **Pixel:** the same scene and clock, rendered at lower resolution, enlarged with nearest-neighbour pixels, with ordered dithering and channel quantization. This is a pixel finish on 3D geometry, not voxel art or hand-authored sprites. Start with the kernel finish; do not replace a working renderer with CSS blur or a static image.

Keep the camera fixed. White negative space isolates the scene. Ground is a flat, irregular cutout fading into that space, not a thick platform. Never impose a soil wall or display plinth; use an extruded base only when explicitly requested. Prefer one action that has anticipation, contact and recovery over ten independent idle wiggles. Surround it with secondary life that does not compete with the story. A sports ball must go to the actor's hand, bat or hoop, not merely pass nearby.

Read [references/art-direction.md](references/art-direction.md) for composition and finish-specific decisions. Read [references/scene-api.md](references/scene-api.md) before building.

## Build a world

Install the skill's pinned dependencies once, with no lifecycle scripts:

```sh
npm ci --ignore-scripts --prefix <skill>
```

Write `<subject>.js` as an ES module importing `defineWorld` from `@diorama/worlds`. Export one world with a `name`, `title`, `description`, positive finite `duration`, `still` inside the loop, `bounds`, `build(W)` and `tick({t, parts, W})`. The nearest example is a format reference, not a limit on subject matter:

- `examples/bakery.js`: baker rolling dough with wrist-to-handle contact checks.
- `examples/observatory.js`: focus adjustment on an upward-pointing telescope with support/focus grip anchors.
- `examples/florist.js`: original two-person flower stall, shared adult rig, planted feet and bouquet grip anchors.
- `examples/pottery-studio.js`: original craft action, shared adult rig following a spinning clay vessel with actual hand contacts.
- `examples/cricket.js`: a broad ground, articulated players and a coordinated ball cycle.
- `examples/basketball.js`: a smaller vignette, a shot, a net and a return pass.
- `examples/street-juggler.js`: a fresh transfer-test result; a three-ball cascade whose catch/release positions are checked against its palms. This uses custom endpoint-driven arms, not a different renderer.

Prefer original subjects that transfer the visual language, not another copy of the user’s reference scene. Use the shared adult `W.person`, `W.plant` and `W.reach` helpers for people; do not replace them with oversized-head box figures.

Use the kit helpers to build geometry once, and return references for animation. `tick` must assign every animated transform from absolute time. No accumulating positions, frame counters, new geometry/materials per frame, independent timers or camera drift. Use real-time event timing: a basketball shot should not float for two seconds unless slow motion was requested. Set up anticipation, quick flight/contact and readable recovery; the default playback rate is 1×, not a repair for a slow timeline. The runtime clock is independent of dropped frames.

Set bounds to cover all poses, moving props and shadows, not just the initial geometry. Repeated parts are automatically instanced by geometry and material; reuse palette colors.

Subject-specific objects may be constructed with groups and primitives. For a custom Three.js geometry or material, register it with `W.own(resource)` so teardown disposes it. Do not add controls that require hovering: the scene's story must work on touch without a pointer.

Build a single offline HTML file:

```sh
node <skill>/scripts/build-world.mjs <subject>.js <output.html>
```

The result includes Three.js, generated textures, scene and controls. It is larger than the diorama skill's SVG output: disclose that tradeoff. No CDN imports, stock textures, model downloads or API keys are needed. Keep new external assets optional and disclose their licensing and network cost if requested.

## Prove the actual output

Run the render check on the new scene, not only the bundled examples:

```sh
node <skill>/scripts/look-world.mjs <subject>.js <output-directory>
```

It opens the actual generated HTML in Chromium without network access, saves multiple phases and all four finishes, a mobile view, and a JSON report. For a contact-driven story, declare `contactTimes` and a `contacts({t,parts,W})` inspector returning `{label,a:[x,y,z],b:[x,y,z]}` pairs. The look command compares actual posed endpoints at those times. Also verify ball/prop and palm/bat/hoop coordinates at the named release and contact times. Generic motion and seam checks do not catch a prop missing its actor.

It checks browser errors, visible non-white geometry, scene changes, real wall-clock speed, declared hand/prop contacts, draw-call budget, deterministic seeks, the loop seam, reduced motion, pause, offscreen suspension and disposal. `CHROME_PATH` can select an installed Chromium; otherwise `npx playwright install chromium` in the skill folder installs Playwright's supported browser.

Then **open the saved images and look**. Passing structural checks does not establish likeness, narrative or art quality. Inspect the shot/contact moment, silhouettes, shadows, ground edge, pixel readability, camera clipping and mobile scale. Read [references/art-direction.md](references/art-direction.md), correct failures in the scene and rerun. Keep performance fixes in reusable kit only when the fault is demonstrably there, not because one scene needs a different composition.

For kit changes also run:

```sh
npm test --prefix <skill>
```

Never claim visual review without opening screenshots. Never claim a fresh skill evaluation merely because the two maintained examples pass. A new subject generated from these instructions is the transfer test; save its prompt, output and findings separately. If browser/WebGL is unavailable, report the blocker and leave visual quality explicitly unverified.

## Deliver honestly

Provide the built HTML and at least one reviewed screenshot. State concept, finishes, chosen still time, approximate file size and known limitations. For embedding, see [references/scene-api.md](references/scene-api.md). Do not claim original reference fidelity, accessibility, device performance or a seamless loop beyond what was inspected or measured. The initial public release is not a production-certified renderer; disclose actual limitations and measured checks.
