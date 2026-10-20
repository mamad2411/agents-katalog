---
name: web-anti-crawl-bypass
description: Standard operating procedure for bypassing common web anti-crawl mechanisms (Cloudflare, rate limiting) using ethical and compliant methods. Rotates headers, respects robots.txt, and uses exponential backoff.
---

# Web Anti-Crawl Bypass SOP

Standard operating procedure for bypassing common web anti-crawl mechanisms (Cloudflare, rate limiting) using ethical and compliant methods. Rotates headers, respects robots.txt, and uses exponential backoff.

## When to Use

- User wants to 403
- User wants to 429
- User wants to 503
- Keywords: web, anti-crawl, scraping, cloudflare, http

## Required Parameters

- **target_url** (string): The URL to access that is being blocked by anti-crawl

## Optional Parameters

- **max_retries** (number): Maximum number of retry attempts (default: 5)
- **initial_delay_ms** (number): Initial delay before first retry in milliseconds (default: 1000)

## Output

- **status_code** (number): Final HTTP status code
- **body** (string): Response body content
- **retries_used** (number): Number of retries performed

## Security

- Sandbox level: strict
- Max execution time: 60000ms
- Network whitelist: *
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `check_robots` -> 10 steps -> Exit: `return_success`, `return_retry_result`, `abort_blocked`
