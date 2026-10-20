---
name: work-on-my-side-project
skill_id: browser-skill:work-on-my-side-project
description: One concrete step this week on the thing you are building on the side
when_to_use:
  - intent_keywords: [side project, side quest, building, my project, ship it, launch]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what people ship first when starting a side project
    capability_target: web_search
    mutation_boundary: read_only
  - caption: where to find the first users for a small project
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: your_project
    current_value: launching a small side project
    fill_rule: say what you are building and Luke picks the next step
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [side project, weekly, building, momentum]
    related_skills: [browser-skill:what-should-i-learn]
platforms: [macos]
---

# Side quest

## Purpose
Saturday morning, one step on the thing you actually want to build. Not a
roadmap, not a strategy. One step that leaves it further along than yesterday.

## Reads
- Search results for what people ship first when starting a side project launching a small side project.
- Search results for where to find the first users for a small project launching a small side project.

## Lands in
- One step, finishable this weekend, with a visible result at the end. Short enough to act on straight away.

## Steps
1. Look up what people ship first when starting a side project launching a small side project.
2. Look up where to find the first users for a small project launching a small side project.
3. One step, finishable this weekend, with a visible result at the end.

## Success criteria
- One step, finishable this weekend, with a visible result at the end.
- Says what it unlocks, so the step feels worth taking.
- Skips anything that needs money, a team, or permission.

## Failure behavior
- If a source will not load, skip it and keep going.
- If the project has not been described yet, ask once in one line.

## Never
- Never bring up weeks where nothing happened.
- Never compare the project to someone else's launch.
- Never sign in, post, publish, or contact anyone on the user's behalf.

## Redaction
Omit query strings, account details, unpublished project names the user has
not shared, and anything shown after a page unexpectedly asks for a login.
