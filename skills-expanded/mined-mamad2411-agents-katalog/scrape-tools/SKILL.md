---
name: scrape-tools
description: Use when a task needs structured data extracted from web pages or HTML files - CSS/XPath selection, TLS-impersonated fetching, adaptive selectors that survive markup churn. Routes to extensions/scrape-tools.
triggers: [user, model]
---
# scrape-tools

Extension: `extensions/scrape-tools/` (installed to `%APPDATA%\devin\extensions\scrape-tools\`).

## When to use

- Extract data from saved HTML -> `parse.py` (offline, zero network).
- Fetch + extract in one step -> `scrape.py` (curl_cffi, TLS impersonation,
  SSRF-safe redirects on).
- Selector rot expected (sites that reshuffle classes) -> `--adaptive`.
- JS-rendered or bot-walled targets -> `--browser dynamic|stealthy`, but
  ONLY after the user has run `python -m scrapling.cli.install` themselves.

## When NOT to use

- Credential scraping, auth-bypass crawling, ToS-violating targets - refuse.
- "Undetectable" promises - not supported; enterprise WAFs still block.
- API endpoints that exist - prefer the real API over scraping HTML.
- XML feeds - parser is HTML-only.

## Commands

```bash
PARSE:  .venv/Scripts/python parse.py <file|-> --css SEL [--first]
SCRAPE: .venv/Scripts/python scrape.py <url> --css SEL [--impersonate chrome] [--adaptive]
BROWSER:.venv/Scripts/python scrape.py <url> --css SEL --browser stealthy
        # fails closed with feature_off:browser_tier_not_installed until
        # user runs: .venv/Scripts/python -m scrapling.cli.install
```

All output is JSON on stdout; exit!=0 with `{"ok":false,"error":...}` on failure.
