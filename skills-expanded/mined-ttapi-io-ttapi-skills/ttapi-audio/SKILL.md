---
name: ttapi-audio
description: Generate music, songs, instrumental BGM and lyrics through TTAPI using Suno or FlowMusic; retrieve and save results, extend or cover completed tracks, and separate stems. Use for TTAPI audio requests including 生成音乐、写歌、纯音乐、背景音乐、续写歌曲、翻唱、分离人声. Requires a TTAPI API key.
---

# TTAPI Audio

Use TTAPI's existing music APIs to deliver a playable audio file or the requested lyrics. This skill calls a paid hosted API; installing the skill is free. Generation and editing consume the user's TTAPI quota. Read [current audio pricing](https://docs.ttapi.io/grids/en/start/pricing/audio) when quoting costs. Suno `max_mode: true` doubles quota consumption.

## Choose the workflow

- **Suno**: songs with custom lyrics, instrumental BGM, continuation, covers and stem extraction. Read [Suno](references/suno.md) for mode-specific inputs and track IDs.
- **FlowMusic**: prompt-to-music or lyrics-to-music with Lyria models, lyrics writing, continuation, covers, stems, URL audio import and format export. Read [FlowMusic](references/flowmusic.md).
- Preserve a requested model or service. For an unspecified general music request, start with one Suno generation using `chirp-v6`; use FlowMusic when the user asks for Lyria or exactly one clip.

## Run

Requires Node.js and `TTAPI_API_KEY` in the environment inherited by the agent. It is sent as the `TT-API-KEY` header to `https://api.ttapi.io`. Obtain a key in the [TTAPI dashboard](https://dashboard.ttapi.io). Do not ask the user to paste a secret in chat or place it in committed input files.

Resolve this skill's directory before running its bundled `scripts/ttapi.mjs`. Commands below run from that directory. Put generated media in the user's requested project or output directory, preferably using an absolute output path.

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema suno-generate
node scripts/ttapi.mjs submit suno-generate --input examples/suno-generate.json --dry-run
node scripts/ttapi.mjs submit suno-generate --input examples/suno-generate.json --wait --output ./outputs
```

Use an input JSON file based on the operation's schema and the user's brief. For covers, extension and stems, replace the sample ID with a completed track's real `musicId` or `clip_id`; sample IDs and example.com audio URLs are documentation values.

The user asking for generation authorizes that requested paid operation. Proceed within the requested number of outputs and existing budget; do not add another approval question. A preview, explanation or dry run does not authorize generation. Do not expand a one-track request into a batch or add follow-up paid edits without an instruction to do so.

## Finish and recover

1. On an asynchronous submission, retain the operation and `jobId` immediately. A submit response with `status: SUCCESS` and only `data.jobId` means accepted, not finished.
2. Poll the same task until terminal success or failure. `ON_QUEUE` means work is pending or running; FlowMusic also uses `PENDING_QUEUE`. Do not start another paid generation to check progress.
3. Download output audio using `--output`. Keep the response JSON and return the saved file path, model and task ID. If the user asked for lyrics, return `data.lyrics` directly and save text when requested.
4. After a timeout or interrupted wait, resume the same job:

```sh
node scripts/ttapi.mjs get suno-generate --task SAVED_JOB_ID --wait --output ./outputs
node scripts/ttapi.mjs get flowmusic-generate --task SAVED_JOB_ID --wait --output ./outputs
```

Do not automatically resubmit an uncertain POST after a network timeout: the server may already have accepted it. Check saved responses or the dashboard first. If an accepted task fails, report the returned error; a retry creates another generation. Authentication or insufficient quota errors require a corrected key or account state, not repeated requests.

FlowMusic lyrics normally return their text synchronously. If that endpoint instead returns a queue status and a task ID, use `get flowmusic-lyrics --task ID` to query the shared FlowMusic fetch endpoint; do not report missing lyrics as completed. A retrieved lyrics task may place its text in `data.clips[].lyrics_timing_markers` rather than inline `data.lyrics`; read the raw response.

## Scope

This release wraps the operations listed by `models`. It does not synthesize local audio, mix videos, upload local files automatically, or expose every Suno endpoint. For a missing advanced operation, consult the [official docs index](https://docs.ttapi.io/llms.txt) and endpoint schema before constructing a request. Do not infer parameter names across model families.
