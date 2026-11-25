---
name: ui-motion-reel
description: Make a Dribbble-grade product motion video, a "showreel" or launch/demo video for an app, site or hackathon project. One UI shape morphs through every screen of the product (never cuts), a cursor drives each change with real clicks, drags and holds, springs animate everything, the camera zooms to fit each state, the last frame loops into the first, and an original soundtrack plus UI sound design is scored to the same timeline. Rendered frame-exact to 1080p60 MP4 with headless Chrome + ffmpeg. Use this whenever the user wants a demo video, promo video, product walkthrough animation, motion graphics, launch video, X/Twitter or LinkedIn video, "showreel", UI animation video, app teaser, or a video for a hackathon submission, even if they don't say "motion reel". Also use it to re-theme, retime, re-score or extend a reel made with it before.
---

# UI motion reel

A reel is one HTML scene rendered frame by frame. Every animated value (shape size, radius, colour, camera zoom, cursor, controls) is a damped spring simulated once up front at 8x the frame rate, so any frame can be rendered independently and in parallel. The score is synthesised from the same timeline, so every beat, click and whoosh lines up with the picture.

The bundled pieces:

- `assets/engine/reel.js`: the engine (springs, measurement, cursor script, camera, content blur-swaps, hover and press, seamless loop, odometer counters, the icon set).
- `assets/engine/score.js`: an original loopable track (pads, plucked arpeggio, bass, drums, risers, bells) plus UI sound design (clicks, whooshes, typing, detents, swipes), rendered with OfflineAudioContext.
- `assets/template/index.html`: a 24 s starter scene with every interaction type: list with row hovers, slider drag, toggle, odometer, hold-to-confirm ring, success pill, summary card, loop back.
- `scripts/setup.sh`: scaffolds a reel folder (engine + template + scripts + node deps).
- `scripts/render.mjs`: stills, audio, and a parallel MP4 render with the score muxed and loudness-normalised.
- `scripts/qa.mjs`: contact sheet, raw loop-seam check, transition strips, loudness and spectrogram.
- `references/api.md`: the full `Reel.define` config reference. Read it before writing a scene.
- `references/craft.md`: the motion and design rules, and the mistakes that were already made and fixed. Read it before designing states.
- `references/score.md`: how to shape the music and sound design, and how to check a mix you cannot hear.
- `references/examples/stockback.html`: the original 60 s, 14-state reel this skill was extracted from (a fintech receipt-to-stocks app). Read it for content ideas and denser choreography. It predates the engine API, so copy patterns, not code.

## Workflow

1. **Learn the product first.** Read the product's site or code for its palette, fonts, logo, and the 5-8 moments that tell its story (the input, the "magic", the proof, the payoff). Pull real copy and real data where you can: real numbers and real logos make the reel believable. If the user asked for a specific look, that wins over the product's own look.

2. **Script the states before you write markup.** For each state decide its size (w, h, radius), fill (one of 3-4 palette colours), camera zoom (so it fills about 80% of the frame height or width), duration, and what the cursor does. Aim for 45-60 s and 10-14 states for a full reel, or 20-30 s and 5-7 states for a teaser. At 120 BPM a beat is 0.5 s and a bar is 2 s. Make every state's duration a multiple of 0.5 s and put the big moments on bar lines (multiples of 2 s) so the music can hit them. Durations must add up exactly to the total.

3. **Scaffold.** `bash ~/.claude/skills/ui-motion-reel/scripts/setup.sh <project>/video`, then edit `<project>/video/index.html`. Keep the engine files unmodified unless the reel needs an engine feature; if so, change the copy in the project and mention it.

4. **Build the scene** following `references/api.md`: one `.content` block per state (`id="c-<id>"`, `data-w`/`data-h` equal to the state's w/h), ids on everything the cursor targets or you animate, then `Reel.define({...})` with states, cursor events, custom channels (sliders, toggles, holds, scrubs) and per-state `update` functions for inner animation.

5. **Review stills early and often.** `node render.mjs --stills 0,1.5,4,...` then look at them (build a contact sheet with `node qa.mjs --every 2`). Check every state at rest and a few mid-morph frames. Rendering stills takes seconds; a full render takes about a minute and a half for 60 s on 6 workers.

6. **Score it.** Set `score` (progression, hits on the key states, breaks) and an `sfx` hook for scene-specific sounds (typing, detents, counters, swipes). `node render.mjs --audio`, then `node qa.mjs` and read the loudness line and `out/qa/spectrum.png` (see `references/score.md`: you cannot listen, so you judge the mix by numbers and pictures).

7. **Render and QA.** `node render.mjs --mp4 --with-audio --out <name>.mp4`, then `node qa.mjs --transitions --video out/<name>.mp4`. Confirm the raw loop seam is 1.000000, look at `transitions.png` for grey mid-morphs or content spilling off-frame, and look at the contact sheet once more.

8. **Deliver** the MP4 (and a 720p copy if a file transfer might struggle with size), plus a short list of what's in it: states, interactions, what the music does. Tell the user honestly that you checked the audio by analysis, not by ear. Offer to retime or re-theme: a re-render is cheap.

## Non-negotiables (the look)

These are what make it read as a designer's reel rather than a template. `references/craft.md` explains each one.

- One shape, never cut. Every state is the same element changing size, radius and fill; content swaps inside it with a short blur (the engine does this).
- A cursor causes every change: a click, a drag, or a press-and-hold. No state changes by itself unless it's a genuine system response (a hold completing).
- Springs everywhere; at most a tiny overshoot (zeta around 0.86 for size, 1.0 for colour and camera). No bouncy easing.
- The camera fits each state; the last frame equals the first so the reel loops.
- No dead time: something meaningful moves at every moment, and the cursor never waits more than about a second.
- No particle bursts, glows, lens flares, gradients on UI chrome, or mismatched icon strokes (use the engine's icon set: one 24 grid, one 1.75 stroke).
- One UI typeface, optionally with one display accent (the template pairs Geist with Instrument Serif italics). Use the product's fonts when it has them.

## Performance notes

- A 60 s reel at 1080p60 is 3,600 frames. With 6 workers it renders in about 80-90 s on an Apple-silicon Mac.
- The scripts call `process.exit` at the end because puppeteer can keep Node alive after the work is done. If you write your own scripts, do the same, or long commands will look hung.
- On networks where large uploads time out, also export a 720p copy: `ffmpeg -i reel.mp4 -vf scale=1280:720 -c:v libx264 -crf 25 -c:a aac -b:a 160k reel-720p.mp4` (ffmpeg is at `node_modules/@ffmpeg-installer/*/ffmpeg`).
