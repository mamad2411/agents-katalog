---
name: remotion-best-practices
description: Design and implement maintainable Remotion video compositions with deterministic rendering.
category: design
aliases:
- remotion
- video
- react-video
- motion
triggers:
- Make a video with Remotion
- Render a Remotion project
- Remotion composition
- Programmatic video
keywords:
- remotion
- video
- react
- composition
- render
- motion
- ffmpeg
- programmatic
dependencies:
- optional:node
- optional:remotion
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- remotion-best-practices
- design
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- best
- composition
- design
- practices
- react
- remotion
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Remotion Best Practices

## Purpose
Build Remotion projects that are correct, performant, and renderable in a CI-style
pipeline. The skill encodes patterns for composition, asset loading, timing,
preview, and headless render so an agent can write or modify a Remotion codebase
without common pitfalls.

## When to Use
- The user is building or modifying a Remotion project
- A programmatic video needs to be rendered headlessly (server, CI)
- A new composition needs to be added to an existing project

## When NOT to Use
- The user wants to edit a video with a GUI (use a video editor)
- The user wants stock footage, music, or voiceover selection (use a media skill first)

## Capabilities
- Structure a Remotion project (`src/Composition.tsx`, `src/Root.tsx`, `remotion.config.ts`)
- Use `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`, `Sequence`
- Load static assets via `staticFile()` and respect `public/`
- Configure render concurrency, codec, and pixel format
- Set up `npx remotion render` in a CI pipeline with deterministic output
- Use `@remotion/lambda` or `@remotion/cloud-run` for cloud rendering
- Use `@remotion/media-parser` to inspect and validate media

## Inputs
- The composition to build (description)
- The target fps (default 30), resolution (default 1920Ã—1080), duration (in seconds)
- The render target (local, Lambda, Cloud Run)
- The codec (default `h264`)

## Workflow
1. **Verify** `node` â‰¥ 18, `ffmpeg` on PATH, `@remotion/cli` installed.
2. **Define composition** in `src/Root.tsx` with `<Composition id=â€¦ fps=â€¦ width=â€¦ height=â€¦ durationInFrames=â€¦ />`.
3. **Load assets** via `staticFile()` and put files under `public/`.
4. **Build the timeline** with `Sequence`, `AbsoluteFill`, and proper `useCurrentFrame` math.
5. **Optimize** — `spring()` over manual interpolation, `OffthreadVideo` over `<video>`, pre-encode expensive transitions.
6. **Preview** with `npx remotion studio`.
7. **Render** with `npx remotion render <compId> out/<id>.mp4 --concurrency 4 --codec h264`.
8. **Validate** the output (`ffprobe`, file size, frame count) and surface a thumbnail.

## Tools
optional:node, optional:remotion

## Examples
**User:** "Make a 10-second countdown video."
**Response:** Single composition, 300 frames @ 30 fps. `spring()` scale on each
tick. Render to `out/countdown.mp4`.

**User:** "Render this in Lambda."
**Response:** `npx remotion lambda render <compId> out/<id>.mp4 --region us-east-1`.

## Safety
- Respect third-party asset licenses
- Never auto-upload rendered video to a public bucket without consent
- Pin Remotion version in `package.json`
- Do not embed unverified `userId` / `apiKey` in the composition

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical design category.
