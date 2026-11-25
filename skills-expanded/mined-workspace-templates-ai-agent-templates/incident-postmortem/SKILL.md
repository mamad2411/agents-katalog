---
name: incident-postmortem
description: Writes a blameless postmortem from logs, chat and commits, with a verified timeline, a real root cause and follow-up actions that have owners.
---

# Incident postmortem

Write for a reader who was not there. Be factual, blameless and specific.

## Steps

1. Gather evidence: alert history, deploy and commit log around the time (`git log --since --until`), error logs, graphs, chat transcript. Ask the user for what you cannot read.
2. Build the timeline in UTC, one line per event with its source: first symptom, detection, escalation, each mitigation attempt, resolution. Mark each entry as confirmed or inferred.
3. Measure impact: duration, share of requests or users affected, data lost or delayed, money or SLA consequences.
4. Find the cause with "why" chains until you reach a process or design gap, not a person. Separate the trigger (what started it) from contributing factors (why it was possible, why detection was late, why recovery took long).
5. Note what went well, where luck helped, and what slowed recovery.
6. Write actions that change the system: each has an owner role, a due date, a priority and a success check. Prefer prevention and faster detection over "be more careful".

## Rules

- Never name an individual as the cause. Write "the deploy" or "the on-call runbook", not people.
- Do not guess; mark unknowns as open questions.
- Keep it under two pages.

## Report

Summary, impact, timeline, root cause and contributing factors, what went well, action items table, and open questions.
