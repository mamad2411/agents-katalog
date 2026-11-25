---
name: ffmpeg
description: Use this skill for media processing with ffmpeg/ffprobe — inspect, convert, trim, resize, compress, extract frames/audio, replace audio, mute, make GIFs, add subtitles/overlays, and combine videos. Triggers on 'combine these videos', 'merge my clips', 'join these videos together', 'put them end to end', 'stitch the clips into one video', 'concatenate these files', 'make one long video from these parts', 'append the second video to the first', 'chain these videos', 'compress video', 'extract audio', 'resize video', 'make gif', 'remove audio', 'thumbnail', 'storyboard', 'slideshow', 'social-media crop', 'codec settings', 'crf', 'preset', 'stream mapping', 'ffmpeg troubleshooting'.
---

# FFmpeg Skill for Computer-Use Agents

Process media files with ffmpeg and ffprobe. This skill adds agent-specific safety rules and decision logic on top of ffmpeg knowledge the model already has.

For additional recipes (convert, remux, extract audio, replace audio, remove audio, GIF, subtitles, overlays, and more), see `references/recipes.md`.

---

## Safety Policy

### No-overwrite default

Use `-n` unless the user explicitly asks to overwrite.

```bash
ffmpeg -n -i "$INPUT" [output options] "$OUTPUT"
```

If overwriting is explicitly requested, use `-y`.

### Temp-file workflow

Write to a temporary file with the same extension as the intended output, verify, then rename:

```bash
# Derive temp path preserving the target extension
TMP_OUTPUT="${OUTPUT%.*}.tmp.${OUTPUT##*.}"

ffmpeg -n -i "$INPUT" [output options] "$TMP_OUTPUT" &&
ffprobe -v error "$TMP_OUTPUT" &&
mv "$TMP_OUTPUT" "$OUTPUT"
```

### Other rules

- Quote all file paths.
- Only use local file paths with `-i`. Do not pass user-supplied URLs directly to ffmpeg/ffprobe without validating the protocol (stick to `file://` or bare paths).
- Do not delete the input file unless the user explicitly requests it.
- After generating output, verify with `ffprobe`.
- Clean up temp directories after successful operations.

---

## Inspect First

Always probe unknown media before complex operations:

```bash
# Human-readable
ffprobe -hide_banner -i "$INPUT"

# Machine-readable JSON
ffprobe -v error -show_format -show_streams -of json "$INPUT"

# Quick queries
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT"          # duration
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$INPUT"        # resolution
ffprobe -v error -show_entries stream=index,codec_type,codec_name -of table "$INPUT"                    # codecs
```

---

## Decision Tree: Copy vs Re-encode

### Use `-c copy` when

- Changing container only (e.g. `.mkv` to `.mp4`)
- Removing or extracting a stream
- Approximate keyframe-aligned trim
- Avoiding quality loss

```bash
ffmpeg -n -i "$INPUT" -c copy "$OUTPUT"
```

### Re-encode when

- Resizing, cropping, padding, rotating
- Applying any `-vf` or `-af` filter
- Changing codec, frame rate, or pixel format
- Frame-accurate trim required
- Web/browser compatibility required

### Audio codec decision

| Goal | Audio option |
|------|-------------|
| Preserve source audio exactly | `-c:a copy` (may not be compatible with all containers) |
| Web-compatible MP4 | `-c:a aac -b:a 128k` (always safe) |
| Audio for transcription | `-vn -acodec pcm_s16le -ar 16000 -ac 1` |

When the target is a web-compatible MP4, prefer `-c:a aac` over `-c:a copy` -- copied audio may retain a codec the browser cannot play.

---

## Web-Compatible MP4 Defaults

```bash
ffmpeg -n -i "$INPUT" \
  -c:v libx264 -crf 23 -preset medium -threads 4 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "$OUTPUT"
```

Always include `-threads 4` when re-encoding. Without it, ffmpeg uses all CPU cores, which causes severe contention when multiple agents run concurrently.

| Profile | Codec | CRF | Preset | Audio | Notes |
|---------|-------|-----|--------|-------|-------|
| General (default) | libx264 | 23 | medium | aac 128k | Best compatibility |
| High quality | libx264 | 18 | slow | aac 192k | Archival, mastering |
| Smaller file | libx264 | 28 | medium | aac 96k | |
| Minimum size | libx264 | 32 | slow | aac 64k | |
| Modern smaller MP4 | libx265 | 24 | medium | aac 128k | Add `-vtag hvc1`; less compatible, smaller files |
| WebM/VP9 | libvpx-vp9 | 15 | n/a | libopus | Add `-b:v 0`; web-native, slow encode |

When the user does not specify a codec, default to H.264 (libx264). Use H.265/VP9 only when the user asks for smaller files or specifies these codecs.

---

## Core Recipes

### 1. Inspect media

```bash
ffprobe -hide_banner -i "$INPUT"
```

### 2. Combine / Merge / Join / Stitch Videos End-to-End

Use this when the user says "combine", "merge", "join", "stitch", "put end to end", "make one long video", "append", or "chain" videos. These mean sequential concatenation -- playing clips one after another. If the user asks for side-by-side, overlay, grid, or picture-in-picture, see `references/recipes.md` instead.

**Same codec (fast, no re-encode):**

The concat demuxer file list uses single-quoted paths, which breaks on filenames containing single quotes. For reliable automation, symlink inputs into a temp directory with safe names (zero disk I/O, no file copies):

```bash
# Replace the list with the actual input files (any number of files)
INPUT_FILES=("video1.mp4" "video2.mp4" "video3.mp4")

_tmpd="$(mktemp -d)"
trap 'rm -rf "$_tmpd"' EXIT

i=0
for f in "${INPUT_FILES[@]}"; do
  safe="$_tmpd/clip_$(printf '%03d' $i).${f##*.}"
  ln -s "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" "$safe"
  printf "file '%s'\n" "$safe" >> "$_tmpd/concat_list.txt"
  i=$((i+1))
done

ffmpeg -n -f concat -safe 0 -i "$_tmpd/concat_list.txt" -c copy "$OUTPUT"
```

**Mixed codecs (re-encodes):**

All inputs must have audio streams. If any input lacks audio, add a silent track first (see `references/recipes.md` section "Handling Missing Audio Streams"). Adjust `-i` count and `concat=n=N` to match the actual number of inputs:

```bash
# Example with 3 inputs -- adjust n=, -i count, and stream labels for actual input count
ffmpeg -n \
  -i "$VIDEO1" \
  -i "$VIDEO2" \
  -i "$VIDEO3" \
  -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 23 -preset medium -threads 4 -c:a aac \
  "$OUTPUT"
```

For video-only concat and more variants, see `references/recipes.md` section "Concatenate (Mixed Codecs)".

### 3. Trim

Fast (keyframe-aligned, not frame-accurate):

```bash
ffmpeg -n -ss "00:01:00" -i "$INPUT" -t "00:00:10" -c copy "$OUTPUT"
```

Accurate (re-encodes):

```bash
ffmpeg -n -i "$INPUT" \
  -ss "00:01:00" -t "00:00:10" \
  -c:v libx264 -c:a aac -pix_fmt yuv420p \
  "$OUTPUT"
```

**Trim semantics**: `-t` is duration from the seek point. `-to` is an absolute timestamp on the *output* timeline (not the source timeline) when `-ss` is on the output side. Use `-t duration` when the user specifies a clip length; use input-side `-ss` + `-to` when the user gives absolute source timestamps.

### 4. Fade In / Fade Out

Video fade (black to visible / visible to black):

```bash
# Fade in first 2 seconds, fade out last 2 seconds of a 30s video
ffmpeg -n -i "$INPUT" \
  -vf "fade=t=in:st=0:d=2,fade=t=out:st=28:d=2" \
  -c:v libx264 -crf 23 -preset medium -c:a aac \
  "$OUTPUT"
```

Audio fade:

```bash
# Fade in first 2 seconds, fade out last 2 seconds
ffmpeg -n -i "$INPUT" \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=28:d=2" \
  -c:v copy -c:a aac \
  "$OUTPUT"
```

Combined video + audio fade:

```bash
ffmpeg -n -i "$INPUT" \
  -vf "fade=t=in:st=0:d=2,fade=t=out:st=28:d=2" \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=28:d=2" \
  -c:v libx264 -crf 23 -preset medium -c:a aac \
  "$OUTPUT"
```

To calculate fade-out start: probe duration first, then `st = duration - fade_duration`. Video fade requires re-encoding video; audio fade requires re-encoding audio.

### 5. Resize

```bash
# By width (auto height, -2 ensures even dimensions)
ffmpeg -n -i "$INPUT" -vf "scale=1280:-2" \
  -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "$OUTPUT"

# By height
ffmpeg -n -i "$INPUT" -vf "scale=-2:720" \
  -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "$OUTPUT"
```

After any scale, pad, or crop, add `setsar=1` to the filter chain if the output aspect ratio looks wrong (non-square pixels).

### 6. Extract frames / single frame / thumbnail

```bash
# One frame per second
mkdir -p "$FRAME_DIR"
ffmpeg -n -i "$INPUT" -vf "fps=1" "$FRAME_DIR/frame_%06d.jpg"

# Single frame at timestamp (thumbnail)
ffmpeg -n -ss "00:00:01.500" -i "$INPUT" -frames:v 1 -q:v 2 "$OUTPUT"
```

For storyboard / contact sheet and slideshow recipes, see `references/recipes.md`.

---

## Common Failure Modes

| Error | Fix |
|-------|-----|
| Width not divisible by 2 | Add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"` |
| Output file already exists | Use different output path, or `-y` only if overwrite allowed |
| Codec not supported in container | Re-encode instead of `-c copy` |
| Output has no audio | Probe input; use `-map 0:a:0?` for optional audio |
| Output is huge | Increase CRF (`-crf 28`) or reduce resolution |
| Browser cannot play output | Use H.264 + AAC + yuv420p + faststart |
| MP4 not streamable / slow to start | Add `-movflags +faststart` |
| moov atom not found | Input file is incomplete or corrupt; re-download or recover source |
| Audio out of sync after speed change | Apply matching `atempo` filter to audio stream |
| Aspect ratio wrong after scale/pad/crop | Append `setsar=1` to the filter chain |
| `drawtext` breaks on special characters | Use `drawtext=textfile=input.txt` instead of inline `text=` for user-supplied text |

---

## Command Construction Checklist

1. What is the input path? Probe it if unknown.
2. What is the output path and extension?
3. Overwrite allowed? Default: `-n`.
4. Container-only change? `-c copy`.
5. Resizing/filtering? Re-encode video.
6. Multiple inputs? Use `-map`.
7. Audio might be absent? Use `0:a:0?`.
8. Web-compatible? H.264 + AAC + yuv420p + faststart.
9. Frame-accurate cut? Output-side `-ss`, re-encode.
10. Verify output with `ffprobe`.

---

## Agent Behavior Rules

1. Before constructing any command, identify: source format, desired output container/codec, target dimensions/duration, and whether the user prioritizes quality, speed, or file size.
2. Inspect with `ffprobe` if media details are unknown.
3. Choose the simplest applicable command.
4. Treat "combine/merge/join/stitch videos" as sequential concatenation unless the user explicitly asks for side-by-side, overlay, grid, or picture-in-picture.
5. Use `-c copy` only when not modifying media content.
6. Re-encode when applying any filter.
7. Quote every path. Keep filter graphs in double quotes; use single quotes inside for expressions like `enable='between(t,1,7)'`. Never interpolate untrusted text directly into filter strings -- use `textfile=` for user-supplied text.
8. Use `-n` unless overwrite was explicitly requested.
9. Save to a new output path.
10. Verify output with `ffprobe`.
11. If FFmpeg fails, read the error and adjust -- do not retry the same command.
12. For complex filter_complex, multi-input, or advanced tasks, read `references/recipes.md`.

---

## References

- [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html)
- [FFprobe documentation](https://ffmpeg.org/ffprobe.html)
- [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html)
- [H.264 encoding guide](https://trac.ffmpeg.org/wiki/Encode/H.264)

---

## 融合工具包（来自开源 bundled skills）

以下 2 组脚本从开源 bundled skills 融合而来（video-merger / subtitle-burner），作为本 skill 的可选增强工具。均为独立 Python CLI（纯确定性，无 LLM），可与 ffmpeg 原生命令混用。

### 1. 视频合并（video-merger）

**用途**：将目录中按数字前缀编号的 MP4 片段（`1_*.mp4`、`2_*.mp4`、…）按序号拼接为单个 MP4（或按 `--chunk-duration` 切成多个约 60s 的分块），统一分辨率/帧率/编码，可选淡入淡出转场。

**脚本路径**：`scripts/merge_videos.py`（核心库在 `src/video_merger.py`）

**调用方式与关键参数**：

```bash
python scripts/merge_videos.py --input <片段目录> --output <输出.mp4> \
  [--mode full|chunk] [--transition 0.5] [--fps 24] \
  [--crf 22] [--preset medium] [--resolution 1080x1920] \
  [--chunk-duration 60] [--ffmpeg-path ffmpeg] [--ffprobe-path ffprobe]
```

- `--input`：包含 `\d+_*.mp4` 片段的目录（必填）；`--output`：full 模式为输出 mp4 路径，chunk 模式为输出目录（必填）
- `--mode`：`full`（合成单个完整视频）或 `chunk`（按 `--chunk-duration` 切分多个分块）
- `--transition`：转场淡入淡出时长（秒），`0` 禁用
- `--resolution`：统一输出分辨率（如 `1080x1920`）；缺省取第一个片段的原始分辨率
- 片段命名必须匹配 `^\d+_.*\.mp4$`，按前导整数排序；先无损拼接（`-c copy`）再重编码，统一参数并加转场
- `--ffmpeg-path` / `--ffprobe-path`：可显式指定可执行文件路径（Windows 下 PATH 继承不可靠时使用）

**依赖**：ffmpeg ≥ 5.0、ffprobe、Python 3.8+；仅用标准库，无额外 Python 包。

### 2. 字幕烧录（subtitle-burner）

**用途**：用 ffmpeg `subtitles=` 滤镜（libass）将 SRT 字幕烧录进 MP4。视频单遍重编码（H.264 + faststart + yuv420p），音频原样 `-c:a copy`。内置 CJK 友好字体回退链（Microsoft YaHei → SimHei → Arial Unicode MS → Arial）。

**脚本路径**：`scripts/burn_subtitles.py`

**调用方式与关键参数**：

```bash
python scripts/burn_subtitles.py --input <源.mp4> --subtitles <字幕.srt> --output <输出.mp4> \
  [--font "Microsoft YaHei,SimHei,Arial Unicode MS,Arial"] [--font-size 42] \
  [--margin-v 80] [--play-res auto|720x1280] [--crf 20] [--preset medium] \
  [--alignment 2] [--outline 2] [--ffmpeg-path ffmpeg]
```

- `--play-res`：`auto` 时用 ffprobe 探测源视频分辨率，使 `--font-size`/`--margin-v` 以源视频像素为单位；也可直接传 `WxH`（如 `720x1280`）
- 脚本自动处理 Windows 路径转义（驱动器冒号 `C\:`、正斜杠、路径内单引号），调用方无需关心
- 样式默认白字 + 2px 黑描边、`BorderStyle=3`、底部居中、距底 80px；失败时 stderr 输出 ffmpeg 日志末尾约 2.5KB
- 输出打印绝对路径到 stdout；非零退出码表示失败

**依赖**：ffmpeg ≥ 5.0（libass，现代构建均内置）、Python 3.8+；无额外 Python 包。
