---
name: pick-engine
description: Choose the rendering engine(s) for a video beat or a whole piece - GSAP, SVG rig, Lottie, Rive, Pixi, Three.js, Blender, page capture or footage - from the look wanted, the assets available and the render cost. Use while writing a storyboard or when asked "what should we use for this?"
---

# Picking an engine

The full table and the determinism rules are in `engines/README.md`. Read it first.

Pick the look first (`looks/README.md`): it names its usual engines (neon-noir → Three.js `emissive` + `bloom`,
photoreal → `realistic` + `pbr` or Blender Cycles, toon-3d → `toon` + `outline`, editorial and kinetic-type → GSAP).
Then use the questions below for each beat.

## Decide by asking, in order

1. **Is it mostly text, UI or layout?** → GSAP only. Most ads are this. Stop here unless a hero visual is needed.
2. **Is there a character?**
   - A designer gave a Lottie (`.json`) → Lottie.
   - A designer gave a Rive (`.riv`) → Rive (`engines/rive.js`; state machines take timed inputs).
   - No designer file → SVG rig (`engines/svg-rig.js`). Draw it from simple shapes in the brand colours.
   - It speaks the voiceover → add lip sync (`scripts/lipsync.sh` + `engines/lipsync.js`) to whatever draws it: SVG
     rig, the brand's mascot PNG, Three.js or Blender. Seconds per line; it is not an extra engine to justify.
3. **Is the hero a physical product or a 3D object?**
   - Real CAD or a GLB model, or camera moves around an object → Three.js. Realistic: `realistic()` + `pbr()`;
     glowing: `emissive()` + `bloom()`.
   - Wants soft light, a premium look, or physics (cloth, liquid, many falling objects) → Blender plate.
   - Cartoon 3D: Three.js `toon()` + `outline()` for speed; Blender `toon()` for quality.
4. **Does the brand already have a live web page with the visual (a 3D scene, a web app)?** → page capture. It reuses
   real work and shows the real product.
5. **Lots of small moving things (confetti, particles, crowds)?** → Pixi on top.
5b. **Between scenes:** a hard cut on the beat (`Studio.swap`, `Studio.bar(n)`) is the default. `Studio.transition`
   (wipe, iris, push, slide, zoom, whip, blinds, flash) works on any layer; `engines/gl-transitions.js` (dissolve,
   ripple, zoom blur, glitch, pixelate) only between layers with pixels (Three.js, Pixi, plates, images).
6. **Real people or places?** → footage plate (stock or AI video). Check the brand's compliance on AI disclosure.
   Never use generated footage to show product features.

## Costs to weigh

| Engine | Render cost (6 s at 1080×1920, M-series Mac) | Change cost |
|---|---|---|
| GSAP / SVG / Lottie / Pixi / Three.js | seconds (demo: 16 s for 180 frames, all engines) | edit HTML, re-render |
| Blender (Eevee) | ~9 s per second of video at 540×960 for the simple example scene, including start-up; much more for full size, complex scenes or Cycles | edit the Python scene, re-render the plate, then the composition |
| Page capture | ~1 s per frame (the Bike Logger capture took ≈5 min for 28 s) | re-drive the page, re-capture |

## Write the choice down

In the storyboard's *Engines* field and per beat: the engine and one reason ("Three.js: real CAD of the box,
camera orbit"). More than two engines in one piece → justify it or simplify.
