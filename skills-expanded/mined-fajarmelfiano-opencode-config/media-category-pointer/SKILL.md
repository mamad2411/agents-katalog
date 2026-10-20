---
name: media-category-pointer
description: "Pointer to a library of 42 specialized Media skills. Use when working on media-related tasks."
risk: none
---

# Media Capability Library 🎯

This is a **pointer skill**. The 42 specialized Media skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **ai-image-generation-studio** — Install and use the official AI Image Generator package, pinned by digest, for paid hosted work on the Beatra service.
- **ai-logo-maker** — Install and use the official AI Logo Maker package, pinned by digest, for paid hosted work on the Beatra service.
- **ai-multilingual-dubbing** — Install and use the official Multilingual Voiceover package, pinned by digest, for paid hosted work on the Beatra service.
- **ai-photo-restyler** — Install and use the official Photo to Anime package, pinned by digest, for paid hosted work on the Beatra service.
- **ai-podcast-voiceover** — Install and use the official AI Podcast Voiceover package, pinned by digest, for paid hosted work on the Beatra service.
- **atlas-cloud-media** — Generate Atlas Cloud images and videos through its asynchronous media API with schema-first model selection and credential-safe polling.
- **beatra** — Install and use the official AI Media Generator package, pinned by digest, for paid hosted work on the Beatra service.
- **beatra-ai-video-studio** — Install and use the official Beatra AI Video Studio package, pinned by digest, for paid text-to-video, image-to-video, and video edit or extend jobs on the hosted Beatra service.
- **ecommerce-listing-image-set** — Install and use the official Ecommerce Product Images package, pinned by digest, for paid hosted work on the Beatra service.
- **film-crew** — Turn a one-line AI video idea into a shot list and per-shot, model-ready prompts via a film crew (director, DP, gaffer, editor, script supervisor). Also fixes failing video prompts and diagnoses bad clips before a reroll. Works with Wan, LTX, Kling, Veo, Seedance, Hailuo, Runway.
- **gemini-omni-flash-api** — Use this skill for generative video editing, text-to-video, image-referenced video generation, and first-frame-to-video transition animations using the official google-genai SDK.
- **generate-nanobanana** — Generate and edit images/video with Google's Gemini media models (Nano Banana 2/Pro, Gemini Omni Flash), with cost-approval gates, reference-image support, and a prompt/output log per call.
- **image-generator** — Generate and edit images using Gemini's Nano Banana Pro model (gemini-3-pro-image-preview). Use this skill when the user asks you to generate images, create visuals, edit photos, create logos, generate product mockups, or perform any image generation/editing task.
- **ingest-youtube** — Pull a YouTube video transcript into a queryable markdown vault with yt-dlp subtitle discovery, VTT cleanup, metadata frontmatter, and capture-seed stubs.
- **macos-screen-recorder** — macOS screen recorder that captures the main display PLUS system audio via ScreenCaptureKit — no BlackHole/loopback driver, no sudo, just the standard Screen Recording permission. CLI-driven; fills the headless-screen-recording-with-system-sound gap QuickTime and `screencapture -v` can't.
- **magic-animator** — AI-powered animation tool for creating motion in logos, UI, icons, and social media assets.
- **md2video-audio** — Convert Markdown documents into narrated MP4 videos with synchronized visuals and voice narration.
- **muapi-media** — Generate images and videos with MuAPI's schema-driven asynchronous media API while protecting keys, polling, and output downloads.
- **music-generation-studio** — Install and use the official AI Music Generator package, pinned by digest, for paid hosted work on the Beatra service.
- **nsfw-ai-spicyapi** — Generate adult (18+) images, image-to-video clips and image edits through the SpicyAPI API, with a cost quote before every paid run and adults-only / consent rules.
- **podcast-generation** — Generate real audio narratives from text content using Azure OpenAI's Realtime API.
- **poster-design-studio** — Install and use the official AI Poster Maker package, pinned by digest, for paid hosted work on the Beatra service.
- **product-photo-studio** — Install and use the official AI Product Photography package, pinned by digest, for paid hosted work on the Beatra service.
- **remotion** — Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays
- **remotion-best-practices** — Best practices for Remotion - Video creation in React
- **remotion-captions** — Transcribing, displaying and animating captions
- **remotion-create** — Create a new Remotion video
- **remotion-docs** — Search Remotion documentation
- **remotion-interactivity** — Structure Remotion markup for interactivity
- **remotion-render** — Export a Remotion video
- **screenstudio-alt** — Open-source headless Screen Studio alternative: auto speed-up of idle, auto-zoom on click clusters, keystroke overlay chips, smoothed synthetic cursor, and 9:16 vertical export that follows the action — post-production for screen recordings from the CLI.
- **slack-gif-creator** — A toolkit providing utilities and knowledge for creating animated GIFs optimized for Slack.
- **stability-ai** — Geracao de imagens via Stability AI (SD3.5, Ultra, Core). Text-to-image, img2img, inpainting, upscale, remove-bg, search-replace. 15 estilos artisticos.
- **suno-lyrics-to-song** — Install and use the official Lyrics to Song package, pinned by digest, for paid hosted work on the Beatra service.
- **talking-avatar-video** — Install and use the official Talking Avatar Video package, pinned by digest, for paid hosted work on the Beatra service.
- **video-router** — Route a video-production brief to generation, deterministic composition, supplied-footage editing, or an automatic cross-modal plan before production begins.
- **videodb** — Video and audio perception, indexing, and editing. Ingest files/URLs/live streams, build visual/spoken indexes, search with timestamps, edit timelines, add overlays/subtitles, generate media, and create real-time alerts.
- **videodb-skills** — Upload, stream, search, edit, transcribe, and generate AI video and audio using the VideoDB SDK.
- **viral-video-teardown-remake** — Install and use the official Viral Video Remake package, pinned by digest, for paid hosted work on the Beatra service.
- **voice-cloning-studio** — Install and use the official AI Voice Cloning package, pinned by digest, for paid hosted work on the Beatra service.
- **voiceover-narration-studio** — Install and use the official AI Voiceover Generator package, pinned by digest, for paid hosted work on the Beatra service.
- **web-media-getter** — One query across free image / video / GIF APIs (stock + historical/archival + GIF engines), returning normalized, license-tagged results with optional top-K download + attribution sidecar. The retrieval peer to local semantic search and generative media.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/media/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/media`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
