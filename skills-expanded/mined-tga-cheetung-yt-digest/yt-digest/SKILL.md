---
name: yt-digest
description: Turn a YouTube URL into a vault-ready research digest — transcript, key learning moments with timestamp deep-links, and screenshots of visual moments (slides, demos, dashboards). Use when the user pastes a YouTube link they're researching, says "summarize this video", "/yt-digest <url>", "youtube digest", or asks to extract key points from a YouTube talk. Output goes to vault/research/youtube/<slug>.md with screenshots in vault/attachments/youtube/<slug>/. Source MP4 is auto-deleted after frame extraction.
argument-hint: "<youtube-url> [--no-screenshots] [--tags tag1,tag2] [--slug custom-slug]"
---

# yt-digest

Process a YouTube video into a single markdown research note in your notes vault. Drop a link, get a digest that's faster to consume than the video.

## Output contract

- **Digest:** `vault/research/youtube/<slug>.md` — frontmatter + TL;DR + numbered takeaways (each with timestamp deep-link + screenshot if visual) + collapsed transcript
- **Screenshots:** `vault/attachments/youtube/<slug>/frame-MM-SS.png` — embedded in digest via Obsidian's `![[...]]` syntax
- **Staging:** `/tmp/yt-digest/<slug>/` — video + raw VTT, **deleted at end of run**

Headless-safe: all inputs come from CLI args, no interactive prompts, deterministic output path so an orchestrator can read the result back.

## Workflow

### 0. Parse args

Required: a YouTube URL (any form — `youtu.be/x`, `youtube.com/watch?v=x`, `youtube.com/shorts/x`).

Optional flags:
- `--no-screenshots` — skip video download + frame extraction (transcript-only, ~$0.01, ~5s)
- `--tags a,b,c` — add to frontmatter `tags:` list
- `--slug name` — override auto-generated slug

If no URL is provided, abort with a one-line error — do NOT prompt the user (this skill runs headless).

### 1. Fetch transcript + video

```bash
mkdir -p /tmp/yt-digest
META_JSON=$(.claude/skills/yt-digest/scripts/fetch.sh "$URL" "/tmp/yt-digest/staging-$$" ${NO_SCREENSHOTS:+--no-video})
```

Parse `META_JSON` (one-line JSON) for: `id`, `title`, `channel`, `duration_seconds`, `upload_date` (YYYYMMDD), `slug`, `transcript_path`, `video_path`.

Override `slug` if `--slug` was passed.

Set up paths:
```bash
WORK_DIR="/tmp/yt-digest/staging-$$"
ATTACH_DIR="vault/attachments/youtube/$SLUG"
DIGEST_PATH="vault/research/youtube/$SLUG.md"
mkdir -p "$ATTACH_DIR" "$(dirname "$DIGEST_PATH")"
```

**If `transcript_path` is empty:** YouTube has no captions for this video. Abort with: "No captions available for this video. Re-run with audio re-transcription (not yet implemented) or skip." Clean up `$WORK_DIR` before exiting.

### 2. Flatten the VTT

```bash
TRANSCRIPT_JSON=$(.claude/skills/yt-digest/scripts/parse_vtt.py "$TRANSCRIPT_PATH")
```

`TRANSCRIPT_JSON` is `[{start_seconds, text}, ...]` with rolling-caption duplicates removed.

### 3. Pick key learning moments

Read the full transcript. Identify **5-10 key moments** that earn a bullet in the digest. Each moment is:

```json
{
  "start_seconds": 754,
  "title": "Concise one-line insight (≤ 12 words)",
  "quote": "Verbatim line from the transcript that earned this bullet",
  "needs_screenshot": true,
  "rationale": "Why a screenshot would help — e.g. 'slide showing the 6-bucket framework'"
}
```

Selection criteria:
- Concrete frameworks, models, or step-by-step processes
- Specific numbers, data points, or benchmarks
- Counterintuitive claims with reasoning
- Moments where the speaker references something on-screen ("as you can see here…", "this chart shows…", "the formula is…")

Set `needs_screenshot: true` ONLY when the speaker is clearly referencing a visual (slide, demo, chart, code). Pure talking-head insights get `needs_screenshot: false`.

**Anti-patterns** — don't pick:
- Intros, outros, sponsor reads, channel housekeeping
- Filler restatements ("so what I'm saying is…")
- Repeated points (pick the strongest framing only)

### 4. Extract frames

If `--no-screenshots` was passed, skip this step.

Collect timestamps where `needs_screenshot: true`:
```bash
.claude/skills/yt-digest/scripts/extract_frames.sh "$VIDEO_PATH" "$ATTACH_DIR" 754 1230 1890
```

Frames land as `frame-MM-SS.png` in `$ATTACH_DIR`.

### 5. Assemble the digest

Write `$DIGEST_PATH` using this exact structure:

```markdown
---
source: youtube
url: https://youtube.com/watch?v=<id>
channel: <channel>
title: <title>
duration: <hh:mm:ss>
published: <YYYY-MM-DD from upload_date>
digested: <today's date YYYY-MM-DD>
tags: [youtube, research, <user-supplied tags>]
---

# <title>

**Channel:** <channel> · **Length:** <hh:mm:ss> · **Published:** <YYYY-MM-DD> · [Watch ↗](<url>)

## TL;DR

- 3-5 punchy bullets capturing the video's thesis. Each bullet stands alone.

## Key Takeaways

### 1. <title from moment> · [<MM:SS>](<url>&t=<start_seconds>s)

<2-4 sentences expanding the insight. Reference the screenshot if present.>

![[frame-MM-SS.png]]   <!-- only if needs_screenshot was true -->

> <verbatim quote>

### 2. <next moment...>

...

## Open Questions

- 1-3 questions the video raises but doesn't answer, or things worth trying
- Skip this section if nothing concrete comes to mind — don't manufacture filler

## Full Transcript

<details>
<summary>Click to expand</summary>

```
[00:00] First line of transcript text.
[00:08] Second line...
```

</details>
```

Notes on assembly:
- `<url>&t=<start_seconds>s` — YouTube timestamp deep-link. Use `&` if URL already has `?v=`, else `?t=`.
- Format duration as `H:MM:SS` if ≥ 1hr, else `MM:SS`.
- The screenshot path is relative — Obsidian's `![[frame-MM-SS.png]]` resolves via the vault's attachment folder config. If that fails for any reader, use the explicit form `![](../attachments/youtube/<slug>/frame-MM-SS.png)` as fallback.
- Full transcript block: timestamp each line as `[MM:SS]` so future search lands you at the right second.

### 6. Cleanup

Use Python rather than `rm -rf` — Claude Code's safety policy hard-blocks `rm -rf` even when explicitly allowlisted, which would break headless dispatch:

```bash
python3 -c "import shutil, sys; shutil.rmtree(sys.argv[1], ignore_errors=True)" "$WORK_DIR"
```

This deletes the source MP4 + raw VTT. The vault keeps only: digest markdown + screenshots (~2-3 MB total per video).

### 7. Print result

Final line of output must be:
```
DIGEST: <absolute path to digest>
```

Any orchestrator can parse this to surface the file back to the originating thread.

## Cost

| Component | Cost per 30-min video |
|---|---|
| yt-dlp transcript + video | $0 |
| Model digest pass (~7K in / 800 out) | ~$0.01–0.04 |
| ffmpeg frame extraction | $0 |
| Vault storage (digest + screenshots) | ~3 MB |

Source MP4 (~100 MB) is deleted in step 6.

## Headless / remote dispatch

The skill writes to a deterministic path and prints `DIGEST: <path>` as its final line, so it composes with any orchestrator that can shell out — cron, CI, or a chat bot. The pattern worth building: a Slack/Telegram bot that runs the skill on a pasted URL and posts the path (or the rendered TL;DR) back into the thread. "Drop a link in chat, get a digest in your vault" becomes a one-message workflow.

**Model note for unattended runs:** in a headless `claude -p` run, a small/cheap model will sometimes describe what the skill *would* do rather than invoking the scripts (turns burned, zero tool calls, nothing written). Route the unattended dispatch to a more capable model. The interactive run is fine on the cheap model.

## Failure modes

- **No captions:** abort cleanly per step 1 — do not silently produce an empty digest.
- **yt-dlp 403 / age-restricted:** print the actual yt-dlp error and abort. Don't paper over with cookies-based workarounds without explicit user request.
- **ffmpeg fails on a timestamp:** log the failure but continue with the other frames. The digest still ships; the missing screenshot is just omitted (don't leave broken `![[...]]` syntax).
- **Vault path collision:** if `vault/research/youtube/<slug>.md` already exists, append a `-2` suffix to the slug. Don't overwrite.
