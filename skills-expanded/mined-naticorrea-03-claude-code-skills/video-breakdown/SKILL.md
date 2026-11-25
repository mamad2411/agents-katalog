---
name: video-breakdown
description: Break down any video (YouTube, Loom, Instagram, TikTok, local file) frame by frame. Downloads the video, rips scene-change frames + a timestamped transcript locally, then Claude reads the visuals AND the words together to produce a content teardown — hooks, structure, on-screen visuals, why it works. Built in-house, no third-party code, only yt-dlp + ffmpeg. Trigger on "/video-breakdown", "break down this video", "analyze this reel/video", "teardown <url>", "what's working in this video".
---

# Video Breakdown

Reverse-engineer any video the way you actually watch one: visuals + audio at the same time. Built for competitor teardowns and ripping apart trending content in your niche.

## How it works
No video model. The skill splits the video into the two things Claude reads natively — **images** (frames) and **text** (transcript) — with timestamps lined up, so Claude knows what's on screen the moment something is said.

1. `yt-dlp` pulls the video + auto-captions from almost any site (YouTube, Loom, IG, TikTok) or a local file.
2. `ffmpeg` rips frames at every scene change (falls back to interval sampling for static talking-heads), capped at ~80.
3. Captions become a clean timestamped `transcript.txt` (no captions = on-screen text in frames still carries it).
4. Claude reads the frames + transcript and writes the breakdown.

## Run it

```bash
bash ~/.claude/skills/video-breakdown/scripts/grab.sh "<url-or-path>" [slug] [--start MM:SS] [--end MM:SS] [--every N]
```

- `slug` — folder name (auto-derived if omitted)
- `--start / --end` — only analyze a window
- `--every N` — seconds between frames when falling back to interval sampling (default 3)

Output lands in `~/claude-watch/library/<slug>/`:
- `frames/frame_*.jpg` — the visuals
- `frames/times.txt` — ffmpeg pts_time per frame (maps frame number → timestamp)
- `transcript.txt` — `[MM:SS] line` format
- `pacing.txt` — cut-rhythm summary (cut count, first-cut time, avg gap, slow-open/static/fast flags). Heuristic from ffmpeg scene detection, not a motion read.
- `meta.txt` — title, source, frame count

## Then (Claude's job)
1. Read `transcript.txt` fully.
2. Read the frames. Use `times.txt` to know when each frame happens, so visuals align to the script.
3. Produce the teardown. Default structure (adapt to what you asked for):
   - **TLDR** — one line on why this video works
   - **Hook** — first 0–3s, exact words + what's on screen
   - **Structure** — beat-by-beat with timestamps (acts, retention turns, CTA)
   - **Visual playbook** — cuts, text overlays, b-roll, motion, pacing
   - **Why it's trending / what to steal** — the transferable moves
   - If asked: graphics/motion prompts, script template, hook variations for a niche

## Notes
- Caption-less sources (often IG/TikTok, local files): grab.sh falls back to local whisper.cpp (`whisper-cli` + `~/.cache/whisper-cpp/ggml-small.en.bin`, no API key, on-device, wired in 2026-07-05). If whisper-cli or the model is missing, transcript says NO_CAPTIONS. Lean on frames + on-screen text, say so rather than guessing audio.
- Everything runs locally. No content leaves the machine except the original yt-dlp fetch.
- Frame folder is wiped + rebuilt on each run for the same slug.
