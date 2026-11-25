---
name: mhhs-cli
description: Use mhhs-cli for ALL MHHS Programme queries — browsing news articles, reading newsletters (The Clock), searching programme updates, and tracking UK energy settlement reform progress. Invoke whenever user asks about MHHS, half-hourly settlement, Elexon programme updates, or The Clock newsletter.
author: MeetGeorge
version: "0.1.0"
tags:
  - mhhs
  - energy
  - elexon
  - uk-regulation
  - half-hourly-settlement
  - cli
---

# mhhs-cli — MHHS Programme CLI

**Binary:** `mhhs`
**Auth:** None required — all data is public

## Setup

```bash
# Install (requires Node.js 20+)
npm install -g mhhs-cli

# Verify
mhhs --version
```

No API keys, no browser login, no cookies. The MHHS Programme website is fully public.

## Output Format

### Default: Rich table (human-readable)

```bash
mhhs news                             # Pretty table output
```

### JSON / YAML: structured output

```bash
mhhs news -f json                     # JSON for jq / AI agents
mhhs news -f yaml                     # YAML
mhhs news -f md                       # Markdown table
mhhs read <slug> -f json              # Article as JSON
mhhs read <slug> -f md                # Article as Markdown
```

## Command Reference

### List news articles

```bash
mhhs news                             # Latest 20 articles (of 256+ total)
mhhs news --limit 10                  # 10 per page
mhhs news --page 2                    # Page 2
mhhs news --page 5 --limit 10         # Page 5, 10 per page
mhhs news --all                       # All 256+ articles
mhhs news --search "ELS"              # Filter by keyword in title
mhhs news --search "migration"        # Case-insensitive search
mhhs news -f json                     # JSON output
mhhs news -f yaml                     # YAML output
mhhs news -f md                       # Markdown table
```

### Read a specific article

```bash
mhhs read the-clock-18-march-2026                # Read by slug
mhhs read early-life-support-els-phase-3-exit     # Any article slug
mhhs read https://www.mhhsprogramme.co.uk/news-articles/the-clock-18-march-2026  # Full URL also works
mhhs read <slug> -f json              # Article as structured JSON
mhhs read <slug> -f md                # Article as Markdown
mhhs read <slug> -f yaml              # Article as YAML
```

## Agent Workflows

### Get latest news

```bash
mhhs news --limit 5 -f json
```

### Read the most recent newsletter

```bash
SLUG=$(mhhs news --limit 1 -f json | jq -r '.[0].slug')
mhhs read "$SLUG"
```

### Search and read

```bash
mhhs news --search "migration" -f json | jq '.[0].slug' -r | xargs mhhs read
```

### Export all articles

```bash
mhhs news --all -f json > mhhs-articles.json
```

### Browse archive by page

```bash
# Page through the full archive
mhhs news --page 1 --limit 20
mhhs news --page 2 --limit 20
mhhs news --page 3 --limit 20
```

### Find non-newsletter articles

```bash
mhhs news --all -f json | jq '[.[] | select(.title | test("Clock") | not)]'
```

### Get article count

```bash
mhhs news --all -f json | jq 'length'
```

## How It Works

The MHHS Programme website only displays 20 recent articles on its news hub page with no pagination. `mhhs-cli` reads the site's `sitemap.xml` to index all 256+ articles, then fetches individual article pages on demand. No browser, no API key, no authentication required.

## Data Source

All data comes from [mhhsprogramme.co.uk](https://www.mhhsprogramme.co.uk), the official MHHS Programme website operated by Elexon.

## Limitations

- **Read-only** — no write operations (the site has no user-facing API)
- **Public content only** — cannot access SharePoint or login-gated documents
- **Article text only** — embedded PDFs and images are not extracted
- **Sitemap-dependent** — article index relies on the site publishing an up-to-date sitemap.xml
