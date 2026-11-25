---
name: claymation-ad-arcads-mcp
description: >-
  Produce an Aardman/Laika-style stop-motion claymation video ad end-to-end through the optional Arcads MCP server: gpt-image-2 storyboards, Seedance 2.0 animation, Arcads TTS, stitching, and subtitles. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. Otherwise use the shared REST/local claymation-ad prompting guide.
---

# Claymation Ad — Arcads MCP

Build a narrative **claymation** (Aardman/Laika stop-motion) product ad fully on the
Arcads MCP server. Same proven creative pipeline as the REST `claymation-ad` guide —
gpt-image-2 storyboard → Seedance 2.0 image-to-video → narrator VO → stitch →
captions — but every API step is an Arcads MCP tool call. The MCP handles auth and
job orchestration, so there's no hand-rolled HTTP Basic header or `POST
/v2/...` plumbing.

> ⚠️ **Remote-client caveat (read first).** The MCP server cannot read local disk
> unless the client provides explicit filesystem bridging. In Cursor, every reference file (a user product photo, a generated still you
> chain into the next call, a clip you feed into v2v/stitch) must be uploaded via
> `arcads_get_upload_url` + an HTTP `PUT` first, then referenced by the returned S3
> `filePath`. Temp `filePath`s are **single-use**. And keep a `.env` with
> `ARCADS_BASIC_AUTH` for the polling fallback. See **[Uploading & fetching](#uploading-reference-files--fetching-results-remote-agent-clients)**.

| REST `claymation-ad` step | MCP replacement |
|---|---|
| `POST /v2/images/generate` (`gpt-image-2`) + presigned upload of each reference | `arcads_generate_image_gpt` (model `gpt-image-2`); references via `arcads_get_upload_url` + PUT → S3 `filePath` (see Uploading) |
| `POST /v2/videos/generate` (`seedance-2.0`) with `startFrame` URL | `arcads_generate_video_seedance_20` with `referenceImages:[still]` (i2v) |
| ElevenLabs TTS per beat | `arcads_text_to_speech` (one `voiceId` across all beats) — or keep ElevenLabs if the user insists |
| `GET /v1/assets/{id}` polling (+ the "Seedance polls /assets not /videos" gotcha) | `arcads_watch_asset` (status + download URL) — gotcha gone |
| `ffmpeg -f concat` stitch | `arcads_stitch_videos` (2–6 clips/call) — or ffmpeg |
| `.ass` / HyperFrames caption burn | `arcads_add_subtitles` (style catalogue) — or HyperFrames for exact brand styling |
| Manual `Authorization: $ARCADS_BASIC_AUTH` header on every call | MCP injects auth — you only need `.env` for the polling fallback |

What does **not** change vs REST: reference files are still uploaded per call and
temp `filePath`s are still single-use (see Uploading below). What the MCP does remove:
hand-rolled auth headers, the "Seedance polls `/v1/assets` not `/v1/videos`" gotcha
(`arcads_watch_asset` abstracts it), and N-parallel-POSTs for variations (`nbGenerations`).

**The only non-MCP step:** muxing the VO mp3 onto each silent clip + tight-trimming
to kill dead space (the "VO drives clip duration" rule). No single Arcads MCP tool
muxes a standalone audio track onto a video, so that one step uses local `ffmpeg`.

## Read order (creative source of truth — read before generating)

1. **This file** — the MCP workflow & tool mapping.
2. **[../../shared/skills/claymation-ad/prompting/guide.md](../../shared/skills/claymation-ad/prompting/guide.md)** — the full claymation creative bible: aesthetic traits, the 8-beat arc, cast sheet, STYLE LOCK, narration rules, "no dead space" rule, negative block, captioning. **API-agnostic — all of it applies.**
3. **[../../shared/skills/claymation-ad/prompting/storyboard-gpt-image-2.md](../../shared/skills/claymation-ad/prompting/storyboard-gpt-image-2.md)** — per-beat gpt-image-2 still prompts.
4. **[../../shared/skills/claymation-ad/prompting/animate-seedance-2.md](../../shared/skills/claymation-ad/prompting/animate-seedance-2.md)** — per-beat Seedance 2.0 image-to-video prompts.
5. **[../arcads-external-api/prompting/prompt-library/seedance-2.md](../arcads-external-api/prompting/prompt-library/seedance-2.md)** — Seedance platform rules (forbidden words, motion, timestamps).

## Tools used (Arcads MCP)

| Tool | Role | Key params |
|---|---|---|
| `arcads_list_products` | Resolve `productId` (auto-selected if only one). | — |
| `arcads_generate_image_gpt` | Storyboard stills. | `prompt`, `model:"gpt-image-2"`, `aspectRatio:"9:16"`, `referenceImages` (≤5 — chain prior approved stills for identity), `nbGenerations` |
| `arcads_generate_image_nano_banana` | Clay-texture fallback for close-ups (beats 5–6). | `model:"nano-banana"` (Pro), `referenceImages` (≤14) |
| `arcads_generate_video_seedance_20` | Animate each approved still (i2v). | `prompt`, `referenceImages:[still]`, `aspectRatio:"9:16"`, `duration` 4–15, `resolution:"720p"`, `audioEnabled:false`, `nbGenerations` |
| `arcads_list_voices` | Pick the narrator voice once. | filter `gender`, `age`, `language:"English"` |
| `arcads_text_to_speech` | Narrator + character VO per beat. | `script`, `voiceId` (same across all beats) |
| `arcads_stitch_videos` | Concatenate clips (2–6 per call). | `videoPaths[]` in playback order |
| `arcads_add_subtitles` | Burn captions on the voiced master. | `videoPath`/`sourceVideoAssetId`, `style` |
| `arcads_watch_asset` | Poll status and fetch the download URL for every asset id. | `assetId` |

## Hard rules — never relax

1. **Aesthetic = Aardman/Laika claymation**, not Pixar/CGI. Paste the STYLE LOCK from the guide verbatim into every still prompt. Honor the guide's banned-words list (`Pixar`, `3D rendered`, `CGI`, `photorealistic`, …) **and** Seedance's forbidden words (`cinematic`, `professional`, `stunning`, `8k`, `studio`, `perfect`).
2. **Storyboard first, then animate.** Never text-to-video the whole ad — identity drifts. Lock each still (with user approval) before animating it.
3. **One narrator voice across all beats.** Pick one `voiceId` and reuse it. Never use Seedance's in-prompt `Narrator:` line — set `audioEnabled:false` and overlay VO in post (the guide's hard rule, confirmed 2026-05-19).
4. **No dead space.** VO drives clip duration — trim each clip to `vo_dur + ~0.5s`. Never `atempo` the VO.
5. **Two mandatory gates, in order:** (a) **script/dialogue approval** (numbered beat block), then (b) **credit-cost estimate** (label as estimate; Arcads has no billing endpoint). Generate only after both.
6. **9:16 only** (no `1:1` on Seedance). Aspect `9:16` for stills and clips.
7. **Log every generation** to `logs/arcads-api.jsonl` (tool, model, beat, duration, ref count, assetId, creditsCharged on completion). No keys.

## Uploading reference files & fetching results (remote agent clients)

**Every reference image/video the MCP consumes must be an Arcads S3 `filePath`, not a
local path.** This applies to a user-supplied product photo **and** to each generated
still you chain forward (Beat 1 → Beat 2 reference, still → Seedance i2v, clip →
stitch).

Upload flow (tested):
1. `arcads_get_upload_url(mimeType)` → `{presignedUrl, filePath}` (`image/png`, `video/mp4`, …).
2. `PUT` the bytes: `curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: image/png" --upload-file "<file>" "<presignedUrl>"` → expect `200`.
3. Pass the returned `filePath` in `referenceImages` / `videoPaths`.

**Single-use rule:** a temp `filePath` is consumed by the **first** call that
references it. Re-uploading the same still for Beat 2's reference and again for the
Seedance i2v step means **two** uploads. Upload a fresh copy immediately before each
consuming call (a single `nbGenerations` call is one consumer — fine). Don't pass an
`arcads_register_image` asset id to `referenceImages` (returns `INVALID_REFERENCE_IMAGES`).

**Chaining generated stills:** after a still reaches `generated`, download it (watch
URL / REST `data.imageUrl`) to `outputs/.../stills/beatN.png`, then upload a fresh temp
copy before each call that uses it as a reference.

**Polling & fetch.** Try `arcads_watch_asset(assetId)` (returns `status` + a
`downloadUrl` once generated). Both MCP polling tools can be unavailable for a
session, so treat
the REST fallback below as the reliable path and don't block on the MCP poll tools.
REST fallback (needs `.env` `ARCADS_BASIC_AUTH` — it already contains the `Basic …`
prefix; `curl -u "$ARCADS_API_KEY:"` returns 403):
```bash
set -a && . ./.env && set +a
BASE="${ARCADS_BASE_URL:-https://external-api.arcads.ai}"
curl -s -H "Authorization: $ARCADS_BASIC_AUTH" "$BASE/v1/assets/<assetId>"
# status: pending→generated/failed | data.imageUrl (image) / data.videoUrl (seedance) / data.audioUrl (tts) | data.creditsCharged
```
Use the client's wait/poll mechanism for long renders instead of blocking a shell
with `sleep` (Seedance render time is variable: observed **195s–510s**, so allow
~15 min).

## Workflow

### Phase 0 — Cast & continuity sheet (BEFORE any generation)
Build the cast sheet from the guide (protagonist, supporting character, narrator
persona, primary + secondary miniature settings, product-as-clay-prop, verbatim
STYLE LOCK). Save to `references/<brand>-claymation-cast.md`. Confirm with the user.

### Phase 1 — 8-beat script (or 5-beat short)
Write one narrator sentence per beat + any sparse character dialogue, following the
arc in the guide (Setup → Inciting → Social validation → Quiet despair → Clay
infographic → Discovery → Transformation → Resolution/CTA). The 5-beat short drops
beats 3–5. **Dialogue approval gate** — present the numbered beat block:

```
📝 Claymation script (confirm before I generate)
  1. [SETUP]      narrator: "Diane had used the same kitchen for thirty years…"
  2. [INCITING]   narrator: "…until the morning the mirror told a different story."
  …
  8. [CTA]        narrator: "Refirm. The age you feel, not the age you are."
Narrator words: ~N total · Est. runtime: ~Xs · One voice across all beats: ✅
Approve this script? (yes / edit / rewrite)
```

### Phase 2 — Storyboard stills (gpt-image-2, sequential for identity)
1. Beat 1 hero still: `arcads_generate_image_gpt(prompt=<beat-1 from storyboard file + STYLE LOCK>, model="gpt-image-2", aspectRatio="9:16")`. Poll `arcads_watch_asset` → save to `outputs/claymation/<slug>/stills/beat1.png`. Show the user; iterate until approved.
2. Protagonist beats (2, 4, 6, 7, 8): generate **sequentially**, passing the approved Beat-1 still (and the most recent approved still) as `referenceImages` (≤5) to lock "Diane." Approve each.
3. Beat 3 (two-character): pass protagonist still + describe the supporting character.
4. Beat 5 (clay infographic) and product close-ups: independent. If gpt-image-2 smooths the clay texture, fall back to `arcads_generate_image_nano_banana(model="nano-banana")` for those beats only.
> MCP note (remote clients): to chain a prior approved still as `referenceImages`, download it then **upload a fresh temp copy** via `arcads_get_upload_url` + PUT immediately before the call (temp `filePath`s are single-use). See [Uploading & fetching](#uploading-reference-files--fetching-results-remote-agent-clients).

### Phase 3 — Animate each still (Seedance 2.0 i2v)
For each approved still, **upload it fresh** (`arcads_get_upload_url` + PUT → S3
`filePath`), read its per-beat prompt in the animate file, then:
`arcads_generate_video_seedance_20(prompt=<beat prompt, no Narrator line, ambient SFX ok>, referenceImages=[<fresh S3 filePath of beatN.png>], aspectRatio="9:16", duration=<6–12 by beat>, resolution="720p", audioEnabled=false, nbGenerations=<N variations>)`.
Beats are independent — fire them, then poll all ids. Seedance ~7 min/clip.
Poll `arcads_watch_asset` → save to `outputs/.../clips/beatN.mp4`.
**QA (claymation-specific):** watch for clay flattening into smooth 3D, fabric losing
knit weave, label paint going digitally crisp, melted features. Up to 2 retries/beat
with a corrected prompt.

### Phase 4 — Narrator VO (Arcads TTS)
1. `arcads_list_voices(pageSize=…)` → pick **one** `voiceId` (Aardman tone: warm storyteller — e.g. **George** `JBFqnCBsd6RMkjVDRZzb`). For character lines, optionally pick a second `voiceId`.
   - ⚠️ **Don't pass the `gender`/`age`/`language` filters** — they 400 (backend wants arrays like `[MIDDLE_AGED]` while the MCP schema sends the string `"Middle Aged"`). Call unfiltered and filter the returned list yourself.
2. Per beat: `arcads_text_to_speech(script=<beat narrator line>, voiceId=<chosen>)` → poll → `arcads_watch_asset` → save `outputs/.../vo/beatN.mp3`.
> ElevenLabs alternative: if the user wants the specific George/Hope/Chris voices and has `ELEVENLABS_API_KEY`, use the ElevenLabs flow from the guide instead. Default is Arcads TTS for an all-MCP pipeline.

### Phase 5 — Reconcile VO ↔ clip (ffmpeg — only non-MCP step)
Per beat, kill dead space (guide's hard rule). Measure both, trim the clip to the VO,
then mux:
```bash
VO=outputs/.../vo/beatN.mp3; CLIP=outputs/.../clips/beatN.mp4
VO_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VO")
TARGET=$(python3 -c "import sys;print(min(float(sys.argv[1]),float(sys.argv[2])+0.5))" \
  "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")" "$VO_DUR")
ffmpeg -y -i "$CLIP" -t "$TARGET" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -an outputs/.../tight/beatN.mp4
ffmpeg -y -i outputs/.../tight/beatN.mp4 -i "$VO" -c:v copy -c:a aac -shortest outputs/.../voiced/beatN.mp4
```
If VO is longer than the clip: split the line across beats or regenerate the clip
longer — never speed up the VO. (`arcads_trim_video` can trim by fixed offsets, but
ffmpeg gives the exact VO-matched cut and does the mux in one place.)

### Phase 6 — Stitch (Arcads MCP)
Upload each voiced clip fresh (`arcads_get_upload_url` + PUT), then
`arcads_stitch_videos(videoPaths=[<filePath beat1> … <filePath beat6>])` — max 6 per
call. For 8 beats: stitch 1–6, download the result, upload it + the remaining clips
fresh, then `arcads_stitch_videos([<part1>, <beat7>, <beat8>])`. Save the master to
`outputs/.../claymation-master.mp4`.
> Optional stop-motion judder: `ffmpeg -i master.mp4 -filter:v "fps=12,fps=24" judder.mp4`.

### Phase 7 — Captions (Arcads MCP)
`arcads_add_subtitles(sourceVideoAssetId="<stitched asset id>", style="style_1")` —
pass the stitch's asset id directly via `sourceVideoAssetId` to **skip re-uploading**
the master (captions auto-transcribe from the baked-in VO). Use `videoPath` only for a
local file with no Arcads asset id.
(white-with-stroke TikTok look). For the orange-highlight-block reference look there's
no exact preset — closest are `fusion`/`style_3`; for exact brand styling use the
HyperFrames caption recipe in the guide. Poll → `arcads_watch_asset` → save final.

### Phase 8 — Deliver
1. Save the captioned final to `outputs/claymation/<slug>/final.mp4`; `open` the folder (macOS).
2. Present the watch URL + per-beat clips. Show total **estimated** credits (sum of `creditsCharged` across all asset ids) with the estimate-only disclosure.
3. Update each `logs/arcads-api.jsonl` entry with final status/credits.

## Credit-cost gate (MANDATORY, before Phase 2 generation)
A full 8-beat ad ≈ 8 gpt-image-2 stills + 8 Seedance clips + 8 TTS lines + 1–2 stitches + 1 caption pass (plus up to 2 retries/beat). Read `logs/arcads-api.jsonl` for past per-call credits; else `MASTER_CONTEXT.md`; else ask. Present the breakdown, label it an **estimate**, tell the user to confirm exact pricing in the Arcads platform, and wait for "yes."

**Measured rates (this workspace, 2026-06-22 — confirm in-platform):** gpt-image-2 still = **0 cr** (on a daily-limit image plan, effectively free) · `arcads_text_to_speech` = **~8 cr/line** · `arcads_generate_video_seedance_20` 5s/720p i2v = **240 cr/clip** (the dominant cost — billed at submission, shows while still `pending`) · `arcads_stitch_videos` = **0 cr** · `arcads_add_subtitles` = **~80 cr**. So an 8-beat ad's cost is essentially `8 × Seedance (~240) ≈ 1,900+ cr`; the credit gate matters because of video, not images. (A validated 2-beat micro-ad ran **576 cr** total.)

## Constraints & gotchas (quick reference)
| Item | Note |
|---|---|
| Seedance aspect | `9:16` / `16:9` only — **no `1:1`**. Use `9:16`. |
| Seedance i2v input | MCP uses `referenceImages:[still]` (not REST `startFrame`). |
| gpt-image-2 refs | max 5 → fine, each beat chains 1–2 prior stills. |
| `referenceImages` + `referenceVideos` | mutually exclusive on Seedance. Claymation is pure i2v — never pass both. |
| Forbidden words | banned-words list (guide) + Seedance's `cinematic/professional/stunning/8k/studio/perfect`. |
| VO muxing | no MCP tool muxes standalone audio onto video → ffmpeg (Phase 5). |
| Stitch limit | `arcads_stitch_videos` = 2–6 clips/call; batch for 8 beats. |
| Polling | `arcads_watch_asset` until `generated`/`failed`; on success it returns the download URL (~12h). If unavailable, use the documented REST fallback. Do not rely on inline widgets. |

## Out of scope
- **Pixar 3D look** → `pixar-style-ad-arcads-mcp`.
- **Live-action UGC / clone an existing ad** → `clone-video-ad-seedance-arcads-mcp`.
- **Static image ads** → `chatgpt-image-ad` / `nano-banana-image-ad`.
- **Meta upload** → `meta-ad-builder`.

## See also
- [../../shared/skills/claymation-ad/prompting/guide.md](../../shared/skills/claymation-ad/prompting/guide.md) — claymation creative bible (REST + this MCP version share it).
- [pixar-style-ad-arcads-mcp](../pixar-style-ad-arcads-mcp/SKILL.md) — sibling 3D-Pixar MCP skill.
- [clone-video-ad-seedance-arcads-mcp](../clone-video-ad-seedance-arcads-mcp/SKILL.md) — clone an existing video ad on Seedance + MCP.
- [../arcads-external-api/SKILL.md](../arcads-external-api/SKILL.md) — broader Arcads conventions.
