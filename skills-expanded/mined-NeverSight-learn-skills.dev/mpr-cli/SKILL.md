---
name: mpr-cli
description: Query USDA MyMarketNews commodity data using the mpr CLI. Use when working with agricultural prices, commodity reports, livestock markets, grain prices, or when the user mentions USDA, commodity data, market reports, or mpr.
---

# MyMarketNews CLI

Query USDA MyMarketNews commodity data using the `mpr` command-line tool.

## Prerequisites

```bash
mpr --version
mpr auth status
```

## Authentication

- API key from USDA MyMarketNews
- Environment variable: `MPR_API_KEY`
- Config file: `~/.mpr/config.json`

## Commodity Reports

### List Reports

```bash
mpr reports list --commodity cattle --limit 50
mpr reports list --location "Nebraska" --days 7
mpr reports search --query "fed steer"
```

### Get Report Details

```bash
mpr reports get REPORT_ID --pretty
mpr reports get REPORT_ID --format csv --output report.csv
```

## Price Queries

```bash
mpr prices --commodity cattle --market "Omaha"
mpr prices --commodity corn --date 2024-01-15
mpr prices --commodity wheat --location "Kansas City" --range 30days
```

## Market Data

```bash
mpr markets list --state Nebraska
mpr markets get MARKET_ID --commodities cattle,hogs
mpr commodities list --category livestock
```

## Historical Data

```bash
mpr history --commodity cattle --market MARKET_ID --start 2024-01-01 --end 2024-03-01
mpr trends --commodity corn --days 90 --output trends.json
```

## Agent Best Practices

1. **Date ranges** for historical analysis
2. **Location filters** for regional pricing
3. **Output formats**: JSON (default), CSV, or table
4. **Rate limits**: Respect USDA API limits (check `--help` for details)
