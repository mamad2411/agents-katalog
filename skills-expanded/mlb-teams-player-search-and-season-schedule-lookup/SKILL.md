---
name: mlb-teams-player-search-and-season-schedule-lookup
description: "Look up every current MLB team, search for a player by name, or pull a full season's schedule and scores, with stadium, roster, and matchup details for each record. Output fields: teamName, playerName, eventName, homeTeam, awayTeam and more, as JSON rows. Use it for requests like \"MLB teams, player search\", or a CSV/JSON export of public MLB data."
---

# MLB Teams, Player Search & Season Schedule Lookup

Look up every current MLB team, search for a player by name, or pull a full season's schedule and scores, with stadium, roster, and matchup details for each record.

- Actor: https://apify.com/vexaloom-labs/mlb-teams-player-search-and-season-schedule-lookup (ID `vexaloom-labs~mlb-teams-player-search-and-season-schedule-lookup`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/mlb-teams-player-search-and-season-schedule-lookup.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [See the MLB schedule before first pitch](https://www.youtube.com/shorts/4VOTofCYCmk)

## When to use

Use this skill when the user wants:

- MLB teams, player search
- a repeatable export of public MLB data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `teamName`: Team Name
- `playerName`: Player Name
- `eventName`: Event Name
- `homeTeam`: Home Team
- `awayTeam`: Away Team
- `matchDate`: Match Date

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | teams | What data to fetch. |
| `searchQuery` | string | no | Shohei Ohtani | Player name for players mode. |
| `season` | string | no | 2024 | MLB season year. |
| `maxItems` | integer | no | 20 | Maximum records to return. |

Example (`references/example-input.json`):

```json
{
  "mode": "teams"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 20, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~mlb-teams-player-search-and-season-schedule-lookup/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~mlb-teams-player-search-and-season-schedule-lookup/runs" \
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
