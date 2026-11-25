---
name: demo-web-fetcher
description: >-
  Fetches a URL and summarizes response headers. Use when converting Claude demo skills or
  testing package migration.
metadata:
  priority: 3
  docs: 
---
# Demo Web Fetcher

Claude-style demo skill used as a conversion fixture.

## Instructions

1. Read `references/headers.md` when header interpretation is needed.
2. Run `scripts/fetch_headers.py --url <url>` with CLI flags only.
