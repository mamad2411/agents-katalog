---
name: dawn-patrol
skill_id: browser-skill:dawn-patrol
description: Whether it is worth getting up, and which beach to point the car at
when_to_use:
  - intent_keywords: [surf, dawn patrol, swell, waves, tide, surf report, paddle out, beach break]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: surf forecast swell period wind and tide for beaches near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: buoy readings water temperature and beach access conditions near
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 06:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: coast
    current_value: Malibu and Santa Monica
    fill_rule: say the breaks you surf
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [surf, ocean, morning, dawn patrol, weekly]
    related_skills: [browser-skill:swim-and-sun]
platforms: [macos]
---
# Dawn patrol

## Purpose
Saturday, quarter past five, still dark. The one honest answer about whether the
ocean is worth it this morning, which beach is working, and the hour you have to
be in the water before the day ruins it.

## Reads
- Search results for surf forecast swell period wind and tide for beaches near Malibu and Santa Monica.
- Search results for buoy readings water temperature and beach access conditions near Malibu and Santa Monica.

## Lands in
- Explains why the window closes, not just that it exists. Short enough to act on straight away.

## Steps
1. Look up surf forecast swell period wind and tide for beaches near Malibu and Santa Monica.
2. Look up buoy readings water temperature and beach access conditions near Malibu and Santa Monica.
3. Explains why the window closes, not just that it exists. Overnight the land cools faster than the ocean, so air drains seaward as a light offshore breeze and holds the wave faces up. Once the sun heats the land the flow reverses, onshore wind arrives, and the same beach turns to mush, often by mid morning. That single fact is the whole reason dawn patrol exists.

## Success criteria
- Explains why the window closes, not just that it exists. Overnight the land
  cools faster than the ocean, so air drains seaward as a light offshore breeze
  and holds the wave faces up. Once the sun heats the land the flow reverses,
  onshore wind arrives, and the same beach turns to mush, often by mid morning.
  That single fact is the whole reason dawn patrol exists.
- Reads swell period, not just wave height, because period is the energy. Long
  period swell arrives with power and organization, short period swell is
  windswell and closes out. A star rating alone tells you nothing, and two feet at
  long period beats four feet of chop.
- Names the tide window for that specific beach, since the same swell breaks well
  on a pushing tide at one spot and shuts down on a low at the next one over.
- Gives the first move without hedging: the hour to leave, which lot to use, and
  the wetsuit thickness for today's water temperature, so nobody stands in the
  parking lot deciding.
- Says plainly when it is not worth it, and names the beginner friendly beach that
  still works on a bad morning.

## Failure behavior
- If a forecast source will not load, skip it and fall back to the buoy reading.
- If the swell is flat or the wind is already onshore, say so in one line and give
  the next morning that looks better.

## Never
- Never sign in, buy a forecast subscription or book a lesson.
- Never invent a swell height, a period, a tide time or a water temperature.
- Never send a beginner to a heavy reef, a rip prone beach or a closed break.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
