---
name: bilingual-subtitle
description: 视频字幕提取、翻译、双语合并、烧录。不用于：纯音频转文字、翻译文本文件、视频剪辑
---

Extract subtitles from video using Whisper (GPU-accelerated), translate to Chinese, and optionally burn bilingual subtitles into video.

All output files go to the working directory (工作目录). Always use `auto_send: true` on the final shell call.

**IMPORTANT: Always use `process.py`. Never invent script names or parameters.**

## From URL (one command handles everything)

The script auto-detects URLs and handles: CC subtitle download → audio/video download → Whisper → translate → merge.

### Plain text subtitles, no timestamps (fastest when user says no timestamps)
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'URL' --source-only --txt-only -m tiny --beam-size 1 -o {WORKDIR}/output_source.txt", "timeout": 1800000, "auto_send": true}
```

### SRT subtitles only
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'URL' --srt-only -o {WORKDIR}/output_bilingual.srt", "timeout": 600000, "auto_send": true}
```

### Subtitles + burn into video
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'URL' -o {WORKDIR}/output_bilingual.mp4", "timeout": 600000, "auto_send": true}
```

### Chinese-only subtitles from URL
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'URL' -l zh --source-only --srt-only -o {WORKDIR}/output_zh.srt", "timeout": 600000, "auto_send": true}
```

## From local file

### Extract subtitles only
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'VIDEO_FILE' --srt-only -o {WORKDIR}/OUTNAME_bilingual.srt", "timeout": 300000, "auto_send": true}
```

### Extract + burn into video
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'VIDEO_FILE' -o {WORKDIR}/OUTNAME_bilingual.mp4", "timeout": 600000, "auto_send": true}
```

### Chinese-only subtitles
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'VIDEO_FILE' --chinese-only --srt-only -o {WORKDIR}/OUTNAME_zh.srt", "timeout": 300000, "auto_send": true}
```

### Source-only subtitles (no translation)
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'VIDEO_FILE' --source-only --srt-only -o {WORKDIR}/OUTNAME_source.srt", "timeout": 300000, "auto_send": true}
```

### Karaoke mode
```
{"command": "python skills/bilingual-subtitle/scripts/process.py 'VIDEO_FILE' --karaoke --fontsize 24 -o {WORKDIR}/OUTNAME_karaoke.mp4", "timeout": 600000, "auto_send": true}
```

## Parameters
| Parameter | Description | Default |
|---|---|---|
| `-o, --output` | Output file path | auto-generated |
| `-l, --language` | Source language (auto-detected by Whisper if omitted) | auto-detect |
| `-t, --target` | Target language | `zh-CN` |
| `-m, --model` | Whisper model (tiny/base/small/medium/large) | `small` |
| `--beam-size` | Whisper beam size; 1 is fastest | `1` |
| `--fontsize` | Subtitle font size | `14` |
| `--margin` | Bottom margin | `25` |
| `--srt-only` | Generate subtitle file only, skip video encoding | - |
| `--txt-only` | Generate plain text without timestamps, skip video encoding | - |
| `--chinese-only` | Output Chinese subtitles only | - |
| `--source-only` | Output source language subtitles only, skip translation entirely | - |
| `--karaoke` | Karaoke mode with word-level highlight | - |
| `--no-speech-threshold` | Filter non-speech segments (0-1) | `0.6` |

## Rules
- ALWAYS use bash shell (default), never PowerShell.
- ALWAYS copy the exact command templates above. Do NOT rename scripts or invent parameters.
- The ONLY script is `skills/bilingual-subtitle/scripts/process.py`. No other scripts should be called directly.
- timeout: 300000 (5min) for local files with --srt-only, 600000 (10min) for normal URLs or video encoding. For long videos or user-provided duration >30 minutes, use 1800000 (30min).
- GPU auto-detected: NVIDIA CUDA > Apple Silicon mlx > CPU int8. No config needed.
- Source language is auto-detected by Whisper. Use `-l` only to override (e.g., `-l zh` to force Chinese). If source and target language match, translation is automatically skipped.
- If the user asks for subtitles without timestamps or pure transcript text, use `--source-only --txt-only -m tiny --beam-size 1` directly. Do not generate SRT and post-process with shell.
- Do NOT run yt-dlp separately. The script handles URL downloading internally.
