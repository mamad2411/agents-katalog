---
name: wild-soak
skill_id: browser-skill:wild-soak
description: A hot spring or swimming hole that is actually open, and safe today
when_to_use:
  - intent_keywords: [hot spring, swimming hole, soak, natural pool, river swim, waterfall, wild swim]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: natural hot springs and swimming holes with current access near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: river flow closures water quality advisories and trailhead parking for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: water
    current_value: California hot springs
    fill_rule: say your state or region
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [hot springs, swimming, water, outdoors, on demand]
    related_skills: [browser-skill:swim-and-sun]
platforms: [macos]
---
# Wild soak

## Purpose
You want warm water under open sky, or a cold pool at the bottom of a trail. Most
of the good ones are unsigned, half of the listings are out of date, and a few are
genuinely dangerous on the wrong day. This picks one that is open today and gets
you moving.

## Reads
- Search results for natural hot springs and swimming holes with current access near California hot springs.
- Search results for river flow closures water quality advisories and trailhead parking for California hot springs.

## Lands in
- Checks the river gauge before sending anyone to moving water. Short enough to act on straight away.

## Steps
1. Look up natural hot springs and swimming holes with current access near California hot springs.
2. Look up river flow closures water quality advisories and trailhead parking for California hot springs.
3. Checks the river gauge before sending anyone to moving water. USGS streamflow updates roughly every 15 minutes in cubic feet per second, and the trend across the last 48 hours matters more than the single reading, because rising water brings debris and changes the hydraulics. High spring runoff is also when riverside hot springs get flooded out and simply do not exist for the season.

## Success criteria
- Checks the river gauge before sending anyone to moving water. USGS streamflow
  updates roughly every 15 minutes in cubic feet per second, and the trend across
  the last 48 hours matters more than the single reading, because rising water
  brings debris and changes the hydraulics. High spring runoff is also when
  riverside hot springs get flooded out and simply do not exist for the season.
- Says the one hot spring rule almost nobody knows: do not put your head under.
  Naegleria fowleri lives in warm natural water and only infects through the nose,
  so soaking and even drinking are not the risk, dunking and diving are.
- Gets the season right. Undeveloped springs are best in late fall and winter, when
  the air is cold enough to make the water feel like the point and the crowds are
  gone. Midsummer is the worst combination of hot air, low water and full
  pullouts.
- Names the parking reality, because it is the usual failure: many trailheads need
  a day pass on the dash, five dollars a day or thirty a year for a Northwest
  Forest Pass or a Southern California Adventure Pass, and the pullout for a
  popular spring fills by mid morning on a weekend.
- Gives the first move plainly: the hour to arrive, the walk in from the car, and
  what to carry, which is water, shoes you can walk wet in, a headlamp for the
  hike out, and a bag to pack out everything including the glass someone else left.

## Failure behavior
- If a listing or gauge page will not load, skip it and keep going.
- If the spot is closed, flooded, under a health advisory or burned over, say so in
  one line and name the next one within reach.

## Never
- Never sign in, buy a pass, reserve a soak or book a resort.
- Never invent a flow reading, a closure, a water temperature or an access road.
- Never send someone to a spot that is closed, posted or under an advisory.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
