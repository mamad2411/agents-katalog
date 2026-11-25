---
name: forge-demo
description: Regenerate the forge sales demo end-to-end — script the story, record real GitLab UI segments with the in-app browser, generate FluidAudio (Kokoro) voiceover, and assemble the final MP4 with ffmpeg. Use when the demo video or its voiceover/scenes must be rebuilt after product changes.
---

# forge-demo: regenerate the sales demo

The demo is **real screen recordings of the GitLab UI only** — no stills, no
terminal mockups. Long waits are sped up (`setpts`), never cut
(`demo/assemble_full_ui.py` is the canonical assembler).

## 0. Prerequisites

- `ffmpeg` (+ `ffprobe`), `asciinema`, `agg` (brew).
- FluidAudio CLI (Kokoro TTS, voice `af_heart`, English only):
  `git clone https://github.com/FluidInference/FluidAudio && cd FluidAudio &&
  swift build -c release --product fluidaudiocli` →
  `.build/arm64-apple-macosx/release/fluidaudiocli`. First TTS run downloads
  the model; mmap cache warnings are harmless. Keep each request ≤ ~300
  chars (Kokoro 524-phoneme limit).
- A live lab: GitLab CE + forge stack (`forge-lab` skill) with a demo user
  in `FORGE_APPROVERS` and the seeded `utils.slugify` bug in the target
  repo (guarantees the red-CI → repair beat).
- ZCode browser-use (`control-browser` skill) — recordings use the IAB
  `tab.recording.start({actions})` API.

## 1. Story (demo/SCRIPT.md)

10 beats: hook → repo → live `/implement` → plan → `/go` gate → agent
streaming in CI → red pipeline + bounded repair (fail-safe) → Draft MR with
review + evidence → the merge button is yours → outro. Generate the
voiceover first (`S01…S10.wav`, 24 kHz mono) — scene durations follow the
audio.

## 2. Recording segments (IAB, 1280×800 @20fps, showCursor)

Known-good GitLab selectors:

- comment editor click: `[data-testid="content_editor_editablebox"]`
- typing target (ProseMirror hides contenteditable): `.ProseMirror`
- submit: `[data-testid="confirm-button"]`

Segments (one `recording.start` cell each, actions DSL has no reload/goto —
plan camera moves inside one page):

- **A** issue page: type `/implement` → Comment → wait 60 s — GitLab
  live-appends the forge plan on camera.
- **B** issue page: type `@forge /go <full-run-id>` → Comment → hold.
- **C** job page **from birth**: post `/go` from a shell, write the job URL
  to a file the moment the API exposes it (`/pipelines?ref=…` pagination is
  unreliable — resolve the pipeline id from forge's DB
  `evidence->'harness'->>'pipeline_id'`), and have the JS cell poll that
  file, goto, and record 90 s. The pretty trace
  (`[grok:say]/[grok:tool]/[grok:usage]`) comes from
  `ci/templates/grok-events-filter.mjs` on main.
- **C1** verification pipeline page (red) after adoption.
- **C2** repair forge-agent job page (scroll the completed pretty log).
- **D** Draft MR: overview → review verdict → evidence → back to merge
  button (scroll up at the end for the S09 beat).
- **E** repository page scroll (outro).

Poll `recording.status(id)` every ~2 s; only the final call passes
`outputPath` (workspace-relative, `.webm`). Failed/cancelled recordings
usually still executed their actions — check for side effects (extra
comments/runs) and take a fresh issue for retakes.

## 3. Assemble

1. Transcode every `.webm` → CFR mp4:
   `ffmpeg -i x.webm -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 25 -an x.mp4`
2. `python3 demo/assemble_full_ui.py` — speeds up long waits (setpts,
   3–6×) without cutting, places VO with `adelay`, renders title/end cards,
   concatenates to `demo/forge-demo.mp4` (1080p30, AAC).
3. QC: `ffprobe` duration/size; `volumedetect` (max ≈ −4 dB is healthy);
   extract frames at scene boundaries and eyeball them.

## 4. Gotchas (all hit for real)

- **agg dies via SIGPIPE when piped** — redirect to /dev/null, never `| tail`.
- GIF → x264 fails on odd widths — `-vf scale=1280:-2`.
- `amix` with zero inputs → build the audio graph conditionally (see
  `seg()` in assemble_full_ui.py).
- IAB recording jobs don't survive kernel boundaries — a segment must be
  one JS cell (≤118 s); `status(outputPath)` is also the stop call.
- `screencapture -v` works but records the whole desktop — prefer IAB.
- GitLab trace live-updates arrive in ~30 s flushes; time job-page cameras
  accordingly (or accept the speed-up).
- zsh does not word-split unquoted `$VAR`; use `while read` loops.
- `.env` re-source in EVERY shell call that recreates containers — an empty
  `GITLAB_URL` produces tasks failing with "missing protocol".
