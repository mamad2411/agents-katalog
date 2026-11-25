---
name: daily-priority-planner
description: "Turn task dumps into a realistic daily execution plan using priority frameworks and time blocks. USE WHEN a task matches the Craft workspace workflow for daily-priority-planner."
cluster: ai-agents-meta
version: 1.0.0
origin: "craft-agent workspace"
---

# Daily Priority Planner

Use this skill when the user needs help deciding what to do today and in what order.

## Trigger Conditions
- User has too many tasks and needs prioritization
- User asks for daily planning/time blocking
- User needs urgent-vs-important clarity

## Required Inputs
1. Full task list
2. Available time today
3. Hard deadlines and meetings
4. Energy constraints (optional)

## Workflow
1. **Task triage**: classify by impact, urgency, and effort.
2. **Prioritization**: apply Eisenhower-style sorting and sequencing.
3. **Time blocking**: assign realistic blocks with buffers.
4. **Focus strategy**: identify one critical outcome for the day.
5. **Review loop**: define end-of-day reflection and carry-forward list.

## Output Format
- Priority-ranked task list
- Time-blocked day schedule
- Top 1-3 must-win outcomes
- Deferral/delegation suggestions

## Guardrails
- Keep plan executable within available hours.
- Avoid overstuffed schedules.
- Build buffer time for interruptions.
