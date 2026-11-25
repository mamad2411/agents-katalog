---
name: rank-tracking
description: Use when the user wants to track Google rankings over time for rank-and-rent or client sites, check "has it ranked yet", set up scheduled SERP position monitoring, or validate the 12-week ranking test for a new site. Also when asked "where does [site] rank for [keyword]".
---

# Rank Tracking (DataForSEO)

## Overview

Weekly SERP position log per keyword per site, with alerts when a site enters/leaves the top 3. This is the measurement for the rank-and-rent methodology test ("if it doesn't rank in 12 weeks, the methodology has a problem").

## Setup

Portfolio config lives at `~/Dropbox/Projects/Rank and Rent/tools/rank-tracking/keywords.json`. Credentials come from `Rank and Rent/.env` (`DATAFORSEO_LOGIN`/`DATAFORSEO_PASSWORD`) — the script auto-loads the `.env` next to or one level above the config.

Config entry per tracked keyword:
```json
{"keyword": "mobile mechanic york", "domain": "mobilemechanicyork.co.uk",
 "location": "York,England,United Kingdom", "device": "mobile"}
```
`device` defaults to mobile (local-intent searches are mobile-first). Add one entry per site at launch (step 7 of the rank-and-rent factory).

## Run

```bash
python3 ~/.agents/skills/rank-tracking/track.py \
  "$HOME/Dropbox/Projects/Rank and Rent/tools/rank-tracking/keywords.json"
```

- Appends one JSONL row per keyword to `rank-log.jsonl` next to the config: `position` (organic rank — the headline number), `absolute` (full-SERP rank incl. ads/local pack), `top3` domains.
- Prints a summary table + `ALERT:` lines on top-3 entry/exit vs the previous run.
- Cost: ~fractions of a penny per keyword per run (live SERP query).

## Scheduling

Weekly is the right cadence (daily burns money on noise). Use the `schedule` skill / cron to run the command above every Monday and report the table + any ALERT lines. When reporting, also compute weeks-since-first-log-entry per keyword — flags the 12-week validation deadline.

## Reading Results

| Signal | Meaning |
|---|---|
| `position` 1–3 | Rentable — lead flow territory |
| `position` improving week-over-week | Methodology working; keep building links/content |
| `position` null after 12 weeks | Methodology problem per George's own test — review, don't just wait |
| `position` good but `absolute` poor | Organic rank fine but ads/local pack push it down the page — consider the local pack angle (but note: no GBP for rank-and-rent sites) |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Tracking without `location` | UK-wide rank is meaningless for "boiler repair tiverton". Always set the town-level location. |
| Reporting `absolute` as "the rank" | George means organic position when he asks "where does it rank". Report both, lead with organic. |
| Re-running many times a day to watch it move | SERPs wobble; weekly trend is the signal. Each run costs API credit. |
| Adding a keyword but no domain | The script matches your domain in results — both fields required. |
