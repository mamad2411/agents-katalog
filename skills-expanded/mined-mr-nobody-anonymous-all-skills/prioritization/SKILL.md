---
name: prioritization
description: Help the user decide what to do first, what to defer, and what to drop when everything feels important.
category: productivity
aliases:
- prioritize
- triage
- eisenhower
- what-should-i-do-first
triggers:
- what should I do first
- prioritize this
- I have too many things
- what's most important
- triage
- help me decide what to do
keywords:
- priority
- prioritize
- important
- urgent
- decide
- first
- drop
- defer
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- important
- prioritization
- prioritize
- priority
- productivity
- urgent
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Prioritization

## Purpose

Help the user make a defensible decision about what to work on, what to defer, and what to
drop — when there is more to do than time to do it.

## When to Use

- User has many competing tasks and can't pick
- User is overwhelmed by their task list
- User asks "what should I do first?"

## When NOT to Use

- There is actually only one task (route to `focus` or `unlazy`)
- The user is avoiding a known important task (route to `unlazy`)

## Capabilities

- Apply prioritization frameworks: Eisenhower, ICE, MoSCoW, ABC
- Surface "should this even be on the list?"
- Force a single #1, single #2, etc.
- Suggest deferring or dropping with rationale

## Inputs

- The list of candidate tasks (or a description of what's competing)
- User's context (deadline, energy, role)

## Workflow

1. **Inventory.** Capture all candidates briefly. If many, ask for top 5–7.
2. **Apply a frame.** Default to Eisenhower: Important × Urgent. Offer ICE for product work.
3. **Force a ranking.** No ties. Each item gets a position.
4. **Identify drops / defers.** Be explicit about what is NOT being worked on.
5. **Pick the #1.** Single verb phrase, single target time.

## Tools

- Paper / plain text
- Optional: spreadsheet for larger lists

## Examples

**User:** "I have 12 things to do and no idea where to start."
**Response:** "Let's narrow to the 5 that actually matter this week. Of those, which one has a hard external deadline? That's #1."

## Safety

- Don't impose false urgency
- Validate the user's choice if it's reasonable

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `task-decomposition` (after picking what to do)
- `planning` (for longer-horizon prioritization)