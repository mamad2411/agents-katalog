---
name: personal-productivity
description: Use when helping a user organize personal work, tasks, priorities, schedule, habits, inbox, notes, goals, study plan, decision backlog, or weekly planning. Prefer this Skill when the task needs prioritization, next actions, time blocking, habit design, focus plan, or lightweight personal operating system. Do not use for medical advice, mental health treatment, or calendar/task app actions.
meta:
  version: 1
  display_name: 个人效率
---

# Personal Productivity

## Purpose

Help users turn messy work and life inputs into priorities, next actions, schedule blocks, routines, and review habits.

## Use When

Use for:

- task organization
- weekly planning
- prioritization
- time blocking
- inbox or notes cleanup
- habit planning
- study or learning plans
- personal goal breakdown

## Material Gate

Identify:

- goals, deadlines, obligations, energy constraints, available time, and current task list
- urgency, importance, dependency, and effort
- whether the user wants a plan, schedule, checklist, or reflection

If inputs are vague, create a lightweight triage before detailed scheduling.

## Workflow

1. Capture tasks and commitments.
2. Classify by urgency, importance, deadline, effort, and dependency.
3. Reduce overload by choosing must-do, should-do, delegate/defer, and drop candidates.
4. Convert priorities into next actions.
5. Place work into time blocks or routines if requested.
6. Add review checkpoints and fallback plans.
7. Use `html-report-builder` only for shareable planning dashboards or review reports.

## Checks

- Plan has concrete next actions.
- Time blocks respect constraints.
- Priorities are not all marked urgent.
- Habit plan is small enough to start.
- Health or mental health claims are avoided.

## Outputs

- prioritized task list
- weekly plan
- time-block schedule
- habit plan
- study plan
- notes cleanup structure
- personal review

## Boundary

This Skill owns personal organization, prioritization, planning, and habit structure. It does not own medical advice, therapy, financial planning, legal advice, calendar writes, reminder creation, or task app updates.

It must not run shell, Python, Node, npm, curl, MCP, calendar, task app, email, notification, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
