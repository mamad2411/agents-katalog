---
name: cctv-news-scraper
description: Scrape today's CCTV Xinwen Lianbo (新闻联播) daily news summary from EastMoney (东方财富网). Use when the user asks to get today's 新闻联播 content, CCTV news summary, or wants to fetch the latest 央视新闻联播要闻集锦 article. Triggers on requests mentioning 新闻联播, xinwen lianbo, CCTV news digest, or EastMoney news scraping.
---

# CCTV News Scraper

Scrape the daily CCTV 新闻联播要闻集锦 (Xinwen Lianbo News Highlights) article from EastMoney using Playwright.

## Prerequisites

Ensure the environment has:
```
pip install playwright
playwright install chromium
```

## Usage

Run the bundled script to fetch today's news:

```bash
python scripts/scrape_eastmoney.py
```

Options:
- `--date YYYY-MM-DD` — Fetch a specific date's news (default: today)
- `--headless` — Run browser without visible window

The script outputs the article HTML content to stdout. Status messages go to stderr.

## How It Works

1. Opens EastMoney search page with keyword "新闻联播"
2. Searches for an `<a>` tag matching the pattern `{M}月{D}日晚间央视新闻联播要闻集锦`
3. Navigates to the article page
4. Extracts cleaned HTML from `div#ContentBody.txtinfos`, stripping non-essential attributes and videos
5. Splits on `<!--文章主体-->` marker to isolate the main article body

## Troubleshooting

- **No results found**: EastMoney may not have published the article yet (usually available after ~19:30 CST). The page structure may also change over time.
- **Timeout errors**: Network conditions or anti-bot measures may cause delays. Try running without `--headless`.
- **Missing content div**: The article page layout may have changed. Inspect the page manually to verify the selector `div#ContentBody.txtinfos` still exists.
