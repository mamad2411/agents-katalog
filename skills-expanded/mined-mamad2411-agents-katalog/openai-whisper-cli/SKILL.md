---
name: openai-whisper-cli
description: 'Command-line usage for OpenAI Whisper, focusing on audio transcription, translation, and specifying models or languages. You MUST load this skill when interacting with the whisper command.'
license: MIT
---

# openai-whisper-cli

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Transcribing audio files into English or other languages using `whisper`.
- Translating non-English speech into English using `whisper --task translate`.
- Selecting specific Whisper models (e.g., `turbo`, `medium`, `large`) for speed vs accuracy tradeoffs.
- Specifying the source language for transcription using `--language`.

## WHEN NOT TO USE

- Using OpenAI Whisper from within Python scripts (this skill focuses purely on CLI usage).
- API integrations with OpenAI's hosted Whisper endpoints (this is for local execution).

## Core Process

1. **Model Selection**: Determine the right model. The default is `turbo`, which is fast and good for English transcription but *not* for translation. For translating non-English to English, use `medium` or `large`.
2. **Language Specification**: If the audio is not in English, it is often helpful to specify the language with `--language`.
3. **Task Definition**: Use `--task translate` if you need the output in English from a non-English audio file.
4. **Execution**: Run the `whisper` command with the appropriate flags and input audio file.

## Command-Line Examples

- **Basic Transcription (Default `turbo` model, good for English):**

  ```bash
  whisper audio.flac audio.mp3 audio.wav --model turbo
  ```

- **Transcribe non-English speech (e.g., Japanese):**

  ```bash
  whisper japanese.wav --language Japanese
  ```

- **Translate non-English speech into English:**

  ```bash
  whisper japanese.wav --model medium --language Japanese --task translate
  ```

  *(Note: The `turbo` model will return the original language even if `--task translate` is specified. Use `medium` or `large` for best translation results).*

## Core Principles

- **Model Capabilities**: The `turbo` model is optimized for transcription speed but degrades for translation. Always switch to `medium` or `large` when the goal is translation to English.
- **Multilingual vs English-only**: `.en` models (like `base.en`, `small.en`) tend to perform better for English-only tasks. Without `.en` (like `base`, `small`), the model is multilingual.

## Common Pitfalls

- **Using `turbo` for Translation**: Pitfall: Using `whisper --model turbo --task translate`. Prevention: The `turbo` model is not trained for translation tasks. Switch to `--model medium` or `--model large`.
- **Missing Dependencies**: Pitfall: `whisper` fails to run due to missing `ffmpeg` or Rust. Prevention: Ensure `ffmpeg` is installed via system package manager (e.g., `apt install ffmpeg`, `brew install ffmpeg`).

## References

- [OpenAI Whisper Repository](https://github.com/openai/whisper)
- [OpenAI Whisper Discussions](https://github.com/openai/whisper/discussions)
  USE FOR: searching issues or answers to questions.
- [OpenAI Whisper Pull Requests](https://github.com/openai/whisper/pulls)
  USE FOR: searching issues or features.
