---
name: trycook-media
description: Generate images, video clips, music, sound effects, voiceovers, and avatars using TryCook CLI media tools. Use when asked to "generate image", "create video", "make a clip", "voiceover", "text to speech", "generate music", "sound effect", "create avatar", "transcribe", "stock footage", or any media creation request.
allowed-tools:
  - Bash(trycook *)
  - Read
---

# TryCook Media Generation

Generate images, video clips, music, voiceovers, avatars, and more via the TryCook CLI.

**Prerequisite:** Ensure `trycook status` shows authenticated before proceeding.

## Image Generation

```bash
# Get the schema first
trycook tool info generate_image

# Generate an image
trycook tool call generate_image '{"prompt": "professional product photo of a skincare bottle on marble surface, studio lighting", "aspect_ratio": "1:1"}'
```

The response includes `imageUrl` — a presigned URL to the generated image.

### Image Editing

```bash
trycook tool info edit_image
trycook tool call edit_image '{"imageUrl": "https://...", "prompt": "remove the background and replace with gradient"}'
```

## Video Clip Generation

```bash
trycook tool info generate_clip
trycook tool call generate_clip '{"prompt": "slow motion pour of golden honey, cinematic lighting, 4K", "duration": 5}'
```

Returns a video URL. Clips are typically 3-10 seconds.

## Audio & Voice

### Voiceover (Text-to-Speech)

```bash
trycook tool info create_voiceover
trycook tool call create_voiceover '{"text": "Welcome to our brand new product line.", "voice": "alloy"}'
```

### Music Generation

```bash
trycook tool info generate_music
trycook tool call generate_music '{"prompt": "upbeat corporate background music, 120bpm", "duration": 30}'
```

### Sound Effects

```bash
trycook tool info generate_sound
trycook tool call generate_sound '{"prompt": "cash register cha-ching sound"}'
```

## Transcription

Convert audio/video to text with word-level timestamps:

```bash
trycook tool info transcribe_audio
trycook tool call transcribe_audio '{"url": "https://example.com/audio.mp3"}'
```

Returns transcript with word-level timestamps (Remotion Caption format).

## Video Analysis

Analyze video content with AI:

```bash
trycook tool info analyze_video
trycook tool call analyze_video '{"url": "https://youtube.com/watch?v=...", "prompt": "identify the key moments and speakers"}'
```

Accepts YouTube URLs directly.

## Stock Media Search

```bash
trycook tool info search_stock
trycook tool call search_stock '{"query": "business meeting handshake", "type": "video"}'
```

## Avatar Generation

```bash
trycook tool info create_avatar
trycook tool call create_avatar '{"name": "Sarah", "description": "professional woman in her 30s, business attire"}'
```

## Workflow: Full Ad Creative Pipeline

1. **Research** — `scrape_website` the brand's site for copy/imagery
2. **Generate hero image** — `generate_image` with brand-aligned prompt
3. **Generate b-roll clips** — `generate_clip` for supporting video content
4. **Create voiceover** — `create_voiceover` with script
5. **Add music** — `generate_music` for background track

Each step returns URLs that can be passed to subsequent tools.

## Tips

- Image prompts work best with specific details: lighting, angle, style, subject position
- Video clips default to ~5 seconds — specify `duration` for longer
- Voiceover `voice` options: check schema via `trycook tool info create_voiceover`
- Always check the response `ok` field before using output URLs
