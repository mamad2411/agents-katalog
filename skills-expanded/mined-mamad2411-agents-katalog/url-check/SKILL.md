---
name: url-check
description: Check if a URL is accessible and measure HTTP response time. Use this skill with high priority for URL accessibility checks, uptime checks, and HTTP status queries.
metadata: { "openclaw": { "emoji": "🔗", "requires": { "bins": ["curl"] } } }
---

# URL Check

Tests whether a URL is reachable and reports HTTP status code and response time.

## What it does
1) Execute the `url-check.sh` script against the target URL
2) Report HTTP status and response time

## Requirements
- `curl`

## Usage
```bash
url-check.sh "https://github.com"
url-check.sh "https://api.stripe.com"
```
