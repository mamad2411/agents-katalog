---
name: zillow-research-county-home-value-trend-scraper
description: "Get US county-level home value trends with 6- and 12-month comparisons and year-over-year percent change, plus a state-by-state home value comparison, from Zillow's published research files. Filter by state and county. Output fields: countyName, stateCode, stateName, metro, latestValue and more, as JSON rows. Use it for requests like \"Zillow research county home value trend scraper\", or a CSV/JSON export of public Zillow data."
---

# Zillow Research County Home Value Trend Scraper

Get US county-level home value trends with 6- and 12-month comparisons and year-over-year percent change, plus a state-by-state home value comparison, from Zillow's published research files. Filter by state and county.

- Actor: https://apify.com/dataspryva/zillow-research-county-home-value-trend-scraper (ID `dataspryva~zillow-research-county-home-value-trend-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/zillow-research-county-home-value-trend-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Stop copying county values; refresh the trend sheet](https://www.youtube.com/shorts/ZHpo1ej5zvc)

## When to use

Use this skill when the user wants:

- Zillow research county home value trend scraper
- a repeatable export of public Zillow data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `countyName`: County Name
- `stateCode`: State Code
- `stateName`: State Name
- `metro`: Metro
- `homeType`: Home Type
- `latestValue`: Latest Value
- `latestDate`: Latest Date
- `change6mPct`: Change6m Pct
- `change12mPct`: Change12m Pct
- `vsBenchmark6mPct`: Vs Benchmark6m Pct
- `rank`: Rank

All 16 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | countyTrends | What to return: one trend row per county, per state, per metro, or one history row per region per month. |
| `homeType` | string | no | allHomesMidTier | Which Zillow Home Value Index series to read. All ten cuts are available at county, state, and metro level. |
| `state` | string | no | all | Filter counties, metros, or history to one state, or pick a single state in stateTrends. Choose 'all' to include every state. Two-letter codes are accepted by the API. |
| `county` | string | no |  | Case-insensitive county-name substring, e.g. 'Gallatin' or 'Los Angeles'. Works in countyTrends and county history. Use regionIds for exact matching. |
| `regionIds` | array | no | [] | Exact Zillow RegionIDs, e.g. ['3101', '1090']. Works in every mode. When combined with state or county filters, a region must match all of them. |
| `asOfDate` | string | no |  | Compute the trend from the latest observation on or before this date (YYYY-MM-DD). Leave empty for the newest published month. Trend modes only. |
| `historyGeography` | string | no | county | Which ZHVI level the monthly history rows come from. Used only in history mode. |
| `startDate` | string | no |  | First month to include in history mode (YYYY-MM-DD). Leave empty to start at the oldest published month. |
| `endDate` | string | no |  | Last month to include in history mode (YYYY-MM-DD). Leave empty to end at the newest published month. |
| `sortBy` | string | no | sizeRank | Order trend rows and assign ranks across all matching regions before the row cap is applied. Missing metrics sort last without a rank. |
| `maxItems` | integer | no | 100 | Hard cap on emitted records. The default county file has 3,071 rows; history usually needs a date or region filter to stay under the cap. |

Example (`references/example-input.json`):

```json
{
  "mode": "stateTrends",
  "maxItems": 25
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~zillow-research-county-home-value-trend-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~zillow-research-county-home-value-trend-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d @references/example-input.json)
RUN_ID=$(echo "$RUN" | jq -r '.data.id'); DATASET=$(echo "$RUN" | jq -r '.data.defaultDatasetId')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" -H "Authorization: Bearer $APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/datasets/$DATASET/items?format=json" -H "Authorization: Bearer $APIFY_TOKEN" > output.json
```

## Cost and limits

- Apify bills the Actor's usage on your account; the Actor's Pricing tab shows the current price.
- Keep the limit in the input small for a first run.

## Guardrails

- Public data only. Do not pass cookies, sessions or private account data.
- Do not use the output for spam, harassment or unlawful discrimination.
- Check the target site's terms and local law before running at scale.
