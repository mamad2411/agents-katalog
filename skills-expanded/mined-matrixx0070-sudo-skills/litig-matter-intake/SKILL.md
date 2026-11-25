---
name: litig-matter-intake
version: 1.0.0
description: Open a new litigation matter by capturing parties, claims, jurisdiction, key dates, running a conflicts check, and setting up the file.
author: matrixx0070
tags: [litigation, intake, conflicts, docketing, case-management]
capabilities: []
---

## When to use
Use this when a prospective or new client engagement first lands and you need to stand up a clean litigation matter record. Use it to structure the who/what/where/when before any substantive work begins. It captures the facts you will rely on for docketing, conflicts, and staffing.

**Not for:** ongoing status logging (see litig-matter-briefing and the update skill) or folder scaffolding (see litig-matter-workspace).

## Method
1. Capture full legal names of all parties and their roles (plaintiff, defendant, third-party, counsel of record).
2. Record the claims/causes of action and the relief sought, plus any counterclaims signaled.
3. Fix jurisdiction and venue: court, case number if filed, and governing law.
4. Extract key dates: filing date, service date, and any statute-of-limitations horizon. **Decision point:** if a limitations or response deadline falls within 14 days, flag URGENT and surface it first.
5. Run a conflicts check against all named and related parties. **Decision point:** if any potential conflict surfaces, halt intake and route to the conflicts partner before proceeding.
6. Assign a matter number, responsible attorney, and billing arrangement.
7. ATTORNEY-ESCALATION gate: route the completed intake summary to a supervising attorney for review and formal engagement decision before any client communication or filing.

## Example
> A caller reports being sued in Cook County for breach of a supply contract, served yesterday. You capture parties, note the 30-day Illinois response window (URGENT: due in 29 days), record the venue, run conflicts against the counterparty, and route to the supervising attorney for the engagement call.

## Pitfalls
- **Missed limitations horizon:** never treat "recently happened" as safe; compute the actual bar date from the accrual event.
- **Incomplete party list:** related entities and affiliates drive conflicts; capture parents, subsidiaries, and insurers.
- **Assumed venue:** confirm the court from the caption, not the client's paraphrase.
- **Skipping the conflicts halt:** a soft conflict is still a stop condition until cleared.

## Output format
```
MATTER: <name> | No: <matter#>
PARTIES: <party — role; ...>
CLAIMS: <causes of action / relief>
JURISDICTION/VENUE: <court, case#, governing law>
KEY DATES: <event — date>  [URGENT flags]
CONFLICTS: <clear / potential — detail>
RESPONSIBLE ATTORNEY: <name>
STATUS: pending attorney review
```

## Reference
Response deadlines vary: FRCP 12(a) allows 21 days after service (60 days for the U.S. or a waiver-of-service defendant); many states differ (e.g., Illinois generally 30 days). Statutes of limitations are jurisdiction- and claim-specific — contract and tort periods commonly range 2–6 years, and discovery-rule tolling can shift accrual. Conflicts analysis follows ABA Model Rules 1.7 (concurrent) and 1.9 (former client); imputation under 1.10 reaches the whole firm absent screening. Preserve any litigation hold trigger at intake. This is general information and varies by jurisdiction; confirm current rules and dates with the supervising attorney.
