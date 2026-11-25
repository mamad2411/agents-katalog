---
name: clone-video-ad-seedance-arcads-mcp
description: >-
  Clone an existing video ad onto a new product using Seedance 2.0 through the optional Arcads MCP server. Analyzes the source with arcads_analyze_media, adapts its structure, generates via arcads_generate_video_seedance_20, and polls with arcads_watch_asset. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. Otherwise use the arcads-external-api clone-ad sub-skill.
---

# Clone Video Ad — Seedance 2.0 (Arcads MCP)

Clone an existing video ad onto a different product. The agent analyzes the source
ad with the Arcads MCP's `arcads_analyze_media` tool (Gemini watches the whole
video — dialogue, beats, camera, tone), adapts the structure for the user's
product, and generates a new **Seedance 2.0** video via `arcads_generate_video_seedance_20`.

**This is the MCP-native version.** It replaces the REST `clone-ad` sub-skill's
machinery — no `.env`, no HTTP Basic auth, no presigned-upload plumbing, no
`ffmpeg` frame extraction, no local `whisper` transcription, no session-folder
REST calls. The Arcads MCP server handles auth, file upload, and analysis.

| REST `clone-ad` step | MCP replacement |
|---|---|
| `ffmpeg` extract-frames + read frames + `whisper` transcribe | **one** `arcads_analyze_media` call (Gemini) |
| Hand-rolled curl auth / `.env` HTTP Basic | MCP handles auth — no `.env` needed for generation |
| `POST /v2/videos/generate` (model `seedance-2.0`) | `arcads_generate_video_seedance_20` |
| `GET /v1/assets/{id}` polling loop | `arcads_watch_asset` (status + download URL), with a REST fallback (see Polling) |
| N parallel POSTs for N variations | `nbGenerations` (1–10) in a single call |
| Session folder / project / add-to-project | nothing — `productId` auto-selects |

> ⚠️ **Reference files need an explicit upload in remote agent clients.** Automatic
> local-path upload only works in MCP clients with explicit filesystem bridging.
> In Cursor the MCP server cannot read local disk; passing a local
> path returns `400 REFERENCE_FILE_NOT_FOUND`. You must upload via
> `arcads_get_upload_url` + an HTTP `PUT`, then pass the returned S3 `filePath`. See
> **[Uploading reference files](#uploading-reference-files-remote-agent-clients)** below.

## Tools used (Arcads MCP)

| Tool | Role |
|---|---|
| `arcads_list_products` | Resolve `productId` (skip if you already have it; the generate tools auto-select when there's only one product). |
| `arcads_get_upload_url` | Get a presigned S3 URL for each local reference file (source video, product image). **Required in remote agent clients such as Cursor** — see Uploading below. |
| `arcads_analyze_media` | Watch + transcribe the source ad. `referenceVideos: ["<s3 filePath>"]`. Returns the blueprint in `data.generatedText`. |
| `arcads_generate_video_seedance_20` | Generate the clone. Key params below. |
| `arcads_watch_asset` | Poll status and get the signed download URL once generated. Primary polling tool; REST fallback below. |

### `arcads_generate_video_seedance_20` parameters

| Param | Value | Notes |
|---|---|---|
| `prompt` | string (required) | The adapted Seedance prompt. 100–260 words. |
| `aspectRatio` | `"9:16"` or `"16:9"` | **No `1:1`.** Match the source ad. Default `9:16` for UGC/social. |
| `duration` | `4`–`15` (int) | Match source (≤15s) or split. Default 15 for no-dialogue. |
| `resolution` | `"480p"` \| `"720p"` \| `"1080p"` | Default `720p`. `480p` for cheap test runs. |
| `audioEnabled` | boolean | `true` when the source has speech (confirm with user). |
| `referenceImages` | array, max 3 | i2v: pass the product image. `@(img1)` = index 0. |
| `referenceVideos` | array, max **1 effective** | v2v: pass a product-only / hands-only clip. **Mutually exclusive with `referenceImages`.** |
| `referenceAudios` | array, max 3 | Optional voice clone. |
| `nbGenerations` | `1`–`10` | Variations in one call. |
| `productId` | UUID | Optional — auto-selected if only one product. |

## Read order

1. **This file** — the MCP workflow.
2. **[../arcads-external-api/prompting/prompt-library/seedance-2.md](../arcads-external-api/prompting/prompt-library/seedance-2.md)** — Seedance 2.0 platform rules (prompt structure, motion, timestamps, forbidden words). **Read before composing any prompt.**
3. The closest style template for the source ad's vibe:
   - UGC selfie / testimonial → [seedance-2-ugc.md](../arcads-external-api/prompting/prompt-library/seedance-2-ugc.md)
   - Dark-void premium reveal (no person) → [seedance-2-premium-reveal.md](../arcads-external-api/prompting/prompt-library/seedance-2-premium-reveal.md)
   - Elemental product hero (no person) → [seedance-2-product-hero.md](../arcads-external-api/prompting/prompt-library/seedance-2-product-hero.md)
   - Polished voiceover lookbook → [seedance-2-studio-lookbook.md](../arcads-external-api/prompting/prompt-library/seedance-2-studio-lookbook.md)
   - Fast feature demo → [seedance-2-feature-walkthrough.md](../arcads-external-api/prompting/prompt-library/seedance-2-feature-walkthrough.md)

## Hard rules — never relax

1. **Model is Seedance 2.0.** Use `arcads_generate_video_seedance_20`. If the user wants Veo/Sora/Kling, redirect to the `arcads-external-api` skill.
2. **Analyze before adapting.** Never write the clone prompt from a thumbnail or the user's description of the ad — always run `arcads_analyze_media` on the real source video first.
3. **Dialogue confirmation gate (Phase 5) is mandatory** for any clone with speech, and is **separate** from the credit-cost gate. Never assume approval from an earlier confirmation.
4. **Credit cost is an estimate** (Phase 6). Arcads exposes no billing endpoint — always label totals as estimates and tell the user to confirm exact pricing in the Arcads platform. Do not generate until the user confirms.
5. **No `1:1`** aspect ratio on Seedance. **No forbidden words** in the prompt: `cinematic`, `professional`, `stunning`, `8k`, `studio`, `perfect`.
6. **`referenceImages` and `referenceVideos` are mutually exclusive** in a single call. Pick i2v **or** v2v, never both.
7. **Log every generation** to `logs/arcads-api.jsonl` (model, duration, resolution, aspectRatio, audioEnabled, ref counts, assetId). Never log prompts-in-full secrets or keys.

## Uploading reference files (remote agent clients)

Any local file you feed the MCP — the **source video** (for `arcads_analyze_media`)
and the **product image** (for `referenceImages`) — must be uploaded first. Tested,
working flow:

1. `arcads_get_upload_url(mimeType)` → returns `{presignedUrl, filePath}`
   (`mimeType` = `video/mp4`, `image/jpeg`, `image/png`, …).
2. HTTP `PUT` the raw bytes to `presignedUrl` with the matching `Content-Type`:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" -X PUT \
     -H "Content-Type: image/jpeg" --upload-file "<local file>" "<presignedUrl>"
   ```
   Expect `200`. (The presigned URL carries a `x-amz-checksum-crc32` query param;
   a plain `PUT` still succeeds — no extra checksum header needed.)
3. Pass the returned **`filePath`** (e.g. `external-api-temp-uploads/<uuid>.jpg`) in
   `referenceVideos` / `referenceImages`.

**Gotchas confirmed by testing — these will bite if ignored:**

- **Temp `filePath`s are single-use.** Each upload is consumed by the **first** tool
  call that references it. If you upload an image, use it in `arcads_analyze_media`,
  then reuse the same `filePath` in `arcads_generate_video_seedance_20`, the second
  call fails with `REFERENCE_FILE_NOT_FOUND`. **Upload a fresh copy immediately before
  the generation call**, with no other call consuming it in between. (`nbGenerations`
  inside one call is fine — that's a single consumer.)
- **`referenceImages` wants the S3 `filePath`, not a registered asset id.** Passing an
  `arcads_register_image` asset id returns `INVALID_REFERENCE_IMAGES`. Registration is
  only useful for persistent assets referenced by other registration-aware fields; for
  Seedance `referenceImages`/`referenceVideos`, pass the fresh temp `filePath`.
- For **multi-clip v2v chaining**, download clip N's mp4, then upload it fresh and pass
  its temp `filePath` as `referenceVideos` for clip N+1.

## Polling & fetching the result

Primary path: call `arcads_watch_asset(assetId)` until it returns
`status: generated` or `status: failed`; on success it also returns the download URL.

**REST fallback** (use when `arcads_watch_asset` is unavailable). Requires `.env`
with `ARCADS_BASIC_AUTH`:

```bash
set -a && . ./.env && set +a
BASE="${ARCADS_BASE_URL:-https://external-api.arcads.ai}"
# IMPORTANT: use the Authorization header form. `curl -u "$ARCADS_API_KEY:"` returns 403.
curl -s -H "Authorization: $ARCADS_BASIC_AUTH" "$BASE/v1/assets/<assetId>"
```

Response fields (confirmed by testing):
- `status` — `pending` → `generated` / `failed`.
- **`arcads_analyze_media`** (type `llm`): blueprint text is in **`data.generatedText`**.
- **Seedance video** (type `seedance_20`): the playable file is at the **top level** —
  **`url`** (HD mp4), `sdUrl` (SD mp4), `thumbnailUrl` (poster). **Not** under `data`.
  The bill is in `data.creditsCharged`; clip length in `data.duration`.
- The endpoint occasionally returns an empty/non-JSON body — **retry** rather than
  treating it as failed. Poll on a relaxed cadence (Seedance ~7–15 min; analyze ~1 min).

## Workflow

### Phase 0 — Gather inputs

| Input | Required | Notes |
|---|---|---|
| **Source video ad** | yes | Local path (`.mp4/.mov/.webm`) or a public URL. This is what gets cloned. |
| **Product image** | recommended | The user's product. Becomes `referenceImages` / `@(img1)`. Without it, Seedance invents a product. |
| **Product / offer description** | if no image | Name, features, audience, key claims — used to rewrite dialogue. |
| **Brand voice** | optional | Check `MASTER_CONTEXT.md`; if empty, ask for tone/audience. |

If the user gives only a video and "clone this for my product," ask for a product
image **or** a text description before continuing.

### Phase 1 — Analyze the source ad (one MCP call)

First **upload the source video** (see [Uploading reference files](#uploading-reference-files-remote-agent-clients)) → get its S3 `filePath`. Then call `arcads_analyze_media`:

- `referenceVideos: ["<s3 filePath from upload>"]`
- `prompt`: ask Gemini to return a beat-by-beat blueprint. Use this template:

  > "You are reverse-engineering a video ad so it can be recreated for a different
  > product. Analyze this video and return: (1) total duration in seconds and aspect
  > ratio (9:16 or 16:9); (2) a beat map — for each beat: timestamp range, label
  > (HOOK / SHOW / DEMO / VERDICT / CTA etc.), what's on screen, camera framing &
  > movement, and whether anyone speaks; (3) the FULL spoken transcript, verbatim,
  > with per-beat line breaks (or 'SILENT' if no speech); (4) speaker tone, energy
  > arc, and relationship to viewer; (5) lighting & capture style (phone/handheld,
  > tripod, studio); (6) how the product is physically shown and what claims/features
  > are called out; (7) the 2–3 defining traits that make this ad recognizable and
  > MUST transfer to a clone. Be precise and concise."

The result text is your internal blueprint. (If the source is **silent**, note it —
you'll skip the dialogue gate.)

> Polling: `arcads_analyze_media` returns an asset id. Poll until `status: generated`,
> then read `data.generatedText` (see [Polling & fetching](#polling--fetching-the-result)).
> Do not rely on an inline widget; poll explicitly in Cursor.
> Typical time ~1 minute.

### Phase 2 — Present the analysis & confirm

Show the user a tight summary and the swap plan, then wait for confirmation:

```
📋 Source ad analysis
Duration: Xs · Aspect: 9:16 · Beats: N · Dialogue: Y words · Style: [name]

Beat map:
  [00:00–00:03] HOOK — close-up, excited, "opening line"
  [00:03–00:07] SHOW — tilts product to lens, "feature call-out"
  [00:07–00:10] DEMO — (silent) uses product, macro on texture
  [00:10–00:15] VERDICT — back to camera, "closing line + CTA"

Defining traits: 1) … 2) … 3) …

Transfers:  ✅ structure, pacing, camera, edit style, tone, energy, dialogue pattern
Swaps:      🔄 product → yours · claims → your features · brand → yours

Proceed with adaptation? (yes / adjust)
```

### Phase 3 — Decide generation mode

```
Source ≤ 15s?
  YES → single clip
  NO  → multi-clip: split at natural beat boundaries, each ≤ 15s (see Multi-clip below)

Product IMAGE provided?
  YES → i2v: referenceImages:[product], keep @(img1) in prompt
  NO  → text-only (describe product in prompt) — OR v2v only if the source is
        product-only / hands-only with NO human faces (v2v + faces → content-checker
        rejection, still billed)

Source has someone SPEAKING?
  YES → audioEnabled: true (confirm) → Phase 5 dialogue gate REQUIRED
  NO  → audioEnabled: false (or ask) → skip dialogue gate
```

Tell the user which mode you're using and why.

### Phase 4 — Adapt for the user's product

Read [seedance-2.md](../arcads-external-api/prompting/prompt-library/seedance-2.md) first, then the closest style template.

**Dialogue (if source has speech):** keep the same conversational pattern, the same
number of spoken lines, the same silent-beat placement, the same energy arc. Swap
product references for the user's product; match each line's word count (±3) to
preserve pacing.

**Visual:** keep camera work, framing per beat, edit style, setting, lighting, and
technical-flaw cues. Swap only the product (appearance, colors, materials, label).

**Prompt composition (Seedance rules):**
- Order: **Subject + Action + Camera + Style + Constraints**.
- 100–260 words. One primary action per shot; use degree adverbs (slowly, casually).
- Timestamps `[00:00]`, `[00:04]`… for multi-beat pacing.
- If product image provided: include `@(img1)` and add "The product from @(img1)
  must remain visually unchanged in every shot."
- At least one style anchor (`documentary`, `photorealistic`, `handheld`).
- **No forbidden words.**

### Phase 5 — Dialogue confirmation gate (MANDATORY if speech)

```
📝 Dialogue script (confirm before I generate)
  1. [HOOK]    "adapted line matching original pattern"
  2. [SHOW]    "adapted feature call-out for your product"
  3. [DEMO]    (silent beat — physical demonstration)
  4. [VERDICT] "adapted closing line / CTA"

Total spoken words: ~N · Target: Xs · Fits at natural pace: ✅/❌
Approve this dialogue? (yes / edit / rewrite)
```

Separate from the credit gate. Loop on "edit" until approved. Skip only if silent.

### Phase 6 — Credit-cost estimate (MANDATORY)

1. Read `logs/arcads-api.jsonl` for past Seedance entries with similar config →
   cite the recorded `creditsCharged`.
2. Else fall back to `MASTER_CONTEXT.md` rate table; else ask the user and save it.
3. Present with the estimate-only disclosure and **wait for confirmation**:

```
Estimated credit cost:
  Seedance 2.0 (15s, 720p, i2v) × 1 var = ~0.9 credits  (logs 2026-04-09)
  ─────────────────────────────────────
  Estimated total: ~0.9 credits
  ⚠️ Estimate only — confirm exact cost in the Arcads platform.  Proceed? (yes/no)
```

QA-fix regenerations after the initial confirmation don't need re-confirmation, but
note the extra credits in the summary.

### Phase 7 — Generate

Single clip — **upload the product image fresh right before this call** (Uploading
section), then pass its S3 `filePath`:

```
arcads_generate_video_seedance_20(
  prompt        = "<adapted prompt>",
  aspectRatio   = "9:16",            # match source
  duration      = 15,                # from Phase 4
  resolution    = "720p",
  audioEnabled  = true,              # from Phase 3/5 — confirmed OK alongside referenceImages
  referenceImages = ["external-api-temp-uploads/<uuid>.jpg"],  # i2v: fresh S3 filePath; OMIT for text-only/v2v
  nbGenerations = <N>,               # variations in one call
)
```

Right after the call succeeds, append a log entry to `logs/arcads-api.jsonl`
(model `seedance-2.0`, duration, resolution, aspectRatio, audioEnabled, ref counts,
each returned assetId). Do not log keys.

**Multi-clip (source > 15s) — pick the pattern by source type:**

Look at the beat map from Phase 1 and choose:

**Pattern A — multi-scene explainer (DEFAULT for most long ads).** The source is a
sequence of *distinct scenes* (different setting/action per beat) with **no visual
continuity** to preserve between beats — e.g. an "if she takes X… / problem / solution
/ offer" benefit-stack explainer. Use **per-beat i2v, fired in PARALLEL** (validated
2026-06-22 on a 110s, 8-beat clone):
1. Map each beat to one clip (≤15s). Embed that beat's adapted line in its prompt.
2. **Lock identity across beats** by repeating an identical character description
   verbatim in every prompt (e.g. "a warm 3D-animated woman in her early forties with
   shoulder-length chestnut hair") — text alone held character well; for tighter
   control, generate one hero still and pass it as `referenceImages` on each beat
   (fresh upload per beat). Repeat the **style anchor** verbatim too (e.g. "stylized 3D
   animation, soft warm lighting") so the look is consistent.
3. Beats where the **product** appears → i2v with a **fresh** upload of the product
   image (`@(img1)`). Lifestyle/benefit beats with no package on screen → text-only.
4. **Fire all beats at once** (independent — no ordering dependency). Poll all,
   download each as `beat_N.mp4` preserving order.

**Pattern B — single continuous scene → chained i2v → v2v.** Use only when the whole
ad is *one* person/setting and you need the hands/surface/lighting to carry between
beats:
1. Clip 1: i2v with the product image. Generate → poll → download.
2. Clip 2: v2v with **clip 1's downloaded mp4** as `referenceVideos` (no
   `referenceImages` — mutually exclusive). Upload that mp4 fresh first.
3. Clip 3+: chain v2v from the **most recent** clip. Run **sequentially** (each depends
   on the previous output). Only chain product-only / hands-only clips (faces →
   rejection).

**Stitch (both patterns)** with absolute paths — re-encode for clean A/V sync since
clips come from separate renders:
```bash
printf "file '%s'\n" "$PWD"/beat_*.mp4 > /tmp/list.txt   # ensure correct numeric order
ffmpeg -y -f concat -safe 0 -i /tmp/list.txt -c:v libx264 -crf 20 -c:a aac -movflags +faststart stitched.mp4
```
(`arcads_stitch_videos` is the MCP-native alternative but caps at 6 clips/call and,
in remote clients, needs each clip uploaded first — ffmpeg is simpler for the final master.)

### Phase 8 — Poll, fetch, present

1. For each assetId: poll `arcads_watch_asset` until `generated` / `failed`
   (Seedance ~7 min — poll on a relaxed cadence). Update the log entry with final
   `status`, `creditsCharged`, `generationTimeSec`.
2. Save the returned download URL to `outputs/clone-video-ad/<slug>/`.
3. Open the folder: `open "outputs/clone-video-ad/<slug>/"` (macOS).
4. Present watch/download URLs; numbered list if multiple variations; for multi-clip
   show each clip + the stitched file. Show the total estimated credits.
5. **Optional QA:** spot-check a frame for melted product / wrong hands / drifted
   label. If clearly broken, regenerate once with a corrected prompt (cap 2 retries).

## Seedance 2.0 constraints (quick reference)

| Constraint | Impact |
|---|---|
| `referenceImages` + `referenceVideos` mutually exclusive | Combining → API error. Pick i2v or v2v. |
| v2v with human faces in reference video | Content checker rejects; credits still charged. Use product/hands-only clips for v2v. |
| `audioEnabled: true` + `referenceImages` | Confirmed working (2026-06-22). Historically showed intermittent 500s — if it fails: drop audio, or go text-only, or do silent i2v then v2v with audio. |
| `referenceVideos` count | Only 1 effective despite max 3. |
| `nbGenerations` | 1–10 in one call (use for variations). |
| Aspect ratio | `9:16` or `16:9` only — no `1:1`. |
| Resolution | `480p` / `720p` / `1080p` (MCP adds 1080p vs REST). |
| Duration | 4–15s continuous. |
| Prompt length | 100–260 words. |
| Forbidden words | `cinematic`, `professional`, `stunning`, `8k`, `studio`, `perfect`. |

## Error recovery

| Symptom | Fix |
|---|---|
| `arcads_analyze_media` returns thin/empty blueprint | Re-call with a shorter, sharper prompt; or pass a trimmed clip. Confirm the path/URL is reachable. |
| Generation `status: failed`, content-related | Don't resend the same prompt. Remove flagged language / forbidden words, tighten motion. |
| 500 on audio + image | Audio+image regression — apply the fallback in the constraints table. |
| v2v face rejection | Switch to i2v with the product image. |
| Prompt > 260 words | Trim tone/setting detail; keep beat structure + dialogue. |
| Source > 15s | Split into ≤15s clips; chain i2v→v2v; stitch. |
| Product drifts between shots | Add "@(img1) product unchanged in every shot" + lock label details. |

## Out of scope

- **Static image ads** → `chatgpt-image-ad` / `nano-banana-image-ad`.
- **Reusable markdown templates** (not a generated video) → `arcads-external-api`
  `analyze-video` sub-skill.
- **Veo / Sora / Kling video** → `arcads-external-api` skill.
- **Meta upload** → `meta-ad-builder` skill (this skill outputs files only).

## See also

- [../arcads-external-api/prompting/clone-ad/SKILL.md](../arcads-external-api/prompting/clone-ad/SKILL.md) — the REST/script version (ffmpeg + whisper + curl).
- [../arcads-external-api/prompting/prompt-library/seedance-2.md](../arcads-external-api/prompting/prompt-library/seedance-2.md) — Seedance 2.0 platform rules.
- [../arcads-external-api/SKILL.md](../arcads-external-api/SKILL.md) — broader Arcads conventions (credit estimation, logging, QA loop).
