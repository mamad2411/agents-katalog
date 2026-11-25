---
name: corpl-material-contract-schedule
version: 1.0.0
description: Build the material-contract schedule for a disclosure schedule or diligence deliverable — every in-scope agreement with the terms that matter.
author: matrixx0070
tags: [corporate-legal, m&a, disclosure-schedule, contracts, materiality, diligence]
capabilities: []
---

## When to use

Use this to compile the schedule of material contracts that supports a disclosure schedule (against the definitive agreement's reps) or a diligence deliverable: which agreements are in scope, their key economic and legal terms, and the flags (assignment, change-of-control, exclusivity) that drive deal decisions.

**Not for:** open-ended issue-spotting across all documents (use corpl-diligence-issue-extraction); drafting the reps themselves; deciding whether a given contract legally qualifies as "material" under the agreement's definition — apply the stated threshold and flag edge cases for counsel. The schedule organizes facts against a defined standard; counsel confirms scope calls.

## Method

1. **Fix the materiality standard.** Use the definitive agreement's contract-schedule definition, or the customized threshold (dollar value, term length, contract type). Do not improvise "material."
2. **Assemble the contract population** from the data room, deduplicating amendments against their base agreements.
3. **Screen each contract against the standard.** In-scope / out-of-scope; *Decision point:* borderline calls are listed and flagged for counsel rather than silently included or dropped.
4. **Extract key terms per in-scope contract:** parties, effective date, term/renewal, value, termination rights, assignment clause, change-of-control provision, exclusivity/non-compete, governing law.
5. **Flag deal-relevant triggers** — especially consent-on-assignment and change-of-control, which determine what the transaction requires.
6. **Organize by the schedule's section structure** so it maps cleanly onto the corresponding rep.
7. **Route to counsel** for scope confirmation before it becomes part of the disclosure schedule.

## Example

Threshold from the SPA: contracts >$100K/yr, any exclusivity, or any change-of-control clause. Population: 60 agreements, 12 dropped as amendments to base contracts, 41 in scope, 7 borderline (near-threshold value) flagged for counsel. Extracted into a table; 9 contracts have change-of-control consent triggers, 3 have exclusivity — surfaced as deal-relevant. Organized under disclosure-schedule §3.11 (Material Contracts).

## Pitfalls

- **Inventing the materiality line.** The threshold comes from the agreement or the profile, never from feel.
- **Counting amendments as separate contracts.** Roll amendments into their base agreement.
- **Missing change-of-control and assignment clauses.** These are the terms the whole transaction turns on.
- **Silent scope calls.** A borderline contract quietly included or excluded can misstate a rep — flag it.

## Output format

```
MATERIAL CONTRACT SCHEDULE — <deal> | Standard: <threshold/definition>
Schedule section: <e.g., §3.11>
  | # | Contract | Parties | Effective | Term/renewal | Value | Assignment | Change-of-control | Exclusivity | Gov. law |
Deal-relevant triggers (assignment/CoC/exclusivity):
Borderline scope calls — for counsel:
Population reconciliation: <total docs / amendments merged / in scope>
For attorney scope confirmation before inclusion in the disclosure schedule
```

## Reference

Disclosure-schedule structure: schedules are keyed to specific representations in the definitive agreement (e.g., the material-contracts rep), so organize the contract schedule to map onto its section. Materiality is defined by the agreement or the engagement profile — apply it, do not create it. The load-bearing terms for M&A are assignment/anti-assignment, change-of-control, exclusivity/non-compete, and termination rights, since they determine required consents and post-closing effect. Scope determinations and final inclusion are confirmed by counsel.
