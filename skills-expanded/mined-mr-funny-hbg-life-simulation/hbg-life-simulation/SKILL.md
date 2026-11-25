---
name: hbg-life-simulation
description: Create Chinese HBG “模拟人生 / 人生副本” narrative videos with a consistent comic IP, a rapid multi-life opening, continuous natural-speed narration, synchronized short captions, dense static manga storyboards, audible fixed-level BGM, alternating zoom/pan motion in HyperFrames, and a consent-gated localhost-only account-backed Images API through CLIProxyAPI as the preferred image channel. Use for 模拟人生、人生副本、统一主角漫画、快闪职业开头、旁白配图、静态漫画分镜、zoom 推拉、左右平移、Edge TTS、字幕压制、本地反代自己的 Codex 账号、CLIProxyAPI，或把长篇中文人生故事组装成视频。
---

# HBG Life Simulation

Build a repeatable Chinese narrative-video pipeline: preserve the story, lock character identity, create an HBG opening, align narration, generate sufficiently dense comic frames, add restrained camera motion, mix audible BGM, and deliver a verified MP4.

## Required skill order

1. Read `/imagegen` before generating or editing raster art.
2. Read `/hyperframes`, then the required HyperFrames domain skills before authoring or rendering.
3. Read `/media-use` for narration, captions, BGM, or SFX.
4. Read `/code-video-visual-qa` before the final visual pass.

## Required project artifacts

Keep these files in every project:

- `SCRIPT_SOURCE.md`: verbatim user copy.
- `PROJECT_SPEC.json`: story-specific title, chapters, corrections, narration settings, opening assets, flash lives, and audio paths; never hard-code these values in builders.
- `SCRIPT.md`: narration-ready copy; record meaningful corrections at the top.
- `CHARACTERS.md`: immutable identity, clothing, age, and relationship rules.
- `STORYBOARD_BASE.json`: semantic beats with narration-relative `cueTime`.
- `STORYBOARD.json`: final global timing and asset paths.
- `PROMPTS.md`: exact ImageGen prompts and call identifiers.
- `HBG_STYLE.json`: single source of truth for orientation, canvas, caption style/safe area, opening motion, approved opening path, and BGM baseline.
- `audio_meta.json`: real durations and opening/body timing.
- `assets/generated/anchors/`: approved identity/style anchors.
- `assets/generated/sheets/`: original generated sheets.
- `assets/generated/scenes/`: split final scene images.
- `qa/`: source snapshots, encoded frames, media probes, and mix previews.

Never silently rewrite plot, viewpoint, tone, ending, or character motivation.

## Workflow

### 0. Select the image channel before project work

Read [references/local-account-api.md](references/local-account-api.md) and [references/image-generation.md](references/image-generation.md). Run this read-only readiness check before initializing a new HBG project:

```bash
scripts/setup_local_cliproxyapi.sh ready
```

Prefer the user's own localhost CLIProxyAPI account channel, but require explicit confirmation for each new project before consuming account capacity. Never treat invoking this Skill as consent to use the account, install software, start the proxy, start OAuth, log in, or repair an account session.

- If the result is `ready`, tell the user a local account API is available and ask whether to use it for this project. Select `local-account-api` only after the user agrees; do not manually open, print, or summarize its protected environment or OAuth files.
- If the result is `not-running`, ask before starting the configured local proxy.
- If the result is `not-configured` or `unhealthy`, explicitly ask whether to initialize or repair CLIProxyAPI with the user's own account. State that CLIProxyAPI is a third-party proxy, the user must complete browser/device login personally, the flow remains subject to account permissions, quotas, and provider terms, and the setup includes a models check plus one image smoke test that consumes account capacity.
- Do not start image generation, run `start`, `install`, `bootstrap`, `login`, or an OAuth-capable installer command until the user clearly agrees in the current conversation. Do not infer consent from the story request or Skill invocation.
- Never ask the user to paste an account password, Cookie, OAuth record, access token, or API key. Never inspect `auths/`, `client.env`, browser storage, cookies, or provider account data.
- After consent, let the user complete OAuth in the browser or device-code page. Run only non-secret readiness/models checks and the disclosed single-image test.
- If the user declines, the account lacks image entitlement, or the local channel cannot be made healthy without further account action, select `built-in-imagegen` and continue.

Use this consent prompt or a concise equivalent:

```text
是否使用你自己的账号在本机初始化 CLIProxyAPI，作为本次人生副本的默认生图接口？

这会安装第三方 CLIProxyAPI，并打开浏览器或显示设备码，由你本人完成登录。Agent 不会读取账号、Cookie、OAuth 文件或密钥。初始化后会检查 models，并生成 1 张测试图验证图片权限；这会消耗你的账户额度，且仍受账户权限、配额和服务条款限制。

是否继续？
```

When the result is already `ready`, use a shorter prompt that still discloses account usage:

```text
检测到你已配置好的本地 CLIProxyAPI。是否使用你自己的账号为本项目生成图片？这会消耗你的账户额度，并仍受账户权限、配额和服务条款限制。
```

Record only the selected channel, consent state, provider label, model, and concurrency in `PROJECT_SPEC.json`. Never record an endpoint, key, OAuth path, token, Cookie, or account identifier.

### Initialize the project style

Before step 1, initialize and read the style system:

```bash
# Default: landscape 16:9, 1920×1080
node scripts/init_project_style.mjs PROJECT_DIR

# Only when the user explicitly asks for portrait / 9:16 / vertical video
node scripts/init_project_style.mjs PROJECT_DIR --orientation portrait
```

If the user does not specify orientation, always use landscape. Portrait is supported but never inferred from short-video subject matter, platform, or a previous project. Read [references/style-system.md](references/style-system.md). Do not author separate HTML and ASS style constants, and never copy raw landscape caption/crop coordinates into portrait or vice versa.

Create `PROJECT_SPEC.json` before running any builder. Read [references/project-spec.md](references/project-spec.md). Story-specific data belongs in this file or the semantic storyboard, not in JavaScript. Run the shared builders from the project directory:

```bash
node SKILL_DIR/scripts/build_script.mjs
node SKILL_DIR/scripts/build_storyboard_base.mjs
node SKILL_DIR/scripts/build_narration.mjs
node SKILL_DIR/scripts/build_composition.mjs
```

### 1. Normalize and estimate

Preserve the source first. Correct only unmistakable transcription errors, broken pronouns, punctuation, or domain terms. Keep second-person narration unless asked otherwise.

Write correction `from` values as the smallest unique source fragment. Do not span optional punctuation or paragraph line breaks when two smaller replacements are safer; source copy often contains transcription-inserted newlines, so long literal replacements create avoidable validation retries.

Estimate duration before generating art. Use 3.4–4.2 Chinese characters per second as an early estimate, then replace estimates with real TTS/VTT timing.

### 2. Lock the visual IP

Read [references/visual-system.md](references/visual-system.md). Derive project-specific identities in `CHARACTERS.md`; never reuse characters from an example story. Generate and approve the required character anchor or anchors before story scenes. Repeat immutable facial traits in every later prompt; never rely on names alone.

### 3. Build the HBG opening

Read [references/opening-system.md](references/opening-system.md). Treat the opening as a fixed module inside the full video, not as the whole skill.

Keep the mandatory order:

1. Narrate only `今天体验的人生副本是……`.
2. Immediately run ratchet SFX and rapid alternate-life flash together.
3. Stop on the selected-life image.
4. Narrate the complete selected-life title while that image remains visible.
5. Start body narration only after the reveal finishes.

Render Chinese titles in HTML, never inside generated images.

After the opening preview is approved, bind its exact path in `audio_meta.opening.previewVideo` or adopt it to the canonical `HBG_STYLE.json` path. Full rendering must fail when that approved file is absent; never silently reuse an older preview or the raw flash/SFX video.

### 4. Generate narration and timing

Default to one continuous full-story Edge TTS asset at `+0%` rate. Keep only the opening lead and selected-life reveal as separate TTS assets. Preserve the VTT and treat it as the master timeline.

Treat line wrapping in `SCRIPT.md` as editorial formatting, not speech direction. Before sending the chapter body to Edge TTS, join wrapped lines without inserting a pause and rely on sentence punctuation for phrasing. Never let a newline divide a word, amount, date, measurement, or sentence. Add missing punctuation such as a colon before a spoken list as a recorded source correction rather than letting a line break imitate punctuation.

Derive scene starts, chapter starts, and captions from real cue times. Never distribute scenes evenly after audio exists.

Burn in short synchronized captions, but preserve complete semantic phrases. Use Chinese word segmentation and punctuation boundaries before considering character count. Landscape captions may normally use 8–18 Chinese characters; portrait normally uses 8–14. A complete short utterance such as `你点头` may remain short, but a split operation must never leave a one-to-five-character suffix such as `起来`, `柜上`, `栗子`, `清楚`, or `一步`. Keep one line where possible and no more than two lines. Remove sentence-ending punctuation when the spoken pause already supplies it. Read the values from `HBG_STYLE.json`; do not duplicate them in a composition builder. Use the orientation-specific caption baseline from [references/style-system.md](references/style-system.md): landscape defaults to 48 px with a 58 px bottom margin at 1920×1080; the validated portrait baseline uses 48 px with a 280 px bottom margin at 1080×1920. In ASS, `BorderStyle=3` requires non-zero box padding/outline; zero makes the encoded background effectively disappear. Keep the complete caption box inside the safe area for the selected orientation.

Run `node scripts/audit_caption_semantics.mjs PROJECT_DIR` after narration generation. Do not build the composition when it reports a short split tail, an undersized generated fragment, or a narration line that ends without sentence punctuation.

### 5. Enforce storyboard density

Read [references/storyboarding.md](references/storyboarding.md). Select semantic beats, then audit every calculated scene duration.

- Target ordinary still duration: 4–8 seconds.
- Allow 8–12 seconds only for a deliberate emotional hold or complex visual reading.
- Split ordinary scenes longer than 12 seconds.
- Treat any scene longer than 16 seconds as a mandatory missing-image defect.
- For an 8–12 minute narration, expect roughly 70–110 stills unless the user explicitly chooses a sparse style.
- For other lengths, size the first storyboard from real TTS duration instead of reusing the 8–12 minute count: start near `ceil(bodyDuration / 6.5)` stills, with a practical range of `bodyDuration / 8` to `bodyDuration / 5`. A 14–15 minute story normally needs about 125–165 stills. Place extra beats proactively inside long explanatory paragraphs, repeated financial details, internal-identity conflict, and denouement passages before generating art.

Add a new still when location, time, dominant action, emotional power, focal object, or memory state changes. Do not hide sparse coverage with an extra-long zoom.

Before building API prompts, write `participants.count` and `participants.allowed` explicitly on every semantic scene. Do not infer participant count later from a keyword heuristic: pronouns such as `他`, `对面`, or `当着他的面` are easy to miss and can turn a two-person action into an incorrect solo frame. Treat missing participant metadata as a planning defect.

### 6. Generate scene art

Use the image channel selected in step 0. Generate strict 2×2 sheets only when four related, low-risk beats share characters and setting. Require equal panels, uniform black gutters, no text, no captions, no speech bubbles, no logos, and no watermark. Generate high-risk frames as standalone images rather than grid panels: hand close-ups, overlapping limbs, phone front/back orientation, typing, smoking, chopsticks, soldering or other tool contact, and identity-critical hero shots. If a grid panel fails one of these checks, regenerate that beat alone; never rescue it by cropping around the defect.

Opening flash sheets must preserve the target orientation at the panel level. For a landscape project, use standalone landscape images or strict 2×2 sheets whose individual panels are landscape; never split a 5×2 landscape sheet into ten portrait cells and then enlarge them with `object-fit: cover`. Resolve every final flash asset to the exact canvas size before composition building: 1920×1080 for landscape or 1080×1920 for portrait. `validate_style_system.mjs` treats a mismatched flash asset as a hard failure.

The user-owned localhost CLIProxyAPI path is the preferred default after the consent and readiness gate in step 0. Built-in ImageGen is the fallback after decline, failed entitlement, or an unavailable local channel. A user-approved CLIProxyAPI localhost endpoint may supply the bundled imagegen CLI path only after `/v1/models` and one disclosed image smoke test pass. Never store an API key in the project, skill, prompt JSONL, shell history file, or report. After the anchor is approved, independent sheets may run concurrently; default to 5 and cap concurrency at 10. Treat one sheet or standalone frame as one generation job. API output must still be displayed visibly in chat, saved project-locally, inspected, and counted.

For API batches, create `assets/generated/prompts/SHEET_MAP.json` before generation. Map every job to final scene IDs in panel order and prove that every storyboard scene is covered exactly once. Generate into a dedicated staging directory. Some compatible providers or CLI versions flatten `out` subdirectories to basenames when `--out-dir` is used; never assume `sheets/g01.png` will remain nested. Resolve staged files by verified basename, reject collisions, then copy sheets and singles into canonical project directories.

Do not trust the requested API size as the delivered pixel size. Probe every output and normalize every final scene to the exact canvas (`1920×1080` landscape or `1080×1920` portrait) before composition building. Split sheets only after confirming four independent panels and uniform gutters.

Every prompt must declare the exact number of visible people and which characters are allowed. Do not paste the entire supporting-character roster into every prompt: models may insert every described character. Add an explicit prohibition such as `No other person may appear` for identity-critical and high-risk frames.

After every call:

1. Show the generated sheet visibly in chat.
2. Save it under `assets/generated/sheets/`.
3. Inspect identity, anatomy, real-world object orientation and use, gutters, and panel order.
4. Split it with `scripts/split_2x2.sh`.
5. Inspect the split images before adding them to the storyboard.

Reject physically impossible anatomy or props even when the image is otherwise attractive. Before judging pose quality, count each visible person's arms, hands, palms, and fingers; confirm every hand belongs to one arm, has the expected number of digits, and remains spatially distinct under overlap. For every hand close-up, inspect the source at 100%: trace each fingertip backward through one palm, one wrist, and one forearm. If overlap makes the number or ownership of hands impossible to prove, reject the frame instead of assuming the anatomy is hidden correctly. A two-hand contact shot must show exactly two wrist-to-palm chains and must not contain a third palm-shaped mass, duplicated finger fan, or finger cluster emerging from beneath another hand. Reject extra, fused, detached, duplicated, ownership-ambiguous, or impossible hands. Phones must have the screen facing the viewer/user, cameras and buttons on plausible sides, fingers wrapping the device naturally without passing through it, and the gaze aligned with the visible screen. Apply the same reality check to cigarettes, chopsticks, bowls, soldering irons, circuit boards, doors, chairs, bedding, tools, and every hand-object contact.

Use separate calls for unrelated settings or identity-sensitive hero frames.

### 7. Animate static frames

Use deterministic linear camera motion and alternate directions:

- zoom in: `scale 1.00 → 1.10–1.13` with slight x/y drift;
- zoom out: `scale 1.12 → 1.00`;
- pan left/right: retain `scale 1.07–1.11`, move no more than 4% of frame width;
- emotional hold: `scale 1.00 → 1.025`;
- use hard cuts for memory fragments and short dissolves only for emotional continuity.

Animate an image child inside a full-bleed clipped wrapper. Never overlap transform tweens on the same element. Keep every image covering the canvas throughout its motion.

### 8. Mix narration, SFX, and BGM

Keep narration, ratchet SFX, BGM, and images on distinct tracks. Default to a constant BGM baseline with no narration-triggered ducking or repeated volume automation.

Create a 15–20 second opening mix preview before rendering the full video. Start with an audible bed around 8–12 dB below narration, then adjust in 3–4 dB steps by ear. Preserve at least 3 dB true-peak headroom in the encoded mix. Use [references/opening-system.md](references/opening-system.md) for the validated HBG example.

### 9. Assemble in HyperFrames

Use one clip per beat or one sub-composition per chapter. Derive clip timing from aligned narration. Use HTML for titles, act labels, and captions. Generate `第一幕`, `第二幕`, and later act labels from the configured chapter count; do not assume exactly ten chapters. Avoid game HUD counters unless explicitly requested.

### 10. Render long videos safely

Read [references/render-and-qa.md](references/render-and-qa.md) before rendering any video longer than four minutes.

1. Run `scripts/preflight_long_render.sh PROJECT_DIR`; keep at least 12 GiB free for a 1080p high-quality 8–12 minute render unless a measured project-specific estimate proves less is safe.
2. Run `node scripts/validate_style_system.mjs PROJECT_DIR`; do not start the long render unless the approved opening, safe caption ratios, flash zoom, and selected-life zoom pass.
3. Run `scripts/render_long_video.sh PROJECT_DIR OUTPUT.mp4`. It enables chunked encoding, raises the FFmpeg timeout, and uses VideoToolbox on macOS by default.
4. If measured HyperFrames capture would materialize the full timeline and exceed safe disk space, validate and use `scripts/render_streaming_ffmpeg.mjs PROJECT_DIR OUTPUT.mp4`. Keep scene timing, motion, captions, chapter labels, opening, and audio mix identical; change only the rendering transport.
5. Always render to a new revisioned filename. Never overwrite the last verified MP4.
6. On `ENOSPC`, stop and inspect exact `renders/work-<renderJobId>-*` or `renders/ffmpeg-work-<output-name>` directories. Delete only abandoned render work directories after confirming no matching render process is alive; preserve source assets and completed MP4 files.
7. On `ffmpegEncodeTimeout`, do not recapture repeatedly with the same settings. Keep chunked encoding enabled, use a supported hardware encoder, and raise `FFMPEG_ENCODE_TIMEOUT_MS`.

### 11. Quality gate

Do not deliver until:

- the anchor and generated sheets are visible in chat;
- every referenced asset is project-local;
- the duration-density audit reports no unexplained scene over 16 seconds;
- `hyperframes check --strict` passes;
- source hero frames and transition midpoints are inspected;
- encoded opening, body transitions, long holds, and final frame are inspected;
- the HTML preview and final ASS caption path both use `HBG_STYLE.json`, and at least one encoded ASS caption frame has a visible background box inside the selected orientation's safe area;
- every visible person has the correct count and ownership of limbs, hands, palms, and fingers, including during overlaps;
- every hand close-up has been opened at full resolution and each fingertip has been traced to exactly one palm, wrist, and forearm; unverifiable occlusion is a rejection, not a pass;
- every important prop is oriented and used plausibly, with special attention to phone front/back direction and hand-object contact;
- resolution, FPS, duration, frame count, audio streams, true peak, and black-frame detection are verified.
- the final encoded MP4, not only source snapshots, has been checked with `scripts/verify_final_video.sh` at the opening, every corrected/high-risk shot, one phone/tool shot, one body transition, and the ending.

Regenerate identity-drifted sheets. Never conceal bad faces or sparse storyboarding with motion blur or speed.

## Reusable helpers

- `scripts/audit_storyboard_density.mjs`: report or gate storyboard holds longer than 12/16 seconds.
- Run the density audit with the JSON path, for example `node scripts/audit_storyboard_density.mjs PROJECT_DIR/STORYBOARD.json`; passing the project directory itself is invalid.
- `scripts/audit_caption_semantics.mjs`: reject semantic split tails, undersized generated caption fragments, and narration lines without terminal punctuation.
- `scripts/build_script.mjs`: turn `SCRIPT_SOURCE.md` plus `PROJECT_SPEC.json` into a corrected, chaptered `SCRIPT.md`.
- `scripts/build_storyboard_base.mjs`: validate and normalize the agent-authored semantic storyboard without embedding story beats in code.
- `scripts/build_narration.mjs`: generate config-driven continuous Edge TTS, captions, audio timing, and final storyboard timing.
- `scripts/build_composition.mjs`: build a config-driven HyperFrames project with dynamic chapters, opening lives, titles, BGM, and orientation layout.
- `scripts/init_project_style.mjs`: create a locked landscape `HBG_STYLE.json` by default, or a portrait one only with `--orientation portrait`, without overwriting an existing project style.
- `scripts/validate_style_system.mjs`: fail fast on wrong opening dimensions/duration, unsafe caption ratios, missing ASS box padding, or absent opening zoom.
- `scripts/split_2x2.sh`: split a generated sheet into four landscape 1920×1080 PNGs by default, or portrait 1080×1920 PNGs when passed `portrait`.
- `scripts/make_contact_sheet.sh`: create a contact sheet for review.
- `scripts/preflight_long_render.sh`: check free disk space and list abandoned render work directories before a long render.
- `scripts/render_long_video.sh`: run revision-safe long-form HyperFrames rendering with chunked encoding and an extended timeout.
- `scripts/render_streaming_ffmpeg.mjs`: low-disk fallback that renders each still to a short zoom/pan segment, concatenates, burns captions, and mixes the final audio without writing every timeline frame.
- `scripts/verify_final_video.sh`: probe the encoded MP4, scan black/silent intervals and loudness, extract named QA frames, and build a contact sheet.
- `scripts/setup_local_cliproxyapi.sh`: check local readiness without exposing secrets, then—with explicit consent—install a checksum-verified CLIProxyAPI release outside projects, bind a user-owned account to localhost, and create a protected OpenAI-compatible client environment for batch work.
