---
name: anycrawl-crawl
description: |
  Bulk extract content from an entire website or site section. Use when the user wants to crawl a site, extract all pages from a docs section, bulk-scrape multiple pages following links, or says "crawl", "get all the pages", "extract everything under /docs", or "bulk extract".
allowed-tools:
  - Bash(anycrawl *)
  - Bash(npx anycrawl *)
---

# anycrawl crawl

Bulk extract content from a website. Crawls pages following links up to a depth/limit.

## When to use

- You need content from many pages on a site (e.g., all `/docs/`)
- You want to extract an entire site or section — use `crawl` directly

## Quick start

```bash
# Crawl and wait for completion
anycrawl crawl "https://example.com" --wait -o .anycrawl/crawl.json

# With progress indicator
anycrawl crawl "https://example.com" --wait --progress -o .anycrawl/crawl.json

# Limit pages and scope
anycrawl crawl "https://example.com" --include-paths /docs --limit 50 --wait -o .anycrawl/crawl.json

# Check status of a running crawl
anycrawl crawl <job-id>

# Cancel a crawl
anycrawl crawl cancel <job-id>
```

## Options

| Option                    | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| `--wait`                  | Wait for crawl to complete before returning                 |
| `--progress`              | Show progress while waiting                                 |
| `--limit <n>`             | Max pages to crawl                                          |
| `--max-depth <n>`         | Max link depth to follow                                    |
| `--include-paths <paths>` | Only crawl URLs matching these paths                        |
| `--exclude-paths <paths>` | Skip URLs matching these paths                              |
| `--scrape-paths`          | Only scrape content for matching paths                      |
| `--strategy`              | Crawl strategy                                              |
| `--engine`                | auto (default, recommended), playwright, cheerio, puppeteer |
| `-o, --output <path>`     | Output file path                                            |
| `--pretty`                | Pretty print JSON output                                    |

## Tips

- Always use `--wait` when you need the results immediately. Without it, crawl returns a job ID for async polling.
- Use `--include-paths` to scope the crawl — don't crawl an entire site when you only need one section.

## See also

- [anycrawl-scrape](../anycrawl-scrape/SKILL.md) — scrape individual pages
- [anycrawl-map](../anycrawl-map/SKILL.md) — discover URLs before deciding to crawl
- [anycrawl-search](../anycrawl-search/SKILL.md) — find pages on a topic
