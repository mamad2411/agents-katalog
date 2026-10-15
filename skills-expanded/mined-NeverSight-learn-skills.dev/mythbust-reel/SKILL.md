---
name: mythbust-reel
description: >
  Produce a finished 15-20s vertical Reel/TikTok from nothing but a topic: trend research
  → 6-beat myth-bust script → ElevenLabs narration with word timings → AI B-roll →
  HyperFrames frames + word-by-word captions + punch zooms → its own BGM and SFX →
  full-sweep QA → MP4. Brand-agnostic — reads the client's colours, fonts, voice and copy
  laws from BRAND.md. Use when asked for a short-form reel, TikTok, Shorts, 릴스, 숏폼,
  "make me a reel", a myth-bust video, or a vertical social video for a local service
  business. NOT for long-form edits or static carousels.
---

# Myth-bust Reel — production pipeline

A reel that has to earn distribution in 1.5 seconds, for a real business, from a fixed
pipeline and a creative layer that must change every time.

Two laws:

1. **It must not read as AI-generated.** Every step below has a QA gate for that.
2. **Every new video differs from the last on ≥2 axes** — hook type, format, footage
   style, subject. This skill is infrastructure, not a formula.

The reference build is a 18.7s dental-hygiene myth-bust: *"Stop brushing right after your
iced coffee."* Its beat sheet, timings and cue math are in
`templates/STORYBOARD.template.md`. Copy the structure, never the copy.

## Prerequisites

```bash
scripts/doctor.sh          # checks all of the below and prints what is missing
```

- Node 18+ and `npx hyperframes` (HyperFrames CLI — composition, assembly, render)
- `ffmpeg` + `ffprobe`
- Python 3.9+
- `ELEVENLABS_API_KEY` in the environment (narration + music)
- An AI video generator for B-roll. Scripts here call the `higgsfield` CLI
  (Seedance / Kling); any generator works if it outputs 9:16 MP4 into `public/`.
- `BRAND.md` for the client — copy `BRAND.md.example` and fill it in **before Step 1**.
  Nothing downstream may invent a brand fact that isn't in that file.

## Step 0 — Trend research (mandatory, every video)

Short-form grammar goes stale in weeks. Never build from a remembered formula.

Run a fresh search on the content angle plus current hook formats and caption styles in
the target vertical, then write what you found into `STORYBOARD.md` — later steps cite it.

`reference/viral-grammar.md` holds the 2026-07 baseline (hook rates, completion bar,
caption style, punch cadence, BPM band) with sources. Treat it as a starting hypothesis
to re-verify, not as truth.

## Step 1 — Concept (the variety engine)

If the client has shipped reels before, read their deliverables README first and pick a
concept that differs on ≥2 axes from the most recent one. Same-again is a failure.

**Hook menu** (rotate): negative command ("Stop doing X") · identity call ("If you're the
type who…") · counterintuitive claim · POV realism · specific outcome · unpopular
opinion · pattern interrupt. Whatever you pick, **the hook text is on screen in frame
one** — not after a beat.

**Format menu** (rotate): myth-bust · fear-reversal (dread → relief) · insider POV
("things your [pro] notices") · rule-of-three listicle · seasonal tie-in ·
before/after-FEELING (never fabricated results) · storytime · trend-sound adaptation.

**Copy laws** — from `BRAND.md`, non-negotiable:

- Never deny the client's own category to sound cool ("Spa, not a clinic" kills a real
  clinic's authority). Say what it *feels* like instead: "Feels like a spa."
- Claims only from the approved-language list. No outcome promises the business can't make.
- Brand facts (handle, phone, service area, hours, payment) verbatim from `BRAND.md`.
- An AI person is not a fake customer. The voiceover speaks as the business ("we"); the
  on-screen person enacts the viewer. No "I"-testimonials, no real-person likeness.

## Step 2 — Project setup

```bash
npx hyperframes init "<slug>" --non-interactive --example=blank
cd <slug>
cp <skill>/templates/frames/*.html            compositions/frames/
cp <skill>/templates/caption-skin-tiktok.html .hyperframes/caption-skin.html
cp <skill>/templates/reel.config.example.json reel.config.json
cp <skill>/scripts/inject-broll.py <skill>/scripts/inject-punchzoom.py scripts/
```

Put the brand tokens from `BRAND.md` into the `:root` block each frame template carries
(`--accent`, `--ink`, `--paper`, `--font-display`, `--font-body`), and drop the wordmark
PNG into `public/`. Never re-typeset a wordmark — embed the supplied file.

## Step 3 — Script + narration

Write `SCRIPT.md` from `templates/SCRIPT.template.md`: **6 lines, ~15-18s spoken.**
Faster is better. One idea per line, one frame per line.

```
1 Hook        negative command / pattern interrupt      ~2.5s
2 Mechanism   why it's true, plainly                    ~2.5s
3 Twist       the consequence — the uh-oh beat          ~3.0s
4 Fix         two numbered actions                      ~3.0s
5 Authority   "your [pro] will tell you the same"       ~2.5s
6 CTA         one ask + the objection-killer fact       ~2.5s
```

```bash
export ELEVENLABS_API_KEY=...
REEL_VOICE_ID=<voice> python3 scripts/gen_narration.py .
```

- Calls `/v1/text-to-speech/{voice}/with-timestamps` **sequentially with a 1.2s gap**.
  Character alignment comes back in the response — no Whisper pass, no parallel calls
  (parallel gets you 429s on half the lines and empty word timings).
- Writes `assets/voice/NN.wav` + `audio_meta.json` with per-word cues. **Those cues are
  the timing truth** for frame animation, punch zooms and SFX.
- **Regeneration shifts every length by ±0.5s.** Once frames are cued to the audio, do not
  regenerate. If you must, re-cue everything downstream.
- Frame duration = line duration + 0.3-0.6s tail. End card 3.6s fixed.

## Step 4 — B-roll

Pattern: `scripts/gen_broll.template.sh` (edit the prompts, keep the structure).

- 9:16 · 5s · audio off · one clip per frame. **Generate sequentially** — parallel calls
  rate-limit.
- People: write ONE character description and repeat it **verbatim** in every prompt.
  That's what holds a consistent person across clips.
- Expressions stay subtle. A theatrical wince reads as AI instantly.
- Every prompt names one motion source, states that everything else is still, declares
  the camera grammar (handheld phone vs. documentary), and ends with
  "no warping, no morphing, no extra fingers".
- QA each clip from extracted stills **before** wiring it in; regenerate uncanny takes.
- Real client footage beats any generation. If the client sends phone video, transcode it
  to the same path and it drops straight in:
  `ffmpeg -ss <in> -t <len> -vf "scale=1080:1920:flags=lanczos,fps=30" -an -crf 18`.
  Keep the AI take in `broll-compare/` as a rollback.

## Step 5 — Frames

- Grammar: full-bleed footage, hero words in white with a hard dark shadow stack, the
  brand accent as the ONLY colour accent.
- **Keyword emphasis on bright footage = accent CHIP** (accent background, white text,
  ~12-18px radius). Bare accent-coloured text disappears on glass, tile and daylight.
- **Face-clear layout.** Head positions differ per clip — measure from the actual stills,
  don't assume. Heroes go above or beside the head; captions drop to the lower third
  (~y1480-1500) on person frames and sit centred (y960) on object frames; end-card
  caption y240. Nothing below y1600 (platform UI keep-out).
- Framework rules that break the render if ignored: frame root carries `data-duration`;
  every `<style>`/`<script>` lives inside the `<template>`; one paused timeline registered
  at `window.__timelines["<id>"]`; entrances are `fromTo` on word cues; `power3` easing
  only, never bounce; **no `<video>` inside a sub-composition** — it renders black.

## Step 6 — Assembly (order matters)

```bash
node .hyperframes/captions.mjs build      # word-by-word caption groups
node .hyperframes/assemble-index.mjs      # REWRITES index.html
node .hyperframes/transitions.mjs inject  # needs data-duration on each frame root
python3 scripts/inject-broll.py .         # footage as host-root <video> elements
python3 scripts/inject-punchzoom.py .     # punch zooms on the main timeline
```

- `assemble-index` rewrites `index.html`, so **inject-broll and inject-punchzoom re-run
  after every assemble**. Both are idempotent (marker blocks).
- Injected videos: direct children of the host root, `id` required, and **`z-index:-1`**.
  Without it they cover the frame graphics — and captions survive at z20, so the video
  looks fine while every designed element vanishes. Nasty to debug.
- Punch zooms: ~3s cadence on emphasis cues, scale 1.06-1.12, 0.10-0.14s in. The end card
  never punches; the breather frame (5) takes a soft one at most (≤1.08).
- Both injectors read `reel.config.json`. Keep footage maps and punch cues there, not in
  the scripts.

## Step 7 — Audio identity

**Every video gets its own track.** Reusing a bed across a client's reels makes the set
feel like one template.

```bash
python3 scripts/gen_music.py . --prompt "punchy minimal beat, 125 BPM, ..." --seconds 19
```

- Prompt must carry: genre + BPM (90 lo-fi for UGC · 105-110 calm for trust · 120-130 for
  punchy), "absolutely no vocals", and **"sits UNDER a spoken voiceover, open midrange,
  no swells, no drops, clean ending"**.
- The script registers `bgm` in `audio_meta.json` at volume 0.18 — registration only takes
  effect on the next assemble.
- SFX where the grammar is punchy: `audio_meta.sfx` entries
  `{frame, file, offset_s (frame-local), duration_s, volume}`, files copied into
  `assets/sfx/`. Volumes 0.3-0.5. Whoosh on the hook, soft clicks on enumerated actions,
  one chime on the CTA. They mount only at assemble → re-run Step 6.
- Some caption/SFX helpers in other toolchains **overwrite `audio_meta.json` wholesale**
  and silently drop your bgm + word cues. Wire SFX by hand; back the file up first.
- Mix check: `ffmpeg -af volumedetect` → mean_volume −19 to −20 dB.

## Step 8 — QA (full sweep, never spot checks)

```bash
npx hyperframes lint          # 0 errors before rendering
npm run render
scripts/qa-sweep.sh renders/<file>.mp4 qa/
```

`qa-sweep.sh` pulls every second of the **render** and tiles it into strips — read all of
them. A single-timestamp spot check misses late-landing elements colliding with text that
was already on screen.

Checklist: text-on-text collisions · text-on-face · accent-on-bright contrast · caption
vs. end-card CTA saying the same thing twice · hands, teeth and jewellery artifacts ·
punch timing against the voiceover · first frame legible as a thumbnail.

Fix → re-render → sweep again.

## Step 9 — Deliver

Copy the render to `deliverables/NN-<concept>.mp4`, update the deliverables README table
(concept · length · music · SFX), keep the heavy media out of Git, and open the folder.

Report: the ≥2-axis delta versus the previous video, the research that drove the hook, and
posting-order recommendation.
