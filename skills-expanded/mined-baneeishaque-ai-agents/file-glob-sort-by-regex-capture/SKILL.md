---
name: file-glob-sort-by-regex-capture
description: >-
  Base primitive: given a directory, glob pattern, and regex with a capture
  group, produce a sorted list of matching files with metadata (size, mtime),
  ordered by the extracted capture value. Domain-agnostic.
category: File-Management
---

# File Glob Sort by Regex Capture (v1) — Base Primitive

This is the **base** skill. It scans a directory for files matching a glob
pattern, extracts a sort key from each filename using a regex capture group,
and outputs a deterministic sorted list as JSON Lines. The primitive is
domain-agnostic — any workflow that needs to order files by an embedded
timestamp, sequence number, or other key in the filename can compose this
skill instead of re-implementing the glob+regex+sort pipeline.

The originating use case is sorting webinar recording segments
(`video-<epoch_ms>.webm`) by their embedded Unix millisecond timestamp, but
the same primitive handles log-file date stamps (`app-2026-06-17.log`),
screenshot sequence numbers (`Screenshot 2026-06-17 at 14.30.00.png`),
or any filename pattern with a sortable capture group.

***

## 1. Scope & Intent

- **In scope**: Accept a directory path, a glob pattern, a regex containing at
  least one capture group, and an optional sort-type flag (`int` / `float` /
  `str`). Output one JSON object per matched file, sorted by the extracted key,
  with filename, absolute path, raw key string, key type, size in bytes, and
  POSIX mtime epoch. Support `--reverse` for descending order.
- **Out of scope**:
    - Walking subdirectories recursively (the caller supplies the glob; `**/` in
    the glob produces recursive behaviour if desired, but the skill is
    designed for single-directory scans).
    - Modifying any file (read-only).
    - Converting or interpreting the extracted key beyond sorting (e.g. epoch-ms
    to human-readable date — that is the composer's responsibility).
    - Any filesystem traversal beyond `glob.glob()`.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — the script uses the standard library only (`argparse`,
  `glob`, `json`, `os`, `re`, `sys`). No external PyPI packages. Verify:

  ```bash
  python3 --version
  ```

No other tools required.

### 2.2 Verification

```bash
python3 -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"; print("OK")'
```

***

## 3. CLI Contract

Located at [`scripts/sort-by-capture.py`](./scripts/sort-by-capture.py).

```bash
python3 .agents/skills/file-glob-sort-by-regex-capture/scripts/sort-by-capture.py \
    --directory "/path/to/dir" \
    --glob "video-*.webm" \
    --regex "video-(\d+)" \
    [--sort-type int] \
    [--reverse] \
    [--min 30] [--max 36]
```

### 3.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--directory` | Yes | — | Directory to scan. Resolved to an absolute path. |
| `--glob` | Yes | — | Glob pattern (e.g. `video-*.webm`, `*.log`, `Screenshot *.png`). |
| `--regex` | Yes | — | Python regex with at least one capture group `(...)`. Must match the expected portion of each filename. |
| `--sort-type` | No | `int` | How to interpret the captured string for sorting: `int`, `float`, or `str`. |
| `--reverse` | No | — | If set, sort descending (largest key first). |
| `--min` | No | — | Numeric-span lower bound (inclusive). Drop entries whose captured numeric key is below this value. Requires `--sort-type int` or `float`. |
| `--max` | No | — | Numeric-span upper bound (inclusive). Drop entries whose captured numeric key is above this value. Requires `--sort-type int` or `float`. |

### 3.2 Output Format

One JSON object per line (JSON Lines / NDJSON), sorted by key. Each object contains:

| Field | Type | Description |
| :--- | :--- | :--- |
| `filename` | string | Bare filename (no path). |
| `abspath` | string | Absolute filesystem path. |
| `key` | string | Raw captured string from the regex capture group. |
| `key_type` | string | Sort type used (`int`, `float`, or `str`). |
| `size_bytes` | integer | File size in bytes. |
| `mtime_epoch` | integer | Last modification time as Unix epoch seconds. |

Example output:

```json
{"filename": "video-1780724440748.webm", "abspath": "/path/video-1780724440748.webm", "key": "1780724440748", "key_type": "int", "size_bytes": 18874368, "mtime_epoch": 1756780800}
{"filename": "video-1780724540587.webm", "abspath": "/path/video-1780724540587.webm", "key": "1780724540587", "key_type": "int", "size_bytes": 84934656, "mtime_epoch": 1756780800}
```

When `--min` / `--max` are set, the output set is the intersection of the glob+regex
matches and the inclusive numeric span of the captured key (e.g. `--min 30 --max 36`
with `--regex "^(\d{3})-"` keeps only files whose leading 3-digit number is 030–036).

### 3.3 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Success — JSON Lines written to stdout. |
| 1 | Error — directory not found, no files matched, or regex failed to capture on all files. Diagnostic printed to stderr. |

***

## 4. Protocol

### 4.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 4.2 Step 2 — Run the Script

```bash
python3 .agents/skills/file-glob-sort-by-regex-capture/scripts/sort-by-capture.py \
    --directory "/path/to/dir" \
    --glob "video-*.webm" \
    --regex "video-(\d+)"
```

### 4.3 Step 3 — Consume Output

Pipe the JSON Lines output into a consuming script or redirect to a file:

```bash
python3 .agents/skills/file-glob-sort-by-regex-capture/scripts/sort-by-capture.py \
    --directory "/path/to/dir" \
    --glob "video-*.webm" \
    --regex "video-(\d+)" \
    > /tmp/sorted-files.jsonl

# Parse with Python
python3 - << 'PY'
import json, sys
with open("/tmp/sorted-files.jsonl") as f:
    for line in f:
        entry = json.loads(line)
        print(entry["filename"], entry["key"], entry["size_bytes"])
PY
```

***

## 5. Edge Cases & Constraints

- **No files match the glob**: The script prints an error to stderr and exits 1.
- **Regex does not match a file's basename**: That file is skipped with a
  warning on stderr. If no file matches, the script exits 1.
- **Multiple capture groups**: Only the first capture group (`group(1)`) is
  used as the sort key. Additional groups are ignored.
- **Non-numeric key with `--sort-type int`**: Python's `int()` conversion
  raises `ValueError`, which propagates as an unhandled exception. Use
  `--sort-type str` for non-numeric keys.
- **`--min` / `--max` with `--sort-type str`**: a usage error (exit 2) — the
  span filter is numeric-only. Selection of `int` vs `float` derives from
  `--sort-type`, so pass the matching type.
- **Range with no survivors**: if the numeric span intersects zero files
  (e.g. `--min 999`), the script prints an error to stderr and exits 1.
- **`--min` and `--max` are independent**: either, both, or neither may be set;
  bounds are inclusive.
- **Very large directories**: `glob.glob()` returns all matches in memory.
  For directories with >100 000 matching files, consider a streaming approach
  (this skill targets typical media/project directories with dozens to
  thousands of files).

***

## 6. Prohibited Actions

- The Agent MUST NOT re-implement the glob+regex+sort pipeline inline when
  this skill is available. The script is the SSOT.
- The Agent MUST NOT modify files discovered by this skill — it is a read-only
  operation.
- The Agent MUST NOT use this skill for recursive directory traversal unless
  the glob explicitly contains `**/` — the caller controls the scope via the
  glob pattern.

***

## 7. Script Reference

[`scripts/sort-by-capture.py`](./scripts/sort-by-capture.py) performs:

1. Resolve `--directory` to an absolute path; validate it exists.
2. Build the full glob pattern (`<directory>/<glob>`) and run `glob.glob()`.
3. For each file, extract `re.search(regex, basename).group(1)`.
4. Build a list of dicts with filename, abspath, key, size_bytes, mtime_epoch.
5. When `--min` / `--max` are set (numeric sort types only), filter the list to
   the inclusive numeric span of the captured key; exit 1 if the span is empty.
6. Sort by key converted to `--sort-type` (int / float / str).
7. Write one JSON object per line to stdout.

***

## 8. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [`media-timestamp-summary`](../media-timestamp-summary/SKILL.md) | Calls this base script with `--glob "video-*.webm" --regex "video-(\d+)"` and `--sort-type int` to obtain chronologically-sorted webinar recording segments, then consumes the JSON Lines to generate a human-readable summary file with date conversions and time-gap analysis. |
| [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) | Calls this base script with `--glob "Screenshot *.png"` / `--glob "Screen Recording *.mov"` and a date-extraction regex to obtain JSON Lines of OneDrive-synced files sorted by embedded date key. Consumes the JSONL stdout and pipes into `json-group-stats` and `json-batch-file-move` via the composer script. |
| [`opencode-session-transcript-to-source-resolve`](../opencode/opencode-session-transcript-to-source-resolve/SKILL.md) | For `to N` range references, calls this base script with `--directory <session-dir> --glob "0*-*.yaml" --regex "^(\d{3})-" --sort-type int --min <start> --max <N>`, consumes the `abspath` field of the JSONL stdout, and resolves each transcript reference to its source log path. |

New composers (e.g. log-file date-range report, screenshot sequence auditor,
archive-by-timestamp organizer, flat-folder date-based organizer) MUST reuse
this base script rather than re-implementing the glob+regex+sort pipeline.
Composer scripts MUST resolve this base script via a relative path anchored to
their own location, per the
[Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md).

***

## 9. Related Skills

- [`media-timestamp-summary`](../media-timestamp-summary/SKILL.md) — composer
  that consumes this base skill to produce a formatted summary of media files
  sorted by embedded epoch-ms timestamp.
- [`opencode-session-transcript-to-source-resolve`](../opencode/opencode-session-transcript-to-source-resolve/SKILL.md)
  — composer that consumes this base's `--min`/`--max` numeric-span filter to
  expand `to N` ranges of opencode session log files into their full source-log
  listing.
- [`text-lines-sort-by-length`](../text-lines-sort-by-length/SKILL.md) —
  sibling base primitive for sorting lines within a text file by physical line
  length (complementary — operates on file content rather than filenames).
- [`folder-comparison`](../folder-comparison/SKILL.md) — compares directory
  contents for consistency; may use this skill for ordered file listing.
- [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) —
  sibling media-domain base skill; operates on file content (audio) rather than
  filenames.
- [`json-group-stats`](../json-group-stats/SKILL.md) — downstream consumer;
  groups this script's JSON Lines output by a key field and emits per-group
  counts or grouped records.
- [`json-batch-file-move`](../json-batch-file-move/SKILL.md) — downstream
  consumer; takes a JSON array with abspath+key from this script's output and
  moves files into subfolders named by key.
- [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) —
  composer that orchestrates the 3-base pipeline for OneDrive 5000-file-limit
  workaround.
- [`macos-screenshots-folder-split`](../macos-screenshots-folder-split/SKILL.md) —
  domain composer wrapping the OneDrive composer for macOS screenshot and
  screen recording folders.
