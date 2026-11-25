---
name: audio-transcribe
description: "Turn speech in any audio or video into text, on this machine, free. Triggers: 'transcribe this', 'what does this voice note say', 'read this recording', 'transcript of this meeting', 'make subtitles for this video', 'what is said in this clip', 'transcribe this YouTube video'. Arabic (including Egyptian dialect), English, or detected automatically. Takes a local file, a direct media link, or a YouTube or other site link. Outputs plain text, SRT, VTT or JSON with timings. Runs Whisper locally: no API key, no account, nothing leaves the machine."
license: MIT
compatibility: Runs on macOS and Linux; the script is bash. On Windows use Git Bash or WSL. Requires ffmpeg and a local Whisper engine (mlx-whisper on Apple Silicon, whisper-ctranslate2 or openai-whisper elsewhere), and yt-dlp for site links. Run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check and install them. The first use of a model downloads it once, 0.15 to 3.1 GB, and only after saying so. Needs network access only for links and that first download.
metadata:
  author: itqanlab
  version: "1.0.0"
  category: media
  short: "Transcribe any recording, locally and free"
  starter: "transcribe this voice note and tell me what they want"
---

# audio-transcribe

Speech to text, fully local. Whisper runs on this machine, so it is free and safe for confidential audio: client calls, legal recordings, anything private.

## Who you are doing this for

Assume the person has never opened a terminal. You run the commands. Report the transcript in plain words, and say where any file was written.

## Before anything else: check the dependencies

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means something is missing. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) shows the install commands and asks before running them; `--yes` skips the question. `--with-ytdlp` adds support for site links.

## The command

```
bash scripts/transcribe.sh <source> [--lang ar|en|auto] [--model turbo|large|medium|small|base]
     [--format txt|srt|vtt|json] [--out DIR] [--prompt "names, terms"] [--engine mlx|ctranslate2|openai]
     [--allow-download]
```

| Option | Values | Default |
| :-- | :-- | :-- |
| `--lang` | `ar`, `en`, `auto`, or any Whisper language code | `auto` |
| `--model` | `turbo`, `large`, `medium`, `small`, `base` (on Apple Silicon also an `org/repo` id) | `turbo` |
| `--format` | `txt`, `srt`, `vtt`, `json` | `txt` |
| `--out` | a folder to also write `<source name>.<format>` into | none |
| `--prompt` | names and terms to spell right | none |
| `--engine` | force one engine | the fastest one installed |
| `--allow-download` | allow the first download of a model | off |

`<source>` is a local audio or video file (the audio track is taken from video), a direct media link (`.mp3`, `.m4a`, `.mp4` and so on), or a link to YouTube or any site yt-dlp supports.

The transcript goes to stdout and notes go to stderr. On failure the last line of stdout is `__TRANSCRIBE_FAILED__` and the exit code is non-zero, so a loop over many files can carry on.

## Models and downloads

A model that is not on disk yet is never downloaded silently. The script names its size and stops; ask the user, then re-run with `--allow-download`.

| Model | Download, once | Use it for |
| :-- | :-- | :-- |
| `turbo` | about 1.6 GB | Almost everything, including Egyptian Arabic. Fast |
| `large` | about 3.1 GB | Mumbled, noisy or heavily dialectal audio, when `turbo` reads as nonsense |
| `medium`, `small`, `base` | 1.5, 0.5, 0.15 GB | Slow machines or small disks. Weaker on Arabic |

On an Apple Silicon Mac, a 4 second clip took about 4 seconds on `turbo`, most of it loading the model.

## Language

Pass `--lang ar` or `--lang en` when you know it. `auto` works on clean audio but can guess wrong on short clips or mixed speech, and Arabic mixed with English terms is exactly that case. Whisper writes Egyptian colloquial in Arabic script as spoken; it does not turn it into Modern Standard Arabic.

## Accuracy rules: read before quoting a transcript

1. **Near-silent audio gets invented text.** The script warns when the audio is near-silent. On 3 seconds of silence Whisper still wrote "Thank you." Do not quote it; say the clip was empty.
2. **Repetition loops.** If one phrase repeats over and over, the decoder looped. The script retries once with `large` automatically, and warns if the loop remains.
3. **Names drift.** Brand and personal names, Arabic names most of all, come out misspelled. Pass them with `--prompt`.
4. **A transcript is evidence, not testimony.** For a number, a date, an amount or a commitment, say it came from an automatic transcript and let the user check the audio. Never act on a transcribed figure as if it were confirmed.

## When to use something else

For speaker labels (who said what) or a list of key terms it must spell right, the paid ElevenLabs transcription in the `elevenlabs-studio` skill (`stt`) does both, when that skill is installed. It sends the audio to ElevenLabs and costs credits, so use this skill first unless those features are needed.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
