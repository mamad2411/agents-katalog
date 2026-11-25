---
name: incident-response
description: Runs a production incident - mitigate first, coordinate, communicate - then a blameless postmortem with tracked actions. Triggers - production is down, users are reporting errors right now, outage, page fired, write the postmortem, rollback now, sev1.
---

# Incident Response

An incident is not a debugging session. The objective is **restoring service**,
which frequently means acting before you understand the cause. Engineers'
instinct — diagnose then fix — is correct in development and wrong here; it is
the main reason incidents last longer than they should.

## Priority order (never reorder)

1. **Stop the harm** — mitigate, even without understanding
2. **Communicate** — tell affected people what you know
3. **Preserve evidence** — capture before it rotates away
4. **Diagnose** — after service is restored
5. **Learn** — postmortem and follow-through

## Mitigate first

Fastest first, in this order:

| Move | When |
|---|---|
| Turn the flag off | The change is behind one — instant, no deploy |
| Roll back | A recent deploy correlates with the start |
| Fail over / restart | A specific instance or zone is unhealthy |
| Shed load / rate-limit | Overload, cascading failure |
| Degrade deliberately | Disable the expensive feature, serve stale data |
| Scale up | Resource exhaustion with headroom available |

A rollback that loses an hour's work is cheaper than an outage. Do not debug
the new code while it is burning; revert and diagnose in peace.

**Correlation with a recent change is enough to justify a rollback.** You are
not proving causation, you are restoring service.

## Roles

Even with three people, name them out loud:

- **Incident commander** — decides, does not debug. Their job is the timeline,
  the priorities and who is doing what.
- **Operations** — makes changes to the system. One person touches production;
  parallel uncoordinated fixes cause second incidents.
- **Communications** — updates status page, stakeholders, support.
- **Scribe** — timestamps every action and observation in the channel.

One channel. One document. Everything written down as it happens — memory
reconstructed afterwards is unreliable, and the timeline is the raw material
for the postmortem.

## Communication

Update on a fixed cadence (every 30 minutes) even with no news — silence is
read as chaos. Each update: what is affected, what users experience, what we
are doing, next update time. State impact in user terms, never "the queue
consumer is lagging". Do not promise a resolution time you do not have.

## Evidence

Before restarting anything: capture logs around the failure window, a thread
dump or heap snapshot if the process is in a bad state, current metrics
screenshots, the exact deployed versions, and recent changes (deploys, config,
flags, infrastructure, dependency incidents). Restarting destroys most of the
diagnostic state — and "restart and hope" makes the next occurrence just as
mysterious.

## Postmortem

Within a few days, while memory is fresh. Blameless is not politeness; it is
accuracy. A person who fears blame gives you an incomplete account, and you
learn the wrong lesson.

```markdown
# Incident YYYY-MM-DD: <user-visible summary>
Severity · Duration (detection → mitigation → resolution) · Impact (who, how many, what)

## Timeline
Timestamped facts only. What was observed, what was done. No interpretation.

## Root cause
The causal chain. Usually several contributing factors — a single cause is a
sign of an incomplete analysis.

## What went well
Detection, tooling, decisions that helped. Keep these deliberately.

## What made it worse
Missing telemetry, misleading alert, unclear ownership, absent runbook.

## Action items
| Action | Owner | Due | Priority |
Each one concrete and verifiable. "Be more careful" is not an action item.
```

**"Human error" is never a root cause.** It is a prompt: what allowed a normal
person, acting reasonably with the information available, to cause this? The
answer is a missing guardrail, a confusing interface or an absent check — and
that is the thing to fix.

Track the action items like any other work. Unimplemented postmortem actions
are the reason the same incident recurs, and recurrence destroys trust in the
process.

## Runbooks

Every alert has one, with: what it means, user impact, first three diagnostic
steps with the exact commands, mitigation options, and escalation. Written so
someone woken at 3am who did not build the system can act.

Update the runbook during the incident, while you are learning what it should
have said.

## Exit checklist

- [ ] Mitigation attempted before diagnosis
- [ ] Roles named; one person changing production
- [ ] Evidence captured before restarts
- [ ] Stakeholders updated on a cadence, in user terms
- [ ] Timeline recorded as events happened
- [ ] Postmortem written, blameless, with contributing factors
- [ ] Action items have owners and dates, tracked to completion
- [ ] Runbook and alerting updated with what was learned
