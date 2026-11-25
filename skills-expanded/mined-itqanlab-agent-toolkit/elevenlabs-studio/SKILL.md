---
name: elevenlabs-studio
description: "Voice-over, sound effects, music, transcription, voice changing, noise removal and dubbing with ElevenLabs, on a budget. Triggers: 'make a voice-over', 'read this script aloud', 'generate a sound effect', 'make background music', 'transcribe this with speaker names', 'change the voice in this recording', 'remove the background noise', 'dub this video into Arabic', 'find a voice for this video', 'how many ElevenLabs credits are left', 'elevenlabs'. Every paid call is priced first, never paid for twice, measured after, and written to a ledger in the project. A reserve stops a runaway loop from emptying the month. Needs an ElevenLabs API key, set up once through a guided flow without the key ever being typed into the chat. Works on macOS, Windows and Linux."
license: MIT
compatibility: "Requires Node 18 or newer. Run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Needs network access to the ElevenLabs API and an ElevenLabs account. Generating audio spends that account's credits."
metadata:
  author: itqanlab
  version: 1.2.0
  category: media
  short: "Voice-over, sound effects and music, on a budget"
  starter: "make a voice-over for this script without wasting credits"
---

# ElevenLabs Studio

Voice-over (text to speech), sound effects, music, transcription (speech to text), voice changing, voice isolation and dubbing from ElevenLabs. ElevenLabs is paid by the credit, so every call goes through one script, `scripts/eleven.mjs`, which prices the call before making it, never pays twice for the same request, and writes what each call really cost. Never call the ElevenLabs API any other way from this skill.

## Who you are doing this for

Assume the person asking has never opened a terminal. **You run the commands; they never do.** The one thing they do by hand is create a key on the ElevenLabs website and paste it into a file, so it never passes through the conversation.

Report in plain words: "the voice-over is in `vo/line-03.mp3`, it cost 64 credits, 41,200 are left." Do not make them read JSON. If they are clearly comfortable with a terminal, let them drive.

## Before anything else: check the dependencies

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means Node is missing or older than 18. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for the machine and asks before running it; `--yes` skips the question.

## Connect an account first

```
node scripts/setup.mjs status
```

If ElevenLabs is not connected, run the guided setup and follow what it prints:

```
node scripts/setup.mjs begin
```

It creates an empty credential file and tells the user how to make the key. The key is created at https://elevenlabs.io/app/settings/api-keys with these permissions switched on: **Text to Speech**, **Sound Effects**, **Music**, **Voices (read)** and **User (read)**. For the newer commands also switch on **Speech to Text** (`stt`), **Speech to Speech** (`change`), **Audio Isolation** (`isolate`) and **Dubbing** (`dub`). Only the rows for what the user will do are needed, and a missing one is named when it is first used. User read is what lets the tool read the credit balance. Without it every paid call is refused, because the tool will not spend what it cannot count. If the key form has a History row, set it to Read: that lets the tool measure each voice-over's exact cost.

**Never ask for the key in the conversation, and never display the credential file.** The user pastes the key into the file the script names. When they say they are done:

```
node scripts/setup.mjs finish
```

That checks the key with two free calls, reports the plan and credits left, and records when it was verified. `begin --force` replaces a saved key. The file and its location come from the shared credential convention, `toolkit-credentials`: `<store root>/credentials/elevenlabs.env`, where the store root is `AGENT_TOOLKIT_HOME`, or `.itqan-agent-toolkit` in the user's home folder.

## Commands

Free:

```
node scripts/eleven.mjs account                      plan, credits used and left, reset date
node scripts/eleven.mjs voices [--q calm] [--library] [--lang en] [--previews DIR]
node scripts/eleven.mjs plan --prompt "..." --ms 45000 --out plan.json [--model music_v1]
node scripts/eleven.mjs ledger                       what has been spent, by kind and by tag
node scripts/eleven.mjs check --file take.mp3 --text "the line" [--lang ar] [--dialect eg] [--pitch 100-160]
                                                     pitch in range, every word heard. Exit 5 = redo
```

Paid:

```
node scripts/eleven.mjs tts --voice ID --text "..." --out line.mp3 [--model eleven_v4]
     [--timestamps] [--prev "..."] [--next "..."] [--settings '{"stability":0.5}'] [--lang en] [--format mp3_44100_128]
node scripts/eleven.mjs sfx --text "..." --out hit.mp3 [--duration 2.5] [--influence 0.6] [--loop]
node scripts/eleven.mjs music (--plan plan.json | --prompt "..." --ms 45000) --out bed.mp3 [--model music_v1] [--instrumental]
node scripts/eleven.mjs stt (--file rec.mp3 | --source-url URL --seconds N) --out talk.txt [--lang en] [--diarize] [--keyterms "A,B"] [--clean]
node scripts/eleven.mjs change --voice ID --file take.mp3 --out new.mp3 [--denoise]
node scripts/eleven.mjs isolate --file noisy.mp3 --out clean.mp3
node scripts/eleven.mjs dub (--file video.mp4 | --source-url URL --seconds N) --to es --out es.wav [--from en] [--keyterms "A,B"]
```

`stt`, `change`, `isolate` and `dub` upload a recording. They are priced by its length, which `ffprobe` reads. When there is no `ffprobe`, or the source is a URL, pass `--seconds N`. Without a length the tool refuses: a paid call is never made blind.

Every paid command also takes `--dry` (print the estimate and the request, call nothing), `--max N` (refuse above N credits), `--fresh` (skip the cache, needs `--why`), `--tag NAME`, `--why "..."` and `--out FILE`.

- `voices --previews DIR` saves each voice's sample. Those are static files and cost nothing.
- `tts --timestamps` also writes `<out>.json`: the timing of every character, which is what a picture is cut to.
- `eleven_v4` is the default, as it is ElevenLabs' own. It takes only `stability` and `similarity_boost` in `--settings`; the tool refuses the rest. Direct the delivery with audio tags in the text, such as `[whispers]`.
- `--prev` and `--next` pass the neighbouring lines, so separate takes sound like one read. `eleven_v3` does not support them, so the tool refuses them on that model. On `eleven_v4` they are not yet tested. Stitch with `eleven_multilingual_v2`.
- `eleven_v3` can drift a voice away from its speaker: a male library voice came back female (median pitch 216 Hz, against 106 Hz for the same voice on `eleven_multilingual_v2`). Not yet checked on v4. Check each take with `check`, and use `eleven_multilingual_v2` for a voice that drifts.
- `check` is free and local. It reads the median pitch with ffmpeg, and hears the words with a local transcriber when one is installed beside this skill (`audio-transcribe`) or named in `TRANSCRIBE_CMD`. Otherwise pass `--transcript FILE`. Arabic is compared without diacritics; `--dialect eg` also accepts the Egyptian qaf, said as a glottal stop. Set `--pitch` from the voice's first good take, then hold every later take to it.
- `stt` writes plain text to `--out` and every word with its timing and speaker to `<out>.json`. A free local transcriber costs nothing; prefer it when one is installed and no speaker labels or key terms are needed.
- `change` takes at most 5 minutes per request, and refuses longer input before sending it.
- `dub` waits until the dub is done, which takes minutes. Its output is the dubbed audio track as WAV, not a new video. If it is interrupted, run the same command again: it resumes the same job and does not pay twice.
- `plan` is free according to ElevenLabs' own documentation. It is still measured, like everything else.
- `music` defaults to `music_v1` with `respect_sections_durations: true`. It is the only model that holds each section to its `duration_ms`. The v2 models ignore section lengths, so their music cannot be cut to a picture. Make the plan with the same model you render with, because the plan shape differs.

API detail (models, voice settings, output formats, the plan schema) is in `references/tts.md`, `references/music.md`, `references/sound-effects.md`, `references/speech-to-text.md`, `references/voice-changer.md`, `references/voice-isolator.md` and `references/dubbing.md`. Read them when you need a field, not before. `references/ATTRIBUTION.md` credits the material adapted from ElevenLabs.

## How credits are protected

1. **Cache by request.** The cache key is a hash of the endpoint and the body. The same request returns the file already paid for, at 0 credits. `--fresh` is the only way past it, and it refuses to run without a reason in `--why`.
2. **Estimate before calling.** From a rate table: text to speech about 0.11 credits per character on `eleven_v4` (measured once; the tool estimates 0.15), about 0.45 on `eleven_v3` and `eleven_multilingual_v2` (measured on a Creator plan; published was 1), flash about 0.25 (assumed, not measured), a sound effect about 11.2 per second when `--duration` is set (measured) or about 200 when the model picks the length (published), music about 825 per minute (measured; the published figure was 900), a plan free. Per minute of input audio: voice changer 1000 (published by ElevenLabs), isolator 1000 and transcription 330 (third-party figures, assumed), dubbing 10000 (assumed: reports range from 2000 to 10000, so the tool takes the top). These are estimates, not quotes.
3. **Measure after calling.** Text to speech is measured exactly, from the history item that matches the call's request id (free to read). Other calls fall back to the balance read before and after, which ElevenLabs settles a few seconds late, so the tool polls it for up to about 30 seconds, no faster than every 4 seconds. Back-to-back calls can blur a balance reading; the ledger's `measured_by` says which method was used. A row with `settled: false` was not measured. It does not mean the call was free.
4. **Keep a reserve.** A call that would leave fewer than `ELEVEN_RESERVE` credits (default 1000) is refused. Change it only when the user says so.

The cache and ledger live in `.elevenlabs/` in the folder the command runs from, so each project keeps its own record. `ELEVENLABS_HOME` moves it. `ledger.jsonl` is the record and is worth keeping in version control. `cache/` holds audio: tell the user to add `.elevenlabs/cache/` to `.gitignore`.

## The working order: cheap first

Never buy something you could have heard for free first.

1. **Choose the voice by ear, for free.** `voices --library --q "..." --lang en --previews <dir>`, then listen. Never generate a test sentence to choose a voice.
2. **Fit the script on paper.** Natural narration runs at about 2.6 words per second. If a line cannot fit its window, rewrite it before anything is spoken.
3. **Scratch take with flash** (`--model eleven_flash_v2_5`, half price) and `--timestamps`. It answers one question: does it fit? The timing comes back as data.
4. **Final take, one line at a time.** Use `eleven_multilingual_v2` with `--prev` and `--next` when the lines must sound like one read, or `eleven_v3` without stitching when its range is worth it. Run `check` on each take. Redo a line, never the whole script.
5. **Music: plan first.** Get a plan free from `plan`, or write one. Edit the sections until each one matches a scene, then render once with `music_v1`.
6. **Recordings: clean once, at the right step.** Pass `--denoise` to `change` instead of paying for a separate `isolate`. Transcribe locally for free when no speaker labels are needed.
7. **Dubbing: one minute first.** A dub is the most expensive call here. Dub a short cut first, listen, then the whole thing.
8. **Sound effects: one prompt, one take.** Describe what the moment means, and ask for the exact duration. Setting it is also far cheaper: about 29 credits for 2.6 seconds, against about 200 when the model chooses. Make a second take only after listening to the first.

## Rules

- **Cache first.** Check whether the request was already made before changing a word.
- **`--dry` before any batch,** and show the user the total estimate.
- **`--max N` on anything over 300 credits.**
- **Tag every call** with `--tag` and `--why`. A ledger row with no reason cannot be learned from.
- **Ask before a large spend.** Anything over about 2,000 credits, or 10% of what is left, needs the user's yes first.
- **Disclosure.** Synthesized voice and generated music count as AI-generated material on most social platforms. Tell the user to use each platform's AI disclosure label when they publish it.

## Failure messages

Errors are rewritten for people. A missing key names the file it belongs in. A missing permission names the exact row to switch on, and says the key does not need replacing. An invalid request says nothing was charged. Keep that habit for anything added here.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
