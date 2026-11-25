---
name: washington-trails-association-hike-and-trip-report-finder
description: "Find Washington State hikes by region or keyword with length, elevation, rating and feature data, pull full trail stats and coordinates by hike URL, or check recent trip report activity. Output fields: trailName, region, lengthMiles, rating, reviewCount and more, as JSON rows. Use it for requests like \"Washington Trails Association hike\", or a CSV/JSON export of public Washington Trails Association data."
---

# Washington Trails Association Hike & Trip Report Finder

Find Washington State hikes by region or keyword with length, elevation, rating and feature data, pull full trail stats and coordinates by hike URL, or check recent trip report activity.

- Actor: https://apify.com/dataspryva/washington-trails-association-hike-and-trip-report (ID `dataspryva~washington-trails-association-hike-and-trip-report`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/washington-trails-association-hike-and-trip-report-finder.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Stop opening trail tabs; compare hikes in one sheet](https://www.youtube.com/shorts/0sgh1HcSZeM)

## When to use

Use this skill when the user wants:

- Washington Trails Association hike
- a repeatable export of public Washington Trails Association data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `trailName`: Trail Name
- `region`: Region
- `lengthMiles`: Length Miles
- `elevationGainFeet`: Elevation Gain Feet
- `difficulty`: Difficulty
- `rating`: Rating
- `reviewCount`: Review Count
- `tripReportCount`: Trip Report Count
- `latitude`: Latitude
- `longitude`: Longitude
- `trailUrl`: Trail Url

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | searchTrails | What to fetch from wta.org. |
| `searchQuery` | string | no |  | Free-text search of WTA hike descriptions (modes searchTrails, searchTripReports). |
| `nameQuery` | string | no |  | Match the hike name only (modes searchTrails, getTripReports, searchTripReports). |
| `region` | string | no |  | Washington region. Choose All Washington to search statewide (modes searchTrails, getTripReports, searchTripReports). |
| `subregion` | string | no | all | Optional sub-region. Selecting one also selects its parent region. |
| `features` | array | no | [] | Require all selected features (mode searchTrails). Empty = no feature filter. |
| `dogPolicy` | string | no | any | Filter by dog access (mode searchTrails). |
| `kidFriendly` | boolean | no | false | Only kid-friendly trails (mode searchTrails). |
| `wheelchairFriendly` | boolean | no | false | Only wheelchair-friendly trails (mode searchTrails). |
| `minRating` | number | no |  | Minimum average community rating, 0–5 (mode searchTrails). |
| `minVoteCount` | integer | no |  | Minimum number of rating votes (mode searchTrails; applied after the listing fetch). |
| `minLengthMiles` | number | no |  | Only trails at least this long (mode searchTrails). Trails with unknown length are excluded. |
| `maxLengthMiles` | number | no |  | Only trails at most this long (mode searchTrails). Trails with unknown length are excluded. |
| `minElevationGainFeet` | integer | no |  | Only trails with at least this gain (mode searchTrails). Unknown gain is excluded. |

25 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "region": "Snoqualmie Region",
  "tripReportsPerTrail": 3,
  "maxItems": 25,
  "mode": "searchTrails",
  "searchQuery": "head of growth"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~washington-trails-association-hike-and-trip-report/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~washington-trails-association-hike-and-trip-report/runs" \
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
