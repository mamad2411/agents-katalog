---
name: litig-matter-update
version: 1.0.0
description: Log a structured status update to an existing litigation matter, recording what happened, deadline changes, and next actions.
author: matrixx0070
tags: [litigation, docketing, status-update, deadlines, case-management]
capabilities: []
---

## When to use
Use this after any event that moves a matter: a filing, an order, a discovery exchange, a hearing, or a client instruction. Use it to keep the docket and next-action list current so nothing slips. Each update should stand alone and be readable by anyone picking up the file.

**Not for:** opening a new matter (see litig-matter-intake) or a full get-up-to-speed narrative (see litig-matter-briefing).

## Method
1. Identify the matter by name and number so the entry attaches correctly.
2. State what happened in one or two factual sentences, dated.
3. Update the docket: which deadlines moved, were satisfied, or newly triggered. **Decision point:** if a court order changes a deadline, recompute all downstream dates that cascade from it.
4. List concrete next actions with owners and due dates.
5. Note any client communication needed. **Decision point:** if the event requires a strategic decision or client authority, mark it BLOCKED-ON-DECISION rather than guessing.
6. ATTORNEY-ESCALATION gate: any update that includes advice, a strategy recommendation, or client-facing language must be routed to the supervising attorney before it is sent.

## Example
> The court grants a 21-day extension on the discovery cutoff. You log the order, recompute the expert-disclosure and dispositive-motion dates that key off the cutoff, add "serve amended scheduling order to client" as a next action, and route the client note for attorney review.

## Pitfalls
- **Orphaned cascades:** moving one date without recomputing dependent deadlines is the classic malpractice trap.
- **Vague next actions:** "follow up" without an owner and date is not an action.
- **Silent assumptions:** if you inferred a deadline, label it and confirm against the order text.
- **Lost client authority:** decisions that need client sign-off must be flagged, not assumed.

## Output format
```
MATTER: <name> | No: <matter#> | Date: <YYYY-MM-DD>
EVENT: <what happened>
DEADLINES CHANGED: <old -> new; cascades>
NEXT ACTIONS: <action — owner — due>
CLIENT COMMS: <needed? / BLOCKED-ON-DECISION>
STATUS: <active / awaiting attorney review>
```

## Reference
Scheduling in federal court is governed by FRCP 16, and deadline computation by FRCP 6(a): exclude the trigger day, count every day including weekends, and roll a due date that lands on a weekend or legal holiday to the next business day. Service adds time — FRCP 6(d) adds 3 days when service is by mail or certain electronic means. Discovery deadlines cascade: expert disclosures (FRCP 26(a)(2)) key off trial or cutoff dates, and dispositive-motion deadlines often follow the discovery close. State rules and standing orders vary; always verify computation against the governing order and local rules with the supervising attorney.
