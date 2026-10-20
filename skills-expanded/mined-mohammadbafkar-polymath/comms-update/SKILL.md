---
name: comms-update
description: Draft an incident communication update — plain language, status (investigating/identified/monitoring/resolved), impact, next-update ETA.
---

# comms-update

> Draft one comms update (status page / customer email / internal stakeholder note). Output is the update, ready to post.

## When to use

- A sev1/sev2 needs an external update.
- Stakeholders need an internal update during a long incident.
- A workflow's comms step generates a draft (e.g. `respondToIncident` paired with `polymath-chat:post-incident-comms`).

## Procedure

1. **Status** — pick one from a fixed scale:
   - **investigating** — we know there's a problem; we don't know the cause.
   - **identified** — we know the cause; mitigation in progress.
   - **monitoring** — we believe we've mitigated; watching to confirm.
   - **resolved** — service is healthy; postmortem to follow.
2. **Audience** — externals (status page, customer email) get different language than internal stakeholders. Pick once.
3. **Plain language** — what users see and can/can't do. Not "ELB target group degraded".
4. **Workarounds** — if any, name them simply.
5. **Next-update ETA** — always specify. "Next update in 30 minutes" beats silence.
6. **What we know / don't know** — both sections present. Don't speculate.

## Output

```text
Update #3 — Refund processing degraded

Status: identified

What's happening:
  Customers attempting to issue a refund are seeing errors. New refunds
  are being queued internally and will process once we restore service.
  Existing orders, account access, and other operations are unaffected.

Impact:
  - All customers attempting refunds since 14:02 UTC.
  - Refunds queued during this window will process after recovery; no
    refunds will be lost.

What we're doing:
  Rolled back the recent refund-service deploy. Metrics improving; we
  are watching to confirm recovery.

What we know:
  A bad deploy of refund-service introduced a regression in the
  payment-provider integration. The rollback restores prior behavior.

What we don't know yet:
  Whether the queued refunds will all process within the next 15
  minutes (estimated based on queue depth).

Next update in 15 minutes, at 14:35 UTC.
```

## Quality bar

- One of the four fixed status values.
- Next-update ETA stated.
- "What we don't know yet" present and honest.
- No internal-jargon component names.
- No "due to a database issue" — that's the cause, not the impact.

## Anti-patterns to avoid

- "We are aware of an issue" without saying what's broken.
- Silence between updates.
- Speculation about root cause in the comms update.
- Promising a fix ETA you can't keep.
