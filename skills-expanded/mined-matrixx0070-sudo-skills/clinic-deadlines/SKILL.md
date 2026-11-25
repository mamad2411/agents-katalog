---
name: clinic-deadlines
version: 1.0.0
description: Build and track a docketing calendar for a matter — limitations periods, filing and response deadlines, and hearing dates — with double-calendaring and supervisor confirmation.
author: matrixx0070
tags: [legal-clinic, docketing, deadlines, statute-of-limitations, malpractice, supervision]
capabilities: []
---

## When to use
Use this whenever a matter has any date that carries consequences: a statute of limitations, a filing or response window, a service deadline, or a hearing. Missing a deadline is one of the top causes of legal malpractice, so this skill exists to make your dates computed, double-checked, and confirmed rather than assumed.

**Not for:** discovering the underlying facts (use clinic-cold-start-interview), adapting the documents those deadlines govern (use clinic-customize), or writing the filing itself (use clinic-draft).

## Method
1. Inventory every date-triggering event: incident date, service date, order date, notice date.
2. Identify the governing rule for each deadline — the statute, court rule, or scheduling order — and cite it. Do not rely on memory or a tool's guess.
3. Compute each date, counting carefully: calendar vs. court days, trigger inclusion, weekends and holidays, mailing/service add-ons.
   **Decision point:** if the limitations period, its accrual date, or any tolling is uncertain, treat the EARLIEST plausible date as the deadline and escalate to your supervisor immediately — never let ambiguity extend a bar date.
4. Double-calendar: record every deadline in the matter file AND the clinic's central docketing system.
5. Add reminder milestones ahead of each hard date (e.g., 30/14/7 days out).
6. Have the supervising attorney confirm the computed dates before you rely on them.

## Example
> Employment clinic: client was terminated on March 3. You note the EEOC charge window, compute the deadline against the governing filing period, count backward for a review milestone, and enter it in both the matter file and the clinic docket. Because accrual timing is arguable, you flag the earliest date and ask your supervisor to confirm before the calendar is trusted.

## Pitfalls
- Counting calendar days when the rule means court days, or forgetting service/mailing add-ons.
- Single-calendaring — one entry, one point of failure.
- Trusting a date a GenAI or web tool produced without verifying it against the actual rule — ABA Op. 512 competence and candor; a hallucinated deadline is malpractice-grade.
- Assuming a limitations period without confirming accrual and tolling with your supervisor.

## Output format
```
MATTER: <matter id>
DEADLINE: <description>
  trigger event / date: ...
  governing rule (cited): ...
  computation: <trigger> + <period> -> <computed date>
  day type: [calendar | court]  add-ons: ...
  reminders: 30d / 14d / 7d
  calendared in: [ ] matter file  [ ] central docket
  SUPERVISOR CONFIRMED: [ ] pending
```

## Reference
- Model Rule 1.3 (diligence — no missed deadlines), 1.1 (competence in computing them), 5.5 (supervised practice).
- ABA Formal Opinion 512 — verify any date or rule a GenAI tool provides; never file on unverified authority.
- Clinic norm: all computed dates double-calendared and confirmed by the supervising attorney.
