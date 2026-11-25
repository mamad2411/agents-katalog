---
name: reddit
description: Curate and summarize content from Reddit. Use when user asks for Reddit digest or /reddit.
---

# Reddit Digest Skill

Curates content from configured subreddits and creates a summarized digest.

## Usage

```bash
python3 _scripts/reddit_digest.py
```

## Configuration

`_scripts/subreddits.txt` — subreddits to monitor (one per line)

## Output

`Sources/Reddit Digest - YYYY-MM-DD.md` (theme-organized, [[wikilinks]])
