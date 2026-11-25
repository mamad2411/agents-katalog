---
name: social-video-analyzer
description: "Download and analyze any social media video from Instagram, YouTube, TikTok, X/Twitter, Reddit, Facebook, Vimeo, Twitch, and 1000+ platforms. Get full transcripts, visual scene descriptions, key takeaways, and content format analysis using Gemini native video understanding. Supports custom analysis prompts for competitive research, content repurposing, ad analysis, and influencer tracking. Built for AI agents — uses yt-dlp for downloading and Google Gemini for analysis. Use for video transcription, social media monitoring, content analysis, competitor research, video summarization, and multimedia intelligence."
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["GOOGLE_AI_API_KEY"]}, "primaryEnv": "GOOGLE_AI_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🎬 Social Video Analyzer

Download and analyze any social media video — Instagram, YouTube, TikTok, X, Reddit, and 1000+ more platforms.

## Features

- **Download from 1000+ sites** via yt-dlp (YouTube, Instagram, TikTok, X, Reddit, Facebook, Vimeo, Twitch)
- **Transcribe full audio** — complete spoken content extraction
- **Describe visuals** — scene-by-scene breakdown of what's shown
- **Extract key takeaways** — summarized main points
- **Analyze content format** — platform, duration, style, production quality
- **Custom prompts** — ask specific questions about any video
- **Native video understanding** — Gemini processes video natively (not frame extraction)
- **Shell and Python interfaces** — quick bash script or full Python control
- **Auto-cleanup** — temporary files managed automatically
- **Handles large videos** — up to 2GB per Gemini API limits

## Requirements

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_AI_API_KEY` | ✅ | Get from [Google AI Studio](https://aistudio.google.com/apikey) |

## Quick Start

```bash
# Quick analysis (shell)
./skills/social-video-analyzer/scripts/analyze_video.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Full control (Python)
GOOGLE_AI_API_KEY=your_key python3 skills/social-video-analyzer/scripts/analyze_video.py "https://youtube.com/watch?v=VIDEO_ID"

# Custom question
python3 skills/social-video-analyzer/scripts/analyze_video.py "https://tiktok.com/@user/video/123" --prompt "What product is being advertised?"
```

## Commands

### Shell Script (Quick)
```bash
./scripts/analyze_video.sh "VIDEO_URL"
```

### Python (Full Control)
```bash
# Default analysis
python3 scripts/analyze_video.py "VIDEO_URL"

# Custom prompt
python3 scripts/analyze_video.py "VIDEO_URL" --prompt "Your question"

# Competitive analysis
python3 scripts/analyze_video.py "VIDEO_URL" --prompt "What hooks and CTAs are used?"

# Content repurposing
python3 scripts/analyze_video.py "VIDEO_URL" --prompt "Extract quotes suitable for social media posts"
```

## Output Format

```
## Transcript
[Full spoken content]

## Visual Description
[Scene-by-scene breakdown]

## Key Takeaways
- Point 1
- Point 2

## Content Format Analysis
- Platform: YouTube
- Duration: ~3:20
- Style: Tutorial/explainer
- Production: Professional
```

## Supported Platforms

YouTube, Instagram, TikTok, X/Twitter, Reddit, Facebook, Vimeo, Twitch clips, and [1000+ more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Script Reference

| Script | Description |
|--------|-------------|
| `{baseDir}/scripts/analyze_video.sh` | Quick shell wrapper for video analysis |
| `{baseDir}/scripts/analyze_video.py` | Full Python CLI with custom prompts |

## Limitations

- Max video size: 2GB (Gemini API limit)
- Private/login-required videos may fail
- Rate limits apply per platform

## Data Policy

Videos are temporarily downloaded for analysis, uploaded to Google Gemini API for processing, and auto-cleaned after 48 hours.

---

Built by [M. Abidi](https://www.agxntsix.ai)

[LinkedIn](https://www.linkedin.com/in/mohammad-ali-abidi) · [YouTube](https://youtube.com/@aiwithabidi) · [GitHub](https://github.com/aiwithabidi) · [Book a Call](https://cal.com/agxntsix/abidi-openclaw)
