---
name: whisperx-transcribe
description: Transcribes local audio/video files (meetings, interviews, podcasts, lectures, recorded calls) into a clean, speaker-labeled Markdown transcript using WhisperX, so an LLM can read and reason about a long recording without processing raw audio itself. Use this whenever the user gives you a video/audio file path (mp4, mov, mp3, wav, m4a, etc.) and wants the transcript, notes, summary, action items, or "what did X say" answered from it — even if they don't say "WhisperX" or "transcribe" explicitly, e.g. "here's the recording from our standup, what did we decide", "summarize this interview.mp4", or "pull the quotes about pricing from this call". Also use it proactively when a task involves a meeting/video that's too long to fit in context as-is — transcribe first, then work from the Markdown.
---

# WhisperX Transcription

Turns a video/audio file into a clean Markdown transcript via [WhisperX](https://github.com/m-bain/whisperX)
(Whisper + forced alignment + optional speaker diarization). The point isn't just
"get text out of audio" — it's turning an hour of audio that can't fit in context
into a skimmable Markdown document that can: speaker turns or time-chunked
sections instead of a wall of text, so you (or whoever reads the transcript next)
can jump straight to the part that matters instead of reading it all.

## Before running anything

Run the setup check — WhisperX has real dependencies (ffmpeg, torch, the whisperx
package, optionally a HuggingFace token) and failing 5 minutes into a transcription
because one of them is missing wastes the user's time:

```bash
python3 scripts/check_setup.py            # add --diarize if you plan to diarize
```

If it reports anything missing, stop and either fix it yourself (e.g. `pip install
whisperx`) or tell the user what's needed — don't attempt the transcription anyway.
With `--diarize`, this also verifies the `HF_TOKEN` can actually reach the gated
pyannote model (not just that it's set) — a token whose owner hasn't accepted the
model's user agreement yet fails here instead of 10+ minutes into a diarization run.
Full install/troubleshooting detail is in [references/SETUP.md](references/SETUP.md);
skim it once, especially the note that Apple Silicon Macs must run on CPU (WhisperX's
backend doesn't support MPS), before assuming a Mac will use its GPU.

**The first transcription (ever, or with a new `--model` size) will be slow before
it even starts** — WhisperX downloads the model weights from the internet the first
time that model is used (a few hundred MB for `medium`, multiple GB for `large-v2`/
`large-v3`), and `--diarize` additionally downloads the pyannote diarization models
the first time it's used. This can take several minutes depending on connection
speed and looks like nothing is happening. Tell the user to expect this on a first
run — every run after that reuses the cached weights and starts transcribing
immediately.

## Workflow

### 1. Transcribe

```bash
python3 scripts/transcribe.py /path/to/input.mp4 --model medium --device cpu --compute_type int8
```

This decodes the file with ffmpeg (any audio or video container it supports works —
no separate extraction step needed), transcribes, aligns for accurate word-level
timestamps, and writes `<input-basename>.whisperx.json` next to the input (or
wherever `--output` points). It prints the JSON path on success.

Pick options based on the situation, not just the defaults:

- **`--model`**: see the size guide below — don't reflexively reach for `large-v2`
  on a CPU-only laptop when `medium` will finish in a fraction of the time with
  only a small accuracy tradeoff. This is a time-vs-accuracy tradeoff only the
  user can weigh for their situation (a quick check of a call vs. a transcript
  they'll rely on for quotes) — for anything beyond a short file on a fast
  machine, tell them the expected wait for their file's length and device
  (see the model size guide) and ask which they'd rather have, rather than
  silently picking `medium` and finding out later it wasn't accurate enough,
  or picking `large-v3` and having them wait hours without warning.
- **`--device` / `--compute_type`**: `check_setup.py` tells you which to use.
  `cuda`+`float16` if there's an NVIDIA GPU, otherwise `cpu`+`int8`.
- **`--language`**: pass it if you already know it (e.g. `en`); otherwise WhisperX
  auto-detects from the first ~30s, which is fine for single-language recordings.
- **`--diarize`**: only if the user wants to know *who* said what, or the content
  clearly has multiple speakers (a meeting, an interview) and that distinction
  matters for the task. It requires `HF_TOKEN` (see SETUP.md) and adds real time
  for the pyannote model download + inference — skip it for a single-narrator
  video or lecture where nobody's asking "who said X".
- **`--min-speakers`/`--max-speakers`**: pass these when you know the count (e.g.
  a 1:1 interview is always 2) — it measurably improves diarization accuracy.

### 2. Format into Markdown

```bash
python3 scripts/format_transcript.py /path/to/input.whisperx.json
```

This is the step that actually makes the transcript usable: it collapses WhisperX's
raw segment list into either speaker turns (`### [00:01:23] Speaker 1`) or, when
there's no diarization, time-chunked sections (`## 00:00–00:05`) so a long
recording still has landmarks to skim by. Don't skip this and hand the raw JSON to
whoever needs to read the transcript — it's flat, repetitive, and burns context for
no benefit.

Useful options:

- **`--speaker-names "Alice,Bob"`**: if the user tells you (or it's obvious from
  context) who the diarized speakers actually are, relabel `Speaker 1`/`Speaker 2`
  with real names — much more useful than generic labels.
- **`--chunk-minutes N`**: for a non-diarized transcript, controls how often a new
  `##` section starts. Default 5, which on a long recording can produce large
  paragraphs with no landmarks in between. If the user wants finer-grained
  timestamps instead of (or in addition to) speaker labels, lower this — e.g.
  `1` for a heading roughly every minute, `0.5` for every 30 seconds. Don't
  silently guess a value for this — ask the user what granularity they want
  before running the formatting step, since "well organized" means different
  things depending on how they plan to read/search the transcript.
- **`--title`**: defaults to the filename; set it to something meaningful if you
  know what the recording actually is (e.g. "Q3 Planning Call").
- **`--max-turn-seconds N`**: for a diarized transcript, caps how long one
  speaker's turn can run before it's split into a fresh turn with a new
  timestamp, even if the same person keeps talking. Default 90s. Without this,
  one person talking uninterrupted for several minutes becomes a single giant
  paragraph with only one (increasingly stale) timestamp — the same
  "not well organized" problem `--chunk-minutes` fixes for non-diarized output.

### 3. Use the transcript

Read the resulting `.md` file to answer the user's actual question (summarize,
extract action items, quote a specific part, etc.) instead of re-processing the
audio. If the transcript is still very large relative to what you need, it's
now plain Markdown — grep it, read a specific time range, or ask about a specific
speaker's turns rather than loading the whole thing.

## Batch processing multiple files

For more than a couple of files (e.g. a folder of call recordings), use
`batch_transcribe.py` instead of looping `transcribe.py` + `format_transcript.py`
yourself. It loads the Whisper (and diarization) model **once** and reuses it
across every file, then formats each result to Markdown automatically — one
command instead of 2×N:

```bash
python3 scripts/batch_transcribe.py calls/*.mp3 --model medium --device cpu --compute_type int8
python3 scripts/batch_transcribe.py --input-dir calls --pattern "*.mp3" \
    --diarize --min-speakers 2 --max-speakers 2 --output-dir transcripts
```

- Quote glob patterns (`"calls/*.mp3"`) so the script expands them itself, or pass
  `--input-dir` + `--pattern` for a whole folder.
- `--output-dir` writes all `.whisperx.json`/`.md` outputs there instead of next to
  each input — useful when inputs are scattered across folders.
- `--skip-existing` skips a file if its `.md` already exists, so a batch can be
  safely re-run after a partial failure instead of redoing everything.
- A single bad file doesn't kill the run — it's logged as failed and the batch
  continues; a summary of succeeded/failed/skipped counts prints at the end.
- Same model-size and `--diarize`/`--min-speakers`/`--max-speakers` guidance from
  step 1 applies here — e.g. for a folder of 1:1 call recordings, `--diarize
  --min-speakers 2 --max-speakers 2` is almost always worth the extra time.
- `--speaker-names`/`--max-turn-seconds` from step 2 also work here and apply to
  every file in the batch — only use `--speaker-names` when every file genuinely
  has the same people in the same speaking order (e.g. repeated calls with the
  same two participants), otherwise leave it off and relabel individual files
  afterward if needed.
- If any file is long (over ~60 min) and you're using `large-v2`/`large-v3` on
  CPU, the script logs a per-file warning since that combination can take hours;
  it doesn't block the run, but flag it to the user before kicking off a long
  batch rather than letting them discover it mid-run.
- Wall-clock still scales with total audio length summed across all files — CPU
  transcription doesn't get faster in batch, it just avoids reloading the model
  per file. 20 short calls finish quickly; 20 hour-long recordings still take
  hours in total.

## Model size guide

| Model | Relative speed | Accuracy | When to use |
|---|---|---|---|
| `tiny` / `base` | fastest | rough | Quick check of what's in a file, non-critical content |
| `small` | fast | decent | Long CPU-only recordings where turnaround matters more than perfect wording |
| `medium` | moderate | good | **Default** — solid accuracy/speed balance for meetings and interviews on CPU |
| `large-v2` | slow on CPU, fast on GPU | best, most stable | Anything where accuracy really matters and there's a GPU, or the recording is short |
| `large-v3` | slow on CPU, fast on GPU | highest peak accuracy, occasionally more prone to hallucinating on silence | Same as large-v2; try v2 instead if you see repeated/garbled phrases |

On CPU (which includes every Mac), model size is the main lever on wall-clock time —
a `large-v2` transcription of a 1-hour meeting can take substantially longer than
the recording itself. Default to `medium` unless the user has a GPU or explicitly
wants maximum accuracy and is willing to wait.

## Output format

`format_transcript.py` always emits a short header (duration, language, speaker
count if diarized) followed by the body. Example of the diarized style:

```markdown
# Transcript: Q3 Planning Call
**Duration:** 05:50
**Language:** en
**Speakers:** 2 (Priya, Sam)

### [00:00] Priya
Hey everyone, thanks for joining the call today...

### [00:09] Sam
Sounds good, can you share your screen?
```

And the non-diarized, time-chunked style:

```markdown
# Transcript: Product Update
**Duration:** 10:20
**Language:** en

## 00:00–05:20
Welcome to today's product update. We're going to cover three things...

## 05:20–10:20
Moving on to pricing, we're introducing a new mid tier plan next month...
```
