---
name: yt-tran
description: Analyze a YouTube video into an action report — deep mode (-h, default) synthesizes transcript, description, chapters, top comments, thumbnail, and key frames; fast mode (-l) returns transcript + key points only. Use to extract the substance of a video without watching it.
---

# YouTube Video Intelligence Skill

Analyze a single YouTube video from every available signal and produce a structured **action report** — not a raw transcript dump.

**Arguments:** `[video-url] [-l | -h]`
- `-h` or no flag → **High mode** (deep analysis). Run the **HIGH MODE** section below.
- `-l` → **Low mode** (fast: transcript + key points). Run the **LOW MODE** section below.

Only single videos are supported. If the URL contains `/playlist?`, `/@`, `/channel/`, or `/c/`, stop:
> "This skill is for single videos only. Please provide a direct video URL (e.g. `https://www.youtube.com/watch?v=...`)."

**Prerequisites:** `yt-dlp` (required), `ffmpeg` (frame extraction, optional), `faster-whisper` (transcription fallback, optional — GPU-accelerated with CPU fallback).

**Output location:** reports are saved under `research/youtube/` in your working directory (change the path to suit your setup). Temp `yt_session*` files are written to the working directory and deleted at the end.

---

# HIGH MODE (-h, default)

Use ALL signals: metadata, description, chapters, top comments, transcript, thumbnail, and key frames. Treat the output as a briefing from someone who watched the video, read every comment, and analyzed every visual.

## Phase 1: Check & Update yt-dlp

```bash
command -v yt-dlp
```

**If not found**, install:
- **Windows (winget)**: `winget install yt-dlp.yt-dlp`
- **Windows (pip fallback)**: `pip install yt-dlp`
- **macOS**: `brew install yt-dlp`
- **Linux**: `pip3 install yt-dlp`

If all install attempts fail, point the user to https://github.com/yt-dlp/yt-dlp#installation and stop.

**Always update** — stale installs are the #1 cause of silent failures:
```bash
yt-dlp -U
```

## Phase 2: Detect Playlist or Channel URLs

Check the URL for `/playlist?`, `/@`, `/channel/`, `/c/`. If any match, stop with the single-video message.

## Phase 3: Fetch All Video Data in One Pass

```bash
yt-dlp \
  --write-info-json \
  --write-comments \
  --write-thumbnail \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en.*,a.en" \
  --skip-download \
  --output "yt_session" \
  "VIDEO_URL"
```

**Why `en.*,a.en`:** manual subs use codes like `en`, `en-US`, `en-GB` (matched by `en.*`). Auto-generated captions use `a.en` — a different prefix that `en.*` does NOT match. Both patterns are required.

This produces `yt_session.info.json`, `yt_session.jpg`/`.webp` (thumbnail), and `yt_session*.vtt` (subtitles). Comment fetching may take 15–30s for popular videos — normal. If the command fails entirely (private/age-restricted/unavailable), inform the user and stop.

## Phase 4: Parse Metadata, Description & Comments

Run as a **single bash block** (Python detection and invocation in the same shell call):

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
PYTHONUTF8=1 $PYTHON -c "
import json, glob, sys

files = glob.glob('yt_session*.info.json')
if not files:
    print('ERROR: info JSON not found')
    sys.exit(1)

with open(files[0], encoding='utf-8') as f:
    info = json.load(f)

print('=== METADATA ===')
print('Title: ' + str(info.get('title', 'Unknown')))
print('Uploader: ' + str(info.get('uploader', 'Unknown')))
print('Duration: ' + str(info.get('duration_string', 'Unknown')))
print('Duration_secs: ' + str(info.get('duration', 0)))
upload = str(info.get('upload_date', ''))
if len(upload) == 8:
    upload = upload[:4] + '-' + upload[4:6] + '-' + upload[6:]
print('Upload date: ' + upload)
views = info.get('view_count') or 0
likes = info.get('like_count') or 0
print('Views: ' + format(views, ','))
print('Likes: ' + format(likes, ','))
tags = info.get('tags') or []
if tags:
    print('Tags: ' + ', '.join(str(t) for t in tags[:12]))
cats = info.get('categories') or []
if cats:
    print('Categories: ' + ', '.join(str(c) for c in cats))

print()
print('=== DESCRIPTION ===')
desc = (info.get('description') or '').strip()
if desc:
    print(desc[:3500])
    if len(desc) > 3500:
        print('...[truncated]')
else:
    print('[No description]')

print()
print('=== CHAPTERS ===')
chapters = info.get('chapters') or []
if chapters:
    for ch in chapters:
        t = int(ch.get('start_time') or 0)
        h, m, s = t // 3600, (t % 3600) // 60, t % 60
        print('  %02d:%02d:%02d -- %s' % (h, m, s, ch.get('title', 'Chapter')))
else:
    print('[No chapters detected]')

print()
print('=== TOP COMMENTS ===')
comments = info.get('comments') or []
if comments:
    top = sorted(comments, key=lambda c: c.get('like_count') or 0, reverse=True)[:20]
    for i, c in enumerate(top, 1):
        text = (c.get('text') or '').replace('\n', ' ').strip()[:300]
        lk = c.get('like_count') or 0
        author = c.get('author', 'Unknown')
        print('%d. [%d likes] %s: %s' % (i, lk, author, text))
else:
    print('[No comments fetched — may be disabled or rate-limited]')
" > yt_session_meta.txt 2>&1
```

Read `yt_session_meta.txt` with the **Read tool**. If it contains `ERROR: info JSON not found`, Phase 3 failed — stop. Note the `Duration_secs` value (needed for Phase 6).

## Phase 5: Check for Subtitles

**Glob** for `yt_session*.vtt`. If a VTT exists → Phase 5a. If none was created, retry without the language filter (catches non-English videos):

```bash
yt-dlp --write-subs --write-auto-subs --skip-download --output "yt_session" "VIDEO_URL"
```

Glob again. Still nothing → Phase 5b (Whisper fallback).

## Phase 5a: Convert VTT → Readable Text

Run as a **single bash block**:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
PYTHONUTF8=1 $PYTHON -c "
import re, sys, glob, html

files = glob.glob('yt_session*.vtt')
if not files:
    print('NO_VTT_FOUND')
    sys.exit(1)

# Prefer manual subs (shorter filename: yt_session.en.vtt) over auto-gen (yt_session.a.en.vtt)
vtt_file = sorted(files, key=len)[0]

# Step 1: Parse VTT — keep the longest text per start-time second
# This collapses same-second rolling duplicates (auto-sub artifact)
time_bucket = {}
time_order = []
current_time = ''

with open(vtt_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if '-->' in line:
            current_time = line.split('-->')[0].strip().split('.')[0]
        elif line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and line != 'NOTE' and not line.startswith('NOTE ') and not line.isdigit():
            clean = re.sub(r'<[^>]+>', '', line)
            clean = html.unescape(clean).strip()
            if clean and current_time:
                if current_time not in time_bucket:
                    time_order.append(current_time)
                    time_bucket[current_time] = clean
                elif len(clean) > len(time_bucket[current_time]):
                    time_bucket[current_time] = clean  # keep longest (rolling window)

# Step 2: Collapse rolling-window duplicates across different seconds
final_lines = []
for i, t in enumerate(time_order):
    text = time_bucket[t]
    if i + 1 < len(time_order):
        next_text = time_bucket[time_order[i + 1]]
        if next_text.startswith(text) and next_text != text:
            continue  # this cue is incomplete — next one has the full text
    final_lines.append('[' + t + '] ' + text)

print('\n'.join(final_lines))
" > yt_session_out.txt
```

Read `yt_session_out.txt` with the **Read tool**.

## Phase 5b: Whisper Fallback (Last Resort)

Only if Phase 5 produced no VTT. Requires explicit user confirmation. Tell the user:
> "No subtitles found for this video. I can download the audio and transcribe it locally with Whisper (runs on GPU if available, else CPU). First install pulls the faster-whisper package. Should I proceed?"

**Wait for confirmation.** If confirmed:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)

# Install faster-whisper if missing (first run only). For NVIDIA GPU, also install:
#   nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*
if ! PYTHONUTF8=1 $PYTHON -c "import faster_whisper" 2>/dev/null; then
    $PYTHON -m pip install --user faster-whisper
fi

yt-dlp -x --audio-format mp3 --output "yt_session_audio.%(ext)s" "VIDEO_URL"

PYTHONUTF8=1 $PYTHON -c "
import sys
from faster_whisper import WhisperModel
def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return '%02d:%02d:%06.3f' % (h, m, s)
audio, out = sys.argv[1], sys.argv[2]
try:
    model = WhisperModel('small', device='cuda', compute_type='float16')
except Exception:
    model = WhisperModel('small', device='cpu', compute_type='int8')
segments, info = model.transcribe(audio, vad_filter=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write('WEBVTT\n\n')
    for seg in segments:
        f.write('%s --> %s\n%s\n\n' % (fmt(seg.start), fmt(seg.end), seg.text.strip()))
" yt_session_audio.mp3 yt_session_audio.vtt

rm -f yt_session_audio.mp3
```

This writes `yt_session_audio.vtt`. The Phase 5a glob `yt_session*.vtt` will find it — proceed to Phase 5a.

## Phase 6: Visual Analysis

### 6a: Analyze Thumbnail (Always)

**Glob** for `yt_session*.jpg` (then `.webp`). **Read** the thumbnail and analyze: what topic/concept does it signal? Is there a presenter, a setting? Text overlays, code snippets, UI screenshots, diagrams, terminal output? What emotion/urgency/style does it project?

### 6b: Extract Key Frames (Optional)

Run as a **single bash block** with all guards inline:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)

DURATION=$(PYTHONUTF8=1 $PYTHON -c "
import json, glob
files = glob.glob('yt_session*.info.json')
if files:
    with open(files[0], encoding='utf-8') as f:
        print(json.load(f).get('duration') or 9999)
else:
    print(9999)
")

# Only proceed if ffmpeg exists AND video is 30 min or under
if command -v ffmpeg &>/dev/null && [ "$DURATION" -le 1800 ]; then

    PYTHONUTF8=1 $PYTHON -c "
import json, glob
files = glob.glob('yt_session*.info.json')
if not files:
    print('5,30,60,120')
else:
    with open(files[0], encoding='utf-8') as f:
        info = json.load(f)
    duration = info.get('duration') or 0
    chapters = info.get('chapters') or []
    if chapters:
        timestamps = [int(c.get('start_time') or 0) for c in chapters[:6]]
        if not timestamps or timestamps[0] > 30:
            timestamps = [5] + timestamps
    else:
        timestamps = [max(5, int(duration * p / 100)) for p in [5, 25, 50, 75]]
    print(','.join(str(t) for t in timestamps))
" > yt_session_timestamps.txt

    TIMESTAMPS=$(cat yt_session_timestamps.txt)
    IFS=',' read -ra TS_ARRAY <<< "$TIMESTAMPS"

    for i in "${!TS_ARRAY[@]}"; do
        T=${TS_ARRAY[$i]}
        END=$((T + 3))
        # Download a 3-second clip at this timestamp (lowest quality, no full download)
        yt-dlp -f "worst[ext=mp4]/worst" \
          --download-sections "*${T}-${END}" \
          -o "yt_session_clip_${i}.%(ext)s" \
          "VIDEO_URL" 2>/dev/null || true
        CLIP=$(ls yt_session_clip_${i}.* 2>/dev/null | head -1)
        if [ -n "$CLIP" ]; then
            ffmpeg -i "$CLIP" -vframes 1 "yt_session_frame_${i}.jpg" -y 2>/dev/null || true
        fi
    done

    echo "FRAMES_DONE"
else
    echo "FRAMES_SKIPPED: duration=${DURATION}s, ffmpeg=$(command -v ffmpeg &>/dev/null && echo found || echo missing)"
fi
```

If output is `FRAMES_DONE`, **Glob** `yt_session_frame_*.jpg` and **Read** each. For each note: what is shown (editor, terminal, browser, slides, presenter); which chapter/timestamp it maps to; any text, commands, settings, UI, or file content visible. If `FRAMES_SKIPPED`, note it and move on.

## Phase 7: Comprehensive Analysis → Action Report

Synthesize all sources:

| Source | What to extract |
|--------|----------------|
| **Title** | Topic signals, specific claim or promise |
| **Description** | Chapters/timestamps, tools/links referenced, sponsor sections |
| **Chapters** | Exact structure — what's covered and where |
| **Comments** | What viewers valued (most liked), recurring questions, timestamps called out, whether the advice worked |
| **Transcript** | Actual spoken content, verbatim quotes, exact steps and commands |
| **Thumbnail** | Visual positioning, topic signal, what's emphasized |
| **Key frames** | What's demonstrated on screen — code, UI, terminal, configs |

Produce the report. Be direct and opinionated — a briefing, not a summary.

```
## What this is about
[1 sentence — topic and the speaker's specific angle or claim]

## The core idea
[2–4 sentences — what they recommend and the reasoning]

## Video structure
[Chapter list if chapters exist, otherwise a 3–5 point outline. Include timestamps.]

## Actionable steps
1. [Specific and concrete — include exact commands, prompts, settings, file content.]
2. ...
[Number every step. Verbatim content goes here, not paraphrases.]

## Things you can copy directly
[Exact prompts, configs, commands, settings, file structures, scripts. Verbatim. If nothing is copyable, say so.]

## What the viewers said
[Top comment themes by like count — what resonated, recurring questions, whether people confirm it works, timestamps called out as must-watch. Note comment volume as engagement signal.]

## Is this worth doing?
[Honest assessment: effort, expected benefit, whether the advice is solid or shallow, better alternatives, fit to your setup. Factor in viewer reception.]

## Watch out for
[Prerequisites, sponsor sections to skip, caveats glossed over, things that may not apply, downsides]

## Resources & links
[Tools, docs, repos, prompts, external links from the description. Skip social/subscribe links.]
```

## Phase 8: Save to Disk

Generate the filename as a single bash block:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
TODAY=$(date +%Y-%m-%d)
SLUG=$(PYTHONUTF8=1 $PYTHON -c "
import re, json, glob
files = glob.glob('yt_session*.info.json')
if files:
    with open(files[0], encoding='utf-8') as f:
        title = json.load(f).get('title', 'untitled')
else:
    title = 'untitled'
slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
print(slug)
")
echo "${TODAY}_${SLUG}.md" > yt_session_filename.txt
cat yt_session_filename.txt
```

Read the filename, create the output dir, then **Write** the report:

```bash
mkdir -p "research/youtube"
```

Write to `research/youtube/[filename]`:

```markdown
---
title: VIDEO_TITLE
url: VIDEO_URL
date: TODAY
duration: VIDEO_DURATION
uploader: VIDEO_UPLOADER
upload_date: UPLOAD_DATE
views: VIEW_COUNT
likes: LIKE_COUNT
mode: high
---

# VIDEO_TITLE

**URL:** VIDEO_URL | **Duration:** VIDEO_DURATION | **Channel:** VIDEO_UPLOADER
**Uploaded:** UPLOAD_DATE | **Views:** VIEW_COUNT | **Likes:** LIKE_COUNT

## What this is about
[from Phase 7]

## The core idea
[from Phase 7]

## Video structure
[from Phase 7]

## Actionable steps
[from Phase 7]

## Things you can copy directly
[from Phase 7]

## What the viewers said
[from Phase 7]

## Is this worth doing?
[from Phase 7]

## Watch out for
[from Phase 7]

## Resources & links
[from Phase 7]

---

## Description

[full description from Phase 4]

---

## Top Comments

[top 20 comments with like counts and authors from Phase 4]

---

## Full Transcript

[full timestamped transcript from yt_session_out.txt]
```

Tell the user the full save path.

## Phase 9: Cleanup

```bash
rm -f yt_session*.info.json yt_session*.vtt yt_session*.jpg yt_session*.webp \
  yt_session*.png yt_session_meta.txt yt_session_out.txt yt_session_timestamps.txt \
  yt_session_filename.txt yt_session_clip_* yt_session_frame_*.jpg yt_session_audio.*
```

The saved `.md` in `research/youtube/` is kept permanently.

## High-Mode Error Reference

| Error | Solution |
|-------|----------|
| yt-dlp not found | Install via winget/brew/pip (Phase 1) |
| Download fails unexpectedly | Run `yt-dlp -U` — YouTube API changes break old versions |
| No subtitles after both attempts | Offer Whisper (Phase 5b) |
| Private / age-restricted | Cannot bypass — inform user and stop |
| info JSON missing after Phase 3 | Phase 3 failed — check yt-dlp error output and rerun |
| `NO_VTT_FOUND` in conversion | Phase 5 retry should have found something — check `ls yt_session*` |
| Whisper install fails | Install ffmpeg first: `winget install Gyan.FFmpeg` (Windows) |
| `python3` not found | Detection falls back to `python` automatically |
| `FRAMES_SKIPPED` | Normal — video too long or ffmpeg missing; thumbnail still gives visual context |
| `[No comments fetched]` | Rate-limited or comments disabled — proceed without viewer reception |
| Phase 4 output contains a bash error | `$PYTHON` resolved empty — keep detection and invocation in the same bash block |

---

# LOW MODE (-l)

Fast, minimal analysis: transcript + basic metadata, clean brief. No comments, no thumbnail, no frame extraction. Use when the topic is clear and you don't need community context or visual verification.

## Phase 1: Check & Update yt-dlp

```bash
command -v yt-dlp
```
Install if missing (winget / pip / brew — see High Mode Phase 1), then `yt-dlp -U`.

## Phase 2: Detect Playlist or Channel URLs

Check URL for `/playlist?`, `/@`, `/channel/`, `/c/`. If any match, stop with the single-video message.

## Phase 3: Fetch Metadata & Subtitles

```bash
yt-dlp \
  --write-info-json \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en.*,a.en" \
  --skip-download \
  --output "yt_session" \
  "VIDEO_URL"
```

No `--write-comments`, no `--write-thumbnail` — keeps this fast. If the command fails entirely, inform the user and stop.

## Phase 4: Parse Metadata

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
PYTHONUTF8=1 $PYTHON -c "
import json, glob, sys

files = glob.glob('yt_session*.info.json')
if not files:
    print('ERROR: info JSON not found')
    sys.exit(1)

with open(files[0], encoding='utf-8') as f:
    info = json.load(f)

print('Title: ' + str(info.get('title', 'Unknown')))
print('Uploader: ' + str(info.get('uploader', 'Unknown')))
print('Duration: ' + str(info.get('duration_string', 'Unknown')))
print('Duration_secs: ' + str(info.get('duration', 0)))

print()
print('=== DESCRIPTION ===')
desc = (info.get('description') or '').strip()
if desc:
    print(desc[:2000])
    if len(desc) > 2000:
        print('...[truncated]')
else:
    print('[No description]')
" > yt_session_meta.txt 2>&1
```

Read with the **Read tool**. If `ERROR: info JSON not found`, Phase 3 failed — stop.

## Phase 5: Check for Subtitles

**Glob** `yt_session*.vtt`. If found → Phase 5a. If not, retry without the language filter:
```bash
yt-dlp --write-subs --write-auto-subs --skip-download --output "yt_session" "VIDEO_URL"
```
Glob again. Still nothing → Phase 5b.

## Phase 5a: Convert VTT → Readable Text

Use the identical VTT-to-text conversion block from **High Mode Phase 5a**, writing to `yt_session_out.txt`, then Read it.

## Phase 5b: Whisper Fallback (Last Resort)

Only if Phase 5 produced no VTT. Requires explicit user confirmation:
> "No subtitles found. I can transcribe the audio locally with Whisper (GPU if available, else CPU). First install pulls the faster-whisper package. Proceed?"

If confirmed, use the identical Whisper block from **High Mode Phase 5b** (writes `yt_session_audio.vtt`), then proceed to Phase 5a.

## Phase 6: Analysis → Brief Report

Read the transcript and description. Keep it tight:

```
## What this is about
[1 sentence — topic and the speaker's specific angle]

## Key points
- [bullet per main idea — specific, not vague]
- ...
[Include exact commands, numbers, or steps if present.]

## Things to copy directly
[Verbatim only: commands, prompts, configs, formulas, settings. If nothing, write "None."]
```

No comments section, no "is this worth doing", no visual analysis.

## Phase 7: Save to Disk

Generate the filename (same block as High Mode Phase 8), create `research/youtube/`, then **Write** to `research/youtube/[filename]`:

```markdown
---
title: VIDEO_TITLE
url: VIDEO_URL
date: TODAY
duration: VIDEO_DURATION
uploader: VIDEO_UPLOADER
mode: low
---

# VIDEO_TITLE

**URL:** VIDEO_URL | **Duration:** VIDEO_DURATION | **Channel:** VIDEO_UPLOADER

## What this is about
[from Phase 6]

## Key points
[from Phase 6]

## Things to copy directly
[from Phase 6]

---

## Full Transcript

[full timestamped transcript]
```

Tell the user the save path.

## Phase 8: Cleanup

```bash
rm -f yt_session*.info.json yt_session*.vtt yt_session*.jpg yt_session*.webp \
  yt_session*.png yt_session_meta.txt yt_session_out.txt \
  yt_session_filename.txt yt_session_audio.*
```

## Low-Mode Error Reference

| Error | Solution |
|-------|----------|
| yt-dlp not found | Install via winget/brew/pip (Phase 1) |
| Download fails | Run `yt-dlp -U` |
| No subtitles | Offer Whisper (Phase 5b) |
| Private / age-restricted | Cannot bypass — inform user and stop |
| info JSON missing | Phase 3 failed — check yt-dlp output |
| `python3` not found | Detection falls back to `python` |
