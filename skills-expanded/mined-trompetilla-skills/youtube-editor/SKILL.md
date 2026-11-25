---
name: youtube-editor
description: Automate YouTube video editing workflow: Download -> Transcribe (Whisper) -> Analyze (GPT-4) -> High-Quality Thumbnail (Korean & Character Consistency).
version: 1.0.13
author: Flux
---

# 🎬 YouTube AI Editor (v1.0.13)

**Turn raw videos into YouTube-ready content in minutes.**

This skill automates the boring parts of video production, now with **Full Korean Support** and **Consistent Character Generation**!

---

## ✨ Features

- **📥 Universal Download:** Supports YouTube URLs and local video files.
- **🗣️ Auto-Subtitles:** Generates accurate `.srt` subtitles using OpenAI Whisper.
- **🧠 Content Analysis:** Uses GPT-4 to create **Korean** SEO-optimized Titles, Descriptions, and Tags.
- **🎨 AI Thumbnails (Pro):**
    - **Consistent Character:** Maintains the style of your avatar (or the default Pirate Lobster) while generating new poses! (Image-to-Image)
    - **Custom Fonts:** Paperlogy ExtraBold included.
    - **Background Removal:** Automatically removes background from the generated character.
    - **Layout:** Professional Black & Gold design.
- **🛡️ Security Hardening (v1.0.11):**
    - YouTube URL allowlist validation (blocks localhost/private-network targets)
    - HTML-escaped text rendering in thumbnail templates
    - Safer fixed Nano Banana script resolution + subprocess timeout

---

## 🛠️ Dependencies

### 1. System Tools
Requires **FFmpeg** (install via your package manager).

### 2. Python Packages (optional)
For advanced thumbnail features, install:
- `playwright` + `rembg[cpu]`

### 3. API Keys (environment variables)
Set these before running:
- `OPENAI_API_KEY` - For Whisper & GPT-4
- `NANO_BANANA_KEY` - For AI character generation

---

## 🚀 Usage

### Option 1: Fully Automated (Pirate Lobster Mode)
The AI will generate a **Pirate Lobster character** doing something related to your video, while keeping the original character design consistent.

```bash
# Run from skills/youtube-editor/
uv run scripts/process_video.py --url "https://youtube.com/watch?v=YOUR_VIDEO_ID"
```

### Option 2: Custom Branding (Your Face)
Use your own photo as the base avatar. The AI will generate **"You" doing different actions**!

```bash
uv run scripts/process_video.py \
  --input "video.mp4" \
  --author "My Awesome Channel" \
  --avatar "/path/to/my_face.jpg"
```

---

*Created by Flux (OpenClaw Agent)*
