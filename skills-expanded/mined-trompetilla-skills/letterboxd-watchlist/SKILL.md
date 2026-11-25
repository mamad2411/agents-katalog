---
name: letterboxd-watchlist
description: Scrape a public Letterboxd user's watchlist into a CSV/JSONL list of titles and film URLs without logging in. Use when a user asks to export, scrape, or mirror a Letterboxd watchlist; to build watch-next queues; or to match a watchlist against a local media library.
---

# Letterboxd Watchlist Scraper

Use the bundled script to scrape a **public** Letterboxd watchlist (no auth).

## Script

- `scripts/scrape_watchlist.py`

### Basic usage

```bash
python scripts/scrape_watchlist.py 1980vhs --out watchlist.csv
```

### Output formats

- `--out *.csv` → `title,link`
- `--out *.jsonl` → one JSON object per line: `{ "title": "…", "link": "…" }`

## Notes / gotchas

- Letterboxd usernames are case-insensitive, but must be exact.
- The script scrapes paginated pages: `/watchlist/page/<n>/`.
- Stop condition: first page with **no** `data-target-link="/film/..."` poster entries.
- This is best-effort HTML scraping; if Letterboxd changes markup, adjust the regex in the script.

## Common follow-ups

- Match against a local library: list folders in `/media/movies` and fuzzy-match titles.
- Build a watch-next list: shuffle, filter by decade/genre (requires additional lookups), or prioritize unwatched/rare items.
