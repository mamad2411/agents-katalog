---
name: sofascore-live-scores-standings-and-team-search-data
description: "Get SofaScore live scores, scheduled fixtures, league standings and team/player/tournament search results across 17 sports including football, basketball and tennis. Output fields: name, homeTeam, awayTeam, homeScore, awayScore and more, as JSON rows. Use it for requests like \"SofaScore live scores, standings\", or a CSV/JSON export of public SofaScore data."
---

# SofaScore Live Scores, Standings & Team Search Data

Get SofaScore live scores, scheduled fixtures, league standings and team/player/tournament search results across 17 sports including football, basketball and tennis.

- Actor: https://apify.com/vexaloom-labs/sofascore-live-scores-standings-and-team-search (ID `vexaloom-labs~sofascore-live-scores-standings-and-team-search`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/sofascore-live-scores-standings-and-team-search-data.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Build a live football score sheet by matchday](https://www.youtube.com/shorts/qMmkq9VlH8k)

## When to use

Use this skill when the user wants:

- SofaScore live scores, standings
- a repeatable export of public SofaScore data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `name`: Name
- `eventId`: Event Id
- `homeTeam`: Home Team
- `awayTeam`: Away Team
- `homeScore`: Home Score
- `awayScore`: Away Score
- `status`: Status
- `startTime`: Start Time
- `sport`: Sport
- `tournamentName`: Tournament Name
- `teamId`: Team Id
- `playerId`: Player Id
- `points`: Points
- `rankingTypeName`: Ranking Type Name

All 16 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | What to fetch from SofaScore. |
| `searchQueries` | array | no |  | Team, player, tournament or match names to resolve (mode=search). |
| `searchType` | string | no | all | Restrict search results to one entity type (mode=search). |
| `sports` | array | no | ["football"] | Sports for live and scheduled modes. Supported: football, basketball, tennis, american-football, aussie-rules, ice-hockey, handball, rugby, futsal, minifootball, floorball… |
| `date` | string | no |  | Start date for fixtures (mode=scheduled), format YYYY-MM-DD. Defaults to today UTC. |
| `daysAhead` | integer | no | 0 | Number of extra days after Date to include (mode=scheduled). |
| `teamIds` | array | no |  | SofaScore team IDs or team page URLs (mode=team). |
| `playerIds` | array | no |  | SofaScore player IDs or player page URLs (mode=player). |
| `tournamentIds` | array | no |  | SofaScore unique-tournament IDs or tournament page URLs (modes tournament, standings). |
| `eventIds` | array | no |  | SofaScore match IDs or match page URLs (mode=event). |
| `seasonId` | integer | no |  | Optional season ID for standings or tournament mode. If omitted, the latest season with a table is used. |
| `tableType` | string | no | total | Standings table to fetch (modes standings, tournament). |
| `rankingType` | string | no | fifa | Ranking table to fetch (mode=rankings). |
| `includeStatistics` | boolean | no | true | Add team and player statistics to match records. |

12 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "searchQueries": [
    "Real Madrid"
  ],
  "includeStatistics": false,
  "includeLineups": false,
  "includeIncidents": false,
  "maxItems": 25,
  "mode": "search"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~sofascore-live-scores-standings-and-team-search/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~sofascore-live-scores-standings-and-team-search/runs" \
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
