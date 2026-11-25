---
name: Seedance
description: AI video generation using ByteDance Seedance via fal.ai. USE WHEN generate video, create video, text to video, image to video, Seedance, video generation, animate image, AI video.
---

# Seedance

AI video generation using ByteDance's Seedance model via fal.ai API. Supports text-to-video and image-to-video generation with audio.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/Seedance/`

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the Seedance skill"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **Seedance** skill...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Generate** | "generate video", "create video", "text to video", "image to video", "animate this" | `Workflows/Generate.md` |

## Quick Reference

```bash
# Text-to-video
bun run ~/.claude/skills/Seedance/Tools/Generate.ts \
  --prompt "A cat walking through a neon city" \
  --duration 5 --resolution 720p --output ~/Downloads/video.mp4

# Image-to-video (animate a still image)
bun run ~/.claude/skills/Seedance/Tools/Generate.ts \
  --image ~/Downloads/photo.png \
  --prompt "Camera slowly zooms in, gentle wind" \
  --duration 5 --output ~/Downloads/animated.mp4
```

**Environment:** Requires `FAL_KEY` in `~/.claude/.env`

**Full API details:** `ApiReference.md`

## Current Model

**Seedance 1.5 Pro** (fal.ai) — Latest available via API.
Seedance 2.0 is China-only (Dreamina) as of Feb 2026. When it hits fal.ai, update the endpoint constant in `Tools/Generate.ts`.

## Examples

**Example 1: Generate video from text**
```
User: "generate a video of ocean waves at sunset"
-> Invokes Generate workflow
-> Calls fal.ai Seedance text-to-video
-> Downloads MP4 to ~/Downloads/
-> Opens video for preview
```

**Example 2: Animate a still image**
```
User: "animate this image" (with reference to an image)
-> Invokes Generate workflow (image-to-video mode)
-> Uploads image + prompt to fal.ai
-> Returns animated video
```

**Example 3: High-res cinematic clip**
```
User: "generate a cinematic 1080p video of a samurai walking through fog, 10 seconds"
-> Invokes Generate workflow
-> --resolution 1080p --duration 10
-> Full HD output with audio
```
