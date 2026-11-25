---
name: media-timestamp-summary
description: >-
  Composer: generate a human-readable summary of media files sorted by
  epoch-ms timestamp embedded in their filenames. Composes the
  file-glob-sort-by-regex-capture base skill for deterministic sorting,
  adds date conversion, time-gap analysis, and a formatted output file.
category: Media-Processing
---

# Media Timestamp Summary Skill (v1) — Composer

This is a **composer** skill. It scans a directory for media files whose
filenames contain a Unix epoch-millisecond timestamp (e.g.
`video-1780724440748.webm`), sorts them chronologically, and writes a
detailed human-readable summary file (e.g. `video-info.txt`) to the same
directory.

The composer delegates the deterministic sorting primitive to the
[`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md)
base skill, then adds domain-specific formatting: millisecond-to-UTC date
conversion, time-gap calculations between consecutive files, total size
rollup, and a structured text summary.

The originating use case was organizing webinar recording segments saved
by a meeting-recording tool that names files as `video-<epoch_ms>.webm`.

***

## 1. Scope & Intent

- **In scope**: Accept a directory path and an optional glob/regex pattern
  (defaulting to `video-*.webm` / `video-(\d+)`). Write a structured
  chronological summary file containing: ordered file list with readable
  timestamps, individual file sizes, time gaps between consecutive files,
  total span duration, and total file count/size.
- **Out of scope**:
    - Modifying, moving, or renaming any source file (read-only).
    - Recursive subdirectory scanning (single-directory only; override the
    glob if `**/` is needed).
    - Non-media files or filenames that lack a timestamp capture group.
    - Any format other than `.txt` for the output summary (plain text).

***

## 2. Composition Rationale

This skill is a **composer**: it does NOT re-implement the glob expansion,
regex capture, or sort logic. It orchestrates one atomic base skill:

1. **[`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md)**
   — invoked FIRST. The composer shells out to its
   `scripts/sort-by-capture.py` with `--glob "video-*.webm" --regex
   "video-(\d+)" --sort-type int`. The base script's stdout (one JSON
   object per file, sorted by timestamp ascending) is consumed by this
   composer for all downstream processing.

The composer's domain-specific value-add over the base alone:
millisecond-to-human-readable date conversion, time-gap computation
between consecutive entries, total span calculation, formatted table
layout, and file-system output to `video-info.txt`. Inlining the base
logic would duplicate a primitive that other composers (log-file
date-range report, screenshot sequence auditor, archive-by-timestamp
organizer) also consume.

Bidirectional discoverability: the base skill lists this composer in
its `## Composition by Higher-Level Skills` table.

***

## 3. Environment & Dependencies

### 3.1 Runtime

- **Python 3.12+** — the script uses the standard library only (`argparse`,
  `json`, `os`, `subprocess`, `sys`, `datetime`). No external PyPI packages.
  Verify:

  ```bash
  python3 --version
  ```

### 3.2 Base Skill Dependency

The [`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md)
base skill MUST be present at its canonical relative path. The composer
script resolves it via `../file-glob-sort-by-regex-capture/scripts/sort-by-capture.py`
anchored to its own location — no `cwd` assumptions.

### 3.3 Verification

```bash
# Python version
python3 -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"; print("OK")'

# Base script reachable
python3 .agents/skills/media-timestamp-summary/scripts/generate-summary.py --directory /tmp --glob "*.tmp" --regex "(\\d+)" 2>&1 || true
```

***

## 4. Protocol

### 4.1 Step 1 — Run the Summary Script

```bash
python3 .agents/skills/media-timestamp-summary/scripts/generate-summary.py \
    --directory "/path/to/media/files" \
    [--glob "video-*.webm"] \
    [--regex "video-(\\d+)"] \
    [--output video-info.txt]
```

The script:

1. Validates the target directory exists.
2. Resolves the base script path relative to its own location and verifies
   it exists.
3. Calls the base script via `subprocess.run()` with the provided glob,
   regex, and `--sort-type int`.
4. Parses each JSON Lines line from the base script's stdout.
5. Converts each epoch-ms key to a human-readable UTC date using
   `datetime.fromtimestamp(ms / 1000, tz=timezone.utc)`.
6. Computes time gaps between consecutive entries.
7. Formats a structured text summary with:
   - A table of all files in chronological order (rank, filename, timestamp
     ms, readable time, file size).
   - Per-file detail blocks with exact timestamp and gap from previous.
   - A time-spacing overview.
   - Total file count and total size.
8. Writes the summary to `<directory>/<output>` (default: `video-info.txt`).

### 4.2 Step 2 — Verify Output

```bash
cat "/path/to/media/files/video-info.txt"
```

Confirm the file lists entries sorted chronologically (earliest first),
with timestamps increasing monotonically.

***

## 5. Edge Cases & Constraints

- **No matching files**: The base script exits non-zero; the composer
  propagates the error and exits 1. No output file is written.
- **Regex mismatch on some files**: Those files are silently skipped by the
  base script with a stderr warning. If no files match, the composer exits 1.
- **Empty directory**: The glob returns no matches; the base script exits 1.
- **Very large file sets** (>10 000 files): The JSON Lines output is held
  in memory. For extremely large directories, consider a streaming composer
  variant.
- **Non-epoch-ms timestamps**: The default regex assumes a decimal integer
  representing milliseconds since Unix epoch. Custom `--regex` patterns
  may capture any numeric key; the `--sort-type` is hard-coded to `int` in
  the composer.

***

## 6. Prohibited Actions

- The Agent MUST NOT re-implement the glob expansion, regex capture, or sort
  logic inline — the base skill is the SSOT for file discovery and ordering.
- The Agent MUST NOT modify the source media files — this is a read-only
  summary operation.
- The Agent MUST NOT change the output file's plain-text format unless the
  user explicitly requests a different output format.

***

## 7. Script Reference

[`scripts/generate-summary.py`](./scripts/generate-summary.py) performs:

1. Resolve `--directory` to absolute path; validate it exists.
2. Locate the base script at
   `../../file-glob-sort-by-regex-capture/scripts/sort-by-capture.py` relative
   to its own `SCRIPT_DIR`.
3. Invoke the base script via `subprocess.run()`.
4. Parse each line of base script's stdout as JSON.
5. For each entry, convert `key` (epoch-ms) to UTC datetime string.
6. Compute per-file size in human-readable form and gaps between consecutive
   entries.
7. Assemble a structured text summary with table, detail blocks, spacing
   overview, and totals.
8. Write the summary to `<directory>/<output>`.
9. Print the summary to stdout for immediate review.

***

## 8. Related Skills

- [`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md)
  — base skill composed by this skill; owns the glob expansion, regex
  capture, and sort primitive.
- [`webm-recording-merge-with-filler`](../webm-recording-merge-with-filler/SKILL.md)
  — sibling media-processing composer; merges discontinuous webm recordings
  with filler transitions. May use this summary skill to inventory segments
  before merging.
- [`webm-recording-interrupted-recovery`](../webm-recording-interrupted-recovery/SKILL.md)
  — sibling composer for recording interruption recovery; may use this skill
  to timestamp-order the main + continuation recordings.
- [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) —
  sibling base skill for detecting spoken language from media audio tracks;
  domain-related but does not compose this skill.
