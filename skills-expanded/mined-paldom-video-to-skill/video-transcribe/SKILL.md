---
name: video-transcribe
description: Fetches a timestamped transcript for a YouTube URL, talk or local video - creator captions, then auto-captions, then local Whisper - with a quality verdict. Use when the user asks to transcribe a video, get its transcript, captions or subtitles, run speech-to-text, or what someone said or actually says in a talk. Not for writing notes, extracting frames, or editing a subtitle file.
license: MIT
argument-hint: <video-url-or-file>
---

# Video transcribe

Gets the most faithful transcript a video can give you, and tells you when that
transcript is not trustworthy. Emits `transcript.json` (millisecond-timed
segments) and `metadata.json`. Everything here is deterministic — no model is
involved in acquisition or in the quality verdict.

## When to use

The user wants the *words*: "transcribe this", "get me the transcript",
"what did they say", "grab the captions".

**When not to:** they want a written-up note or summary (`video-notes`), or
they want images and on-screen text (`video-keyframes`). If they asked for
notes, `video-notes` calls this skill for you — do not run it directly.

## Workflow

### 1. Run the extractor

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/fetch_transcript.py" "<url-or-file>" --out <workdir>
```

Useful flags: `--lang de` (preferred language when the video declares none),
`--asr-model medium` (harder audio), `--no-asr` (fail instead of transcribing),
`--force` (overwrite), `--cookies-from-browser chrome` and `--sleep-requests 2`
(the remedies for a throttled or bot-checked IP — they reach every yt-dlp call).

Create `<workdir>` next to where the user wants the output, and write a
`.gitignore` containing `*` into it on creation so it never dirties their repo.

The script prints a JSON summary and exits non-zero on failure with
`{"error","message","fix"}` on stderr. **Act on `fix` — do not improvise.**

### 2. Read the verdict before using the transcript

The `quality` field is `pass`, `warning`, or `fail`.

| Verdict | What to do |
| --- | --- |
| `pass` | Use it. |
| `warning` | Use it, but repeat the reason codes to the user in your answer. |
| `fail` | Exit code is 1. Do **not** build anything on it — say why and offer a fix. |

Reason codes: `empty_transcript`, `suspiciously_short`, `short_for_duration`,
`low_characters_per_minute`, `highly_repetitive`, `repetitive`,
`very_low_timed_coverage`, `low_timed_coverage`, `large_segment_gap`.

`highly_repetitive` almost always means one of two things: Whisper looped over
silence, or rolling captions were not de-duplicated. Both make the transcript
useless for quoting. Retry with `--asr-model medium`, or report it.

### 3. Report what you got

Tell the user which rung produced the transcript — `manual`, `auto`, or `asr` —
and the language. A manual track is the creator's own text; an `asr` transcript
is a guess. That distinction changes how much they should trust a quote.

## The ladder, and why the order matters

1. **Manual/creator captions.** Real punctuation, casing and speaker labels.
2. **Auto-captions in the video's own language.** Unpunctuated, but time-aligned.
3. **Local ASR** (whisper.cpp with Metal on Apple Silicon, else faster-whisper).

An auto-**translation** is never used. YouTube names them `<target>-<source>`
(`en-de` is "English from German"), and a machine translation of a machine
transcription compounds two error rates. The script resolves the video's own
language first — falling back to the shared source subtag of the translation
list when yt-dlp reports `language: NA`, which is common.

Details and the exact selection rules: [references/caption-ladder.md](references/caption-ladder.md).

## Output

```
<workdir>/
├── transcript.json   # {kind, track, quality:{status,reasons,metrics}, segments:[{start_ms,end_ms,text}]}
└── metadata.json     # {source, video_id, title, channel, url, duration_s, upload_date, language, chapters, ...}
```

Timings are integer milliseconds. Render `HH:MM:SS` for humans; never store
formatted strings as the source of truth, and never compute a timestamp yourself
— use the ones in the file.

## Failure modes

| Symptom | Cause | Response |
| --- | --- | --- |
| `missing_dependency` | no yt-dlp / ffmpeg | run the `fix` command; do not proceed |
| `bot_check` | YouTube served a bot challenge | `yt-dlp -U`, then `--cookies-from-browser chrome`; datacenter IPs have no fix |
| `rate_limited` | HTTP 429 on captions | measured: retries, alternate clients and cookies all fail. Change network or wait hours. ASR still works |
| `restricted` | private/members-only/age-gated | needs browser cookies, or use a local file |
| `no_asr_backend` | no captions and no Whisper | install a backend per the `fix`, or accept no transcript |
| `transcript_quality_fail` | the gate rejected it | report the reason codes; do not build on it |

Two more worth knowing:

- **yt-dlp needs a JS runtime.** Recent versions warn that extraction without
  one is deprecated and some formats go missing. If extraction degrades, install
  `deno`.
- **A zero-byte caption file is not a transcript.** The script deletes empty
  artefacts rather than parsing them into an empty result that looks like success.

## Legal

Downloading from YouTube conflicts with its Terms of Service, and captions may
be copyrighted. This skill is for personal notes on content the user can already
access. Do not use it to republish transcripts wholesale.
