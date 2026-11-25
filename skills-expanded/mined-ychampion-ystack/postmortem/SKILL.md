---
name: postmortem
description: >-
  Write a blameless incident postmortem from the raw material: logs, alerts, deploy history, commits
  and chat threads. Builds a timestamped timeline, separates the trigger from the root cause and the
  things that made it worse, measures impact, and turns lessons into owned, checkable actions. Use for
  "write a postmortem", "incident report", "what happened with the outage", "RCA", or after any
  production incident or near miss.
---

# Postmortem

The value of a postmortem is the actions that stop the next one. A good one is built from evidence,
names systems instead of people, and ends with a short list of fixes someone owns.

## Procedure

### 1. Gather the evidence

Collect, with timestamps: alerts and pages, logs and error rates around the window, deploys and
config changes (`git log --since --until`, the deploy tool's history), the chat or incident channel,
support tickets. Note the source of every fact. Normalize all times to one timezone, stated once.

### 2. Build the timeline

```
| Time (UTC) | Event | Source |
| 14:02 | deploy of v4.12 starts | deploy log |
| 14:09 | error rate on /checkout rises to 18% | dashboard |
| 14:21 | first alert fires | pager |
| 14:35 | rollback started | chat |
| 14:41 | error rate back to baseline | dashboard |
```

Mark four moments: started, detected, mitigated, resolved. The gaps between them are findings in
themselves (why did detection take 12 minutes?).

### 3. Separate the causes

- **Trigger:** the change or event that started it.
- **Root cause:** why the trigger could do damage. Keep asking why until the answer is a missing
  safeguard, check or design property, not a person's slip.
- **Contributing factors:** what made it bigger or longer: slow detection, missing runbook, noisy
  alerts, hard rollback.

If the evidence doesn't settle the root cause, say so and list what would.

### 4. Measure impact

Duration, users or requests affected, errors, data lost or corrupted, money, support load. Use
numbers from the evidence; label estimates as estimates.

### 5. Turn lessons into actions

Each action: concrete, checkable and owned, ranked by how much it would have reduced this incident.

```
| Action | Prevents / shortens | Owner | Due |
| Add a canary stage that halts on error rate > 2% | detection, blast | <owner> | <date> |
```

"Be more careful" is not an action. Three to six real actions beat fifteen vague ones.

## Output

```
# Incident: <title>   (<date>, severity <n>)
Summary: <three sentences: what broke, for whom, how long, how it was fixed>
Impact: <numbers>
Timeline: <table>
Trigger / Root cause / Contributing factors
What went well: <short>
Actions: <table>
Open questions: <what the evidence didn't settle>
```

## Rules

- Blameless: describe what people saw and did, and why it made sense at the time. Never name a person
  as the cause.
- Every timeline entry has a source.
- Strip secrets and personal data from quoted logs and chat.
- Draft only: owners and dates are the user's to confirm.
