---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing Toolkit

Test local web applications using Playwright with Python.

## Dependencies

```bash
pip install playwright
playwright install chromium
```

## Decision Tree

1. **Static HTML?** → Read the file directly
2. **Dynamic app?** → Use `scripts/with_server.py` to manage the server
3. **Need screenshots?** → Use Playwright with `page.screenshot()`

## Core Pattern

```python
import asyncio
from playwright.async_api import async_playwright

async def test_app():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("http://localhost:3000")

        # ALWAYS wait for network idle before inspecting
        await page.wait_for_load_state('networkidle')

        # Now safe to inspect
        title = await page.title()
        print(f"Title: {title}")

        # Take screenshot
        await page.screenshot(path="screenshot.png")

        await browser.close()

asyncio.run(test_app())
```

## Server Management (scripts/with_server.py)

The `with_server.py` helper manages server lifecycle:

```bash
# Always check --help first
python scripts/with_server.py --help

# Single server
python scripts/with_server.py \
  --server "npm run dev" \
  --port 5173 \
  -- python my_test.py

# Multiple servers (e.g., frontend + backend)
python scripts/with_server.py \
  --server "npm run dev" --port 5173 \
  --server "python api.py" --port 8000 \
  -- python my_test.py
```

Treat bundled scripts as opaque tools — use `--help` rather than reading source.

## Best Practices

### Always Wait for Load
```python
# CRITICAL: Wait before inspecting DOM
await page.wait_for_load_state('networkidle')

# Or wait for specific element
await page.wait_for_selector('.main-content')
```

### Descriptive Selectors
```python
# Good: role/text/CSS selectors
await page.click('button[role="submit"]')
await page.click('text=Submit')
await page.click('.submit-button')

# Avoid: fragile nth-child selectors
await page.click('div:nth-child(3) > button')  # brittle
```

### Always Close Browser
```python
try:
    # your test code
    pass
finally:
    await browser.close()
```

## Common Operations

### Click and Navigate
```python
await page.click('a[href="/dashboard"]')
await page.wait_for_url('**/dashboard')
await page.wait_for_load_state('networkidle')
```

### Fill Forms
```python
await page.fill('input[name="email"]', 'test@example.com')
await page.fill('input[name="password"]', 'password123')
await page.click('button[type="submit"]')
```

### Extract Content
```python
# Single element
text = await page.inner_text('h1')

# Multiple elements
items = await page.query_selector_all('.list-item')
texts = [await item.inner_text() for item in items]
```

### Console Logging
```python
page.on("console", lambda msg: print(f"Console: {msg.text}"))
```

### Check Visibility
```python
is_visible = await page.is_visible('.error-message')
if is_visible:
    error = await page.inner_text('.error-message')
    print(f"Error: {error}")
```

## Static HTML Testing

For static files, just read them directly — no server needed:

```python
from pathlib import Path
from html.parser import HTMLParser

content = Path("index.html").read_text()
# Parse and analyze
```

Or use Playwright with file:// URL:
```python
await page.goto(f"file://{Path('index.html').absolute()}")
```
