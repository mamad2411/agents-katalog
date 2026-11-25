---

name: firecrawl
description: firecrawl lets the user scrape, crawl, and map websites into clean markdown, which is useful when they need to extract content from pages, audit site structures, build knowledge bases from web sources, or feed structured web content into AI workflows without broken HTML or layout artifacts.
triggers:
  - scrape this website
  - crawl this site
  - map this domain
  - extract content from
  - get markdown from
  - firecrawl
version: 1.0.0
author: Charles Blair
created: 2026-03-12

---
Reliable web scraping, crawling, and domain mapping via Firecrawl CLI.

## What This Skill Does

This skill firecrawl lets the user scrape, crawl, and map websites into clean markdown, which is useful when they need to extract content from pages, audit site structures, build knowledge bases from web sources, or feed structured web content into AI workflows without broken HTML or layout artifacts.

## What It Does

- **Scrape:** Convert any URL to clean markdown
- **Search & Scrape:** Search the web and scrape top results
- **Crawl:** Recursively crawl an entire website
- **Map:** Generate a complete sitemap of any domain

## Setup (One-Time)

```bash
# Install
npm install -g firecrawl-cli

# Authenticate
firecrawl login --api-key fc-ac68ad954b054301b60dc0e822836158

# Verify (optional)
firecrawl --version
```

## Core Commands

### 1. Scrape a Single Page

```bash
# Basic scrape (full content)
firecrawl scrape https://example.com

# Clean output (main content only, recommended)
firecrawl scrape https://example.com --only-main-content

# Save to file
firecrawl scrape https://example.com --only-main-content > output.md

# Short alias
firecrawl https://example.com --only-main-content
```

### 2. Search & Scrape

```bash
# Search and scrape top results
firecrawl search "real estate investing strategies" --limit 5

# Search and save
firecrawl search "AI automation tools" --limit 10 > search-results.md
```

### 3. Crawl an Entire Website

```bash
# Crawl with default settings (max 100 pages)
firecrawl crawl https://example.com

# Custom page limit
firecrawl crawl https://example.com --limit 50

# Exclude specific paths
firecrawl crawl https://example.com --exclude "/blog/*,/archive/*"

# Include only specific paths
firecrawl crawl https://example.com --include "/docs/*"

# Save crawl results
firecrawl crawl https://example.com --limit 100 > crawl-output.md
```

### 4. Map a Domain

```bash
# Generate complete sitemap
firecrawl map https://example.com

# Save map
firecrawl map https://example.com > sitemap.json

# Map with custom options
firecrawl map https://example.com --include-subdomains
```

## Common Use Cases

### Extract Blog Post Content

```bash
firecrawl scrape https://example.com/blog/post-title --only-main-content
```

### Scrape Competitor Website

```bash
# Get all pages
firecrawl crawl https://competitor.com --limit 200 > competitor-content.md

# Map their structure
firecrawl map https://competitor.com > competitor-sitemap.json
```

### Research & Data Collection

```bash
# Search and scrape multiple sources
firecrawl search "landlord tenant laws Maryland" --limit 10 > md-laws-research.md
```

### Content Audit

```bash
# Map your own domain
firecrawl map https://yoursite.com > audit-sitemap.json

# Crawl and review content
firecrawl crawl https://yoursite.com --limit 500 > content-audit.md
```

## Output Formats

- **Scrape/Crawl:** Returns markdown by default
- **Map:** Returns JSON sitemap structure
- **Search:** Returns markdown with sources

## Advanced Options

```bash
# Custom timeout (seconds)
firecrawl scrape https://slow-site.com --timeout 60

# Follow redirects
firecrawl scrape https://example.com --follow-redirects

# Custom user agent
firecrawl scrape https://example.com --user-agent "CustomBot/1.0"

# Include metadata
firecrawl scrape https://example.com --include-metadata
```

## Workflow Integration

### 1. Scrape → Analyze

```bash
# Scrape competitor page
firecrawl scrape https://competitor.com/pricing --only-main-content > competitor-pricing.md

# (Then use AI to analyze the markdown)
```

### 2. Crawl → Process

```bash
# Crawl entire site
firecrawl crawl https://example.com --limit 100 > site-content.md

# Extract insights with AI
# (Pass site-content.md to analysis tool)
```

### 3. Map → Plan

```bash
# Map domain structure
firecrawl map https://example.com > structure.json

# Use JSON to plan content strategy
```

## Best Practices

1. **Use `--only-main-content`** for cleaner output (removes nav, footer, ads)
2. **Set reasonable limits** on crawls to avoid timeouts
3. **Save to files** for large outputs instead of terminal display
4. **Respect rate limits** — Firecrawl handles this automatically
5. **Use search** when you need multiple sources on a topic

## Troubleshooting

### Authentication Issues

```bash
# Re-authenticate
firecrawl logout
firecrawl login --api-key fc-ac68ad954b054301b60dc0e822836158
```

### Timeout Errors

```bash
# Increase timeout
firecrawl scrape https://slow-site.com --timeout 120
```

### Too Much Output

```bash
# Always save large results to file
firecrawl crawl https://big-site.com --limit 500 > output.md

# Or use --only-main-content to reduce noise
firecrawl scrape https://example.com --only-main-content
```

## When to Use This Skill

✅ **Use Firecrawl when:**
- Extracting content from any website
- Researching competitors or markets
- Building datasets from web sources
- Mapping site structures
- Collecting content for analysis
- Scraping dynamic or JavaScript-heavy sites

❌ **Don't use when:**
- Simple static page fetch is enough (use `curl` or `web_fetch` tool)
- Site explicitly blocks scraping (check robots.txt/terms)
- You need real-time browser interaction (use `browser` tool instead)

## Integration with Other Skills

- **Combine with `brave-search`:** Search first, then scrape top results
- **Combine with `gog` (Google Docs):** Scrape → save to Drive for team review
- **Combine with `apify-runner`:** Use Apify for complex scraping, Firecrawl for quick hits
- **Combine with analysis prompts:** Scrape → analyze with AI

## Quick Reference

```bash
# Single page (clean)
firecrawl https://example.com --only-main-content

# Search & scrape
firecrawl search "query" --limit 10

# Crawl site
firecrawl crawl https://example.com --limit 100

# Map domain
firecrawl map https://example.com
```

---

**Status:** ✅ Installed & Authenticated  
**API Key:** `fc-ac68ad954b054301b60dc0e822836158` (configured)  
**CLI Version:** Latest (global install)
