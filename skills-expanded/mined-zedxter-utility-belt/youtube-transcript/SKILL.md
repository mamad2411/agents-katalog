---
name: youtube-transcript
description: Fetch the transcript (subtitles/captions) of a YouTube video as plain text, timestamped lines, SRT or JSON using the free, key-less youtube-transcript-api library. Use whenever the user shares a YouTube link or video id and wants the transcript, a summary, notes, key takeaways, quotes, a translation, or any analysis of what is said in the video ("конспект видео", "о чём это видео"). Not for finding videos (youtube-search), saving the audio (youtube-audio), or audio and video files the user already has (transcribe-audio).
license: MIT
compatibility: Python 3.12+ with uv (preferred) or pip; macOS, Linux, Windows. Needs network access to youtube.com; requests from cloud/datacenter IPs are frequently blocked by YouTube (use --proxy).
metadata:
  author: zedxter
  version: "1.1.1"
  source: https://github.com/zedxter/utility-belt
---

# YouTube Transcript

Get the text of a YouTube video without downloading audio, without API keys and
without paid services. The script reads the video's existing captions (manual or
auto-generated) via the `youtube-transcript-api` Python library.

## When to use

Trigger this skill when the user:

- pastes a YouTube URL (`youtube.com/watch?v=…`, `youtu.be/…`, `/shorts/…`,
  `/live/…`, `/embed/…`) or a bare 11-character video id, and
- asks for the transcript, subtitles, "what does this video say", a summary,
  recap, notes/outline, key points, quotes, timestamps of a topic, a translation,
  or wants to answer questions about the video's content.

Do **not** use it for playlists, channels, comments, view counts or video
metadata (title, description) — the script only returns spoken text.

## Quick start

The script lives at `scripts/transcript.py` relative to this skill. Run it with
`uv` (installs the dependency into a cached environment automatically):

```bash
uv run scripts/transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Always pass the full URL, quoted**, not a bare id: ids can start with `-`
(e.g. `-PTlnwUCwuU`), which shells and argument parsers treat as an option. If
you only have the id, put `--` before it so it cannot be read as a flag:

```bash
uv run scripts/transcript.py "https://www.youtube.com/watch?v=-PTlnwUCwuU"   # preferred
uv run scripts/transcript.py -f timestamps -- -PTlnwUCwuU                      # also safe
```

Options go *before* `--`; everything after it is taken literally. The script
also rewrites a bare `-PTlnwUCwuU` into a URL by itself, but the two forms above
are unambiguous for every shell and wrapper.

Without `uv`:

```bash
pip install youtube-transcript-api
python3 scripts/transcript.py dQw4w9WgXcQ
```

Default behaviour: prefer Russian, then English captions (`--lang ru en`); if
neither exists, fall back to any available transcript (manual before auto) and
print a `note:` on stderr. Never pass `--translate` — fetch the original and
translate in your reply (see workflow step 4). Output is plain text joined into ~60-second
paragraphs, prefixed by a two-line header with the video id and the language used:

```
# video: 9m-nmKNKD1U
# language: English (en, auto-generated)
```

## Options

| Flag | Meaning |
|------|---------|
| `-l, --lang ru en …` | Preferred caption languages, in order. Falls back to anything available. |
| `-t, --translate LANG` | **Do not use.** Asks YouTube to machine-translate the captions; YouTube blocks this endpoint far more aggressively than plain caption fetches, so it fails with exit 4 where a normal fetch succeeds. Kept only for manual experiments. |
| `-f, --format text\|timestamps\|srt\|json` | `text` (paragraphs, default), `timestamps` (`[mm:ss] line`), `srt` (subtitle file), `json` (raw snippets with start/duration). |
| `--paragraph-seconds N` | Target paragraph length for `text` format (default 60). A paragraph ends at the first sentence end after N seconds; if none shows up (auto captions have no punctuation) it is cut at the next caption after 2×N. |
| `--no-header` | Omit the `# video / # language` header. |
| `--list` | Show available transcripts (language, manual/auto, translatable) and exit. |
| `-o, --out FILE` | Write to a file instead of stdout. |
| `--proxy URL` | HTTP(S) proxy, e.g. `http://user:pass@host:port`, when YouTube blocks the IP. |

## Recommended workflow

1. **Fetch once, save to a file.** Transcripts of long videos are large; keep
   them out of the conversation and read selectively:
   ```bash
   uv run scripts/transcript.py <url> -o transcript.txt
   ```
   Use a path that works on the current OS (the working directory, or the
   agent's scratch/temp directory) — do not hard-code `/tmp` on Windows.
2. **Pick the format for the task.**
   - Short video (<20 min), full summary or notes → `text` (default).
   - **Long video (>20 min), or any targeted question** → `timestamps`. One
     caption per line with `[hh:mm:ss]` makes the file greppable: search for
     the keywords of the user's question, read only the lines around the hits,
     and quote with exact times. This is far cheaper than reading the whole
     transcript and works for "where does she talk about X", chapter markers
     and fact-checking.
   - Subtitle file for the user → `srt`.
   - Programmatic processing → `json`.
3. **Mind the size.** A 10-minute talk is ~1,500 words; a 2-hour podcast is
   ~20,000 words. For long videos: save as `timestamps`, grep for the topics you
   need (your search tool, or `grep -i` / `Select-String` on Windows), then read
   only those regions with your file-reading tool (offset/limit). For a full
   summary of a long video, read it in chunks, summarise each, then merge —
   never paste the whole file into the reply.
   ```bash
   uv run scripts/transcript.py "<url>" -f timestamps -o transcript.txt
   grep -n -i "pricing\|price\|cost" transcript.txt
   ```
4. **Translate yourself, never with `--translate`.** Always fetch the
   original-language captions and do the translation in your own reply. If the
   user wants the transcript in another language (e.g. an English video, text
   in Russian), fetch the English captions to a file, then translate the file
   chunk by chunk — do not call the script with `-t`. Reasons: YouTube blocks
   the translation endpoint even when ordinary fetches work, and its machine
   translation is worse than yours. Reply in the user's language regardless of
   the caption language.
5. **Auto-captions are noisy.** No punctuation, wrong homophones, mangled
   names and numbers. The header says `auto-generated` when that is the case —
   mention it when quoting precisely, and sanity-check names/figures.
6. **Cite timestamps** when the user may want to jump to a moment:
   `https://youtu.be/<id>?t=<seconds>`.

## Errors and exit codes

The script prints a one-line `error:` on stderr and exits non-zero. Act on the
code rather than guessing:

| Exit | Meaning | What to do |
|------|---------|------------|
| 2 | Bad input (not a YouTube URL/id) or missing dependency | Ask for a correct link; or install `youtube-transcript-api` / use `uv run`. |
| 3 | No transcript: captions disabled, none in any language, or not translatable | Run `--list` to show what exists. If nothing exists, tell the user the video has no captions. Offer `transcribe-audio` (below). |
| 4 | Blocked by YouTube (`RequestBlocked` / `IpBlocked`) | If you used `--translate`, drop it and fetch the original captions instead — that is the usual cause. Otherwise typical on cloud/datacenter IPs or after many rapid requests: wait a minute and retry once; then suggest `--proxy` with a residential proxy or running from the user's own machine. Do not hammer with retries — it extends the block. |
| 5 | Video unavailable: private, deleted, region-locked, age-restricted | Nothing to fetch; report it. Age-restricted videos require a signed-in session, which this tool does not support. |
| 6 | Network failure | Check connectivity and retry. |
| 7 | Other YouTube error (unparsable page, consent cookie, etc.), or an unexpected error in the script (the message says `unexpected`) | Usually transient or a YouTube-side change; retry, then report with the message. Upgrading `youtube-transcript-api` often fixes parser breakage. |
| 130 | Interrupted | — |

Note that `--list` can succeed while the actual fetch is blocked (the two use
different YouTube endpoints), so a successful listing does not guarantee the
transcript is retrievable from the current IP.

## No captions? Transcribe the audio

If a video genuinely has no captions (exit 3 and `--list` is empty), use the
`transcribe-audio` skill from the same collection with the same URL: it
downloads the audio and runs Whisper locally (no key, no upload) and prints
the same text/timestamps/SRT formats (plus VTT and its own JSON). It needs a
one-time model download (486 MB for the default `small`) and takes minutes
for long videos on a CPU,
so tell the user and let them decide before proceeding.

## Finding the video first

If the user has no link yet ("summarise the latest talk about X"), use the
`youtube-search` skill from the same collection — general web search is poor at
finding YouTube videos. It returns candidates with date, views and duration;
pick one, then come back here with its URL. Without that skill, `yt-dlp` can
search too: `uv run --with yt-dlp yt-dlp "ytsearch5:<query>" --flat-playlist --print "%(id)s %(title)s"`.

## Limitations

- Only existing captions: no captions → no transcript.
- Timestamps are caption cue starts, not word-level.
- Speaker labels are not available.
- YouTube rate-limits and blocks datacenter IPs aggressively; this is a
  YouTube policy, not a bug in the script.
