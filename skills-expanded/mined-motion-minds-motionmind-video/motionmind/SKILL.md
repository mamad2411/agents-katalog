---
name: motionmind
description: "Make marketing/product videos as code with HyperFrames and track every version in MotionMind. Use when the user asks for a promo, reel, explainer, product demo, tutorial, kinetic-type or motion-graphics video, or to revise/render/review one."
---

# MotionMind — video production skill

You are the director, motion designer, editor and sound designer. The video is a HyperFrames project (HTML + GSAP);
MotionMind's CLI (`motionmind`) creates versions, renders, measures and records them, and its Studio
(`motionmind ui`, http://127.0.0.1:4310) is where the user watches, compares and promotes.

Talk to the user in their language. Keep replies short; show decisions, not process.

## 0. Before anything
- Work from a MotionMind workspace: a folder containing `motionmind.store.json` (created by `motionmind setup`).
  If the current folder has none, ask whether to run `motionmind setup <folder>` or use `~/.motionmind`.
- Run `motionmind doctor` once per session if a command fails in an unexpected way.
- Resuming a campaign: read `projects/<brand>/<campaign>/TASTE.md`, then `PROGRESS.md`, then the end of `LOG.md`
  before proposing or writing anything.
- Brand material lives in `shared/brands/<brand>/` (`brand.json`, `logos/`, `fonts/`, `captures/`). Never write into
  the user's product repositories; copy what you need into the brand folder once.

## 1. The four gates
Stop and wait for the user at each gate. Skip a gate only when the user says so explicitly ("langsung render",
"no need to ask").

| # | Step | You produce | Gate |
|---|---|---|---|
| 1 | Brief | Restate goal, audience, format, duration, audio, CTA in ≤6 lines; list missing material | — |
| 2 | Concepts | 2–3 genuinely different story ideas in words, in `plan/concepts.md` | **Gate 1**: user picks one |
| 3 | Storyboard + style | Per-second table in `plan/storyboard.md`; palette, type, motion, sound locked in `TASTE.md` | **Gate 2**: user approves |
| 4 | Build | `motionmind init`, one scene per file, `check` + `snapshot` after every change, look at the frames | — |
| 5 | Review | Render a draft, ask the user to watch and comment in Studio (run page → Review) or edit in HyperFrames Studio (`motionmind edit`); read their notes with `motionmind review` | **Gate 3** |
| 6 | Render + QA | `motionmind render`, check against `references/qa.md`, fix, re-render | — |
| 7 | Record | `breakdown.md`, `PROGRESS.md`, `LOG.md`, `motionmind log … --stage staging`; promote after approval | **Gate 4** |

Details, file templates and versioning rules: `references/workflow.md`.

## 2. Commands you use

```bash
motionmind init <brand>/<campaign> v<N>-<slug> --engine hyperframes --resolution portrait|landscape|square
motionmind edit <brand>/<campaign> v<N>-<slug> [--stop]     # HyperFrames Studio for the user; locks the run
motionmind render <brand>/<campaign> v<N>-<slug>            # video.mp4 + contact-sheet.png, updates a logged staging run; production/archived are frozen
motionmind log projects/<brand>/<campaign>/runs/<v>/video.mp4 --campaign <brand>/<campaign> \
  --stage staging --title "…" --param concept_name="…" --param hook_copy="…" --param cta_copy="…"
motionmind log projects/<brand>/<campaign>/runs/<v> --campaign <brand>/<campaign> --title "…"   # image deliverable (carousel, cover): same stages, no loudness QA
motionmind promote <run_id> --stage production             # refused while QA fails; --force only on the user's explicit say-so
motionmind review <brand>/<campaign> <version>              # reviewer verdict + comments with video times (open first)
motionmind review <brand>/<campaign> <version> --resolve 3   # after the fix is in the new version; never --approve for the user
motionmind music --out src/assets/audio/music.wav --duration 15 --bpm 120 --sections "0:tense,2:groove,5:outro"  # bars, not seconds
motionmind sfx list [--query click]                         # licensed sound catalogue; copy what you use into the run
motionmind list · motionmind compare <a> <b>
```

Inside a run's `src/`: `npx hyperframes@<pinned> check` and `npx hyperframes@<pinned> snapshot --at 1,2.5,4 --no-end`
(the pinned version is in `src/package.json`; set `HYPERFRAMES_NO_TELEMETRY=1`).

## 3. Non-negotiables
- **One version = one folder.** A new hook, palette, music, aspect ratio or creative direction is a new
  `v<N+1>` (`motionmind init`); only technical fixes before approval happen in place. Never overwrite an approved version (`motionmind render` refuses a production/archived run; never pass `--force` unless the user asks for it).
- **Edit lock.** If `runs/<v>/.editing.json` exists the user is editing in HyperFrames Studio: do not touch `src/`.
  When it is gone, run `npx hyperframes history` in `src/` and continue from the user's changes.
- **Determinism.** Every frame is a function of time only: no `Math.random()`, `Date`, timers, or state carried
  between frames. Same render twice = identical pixels.
- **Look at your output.** After every build step open the snapshot frames; after render open the contact sheet.
  Never report a video as done without having looked at it.
- **Loudness.** −14 LUFS ±0.5 integrated, true peak ≤ −1 dBFS, measured from the rendered file (`motionmind render`/`log`
  print it and warn on a miss; `promote --stage production` refuses it). HyperFrames does not normalise: set the master
  gain on the root (see `references/sound.md`). Never pass `--force` to get past QA unless the user asks for it.
- **9:16 safe area.** Headlines, UI and CTA inside y 285–1635 (the 4:5 centre crop); CTA held still ≥ 1.5 s at the end.
- **Record before you say done.** A rendered version is not finished until `motionmind log` (or `render` on a logged
  run) has written it to the registry.
- **Rights.** Use only assets the user owns or that carry a licence for the use; note the source of every downloaded
  or generated asset in the campaign `manifest.json`. Sounds without a licence in the catalogue stay out of commercial videos.

## 4. Load only what the task needs
| Task | Read |
|---|---|
| Any new video or new version | `references/workflow.md` |
| Writing or fixing scenes | `references/hyperframes.md` |
| Choosing look, pacing, type, transitions | `references/motion.md` |
| Music, SFX, voice-over, loudness | `references/sound.md` |
| Before Gate 3 and before promoting | `references/qa.md` |
| Product demos / tutorials with real app screens | `references/screen-demo.md` + `assets/screen-kit.js` |
