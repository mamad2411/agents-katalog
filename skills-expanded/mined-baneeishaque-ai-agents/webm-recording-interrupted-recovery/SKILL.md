---
name: webm-recording-interrupted-recovery
description: Recover from a recording interruption by trimming the continuation recording and merging with a filler transition — composes ffmpeg-lossless-split and webm-recording-merge-with-filler.
category: Media-Processing
---

# WebM Recording Interrupted Recovery Skill (v1)

This is a **composer** skill. It recovers from a screen-recording or meeting-recording interruption where the
recording was interrupted and then continued in a separate file.

The composer orchestrates two lower-layer skills:

1. **[FFmpeg Lossless Split](../ffmpeg-lossless-split/SKILL.md)** (base) — trims any pre-interruption content from
   the beginning of the continuation recording, keeping only the post-interruption segment.
2. **[WebM Recording Merge with Filler](../webm-recording-merge-with-filler/SKILL.md)** (composer) — generates a
   filler transition (black screen + "Recording interrupted" text) and merges the main recording + filler + trimmed
   continuation into a single lossless webm file.

***

## 1. Scope & Intent

- **In scope**: Accept a main recording path, a continuation recording path, and an interruption timestamp. Trim the
  continuation to remove pre-interruption overlap, generate a filler transition, and merge everything into one
  lossless webm.
- **Out of scope**:
    - Detecting the interruption timestamp automatically (user-supplied).
    - Handling more than one continuation file (the filler-merge skill supports arbitrary segments; this composer
      covers the common 2-file case — extend the script for multi-continuation scenarios).
    - Splitting the main recording (user provides the main recording as-is).
    - Transcoding or re-encoding any source segment.

***

## 2. Composition Rationale

This skill is a **composer** — it does NOT implement split logic, filler generation, or lossless concatenation itself.
It orchestrates two existing skills:

1. **[`ffmpeg-lossless-split`](../ffmpeg-lossless-split/SKILL.md)** — invoked FIRST. The composer shells out to
   `scripts/split-lossless.py --input <continuation> --split-at <time> --output <temp>` to extract the
   post-interruption segment from the continuation recording. The split is lossless (`-c copy`). The trimmed output
   is written to a temporary file that is cleaned up after the merge completes.

2. **[`webm-recording-merge-with-filler`](../webm-recording-merge-with-filler/SKILL.md)** — invoked SECOND. The
   composer shells out to `scripts/generate_filler_and_merge.py --segment <main> --segment <trimmed> --filler-text
   "Recording interrupted" ... --output <final>` which generates a filler transition and merges all segments
   losslessly via the `ffmpeg-lossless-concat` base skill.

The composer's domain-specific value over either skill alone: it saves the user from knowing the two-step protocol
(trim then merge), handles temp-file lifecycle, and provides a single CLI surface whose parameters match the
user's mental model ("I have a main recording and a continuation that was interrupted at timestamp X").

Bidirectional discoverability: both `ffmpeg-lossless-split` and `webm-recording-merge-with-filler` list this
composer in their respective `## Related Skills` sections.

***

## 3. Environment & Dependencies

### 3.1 Required Tools

- **ffmpeg** 5.0+ — For split and concat operations. Verify:

  ```bash
  ffmpeg -version | head -1
  ```

- **ffprobe** (ships with ffmpeg) — For stream probing. Verify:

  ```bash
  ffprobe -version | head -1
  ```

- **Python 3.12+** — With **Pillow** (required by the filler-merge composer). Verify:

  ```bash
  python3 -c 'from PIL import Image; print("Pillow:", Image.__version__)'
  ```

- **Base skill scripts** MUST exist at:

  ```text
  .agents/skills/ffmpeg-lossless-split/scripts/split-lossless.py
  .agents/skills/webm-recording-merge-with-filler/scripts/generate_filler_and_merge.py
  .agents/skills/ffmpeg-lossless-concat/scripts/ffmpeg_lossless_concat.py
  ```

### 3.2 Verification

```bash
which ffmpeg ffprobe python3
python3 -c 'from PIL import Image; print("Pillow:", Image.__version__)'
test -f .agents/skills/ffmpeg-lossless-split/scripts/split-lossless.py && echo "split script OK"
test -f .agents/skills/webm-recording-merge-with-filler/scripts/generate_filler_and_merge.py && echo "filler-merge script OK"
test -f .agents/skills/ffmpeg-lossless-concat/scripts/ffmpeg_lossless_concat.py && echo "concat script OK"
```

If any tool is missing, consult the [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) skill.
If Pillow is missing, install it with `pip install Pillow` or `brew install pillow`.

***

## 4. Protocol

### 4.1 Step 1 — Identify Files and Interruption Timestamp

The caller supplies:

- `--main` — the main recording file (what was captured before the interruption).
- `--continuation` — the continuation recording (what was captured after the interruption was noticed). This file
  may include content recorded *before* the interruption point if the recording started before the user noticed.
- `--split-at` — the timestamp in `HH:MM:SS`, `MM:SS`, or seconds format marking where the interruption occurred.
  Content in the continuation file **before** this timestamp will be trimmed.

### 4.2 Step 2 — Run Recovery

```bash
python3 .agents/skills/webm-recording-interrupted-recovery/scripts/recover-interrupted.py \
    --main /path/to/main.webm \
    --continuation /path/to/continuation.webm \
    --split-at 06:18 \
    --filler-text "Recording interrupted" \
    --filler-subtext "\u2014 content missing \u2014" \
    --output /path/to/recovered.webm
```

The script:

1. **Trims** the continuation at the interruption timestamp using `ffmpeg-lossless-split` (lossless `-c copy`),
   saving the post-interruption segment to a temporary file.
2. **Generates filler** and **merges** the main recording + filler + trimmed continuation using
   `webm-recording-merge-with-filler`, which itself composes `ffmpeg-lossless-concat` for lossless concatenation.
3. **Cleans up** the temporary trimmed file.

### 4.3 Step 3 — Verify Output

```bash
# Confirm output exists
ls -lh /path/to/recovered.webm

# Check stream parameters match originals
ffprobe -v quiet -show_entries stream=codec_name,width,height /path/to/recovered.webm

# Confirm duration ≈ main duration + 3s filler + continuation duration
ffprobe -v quiet -show_entries format=duration /path/to/recovered.webm
```

The output file MUST:

- Have the same video codec (VP9) and audio codec (Opus) as the input segments.
- Show the filler text at the gap position (between end of main and start of trimmed continuation).
- Play seamlessly across all transitions.

***

## 5. Script Reference

[`scripts/recover-interrupted.py`](./scripts/recover-interrupted.py) performs:

1. Parse `--main`, `--continuation`, `--split-at`, `--filler-text`, `--filler-subtext`, `--filler-duration`, and
   `--output`.
2. Verify all input files exist.
3. Resolve `scripts/split-lossless.py` and `scripts/generate_filler_and_merge.py` via
   `os.path.normpath(os.path.join(script_dir, "..", "..", "<skill>/scripts/<script>"))`.
4. Run `scripts/split-lossless.py --input <continuation> --split-at <time> --output <temp>` to extract the
   post-interruption segment.
5. Run `scripts/generate_filler_and_merge.py --segment <main> --segment <temp> --filler-text ... --output <final>`.
6. Remove the temporary trimmed file.
7. Exit 0 on success, 1 on failure (the failing sub-script's stderr is surfaced verbatim).

### 5.1 Argument Breakdown

| Flag | Purpose |
| :--- | :--- |
| `--main <path>` | Main recording file (first segment, pre-interruption). |
| `--continuation <path>` | Continuation recording file (post-interruption, may include overlap before the interruption point). |
| `--split-at <time>` | Timestamp to split the continuation at (`HH:MM:SS`, `MM:SS`, or seconds). Content before this is trimmed. |
| `--filler-text <str>` | Primary text displayed on the filler (default: "Recording interrupted"). |
| `--filler-subtext <str>` | Secondary subtitle text (default: "\u2014 content missing \u2014"). |
| `--filler-duration <sec>` | Duration of the filler in seconds (default: 3). |
| `--output <path>` | Path for the final recovered webm file. |

***

## 6. Edge Cases & Constraints

- **Continuation has no pre-interruption overlap**: If the continuation file starts exactly at the interruption point,
  the trim will produce an empty or near-empty file (only 0–2 keyframes from the keyframe accuracy window). Verify
  with `--verify-only` on the split script first when in doubt.
- **Non-matching codecs between main and continuation**: The filler-merge composer's base skill detects this and
  reports the mismatch. This composer surfaces that error verbatim.
- **Missing split or filler-merge script**: The script verifies both dependency scripts exist at startup and exits
  1 with a clear error message if either is missing.
- **Very short continuation** (< 1 second after split point): The split will still produce a valid file but playback
  may be too brief to perceive the filler transition.

***

## 7. Prohibited Actions

- The Agent MUST NOT inline the split logic, filler generation, or concat logic into this composer — composition
  through the shared scripts is mandatory.
- The Agent MUST NOT re-encode source segments — only the filler is encoded; source segments are stream-copied.
- The Agent MUST NOT hard-code filler text, duration, or styling — these MUST be user-configurable via flags.
- The Agent MUST NOT leave the temporary trimmed file on disk after completion.

***

## 8. Related Skills

- [FFmpeg Lossless Split](../ffmpeg-lossless-split/SKILL.md) — base skill invoked for trimming the continuation.
- [WebM Recording Merge with Filler](../webm-recording-merge-with-filler/SKILL.md) — composer invoked for filler
  generation and lossless merge.
- [FFmpeg Lossless Concat](../ffmpeg-lossless-concat/SKILL.md) — base skill used transitively via the filler-merge
  composer for lossless concatenation.
- [Media Timestamp Summary](../media-timestamp-summary/SKILL.md) — composer that inventories webm segments by
  chronological order; use to identify main vs continuation recordings by timestamp.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — installs ffmpeg / Pillow if missing.
