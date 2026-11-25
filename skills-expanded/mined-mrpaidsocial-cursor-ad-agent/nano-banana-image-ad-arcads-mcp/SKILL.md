---
name: nano-banana-image-ad-arcads-mcp
description: >-
  Generate one or more standalone Meta image-ad creatives via Nano Banana 2 through the optional Arcads MCP server. Uses arcads_generate_image_nano_banana and polls with arcads_watch_asset. Strips platform chrome, enforces edge-safe layouts, and supports up to 14 reference images. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. For normal photoreal, lifestyle, or multi-reference requests, use the REST/local nano-banana-image-ad skill.
---

# nano-banana-image-ad (Arcads MCP)

Generate **standalone Meta image-ad creatives** with the **Nano Banana** family
(default `nano-banana-2`, Gemini Flash Image) through the Arcads **MCP server**.
Image files hand off to your `meta-ad-builder` skill — this skill generates images only.

**This is the MCP-native version** of `nano-banana-image-ad`. No `.env`, no HTTP Basic
auth, no `generate_image.py`, no manual presigned-upload loop, no session-folder calls.

| REST `nano-banana-image-ad` step | MCP replacement |
|---|---|
| `generate_image.py` + curl auth / `.env` | `arcads_generate_image_nano_banana` (MCP handles auth) |
| `POST /v2/images/generate` Nano Banana model | `arcads_generate_image_nano_banana(model=…)` |
| presigned upload + PUT (in-script) | `arcads_get_upload_url` + PUT (explicit — see Uploading) |
| `GET /v1/assets/{id}` polling loop | `arcads_watch_asset` (status **and** URL in one call) |
| `--n` → N parallel POSTs | `nbGenerations` (1–10) in a **single** call |
| `PRODUCT_ID` / session folder | nothing — `productId` auto-selects |

> **MCP model divergence (important):** the MCP tool `arcads_generate_image_nano_banana`
> only accepts **`nano-banana`** and **`nano-banana-2`**. The REST script's
> `nano-banana-pro` and `nano-banana-edit` variants are **not** exposed on this MCP tool.
> Default to **`nano-banana-2`** (up to 14 refs — the standard for ad creatives). For a
> tighter masked inpaint edit there is no MCP enum here; do a full regen with the change
> described in the prompt, or use the REST `nano-banana-image-ad` skill for `nano-banana-edit`.

## Tools used (Arcads MCP)

| Tool | Role |
|---|---|
| `arcads_generate_image_nano_banana` | Generate the ad. `model`, `prompt`, `aspectRatio`, `referenceImages` (≤14), `nbGenerations` (1–10). |
| `arcads_get_upload_url` | Presigned S3 URL for each local reference image. **Required in remote agent clients such as Cursor.** |
| `arcads_watch_asset` | Poll status **and** fetch the signed `downloadUrl`. Primary poll tool. |
| `arcads_list_products` | Resolve `productId` (optional — auto-selects with one product). |

### `arcads_generate_image_nano_banana` parameters

| Param | Value | Notes |
|---|---|---|
| `prompt` | string (required) | The rewritten ad prompt (Phase 3). |
| `model` | `"nano-banana-2"` (default) \| `"nano-banana"` | `nano-banana-2` supports up to 14 refs. |
| `aspectRatio` | `"1:1"` \| `"16:9"` \| `"9:16"` | **Only these three.** No `4:5`/`2:3` — render `1:1`/`9:16` and crop. |
| `referenceImages` | array, **max 14** | S3 `filePath`s from upload (not local paths, not asset ids). Name roles in the prompt. |
| `nbGenerations` | `1`–`10` | Variants in one call. Default 1; cap 5 for ad batches. |
| `productId` | UUID | Optional — auto-selected if only one product. |

## Read order

1. **This file** — the MCP workflow.
2. **[../../shared/skills/nano-banana-image-ad/prompting/guide.md](../../shared/skills/nano-banana-image-ad/prompting/guide.md)** — Nano Banana strengths/limits, named reference roles, lighting/material specifics, retry mode.
3. **[../../shared/skills/image-ad-prompting/prompting/prompt-library.md](../../shared/skills/image-ad-prompting/prompting/prompt-library.md)** — 37 validated templates with per-model notes. **Read before composing.**
4. **[../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md](../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md)** — the 3 always-on guards.

## Hard rules — never relax

1. **Model is Nano Banana** (`nano-banana-2` default). If the user wants gpt-image-2, use `chatgpt-image-ad-arcads-mcp`.
2. **No platform/screenshot chrome** unless the concept requires it.
3. **Edge-safe** layout — keep subjects and any text inside a safe central margin.
4. **Max 14 reference images.** Pass brand wordmarks / product / character / style as named roles in the prompt for best adherence.
5. **No Meta upload here.** Hand off image files to `meta-ad-builder`.
6. **Credit cost is an estimate** — present before generating and wait for confirmation. (Daily-limit workspaces show `creditsCharged: 0`, `usedDailyLimit: true` — still confirm.)

## Uploading reference files (remote agent clients)

> ⚠️ Local paths do **not** work when the MCP server cannot access the client's
> filesystem, including Cursor's remote MCP transport. Passing one returns
> `File not found … Use arcads_get_upload_url`. Upload first.

1. `arcads_get_upload_url(mimeType)` → `{presignedUrl, filePath}`.
2. `curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: image/png" --upload-file "<local>" "<presignedUrl>"` → expect `200`.
3. Pass the returned **`filePath`** in `referenceImages`.

**Gotchas:** temp `filePath`s are **single-use** (upload fresh before each separate generation call; `nbGenerations` within one call is fine). `referenceImages` wants the S3 `filePath`, **not** an `arcads_register_image` asset id.

## Polling & fetching the result

**Poll with `arcads_watch_asset(assetId)`** — returns `status` **and** the signed `downloadUrl` together; while `pending` there is no `downloadUrl` (wait ~15–20s and re-call; nano-banana ≈ 30–60s).

> ⚠️ `arcads_get_asset` can return `-32602 (tool not found)` on the current build —
> use `arcads_watch_asset` (it already returns `status`).

**REST fallback** (only if MCP polling is unavailable):
```bash
set -a && . ./.env && set +a
BASE="${ARCADS_BASE_URL:-https://external-api.arcads.ai}"
curl -sS -H "Authorization: $ARCADS_BASIC_AUTH" "$BASE/v1/assets/<assetId>"
```

Download: `curl -sS -o <out.png> "<downloadUrl>"`.

## Workflow

### Phase 1 — Gather inputs
Seed prompt; aspect ratio; reference image(s) ≤14 (product / character / style — recommended); variant count N (default 1, cap 5); model (`nano-banana-2` default).

### Phase 2 — Prompt rewrite
Read the prompt library. If the brief matches a template, **check the Model notes** — proceed only if `nano-banana` is clean/preferred/strong; if gpt-image-2 is preferred (dense typography), suggest `chatgpt-image-ad-arcads-mcp`. Fill `{placeholders}`, lean on Nano Banana strengths (named reference roles, lighting, materials), append the no-chrome + edge-safe guards, show the prompt, loop until approved. Fresh prompts → guide.md § Phase 3b.

### Phase 3 — Credit estimate (MANDATORY)
Read `logs/arcads-api.jsonl` (or `MASTER_CONTEXT.md`); present `~credits × N` as an estimate and wait for confirmation.

### Phase 4 — Upload references (if any)
Per **Uploading reference files** — fresh upload, collect S3 `filePath`s.

### Phase 5 — Generate
```
arcads_generate_image_nano_banana(
  prompt = "<rewritten>", model = "nano-banana-2",
  aspectRatio = "<1:1|16:9|9:16>",
  referenceImages = ["external-api-temp-uploads/<uuid>.png", ...],  # ≤14; omit if none
  nbGenerations = <N>,
)
```
Append a log entry (model, aspectRatio, ref count, N, each assetId).

### Phase 6 — Poll + Visual QA (MANDATORY)
Poll with `arcads_watch_asset`; download; **Read each image**. Inspect for: extra fingers / wrong limb count (common Gemini-family failure); garbled small text; wordmark drift; character identity drift across variants. If defective, regenerate with a corrected prompt (guide.md § Retry mode). Cap 2 retries per variant.

### Phase 7 — Confirm + hand off
Show paths; "use all / these / regenerate / cancel." Selected files → `meta-ad-builder`. Save to `outputs/nano-banana-image-ad/<slug>/` and `open` the folder.

## Constraints quick reference

| Constraint | Impact |
|---|---|
| Aspect ratios | `1:1`, `16:9`, `9:16` only. |
| Model enum (MCP) | `nano-banana`, `nano-banana-2` only — no `-pro`/`-edit`. |
| Reference images | Max **14**. S3 `filePath`s only. Single-use. |
| `nbGenerations` | 1–10 in one call. |
| Hands / fine text | Gemini-family risk — QA every variant; ask for "exactly five fingers", "legible text". |

## Error recovery

| Symptom | Fix |
|---|---|
| `File not found` on a reference | Local path passed — upload first. |
| `REFERENCE_FILE_NOT_FOUND` on generate | `filePath` consumed — re-upload fresh before the call. |
| `INVALID_REFERENCE_IMAGES` | You passed a register-image asset id — pass the S3 `filePath` instead. |
| `-32602 arcads_get_asset not found` | Poll with `arcads_watch_asset`. |
| Extra fingers / melted object | Regenerate with explicit anatomy/material constraints; don't resend the identical prompt. |
| `422` validation/moderation | Tighten prompt; confirm `aspectRatio` in set. |

## Out of scope
- **ChatGPT Image 2 / gpt-image-2** → `chatgpt-image-ad-arcads-mcp`.
- **Meta upload** → `meta-ad-builder`.
- **Video / carousel / DCO** — image only. Video → `arcads-mcp`.
- **Reverse-engineering an existing ad into a template** → `image-ad-clone-arcads-mcp`.

## See also
- [nano-banana-image-ad](../nano-banana-image-ad/SKILL.md) — the REST/script version.
- [chatgpt-image-ad-arcads-mcp](../chatgpt-image-ad-arcads-mcp/SKILL.md) — sibling for typography-heavy / UI-mimicry.
- [image-ad-clone-arcads-mcp](../image-ad-clone-arcads-mcp/SKILL.md) — reverse-engineer an ad into a library template (MCP).
- [arcads-mcp](../arcads-mcp/SKILL.md) — broad Arcads-MCP generation conventions.
