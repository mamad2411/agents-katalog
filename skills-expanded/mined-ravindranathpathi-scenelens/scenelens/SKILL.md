---
name: scenelens
description: Watch a video (URL or local path). Picks frames at scene changes, OCRs each frame so on-screen text is read as text not pixels, pulls a timestamped transcript (captions or Whisper, auto-chunked for long audio), and hands it all to Claude.
argument-hint: "<video-url-or-path> [question]"
allowed-tools: Bash, Read, AskUserQuestion
homepage: https://github.com/ravindranathpathi/scenelens
repository: https://github.com/ravindranathpathi/scenelens
author: Ravindranath Pathi
license: MIT
user-invocable: true
---

# /scenelens — Claude watches a video, smarter

You don't have a video input; this skill gives you one. Compared to a fixed-fps frame grab, scenelens:

1. **Picks frames at scene changes** — content-aware sampling instead of time-uniform sampling. Same frame budget, far better signal.
2. **Runs OCR on every frame** — on-screen text (slides, code, terminals, dashboards) is extracted as text alongside the image, so you don't burn vision tokens reading static pixels.
3. **Auto-chunks long audio** — Whisper's 25 MB cap no longer fails outright on long videos.

A Python script does all of this and prints a markdown report. You then `Read` each frame path to see the images and combine them with OCR + transcript to answer the user.

## Step 0 — Setup preflight (silent on success)

**Python interpreter:** every `python3 ...` command in this skill is for macOS/Linux. On **Windows**, substitute `python` — `python3` on Windows is the Microsoft Store stub and won't run the script.

Before every `/scenelens` call, verify dependencies and an API key are in place:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" --check
```

This is a <100 ms lookup. On exit 0, the script emits **nothing** — proceed to Step 1 silently. **Do NOT announce "setup is complete"** — that's spam.

On non-zero exit:

| Exit | Meaning | Action |
|------|---------|--------|
| `2` | Missing required binaries (ffmpeg / ffprobe / yt-dlp) | Run installer |
| `3` | No Whisper API key | Run installer to scaffold `.env`, then ask user for a key |
| `4` | Both missing | Run installer, then ask for a key |

The installer is idempotent:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py"
```

On macOS with Homebrew, it auto-installs `ffmpeg`, `yt-dlp`, and (optionally) `tesseract`. On Linux/Windows, it prints exact install commands.

**Tesseract is optional.** Without it, the OCR pass is silently skipped — frames are still extracted, transcript still pulled. The skill works; it just loses the OCR sidechannel. The installer prints the install command for tesseract on each platform.

**If an API key is still missing after install:** use `AskUserQuestion` to ask whether the user has a Groq API key (preferred — cheaper, faster) or an OpenAI key, then write it into `~/.config/scenelens/.env` on the matching `GROQ_API_KEY=...` or `OPENAI_API_KEY=...` line. If they don't want Whisper, proceed with `--no-whisper` and tell them captions-less videos come back frames-only.

**Structured mode:** `python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" --json` emits `{status, first_run, missing_binaries, missing_optional, ocr_available, whisper_backend, has_api_key, config_file, platform}`.

Within a single session, skip Step 0 on follow-up calls — once `--check` returned 0, nothing has changed.

## When to use

- User pastes a video URL (YouTube, Vimeo, X, TikTok, Twitch clip, anything yt-dlp supports) and asks about it.
- User points at a local video file (`.mp4`, `.mov`, `.mkv`, `.webm`, etc.) and asks about it.
- User types `/scenelens <url-or-path> [question]`.

## How to invoke

**Step 1 — parse user input.** Separate the video source from any question. `/scenelens https://youtu.be/abc what hook did they open with?` → source = `https://youtu.be/abc`, question = `what hook did they open with?`.

**Step 2 — run the script.** Pass the source verbatim:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/scenelens.py" "<source>"
```

Optional flags:

- `--mode auto|scene|fixed` — frame selection strategy. Default `auto`: scene-aware first, fixed-fps fallback if scene changes are sparse. Force `fixed` for content with no hard cuts (e.g. a single-take talking head).
- `--scene-threshold F` — sensitivity (0-1, default 0.30). Lower = more frames captured. Bump to 0.20 for subtle visual changes.
- `--start T` / `--end T` — focus on a section (`SS`, `MM:SS`, `HH:MM:SS`).
- `--max-frames N` — lower the cap for tighter token budget.
- `--resolution W` — frame width in px (default 512; bump to 1024 only when the user must read tiny on-screen text and OCR isn't catching it).
- `--no-ocr` — skip the OCR pass. Use for content with no on-screen text (podcasts, interviews) to save a few hundred ms.
- `--ocr-lang CODE` — Tesseract language (default `eng`).
- `--fps F` — only applies in fixed-fps mode. Capped at 2 fps.
- `--whisper groq|openai` — force a specific backend. Default: prefer Groq when both keys exist.
- `--no-whisper` — disable Whisper entirely; frames-only if no captions.
- `--sub-langs L1,L2` — caption languages in priority order (default `en,en-US,en-GB,en-orig`).
- `--out-dir DIR` — keep working files somewhere specific.

**Step 3 — Read every frame path the script lists.** The Read tool renders JPEGs directly as images. Read all frames in a single message (parallel tool calls). Each frame has a `t=MM:SS` timestamp. When OCR text is present, the report shows it inline — use that text directly instead of trying to read pixels.

**Step 4 — answer the user.** You now have THREE streams of evidence:
- **Frames** — what's on screen (chosen at scene cuts when possible)
- **OCR** — on-screen text, already extracted
- **Transcript** — what was said, with timestamps

If the user asked something specific, answer with timestamp citations. Otherwise summarize: structure, key visuals, what was said.

**Step 5 — clean up.** The script prints a working directory at the end. If the user isn't asking follow-ups, delete it with `rm -rf <dir>`.

## Frame selection — why scene-aware matters

A 10-minute video with one demo and nine minutes of talking head:
- **Fixed fps:** 80 frames evenly spaced — 8 of them on the demo, 72 on the head.
- **Scene-aware:** dense around scene cuts — the demo frames cluster on UI changes, the head frames spread sparsely.

Same token cost, dramatically better signal. The default mode is `auto`: scene detection first, with automatic fallback to fixed-fps when fewer than 8 scene changes are detected (single-take videos, screen recordings of static UI). Use `--mode fixed` to force the legacy behavior; use `--mode scene` to disable the fallback.

## Focusing on a section

When the user names a moment ("around 2:30", "the first 10 seconds", "the last 30 seconds"), pass `--start` / `--end`. Frame budget tightens around the range, transcript filters to the same window, frame timestamps stay absolute (real video timeline).

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/scenelens.py" video.mp4 --start 50 --end 60
python3 "${CLAUDE_SKILL_DIR}/scripts/scenelens.py" "$URL" --start 2:15 --end 2:45
python3 "${CLAUDE_SKILL_DIR}/scripts/scenelens.py" "$URL" --start 1:12:00
```

## Transcription

1. **Native captions (free, preferred).** yt-dlp pulls manual or auto-generated subtitles when available.
2. **Whisper API fallback.** If captions are missing, the script extracts mono 16 kHz mp3 audio (~480 kB/min) and uploads it to Groq's `whisper-large-v3` (preferred) or OpenAI's `whisper-1`.
3. **Auto-chunking for long audio.** Audio >24 MB is split into chunks under the 25 MB API cap, each transcribed separately, then merged with offset timestamps. A 4-hour podcast no longer fails — it just makes more API calls.

Both keys live in `~/.config/scenelens/.env`. Unlike skills that fall back to a project-local `.env`, scenelens reads ONLY from `~/.config/scenelens/.env` and process env — to avoid silently picking up keys from random project directories.

## Failure modes

- **Setup preflight failed** → run `python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py"` (auto-installs ffmpeg/yt-dlp via brew on macOS, scaffolds `.env`). For an API key, ask the user via `AskUserQuestion` and write it to `~/.config/scenelens/.env`.
- **No transcript available** → captions missing AND (no Whisper key OR Whisper API failed). Proceed frames-only and tell the user.
- **`--mode scene` returned no frames** → the video has no detectable scene changes. Re-run with `--mode auto` (default) or `--mode fixed`.
- **OCR not available** → tesseract not installed. The skill keeps working; the report says `OCR: unavailable`. Mention to the user that installing tesseract would unlock the OCR sidechannel.
- **Whisper request fails** → printed to stderr (likely: invalid key, rate limit, or all chunks failed). Retry with `--whisper openai` if Groq failed (or vice versa).

## Token efficiency

Frames dominate token cost. Order of magnitude:
- 80 frames @ 512 px ≈ 50-80 k image tokens.
- Transcript ≈ a few thousand tokens for a 10-min video.
- OCR text is cheap — a few hundred to a couple thousand tokens.
- Bumping `--resolution` to 1024 roughly 4x's image tokens per frame. Only do it when OCR doesn't catch what's needed.

If you already watched a video this session and the user asks a follow-up, do **not** re-run the script — you already have the frames + OCR + transcript. Answer from context.

## Security & Permissions

**What this skill does:**
- Runs `yt-dlp` locally to download the video and pull native captions (public data, request goes to whatever host the URL points at).
- Runs `ffmpeg` / `ffprobe` locally to extract frames and (when Whisper is needed) mono 16 kHz audio.
- Runs `tesseract` locally on the extracted JPEG frames (no network call).
- Sends the audio clip to Groq's Whisper API (`api.groq.com/openai/v1/audio/transcriptions`) when `GROQ_API_KEY` is set.
- Sends the audio clip to OpenAI's audio transcription API (`api.openai.com/v1/audio/transcriptions`) when `OPENAI_API_KEY` is set and Groq is not, or when `--whisper openai` is forced.
- Writes downloaded video, frames, audio, and intermediate transcripts to a working directory under the system tmp dir (or `--out-dir`) so Claude can `Read` them.
- Reads / creates `~/.config/scenelens/.env` (mode `0600` on POSIX) for the Whisper API key(s) and a `SETUP_COMPLETE` marker.

**What this skill does NOT do:**
- Does NOT upload the video itself anywhere — only the extracted audio goes out, and only when captions are missing AND Whisper is enabled.
- Does NOT read `.env` from the current working directory (would silently pick up keys from random project dirs).
- Does NOT write to system paths — `--out-dir` is rejected if it resolves under `/etc`, `/bin`, `/sbin`, `/usr/bin`, `/usr/sbin`, or `/boot`.
- Does NOT log API keys to stdout, stderr, or output files.
- Does NOT access platform accounts (no login, no cookies, no posting).
- Does NOT share keys between providers (Groq key only goes to `api.groq.com`, OpenAI key only to `api.openai.com`).

**Bundled scripts:** `scripts/scenelens.py` (entry), `scripts/download.py` (yt-dlp wrapper), `scripts/frames.py` (scene + fixed-fps extraction), `scripts/ocr.py` (Tesseract wrapper), `scripts/transcribe.py` (VTT parser), `scripts/whisper.py` (Groq/OpenAI clients with chunking), `scripts/setup.py` (preflight + installer).

Review scripts before first use to verify behavior.
