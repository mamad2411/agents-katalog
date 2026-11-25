---
name: steel-browse
description: "Browse the web using Steel Browser API at {{STEEL_HOST}}:{{STEEL_PORT}}. Full session management, anti-detection, proxy support, and CAPTCHA solving for AI agents."
metadata:
  openclaw:
    emoji: "🔥"
---

# Steel Browser Skill

Steel Browser provides a powerful API at `http://{{STEEL_HOST}}:{{STEEL_PORT}}` for AI agent web automation.

## Create a Session

```bash
curl -X POST http://{{STEEL_HOST}}:{{STEEL_PORT}}/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"blockAds": true, "sessionTimeout": 1800000}'
```

## Scrape a Page

```bash
curl -X POST http://{{STEEL_HOST}}:{{STEEL_PORT}}/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "waitFor": 2000}'
```

## Take a Screenshot

```bash
curl -X POST http://{{STEEL_HOST}}:{{STEEL_PORT}}/v1/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "fullPage": true}'
```

## Convert to Markdown

```bash
curl -X POST http://{{STEEL_HOST}}:{{STEEL_PORT}}/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "format": "markdown"}'
```

## Connect with Puppeteer

```javascript
const browser = await puppeteer.connect({
  browserWSEndpoint: `ws://{{STEEL_HOST}}:{{STEEL_PORT}}?sessionId=${sessionId}`
});
const page = await browser.newPage();
await page.goto('https://example.com');
```

## Key Features

- **Session Management**: Persistent browser sessions with cookies and storage
- **Anti-Detection**: Built-in stealth plugins and fingerprint management
- **Proxy Support**: Rotate IPs per session for scraping at scale
- **CAPTCHA Solving**: Auto-solve CAPTCHAs without manual intervention
- **Multiple Formats**: Get pages as HTML, markdown, PDF, or screenshots
- **CDP Compatible**: Connect with Puppeteer, Playwright, or Selenium

## Tips

- Use sessions for multi-step workflows (login, navigate, extract)
- Enable ad blocking for faster page loads
- Use the markdown endpoint for clean text extraction for LLM processing
- Set session timeouts to auto-cleanup abandoned sessions
