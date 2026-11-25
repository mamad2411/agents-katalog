---
name: still-to-film
description: Turn still images (AI-generated or photos) into a cinematic film with real camera moves instead of a slideshow. Use when someone wants to animate stills, make a trailer or short from images, add depth/parallax to a picture, make a "2.5D" or "Ken Burns but better" shot, cut stills to music, or finish/grade a film made from stills. Pipeline: plates (4x upscale + depth maps) -> beat-grid animatic -> WebGL depth-parallax shots in HyperFrames with motion inside the frame (sprites, water, energy pulses) -> optional Blender CG inserts -> per-shot grade and film finish -> flash/loudness QA. Pairs with the shot-director skill for planning and camera language.
license: MIT
---

# still-to-film

Built while making **HOME**, a 2-minute vertical sci-fi short made from stills with an AI agent. A still that is
only zoomed reads as a slideshow. This skill gives a single image a third dimension (estimated depth + a virtual
camera with parallax and motion blur), puts motion inside the frame, and finishes the result like a film.

Works with any agent and model: everything is plain markdown, Python, JavaScript and shell. Harnesses that support
`SKILL.md` load it automatically; anywhere else, point the agent at this file.

**Plan first.** What to shoot and how the camera moves comes from the `shot-director` skill (six-layer shot specs,
one main move per shot, start/end/holds, choosing moves by feeling, time and space). This skill is how to build it.

## Requirements

| Tool | For | Notes |
|---|---|---|
| Python 3.10+, numpy, scipy, Pillow, OpenCV | all scripts | `pip install numpy scipy pillow opencv-python` |
| torch + transformers | `prep_plate.py` (Swin2SR, Depth Anything V2) | NVIDIA GPU recommended; CPU works, slowly |
| ffmpeg / ffprobe | finish, QA, contact sheets | on PATH |
| Node 18+ and `npx hyperframes` | composing and rendering shots | HTML -> video, seekable GSAP timeline |
| Blender 4.x / 5.x (optional) | CG inserts | headless Python, Cycles |

## Workflow

1. **Story and delivery.** Beats before images. Fix aspect, fps, length and music. Tempo = edit grid
   (125 BPM -> 1.92 s bars). Write the shot list with `shot-director`.
2. **Stills.** One per beat; generate the missing ones to match light, palette, lens and aspect. Credit borrowed images.
3. **Plates.** For each depth shot:
   `python scripts/prep_plate.py still.png --out assets --name s03 --frame 1080x1620`
   Look at the depth map before animating. Add masks if the shot needs them:
   `scripts/water_mask.py` (flowing water), `scripts/energy_mask.py` (pulses on cables/lines), a painted sway mask,
   alpha sprites for anything that should fly through.
4. **Animatic.** The whole film, rough, on the beat grid, with music. Review with contact sheets
   (`scripts/contact_sheet.py`) and by watching. Cut shots here, not later. Burn shot labels + a clock in review mode.
5. **Look test.** Take one shot to final before building the rest.
6. **Production.** Each depth shot is a `depthShot({...})` call in HyperFrames (start from `templates/depth-shot/`).
   Every shot gets something alive inside the frame. Use CG (Blender, WebGL, canvas) only where a still can't do the
   job, e.g. a ship that must fly in (`examples/blender/mothership.py`). Title cards go over a starfield
   (`scripts/make_starfield.py`), not flat black.
7. **Render, finish, QA.**
   `npx hyperframes render` -> `python scripts/finish.py raw.mp4 final.mp4 --shot ... --fade-out ...`
   -> `python scripts/flash_check.py final.mp4` -> contact sheet -> loudness check -> a human watches it with sound.

## Decision points

- **Depth shot or CG?** Depth shot if the camera move stays within the picture (push, pull, small truck/roll).
  CG if something must enter the frame, turn, or be seen from another side.
- **Browser CG or Blender?** WebGL/canvas for graphic, type-led or fast-iterating shots. Blender (headless, Cycles)
  when light must bounce for real, the subject is seen from many sides, or physics is involved; budget hours.
  See `references/blender-route.md`.
- **Footage that won't hold up as a picture?** Don't show it; project it. Use generated or procedural clips as
  light on a blank 3D object in a dark, hazy room, so form comes from 3D and the footage's flicker reads as
  flowing light. See `references/footage-as-light.md`.
- **How far can the camera go?** Push and pull: far (HOME pushed to 5x). Truck/pedestal: small. Pan, tilt and orbit
  beyond about 10% of the frame: no; cut or extend the plate. See `references/depth-renderer.md`.
- **Flat or deep?** Thin planar subjects (rings, glass, signs, water from above) get `pz: 0`.
- **Cut it out or leave it?** Leave heavy or large objects in the plate unless the hole behind them can be filled cleanly.
- **Sound effects?** Default to music only; ask before adding SFX.

## Rules that save rework

- One main camera move per shot, with a start, an end and what stays fixed (from `shot-director`).
- Something moves inside every frame; the camera alone isn't enough.
- No flashes, no on-screen text inside in-world screens, nothing heavy wobbling, unless asked.
- Every frame is a pure function of timeline time: no clocks, no unseeded randomness.
- Decode textures before building the timeline; register `window.__timelines["main"]` after.
- The first frame is the thumbnail on most platforms: never open on black, and open on a frame that works as a cover.
- The agent can't watch or listen in real time: verify with snapshots, contact sheets, `flash_check.py` and
  `volumedetect`, and say so when reporting.

## Files

| Path | What |
|---|---|
| `references/pipeline.md` | each stage in detail |
| `references/depth-renderer.md` | camera parameters, how they map to moves, safe ranges, masks, sprites |
| `references/pitfalls.md` | every failure we hit (renderer, masks, Blender 5.x, ffmpeg, process) and the fix |
| `references/finishing.md` | per-shot matching, film look, sound, encode, delivery for social |
| `references/blender-route.md` | full-CG films in headless Blender: when to choose it, rules, the test loop |
| `references/footage-as-light.md` | projecting moving images onto 3D form: the five roles, build notes, review |
| `assets/depthshot.js` | the WebGL2 depth-parallax renderer |
| `templates/depth-shot/` | minimal working HyperFrames composition (procedural demo assets) |
| `scripts/prep_plate.py` | 4x upscale + depth map for one still |
| `scripts/water_mask.py`, `scripts/energy_mask.py` | masks for water flow and energy pulses |
| `scripts/make_starfield.py` | deep-space plates for cards and backgrounds |
| `scripts/finish.py`, `scripts/finish.sh` | one-pass grade, grain, vignette, music fade |
| `scripts/flash_check.py`, `scripts/contact_sheet.py` | QA |
| `scripts/make_demo_plate.py` | regenerates the template's demo assets |
| `examples/blender/mothership.py` | a procedural CG ship (HOME-specific example) |
| `ROADMAP.md` | what is not generalised yet |
