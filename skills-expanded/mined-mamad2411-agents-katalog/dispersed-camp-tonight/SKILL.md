---
name: dispersed-camp-tonight
skill_id: browser-skill:dispersed-camp-tonight
description: Free legal camping on public land tonight, no booking, no gate
when_to_use:
  - intent_keywords: [dispersed camping, free camping, blm, national forest, boondock, no reservation, car camp]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: dispersed camping areas on national forest and BLM land near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: motor vehicle use map rules fire restrictions and road conditions for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: area
    current_value: dispersed camping national forest in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [camping, free, public land, dispersed, on demand]
    related_skills: []
platforms: [macos]
---
# Dispersed camp tonight

## Purpose
Everything is booked and you still want to sleep outside tonight. Most of the
public land in this country takes no reservation, charges nothing and has no
gate. It just has rules, and the rules are the whole game.

## Reads
- Search results for dispersed camping areas on national forest and BLM land near dispersed camping national forest in Los Angeles.
- Search results for motor vehicle use map rules fire restrictions and road conditions for dispersed camping national forest in Los Angeles.

## Lands in
- Names the rules a first timer gets wrong. Short enough to act on straight away.

## Steps
1. Look up dispersed camping areas on national forest and BLM land near dispersed camping national forest in Los Angeles.
2. Look up motor vehicle use map rules fire restrictions and road conditions for dispersed camping national forest in Los Angeles.
3. Names the rules a first timer gets wrong. You get 14 nights in any 28 day period, and when your time is up you move, often 25 miles or more, not to the next pullout. Camp on already bare ground, at least 100 feet from water, and well away from developed campgrounds, picnic areas and trailheads.

## Success criteria
- Names the rules a first timer gets wrong. You get 14 nights in any 28 day
  period, and when your time is up you move, often 25 miles or more, not to the
  next pullout. Camp on already bare ground, at least 100 feet from water, and
  well away from developed campgrounds, picnic areas and trailheads.
- Says the Motor Vehicle Use Map is the legal document, not the camping app. The
  MVUM sets which numbered roads you may drive and how far off them you may pull,
  and that distance is set per forest, 150 feet on Gifford Pinchot and Siuslaw,
  300 feet on Black Hills and Willamette. Apps narrow the search, the MVUM
  decides whether you are legal.
- Gives one real first move: leave with at least two hours of daylight left. The
  spots are unsigned, forest roads get worse than the satellite view suggests,
  and picking a site in the dark is how people get stuck.
- Names what to bring that developed campgrounds hand you for free: all your own
  water, a way to pack out waste, and a shovel. There is no tap, no toilet and no
  trash can.
- Flags the fire rule for that unit, including whether a free campfire permit is
  required and whether stoves only are in effect right now.

## Failure behavior
- If a forest or BLM page will not load, skip it and keep going.
- If the area is closed for fire, snow or seasonal road closure, say so in one
  line and name the next unit over.

## Never
- Never sign in, buy a permit, reserve a site or pay a fee.
- Never invent a road number, a setback distance, a stay limit or a fire rule.
- Never send someone onto private land or a road the vehicle map does not open.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
