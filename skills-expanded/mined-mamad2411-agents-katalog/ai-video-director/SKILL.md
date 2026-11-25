---
name: ai-video-director
description: Create AI-generated video content using Kling 3.0 (multi-shot sequences with dialogue), Sora (scene generation with character consistency), or Grok (restricted content). Use when writing shot-by-shot video prompts, building character-consistent animated series, or routing between video generation tools.
cluster: media-gen
version: 1.0.0
---

# AI Video Director

Write shot-by-shot video prompt sequences for AI video generation tools. Supports multi-shot sequences (up to 6 shots), dialogue with voice control, and character consistency across scenes.

## When to Use

- Writing multi-shot video sequences with scene transitions
- Creating AI-generated animated series with consistent characters
- Adding dialogue with emotion/tone control to video prompts
- Routing between video tools (Kling 3.0, Sora, Grok) based on content needs

## Tool Routing

| Tool | Best For | Key Capability |
|------|----------|----------------|
| **Kling 3.0** | Multi-shot sequences with dialogue | Up to 6 native shots, audio control, subject anchoring |
| **Sora** | Scene generation, character consistency | Best for narrative scenes, handles [cut] transitions |
| **Grok** | Restricted/romantic content | Fewer content restrictions than Sora |
| **Midjourney** | Character source images | Style/Omni reference for initial character design |

## Workflow

1. **Define characters** -- Lock identity traits early (appearance, clothing, key features)
2. **Write shot sequence** -- Describe each shot with cinematic language (profile, macro, tracking, POV)
3. **Add audio** -- Structure dialogue as `[Character: Label, tone]: "text"`
4. **Route to tool** -- Select based on content requirements and shot count
5. **Generate insert shots** -- Create reusable clips for character consistency

## Core Principles (Kling 3.0)

1. **Think in Shots, Not Clips** -- Use cinematic language (profile shots, macro close-ups, tracking, shot-reverse-shot)
2. **Anchor Subjects Early** -- Define core subjects clearly at the beginning for consistency
3. **Describe Motion Explicitly** -- Specify camera behavior (tracking, following, freezing, panning) AND subject movement
4. **Native Audio** -- Use `[Character A: Label, tone]: "Dialogue"` format with linking words for rhythm
5. **Image-to-Video: Lock First** -- Treat input image as anchor, focus on how scene evolves FROM the image

## Audio Prompting Rules

| Principle | Guideline | Example |
|-----------|-----------|---------|
| Structured Naming | Unique, consistent labels | `[Character A: Black-suited Agent]` |
| Visual Anchoring | Action first, then dialogue | `The agent slams the table. [Agent, angrily]: "Where?"` |
| Audio Details | Tone and emotion labels | `[Agent, raspy, deep voice]: "Don't move."` |
| Temporal Control | Linking words for rhythm | `[Agent]: "Why?" Immediately, [Assistant]: "Because."` |

## Character Consistency Workflow (Framer X)

For animated series with consistent characters across multiple scenes:

1. **Step 1:** Generate character source images (Midjourney Style/Omni reference)
2. **Step 2:** Create establishing scenes (Sora) with `[cut]` transitions
3. **Step 3:** Generate interaction scenes (Sora) in different environments
4. **Step 4:** Create insert shots for reusable character clips
5. **Step 5:** Route restricted content to Grok with custom source images

See `references/prompt-templates.md` for complete examples.
