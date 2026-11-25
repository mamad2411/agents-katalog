---
name: cfb-data
description: "College Football (CFB) data via ESPN public endpoints and the NCAA's official endpoints — scores, standings, rosters, schedules, game summaries, play-by-play, rankings, injuries, futures, team/player stats, and news for FBS, plus official FCS scoreboards, NCAA game detail with drive context, and the"
category: sports
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/machina-sports/sports-skills"
source_repository: "machina-sports/sports-skills"
source_path: "skills/cfb-data/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# College Football Data (CFB)

Before writing queries, consult `references/api-reference.md` for endpoints, conference IDs, team IDs, and data shapes.

## Setup

Before first use, check if the CLI is available:
```bash
which sports-skills || pip install sports-skills
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills cfb get_scoreboard
sports-skills cfb get_rankings
sports-skills cfb get_standings --group=8
```

## CRITICAL: Before Any Query

CRITICAL: Before calling any data endpoint, verify:
- Season year is derived from the system prompt's `currentDate` — never hardcoded.
- For standings, the `group` parameter is set to the correct conference ID (see `references/api-reference.md`).
- If only a team name is provided, use `get_teams` to resolve the team ID.

## Choosing the Season

Derive the current year from the system prompt's date (e.g., `currentDate: 2026-02-28` → current year is 2026).

- **If the user specifies a season**, use it as-is.
- **If the user says "current", "this season", or doesn't specify**: The CFB season runs August–January. If the current month is February–July (offseason), use `season = current_year - 1`. From August onward, use the current year.

## Important: College vs. Pro Differences

- **Standings are per-conference** — use the `group` parameter to filter
- **Rankings replace leaders** — college uses AP Top 25, Coaches Poll, and CFP rankings
- **Ranked teams** have a `rank` field (null = unranked) on scoreboard competitors
- **Week-based schedule** — like NFL, college football uses week numbers

## Commands

| Command | Description |
|---|---|
| `get_scoreboard` | Live/recent college football scores |
| `get_standings` | Standings by conference (use `group` parameter) |
| `get_teams` | All 750+ FBS college football teams |
| `get_team_roster` | Full roster for a team |
| `get_team_schedule` | Schedule for a specific team |
| `get_game_summary` | Detailed box score and scoring plays |
| `get_rankings` | AP Top 25, Coaches Poll, CFP rankings |
| `get_news` | College football news |
| `get_play_by_play` | Full play-by-play for a game |
| `get_win_probability` | Win probability timeline for a completed game |
| `get_schedule` | Season schedule by week |
| `get_injuries` | Injury reports across all teams |
| `get_futures` | Futures/odds markets (National Championship, Heisman, etc.) |
| `get_team_stats` | Team statistical profile |
| `get_player_stats` | Player statistical profile |
| `get_ncaa_scoreboard` | Official NCAA scoreboard — FBS and FCS |
| `get_ncaa_schedule` | Which weeks have games (official index) |
| `get_ncaa_game` | Official NCAA game information |
| `get_ncaa_boxscore` | Official NCAA box score |
| `get_ncaa_play_by_play` | Official play-by-play with drive context |
| `get_ncaa_scoring_summary` | Official scoring summary |
| `get_ncaa_schools` | NCAA schools index (all divisions) |

See `references/api-reference.md` for full parameter lists and return shapes.

## Official NCAA Backend

The `get_ncaa_*` commands read the NCAA's own endpoints (data.ncaa.com +
sdataprod.ncaa.com) — coverage ESPN does not carry:

- **FCS scoreboards** via `division="fcs"` — ESPN's college coverage is
  FBS-centric.
- **Official game detail**: `get_ncaa_game`, `get_ncaa_boxscore`,
  `get_ncaa_play_by_play` (with drive context), `get_ncaa_scoring_summary`.
- **The schools index** (~1,200 schools, all divisions): `get_ncaa_schools`.

NCAA game ids (e.g. `6306261`, from `get_ncaa_scoreboard`) and ESPN event ids
share nothing — join on game date plus team names. Football divisions are
`fbs`/`fcs` (not d1-d3). Game-detail commands ride NCAA's GraphQL persisted
queries, whose hashes rotate when ncaa.com redeploys; when that happens those
commands say so explicitly while the scoreboard/schedule commands keep working.

## Examples

Example 1: Current rankings
User says: "What are the college football rankings?"
Actions:
1. Call `get_rankings()`
Result: AP Top 25, Coaches Poll, and CFP rankings with rank, previous rank, record

Example 2: Conference standings
User says: "Show me SEC football standings"
Actions:
1. Derive season year from `currentDate`
2. Call `get_standings(group=8, season=<derived_year>)` (group 8 = SEC)
Result: SEC standings with W-L records per team

Example 3: Team schedule
User says: "What's Alabama's schedule this season?"
Actions:
1. Derive season year from `currentDate`
2. Call `get_team_schedule(team_id="333", season=<derived_year>)`
Result: Alabama's full season schedule with opponent, date, score (if played)

Example 4: Weekly scores
User says: "Show me this week's college football scores"
Actions:
1. Call `get_scoreboard()`
Result: All live and recent CFB games with scores and ranked status

Example 5: Heisman favorites
User says: "Who's the Heisman favorite?"
Actions:
1. Call `get_futures(limit=10)`
Result: Top Heisman Trophy candidates with odds values

Example 6: Team statistics
User says: "Show me Alabama's team stats"
Actions:
1. Derive season year from `currentDate`
2. Call `get_team_stats(team_id="333", season_year=<derived_year>)`
Result: Alabama's season stats by category with value, rank, and per-game averages

## Commands that DO NOT exist — never call these

- ~~`get_odds`~~ / ~~`get_betting_odds`~~ — not available. For prediction market odds, use the polymarket or kalshi skill.
- ~~`search_teams`~~ — does not exist. Use `get_teams` instead.
- ~~`get_box_score`~~ — does not exist. Use `get_game_summary` instead.
- ~~`get_player_ratings`~~ — does not exist. Use `get_player_stats` instead.
- ~~`get_bcs_rankings`~~ / ~~`get_playoff_rankings`~~ — does not exist. Use `get_rankings` instead.

If a command is not listed in the Commands table above, it does not exist.

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. If no events found for a date, check if it's in the off-season (CFB runs August–January)
2. If standings are empty without a group filter, try with a specific conference group
3. Only report failure with a clean message after exhausting alternatives

## Troubleshooting

Error: `sports-skills` command not found
Cause: Package not installed
Solution: Run `pip install sports-skills`

Error: No games found
Cause: CFB is seasonal (August–January); off-season scoreboard will be empty
Solution: Use `get_rankings` or `get_news` year-round; use `get_schedule` to find when the season starts

Error: Too many teams returned
Cause: `get_teams` returns 750+ FBS teams
Solution: Help users narrow down by suggesting specific team IDs from `references/api-reference.md`, or use ESPN URLs to look up IDs

Error: Rankings empty in off-season
Cause: Rankings are only published during the season and early off-season
Solution: Use `get_news` in the offseason; rankings resume in August
