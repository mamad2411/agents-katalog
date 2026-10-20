---
name: browserless-browse
description: "Capture screenshots, scrape web content, and generate PDFs using the headless Chrome instance at {{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}."
metadata:
  openclaw:
    emoji: "🌐"
---

# Browserless Browse Skill

Headless Chrome (Browserless) is available at `http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}` within the Docker network.

## Taking a Screenshot

Capture a full-page or viewport screenshot of any URL:

```bash
# Viewport screenshot
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/screenshot" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "type": "png",
      "fullPage": false
    }
  }' \
  -o /data/output/screenshot.png

# Full-page screenshot
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/screenshot" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "type": "png",
      "fullPage": true
    }
  }' \
  -o /data/output/full_page.png
```

## Generating a PDF

Render a web page to PDF:

```bash
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "format": "A4",
      "printBackground": true,
      "margin": { "top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm" }
    }
  }' \
  -o /data/output/page.pdf
```

## Scraping Page Content

Extract text content or HTML from a page:

```bash
# Get page content via the /content endpoint
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/content" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

## Running Custom JavaScript

Execute arbitrary JavaScript on a loaded page and retrieve the result:

```bash
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/function" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "module.exports = async ({ page }) => { await page.goto(\"https://example.com\"); const title = await page.title(); const links = await page.$$eval(\"a\", els => els.map(e => ({ text: e.textContent, href: e.href }))); return { title, links }; }"
  }'
```

## Waiting for Dynamic Content

Handle SPAs and dynamic pages by waiting for selectors:

```bash
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/screenshot" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/dashboard",
    "waitForSelector": { "selector": "#main-content", "timeout": 10000 },
    "options": { "type": "png", "fullPage": true }
  }' \
  -o /data/output/dashboard.png
```

## Setting Viewport and User Agent

```bash
curl -X POST "http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/screenshot" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "viewport": { "width": 1920, "height": 1080 },
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OpenClaw/1.0",
    "options": { "type": "png" }
  }' \
  -o /data/output/desktop_view.png
```

## Output Patterns

- `/data/output/screenshots/` — captured screenshots
- `/data/output/pdfs/` — generated PDF documents
- `/data/output/scrapes/` — scraped content (HTML/JSON)

## Tips for AI Agents

- Use `waitForSelector` or `waitForTimeout` when scraping SPAs to ensure dynamic content has loaded.
- Prefer `/content` over `/function` for simple HTML extraction; use `/function` only when you need custom JS logic.
- Set realistic viewports (1920x1080 for desktop, 375x812 for mobile) to get accurate visual captures.
- For authenticated pages, pass cookies in the `cookies` array or use the `/function` endpoint with login steps.
- Use `gotoOptions: { waitUntil: "networkidle0" }` for pages with heavy async loading.
- Check Browserless health at `http://{{BROWSERLESS_HOST}}:{{BROWSERLESS_PORT}}/pressure` to monitor concurrency limits.
- Set `blockAds: true` in requests to speed up page loading for scraping tasks.
