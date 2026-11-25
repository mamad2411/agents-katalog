---
name: create-video
description: Generate synchronized audio-video locally with MiniMax H3 Turbo on the ROCm GPU. Use this skill ONLY when the user explicitly asks to generate, create, make, or animate a video/moving-image deliverable (for example 生成影片、製作動畫、做影片, create a video, animate this image, or make an MV), or explicitly requests MiniMax/Hailuo H3 video generation. Do not load it merely because the prompt mentions video, animation, movie, film, clips, MiniMax H3, or an existing video.
version: 3.0.1
author: Hermes Agent
license: MIT
prerequisites:
  commands: [ffmpeg]
  paths: [~/src/ComfyUI]
metadata:
  hermes:
    tags: [video, generation, ai, minimax, minimax-h3, hailuo-h3, comfyui, text-to-video, image-to-video, t2v, i2v, fl2va, diffusion, audio, animation, zero-swap-uma]
    related_skills: [create-image, create-music, mock-voice, restyle-music]
---

# Create Video — MiniMax H3 (synchronized audio, ROCm)

Generate text-to-video and first-frame image-to-video with MiniMax H3 on the Radeon
8060S/gfx1151 through the persistent ComfyUI service at `http://127.0.0.1:8188`.
MiniMax H3 is the only backend in this skill.

## Small-model executable protocol — follow literally

> [!IMPORTANT]
> **No workspace switch, no extension.** Do **not** run `switch-workspace.py`, do **not** `cd`
> into or switch the channel to `~/video_workspace`, and do **not** call any `video_workflow`,
> `video_define_brief`, `video_define_cut_plan`, `video_submit_artifacts` or `video_record_review`
> tool (the create-video-guard extension is not used). Stay in the current workspace and run the
> CLI wrapper directly with bash.

This section overrides improvisation. Apply it only after the user has explicitly requested a
new generated video, animation, animate-a-still result, MV, or other moving-image deliverable.
Mere topical mention is not activation. Once that explicit generation intent is present:

0. **CLI only — never drive ComfyUI yourself.** Generate video exclusively with
   `$HOME/.pi/agent/skills/create-video/create_video.sh`. Do **not** open the ComfyUI web frontend
   (`http://127.0.0.1:8188` in a browser/nodriver/playwright), do **not** `curl`/`wget`/`requests`/
   `urllib` POST to `/prompt`, and do **not** poll `/queue`, `/history`, `/view` or `/ws` to run or
   collect a generation. Do not hand-build or edit workflow JSON (including `workflows/*.json`) and
   submit it. The wrapper already builds the graph, submits, waits, and copies the MP4 to `--output`.
1. **Single short clip (≤5.2 s), e.g. "生成一段 5 秒影片":** write one structured prompt (see
   **Prompt structure**) and run the wrapper once, foreground, bash timeout ≥600 s:
   `$HOME/.pi/agent/skills/create-video/create_video.sh --duration 5 --prompt-file <prompt.txt> -o "$HOME/generated/minimax-h3/<name>.mp4"`
   (write the plain-text English prompt to the file with a quoted heredoc; never base64-encode it).
   Follow **Prompt adherence** below so the clip matches the user's request.
   Do not ask for a creative brief, character sheet, or storyboard first unless the user asked for one.
2. **Animate a supplied image:** same command plus `--image /abs/path.png --resolution 864x480`
   (the image must already be 864×480; see the storyboard section below).
3. **Longer story (>5.2 s):** plan editorial cuts (1–15 s each) and split each into segments of at
   most 5.2 s. Write the plan in your reply (cut, duration, start frame, action, end state, sound).
   Generate the first segment of each cut from its prompt or approved first-frame image; later
   segments in the same cut use the previous segment's extracted last frame as `--image`.
   Generate one segment at a time and inspect it before the next.
4. **MV / existing song:** use the R2V route (`--mv --reference-image --reference-audio`) as in
   **Mandatory MV workflow** below; never use `--image` for an MV.
5. **Inspect before delivering:** run `ffprobe` (864x480, 24 fps, expected frames, video+audio
   streams) and look at first/middle/last frames. Regenerate a failed take instead of delivering it.
6. **Send the video to the user (mandatory).** After the wrapper prints `>> done: <path>` and the
   check in step 5 passes, put the MP4 in your **final reply** on its own line with the outbox
   marker, using the absolute path from `>> done:`:
   `[[video: /home/chihmin/generated/minimax-h3/<name>.mp4]]`
   PiWeb shows it as a playable card; Piscord uploads it to Discord. Plain paths, Markdown links,
   or `file://` URLs do **not** reach the user. Send every requested deliverable (each clip of a
   multi-clip job, or the assembled final for a long video) in the same reply, plus one line
   with duration/resolution/seed. Never end the job with only "saved to <path>".
7. **On wrapper failure:** report the exact error text and stop. Do not retry with different flags,
   do not work around it through the ComfyUI API, and do not read source code to improvise.
8. If ComfyUI disappears after H3 submission, check the service journal (`journalctl --user -u comfyui -n 50`). Eager eviction purges the 15 GB text encoder automatically; if memory exceeds thresholds due to prior external workloads, restart `comfyui.service` once to reset memory allocator state, then retry the same shot once.

## Mandatory Anima style lock for every anime sequence

Before the character sheet, persist `continuity_bible.style_bible` with one exact
`positive_prompt_prefix`, one exact `negative_prompt`, and fixed line grammar, cel shading,
palette, background rendering, contrast, and color temperature. Also persist
`continuity_bible.generation_lock` with checkpoint, sampler, steps, CFG, and resolution.

For Anima Base production, use the official-model-card baseline `er_sde`, 30 steps, CFG 4.5.
Copy the positive prefix **verbatim at the beginning of every character-sheet and storyboard
prompt**, pass the same negative using `--negative-prompt`, and append only identity and shot-specific
clauses. Never paraphrase the style block between shots. Keep checkpoint, LoRA chain and strengths,
sampler, steps, CFG, and canvas unchanged. Use IP-Adapter for identity and LLLite for structure;
LLLite is not a style lock. See the create-image skill's “Sequence-wide Anima style lock.”

## When to use

### Hard activation rule

Load this skill **only when the user's current request explicitly asks for a generated
moving-image deliverable**. The request must contain a clear creation action plus a video-like
output, such as “生成影片”, “製作動畫”, “做一支 MV”, “create a video”, “make an animation”,
“animate this image”, or an explicit request to use MiniMax/Hailuo H3 to generate video.

Do **not** load or use this skill merely because the request:

- mentions the words video, animation, animate, movie, film, clip, MV, MiniMax H3, or Hailuo H3;
- asks a question about video generation, models, prompting, workflows, or this skill;
- asks to summarize, analyze, transcribe, download, inspect, compare, troubleshoot, or discuss an existing video;
- asks to edit code, documentation, configuration, extensions, or skills related to video;
- includes a video URL or file without explicitly requesting a newly generated moving-image output;
- is ambiguous about whether the desired deliverable is a still image or a video.

For ambiguity, do not activate this skill. Ask whether the user wants a generated video, or use
the more appropriate non-generation skill. Do not infer generation intent from keywords alone.
A prior video-generation request does not carry over automatically to a later request.

Use it when:

- The user explicitly asks for a generated `.mp4` or other moving-image file.
- The user provides a still and explicitly asks to animate it into a video.
- The user explicitly asks to generate an MV, lyric video, short film, or animated clip.
- The user explicitly requests synchronized ambience, SFX, dialogue, or music as part of a newly generated video.
- An explicitly requested longer generated story needs 1–15 second editorial cuts, each split into local H3 generation segments no longer than 5.2 seconds.
- An explicitly requested 2D anime video needs one `/create-image` first-frame storyboard per approved editorial cut;
  later generation segments inside that same cut continue from actual last frames.

## Validated defaults

| Setting | Default |
|---|---:|
| Resolution | 864×480 |
| Frame rate | 24 fps |
| Requested duration | 5 seconds |
| Valid frames | 124 (`17k+5`) |
| Actual duration | about 5.167 seconds |
| Sampler | Turbo v4 step600 EMA |
| Steps | 6 |
| Audio | native 32 kHz stereo, on |
| Typical wall time | about 5m25s |

Use 8 Turbo steps when quality matters more than time. Use the 20-step reference sampler
only for controlled comparisons or a shot that repeatedly fails to reach its endpoint.

## Standard workflow

1. Treat the user's wording as a **creative brief**, even when it is only a vague idea. Preserve
   that wording verbatim, then have the agent expand it into a production treatment before making
   character sheets: explicit requirements, attributed assumptions with confidence, creative
   choices, story/emotional beats, exact-duration Shot Manifest, continuity bible, and audio plan.
   Ask the user only when ambiguity changes the protagonist, ending, core emotion, language,
   safety/rights, or production cost substantially; otherwise make traceable reasonable choices.
2. After character-sheet approval, derive and persist the authoritative editorial Cut Plan. Every
   cut lasts 1–15 seconds and records `scene_id`, duration, a complete `start_frame` description,
   a complete `action` description, and ordered local generation segments.
3. `start_frame` records the scene, all characters and objects, exact pose and expression,
   composition, initial camera/lens, and lighting. `action` records camera movement, scene changes,
   all character and facial actions, complete body motion, temporal progression, exact end state,
   and sound. Review the cut plan yourself before image generation.
4. Split cuts longer than the local model limit into contiguous generation segments at most 5.2
   seconds each. The first segment uses `storyboard`; later segments use `previous_last_frame` and
   stay inside the same editorial cut. Cut durations sum to the target; segment durations sum to
   their parent cut.
5. After the cut plan is reviewed, generate a horizontal `/create-image --output-size 864x480`
   first-frame storyboard for each cut's `start_frame`, then use each segment's action slice as the
   H3 prompt.
6. Reject every style outlier before expensive generation; user approval cannot override a
   failed technical style/continuity gate without explicitly changing the art direction.
7. Give each H3 segment one main character action and one environmental progression.
8. Generate one action-sized segment at a time, using a variable duration no longer than 5.2 seconds.
9. Chain longer stories using motion context when available, otherwise the previous segment's
   actual final frame and optional FL2VA endpoint.
10. Assemble with duplicated-context trimming and a hard join or tiny audiovisual microfade.
11. Validate dimensions, fps, duration, video/audio streams, finite audio, visual continuity,
    and scene evolution before delivery.

## Mandatory MV workflow: storyboard + source-audio R2V

Treat any request to make an **MV, music video, lyric video, or visuals for an existing song** as
`project_type=mv`. Do not use first-frame `--image` FL2VA for an MV and do not ask H3 to invent a
replacement song.

1. Probe the supplied MP3/WAV and set the production target duration from the requested excerpt
   or source duration. Generated audio is reference-only; the final always remuxes the original song.
2. After character approval, design 1–15 second editorial cuts against musical phrases, beats,
   vocal entries, transitions, and payoff—not arbitrary equal lengths. Every cut stores complete
   `start_frame` and `action` data in the written cut plan. Cut durations sum exactly to target duration.
3. Split every editorial cut into local 2–5.2 second R2V generation segments. Every MV segment
   stores `audioStartSeconds`, an action slice, exact end state, and continuation. Segment durations
   sum exactly to the parent cut.
4. After cut-plan review, query and approve one `<Picture 1>` first-frame storyboard per editorial
   cut. Extract the matching `<Audio 1>` source excerpt for every nested generation segment using
   its `audioStartSeconds` and duration; never feed the entire song to each segment.
5. Generate each shot only through R2V with both references. The prompt must explicitly assign
   `<Picture 1>` to visual identity/style/composition and `<Audio 1>` to musical timing, rhythm,
   vocal phrasing, and synchronized action:

```bash
$HOME/.pi/agent/skills/create-video/create_video.sh --mv \
  --reference-image /abs/path/approved-shot-S01.png \
  --reference-audio /abs/path/song-S01.wav \
  --duration 3.75 \
  --prompt "Use <Picture 1> as the visual identity, anime style, costume, scene, and composition reference. Use <Audio 1> as the exact musical timing and rhythm reference; synchronize the described movement and cuts to its beats and vocal accents. <observable shot action and end state>." \
  --output /abs/path/S01.mp4
```

6. Review motion, visual identity, beat synchronization, and cut endpoints per shot. R2V audio is
   conditioning and generated output—not a bit-perfect preservation of the song.
7. After picture edit, replace/mux the generated soundtrack with the original source-audio excerpt
   on the final timeline. Verify sync, duration, no clipping, and no duplicated or missing music at
   joins. The original supplied track is the authoritative final music master.

The local MV route uses `minimax_h3_ref2va_pruned_int8_convrot.safetensors` and
`MiniMaxH3ReferenceToVideo`. In an MV job never use FL2VA/I2VA (`--image`); always pass
`--mv --reference-image --reference-audio`.

### Singing performance and lyric lip-sync

For an existing-song MV in which a visible character must sing, audio reference alone is not
enough. MiniMax's official H3 example explicitly assigns a character to sing with vocals matching
an audio reference, and its full-reference prompt guide requires stable speaker IDs and exact
lyrics inside `<d>` blocks. Use all of the following rules:

1. Use Ref2VA, never ordinary I2VA/FL2VA. Assign `<Picture 1>` to the singer's identity, style,
   costume, and shot composition, and assign `<Audio 1>` to the source-song excerpt's vocal
   timing, lyrics, phonemes, breaths, pauses, sustained notes, rhythm, and beat structure.
2. Define the visible singer as `<Subject 1> (S1)`. State that the subject **physically sings**;
   `dance to the music`, `music synchronization`, or `lip sync` alone may produce beat motion
   without reliable lyric articulation.
3. Preserve the exact source lyrics and original language inside
   `<d>[Language] exact lyric excerpt</d>`. Never translate or invent words. Mark unintelligible
   spans `[unclear]` as required by the official guide.
4. Cut audio on lyric-phrase boundaries, breaths, or instrumental rests. Never cut through a
   syllable or sustained vowel. On this host, prefer one 3–5.2 second phrase per generation.
5. Stage one unobstructed singer in an MCU/CU, front or mild three-quarter view, with the whole
   mouth visible. Avoid hair, hands, props, or microphones crossing the lips; avoid fast head
   turns, profile views, distant framing, multiple singers, rapid cuts, and complex dance motion
   in the same short segment. Use a static view or one gentle camera move.
6. Describe visible articulation and rests: lips begin at the vocal onset, close naturally during
   silence, form readable vowel openings, close for bilabial consonants such as M/B/P, follow
   breaths and jaw motion, sustain the final vowel for the reference duration, and settle closed
   after the phrase. These are observable performance cues, not a guarantee of frame-perfect sync.
7. Treat the H3 output audio as `reference`, not `fully_copy`. H3 jointly generates audio and
   picture and may not preserve the supplied recording bit-for-bit. After picture lock, discard
   the generated track and remux the authoritative original song excerpt.

Extract an accurate local phrase without changing its timing:

```bash
ffmpeg -i /abs/path/song.wav -ss 12.500 -t 3.750 -vn \
  -ar 32000 -ac 2 -c:a pcm_s16le /abs/path/song-S01.wav
```

Use this full-reference prompt pattern:

```text
subject_definitions:
<Subject 1> is the singer shown in <Picture 1>; preserve the exact face, hair, costume,
body proportions, and rendering style.
<Audio 1> is the source-song excerpt and vocal-timing reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> performs the vocal phrase from
<Audio 1>, with facial performance and mouth articulation synchronized to its lyrics,
phonemes, breaths, pauses, rhythm, and sustained notes.

retention_analysis:
<Subject 1>: fully_preserved - preserve identity, costume, face, and visual style.
<Audio 1>: reference - follow its vocal timing, exact lyric content, phrasing, breaths,
pitch contour, rhythm, and beat structure without claiming to copy the signal.

detailed_description:
2D anime music-video style. [Shot 1] A medium close-up frames <Subject 1> from the chest
upward, facing three-quarters toward the view with the mouth fully visible and unobstructed.
<Subject 1> (S1) physically sings the phrase from <Audio 1>:
<d>[Japanese] exact source lyric for this excerpt</d>
The lips articulate each syllable at <Audio 1>'s vocal onset and timing; natural jaw,
cheek, throat, breath, and subtle head motion follow the performance. The lips close during
rests, form readable vowels, close for M/B/P consonants, sustain the final vowel for the same
duration as <Audio 1>, then settle closed. The view makes only a slow small push-in.

overall_soundscape:
No added dialogue; only subtle breath and clothing movement associated with the performance.

non_diegetic_music:
<Audio 1> provides the song timing, vocal phrasing, rhythm, and musical-structure reference.
```

Generate through the local wrapper:

```bash
$HOME/.pi/agent/skills/create-video/create_video.sh --mv \
  --reference-image /abs/path/approved-singer-S01.png \
  --reference-audio /abs/path/song-S01.wav \
  --duration 3.75 --steps 20 \
  --prompt "<the complete full-reference prompt above>" \
  --output /abs/path/S01-generated.mp4
```

If the lead vocal is buried under loud instrumentation, harmony stacks, or heavy reverb, use a
clean lead-vocal stem as the single local audio reference and remux the original full mix later.
Official H3 supports up to three standalone audio references, so an ideal advanced workflow can
assign `<Audio 1>` to the full mix for beat/music structure and `<Audio 2>` to an isolated lead
vocal for phoneme timing. The current local wrapper exposes only one `--reference-audio`; do not
claim dual-audio conditioning until its graph and CLI are extended and tested.

After choosing the approved take, replace its generated audio with the exact original excerpt:

```bash
ffmpeg -i /abs/path/S01-generated.mp4 -i /abs/path/song-S01.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -ar 32000 -shortest \
  /abs/path/S01-original-audio.mp4
```

Lip-sync QC is a hard per-shot gate. Inspect vocal onset, M/B/P lip closures, open vowels, breaths,
rests, sustained final vowels, and the exact end pose at full resolution. Reject mouth motion that
continues during silence, generic open-close flapping, obstructed lips, identity drift, or a phrase
that finishes early/late. H3 is stochastic; regenerate weak takes, and use a dedicated post
lip-sync pass when production requires stricter frame-level alignment than H3 can reliably deliver.

## CLI

> [!IMPORTANT]
> **The only generation command is the wrapper at its absolute path:**
> `$HOME/.pi/agent/skills/create-video/create_video.sh`
>
> - `create_video.sh` is **not on PATH**. A bare `create_video.sh ...` fails with
>   `command not found`. Always type the full `$HOME/.pi/agent/skills/create-video/` prefix,
>   including when copying a command from an earlier example.
> - Do not call `~/src/ComfyUI/scripts/minimax_h3_generate.py` directly for normal work; it is
>   a debugging tool only (see below) and uses different flags.
> - Wrapper duration flag is `--duration` / `-d` (max 5.2). `--seconds`, `--width`,
>   `--height`, `--prefix`, and `--server` are generator-only flags and are **rejected** by the
>   wrapper. Use `--resolution 864x480` instead of width/height.
> - Always pass `--output /absolute/path.mp4`; otherwise the file lands in the current directory
>   with a timestamped name.
> - **The prompt is sent to the model verbatim.** Never base64-encode, URL-encode, or escape it.
>   (2026-10-09: an agent passed `-p "$(... | base64)"` without decoding; H3 received
>   `bGFyZ2UgZXhwbG9zaW9u...` and produced unrelated video. The wrapper now rejects such prompts.)
> - For long, multi-line, quoted, or Chinese prompts, write the plain text to a file with a
>   **quoted** heredoc and pass `--prompt-file` (no shell-quoting problems):
>   ```bash
>   mkdir -p "$HOME/generated/minimax-h3"
>   cat > "$HOME/generated/minimax-h3/shot01.prompt.txt" <<'PROMPT_END'
>   integrated_multimodal_description: [Shot 1] ...
>   overall_soundscape: ...
>   non_diegetic_music: ...
>   PROMPT_END
>   $HOME/.pi/agent/skills/create-video/create_video.sh \
>     --prompt-file "$HOME/generated/minimax-h3/shot01.prompt.txt" --duration 5 \
>     -o "$HOME/generated/minimax-h3/shot01.mp4"
>   ```
> - After launching, read the wrapper's `prompt    :` echo line. It must show your readable
>   English text; if it shows anything else, stop and fix the command.
> - One 5 s Turbo clip takes about **6 minutes** (~355 s measured 2026-10-09). Run it in the
>   foreground with a bash timeout of at least 600 s; do not background it and poll.
> - Success prints `>> done: <output path>`. Deliver it with `[[video: <output path>]]` in the reply after verifying with
>   `ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,nb_frames -of compact <out.mp4>`
>   (expect 864x480, 124 frames, ~5.17 s, one video + one audio stream).
> - **Never bypass the wrapper** by POSTing to ComfyUI `/prompt`, polling `/queue`/`/history`,
>   or using the ComfyUI web frontend. Those paths skip resolution/frame snapping,
>   output copying and audio handling (a hand-made job saving to `/tmp` is rejected by ComfyUI).
> - If the wrapper fails (e.g. `HTTP Error 400: Bad Request` = ComfyUI rejected the graph), do not
>   retry and do not work around it via the API. Report the exact error text to the user and stop;
>   fixing the wrapper/generator is a maintenance task, not part of a generation job.
> - To stop a generation, interrupt the wrapper command; do not send ComfyUI API calls.

Canonical text-to-video (5 s, Turbo, native audio):

```bash
$HOME/.pi/agent/skills/create-video/create_video.sh \
  --duration 5 --seed 2026 \
  -p "integrated_multimodal_description: [Shot 1] ... overall_soundscape: ... non_diegetic_music: ..." \
  -o "$HOME/generated/minimax-h3/shot01.mp4"
```

Canonical image-to-video (approved first frame, same resolution as the video):

```bash
$HOME/.pi/agent/skills/create-video/create_video.sh \
  --image /abs/path/approved-864x480.png --resolution 864x480 --duration 5 \
  -p "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. ..." \
  -o "$HOME/generated/minimax-h3/shot01.mp4"
```

### Put an approved storyboard/reference image into MiniMax H3

The wrapper's `--image` option is the CLI input for an approved storyboard keyframe. It routes
the image to H3 FL2VA as the **exact first frame and geometry anchor**; it is not a loose style
reference. Use one clean horizontal frame generated at **exactly the same resolution as the
planned video**—normally 864×480. A matching aspect ratio alone is not sufficient.

```bash
REF_IMAGE="/absolute/path/to/approved_storyboard_shot01_864x480.png"
OUT="$HOME/generated/minimax-h3/shot01.mp4"

$HOME/.pi/agent/skills/create-video/create_video.sh \
  --model minimax-h3 \
  --image "$REF_IMAGE" \
  --resolution 864x480 \
  --duration 5 \
  --steps 6 \
  --prompt "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. integrated_multimodal_description: [Shot 1] Preserve Picture 1's exact adult character identity, costume, horizontal composition, scene geography, landmarks, eye-level camera, and focal length. The character <one concrete action>. At the same time <one environmental change travels from foreground through mid-ground to background>. By the end <exact character and environment end state>. Traditional hand-drawn 2D cel animation; do not replace the background. overall_soundscape: <continuing ambience and action-linked sounds>. non_diegetic_music: <music development or none>." \
  --output "$OUT"
```

Paths containing spaces are safe when enclosed in double quotes. When creating the storyboard,
set one shared resolution variable and pass the exact same value to both tools:

```bash
VIDEO_RESOLUTION="864x480"
STORYBOARD_DIR="$HOME/generated/minimax-h3/storyboards"
mkdir -p "$STORYBOARD_DIR"

cd "$HOME/models-work/flux2"
source .venv-rocm72/bin/activate
FLUX2_BIG_WMMA_LINEAR=1 python \
  "$HOME/.pi/agent/skills/create-image/scripts/create_image.py" \
  "Horizontal landscape 16:9 full-bleed anime image, not portrait or square. <exact shot design>" \
  --anime --aspect-ratio 16:9 --output-size "$VIDEO_RESOLUTION" \
  --out-dir "$STORYBOARD_DIR" --prefix shot01

# Confirm the returned final_path is exactly 864x480 before using it.
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=s=x:p=0 "/absolute/final_path/from/create-image.png"

$HOME/.pi/agent/skills/create-video/create_video.sh \
  --image "/absolute/final_path/from/create-image.png" \
  --resolution "$VIDEO_RESOLUTION" \
  --prompt "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. <motion, environment, and sound>" \
  --output "$HOME/generated/minimax-h3/shot01.mp4"
```

Do not generate a 1920×1080 storyboard for an 864×480 video and rely on H3 to resize it.
Generate the storyboard at the final video canvas from the start. Use FFmpeg cropping only to
repair legacy or externally supplied images that cannot be regenerated.

Direct ComfyUI generator equivalent, **for debugging the wrapper only** (different flags: `--seconds`/`--width`/`--height`; never use these flags with `create_video.sh`):

```bash
cd "$HOME/src/ComfyUI"
./.venv/bin/python scripts/minimax_h3_generate.py \
  --image "/absolute/path/to/approved_storyboard_shot01_864x480.png" \
  --prompt "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. <observable motion, environment, and sound>" \
  --width 864 --height 480 --seconds 5 --steps 6 --seed 12345 --turbo \
  --prefix "video/storyboard_shot01" --server http://127.0.0.1:8188
```

**Selective storyboard rule:** do not pass several unrelated storyboards into one wrapper call.
An unchanged scene does not require one image per segment. Generate the first clip directly from
its complete prompt, then use clip N's losslessly extracted actual final frame as clip N+1's
`--image`. Generate a new approved storyboard only when the locked policy identifies a major
scene/geography change (or an explicit endpoint). An incompatible angle change should still use
an editorial cut rather than a morph.

### Options

| Flag | Meaning | Default |
|---|---|---:|
| `--model` | Compatibility selector: `minimax-h3`, `minimax`, or `h3` | `minimax-h3` |
| `-p, --prompt` | Observable visual and audio description, plain text (never encoded) | required* |
| `-f, --prompt-file` | Read the plain-text prompt from a file (*use instead of `-p`) | none |
| `-i, --image` | Exact first-frame image for FL2VA; blocked in MV mode | none |
| `--mv` | Use the Ref2VA MV route instead of FL2VA/I2VA | off |
| `--reference-image` | Approved R2V identity/style/composition reference (`<Picture 1>`) | none |
| `--reference-audio` | Source-song or vocal excerpt (`<Audio 1>`); required with `--mv` | none |
| `-d, --duration` | Action-sized duration; variable up to 5.2 seconds | `5` |
| `--fps` | Native fps; must remain 24 | `24` |
| `-a, --aspect` | Aspect ratio when resolution is omitted | `16:9` |
| `-r, --resolution` | Explicit dimensions, snapped to multiples of 32 | `864x480` |
| `--hq` | Use a 576-pixel short side | off |
| `-o, --output` | Output MP4 | timestamped path |
| `--seed` | Random seed | random |
| `--steps` | Denoise steps | Turbo `6`, reference `20` |
| `--turbo` | Turbo v4 sampler | on |
| `--no-turbo` | Reference sampler | off |
| `--audio` | Keep synchronized native stereo audio | on |
| `--no-audio` | Strip audio from final MP4 | off |

## Prompt structure

Use a structured multimodal prompt:

```text
integrated_multimodal_description: [Shot 1] <subject, concrete action, environment,
lighting, viewpoint, focal length, framing, camera movement, temporal progression>.
overall_soundscape: <continuing ambience and synchronized visible SFX>.
non_diegetic_music: <genre, instruments, development, or "none">.
```

For image-to-video, begin with:

```text
For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced.
```

Then specify what moves and changes. Do not redescribe a conflicting identity, costume,
geometry, or viewpoint.

### Prompt adherence — what makes H3 follow the prompt

H3's text encoder (Qwen3-VL) reads full sentences. It follows **concrete, ordered, visible events**
much better than tags or adjectives.

- **Write in English, full sentences, present tense.** Translate the user's Chinese request
  faithfully; keep every subject, action, and key detail they asked for. Do not drop or replace
  the user's subject with a "safer" or more cinematic idea.
- **Keep the three-field structure** (`integrated_multimodal_description` / `overall_soundscape` /
  `non_diegetic_music`). Do not "simplify" into a comma-separated keyword list
  (`explosion, fireball, cinematic, 8k`) — tag lists lose actions and ordering.
- **Lead with the subject and its main action** in the first sentence, then setting, then camera.
  One shot, one dominant action, one environmental change; at 3–5 s, 2–3 timed beats at most.
- **Describe the timeline:** "At first … then … by the end …". State the exact end state.
- **Be literal and visible:** say what the viewer sees (colors, sizes, counts, positions,
  direction of motion), not moods or quality words ("epic", "masterpiece", "best quality").
- **Name the camera once:** shot size, angle, lens (e.g. "wide shot, low angle, 24 mm, slow
  push-in"). Conflicting camera instructions make H3 ignore some of them.
- **Sound follows picture:** list sounds tied to visible events; `non_diegetic_music: none` unless
  music was requested.
- **Duration matches the action:** give 5 s for an event with build-up and aftermath; very short
  clips (≤3 s) compress or skip beats.
- **Keep default sampling:** Turbo 6 steps. Changing steps, seed, or shortening the prompt does
  not fix adherence; rewriting the prompt more concretely does.
- **When the result doesn't match:** first confirm the echoed prompt is the intended text, then
  compare the frames with each sentence, rewrite the sentence that was ignored (more specific,
  earlier in the prompt), and regenerate once. Report to the user what changed.

Example (user: 「一個大爆炸」):

```text
integrated_multimodal_description: [Shot 1] A huge orange fireball explodes in the middle of an
empty concrete warehouse. At first a bright white flash fills the center of the frame; then the
fireball rolls upward and outward, throwing chunks of concrete and sparks toward the camera; by
the end thick black smoke fills the upper half of the frame while small fires burn on the floor.
Wide shot, eye level, 24 mm lens, the camera shakes once at the blast and then holds still.
overall_soundscape: a deep boom at the flash, debris clattering on concrete, crackling fire.
non_diegetic_music: none.
```

## Cinematic Shot Map: angle, focal length, and movement

Before generating storyboards or clips, maintain one shared Shot Map as the source of truth.
Do not invent independent image and video prompts: derive both from the same row.

```text
Shot/beat | duration | shot size | viewpoint angle and height | simulated focal length
framing and depth of field | viewpoint movement | subject movement | start state | end state
environment and light progression | screen direction/continuity | audio | next-shot join
```

### Shot size and viewpoint angle

Use shot size and viewpoint angle as separate controls:

- **EWS/WS/full shot:** geography, full-body action, choreography, and floor contact.
- **MS/MCU:** body language, dialogue, hand actions, and social tension.
- **CU/ECU/insert:** expression, eye line, impact reaction, or decisive prop detail.
- **Eye-level:** neutral human scale. **Low angle:** power or threat. **High angle:**
  vulnerability or overview.
- **Overhead/bird's-eye:** spatial geometry and choreography. **Worm's-eye:** extreme upward
  force, heroic jumps, falling debris, or vertigo.
- **Dutch angle:** instability or impact; state an observable horizon tilt, normally 10–25°,
  instead of merely saying “Dutch angle.”
- **Profile/three-quarter/OTS/POV/reverse:** specify which shoulder or character owns the
  foreground, where the view looks, and the subjects' spatial relationship.

Describe viewpoint geometry in natural language. Avoid the bare word `camera` in image prompts
when a model may render equipment; use `viewpoint`, `view`, or `framing`. Video prompts may use
standard cinematography terms when describing motion.

### Simulated focal-length guide

Millimetres are visual intent for generative models, not guaranteed physical calibration.
Always pair a focal length with visible perspective cues:

| Simulated lens | Use | Observable cues to request |
|---|---|---|
| 14–18 mm ultra-wide | worm's-eye, extreme speed, monumental space | strong near/far scale, enlarged foreground, converging lines, edge stretch |
| 20–24 mm wide | close action, narrow interiors, movement toward view | pronounced depth, foreground energy, readable environment |
| 28–35 mm moderate wide | establishing, full-body combat, tracking | natural wide perspective, character plus geography |
| 40–50 mm normal | dialogue, medium shots, neutral observation | restrained distortion, natural proportions |
| 65–85 mm short telephoto | portrait, emotion, close-up | shallow depth, clean face, separated background |
| 100–135 mm telephoto | standoff, pursuit, surveillance | compressed distance, stacked background planes |
| 200 mm+ long telephoto | remote observation, extreme compression | flattened depth, narrow field of view, strong isolation |
| Fisheye | comic aggression or surreal motion | curved edges and deliberate radial distortion |

Do not choose lens by shot size alone: an 18 mm close-up exaggerates the face, while an 85 mm
close-up flatters and isolates it. For character beauty shots, prefer 50–85 mm. For dynamic
foreshortening, prefer 14–28 mm and explicitly identify the enlarged foreground limb or prop.
Treat 28 mm establishing, 50 mm medium, and 85 mm close views as editorial cuts, not endpoints
to be morphed together.

### Viewpoint-movement grammar

For every moving shot specify **movement type + direction/path + amplitude + speed + subject
relationship + endpoint**:

- `slow push-in from a wide two-shot to a medium close-up, stopping before the face crops`
- `fast side-tracking left-to-right parallel to the runner, keeping the full body centered`
- `low 18 mm viewpoint retreats rapidly as the swordswoman lunges toward it`
- `crane rises three metres into an overhead view, revealing the circular spell pattern`
- `clockwise 120° orbit at constant radius while both fighters remain opposite each other`
- `whip-pan follows the strike and resolves on the opponent's impact pose`

Available movement vocabulary includes static, pan, tilt, push/pull, tracking, side tracking,
arc/orbit, crane/boom, pedestal, handheld, zoom, and dolly zoom. Distinguish viewpoint movement
from subject movement. Avoid stacking more than one dominant viewpoint move and one subject
action in one segment no longer than 5.2 seconds unless deliberately testing a complex shot.

### Continuity checks

Track these across connected shots: identity, wardrobe, prop/weapon hand, eye line, screen
direction, character facing, ground position, scene geography, landmark placement, light
source direction, weather, environmental state, and action phase. Preserve the 180-degree rule
unless a motivated crossing shot visibly re-establishes geography. Every shot must have a new
story function; do not repeat the same pose, distance, and angle without narrative purpose.

For action, preserve readable causality:

```text
anticipation/charge → initiation → contact or evasion → reaction → settle/new threat
```

A single storyboard frame should depict one readable instant, not several moments at once.

## Segmentation and editorial assembly plan

Choose the join before generation; continuity does not mean forcing every clip through the
previous final frame.

| Relationship to next segment | First-frame source | Recommended join |
|---|---|---|
| Same continuous action and viewpoint | previous clip's actual final frame or motion context | remove duplicate context/frame; hard seamless join |
| Same scene, deliberate new angle or focal length | independently approved storyboard | cut-on-action, reaction cut, match cut, or audio J/L cut |
| New scene or time | new storyboard | motivated hard cut, ambience bridge, flash/occlusion if appropriate |
| Fast combat montage | independent 2–3 s shots | impact cut or whip-pan cut |
| Dialogue/emotional scene | independent 4–6 s shots | reaction cut with J/L-cut dialogue or ambience |
| Incompatible existing clips | dedicated bridge only if spatially plausible | otherwise keep an honest editorial cut |

Choose segment duration from the action and dialogue rather than forcing five seconds. Keep each
local generation at or below 5.2 seconds. Split for a major location/geography change or when the
planned action exceeds that limit; camera/viewpoint/action changes inside one continuous scene do
not automatically require an image storyboard. For each segment write:

```text
Segment N — duration/frame count; start state; one dominant action; one dominant viewpoint
move; environment/light progression; sound progression; exact end state; continuity source;
join type and trim/crossfade amount.
```

Assembly rules:

1. Prefer motion-context continuation for a truly continuous shot; otherwise extract the
   previous clip's lossless final frame for chained I2VA/FL2VA.
2. Use a fresh approved storyboard for a genuine cut. Do not let the previous frame lock a new
   angle into a weak morph.
3. Trim duplicated motion-context time or the repeated opening frame before concatenation.
4. Prefer a hard cut. Use only a 0.1–0.25 second audiovisual microfade when needed; never hide
   broken geometry with a long dissolve.
5. Preserve ambience across cuts with J/L cuts, but keep visible impact SFX synchronized.
6. Inspect several frames before and after every join for pose, velocity, screen direction,
   lighting, identity, audio phase, and background continuity.

## MiniMax H3 operational rules

- Source images should match the target aspect ratio. For the tuned path, prepare the approved
  keyframe at exactly 864×480 because it is the first-frame geometry anchor.
- Width and height must be divisible by 32.
- Use native 24 fps.
- Valid frame counts follow `17k+5`: 73 ≈ 3.04 s, 90 ≈ 3.75 s,
  107 ≈ 4.46 s, and 124 ≈ 5.17 s.
- Keep one primary shot/action in each segment. Describe concrete movement rather than
  internal emotion.
- State dialogue, ambience, visible SFX, and music explicitly. Keep dialogue short and quote
  exact words.
- Do not enable global SageAttention; long-sequence backend corruption has been reported.
- Use the validated FP16 video VAE path. Do not force FP32 video VAE. Audio VAE stays FP32.
- This host is UMA. CPU offload does not release physical memory and only adds copies.
- Never stop or shrink `qwen-mtp.service` to make room. H3 is validated while it remains active.

## Videos longer than five seconds

Never force an action longer than 5.2 seconds into one local generation. Choose variable durations
from the actual movement/dialogue beat. For one continuous scene, generate segment 1 directly,
losslessly extract its actual last frame, pass that frame as segment 2's exact first frame, and
repeat. Every segment needs:

```text
Segment N — frame count; start state; character action; environmental progression;
camera/lens; sound development; exact end state; next context source.
```

Keep resolution, fps, identity, scene geography, screen direction, lens logic, and base art
direction coherent across a continuous editorial cut. Every approved cut has one plan-derived
first-frame storyboard, regardless of whether it contains one or several local generations. A cut
longer than 5.2 seconds does **not** need another image for each nested segment: it needs complete
segment action slices and previous-last-frame chaining. An end keyframe remains optional when
FL2VA needs a controlled landing.

### Preferred: latent and audio motion context

When a compatible H3 Motion Context workflow is installed, pass the previous segment's final
video latent and audio context into the next generation. This preserves speed, direction,
pose trajectory, color, ambience, and sound continuity better than decoding a single frame.

- Prefer 22 context frames (about 0.92 seconds), the community node's current tested default.
- Use 39 or 56 only when longer motion history is justified and memory permits.
- Trim the pinned head from picture and audio before concatenation; otherwise context repeats.
- Keep resolution unchanged throughout the chain.
- Continuation prompts must first preserve established movement, composition, environmental
  state, and sound bed, then introduce the next action.
- Trim duplicated context during assembly and inspect the exact join.
- The simple wrapper does not claim to perform latent/audio chaining automatically.

Community workflow: https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context

### Required portable baseline: chained I2VA/FL2VA from the actual last frame

This is the default same-scene path supported by the local wrapper and is also used by community
loop controllers. Extract the final decoded frame to a lossless PNG—not a screenshot or planned
storyboard:

```bash
ffmpeg -sseof -1 -i segment-A.mp4 -an -fps_mode passthrough -update 1 -y segment-A-last.png
```

1. Generate segment A with its action-sized duration.
2. Extract A's actual final frame to PNG using the command above and visually verify it.
3. Use it as segment B's `first_frame`/`--image`.
4. For free continuation, describe forward development. For a planned endpoint, use the next
   approved storyboard as `last_frame` and describe one continuous path toward it.
5. Remove the duplicated opening frame during assembly.
6. Prefer a hard join. If required, use only a 0.1–0.25 second audiovisual microfade.
7. Never use a long dissolve to hide incompatible poses; it produces ghosting.

If independent clips already exist, generate a separate 3–5 second FL2VA bridge from clip A's
actual final frame to clip B's first frame.

### Deliberate shot changes

Do not morph incompatible focal lengths or viewpoints. Use an editorial cut, cut-on-action,
occlusion, petals, flash, or whip-pan. Preserve ambience with an audio J/L cut or tiny
acrossfade. Frame interpolation can smooth cadence within a shot but cannot repair identity,
pose, camera, or scene discontinuity.

## Cut-first 2D anime storyboards with `/create-image`

For 二次元動畫, anime, cel-animation, and hand-drawn requests, use the approved written Cut Plan and
use Anima to generate exactly one first-frame keyframe for every editorial cut. Do not generate
another scene image for nested same-cut continuation segments; the verified white identity sheet
remains mandatory and is not counted as a storyboard.

1. Define exact subject ground position and screen position, body orientation, foot placement,
   action, viewpoint side, viewpoint height, focal length, framing, fixed landmarks, and
   entry/exit movement for every shot.
2. **Generate every cut's stored first frame horizontally and at the exact video resolution.** Produce one
   clean, full-frame **16:9 landscape image per editorial cut** with `/create-image --output-size
   864x480` for the tuned default. If the video uses another canvas, pass that exact `WxH` to
   both `create-image --output-size` and `create_video.sh --resolution`. Never default to
   portrait, vertical, square, panels, or a contact sheet.
3. Begin image prompts with:
   `Horizontal landscape 16:9 full-bleed image, not portrait or square.`
4. Do not put panel numbers, captions, lens labels, camera diagrams, borders, or fake UI into
   image prompts.
5. Use non-native draft generation first. Spend native 1080p time only after art-direction
   approval or when the user explicitly requests a final high-quality still.
6. For hand-drawn style, specify varied ink lines, flat opaque cel colors, hard two-tone
   shadows, and painted gouache/paper backgrounds. Exclude 3D, CGI, glossy rendering, plastic
   skin, bloom, bokeh, volumetric effects, visible camera equipment, text, and watermarks.
7. Establish a character master and scene map. Reuse appearance, palette, screen direction,
   ground markers, and landmarks. Use conservative img2img for adjacent poses and inspect
   identity, hands, feet, clothing, background, and perspective after every generation.
8. Show stills to the user and obtain visual approval before generating video.
9. Use same-composition adjacent keyframes as FL2VA endpoints. Treat 28 mm establishing,
   50 mm medium, and 85 mm close views as deliberate cuts rather than forced morphs.
10. Confirm the `create-image` JSON `final_path` has the exact target dimensions before video
    generation. Do not silently resize a newly generated storyboard afterward; matching pixel
    geometry must be established during storyboard generation.
11. For recurring characters, first approve a dedicated pure-white setting sheet containing
    exactly one neutral, front-facing, full-body depiction per character. Keep characters
    widely spaced; reject turnarounds, repeated views, labels, swatches, scenery, furniture,
    floating props, overlaps, cropped anatomy, and extra people. Every Anima LLLite storyboard
    must use this verified sheet—not a scene frame—as its `--reference`.

Image prompt skeleton:

```text
Horizontal landscape 16:9 full-bleed anime image, not portrait or square.
<adult character design> stands <exact world position> and appears <screen position>.
Body faces <direction>; feet and weight <placement>. Viewpoint is <side and height>,
<focal length>, <shot size>. <Fixed landmarks and screen direction>.
Traditional hand-drawn 2D animation keyframe, varied ink lines, flat cel colors,
hard two-tone shadows, painted paper background. No panels, captions, text, visible
camera, 3D, CGI, glossy rendering, bloom, bokeh, or watermark.
```

## Storyboard style-consistency gate for editorial-cut first frames

Treat the complete set of plan-derived cut first frames as one visual sequence and use a locked
art-direction package plus three review passes. Nested generation segments do not add storyboard
images, but every editorial cut must be present and approved; clip and join QC remain mandatory.

### 1. Lock an art-direction package before drawing shots

Create and preserve these sources of truth:

```text
character master | style key | location key/map | palette and light key | Shot Map | seed/settings ledger
```

- **Character master:** the verified white setting sheet described above. It owns facial
  construction, head/body ratio, hair silhouette, ears/tail, costume seams, accessories,
  footwear, and prop handedness. Traditional animation uses model sheets as authoritative
  references; in this Anima workflow, keep the generation reference to the simpler verified
  single-view white sheet because multi-view sheets have produced duplicates.
- **Style key:** one approved hero frame or tightly cropped style sample defining outer and
  inner line weight, line color, flat-fill behavior, number and hardness of cel-shadow layers,
  highlight treatment, texture, contrast, saturation, and forbidden rendering traits. It is a
  comparison target, not a replacement for the white-sheet `--reference`.
- **Location key/map:** fixed landmarks, horizon, entrances, ground markers, dominant material
  treatment, background edge density/brushwork, and light-source direction.
- **Palette/light key:** named swatches or sampled colors for skin, hair, costume, props,
  background families, shadow hue, highlight hue, and white balance. Story-motivated lighting
  may change, but the rendering grammar must not.
- **Generation ledger:** exact checkpoint, adapter/patch, steps, canvas, prompt style capsule,
  LLLite strength/end-percent, and seed per candidate. Keep the recipe fixed across the batch;
  when repairing a failure, change one variable at a time.

Use this immutable style capsule in every storyboard prompt, with project-specific values:

```text
STYLE LOCK — same facial construction and costume geometry as the verified character master;
<outer-line weight/color>; <inner-line weight>; flat opaque colors; exactly <N> hard-edged
cel-shadow layers; <highlight rule>; <palette/white balance>; <background medium, texture, and
edge density>; <contrast/saturation>. Exclude <3D/CGI, gradients, glossy skin, bloom, unwanted
bokeh, photoreal texture, or other forbidden traits>. Lens and depth of field may change only
as specified by the Shot Map; the drawing and paint system must remain unchanged.
```

Do not depend on prose alone for identity. IP-Adapter/image-prompt conditioning is suited to
appearance and style, while LLLite/ControlNet-style conditioning is suited to pose, framing,
and perspective. When the local hybrid workflow is available, use identity/style conditioning
plus low-strength structural guidance; otherwise use the verified white sheet with conservative
LLLite and reject drift manually. Same seed is not a style guarantee.

### 2. Draw in two passes, then compare as a set

**Pass A — layout blocking:** make inexpensive rough compositions from the Shot Map. Judge only
shot function, silhouette, staging, axis, eyelines, screen direction, geography, action phase,
and cut logic. Do not mistake a rough layout for an H3-ready keyframe.

**Pass B — final color keys:** render one clean 864×480 frame for each editorial shot using the
same character master, style capsule, model recipe, palette/light key, and location map. Generate
adjacent shots as one production batch when practical, but save each as a separate full-frame
PNG. Never ask the image model to draw a multi-panel storyboard.

Then create review artifacts without replacing the originals:

- **Original frames:** required for face, hands, feet, costume, and texture inspection.
- **Pair sheets:** `Shot N | Shot N+1`, same display size, for every intended cut.
- **Page contact sheets:** 4–6 equal-size shots per page in story order for readable comparison.
- **Global thumbnail strip:** the whole sequence in order to reveal palette, contrast, linework,
  background-treatment, and character-proportion outliers.

For more than six shots, use multiple numbered page sheets plus one global strip. Do not shrink
all originals into one unreadable contact sheet. Submit the complete planned set in one
`storyboards` review batch; partial approval does not unlock clip generation.

### 3. Mandatory three-pass visual review

**Gate A — frame-level correctness:** inspect every original at useful scale.

- planned character count; identity, facial geometry, hair/ears/tail, body proportions
- costume construction, accessory/weapon placement and handedness
- hands, feet, anatomy, silhouette, pose, action phase, shot size, viewpoint, focal-length cues
- exact canvas, no text/panels/watermarks, and Shot Map composition

**Gate B — adjacent-pair continuity:** inspect every intended cut as `N → N+1`.

- identity and proportions do not jump
- wardrobe, prop state/hand, injuries, weather, time, and environmental state agree
- action phase advances causally; velocity and screen travel do not reverse accidentally
- eyelines, nose room, facing, landmarks, and 180-degree axis remain legible
- line weight, cel-shadow grammar, palette/temperature, contrast, and background brushwork match
- a focal-length or depth-of-field change reads as intentional cinematography, not a new artist

**Gate C — sequence-wide style:** inspect page sheets and the global strip.

Use a **difference-first protocol** to avoid rubber-stamping attractive images: before setting
any boolean, name the largest visible drawing/paint difference in each adjacent pair and the
single strongest outlier in the global strip. Compare at equal display scale and open originals
for ambiguous details. If the difference is intentional, tie it to a specific Shot Map field;
otherwise fail it. Broadly matching colors or character concept do not excuse a softer face,
rounder proportions, different line grammar, smooth gradient shading, reduced background edge
density, or a painterly-versus-clean-digital rendering change.

- no single frame is softer, glossier, more detailed, more photoreal, more pastel, or differently
  outlined than the established style key
- facial design, costume construction, cel layers, background medium, palette family, contrast,
  saturation, and color temperature form one production
- geography and lighting progression are narratively motivated rather than random regeneration
- every shot adds new story information and the visual rhythm is readable

A storyboard stage may pass only when all planned shots are present and every required check is
explicitly true: `all_planned_shots_present`, `identity_consistent`,
`composition_matches_shot_map`, `line_weight_consistent`, `cel_shading_consistent`,
`palette_temperature_consistent`, `background_rendering_consistent`,
`scene_geography_consistent`, `screen_direction_eyelines_consistent`,
`props_costume_hands_consistent`, `adjacent_cuts_compatible`, and `style_outliers_absent`.
A passing storyboard review must also include written pairwise evidence naming
each compared cut (or `single-shot: not applicable`) and `sequence_style_evidence` describing
the strongest global comparison against the locked style key.

### 4. Failure and repair policy

- Fail closed: one style outlier rejects the storyboard stage; user aesthetic approval alone
  does not make a technically mismatched frame production-ready.
- Regenerate only the failed shot first, using the same locked recipe and a prompt that names
  the observed mismatch. Do not regenerate accepted neighbors unnecessarily.
- If identity fails repeatedly, strengthen identity conditioning or use regional inpainting.
  If pose/perspective fails, adjust LLLite strength or the structural reference. If the whole
  batch drifts, fix the shared style capsule/recipe rather than chasing seeds.
- After replacing any frame, rerun Gate A on it, Gate B on both neighboring cuts, and Gate C on
  the rebuilt sequence sheets. Previous sequence approval is invalidated by replacement.
- Do not average incompatible frames with interpolation, dissolve, or color grading. Grading
  may harmonize small exposure differences but cannot repair facial construction, linework,
  cel shading, costume geometry, or background-medium drift.

This review separates **cinematic variation** from **style drift**: shot size, viewpoint,
focal length, depth of field, and motivated lighting may vary; facial design, costume design,
line grammar, cel-paint logic, palette system, and background rendering must remain locked.

## Animation philosophy: animate the world, not only the character

A successful animation is not a moving character pasted over a frozen illustration. Treat the
character, environment, light, atmosphere, sound, and camera as one causal system. A static
camera means stable framing, not a static world.

1. **Protect invariants; animate variables.** Keep identity, costume, geography, landmarks,
   screen direction, lens, and art direction stable. Deliberately evolve wind, grass,
   branches, clouds, water, crowds, practical lights, shadows, weather, particles, or distant
   activity.
2. **Give the environment an arc.** Every segment needs an environmental beginning,
   progression, and readable ending. The ending becomes the next segment's starting state.
3. **Use visible cause and effect.** A spell sends a light wave across flowers; footsteps
   disturb dust and grass; a door changes interior light. Avoid unrelated decorative motion.
4. **Stage change through depth and time.** Describe when motion reaches foreground,
   mid-ground, background, and landmarks. Use `begins`, `travels`, `one after another`,
   `gradually`, and `settles` rather than listing simultaneous effects.
5. **Keep change legible.** Prefer one dominant environmental transformation plus two or three
   supporting motions. Too many unrelated changes cause geometry replacement and flicker.
6. **Preserve geography during transformation.** Progressively transform the established
   scene; never suddenly replace the background.
7. **Let lighting tell time and emotion.** Cloud shadows, dusk shifts, lanterns, reflections,
   and magic illumination must affect both character and environment consistently.
8. **Make sound undergo the same event.** Continue ambience and add spatial cues in causal
   order. Music may develop with the transformation but must not restart as an unrelated take.
9. **Use stillness intentionally.** Held poses may contrast action, while breathing, cloth,
   light, and atmosphere retain life.
10. **Judge continuity as motion, not matching pixels.** Inspect velocity, direction,
    illumination, sound, and environmental state around every join.

Temporal prompt pattern:

```text
At first <stable character and environmental state>.
Then <character action> causes <dominant environmental event>.
The effect travels from <foreground> through <mid-ground> to <background landmark>.
Meanwhile <two supporting motions> evolve consistently.
By the end <character pose, lighting, environment, and sound settle into next state>.
Preserve <identity, geography, camera, lens, and art style>; do not replace the background.
```

## Deployment and performance

- ComfyUI: `~/src/ComfyUI`
- Service: `~/.config/systemd/user/comfyui.service`
- API: `http://127.0.0.1:8188` — internal to the wrapper only; agents must not call it or open its web UI
- Generator: `~/src/ComfyUI/scripts/minimax_h3_generate.py`
- Diffusion model: `minimax_h3_fl2va_pruned_int8_convrot.safetensors`
- Text encoder: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`
- Video VAE: `minimax_h3_video_vae_fp16.safetensors`
- Audio VAE: `minimax_h3_audio_vae_fp32.safetensors`
- Turbo LoRA: `minimax_h3_turbo_v4_step600_ema.safetensors`

### AMD Strix Halo (gfx1151 / UMA) Memory Architecture & Eager Eviction
On AMD Strix Halo APU systems (128 GB Unified Memory Architecture), MiniMax H3 runs natively with **Zero Swap (0 Bytes)** and **Eager PyTorch Model Lifecycle Eviction**:
1. **Text Encoder Eager Eviction**: The 15.0 GB Qwen3-VL text encoder is eagerly purged from physical memory immediately after generating prompt conditioning in `MiniMaxH3ImageToVideo` / `MiniMaxH3ReferenceToVideo`, recovering 15 GB of memory before the DiT diffusion backbone loads.
2. **Peak Memory Footprint**: Peak memory is reduced from > 55 GB to ~23 GB, allowing MiniMax H3 to safely coexist with a 520k-context `llama-server` without OOM killer triggers or ZRAM swapping contention.
3. **ComfyUI Service Flags**:
   `ExecStart=... main.py --listen 127.0.0.1 --port 8188 --disable-smart-memory --disable-async-offload --disable-pinned-memory --cache-none --reserve-vram 4`
4. **Kernel & Sampling Performance**: Materializes contiguous Q/K/V before SDPA on gfx1151. Standard 6-step Turbo sampling executes in ~246 seconds (41s/step) with total wall time ~370 seconds. Never configure or rely on ZRAM swap, which introduces memory bandwidth contention on the unified LPDDR5X bus.

## Validation before delivery

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels \
  -of json output.mp4
```

Confirm:

- MP4 exists and is non-empty.
- Video is H.264, requested dimensions, and 24 fps.
- Native-audio output contains AAC 32 kHz stereo.
- Decoded audio contains no NaN or Inf.
- Beginning, middle, end, and every segment join are visually inspected.
- Every editorial cut's plan-derived first-frame storyboard passed frame-level, adjacent-pair, and
  sequence-wide review; no unnecessary images were generated for nested same-cut segments.
- Character identity, hands, feet, costume, geography, and screen direction remain coherent.
- The environment visibly evolves rather than behaving like a frozen illustration.
- Sound development matches visible events.
- No long ghosting dissolve hides a broken join.
- `comfyui.service` and protected `qwen-mtp.service` remain healthy.

Then deliver: the final reply contains `[[video: /absolute/path/to/output.mp4]]` on its own
line for every deliverable MP4 (see protocol step 6). The job is not finished until the video is
sent this way.

## References

- MiniMax official H3 launch and audio-matched singing example: https://www.minimax.io/blog/minimax-h3
- Official ComfyUI workflow: https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- Official model repository: https://huggingface.co/Comfy-Org/MiniMax-H3
- Official base prompt guide: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md
- Official full-reference prompt guide: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md
- Practical H3 sound/dialogue/lip-sync guide: https://runware.ai/docs/models/minimax-h3/guides/sound-and-voice
- Community last-frame loop controller: https://github.com/metantonio/comfyui-infinite-minimaxh3-loop
- Community latent AV continuation: https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context
- Community freeze-aware FL2VA chaining: https://github.com/HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite
- Toon Boom character model sheets: https://learn.toonboom.com/modules/character-design/topic/character-model-sheets
- StoryboardArt continuity and 180-degree rule: https://storyboardart.org/storyboard-tutorials/continuity-for-storyboards/
- Learn About Film eyelines and screen direction: https://learnaboutfilm.com/film-language/sequence/180-degree-rule/
- IP-Adapter paper (identity/style image prompting): https://arxiv.org/abs/2308.06721
- ControlNet paper (spatial conditioning): https://arxiv.org/abs/2302.05543
- StoryDiffusion paper (series-level consistency): https://arxiv.org/abs/2405.01434
