---
name: unflick-subtitles
description: >-
  Generate subtitles for a video locally (whisper.cpp, no cloud) and translate
  them to another language, then load and display them — with the unflick
  player. Use when the user asks to transcribe, caption, subtitle, or translate
  a video's speech. Requires the unflick MCP server (or CLI).
license: MIT
---

# unflick: generate & translate subtitles

unflick transcribes speech to `.srt` **locally** with whisper.cpp (private, no
upload) or via the OpenAI API, and can translate an `.srt` to another language.

## Tools

- `generate_subtitles(video, mode?, whisper?, model?, api_key?, output_dir?)`
  - `mode="local"` (default when a model is available) uses bundled/supplied
    whisper.cpp — fully offline. `mode="api"` uses OpenAI (needs `api_key`).
  - Returns the path of the generated `.srt`.
- `translate_subtitles(srt, target_lang, api_key, output_dir?)` — translate an
  `.srt` (e.g. `target_lang="Chinese"`). Returns the translated `.srt` path.
- `load_subtitle(file)` + `subtitle_select(id)` — display a subtitle track
  (`subtitle_select(0)` disables subtitles). `subtitle_list` shows tracks.

## Flows

- **"Subtitle this video"** → `generate_subtitles(video=…)` →
  `load_subtitle(file=<returned .srt>)` so it shows immediately.
- **"…and translate to Spanish"** → take the generated `.srt` →
  `translate_subtitles(srt=…, target_lang="Spanish", api_key=…)` →
  `load_subtitle` the result.

```bash
unflick subtitle generate movie.mkv            # local whisper -> movie.srt
unflick subtitle translate movie.srt "Chinese" # needs OpenAI key in settings/env
```

## Look for one online first

Transcribing takes minutes; a published subtitle takes seconds. Try
OpenSubtitles before whisper when the file is something that exists in the
world (a film, an episode) rather than the user's own recording.

- `get_subtitles(query?, languages?, file?, load?)` — search and load the best
  match in one step.
- `find_subtitles(…)` / `download_subtitle(file_id)` — when the user should
  pick from the candidates.

```bash
unflick subtitle auto --lang zh-CN,en     # derives the query from what's playing
unflick subtitle search "the matrix" --lang en
```

This needs an OpenSubtitles API key — downloads come out of a personal daily
allowance, so unflick ships no shared key. With none configured the tools say
so and where to get one; pass that on instead of retrying.

## Timing and appearance

- `subtitle_delay(seconds?, relative?)` — omit the value to read it. Positive
  values show subtitles later.
- `subtitle_style_get()` / `subtitle_style_set(name, value)` — `name` ∈ {`scale`,
  `pos`, `color`, `border_size`, `bold`}.

"Subtitles are a second early" is `subtitle_delay(seconds=1)`, not a re-encode.

## Guidance

- Default to **local** mode for privacy; only use `api` mode if the user asks or
  no local model is present.
- Translation currently requires an OpenAI key — if it's missing, ask for it (or
  point the user at `settings_set`) rather than failing silently.
- Report both the generated and translated file paths.
