---
name: yue2-studio
description: Make and manage songs in the local YuE2 Studio app through its MCP tools (studio_status, generate_song, get_job, list_songs, write_song, playlists, voices, effects). Use when the user asks to create a song, check song progress, or organize their YuE2 library.
---

# YuE2 Studio MCP

Use this MCP when an agent (Claude, Codex, Grok, or another MCP client) needs to work with the running YuE2 Studio desktop app without controlling its window. It speaks to the app's existing local service, and every tool invocation is shown in the Studio **MCP** screen with the agent's name.

## Preconditions

- YuE2 Studio must be open and ready. The local service listens only on `127.0.0.1:7794`. If a tool says Studio is not reachable, launch `YuE2 Studio.exe` from the app folder (the user authorized launching it as needed) and poll `studio_status` until ready. When your song work is done and the queue is idle, call `clear_memory`, then close the window gracefully. Don't close it while any job, including one owned by someone else, is queued or running. Never drive the window's controls; use MCP tools only.
- Start with `studio_status`. Do not queue generation when the model or service reports not ready.
- Songs share one GPU queue with everyone using Studio (the studio PC and browsers on the home network). New songs join the back of the line. `studio_status` returns `queue` with each song's position, owner, and phase. Songs you queue are labelled with your agent name.
- Treat song generation, cancellation, updates, ratings, playlists, profile creation, and effect generation as state-changing actions. Explain the intended action before invoking it when appropriate. Only cancel jobs you queued unless the user asks otherwise.

## Tool guide

- Use `list_songs` before addressing a song, then pass its exact `folder_name` (it may contain spaces and a genre folder, such as `Acoustic bluegrass/Frogs at the Creek`) to `get_song`, `update_song`, or `rate_song`.
- Use `generate_song` to submit a YuE2 generation. It needs a `description` (music style: genre, instruments, mood, vocal type) and, for vocal songs, `lyrics` with section tags such as `[Verse]`, `[Chorus]`, `[Bridge]` on their own lines. It returns a job id. Follow it with `get_job` every 30–60 seconds rather than rapidly. A song takes a few minutes, longer if others are ahead in the queue.
- `generate_song` rejects a title or lyrics that use the Studio lyric ban list (Settings → lyric preferences), reporting each banned word or phrase. Revise with different concrete imagery and resubmit; do not swap in equally formulaic filler.
- `clear_memory` unloads YuE2 from VRAM so another app (image or video generation) can use the GPU. Studio refuses while any song job is queued or running, so confirm the queue is idle first.
- `write_song` uses the app's configured AI-writing provider (set in the app's **Keys** tab) to generate, optimize, title, describe, compose, or translate song text. It does not generate audio. You may instead write the style and lyrics yourself and pass them to `generate_song`.
- `voices` manages or compiles the Studio voice profiles. `effects` lists effects or queues a sound-effect job. `playlists` handles playlist listing and membership.

## Advanced local workflow (MCP 1.1.0)

- `generate_song` accepts native `cot_mode` (`full`, `melody`, `off`), `abc_score`, `voice_slots` (`female`, `male`, `backing` profile IDs), `voice_snapshots`, `lyrics_language`, `english_translation`, `exclude_styles`, `vocal_gender`, `cfg`, `top_k`, `temperature`, and `album`, alongside its original fields. Full plans melody/chords; Melody plans melody; Off skips symbolic planning. ABC requires Full or Melody. Keep title/lyrics original and checked against the live ban list. A clear supplied title avoids optional blank-title writing. Preserve supplied scores; do not promise exact note adherence.
- `get_song` preserves submitted `abc_score` and adds `planned_abc_score` from the saved `score.abc` route. Use that planned score to remix through `generate_song`; no separate score tool is needed. Voice profiles are descriptive musical guidance, not identity cloning or LoRA training. `voices` compile also accepts profile `snapshots`.
- `effects` supports `engine=stable|woosh`, duration, seed, steps, sampler, CFG, chunked decode, and Woosh negative prompts. Stable Audio 3 Small SFX runs on CPU, default 8 steps/pingpong, and ignores negative prompts (the bridge rejects non-empty ones). Woosh uses GPU and unloads YuE2, default 32 steps/DOPRI5; only DOPRI5/Euler and at most 5 seconds are supported. Woosh is CC-BY-NC. With `action=generate` and exact `folder`, create SFX in that song's Studio. `action=add_to_studio` needs `effect_id` and `folder` to add an existing effect.
- `extract_stems(folder, mode="2"|"4")`, `synchronize_lyrics(folder)`, `regenerate_cover(folder, direction?)`, and `transcribe_cover(folder, melody_only?, reuse_cached?)` queue existing installed local features and return jobs. Cover regeneration replaces saved art on success. Cover transcription (SheetSage2, CC-BY-NC) produces ABC; it does not sing a cover. Poll `get_job` before consuming outputs. Missing capabilities fail without installing/downloading anything.
- `studio_mix(action="save"|"bounce", folder, tracks, variant?, selection?, content_end?)` uses complete typed track/clip/effect state. Read `get_song` first for `studio`, `studio_imports`, and `stems`; `song.wav` names the original mix. Supply the full desired track session: Save replaces saved state; Bounce renders the supplied state and saves it. Controls include gain, mute/solo, timing/trims/fades, cuts, effect regions, and clips with source windows and stereo gains. Variant is `custom`, `instrumental`, or `acapella`. A full custom bounce creates another library take; selections or other variants return a mix download. These operations are synchronous, not jobs.
- `export_audio(folder, format="mp3"|"flac")` synchronously creates a tagged export using installed FFmpeg and returns `filename`/`download_url`. It replaces a previous `song.mp3`/`song.flac` export. Download URLs are local service paths, not uploads.
- New generation/job adapters check readiness before mutation. Submit once; after an ambiguous timeout, inspect jobs/library rather than retrying blindly. Visible MCP activity and agent-labelled queue remain in use. No tool changes provider settings, handles credentials, installs models, or performs headless video rendering. Video Studio still needs the browser's canvas/audio capture.

## Visibility and privacy

The MCP records the tool name, outcome, and a non-sensitive summary in the Studio MCP page. It never sends local Studio data outside the machine by itself. API keys remain inside YuE2 Studio's local vault and are never returned by this MCP.

Do not use browser or computer-control tools for normal YuE2 work once this MCP is connected. Use the Studio GUI only to let the user inspect connection status, live activity, generated jobs, and results.
