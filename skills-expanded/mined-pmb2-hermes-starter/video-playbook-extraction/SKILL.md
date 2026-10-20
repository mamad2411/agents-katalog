---
name: video-playbook-extraction
description: Extract structured, multi-file playbooks (summary, system architecture, strategies, implementation plan) from long-form educational YouTube videos. Goes beyond simple transcript summaries to produce reusable strategic knowledge.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [youtube, video-content, playbook, extraction, strategy, educational-content, knowledge-management]
    triggers:
      - extract playbook from video
      - pull out the entire playbook
      - get the system from this video
      - save the framework from this video
      - extract every concept from this video
      - watch this and extract the playbook
    related_skills:
      - youtube
      - subagent-driven-development
      - skill-content-audit
      - domain-modeling
---

# Video Playbook Extraction

Systematic extraction of structured strategic knowledge from long-form educational YouTube videos. Produces 4 markdown files that together form a reusable playbook.

## When to Use

User shares a YouTube URL for a strategy/educational video and says any of:
- "Watch this and pull out the entire playbook"
- "Extract every concept and idea"
- "Save it to documents and ingest it"
- "Get the system from this video"
- "I want us to take actions on this"

## Don't Use For

- Short news clips or entertainment (one-line summary is enough)
- Music videos or vlogs (no structured knowledge to extract)
- Videos under 5 minutes (unlikely to contain a full playbook)
- When the user just wants a simple summary (use the `youtube` skill's summary format)

## Output Files

Create 4 numbered markdown files in a dedicated directory (e.g., `playbook/video-title/`):

| File | Contents | Target Size |
|------|----------|-------------|
| `01-summary.md` | Video overview, key themes, framework summary, 10+ bullet takeaways | 3-6K chars |
| `02-system-architecture.md` | Complete system components, data flow, tool stack, platform architecture, costs, entity relationships | 8-16K chars |
| `03-actionable-strategies.md` | Every concrete tactic, methodology, research approach, startup idea, and implementation tactic | 5-10K chars |
| `04-implementation-plan.md` | Step-by-step: what to do first, infrastructure checklist, tools to acquire, deployment sequence | 3-8K chars |

## Workflow

### 1. Extract Metadata

Before fetching the transcript, get the video's title, description, and channel to frame the extraction:

```bash
yt-dlp --print "%(title)s" --print "%(description)s" --print "%(channel)s" --print "%(duration)s" "URL"
```

The description often contains the chapter outline — critical context for the extraction.

### 2. Fetch the Transcript

**Preferred for verbatim extraction: yt-dlp auto-subtitle VTT download** (gives the full original ASR script with exact quotes and numbers, no auth, works even when the JS-runtime warning appears):

```bash
mkdir -p C:/tmp/yt
yt-dlp --write-auto-subs --sub-langs 'en.*' --sub-format vtt --skip-download \
  -o 'C:/tmp/yt/%(id)s' 'URL'
# Writes C:/tmp/yt/<ID>.en-orig.vtt (original ASR, most complete) and <ID>.en.vtt
```

Clean the VTT to plain text (strip `<c>`/timestamp tags, drop `-->` lines, dedupe consecutive repeats — VTT repeats each line across segments):

```python
import re
lines = []
for x in open('C:/tmp/yt/VIDEO_ID.en-orig.vtt', encoding='utf-8').read().splitlines():
    if '-->' in x or not x.strip() or x.strip().isdigit():
        continue
    x = re.sub(r'<[^>]+>', '', x).strip()
    if not lines or x != lines[-1]:
        lines.append(x)
open('C:/Users/<you>/<video>_clean.txt', 'w', encoding='utf-8').write('\n'.join(lines))
```

`youtube-transcript-api` remains a good secondary option:

```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch("VIDEO_ID")
segments = [{"text": seg.text, "start": seg.start, "duration": seg.duration} for seg in transcript]
```

**Fallback path:** If both fail (HTTP 403/429):
1. `yt-dlp --cookies-from-browser firefox` with audio extraction + Whisper (local) or transcription service
2. Tactiq.io via browser for copy-paste of full transcript
3. Description-only extraction using `ytInitialPlayerResponse` from page source

### 3. Read the Full Transcript

Read the full transcript into your context. For large transcripts (>50K chars), chunk into overlapping segments.

**Long-transcript navigation pattern (avoids context flood):** for a 60-minute course, reading the whole script into context is wasteful. Save the cleaned text to a file, then:
- Locate sections by keyword: `rg -n 'upsell|pricing|guarantee' <video>_clean.txt` (or on the raw VTT for line numbers).
- Pull only relevant ranges: `sed -n '4800,5450p' file.vtt | sed -E 's/<[^>]*>//g' | sed -E '/^[[:space:]]*$/d' | awk '!seen[$0]++'`.
- Rough mapping: ~5 VTT lines per second of audio, so a line range ≈ 30-40 lines per video minute; `rg -n '00:MM:'` locates a specific minute.
- Iterate range-by-range (each range ~20-30KB of output is safe), extracting exact scripts/quotes per section instead of one giant dump. This is how the $999-assessment course was transcribed into a 28KB playbook with verbatim scripts in one pass.

### 4. Identify the Playbook Structure

Before writing, identify the structural pattern the video uses:

- **System architecture** — does the speaker describe a multi-component system? (data pipeline → decision layer → action layer)
- **Phased methodology** — is there a step-by-step process? (research → build → test → scale)
- **Tool stack** — specific tools named with reasoning
- **Startup ideas** — explicit business opportunities presented
- **Anti-patterns** — what NOT to do

### 5. Write the 4 Files

Each file is self-standing — written to be read independently:

- **01-summary.md** — Start with a one-paragraph overview, then key themes as subsections, then bullet takeaways. Include the video title, speaker, and format at the top.
- **02-system-architecture.md** — Use tables for the component stack, ASCII/block-style diagrams for data flow, and explicit entity definitions. Quote the speaker on the three requirements/definitions.
- **03-actionable-strategies.md** — Group strategies by theme. Each tactic gets an action verb + outcome. Include timestamps or quote references where possible.
- **04-implementation-plan.md** — Ordered checklist. Separate "what we have" vs "what we need." Include cost estimates and time estimates where known.

### 6. Save and Commit

Save all 4 files to a dedicated directory under the project's `playbook/` folder. Git-add and commit immediately with a message describing the video title and extraction scope.

## Pitfalls

- **Transcript is not always available.** ~30% of YouTube videos have auto-captions disabled. Handle the `TranscriptsDisabled` error gracefully and fall back to description-only extraction.
- **The yt-dlp JS-runtime warning is NOT fatal for subtitles.** "No supported JavaScript runtime could be found" appears on Windows, but `--write-auto-subs --skip-download` still downloads the caption tracks fine. Only audio/video format extraction is affected.
- **MSYS `/tmp` is a trap.** `-o '/tmp/yt/%(id)s'` actually writes to `C:/tmp/yt` on git-bash. Always use explicit `C:/tmp/...` in `-o` paths and read back via `C:/tmp`. `find / -name` scans the whole drive and hangs for minutes; use `ls` on the known directory.
- **Heredocs and nested quotes break inside execute_code's terminal() wrapper.** `python - <<'PY'` and `python -c "..."` with nested double quotes throw SyntaxError because the sandbox re-wraps the command string. Write a `.py` file with write_file and run `python file.py`, or use `sed`/`awk` pipelines.
- **Transcript is single-line joined text.** `read_file` returns the whole thing as one line (line 1). Use Python to read it as a string, not line-by-line.
- **Don't fabricate missing content.** If the video doesn't cover a topic, say "not covered in the video" rather than inventing plausible-sounding details.
- **Multi-reference quotes:** When extracting quotes, verify they're actual statements from the transcript, not interpolations. Mark uncertain attributions.
- **Subagent delegation works but can have file path issues.** When delegating extraction to a subagent, give it the exact Windows absolute path for file reads. MSYS paths (`/c/Users/...`) may not resolve in subagent contexts.
- **Clear temp files** — video audio downloads and transcript JSON are large. Remove them after extraction is complete and commit.

## Verification

- [ ] 4 files created (01 through 04)
- [ ] 01-summary includes video title, speaker, format, duration
- [ ] 02-system-architecture has at least 1 table and 1 flow diagram
- [ ] 03-actionable-strategies lists 5+ concrete tactics
- [ ] 04-implementation-plan has ordered steps with what-we-have/what-we-need
- [ ] No fabricated content — all insights traceable to the transcript
- [ ] Files committed to repo
- [ ] Raw media files cleaned up
