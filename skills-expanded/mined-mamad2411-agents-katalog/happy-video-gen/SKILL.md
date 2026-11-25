---
name: happy-video-gen
description: Universal AI video generation supporting OpenAI Sora, Google Veo 2/3, Runway Gen-3/Gen-4, Pika 2.2, Luma Dream Machine (Ray 2), FAL (Kling / Wan / Veo / Sora wrappers), Ark Seedance 1.5 Pro/Lite, Bailian Wanx (i2v), MiniMax Hailuo-02, and Vidu Q3. Use this skill whenever the user asks to generate, create, make, or synthesize a video from a text prompt or from a first-frame image. Covers text-to-video and image-to-video, with optional last-frame control on providers that support it. Typical phrases include "generate a video of ...", "make a 5-second clip of ...", "animate this image", "生成一段视频", "做个短片", or any mention of video-generation model families like Sora, Veo, Runway Gen, Kling, Wan, Seedance, Hailuo, Pika, Dream Machine, Vidu. Always use this skill even if the user does not name a specific model — pick a provider from their EXTEND.md defaults or available API keys. Do NOT use this skill when the user explicitly mentions 即梦 / Dreamina / Jimeng — those go to happy-dreamina instead.
version: 0.1.0
---

# happy-video-gen

Generates short videos (text-to-video or image-to-video) across 10 providers through one CLI: `bun scripts/main.ts ...`. All providers are async — the CLI submits a job, polls until the provider finishes, then downloads the MP4 / WebM.

## Quick usage

```bash
# Text-to-video
bun scripts/main.ts --prompt "camera slowly pushes into a calico cat on grass" --ar 16:9 --duration 5 --video ./out.mp4

# Image-to-video (first frame)
bun scripts/main.ts --prompt "subtle zoom, leaves swaying" --image ./keyframe.png --duration 5 --video ./out.mp4

# Image-to-video with last-frame control (provider-dependent)
bun scripts/main.ts --prompt "seamless morph" --image ./a.png --last-frame ./b.png --video ./out.mp4
```

## When to invoke this skill

- User asks to generate / create / make / synthesize a video from text.
- User asks to animate a still image, or provides a first-frame path.
- User names any video model family (Sora, Veo, Runway, Kling, Wan, Seedance, Hailuo, Pika, Dream Machine, Vidu).

Route to `happy-dreamina` if the user explicitly mentions 即梦 / Jimeng / dreamina CLI. Route to `happy-image-gen` if the user actually wants a still image.

## Step 0: Preflight (BLOCKING)

1. **Locate EXTEND.md** (same resolution order as happy-image-gen):
   - `./.happy-skills/happy-video-gen/EXTEND.md`
   - `$XDG_CONFIG_HOME/happy-skills/happy-video-gen/EXTEND.md`
   - `~/.happy-skills/happy-video-gen/EXTEND.md`

   If none, run `bun scripts/main.ts --setup` and walk the user through `references/config/first-time-setup.md`.

2. **Verify one provider has credentials.** Check env vars in the order the CLI auto-detects (see providers.md). Do not proceed without one usable provider.

3. **Verify Bun**. Fall back to `npx -y bun` if missing.

4. **Warn about cost.** Video generation is 10–100× more expensive per call than images. If the user asks for HD 1080P / 10-second clips, confirm before firing — show them the expected provider cost bracket from `references/providers.md`.

## Step 1: Choose provider

Preference order:

1. `--provider <id>` explicitly passed.
2. EXTEND.md `default_provider`.
3. Auto-detect from env vars: `fal > ark > minimax > runway > luma > pika > vidu > google > bailian > openai`.

Pick by strength of the actual task:

- **Chinese prompts / Chinese text in frame** → `ark` (Seedance) or `bailian` (Wanx).
- **Photorealistic portraits** → `google` (Veo 3) or `runway` (Gen-4).
- **Anime / stylized** → `fal` (Kling) or `luma`.
- **Cheap draft** → `ark` Seedance Lite, `fal` Kling v2.5 turbo, `vidu` Q1.
- **Voice-synced dialogue video** (if applicable) → `google` Veo 3, `openai` Sora 2.

## Step 2: Fill parameters

- **`--prompt`**: always double-quote.
- **`--image <path>`** / **`--last-frame <path>`**: local paths, will be base64-encoded as data URIs automatically. `--last-frame` only accepted by Luma and a few FAL endpoints.
- **`--duration <seconds>`**: 5 is universal default. Caps: Sora-2 / Kling up to 10; Seedance up to 10; Luma up to 9.
- **`--ar <ratio>`**: `16:9 / 9:16 / 1:1 / 4:3 / 3:4`. See `references/aspect_ratio_map.md` for provider-specific quirks.
- **`--resolution`**: `480p / 720p / 1080p`. Not all providers honour it; most cap at 720p on cheap tiers.
- **`--poll-timeout`**: default 600s (10 min). Increase for 1080P or >5s clips.

## Step 3: Submit and wait

```bash
bun scripts/main.ts \
  --prompt "..." \
  --video ./out.mp4 \
  --provider ark \
  --duration 5 \
  --ar 16:9 \
  --resolution 720p
```

While waiting, do **not** fire another job on the same provider — concurrency caps on cheap tiers are strict (often 1). On success the CLI writes the MP4 and reports size + path. JSON output:

```json
{ "success": true, "provider": "ark", "model": "doubao-seedance-1-0-lite-t2v-250408", "video": "/abs/out.mp4", "size_bytes": 4823456, "format": "mp4" }
```

## Step 4: Timeouts and recovery

If polling exceeds `--poll-timeout`, the CLI throws with the provider-specific external id (task id / job id / operation name / request id). Capture it from stderr and resume later with provider-specific tooling. See `references/async-protocol.md` for the per-provider id format and manual resume commands.

## References

- **`references/providers.md`** — all 10 providers with env vars, defaults, cost notes, feature matrix.
- **`references/async-protocol.md`** — external id format per provider + how to resume a stuck task.
- **`references/aspect_ratio_map.md`** — `--ar` mapping per provider.
- **`references/error_codes.md`** — common errors and fixes.
- **`references/config/first-time-setup.md`** — setup walkthrough.
- **`references/config/extend-schema.md`** — EXTEND.md schema.
- **`assets/EXTEND.template.md`** — config template.
