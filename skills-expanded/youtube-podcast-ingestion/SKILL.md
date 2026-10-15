---
name: youtube-podcast-ingestion
description: Ingest YouTube podcasts into your knowledge base — fetch transcripts, split by speaker/chapter, generate summaries, and save to any markdown vault (Obsidian, etc). Use when the user shares a podcast URL, asks to ingest a YouTube interview/episode, or wants to archive spoken long-form content for later reference.
version: 1.0.0
author: Uzair Ansar
license: MIT
metadata:
  hermes:
    tags: [youtube, podcast, transcript, obsidian, knowledge-base, ingestion]
    related_skills: [youtube-content, obsidian, karakeep]
---

# YouTube Podcast Ingestion

Ingest YouTube podcasts, interviews, and long-form spoken content into a structured markdown knowledge base. Extracts transcripts, identifies speakers and chapters, generates summaries, and saves everything as linked markdown files.

## Prerequisites

```bash
pip install youtube-transcript-api
```

Optional but recommended:
```bash
pip install openai  # for AI-powered speaker identification & chaptering
```

## Overview

This skill handles the full pipeline for podcast ingestion:

1. **Fetch** — extract transcript from any YouTube URL (standard, shorts, live, embed, youtu.be)
2. **Chunk** — split long transcripts into manageable segments by time or topic
3. **Structure** — identify speakers, chapters, and key segments
4. **Summarize** — generate per-chapter and full-episode summaries
5. **Save** — write structured markdown to your vault with frontmatter, tags, and backlinks

## When to Use

- User shares a podcast, interview, or long-form YouTube URL
- User says "ingest this podcast" or "save this episode"
- User wants to build a personal knowledge base from spoken content
- User references a podcast episode and wants it searchable in Obsidian

**Don't use for:** Short clips under 5 minutes (use `youtube-content` instead), music videos, or videos without spoken dialogue.

## Quick Start

```bash
# Ingest a podcast episode
python3 scripts/ingest.py "https://youtube.com/watch?v=VIDEO_ID" --vault ~/obsidian-vault/Podcasts

# With speaker identification (requires OpenAI API key)
python3 scripts/ingest.py "URL" --vault ~/obsidian-vault/Podcasts --identify-speakers --api-key $OPENAI_API_KEY

# Just fetch and preview, don't save
python3 scripts/ingest.py "URL" --dry-run
```

## Set Your Vault Path

The `--vault` flag points to **any** directory you choose. Examples:

```bash
# Obsidian vault (iCloud or local)
python3 scripts/ingest.py "URL" --vault ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/MyVault/Podcasts

# Any local folder
python3 scripts/ingest.py "URL" --vault ~/Documents/podcast-notes

# Current directory
python3 scripts/ingest.py "URL" --vault .
```

You can also set a default in `~/.config/youtube-podcast-ingestion/config.yaml`:

```yaml
vault_path: ~/obsidian-vault/Podcasts
```

## The Ingestion Pipeline

### 1. Fetch Transcript

Uses `youtube-transcript-api` to extract the full transcript. Handles:
- Auto-generated and manual captions
- Language fallback (e.g., `--language en,tr`)
- Any YouTube URL format

```bash
python3 scripts/fetch_transcript.py "URL" --timestamps
```

### 2. Detect Chapters

YouTube chapters (if present) are extracted from the video description. If no chapters exist, the script can optionally generate them via AI or use fixed time windows.

**From description (free):**
```bash
python3 scripts/ingest.py "URL" --vault ~/vault --chapters-from-description
```

**AI-generated (requires API key):**
```bash
python3 scripts/ingest.py "URL" --vault ~/vault --generate-chapters --api-key $OPENAI_API_KEY
```

**Fixed windows (free, deterministic):**
```bash
python3 scripts/ingest.py "URL" --vault ~/vault --chunk-minutes 10
```

### 3. Identify Speakers

For multi-speaker podcasts, speaker labels can be inferred from:
- **AI diarization** (best quality, requires API key)
- **Pattern heuristics** (free, catches "Host:" and "Guest:" patterns in transcript)
- **Manual override** via `--speakers "Host Name,Guest Name"`

```bash
python3 scripts/ingest.py "URL" --vault ~/vault --speakers "Lex Fridman,Elon Musk"
```

### 4. Generate Summaries

Summaries are generated at three levels:
- **Episode summary** — 3-5 sentence overview
- **Chapter summaries** — one paragraph per chapter
- **Key quotes** — notable statements with timestamps

AI-powered (default if `--api-key` provided):
```bash
python3 scripts/ingest.py "URL" --vault ~/vault --api-key $OPENAI_API_KEY
```

Template-based (free, no API key):
- Uses simple extractive summarization: first/last sentences of each chapter + longest sentence as key quote

### 5. Save to Vault

Output is a markdown file with YAML frontmatter:

```markdown
---
title: "Podcast Title"
channel: "Channel Name"
date: "2026-05-01"
duration: "2:34:56"
url: "https://youtube.com/watch?v=..."
tags: [podcast, ai, interview]
speakers: ["Lex Fridman", "Elon Musk"]
chapters:
  - title: "Introduction"
    start: "0:00"
    end: "5:30"
    summary: "Host introduces the guest and topics."
---

# Podcast Title

## Episode Summary

[AI or template-generated summary]

## Chapters

### Introduction (0:00 - 5:30)

**Summary:** Host introduces the guest and topics.

**Key Quotes:**
- "..." — Speaker Name (0:45)

**Transcript:**
> [Timestamped transcript excerpt]

---

### [Next Chapter] ...

## Full Transcript

<details>
<summary>Click to expand full transcript</summary>

[Complete transcript with timestamps]

</details>
```

## Configuration

Create a config file at `~/.config/youtube-podcast-ingestion/config.yaml`:

```yaml
vault_path: ~/obsidian-vault/Podcasts
api_key: ${OPENAI_API_KEY}  # env var substitution
model: gpt-4o-mini
default_tags: [podcast, ingested]
chunk_minutes: 15
speaker_detection: heuristic  # heuristic | ai | none
chapter_source: description   # description | ai | fixed
```

Or pass all options as CLI flags — the script never requires a config file.

## CLI Reference

```
usage: ingest.py [-h] [--vault VAULT] [--config CONFIG] [--dry-run]
                 [--tags TAGS] [--api-key API_KEY] [--model MODEL]
                 [--speakers SPEAKERS] [--identify-speakers]
                 [--chapters-from-description] [--generate-chapters]
                 [--chunk-minutes CHUNK_MINUTES] [--language LANGUAGE]
                 url

positional arguments:
  url                   YouTube URL or video ID

options:
  -h, --help            show this help message and exit
  --vault VAULT         Output directory for markdown file (default: current dir)
  --config CONFIG       Path to config YAML
  --dry-run             Print output without saving
  --tags TAGS           Comma-separated tags (default: podcast)
  --api-key API_KEY     OpenAI API key for AI features
  --model MODEL         OpenAI model (default: gpt-4o-mini)
  --speakers SPEAKERS   Comma-separated speaker names
  --identify-speakers   Auto-detect speakers (requires --api-key)
  --chapters-from-description
                        Extract chapters from video description
  --generate-chapters   AI-generate chapters (requires --api-key)
  --chunk-minutes CHUNK_MINUTES
                        Fixed chunk size in minutes (default: 15)
  --language LANGUAGE   Comma-separated language codes (default: en)
```

## Workflows

### Ingest to Obsidian

```bash
python3 scripts/ingest.py "https://youtube.com/watch?v=..." \
  --vault ~/obsidian-vault/Podcasts \
  --tags podcast,ai,interview \
  --chapters-from-description
```

File is saved as `~/obsidian-vault/Podcasts/YYYY-MM-DD-podcast-title.md` with full frontmatter.

### Ingest with AI Summaries

```bash
export OPENAI_API_KEY="***"
python3 scripts/ingest.py "URL" \
  --vault ~/obsidian-vault/Podcasts \
  --generate-chapters \
  --identify-speakers \
  --tags podcast,ai
```

### Batch Ingest a Playlist

```bash
for url in $(cat podcast_urls.txt); do
  python3 scripts/ingest.py "$url" --vault ~/obsidian-vault/Podcasts --chapters-from-description
done
```

### Preview Before Saving

```bash
python3 scripts/ingest.py "URL" --dry-run | head -100
```

## Output Structure

```
~/obsidian-vault/
└── Podcasts/
    ├── 2026-05-01-lex-fridman-elon-musk.md
    ├── 2026-04-28-huberman-sleep.md
    └── .index/
        └── podcast-index.md   # auto-generated backlinks index
```

The optional `.index/podcast-index.md` is updated on each ingestion and links all episodes by tag, channel, and speaker for graph navigation in Obsidian.

## Pitfalls

1. **Transcript disabled:** Some podcasts disable auto-captions. The script exits with a clear error — check if the video has manual subtitles available.

2. **AI costs add up:** For 3-hour podcasts, AI chaptering + speaker ID + summarization can use ~50K tokens. Use `--model gpt-4o-mini` (default) to keep costs low (~$0.03/episode).

3. **YouTube chapters are user-defined:** Not all podcasts have chapters. The `--chapters-from-description` flag falls back to `--chunk-minutes` if no chapters are found.

4. **Speaker identification is heuristic by default:** Without `--api-key`, speakers are guessed from transcript patterns (e.g., "Host:" prefixes). This is often wrong for unstructured conversations. Use `--speakers` for manual override or `--identify-speakers` with an API key.

5. **Large transcripts:** Episodes over 4 hours can produce markdown files >1MB. Obsidian handles them fine, but mobile sync may lag. Use `--chunk-minutes` to split into multiple files if needed.

6. **ASR hallucinations:** Auto-generated transcripts mishear tech names. Common issues documented in `youtube-content` skill apply — "xAI" becomes "SpaceX", product names get mangled. Always spot-check key quotes before citing.

7. **Rate limits:** `youtube-transcript-api` has no explicit rate limit, but bulk ingestion (>50 videos/hour) can trigger IP throttling. Add `sleep 5` between requests in batch scripts.

## Verification Checklist

- [ ] `pip install youtube-transcript-api` installed
- [ ] Target `--vault` directory exists and is writable
- [ ] Episode markdown file created with correct frontmatter
- [ ] Chapters align with actual content (spot-check 2-3 chapters)
- [ ] Key quotes are correctly attributed and timestamped
- [ ] Obsidian graph shows the new node and backlinks
- [ ] `.index/podcast-index.md` updated (if using `--update-index`)
