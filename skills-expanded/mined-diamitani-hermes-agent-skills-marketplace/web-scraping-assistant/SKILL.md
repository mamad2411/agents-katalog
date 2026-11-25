---
name: web-scraping-assistant
description: "Use when helping build and use web scrapers, particularly on the Apify platform. Guides scraper construction and data extraction workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-scraping, apify, data-extraction, crawlers, automation]
---

# Web Scraping Assistant

## Overview

Guide for building, configuring, and running web scrapers with a focus on the Apify platform. Covers the full scraping lifecycle: identifying target data, selecting the right actor/tool, configuring extraction rules, handling pagination and anti-bot measures, and exporting structured data. Also covers general scraping best practices applicable outside Apify.

## When to Use

- "Scrape [website] for [data type]" — targeted data extraction
- "Set up an Apify actor to..." — Apify platform configuration
- "I need to extract product listings from..." — e-commerce scraping
- "Build a crawler that monitors..." — recurring/automated scraping
- "How do I handle pagination/infinite scroll/login walls" — scraping challenges

**Don't use for:** API integration (use the API if available), simple one-off curl requests, or downloading single files.

## How It Works

**1. Target Assessment → 2. Tool Selection → 3. Scraper Configuration → 4. Data Extraction → 5. Export & Validate**

## Steps

### 1. Assess the Target
- Inspect the target website: is the data in HTML, rendered by JS, or behind a login?
- Check for `robots.txt` and terms of service — respect scraping policies
- Determine data volume (single page vs. multi-page crawl vs. sitemap)

### 2. Select the Right Tool
- **Apify actors** (pre-built scrapers): Web Scraper, Puppeteer Scraper, Cheerio Scraper
- **Custom Apify actors** when pre-built actors don't fit
- **Standalone scripts** (Python + BeautifulSoup/Scrapy, Node + Puppeteer/Playwright) for one-off local scraping

### 3. Configure the Scraper
- Define start URLs and link selectors for crawling
- Write extraction rules: CSS selectors, XPath, or JSON-LD for structured data
- Configure request delays (respect rate limits: 1-5 second delays)
- Set up proxy rotation for large-scale scraping
- Handle dynamic content: wait for selectors, scroll triggers, click interactions

### 4. Extract & Transform Data
- Map extracted fields to a clean output schema
- Handle missing fields gracefully (default to null, not errors)
- Clean data: strip whitespace, normalize dates, validate formats
- Deduplicate results based on unique identifiers

### 5. Export & Validate
- Export to JSON, CSV, JSONL, or push to a database/webhook
- Spot-check output for completeness and accuracy
- Set up scheduling if this is a recurring scrape

## Common Pitfalls

1. **Ignoring robots.txt and rate limits.** Aggressive scraping gets IPs blocked. Always add delays and respect crawl-delay directives. On Apify, use the built-in proxy and rate-limiting features.

2. **Brittle CSS selectors.** Sites change layouts. Prefer data attributes, semantic selectors (`[data-testid]`, `[itemprop]`), or JSON-LD structured data over brittle class chains like `.div > div > div > span`.

3. **Not handling JavaScript rendering.** Many modern sites load data via XHR/fetch. If you're not seeing expected content with Cheerio (static HTML), switch to Puppeteer/Playwright for JS-rendered pages.

4. **No error handling for missing fields.** A single missing element shouldn't crash the entire scrape. Wrap each field extraction in try/except or use optional chaining.

5. **Scraping when an API exists.** Always check the Network tab first — many sites serve data via internal JSON APIs that are easier and more reliable to call directly than parsing HTML.
