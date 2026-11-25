---
name: camera-moves
description: >-
  Higgsfield-style cinematic camera moves (crash zoom, dolly, orbit, push-in, pull-back,
  handheld) on STILL photos, via monocular depth + a WebGL parallax shader — deterministic,
  beat-lockable, zero credits. Use when a reel needs "filmed" energy on photography: hero
  shots, montage beats, climax punch-ins. Composes with the mograph rig (same GSAP timeline,
  same __seek contract).
---

# Depth-parallax camera moves

A still photo + a depth map + a 60-line shader = a camera operator. Near pixels move more
than far pixels (2.5D), so a lateral slide reads as a dolly and a fast zoom with negative
parallax reads as a crash-in. Unlike AI video generation this is deterministic (same frames
every render), beat-lockable to the grid, and free per use.

## Pipeline

**1. Depth per photo** (once, ~15 s CPU after a one-time ~100 MB model download):
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/depth_map.py photo.jpg <reel>/shots/hero1
```
Writes `hero.jpg` (capped 1440px), `depth.png` (Depth Anything V2 small), and `assets.js`
(both as data URIs — **WebGL refuses `file://` textures as cross-origin**, so the rig must
load data URIs; this is non-negotiable in the headless renderer).

**2. In the reel page** — copy `templates/camera-kit.js` next to the reel and:
```html
<canvas id="cam1" width="1080" height="1920"></canvas>
<script src="shots/hero1/assets.js"></script><script src="camera-kit.js"></script>
```
```js
const shot = CamShot(document.getElementById('cam1'), IMG_SRC, DEP_SRC);
await shot.ready;                                  // BEFORE window.__ready = true
const cues = camPreset(tl, shot, 'crash_zoom', T_DROP-1.6, {dur:2.4});
cues.forEach(c=>AUDIO.push(c));                    // presets suggest their own hits
```
Multiple shots = multiple canvases + one assets.js each (rename the consts per shot:
`const IMG_SRC_2=...` etc, or load sequentially and stash).

## Presets (in camera-kit.js)

| preset | feel | use for |
|---|---|---|
| `crash_zoom` | creep → violent punch-in on a drop → elastic settle | THE climax; lands its own boom+hit cues |
| `dolly` | lateral slide, subject shifts against background | hero holds, montage beats |
| `orbit` | phase-shifted pan+parallax → arc | premium product/portrait moments |
| `push_in` | slow dolly-in | tension, "listen to this" |
| `pull_back` | reverse reveal | openings, context reveals |
| `handheld` | deterministic sum-of-sines drift | documentary energy; keep amp ≤1 |

`{amp}` scales move size; `{dur}` overrides length. Land move apexes on downbeats.

## Craft rules (learned building this)

- **Parallax magnitude ≤ ~0.035** — beyond that, depth-edge stretching shows at silhouettes.
- **Choose photos with layered depth** (subject + midground + background). Flat frontal
  shots waste the effect; the depth map preview tells you instantly.
- **focusD pins a depth plane** (default 0.72 ≈ subject) — that plane stays put, everything
  else moves around it. Lower it to pin the background instead.
- **One move per shot, apex on the beat.** Two simultaneous moves read as drift, not intent.
- **WebGL renders ~3× slower than DOM** in headless Chromium (SwiftShader software GL,
  ~4 fps/frame-write at 1080×1920 vs ~12) — budget render time or keep GL shots to the
  moments that earn it.
- The canvas draws on GSAP's onUpdate, so `__seek` replays are exact — no wall-clock anywhere
  (handheld uses a tweened noise-clock, not Date.now()).

## Read this before you start
`${CLAUDE_PLUGIN_ROOT}/LESSONS.md` — and append what you learn.
