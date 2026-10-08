---
name: headless-browser
description: Navigate and interact with web pages using a headless browser with full JavaScript support
emoji: 🌐
---

# Headless Browser

Use the `web_browse` tool to open web pages, run JavaScript, click and type into elements, and extract rendered content. Ideal for SPAs and JS-heavy sites where `web_fetch` returns little or no content.

## When to use
- User asks to open a specific URL or "go to" a page
- Site content is loaded by JavaScript and `web_fetch` returns empty or minimal HTML
- User wants to interact with a page (click buttons, fill forms, scroll)
- User needs content that only appears after JS runs (e.g. infinite scroll, modals)

## Tool: web_browse

Single tool with an `action` parameter. Maintains one browser session; use `close` when done to free resources.

### Actions
- **navigate** — Load a URL. Params: `url` (required), optional `wait_ms` (default 2000) for JS to settle.
- **get_content** — Get current page text as markdown. Optional `max_chars` (default 50000).
- **get_html** — Get raw HTML. Optional `max_chars`.
- **click** — Click element by CSS selector. Param: `selector`.
- **type** — Type text into element. Params: `selector`, `text`.
- **js** — Run arbitrary JavaScript. Param: `script`. Use for complex interactions.
- **scroll** — Scroll page. Params: `direction` (down/up), optional `amount` (pixels, default 500).
- **back** / **forward** — Browser history.
- **close** — Close the session. Call when finished to release the browser.

## Workflow
1. `navigate` to the URL (use higher `wait_ms` for heavy SPAs).
2. Optionally `scroll` to load lazy content, then `get_content` or `get_html`.
3. To interact: `click` or `type` with a CSS selector, then `get_content` if the page changed.
4. When done, call `close`.

## Tips
- Prefer `get_content` over `get_html` for summaries; use `get_html` only when structure matters.
- If content is missing, increase `wait_ms` on navigate or scroll first.
- Use simple, robust selectors (e.g. `button.primary`, `#submit`) for click/type.
- Close the session when finished to avoid leaving the browser in use.
