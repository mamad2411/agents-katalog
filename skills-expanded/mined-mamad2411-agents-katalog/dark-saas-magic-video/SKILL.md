---
name: dark-saas-magic-video
description: >
  Create dark cinematic SaaS/product motion videos in the Presenton-like "magic
  UI" style: black starfield stage, bottom purple glow, large kinetic type,
  cyan-to-magenta CTA buttons, prompt cards, floating UI templates, integration
  badges, model rings, export objects, speed-blur transitions, and short
  product capability arcs. Use when the user asks for "这种风格", "同款风格",
  dark SaaS promo, AI product demo, magic UI product video, or a style-level
  creation inspired by a reference video. Do not use for pixel-level or
  frame-accurate replication; use reference-video-replica-qc first for that.
---

# Dark SaaS Magic Video

## Role

Create new product videos in a dark, cinematic, UI-conjuring style. This is a
style-generation skill, not a reference-alignment skill. Use it after
`video-production-director` selects a style-level product or SaaS video route.

## Canonical Showcase

- Human display name: 暗色 SaaS 魔术短片
- Example finished piece: 雪踏乌云暗色 SaaS 介绍短片
- File: `assets/showcases/xuetawuyun-dark-saas-showcase-1080p.mp4`
- Use this as a style reference for scale, pacing, scene vocabulary, and final
  polish. Do not copy its text unless the user asks for the same brand/account.

## Boundaries

- Use this for style-level creation: "做成这个感觉", "类似 Presenton 这种风格",
  "暗色科技感 SaaS 产品短片", "AI 工具产品演示".
- Do not use this for pixel-level, frame-accurate, or timestamp-accurate
  remakes. Use `reference-video-replica-qc` first.
- Do not replace `product-launch-video`; use this when the requested visual
  language is specifically dark magic UI, not a generic product launch.
- Build with HyperFrames unless the user explicitly requests Remotion.

## Required Reads

Before writing a composition, read:

1. `references/style-language.md`
2. `references/scene-blueprints.md`
3. `references/timing-presets.md`
4. `references/asset-contract.md`

Before final handoff, read `references/qc-checklist.md`.

## Inputs

Collect or infer:

- product name and one-line promise
- target viewer and platform
- duration preset: `sting`, `standard`, or `extended`
- pain words or opening claim
- core workflow: prompt, generate, connect, model, export, share, automate
- available assets: logo, screenshots, UI cards, integration logos, export names
- output ratio and archive slug

If assets are missing, use abstract UI cards and text badges. State that the
result is a style-level product video, not a product-accurate UI recording.

## Hard Style Rules

1. Use a black spatial stage with fine grain/star particles and a weak bottom
   purple horizon glow.
2. Avoid persistent horizontal neon-line backgrounds; they flatten the style.
3. Use large white kinetic typography as story beats, not small labels.
4. Include at least one cyan-to-magenta gradient CTA that triggers a visible
   transformation.
5. Make hero objects large at their most visible frame: prompt card, CTA, UI
   board, badge ring, or export object must not feel like tiny distant props.
6. Use speed blur, smear, scale rush, or white velocity wipes for major
   transitions.
7. Include UI objects that feel summoned from darkness: cards, badges, folders,
   model chips, app windows, or export pills.
8. Never add unexplained full-screen solid color flashes.
9. Never claim pixel-level fidelity for this style workflow.

## Workflow

### 1. Shape The Arc

Pick a duration preset from `references/timing-presets.md`. Map the product into
5-8 capability beats. Prefer a cause-and-effect chain: text promise -> prompt ->
CTA click -> generated result -> integrations/models -> export -> final claim.

### 2. Select Blueprints

Use `references/scene-blueprints.md` to choose scene modules. Do not blindly use
all modules; match the product's real capabilities.

### 3. Build With HyperFrames

Load the relevant HyperFrames skills:

- `hyperframes` for composition authoring
- `hyperframes-cli` for lint, validate, inspect, render
- `hyperframes-animation` for speed blur, type motion, rings, cursor clicks
- `hyperframes-media` only if audio, TTS, SFX, or captions are needed

Use deterministic motion. Build hero frames first, then animate into them.

### 4. QC

Use `references/qc-checklist.md`. If the user supplied a reference video and
cares about alignment, also use `reference-video-replica-qc`.

## Output

Deliver the final MP4 path, QC contact sheet path, confirmed specs, and a short
note naming the duration preset and scene modules used.
