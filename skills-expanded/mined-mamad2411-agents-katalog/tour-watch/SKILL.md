---
name: tour-watch
skill_id: browser-skill:tour-watch
description: New tour dates and presales for the artists you actually listen to
when_to_use:
  - intent_keywords: [tour, tour dates, presale, tickets, on sale, concert, artist announcement]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: tour dates announced this week and the cities on the run for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: presale times, codes and general on sale dates for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 4
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: artists
    current_value: 2026 tour dates announced
    fill_rule: name the artists you would actually travel for
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [music, tours, tickets, presales, weekly]
    related_skills: []
platforms: [macos]
---
# Tour watch

## Purpose
Wednesday morning, the week's tour announcements for the artists on the user's
list. Presale time, on sale time, nearest city. So the calendar entry exists
before tickets do.

## Reads
- Search results for tour dates announced this week and the cities on the run for 2026 tour dates announced.
- Search results for presale times, codes and general on sale dates for 2026 tour dates announced.

## Lands in
- Names the artist, the venue, the show date and the on sale time. Short enough to act on straight away.

## Steps
1. Look up tour dates announced this week and the cities on the run for 2026 tour dates announced.
2. Look up presale times, codes and general on sale dates for 2026 tour dates announced.
3. Names the artist, the venue, the show date and the on sale time.

## Success criteria
- Names the artist, the venue, the show date and the on sale time.
- Gives the nearest city to the user, and one drivable second option.
- Says plainly which dates are already gone rather than listing them anyway.
- Says the time in the user's own time zone, not the venue's.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If nobody on the list announced anything, say so in one line and name who is
  rumored to be touring next.

## Never
- Never sign in, buy tickets, join a presale or enter a queue.
- Never invent a date, a venue, a presale code or an on sale time.
- Never pass a resale listing off as an official on sale.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
