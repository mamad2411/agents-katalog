---
name: hyllo-cli
description: Transcribe local audio or video files into text with the Hyllo CLI. Use when Codex needs to do speech recognition, create transcripts, extract subtitles, convert recordings to markdown text, or process local media files with Hyllo APP running on the user's machine.
---

# Hyllo CLI

Use `hyllo-cli` to run local speech recognition through the Hyllo APP.

Follow this workflow:

1. Check that Hyllo APP is available with `hyllo-cli status`.
2. If needed, inspect available models with `hyllo-cli models`.
3. Before every transcription, confirm the spoken language with the user. Offer short explicit options so the user can reply by choosing one directly. Do not run `transcribe` until the user has explicitly confirmed the language.
4. Run one transcription command.
5. Monitor stdout until the command finishes or the user asks to stop.
6. Read or summarize the generated markdown file for the user if needed.

## Language confirmation is required

Before running any transcription command, confirm the spoken language with the user.

When asking, prefer a short options-based prompt so the user can answer with a single choice. For example:

```text
Which primary language should I use for transcription?
1. English (`en`)
2. Chinese (`zh`)
3. Cantonese (`yue`)
4. Japanese (`ja`)
5. Korean (`ko`)
```

You may tailor the options to the file or likely languages, but keep the list short and include the language code when useful.

Rules:

- Never run `hyllo-cli transcribe` without first confirming the language.
- Even if the language seems obvious from the file name, prior context, or the user's region, still ask unless the user already explicitly provided the language in the current request.
- Treat an explicit language in the current request as confirmation.
- If the user gives an ambiguous description such as "mostly Chinese", "bilingual", or "mixed English and Chinese", ask a brief follow-up with options to determine the best `--lang` value.
- If the audio may contain multiple languages, ask which primary language should be used for transcription.
- If the user does not know, offer a short options list with a recommended guess if helpful, but still wait for approval before proceeding.
- If the interface supports structured choices, use them. Otherwise present the options in plain text and let the user reply with the number, label, or language code.

## Verify availability

Run:

```bash
hyllo-cli status
```

Treat output like `Hyllo server is running` as healthy.

If the command fails or reports that the server is unavailable, tell the user to start Hyllo APP or log in before retrying.

## Inspect models

Run:

```bash
hyllo-cli models
```

Do not hard-code the model list. Read the current output because installed models can change. The current CLI may show numeric model IDs and supported languages for each model.

Choose a model from the real output:

- Prefer the fast general-purpose Chinese and mixed-language model for `zh`, `yue`, `ja`, or `ko` unless the user requests another model.
- Prefer `Parakeet` for English and many European languages when available.
- If the user already specified a model, pass it through exactly as requested.

## Transcribe media

Run:

```bash
hyllo-cli transcribe --model_id <model_id> --lang <language_code> --output <output_path> <audio_file>
```

Arguments:

- `<audio_file>`: local media file path.
- `--model_id`: model ID from `hyllo-cli models`.
- `--lang`: language code for the spoken audio.
- `--output`: markdown output path.

Supported input formats depend on the local Hyllo installation, but common audio and video formats such as `wav`, `mp3`, `m4a`, `mp4`, and `flac` are expected to work.

If the user does not provide an output path, write the transcript to a file `{audio_file_name}.md` in the current directory unless the surrounding task needs another location.

## Monitor progress

The transcription command is synchronous and can take time on long recordings.

Watch stdout for progress logs such as:

```text
Recognizing...
10:03:00 Recognized 30%...
10:03:22 Recognized 60%...
10:03:45 Recognized 90%...
10:03:59 Recognized 100%...
```

Do not start multiple transcription commands at the same time.

If the user asks to stop, interrupt the running process immediately. Expect no transcript file to be saved when interrupted.

## Failure handling

- If `status` fails: ask the user to open Hyllo APP or log in.
- If `models` output does not include the requested language: tell the user to install a suitable model through Hyllo APP before retrying.
- If transcription fails: report the CLI error briefly and keep the original media file untouched.

