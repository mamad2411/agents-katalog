---
name: watch
description: "When the user wants to read, transcribe, summarize, or research a video — YouTube link, podcast clip, Loom, TikTok, X/Twitter video, local file, or any URL yt-dlp supports. Use when they paste a video URL, say 'transcribe this,' 'summarize this video,' 'what does this video say about X,' 'pull the transcript,' 'analyze this YouTube video,' or hand you a video for content research. Default is fast transcript-only (no video download). Pass --with-frames when the visual layer matters (UI bugs, on-screen text, visual breakdowns)."
metadata:
  version: 1.0.0
---

# Watch — read a video like a PDF

You don't have a video input. This skill bundles a Python script that fetches the timestamped transcript (and optionally frames) so you can answer questions about video content.

**Default mode is transcript-only.** No video download, no frame extraction — just captions pulled via yt-dlp in a few seconds. That covers ~every YouTube video and is the right default for research, summarization, and content analysis.

**Opt into `--with-frames`** only when the visual layer matters: debugging a screen recording, breaking down a thumbnail/hook visually, reading on-screen text, analyzing UI behavior.

## Requirements

Locally installed:
- `yt-dlp` — `brew install yt-dlp` (macOS) / `pipx install yt-dlp` (Linux) / `winget install yt-dlp.yt-dlp` (Windows)
- `ffmpeg` + `ffprobe` — `brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install Gyan.FFmpeg`. Only required for `--with-frames` and the Whisper audio fallback. Transcript-only on a captioned YouTube video does not need ffmpeg.

If the user's missing one, tell them the install command and stop. Do not auto-install.

## How to invoke

The script lives next to this SKILL.md. Invoke it with the absolute path or `${CLAUDE_SKILL_DIR}/watch.py`:

```bash
python3 "${CLAUDE_SKILL_DIR}/watch.py" "<url-or-path>"
```

If `${CLAUDE_SKILL_DIR}` isn't set in this agent, resolve the path yourself — it's the directory holding this SKILL.md file.

### Default (transcript-only)

```bash
python3 "${CLAUDE_SKILL_DIR}/watch.py" "https://youtu.be/abc123"
```

Returns a markdown report with title, channel, duration, and a timestamped transcript like:

```
[00:01] All right, so here we are, in front of the elephants
[00:05] the cool thing about these guys is that they have really...
```

### With frames (visual layer)

```bash
python3 "${CLAUDE_SKILL_DIR}/watch.py" "<url>" --with-frames
```

Returns frame paths + transcript. **Read each frame path in parallel** with the Read tool so you see the full chronological visual flow alongside the transcript.

### Focus on a section

```bash
python3 "${CLAUDE_SKILL_DIR}/watch.py" "<url>" --start 1:30 --end 2:00
```

Works in both modes. Times accept `SS`, `MM:SS`, or `HH:MM:SS`. In transcript-only mode it filters the transcript. In `--with-frames` mode it also limits frame extraction and switches to a denser frame budget.

### Other flags

| Flag | Purpose |
|------|---------|
| `--no-whisper` | Don't fall back to Whisper if captions are missing. Fail with a clear error instead. |
| `--whisper groq\|openai` | Force a Whisper backend. Default: prefer Groq, fall back to OpenAI. |
| `--max-frames N` | (frames mode) Cap on frame count. Default 80, hard max 100. |
| `--resolution W` | (frames mode) Frame width in px. Default 512. Bump to 1024 only if reading on-screen text matters. |
| `--fps F` | (frames mode) Override auto-fps (clamped to 2 fps). |
| `--out-dir DIR` | Keep working files somewhere specific (default: tmp). |
| `--json` | (transcript mode) Emit machine-readable JSON instead of markdown. |

## When the script needs Whisper

If a video has no captions (rare for YouTube, common for Loom / Instagram / local files) and you didn't pass `--no-whisper`, the script will:

1. Download audio only (transcript-only mode) or extract from the downloaded video (`--with-frames`)
2. Upload it to Groq's `whisper-large-v3` (preferred — cheap, fast) or OpenAI's `whisper-1`
3. Return the same `[MM:SS]` timestamped format

To enable Whisper, set one of these (script reads env vars or `~/.config/watch/.env`):

```
GROQ_API_KEY=...        # console.groq.com/keys
OPENAI_API_KEY=...      # platform.openai.com/api-keys
```

If neither key is set and captions are missing, the script exits 2 with a clear message — tell the user how to enable Whisper or that this particular video can't be transcribed.

## Output flow

**Transcript-only (default).** The script prints a self-contained markdown report. Quote timestamps when citing claims. Don't re-print the full transcript back to the user — summarize, extract, or answer their question.

**`--with-frames`.** Same report plus a list of frame paths. After running:

1. Read every frame path in a single parallel batch — you need them all to follow the visual flow.
2. Combine frames with the transcript when answering. If the user asked about the hook, look at frames 1-3 + transcript 0:00–0:15.

## Cleanup

The script prints a working directory. If the user isn't going to ask follow-ups about this video, `rm -rf <dir>` when you're done. Otherwise leave it in place — re-runs can reuse it via `--out-dir`.

## Common research workflows

**Hook deconstruction.** `python3 watch.py "<url>" --start 0 --end 15 --with-frames` → analyze cold open: words said, what's on screen, pattern interrupt timing.

**Channel research.** Run transcript-only on 5-10 competitor videos. Compare structure, topic mix, CTA placement, transcript length-to-duration ratio.

**Quote extraction.** Transcript-only + grep for a topic in the report (use Bash on the printed work dir).

**UI bug repro.** `--with-frames` on a screen recording, then ask which frame the bug appears. Frames mode shines here.

## Don't

- Don't re-run the script on a video you already watched this session — you have the transcript in context. Just answer.
- Don't pass `--with-frames` for pure-text research. It downloads the full video and burns image tokens for no benefit.
- Don't write API keys into the repo or to stdout. They live in `~/.config/watch/.env` (mode 0600).

## Security

The script runs `yt-dlp` and `ffmpeg` locally — no third-party server in the middle. Audio only leaves the machine when Whisper is needed AND a key is configured (Groq or OpenAI endpoint, whichever matches). The video itself never gets uploaded.

Inspect `watch.py` before first run if you want to verify.
