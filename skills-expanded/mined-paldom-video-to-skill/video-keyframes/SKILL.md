---
name: video-keyframes
description: Captures scene-change frames from a local video or mp4, OCRs them, and writes a timeline digest of what is on screen when. Use when the user asks to pull or sample frames, slides, screenshots, keyframes or stills from a video or a time range, to read on-screen text, code or a diagram, or what is visible at a timestamp. Not for transcribing speech or writing notes.
license: MIT
argument-hint: <video-file> [timestamp]
---

# Video keyframes

Extracts the frames that show something *new* — not one frame every N seconds,
and not every frame. Produces `frames/*.jpg` and `timeline.json`, a token-lean
digest you read **before** opening any image.

## When to use

The user wants what was on the *screen*: "pull the slides out of this", "what's
on screen at 4:20", "screenshot the commands he runs", "read the diagram".

**When not to:** they want the spoken words (`video-transcribe`), or a written
note (`video-notes` — it calls this skill itself).

**Speech-only video is not worth framing.** For a podcast, interview or
talking-head, frames cost effort and teach nothing. Check the genre first.

## Input is a local file

This skill does not download anything. For a URL, fetch it first:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" -o video.mp4 "<url>"
```

720p answers essentially every question a video can answer; 4K costs minutes of
transfer to answer it no better.

## Workflow

### 1. Extract

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/extract_frames.py" video.mp4 --out <workdir> \
    [--transcript <workdir>/transcript.json] [--start MM:SS --end MM:SS] [--max-frames N]
```

Pass `--transcript` whenever you have one: each shot then carries the speech
that covers it, which is what lets you caption a figure without a vision call.

### 2. Read `timeline.json` first

One row per shot: `start`/`start_ms`, `frame` path, `ocr` text, `motion`, and
`speech`. Read this **before** any image. For most shots the OCR plus the speech
span already answers the question, and no image needs opening at all.

### 3. Look closer only where the evidence demands it

```bash
# several exact moments in ONE call — never loop one call per frame
python3 "${CLAUDE_SKILL_DIR}/scripts/extract_frames.py" frame-at video.mp4 --out <workdir> 1:02 1:15 4:20

# a range, sampled
python3 "${CLAUDE_SKILL_DIR}/scripts/extract_frames.py" clip video.mp4 6:00 6:30 --out <workdir> --fps 2
```

Re-look when the speech describes an action the keyframe does not show, when
`motion` spikes, or when you must read on-screen text exactly.

## How the threshold is chosen

ffmpeg's `scene` score is **not** a fraction of pixels changed. Measured on a
plain light slide deck, a full slide transition scores about **0.03** — so the
conventional `gt(scene,0.4)` and even a 0.05 floor detect *nothing* on the most
common slide case. The script therefore measures the video's real scene-score
distribution in one cheap downscaled pass and picks the threshold that admits
roughly the frame budget. Do not hardcode a threshold from a blog post.

If scene detection leaves a stretch longer than two minutes unobserved, the
script switches to interval sampling and says so on stderr. `strategy` in
`timeline.json` records which one ran — report it, because it tells the user how
complete the coverage is.

## Output

```
<workdir>/
├── frames/*.jpg
└── timeline.json   # {duration_s, strategy, scene_threshold, frames_kept, frame_budget, shots:[...]}
```

## Gotchas

- **OCR mangles command flags.** Tesseract routinely renders `--maxfail` as
  `—-maxfail` and confuses `l`/`1`/`I`, `O`/`0`. Treat `ocr` as a search index,
  not as a source of truth: read any command you intend to reproduce off the
  image itself.
- **Perceptual dedup is luminance-only.** A button turning red, or a total
  turning green, is invisible to it, so a UI flow can collapse to a single
  frame. The script pins evenly spaced frames that dedup may never drop; if you
  still see a flow missing its middle, re-sample it with `clip`.
- **The first frame is kept deliberately.** Scene detection never fires on frame
  0, so without it the opening title is silently lost.
- **`-vsync` is gone.** ffmpeg 8 removed it and hard-errors; the script probes
  for `-fps_mode` and falls back only on older builds. If you write your own
  ffmpeg command, do the same.
- **No tesseract is survivable.** OCR degrades to frames-without-text and the
  run continues; it is not a hard dependency.

Threshold measurements, budget tiers and dedup details:
[references/frame-selection.md](references/frame-selection.md).
