---
name: gsc-indexing-troubleshooter
description: Troubleshoots Google Search Console indexing issues and coverage errors.
---

# Google Search Console Indexing Troubleshooter

Use this skill when the user asks for help with Google Search Console (GSC) indexing issues.

## Core Concepts

1. **URL Inspection Tool**: Always ask the user to run the affected URL through the GSC URL Inspection tool to get the current index status.
2. **Page Indexing Report**: Understand common reasons why pages aren't indexed:
    *   **Discovered - currently not indexed**: Google found the URL but hasn't crawled it yet, often due to site load issues or crawl budget.
    *   **Crawled - currently not indexed**: Google crawled the page but decided not to index it. Could be due to thin content, duplicates, or perceived low quality.
    *   **Excluded by 'noindex' tag**: The page explicitly blocks indexing. Verify if this is intentional.
    *   **Not found (404)**: The URL doesn't exist. Check for broken internal links.
    *   **Server error (5xx)**: Googlebot couldn't access the server. Check server logs and uptime.

## Workflow

1. Identify the specific indexing error reported by GSC.
2. Request the URL(s) affected.
3. Suggest a technical audit of the URL (checking robots.txt, meta robots tags, canonical tags, and server response codes).
4. Provide actionable steps to resolve the issue and request indexing in GSC.
