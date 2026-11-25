---
name: pinterest-trending-topics-and-shopping-category-scraper
description: "Collect Pinterest's public featured and editorial trend topics, its shopping category taxonomy, and shopping-category click metrics with history and forecast, by region. Output fields: term, title, name, region, rank and more, as JSON rows. Use it for requests like \"Pinterest trending topics scraper\", or a CSV/JSON export of public Pinterest data."
---

# Pinterest Trending Topics & Shopping Category Scraper

Collect Pinterest's public featured and editorial trend topics, its shopping category taxonomy, and shopping-category click metrics with history and forecast, by region.

- Actor: https://apify.com/vexaloom-labs/pinterest-trending-topics-and-shopping-category (ID `vexaloom-labs~pinterest-trending-topics-and-shopping-category`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/pinterest-trending-topics-and-shopping-category-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Your Pinterest topics are already ranked](https://www.youtube.com/shorts/14Wbs-96RPg)

## When to use

Use this skill when the user wants:

- Pinterest trending topics scraper
- a repeatable export of public Pinterest data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `term`: Term
- `title`: Title
- `name`: Name
- `region`: Region
- `trendType`: Trend Type
- `rank`: Rank
- `weekOverWeekChange`: Week Over Week Change

All 9 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | trendingSearches | Choose a Pinterest Trends dataset. |
| `region` | string | no | US | Pinterest Trends market. Combined codes such as `GB+IE` cover Pinterest's published regional groups. |
| `trendType` | string | no | topMonthly | Trending list to collect (mode=trendingSearches). |
| `lookbackWindow` | string | no | 30D | Comparison window used by Pinterest for trending searches (mode=trendingSearches). |
| `endDate` | string | no |  | Historical end date in `YYYY-MM-DD` format. Leave empty for Pinterest's latest available date (mode=trendingSearches, keywordResearch, shoppingCategories, shoppingMetrics). |
| `interest` | string | no | all | Pinterest interest filter for trending searches (mode=trendingSearches). |
| `moment` | string | no | all | Pinterest seasonal moment filter for trending searches (mode=trendingSearches). |
| `keywordsToInclude` | array | no | [] | Only keep trending searches containing at least one of these words (mode=trendingSearches). |
| `keywordsToExclude` | array | no | [] | Drop trending searches containing any of these words (mode=trendingSearches). |
| `ageGroup` | string | no | all | Pinterest audience age filter for trending searches and keyword research. |
| `gender` | string | no | all | Pinterest audience gender filter for trending searches and keyword research. |
| `keywords` | array | no | [] | Terms to research (mode=keywordResearch). Leave empty to use Pinterest's current top trending searches. |
| `days` | integer | no | 90 | History length in days for keyword research and shopping metrics. |
| `predictedDays` | integer | no | 0 | Pinterest forecast horizon. Forecasts are published for the US only (mode=keywordResearch, shoppingMetrics). |

8 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "maxItems": 25,
  "mode": "trendingSearches"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~pinterest-trending-topics-and-shopping-category/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~pinterest-trending-topics-and-shopping-category/runs" \
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
