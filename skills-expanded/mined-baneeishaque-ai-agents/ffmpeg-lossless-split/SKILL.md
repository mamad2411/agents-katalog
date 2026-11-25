---
name: ffmpeg-lossless-split
description: Losslessly split or extract a segment from a media file at a timestamp using ffmpeg `-c copy` (zero re-encoding). Validates timestamps before executing.
category: Media-Processing
---

# FFmpeg Lossless Split Skill (v1)

This is a **base** skill. It takes a media file and a timestamp, then either:

- **Splits** the file into two parts at the given timestamp (with `--output-prefix`).
- **Extracts** a segment from `--split-at` to `--to` as a single output file.

Both operations use `ffmpeg -c copy` — frames are stream-copied, not decoded and re-encoded. The skill is intended
to be **composed by higher-level skills** (e.g. recording-interrupted recovery, meeting-recording trim, podcast-cut)
that need lossless timestamp-based extraction as a pipeline stage.

***

## 1. Scope & Intent

- **In scope**: Split a media file into two lossless parts at a timestamp; extract a sub-segment bounded by start and
  end timestamps; validate timestamps against file duration before executing.
- **Out of scope**:
    - Transcoding, filtering, or re-encoding any stream.
    - Detecting scene boundaries or smart cut points (timestamp is user-supplied).
    - Non-timestamp-based splitting (e.g. by file size, keyframe count, scene change).
    - Concatenating multiple files (handled by the sibling [FFmpeg Lossless Concat](../ffmpeg-lossless-concat/SKILL.md)
      base skill).

***

## 2. Composition Rationale

This skill is a **base** — it owns the generic primitive "split/trim a media file at a timestamp without re-encoding."
Multiple domain-specific composers reuse this primitive:

- [`webm-recording-interrupted-recovery`](../webm-recording-interrupted-recovery/SKILL.md) — trims a continuation
  recording at the interruption point before merging with a filler transition.
- Any future skill that needs to cut segments from a longer recording (meeting trim, security-camera segment extraction,
  podcast chapter split) should invoke this skill rather than re-deriving the `ffmpeg -c copy -ss` incantation.

The layering test: *"Could a different domain need the same primitive?"* — **YES**. Inlining the split logic into a
composer would split the SSOT across every consumer.

***

## 3. Environment & Dependencies

### 3.1 Required Tools

- **ffmpeg** 5.0+ — The `-c copy` option must be available. Verify:

  ```bash
  ffmpeg -version | head -1
  ```

- **ffprobe** (ships with ffmpeg) — Reads file duration and stream info. Verify:

  ```bash
  ffprobe -version | head -1
  ```

- **Python 3.12+** — The automation script uses the standard library only. Verify:

  ```bash
  python3 --version
  ```

If any tool is missing, consult the [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) skill.

### 3.2 Verification

```bash
which ffmpeg ffprobe
python3 -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"; print("OK")'
```

***

## 4. Protocol

### 4.1 Step 1 — Identify the File and Split Timestamp

The caller supplies:

- The source media file path (`--input`).
- The split timestamp (`--split-at`) in `HH:MM:SS`, `MM:SS`, or raw seconds format.
- Either `--output-prefix` (to produce two files) or `--output` with `--to` (to extract a single segment).

### 4.2 Step 2 — Validate Timestamps

```bash
python3 .agents/skills/ffmpeg-lossless-split/scripts/split-lossless.py \
    --input source.webm \
    --split-at 06:18 \
    --verify-only
```

The script probes the file duration and verifies:

- `--split-at` is within the file (≥ 0 and < duration).
- `--to` (if given) is after `--split-at` and within the file.

If valid, it prints a summary and exits 0.

### 4.3 Step 3 — Split or Extract

**Split mode** — produce two files at the timestamp:

```bash
python3 .agents/skills/ffmpeg-lossless-split/scripts/split-lossless.py \
    --input source.webm \
    --split-at 06:18 \
    --output-prefix /path/to/output
```

Produces `output_part1.webm` (0–06:18) and `output_part2.webm` (06:18–end).

**Segment extraction mode** — extract a bounded segment:

```bash
python3 .agents/skills/ffmpeg-lossless-split/scripts/split-lossless.py \
    --input source.webm \
    --split-at 06:18 \
    --to 10:30 \
    --output /path/to/segment.webm
```

Produces `segment.webm` (06:18–10:30).

### 4.4 Step 4 — Verify Output

```bash
# Confirm output files exist
ls -lh /path/to/output_part1.webm /path/to/output_part2.webm

# Check stream parameters match the input
ffprobe -v quiet -show_entries stream=codec_name,width,height /path/to/output_part1.webm

# Confirm durations are approximately correct
ffprobe -v quiet -show_entries format=duration /path/to/output_part1.webm
```

The output files MUST have identical codec parameters to the input (same codecs, resolution, frame rate).

***

## 5. Script Reference

[`scripts/split-lossless.py`](./scripts/split-lossless.py) performs:

1. Parse `--input`, `--split-at`, optional `--to`, and output flags.
2. Run `ffprobe` on the input to get duration and stream info.
3. Validate all timestamps against the file duration.
4. If `--verify-only`: print summary and exit 0.
5. If `--output-prefix`:
   - Run `ffmpeg -y -i <input> -c copy -ss 0 -to <split-at> <prefix>_part1<ext>`.
   - Run `ffmpeg -y -i <input> -c copy -ss <split-at> <prefix>_part2<ext>`.
6. If `--output`:
   - Run `ffmpeg -y -i <input> -c copy -ss <split-at> -to <to> <output>`.
7. Exit 0 on success, 1 on failure with ffmpeg stderr captured.

### 5.1 Argument Breakdown

| Flag | Purpose |
| :--- | :--- |
| `--input <path>` | Source media file to split/trim. |
| `--split-at <time>` | Timestamp to split at (`HH:MM:SS`, `MM:SS`, or seconds). |
| `--to <time>` | End timestamp for segment extraction. Requires `--output`. |
| `--output <path>` | Single output file path. Requires `--to`. |
| `--output-prefix <prefix>` | Prefix for split output files. Generates `<prefix>_part1.<ext>` and `<prefix>_part2.<ext>`. |
| `--verify-only` | Validate timestamps only; do not execute the split. |

### 5.2 Timestamp Accuracy with `-c copy`

The `-c copy` mode selects the **nearest keyframe** to the requested timestamp. This means:

- The first part (`-ss 0 -to <time>`) may end a few frames **after** the requested timestamp if the next keyframe
  is past it.
- The second part (`-ss <time>`) may start a few frames **before** the requested timestamp (from the preceding
  keyframe).

For most meeting-recording and screen-capture use cases this is acceptable (≤ 1–2 seconds of overlap). For
frame-accurate cuts, a re-encode (`-c libx264` etc.) at the exact timestamp is required.

***

## 6. Edge Cases & Constraints

- **Timestamp beyond duration**: Script exits 1 with an error message showing the file's total duration.
- **Nonexistent input**: Script exits 1 with a clear error.
- **Keyframe inaccuracy**: The output parts may have brief overlap or gap at the split point (see §5.2). This is
  inherent to lossless stream-copy splitting.
- **Missing ffmpeg/ffprobe**: Script exits 1 with a suggestion to install ffmpeg.
- **Special characters in paths**: The script passes paths directly to ffmpeg; spaces and special characters are
  handled by the shell. Paths with special characters MUST be quoted on the command line.

***

## 7. Prohibited Actions

- The Agent MUST NOT re-encode input files to achieve frame-accurate splits — that is the domain of a re-encoding
  transcoder skill, not this base skill.
- The Agent MUST NOT manually invoke `ffmpeg -c copy -ss` without using the script — the script validates timestamps
  and streams before executing.
- The Agent MUST NOT use this skill for concatenation; concat is owned by
  [`ffmpeg-lossless-concat`](../ffmpeg-lossless-concat/SKILL.md).

***

## 8. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [`webm-recording-interrupted-recovery`](../webm-recording-interrupted-recovery/SKILL.md) | Invokes `scripts/split-lossless.py --input <continuation> --split-at <time> --output <temp>` to trim the pre-interruption content from a continuation recording, then feeds the trimmed segment into a filler-merge composer. |

***

## 9. Related Skills

- [FFmpeg Lossless Concat](../ffmpeg-lossless-concat/SKILL.md) — sibling base skill for lossless concatenation.
- [WebM Recording Merge with Filler](../webm-recording-merge-with-filler/SKILL.md) — composer that inserts a filler
  transition between webm segments and losslessly concatenates them.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — installs ffmpeg/ffprobe if missing.
