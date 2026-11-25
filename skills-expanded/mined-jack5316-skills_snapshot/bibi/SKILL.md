---
name: bibi
description: Summarize videos, audio, and podcasts via BibiGPT CLI. Use when user asks to summarize a video/audio URL or /bibi.
---

# BibiGPT CLI Skill

Summarizes videos, audio files, and podcasts from the terminal using the `bibi` CLI (BibiGPT).

Supports YouTube, Bilibili, podcasts, and other audio/video sources.

## Prerequisites

- BibiGPT Desktop installed: `brew install --cask jimmylv/bibigpt/bibigpt`
- Logged in via the desktop app at least once (or set `BIBI_API_TOKEN` env var)
- Verify: `bibi --version`

## Usage

```bash
# Basic summary (Markdown to stdout)
bibi summarize "<URL>"

# Async mode — for videos longer than ~30 min
bibi summarize "<URL>" --async

# Chapter-by-chapter breakdown
bibi summarize "<URL>" --chapter

# Raw transcript/subtitle only (no AI summarization)
bibi summarize "<URL>" --subtitle

# JSON structured output
bibi summarize "<URL>" --json

# Save to Obsidian vault
bibi summarize "<URL>" > Sources/Bibi\ -\ $(date +%Y-%m-%d).md

# Check auth status
bibi auth check

# Update CLI
bibi check-update
```

## Output

Markdown summary to stdout. Pipe to a file to save as a vault note:
```bash
bibi summarize "<URL>" > "Sources/Bibi - Title - YYYY-MM-DD.md"
```

Error codes: 401 = expired token, 402/403 = quota exceeded, 429 = rate limited.
