---
name: planning
description: Turn a vague goal, idea, or situation into a clear, scoped plan with objectives, scope, and first moves.
category: productivity
aliases:
- plan
- strategic-planning
- goal-planning
- daily-planning
triggers:
- help me plan
- I want to plan
- let's plan this
- daily plan
- weekly plan
- I need a plan
- goal planning
keywords:
- plan
- planning
- goal
- objective
- scope
- schedule
- strategy
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- goal
- objective
- plan
- planning
- productivity
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

# Planning

## Purpose

Move from "I have a vague goal / situation / idea" to a clear, scoped, time-bounded plan with
defined outcomes and a path to them.

## When to Use

- User wants to plan a project, week, day, or goal
- User has an unclear goal that needs scoping
- User is overwhelmed and needs structure

## When NOT to Use

- The user already has a clear plan and just needs to execute (route to `focus` or `task-decomposition`)
- The user is procrastinating on a known task (route to `unlazy`)

## Capabilities

- Clarify objectives and success criteria
- Scope what's in and out
- Identify constraints and resources
- Produce milestones with dates
- Surface risks and assumptions

## Inputs

- The goal, project, or situation
- Time horizon (day / week / quarter / year)
- Constraints (time, money, energy)
- Stakeholders (if any)

## Workflow

1. **Clarify the goal.** What specifically do you want, by when, and how will you know?
2. **Scope it.** What's in scope? What's explicitly out?
3. **Constraints.** What limits your options (time, money, energy, other people)?
4. **Milestones.** 3–7 waypoints between now and done. Each with a rough date.
5. **First concrete step.** The very next thing the user will do.
6. **Risks / unknowns.** What could derail this? What would you learn first?

## Tools

- Plain text / paper
- Calendar
- Optional: planning templates

## Examples

**User:** "Help me plan my week."
**Response:** "Let's start with: what's the ONE thing that, if done this week, would make the week a success? Then we schedule that first and fill around it."

## Safety

- Don't optimize for "perfect plan" — plans are hypotheses
- Encourage revisiting the plan weekly

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `task-decomposition` (after planning)
- `prioritization` (when too many things compete for the plan)