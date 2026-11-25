---
name: pixar-style-ad-arcads-mcp
description: >-
  Produce a Disney-Pixar-style 3D animated video ad end-to-end through the optional Arcads MCP server: gpt-image-2 storyboards, Seedance 2.0 animation, Arcads TTS, stitching, and subtitles. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. Otherwise use the shared REST/local pixar-style-ad prompting guide.
---

# Pixar-Style Ad — Arcads MCP

Build a Disney-Pixar-style 3D animated product ad fully on the Arcads MCP server.
Same proven creative pipeline as the REST `pixar-style-ad` guide — gpt-image-2
storyboard → Seedance 2.0 image-to-video → VO → stitch → captions — but every API
step is an Arcads MCP tool call. The MCP handles auth and job orchestration, so
there's no hand-rolled HTTP Basic header or `POST /v2/...` plumbing.

> ⚠️ **Remote-client caveat (read first).** The MCP server cannot read local disk
> unless the client provides explicit filesystem bridging. In Cursor, every reference file (a user product photo, a generated still you
> chain into the next call, a clip you feed into stitch) must be uploaded via
> `arcads_get_upload_url` + an HTTP `PUT` first, then referenced by the returned S3
> `filePath`. Temp `filePath`s are **single-use**. And keep a `.env` with
> `ARCADS_BASIC_AUTH` for the polling fallback. See **[Uploading & fetching](#uploading-reference-files--fetching-results-remote-agent-clients)**.

| REST `pixar-style-ad` step | MCP replacement |
|---|---|
| `POST /v2/images/generate` (`gpt-image-2`) + presigned upload of each reference | `arcads_generate_image_gpt` (model `gpt-image-2`); references via `arcads_get_upload_url` + PUT → S3 `filePath` (see Uploading) |
| `POST /v2/videos/generate` (`seedance-2.0`) with `startFrame` URL | `arcads_generate_video_seedance_20` with `referenceImages:[still]` (i2v) |
| ElevenLabs TTS VO | `arcads_text_to_speech` (one `voiceId` across all beats) — or keep ElevenLabs if the user insists |
| `GET /v1/assets/{id}` polling (+ "Seedance polls /assets not /videos" gotcha) | `arcads_watch_asset` (status + download URL) — gotcha gone |
| `ffmpeg -f concat` stitch | `arcads_stitch_videos` (2–6 clips/call) — or ffmpeg |
| `.ass` / HyperFrames caption burn | `arcads_add_subtitles` (style catalogue) — or HyperFrames for exact brand styling |
| Manual `Authorization: $ARCADS_BASIC_AUTH` header on every call | MCP injects auth — you only need `.env` for the polling fallback |

What does **not** change vs REST: reference files are still uploaded per call and
temp `filePath`s are still single-use (see Uploading below). What the MCP does remove:
hand-rolled auth headers, the "Seedance polls `/v1/assets` not `/v1/videos`" gotcha
(`arcads_watch_asset` abstracts it), and N-parallel-POSTs for variations (`nbGenerations`).

**The only non-MCP step:** muxing the VO mp3 onto each silent clip + tight-trimming
to kill dead space. No single Arcads MCP tool muxes a standalone audio track onto a
video, so that one step uses local `ffmpeg`.

## Read order (creative source of truth — read before generating)

1. **This file** — the MCP workflow & tool mapping.
2. **[../../shared/skills/pixar-style-ad/prompting/guide.md](../../shared/skills/pixar-style-ad/prompting/guide.md)** — the Pixar creative bible: aesthetic traits, the 4-beat anthropomorphism arc, cast sheet, STYLE LOCK, "no dead space" rule, negative block, captioning. **API-agnostic — all of it applies.**
3. **[../../shared/skills/pixar-style-ad/prompting/storyboard-gpt-image-2.md](../../shared/skills/pixar-style-ad/prompting/storyboard-gpt-image-2.md)** — per-beat gpt-image-2 still prompts.
4. **[../../shared/skills/pixar-style-ad/prompting/animate-seedance-2.md](../../shared/skills/pixar-style-ad/prompting/animate-seedance-2.md)** — per-beat Seedance 2.0 image-to-video prompts.
5. **[../arcads-external-api/prompting/prompt-library/seedance-2.md](../arcads-external-api/prompting/prompt-library/seedance-2.md)** — Seedance platform rules (forbidden words, motion, timestamps).

## Tools used (Arcads MCP)

| Tool | Role | Key params |
|---|---|---|
| `arcads_list_products` | Resolve `productId` (auto-selected if only one). | — |
| `arcads_generate_image_gpt` | Storyboard stills. | `prompt`, `model:"gpt-image-2"`, `aspectRatio:"9:16"`, `referenceImages` (≤5 — chain prior approved stills for identity), `nbGenerations` |
| `arcads_generate_video_seedance_20` | Animate each approved still (i2v). | `prompt`, `referenceImages:[still]`, `aspectRatio:"9:16"`, `duration` 3–15, `resolution:"720p"`, `audioEnabled:false`, `nbGenerations` |
| `arcads_list_voices` | Pick the VO voice once. | filter `gender`, `age`, `language:"English"` |
| `arcads_text_to_speech` | Voiceover per beat. | `script`, `voiceId` (same across all beats) |
| `arcads_stitch_videos` | Concatenate clips (2–6 per call). | `videoPaths[]` in playback order |
| `arcads_add_subtitles` | Burn captions on the voiced master. | `videoPath`/`sourceVideoAssetId`, `style` |
| `arcads_watch_asset` | Poll status and fetch the download URL for every asset id. | `assetId` |

## Hard rules — never relax

1. **Aesthetic = Disney-Pixar 3D feature film**, not anime/Ghibli/2D/Dreamworks. Paste the STYLE LOCK from the guide verbatim into every still prompt. Honor the guide's banned-words list (`anime`, `Ghibli`, `2D`, `cel-shaded`, `cartoon`, `photorealistic`, …) **and** Seedance's forbidden words (`cinematic`, `professional`, `stunning`, `8k`, `studio`, `perfect`).
2. **The hook is anthropomorphism + a tiny story, not the product.** Beat 1 gives the pain point a sentient face/voice. Plan all beats up front for character/setting continuity.
3. **Storyboard first, then animate.** Never one-shot text-to-video the whole ad — character drifts and Seedance's 15s ceiling caps you below 60–90s anyway. Lock each still (user approval) before animating.
4. **One VO voice across all beats.** Pick one `voiceId` and reuse it. Never use Seedance's in-prompt `Narrator:` line — set `audioEnabled:false` and overlay VO in post (cross-skill hard rule).
5. **No dead space.** VO drives clip duration — trim each clip to `vo_dur + ~0.5s`. Never `atempo` the VO.
6. **Two mandatory gates, in order:** (a) **script/dialogue approval** (numbered beat block), then (b) **credit-cost estimate** (label as estimate; Arcads has no billing endpoint). Generate only after both.
7. **9:16 default** (no `1:1` on Seedance; avoid `16:9` — the close-up macro framings don't translate). **Log every generation** to `logs/arcads-api.jsonl` (no keys).

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
references it. Re-using the same still for Beat 2's reference and again for the Seedance
i2v step means **two** uploads. Upload a fresh copy immediately before each consuming
call (a single `nbGenerations` call is one consumer — fine). Don't pass an
`arcads_register_image` asset id to `referenceImages` (returns `INVALID_REFERENCE_IMAGES`).

**Chaining generated stills:** after a still reaches `generated`, download it (watch
URL / REST `data.imageUrl`) to `outputs/.../stills/beatN.png`, then upload a fresh temp
copy before each call that uses it as a reference.

**Polling & fetch.** Call `arcads_watch_asset(assetId)` until `generated` or
`failed`; on success it also returns the download URL. Do not rely on an inline
widget. If the polling tool is unavailable, use the REST fallback (needs `.env`
`ARCADS_BASIC_AUTH`):
```bash
set -a && . ./.env && set +a
BASE="${ARCADS_BASE_URL:-https://external-api.arcads.ai}"
curl -s -H "Authorization: $ARCADS_BASIC_AUTH" "$BASE/v1/assets/<assetId>"  # status, data.imageUrl/videoUrl, data.creditsCharged
```

## Workflow

### Phase 0 — Cast & continuity sheet (BEFORE any generation)
Build the cast sheet from the guide: protagonist (human hero), the anthropomorphic
problem character (beat 1), mascot characters (beat 3 mechanism), setting, product
packaging, verbatim STYLE LOCK. Save to `references/<brand>-pixar-cast.md`. Confirm.

### Phase 1 — 4–6 beat script
One sentence per beat following the arc: **Hook (anthropomorphized problem) →
Reveal (protagonist meets product) → Mechanism (mascot scene) → CTA (protagonist +
packaging)**. Optional variations: cold-open intercut, multi-pain montage,
testimonial overlay. **Dialogue approval gate** — numbered beat block:

```
📝 Pixar script (confirm before I generate)
  1. [HOOK]      drain-hair character: "I clog your shower every single morning…"
  2. [REVEAL]    protagonist: "Then I found this."
  3. [MECHANISM] narrator: "Tiny helpers rebuild each strand from the root."
  4. [CTA]       narrator: "Try {Brand} {Product} now."
VO words: ~N total · Est. runtime: ~Xs · One voice across all beats: ✅
Approve this script? (yes / edit / rewrite)
```

### Phase 2 — Storyboard stills (gpt-image-2, sequential for identity)
1. Beat 1 hero still (the anthropomorphized problem character): `arcads_generate_image_gpt(prompt=<beat-1 from storyboard file + STYLE LOCK>, model="gpt-image-2", aspectRatio="9:16")`. Poll `arcads_watch_asset` → save `outputs/pixar/<slug>/stills/beat1.png`. Show user; iterate until approved.
2. Beats 2–N: generate **sequentially**, passing the prior approved still(s) as `referenceImages` (≤5) to lock the protagonist's face/outfit and product packaging. Approve each before the next.
3. Mascot/mechanism beat: pass the protagonist still only if the protagonist appears; otherwise generate independently from the cast-sheet mascot description.
> MCP note (remote clients): to chain a prior approved still as `referenceImages`, download it then **upload a fresh temp copy** via `arcads_get_upload_url` + PUT immediately before the call (temp `filePath`s are single-use). See [Uploading & fetching](#uploading-reference-files--fetching-results-remote-agent-clients).

### Phase 3 — Animate each still (Seedance 2.0 i2v)
For each approved still, **upload it fresh** (`arcads_get_upload_url` + PUT → S3
`filePath`), read its per-beat prompt in the animate file, then:
`arcads_generate_video_seedance_20(prompt=<beat prompt, no Narrator line, ambient SFX ok, "no on-screen text/captions">, referenceImages=[<fresh S3 filePath of beatN.png>], aspectRatio="9:16", duration=<3–10 by beat>, resolution="720p", audioEnabled=false, nbGenerations=<N>)`.
Beats are independent — fire them, then poll all ids (Seedance ~7 min/clip).
Poll `arcads_watch_asset` → save `outputs/.../clips/beatN.mp4`.
**QA:** watch for character morphing, hand artifacts, eye misalignment, product-label
drift, and Seedance inventing captions (the negative block fights this). ≤2 retries/beat.

### Phase 4 — Voiceover (Arcads TTS)
1. `arcads_list_voices(language="English", gender=<by persona>, age=<by persona>)` → pick **one** `voiceId`. For the anthropomorphized problem character's line you may pick a second characterful `voiceId`.
2. Per beat: `arcads_text_to_speech(script=<beat line>, voiceId=<chosen>)` → poll → `arcads_watch_asset` → save `outputs/.../vo/beatN.mp3`.
> ElevenLabs alternative available if the user insists and has `ELEVENLABS_API_KEY`; default is Arcads TTS for an all-MCP pipeline.

### Phase 5 — Reconcile VO ↔ clip (ffmpeg — only non-MCP step)
Per beat, trim the clip to the VO and mux (kills dead space):
```bash
VO=outputs/.../vo/beatN.mp3; CLIP=outputs/.../clips/beatN.mp4
VO_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VO")
TARGET=$(python3 -c "import sys;print(min(float(sys.argv[1]),float(sys.argv[2])+0.5))" \
  "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")" "$VO_DUR")
ffmpeg -y -i "$CLIP" -t "$TARGET" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -an outputs/.../tight/beatN.mp4
ffmpeg -y -i outputs/.../tight/beatN.mp4 -i "$VO" -c:v copy -c:a aac -shortest outputs/.../voiced/beatN.mp4
```
If VO is longer than the clip: split the line or regenerate the clip longer — never
speed up the VO.

### Phase 6 — Stitch (Arcads MCP)
Upload each voiced clip fresh (`arcads_get_upload_url` + PUT), then
`arcads_stitch_videos(videoPaths=[<filePath beat1> … <filePath beatN>])` — max 6 per
call; for >6 beats stitch in batches, download each part, and combine the parts
(re-uploading fresh). Save `outputs/.../pixar-master.mp4`.

### Phase 7 — Captions (Arcads MCP)
`arcads_add_subtitles(videoPath="outputs/.../pixar-master.mp4", style="style_1")` for
the white-with-black-stroke TikTok look (try `style_2`/`glide` for variants; exact
brand styling → HyperFrames recipe in the guide). Poll → `arcads_watch_asset` → save final.

### Phase 8 — Deliver
1. Save the captioned final to `outputs/pixar/<slug>/final.mp4`; `open` the folder (macOS).
2. Present the watch URL + per-beat clips. Show total **estimated** credits with the estimate-only disclosure.
3. Update each `logs/arcads-api.jsonl` entry with final status/credits.

## Credit-cost gate (MANDATORY, before Phase 2 generation)
A typical 5-beat ad ≈ 5 gpt-image-2 stills + 5 Seedance clips + 5 TTS lines + 1 stitch + 1 caption pass (plus ≤2 retries/beat). Read `logs/arcads-api.jsonl` for past per-call credits; else `MASTER_CONTEXT.md`; else ask. Present the breakdown, label it an **estimate**, tell the user to confirm exact pricing in the Arcads platform, and wait for "yes."

## Constraints & gotchas (quick reference)
| Item | Note |
|---|---|
| Seedance aspect | `9:16` / `16:9` only — **no `1:1`**. Use `9:16` (avoid `16:9` for this genre). |
| Seedance i2v input | MCP uses `referenceImages:[still]` (not REST `startFrame`). |
| gpt-image-2 refs | max 5 → fine, each beat chains 1–2 prior stills. |
| `referenceImages` + `referenceVideos` | mutually exclusive on Seedance. Pixar is pure i2v — never pass both. |
| Forbidden words | banned-words list (guide) + Seedance's `cinematic/professional/stunning/8k/studio/perfect`. |
| Seedance invents captions | always include "no on-screen text, no captions, no subtitles" in the animate prompt; burn captions in post. |
| VO muxing | no MCP tool muxes standalone audio onto video → ffmpeg (Phase 5). |
| Stitch limit | `arcads_stitch_videos` = 2–6 clips/call; batch for >6. |
| Polling | `arcads_watch_asset` until `generated`/`failed`; on success it returns the download URL (~12h). If unavailable, use the documented REST fallback. Do not rely on inline widgets. |

## Out of scope
- **Clay stop-motion look** → `claymation-ad-arcads-mcp`.
- **Live-action UGC / clone an existing ad** → `clone-video-ad-seedance-arcads-mcp`.
- **Static image ads** → `chatgpt-image-ad` / `nano-banana-image-ad`.
- **Meta upload** → `meta-ad-builder`.

## See also
- [../../shared/skills/pixar-style-ad/prompting/guide.md](../../shared/skills/pixar-style-ad/prompting/guide.md) — Pixar creative bible (REST + this MCP version share it).
- [claymation-ad-arcads-mcp](../claymation-ad-arcads-mcp/SKILL.md) — sibling clay stop-motion MCP skill.
- [clone-video-ad-seedance-arcads-mcp](../clone-video-ad-seedance-arcads-mcp/SKILL.md) — clone an existing video ad on Seedance + MCP.
- [../arcads-external-api/SKILL.md](../arcads-external-api/SKILL.md) — broader Arcads conventions.
