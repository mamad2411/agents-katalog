---
name: vox-video-director
description: >
  Turn ONE topic into a finished Vox-style paper-collage explainer / ad video, end to end
  with Aliyun Bailian CLI + local ffmpeg — script, collage keyframes, motion, voice-over,
  music, captions, all automated. Use this whenever the user wants a "Vox style" video,
  a paper/torn-paper collage animation, a "motion collage", a narrated explainer or short
  ad built from AI-generated collage posters, a scrapbook-style tribute, or wants to turn
  a topic / product / person into a punchy narrated collage video — even if they don't say
  the word "Vox". Also use when reproducing Stav Zilber / rom1trs / Higgsfield-style collage
  ad workflows.
  Three input modalities: a topic (B-roll), a talking-head video (A-roll mode), or a single
  photo of a person/product anchored into the collage (C-roll mode).
  Triggers: "vox video", "collage video", "motion collage", "paper collage
  explainer", "make a collage ad", "turn this topic into a collage video", "turn my
  photo/this product shot into a collage video".
---

# Vox Video Director

Turn a one-line topic into a finished **Vox-style paper-collage video**: a bold, punchy,
narrated explainer/ad where each beat is a torn-paper collage poster that comes alive, with
voice-over, optional music and captions. Runs through authenticated **Bailian CLI (`bl`)** + local **ffmpeg**.

The look is the modern editorial paper-collage popularized by Vox explainers and creators
like Stav Zilber / rom1trs: hand-cut paper cut-outs, torn edges, tape, halftone dots,
newspaper clippings, bold flat color per beat, big cut-out headlines.

## The core idea (read this first)

The Vox collage look and the collage motion are **two different steps**:

1. **The look is born in the IMAGE step.** Each beat is a finished collage *poster* made by a
   text-to-image model. All the collage DNA (torn paper, cut-outs, halftone, bold color,
   headline text) lives in that image. If the image isn't a rich collage, nothing downstream
   will save it.
2. **The motion is added after.** By default an AI video model animates the whole poster (the
   "living poster" path — simple, automated). For dramatic *piece-by-piece* assembly you cut
   the poster into parts and drive them with the local keyframe engine (advanced path).

Everything hinges on the prompts. **Before writing any image or video prompt, read
`references/prompt-guide.md`** — it has the exact prompt structures that make the difference
between "a real Vox collage" and "a moving PowerPoint".

## Prerequisites (check, don't skip)

- `bl --version` — requires Bailian CLI 1.14.3 or newer.
- `bl auth status` — if unauthenticated, run `bl auth login --api-key <key>` and stop until login succeeds.
- `command -v ffmpeg ffprobe` — required for assembly (`brew install ffmpeg` on macOS).
- `python3 -c "import PIL"` — Pillow, for captions/watermark overlays.

## Standard workflow (topic → film)

This is the default, most-automated path. Every stage is one script, all driven by a single
`beats.json` per project under `out/<project>/`.

1. **Topic → beat map.** First **read `references/beat-layer.md`** (the story layer) and pick a
   narrative `arc` that fits the topic (`timeline` for history, `pas`/`bab` for ads,
   `how_it_works` for explainers, `man_in_hole` for transformations, …). Then write
   `out/<project>/beats.json` following that arc. **Beat 1 must hook within 3s.** Default to
   **one beat = one generated video segment = one shot**. Size every segment from its narration,
   not a fixed template: target **5–10s**, use `python3 scripts/timing.py out/<project>
   --estimated`, and split any narration that estimates above 10s. A 60s film is usually 7–10
   content-sized beats, not six fixed 10s blocks or twelve fixed 5s shots. Vary `camera_move`
   across adjacent beats (never repeat; use `static` on the payoff) and write rich
   `element_motion`. Each beat needs `narration`, `title_cn`/`title_en`, `scene`, `bg`, `feel`,
   `hook`, and one `shots` item whose `dur` may be omitted. This draft with estimated durations
   is the **first mandatory approval gate**. Use `examples/content-timing.beats.json` as the
   default schema example.

2. **Pick the visual style (hybrid — do this BEFORE keyframes).** Do not reuse one house style
   for every topic. Read `references/prompt-guide.md` (§5 theme presets); pick 3–4 **theme presets**
   (`styles.THEME_PRESETS`: `american-retro`, `swiss-modern`, `punk-zine`,
   `soviet-constructivist`, `wpa-propaganda`, `70s-groovy`, `chinese-ink`, `atomic-age`,
   `newsprint-editorial`) that fit
   the topic's era/culture/tone — **or compose a custom theme** by mixing the prompt-guide dimensions
   (medium/era/palette/type/finish) when none fit. Match the topic, **not** the language (an
   English film on Chinese history should look Chinese). A theme bundles the whole LOOK layer
   (idiom+palette+type+finish+mood+motion). Run a bake-off and let the user pick by eye — AI
   proposes, the library is the quality floor, the human decides. Set the pick as `"theme"`:
   `python3 scripts/style_bakeoff.py out/<project> american-retro,swiss-modern,punk-zine,atomic-age`
   Set the chosen name as `"collage_style"` in beats.json (keyframes.py reads it).

3. **Voice + measured timing.** `python3 scripts/audio.py out/<project>`
   Generates one consistent narrator with **`bl speech synthesize` + cosyvoice-v3-flash**, then
   replaces text estimates with measured audio durations plus a short edit tail. New segments
   clamp to 5–10s. If `timing_issues` is non-empty, split those narration beats and run audio
   again **before** paying for images or videos. Pick `voice_id` for the topic and language; see
   `references/voices.md`. Bailian CLI 1.14.x has no music generation command; provide a local
   `bgm_path` or assemble without music.

4. **Keyframes (the collage look).** `python3 scripts/keyframes.py out/<project>`
   Generates one collage poster per beat/shot with **`bl image generate` + qwen-image-3.0**,
   headline text baked in. Compose prompts with the 5-part structure in
   `references/prompt-guide.md`. Verify each poster looks like a *real layered collage*
   before animating — re-roll cheap ($0.08) here rather than paying to animate a weak image.

5. **Motion.** `python3 scripts/clips.py out/<project>`
   Animates each poster with **`bl video generate` + happyhorse-1.1-i2v**. Two independent axes
   (see `references/beat-layer.md` §3, tested on our stack):
   • **`camera_move`** — ONE move per shot. Safe/default: `{static, push_in, pull_out, pan, tilt,
     parallax}`. **Bold/experimental** `{orbit, dolly_zoom, roll, whip}` are **available, not
     banned** — they can warp the flat art, so pair with `constraints: loose` and **re-roll**.
     Any custom phrase also passes through.
   • **`element_motion`** — where the energy lives; **AI writes it per beat to fit that scene** (not a
     template). Make it RICH (several elements moving) — be bold. A **hero element flying across
     the frame** (paper bird/plane/coins) is a great **occasional** punch on a key beat, **not
     every shot** (a flyer in every frame reads as a formula).
   `motion_style` = amplitude `calm | punchy | max` (the theme sets a default). **`constraints`**
   = `strict` (default: defect guards on — flat-2D, one-way, no-morph; best for clean text-heavy
   explainers) or `loose` (let the model explore 3D/bold moves; re-roll the misses). **Headline
   text is hard-protected only on shots that have a title** (detail shots without a headline are
   free to go wild). The Bailian default is `happyhorse-1.1-i2v`; validate real-person
   and brand use against the selected model's current policy before a full run.
   **Aspect routing** (`styles.resolve_video_aspect`, second approval gate): `clips.py` resolves
   `doc["aspect"]` against the chosen `video_model`'s own supported ratios — exact match wins;
   Omni is 16:9/9:16 only, Kling reference-to-video adds 1:1, Kling image-to-video/video-edit and
   Seedance just follow the input/ratio param. When there's no exact match it picks the nearest
   ratio but **stops and asks you to confirm** (set `"aspect_approx_confirmed": true` once you
   have) rather than silently reframing the film — every clip in one run shares the same resolved
   aspect so the finished film is never mixed.

6. **Assemble.** `python3 scripts/assemble.py out/<project>`
   ffmpeg: normalize + concat all shots, lay the single narration ducked under the music,
   burn captions timed per beat, add the watermark. Output `out/<project>/final.mp4`.

7. **Verify.** You can't read an mp4 directly — extract frames to jpg and look:
   `ffmpeg -ss <t> -i final.mp4 -vf "scale=640:-1,format=yuvj420p" -frames:v 1 f.jpg`

### Cadence — content decides duration

- Default to one narration beat and one generated clip per segment. Keep each segment in the
  model-safe **5–10s** range.
- Estimate before generation from text length; after TTS, treat measured `narration_dur` as
  authoritative and round up to the next 0.5s with a ~0.45s edit tail.
- Video APIs receive the next whole second (for example 6.5s → request 7s); assembly trims the
  returned clip to the exact edit duration, so narration is never cut.
- Short text still gets 5s so the idea can land. Long text gets up to 10s. If narration plus
  tail exceeds 10s, split it at a sentence or clause boundary; never speed-read or silently
  stretch a clip past the model limit.
- A 60s film usually lands at 7–10 segments of mixed lengths. Avoid identical durations across
  the whole film unless the source genuinely has equal-length beats.
- Use multiple shots inside one beat only as an explicit editorial choice. Legacy multi-shot
  projects remain supported, but new content-driven projects should split the narration into
  separate beats so each generated clip still has its own 5–10s content unit.

## A-roll mode (talking-head → collage)

The standard workflow above is **B-roll**: a topic becomes AI-generated collage posters
that get animated. **A-roll is the reverse case** — the user already has a real recorded
talking-head video (a presenter speaking to camera) and wants it *itself* turned into the
collage look, keeping their actual performance (face, lip movement, gestures) intact. There
is no poster to generate; the "keyframe" is the presenter's own footage. Use A-roll when the
user gives you a video file of themselves/a presenter talking, not a topic to write from
scratch.

1. **Transcribe + auto-segment.** `python3 scripts/asr_beats.py <project_dir> <source.mp4>`
   Runs `bl speech recognize` (`fun-asr`) on the source audio and cuts it into beats at sentence-ending
   punctuation or natural pause gaps (never exceeding ~9.5s, under Omni/Kling video-edit's
   10s per-call cap). Writes `beats.json` with each beat's `start`/`end`/`text` — **this is
   the same mandatory approval gate as the B-roll beat map**: review it, set `"theme"` (run
   `style_bakeoff.py` the same way — the presenter's segment works fine as the bake-off
   source), and optionally fill in a `content_beats` string per beat (a sticker/stamp idea
   to layer in) before generating anything.

2. **Generate.** `python3 scripts/aroll_clips.py <project_dir> [only_ids]`
   Cuts each beat's time range out of the source, uploads it, and re-styles it with a
   **photographic paper-cutout sticker** treatment on the presenter — her real likeness,
   lip movement, eye-line and gestures follow the source frame-for-frame; only the
   silhouette edge and the world around her are paper-collage. Default model is
   `happyhorse-1.0-video-edit` through `bl video edit` (set via
   `video_model`/`video_model_fallback` in beats.json). **Never ask the model to redraw or halftone-texture the face itself** —
   that gets rejected regardless of how the prompt is worded (tried both a strong and a
   softened phrasing; both failed). Uses the same aspect-routing confirm gate as `clips.py`.

3. **Assemble.** `python3 scripts/aroll_assemble.py <project_dir>`
   Muxes each generated clip with the *original* beat segment's own audio (never whatever
   audio the video model produced) so lip-sync is guaranteed regardless of which model
   handled that beat, normalizes every beat to one canvas, and concats into `final.mp4`.

## C-roll mode (one photo → collage)

The third input modality — "cutout roll". A-roll re-styles a talking-head VIDEO; B-roll
generates everything from a topic; **C-roll takes a single still PHOTO** (a selfie, an
avatar card, a product shot) and anchors it inside the collage world: the subject is cut
out as a PHOTOGRAPHIC sticker — never redrawn — and per-beat posters are generated around
it with an image-EDIT model, then animated through the normal clip stage. Use C-roll when
the user gives you one photo and a topic: a personal explainer fronted by their own face,
or a collage ad built around a real product shot (validated on both, 2026-07-17).

1. **Beat map.** Same as B-roll (`references/beat-layer.md`, same approval gate), plus the
   C-roll fields in beats.json: `"mode": "croll"`, `"anchor_photo"`, `"croll_subject"`
   (`portrait` | `product`), and `subject_wardrobe` (portrait — lock the outfit or the
   paper-doll body drifts) or `subject_desc` (product). Set `"title": false` on shots —
   C-roll posters carry no headline; text belongs to captions. If there is no separate
   script, transcribe/derive narration first and let the audio's ASR timestamps define the
   beats (audio-first, like A-roll — not text-first like B-roll).

2. **Anchored keyframes.** `python3 scripts/croll_keyframes.py <project_dir>`
   Uploads the photo once and generates one anchored poster per shot via
   `qwen-image-3.0` through `bl image edit`. Portraits get a
   photographic face + illustrated paper-doll body; products get a pixel-faithful sticker
   with label typography intact. Prompt rules that are baked in (all three cost a re-run to
   learn): poses/expressions go to the BODY only — asking for a wink redraws the face;
   halftone must be scoped to the background or it bleeds onto skin; portrait clothing must
   be locked explicitly. The script also writes `anchor_freeze` into beats.json.

3. **Voice timing + animate + assemble.** Standard `audio.py` → `clips.py` → `assemble.py`.
   `clips.py` injects the `anchor_freeze` guard into every motion prompt — without it the
   video stage can re-letter a product label (observed: "PARFUM" → "PAREUM") or re-time a
   face. For narration in the subject's own voice, set `voice.clone_ref` (see Voice + music
   above); derive stamp/snap-zoom timing from the narration's ASR word timestamps
   (`asr_beats.py` works on any audio, not just A-roll footage).

## beats.json schema

```json
{
  "project": "my-film", "topic": "...", "language": "en",
  "aspect": "9:16",                       // 16:9 | 9:16 | 1:1 | 3:4
  "style": "collage",
  "provider": "bailian_cli",              // default; invokes authenticated `bl` child processes
  "theme": "american-retro",              // THEME_PRESET (styles.THEME_PRESETS) — the LOOK layer
  "arc": "timeline",                      // narrative arc (beat-layer.md) — the STORY skeleton
  "video_model": "happyhorse-1.1-i2v",
  "image_model": "qwen-image-3.0",
  "image_resolution": "1k",               // 1k (default) | 2k | 4k
  "video_resolution": "720p",             // 720p (default); Seedance also 480p/1080p (Omni is 720p-only)
  "motion_style": "punchy",               // amplitude: calm | punchy | max (theme sets a default)
  "constraints": "strict",                // strict = defect guards on | loose = let AI explore + re-roll
  "timing_mode": "content",               // default: text estimate, then measured TTS duration
  "timing": {"min_segment": 5, "max_segment": 10, "tail": 0.45},
  "voice": {"voice_id": "longtian_v3", "language": "zh", "speed": 1.0}, // see references/voices.md
                                          // + optional "clone_ref": "path/to/sample.mp3" (clone that voice via seed-audio)
                                          //   and "persona": "YouTube tutorial creator" (delivery style for cloned VO)
  "bgm_path": "path/to/instrumental.mp3", // optional; omit to assemble without music
  "mix": {"music": 0.6, "voice": 1.25},   // audio balance — optional; these are the defaults (BGM ducks under the VO)
  "caption_style": "white",               // white (default: clean white subtitle) | paper (cream cut-out collage look)
  "captions": true,                       // false = no burned-in captions (deliver clean, subtitle in post)
  "watermark": "Made By 阿里云百炼CLI",
  "mode": "croll",                        // C-roll only — plus the four fields below
  "anchor_photo": "path/to/photo.png",    // C-roll: the still to anchor (person or product)
  "croll_subject": "portrait",            // C-roll: portrait | product
  "subject_wardrobe": "a cream knitted sweater and charcoal trousers",  // C-roll portrait: outfit lock
  "subject_desc": "the perfume bottle",   // C-roll product: short noun phrase for the sticker
  "beats": [
    {
      "id": 1, "title_cn": "", "title_en": "BEFORE MONEY",
      "bg": "earthy clay tan", "feel": "ancient, humble", "hook": "surprising_stat",
      "narration": "For most of history, there was no money...",
      "shots": [
        // Omit dur: timing.py/audio.py sets a content-driven 5-10s duration.
        {"id": "a", "title": true, "shot_size": "WIDE", "camera_move": "push_in",
         "scene": "...wide establishing collage...",
         "element_motion": "traders gesture, goat bobs, a paper bird crosses, coins scatter"}
      ]
    }
  ]
}
```
`theme`+`arc` set the two big layers; `element_motion` per shot is the energy (make it rich — see
below). `motion`/`collage_style`/`era` are still read for back-compat.

## Bailian model selection

Use `bl model list` when you need to verify or override an ID. Defaults for this edition:

| Job | Model | Note |
|---|---|---|
| Keyframe / collage poster | `qwen-image-3.0` | called through `bl image generate` |
| Anchored image edit | `qwen-image-3.0` | called through `bl image edit` |
| Animate / image-to-video | `happyhorse-1.1-i2v` | called through `bl video generate` |
| Talking-head restyle | `happyhorse-1.0-video-edit` | called through `bl video edit` |
| Narration | `cosyvoice-v3-flash` | called through `bl speech synthesize` |
| ASR | `fun-asr` | called through `bl speech recognize` |
| Music | local file | set `bgm_path`; optional |

See `references/models-and-gotchas.md` for the full model-choice reasoning and every
API / ffmpeg gotcha (auth header, curl downloads, no-libass captions, content blocks, etc.).
Read it before debugging any failure — most failures are already documented there.

**Backends are pluggable.** Every generation call goes through `scripts/provider.py`.
`bailian_cli` is the default and starts parallel `bl` child processes without exposing an API key
to the project. `atlas_cloud` remains as an explicit compatibility backend. Failed CLI jobs may
retry; running CLI jobs are never duplicated on a stall because that could create duplicate charges.

## Advanced: element-level motion collage

The standard path animates the *whole* poster (great, automated, "living poster"). For the
dramatic **pieces-fly-in-and-assemble** motion collage (à la cr7v2), or to animate **real
people with full control and zero content filters**, cut each poster into independent
elements and drive them with the local keyframe engine (no video model needed).

Read `references/local-engine.md`. In short: `extract_elements.py` (crop + background-removal
+ residue/erase cleanup) → `motion.py` (Layer + keyframes, `fly_in`/`slap`/`drop`/`pop_settle`
easings, procedural confetti/starburst, camera zoom+shake+whip, frame render). Pieces fly
back to their **original positions** on a blurred-placeholder backdrop, so the assembled
frame reconstructs the original poster.

## Editions

- **Auto edition** (this skill): topic in, film out, through Bailian CLI.
- **Manual prompt-pack**: if the user cannot run Bailian CLI, just produce the beat map + the per-beat
  image prompts + the per-clip motion prompts + the narration script for them to paste into
  any generator. The creative engine (the prompts) is identical.
