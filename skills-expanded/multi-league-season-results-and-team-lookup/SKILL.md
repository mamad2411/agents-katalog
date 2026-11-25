---
name: multi-league-season-results-and-team-lookup
description: "Get final scores for a season across 10 major soccer, football, basketball, baseball, and hockey leagues, or look up every team's roster details for a league in one run. Output fields: homeTeam, awayTeam, homeScore, awayScore, matchDate and more, as JSON rows. Use it for requests like \"Multi-League season results\", or a CSV/JSON export of public Multi-League data."
---

# Multi-League Season Results & Team Lookup

Get final scores for a season across 10 major soccer, football, basketball, baseball, and hockey leagues, or look up every team's roster details for a league in one run.

- Actor: https://apify.com/dataspryva/multi-league-season-results-and-team-lookup (ID `dataspryva~multi-league-season-results-and-team-lookup`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/multi-league-season-results-and-team-lookup.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Build the season sheet from match scores](https://www.youtube.com/shorts/-_kZpsDWfXw)

## When to use

Use this skill when the user wants:

- Multi-League season results
- a repeatable export of public Multi-League data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `homeTeam`: Home Team
- `awayTeam`: Away Team
- `homeScore`: Home Score
- `awayScore`: Away Score
- `matchDate`: Match Date
- `status`: Status
- `oddsHome`: Odds Home
- `oddsDraw`: Odds Draw
- `oddsAway`: Odds Away
- `bookmakerCount`: Bookmaker Count

All 25 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | results | Season results with odds, a league's team roster, or a team lookup by name. |
| `sport` | string | no | epl | Which competition to fetch. Ignored when leagueUrls is set. |
| `season` | string | no | 2024-2025 | Season to fetch. Soccer-style seasons use YYYY-YYYY (a plain YYYY expands to YYYY-YYYY); calendar-year leagues (MLB, MLS, NPB, J1, K League) use YYYY; 'current' is the live… |
| `leagueUrls` | array | no |  | Optional: one or more OddsPortal league or season-results URLs (any sport or league, e.g. `https://www.oddsportal.com/football/england/premier-league-2024-2025/results/`). |
| `teamQuery` | string | no |  | Team to look up by name (teamSearch mode), e.g. Arsenal or Real Madrid. |
| `includeOdds` | boolean | no | true | Add 1X2 average and maximum odds, bookmaker count and per-bookmaker prices to each result. |
| `includeUpcoming` | boolean | no | true | Keep scheduled and in-progress matches; turn off to get only finished results. |
| `enrichTeams` | boolean | no | true | In teams and teamSearch modes, open each team's page for its full name, venue, city, country and coach. Adds one request per team. |
| `regionalFallback` | boolean | no | true | When a league-season is empty on the main domain, retry it on the same site's regional edition (a few competitions, e.g. ACB, only publish older seasons there). |
| `maxItems` | integer | no | 20 | Maximum records to return (1-10000). The run also stops when the source runs out of pages. |

Example (`references/example-input.json`):

```json
{
  "teamQuery": "Arsenal",
  "enrichTeams": false,
  "mode": "results"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 20, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~multi-league-season-results-and-team-lookup/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~multi-league-season-results-and-team-lookup/runs" \
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
