---
name: time-management
description: Design calendars, schedules, and time allocations that match the user's energy, priorities, and constraints.
category: productivity
aliases:
- schedule
- calendar
- time-block
- timebox
- weekly-planning
triggers:
- help me schedule
- time management
- weekly schedule
- calendar planning
- when should I do this
keywords:
- schedule
- time
- calendar
- block
- plan
- weekly
- day
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- block
- calendar
- management
- productivity
- schedule
- time
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

# Time Management

## Purpose

Translate priorities into a concrete schedule that respects the user's energy, constraints,
and calendar reality.

## When to Use

- User wants help structuring their day or week
- User has too much to fit in available time
- User is unsure when to do focused work vs. meetings vs. recovery

## When NOT to Use

- The user doesn't yet know what they want to do (route to `prioritization` or `planning`)
- The user needs to do ONE thing now (route to `focus`)

## Capabilities

- Time blocking
- Energy-based scheduling (deep work in peak hours)
- Meeting audits
- Recovery and break planning

## Inputs

- Available time
- Energy patterns (when is the user sharpest?)
- Fixed commitments
- Top priorities

## Workflow

1. **Inventory fixed commitments.** Meetings, appointments, hard deadlines.
2. **Identify peak energy windows.** When does the user do their best focused work?
3. **Place deep work first.** Schedule the most important task in the best window.
4. **Batch similar work.** Email, admin, calls in batches, not scattered.
5. **Plan recovery.** Breaks are not optional. End-of-day wind-down.
6. **Leave slack.** ~20% unscheduled for the unexpected.

## Tools

- Calendar (digital or paper)
- Optional: time-tracking app

## Examples

**User:** "I have 8 hours of meetings and a 6-hour project. Help."
**Response:** "That's 14 hours in an 8-hour day. We either cut meetings, cut project scope, or defer the project. Let's see which is on the table."

## Safety

- Don't recommend unrealistic schedules
- Don't optimize for overwork

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `planning` (overall plan first)
- `prioritization` (what makes the schedule)
- `focus` (the actual sessions)