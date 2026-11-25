---
name: audio-narrate
description: "Turn text into natural English or Arabic narration for free, as one file or one file per video scene. Triggers: 'read this aloud', 'make a narration for this script', 'voice-over for this video, free', 'text to speech in Arabic', 'one audio file per scene', 'narrate this offline', 'record an Arabic voice-over for this'. Online neural voices by default (edge-tts), Piper when there is no internet, a pronunciation list for words the voice says wrong, and language detected per line. No key, no sign-up, no cost."
license: MIT
compatibility: "Runs on macOS and Linux with bash; Windows has setup.ps1 and run.ps1, not yet tested. Needs Python 3 (or uv) and ffmpeg. scripts/setup.sh creates a Python environment of about 155 MB outside the skill folder, and --piper downloads two offline voices of about 126 MB. The default engine needs internet; Piper works offline."
metadata:
  author: itqanlab
  version: "1.0.0"
  category: media
  short: "Free English and Arabic narration from text"
  starter: "narrate this script in Arabic, one file per scene"
---

# audio-narrate

Text in, spoken audio out. English and Arabic (Modern Standard), free, no key.

Two engines share one Python environment:

| Engine | Script | When | Quality |
| :-- | :-- | :-- | :-- |
| edge-tts | `scripts/edge.py` | Default. Needs internet | Natural neural voices, clearly best for Arabic |
| Piper | `scripts/tts.py` | No internet, or edge is refusing | Offline and fast, more robotic |

When the `elevenlabs-studio` skill is installed and the user wants studio quality, a cloned voice, or exact timing per character, that is the paid option. Say what it costs before suggesting it. This skill costs nothing.

## Who you are doing this for

Assume the person has never opened a terminal. You run the commands. Report in plain words: "the narration is in `vo/intro.mp3`, 14 seconds, made with the Arabic male voice."

## First: setup

```
bash scripts/setup.sh --check
```

Exit 0 means ready. Otherwise:

```
bash scripts/setup.sh            # the Python environment with both engines, about 155 MB
bash scripts/setup.sh --piper    # also the two offline voices, about 126 MB. Only when offline is needed
```

Say the size before downloading. On Windows use `.\scripts\setup.ps1` (`-Check`, `-Piper`). Everything goes in one folder outside the skill: `AUDIO_NARRATE_HOME`, or `audio-narrate` inside the toolkit folder (`AGENT_TOOLKIT_HOME`, by default `.itqan-agent-toolkit` in the user's home). `bash scripts/setup.sh --where` prints the Python it uses.

ffmpeg is required. `--check` prints the install command for the machine.

## Commands

Run either engine through `scripts/run.sh` (Windows: `scripts/run.ps1`), which finds the right Python:

```
bash scripts/run.sh edge --text "Welcome to the tour." --out intro.mp3
bash scripts/run.sh edge --text "مرحبا بكم في الجولة." --female --out intro_ar.mp3
bash scripts/run.sh edge --input script.json --out narration.mp3
bash scripts/run.sh edge --input script.json --per-segment scenes/ --out scene.mp3
bash scripts/run.sh piper --text "No internet needed." --out offline.wav
```

`script.json` is a list of lines: `[{"lang":"ar","text":"..."},{"lang":"en","text":"..."},{"text":"language detected"}]`. A `.txt` input is split on blank lines. `--per-segment DIR` writes one file per line, named `001_ar.mp3`, `002_en.mp3` and so on, which is what a video cuts to.

edge options: `--female`, `--voice <any edge voice id>`, `--lang auto|en|ar`, `--rate +0%`, `--pitch +0Hz`, `--volume +0%`, `--gap-between 350` (ms between lines), `--lexicon FILE`, `--no-lexicon`.

Piper options: `--lang auto|en|ar`, `--ar-speed 0.72`, `--en-speed 1.0`, `--sentence-gap 250`, `--comma-gap 110`, `--gap-between 350`.

The output format follows the `--out` extension: mp3, wav or m4a.

## Voices

| Language | Male (default) | Female (`--female`) | Piper |
| :-- | :-- | :-- | :-- |
| Arabic (MSA) | `ar-JO-TaimNeural` | `ar-SA-ZariyahNeural` | `ar_JO-kareem-medium` |
| English | `en-US-GuyNeural` | `en-US-AriaNeural` | `en_US-amy-medium` |

Any other edge voice works with `--voice`. To list them: run the environment's `edge-tts --list-voices`.

## Pronunciation fixes

edge reads loanwords, brand names and tech terms badly, and its free endpoint ignores SSML. The fix is to respell the text before it is spoken. The tool applies, in order, later winning:

1. `lexicon.json` in this skill, the built-in list (empty buckets to start)
2. `narrate-lexicon.json` in the folder the command runs from: the project's own words
3. `--lexicon FILE`

```json
{ "ar": { "لاب": "لَاابْ" }, "en": { "SQL": "sequel" } }
```

Longer keys win, so a phrase beats a single word. For Arabic, these work: explicit tashkeel (a fatha), madd or an extra alif to lengthen a vowel, a sukun to end a consonant crisply, and a comma for a pause. Piper does not use the lexicon.

## Working order

1. Write numbers and abbreviations the way they should be heard.
2. Make one line first and listen to it. Fix words with the lexicon, not by rewording the script.
3. For video, use `--per-segment` and cut each scene to its file.
4. Offline or edge refusing: use Piper, and tell the user the quality is lower.

## Failure messages

- **"Microsoft's voice service refused the request"**: the free edge endpoint is unofficial and changes without notice. Nothing is wrong with the text. Use Piper for now, and try edge again later.
- **"path too long for espeak-ng"**: Piper's espeak cannot read a data path over about 160 characters. Point `AUDIO_NARRATE_HOME` at a shorter folder and run setup again.
- **"Piper voice missing"**: run `bash scripts/setup.sh --piper`.

## Licences and disclosure

edge-tts uses Microsoft's free read-aloud service. Its terms for commercial use are unclear, so flag that before high-stakes commercial work. Piper and its two voices are free to use. Do not swap in XTTS-v2 or models built on it (such as EGTTS) for commercial work: their weights are non-commercial, and no commercial licence can be bought.

Synthesized voice counts as AI-generated material on most platforms. Tell the user to use each platform's AI label when they publish.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
