---
name: frc-events
description: "FRC Events API skill. Use when working with FRC Events for root, {season}. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# FRC Events

## Auth
Basic username:password

## Base URL
https://frc-api.firstinspires.org/v3.0

## Setup
1. Configure auth: Basic username:password
2. GET / -- verify access

## Endpoints

19 endpoints across 2 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | API Index |

### {season}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{season} | Season Summary |
| GET | /{season}/events | Event Listings |
| GET | /{season}/districts | District Listings |
| GET | /{season}/teams | Team Listings |
| GET | /{season}/avatars | Team Avatar Listings |
| GET | /{season}/awards/event/{eventCode} | Event Awards |
| GET | /{season}/awards/list | Awards Listings |
| GET | /{season}/awards/team/{teamNumber} | Team Awards |
| GET | /{season}/awards/eventteam/{eventCode}/{teamNumber} | Event Team Awards |
| GET | /{season}/scores/{eventCode}/{tournamentLevel} | Score Details |
| GET | /{season}/matches/{eventCode} | Event Match Results |
| GET | /{season}/rankings/district/qualPerformanceCalculation | Qual Performance Points |
| GET | /{season}/rankings/district/allianceSelectionCalculation | Alliance Selection Points |
| GET | /{season}/rankings/district/playoffAdvancementCalculation | Playoff Advancement Points |
| GET | /{season}/rankings/{eventCode} | Event Rankings |
| GET | /{season}/rankings/district | District Rankings |
| GET | /{season}/schedule/{eventCode} | Event Schedule |
| GET | /{season}/alliances/{eventCode} | Event Alliances |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all events?" -> GET /{season}/events
- "List all districts?" -> GET /{season}/districts
- "List all teams?" -> GET /{season}/teams
- "List all avatars?" -> GET /{season}/avatars
- "Get event details?" -> GET /{season}/awards/event/{eventCode}
- "List all list?" -> GET /{season}/awards/list
- "Get team details?" -> GET /{season}/awards/team/{teamNumber}
- "Get eventteam details?" -> GET /{season}/awards/eventteam/{eventCode}/{teamNumber}
- "Get score details?" -> GET /{season}/scores/{eventCode}/{tournamentLevel}
- "Get matche details?" -> GET /{season}/matches/{eventCode}
- "List all qualPerformanceCalculation?" -> GET /{season}/rankings/district/qualPerformanceCalculation
- "List all allianceSelectionCalculation?" -> GET /{season}/rankings/district/allianceSelectionCalculation
- "List all playoffAdvancementCalculation?" -> GET /{season}/rankings/district/playoffAdvancementCalculation
- "Get ranking details?" -> GET /{season}/rankings/{eventCode}
- "List all district?" -> GET /{season}/rankings/district
- "Get schedule details?" -> GET /{season}/schedule/{eventCode}
- "Get alliance details?" -> GET /{season}/alliances/{eventCode}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
