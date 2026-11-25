---
name: media-gen-core
description: "Shared reference for the media-gen cluster: the backend-routing decision (access/billing model × modality), the generate→transform→assemble pipeline, output-format conventions, and the cross-tool guardrails. USE WHEN choosing an image/video/3D/GIF backend, planning a multi-stage media pipeline, or reasoning about cost, format, or provider policy."
cluster: media-gen
version: 1.0.0
---

# Media-Gen Core

Shared model for the `media-gen` cluster. The generators and processors all hang off one
decision and one pipeline — keep them consistent here so no spoke contradicts another.

## 1. The routing decision (this cluster's defining choice)

Every generative request resolves on two axes: **modality** (what asset) × **access model** (what
it costs / what it needs to run). Pick the cell, then the spoke.

```
Request ──> [ modality: image | 3D | video | GIF ]
        ──> [ access:  subscription-CLI | API-key+billing | local/hosted-GPU | free-search ]
        ──> spoke
```

- **Subscription-CLI** — runs through an existing consumer plan, *no* per-asset billing.
  `gpt-image-2` (your ChatGPT Plus/Pro via the Codex CLI). Cheapest marginal cost; rate-limited by
  the plan.
- **API-key + billing** — a provider key, billed per image/call. `openai-image-gen` (OpenAI Images
  API, `OPENAI_API_KEY`), and paid image/video APIs in general. Predictable, scalable, **costs money
  per call** — state batch size before running.
- **Local / hosted-GPU** — model runs on a GPU you reach, not a metered text-prompt API.
  `hunyuan3d` (Tencent Hunyuan3D-2.1 via a Hugging Face Gradio endpoint). No per-call billing, but
  subject to the endpoint's availability/queue.
- **CLI-inference / grounded** — `nano-banana-2` (Gemini 3.1 Flash Image via the `infsh` CLI;
  multi-image input up to 14, Google-Search grounding) sits between subscription and API depending
  on how it's keyed.
- **Free-search / processing** — no generation at all: `gifgrep` (search & download), `ffmpeg` /
  `video-frames` (deterministic local transforms), `image-enhancer` (upscale). Zero model cost.

**Rule:** confirm the chosen backend's prerequisite (plan / key / GPU endpoint) is present
**before** generating; never silently swap one access model for another — a failed or mis-billed
call is the failure mode this cluster exists to prevent.

## 2. The pipeline (how spokes compose)

```
GENERATE ──> TRANSFORM ──> ASSEMBLE/DELIVER
 image/3D/video      enhance · restyle · extract      encode · size-fit · gallery
```

Generators emit raw assets; processors refine and package them. A request that needs motion or a
final container almost always ends in `ffmpeg`. Examples:
- Still → upscaled still: `gpt-image-2`/`nano-banana-2`/`openai-image-gen` → `image-enhancer`.
- Photo → 3D: reference image (any image spoke) → `hunyuan3d` → GLB.
- Concept → clip: `ai-video-director` (shots) → `ffmpeg` (encode/resize) ; pull stills with
  `video-frames`.
- Reaction GIF: `gifgrep` (find/extract) **or** `slack-gif-creator` (author) → `ffmpeg` (GIF↔MP4,
  size fit).

## 3. Backend / modality matrix

| Modality | Spoke | Backend | Access model | Output |
|---|---|---|---|---|
| Image (gen) | `gpt-image-2` | GPT Image 2 (ChatGPT Images 2.0) | subscription-CLI (ChatGPT Plus/Pro) | PNG, edits, refs |
| Image (gen) | `nano-banana-2` | Gemini 3.1 Flash Image | `infsh` CLI (multi-image, grounded) | images, multi-input edits |
| Image (gen, batch) | `openai-image-gen` | OpenAI Images API | API key + billing | PNG + `index.html` gallery |
| Image (system) | `art` | mixed (icons, diagrams, mermaid) | provider keys in agent `.env` | headers, icons, diagrams |
| Image (transform) | `image-enhancer` | upscaler | local / no model cost | sharpened/upscaled image |
| 3D | `hunyuan3d` | Hunyuan3D-2.1 | hosted GPU (HF Gradio) | GLB / OBJ / PLY / STL |
| Video (gen) | `ai-video-director` | Kling 3.0 · Sora · Grok | per-tool (key/plan) | shot-by-shot prompts → clips |
| Video (process) | `ffmpeg` | FFmpeg | local CLI | convert/resize/compress/audio |
| Video (extract) | `video-frames` | FFmpeg | local CLI | frames / short clips |
| GIF (find) | `gifgrep` | GIF providers | free search/download | GIFs, stills, sheets |
| GIF (author) | `slack-gif-creator` | composable primitives | local | Slack-size-validated GIF |

## 4. Output & convention notes

- **Formats**: 3D → GLB is the portable default (OBJ/PLY/STL on request). Video masters stay in a
  lossless/high-bitrate container; only down-encode at the delivery step. GIF for Slack must pass
  the size validators in `slack-gif-creator`.
- **Determinism**: `ffmpeg`, `video-frames`, `image-enhancer`, `gifgrep` are reproducible; the
  generative spokes are **not** — same prompt ≠ same output. Capture the prompt/seed when one matters.
- **Reference images** (image-to-image / multi-ref / image-to-3D) are first-class inputs across
  `gpt-image-2`, `nano-banana-2`, and `hunyuan3d` — feed an asset from an earlier stage rather than
  re-describing it.

## 5. Shared guardrails

- **Prerequisite before spend**: verify plan/key/GPU endpoint exists before a generative call.
- **State the cost/quota** of any batch or paid API run up front.
- **Don't swap access models silently** — subscription, API-billing, and local are not equivalent.
- **Respect provider content policy** and the **license/attribution** of downloaded GIFs and
  reference images.
- **Preserve masters**: re-encode lossless-aware; never transcode the source in place.
- Generative output is non-deterministic — record prompt/seed when reproducibility matters.
