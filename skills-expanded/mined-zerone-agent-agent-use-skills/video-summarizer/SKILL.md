---
name: video-summarizer
description: Download videos from URLs (YouTube, Bilibili, and any yt-dlp supported platform), transcribe speech to text using Whisper, generate a structured summary, and save both the summary and full transcript as linked Obsidian notes. Use this skill whenever the user wants to summarize a video, transcribe video content, extract key points from a video, or save video notes to Obsidian. Also trigger when the user shares a video URL and asks for analysis, notes, or a recap.
---

# Video Summarizer

Convert video URLs into structured summaries and full transcripts, saved as linked notes in Obsidian.

## Prerequisites

- `yt-dlp` installed and available in PATH
- `ffmpeg` installed and available in PATH
- `whisper` (OpenAI) installed at `~/.whisper-venv/` with `turbo` model. If missing, install: `python3 -m venv ~/.whisper-venv && source ~/.whisper-venv/bin/activate && pip install openai-whisper`
- `obsidian` CLI installed (via obsidian-cli skill)
- Obsidian must be running

If any dependency is missing, tell the user what's missing and stop.

## Workflow

### Step 1: Extract video metadata

Before downloading, get the video title and metadata for naming:

```bash
yt-dlp --print title --print channel --print upload_date "%VIDEO_URL%"
```

Parse the output: first line = title, second line = author, third line = upload date (YYYYMMDD).

Clean the title for use as a filename: replace `/ \ : * ? " < > |` with `-`, collapse multiple hyphens, trim leading/trailing hyphens and spaces.

### Step 2: Download video

Download to a temp directory:

```bash
mkdir -p /tmp/video-summarizer
yt-dlp -o "/tmp/video-summarizer/%(title)s.%(ext)s" "%VIDEO_URL%"
```

### Step 3: Extract audio

Use ffmpeg to extract audio as mp3:

```bash
ffmpeg -i "/tmp/video-summarizer/VIDEO_FILENAME" -vn -acodec libmp3lame -q:a 2 "/tmp/video-summarizer/audio.mp3" -y
```

### Step 4: Transcribe with Whisper

Run Whisper to produce a txt transcript. Use `--language zh` for Chinese content (Bilibili, Douyin, etc.). For YouTube or other platforms where the language is unknown, omit `--language` to let Whisper auto-detect.

```bash
source ~/.whisper-venv/bin/activate && whisper "/tmp/video-summarizer/audio.mp3" --model turbo --language zh --output_format txt --output_dir /tmp/video-summarizer
```

Read the resulting `.txt` file to get the full transcript.

### Step 5: Generate structured summary

Based on the transcript, create a summary with this structure:

```
## 一句话核心

（一句话概括视频最核心的观点或主题）

## 主要论据

（按要点列出 3-5 个关键论据或信息点，每个用加粗标题开头）

## 关键信息

（用表格整理视频中出现的具体数据、概念、工具、人名等结构化信息）
```

Write the summary in the same language as the video content. If the transcript is in Chinese, write the summary in Chinese.

### Step 6: Save to Obsidian

Create two notes in Obsidian's `Inbox/` folder, linked via wikilinks.

**Summary note:** `Inbox/{clean-title}-视频总结.md`

```markdown
---
title: "{video title}"
source: "{video URL}"
author: "{channel name}"
date: {YYYY-MM-DD}
tags:
  - video-summary
type: video-summary
---

# {video title}

> [!info] 来源
> 作者：{channel name}
> 链接：[{video URL}]({video URL})
> 日期：{YYYY-MM-DD}

## 一句话核心

{one-line core point}

## 主要论据

1. **{point 1 title}** — {description}
2. **{point 2 title}** — {description}
3. **{point 3 title}** — {description}

## 关键信息

| 项目 | 内容 |
|------|------|
| ... | ... |

---

> 完整逐字稿见 [[{clean-title}-逐字稿]]
```

**Transcript note:** `Inbox/{clean-title}-逐字稿.md`

```markdown
---
title: "{video title} - 逐字稿"
source: "{video URL}"
author: "{channel name}"
date: {YYYY-MM-DD}
tags:
  - video-transcript
type: video-transcript
---

# {video title} - 逐字稿

> [!info] 来源
> 作者：{channel name}
> 链接：[{video URL}]({video URL})
> 日期：{YYYY-MM-DD}

视频总结见 [[{clean-title}-视频总结]]

---

{full transcript text}
```

Use the `obsidian` CLI to create both files:

```bash
obsidian create path="Inbox/{clean-title}-视频总结.md" content="{content}" silent
obsidian create path="Inbox/{clean-title}-逐字稿.md" content="{content}" silent
```

### Step 7: Cleanup

Remove all temp files:

```bash
rm -rf /tmp/video-summarizer
```

### Step 8: Report to user

Tell the user:
1. Both notes have been saved to Obsidian
2. The note names and paths
3. A brief one-line summary of the video content

## Notes

- For long videos (>30 min), Whisper turbo may take a while. Warn the user if the video is long.
- If yt-dlp fails, the URL may not be supported or may require authentication. Tell the user.
- If Whisper fails, check that it's installed and the turbo model has been downloaded (first run downloads ~1.5GB).
- The `obsidian create` command uses `\n` for newlines in the content parameter.
