---
name: media-gen-orchestrator
description: "Route a media-generation task to the right tool among 11 specialists — image generation (GPT Image 2, Nano Banana 2, OpenAI Images), image enhancement, image-to-3D, AI video direction, FFmpeg processing, frame extraction, and GIF search/authoring. USE WHEN a user wants to generate, edit, upscale, convert, or assemble an image, 3D model, video, or GIF but hasn't named the specific tool or backend."
cluster: media-gen
version: 1.0.0
---

# Media-Gen Orchestrator

The single entry skill for generative + transformational media work. It locates the task on the
**modality × stage** map — *what asset* (image / 3D / video / GIF) and *what stage* (generate →
transform → assemble) — and delegates to one of 11 specialist spokes. The cross-cutting decision
every request shares — **which backend to route to, given its access/billing model and the
modality** — lives in `media-gen-core`; read it before picking an image or video generator.

## Routing map (intent → spoke)

**Generate an image**
- Via your ChatGPT Plus/Pro plan, no per-image billing → `gpt-image-2`
- Via Google Gemini 3.1 Flash Image (multi-image input, Search grounding) → `nano-banana-2`
- Batch generation against the OpenAI Images API (+ gallery) → `openai-image-gen`
- Headers, icons, diagrams, mermaid, infographics (a full visual-content system) → `art`

**Transform / clean up an image**
- Upscale, sharpen, de-noise screenshots & assets → `image-enhancer`
- Restyle / edit an existing image (image-to-image) → `gpt-image-2`, `nano-banana-2`  *(both edit, not just generate)*

**Make a 3D asset**
- Image(s) → textured mesh (GLB/OBJ/PLY/STL) via Hunyuan3D-2.1 → `hunyuan3d`

**Generate video**
- Shot-by-shot AI video (Kling / Sora / Grok), character-consistent series → `ai-video-director`

**Process / assemble video**
- Convert, resize, compress, extract audio, GIF↔MP4 → `ffmpeg`
- Pull frames or short clips out of a video → `video-frames`

**Work with GIFs**
- Search GIF providers, download, extract stills/sheets → `gifgrep`
- Author a size-constrained animated GIF for Slack → `slack-gif-creator`

## Picked-up spokes

Additional image-generation spokes (picked up from antigravity-awesome-skills, MIT). Route to these
alongside the generators above:

- **Standalone Gemini image CLI** — generate an image from a prompt with *only* a `GEMINI_API_KEY`
  and stdlib Python, no MCP server (good for UI placeholders, docs illustrations, icons) → `imagen`
- **SEO-optimized image assets** — OG/social cards, blog heroes, schema `ImageObject` visuals,
  product shots, infographics, each with per-use-case aspect ratio + resolution and a post-gen SEO
  checklist (alt text, WebP, schema, `og:image` tags) → `seo-image-gen`

Routing note: prefer `seo-image-gen` when the image is destined for a page/social card and must be
search/social optimized; prefer `imagen` for a quick subscription-free local generate; prefer the
plan-backed generators (`gpt-image-2`, `nano-banana-2`, `openai-image-gen`) when their specific
backend/capability (multi-image input, character consistency, batch gallery) is required.

## Standard Operating Flow

1. Locate the task: which **modality** (image / 3D / video / GIF) and which **stage** (generate →
   transform → assemble).
2. If it **generates** an image or video, pull the routing model from `media-gen-core` first —
   the right backend depends on access (subscription vs API key vs local GPU/HF), cost, and the
   specific capability needed (multi-image input, character consistency, format).
3. Delegate to the spoke(s). Multi-step asks fan out in modality order — generators produce
   assets, then processors transform/assemble them. E.g. *"make an animated logo intro"* →
   `art`/`gpt-image-2` (frames) → `ai-video-director` or `ffmpeg` (motion) → `ffmpeg` (encode).
4. Return: chosen spoke(s), the backend/model selected and why (access + capability), the output
   format, and the next action.

## Guardrails

See `media-gen-core`. In short: **confirm the backend's prerequisite before generating** — a
subscription-backed CLI (`gpt-image-2`), an API key + billing (`openai-image-gen`, paid image
APIs), or a local/hosted GPU (`hunyuan3d` via HF Gradio) are *not* interchangeable, and silently
picking the wrong one wastes a paid call or fails. Generation is non-deterministic and may incur
cost or rate limits — state the cost/quota implication before a batch. Respect provider content
policies and the license/attribution of any downloaded GIF or reference image. Keep `ffmpeg`/
`video-frames` re-encodes lossless-aware (don't silently transcode a master).

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as
skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named
above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside
the skill-clusters repo).
