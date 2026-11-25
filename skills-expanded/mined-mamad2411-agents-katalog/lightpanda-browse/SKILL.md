---
name: lightpanda-browse
description: "Browse the web using the ultra-fast LightPanda headless browser at {{LIGHTPANDA_HOST}}:{{LIGHTPANDA_PORT}}. 9x less memory than Chrome. CDP-compatible with Puppeteer."
metadata:
  openclaw:
    emoji: "🐼"
---

# LightPanda Browse Skill

LightPanda is an ultra-fast headless browser available via CDP at `ws://{{LIGHTPANDA_HOST}}:{{LIGHTPANDA_PORT}}`.

## Connection

Connect via Puppeteer or Playwright using the CDP WebSocket endpoint:

```javascript
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://{{LIGHTPANDA_HOST}}:{{LIGHTPANDA_PORT}}"
});
```

## Navigate and Scrape

```javascript
const page = await browser.newPage();
await page.goto('https://example.com');
const title = await page.title();
const content = await page.evaluate(() => document.body.innerText);
```

## Extract Links

```javascript
const links = await page.evaluate(() =>
  Array.from(document.querySelectorAll('a'))
    .map(a => ({ href: a.href, text: a.textContent }))
);
```

## Take Screenshots

```bash
# Via CDP protocol
curl -s http://{{LIGHTPANDA_HOST}}:{{LIGHTPANDA_PORT}}/json/version
```

## Key Advantages

- 9x less memory than Chrome (ideal for parallel scraping)
- 11x faster page loading
- Instant startup (no Chromium boot time)
- Full CDP compatibility (Puppeteer, Playwright)
- Perfect for high-volume scraping and AI agent browsing

## Tips

- Use LightPanda for speed-critical scraping tasks
- Fall back to Browserless or Steel for sites requiring full Chrome compatibility
- Multiple concurrent pages use minimal memory
