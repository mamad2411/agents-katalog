---
name: video-studio
description: Make a short brand or promo video in code with Claude Code and HyperFrames (HTML + GSAP, rendered locally to MP4) — the direction brief, project layout, settings-first editing, sound, craft rules, review rules and the build loop. Use when asked for a promo, launch, explainer or social video made in code, or to change one. For exporting and checking the final files, load video-delivery. For paid AI-generated realistic shots, load ai-video-shots.
---

# Make a brand video in code

Code renders exact words, numbers, UI screens and brand colours perfectly every time. That is
what this skill is for: 30–60 s videos built from big moving words, mock UI screens, a simple
character drawn in SVG, music and sound effects, rendered locally with
[HyperFrames](https://hyperframes.heygen.com).

A full worked example (a 45 s recruiting video) is in `example/` of this repo. Reuse its tools and
helpers; write a new story for every new video.

## Setup (once per project)
1. `npx skills add heygen-com/hyperframes` inside the project. This installs the HyperFrames
   skills (core, animation, audio, CLI, media) that this skill builds on.
2. Copy `example/lib`, `example/tools`, `example/styles.css` and the shape of
   `example/settings.js`. Get the assets listed in `example/ASSETS.md`.
3. Pin one HyperFrames version and use it everywhere (`npx --yes hyperframes@<version> ...`).

## Your brand kit (fill this in first)
Background colour, 1–2 accent colours, a "joke" or contrast colour if the story has a before/after,
fonts (local files, never loaded from the internet at render time), a vector logo (SVG — PNG logos
go blurry at 4K), tagline, website. Write it at the top of `settings.js`.

## Facts rule
Every number on screen comes from the owner, with its meaning. Ask before using any other figure.
Joke labels ("version 37") are fine; invented performance counters are not. No real customer
names or faces unless the owner says so.

## The build, step by step
1. **Direction brief**, one short paragraph each: audience · the one action we want · the opening
   frustration (frame 0 must already show a problem, not an action) · the proof (real figures
   only) · the ending invitation.
2. **Storyboard table**: time · on screen · big words · what the viewer should notice.
   Get 2–3 variants and pick one. Check the jokes aren't lifted from your reference video.
3. **Ask for a reference song** on day one (any song, only for measuring). See `references/sound.md`.
4. **Stills before motion**: one designed still per scene (`hyperframes snapshot`), approved
   before anything moves.
5. **Build with a subagent** from a written spec. Write rhythm in seconds (holds 0.2 / 0.4 / 0.6 s,
   which cuts are hard): uniform easing and pacing is the giveaway of AI-made video. Expect many
   rounds; one-shot is a myth.
6. **Before every render**: `hyperframes lint` + `check` clean; a review pass lists problems as
   P0 (broken / wrong fact) / P1 (hurts the video) / P2 (polish); every number checked.
7. **Review** (below), fix, get an independent review of the finished render, fix, then load
   `video-delivery`.

## Settings rule
Every word, number, scene time, colour, music and sound-effect time lives in `settings.js`, one
per line, with a plain-English comment, so a non-developer can change the video by editing one
line. HyperFrames needs audio timing as static `<audio>` attributes, so
`node tools/sync-audio.mjs [file.html]` writes them from `settings.js`. Run it after changing any
music or SFX time.

## Review rule (never approve from a report or a contact sheet alone)
- Fresh render + matching contact sheet from the same code.
- Full-size frames at every scene change (+0.15 s) and every punchline.
- Watch and listen at full speed; then muted at phone size (~400 px wide).
- Counters land and hold; no frame shows two scenes at once; no word cut at the edges.
- A subagent's "done" is a claim: re-run its check yourself.

## References in this skill
- `references/craft.md` — readability sizes, easing, holds, transitions, layouts for other shapes.
- `references/sound.md` — music, free sound effects, mixing, licences.
- `references/speed.md` — the cheap fast loop, render speed, tokens and model routing.
- `references/troubleshooting.md` — every gotcha we hit, with the fix.
