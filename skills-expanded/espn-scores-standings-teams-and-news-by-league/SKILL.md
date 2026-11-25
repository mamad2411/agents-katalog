---
name: espn-scores-standings-teams-and-news-by-league
description: "Pull live and recent scores, league standings, team rosters, news headlines, and full game boxscores for NFL, NBA, MLB, NHL, MLS, Premier League, La Liga, F1, UFC, PGA Golf, ATP Tennis, and more. Output fields: mode, sport, league, homeScore, awayScore and more, as JSON rows. Use it for requests like \"ESPN scores, standings, teams\", or a CSV/JSON export of public ESPN data."
---

# ESPN Scores, Standings, Teams & News by League

Pull live and recent scores, league standings, team rosters, news headlines, and full game boxscores for NFL, NBA, MLB, NHL, MLS, Premier League, La Liga, F1, UFC, PGA Golf, ATP Tennis, and more.

- Actor: https://apify.com/vexaloom-labs/espn-scores-standings-teams-and-news-by-league (ID `vexaloom-labs~espn-scores-standings-teams-and-news-by-league`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/espn-scores-standings-teams-and-news-by-league.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- ESPN scores, standings, teams
- a repeatable export of public ESPN data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `mode`: Mode
- `sport`: Sport
- `league`: League
- `name`: Name
- `status`: Status
- `homeTeam`: Home Team
- `awayTeam`: Away Team
- `homeScore`: Home Score
- `awayScore`: Away Score
- `date`: Date

All 11 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | news | What to fetch from ESPN. |
| `league` | string | no | nba | League slug. The sport is derived automatically. |
| `leagues` | array | no |  | Optional multi-league override for modes that iterate leagues (scoreboard, odds, standings, teams, teamDetail, news, players, schedule, rankings), e.g. ["nba","nfl"]. |
| `datePreset` | string | no | today | Date window for scoreboard and odds. ESPN accepts one date per request, so ranges are fetched one day at a time. |
| `startDate` | string | no |  | First date for datePreset=custom, in YYYYMMDD or YYYY-MM-DD. |
| `endDate` | string | no |  | Last date for datePreset=custom (inclusive), in YYYYMMDD or YYYY-MM-DD. Maximum 366 days. |
| `season` | integer | no |  | ESPN season year for standings, schedule, players and rankings (e.g. 2025). Leave blank for the current season. |
| `seasonType` | string | no |  | Filter a team schedule by season phase (ignored for soccer schedules, which ESPN reports as one league season). |
| `teamIds` | array | no |  | Teams for teams/teamDetail/schedule/players. Accepts 2, BOS or nba/BOS. Get IDs from mode=teams. |
| `eventIds` | array | no |  | Games for gameDetail/odds. Accepts 401909904 or nba/401909904. Get IDs from mode=scoreboard. |
| `athleteQueries` | array | no |  | Player names to search, e.g. ["LeBron James", "Jannik Sinner"]. |
| `athleteIds` | array | no |  | ESPN athlete IDs for direct profiles, e.g. ["1966"]. |
| `rankingType` | string | no | all | Which poll to return. 'all' includes every poll ESPN publishes for the league. |
| `statusFilter` | string | no | all | Filter scoreboard, odds or schedule rows by game state. |

8 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "includeTeamDetails": false,
  "maxItems": 25,
  "mode": "news"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~espn-scores-standings-teams-and-news-by-league/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~espn-scores-standings-teams-and-news-by-league/runs" \
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
