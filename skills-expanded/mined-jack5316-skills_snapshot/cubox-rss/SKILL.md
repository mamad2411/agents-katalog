---
name: cubox-rss
description: Automate RSS subscription to Cubox. Syncs RSS feeds to Cubox for reading. Use when you want to auto-save RSS items to Cubox, /cubox-rss, or Cubox RSS automation.
---

# Cubox RSS Skill

Automatically sync RSS feed items to Cubox via the [Cubox Open API](https://help.cubox.pro/save/89d3/). Fetches configured RSS feeds and saves each new item as a URL to Cubox. Tracks sent items to avoid duplicates.

## Quick Start

```bash
python3 _scripts/cubox_rss.py
```

## Setup

1. **Enable Cubox API** (Premium feature): Cubox 偏好设置 > 扩展中心和自动化 > API 扩展 > 启用 API 链接
2. **Add to .env**:
   ```
   CUBOX_API_URL=https://cubox.pro/c/api/save/YOUR_API_KEY
   ```
3. **Configure feeds** in `_scripts/cubox_rss_feeds.txt`:
   ```
   Feed Name | RSS URL | Folder (optional)
   ```

## Configuration

**cubox_rss_feeds.txt** — Format: `Feed Name | RSS URL | Folder`

- Folder defaults to "RSS" if omitted
- One feed per line; lines starting with `#` are ignored

Example:
```
Hacker News | https://hnrss.org/frontpage | HN
Lex Fridman | https://lexfridman.com/feed/podcast/ | Podcasts
```

## Usage

Sync all feeds (last 7 days):
```bash
python3 _scripts/cubox_rss.py
```

Only last 3 days:
```bash
python3 _scripts/cubox_rss.py --days 3
```

Preview without saving:
```bash
python3 _scripts/cubox_rss.py --dry-run
```

List configured feeds:
```bash
python3 _scripts/cubox_rss.py --list
```

## Options

- `--days N`: Only sync items from last N days (default: 7)
- `--dry-run`: Preview what would be saved without calling API
- `--list`: List configured feeds and exit

## Output

- **Terminal**: Progress for each feed, count of saved/skipped items
- **Cubox**: Each new RSS item saved as a URL with title, description, and folder
- **Log**: `_logs/cubox_rss_sent.json` tracks sent URLs to avoid duplicates

## Limits

- Cubox Premium: 500 API calls/day
- Script uses ~1.5s delay between requests to be respectful

## Scheduling

Use `/scheduler` to run automatically (e.g., daily):

```bash
python3 _scripts/scheduler.py add cubox-rss "python3 _scripts/cubox_rss.py" --daily
```
