---
name: campsite-drop-watch
skill_id: browser-skill:campsite-drop-watch
description: The campsite you thought was sold out, and the exact morning it drops
when_to_use:
  - intent_keywords: [campsite, reservation, recreation.gov, sold out, booking window, cancellation, campground]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: recreation.gov booking window and release time for campground
    capability_target: web_search
    mutation_boundary: read_only
  - caption: campsite cancellations and last minute availability at sold out campgrounds
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 4
  time: 06:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: campground
    current_value: recreation.gov campground booking window
    fill_rule: name the campground or park you keep failing to get into
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [camping, reservations, campsite, timing, weekly]
    related_skills: []
platforms: [macos]
---
# Campsite drop watch

## Purpose
Wednesday, half an hour before the drop. Sold out is a lie about timing, not
about space. This gets you the exact morning and the exact minute the site you
want goes live, and the two windows where other people hand theirs back.

## Reads
- Search results for recreation.gov booking window and release time for campground recreation.gov campground booking window.
- Search results for campsite cancellations and last minute availability at sold out campgrounds recreation.gov campground booking window.

## Lands in
- Says the release is a rolling window, not a single opening day. Short enough to act on straight away.

## Steps
1. Look up recreation.gov booking window and release time for campground recreation.gov campground booking window.
2. Look up campsite cancellations and last minute availability at sold out campgrounds recreation.gov campground booking window.
3. Says the release is a rolling window, not a single opening day. Most Recreation.gov sites go live exactly six months out at 7am Pacific, which is 8am Mountain and 10am Eastern, and only the one night six months ahead drops that morning. ReserveCalifornia runs the same daily rolling six months at 8am Pacific. The campground's own Seasons and Fees tab is the only page to trust, because Yosemite Valley breaks the pattern and releases a month at a time on the 15th, five months ahead.

## Success criteria
- Says the release is a rolling window, not a single opening day. Most
  Recreation.gov sites go live exactly six months out at 7am Pacific, which is
  8am Mountain and 10am Eastern, and only the one night six months ahead drops
  that morning. ReserveCalifornia runs the same daily rolling six months at 8am
  Pacific. The campground's own Seasons and Fees tab is the only page to trust,
  because Yosemite Valley breaks the pattern and releases a month at a time on
  the 15th, five months ahead.
- Names both cancellation waves, because they are the real way in. The first is
  10 to 14 days out, when the full refund minus a $10 fee deadline expires and
  people who booked speculatively finally let go. The second is inside 48 hours,
  when a cancellation earns nothing back and the site just reappears. Flexible
  people get in during that second wave almost every time.
- Names the one thing to do before the drop: be logged in, have the dates and
  site number picked, and be refreshing at 6:59, because desirable sites go in
  under a minute and the cart holds a site only briefly.

## Failure behavior
- If an availability page will not load, skip it and keep going.
- If the campground is genuinely gone for the season, say so in one line and name
  the nearest first come first served or walk up option instead.

## Never
- Never sign in, hold a cart, book a site or pay a fee.
- Never invent a release time, a booking window, an opening or a refund rule.
- Never pass a paid alert service off as an official reservation source.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
