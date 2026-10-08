---
name: agent-ops-handoff
description: "Move an agent from laptop demo to operated system, tracing, cost dashboard, scheduled runs, alerting, and rollback. Use when an agent is about to run unattended or serve real users."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [agents, ops, observability, cron, ship]
    related_skills: [agent-loop-safety, cloud-deploy-gate, error-analysis-50]
    program_weeks: [17]
---

# Agent Ops Handoff

## 1 · Purpose

Close the gap between "the agent works on my machine" and "the agent runs
unattended and someone owns it", tracing, cost control, scheduling, alerting, and a
way back.

## 2 · When to use

- Moving any agent from interactive use to scheduled, event-driven, or
  user-facing operation (including personal assistants like OpenClaw on a VPS).
- When an unattended agent has surprised its owner, the post-incident checklist.

## 3 · Inputs

- The agent with loop safety in place (`agent-loop-safety`).
- The run schedule or trigger (cron, webhook, message gateway).
- An owner: a named human who gets the alerts.

## 4 · Procedure

1. **Centralize traces.** Write per-run traces (thoughts, tool calls, costs) to a
   durable store, not scrollback. Queryable by run ID, date, and status.
2. **Stand up the cost dashboard.** Per-run dollars and tokens, daily rollups, and
   the budget line. Cost per successful task is the metric; raw spend is the alarm.
3. **Schedule deliberately.** Cron or the platform scheduler with three rules:
   off-peak minutes (not :00/:30), an explicit timezone, and a catch-up policy for
   missed runs written down (skip, do not stampede).
4. **Alert on the four signals.** Run failure, cost-cap trip, guardrail refusal,
   and silence (a scheduled run that never reported). Route to the owner, not a
   channel nobody reads.
5. **Gate the outputs.** Unattended writes to shared systems (email, tickets,
   production tables) stay human-approved until 30 clean runs. Count them.
6. **Write the rollback.** How to disable the schedule, revoke the credentials,
   and restore the prior version, as commands, tested once.
7. **Define the weekly review.** 30 minutes: read 5 traces (2 failures, 3 random),
   review cost per task, check guardrail counts. This is the external feedback loop
   made operational.
8. **Hand over.** The owner acknowledges the dashboard, the alerts, and the
   rollback, in writing (an issue comment is fine).

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "It's just a personal assistant." | Personal assistants have your credentials and your contacts. Ops lite is still ops. |
| "I'll add monitoring after launch." | The first silent failure is when you needed it. That is always day one. |
| "Cron at 9:00 sharp is fine." | Thousands of jobs think that. Pick 9:17, name the timezone, survive the DST change. |
| "Rollback is just ctrl-C." | A running schedule with live credentials is not stopped by a closed laptop. |

## 6 · Red flags

- No record of what the agent did yesterday.
- Cost is discovered from the invoice.
- The schedule's timezone is "the server's".
- Nobody can name the owner.

## 7 · Verify

- Traces queryable; dashboard shows cost per successful task.
- Schedule documented: cron expression, timezone, catch-up policy.
- Four alert signals tested end-to-end (fire each once).
- Rollback commands written and tested once.
- Named owner acknowledged in writing.

## 8 · ZoroLogistics example

Week 17: OpenClaw runs as the lab assistant on a small VPS, wired to the Week-16
MCP server, with a local Hermes-class brain for cheap lanes. Cron jobs at :13 and
:47 past the hour, America/New_York. Traces land in SQLite with a query CLI; the
cost dashboard separates "local brain $0" from frontier fallbacks; Telegram gets
the four alerts. After 30 clean days, the refund tool graduates from approval-gated
to auto-under-$50, a policy change, recorded, with the trace count behind it.

---
© 2026 Zorost Intelligence LLC · zorost.com
