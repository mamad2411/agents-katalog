---
name: structural-retrospective
description: Use when running retrospectives, post-incident reviews, postmortems, learning reviews, near-miss reviews, or turning incidents into follow-up work.
---

# Structural Retrospective

The lesson should live in the system after everyone forgets the meeting.

Core rule:

> Reproduce the cause, blame the system gap, encode the lesson as a guardrail, and feed owned work back into triage.

## Default output

```md
## Reconstructed failure
- Evidence:
- Reproduction:
- Timeline by artifacts:

## System gap
- What structure allowed it:
- Missing signal:
- Failure mode to remove:

## Structural follow-ups
- Test/assertion/alert/delete/runbook:
- Owner:
- Date:
- Triage-ready issue:
```

## Retrospective checks

- Reproduce or reconstruct the failure from logs, traces, metrics, and inputs before explaining it.
- Ask what the system let happen, not who did it. Blameless means system-causal, not ownerless.
- Find missing or silent signals: swallowed errors, absent alerts, misleading dashboards, slow burns.
- Convert the lesson into something that re-runs without the meeting: regression test, assertion, alert, lint rule, schema, runbook.
- Prefer deleting the failure mode to adding another guard.
- Give every follow-up one owner and one due date, or explicitly drop it.
- Feed outputs back as triage-ready issues. The report explains the work; it is not the work.

## Red flags

- Confident memory outranking reproducible evidence.
- “Human error” as root cause.
- “We should be careful” as action item.
- Alert added without owner, action, or false-positive control.
- Retro ends with prose and no tracked issues.
