---
name: url-to-md
description: Fetch web pages and output clean, LLM-friendly markdown. Ideal for read-only content extraction, documentation reading, and web scraping. For interactive workflows (click, type, JS eval), use cdp-cli.
---

# Web Content Extraction With url-to-md

## When to Use url-to-md vs cdp-cli

| Capability | url-to-md | cdp-cli |
|-----------|-----------|---------|
| Content extraction (read-only) | ✅ Clean markdown, tag filtering | ⚠️ DOM snapshot unreliable |
| Click, fill forms, press keys | ❌ Read-only | ✅ Full automation |
| JavaScript evaluation | ❌ | ✅ `eval` command |
| Screenshots | ❌ | ✅ |
| Network monitoring | ❌ | ✅ (browser requests only) |
| Console messages | ❌ | ✅ |
| Pair browsing (visible session) | ❌ | ✅ `--cdp-url` |
| Cookie consent handling | ✅ Automatic | ⚠️ Manual JSF link navigation |
| Multi-step interaction workflows | ❌ | ✅ |
| File download/egress | ❌ | ❌ |

**Rule of thumb**: If you only need to read/extract content → `url-to-md`. If you need to interact (click, type, evaluate JS) → `cdp-cli`. For hybrid workflows, use `url-to-md` for extraction steps and `cdp-cli` for interaction steps.

## Instructions

`url-to-md` fetches a URL using a headless browser and converts the page to clean markdown. It handles cookie consent automatically, strips noise with `--clean-content`, and can target specific HTML tags with `--include-tags` / `--remove-tags`.

### Quick Start

```bash
# Basic fetch
url-to-md https://example.com

# Clean extraction (strips nav, footer, header, aside, script, style)
url-to-md --clean-content https://example.com

# Target specific content areas
url-to-md --clean-content --include-tags main https://example.com

# Extract only table bodies (e.g., search results)
url-to-md --clean-content --include-tags tbody 'https://site.com/search?q=...'
```

### Command Reference

```
Usage: url-to-md [options] <url>

Options:
  -o, --output <file>         Write output to file instead of stdout
  --no-links                  Remove webpage links from the output
  --no-images                 Remove images from the output
  --no-gif-images             Remove GIF images from the output
  --no-svg-images             Remove SVG images from the output
  --clean-content             Remove common non-content tags (nav, footer,
                              aside, script, style, header, noscript, canvas)
  --include-tags <tags...>    Include only specific HTML tags and their content
  --remove-tags <tags...>     Remove specific HTML tags from the output
  --wait <seconds>            Seconds to wait for the page to load (default: 1.5)
  --show-browser              Show the browser window (visible mode)
  --mobile                    Use mobile viewport (375x667 - iPhone)
  --tablet                    Use tablet viewport (768x1024 - iPad portrait)
  --desktop                   Use desktop viewport (1920x1080)
  --viewport-width <width>    Set viewport width in pixels (320-1920)
  --viewport-height <height>  Set viewport height in pixels (568-1080)
  --disable-web-security      Disable web security (CORS) - for difficult sites
```

### Common Patterns

**Extract search results / listings**:
```bash
url-to-md --clean-content --include-tags tbody 'https://site.com/search?...'
# Grep for IDs or links in the output
url-to-md ... | grep 'id='
```

**Extract article content**:
```bash
url-to-md --clean-content --include-tags article https://news-site.com/post
```

**Extract documentation**:
```bash
url-to-md --clean-content --include-tags main section https://docs.example.com
```

**Extract with ad removal**:
```bash
url-to-md --clean-content --include-tags article --remove-tags aside nav https://news.com
```

**Save to file for later processing**:
```bash
url-to-md --clean-content --include-tags main -o page.md https://example.com
```

**Debug with visible browser**:
```bash
url-to-md --show-browser --clean-content --include-tags main https://example.com
```

**Slow-loading SPAs**:
```bash
url-to-md --wait 5 --clean-content --include-tags main https://spa-site.com
```

### Tag Filtering Rules

- `--include-tags`: Only content within these tags is processed. Everything else is discarded.
- `--remove-tags`: Removes specific tags from the output. When used with `--include-tags`, removes tags within the included content.
- **Priority**: If a tag appears in both `--include-tags` and `--remove-tags`, `--include-tags` takes precedence.

### Pros

- **Clean output**: Markdown optimized for LLM consumption — no HTML noise
- **Automatic cookie consent**: Handles cookie walls without manual intervention
- **Surgical extraction**: `--include-tags` / `--remove-tags` give precise control
- **Self-contained**: Manages its own browser lifecycle — no manual Chromium startup
- **Viewport control**: Mobile/tablet/desktop viewports for responsive sites
- **Fast**: Default 1.5s wait, adjustable for slow sites

### Cons

- **Read-only**: No clicking, typing, form submission, or JS evaluation
- **No screenshots**: Can't capture visual state
- **No network monitoring**: Can't inspect API calls
- **No file download**: Can't retrieve files (ZIPs, PDFs) from pages
- **No multi-step workflows**: Each call is a fresh page load — can't maintain session state across calls
- **No pair browsing**: Can't connect to a user's visible browser session

### Comparison With fetch_content

`url-to-md` is a local tool (uses your system's Chromium). `fetch_content` is a Pi built-in that fetches via remote service with Gemini fallback. Use `url-to-md` for:
- Sites that need cookie consent or JavaScript rendering
- Precise tag-level extraction control
- Offline/local-first operation

Use `fetch_content` for:
- YouTube transcripts and video analysis
- GitHub repository contents
- Sites that block local bots (falls back to Gemini)
- When you don't have Chromium running
