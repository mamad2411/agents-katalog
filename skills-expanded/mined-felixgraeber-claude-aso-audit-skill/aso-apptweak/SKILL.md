---
name: aso-apptweak
description: >
  Live ASO data via AppTweak REST API. Keyword suggestions with volume/difficulty,
  app rankings, competitor analysis, review sentiment, and historical data.
  Requires AppTweak API key. Triggers on: "apptweak", "live data", "keyword volume".
---

# ASO AppTweak — Live Data Integration

Provides live ASO data from AppTweak's API. Requires API key stored in `.env`.

## Commands

| Command | What it does |
|---------|-------------|
| `/aso apptweak keywords <seed>` | Keyword suggestions with search volume and difficulty |
| `/aso apptweak rankings <app-id>` | Current keyword rankings for the app |
| `/aso apptweak competitors <app-id>` | Similar apps with keyword overlap scores |
| `/aso apptweak timeline <app-id>` | Historical ranking data |
| `/aso apptweak reviews <app-id>` | Recent reviews with sentiment analysis |

## Usage

All commands use:
```bash
uv run python scripts/apptweak_client.py <command> <args> --json
```

## Authentication

API key loaded from `APPTWEAK_API_KEY` or the ASO env file.

## Available Tools
Read, Bash, Write, Glob, Grep
