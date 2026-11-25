---
name: hn
description: Create Hacker News newsletter digest. Use when user asks for HN digest or /hn.
---

# Hacker News Skill

Curates top stories from Hacker News and creates a digest with AI summaries.

## Usage

```bash
python3 _scripts/hn_newsletter.py [--count N]
```

Default: 15 stories. Use `--count N` to change.

## Output

`Sources/HN Digest - YYYY-MM-DD.md` (category-organized, [[wikilinks]])
