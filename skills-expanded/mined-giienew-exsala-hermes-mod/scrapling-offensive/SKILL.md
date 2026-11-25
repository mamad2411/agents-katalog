---
name: scrapling-offensive
description: Use when scraping anti-bot sites from the VPS.
tags: [scraping, stealth, cloudflare-bypass, scrapling]
version: 1.0.0
author: Me
---

# Scrapling — Senjata Scraping di VPS

Framework scraping anti-bot (github.com/D4Vinci/Scrapling). Terinstall di KAGIRO 2026-10-01 (v0.4.15, `pip install "scrapling[all]"` + `scrapling install`).

## Kapan dipakai
- Target punya anti-bot / Cloudflare → StealthyFetcher
- Page JS-rendered → DynamicFetcher
- Bulk statis cepat → Fetcher (no browser, impersonate chrome)
- Pengganti firecrawl buat scraping rutin (gratis unlimited, hemat kredit farm)

## CLI (udah di PATH)
```bash
scrapling extract get 'https://target.com' out.md
scrapling extract get URL out.md --css-selector '.content' --impersonate chrome
scrapling extract fetch URL out.md --css-selector X --network-idle   # JS render
scrapling extract stealthy-fetch URL out.html --solve-cloudflare --block-webrtc --hide-canvas
scrapling extract post 'https://api.com/x' out.json --json '{"q":"term"}'
```

## Python API
```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
r = Fetcher.get('https://target.com', impersonate='chrome', proxy='http://user:pass@host:port')
print(r.status, r.css('title::text').get())
r = StealthyFetcher.fetch('https://cf-protected.com', solve_cloudflare=True, headless=True, proxy=PROXY)
r = DynamicFetcher.fetch(url, headless=True, network_idle=True)
```

## Integrasi proxy pool KAGIRO
```python
import urllib.request, json
PROXY_POOL = 'http://user:CHANGE_ME_PASSWORD@127.0.0.1:PORT_PROXY'
def next_proxy(cc=None):
    q = f'{PROXY_POOL}/next' + (f'?cc={cc}' if cc else '')
    return json.loads(urllib.request.urlopen(q, timeout=10).read())
# scrape kena block → next_proxy() → retry dengan proxy baru
```

## Trap & pitfall
- Timeout Fetcher = SECONDS; Dynamic/Stealthy = MILLISECONDS (default 30000ms)
- `solve_cloudflare=True` nambah 5-15 detik — coba dulu tanpa itu (sering lolos cuma pakai impersonate)
- StealthyFetcher = browser asli — batasi concurrent (1-2 instance) di VPS RAM kecil
- `scrapling install` wajib setelah pip install, kalau tidak Dynamic/Stealthy error
- Browser binaries: ~/.cache/ms-playwright — jangan prune
- Python 3.10+ required

## MCP server — konekin ke Hermes via mcporter
Udah TERKONEK live di KAGIRO (config /root/config/mcporter.json, server name: `scrapling`):
```bash
npx mcporter list scrapling              # liat semua tools
npx mcporter call scrapling.bulk_get --args '{"urls":["https://target.com"],"impersonate":"chrome"}' --output json
npx mcporter call scrapling.get --args '{"url":"https://target.com"}'
```
Tools MCP scrapling: `get`, `bulk_get`, `fetch` (JS render), `stealthy_fetch`, `session_open` (session persist: dynamic/stealthy), `session_fetch`. Ad-hoc tanpa config: `mcporter call --stdio "scrapling mcp" ... --name scrapling`. HTTP transport juga ada: `scrapling mcp --http --host 127.0.0.1 --port 8000 --auth-token <tok>` (streamable-http, taruh token di env SCRAPLING_MCP_AUTH_TOKEN biar gak keliatan di ps).
