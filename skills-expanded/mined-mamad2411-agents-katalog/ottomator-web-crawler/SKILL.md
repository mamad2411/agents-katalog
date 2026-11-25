---
name: ottomator-web-crawler
description: Web crawling, sitemap parsing, recursive link scraping, and HTML-to-Markdown chunking for RAG using Crawl4AI and Ottomator tools. Use when scraping documentation, batch crawling sitemaps, or generating vector chunks.
---

# Ottomator Web Crawler

## Overview
Automated web crawler based on Crawl4AI and Ottomator patterns. Designed for high-speed documentation scraping, parallel sitemap traversal, and hierarchical Markdown chunking.

> [!NOTE]
> For authenticated portals (Instagram, LinkedIn, X), use `agent-reach` with `curl_cffi` instead.

---

## Capabilities & Workflows

### 1. Single Page Scraping
Scrapes a single page and outputs cleaned Markdown.
```bash
python3 ~/.agents/skills/ottomator-web-crawler/scripts/crawl.py --url "https://docs.example.com"
```

### 2. Parallel Sitemap Crawling
Batch crawls all links listed in an XML sitemap using memory-adaptive concurrency.
```bash
python3 ~/.agents/skills/ottomator-web-crawler/scripts/crawl.py --sitemap "https://docs.example.com/sitemap.xml" --max-concurrent 5
```

### 3. Recursive Link Crawling
Crawls internal links starting from a root URL up to a specified depth.
```bash
python3 ~/.agents/skills/ottomator-web-crawler/scripts/crawl.py --url "https://docs.example.com" --recursive --max-depth 2
```

### 4. Hierarchical RAG Chunking
Splits scraped Markdown into header-aligned (`#`, `##`, `###`) chunks under 1,000 characters for vector index insertion.
```bash
python3 ~/.agents/skills/ottomator-web-crawler/scripts/crawl.py --url "https://docs.example.com" --chunk
```

---

## Library References & Examples
The underlying crawler architecture leverages [Crawl4AI](https://github.com/unclecode/crawl4ai).
