---
name: digital-product-sales-automation
description: "Full sales automation system: create listings, manage Gumroad products, handle inquiries, monitor sales"
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales, automation, gumroad, ecommerce, operations]
    triggers: [sell a product, build sales tooling, sales automation, manage listings, gumroad management]
    related_skills: [business-voice-outreach, entity-phone-enrichment]
---

# Digital Product Sales Automation System

Complete tooling to create, post, and manage digital product sales across Gumroad and other platforms.

## System Location

All scripts at `~/AppData/Local/hermes/scripts/sales-automation/`

## Components

- `run.py` — Master orchestrator: status, launch, check, summary, setup
- `listing_manager.py` — Create product listings post to platforms
- `gumroad_manager.py` — Full Gumroad API client (CRUD, sales, webhooks, licenses, customers)
- `sales_monitor.py` — Monitor sales, manage customers, auto-respond to inquiries, webhook listener
- `products/` — Packaged sellable products ready to launch

## Commands

```
python3 run.py status              # Full system status
python3 run.py launch <product>    # Launch a product end-to-end
python3 run.py check               # Check sales and inquiries
python3 run.py summary             # Daily summary
python3 run.py setup               # Setup guide (first time)
```

## Products Ready to Sell

- `market-lead-mcp-server` ($49) — MCP server for real estate property research (6 tools: search, tax, comps, skip-trace, bulk, counties)

## First-Time Setup

### Gumroad Account (requires user action)
Gumroad requires web-based signup with email verification (API-based signup is rate-limited). The user must:
1. Go to `gumroad.com` and sign up with their email
2. Verify email, then go to **Settings → API**
3. Generate an API token and paste it here
4. I save it to `~/.env` as `GUMROAD_TOKEN`

### Once Token is Set
```
python3 run.py launch market-lead-mcp-server
```

### Alternative Distribution (no Gumroad needed)
GitHub Releases work immediately (gh CLI is authenticated):
```
cd ~/AppData/Local/hermes/scripts/sales-automation
gh release create v1.0.0 --repo pmb2/digital-content-agent \
  --title "Real Estate MCP Server v1.0" \
  "market-lead-mcp-server.zip#Package"
```

A Gumroad webhook can be set up at `https://app.gumroad.com/settings/webhooks` pointing to `http://YOUR_IP:8080` for automatic sale notifications.

## Pitfalls

### Windows/MSYS Path Resolution

When running under git-bash (MSYS) on Windows, `python3 ~/AppData/Local/hermes/scripts/sales-automation/sales_monitor.py check` **fails** because MSYS translates `~/AppData/...` into `C:\c\Users\...` (a doubled-up incorrect path). The error looks like:
```
can't open file 'C:\\c\\Users\\<you>\\AppData\\Local\\hermes\\scripts\\sales-automation\\sales_monitor.py'
```

**Fix:** Always `cd` to the script directory first, then run the command:
```bash
cd ${HERMES_HOME}/scripts/sales-automation && python3 sales_monitor.py check
```
Or use the explicit MSYS root path without `~`.

This applies to ALL commands in this skill that pass an `~/AppData/...` path directly to `python3`.

### Gumroad API Token

`GUMROAD_TOKEN` must be set in the environment. Without it, `gumroad_manager.py` and `sales_monitor.py check` immediately exit with `ERROR: GUMROAD_TOKEN environment variable not set.` and no sales data is fetched. The token goes in `~/AppData/Local/hermes/.env` as `GUMROAD_TOKEN=your_token_here` (generated at Gumroad Settings → Advanced → API Access Token).

### Known Issues

- Gumroad signup via API returns HTTP 429 (rate limited). Must use web browser.
- Gumroad uses Inertia.js SPA — standard form POSTs don't work for signup.
- CloakBrowser CDP port may not be available — browser automation for signup may fail.

## Cron Jobs

`sales-monitor` job runs every 4h to check sales and inquiries.
