---
name: ig-research-scrape
version: 1.0.0
description: |
  Scrape state — runs the Instagram scraper via Chrome DevTools Protocol.
  Requires config.json to exist in the project directory.
  Reads search terms + competitors from config, scrapes engagement data,
  downloads audio, and captures hook screenshots.

allowed-tools:
  - Bash
  - Read
  - Write
---

# Social Research — Scrape State

Scrapes top-performing Instagram posts in a niche. Requires Chrome running with `--remote-debugging-port=9222` and user logged into Instagram.

## Before running

Ensure:
1. Chrome is open with `--remote-debugging-port=9222` flag
2. Instagram is logged in (tab stays open)
3. Config exists at `.ig-research/projects/<project-name>/config.json`

## Run

```bash
node "$CLAUDE_SKILL_ROOT/scripts/scrape.js" <project-name> [sessionId]
# fallback: node ./skills/ig-research/scripts/scrape.js <project-name> --session $SESSION
```

**Important**: Keep the Instagram tab in the foreground (visible, not minimized) while this runs. Chrome throttles background tabs and screenshots will fail.

## What it does

1. Navigates to Instagram hashtag search pages (from config.searchTerms)
2. Scrolls to collect post links
3. Visits each post and extracts: likes, comments, shares, caption, author, post type
4. Pauses video and captures screenshots at 0s, 1s, 2s (reels only)
5. Downloads audio via yt-dlp (reels only)
6. Navigates to competitor profiles (if configured) and repeats
7. Deduplicates and sorts results by engagement
8. Saves `raw-posts.json`

## Output

```
.ig-research/projects/<project-name>/
├── raw-posts.json        # All scraped data, sorted by engagement
├── hook-screenshots/     # First 3 frames of each Reel (jpg)
└── transcripts/          # Audio files (m4a) for transcription
```

## Platform-specific scrapers

- Instagram: `scripts/scrape.js` (default)
- Future: `platforms/<name>/scrape.js`

Override by setting `config.platform` and using the corresponding scraper:

```bash
node "$CLAUDE_SKILL_ROOT/platforms/<platform>/scrape.js" <project-name> --session $SESSION
```
