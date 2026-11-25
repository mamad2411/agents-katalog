---
name: college-football-data-api
description: "College Football Data API skill. Use when working with College Football Data for wepa, teams, roster. Covers 60 endpoints."
version: 1.0.0
generator: lapsh
---

# College Football Data API
API version: 5.13.2

## Auth
Bearer bearer

## Base URL
https://api.collegefootballdata.com/

## Setup
1. Set Authorization header with your Bearer token
2. GET /wepa/team/season -- verify access

## Endpoints

60 endpoints across 25 groups. See references/api-spec.lap for full details.

### wepa
| Method | Path | Description |
|--------|------|-------------|
| GET | /wepa/team/season | Retrieve opponent-adjusted team season statistics |
| GET | /wepa/players/passing | Retrieve opponent-adjusted player passing statistics |
| GET | /wepa/players/rushing | Retrieve opponent-adjusted player rushing statistics |
| GET | /wepa/players/kicking | Retrieve Points Added Above Replacement (PAAR) ratings for kickers |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams | Retrieves team information |
| GET | /teams/fbs | Retrieves information on teams playing in the highest division of CFB |
| GET | /teams/matchup | Retrieves historical matchup details for two given teams |
| GET | /teams/ats | Retrieves against-the-spread (ATS) summary by team |

### roster
| Method | Path | Description |
|--------|------|-------------|
| GET | /roster | Retrieves historical roster data |

### conferences
| Method | Path | Description |
|--------|------|-------------|
| GET | /conferences | Retrieves list of conferences |

### talent
| Method | Path | Description |
|--------|------|-------------|
| GET | /talent | Retrieve 247 Team Talent Composite for a given year |

### venues
| Method | Path | Description |
|--------|------|-------------|
| GET | /venues | Retrieve list of venues |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats/player/season | Retrieves aggregated player statistics for a given season |
| GET | /stats/season | Retrieves aggregated team season statistics |
| GET | /stats/categories | Gets team statistical categories |
| GET | /stats/season/advanced | Retrieves advanced season statistics for teams |
| GET | /stats/game/advanced | Retrieves advanced statistics aggregated by game |
| GET | /stats/game/havoc | Retrieves havoc statistics aggregated by game |

### recruiting
| Method | Path | Description |
|--------|------|-------------|
| GET | /recruiting/players | Retrieves player recruiting rankings |
| GET | /recruiting/teams | Retrieves team recruiting rankings |
| GET | /recruiting/groups | Retrieves aggregated recruiting statistics by team and position grouping |

### ratings
| Method | Path | Description |
|--------|------|-------------|
| GET | /ratings/sp | Retrieves SP+ ratings for a given year or school |
| GET | /ratings/sp/conferences | Retrieves aggregated historical conference SP+ data |
| GET | /ratings/srs | Retrieves historical SRS for a year or team |
| GET | /ratings/elo | Retrieves historical Elo ratings |
| GET | /ratings/fpi | Retrieves historical Football Power Index (FPI) ratings |

### rankings
| Method | Path | Description |
|--------|------|-------------|
| GET | /rankings | Retrieves historical poll data |

### plays
| Method | Path | Description |
|--------|------|-------------|
| GET | /plays | Retrieves historical play data |
| GET | /plays/types | Retrieves available play types |
| GET | /plays/stats | Retrieve player-play associations (limit 2000) |
| GET | /plays/stats/types | Retrieves available play stat types |

### player
| Method | Path | Description |
|--------|------|-------------|
| GET | /player/search | Search for players (lists top 100 results) |
| GET | /player/usage | Retrieves player usage data for a given season |
| GET | /player/returning | Retrieves returning production data. Either a year or team filter must be specified. |
| GET | /player/portal | Retrieves transfer portal data for a given year |

### ppa
| Method | Path | Description |
|--------|------|-------------|
| GET | /ppa/predicted | Query Predicted Points values by down and distance |
| GET | /ppa/teams | Retrieves historical team PPA metrics by season |
| GET | /ppa/games | Retrieves historical team PPA metrics by game |
| GET | /ppa/players/games | Queries player PPA statistics by game |
| GET | /ppa/players/season | Queries player PPA statistics by season |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics/wp | Query play win probabilities by game |
| GET | /metrics/wp/pregame | Queries pregame win probabilities |
| GET | /metrics/fg/ep | Queries field goal expected points values |

### live
| Method | Path | Description |
|--------|------|-------------|
| GET | /live/plays | Queries live play-by-play data and advanced stats |

### lines
| Method | Path | Description |
|--------|------|-------------|
| GET | /lines | Retrieves historical betting data |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Retrieves information about the user, including their Patreon level and remaining API calls. |

### games
| Method | Path | Description |
|--------|------|-------------|
| GET | /games | Retrieves historical game data |
| GET | /games/teams | Retrieves team box score statistics |
| GET | /games/players | Retrieves player box score statistics |
| GET | /games/media | Retrieves media information for games |
| GET | /games/weather | Retrieve historical and future weather data (Patreon only) |

### records
| Method | Path | Description |
|--------|------|-------------|
| GET | /records | Retrieves historical team records |

### calendar
| Method | Path | Description |
|--------|------|-------------|
| GET | /calendar | Retrieves calendar information |

### scoreboard
| Method | Path | Description |
|--------|------|-------------|
| GET | /scoreboard | Retrieves live scoreboard data |

### drives
| Method | Path | Description |
|--------|------|-------------|
| GET | /drives | Retrieves historical drive data |

### draft
| Method | Path | Description |
|--------|------|-------------|
| GET | /draft/teams | Retrieves list of NFL teams |
| GET | /draft/positions | Retrieves list of player position categories for the NFL Draft |
| GET | /draft/picks | Retrieve historical NFL draft data |

### coaches
| Method | Path | Description |
|--------|------|-------------|
| GET | /coaches | Retrieves historical head coach information and records |

### game
| Method | Path | Description |
|--------|------|-------------|
| GET | /game/box/advanced | Retrieves an advanced box score for a game |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all season?" -> GET /wepa/team/season
- "List all passing?" -> GET /wepa/players/passing
- "List all rushing?" -> GET /wepa/players/rushing
- "List all kicking?" -> GET /wepa/players/kicking
- "List all teams?" -> GET /teams
- "List all fbs?" -> GET /teams/fbs
- "List all matchup?" -> GET /teams/matchup
- "List all ats?" -> GET /teams/ats
- "List all roster?" -> GET /roster
- "List all conferences?" -> GET /conferences
- "List all talent?" -> GET /talent
- "List all venues?" -> GET /venues
- "List all season?" -> GET /stats/player/season
- "List all season?" -> GET /stats/season
- "List all categories?" -> GET /stats/categories
- "List all advanced?" -> GET /stats/season/advanced
- "List all advanced?" -> GET /stats/game/advanced
- "List all havoc?" -> GET /stats/game/havoc
- "List all players?" -> GET /recruiting/players
- "List all teams?" -> GET /recruiting/teams
- "List all groups?" -> GET /recruiting/groups
- "List all sp?" -> GET /ratings/sp
- "List all conferences?" -> GET /ratings/sp/conferences
- "List all srs?" -> GET /ratings/srs
- "List all elo?" -> GET /ratings/elo
- "List all fpi?" -> GET /ratings/fpi
- "List all rankings?" -> GET /rankings
- "List all plays?" -> GET /plays
- "List all types?" -> GET /plays/types
- "List all stats?" -> GET /plays/stats
- "List all types?" -> GET /plays/stats/types
- "List all search?" -> GET /player/search
- "List all usage?" -> GET /player/usage
- "List all returning?" -> GET /player/returning
- "List all portal?" -> GET /player/portal
- "List all predicted?" -> GET /ppa/predicted
- "List all teams?" -> GET /ppa/teams
- "List all games?" -> GET /ppa/games
- "List all games?" -> GET /ppa/players/games
- "List all season?" -> GET /ppa/players/season
- "List all wp?" -> GET /metrics/wp
- "List all pregame?" -> GET /metrics/wp/pregame
- "List all ep?" -> GET /metrics/fg/ep
- "List all plays?" -> GET /live/plays
- "List all lines?" -> GET /lines
- "List all info?" -> GET /info
- "List all games?" -> GET /games
- "List all teams?" -> GET /games/teams
- "List all players?" -> GET /games/players
- "List all media?" -> GET /games/media
- "List all weather?" -> GET /games/weather
- "List all records?" -> GET /records
- "List all calendar?" -> GET /calendar
- "List all scoreboard?" -> GET /scoreboard
- "List all drives?" -> GET /drives
- "List all teams?" -> GET /draft/teams
- "List all positions?" -> GET /draft/positions
- "List all picks?" -> GET /draft/picks
- "List all coaches?" -> GET /coaches
- "List all advanced?" -> GET /game/box/advanced
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
