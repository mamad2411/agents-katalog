---
name: unflick-clip-gif
description: >-
  Cut a video clip or make a GIF from a moment in a video using the unflick
  player. Use when the user asks to "clip", "trim", "cut", "extract a segment",
  "make a GIF", or "grab that part" from a file or what's currently playing.
  Requires the unflick MCP server (or CLI) and ffmpeg on PATH.
license: MIT
---

# unflick: clip & GIF extraction

Extract a segment from a video as MP4 or GIF via the `clip` tool. Needs `ffmpeg`
on PATH (bundled with the Windows AI edition; otherwise install separately).

## Tool

`clip(start, end, file?, output?, gif?)`
- `start`, `end` — seconds (required).
- `file` — input path; **omit to clip the currently playing file**.
- `output` — destination path; auto-generated next to the source if omitted.
- `gif` — `true` to export an animated GIF instead of MP4.

## Typical flows

- **"Clip the last 10 seconds I just watched"** → `get_status` for `position`,
  then `clip(start=position-10, end=position)`.
- **"Make a GIF of 0:05–0:08 from intro.mp4"** →
  `clip(file="intro.mp4", start=5, end=8, gif=true)`.

```bash
unflick clip 5 8 --gif --output meme.gif
unflick clip 90 120 --output highlight.mp4
```

## Guidance

- Clamp `end` to the file's `duration` (from `file_info` or `get_status`).
- GIFs balloon fast — keep ranges short (a few seconds) and warn the user if
  they ask for a long GIF.
- Always report the final output path back to the user.
