---
name: reels-editor
description: Edit vertical Instagram Reels end-to-end in this Remotion project (talking-head, unboxing/review, react/reaction reels, tutorials with B-roll). Covers transcription, silence cuts, S-Log3 color grading with skin/teeth care, rotoscopy, captions, SFX, music mix, Instagram safe area and the 2-pass VBR export. Use whenever the user wants to edit, cut, grade, caption, mix or export a reel/short, or mentions "react", "unboxing", "reels", "legenda", "color grading", "slog3", "safe area" or "exportar para Instagram".
---

# Reels editor

Pipeline + reusable scripts + Remotion templates for editing 9:16 reels.
The defaults below were tuned for the original maintainer (Portuguese-speaking creator; reply in the user's language, captions in the language spoken in the video).
Worked example: `examples/` (a real unboxing reel, anonymised).
Everything here was learned on real reels; `references/pitfalls.md` lists what went wrong so you don't repeat it.

## Golden rules (do not skip)

1. **Plan first, then edit.** Probe the footage, transcribe, then present: cut plan, where B-roll/roto/graphics go, duration, open questions. Wait for answers.
2. **Preview before final.** Render a 540p preview (`--scale=0.5`), show key frames, let the user review. Final 1080p render + export only when they ask ("pode renderizar").
3. **Measure, don't guess.** You can't hear or see in real time: use ffmpeg `ebur128`/RMS for audio, `scripts/patch.mjs` (Lab/HSV) for skin and teeth, contact sheets for frames, `cropdetect`/pixel scans for centering. Say plainly what you did **not** verify (e.g. "I didn't listen to the audio").
4. **Instagram safe area** for every text/graphic (see `references/captions-safe-area.md`): top 300 px, bottom 480 px (text ends at y=1440), sides **symmetric 130 px** so everything is centred on x=540. Full-bleed footage/B-roll may ignore it.
5. **Final export = `scripts/encode-instagram.sh`** (H.264 High, 2-pass VBR 12/16 Mbps, closed GOP 2 s, BT.709, AAC 256k 48 kHz, −14 LUFS, TP −1.5). Never ship the raw Remotion output.
6. **Corrections are on-screen titles, not cuts** (creator said the wrong word → `Correction` template over the live video).
7. Don't commit renders, `public/roto`, `whisper.cpp`, `work/`, or the exported `out/` files; follow the user's own commit/PR rules.

## Creator defaults (the maintainer's preferences — edit this section for your own channel)

- Format 1080×1920, 30 fps, vertical. Camera: Sony **S-Log3 / S-Gamut3.Cine**, files carry a rotation tag (ffprobe shows 3840×2160 but frames are 2160×3840 portrait → no crop needed). Audio: **safety track** (ch2 ≈ −6 dB of ch1; use ch1, ch2 as fallback for clipped words).
- Brand: default palette (edit `templates/remotion/palette.ts`) → `#040404 #40E4C9 #4817ED #F13D6D #FF5E1E #8E2EE8`. UI/caption font **Montserrat ExtraBold** (`font.ts`); display fonts without accents/`@`/`_` glyphs — never use it for captions.
- Captions: 2–4 words per page, mixed case, ~54 px, white + dark stroke, **no animation, no emoji, no per-word colors**, centred. No captions on silent/effect moments (montage cuts, the megaphone gag).
- Cuts: remove silences hard ("corte ao máximo"), but keep word tails (pad-in 0.09 s / pad-out 0.15 s) or the audio sounds choppy. Hooks: open with the most intriguing line/graphic.
- SFX: tasteful, at transitions/graphics only. **No SFX on handling/unboxing shots** (user hated crinkle/boom there). Music: user supplies; pick the section by beat grid (dips every 2 bars), −27 LUFS bed vs voice −14, small swell when nobody talks, fade-out last 3 s.
- Skin must not look red (target sat ≈ 0.35–0.55 on cheeks) and teeth must not look yellow (target Lab b* ≈ 20–30). Check with `patch.mjs` after any grade change.
- Duration: the maintainer asked for 1:20–1:30; offer to tighten hesitations ("né?") when over target.

## Workflow

Detailed commands: `references/pipeline.md`. Summary:

| # | Step | Tool |
|---|------|------|
| 0 | Intake: reel type, goal, target duration, brand assets, music, CTA/@handle | ask the user |
| 1 | Probe media (rotation, fps, audio channels, levels) | `ffprobe`, `ffmpeg astats` |
| 2 | Extract audio ch1/ch2 16 kHz → transcribe | `scripts/transcribe.mjs` |
| 3 | Fix transcript where Whisper fails (quiet/noisy parts, hallucinations) | re-transcribe boosted windows, RMS check |
| 4 | Silence cuts + manual montage list → **present the cut plan** | `scripts/silence-cuts.mjs` |
| 5 | Grade LUT (S-Log3→Rec709 + look + skin/teeth) → 3–4 test frames | `scripts/make-lut.mjs`, `patch.mjs` |
| 6 | Build master (graded, cut, voice chain, −14 LUFS) | `scripts/build-master.mjs` |
| 7 | Re-transcribe the **master** audio → align word times to audio energy → captions data | `transcribe.mjs`, `align-captions.mjs`, `group-captions.mjs` |
| 8 | Rotoscopy for the few windows that need it | `scripts/roto.sh` |
| 9 | Compose in Remotion (copy templates) + SFX + music | `templates/remotion/*` |
| 10 | Preview 540p, key-frame contact sheet, loudness check → iterate | `remotion render --scale=0.5` |
| 11 | Final render (jpeg-quality 100, crf 10) → Instagram encode | `encode-instagram.sh` |

## Reel types

- **Talking-head / unboxing / review** → `references/pipeline.md` + the templates in `templates/remotion/`.
- **React reel** (creator reacts to someone else's video) → `references/react-reel.md` + `templates/remotion/ReactReel.tsx` (layouts `stack`, `pip`, `cutout`).
- **Tutorial / voice-over with B-roll** → same pipeline; B-roll windows tied to caption times; no roto.
- New type? Reuse the pipeline, add a section to the relevant reference, and keep this table updated.

## Files

npm shortcuts (project root): `bun run reel:cuts|lut|master|captions|roto|encode -- <args>` map to the scripts below.

- `scripts/` — `transcribe.mjs`, `align-captions.mjs`, `silence-cuts.mjs`, `make-lut.mjs`, `build-master.mjs`, `roto.sh` + `roto.swift`, `group-captions.mjs`, `patch.mjs`, `encode-instagram.sh`
- `templates/remotion/` — `safe.ts`, `font.ts`, `palette.ts`, `Captions.tsx`, `LowerThird.tsx`, `Correction.tsx`, `RotoFrame.tsx`, `SfxMusic.tsx`, `ReactReel.tsx` (copy into `src/<ReelName>/`; install `@remotion/google-fonts` and `@remotion/media`)
- `examples/` — `example.reel.config.json`, `example-ranges.json`, `example-caption-fixes.json`
- `references/` — `pipeline.md`, `react-reel.md`, `color-grading.md`, `audio-music-sfx.md`, `captions-safe-area.md`, `rotoscopy.md`, `instagram-export.md`, `pitfalls.md`

For Remotion API questions use the sibling skills (`remotion-best-practices`, `remotion-captions`, `remotion-render`).
