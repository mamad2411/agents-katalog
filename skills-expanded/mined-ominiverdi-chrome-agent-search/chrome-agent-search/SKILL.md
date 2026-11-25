---
name: chrome-agent-search
description: Local-first web search and page reading through chrome-agent. Use for search queries, reading URLs, extracting visible text, full search with page content, and diagnosing blocked/login/challenge pages.
metadata:
  author: ominiverdi
  version: "0.2.1"
  tags: ["search", "web", "reading", "chrome", "local-first"]
---

# chrome-agent-search

`chrome-agent-search` is a pure CLI. It shells out to `chrome-agent`; it does not embed an MCP server.

## Install check

```bash
which chrome-agent-search
which chrome-agent
```

If missing:

```bash
cargo install chrome-agent --locked
cargo install --git https://github.com/ominiverdi/chrome-agent-search --locked
```

## Core workflow

Search first when the user asks for current or unknown web information:

```bash
chrome-agent-search --json search 'query' --limit 5
```

Read a known URL when the user gives one:

```bash
chrome-agent-search read 'https://example.com/article'
```

Use full search when the task needs both discovery and page content:

```bash
chrome-agent-search --json full 'query' --limit 3 --max-chars 8000 --concurrency 3
```

`full` uses Readability first and then retries failed pages with visible text from `main`. JSON results identify the successful path as `readability` or `text_main_fallback` in `fetch_method`.

Extract visible text from a page or container when Readability is not appropriate:

```bash
chrome-agent-search text 'https://example.com/page' --selector body
chrome-agent-search text 'https://example.com/page' --selector main
chrome-agent-search text 'https://example.com/page' --selector article
```

## Engine choice

Default `auto` is best for normal use:

```bash
chrome-agent-search search 'query' --engine auto
```

Use local SearXNG when available:

```bash
chrome-agent-search --searxng http://search.home search 'query' --engine searxng
chrome-agent-search --searxng http://search.home search 'query' --engine auto
```

With `--searxng`, `auto` tries SearXNG first and falls back to browser engines.

Use `all` for exhaustive diagnostics or quality checks:

```bash
chrome-agent-search search 'query' --engine all
```

Specific engines:

```bash
chrome-agent-search search 'query' --engine bing
chrome-agent-search search 'query' --engine brave
chrome-agent-search search 'query' --engine duckduckgo
chrome-agent-search --searxng http://search.home search 'query' --engine searxng
```

## Reading failures and diagnosis

If `read` fails with minimal content, do not assume the page is empty. Diagnose it:

```bash
chrome-agent-search diagnose 'https://example.com/page'
chrome-agent-search --json diagnose 'https://example.com/page'
```

`diagnose` runs `chrome-agent goto --inspect --json` and reports:

- final URL
- redirect status
- HTTP status
- title
- accessibility snapshot excerpt
- a practical hint

Use it for:

- login redirects
- consent/interstitial pages
- WAF or network security blocks
- human-verification pages
- non-article pages where Readability is weak

## Login, challenge, and blocked sites

Use a named browser profile and keep it consistent:

```bash
chrome-agent-search --browser work read 'https://example.com/private'
```

For logged-in sites, try cookies if available:

```bash
chrome-agent-search --copy-cookies read 'https://example.com/private'
```

For sites requiring visible interaction, open headed once:

```bash
chrome-agent-search --browser work --headed diagnose 'https://example.com/private'
```

Complete the visible login/consent/challenge manually. Keep that browser open. Then retry with the same browser profile:

```bash
chrome-agent-search --browser work read 'https://example.com/private'
```

For hard bot protections, attach to a user-launched real Chrome:

```bash
google-chrome --remote-debugging-port=9222
chrome-agent-search --connect http://127.0.0.1:9222 read 'https://example.com/private'
```

Do not automate or bypass CAPTCHA/human-verification challenges. Ask the user to complete them manually in a headed browser.

## Proxy

Use a proxy for managed browser traffic:

```bash
chrome-agent-search --proxy-server socks5://127.0.0.1:9050 search 'query'
```

Do not combine `--proxy-server` with `--connect`; a connected browser must be started with its proxy already configured.

## Cleanup

Close managed browser sessions:

```bash
chrome-agent-search cleanup
```

Purge managed profile data only when intended:

```bash
chrome-agent-search cleanup --purge
chrome-agent-search cleanup --purge-orphans
```

## Benchmarks

Run the public smoke benchmark:

```bash
chrome-agent-search --command-timeout 30 --wait-timeout 3 bench --cases benchmarks/cases.toml
```

Run hard diagnostic cases separately:

```bash
chrome-agent-search --command-timeout 30 --wait-timeout 3 bench --cases benchmarks/hard-cases.toml
```

## Rules for agents

- Prefer `search` for discovery, `read` for known articles, `full` for discovery plus content.
- Use `diagnose` before declaring a blocked or unreadable page empty.
- Reuse the same `--browser` profile for multi-step sessions.
- Keep headed challenge/login sessions open while reusing them from CLI calls.
- Prefer `--searxng <base-url>` when a local SearXNG instance is available.
- Use `--engine all` only when quality/diagnostics matter more than latency.
- Do not solve CAPTCHA automatically.
- Do not claim a source was read unless the command returned content supporting it.
