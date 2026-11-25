---
name: youtube-subtitles
description: >
  Read YouTube videos via subtitles instead of watching them.
  For research, references, and knowledge extraction.
  Triggers when a YouTube URL is shared with intent to extract or summarize its content; NOT for non-YouTube video or audio transcription.
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: youtube-subtitles

## Purpose

Read YouTube videos via subtitles instead of watching them. For
research, references, and knowledge extraction.

## Prerequisite

`yt-dlp` must be installed. If not:

```bash
pip3 install --user --break-system-packages yt-dlp
```

The binary then lives at `~/.local/bin/yt-dlp`.

## Flow

### 1. Download subtitles

```bash
~/.local/bin/yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "/tmp/yt-<topic>" "<youtube-url>"
```

- `--write-auto-sub`: auto-generated subtitles (when no manual
  ones are available).
- `--sub-lang en`: language (adjust as needed, e.g. `de`).
- `--skip-download`: don't download the video.
- Output: `/tmp/yt-<topic>.en.vtt`.

### 2. Clean up and read the subtitles

VTT files have duplicates (every line 3x because of timing
overlaps). Cleanup with Python (awk fails in some shells on
escaping):

```bash
python3 -c "
import re
with open('/tmp/yt-<topic>.en.vtt') as f:
    lines = f.readlines()
seen = set()
out = []
for line in lines:
    line = re.sub(r'<[^>]*>', '', line).strip()
    if line and line[0].isalpha() and line not in seen:
        seen.add(line)
        out.append(line)
with open('/tmp/yt-<topic>-clean.txt', 'w') as f:
    f.write('\n'.join(out))
print(len(out), 'lines')
"
```

Extract a specific time range (e.g. 25:00 to 45:00):

```bash
python3 -c "
import re
with open('/tmp/yt-<topic>.en.vtt') as f:
    content = f.read()
ts = ''
seen = set()
for line in content.splitlines():
    m = re.match(r'(\d{2}:\d{2}:\d{2})', line)
    if m: ts = m.group(1)
    line = re.sub(r'<[^>]*>', '', line).strip()
    if line and line[0].isalpha() and line not in seen and '00:25:00' <= ts <= '00:45:00':
        seen.add(line)
        print(ts, line)
"
```

### 3. Process the content

- Extract core points, summarize, drop into context.
- For reference videos: note relevant passages with timestamps.
- Always cite the source (URL + timestamp).

## Notes

- Auto-generated subtitles have errors (proper names, technical
  terms). Interpret in context.
- `/tmp/` files are volatile — persist relevant excerpts when
  needed.

## Boundary

- No audio transcription (only existing subtitles).
- No video download for other purposes (only subtitles).
- No research workflow (that's research/WORKFLOW.md; here only
  subtitle extraction).
