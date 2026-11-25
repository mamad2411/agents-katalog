---
name: fin-close-management
version: 1.0.0
description: Run a sequenced period-end close with dependencies, single-owner tasks, a critical path, and live status to shorten days-to-close.
author: matrixx0070
tags: [finance, close, month-end, accounting, checklist, critical-path]
---

# Close Management

## When to use
Use this to plan or run a period-end close (month, quarter, year), unblock a stalled close, or build a repeatable close calendar that shortens days-to-close.

**Not for:** preparing the statements the close produces (fin-financial-statements), individual account reconciliations (fin-reconciliation), or drafting the entries booked during close (fin-journal-entry). This orchestrates *when and by whom*, not the accounting itself.

## Method
1. **Define period and target.** State the close period, day-1 date, and the committed deadline (e.g., business day 5, "BD5").
2. **Inventory tasks by workstream.** Group into subledger cutoff (AR, AP, payroll), accruals/deferrals, reconciliations, intercompany, fixed assets, revenue, then consolidation and reporting.
3. **Map dependencies.** Order so upstream feeds finish first: subledgers → reconciliations → variance review → reporting. Decision point: if two tasks share no dependency, run them in parallel to compress the calendar.
4. **Assign owner and due day.** Every task gets one owner and a target business day. Flag the critical path — the longest dependency chain that sets the earliest possible close.
5. **Track status live.** Mark each task not started / in progress / blocked / complete with a timestamp. Decision point: the moment a task is blocked, surface the owner and the blocking dependency — do not wait for standup.
6. **Gate the close.** Do not advance to reporting until all reconciliations are signed off and material variances are explained.
7. **Capture retro items.** Note what ran late and the concrete fix for next cycle.

## Example
March close, day-1 = Apr 1, target BD5 = Apr 7. AP cutoff (owner: J, BD1) and payroll accrual (owner: M, BD1) run in parallel. Bank rec (owner: J, BD3) depends on AP cutoff — critical path. At BD3, bank rec is *blocked*: a $40k deposit-in-transit is unposted, dependency = treasury feed. You escalate same-hour; treasury posts BD3 PM; rec clears BD4; reporting starts BD4 on schedule. Retro: automate the treasury feed to remove the recurring BD3 stall.

## Pitfalls
- **No single owner.** "The team" owns nothing; blocked tasks sit until someone notices.
- **Ignoring the critical path.** Racing non-blocking tasks feels productive but the close is only as fast as its longest chain.
- **Opening reporting before reconciliations sign off.** You will re-issue the package when a rec turns up a difference.
- **Skipping the retro.** The same task slips every month until you record and fix the cause.

## Output format
```
Period: <...> | Day-1: <date> | Deadline: BD<n>
Progress: <complete>/<total> tasks | verdict: on-track / at-risk | days left: <n>
Task register:
  | ID | task | workstream | owner | due BD | status | dependency |
Critical path: <task → task → task>
Blockers: | task | owner | cause | needed action |
Sign-off gate: reconciliations <n/n> | material variances explained: y/n
Retro: <what slipped → fix>
```

## Reference

### Standard close timeline (business days, "BD")
A tight monthly close lands BD5; a stretched one runs BD8–10. Map every task to a business day and to its upstream dependency.

| BD | Workstream | Key tasks |
|---|---|---|
| BD0 (last day) | Cutoff | Freeze sales, receiving, and time entry; communicate cutoff to all subledger owners |
| BD1 | Subledgers | Close AR billing, AP invoice entry, payroll; capture cutoff accruals |
| BD1–2 | Accruals/deferrals | Book recurring accruals, prepaid amortization, deferred-revenue release, depreciation |
| BD2 | Inventory / COGS | Post inventory movements, standard-cost variances, reserves |
| BD2–3 | Intercompany | Match and eliminate IC balances; resolve mismatches before consolidation |
| BD3 | Reconciliations | Cash, key balance-sheet accounts; roll-forwards |
| BD3–4 | FX / consolidation | Revalue monetary balances, translate subsidiaries, consolidate |
| BD4 | Flux / variance | P&L and BS flux review vs prior/budget; investigate outliers |
| BD4–5 | Reporting | Draft statements, tie-outs, management package, commentary |
| BD5 | Sign-off | Controller/CFO review and lock the period |

### Dependency chain (what feeds what)
`Subledger cutoff → accruals/deferrals → reconciliations → flux review → consolidation → reporting → sign-off.` Reporting can never start before reconciliations sign off; consolidation can never start before intercompany matches. Tasks that share no dependency (e.g., AP cutoff and payroll accrual) run in parallel — that parallelism is what compresses the calendar.

### Critical path
The critical path is the longest chain of dependent tasks; it sets the earliest possible close date. Shortening any non-critical task does nothing; only shortening or parallelizing critical-path tasks moves the close in. Recompute the critical path whenever a task is added or a dependency changes.

### Close metrics to track
- **Days-to-close:** business days from period-end to sign-off. Benchmarks: top-quartile ≈ 3–5 BD, median ≈ 5–7 BD, laggards 8–10+.
- **On-time task %:** tasks completed by their target BD ÷ total.
- **Manual JE count / value:** high manual volume signals automation opportunity and error risk.
- **Post-close adjustments:** entries booked after "close"; trend toward zero.
- **Reconciliation completion rate at gate:** should be 100% before reporting opens.

### RACI and controls
Every task has exactly one **Responsible** owner and one **Accountable** approver (they must differ for anything requiring sign-off). Consulted/Informed parties are named so blockers escalate to a person, not "the team." Close checklists are themselves a SOX control area — completeness, timeliness, and evidence of review are testable.

### Accelerators
Continuous/soft close (book throughout the month, not just at period-end); pre-close subledger validation; automated recurring JEs and bank feeds; standardized reconciliation templates with auto-tie-outs; a "no-surprises" flux threshold agreed before close so review focuses only on material movements; a standing retro that converts each late task into a concrete process fix next cycle.
