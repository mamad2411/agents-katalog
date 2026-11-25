---
name: firecrawl-scrape
description: "Use when the user gives a URL and wants its content: \"scrape\", \"grab\", \"fetch\", \"pull\", \"get the page\", \"extract from this URL\", \"read this webpage\". Returns clean LLM-ready markdown from any page, including JavaScript-rendered SPAs and several URLs at once. Needs the Firecrawl CLI. Prefer it over a plain web fetch for page content."
allowed-tools:
  - Bash(firecrawl *)
  - Bash(npx firecrawl *)
---

# firecrawl scrape

Scrape one or more URLs. Returns clean, LLM-optimized markdown. Multiple URLs are scraped concurrently.

## Requires

Firecrawl is a commercial scraping service (firecrawl.dev). This skill wraps its CLI, so it needs
two things the user configures once, outside this plugin:

- the `firecrawl` CLI available on the path (or reachable via `npx`)
- a Firecrawl account and API key, configured wherever that CLI expects to find it — follow
  Firecrawl's own setup docs; this plugin never reads a key itself

Without both, the skill cannot run. Say so plainly rather than silently degrading to a plain fetch —
a plain fetch loses exactly the content some pipeline steps depend on (see **Raw HTML** below).

## When to use

- You have a specific URL and want its content
- The page is static or JS-rendered (SPA)
- Step 2 in the escalation ladder: search → **scrape** → map → crawl → interact. Only this rung
  ships with the plugin; the others are separate Firecrawl commands you can call directly if you
  have the CLI.

## Quick start

```bash
# Basic markdown extraction
firecrawl scrape "<url>" -o .firecrawl/page.md

# Main content only, no nav/footer
firecrawl scrape "<url>" --only-main-content -o .firecrawl/page.md

# Wait for JS to render, then scrape
firecrawl scrape "<url>" --wait-for 3000 -o .firecrawl/page.md

# Multiple URLs (each saved to .firecrawl/)
firecrawl scrape https://example.com https://example.com/blog https://example.com/docs

# Get markdown and links together
firecrawl scrape "<url>" --format markdown,links -o .firecrawl/page.json

# RAW HTML — required whenever <head> tags or JSON-LD matter
firecrawl scrape "<url>" --format rawHtml -o .firecrawl/page.html

# Ask a question about the page
firecrawl scrape "https://example.com/pricing" --query "What is the enterprise plan price?"
```

## Options

| Option                   | Description                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `-f, --format <formats>` | Output formats: markdown, html, rawHtml, links, screenshot, json |
| `-Q, --query <prompt>`   | Ask a question about the page content (5 credits)                |
| `-H`                     | Include HTTP headers in output                                   |
| `--only-main-content`    | Strip nav, footer, sidebar — main content only                   |
| `--wait-for <ms>`        | Wait for JS rendering before scraping                            |
| `--include-tags <tags>`  | Only include these HTML tags                                     |
| `--exclude-tags <tags>`  | Exclude these HTML tags                                          |
| `--redact-pii`           | Redact personally identifiable information from output           |
| `-o, --output <path>`    | Output file path                                                 |

## Raw HTML — when markdown is a FAIL, not a shortcut

The markdown pipeline strips `<head>` and every `<script type="application/ld+json">` block. For most
jobs that is a feature. For any job whose whole purpose is reading meta tags, canonicals, hreflang or
structured data, it silently deletes the answer and returns a clean-looking file that contains none
of it.

**`/founder-pipeline:founder` P4.S4 (Source Gap) requires `--format rawHtml`.** A markdown-only
extraction at that step is a documented FAIL — not a degraded pass — because the competitor schema
blocks the step exists to diff are exactly what markdown removes. The same applies anywhere else the
task is "what is in their head tag": request raw HTML, and never substitute a plain fetch, since
JS-heavy sites render those blocks client-side and a naive fetch loses them too.

Request `markdown` when you want to *read* a page. Request `rawHtml` when you want to *audit* one.

## Tips

- **Prefer plain scrape over `--query`.** Scrape to a file, then use `grep`, `head`, or read the markdown directly — you can search and reason over the full content yourself. Use `--query` only when you want a single targeted answer without saving the page (costs 5 extra credits).
- **Try scrape before interact.** Scrape handles static pages and JS-rendered SPAs. Only escalate to `interact` when you need interaction (clicks, form fills, pagination).
- Multiple URLs are scraped concurrently — check `firecrawl --status` for your concurrency limit.
- Single format outputs raw content. Multiple formats (e.g., `--format markdown,links`) output JSON.
- Always quote URLs — shell interprets `?` and `&` as special characters.
- Naming convention: `.firecrawl/{site}-{path}.md`

## When scrape isn't the right rung

Scrape is the only rung of the ladder that ships as a skill here. The neighbouring jobs are Firecrawl
CLI commands you call directly — no skill wraps them, so run them inline:

- **You don't have a URL yet** — `firecrawl search "<query>"` returns results you can then scrape.
  Any web search tool works too; the advantage of searching through the same provider is that you can
  pipe straight into a scrape.
- **The content is behind an interaction** (a click, a form, pagination, a cookie wall) — scrape
  can't reach it. `firecrawl interact` drives those steps before extracting. Escalate only after a
  plain scrape has actually failed; interaction is slower and costs more credits.
- **You want a whole site, not a page** — `firecrawl map` lists the URLs, `firecrawl crawl` walks
  them. Set a page cap before you start; an uncapped crawl on a large site is the expensive mistake.
