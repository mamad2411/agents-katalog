---
name: scrapling-scrape
description: Use the Scrapling Docker Service and MCP Server to perform extremely fast, anti-bot adaptive web scraping. Scrapling can bypass Cloudflare Turnstile and dynamically track elements across website redesigns.
---

# Scrapling Web Scraper

Scrapling is a powerful Python framework that acts as an adaptive web scraper. Instead of relying purely on static CSS/XPath selectors that break easily, Scrapling learns page structures and bypasses tough anti-bot protections like Cloudflare.

The OpenClaw environment provides a dedicated Scrapling container service.

## Running the Container
When you start the `scrapling` service, it automatically bounds to port 8000 and runs its built-in MCP server (`uv run scrapling mcp`).

## How to use Scrapling
If you need to extract heavily protected data:
1. Ensure the `scrapling` service is active in your OpenClaw environment.
2. The MCP Server runs on `http://localhost:8000`. Connect to it to execute requests.
3. Alternatively, you can use `run_command` in your terminal to execute `docker exec` against the `openclaw-scrapling` container. For example: `docker exec openclaw-scrapling scrapling extract get 'https://example.com' output.md`.

### Python Script Execution
If you need complex crawling, write a python script dynamically and mount/copy it to the container to run it:

```python
from scrapling.spiders import Spider, Response
from scrapling.fetchers import StealthySession

class DemoSpider(Spider):
    name = "demo"
    start_urls = ["https://quotes.toscrape.com/"]

    def configure_sessions(self, manager):
        manager.add("stealth", StealthySession(headless=True, solve_cloudflare=True))

    async def parse(self, response: Response):
        for item in response.css('.quote', auto_save=True):
            yield {"text": item.css('span.text::text').get()}

DemoSpider().start()
```

### Automatic File Extraction (CLI)
You can simply run the extraction binary via a terminal command:
`docker exec openclaw-scrapling scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' captchas.html --css-selector '#padded_content a' --solve-cloudflare`

## When to use this skill
- When hitting heavy anti-bot walls (Cloudflare Turnstile, DataDome, etc.).
- When page structures change frequently and you need `adaptive=True` selection.
- When performing multi-session, high volume HTTP/3 synchronous crawls instead of slow Playwright rendering.
