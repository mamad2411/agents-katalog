---
name: ffmpeg-lossless-concat
description: Losslessly concatenate media files using ffmpeg's concat demuxer with stream copy (`-c copy`), zero re-encoding. Verifies codec compatibility first.
category: Media-Processing
---

# FFmpeg Lossless Concat Skill (v1)

This is the **base** skill. It takes two or more media files (any container / codec supported by ffmpeg) and concatenates
them into a single output file **without re-encoding** (zero generation loss). The concatenation uses ffmpeg's concat
demuxer with `-c copy` — the frames are stream-copied, not decoded and re-encoded.

The skill is intended to be **composed by higher-level skills** (e.g. meeting-recording merge with filler transitions,
security-camera segment assembly, podcast episode join) that need lossless concatenation as their last pipeline stage.

***

## 1. Scope & Intent

- **In scope**: Take a list of media file paths (one per line), verify they share compatible codec parameters (same
  video codec, resolution, pixel format, frame rate; same audio codec, sample rate, channel layout), generate an
  ffmpeg concat demuxer file list, and execute `ffmpeg -f concat -safe 0 -i <filelist> -c copy <output>`.
- **Out of scope**:
    - Transcoding, filtering, or re-encoding any stream.
    - Generating filler / transition segments (delegated to composer skills).
    - Discovering input files (supplied by the caller).
    - Any non-ffmpeg concat strategy.

***

## 2. Environment & Dependencies

### 2.1 Required Tools

- **ffmpeg** 5.0+ — The `-f concat` demuxer and `-c copy` must be available. Verify:

  ```bash
  ffmpeg -version | head -1
  ```

- **ffprobe** (ships with ffmpeg) — Used to read codec parameters from each input file. Verify:

  ```bash
  ffprobe -version | head -1
  ```

- **Python 3.12+** — The automation script uses the standard library only (no external PyPI packages). Verify:

  ```bash
  python3 --version
  ```

If any tool is missing, consult the [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) skill.

### 2.2 Verification

```bash
# Confirm ffmpeg and ffprobe are on PATH
which ffmpeg ffprobe

# Confirm Python 3.12+
python3 -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"; print("OK")'
```

***

## 3. Protocol

### 3.1 Step 1 — Acquire the File List

The caller supplies a list of media file paths. Each path MUST be an absolute or workspace-relative path to an existing
media file readable by ffmpeg. Paths with spaces or shell metacharacters MUST be quoted.

Example file list (`files.txt`):

```text
/path/to/first.webm
/path/to/second.webm
```

### 3.2 Step 2 — Verify Codec Compatibility

Run the verification script to check that all input files share compatible codec parameters:

```bash
python3 .agents/skills/ffmpeg-lossless-concat/scripts/ffmpeg_lossless_concat.py \
    --files files.txt \
    --verify-only
```

The script runs `ffprobe` on every file and compares:

- **Video**: codec name, width, height, pixel format, frame rate
- **Audio**: codec name, sample rate, channel layout (if present)

If all files are compatible, the script exits 0 and prints a summary. If incompatible, it exits 1 and lists the
mismatched parameters with the offending files.

### 3.3 Step 3 — Concatenate

```bash
python3 .agents/skills/ffmpeg-lossless-concat/scripts/ffmpeg_lossless_concat.py \
    --files files.txt \
    --output merged_output.webm
```

The script:

1. Verifies codec compatibility (same check as `--verify-only`).
2. Generates an ffmpeg concat demuxer file list (`file '/path/to/first.webm'`, one per line).
3. Executes:

   ```bash
   ffmpeg -y -f concat -safe 0 -i <temp_filelist> -c copy <output>
   ```

4. Cleans up the temporary file list.
5. Exits 0 on success, 1 on failure (with the ffmpeg stderr captured).

#### 3.3.1 Flag Breakdown

| Flag / Argument | Purpose |
| :--- | :--- |
| `-y` | Overwrite output file without interactive prompt. |
| `-f concat` | Use ffmpeg's concat demuxer (reads a text file listing input files). |
| `-safe 0` | Allow unsafe file paths (absolute paths, paths with `..`). Without this, the demuxer rejects non-relative-sibling paths. |
| `-i <filelist>` | Provide the generated file list as input. |
| `-c copy` | Stream copy — copy every packet without decoding/re-encoding. Zero quality loss. |

### 3.4 Step 4 — Verify Output

```bash
# Confirm the output file exists and is non-empty
ls -lh <output>

# Check its stream parameters match the originals
ffprobe -v quiet -show_entries stream=codec_name,width,height <output>

# Confirm duration is the sum of input durations
ffprobe -v quiet -show_entries format=duration <output>
```

The output file's video and audio codecs MUST be identical to the inputs. The duration MUST approximately equal the sum
of all input durations (stream copy preserves exact timing).

***

## 4. Edge Cases & Constraints

- **Codec mismatch**: If inputs have different codecs (e.g. VP9 + H.264), the concat demuxer with `-c copy` will fail
  because stream copy requires identical codec parameters across all segments. The script exits 1 before running ffmpeg.
- **Resolution mismatch**: Files with different frame dimensions produce a corrupted output. The script detects this and
  rejects the merge.
- **Frame rate mismatch**: Slight differences (< 0.01 fps) are tolerated; larger mismatches are rejected.
- **Audio on some files, not others**: The concat demuxer requires all segments to have the same stream layout.
  A file with no audio stream cannot be losslessly concatenated with files that have one. The script detects this.
- **Very large files** (> 4 GiB): ffmpeg's concat demuxer handles large files natively. No special handling needed.
- **Special characters in paths**: The script writes paths with single-quote escaping inside the concat file list
  per ffmpeg's `-f concat` quoting rules.
- **Duplicate paths in file list**: When the same file appears multiple times in the concat list (e.g. a filler
  segment inserted between every pair), the script deduplicates paths before `verify_compatibility` to avoid the
  grouped-probe returning N × streams for the duplicated file. The concat list itself retains duplicates — ffmpeg's
  concat demuxer handles repeated file references correctly. See `verify_compatibility` in §6.
- **Relative paths in concat list**: The `generate_concat_file` function resolves every path to absolute form
  (`os.path.abspath()`) before writing the ffmpeg concat file list. This ensures ffmpeg resolves paths correctly
  even though the concat file list is written to a temporary directory (`/tmp` or equivalent) whose working
  directory differs from the caller's `cwd`. Composers that supply the file list SHOULD similarly resolve paths
  to absolute form before passing them to this base script.

***

## 5. Prohibited Actions

- The Agent MUST NOT use `-c copy` when inputs have incompatible codec parameters — the script blocks this.
- The Agent MUST NOT re-encode files just to make them compatible — use a re-encoding composer skill if transcoding
  is intended, not this base skill.
- The Agent MUST NOT manually construct the concat file list or manually invoke the ffmpeg concat command — the
  script is the SSOT for the procedure and MUST be used so that compatibility verification is always enforced.

***

## 6. Script Reference

[`scripts/ffmpeg_lossless_concat.py`](./scripts/ffmpeg_lossless_concat.py) performs:

1. Parse `--files` (path to a text file, one path per line) and `--output` (output file path) or `--verify-only`
   (skip the concat, just check compatibility).
2. For each input file, run `ffprobe` to extract stream parameters.
3. Compare all streams pairwise — video codec, resolution, pixel format, frame rate; audio codec, sample rate,
   channel layout.
4. If `--verify-only`: print the compatibility verdict (COMPATIBLE / INCOMPATIBLE with details) and exit.
5. If `--output`: generate an ffmpeg concat file list, execute the concat command, clean up, and exit with ffmpeg's
   return code.

### 6.1 Internal Steps (beyond argument parsing)

- **Deduplication**: Before `verify_compatibility`, paths are deduplicated via `list(dict.fromkeys(file_paths))`
  so the same file listed N times (e.g. a filler segment between every pair) is probed only once. The original
  (non-deduplicated) list is used for the concat step so ffmpeg concatenates all occurrences.
- **Path resolution**: `generate_concat_file` resolves every path to absolute via `os.path.abspath()` so ffmpeg's
  concat demuxer finds the files regardless of where the temp concat file list is written.

### 6.2 Argument Breakdown

- `--files` — Path to a text file listing media files, one absolute or relative path per line. Blank lines and lines
  starting with `#` are ignored.
- `--output` — Path for the merged output file. The parent directory MUST exist.
- `--verify-only` — Only check compatibility; do not run the concat. Exits 0 if all files are compatible.

***

## 7. Composition by Higher-Level Skills

This skill is the **base layer** for any lossless media concatenation. Composers supply domain-specific file discovery
and optional pre-processing (e.g. filler generation), then pipe their file list into this skill:

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [WebM Recording Merge with Filler](../webm-recording-merge-with-filler/SKILL.md) | Calls `scripts/ffmpeg_lossless_concat.py --files <concat-list> --output <merged>` where the concat list interleaves source segments with filler segments (one filler between each pair). The filler is generated by its own base skill (`ffmpeg-filler-generator`). Consumes exit code only; does not parse stdout. |

New composers (e.g. security-camera segment assembly, podcast episode join, screen-recording gap fill) MUST reuse this
base script rather than reinventing compatibility verification and concat invocation. Composer scripts MUST resolve this
base script via a relative path anchored to their own location (`os.path.dirname(os.path.abspath(__file__))`) so the
pipeline works regardless of the caller's current working directory — see the
[Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md) for the project-wide rule.

***

## 8. Related Skills

- [FFmpeg Lossless Split](../ffmpeg-lossless-split/SKILL.md) — sibling base skill for lossless timestamp-based
  splitting (inverse operation of concat).
- [WebM Recording Merge with Filler](../webm-recording-merge-with-filler/SKILL.md) — composer that generates filler
  transitions and pipes into this base skill for lossless concat.
- [WebM Recording Interrupted Recovery](../webm-recording-interrupted-recovery/SKILL.md) — composer that orchestrates
  full recording-interruption recovery; uses this skill transitively via the filler-merge composer.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — installs ffmpeg/ffprobe if missing.
- [YouTube Video Upload](../youtube-video-upload/SKILL.md) — optional downstream consumer; may accept a
  concat output from this skill as upload input.
