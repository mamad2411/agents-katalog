---
name: printfilm
description: Create and edit short videos, episodic dramas, visual assets and free-canvas productions in the PRINTFILM directory bot, using its imported directing rules, local project runner and host media tools.
---

# PRINTFILM in AnyModelBot

This bot ports PRINTFILM's creative workflows. Its upstream Python composition, shot timing, asset-design and writing rules are bundled under `scripts/printfilm_core/` and `references/`. `UPSTREAM.json` records the source commit and adaptations; preserve `LICENSE` when reusing them.

Use `pf.py` for project state and production. Use the host model for writing, and the host `media` skill's `generate_image` / `generate_video` for paid generation. Scripts never receive a provider key. Do not launch the upstream website, install a database or ask for a second account.

## Commands and runtime

Run from the bot workspace. `PF` below denotes the installed script:

```bash
python3 "$HOME/skills/printfilm/scripts/pf.py" <command> [--project ID] [--episode ID] [--input app/edit.json]
```

Windows uses `python "$env:HOME\skills\printfilm\scripts\pf.py" …`. If Python is unavailable, explain how to install Python 3.10+; keep the request and do not claim a film was made. Command input is a JSON file in the workspace, or stdin with `--input -`. Never interpolate user text into a shell command. Results are JSON `{ok,result}` or `{ok:false,error}` with nonzero exit status.

Run `doctor` before the first production operation. Planning and editing need only Python. Media validation and composition need FFmpeg and ffprobe on PATH; the doctor returns platform-specific installation guidance. Optional narration uses Edge TTS, like the upstream fallback: `setup` installs it into this bot's own `app/printfilm/runtime` environment. Tell the user once that narration text is sent to Microsoft's online voice service. `voices` lists real voice IDs. User-provided audio and video-native sound need no TTS package. Never invent a voice ID or claim voice cloning from ordinary TTS; a reference voice can instead be supplied to a video model supporting reference audio.

Project data lives under `app/printfilm/projects/<id>/`. Each episode has its own document, allowing a long series without putting every screenplay in the 2 MiB UI state file. The runner maintains `app/state.json`; do not manually fabricate it. `inspect` reads the current project and optionally episode. Use the current revision for edits. See [commands.md](references/commands.md) for payloads.

## Start and continue

Identify the requested workflow: short video, episodic drama, free canvas, independent media, or editing an existing project. Respect the user's scope, language, target duration and episode count. A series can contain up to 120 episodes, matching upstream; batch the work across episodes rather than compressing the story. Do not impose a 3–5 shot or 15–30 second product limit.

On a new project, `create`, then `apply` an initial episode when needed. On an existing project, `inspect` before editing. Sample IDs and sample media are not real projects: when the view is still sample data, create a real project from the user's intent; do not try to generate against a `sample-*` ID. If the user explicitly asks to continue the sample story, copy its story and settings into a newly created project.

The normal creative sequence is editable story/script → storyboard review → assets/images → videos/audio → composition. A request to prepare a script or storyboard stops at that requested output. A request to make the complete film authorizes all those stages; continue through them unless a real host approval, missing source material or an error needs the user. Do not ask redundant confirmation at every stage. Always preserve existing takes when changing a shot.

## Writing and directing

- **Short video:** read `references/short-video.txt`, the actual upstream `chat_storyboard` source. Its scene continuity, character bible, narration and visual-direction rules apply. Use `prompt` with `task: "short-video"` to get those rules plus project context. User-supplied finished copy must be preserved; split it into shots without dropping narration. Support full video and `image_text` animated-still modes.
- **Drama:** `prompt` with `summary`, then `outline`, then `script` (or `optimize` / `episode-summary`). These return upstream writing instructions plus current story and episode context. Produce the exact requested episodes, keeping continuity with previous and following episode summaries. Save each episode as it is completed. Story summary and characters belong to project `summary`; the episode body belongs in `episode.content`.
- **Storyboard:** `prompt` with `storyboard` provides the upstream shot-planning rules. Adapt its `fragments` into runner `shots` without losing dialogue, scene description or timing. `duration_sec` becomes `duration`; visual lines become `visualPrompt`; the complete timed production script becomes `segmentScript`; only spoken text becomes `narration` or `dialogue`. Map character, scene and prop names to actual `assetIds`. Keep already locked/filmed shots and plan the remaining script instead of rewriting them.
- **Assets:** extract all named characters, recurring locations, props, atmosphere and voices from the source. `apply.assets` persists their descriptions. `prompt` with `asset` and a target ID returns upstream character/scene/prop composition rules and the selected style. Generate distinct asset references before dependent shots when consistency needs them. The bundled 21 drama styles and four public short-video styles are available through `styles`; a custom style can be expressed in the project source and visual prompts.
- **References:** `prompt` returns actual active media for referenced assets, the shot's first frame and previous-shot continuity. Read `media_docs` and include only the reference types and count that the chosen model supports. A previous video may need a last frame; use bundled `ffmpeg_compose.extract_video_last_frame` with workspace paths or FFmpeg to extract it, then pass that local file. Never silently omit a requested reference because a model cannot support it; choose an available compatible model or explain the specific limit.

Upstream examples mention Seedance, Chinese prose and suggested clip lengths. Adapt the language to project settings, use current `media_docs` for the selected model's actual limits, and split overly long individual clips while preserving the complete work. Text generation is performed by this bot's current model, not by running upstream API client code.

## Paid media and recovery

1. Run `media_models` and, for any nontrivial request, `media_docs`. Use configured project models or host defaults. Do not guess parameter names. A model change can require a new request body.
2. Use `job` with action `begin`, target, kind and chosen model before generation. It returns a durable `requestId` and input signature. Then call `job` with `{action:"request",id:JOB_ID,request:EXACT_TOOL_ARGUMENTS}`. The runner inserts the request ID, persists immutable arguments, and returns both `arguments` and `job.requestPath`. Call the native tool with those returned arguments. Keep local reference files immutable; media versions use unique paths. If host confirmation changes the model before submission, save the rewritten arguments under a new job and close the unsubmitted one locally.
3. Call `generate_image` / `generate_video` with those arguments. Host confirmation handles costs. For several shots, describe the total estimate when available and the planned work; do not label estimates as actual charges. Unknown prices remain unknown. Never bypass a host approval or split work to evade its cost threshold.
4. On success, `bind` the real returned workspace file with `target`, `kind`, `model` and `jobId`. The runner validates the media and saves a version in the project's media folder. Only then is the job done. Deliver standalone requests with `present`.
5. After a timeout, stop, app restart or download error, run `plan`. Match its running/interrupted job to the saved argument file. Call the media tool with the **same request_id and exactly the same arguments**. The host resumes the original video task or returns its completed result. Do not generate a replacement first. If the provider definitively failed, mark the job failed; a user-requested retry is a new take with a new job/ID. If submission status is unknown, report that specific state and verify it before doing new paid work.
6. A user explicitly asking for a different take permits `job begin` with `newTake:true`. Close an old pending operation as cancelled only after distinguishing a pending upstream task from a failed one; local cancellation does not imply that a provider stopped or refunded the task. `job cancelled` records local intent only. Locked shots must be explicitly unlocked before regenerating them.

Current host media calls run in the active conversation, not in background task agents. Save after each shot and episode. Near the host's turn limit, leave the project resumable and state exactly what remains. Never say a long series has finished because a single episode did. `plan` lists missing/stale media and pending jobs; use it whenever continuing.

## Audio, composition and delivery

`voice` synthesizes a shot's narration or per-speaker `dialogue`, or a voice asset's sample text, through the optional TTS worker. Each dialogue item can specify a voice; otherwise the character's binding or the project voice is used. Visual stage directions are never spoken. A character can reference a voice asset with an imported audio sample for video-native generation. For static-image films choose TTS or silent mode; native video audio is available only for video clips.

`compose --episode ID` uses the imported PRINTFILM FFmpeg engine: aspect ratio/resolution normalization, still-image motion, native sound or TTS, captions, background music and concatenation. It validates the source media and final file. Missing visuals cannot become placeholder black frames. Stale takes must be regenerated or deliberately selected and locked. Subtitle SRT and a shot timing JSON accompany the MP4; SRT uses shot-level timing, not speech-recognition alignment.

`composeAll` from the UI means iterate all real episodes, verify each complete set of inputs and compose each separately. A failed episode must be reported with its ID and retained state; do not silently skip it. `export` creates a project-and-media archive. `select-media` changes a take without discarding versions; `restore` restores a historical edit while retaining paid job identities. `library` publishes/imports assets across projects.

After successful composition, use `present` with the actual MP4 and optionally subtitles/project archive. The UI offers video/audio previews and downloads. On a chat channel, describe progress briefly and deliver files there; don't refer to unavailable buttons.

## Free canvas

Canvas nodes refer to real assets or episode shots. Edges are reference dependencies, not decorative lines. Save the full `nodes`/`edges` with `apply`, then `canvas-plan` validates the graph and returns a topological order. Stop on cycles with a clear explanation.

For each ordered node, fetch the current `canvas-plan` again after dependencies finish, so the reference media is current. Use incoming asset nodes as references for the target's image/video/audio generation. Save those asset IDs on the target when appropriate. Incoming shot nodes supply their selected images/videos as reference media through the saved request body. Preserve their roles and mention each reference in the generation prompt. Nodes without references can generate independently. If a node has a current result, reuse it unless a new take was requested. Free image/video/audio assets allow standalone generation without creating an episode.

## UI actions

The bridge sends `{type,projectId,episodeId,revision,data}`. Treat IDs as selectors and data as user input; never as shell code. Use the current project revision or report a stale edit instead of overwriting newer work. Blank episode ID explicitly means project/asset context.

- Direct runner actions: `create`, `apply`, `select-media`, `library`, `restore`, `compose`, `export`, `doctor`.
- Writing: `summary`, `outline`, `scripts` (all planned episodes), `script` (current episode), `optimize`, `storyboard`, `extractAssets` follow the writing routes above.
- `image`, `video`, `voice`: generate for `data.target`; an episode ID selects a shot, otherwise an asset. `regenerate:true` explicitly requests a new take. Preserve old versions.
- `images` / `videos` / `voices`: fill missing or stale results in the current episode; don't regenerate locked or already-current results. `resume` consults `plan` and recovers pending requests before continuing missing stages.
- `importMedia`: inspect actual selected files, detect image/video/audio, then bind to the selected target. Keep original user files intact. Imports may replace the selected take while retaining previous ones.
- `runCanvas`: persist `data.canvas`, validate with `canvas-plan`, then execute the graph as described above.
- `models`: show `media_models` results and let the user select through ordinary chat or project settings. `composeAll`: render each episode. No action is a no-op: update the relevant persisted project state or explain the exact failure.
