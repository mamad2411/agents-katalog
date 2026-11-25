---
name: apple-native-transcribe
description: Transcribe local audio files on macOS 26 or newer with the `apple-native-transcribe` CLI. Use when a task needs Apple's on-device SpeechAnalyzer and SpeechTranscriber workflow for `.mp3`, `.m4a`, `.wav`, or similar local audio, and the CLI may need to be verified or installed with `brew install mweinbach/max-skills/apple-native-transcribe`. Do not use this skill on Linux, Windows, or macOS versions earlier than 26.
---

# Apple Native Transcribe

Use this skill only on macOS 26 or newer.

## Workflow

1. Confirm the host is macOS and check `sw_vers -productVersion`.
2. Stop immediately if the host is not macOS 26 or newer.
3. Check whether the CLI exists with `command -v apple-native-transcribe`.
4. If the command is missing, install the CLI with `brew install mweinbach/max-skills/apple-native-transcribe`.
5. Run the CLI with an absolute input path, an absolute output directory, and one output format.
6. On success the CLI exits `0` and prints a JSON manifest (with `"ok": true`) to stdout. On failure it exits non-zero and prints `error: ...` to stderr. Check the exit code, then read the manifest from stdout, then inspect the written transcript file if needed.

Do not invent alternate installation paths. The install command for this skill is:

```bash
brew install mweinbach/max-skills/apple-native-transcribe
```

If Homebrew is unavailable or the install fails, stop and report that clearly.

## Primary Commands

Use flag arguments:

```bash
apple-native-transcribe --input "/abs/path/audio.mp3" --output-dir "/abs/path/out" --format json
```

Use positional arguments:

```bash
apple-native-transcribe "/abs/path/audio.mp3" "/abs/path/out" json
```

List supported locales:

```bash
apple-native-transcribe --list-locales
```

Supported formats:

- `json` — a structured transcript: a full `transcript` string plus `segments` carrying per-segment timing (`startSeconds`/`endSeconds`), word-level `spans`, and `alternatives`. Use this when a tool or model will consume the transcript or needs timestamps.
- `text` — the raw plain-text transcript only.
- `srt` — timed subtitle output.

## Output Contract

On a successful run the CLI always:

- writes the requested transcript file into the output directory as `transcript.<ext>` (`transcript.json`, `transcript.txt`, or `transcript.srt`)
- writes `transcript.debug.json` beside it — a debug artifact with run metadata (asset status, preset, locale) and the full segment data; ignore it unless diagnosing a problem
- prints a JSON manifest to stdout

The written files always use the fixed names above; the manifest's `transcriptFile`/`debugFile` give their absolute paths.

The manifest includes:

- `ok` (boolean success flag)
- `inputFile`
- `outputDirectory`
- `transcriptFile`
- `debugFile`
- `format`
- `localeIdentifier`
- `segmentCount` and `finalSegmentCount`

Prefer `json` when another tool or model will consume the transcript or needs timestamps. Prefer `text` when a human needs the plain transcript, and `srt` for subtitles.

## Debug Flags

Only use debug flags when the default flow is insufficient:

- `--debug-locale <locale-id>`
- `--debug-install-assets`
- `--debug-prewarm`
- `--debug-preset <transcription|alternatives|timeIndexed|progressive|timeIndexedProgressive>`
- `--debug-context <phrase>`

If the CLI reports `Speech assets for locale '<id>' are not installed`, re-run the same command with `--debug-install-assets` added; it downloads the assets when needed and is otherwise a safe no-op. Note that the assets are not always reliably registered between runs, so this error can recur even after a prior successful install — just add the flag again. The first asset download for a locale can take a while.
