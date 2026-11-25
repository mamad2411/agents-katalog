---
name: free-museum-day
skill_id: browser-skill:free-museum-day
description: Which museums near you are free, and on exactly which night
when_to_use:
  - intent_keywords: [free museum, museum day, free admission, gallery, first thursday, museum night]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: free museum days, free evenings and resident free admission near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: this month's free admission dates, hours and whether tickets must be claimed ahead near
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: museums
    current_value: free museum days in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [museums, free, local, weekly, culture]
    related_skills: [browser-skill:art-break]
platforms: [macos]
---
# Free museum day

## Purpose
Thursday morning, because Thursday evening is when the free hours actually
land. Most cities have a museum that is free tonight and the people who live
there have been paying full price for years.

## Reads
- Search results for free museum days, free evenings and resident free admission near free museum days in Los Angeles.
- Search results for this month's free admission dates, hours and whether tickets must be claimed ahead near free museum days in Los Angeles.

## Lands in
- Names the exact weekday, since free evenings cluster on Thursdays and first Fridays and the pattern differs museum by museum. Short enough to act on straight away.

## Steps
1. Look up free museum days, free evenings and resident free admission near free museum days in Los Angeles.
2. Look up this month's free admission dates, hours and whether tickets must be claimed ahead near free museum days in Los Angeles.
3. Names the exact weekday, since free evenings cluster on Thursdays and first Fridays and the pattern differs museum by museum.

## Success criteria
- Names the exact weekday, since free evenings cluster on Thursdays and first
  Fridays and the pattern differs museum by museum.
- Flags Bank of America and Merrill cardholders getting free general admission
  on the first full weekend of every month at over 235 institutions, and that it
  excludes special exhibitions.
- Flags Museums for All, where an EBT card gets four people in for three dollars
  or less at over 600 museums, and out of state EBT cards are accepted.
- Surfaces resident only free admission that visitors never see, like Illinois
  residents free at the Field Museum on Wednesdays, and says what ID proves it.
- Mentions when a reciprocal membership beats paying, since one membership at
  the cheapest participating museum covers entry at over 1500 of them.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If nothing is free this week, say so in one line and give the next free date.

## Never
- Never sign in, claim a ticket, or reserve a timed slot.
- Never invent a free day, an hour, a price or a residency rule.
- Never present a special exhibition as covered when general admission is what is free.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
