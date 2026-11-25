---
name: apifox-docs-extraction
description: Scrape Apifox-hosted docs via llms.txt and .md endpoints.
license: MIT
metadata:
  hermes:
    tags:
    - scraping
    - apifox
    - docs
    - markdown
    - openapi
    - llms.txt
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
  imported_from: hermes
---

# Apifox Docs Extraction

## When to Use

Any documentation site hosted by Apifox — detectable by:
- HTML containing `<script src="https://cdn.apifox.com/docs-site/assets/...">` or `__prepareDocsConfigScript`
- URL pattern `https://<host>/<8-char-pageid>` (e.g. `https://api.railgo.dev/366464494e0`)

The rendered pages are interactive React apps; **do not scrape the HTML**. Apifox serves clean full-page Markdown at `.md` endpoints.

## Fastest Path: llms.txt

1. `curl https://<host>/llms.txt` — Apifox auto-generates this with every page as a markdown link:
   `[标题](https://<host>/<pageid>.md)` — often including descriptions.
2. Each `<pageid>.md` returns the complete page: prose docs + the full OpenAPI 3.0.1 YAML spec embedded in a fenced block. No HTML parsing, no JS.

## Enumerate Pages

- `https://<host>/robots.txt` — usually points to the sitemap.
- `https://<host>/sitemap.xml` — full URL list.
- `https://<host>/llms.txt` — best index (has titles + descriptions).

**Dedupe pitfall:** the sitemap often lists the same page multiple times with `?nav=N` query variants (same page under different nav sections). Strip query strings and dedupe by pageid before fetching.

## Workflow

1. Fetch `robots.txt` → `sitemap.xml` → `llms.txt` (probe all three in one batch).
2. Extract unique page IDs (dedupe `?nav=` variants; pageid = path segment, drop query).
3. Bulk-fetch each `<pageid>.md`, saving as `references/NN-<页面名>.md` (number prefix preserves sitemap order).
4. **Verify every file**: starts with `# <title>`, ends with `components:\n  schemas: {}\n  securitySchemes: {}` (the YAML close). Spot-check first and last lines of each — a truncated download is easy to miss.
5. Record the source facts (sitemap/llms.txt URLs, pageid→title map) in the project `AGENTS.md` so future sessions can re-fetch.

## Real Command Example (13 pages, one shot)

```bash
mkdir -p references && cd references
fetch() { curl -s -L --max-time 60 "https://<host>/$1.md" -o "$2.md" \
  -w "$2: HTTP %{http_code}, %{size_download} bytes\n"; }
fetch <pageid> "01-页面名"
# ... one fetch line per page
```

## Pitfalls

- **The docs pages are NOT the API.** A site that serves Apifox docs (this skill's domain) may be **docs-only** — its `/api/*` paths may 302/404 even though the OpenAPI specs embedded in the pages are real. When the spec shows `servers: []` and live requests to the documented host redirect to a help page, the API has moved to another domain. **Do not build a client against the docs host.** Find the real API host with the `api-feasibility-probe` skill (scan docs HTML/JS for embedded host tokens; check the official client's source on GitHub for URL mappings — e.g. RailGo's `DefaultApiUrls.cs`).
- `.md` responses are UTF-8 — when saving with Chinese filenames use a small script (bash loop is fine on macOS/Linux); do not rely on shell redirection with locale-sensitive tools.
- If `llms.txt` is missing (404), probe `.md` suffix directly on any known pageid — the endpoint pattern is stable per site.
- Some pages have big payloads (e.g. a route-points endpoint doc ran 90KB+); `--max-time 60` and verify after.
- The API itself may be keyless but rate-limit via CDN — batch politely (one request per page), don't hammer.
- `sitemap.xml` is the authoritative page list; `llms.txt` may lag newly added pages.
