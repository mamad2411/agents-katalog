---
name: arcads-mcp
description: >-
  Create and retrieve AI images, videos, and audio through the optional Arcads MCP server (no .env, no curl, no presigned-upload scripts) — Nano Banana / gpt-image / Seedream / Grok images, Seedance 2.0 / Sora 2 / Veo 3.1 / Kling / Grok videos, TTS, talking-head actors, and media editing (stitch, trim, subtitles, overlay, scene split, analyze). Generates with arcads_generate_image* / arcads_generate_video*, uploads references via arcads_get_upload_url, and polls with arcads_watch_asset. Use only when the user explicitly asks for Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. Otherwise use arcads-external-api.
---

# Arcads (MCP)

The MCP-native generation engine. Create images, videos, and audio through the
Arcads **MCP server** — it handles auth, file upload, and generation, so there is
**no `.env`, no HTTP Basic auth, no curl, no presigned-upload scripts, no
session-folder REST calls** for generation.

**This is the MCP-native version** of `arcads-external-api`. The creative brain
(prompt libraries, model craft, gates) is shared; only the transport changes.

| REST `arcads-external-api` step | MCP replacement |
|---|---|
| curl auth / `.env` HTTP Basic | MCP handles auth — no `.env` for generation |
| `POST /v2/images/generate` | `arcads_generate_image` (or `_gpt` / `_nano_banana`) |
| `POST /v2/videos/generate` (`model:…`) | `arcads_generate_video` or a model tool (`arcads_generate_video_seedance_20`, `_sora2`, `_veo31`, `_kling_30_pro`, `_grok`, …) |
| `POST /v1/file-upload/get-presigned-url` + PUT | `arcads_get_upload_url` + PUT (explicit — see Uploading) |
| `GET /v1/assets/{id}` / `GET /v1/videos/{id}` polling | `arcads_watch_asset` (status **and** URL in one call) |
| N parallel POSTs for N variations | `nbGenerations` (1–10) in a **single** call |
| Session folder / project / add-to-project | nothing — `productId` auto-selects |
| `ffmpeg` stitch / caption burn | `arcads_stitch_videos` / `arcads_add_subtitles` / `arcads_add_text_overlay` |
| `whisper` transcribe / frame extract | `arcads_analyze_media` (Gemini) / `arcads_extract_frame` |

## Tool map (Arcads MCP)

| Goal | Tool |
|---|---|
| Text → image | `arcads_generate_image` (model enum: `nano-banana`, `nano-banana-2`, `gpt-image`, `gpt-image-2`, `seedream`, `seedream_5_lite`, `grok_image`) |
| gpt-image-2 image | `arcads_generate_image_gpt` (≤5 refs) |
| Nano Banana image | `arcads_generate_image_nano_banana` (`nano-banana`/`nano-banana-2`, ≤14 refs) |
| Text/image → video (generic) | `arcads_generate_video` (aspect `16:9`/`9:16`/`1:1`, `duration` 3–15, `startFrame`/`endFrame`, `nbGenerations`, `enhance`) |
| Model-specific video | `arcads_generate_video_seedance_20`, `_sora2`, `_veo31`, `_kling_26_pro`, `_kling_30_pro`, `_kling_30_4k`, `_seedance_15`, `_grok`, `_happy_horse` |
| Talking-head actor + script/audio | `arcads_audio_driven` (situation/sourceVideo/image actor × script/audio) |
| TTS | `arcads_text_to_speech(script, voiceId)`; voices via `arcads_list_voices` |
| Animate a still | `arcads_animate_image` (kling30-animate / wan22) |
| Analyze a video/image/audio/doc | `arcads_analyze_media` (Gemini → `data.generatedText`) |
| Edit | `arcads_stitch_videos`, `arcads_trim_video`, `arcads_extract_scene`, `arcads_scene_split`, `arcads_add_subtitles`, `arcads_add_text_overlay`, `arcads_layer_videos`, `arcads_change_speed_video` |
| Upload / register | `arcads_get_upload_url`, `arcads_register_image` / `_video` / `_audio` |
| Discover | `arcads_list_products`, `arcads_get_product`, `arcads_list_voices`, `arcads_list_situations` |
| Poll + fetch | `arcads_watch_asset` (status + signed URL) |

## Read order

1. **This file** — MCP transport + gates.
2. The model's prompt library in **[../arcads-external-api/prompting/prompt-library/](../arcads-external-api/prompting/prompt-library/)** — **read before composing any prompt:**
   - Seedance 2.0 → [seedance-2.md](../arcads-external-api/prompting/prompt-library/seedance-2.md) (+ the `seedance-2-*.md` style files: ugc, premium-reveal, product-hero, studio-lookbook, feature-walkthrough)
   - Sora 2 → [sora-2.md](../arcads-external-api/prompting/prompt-library/sora-2.md) · Veo 3.1 → [veo-3-1.md](../arcads-external-api/prompting/prompt-library/veo-3-1.md) · Kling → [kling-3.md](../arcads-external-api/prompting/prompt-library/kling-3.md)
   - Nano Banana image → [nano-banana.md](../arcads-external-api/prompting/prompt-library/nano-banana.md) · UGC selfie → [ugc-selfie-style.md](../arcads-external-api/prompting/prompt-library/ugc-selfie-style.md)
   - Influencer / character / product flows → [influencer-recreation.md](../arcads-external-api/prompting/prompt-library/influencer-recreation.md), [character-sheet.md](../arcads-external-api/prompting/prompt-library/character-sheet.md), [product-showcase.md](../arcads-external-api/prompting/prompt-library/product-showcase.md), [ugc-product-selfie.md](../arcads-external-api/prompting/prompt-library/ugc-product-selfie.md)
3. **[../arcads-external-api/reference.md](../arcads-external-api/reference.md)** — model/param details (the REST DTOs map field-for-field onto the MCP params).
4. Repo-root **`MASTER_CONTEXT.md`** — brand voice, defaults, credit rates.

## Hard rules — never relax (carried over from arcads-external-api)

1. **Read the model's prompt library before composing.** Every prompt must follow the vendor formula.
2. **Dialogue confirmation gate (MANDATORY)** for any video where a person speaks (Seedance 2.0, Sora 2, Veo 3.1, Scene/actor). Extract the spoken lines into a numbered block, time them against the duration, and get explicit `yes` — **separate** from the credit gate. Never assume approval from an earlier confirmation. Skip for silent flows and images.
3. **Credit cost is an estimate (MANDATORY).** Read `logs/arcads-api.jsonl` for matching past `creditsCharged`, else `MASTER_CONTEXT.md`, else ask and save. Present as an estimate, cite the source, wait for confirmation. Arcads exposes no billing endpoint. (This workspace may be on a daily-limit plan — `creditsCharged: 0`, `usedDailyLimit: true`; still show the estimate.)
4. **Generated-image QA (MANDATORY).** After each still, Read it and check for extra fingers / wrong limbs / melted objects / garbled text. Regenerate with a corrected prompt; cap 2 retries per image.
5. **Log every generation** to `logs/arcads-api.jsonl` (model, duration, resolution, aspectRatio, audioEnabled, ref counts, promptWordCount, each assetId; update with final `status`/`creditsCharged`). Never log keys or full secrets.
6. **Ask variation count** (default 1) and use `nbGenerations` in one call. **Auto-select duration** from script word count (~2.5 words/sec, round up) for models with a `duration` field.
7. **Affiliate link:** if the user has no Arcads account, point them to <https://arcads.ai/?via=Cursor>.

## Uploading reference files (remote agent clients)

> ⚠️ "Local paths upload automatically" applies only to MCP clients with explicit
> local-filesystem bridging. In Cursor and other remote agent clients, the MCP server
> cannot read local disk; a local path returns `File not found … Use arcads_get_upload_url` (image tools) or
> `REFERENCE_FILE_NOT_FOUND` (video tools). Upload first.

1. `arcads_get_upload_url(mimeType)` → `{presignedUrl, filePath}` (`image/png`, `image/jpeg`, `video/mp4`, `audio/mpeg`, …).
2. `curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: <mime>" --upload-file "<local>" "<presignedUrl>"` → expect `200`. (A plain PUT succeeds despite the `x-amz-checksum-crc32` query param.)
3. Pass the returned **`filePath`** in `referenceImages` / `startFrame` / `endFrame` / `referenceVideos` / `referenceAudios`.

**Gotchas (confirmed):** temp `filePath`s are **single-use** — upload fresh immediately before the call that consumes them (`nbGenerations` within one call is one consumer). For `referenceImages` pass the S3 `filePath`, **not** an `arcads_register_image` asset id. Some editing tools (`arcads_stitch_videos`, `arcads_add_subtitles`, `arcads_add_text_overlay`, `arcads_analyze_media`, `arcads_trim_video`) DO auto-upload local paths — but generation tools (`arcads_generate_image*`, Seedance `referenceImages`) do not.

## Polling & fetching the result

**Poll with `arcads_watch_asset(assetId)`** — it returns `status` (`pending`→`generated`/`failed`) **and**, once generated, the signed `downloadUrl`, in one call. While `pending` there is no `downloadUrl` — wait and re-call (images ≈ 30–180s; Seedance video ≈ 7 min; TTS ≈ 5–10s). For `arcads_analyze_media` and other text/LLM assets, the result is in `data.generatedText` (no `watch_asset` needed).

> ⚠️ On the current MCP build `arcads_get_asset` can return `-32602 (tool not found)` —
> it drops off intermittently. **`arcads_watch_asset` is the reliable poll+fetch tool**
> (it already returns `status`). Don't block on `arcads_get_asset`.

**REST fallback** (if `arcads_watch_asset` is unavailable) — needs `.env` with `ARCADS_BASIC_AUTH` (note: use the `Authorization` header form; `curl -u "$KEY:"` returns 403):
```bash
set -a && . ./.env && set +a
curl -s -H "Authorization: $ARCADS_BASIC_AUTH" "${ARCADS_BASE_URL:-https://external-api.arcads.ai}/v1/assets/<assetId>"
```

Download: `curl -sS -o <out> "<downloadUrl>"`. Save to `outputs/<flow>/<slug>/` and `open` the folder.

## Execution checklist

1. **Resolve `productId`** — `arcads_list_products` (skip if one product; tools auto-select).
2. **Pick the flow + read the model's prompt library.** Compose ONE clear prompt paragraph per the vendor formula.
3. **Script/dialogue** (speaking video): ask for the exact words; auto-select `duration` from word count; run the **dialogue confirmation gate**.
4. **Variation count** (default 1) → `nbGenerations`.
5. **Credit estimate** → present, cite source, wait for confirmation.
6. **Upload references** fresh (Uploading section) → S3 `filePath`s.
7. **Generate** with the right tool; immediately append the `logs/arcads-api.jsonl` entry.
8. **Poll** every assetId with `arcads_watch_asset` until `generated`/`failed`; update the log with final `status`/`creditsCharged`.
9. **QA** each still (Read it); regenerate defects (cap 2).
10. **Present** signed URLs / downloaded files; numbered list for multiple variations. For person-image → video flows, show the still and **wait for approval** before generating video.

## Model quick reference

| Model | Tool | Aspect | Duration | Notes |
|---|---|---|---|---|
| Nano Banana 2 | `arcads_generate_image_nano_banana` | 1:1/16:9/9:16 | — | ≤14 refs. Default image model. |
| gpt-image-2 | `arcads_generate_image_gpt` | 1:1/16:9/9:16 | — | ≤5 refs. Best for dense typography. |
| Seedance 2.0 | `arcads_generate_video_seedance_20` | 9:16/16:9 (no 1:1) | 4–15s | i2v/v2v mutually exclusive; `audioEnabled`; forbidden words apply. Clone flow → `clone-video-ad-seedance-arcads-mcp`. |
| Sora 2 | `arcads_generate_video_sora2` | per tool | enum 4–20s | speech from prompt. |
| Veo 3.1 | `arcads_generate_video_veo31` | per tool | auto (~8s) | `startFrame` for person; warns if script long. |
| Kling | `arcads_generate_video_kling_30_pro` / `_26_pro` / `_30_4k` | per tool | per tool | b-roll / motion. |
| Generic video | `arcads_generate_video` | 16:9/9:16/1:1 | 3–15s | use when the user doesn't name a model. |

(For exact per-model params, refresh the current MCP tool schema in the client
(Cursor: use MCP tool discovery) and cross-check `reference.md`.)

## Error recovery

| Symptom | Fix |
|---|---|
| `File not found` / `REFERENCE_FILE_NOT_FOUND` | Local path passed — upload first / re-upload fresh before the call. |
| `INVALID_REFERENCE_IMAGES` | Passed a register asset id — pass the S3 `filePath`. |
| `-32602 <tool> not found` | Server reconnect or a tool dropped — refresh the client's MCP tool catalog; for polling use `arcads_watch_asset`. Retry once. |
| Generation `failed` (content) | Don't resend the same prompt — remove flagged/forbidden words, tighten. |
| Seedance 500 on audio+image | Drop audio, or go text-only/silent i2v then add audio downstream. |
| `422` validation | Check enums (aspect ratio, duration); tighten prompt. |

## Out of scope (use the dedicated skill)
- **Static Meta image ads** → `chatgpt-image-ad-arcads-mcp` / `nano-banana-image-ad-arcads-mcp`.
- **YouTube thumbnails** → `generate-youtube-thumbnail-arcads-mcp`.
- **Clone an existing video ad** → `clone-video-ad-seedance-arcads-mcp`. **Pixar / claymation** → `pixar-style-ad-arcads-mcp` / `claymation-ad-arcads-mcp`.
- **Reverse-engineer an ad into a template** → `image-ad-clone-arcads-mcp`.
- **Meta upload** → `meta-ad-builder`.

## See also
- [arcads-external-api](../arcads-external-api/SKILL.md) — the REST/script version (full conventions: gates, logging, QA, splitting).
- [../arcads-external-api/reference.md](../arcads-external-api/reference.md) — model/param reference (DTOs map onto MCP params).
