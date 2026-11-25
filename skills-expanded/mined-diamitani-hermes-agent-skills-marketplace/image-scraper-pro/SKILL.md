---
name: image-scraper-pro
description: "Use when scraping and extracting relevant images from websites for visual content enhancement."
category: productivity
---

# Image Scraper Pro

Extract relevant images from websites for visual content enhancement.

## Core Capabilities
- **Website Image Extraction**: Identify and extract images from target URLs
- **Relevance Filtering**: Filter by size, format, alt text, and contextual relevance
- **Bulk Collection**: Gather images across multiple pages or product catalogs
- **Format Optimization**: Convert and resize for target platforms
- **Metadata Extraction**: Capture alt text, captions, and source attribution

## Workflow
1. Define target URL(s) and image requirements (size, type, topic)
2. Scrape page for all image elements (img tags, background images, srcsets)
3. Filter by dimensions, file type, and contextual relevance
4. Download qualifying images with proper naming
5. Generate attribution and usage documentation

## Technical Approach
- Parse HTML for `<img>` tags, `<picture>` elements, and CSS backgrounds
- Check `srcset` for responsive image variants
- Filter by minimum dimensions (ignore icons, spacers, tracking pixels)
- Respect `robots.txt` and rate limiting
- Use headless browser for JavaScript-rendered images when needed

## Pitfalls
- Always respect copyright and licensing — check site terms of use
- Don't hotlink — download and host images properly
- Respect `robots.txt` and implement polite scraping delays
- Some sites use CDN image protection — may require alternative approaches
- Never scrape personal images or PII
