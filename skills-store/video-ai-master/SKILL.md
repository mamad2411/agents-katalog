---
name: video-ai-master
description: >-
  Master hub for AI video creation (2026). Generate, edit, and ship video end-to-end —
  text/image-to-video (Veo 3.1, Kling 2.5 Turbo Pro, Runway Gen-4.5, Sora 2, Luma Ray 2, Pika 2.2, Wan 2.2),
  cinematic prompts, multi-shot storyboards, fal.ai/Runway APIs (queue + signed webhooks), image-to-video
  consistency, Remotion v4 install + programmatic render/Lambda, HeyGen/Synthesia avatars, ElevenLabs
  voiceover/music/dub, ffmpeg post, automated QA, and platform export. Bundles 12 skills. Use for ads,
  reels, explainers, UGC, demos, or "install Remotion".
---

# AI Video Creation — Master Hub

End-to-end: **فكرة → سكريبت → storyboard → توليد AI → صوت → مونتاج → QA → تصدير لكل منصة**.

## Two production paths (combine them — that's the professional default)

| Path | When |
|------|------|
| **Generative AI** | photoreal B-roll, cinematic scenes, lifestyle, creative ads |
| **Remotion (code)** | `npx create-video@latest` → crisp brand text, prices, charts, captions, batch/localized variants |

Diffusion owns the *scene*; Remotion owns *everything that must be correct* (text, logo, price, legal). Never bake legible text into a generated frame.

## Workflow

```
video-ai-production-workflow (start — owns brief, artifact contract, cost ceiling)
  → ai-video-models-selection      (route per shot: quality × $ × audio + fallbacks)
  → ai-video-storyboard-multishot  (STORYBOARD.json: model/seed/ref per shot)
  → ai-video-cinematic-prompts     (5-part Veo formula, negative prompts)
  → ai-image-to-video-consistency  (refs, first-last-frame, character cameo)
  → ai-video-api-fal-runway        (generate: queue + signed webhooks + retries)
  → ai-video-audio-voiceover       (TTS VO, music, SFX, dub, caption timing)
  → remotion-programmatic-video    (overlays, captions, batch render) optional
  → video-ffmpeg-post-production   (normalize, concat, loudnorm, burn subs)
  → ai-video-qa-evaluation         (release gate: probe, artifacts, loudness)
  → video-social-export-specs      (master → per-platform variants)
```

Avatar-only: `ai-avatar-presenter-video`.

## Bundled skills (12)

- **video-ai-production-workflow** ⭐ — Pipeline orchestration, brief, artifact contract, cost ceiling, fallback policy, compliance gates.  
  → `skills/video-ai-production-workflow/GUIDE.md`
- **ai-video-models-selection** — Verified 2026 fal/Runway endpoints + params, native-audio, $/sec, fallback chains (Veo 3.1, Kling 2.5 Turbo Pro, Sora 2, Runway Gen-4.5, Luma Ray 2, Pika 2.2, Wan 2.2).  
  → `skills/ai-video-models-selection/GUIDE.md`
- **ai-video-cinematic-prompts** — Google's 5-part Veo formula, film grammar, dialogue/SFX syntax, negative prompts, seed locking, Arabic/RTL.  
  → `skills/ai-video-cinematic-prompts/GUIDE.md`
- **ai-video-storyboard-multishot** — Typed STORYBOARD.json, narrative arcs, transitions, character bible, idempotent batch generation.  
  → `skills/ai-video-storyboard-multishot/GUIDE.md`
- **ai-video-api-fal-runway** — fal queue (submit/status/result), ED25519 webhook verification, Runway SDK, retries, idempotency, cost logging.  
  → `skills/ai-video-api-fal-runway/GUIDE.md`
- **ai-image-to-video-consistency** — Reference-to-video, first-last-frame, Sora cameos, ref prep, Gemini-Flash→Veo workflow.  
  → `skills/ai-image-to-video-consistency/GUIDE.md`
- **remotion-programmatic-video** ⭐ — **Install Remotion** (`npx create-video@latest`), bundled FFmpeg, Studio, brownfield Next.js, programmatic render, `<Player>`, transitions, TikTok captions, Lambda.  
  → `skills/remotion-programmatic-video/GUIDE.md`
- **ai-video-audio-voiceover** — ElevenLabs TTS (eleven_v3/multilingual), Eleven Music, SFX, dubbing, word-level caption timing.  
  → `skills/ai-video-audio-voiceover/GUIDE.md`
- **ai-avatar-presenter-video** — HeyGen v3 (+v2 legacy), Synthesia (green-screen), localization, likeness consent + AI-labeling.  
  → `skills/ai-avatar-presenter-video/GUIDE.md`
- **video-ffmpeg-post-production** — Normalize+concat, two-pass loudnorm, sidechain ducking, burn/soft subs (RTL), chromakey.  
  → `skills/video-ffmpeg-post-production/GUIDE.md`
- **ai-video-qa-evaluation** — Release gate: ffprobe spec checks, black/freeze/silence, loudness, vision-LLM artifact/brand review, golden tests in CI.  
  → `skills/ai-video-qa-evaluation/GUIDE.md`
- **video-social-export-specs** — 2026 aspect/pixel/safe-zone/bitrate/length per platform, captions, master→variants.  
  → `skills/video-social-export-specs/GUIDE.md`

## Pairs well with

`color-design-master` (brand look/tokens), `content-seo-master` (ad copy/scripts),
`ai-mcp-master` (prompt engineering), `documents-master` (image generation for refs).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list. Always copy the exact
model `Model ID` from the live fal/Runway card before production — version strings drift (it's Kling **2.5 Turbo Pro**, not "Kling 3").
