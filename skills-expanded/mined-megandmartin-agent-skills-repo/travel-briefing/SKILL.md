---
name: travel-briefing
description: Builds a complete trip brief from itinerary details — timeline, documents checklist, weather and local context, and a concrete day-1 plan. Use when the user says "trip brief", "I'm flying to X", "prep me for my trip", "what do I need for Tokyo", or shares flight/hotel details. Don't use for scheduling meetings around the trip — use calendar-concierge — or for the daily brief at home — use morning-brief.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Travel, Planning, Briefing]
    related_skills: [calendar-concierge, morning-brief, file-organizer]
---

# Travel Briefing

Turns loose itinerary fragments — a flight confirmation, a hotel name, some dates — into one brief the traveler can trust at 5 a.m. in an airport: chronological timeline, documents checklist, local context with live weather, and a day-1 plan that survives jet lag. The standard: verified facts labeled as verified, assumptions labeled as assumptions, and the brief still works if every network call fails.

## When to Use

- User shares trip details and wants them organized ("flying to Bali on the 14th, back the 21st").
- Pre-departure prep: "what am I forgetting?", "build my trip brief".
- **Not for:** booking anything (this skill never books or pays), rearranging the calendar — use `calendar-concierge` — or the regular at-home brief — use `morning-brief`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Weather at destination | `curl -s --max-time 10 "wttr.in/Tokyo?format=3"` |
| 3-day forecast (compact) | `curl -s --max-time 10 "wttr.in/Tokyo?format=%l:+%c+%t+(%m)"` and `"wttr.in/Tokyo?1&Q&T"` |
| Time difference | `python3 -c "import zoneinfo,datetime as d; print(d.datetime.now(zoneinfo.ZoneInfo('Asia/Tokyo')).strftime('%H:%M %a'))"` |
| Trip-length math | `python3 -c "from datetime import date; print((date(2026,8,21)-date(2026,8,14)).days)"` |
| Gather source docs | `ls` the trip folder; `read_file` confirmations the user points to |
| Save the brief | `trip-brief-<dest>-<YYYY-MM>.md` in the trip folder |

## Procedure

1. **Precheck** — collect what's known: destination, dates, flights (numbers + times), lodging, purpose (work/leisure), passport nationality if visa questions matter. List what's missing in one batch question rather than dribbling questions throughout.
2. **Timeline** — build a chronological table from departure prep to return: check-in windows (long-haul: arrive 3h early), flight times **in local time of each airport**, layover durations, hotel check-in time, and known commitments. Compute the time difference with the python3 zoneinfo one-liner and state it plainly ("Tokyo is 1h ahead of Singapore").
3. **Documents checklist** — passport (flag if user should check expiry — many countries want 6 months' validity), visa/entry requirement (state what you know and mark it **verify against the official source** — never assert entry rules as certain), tickets, insurance, driving license if renting, and payment/SIM notes.
4. **Local context** — run the wttr.in calls for current weather and forecast. Add packing implications ("34°C and monsoon-season showers → light layers + compact umbrella"), plug type, currency, and one etiquette/safety note if relevant. **Offline degradation:** if curl times out or returns HTML, write "Weather unavailable — check before packing" and keep going; the brief never blocks on the network.
5. **Day-1 plan** — the jet-lag-proof version: airport → lodging route with a realistic duration and a fallback (train + taxi backup), earliest check-in, one easy food option near the lodging, and one anchor activity timed to fight the time-zone shift (daylight exposure if flying east). Nothing ambitious on day 1.
6. **Deliver** — assemble the template, mark every unverified item with ⚠️, save the file, and close with the 3 highest-priority to-dos before departure.

## Output Template

```
# Trip Brief — {Destination}, {dates} ({N} nights)
Time zone: {offset vs. home} · Weather now: {wttr line or "unavailable — check before packing"}

## Timeline
| When (local) | What | Details |
|---|---|---|
| {date HH:MM} | {flight/check-in/transfer} | {conf #, terminal, notes} |

## Documents
- [ ] Passport — ⚠️ verify ≥6 months validity for {country}
- [ ] Entry/visa: {what's known} — ⚠️ verify on the official immigration site
- [ ] {tickets, insurance, license, ...}

## Local context
Forecast: {3-day line} · Pack: {implications}
Currency {X} · Plug type {Y} · {one local note}

## Day 1 ({date})
{arrival → lodging route + fallback} → {food near base} → {one anchor activity} → early night.

## Before you go — top 3
1. {highest-priority open item}
```

## Pitfalls

- **Time zones scrambled** — a 23:55 departure landing "yesterday", or a layover computed across zones, produces a wrong timeline the traveler trusts. Recovery: express every time in its local airport zone, compute durations with python3, and sanity-check that arrival minus departure ≈ published flight time.
- **Visa rules asserted from memory** — entry requirements change; a confident wrong answer strands someone at a gate. Recovery: always phrase as "as of my knowledge" + ⚠️ verify-officially flag; never mark the visa checklist item as done.
- **wttr.in returns HTML or rate-limit junk** — pasted raw into the brief it looks broken. Recovery: if output exceeds ~80 chars or contains `<`, retry once, then degrade to the "unavailable" line; the brief must be complete without any network.
- **Day-1 plan ignores jet lag** — a 6-stop itinerary after a red-eye fails by noon. Recovery: day 1 gets one anchor activity maximum; move ambition to day 2.

## Verification

- [ ] Every timeline time is labeled with its local zone; durations recomputed, not copied
- [ ] All unverified claims (visa, hours, routes) carry the ⚠️ flag
- [ ] Weather lines are real curl output or an explicit "unavailable" fallback — no HTML fragments
- [ ] Brief reads complete even if every network call had failed
- [ ] Nothing was booked, purchased, or emailed; file saved to the trip folder
