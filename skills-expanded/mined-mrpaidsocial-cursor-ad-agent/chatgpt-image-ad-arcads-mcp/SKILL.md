---
name: chatgpt-image-ad-arcads-mcp
description: >-
  Generate one or more standalone Meta image-ad creatives via ChatGPT Image 2 (gpt-image-2) through the optional Arcads MCP server. Uses arcads_generate_image_gpt and polls with arcads_watch_asset. Locks the model, strips platform chrome, enforces edge-safe layouts and glyph-safety in body text. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. For normal typography-heavy or UI-mimicry requests, use the REST/local chatgpt-image-ad skill.
---

# chatgpt-image-ad (Arcads MCP)

Generate **standalone Meta image-ad creatives** with **gpt-image-2** through the
Arcads **MCP server**. The image files hand off to your `meta-ad-builder` skill —
this skill generates images only.

**This is the MCP-native version** of `chatgpt-image-ad`. It replaces the REST
machinery — no `.env`, no HTTP Basic auth, no `generate_image.py`, no manual
presigned-upload loop, no session-folder REST calls. The Arcads MCP server handles
auth, upload, and generation.

| REST `chatgpt-image-ad` step | MCP replacement |
|---|---|
| `generate_image.py` + curl auth / `.env` | `arcads_generate_image_gpt` (MCP handles auth) |
| `POST /v2/images/generate` `model:"gpt-image-2"` | `arcads_generate_image_gpt(model="gpt-image-2")` |
| `POST /v1/file-upload/get-presigned-url` + PUT (in-script) | `arcads_get_upload_url` + PUT (explicit — see Uploading) |
| `GET /v1/assets/{id}` polling loop | `arcads_watch_asset` (status **and** URL in one call) |
| `--n` → N parallel POSTs | `nbGenerations` (1–10) in a **single** call |
| `PRODUCT_ID` / session folder | nothing — `productId` auto-selects |

## Tools used (Arcads MCP)

| Tool | Role |
|---|---|
| `arcads_generate_image_gpt` | Generate the ad. `model:"gpt-image-2"`, `prompt`, `aspectRatio`, `referenceImages` (≤5), `nbGenerations` (1–10). |
| `arcads_get_upload_url` | Presigned S3 URL for each local reference image. **Required in remote agent clients such as Cursor.** |
| `arcads_watch_asset` | Poll status **and** fetch the signed `downloadUrl`. Primary poll tool. |
| `arcads_list_products` | Resolve `productId` (optional — auto-selects with one product). |

### `arcads_generate_image_gpt` parameters

| Param | Value | Notes |
|---|---|---|
| `prompt` | string (required) | The rewritten ad prompt (Phase 3). |
| `model` | `"gpt-image-2"` | **Locked.** `gpt-image-2` > `gpt-image` for text fidelity. |
| `aspectRatio` | `"1:1"` \| `"16:9"` \| `"9:16"` | **Only these three.** No `4:5`/`2:3` on this backend — render `1:1` and crop. |
| `referenceImages` | array, **max 5** | S3 `filePath`s from upload (not local paths, not asset ids). |
| `nbGenerations` | `1`–`10` | Variants in one call. Default 1; cap 5 for ad batches. |
| `productId` | UUID | Optional — auto-selected if only one product. |

## Read order

1. **This file** — the MCP workflow.
2. **[../../shared/skills/chatgpt-image-ad/prompting/guide.md](../../shared/skills/chatgpt-image-ad/prompting/guide.md)** — what gpt-image-2 is good/bad at, when to switch to nano-banana, retry mode.
3. **[../../shared/skills/image-ad-prompting/prompting/prompt-library.md](../../shared/skills/image-ad-prompting/prompting/prompt-library.md)** — 37 validated templates with per-model notes. **Read before composing.**
4. **[../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md](../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md)** — the 3 always-on guards.

## Hard rules — never relax

1. **Model is `gpt-image-2`.** If the user wants nano-banana, use `nano-banana-image-ad-arcads-mcp`.
2. **No platform/screenshot chrome** in output unless the concept *requires* it (rare). Append the no-chrome guard to every prompt.
3. **Edge-safe + glyph-safety** guards on by default (they fix real failures). Keep all text inside a safe central margin.
4. **Max 5 reference images** (Arcads cap for gpt-image-2). More → `400 Max 5 reference image(s) allowed`.
5. **No Meta upload here.** Hand off image files to `meta-ad-builder`.
6. **Credit cost is an estimate** — present it before generating and wait for confirmation. Arcads exposes no billing endpoint. (This workspace may be on a daily-limit plan where `creditsCharged` is `0` and `usedDailyLimit` is `true` — still confirm, and surface that in the estimate.)
7. **Comparison-table / two-column prompts must specify BOTH columns' values.** If you only give one set, gpt-image-2 duplicates it into both columns (confirmed). State the "others" values AND the "ours" values explicitly.

## Uploading reference files (remote agent clients)

> ⚠️ "Local paths upload automatically" applies only to MCP clients with explicit
> local-filesystem bridging. In Cursor and other remote agent clients, the MCP server cannot read local disk;
> passing a local path returns `File not found … Use arcads_get_upload_url`. Upload first.

Tested, working flow:

1. `arcads_get_upload_url(mimeType)` → `{presignedUrl, filePath}` (`mimeType` = `image/png`, `image/jpeg`, …).
2. HTTP `PUT` the raw bytes:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" -X PUT \
     -H "Content-Type: image/png" --upload-file "<local file>" "<presignedUrl>"
   ```
   Expect `200`. (The presigned URL carries an `x-amz-checksum-crc32` query param; a plain `PUT` still succeeds — no extra header needed.)
3. Pass the returned **`filePath`** (e.g. `external-api-temp-uploads/<uuid>.png`) in `referenceImages`.

**Gotchas (confirmed by testing):**
- **Temp `filePath`s are single-use** — consumed by the first tool call that references them. For N separate generation calls, upload a fresh copy before each. (`nbGenerations` inside one call is a single consumer — one upload is fine.)
- **`referenceImages` wants the S3 `filePath`, not an `arcads_register_image` asset id.**

## Polling & fetching the result

**Poll with `arcads_watch_asset(assetId)`** — it returns `status` (`pending`→`generated`/`failed`) **and**, once generated, the signed `downloadUrl`, in one call. While `pending` there is no `downloadUrl` — wait ~15–20s and call again (gpt-image-2 ≈ 1–3 min).

> ⚠️ On the current MCP build `arcads_get_asset` can return `-32602 (tool not found)` —
> it drops off intermittently. **`arcads_watch_asset` is the reliable poll+fetch tool**
> (it already returns `status`), so prefer it and don't block on `arcads_get_asset`.

**REST fallback** (only if both MCP poll tools are down) — needs `.env` with `ARCADS_BASIC_AUTH`:
```bash
set -a && . ./.env && set +a
curl -s -H "Authorization: $ARCADS_BASIC_AUTH" "${ARCADS_BASE_URL:-https://external-api.arcads.ai}/v1/assets/<assetId>"
```

Download the image with `curl -sS -o <out.png> "<downloadUrl>"`.

## Workflow

### Phase 1 — Gather inputs
Seed prompt; aspect ratio (`1:1`/`16:9`/`9:16`); reference image(s) ≤5 (optional, recommended for a specific product); variant count N (default 1, cap 5).

### Phase 2 — Prompt rewrite
Read the prompt library. If the brief maps to a template, **check the Model notes** — only proceed if `gpt-image-2` is marked clean/preferred; if nano-banana is preferred, suggest `nano-banana-image-ad-arcads-mcp`. Fill `{placeholders}`, append the no-chrome + edge-safe + glyph-safety guards, show the rewritten prompt, and loop on "use / edit / start over" until approved. For fresh prompts (no template), follow guide.md § Phase 3b.

### Phase 3 — Credit estimate (MANDATORY)
Read `logs/arcads-api.jsonl` for past `gpt-image-2` calls (or `MASTER_CONTEXT.md`); present `~credits × N` as an **estimate** and wait for confirmation. Note if the workspace is on a daily limit (`creditsCharged: 0`).

### Phase 4 — Upload references (if any)
Per **Uploading reference files** — fresh upload, collect S3 `filePath`s.

### Phase 5 — Generate
```
arcads_generate_image_gpt(
  prompt = "<rewritten>", model = "gpt-image-2",
  aspectRatio = "<1:1|16:9|9:16>",
  referenceImages = ["external-api-temp-uploads/<uuid>.png"],  # omit if none
  nbGenerations = <N>,
)
```
Append a log entry to `logs/arcads-api.jsonl` (model `gpt-image-2`, aspectRatio, ref count, N, each assetId). Don't log keys.

### Phase 6 — Poll + Visual QA (MANDATORY)
Poll each assetId with `arcads_watch_asset` until `generated`; download. **Read each image** and inspect for: garbled small text (the main gpt-image-2 failure on dense body text); wordmark drift (pass brand wordmarks as references to mitigate); wrong element count (e.g. 4 chat bubbles instead of 3); iOS-dialog/UI proportion drift. If defective, regenerate with a prompt that explicitly corrects the issue (guide.md § Retry mode). Cap 2 retries per variant.

### Phase 7 — Confirm + hand off
Show paths; ask "use all / these / regenerate / cancel." Selected files are ready for `meta-ad-builder`. Save to `outputs/chatgpt-image-ad/<slug>/` and `open` the folder.

## Constraints quick reference

| Constraint | Impact |
|---|---|
| Aspect ratios | `1:1`, `16:9`, `9:16` only. |
| Reference images | Max **5**. S3 `filePath`s only. Single-use. |
| `nbGenerations` | 1–10 in one call. |
| Dense body text | gpt-image-2's main risk — QA every variant; keep text large and inside the safe margin. |
| Two-column comparisons | Specify both columns' values or they duplicate. |

## Error recovery

| Symptom | Fix |
|---|---|
| `400 Max 5 reference image(s)` | Reduce to ≤5. |
| `File not found` on a reference | You passed a local path — upload first (Uploading section). |
| `REFERENCE_FILE_NOT_FOUND` on generate | The `filePath` was already consumed — re-upload fresh right before the call. |
| `-32602 arcads_get_asset not found` | Use `arcads_watch_asset` to poll (it returns status). |
| Garbled small text | Regenerate: enlarge text, fewer words, "all text large and legible," keep inside the safe margin. |
| `422` validation/moderation | Tighten prompt; confirm `aspectRatio` is in the set. |

## Out of scope
- **Nano Banana / Gemini** → `nano-banana-image-ad-arcads-mcp`.
- **Meta upload** → `meta-ad-builder`.
- **Video / carousel / DCO** — image only. Video → `arcads-mcp`.
- **Reverse-engineering an existing ad into a template** → `image-ad-clone-arcads-mcp`.

## See also
- [chatgpt-image-ad](../chatgpt-image-ad/SKILL.md) — the REST/script version.
- [nano-banana-image-ad-arcads-mcp](../nano-banana-image-ad-arcads-mcp/SKILL.md) — sibling for photoreal/lifestyle/multi-ref.
- [image-ad-clone-arcads-mcp](../image-ad-clone-arcads-mcp/SKILL.md) — reverse-engineer an ad into a library template (MCP).
- [arcads-mcp](../arcads-mcp/SKILL.md) — broad Arcads-MCP generation conventions (image + video + audio).
