---
name: create-video
description: Create or revise a branded narrated video with OfficeKit and HyperFrames. Use for explainers, product videos, motion graphics, narrated walkthroughs, social clips, training videos, or turning a script, document, or deck into video.
compatibility: Requires an OfficeKit workspace, Node.js 22+, npm, Python 3.10+, uv, ffmpeg, and network access for uncached HyperFrames/Kokoro/Strudel dependencies.
metadata:
  author: OfficeKit
  version: "0.2.0"
---

# Create an OfficeKit video

Work in `.office-kit/`. Use `setup-office-kit` first when absent. Author the
video in the main agent. HyperFrames is an external runtime dependency; this
plugin does not bundle its source or skills.

## Boundary

Edit the composition HTML, project CSS, narration data, and project media.
Follow the timing and frame guidance in the scaffolded `frame.md` and
`hyperframes.json`. Never inspect or edit `node_modules`, lockfiles, or
HyperFrames internals. OfficeKit's `video.py` owns preview and audit.

Brand state comes from `brands/<id>/`; the video receives a generated local
snapshot because its runtime cannot serve parent paths. Refresh snapshots with
`video.py refresh`, never by hand.

## Pass

Write `projects/<slug>/plan/PLAN.md`: brief, audience, brand ID, storyboard,
narration per segment, music-bed mood, expected durations, visual direction,
accessibility, assets, requested delivery, and acceptance criteria. Research
factual claims directly using host-provided tools when needed and record
sources in `reports/research.md`. No plan approval gate.

Scaffold and start the health-checked preview:

```bash
uv run python scripts/video/video.py new <slug> --title "…" [--brand <id>]
uv run python scripts/video/video.py dev <slug>
```

Tell the user only the URL printed by `dev`. Build one seek-safe scene at a
time. Use semantic HTML and the composition's `data-*` timing attributes;
keep content within the configured frame and safe areas. Derive segment timing
from measured narration instead of guessing.

Use the `text-to-speech` skill for local narration: one WAV per segment plus a
measured `manifest.json`. Do not substitute cloud TTS.

For the **music bed** (not a standalone track), load three skills in order:

1. `music-composition` — harmonic plan for a commercial / explainer
   underscore (`references/genres/media-and-commercial-music.md`,
   `assets/progressions-catalog.md`). Default cheerful unless the brief is dark.
2. `strudel` — mini-notation and pad patterns (`assets/patterns/ambient-pad.js`).
   Do not ship a strudel.cc URL as the video deliverable.
3. `strudel-offline` — Dough-safe rewrite and local WAV.
   Strudel/Dough are **AGPL-3.0-or-later**; see the repository `LICENSE`
   and `plugins/office-kit/skills/strudel-offline/LICENSE`.

Render `projects/<slug>/media/music-bed.wav` to the root `data-duration` (plus
a short tail). Keep the source pattern beside it as `media/music-bed.js`.
Place the file only after it exists:

```html
<audio
  id="music-bed"
  src="./media/music-bed.wav"
  data-start="0"
  data-duration="{{composition seconds}}"
  data-track-index="10"
></audio>
```

Mix to `config.toml` `[audio.levels]`: narration at `narration_lufs`, bed at
`music_bed_lufs`, and duck the bed by `duck_db` while speech plays. Measure
and apply with `hyperframes normalize-audio` so gain lands on `data-volume`.
Match bed mood to the brief via `music-composition` (cheerful commercial
underscore unless the plan is dark). Skip the bed if the user asks for
silence or supplies a licensed file. Preserve supplied media byte-for-byte
and keep generated assets separately named.

Record checkpoints in `reports/build.md`, then run:

```bash
uv run python scripts/video/video.py audit <slug>
```

Audit must exit 0. Review claims, pacing, synchronization, safe areas,
readability, accessibility, brand fidelity, and audio levels. Fix findings and
write `reports/review.md`.

Render only when the user names a final encoded deliverable, using `[video]`
format/output defaults and the scaffold's render command. Record the output in
`reports/delivery.md`; previews and stale renders are not deliveries.
