---
name: org-daily
description: Run daily automation scripts (ArXiv, HN, Reddit, news, Twitter, agent news). Use when user asks for daily curation or /org-daily.
---

# Daily Organization Skill

Runs broad daily content curation: ArXiv, HN, Reddit, TopHub news, Twitter, and world news feeds.
For an AI-focused synthesis from these outputs, run `/skill ai-brief --skip-fetch` afterwards.

## Usage

```bash
python3 _scripts/org_skill.py --daily
```

## Options

- `-v, --verbose`: Stream each script's output (runs sequentially)
- `-s, --skip s1,s2`: Skip specific scripts

## Scripts

Configured in `_config/pipelines.json` (key: `"daily"`). Current list:
arxiv_digest.py, hn_newsletter.py, reddit_digest.py, tophub_news_simple.py, twitter_capture.py, agent_news.py

To add or remove daily scripts, edit `_config/pipelines.json` — no Python changes needed.

## Output

Notes to `Sources/` with dated filenames (e.g., `Sources/ArXiv Digest - 2026-02-18.md`).
