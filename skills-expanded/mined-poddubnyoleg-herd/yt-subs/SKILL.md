---
name: yt-subs
description: Download a YouTube video's subtitles as clean plain text. Use when the user wants the transcript/captions/text of a YouTube video, asks to summarize a video, or shares a youtube.com / youtu.be link they want analyzed without watching.
user-invocable: true
allowed-tools: Bash, Read
argument-hint: [youtube URL]
---

# YouTube Subtitles

Downloads subtitles via `yt-dlp` and cleans them to plain text. Handles the rolling-overlap format YouTube uses for auto-captions.

## Usage

```bash
~/.claude/skills/yt-subs/yt_subs.py "URL"
```

Options:
- `--lang en,ru` — comma-separated language priority (default: `en,ru`)
- `-o transcript.txt` — write to file instead of stdout
- `--raw` — output the original VTT instead of cleaned text

## Behavior

One yt-dlp call per tier, best fidelity first:

1. **Manual** subs in the requested languages (`en` also matches `en-US`).
2. The **original-language auto track** — YouTube names it `xx-orig` — whatever its language: the speaker's words, not a translation.
3. Last resort: YouTube's **machine translation** into the requested languages. Requested together with the original, it has drawn HTTP 429s that cost the original too.

stderr names the track and its origin — `# subtitle file: ID.en-orig.vtt (auto-original)`; origin is `manual`, `auto-original` or `auto-translated`. Say so when quoting an `auto-translated` transcript. On failure, stderr carries yt-dlp's ERROR/WARNING lines (bot challenge, 429, PO token) and the video's track list, and the exit code is 1.

## Examples

```bash
# default (prefer en, then ru), print to stdout
~/.claude/skills/yt-subs/yt_subs.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Russian-first, save to file
~/.claude/skills/yt-subs/yt_subs.py "URL" --lang ru,en -o transcript.txt

# raw VTT (keep timestamps)
~/.claude/skills/yt-subs/yt_subs.py "URL" --raw -o transcript.vtt
```

## Notes

- Requires `yt-dlp` on PATH (or at `~/opt/anaconda3/bin/yt-dlp`). Install: `pip install yt-dlp`.
- Also requires `curl_cffi` (`pip install curl_cffi`) — yt-dlp uses it for browser impersonation, without which YouTube returns HTTP 429 on subtitle endpoints.
- Single-video only — `--no-playlist` is always set.
- For long videos pipe to a file, then Read it; don't dump 50K-token transcripts into the chat.
- `--lang` still decides between manual tracks: on a Russian talk with human English subs, the default `en,ru` returns those over the Russian auto track. Pass `--lang ru` for the original speech.
- Privacy: yt-dlp talks to YouTube only. Don't paste transcript content into external research tools without checking it for PII first.
