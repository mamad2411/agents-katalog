---
name: scrape-web
description: >
  Extract data from any website. Scrape tables, lists, articles, products, search results.
  Handle pagination, infinite scroll, login walls. Use when: "scrape", "extract data from",
  "get all products from", "collect data", "download article", "parse table", "crawl",
  "web scraping", "data extraction", "pull data from website".
allowed-tools:
  - mcp__sh__browser_open
  - mcp__sh__browser_navigate
  - mcp__sh__browser_tabs
  - mcp__sh__browser_dom
  - mcp__sh__browser_js
  - mcp__sh__browser_page_info
  - mcp__sh__browser_stealth
  - mcp__sh__browser_wait
  - mcp__sh__browser_click
  - mcp__sh__scroll_with_fallback
  - mcp__sh__screenshot_file
  - mcp__sh__playbook_preflight
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_record_learning
  - mcp__sh__memory_query_patterns
---

# Web Scraping & Data Extraction

You are extracting structured data from websites using ScreenHand's browser automation.

## Intelligence Wrapper

Every tool call returns automatic hints. Watch for:
- **`[HINT]`** — selector suggestions if the domain has a reference file (social platforms, common sites)
- **`[WARNING]`** — this tool has failed before on this domain, includes the fix
- **`[STRATEGY]`** — suggested next step based on past successful scraping sequences

The server auto-loads matching reference files when you navigate to known domains.

## Pre-Flight (MANDATORY)

1. `playbook_preflight(url="{target_url}")` — check for:
   - **RED**: CAPTCHA detected → tell user, abort
   - **YELLOW**: Shadow DOM, SPA detected → adjust strategy
   - **GREEN**: Safe to proceed
2. `browser_stealth()` — ALWAYS call before scraping social media, e-commerce, or news sites
3. `memory_recall(task="scrape {domain}")` — check past strategies
4. `memory_query_patterns(scope="{domain}")` — check verified selectors

## Extraction Strategy (Priority Order)

### 1. Structured Data First (fastest, most reliable)
Check for machine-readable data before scraping the DOM:

```javascript
// JSON-LD
const jsonld = [...document.querySelectorAll('script[type="application/ld+json"]')]
  .map(s => JSON.parse(s.textContent));

// Open Graph
const og = {};
document.querySelectorAll('meta[property^="og:"]')
  .forEach(m => og[m.getAttribute('property')] = m.content);

// Meta tags
const meta = {};
document.querySelectorAll('meta[name]')
  .forEach(m => meta[m.name] = m.content);
```

Use `browser_js` with these expressions. If they return useful data, you're done.

### 2. DOM Extraction (primary method)
Use `browser_dom` with CSS selectors to pull elements:

```
browser_dom(selector="article")           — articles
browser_dom(selector="table tr")          — table rows
browser_dom(selector="[class*='product']") — product cards
browser_dom(selector="h1, h2, h3")        — headings
browser_dom(selector="a[href]")           — all links
```

Start broad, then narrow. `browser_dom` returns text content, attributes, and bounds.

### 3. JavaScript Extraction (for complex/dynamic content)
When DOM is deeply nested or data is in JS variables:

```javascript
// Extract table as JSON
const headers = [...document.querySelectorAll('th')].map(th => th.textContent.trim());
const rows = [...document.querySelectorAll('tbody tr')].map(tr =>
  Object.fromEntries([...tr.querySelectorAll('td')].map((td, i) => [headers[i], td.textContent.trim()]))
);
return JSON.stringify(rows);
```

Use `browser_js(expression=...)`. Always return JSON for clean data.

## Handling Pagination

### Link-based pagination
```
1. browser_dom(selector="a[rel='next'], [aria-label='Next'], .pagination a")
2. If found: browser_click on next link
3. browser_wait for new content to load
4. Extract data from new page
5. Repeat until no next link found
```

### URL-based pagination
```
1. Detect pattern: ?page=1, ?p=2, /page/3, ?offset=20
2. Construct URLs programmatically
3. browser_navigate to each
4. Extract data
5. Stop when page returns no results
```

### Infinite scroll
```
1. Get current height: browser_js("document.body.scrollHeight")
2. Scroll down: scroll_with_fallback or browser_js("window.scrollTo(0, document.body.scrollHeight)")
3. browser_wait for new content (height change or new elements)
4. Extract newly loaded items
5. Repeat until height stops changing (3 attempts with no change = end)
```

## Rate Limiting

- **Minimum 1 second** between page loads
- **Randomize delays** 1-3 seconds for protected sites
- Use `browser_js("await new Promise(r => setTimeout(r, 1500))")` for delays
- If rate limited (429 response): wait 60 seconds, reduce pace

## Output Format

Always structure extracted data as clean JSON arrays:

```json
[
  {"title": "...", "url": "...", "price": "...", "date": "..."},
  {"title": "...", "url": "...", "price": "...", "date": "..."}
]
```

Present the data to the user in a readable format (table or list) and offer to save as JSON/CSV.

## Anti-Detection Best Practices

- `browser_stealth()` at the start
- Random delays between actions
- Don't scrape more than 100 pages in one session
- Vary the scroll speed
- If blocked: try incognito tab, clear cookies via `browser_js`

## Save Knowledge

After successful scraping:
- `memory_record_learning(scope="{domain}", method="browser_dom", pattern="{selector that worked}", confidence=0.9)`
- `memory_save(task="scrape {domain}: {description}")` for the full strategy

$ARGUMENTS
