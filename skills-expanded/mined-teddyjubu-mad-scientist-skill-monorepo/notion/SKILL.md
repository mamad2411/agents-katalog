---
name: notion
description: "Notion API via curl: pages, databases, blocks, search."
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Notion, Productivity, Notes, Database, API]
    homepage: https://developers.notion.com
prerequisites:
  env_vars: [NOTION_API_KEY]
---

# Notion API

## What This Skill Does

This skill Notion API via curl: pages, databases, blocks, search.

## Current Notion Routing Override

This skill has older examples that mention `Welcome to Notion` or legacy parent pages. Those are superseded. For any new Notion output, use the current `notion-cli` skill, active workspace `Charles Blair’s Space`, parent/migration root `36325ada250d81b08171fa8170e25c82`, then run Publisher Agent validation and send only the published `finalLink` on `bush-gas-a9e.notion.site`.


Use the Notion API via curl to create, read, update pages, databases (data sources), and blocks. No extra tools needed — just curl and a Notion API key.

## Prerequisites

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it in `~/.hermes/.env`:
   ```
   NOTION_API_KEY=YOUR_NOTION_API_KEY_HERE
   ```
   (Never put the raw key in the SKILL.md itself — always use the .env file. Note: the actual live key is in `~/.hermes/.env`, not in the skill subdirectory.)
4. **Important:** Share target pages/databases with your integration in Notion (click "..." → "Connect to" → your integration name)

## API Basics

All requests use this pattern:

```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

The `Notion-Version` header is required. This skill uses `2025-09-03` (latest). In this version, databases are called "data sources" in the API.

## Common Operations

### Search

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

### Get Page

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Get Page Content (blocks)

```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Create Page in a Database

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

### Query a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

### Create a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

### Update Page Properties

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### Add Content to a Page

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello from Hermes!"}}]}}
    ]
  }'
```

## Property Types

Common property formats for database items:

- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "user@example.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

## Create Page as Child of Another Page

```bash
# CLI (ntn) — use page:PAGE_ID format with the --parent flag
ntn pages create --parent page:36325ada250d81b08171fa8170e25c82 --content '# Page Title\n\nContent here.'

# API (curl) — preferred method; use NOTION_API_KEY env var
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "36325ada250d81b08171fa8170e25c82"},
    "properties": {"title": {"title": [{"text": {"content": "Page Title"}}]}}
  }'
```

**Charles prefers the curl-based API method** (the `notion` skill). Use `notion-cli` (ntn) as fallback only.

## When to Use curl vs. execute_code

For simple single calls (read a page, search, quick patch), `curl` via `terminal()` is fastest.
For complex page creation with many blocks (guides, structured docs, nested content), use `execute_code` with Python — it handles multi-line JSON, variables, and logic cleanly, and the block-building code is readable and maintainable. Example pattern:

```python
import subprocess, json, os

NOTION_KEY = os.environ.get("NOTION_API_KEY", "")
PARENT_PAGE_ID = "page-id-here"

def api(method, path, data=None):
    cmd = ["curl", "-s", "-X", method,
           f"https://api.notion.com/v1{path}",
           "-H", f"Authorization: Bearer {NOTION_KEY}",
           "-H", "Notion-Version: 2025-09-03",
           "-H", "Content-Type: application/json"]
    if data:
        cmd += ["-d", json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(r.stdout)

# Build page
page = api("POST", "/pages", {
    "parent": {"page_id": PARENT_PAGE_ID},
    "properties": {"title": {"title": [{"text": {"content": "Page Title"}}]}}
})
page_id = page["id"]

# Helper functions for block types
def h1(t): return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": t}}]}}
def p(*args):
    """Paragraph with optional mixed inline runs.
    Pass plain strings for simple text, or dicts for formatted spans:
      p("hello")                           → plain text
      p({"text": {"content": "bold"}}, " normal")  → mixed inline
      p({"text": {"content": "link", "link": {"url": "https://..."}}})  → hyperlink
    """
    runs = []
    for a in args:
        if isinstance(a, dict):
            runs.append(a)
        else:
            runs.append({"text": {"content": str(a)}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": runs}}
def code(t): return {"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": t}}], "language": "bash"}}
def cal(t, e="💡"): return {"object": "block", "type": "callout", "callout": {"rich_text": [{"text": {"content": t}}], "icon": {"emoji": e}}}
def ss(t): return {"object": "block", "type": "callout", "callout": {"rich_text": [{"text": {"content": f"[Screenshot placeholder: {t}]"}}], "icon": {"emoji": "📸"}}}
def tbl(rows):
    """Build a table block with its rows as children.
    Notion tables require the table block to have a `children` array containing
    the row blocks — rows are NOT sibling blocks, they are nested children.
    """
    header = rows[0]
    table_block = {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": len(header),
            "has_column_header": True,
            "has_row_header": False,
            "children": []
        }
    }
    for row in rows:
        table_block["table"]["children"].append({
            "object": "block",
            "type": "table_row",
            "table_row": {
                "cells": [[{"text": {"content": c}}] for c in row]
            }
        })
    return table_block

# Screenshot placeholder helper — use when Cloudflare or bot detection blocks
# automated screenshots. Embeds a callout with the label and URL.
def ss(label, url):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"text": {"content": f"[SCREENSHOT: {label}]\n{url}"}}],
            "icon": {"emoji": "📸"}
        }
    }

# Add blocks in batches
def add(*blocks):
    api("PATCH", f"/blocks/{page_id}/children", {"children": list(blocks)})

# Usage
add(h1("Overview"))
add(p({"text": {"content": "Your paragraph text here"}}))
add(cal("Checkpoint: everything is working.", "✅"))
add(code("docker compose up -d"))
add(ss("OpenCLAW dashboard in browser"))
add(*tbl([["Column 1", "Column 2"], ["Value 1", "Value 2"]]))
```

Use `add()` with `*` unpacking to send multiple block types in one API call. Group related blocks (e.g., section heading + content + checkpoint callout) in a single `add()` call. Note: API call batches have a size limit; for guides with 50+ blocks, batch in groups of ~20.

## Key Differences in API Version 2025-09-03

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries and retrieval
- **Two IDs:** Each database has both a `database_id` and a `data_source_id`
  - Use `database_id` when creating pages (`parent: {"database_id": "..."}`)
  - Use `data_source_id` when querying (`POST /v1/data_sources/{id}/query`)
- **Search results:** Databases return as `"object": "data_source"` with their `data_source_id`

## Integration Types — Internal vs. Public

Notion tokens come in two types. The type determines what operations are possible:

| Type | Search works? | Create child pages? | Create workspace pages? | Requirement |
|---|---|---|---|---|
| **Internal** | Returns `{"results": []}` | Yes, if invited to parent | No | Must be invited to each page manually |
| **Public** | Yes | Yes | Yes (with `insert_content`) | Submit to Notion App Directory |

**How to tell which you have:** An `ntn_` prefix typically indicates an internal integration. A `secret_` prefix is usually a public OAuth integration.

### What happens when an internal integration has no page invitations

- `POST /v1/search` returns `{"results": []}` — always empty, even with `query: ""`
- `POST /v1/pages` with `"parent": {"workspace": true}` fails: *"Internal integrations aren't owned by a single user, so creating workspace-level private pages is not supported"*
- `GET /v1/users` returns `403 Forbidden` — personal access tokens cannot list users

### Fix: invite the integration to a page

1. Open Notion and navigate to the **parent page** for the new page
2. Click the **"..."** three-dot menu → **"Add connections"** or **"Connect to"**
3. Find and select your integration by name
4. Copy the **page ID** from the URL — the long alphanumeric string at the end (with or without dashes)
5. Use it: `ntn pages create --parent page:<PAGE_ID> --content '# New Page'`

**Verify connectivity:**
```bash
curl -s "https://api.notion.com/v1/pages/<PAGE_ID>" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
# If this returns page content, the integration is connected
```

## API Key Storage Locations

The `NOTION_API_KEY` lives in two places — **always update both**:

| File | Purpose | Update manually? |
|---|---|---|
| `/root/.hermes/.env` | Primary env var — used by Hermes `notion` skill (curl/Python) | Yes |
| `/root/.openclaw/workspace/hermes-agent-webapi/skills/productivity/notion/SKILL.md` | Example placeholder in skill docs | Yes |

**Do NOT trust mcporter.json paths from old session logs.** Session histories reference configs like `/data/.openclaw/workspace/config/mcporter.json` and `/root/.openclaw/workspace/config/mcporter.json` — these locations are **not confirmed to exist** on this host. The active mcporter config for OpenClaw was not found at those paths during the 2026-05-17 review. If you need to configure mcporter for OpenClaw, check the actual running container's mounted secrets or the active workspace config — do not assume a path from a session log is still valid.

## Shared Token State

Both James (Hermes) and OpenClaw share the **same Notion API token** (`ntn_5316...`, stored in `~/.hermes/.env` on the host, and inside the OpenClaw container at `/data/.openclaw/workspace/.secrets/notion.env`). The token is identical on both sides.

**Access difference:**
- **OpenClaw** sees the full workspace: **43 items** (pages + 3 data_sources named "Documents", "Projects", "Clients")
- **James (Hermes)** sees only **4 items** because it's an internal integration that must be manually invited to each page in Notion's UI (click ... → Connect to → integration name)

Both have functional Notion access. OpenClaw's view is the authoritative/full one. If a new page needs to be accessed programmatically, add the integration to that page in Notion first.

## Charles's Notion Page Format (REI Business)

Charles's guides live under the **Charles Blair’s Space migration root** parent page (ID: `36325ada250d81b08171fa8170e25c82`) and follow this format:

- Page title: **plain text, no emoji**
- Callout boxes with emojis for highlights/tips/checkpoints
- Plain-language explanations (90-year-old grandmother rule — no jargon)
- Screenshot placeholders via `ss()` helper when Cloudflare blocks automated capture
- Pricing data, comparison tables, and step-by-step lists

His Charles Blair’s Space migration root uses a "light print page" visual style. When creating guides for Charles:
1. Create as child of `36325ada250d81b08171fa8170e25c82`
2. No emoji in the title
3. Use callouts for tips, checkpoints, and warnings
4. Keep headings short and punchy

## Pitfalls

### Table blocks: rows must be nested inside the table block as `children`

Notion tables are structured differently from other blocks. The `table_row` blocks are **nested inside** the `table` block's `children` array — they are not sibling blocks at the same level as the table.

**Wrong (what I originally had):**
```python
blocks = [
    {"object": "block", "type": "table", "table": {...}},  # no children
    {"object": "block", "type": "table_row", ...},          # sibling — fails
]
```

**Correct:**
```python
table_block = {
    "object": "block",
    "type": "table",
    "table": {
        "table_width": 3,
        "has_column_header": True,
        "has_row_header": False,
        "children": [
            {"object": "block", "type": "table_row", "table_row": {"cells": [[{"text": {"content": "Col1"}}], ...]}},
            ...
        ]
    }
}
# Add the table_block as a single item in the children array
add(table_block)
```

### Code block language must be a valid Notion language ID

Valid languages include: `bash`, `shell`, `python`, `javascript`, `json`, `html`, `css`, `yaml`, `markdown`, `plain text` (two words, not one). **"plaintext" is not valid** — use `"plain text"` (with a space).

### Browser/screenshot tools blocked by Cloudflare

HeyGen, and many other modern SaaS sites, use Cloudflare bot protection. When `browser_navigate` or `browser_vision` hits a Cloudflare challenge:
- Screenshot placeholders are the correct workaround — use `ss("Label", "https://actual-url")`
- Do not attempt to solve CAPTCHAs programmatically
- Add the actual URL so a human can open it manually

### Screenshot placeholders vs. real screenshots

Use `ss()` when:
- Cloudflare or bot detection blocks the page
- The page requires login/session state to render correctly
- Automated screenshot would capture sensitive/personalized content

Do NOT use `ss()` as a shortcut when real screenshots are available and accessible.

## Notes

- Page/database IDs are UUIDs (with or without dashes)
- Rate limit: ~3 requests/second average
- The API cannot set database view filters — that's UI-only
- Use `is_inline: true` when creating data sources to embed them in pages
- Add `-s` flag to curl to suppress progress bars (cleaner output for Hermes)
- Pipe output through `jq` for readable JSON: `... | jq '.results[0].properties'`
