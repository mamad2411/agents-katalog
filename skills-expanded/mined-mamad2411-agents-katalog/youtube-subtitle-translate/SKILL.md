---
name: youtube-subtitle-translate
description: >
  Download YouTube videos, extract/proofread/translate subtitles, and render them onto video.
  Use whenever the user asks to download a YouTube video with subtitles, translate video subtitles
  to Chinese, add subtitles/burn subtitles to a video, or do ASR transcription on video audio.
  Covers the full pipeline: video download → subtitle extraction → proofreading → translation →
  SRT generation → subtitle rendering. Also use for "下载视频加字幕", "视频翻译字幕",
  "把字幕烧录到视频中". For pure subtitle file creation without rendering (just SRT output),
  this skill handles that too — stop before Phase 5.
---

# YouTube Subtitle Translator

Download YouTube videos, extract and process subtitles (proofread + punctuate + translate), then burn them back into the video. Handles both auto-generated captions and manual uploads, with fallback to ASR when no subtitles exist.

## Hard Rules

- Use at most **3 concurrent subagents** for subtitle chunk processing. When there are more than 3 chunks, run them in waves and launch the next chunk only after one subagent finishes.
- Chunk count is not concurrency. You may split into 10 chunks, but you must not start 10 Codex processes/subagents at once; run at most 3 active workers at any time.
- Always download only the source subtitle track: English when available, otherwise the video's original language. Do not download YouTube's auto-translated target-language captions; translate from the source subtitle instead.
- Never use a YouTube-provided target-language caption track as a shortcut, even for long videos and even if `zh-Hans` or another target language is listed in `automatic_captions`.
- Video download defaults to 1080p. If 1080p is unavailable, download the best available version below 1080p.
- Translation must be performed by subagents over chunk files. Do not use local model helpers for translation.
- Before writing SRT/ASS, strip illegal subtitle characters from text, especially stray backslashes (`\`) that render visibly in video.

## Workflow Overview

```
Phase 1: Download    →  Get video info, download video, extract subtitles
Phase 2: Prepare     →  If no subtitles: extract audio → run ASR
Phase 3: Process     →  Split into chunks → parallel agent proofread + translate
Phase 4: Merge       →  Combine chunks → generate SRT/ASS files
Phase 5: Render      →  Burn subtitles onto video using ffmpeg
```

## Phase 1: Download

### 1.1 Get Video Info

Use the YouTube MCP tool to fetch metadata:

```
youtube_get_video_info(videoId="...", detail="standard")
```

Record: title, duration, channel, whether subtitles are available.

### 1.2 Create Output Directory

Name the directory after the video title. Sanitize for filesystem:

```bash
mkdir -p "/output/path/<Video Title>"
```

### 1.3 Download Video

```
youtube_download(videoId="...", outputPath="<dir>/video.mp4", quality="1080p", force=true)
```

If using `yt-dlp`, prefer 1080p and fall back to the best format below 1080p:

```bash
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]/best" --merge-output-format mp4 \
  -o "<dir>/video.%(ext)s" "<url>"
```

### 1.4 Extract Source Subtitles Only

```
youtube_get_transcript(videoId="...", language="<source-language>")
```

If the result exceeds token limits, it's saved to a tool-results file — read it in chunks.

This is a non-negotiable source-subtitle policy:
- Prefer English subtitles/captions when available.
- If English is not available, use the video's original spoken language.
- Ignore `zh-Hans`, `zh-Hant`, and every other target-language track shown by YouTube, including auto-translated tracks.
- Do not request, retry, merge, or render a YouTube-provided target-language caption track.
- Target-language subtitles must be produced only by subagent translation from the source subtitle.

If a tool returns a list such as `en-orig, zh-Hans`, choose only `en-orig`. Do not include `zh-Hans` in any download command.

If using `yt-dlp`, write only the source subtitle:

```bash
yt-dlp --skip-download --write-auto-subs --write-subs \
  --sub-langs "en.*" --sub-format srt --convert-subs srt \
  -o "<dir>/video.%(ext)s" "<url>"
```

Wrong, do not run:

```bash
yt-dlp --write-auto-subs --sub-langs "en-orig,zh-Hans" ...
```

If the English/original subtitle download succeeds but a target-language request fails with HTTP 429, do not retry the target-language request. That request should not have been made; continue from the source subtitle and translate it through Phase 3.

**If subtitles exist**: Save raw segments as JSON, proceed to Phase 3.
**If NO subtitles** (404/error): Proceed to Phase 2 (ASR fallback).

Save raw data:
- `raw_segments.json` — all segments with text/offset/duration
- `raw_subtitles.srt` — initial SRT conversion

## Phase 2: ASR Fallback (No Subtitles Available)

When the video has no captions/transcripts:

1. **Extract audio** from video using ffmpeg:
   ```bash
   ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
   ```

2. **Run ASR** — user specified qwen3-asr but any whisper-compatible model works:
   ```bash
   qwen3-asr audio.wav --output-format srt > raw_subtitles.srt
   ```
   Or use the built-in approach via hyperframes-media skill's transcribe command.

3. Parse the SRT output back into the segment JSON format expected by Phase 3.

## Phase 3: Parallel Proofreading & Translation

This is the most time-consuming step for long videos. The strategy: split into chunks and process them with subagents, with a hard limit of 3 concurrent subagents.

Do this phase even for very long videos. Length is not a reason to download or use YouTube's target-language auto-captions. The correct shortcut for long videos is chunking plus 3-way subagent concurrency, not target-caption reuse.

### 3.1 Split Segments Into Chunks

Use `scripts/merge-chunks.py`'s inverse logic — split `raw_segments.json` into N chunk files:

```python
# Split into chunks sized for review/translation.
n = len(segments)
chunk_count = min(10, max(1, (n + 75) // 76))
chunk_size = n // chunk_count + 1
for i in range(0, n, chunk_size):
    save_chunk(i, segs[i:i+chunk_size])
```

Save as `chunk_00.json`, `chunk_01.json`, etc. Each contains `{"chunk_id", "start_idx", "end_idx", "segments": [...]}`.

### 3.2 Launch Parallel Agents

For each chunk, spawn a background subagent. Launch no more than 3 subagents at the same time. If there are 10 chunks, start chunks `00`, `01`, and `02` first; when one finishes, start the next pending chunk. Never start all 10 chunks at once. Give each agent:

1. The path to its `chunk_XX.json`
2. Instructions to read [references/subtitle-proofreading.md](references/subtitle-proofreading.md) for the full spec
3. Output path: `result_XX.json` in the same directory

The agent must:
- Read every segment in its chunk
- Proofread English (fix ASR errors, add punctuation)
- Translate to natural Simplified Chinese (keep tech terms in English)
- Save as JSON array with `{index, start, end, en, zh}` per segment
- Remove illegal subtitle characters from `en` and `zh`, especially stray backslashes (`\`), control characters, and raw ASS override braces.

**Important**: Maximum concurrency is 3 subagents/processes. If there are more than 3 chunks, run them in waves. Do not launch 10 Codex child processes for 10 chunks.

### 3.3 Wait for Completion

Monitor which `result_XX.json` files appear. Don't proceed until all chunks complete.

## Phase 4: Merge & Generate Output Files

Run the merge script:

```bash
python3 scripts/merge-chunks.py <output_dir>
```

This auto-discovers all `result_*.json` files and produces:

| File | Content |
|------|---------|
| `final_subtitles.json` | Merged JSON, sorted by timestamp |
| `subtitles_bilingual.srt` | English + Chinese lines |
| `subtitles_zh.srt` | Chinese only |
| `subtitles_en.srt` | English only |

### 4.2 Validate Data Quality

**Before rendering, always validate the merged data.** Parallel agent processing can produce timestamp corruption:

```bash
# Check for abnormal durations (>120s = almost certainly corrupted)
python3 -c "
import json
segs = json.load(open('final_subtitles.json'))
bad = [s for s in segs if s['end'] - s['start'] > 120]
print(f'Abnormal durations: {len(bad)} / {len(segs)}')
for s in bad: print(f'  [{s[\"index\"]}] {s[\"start\"]:.1f}->{s[\"end\"]:.1f} ({s[\"end\"]-s[\"start\"]:.0f}s)')
"
```

If any are found, fix them (cap `end` at `start + 6`) and regenerate SRT/ASS. Both `merge-chunks.py` and `srt-to-ass.py` include auto-detection and auto-fix for this issue.

Verify the output: check first and last few entries have correct timestamps and readable text.

Also verify text sanitation:

```bash
python3 -c "
import json
segs = json.load(open('final_subtitles.json'))
bad = [s for s in segs if '\\\\' in s.get('en','') or '\\\\' in s.get('zh','')]
print(f'Backslash artifacts: {len(bad)}')
for s in bad[:10]: print(s['index'], s.get('en',''), s.get('zh',''))
"
```

## Phase 5: Render Subtitles Onto Video

This is where things get tricky. **Do NOT use the system ffmpeg directly** — see Pitfalls below.

### 5.1 Run the Render Script

```bash
bash scripts/render-subtitles.sh <video.mp4> <subtitles_bilingual.srt> [output.mp4]
```

The script handles everything:
- Detects/builds ARM64-native ffmpeg with libass support
- Converts SRT → ASS with proper CJK font config
- Copies files to /tmp to avoid special-character path issues
- Renders with ffmpeg's ass filter
- Validates the output

### 5.2 Verify Output

Check that:
- Output file exists and is > 10MB (not just audio)
- Duration matches original video (use ffprobe)
- Play the first and last minute to confirm subtitles appear

## Pitfalls & Lessons Learned

These are hard-won lessons from real usage. Follow them to avoid wasting hours.

### ffmpeg Architecture Mismatch (CRITICAL)

**Problem**: macOS Homebrew's ffmpeg is compiled WITHOUT libass, libfreetype, and fontconfig. The `ass`, `subtitles`, and `drawtext` filters simply don't exist.

**Worse**: Static ffmpeg builds from evermeet.cx are **x86_64 (Intel)** binaries. On Apple Silicon Macs they run through Rosetta 2 emulation at ~8-10x slower. A 1.5h video took 2+ hours.

**Solution**: Use `scripts/ensure-ffmpeg.sh`. It detects these issues and compiles ARM64-native ffmpeg from source with all needed libraries. First build takes ~5 minutes; subsequent rebuilds are instant (cached object files).

Required configure flags for full subtitle support:
```
--enable-libass --enable-libfreetype --enable-fontconfig --enable-libdav1d
```

### AV1 Decode Missing

**Problem**: Many modern YouTube videos are encoded in AV1 (`codec_name: av1`). A ffmpeg built without `--enable-libdav1d` will fail with "Function not implemented" errors during decode, producing a 68MB audio-only file.

**Solution**: Always include `--enable-libdav1d` when building ffmpeg.

### Path Special Characters Break ffmpeg Filters

**Problem**: When the video or subtitle path contains characters like em-dashes (—), smart quotes, or non-ASCII characters, ffmpeg's filter parser chokes with "No option name near..." errors. This happens even with proper shell quoting.

**Solution**: Copy subtitle files to `/tmp/subs_<pid>.ass` before passing to ffmpeg. The render script does this automatically.

### moviepy TextClip API Conflicts (AVOID)

**Problem**: moviepy 2.x's `TextClip` has parameter conflicts between positional args and kwargs (`font` appears twice internally). Multiple error variants, none obvious from the error message.

**Recommendation**: Don't use moviepy for production subtitle rendering. Use ffmpeg's ass filter instead — it's faster, more reliable, and handles CJK fonts properly through libass/fontconfig.

### SRT vs ASS for ffmpeg

**Problem**: ffmpeg's `subtitles` filter (which reads SRT directly) also suffers from path-parsing issues on some builds. The `ass` filter is more reliable.

**Solution**: Convert SRT → ASS first using `scripts/srt-to-ass.py`, then use the `ass` filter. The ASS format also gives you fine control over font, size, positioning, and styling.

### Illegal Subtitle Characters

**Problem**: Raw or translated subtitle text can contain stray backslashes (`\`) or ASS override characters. In ASS rendering, a literal backslash can appear on screen or accidentally interact with ASS escape syntax.

**Solution**: Sanitize subtitle text before writing SRT/ASS:
- Remove backslashes from user-visible subtitle text
- Remove control characters except normal whitespace
- Strip raw `{` and `}` braces from subtitle text
- Let `srt-to-ass.py` add only the ASS control sequences it owns, such as `\N` between bilingual lines

### Abnormal Subtitle Durations from Parallel Agent Processing

**Problem**: When processing subtitles in parallel chunks (Phase 3), individual agents can produce entries with corrupted timestamps — specifically, `end` values that are far larger than `start` (e.g., duration of 2600s or 4800s instead of ~6s). This causes those subtitle lines to remain visible on screen for most of the video, overlapping with all other content.

**Root cause**: Agents sometimes mis-assign end times when consolidating fragmented ASR segments across chunk boundaries. The issue is data-level, not a rendering problem — so it won't be caught by ffmpeg errors.

**Solution**: Three layers of defense:
1. **`scripts/srt-to-ass.py`** auto-detects entries with duration > 120s and caps them at 6s with a warning
2. **Phase 4 validation**: After merging chunks, always scan for entries where `(end - start) > 120` seconds
3. **Pre-render check**: Before running ffmpeg, grep the ASS file for suspiciously long Dialogue lines

```bash
# Quick pre-render check: find any subtitle lasting > 2 minutes
python3 -c "
import json, sys
segs = json.load(open('final_subtitles.json'))
bad = [s for s in segs if s['end'] - s['start'] > 120]
if bad: print(f'WARNING: {len(bad)} abnormal durations found!'); sys.exit(1)
else: print('Duration check passed')
"
```

### Font Size Tuning

**Problem**: Default font sizes (16-20px) may be too small on high-resolution 1080p+ videos, especially when viewing on smaller screens or from a distance.

**Solution**: Use `--font-size` flag to adjust. Recommended baseline sizes:
- 1080p video: `--font-size 24` (bilingual) or `--font-size 28` (single language)
- 4K video: `--font-size 36` or larger
- The `render-subtitles.sh` script passes this through to `srt-to-ass.py`

## Dependencies

- **YouTube MCP tools**: `mcp__plugin_youtube_youtube__*` (video download, transcript, info)
- **ffmpeg**: Auto-built by `scripts/ensure-ffmpeg.sh` if system version insufficient
- **Python 3**: For merge/convert scripts
- **Homebrew**: For build dependencies (libass, freetype, dav1d, etc.)
- **ASR tool** (optional): qwen3-asr, whisper, or any speech-to-text tool
