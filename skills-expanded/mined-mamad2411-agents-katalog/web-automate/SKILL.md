---
name: web-automate
description: "Drive a real headless browser with Playwright (Python): navigate pages, screenshot, scrape rendered content, and fill/submit forms — with an optional Camoufox stealth backend. Use whenever the user wants to automate, scrape, or screenshot a website programmatically."
license: MIT (Code Buddy original skill)
nativeEngine:
  triggers:
    - scrape
    - scrape the
    - playwright
    - headless browser
    - automate the browser
    - browser automation
    - screenshot the page
    - screenshot the website
    - fill the form
    - crawl
---

# Browser automation with Playwright (Python)

Drive a real browser programmatically with the open-source **playwright** Python
library: navigate, screenshot, scrape JS-rendered content, fill and submit forms.
Work in **visible steps** and verify each result before reporting.

> For one-off, point-and-click control prefer the built-in browser/computer-use
> tools. Use *this* skill when the user wants a **scripted, reproducible** browser
> task (scrape N pages, screenshot a flow, fill a form) written as Python.

## Preflight (extras-tier — lib + browser binary)
```bash
python3 - <<'PY'
try:
    import playwright  # noqa: F401
except ModuleNotFoundError:
    raise SystemExit(
        "playwright not installed. Run `npm run prepare:python:extras` in cowork/ "
        "(installs playwright + fetches the Firefox binary)."
    )
print("playwright OK")
PY
```
If the browser binary is missing at runtime, fetch it once:
`python3 -m playwright install firefox` (honors `PLAYWRIGHT_BROWSERS_PATH`, which
the app points at the bundled `resources/python/<plat>/ms-playwright`).

## Workflow (one step at a time)
1. **Plan** the target URL and the action (screenshot / scrape / form).
2. **Write a short Python script** (heredoc via `bash`) using the **sync** API,
   launching **Firefox headless** with `--no-sandbox` not required for Firefox.
3. **Run it**; capture the artifact (PNG / extracted text).
4. **Verify**: assert the screenshot file is non-empty, or the scraped text is
   non-empty; print a short confirmation.
5. **Report** the artifact path / extracted data and a one-line summary.

## Conventions
- Always run **headless** (`headless=True`) — the app has no display.
- Set a realistic `user_agent` and a viewport; `wait_until="networkidle"` for JS pages.
- Use `page.wait_for_selector(...)` instead of fixed sleeps.
- Always `browser.close()` in a `finally` / context manager.
- Respect the target site's terms; this is for automating sites the user is
  authorized to use, not for bypassing access controls.

## Example — screenshot + scrape a page
```bash
python3 - <<'PY'
import os
from playwright.sync_api import sync_playwright

URL = "https://example.com"
out = "page.png"
with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(URL, wait_until="networkidle")
    title = page.title()
    heading = page.inner_text("h1")
    page.screenshot(path=out, full_page=True)
    browser.close()

assert os.path.getsize(out) > 0, "screenshot is empty"
print(f"title={title!r} h1={heading!r}; wrote {out} ({os.path.getsize(out)} bytes)")
PY
```

## Optional: Camoufox stealth backend
For sites that fingerprint/block automation, **camoufox** (a hardened Firefox)
is a drop-in replacement; install with `prepare:python:extras` then
`python3 -m camoufox fetch`:
```python
from camoufox.sync_api import Camoufox
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
```
Camoufox is optional — plain Playwright Firefox is the default.
