---
name: flight-skill
description: Look up live flight status, track connecting flights, and check airport delays. Use when the user asks to check a flight, track someone's trip, or look up airport conditions.
allowed-tools: Bash, Read
---

# Flight Skill - Live Flight Tracking

Track flights in real-time using FlightRadar24 data. No API key required.

## Commands

### Check a single flight

```bash
python3 ~/.claude/skills/flight-skill/flight_skill.py status WN3971
python3 ~/.claude/skills/flight-skill/flight_skill.py status UA123 --date 2026-03-16
python3 ~/.claude/skills/flight-skill/flight_skill.py status SWA3971 --live
python3 ~/.claude/skills/flight-skill/flight_skill.py status WN3971 --json
python3 ~/.claude/skills/flight-skill/flight_skill.py status WN3971 -v
```

### Track a connecting trip

```bash
# Multiple flight numbers in order - includes connection analysis
python3 ~/.claude/skills/flight-skill/flight_skill.py trip WN3971 WN1267
python3 ~/.claude/skills/flight-skill/flight_skill.py trip WN3971 WN1267 --date 2026-03-16
python3 ~/.claude/skills/flight-skill/flight_skill.py trip UA100 UA456 DL789 --json
```

### Airport flight board

```bash
python3 ~/.claude/skills/flight-skill/flight_skill.py airport MDW --arrivals
python3 ~/.claude/skills/flight-skill/flight_skill.py airport SFO --departures
python3 ~/.claude/skills/flight-skill/flight_skill.py airport MDW --departures --json
```

## Flight Number Formats

Accepts multiple formats - auto-converts ICAO to IATA:
- `WN3971` (IATA - preferred)
- `SWA3971` (ICAO - auto-converts to WN3971)
- `UA123`, `UAL123`, `DL456`, `DAL456`, `AA789`, `AAL789`

## Features

- Real-time flight status (scheduled, delayed, in-air, landed, cancelled)
- Departure and arrival times in local timezone
- Delay calculation in minutes
- Connection analysis for multi-leg trips (flags tight/missed connections)
- Aircraft info with --verbose flag
- JSON output for programmatic use

## Output

- **ON TIME** (green) - flight on schedule
- **MINOR DELAY** (yellow) - small delay
- **DELAYED** (red) - significant delay
- **SCHEDULED** (gray) - future flight, no live data yet
- **[LIVE - IN AIR]** - currently airborne

## Data Source

FlightRadar24 public API. No auth required. Data updates every 30-60 seconds for live flights.

## Requirements

- Python 3.9+ (standard library only, no pip installs needed)

## Examples

```bash
# "Is my mom's flight delayed?"
python3 ~/.claude/skills/flight-skill/flight_skill.py status WN3971

# "Will she make her connection?"
python3 ~/.claude/skills/flight-skill/flight_skill.py trip WN3971 WN1267

# "What's going on at Midway?"
python3 ~/.claude/skills/flight-skill/flight_skill.py airport MDW --departures
```
