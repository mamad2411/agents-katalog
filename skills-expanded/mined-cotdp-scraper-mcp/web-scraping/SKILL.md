---
name: web-scraping
description: Web scraping toolkit using MCP scraper tools. Invoked when extracting content from web pages, converting HTML to markdown, extracting plain text, or harvesting links from URLs. Provides four specialized tools for different extraction needs with CSS selector filtering, batch operations, and retry logic.
---

# Web Scraping Skill

Toolkit for efficient web content extraction using the scraper MCP server tools.

## When to Use This Skill

- Extracting content from web pages for analysis
- Converting web pages to markdown for LLM consumption
- Extracting plain text from HTML documents
- Harvesting links from web pages
- Batch processing multiple URLs concurrently

## Available Tools

| Tool | Purpose | Best For |
|------|---------|----------|
| `mcp__scraper__scrape_url` | Convert HTML to markdown | LLM-friendly content extraction |
| `mcp__scraper__scrape_url_html` | Raw HTML content | DOM inspection, metadata extraction |
| `mcp__scraper__scrape_url_text` | Plain text extraction | Clean text without formatting |
| `mcp__scraper__scrape_extract_links` | Link harvesting | Site mapping, crawling |

## Tool Usage

### 1. Markdown Conversion (Recommended for LLMs)

Convert web pages to clean markdown format:

```
mcp__scraper__scrape_url(
    urls=["https://example.com/article"],
    css_selector=".article-content",
    timeout=30,
    max_retries=3
)
```

**Response includes:**
- `content`: Markdown-formatted text
- `url`: Final URL (after redirects)
- `status_code`: HTTP status
- `metadata`: Headers, timing, retry info

### 2. Raw HTML Extraction

Get unprocessed HTML for DOM analysis:

```
mcp__scraper__scrape_url_html(
    urls=["https://example.com"],
    css_selector="meta",
    timeout=30
)
```

**Use cases:**
- Extracting meta tags and Open Graph data
- Inspecting page structure
- Getting specific HTML elements

### 3. Plain Text Extraction

Extract readable text without HTML markup:

```
mcp__scraper__scrape_url_text(
    urls=["https://example.com/page"],
    strip_tags=["script", "style", "nav", "footer"],
    css_selector="#main-content"
)
```

**Parameters:**
- `strip_tags`: HTML elements to remove before extraction (default: script, style, meta, link, noscript)

### 4. Link Extraction

Harvest all links from a page:

```
mcp__scraper__scrape_extract_links(
    urls=["https://example.com"],
    css_selector="nav.primary"
)
```

**Response includes:**
- `links`: Array of `{url, text, title}` objects
- `count`: Total links found

## CSS Selector Filtering

All tools support the `css_selector` parameter for targeted extraction.

### Common Patterns

```
# By tag
css_selector="article"

# By class
css_selector=".main-content"

# By ID
css_selector="#article-body"

# By attribute
css_selector='meta[property^="og:"]'

# Multiple selectors
css_selector="h1, h2, h3"

# Nested elements
css_selector="article .content p"

# Pseudo-selectors
css_selector="p:first-of-type"
```

### Example: Extract Open Graph Metadata

```
mcp__scraper__scrape_url_html(
    urls=["https://example.com"],
    css_selector='meta[property^="og:"], meta[name^="twitter:"]'
)
```

## Batch Operations

Process multiple URLs concurrently by passing a list:

```
mcp__scraper__scrape_url(
    urls=[
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ],
    css_selector=".content"
)
```

**Response structure:**
```json
{
    "results": [...],
    "total": 3,
    "successful": 3,
    "failed": 0
}
```

Individual failures don't stop the batch - each result includes success/error status.

## Retry Behavior

All tools implement exponential backoff:

- **Default retries**: 3 attempts
- **Backoff schedule**: 1s → 2s → 4s
- **Retryable errors**: Timeouts, connection errors, HTTP errors

Override defaults when needed:

```
# Quick fail for time-sensitive scraping
mcp__scraper__scrape_url(
    urls=["https://api.example.com/data"],
    max_retries=1,
    timeout=10
)

# Patient scraping for unreliable sources
mcp__scraper__scrape_url(
    urls=["https://slow-site.com"],
    max_retries=5,
    timeout=60
)
```

## Workflow Examples

### Extract Article Content

```
# Get main article as markdown
mcp__scraper__scrape_url(
    urls=["https://blog.example.com/post"],
    css_selector="article.post-content"
)
```

### Scrape Product Information

```
# Get product details
mcp__scraper__scrape_url_text(
    urls=["https://shop.example.com/product/123"],
    css_selector=".product-info, .price, .description"
)
```

### Map Site Navigation

```
# Extract all navigation links
mcp__scraper__scrape_extract_links(
    urls=["https://example.com"],
    css_selector="nav, footer"
)
```

### Batch Research

```
# Process multiple sources
mcp__scraper__scrape_url(
    urls=[
        "https://source1.com/article",
        "https://source2.com/report",
        "https://source3.com/analysis"
    ],
    css_selector="article, .main-content, #content"
)
```
