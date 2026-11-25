---
name: ipl-matter-workspace
version: 1.0.0
description: Set up an auditable workspace for a single IP matter with a docket, folder structure, deadline calendar, and correspondence log.
author: matrixx0070
tags: [workspace, docket, deadlines, organization, evidence, correspondence, matter-management]
capabilities: []
---

## When to use

Use this once a matter is scoped and you need it organized so nothing — especially a deadline — is dropped. It builds the docket entry, folder structure, deadline calendar, evidence/exhibit index, correspondence log, and status tracker that make a matter auditable end to end.

**Not for:** deciding which skill a raw matter belongs to (`ipl-cold-start-interview`), setting org-wide default positions (`ipl-customize`), or the substantive analysis of the matter itself (`ipl-clearance`, `ipl-infringement-triage`, and siblings).

## Method

1. **Create the matter record.** Type, parties, jurisdiction, key dates, responsible people, and the sibling skill(s) in play.
2. **Build the structure.** Folder tree, evidence/exhibit index, and correspondence log seeded and ready.
3. **Seed the deadline docket.** Enter every known date with reminders ahead of each.
4. **Decision point:** classify each date as deadline-critical or informational — deadline-critical dates get docketed with layered reminders and a named owner.
5. **Log every communication.** Inbound and outbound, dated, into the correspondence log as it happens.
6. **ATTORNEY-ESCALATION GATE:** statutory and filing deadlines (trademark maintenance windows, patent office-action response windows, DMCA counter-notice windows) must be confirmed and owned by an attorney or paralegal — a missed deadline can forfeit rights. You maintain the workspace and reminders; you do not calculate or own legal deadlines, and nothing here is legal advice.
7. **Track status to closure.** Move the matter through defined states and archive on close.

## Example

New trademark opposition matter opened. Record: parties, USPTO jurisdiction, filing date. Folder tree and exhibit index built; correspondence log started. Deadline docket seeded with the response window flagged deadline-critical, owner = supervising attorney, reminders at 30/14/3 days. Status: Active. Every TTAB email logged as received.

## Pitfalls

- **Treating an informational date as the deadline.** Distinguish critical statutory windows from soft internal dates.
- **Unowned deadlines.** A docketed date with no named owner is a missed date waiting to happen.
- **Gaps in the correspondence log.** Log communications as they occur — reconstructing later loses the record.
- **Self-calculating a statutory window.** Deadline math is attorney/paralegal work; confirm, don't compute.

## Output format

```
MATTER WORKSPACE — <matter name/id>
Type / parties / jurisdiction:
Skill(s) in play:
Folders: <tree>  | Exhibit index: <ref>  | Correspondence log: <ref>
Deadline docket:
  | Date | Item | Critical? | Owner | Reminders |
Status: <Intake|Active|On hold|Closed>
Attorney/paralegal owner of statutory deadlines:
```

## Reference

Key deadline classes to track: trademark maintenance (§8 declaration between years 5-6, combined §8 & §9 renewal every 10 years); patent maintenance fees (3.5, 7.5, and 11.5 years) and office-action response windows; copyright/DMCA §512(g) counter-notice window (10-14 business days); and applicable statutes of limitations.

These classes tie back to the patentability bars (§§101/102/103/112) and likelihood-of-confusion assessments captured in sibling skills. Confirm every window with an attorney or paralegal — a missed statutory deadline can forfeit rights, and nothing here is legal advice.
