---
name: emplaw-log-leave
version: 1.0.0
description: Append a single new leave event or request into the leave tracker with dates, type, eligibility flag, and the required notices it triggers.
author: matrixx0070
tags: [leave, fmla, intake, record, hr]
capabilities: []
---

## When to use
Use this when one employee has requested or started a leave and you need to record that single event — capturing the dates, leave type, an eligibility determination, and the notices it sets in motion — as one row appended into the register that emplaw-leave-tracker manages. Use it every time a new request lands. **Not for:** building, auditing, or rolling the whole register forward (emplaw-leave-tracker owns the shared structure); new US state setup (emplaw-expansion-kickoff); updating an existing state footprint (emplaw-expansion-update); international hiring (emplaw-international-expansion); handbook edits (emplaw-handbook-updates); policy drafting (emplaw-policy-drafting); or the initial intake interview (emplaw-cold-start-interview).

## Method
1. Pull the employee's existing tracker row so this event appends to their history and shared balances.
2. Record leave type (FMLA, ADA accommodation, state PFL, pregnancy/PWFA, military caregiver) and start/end or intermittent pattern.
3. Decision point: if the employee meets 12 months + 1,250 hours and the site is FMLA-covered, flag FMLA-eligible and open the 12-week (or 26-week caregiver) counter; else mark ineligible and evaluate ADA or state programs instead.
4. Decision point: if the reason is a disability and FMLA is unavailable or exhausted, open the ADA interactive process (15+ employees); else proceed on the applicable statute.
5. Set the notice clocks this event triggers: eligibility/rights notice, 15-day certification request, and designation notice once certification returns.
6. Note stacking: identify whether this leave runs concurrently with or after any other entitlement already on the row.
7. Attorney-escalation gate: if the event involves denial, discipline, or termination adjacent to protected leave, engage licensed counsel in the jurisdiction before acting — not legal advice.

## Example
An Ohio employee with 14 months and 1,500 hours requests 8 weeks for their own serious health condition. You append a row: type FMLA, eligible Yes, 8 of 12 weeks used, certification requested (15-day clock started), designation notice pending. No state PFL in Ohio, so no stacking layer is added.

## Pitfalls
- **Overwriting instead of appending.** Each event is a new record on the shared row; replacing prior entries destroys the balance history.
- **Skipping the eligibility flag.** An unflagged row silently defaults balances wrong and hides ADA duties.
- **Starting the counter before certification.** Provisional designation must follow the certification window, not precede it.
- **Missing concurrent designation.** State or company leave that should run concurrently with FMLA otherwise stacks and over-grants time.

## Output format
```
LEAVE EVENT — <employee> | Logged: <date>
Type: <FMLA/ADA/state PFL/PWFA/caregiver> | Dates: <start–end / intermittent>
Eligible: Y/N (basis) | Counter: <x/12wk or 26wk> | Stacking: <concurrent/after/none>
Notices triggered: eligibility <date> | cert due <date+15> | designation <pending>
Escalation: counsel before any denial/discipline/termination
```

## Reference
FMLA eligibility requires 12 months + 1,250 hours at a site with 50+ employees within 75 miles; entitlement is 12 weeks unpaid (26 for military caregiver). ADA reasonable-accommodation leave applies at 15+ employees through the interactive process. State paid-family-leave programs (CA, NY, WA, etc.) may run concurrently or stack. Pregnancy is protected under the PWFA and PDA. Key deadlines: 15-day certification window and prompt designation notices. General reference only, not tailored legal advice.
