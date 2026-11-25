---
name: generate-youtube-thumbnail-arcads-mcp
description: >-
  Generate high-CTR YouTube thumbnails using Nano Banana 2 through the optional Arcads MCP server. Uses arcads_generate_image_nano_banana at 16:9, uploads references via arcads_get_upload_url, and polls with arcads_watch_asset. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. For normal thumbnail requests, use the REST/local generate-youtube-thumbnail skill.
---

# Generate YouTube Thumbnail (Arcads MCP)

Create high-CTR YouTube thumbnails with **Nano Banana 2** at **16:9** through the
Arcads **MCP server**, with proper character likeness and proven CTR formulas.

**This is the MCP-native version** of `generate-youtube-thumbnail`. No `.env`, no
HTTP Basic auth, no `generate-batch.sh`, no manual presigned-upload pipeline.

| REST `generate-youtube-thumbnail` step | MCP replacement |
|---|---|
| `generate-batch.sh` + curl auth / `.env` | `arcads_generate_image_nano_banana` (MCP handles auth) |
| `POST /v2/images/generate` `nano-banana-2` | `arcads_generate_image_nano_banana(model="nano-banana-2")` |
| presigned upload + S3 PUT (in-script) | `arcads_get_upload_url` + PUT (explicit — see Uploading) |
| `GET /v1/assets/{id}` polling loop | `arcads_watch_asset` (status **and** URL in one call) |
| N parallel POSTs for N concepts | `nbGenerations` (1–10) in a **single** call |
| `productId` from MASTER_CONTEXT | auto-selects (one product) |

## Tools used (Arcads MCP)

| Tool | Role |
|---|---|
| `arcads_generate_image_nano_banana` | Generate thumbnails. `model:"nano-banana-2"`, `aspectRatio:"16:9"`, `referenceImages` (face/brand/product), `nbGenerations`. |
| `arcads_get_upload_url` | Presigned S3 URL per local reference (face photos, logo, product). **Required in remote agent clients such as Cursor.** |
| `arcads_watch_asset` | Poll status **and** fetch the signed `downloadUrl`. Primary poll tool. |
| `arcads_list_products` | Resolve `productId` (optional — auto-selects). |

### Key parameters

| Param | Value | Notes |
|---|---|---|
| `model` | `"nano-banana-2"` | Up to 14 reference images — pass several face angles for likeness. |
| `aspectRatio` | `"16:9"` | **Always 16:9** for YouTube (renders 2752×1536). |
| `referenceImages` | array, ≤14 | Face headshot + 3/4 angles + expressions; brand/logo; product. S3 `filePath`s. |
| `nbGenerations` | `1`–`10` | A/B variations in one call. |

## Read order

1. **This file** — the MCP workflow, batch generation.
2. **[../../shared/skills/generate-youtube-thumbnail/prompting/guide.md](../../shared/skills/generate-youtube-thumbnail/prompting/guide.md)** — likeness alignment, expressions cheat sheet, prompt structure.
3. **[../../shared/skills/generate-youtube-thumbnail/prompting/formulas.md](../../shared/skills/generate-youtube-thumbnail/prompting/formulas.md)** — 5 proven CTR formulas with templates. **Read before composing.**

## Hard rules — never relax

1. **Model is `nano-banana-2`, aspect ratio `16:9`.**
2. **References must be uploaded, not pasted.** Chat-pasted images are not accessible — the user must provide files on disk; you upload them (Uploading section). Without face refs, likeness will not match.
3. **Big, legible, edge-safe text.** Keep face and text inside a safe margin (YouTube overlays a duration stamp bottom-right and progress bar bottom edge — keep critical content away from edges).
4. **One clear focal subject + one big idea.** High contrast, saturated, strong rim light. Follow a formula from formulas.md.
5. **Credit cost is an estimate** — present before generating; wait for confirmation. (Daily-limit workspaces show `creditsCharged: 0`.)

## Uploading reference files (remote agent clients)

> ⚠️ Local paths fail when the MCP server cannot access the client's filesystem,
> including Cursor's remote MCP transport: `File not found … Use arcads_get_upload_url`.

1. For each face/brand/product file: `arcads_get_upload_url(mimeType)` → `{presignedUrl, filePath}`.
2. `curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: image/jpeg" --upload-file "<local>" "<presignedUrl>"` → expect `200`.
3. Pass all returned **`filePath`**s in `referenceImages` (≤14).

**Gotcha:** temp `filePath`s are **single-use**. If you fire several separate generation calls (e.g. different concepts), re-upload the face set fresh before each call. A single call with `nbGenerations` reuses one upload set fine.

## Polling & fetching the result

**Poll with `arcads_watch_asset(assetId)`** — returns `status` and, once generated, the signed `downloadUrl`. While `pending` no `downloadUrl` (re-call every ~15s; nano-banana ≈ 30–60s).

> ⚠️ `arcads_get_asset` can return `-32602 (tool not found)` on the current build — rely on `arcads_watch_asset`.

Download each thumbnail: `curl -sS -o <n>_thumbnail.png "<downloadUrl>"`.

## Workflow

### Phase 1 — Gather inputs
Video topic / title; the hook idea; face photos (5+ recommended: headshot, 3/4 angles, close-up, expressions); brand/logo and product files (optional); how many concepts/variations (default 3–5); the CTR formula (or pick from formulas.md).

### Phase 2 — Upload references
Upload all face/brand/product files (Uploading section); collect S3 `filePath`s.

### Phase 3 — Compose prompts
Read formulas.md; pick a formula; for each concept write a prompt: subject + expression + big text + composition + lighting/contrast. Name the reference roles ("the man from the reference photos"). Keep face on one third, text on the other; legible, edge-safe. Show prompts; loop until approved.

### Phase 4 — Credit estimate (MANDATORY)
Present `~credits × variations` as an estimate; wait for confirmation.

### Phase 5 — Generate
```
arcads_generate_image_nano_banana(
  prompt = "<concept prompt>", model = "nano-banana-2", aspectRatio = "16:9",
  referenceImages = ["external-api-temp-uploads/<face1>.jpg", "...<face2>.jpg", "...<logo>.png"],
  nbGenerations = <N>,   # variations of this concept
)
```
For multiple distinct concepts, re-upload the face set fresh before each concept's call. Log each call to `logs/arcads-api.jsonl` (model, aspectRatio 16:9, ref count, N, assetIds).

### Phase 6 — Poll + Visual QA (MANDATORY)
Poll with `arcads_watch_asset`; download. **Read each thumbnail**: likeness match to the reference face; readable text at small size (thumbnails shrink — text must survive); no extra fingers; face/eyes not distorted; key content not under where YouTube overlays the timestamp. Regenerate defects (cap 2 retries each).

### Phase 7 — Present
Save to `outputs/yt-thumbnails/<slug>-<date>/` as `1_thumbnail.png` … and `open` the folder. Present as a numbered set for A/B comparison; note which formula each used.

## Constraints quick reference

| Constraint | Impact |
|---|---|
| Aspect ratio | `16:9` always (2752×1536). |
| References | ≤14 S3 `filePath`s; single-use; upload-first. |
| `nbGenerations` | 1–10 in one call. |
| Small-size legibility | Text must read at ~210px wide — keep it big and bold. |

## Error recovery

| Symptom | Fix |
|---|---|
| Likeness is off | Add more/clearer face angles as references; name the role explicitly in the prompt. |
| `File not found` on a reference | Local path passed — upload first. |
| `REFERENCE_FILE_NOT_FOUND` | `filePath` consumed — re-upload before the call. |
| `-32602 arcads_get_asset not found` | Poll with `arcads_watch_asset`. |
| Text unreadable when small | Fewer words, larger weight, higher contrast, regenerate. |

## Out of scope
- **Static Meta ad creatives** → `nano-banana-image-ad-arcads-mcp` / `chatgpt-image-ad-arcads-mcp`.
- **Animated / video thumbnails** → `arcads-mcp` (video).
- **Uploading to YouTube** — this skill outputs image files only.

## See also
- [generate-youtube-thumbnail](../generate-youtube-thumbnail/SKILL.md) — the REST/script version.
- [../../shared/skills/generate-youtube-thumbnail/prompting/formulas.md](../../shared/skills/generate-youtube-thumbnail/prompting/formulas.md) — the 5 CTR formulas.
- [arcads-mcp](../arcads-mcp/SKILL.md) — broad Arcads-MCP generation conventions.
