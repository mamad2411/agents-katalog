---
name: the-blue-alliance-api-v3
description: "The Blue Alliance API v3 API skill. Use when working with The Blue Alliance API v3 for district, districts, event. Covers 80 endpoints."
version: 1.0.0
generator: lapsh
---

# The Blue Alliance API v3
API version: 3.12.0

## Auth
ApiKey X-TBA-Auth-Key in header

## Base URL
https://www.thebluealliance.com/api/v3

## Setup
1. Set your API key in the appropriate header
2. GET /search_index -- verify access

## Endpoints

80 endpoints across 11 groups. See references/api-spec.lap for full details.

### district
| Method | Path | Description |
|--------|------|-------------|
| GET | /district/{district_abbreviation}/dcmp_history | Gets a list of DCMP events and awards for the given district abbreviation. |
| GET | /district/{district_abbreviation}/history | Gets a list of District objects with the given district abbreviation. This accounts for district abbreviation changes, such as MAR to FMA. |
| GET | /district/{district_abbreviation}/insights | Gets insights for a given district. |
| GET | /district/{district_key}/advancement | Gets a list of advancement information per team in a district. |
| GET | /district/{district_key}/awards | Gets a list of awards in the given district. |
| GET | /district/{district_key}/events | Gets a list of events in the given district. |
| GET | /district/{district_key}/events/keys | Gets a list of event keys for events in the given district. |
| GET | /district/{district_key}/events/simple | Gets a short-form list of events in the given district. |
| GET | /district/{district_key}/rankings | Gets a list of team district rankings for the given district. |
| GET | /district/{district_key}/teams | Gets a list of `Team` objects that competed in events in the given district. |
| GET | /district/{district_key}/teams/keys | Gets a list of `Team` objects that competed in events in the given district. |
| GET | /district/{district_key}/teams/simple | Gets a short-form list of `Team` objects that competed in events in the given district. |

### districts
| Method | Path | Description |
|--------|------|-------------|
| GET | /districts/{year} | Gets a list of districts and their corresponding district key, for the given year. |

### event
| Method | Path | Description |
|--------|------|-------------|
| GET | /event/{event_key} | Gets an Event. |
| GET | /event/{event_key}/advancement_points | Depending on the type of event (district/regional), this will return either district points or regional CMP points |
| GET | /event/{event_key}/alliances | Gets a list of Elimination Alliances for the given Event. |
| GET | /event/{event_key}/awards | Gets a list of awards from the given event. |
| GET | /event/{event_key}/coprs | Gets a set of Event Component OPRs for the given Event. |
| GET | /event/{event_key}/district_points | Gets a list of district points for the Event. These are always calculated, regardless of event type, and may/may not be actually useful. |
| GET | /event/{event_key}/insights | Gets a set of Event-specific insights for the given Event. |
| GET | /event/{event_key}/matches | Gets a list of matches for the given event. |
| GET | /event/{event_key}/matches/keys | Gets a list of match keys for the given event. |
| GET | /event/{event_key}/matches/simple | Gets a short-form list of matches for the given event. |
| GET | /event/{event_key}/matches/timeseries | Gets an array of Match Keys for the given event key that have timeseries data. Returns an empty array if no matches have timeseries data. |
| GET | /event/{event_key}/oprs | Gets a set of Event OPRs (including OPR, DPR, and CCWM) for the given Event. |
| GET | /event/{event_key}/predictions | Gets information on TBA-generated predictions for the given Event. Contains year-specific information. *WARNING* This endpoint is currently under development and may change at any time. |
| GET | /event/{event_key}/rankings | Gets a list of team rankings for the Event. |
| GET | /event/{event_key}/regional_champs_pool_points | For 2025+ Regional events, this will return points towards the Championship qualification pool. |
| GET | /event/{event_key}/simple | Gets a short-form Event. |
| GET | /event/{event_key}/team_media | Gets a list of media objects that correspond to teams at this event. |
| GET | /event/{event_key}/teams | Gets a list of `Team` objects that competed in the given event. |
| GET | /event/{event_key}/teams/keys | Gets a list of `Team` keys that competed in the given event. |
| GET | /event/{event_key}/teams/simple | Gets a short-form list of `Team` objects that competed in the given event. |
| GET | /event/{event_key}/teams/statuses | Gets a key-value list of the event statuses for teams competing at the given event. |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/{year} | Gets a list of events in the given year. |
| GET | /events/{year}/keys | Gets a list of event keys in the given year. |
| GET | /events/{year}/simple | Gets a short-form list of events in the given year. |

### insights
| Method | Path | Description |
|--------|------|-------------|
| GET | /insights/leaderboards/{year} | Gets a list of `LeaderboardInsight` objects from a specific year. Use year=0 for overall. |
| GET | /insights/notables/{year} | Gets a list of `NotablesInsight` objects from a specific year. Use year=0 for overall. |

### match
| Method | Path | Description |
|--------|------|-------------|
| GET | /match/{match_key} | Gets a `Match` object for the given match key. |
| GET | /match/{match_key}/simple | Gets a short-form `Match` object for the given match key. |
| GET | /match/{match_key}/timeseries | Gets an array of game-specific Match Timeseries objects for the given match key or an empty array if not available. |
| GET | /match/{match_key}/zebra_motionworks | Gets Zebra MotionWorks data for a Match for the given match key. |

### regional_advancement
| Method | Path | Description |
|--------|------|-------------|
| GET | /regional_advancement/{year} | Gets information about per-team advancement to the FIRST Championship. |
| GET | /regional_advancement/{year}/rankings | Gets the team rankings in the regional pool for a specific year. |

### search_index
| Method | Path | Description |
|--------|------|-------------|
| GET | /search_index | Gets a large blob of data that is used on the frontend for searching. May change without notice. |

### status
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Returns API status, and TBA status information. |

### team
| Method | Path | Description |
|--------|------|-------------|
| GET | /team/{team_key} | Gets a `Team` object for the team referenced by the given key. |
| GET | /team/{team_key}/awards | Gets a list of awards the given team has won. |
| GET | /team/{team_key}/awards/{year} | Gets a list of awards the given team has won in a given year. |
| GET | /team/{team_key}/districts | Gets an array of districts representing each year the team was in a district. Will return an empty array if the team was never in a district. |
| GET | /team/{team_key}/event/{event_key}/awards | Gets a list of awards the given team won at the given event. |
| GET | /team/{team_key}/event/{event_key}/matches | Gets a list of matches for the given team and event. |
| GET | /team/{team_key}/event/{event_key}/matches/keys | Gets a list of match keys for matches for the given team and event. |
| GET | /team/{team_key}/event/{event_key}/matches/simple | Gets a short-form list of matches for the given team and event. |
| GET | /team/{team_key}/event/{event_key}/status | Gets the competition rank and status of the team at the given event. |
| GET | /team/{team_key}/events | Gets a list of all events this team has competed at. |
| GET | /team/{team_key}/events/keys | Gets a list of the event keys for all events this team has competed at. |
| GET | /team/{team_key}/events/simple | Gets a short-form list of all events this team has competed at. |
| GET | /team/{team_key}/events/{year} | Gets a list of events this team has competed at in the given year. |
| GET | /team/{team_key}/events/{year}/keys | Gets a list of the event keys for events this team has competed at in the given year. |
| GET | /team/{team_key}/events/{year}/simple | Gets a short-form list of events this team has competed at in the given year. |
| GET | /team/{team_key}/events/{year}/statuses | Gets a key-value list of the event statuses for events this team has competed at in the given year. |
| GET | /team/{team_key}/history | Gets the history for the team referenced by the given key, including their events and awards. |
| GET | /team/{team_key}/matches/{year} | Gets a list of matches for the given team and year. |
| GET | /team/{team_key}/matches/{year}/keys | Gets a list of match keys for matches for the given team and year. |
| GET | /team/{team_key}/matches/{year}/simple | Gets a short-form list of matches for the given team and year. |
| GET | /team/{team_key}/media/tag/{media_tag} | Gets a list of Media (videos / pictures) for the given team and tag. |
| GET | /team/{team_key}/media/tag/{media_tag}/{year} | Gets a list of Media (videos / pictures) for the given team, tag and year. |
| GET | /team/{team_key}/media/{year} | Gets a list of Media (videos / pictures) for the given team and year. |
| GET | /team/{team_key}/robots | Gets a list of year and robot name pairs for each year that a robot name was provided. Will return an empty array if the team has never named a robot. |
| GET | /team/{team_key}/simple | Gets a `Team_Simple` object for the team referenced by the given key. |
| GET | /team/{team_key}/social_media | Gets a list of Media (social media) for the given team. |
| GET | /team/{team_key}/years_participated | Gets a list of years in which the team participated in at least one competition. |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/{page_num} | Gets a list of `Team` objects, paginated in groups of 500. |
| GET | /teams/{page_num}/keys | Gets a list of Team keys, paginated in groups of 500. (Note, each page will not have 500 teams, but will include the teams within that range of 500.) |
| GET | /teams/{page_num}/simple | Gets a list of short form `Team_Simple` objects, paginated in groups of 500. |
| GET | /teams/{year}/{page_num} | Gets a list of `Team` objects that competed in the given year, paginated in groups of 500. |
| GET | /teams/{year}/{page_num}/keys | Gets a list Team Keys that competed in the given year, paginated in groups of 500. |
| GET | /teams/{year}/{page_num}/simple | Gets a list of short form `Team_Simple` objects that competed in the given year, paginated in groups of 500. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all dcmp_history?" -> GET /district/{district_abbreviation}/dcmp_history
- "List all history?" -> GET /district/{district_abbreviation}/history
- "List all insights?" -> GET /district/{district_abbreviation}/insights
- "List all advancement?" -> GET /district/{district_key}/advancement
- "List all awards?" -> GET /district/{district_key}/awards
- "List all events?" -> GET /district/{district_key}/events
- "List all keys?" -> GET /district/{district_key}/events/keys
- "List all simple?" -> GET /district/{district_key}/events/simple
- "List all rankings?" -> GET /district/{district_key}/rankings
- "List all teams?" -> GET /district/{district_key}/teams
- "List all keys?" -> GET /district/{district_key}/teams/keys
- "List all simple?" -> GET /district/{district_key}/teams/simple
- "Get district details?" -> GET /districts/{year}
- "Get event details?" -> GET /event/{event_key}
- "List all advancement_points?" -> GET /event/{event_key}/advancement_points
- "List all alliances?" -> GET /event/{event_key}/alliances
- "List all awards?" -> GET /event/{event_key}/awards
- "List all coprs?" -> GET /event/{event_key}/coprs
- "List all district_points?" -> GET /event/{event_key}/district_points
- "List all insights?" -> GET /event/{event_key}/insights
- "List all matches?" -> GET /event/{event_key}/matches
- "List all keys?" -> GET /event/{event_key}/matches/keys
- "List all simple?" -> GET /event/{event_key}/matches/simple
- "List all timeseries?" -> GET /event/{event_key}/matches/timeseries
- "List all oprs?" -> GET /event/{event_key}/oprs
- "List all predictions?" -> GET /event/{event_key}/predictions
- "List all rankings?" -> GET /event/{event_key}/rankings
- "List all regional_champs_pool_points?" -> GET /event/{event_key}/regional_champs_pool_points
- "List all simple?" -> GET /event/{event_key}/simple
- "List all team_media?" -> GET /event/{event_key}/team_media
- "List all teams?" -> GET /event/{event_key}/teams
- "List all keys?" -> GET /event/{event_key}/teams/keys
- "List all simple?" -> GET /event/{event_key}/teams/simple
- "List all statuses?" -> GET /event/{event_key}/teams/statuses
- "Get event details?" -> GET /events/{year}
- "List all keys?" -> GET /events/{year}/keys
- "List all simple?" -> GET /events/{year}/simple
- "Get leaderboard details?" -> GET /insights/leaderboards/{year}
- "Get notable details?" -> GET /insights/notables/{year}
- "Get match details?" -> GET /match/{match_key}
- "List all simple?" -> GET /match/{match_key}/simple
- "List all timeseries?" -> GET /match/{match_key}/timeseries
- "List all zebra_motionworks?" -> GET /match/{match_key}/zebra_motionworks
- "Get regional_advancement details?" -> GET /regional_advancement/{year}
- "List all rankings?" -> GET /regional_advancement/{year}/rankings
- "List all search_index?" -> GET /search_index
- "List all status?" -> GET /status
- "Get team details?" -> GET /team/{team_key}
- "List all awards?" -> GET /team/{team_key}/awards
- "Get award details?" -> GET /team/{team_key}/awards/{year}
- "List all districts?" -> GET /team/{team_key}/districts
- "List all awards?" -> GET /team/{team_key}/event/{event_key}/awards
- "List all matches?" -> GET /team/{team_key}/event/{event_key}/matches
- "List all keys?" -> GET /team/{team_key}/event/{event_key}/matches/keys
- "List all simple?" -> GET /team/{team_key}/event/{event_key}/matches/simple
- "List all status?" -> GET /team/{team_key}/event/{event_key}/status
- "List all events?" -> GET /team/{team_key}/events
- "List all keys?" -> GET /team/{team_key}/events/keys
- "List all simple?" -> GET /team/{team_key}/events/simple
- "Get event details?" -> GET /team/{team_key}/events/{year}
- "List all keys?" -> GET /team/{team_key}/events/{year}/keys
- "List all simple?" -> GET /team/{team_key}/events/{year}/simple
- "List all statuses?" -> GET /team/{team_key}/events/{year}/statuses
- "List all history?" -> GET /team/{team_key}/history
- "Get matche details?" -> GET /team/{team_key}/matches/{year}
- "List all keys?" -> GET /team/{team_key}/matches/{year}/keys
- "List all simple?" -> GET /team/{team_key}/matches/{year}/simple
- "Get tag details?" -> GET /team/{team_key}/media/tag/{media_tag}
- "Get tag details?" -> GET /team/{team_key}/media/tag/{media_tag}/{year}
- "Get media details?" -> GET /team/{team_key}/media/{year}
- "List all robots?" -> GET /team/{team_key}/robots
- "List all simple?" -> GET /team/{team_key}/simple
- "List all social_media?" -> GET /team/{team_key}/social_media
- "List all years_participated?" -> GET /team/{team_key}/years_participated
- "Get team details?" -> GET /teams/{page_num}
- "List all keys?" -> GET /teams/{page_num}/keys
- "List all simple?" -> GET /teams/{page_num}/simple
- "Get team details?" -> GET /teams/{year}/{page_num}
- "List all keys?" -> GET /teams/{year}/{page_num}/keys
- "List all simple?" -> GET /teams/{year}/{page_num}/simple
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
