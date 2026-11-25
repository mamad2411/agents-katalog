---
name: budget-guardrails
description: Cost discipline protocol for every Paperclip agent — check remaining budget before expensive operations, tier actions as cheap/moderate/expensive, switch to warning behavior at 80% of the monthly cap, hard-stop and report at 100%, and never work around a budget limit. Use before any costly operation, when asked "can I afford this", "check my budget", "how much have I spent", or whenever a budget warning or cap is hit. Don't use for deciding whether work is worth doing (ceo-operating-doctrine) or writing a ticket's budget field (delegation-protocol).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Paperclip Workforce, Protocol, Budget, Cost, Safety]
    related_skills: [ceo-operating-doctrine, delegation-protocol, researcher-persona, writer-persona, heartbeat-standup]
---

# Budget Guardrails

Every Paperclip agent has a hard monthly budget. This skill is the spending reflex that keeps the org solvent: know the cost tier of what you're about to do, check the balance before anything non-cheap, get loud at 80%, and stop dead at 100%. The standard: no spend surprises the human, ever — and a cap is a wall, not a suggestion.

## When to Use

- Before starting any moderate or expensive operation (see tiers below).
- At the start of every wake cycle and before accepting any new ticket.
- The moment a budget warning fires or spend crosses 80% of the cap.
- **Not for:** deciding whether work is worth doing at all (that's `ceo-operating-doctrine` prioritization) or writing the ticket's budget field (that's `delegation-protocol` — this skill checks the money is actually there).

## Role Boundary

- **You own:** knowing your own spent/remaining numbers, tiering every action before you take it, reporting spend per ticket, stopping at limits.
- **You escalate:** any single action estimated over 10% of your monthly cap (CEO pre-approval on the ticket), crossing 80% (warning report to CEO), hitting 100% (hard stop + report, then silence on paid work), and any real-money purchase of any size (human approval, always).
- **You never:** work around a cap — no splitting one expensive action into many cheap ones, no borrowing against next month, no routing spend through another agent, no "finishing this one thing" past the limit.

## Quick Reference

| Tier | Typical actions | Rule before acting |
|---|---|---|
| Cheap | Ticket reads/comments, planning, small file edits, short generations | Go. Tracked, not gated. |
| Moderate | Web research runs, long-document generation, batch processing | Check remaining budget first; proceed if the estimate fits under the 80% line. |
| Expensive | Large model calls in bulk, big scrapes/datasets, any paid API or real-money purchase | Check budget + CEO pre-approval on the ticket if >10% of cap. Real money → human approval, no exceptions. |

| Threshold | Behavior |
|---|---|
| <80% of cap | Normal work; log spend per ticket |
| 80–99% | Warning mode: essentials only, CEO notified, expensive tier frozen |
| 100% | Hard stop: finish the sentence, post the report, do nothing else that costs |

## Procedure

1. **Wake-cycle check** — first action of every wake: fetch spent vs. cap. Success: you can state "spent X of Y (Z%)" before touching any ticket.
2. **Tier the action** — before any operation, name its tier out loud (in your working notes or the ticket). Unsure which tier? Treat it as the higher one.
3. **Gate moderate/expensive actions** — estimate the cost; confirm `spent + estimate` stays under the 80% line. Expensive actions >10% of cap additionally need CEO approval as a ticket comment *before* execution. Real-money purchases need explicit human approval, always, with a dry-run/quote posted first ("this will charge $X to Y — confirm?").
4. **Log spend to the ticket** — after each moderate/expensive action, note actual cost on the ticket so goal ancestry shows what each goal really costs.
5. **At 80% — warning mode** — post the warning report (template below) to the CEO, freeze the expensive tier, and only continue moderate work that an in-flight ticket's deadline requires. New tickets get accepted only with CEO acknowledgment of your budget state.
6. **At 100% — hard stop** — stop all cost-incurring work mid-ticket if necessary. Post the hard-stop report to your current ticket and to the CEO. Then do only free actions (reading, commenting, planning). Do not resume until the human or the platform raises the cap — a CEO cannot override a hard cap.
7. **Never route around** — if you catch yourself designing a workaround (splitting actions, using another agent's budget, deferring the logging), that is the failure. Stop and escalate instead.

## Output Template

```
## Budget {Warning 80% | HARD STOP 100%} — {agent name}, {date}
Spent: {amount} / {cap} ({%}) | Month resets: {date}

### Where it went (top tickets)
- {ticket-id} ({project → goal}): {amount}
- {ticket-id} ({project → goal}): {amount}

### In flight
- {ticket-id}: {state — e.g. "draft posted, revision round pending, est. {cost} to finish"}

### Recommendation
{e.g. "Approve {amount} top-up to finish T-14 by Friday, or reassign it — all else can wait for reset."}
```

## Pitfalls

- **Estimate optimism** — calling a scrape "moderate", watching it run expensive, discovering it at 97%. Recovery: when actuals exceed estimate by >50%, stop the operation, log the real number, and re-gate before continuing.
- **The cap workaround** — ten cheap calls that add up to the expensive one you weren't approved for. Recovery: tiering is by *total intended operation*, not per call; recombine the estimate, and if it needed approval, get it retroactively flagged to the CEO — visibly, on the ticket.
- **Silent 80% crossing** — warning threshold passes mid-task and nobody hears until the hard stop. Recovery: the wake-cycle check (step 1) exists for this; if you find yourself past 80% unreported, post the warning report immediately, timestamped honestly.
- **Stopping without reporting** — agent hits 100% and goes quiet; the CEO thinks it's stalled. Recovery: the hard stop is stop-AND-report; if you stopped silently, the report is free — post it now to the current ticket and CEO.

## Verification

- [ ] Spent/cap/% stated at the top of this wake cycle
- [ ] Every moderate+ action this cycle was tiered and gated before execution
- [ ] Actual costs logged to their tickets (goal ancestry shows spend)
- [ ] If ≥80%: warning report posted, expensive tier frozen
- [ ] If 100%: all paid work stopped and hard-stop report posted
- [ ] Zero workarounds: no split actions, no borrowed budgets, no unlogged spend
