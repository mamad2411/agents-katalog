---
name: flyscrape
description: Write and run web scraping scripts with `flyscrape`, the standalone CLI scraper with jQuery-like selectors. Use this skill when the user asks to scrape a site, extract data from HTML, follow pagination, crawl multiple pages, download files, use browser mode, configure selectors, or mentions `flyscrape`, a scraping script, nested scraping, or depth-controlled crawling.
version: 1.0.0
source: local
license: MIT
---

# Flyscrape

Flyscrape is a command-line web scraping tool that uses JavaScript scraping scripts. It's standalone (single binary), supports jQuery-like selectors, and can render JavaScript-heavy pages via headless browser.

## Quick Reference

```bash
flyscrape new script.js    # Create new script from template
flyscrape dev script.js    # Dev mode: watch & re-run on changes (cached)
flyscrape run script.js    # Run the scraper
flyscrape run script.js --url "http://example.com" --depth 3  # Override config via CLI
```

## Script Structure

Every script has two parts: **config** (controls behavior) and **default function** (extracts data).

```javascript
export const config = {
  url: "https://example.com",
  // See references/config.md for all options
};

export default function({ doc, url, absoluteURL, scrape, follow }) {
  // doc - parsed HTML document with jQuery-like API
  // url - the current page URL
  // absoluteURL(path) - converts relative URLs to absolute
  // scrape(url, fn) - nested scraping of linked pages
  // follow(url) - manually follow a link (use with follow: [])
  
  return {
    title: doc.find("h1").text(),
    // Return object becomes JSON output
  };
}
```

## Essential Config Options

| Option | Default | Description |
|--------|---------|-------------|
| `url` | - | Starting URL |
| `urls` | `[]` | Multiple starting URLs |
| `depth` | `0` | How deep to follow links (0 = no following) |
| `follow` | `["a[href]"]` | CSS selectors for links to follow |
| `browser` | `false` | Enable headless Chromium for JS-heavy sites |
| `cache` | - | Set to `"file"` to cache requests |
| `rate` | - | Requests per minute limit |
| `concurrency` | - | Max concurrent requests |

See `references/config.md` for complete configuration reference.

## Query API (jQuery-like)

```javascript
const el = doc.find(".selector");  // Find element(s)
el.text()                          // Get text content
el.html()                          // Get inner HTML
el.attr("href")                    // Get attribute
el.hasAttr("data-id")              // Check attribute exists
el.hasClass("active")              // Check class exists

// Collections
const items = doc.find("li");
items.length()                     // Count
items.first() / items.last()       // First/last element
items.get(0)                       // Element by index
items.map(el => el.text())         // Map to array
items.filter(el => el.hasClass("x")) // Filter elements

// Traversal
el.parent()                        // Parent element
el.children()                      // Direct children
el.siblings()                      // Sibling elements
el.prev() / el.next()              // Adjacent siblings
el.prevAll() / el.nextAll()        // All prev/next siblings
el.prevUntil("selector")           // Siblings until selector
```

See `references/query-api.md` for full API reference.

## Common Patterns

### Follow Pagination
```javascript
export const config = {
  url: "https://example.com/posts",
  depth: 10,
  follow: [".pagination a.next"],
};
```

### Scrape with Browser Mode (JS-heavy sites)
```javascript
export const config = {
  url: "https://spa-site.com",
  browser: true,
  headless: true,
};
```

### Nested Scraping (detail pages)
```javascript
export default function({ doc, scrape, absoluteURL }) {
  const links = doc.find(".product-link");
  
  return {
    products: links.map(link => {
      const detailUrl = absoluteURL(link.attr("href"));
      return scrape(detailUrl, ({ doc }) => ({
        name: doc.find("h1").text(),
        price: doc.find(".price").text(),
      }));
    }),
  };
}
```

### Download Files
```javascript
import { download } from "flyscrape/http";

export default function({ doc, absoluteURL }) {
  doc.find("img").each(img => {
    download(absoluteURL(img.attr("src")), "images/");
  });
  return { downloaded: true };
}
```

### Rate Limiting & Caching (be polite)
```javascript
export const config = {
  url: "https://example.com",
  rate: 30,           // 30 requests/minute
  concurrency: 2,     // Max 2 concurrent
  cache: "file",      // Cache to scriptname.cache
};
```

## Workflow

1. **Create**: `flyscrape new myscript.js`
2. **Develop**: `flyscrape dev myscript.js` - iterates with cached responses
3. **Run**: `flyscrape run myscript.js` - full execution
4. **Output**: `flyscrape run myscript.js --output.file results.json`

## Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| Getting blocked (403) | Add User-Agent header, reduce rate, use `browser: true` |
| Empty results | Check if site needs browser mode, verify selectors |
| Links not followed | Set `depth > 0`, check `follow` selectors |
| Slow performance | Increase `concurrency`, enable `cache: "file"` |

See `references/troubleshooting.md` for detailed solutions.

## Reference Files

- `references/config.md` - Complete configuration options
- `references/query-api.md` - Full Query API documentation  
- `references/recipes.md` - Common patterns and code snippets
- `references/troubleshooting.md` - Problem solving guide
- `examples/` - Ready-to-use example scripts

## External Resources

- Documentation: https://flyscrape.com/docs/getting-started/
- GitHub: https://github.com/philippta/flyscrape
- Examples: https://github.com/philippta/flyscrape/tree/master/examples
