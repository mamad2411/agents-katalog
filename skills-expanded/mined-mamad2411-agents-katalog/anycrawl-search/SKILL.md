---
name: anycrawl-search
description: |
  Web search with optional full page content extraction. Use when the user asks to search the web, find articles, research a topic, look something up, discover sources, or says "search for", "find me", "look up". Returns real search results with optional full-page markdown.
allowed-tools:
  - Bash(anycrawl *)
  - Bash(npx anycrawl *)
---

# anycrawl search

Web search with optional content scraping. Returns search results as JSON, optionally with full page content.

## When to use

- You don't have a specific URL yet
- You need to find pages, answer questions, or discover sources
- Use `--scrape` to get full page content directly with search results

## Quick start

```bash
# Basic search
anycrawl search "your query" -o .anycrawl/result.json --json

# Search and scrape full page content from results
anycrawl search "your query" --scrape -o .anycrawl/scraped.json --json
```

## Options

| Option                 | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| `--limit <n>`          | Max number of results (default: 10)                         |
| `--offset <n>`         | Skip results                                                |
| `--pages <n>`          | Number of result pages (1-20)                               |
| `--lang <code>`        | Language code                                               |
| `--country <code>`     | Country code for search                                     |
| `--time-range <range>` | day, week, month, year                                      |
| `--safe-search <n>`    | 0, 1, or 2                                                  |
| `--scrape`             | Also scrape full page content for each result               |
| `--scrape-formats`     | Formats when scraping (default: markdown)                   |
| `--scrape-engine`      | auto (default, recommended), playwright, cheerio, puppeteer |
| `-o, --output <path>`  | Output file path                                            |
| `--json`               | Output as JSON                                              |

## Tips

- `--scrape` fetches full content — don't re-scrape URLs from search results.
- Always write results to `.anycrawl/` with `-o` to avoid context window bloat.
- Naming: `.anycrawl/search-{query}.json` or `.anycrawl/search-{query}-scraped.json`

## See also

- [anycrawl-scrape](../anycrawl-scrape/SKILL.md) — scrape a specific URL
- [anycrawl-map](../anycrawl-map/SKILL.md) — discover URLs within a site
- [anycrawl-crawl](../anycrawl-crawl/SKILL.md) — bulk extract from a site
