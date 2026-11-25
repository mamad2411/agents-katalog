---
name: viral-tech-reel-editor
description: End-to-end viral tech reel production for Instagram Reels and TikTok using 2026 trend grammar — retention-first pacing, punch-ins, 3D cinematic AI-generated shots, motion design graphics, proof b-roll, trending SFX, karaoke captions (Georgian/English), safe-zone layout, and QA-gated 1080x1920 export. This skill should be used when the user asks to edit, montage, cut, caption, or finalize a vertical video/reel from talking-head, screen recording, voiceover, or mixed footage (e.g. "დაამონტაჟე", "რილის ედითი გააკეთე", "edit this reel", "add captions and b-roll"). Not for script-only writing (viral-reel-generator) or static posts (georgian-smm).
---

# Viral Tech Reel Editor (2026)

Premium, retention-first vertical reel production: understand the video, transcribe precisely, design the timeline, build all visual/audio layers, render, and self-check before delivery. Treat every edit as a full production pass, never a captions-only pass.

## Start Rule

For every end-to-end edit, create a Goal if a Goal/Todo tool is available, covering the FULL delivery (not just the first technical step). Otherwise maintain an explicit written checklist. Do not mark complete until final export AND the QA gate pass. Before any work, load `references/style-memory.md` — it contains binding user preferences and prior feedback.

## Full Framework Rule

Never deliver a plain "clean baseline" talking-head edit unless the user explicitly requests a minimal edit. A valid edit applies ALL pillars:

1. **Pacing** — visual-change rhythm (punch-ins, overlay/b-roll swaps, reveals) tied to beats. **Default = NO-CUT: the creator's A-roll is already edited — never trim, chop, or silence-cut the host's voice track.** Only run `scripts/silence_cut.py` if the user explicitly asks for cutting on a raw, uncut recording.
2. **Main-shot motion** — punch-ins, zoom-outs, reframes, visual resets tied to key words and story beats.
3. **Proof layer** — contextual b-roll: product/UI footage, extracted promo clips, window-only screen recordings, diagrams, recreated demos that clarify the spoken idea. **AUTO by default**: resolve every proof beat automatically by walking the b-roll ladder in `references/broll-sourcing.md` (owned → official → contextual free stock → recreate → AI-generate) — never ask per-insert; only escalate on a rights/safety/fabrication blocker.
4. **Cinematic layer** — at least one 3D/AI-generated cinematic or high-end motion set-piece on the hook or payoff (see `references/cinematic-3d.md`).
5. **Motion design** — kinetic typography, lower thirds, counters, HUD/diagram animation where they clarify.
6. **Sound design** — license-clear trending SFX mixed clearly under speech; loudness-normalized output.
7. **Captions** — word-accurate karaoke captions, Georgian/English term accuracy, safe placement.
8. **Layout** — deliberate vertical canvas use with ZERO collisions (face, hands, captions, PiP, UI, diagrams).
9. **QA evidence** — contact sheet, loudness report, and a note stating which pillars passed (`scripts/qa_report.py`).

If a pillar cannot be applied: source, download, record, recreate, generate, or design the missing layer. If still impossible, state the blocker in QA notes and ask the user. Convenience is never a valid reason to omit b-roll, SFX, punch-ins, or pacing work.

## Edit Profile (tune before building)

Set these from the user request + style memory; state chosen values in the plan.

| Parameter | Range | TikTok default | IG Reels default |
|---|---|---|---|
| EDIT_INTENSITY (visual-change density — NOT voice cutting; A-roll stays intact) | 1–10 | 8 | 7 |
| MOTION_DENSITY (punch-ins/graphics movement) | 1–10 | 7 | 6 |
| SFX_DENSITY (SFX per 10s) | 1–5 | 3 | 2–3 |
| CINEMATIC_RATIO (generated/3D share of runtime) | 5–30% | 15% | 15–20% |
| CAPTION_PRESET | minimal-pro / kinetic-bold / karaoke-clean | kinetic-bold | minimal-pro |

Higher intensity = more frequent visual changes (overlay/b-roll swaps, punch-ins, reveals), NOT shorter voice segments — the host's track is never re-cut. Tech-explainer content for Tornike's audience usually sits at intensity 7 with proof-heavy layers rather than gimmick transitions.

## Core Workflow

1. **Intake**: source files, platform(s), target duration, language, CTA, brand layer. Prior user feedback = binding style direction.
2. **Transcribe first**: `scripts/elevenlabs_stt.py` (ElevenLabs Scribe, word timestamps) → `scripts/elevenlabs_words_to_captions.py` for caption groups/SRT/VTT. Fall back to Whisper/HyperFrames transcription only if ElevenLabs is unavailable.
3. **Understand before editing**: build a beat map — hook, context, proof/demo, tension, payoff, CTA. Verify names, model numbers, technical terms, Georgian/English wording. Identify spoken search keywords (2026 social-search ranking — keep them audible and captioned).
4. **Trend pass**: read `references/trends-2026.md`. If its snapshot is >30 days old or the user asks for "latest trends", refresh it per the instructions inside.
5. **Plan all layers on the beat map**: cut plan (`scripts/silence_cut.py`), proof b-roll plan (`references/broll-sourcing.md`), cinematic set-pieces (`references/cinematic-3d.md`), motion graphics + SFX map (`references/motion-grammar.md`, `references/sfx-palette.md`).
6. **Choose build path** (`references/tooling.md`): FFmpeg for base cut/audio/packaging; HyperFrames for HTML-first overlays, captions, diagrams (MCP `compose` in claude.ai, CLI locally); Remotion for frame-accurate React/3D components; Higgsfield/imagegen for generated shots.
7. **Layout before animation**: generate the platform overlay with `scripts/safe_zone_overlay.py` and design against it (`references/captions-layout.md`).
8. **Motion pass**: apply the grammar in `references/motion-grammar.md` — cut rhythm, punch-in sizes, easing tokens, transition whitelist, beat/speech-accent sync.
9. **Build and validate**: lint/still-frame checks in the chosen tool; inspect hero frames and the densest caption moments before rendering.
10. **Render and QA**: run `scripts/qa_report.py` (stream info + loudness + contact sheet), then walk `references/qa-checklist.md`. Deliver a phone-openable file/link + QA notes listing pillar evidence. Append distilled feedback to `references/style-memory.md`.

## Non-Negotiables

- **NO-CUT (A-roll integrity)**: the creator's recording is pre-edited. Never cut, trim, shorten, or silence-trim the host's voice/main track. Final A-roll duration must equal the source. Add value by layering OVER the timeline, never by re-cutting it. (Cutting only on explicit request for a raw recording.)
- **Audio = SFX only by default**: no background-music bed for this creator unless explicitly requested. Keep voice + contextual SFX. If a bed is ever requested, it stays heavily ducked.
- **Fill the canvas**: when the host is in PiP or a partial layout, the rest of the screen MUST be filled — full-bleed b-roll, full-screen motion/infographic, or split-screen. Large persistent dead bands (especially below captions or beside a PiP) are a QA fail. Only a small, deliberate margin around a single hero element counts as breathing room.
- **Layer order is fixed**: the host (face) is always the TOP visible layer — never behind an infographic or b-roll. Captions never land on the face/mouth or on the PiP. B-roll never covers the PiP when free space exists. Zero element collisions at any frame.
- **PiP variety**: rotate the host's PiP across different corners AND shapes through the reel; never one static corner/shape. In PiP the face must sit fully inside the frame, centered — never cropped at the chin or top.
- **Image fit**: inserted photos/screenshots use `contain`, centered, key subject never cropped; pad to the frame, never crop to fill.
- **Transitions clean + on-trend**: use 2026-trend transitions (flash / whip / pink camera-flash / CapCut "Glare II"-style) deliberately; never leave transition residue, stray frames, or janky zoom. A "dirty" transition is a fail.
- Maximize canvas use, never by stacking conflicting elements.
- Never cover the speaker's face, mouth, chin, eyes, expressive hands, or critical on-screen UI with any overlay.
- Captions, cards, labels, PiP panels must never collide with each other.
- Never use random stock b-roll as filler. Every proof visual must prove, clarify, or intensify the spoken idea.
- Never skip the proof layer just because the source is talking-head — create it (diagram, recreated UI, source card, window recording).
- Skip promo moments containing presenters/unrelated humans unless explicitly requested; prefer product UI, demos, cursor actions, terminal output, before/after.
- Screen recordings: capture only the relevant app/window or crop tightly. Never include the whole desktop, private files, notifications, API keys, unrelated windows.
- SFX support a specific event (cut, zoom, reveal, caption pop, typing beat, riser) — audible but never fighting the voice. No SFX-on-every-cut.
- Keep Georgian and English technical terms exact. Never introduce Russian. Never render tofu glyphs — verify the font supports Georgian before use.
- Mark photoreal AI-generated segments per platform disclosure rules (TikTok/IG AI labels, 2026).
- Avoid everything in `references/anti-slop.md`. Prefer native social rhythm: fast, clear, proof-heavy, visually alive.
- **Render-safety (HyperFrames)**: never `setpts`-slow a clip (renders black — loop with `-g 15` instead); one `<video>` per `data-track-index`; never duplicate the host/face `src`; chunk Scribe for long audio; Georgian needs line-height ≥ 1.3 + `display:block` stacked node labels; INSPECT RENDERED FRAMES, not lint. Full list: `references/hyperframes-render.md`.
- Deliver phone-openable files/links plus what was checked. Never stop at localhost or an unrendered source file.

## Reference Routing (load only what the task needs)

| File | When to load |
|---|---|
| `references/workflow.md` | Full production pass, artifact/folder structure, multi-platform delivery |
| `references/tooling.md` | Choosing/driving ElevenLabs, HyperFrames, Remotion, FFmpeg, Higgsfield, imagegen |
| `references/hyperframes-render.md` | HyperFrames render gotchas: black/empty cards, video-per-track, slow-vs-loop, Scribe chunking, fonts, frame-inspection (load before any HyperFrames render) |
| `references/trends-2026.md` | Every serious edit (trend pass) + refresh protocol |
| `references/motion-grammar.md` | Cuts, punch-ins, speed ramps, transitions, easing, motion-graphics kit, beat sync |
| `references/cinematic-3d.md` | 3D cinematic set-pieces, AI video generation, 2.5D parallax, Remotion+Three |
| `references/broll-sourcing.md` | Proof visuals: promo extraction, recordings, recreated UI, source safety |
| `references/sfx-palette.md` | SFX selection, sourcing, event mapping, mix levels |
| `references/captions-layout.md` | Caption grouping/typography (Georgian fonts), safe zones, PiP, collisions |
| `references/anti-slop.md` | Before locking the design + final self-scan |
| `references/style-memory.md` | ALWAYS first; append after delivery |
| `references/qa-checklist.md` | Final gate before delivery |

## Scripts

| Script | Usage |
|---|---|
| `scripts/elevenlabs_stt.py` | `python scripts/elevenlabs_stt.py input.mp4 --out transcript.json [--language-code ka]` — Scribe STT with word timestamps (needs `ELEVENLABS_API_KEY`) |
| `scripts/elevenlabs_words_to_captions.py` | `python scripts/elevenlabs_words_to_captions.py transcript.json --out-json captions.json --out-srt captions.srt --out-vtt captions.vtt` — word groups for karaoke captions |
| `scripts/silence_cut.py` | `python scripts/silence_cut.py input.mp4 --plan cutplan.json [--render tight.mp4]` — silence detection → cut plan → optional tightened render |
| `scripts/safe_zone_overlay.py` | `python scripts/safe_zone_overlay.py --platform tiktok --out overlay.png` — safe-zone PNG + ffmpeg preview command |
| `scripts/qa_report.py` | `python scripts/qa_report.py final.mp4 --outdir qa/` — stream specs, LUFS/true-peak, contact sheet, pass/fail report |
