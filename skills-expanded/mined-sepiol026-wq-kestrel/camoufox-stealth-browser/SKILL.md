---
name: camoufox-stealth-browser
description: Advanced stealth browser automation and web scraping with anti-bot fingerprint evasion (Cloudflare, DataDome, Akamai, Turnstile).
tags: [browser, camoufox, stealth, scraping, cloudflare, pentest]
---

# Camoufox Stealth Browser & Anti-Bot Evasion

Camoufox is a custom anti-detect browser engine built on Firefox with native C++ fingerprint injection. It spoofs hardware fingerprints, WebGL, Canvas, audio contexts, fonts, and client hints to bypass sophisticated anti-bot systems (Cloudflare 5s challenge, Turnstile, DataDome, Akamai, PerimeterX) without detection.

## Tool Usage: `camoufox_fetch`

Kestrel provides the `camoufox_fetch` tool:
- `url`: target webpage
- `headless`: run in headless stealth mode (default `true`)
- `wait_seconds`: seconds to allow challenge scripts to resolve (default `3.0`)
- `extract_text`: clean extracted text/markdown
- `screenshot_path`: save visual evidence/verification to disk

```json
{
  "url": "https://target-with-cloudflare.com/login",
  "headless": true,
  "wait_seconds": 4.0,
  "screenshot_path": "/tmp/target_cf.png"
}
```

## Python Integration via `code_mode`

When multi-step interaction, clicking, form submission, or session harvesting is required:

### 1. Synchronous Automation:
```python
from camoufox import Camoufox

with Camoufox(headless=True, humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://target.com")
    page.wait_for_load_state("networkidle")
    
    # Fill forms and interact
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")
    
    # Extract cookies / session
    cookies = page.context.cookies()
    print("Session Cookies:", cookies)
```

### 2. Async Automation with Custom Fingerprint:
```python
import asyncio
from camoufox import AsyncCamoufox

async def scrape():
    async with AsyncCamoufox(
        headless=True,
        os="windows",        # "windows", "macos", "linux"
        block_images=True,   # Speed up recon
    ) as browser:
        page = await browser.new_page()
        await page.goto("https://target.com/waf-protected", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        content = await page.content()
        return content

asyncio.run(scrape())
```
