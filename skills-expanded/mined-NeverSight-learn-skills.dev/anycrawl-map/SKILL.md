---
name: anycrawl-map
description: |
  Discover and list URLs on a website. Use when the user wants to find pages on a site, list all URLs, see the site structure, or says "map the site", "find the URL for", "what pages are on", or "list all pages".
allowed-tools:
  - Bash(anycrawl *)
  - Bash(npx anycrawl *)
---

# anycrawl map

Discover URLs on a site. Essential when the user knows which site but not which exact page.

## When to use

- You need to find a specific subpage on a large site
- You want a list of URLs before choosing which to scrape
- For full site extraction, use `crawl` directly instead

## Quick start

```bash
# Get all URLs from a site
anycrawl map "https://example.com" -o .anycrawl/urls.txt

# JSON output with limit
anycrawl map "https://example.com" --limit 500 --json -o .anycrawl/urls.json

# Include subdomains
anycrawl map "https://example.com" --include-subdomains -o .anycrawl/urls.txt
```

## Options

| Option                 | Description                          |
| ---------------------- | ------------------------------------ |
| `--limit <n>`          | Max URLs to return (1-50000)         |
| `--include-subdomains` | Include subdomain URLs               |
| `--ignore-sitemap`     | Skip sitemap parsing                 |
| `--use-index`          | Use page cache index (default: true) |
| `-o, --output <path>`  | Output file path                     |
| `--json`               | Output as JSON                       |

## Tips

- **Map + scrape is a common pattern**: use `map` to find URLs, then `scrape` the ones you need.

## See also

- [anycrawl-scrape](../anycrawl-scrape/SKILL.md) — scrape the URLs you discover
- [anycrawl-crawl](../anycrawl-crawl/SKILL.md) — bulk extract instead of map + scrape
- [anycrawl-search](../anycrawl-search/SKILL.md) — find pages when you don't have a URL
