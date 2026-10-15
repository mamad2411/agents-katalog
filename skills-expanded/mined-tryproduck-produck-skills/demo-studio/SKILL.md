---
name: demo-studio
description: >
  Build a premium, fully-animated PRODUCT-DEMO / launch motion-graphics video from a written
  brief about your product — the "one seamless film" style: scene-by-scene motion graphics with
  camera moves, real UI mockups, and full sound design, rendered from HTML+CSS+GSAP to MP4 via
  HyperFrames. Use whenever someone wants to "make a product demo video", "launch video",
  "animated walkthrough", "hype/demo reel for <product>", an animated feature or flywheel story,
  or to add any of these set-pieces: a notification/feedback FLOOD of bubbles, real photos of
  people as circular avatars, a GitHub/changelog/release mock, a "context accumulates" web of
  connecting cards, a UI element that MOVES + recolors with the camera following it, a
  contributors wall, an explosion-into-logo endcard, count-up numbers, 3D panel fly-ins, or
  camera zoom/dolly transitions. ALSO covers full SOUND DESIGN — picking the right SFX for each
  animation and placing them (see docs/SOUND.md + the bundled sfx/ kit + templates/). The techniques
  come from a real launch film (https://youtu.be/spaS08Udkyk), but this is a GENERAL-PURPOSE kit: do
  not copy that film's story. Ask the user what THEIR product does, pick a story arc that fits it, and
  re-skin the brand tokens. The bundled example uses deliberately generic placeholder copy. For
  single-concept explainer reels or talking-head edits this is the wrong tool.
license: Apache-2.0
metadata:
  author: produck
  version: "1.0.0"
---

# DemoStudio — the playbook

You are building a **premium product-demo motion-graphics film**: one seamless timeline of
full-screen scenes telling the USER'S story (pick an arc that fits their product, e.g. problem →
product → payoff, before → after, or many inputs → one output; do not default to a feedback-capture
loop), with camera moves between beats. The whole video is **ONE self-contained HyperFrames composition**
(`index.html` = HTML + CSS + GSAP) that renders to MP4, then a single SFX track is muxed on.

**Start from the example:** `example/index.html` is a compact, commented, working scaffold that
shows the whole architecture (paused timeline, 3 scenes, a camera push, a flood, an endcard). Read
it first, then grow it into the real thing scene by scene.

---

## 0. When to use / not use
- **Use** for animated product demos, launch/hype videos, feature stories, flywheel/loop narratives.
  Any "show the product doing something, beautifully, scene by scene" film.
- **Not** for: single-concept explainer reels (one scene per spoken beat), talking-head/CapCut
  edits, or avatar/TTS videos. Different tools entirely.

## 1. Architecture (always the same)
- **One paused timeline:** `const tl = gsap.timeline({paused:true})`; register it on
  `window.__timelines["main"] = tl`. HyperFrames seeks it per frame.
- **Scenes = absolutely-positioned full-frame `<div>`s** inside `#stage`, overlapping in the DOM;
  faded in/out by the timeline. Only the active one is visible at a given time.
- **Schedule by ABSOLUTE time** — the last arg of every `tl.*` call is the start time in seconds.
  Anchor scene offsets with named consts (e.g. `S1`, `S2`, `END`) so changing one shifts the rest.
  A `DUR` const + the `data-duration` attrs (root, bg, stage) must all match the total length.
- **Deterministic only:** no `Math.random()` / `Date.now()` / argless `new Date()` — they break the
  frame-seeked render. Use a seeded PRNG (see the `mul()`/`rnd()` helpers in the example).
- **Build loop:**
  ```
  npx hyperframes lint                       # 0 errors required
  npx hyperframes render --output out/raw.mp4 -q high
  ffmpeg -i out/raw.mp4 -c:v libx264 -pix_fmt yuv420p -g 30 -keyint_min 30 \
    -sc_threshold 0 -r 30 -crf 17 -movflags +faststart out/vNN.mp4     # ALWAYS re-encode
  ffmpeg -ss <t> -i out/vNN.mp4 -frames:v 1 /tmp/f.png                  # verify by viewing frames
  ```
- **gsap defaults:** `gsap.defaults({ease:"power3.out", duration:0.6})`. Register `MotionPathPlugin` if used.

## 2. Brand tokens (re-skin per product) — see docs/BRANDING.md
Everything visual is driven by `:root` CSS vars. To make it *your* product's film, swap the tokens
and keep the system: one canvas colour, near-black ink, exactly ONE restrained accent, status
green/red/blue, a shadow style, and three fonts (display / body / mono). **Keep one focal accent per
scene.** Dark scenes use a deep navy + a warm radial glow, never flat black.

## 3. The technique library — copy these patterns
The full, code-level version is in **docs/ARCHITECTURE.md**. The set-pieces:
- **Text:** typewriter caption (per-char spans + stagger, flip the last word to the accent), kinetic
  fly-in lines (`opacity/y/blur` + stagger), count-up numbers (`tl.call` sets text + a scale punch).
- **People as circular avatars:** any square photo → `border-radius:50%; overflow:hidden` + a name +
  a role/credibility pill. Mix real faces with code-drawn **identicons** (deterministic 5×5 symmetric
  pixel grid) for the natural "not everyone has a face" look.
- **Floods & particles:** scatter with jittered-y + brick-offset-x (don't read as rows), clamp on
  screen; pop in `back.out`; **implode → click → burst** on a ring.
- **Transitions:** 3D fly-in (`rotationY/rotationX/z` + blur → flat), blur-out handoff, edge-on flip
  to swap content unseen, HUD-pill flip to change a label cleanly.
- **Camera (the signature):** it's just `scale` + `x/y` on the scene element. Push/pull, measured
  dolly across a tall element, and a camera that **follows a moving element**.
- **Element moves home:** measure the translate to a target slot, leave a dashed ghost, recolor
  mid-flight, pop a code-diff chip beside it so it references *what* changed.
- **"Context accumulates" web:** SVG lines drawn on (`strokeDashoffset→0`), a hub that grows a notch
  per connection, `+N` badges riding the lines in, a counter ticking up.
- **Explosion endcard:** flash + orange disc + shock ring + ~22 shards + screen shake, revealing a
  value card underneath. Keep it tight (~3s).
- **Realistic SaaS/GitHub UI in pure HTML/CSS:** app windows, nav/subnav, PR rows, a release page
  with per-user credit avatars, diffs that tick green one-by-one. All divs + SVG.

## 4. Gotchas
- `translate(-50%,…)` + GSAP fight over `transform` — center with `xPercent/yPercent` or flex.
- Hidden-then-draw lines/dots: set them hidden at `t=0` or they flash early.
- Scope per-scene CSS under the scene id (`#capture .btn`) to avoid cross-scene collisions.
- **Always re-encode** after render (sparse keyframes → frozen still otherwise).
- `overwrite:"auto"` on tweens retargeting the same property (successive camera scales).
- SVG `transform-origin` is unreliable — prefer `strokeDashoffset` draw-ons / explicit origins.

## 5. Sound design — see docs/SOUND.md + sfx/ + templates/
The film renders **silent**; sound is a separate muxed layer you can re-roll independently.
- The repo ships a complete **all-original SFX kit** in `sfx/` (25 sounds, every one synthesized —
  see `templates/make_kit.py`). Regenerate any time with `python3 templates/make_kit.py`.
- Place cues with `templates/build_audio_kit.py` (edit the `CUES` list of `(time, token, dB, semitones)`)
  → `master.wav` → mux: `ffmpeg -i video.mp4 -i master.wav -c:v copy -c:a aac -shortest out-sound.mp4`.
- **Motion → SFX:** pop=appear, click=click, whoosh=motion, wash=converge, coin cascade=counter,
  confirm(warm muffled)=saved/live, boom=explosion. Full mapping table + mixing rules in docs/SOUND.md.

## 6. Starting a NEW video
1. Copy `example/index.html` into your project (or `npx hyperframes init` and paste the pattern in).
2. Re-skin the `:root` brand tokens to your product (docs/BRANDING.md). Keep the system.
3. Plan the scene beats as a story and lay anchor consts. One accent per scene, no em dashes.
4. Build scene-by-scene, copying patterns from docs/ARCHITECTURE.md. Lint + render + frame-verify each
   scene before moving on. Re-encode.
5. Generate any face photos up front so they bake while you build the timeline.
6. Do the sound pass last: edit the cue list, build `master.wav`, mux the `-sound.mp4`.
