---
name: video-watch
description: "Watch / analyze a video or audio source the agent cannot natively play. Triggers: 'watch this video', 'analyze this short/reel/clip', 'what happens in this video', 'reverse-engineer this video', 'read the frames of', 'transcribe this video', '/video-watch'. A URL from YouTube, TikTok, Instagram, X, Facebook, Vimeo, Reddit, Twitch, LinkedIn or 1750+ other sites, or a local file. Downloads it, pulls captions (or transcribes locally when there are none), and extracts frames so the agent can Read the transcript + frames and describe pacing, hooks, on-screen text, format, or answer questions about the content. No API key needed."
license: MIT
compatibility: Runs on macOS and Linux — both scripts are bash. On Windows use WSL or Git Bash; there is no native PowerShell path. Requires ffmpeg, and yt-dlp for URL sources; run scripts/setup.sh to check for either (--check) or install them (--yes). An optional local whisper engine (free, offline) adds transcripts for sources with no captions. Needs network access for remote videos.
metadata:
  author: itqanlab
  version: "3.0.1"
  category: media
  short: "Let your agent watch and transcribe any video"
  starter: "tell me why the hook of this video works"
---

# video-watch

Let the agent "watch" a video by turning it into a transcript plus frames it can Read.

## When to use
- Someone shares a video URL or a local file and wants it watched, analyzed, summarized, or reverse-engineered — hook, pacing, on-screen text, editing style, format.
- You need the visual or spoken content of a video, not just its metadata.
- Also works on audio-only sources, in which case you get a transcript and no frames.

## Setup

Check and install what this skill needs:

```
bash scripts/setup.sh --check          # report only, installs nothing
bash scripts/setup.sh                  # shows a plan, asks, then installs
bash scripts/setup.sh --yes            # non-interactive, for agent use
bash scripts/setup.sh --with-whisper   # add free offline speech-to-text
```

It detects the platform and package manager (Homebrew, apt, dnf, pacman, zypper, apk, pipx/pip) and prints every command before running it. Nothing installs without a confirmation or an explicit `--yes`.

If a dependency is missing when you run the main script, it will point you here.

## How to use

1. Run the script. It prints a manifest with the transcript path and frame paths:
   ```
   bash scripts/watch.sh "<url-or-path>" [options]
   ```
2. **Read the transcript** — the `.srt` path in the manifest, if present.
3. **Read the frames** in order (`frame_001.jpg`, `frame_002.jpg`, …) — the visual track.
4. Synthesize: answer the question, or describe the hook (first ~1s), pacing and cuts, on-screen text, format (letterbox vs full-bleed), branding, and anything notable.

### Options

| Option | Default | What it does |
| :-- | :-- | :-- |
| `--frames N` | 30 (max 60) | Target frame count |
| `--width W` | 480 | Frame width in px |
| `--start SEC` / `--end SEC` | — | Sample a time range only |
| `--lang CODE` | `en.*` | Caption language, e.g. `ar.*`, `all` |
| `--scenes` | off | One frame per visual cut |
| `--no-whisper` | off | Skip local transcription even if an engine is installed |
| `--whisper-model M` | `base` | Speed vs accuracy, e.g. `large-v3` |
| `--yes` | off | Accept prompts, including installing a transcriber |
| `--cookies BROWSER` | — | Login-gated videos, e.g. `chrome` |
| `--playlist N` | single | Allow a playlist, take first N |
| `--outdir DIR` | temp | Where output lands |
| `--keep-video` | off | Keep the download |

## Choosing options

**Short clips (under 60s).** The default 30 frames is roughly one every 1–2s. Plenty.

**Long videos.** Raise `--frames`, or better, use `--start`/`--end` to sample the section that matters. The whole file downloads before framing, so narrowing the range does not skip the download but does keep the frame count meaningful.

**Edited video with cuts.** `--scenes` gives one frame per visual cut, so you see the shots that actually exist rather than arbitrary samples across them. It falls back to even sampling automatically when a source has too few cuts to be useful, such as a static screencast or a single-shot talking head.

**No captions.** Many sources ship none. The script then looks for captions in any language, and if there are still none it transcribes locally — automatically, whenever a whisper engine is installed. Installing one is the opt-in; `--no-whisper` skips it, and `--whisper-model large-v3` trades speed for accuracy.

**Login-gated or age-restricted.** `--cookies chrome` reuses a browser session you are already signed into. Only use it on accounts and content you have access to.

**Comparing several videos.** Run once per URL into separate `--outdir` directories, then read across the frame sets.

## What it accepts

Any source yt-dlp supports — 1750+ sites including YouTube, TikTok, Instagram, X, Facebook, Vimeo, Reddit, Twitch, Dailymotion, Bilibili, SoundCloud and LinkedIn — plus direct media URLs and local files. Audio-only sources return a transcript with no frames.

## Notes
- Reads publicly accessible media. It does not bypass paywalls or DRM. `--cookies` reuses your own session; it does not defeat access control.
- A playlist URL downloads a single video unless you pass `--playlist N`.
- Downloaded video is deleted after framing unless you pass `--keep-video`. Frames and transcript remain.
- If a source that used to work stops downloading, the usual cause is an out-of-date yt-dlp. `scripts/setup.sh` will update it.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
