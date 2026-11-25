---
name: yueying
description: Let AI watch videos. Use when the user gives a local video/audio file path or a video URL (YouTube, Bilibili, Douyin, Xiaohongshu, TikTok, Vimeo …) and wants a summary, notes, answers, extracted steps/commands/code, or to follow a tutorial. Prefer the yueying MCP tools when available, otherwise run the yueying CLI to get a timestamped transcript plus keyframes, then read the results. 让 AI 看视频。用户给出本地视频文件路径或视频链接（B站、YouTube、抖音、小红书等），想要总结、提取信息、答疑、照着教程操作、整理笔记时使用。先用 yueying 命令把视频转成文字稿和关键帧，再读结果完成用户的需求。
---

# yueying (阅影) · Let AI watch videos

You cannot open a video file, but you can read text and images. yueying turns a video into:
a timestamped transcript (platform subtitles first; otherwise local faster-whisper speech
recognition in dozens of languages), keyframes taken at scene changes (each labelled
"#number mm:ss" bottom-left), 3x3 contact sheets, and a `report.md` index. Everything runs offline.

## Step 0 — use the MCP tools when they exist

If MCP tools named `watch_video` / `get_transcript` / `search_transcript` / `get_frames` /
`get_frame_at` / `list_videos` from a server called `yueying` are available, use them and skip the
CLI steps below:

1. `watch_video(video=<absolute path or URL>)`. If the reply starts with `RUNNING`, call
   `watch_video` again with the same `video` to keep waiting (it resumes the same job); do not start
   another video meanwhile. `DONE` contains the overview and the transcript.
2. `get_frames(video=<video_id>)` shows the contact sheets — read these before single frames.
   `get_frame_at(video, time="03:15")` for one exact moment (code, slides, UI).
   `get_transcript` for a time range, `search_transcript` to find where something is said.

## CLI steps (no MCP server)

1. Run (the first speech recognition downloads a model, which can take minutes; long videos take a
   while — be patient):

   ```
   yueying "<video path or URL>" --out "<absolute output dir>"
   ```

   - Use an absolute `--out`, e.g. `<project>/yueying_out/<video-name>`; without `--out` the
     default is `./yueying_out/<video-name>` relative to the current directory.
   - Add `--ui-lang en` when the user writes in English (report.md headings in English; the
     default is Chinese).
   - Nobody speaks / only the pictures matter: add `--no-asr`. Text only, no pictures: `--no-frames`.
   - Known language: `--lang zh` / `--lang en` / `--lang ja` … improves accuracy.
   - Dense visual detail (code, slides, demos): `--interval 2` (one frame every 2 s). The default is
     automatic by duration: 2 s under 1 min, 6 s under 10 min, 12–20 s for longer videos.
   - HD or member-only Bilibili, sign-in-gated YouTube: `--cookies-from-browser chrome` (or `edge`;
     close Chrome first on Windows).
   - Slow machine or no NVIDIA GPU: `--model small` (or `--model auto`, which picks
     large-v3-turbo on a GPU and small on CPU).
   - Several videos at once: pass several paths/URLs; each gets its own folder under `--out` plus an
     `index.md`. Bilibili multi-part / collections / playlists: add `--all` to process every entry.

2. Read `report.md` in the output folder: summary, chapters, list of contact sheets, list of
   keyframes, and the transcript in timestamped paragraphs.

3. Read `grid_01.jpg` etc. (contact sheets) to get the visual storyline. Open single frames in
   `frames/` only when you need to read code, slides or UI text at one moment. Match pictures to the
   transcript by timestamp.

4. Deliver what the user asked for: summary, steps, code, answers, notes. Quote the video with
   timestamps like (03:15) so the user can jump there.

## Notes

- Speech recognition mis-hears names, numbers and code; trust on-screen text from frames over
  the transcript.
- For long transcripts, do not read everything: start with chapters and contact sheets, then read
  the relevant time range.
- If the command is missing: `pip install yueying` then `yueying --install-skill`; on a machine
  with an NVIDIA GPU also `pip install "yueying[cuda]"`. With uv: `uvx yueying "<path or URL>"`.

## 中文提示

- 有 `yueying` MCP 工具时优先用 `watch_video`；回复以 `RUNNING` 开头就用同一个 `video` 再调一次，不要同时开第二个视频。
- 没有 MCP 时运行 `yueying "<视频路径或链接>" --out "<绝对路径输出目录>"`，然后读 `report.md`、`grid_01.jpg` 等总览图，需要细节再看 `frames/` 单帧。
- 语音识别可能把专有名词、代码听错，画面上的文字以画面为准；引用视频内容时带上时间点，如「（03:15）」。
