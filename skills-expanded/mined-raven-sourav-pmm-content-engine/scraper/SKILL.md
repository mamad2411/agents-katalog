# Skill: Newsletter Scraper

Scrape newsletter posts from Substack and Beehiiv publications. No API keys needed.

## Trigger
User wants to scrape, research, or pull posts from a newsletter URL.

## Supported Platforms

### Substack
Any Substack publication (subdomain or custom domain).

```bash
python3 skills/scraper/scripts/scrape_substack.py --url "https://newsletter.substack.com" --days 30 --output summary
python3 skills/scraper/scripts/scrape_substack.py --url "https://www.lennysnewsletter.com" --keywords "AI" --output json
python3 skills/scraper/scripts/scrape_substack.py --url "https://newsletter.substack.com" --full-content --output json
```

### Beehiiv
Any Beehiiv publication (including custom domains).

```bash
python3 skills/scraper/scripts/scrape_beehiiv.py --url "https://www.growthunhinged.com" --days 30 --output summary
python3 skills/scraper/scripts/scrape_beehiiv.py --url "https://www.growthunhinged.com" --keywords "pricing" --output json
python3 skills/scraper/scripts/scrape_beehiiv.py --url "https://www.growthunhinged.com" --full-content --output json
```

## CLI Flags (both scripts)

| Flag | Default | Description |
|------|---------|-------------|
| `--url` | *required* | Newsletter URL |
| `--keywords` | none | Filter by keywords (comma-separated, OR logic) |
| `--days` | all | Only include posts from last N days |
| `--max-posts` | all | Max posts to return |
| `--full-content` | false | Fetch full post body (slower) |
| `--output` | summary | `summary` (table) or `json` |

## How It Works

- **Substack**: Uses public `/api/v1/archive` JSON endpoint. Returns title, subtitle, word count, reactions, comments, tags, author.
- **Beehiiv**: Uses hidden `/posts` JSON endpoint. Returns title, subtitle, tags, reading time, author.

## Dependencies

Only `requests` — install via `pip install requests`.
