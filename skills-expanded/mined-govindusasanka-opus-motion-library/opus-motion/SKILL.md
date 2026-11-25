---
name: opus-motion
description: Choose, mix and integrate motion graphics from the Opus Motion Library — ~605 parameterised Remotion motions (titles, backdrops, weather, particles, characters, data/HUD, UI mockups, image looks, 3D), 97 transitions, 148 styles and 33 ready-made recipes. Use when the user wants a specific motion ("do the sonar ping", "a stamp slam that says X"), several motions mixed into a shot or video, a narrated explainer, OR animated backgrounds / heroes / stats / loaders / celebration states in a website, web app (React, Next.js, Vite, plain HTML, WordPress), native app (exported mp4/webm-alpha/ProRes) or slides — including when the library has been copied or linked into another project.
---

# Opus Motion Library

Root: the folder this repo is cloned into, or the
copy inside the current host project. **Read `AGENTS.md` there first** — decision procedure, layering rules,
web performance rules and anti-patterns. Then `docs/CHOOSING.md` (intent → motions) and `docs/INTEGRATION.md` (per stack).

## 1. Choose (never guess from memory)
- `node cli/mgl.mjs suggest "<the brief in the user's words>"` — ranks ★ recipes and motions, says why, prints a
  props snippet. Filters `--overlay --image --text --loop --light --category <c> --json`.
- `node cli/mgl.mjs recipes` — ready mixes (previews `recipes/previews/<id>.jpg`): hero-aurora-night, hero-paper-sketch,
  hero-blueprint-logo, product-launch, stats-reveal, testimonial-chat, testimonial-quote, loading-loop, section-divider,
  success-celebration, error-glitch, onboarding-steps, event-countdown, music-neon-promo, ocean-explainer,
  history-timeline, app-store-preview (9:16), social-short-captions (9:16), end-card.
- `node cli/mgl.mjs info <id>` — props + `roles`, `overlay`/`overlayProps`, `loopable`, `mood`, `weight`, `pairsWith`, `textProps`.
- Mix = backdrop + subject + type + subtle accent; one hero per shot; dim supporting layers; replace ALL sample text;
  pass the brand colours.

## 2. Video (Remotion)
```bash
node cli/mgl.mjs render <id> --props '{"key":"value"}' [--format landscape|square|portrait] [--frames N] --out out/<name>.mp4
node cli/mgl.mjs recipe <id> --overrides '{"<motion-id>":{…}}' [--format …] --out out/<name>.mp4
node cli/mgl.mjs still <id> --at 10,60,120 --out out/<name>-sheet.jpg     # preview first, Read the sheet
node cli/mgl.mjs compose specs/<name>.json --out out/<name>.mp4             # scenes[] (motion or layers[]), transitions, overlays, audio
node cli/direct.mjs storyboards/<name>.json                                 # narrated: local Qwen3-TTS -> captions -> render -> master
```
Images: public/ paths (`"demo/owl.jpg"`) or https URLs. Never use cloud voice/music services; music/sfx from `public/music`, `public/sfx`.
Inside another Remotion project: `node cli/mgl.mjs add <motions|recipes> --to <host>/src` (copies only needed source + local registry; prints the npm install line).

## 3. Website / web app
- `npm run build:lib` in the library, then `import {MotionBackground, MotionPlayer, MotionMix} from 'opus-motion-library/web'`
  (Vite: `resolve.dedupe` react/remotion/@remotion/*/three), or `mgl add … --player --to <app>/src` (Next.js: use from a `'use client'` file).
- Plain HTML / WordPress / Vue / Svelte: `<script src="opus-motion.element.js">` + `<opus-motion recipe="…" background>` /
  `<opus-motion motion="…" props='{…}'>`.
- Words in HTML over `MotionBackground` (it drops `type` layers); `overlay` motions float over the page; `playOnView`,
  reduced-motion still frame, lazy mount, ≤ 2 live players per viewport; heavy 3D → exported video on mobile.
- Serve the library `public/` files used (or `assetBase` / absolute URLs).

## 4. Native apps, slides, editors
`node cli/mgl.mjs export <motion|recipe> --as mp4|webm|webm-alpha|prores-alpha|gif|png|poster [--format …] [--props …]`
(alpha exports apply `overlayProps`; check with `ffprobe -c:v libvpx-vp9 … pix_fmt` → `yuva420p`).

## 5. Check before handing over
Tile the render (`ffmpeg -i out/x.mp4 -vf "fps=1,scale=480:-2,tile=6x5" -frames:v 1 out/x-sheet.jpg`) or screenshot the page
(`node examples/screenshot.mjs <url> <dir> --targets "top,#section"` — two shots 1 s apart, reports % changed), Read it, fix.

## Adding a motion to the library
Follow `docs/AUTHORING.md`, put it in `src/motions/<family>/<id>.tsx`, run `node cli/gen-registry.mjs && npx tsc --noEmit && node cli/gen-docs.mjs`;
optionally `node cli/probe-meta.mjs --only <id>` (measures loop / overlay / luma) and add overrides in `docs/motion-meta.json`.
