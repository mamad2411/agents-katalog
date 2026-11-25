---
name: whats-everyone-talking-about
skill_id: browser-skill:whats-everyone-talking-about
description: The storylines everyone is following, caught up like a friend told you
when_to_use:
  - intent_keywords: [discourse, drama, reality tv, celebrity, gossip, what happened, storyline, catch me up]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what actually happened this week in the storylines around
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how people are reacting and what the argument is really about in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: storylines
    current_value: pop culture and big creators
    fill_rule: name the shows, people and corners of the internet you follow
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [culture, reality tv, celebrity, internet, weekly]
    related_skills: []
platforms: [macos]
---
# The discourse

## Purpose
Monday morning, before anyone brings it up. What actually happened over the
weekend in the storylines the user follows, told the way a friend would tell it:
the plot, the receipts, and why people care.

## Reads
- Search results for what actually happened this week in the storylines around pop culture and big creators.
- Search results for how people are reacting and what the argument is really about in pop culture and big creators.

## Lands in
- Says what happened plainly, so it lands even if the user missed two episodes. Short enough to act on straight away.

## Steps
1. Look up what actually happened this week in the storylines around pop culture and big creators.
2. Look up how people are reacting and what the argument is really about in pop culture and big creators.
3. Says what happened plainly, so it lands even if the user missed two episodes.

## Success criteria
- Says what happened plainly, so it lands even if the user missed two episodes.
- Marks the difference between confirmed, denied and pure speculation.
- Gives the reaction, so the user knows the room before walking into it.
- Stops at three storylines, even on a loud week.

## Failure behavior
- If a source will not load, skip it and keep going.
- If the week was genuinely quiet, say so in one line and give the one thing
  still running.

## Never
- Never sign in, post, reply or share anything.
- Never invent a quote, a rumor, a source or a confirmation.
- Never carry a story about a private person, a minor, or someone's grief.

## Redaction
Omit query strings, account details, handles the user has not mentioned, home
address, and anything shown after a page unexpectedly asks for a login.
