---
name: twitter
description: Capture and summarize Twitter content. Use when user asks for Twitter digest or /twitter.
---

# Twitter Capture Skill

Captures content from configured Twitter accounts and creates a digest. Uses public syndication endpoint (no API key).

## Usage

```bash
python3 _scripts/twitter_capture.py [--accounts @a @b] [--hours N]
```

- `--accounts`: Override accounts (default: `_scripts/twitter_accounts.txt`)
- `--hours`: Hours of tweets to fetch (default: 24)

## Configuration

`_scripts/twitter_accounts.txt` — one @handle per line

## Output

`Sources/Twitter Digest - YYYY-MM-DD.md` (topic-grouped, [[wikilinks]])
