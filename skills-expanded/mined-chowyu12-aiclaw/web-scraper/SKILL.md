---
name: Web Scraper
description: Extract structured data from web pages, including tables, lists, prices, and reviews. Supports HTTP fetching, optional MCP browser tools, parallel multi-site collection, and CSV/JSON output.
---

# Web Data Collection (web-scraper)

Act as a web data collection engineer. After the user describes target sites and fields, extract structured data accurately and efficiently.

## Workflow

1. **Analyze the target**: confirm which site and which fields the user wants.
2. **Probe the page**: start with `web_fetch` to inspect returned content.
3. **Choose a strategy**:
   - If `web_fetch` returns complete content, parse the HTML with `code_interpreter`.
   - If content is incomplete or dynamically rendered, inspect the active tool catalog for a namespaced MCP browser tool (`mcp__...`). If none is installed, explain that dynamic browser access must be configured in Settings.
4. **Extract data**:
   - Static pages: use Python HTML parsing in `code_interpreter`.
   - Dynamic pages: use the installed MCP browser's snapshot/evaluate operations when available.
   - Tables: use an MCP browser's table extraction when available.
5. **Write structured output**: normalize records and save CSV or JSON with `write`.

## Multi-Site Collection

When collecting from multiple sites, use `sub_agent` in parallel:

```text
sub_agent(prompt: "Extract product names and prices from https://site-a.com and return JSON.")
sub_agent(prompt: "Extract comparable product data from https://site-b.com and return JSON.")
```

The parent Agent should merge, deduplicate, and write the final dataset.

## Tool Strategies

### Static Pages

`web_fetch` -> `code_interpreter` (parse) -> `write` (save)

### Dynamic Pages

installed `mcp__...` navigate -> snapshot -> evaluate (extract) -> `write` (save)

### Tables

installed `mcp__...` navigate -> table extraction -> `write` (save)

### Pagination

installed `mcp__...` navigate -> extract current page -> click next page -> repeat

## Output Guidelines

- Default to CSV for Excel-friendly output.
- Use JSON for nested data.
- Include the source URL for every record.
- After collection, report total records, field names, and a sample of the first five rows.

## Notes

- Respect robots.txt and explicit site restrictions.
- Control request frequency to avoid stressing target servers.
- If anti-bot defenses appear, such as CAPTCHA or IP blocking, inform the user instead of bypassing them.
