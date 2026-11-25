---
name: amazon-scraper
description: Scrape Amazon product listings with Playwright stealth browser automation. Use when the user asks to scrape, crawl, or extract product data from Amazon (search results, category pages, product listings). Handles Amazon's anti-bot protection by using natural page navigation (clicking "Next" instead of URL manipulation), anti-detection techniques, and human-like browsing behavior.
---

# Amazon Scraper

Scrape Amazon product listings using Playwright with anti-bot evasion.

## Prerequisites

Playwright with Chromium must be installed. If not available, install from the playwright-scraper-skill:

```bash
cd ~/.openclaw/workspace/skills/playwright-scraper-skill && npm install && npx playwright install chromium
```

## Usage

Run the scraper script with `NODE_PATH` pointing to playwright-scraper-skill's node_modules:

```bash
NODE_PATH=~/.openclaw/workspace/skills/playwright-scraper-skill/node_modules \
  node scripts/amazon-scrape.js "<keyword>" --pages <N> [--output <path>] [--delay <ms>]
```

### Parameters

- `<keyword>` (required) — Search term (e.g. "over ear headphones", "mechanical keyboard")
- `--pages <N>` — Number of pages to scrape (default: 5, ~24 products per page)
- `--output <path>` — Save JSON to file instead of stdout
- `--delay <ms>` — Base delay between pages in ms (default: 3000; increase if getting blocked)
- `--no-headless` — Show browser window (debugging)

### Examples

```bash
# Scrape 3 pages of headphones, output to stdout
NODE_PATH=~/.openclaw/workspace/skills/playwright-scraper-skill/node_modules \
  node scripts/amazon-scrape.js "over ear headphones" --pages 3

# Scrape 10 pages, save to file
NODE_PATH=~/.openclaw/workspace/skills/playwright-scraper-skill/node_modules \
  node scripts/amazon-scrape.js "mechanical keyboard" --pages 10 --output keyboards.json

# Slower scraping for heavily protected pages
NODE_PATH=~/.openclaw/workspace/skills/playwright-scraper-skill/node_modules \
  node scripts/amazon-scrape.js "laptop" --pages 5 --delay 5000
```

### Output Format

JSON array of products, each with:

```json
{
  "title": "Product Name",
  "price": "$29.99",
  "rating": "4.5",
  "reviews": "1.2K",
  "asin": "B0XXXXXXXX",
  "link": "https://www.amazon.com/...",
  "image": "https://m.media-amazon.com/...",
  "page": 1
}
```

Progress is logged to stderr; product JSON goes to stdout.

## Key Design Decisions

1. **Use Amazon search page (`/s/`)** — Category pages (`/b/`) don't support pagination
2. **Click "Next" button** to paginate — Direct URL `?page=N` jumps trigger Amazon's anti-bot (returns error page with dog 🐕)
3. **Scroll before extracting** — Amazon lazy-loads product cards; must scroll to render them all
4. **Random delays** between pages — Fixed intervals look robotic; randomized 3-6s delays mimic humans
5. **Anti-detection** — Hide `navigator.webdriver`, fake chrome runtime, realistic UA and headers

## Troubleshooting

- **0 products on later pages** — Increase `--delay` to 5000+; Amazon may be rate-limiting
- **Error/dog page** — Script auto-retries once; if persistent, wait a few minutes and retry
- **CAPTCHA** — Not handled; reduce scraping frequency or use a proxy
