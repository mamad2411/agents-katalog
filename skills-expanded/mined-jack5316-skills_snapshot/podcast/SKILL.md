---
name: podcast
description: Fetch and curate podcast episodes from RSS feeds. Use when user asks for podcast episodes, audio content, or /podcast.
---

# Podcast Digest Skill

Monitors podcast RSS feeds and creates a digest of recent episodes with AI-curated highlights.

## Usage

```bash
python3 _scripts/podcast_digest.py
```

## Configuration

`_scripts/podcast_feeds.txt` — Format: `Podcast Name | RSS Feed URL`

## Default Podcasts

- Lex Fridman Podcast
- The Joe Rogan Experience

## Output

`Sources/Podcast Digest - YYYY-MM-DD.md` (recent episodes with AI recommendations)
