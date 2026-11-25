---
name: delegation-protocol
description: Cross-team delegation rules for Paperclip agents — when to delegate vs. do it yourself, how to write a delegable ticket (context, definition of done, deadline, budget), acceptance criteria for delivered work, and the retry → reassign → escalate-to-human ladder. Use when creating or assigning a ticket, deciding "should I delegate this", reviewing a delivered ticket, or handling a ticket that failed or stalled. Don't use for cEO-level portfolio planning (use ceo-operating-doctrine) or budget math (use budget-guardrails — this skill only requires that you did it).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Paperclip Workforce, Protocol, Delegation, Tickets, Escalation]
    related_skills: [ceo-operating-doctrine, budget-guardrails, researcher-persona, writer-persona, heartbeat-standup]
---

# Delegation Protocol

The shared rulebook for handing work between agents in a Paperclip org. A delegation is a contract: the ticket carries everything the assignee needs, the definition of done says exactly what "accepted" means, and failure follows a ladder instead of a shrug. The standard: any competent agent could pick up your ticket cold and succeed.

## When to Use

- You're about to create or assign a ticket to another agent.
- You're deciding whether to do a task yourself or hand it off.
- A delegated ticket came back and you must accept or reject it.
- A delegated ticket failed, stalled, or blew its deadline.
- **Not for:** CEO-level portfolio planning (use `ceo-operating-doctrine`) or budget math (use `budget-guardrails` — this skill only requires that you did it).

## Role Boundary

- **Any agent may:** delegate downstream or sideways when a role fits better, accept/reject work on tickets they opened, run the ladder's retry and reassign rungs.
- **Escalate to a human:** the ladder's final rung — after one retry and one reassignment both fail — plus any delegation that would spend past a cap or trigger an irreversible action.
- **Never:** delegate work you can't specify a definition of done for, assign without a budget estimate, or skip ladder rungs because you're annoyed.

## Quick Reference

| Question | Rule |
|---|---|
| Delegate or do? | Delegate if another role fits the deliverable better OR it takes you >15 min outside your role. Do it if it's your role and sub-day. |
| Ticket must contain | Context, Definition of Done, Deadline, Budget estimate, Goal ancestry (the "CDDBA" check) |
| Deadline | Concrete date/time, with slack for one revision round |
| Budget | Estimated cost on the ticket; assignee confirms it fits their remaining budget |
| Accept work | Every DoD line met → accept. Any miss → reject once, with specifics |
| Failure ladder | Retry (same agent, better ticket) → Reassign (different agent) → Escalate (human) |

## Procedure

1. **Decide delegate vs. do** — apply the Quick Reference rule. If you delegate to dodge accountability or do it yourself to hoard control, you chose wrong. Log the choice in one line on the ticket.
2. **Write the ticket (CDDBA)** —
   - **Context:** why this exists — name the mission → goal → project chain and link source material. No assignee should need to ask "what's this for?"
   - **Definition of Done:** 2–5 checkable statements ("posted to the ticket", "≤600 words", "2 sources per claim"). If you can't check it, it's not done-able.
   - **Deadline:** explicit, with room for one revision.
   - **Budget:** estimated cost; note the cap it draws from.
   - Success: the CDDBA check passes — all five present.
3. **Assign and confirm** — assign to the role that owns the deliverable. Assignee's first move: confirm intake (per their persona skill) or bounce with what's missing within one wake cycle. Silence past one cycle counts as a stall (step 5).
4. **Accept or reject delivery** — check the deliverable against the DoD line by line. All met: accept, close, thank. Any miss: reject **once** with a comment quoting the exact DoD lines missed and what closing the gap looks like. A rejection re-run counts as the ladder's retry rung.
5. **Run the failure ladder, in order** —
   - **Rung 1 — Retry:** same agent, one more attempt. First improve the ticket — most failures are ticket failures. One retry max.
   - **Rung 2 — Reassign:** different agent (or same role, different instance). Carry over the failed attempt as context so they don't repeat it. One reassignment max.
   - **Rung 3 — Escalate to human:** post the escalation template below. Then stop work on that thread — no rung 4, no heroics.
6. **Log the outcome** — accepted, or which rung resolved it. This is how the org learns which tickets and agents work.

## Output Template

```
## Escalation — {ticket-id}: {title}
Chain: {mission} → {goal} → {project}
Attempts: retry by {agent} ({result}); reassigned to {agent} ({result})
Budget spent on this ticket so far: {amount} of {estimate}

**What's blocked:** {one sentence}
**Why agents couldn't resolve it:** {one sentence}
**Recommendation:** {the option you'd pick}
**Decision needed by:** {date} — after that: {consequence of no decision}
```

## Pitfalls

- **The vibes ticket** ("make this better, thanks") — assignee guesses, delivery disappoints, everyone blames each other. Recovery: rejection isn't allowed against an unwritten standard; write the DoD you should have written, then re-run as the retry rung.
- **Skipping rungs** — straight from one failure to pinging the human, or looping five retries with the same agent and same ticket. Recovery: check the ladder position on the ticket log; you get exactly one retry and one reassign before escalation, no more, no fewer.
- **Delegation without budget** — the assignee burns spend the org didn't allocate. Recovery: if a ticket is discovered in-flight without an estimate, pause it, add the estimate, and have the assignee confirm fit per `budget-guardrails` before resuming.
- **Rejecting by redoing** — you fix the deliverable yourself and close the ticket. The assignee never learns and you just paid twice. Recovery: revert to their version, post the line-by-line DoD gaps, and let the ladder work.

## Verification

- [ ] Ticket passes CDDBA: Context, Definition of Done, Deadline, Budget, goal Ancestry all present
- [ ] Every DoD line is checkable by a third party
- [ ] Assignee confirmed intake and budget fit within one wake cycle
- [ ] Acceptance/rejection decided strictly against the DoD, in ticket comments
- [ ] Any failure followed the ladder in order: one retry, one reassign, then human escalation with the template
- [ ] No spend beyond the ticket's estimate without a logged approval
