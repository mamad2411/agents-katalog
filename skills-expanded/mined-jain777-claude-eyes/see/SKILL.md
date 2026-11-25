---
name: see
description: Watch a video (URL or local path) and answer questions about it. Use when the user shares a video URL, asks Claude to look at a video file, or asks about content in a video. Smart scene-aware frame extraction + optional OCR keep token cost low.
argument-hint: "<video-url-or-path> [question]"
allowed-tools: Bash, Read, AskUserQuestion
user-invocable: true
---

# /see — Claude watches a video

You don't have a video input; this skill gives you one. A Python pipeline
downloads the video, picks **interesting** frames (scene changes + minimum
cadence, after perceptual-dedup), optionally OCRs them, and produces a
markdown report you `Read` to see the video. The report lists frame paths +
timestamps + transcript; you Read frames in parallel to view them.

## Step 0 — Silent preflight

Every `/see` run starts with:

```bash
"${CLAUDE_PLUGIN_ROOT}"/scripts/setup.py --check --quiet
```

Exit 0 → proceed silently. **Do NOT announce "setup is complete"** — the
user doesn't need a status message every turn.

On non-zero exit, follow the table:

| Exit | Meaning | Action |
|------|---------|--------|
| `2` | Missing required binaries (`ffmpeg` / `ffprobe` / `yt-dlp`) | Run the installer |
| `3` | No Whisper API key (only matters when the user wants Whisper) | Run installer to scaffold `.env`, then ask user for a key — OR proceed with `--no-whisper` if user passes `--transcript` |
| `4` | Both missing | Run installer first, then handle key |

Installer (idempotent):

```bash
"${CLAUDE_PLUGIN_ROOT}"/scripts/setup.py
```

For exit 3, **also offer** to skip Whisper entirely by passing `--transcript <file>`
on this invocation — many users have their own subtitle file and don't need
Whisper at all.

A `SessionStart` hook runs this preflight once per session, so within a
single session you can skip Step 0 on follow-up `/see` calls.

## When to use

- User pastes a video URL (YouTube, Vimeo, X, TikTok, Twitch clip — anything
  `yt-dlp` supports) and asks about it.
- User points at a local video file (`.mp4`, `.mov`, `.mkv`, `.webm`, etc.)
  and asks about it.
- User types `/claude-eyes:see <url-or-path> [question]`.

## Step 1 — Parse the user input

Split the argument into:
- **source** — first token. URL or path.
- **question** — everything after (may be empty).
- **Embedded flags** — pull `--start`, `--end`, `--transcript`, `--resolution`,
  `--max-frames`, `--profile`, `--ocr`, `--preview`, `--no-whisper`,
  `--no-cache` out of the user input if present.

Examples:
- `https://youtu.be/abc what language is this?` → source = URL, question = "what language is this?"
- `~/screencast.mp4 --transcript ~/sub.srt summarize` → source = path, `--transcript ~/sub.srt`, question = "summarize"
- `~/talk.mp4 --start 2:15 --end 2:45` → source = path, `--start 2:15 --end 2:45`, no question.

## Step 2 — Preview-first heuristic (the big cost saver)

For broad questions about long videos, full-resolution frame extraction is
overkill. Default to a contact-sheet preview first:

**Use `--preview` when ANY of these are true:**
- Video duration > 5 minutes AND no `--start`/`--end` to scope it.
- Question is broad: "what is this about", "summarize", "give me an overview", "is this useful?", "tldr".
- No question at all (user just shared a video).

Skip `--preview` when:
- User asked about a specific moment ("what happens at 2:15", "the intro").
- User passed `--start`/`--end` themselves.
- User asked a precise question that needs continuous frames ("count the cars", "what does the code on line 42 say").

After reading the contact sheet, decide:
- **Enough info?** Answer the user. Mention they can re-run with `--start`/`--end`
  on a section if they want detail.
- **Need detail?** Re-run without `--preview` on the relevant section.

## Step 3 — Run the pipeline

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/see.py" "<source>" [flags]
```

Flag cheat-sheet (all optional):

| Flag | Meaning |
|---|---|
| `--question "…"` | Pass the user's question so the script can auto-toggle `--ocr` when it mentions on-screen text |
| `--transcript PATH` | User-supplied transcript (`.vtt`, `.srt`, `.json`, `.txt`). **Skips both caption fetch and Whisper** — saves API spend and download time. |
| `--profile {auto,tutorial,live}` | Default `auto`. `tutorial` is aggressive about deduping (screencasts); `live` preserves subtle motion (cameras, gameplay). |
| `--start T --end T` | Focus on a section. Accepts `SS`, `MM:SS`, `HH:MM:SS`. |
| `--max-frames N` | Tighter token budget. Default 100. |
| `--resolution W` | Frame width (default 512). Bump to 768/1024 ONLY if text/visual detail needs it AND OCR didn't capture it. |
| `--ocr` | Force-enable Tesseract OCR pass; writes `<frame>.txt` siblings. Auto-on when the user's question mentions text. |
| `--no-whisper` | Disable Whisper fallback. |
| `--whisper {groq,openai}` | Force a Whisper backend. |
| `--preview` | Contact-sheet mode — one image instead of frames. |
| `--no-cache` | Skip cache lookup and don't write cache. |
| `--out-dir DIR` | Specific working directory (default: cache dir or tmp). |

### Cache

By default, re-running `/see` on the same source with the same settings
re-emits the cached report instantly. If the first line of the report is
`[cached]`, that's why. To force a fresh run, pass `--no-cache`.

## Step 4 — Read what the script produced

The script prints a markdown report listing:
- Frame paths under `## Frames` (in chronological order with `t=MM:SS` timestamps).
- Optional `<frame>.txt` OCR siblings (when `--ocr` ran).
- Transcript under `## Transcript` (source labeled: `captions`, `user-supplied`, or `whisper`).

**If OCR ran**, Read the `.txt` files first — they're cheap text. Only Read
the JPEGs when:
- OCR was empty for a frame and the question needs visual context.
- The question is about visual content (faces, objects, motion, colors).

**If no OCR**, Read all frame JPEGs in parallel (one message, multiple Read
calls) so you see them together.

Frame timestamps are **absolute** (real video timeline, even when `--start`
was used).

## Step 5 — Answer the user

You now have:
- **Frames** — what was on screen at each timestamp.
- **OCR text** (if ran) — what's literally readable on screen.
- **Transcript** — what was said at each timestamp.

If the user asked a specific question, answer it directly with timestamp
citations. If they didn't ask, give a structured summary: what the video is
about, key moments, notable visuals, spoken content.

Use `MM:SS` timestamps when citing — they match the report and the user can
seek to them in the original video.

## Step 6 — Cleanup

The report's last line shows the working directory. If caching was on
(the default), the dir IS the cache entry — **don't delete it**, so future
re-runs hit the cache. If you passed `--no-cache` or `--out-dir`, and the
user isn't going to ask follow-ups, `rm -rf <dir>` is fine.

## Failure modes

- **Preflight failed (exit 2/3/4)** → run the installer. For missing API key,
  offer `--transcript` as the alternative before asking the user for a key.
- **`yt-dlp` failed** → its error goes to stderr. If it's login-required or
  region-locked, tell the user plainly. Don't retry.
- **No transcript** (no captions AND (no Whisper key OR --no-whisper) AND no
  --transcript) → script proceeds frames-only. Tell the user, and offer
  `--transcript` for next time.
- **Whisper failed** (rate-limited or invalid key) → printed to stderr.
  Suggest re-running with `--whisper openai` (or `--no-whisper` + manual
  transcript).
- **Long-video warning** → respect it. Offer `--preview` or `--start`/`--end`
  rather than running a sparse full scan.

## Token efficiency

The pipeline's whole point is fewer tokens than a fixed-fps sampler:
- `--preview` = one contact sheet ≈ 1–2 k vision tokens for the whole video.
- `tutorial` profile dedupes static stretches → typically 20–40 frames where
  fixed-fps would emit 60–80 for the same coverage.
- `--ocr` text is near-free; reading 5 text files is cheaper than reading
  one 1024-px frame.
- If you already watched a video this session and the user asks a follow-up,
  **don't re-run** — you have everything in context.

## Security & permissions

- Runs `yt-dlp`, `ffmpeg`, `ffprobe`, and optionally `tesseract` locally.
- Sends extracted audio (mono 16 kHz mp3, ~480 kB/min) to Groq's or OpenAI's
  Whisper API **only** when (a) captions weren't available, (b) `--transcript`
  wasn't provided, and (c) `--no-whisper` wasn't set.
- Reads / creates `~/.config/claude-eyes/.env` (mode `0600`) for API keys.
- Writes downloaded video, frames, audio, transcripts to
  `${CLAUDE_PLUGIN_DATA}/cache/<hash>/` (or tmp if `--no-cache`).
- Never logs or echoes API keys.

Bundled scripts: `scripts/see.py` (orchestrator), `scripts/frames.py` (smart
extractor), `scripts/download.py` (yt-dlp wrapper), `scripts/transcript.py`
(parser), `scripts/whisper.py` (Groq/OpenAI client), `scripts/ocr.py`
(Tesseract wrapper), `scripts/contact.py` (preview), `scripts/cache.py`,
`scripts/setup.py`. Review before first use if you like.
