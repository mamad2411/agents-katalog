---
name: ipl-cold-start-interview
version: 1.0.0
description: Run a structured intake interview on a new IP matter to capture the minimum facts and route it to the right sibling skill.
author: matrixx0070
tags: [intake, routing, triage, ip, interview, escalation, front-door]
capabilities: []
---

## When to use

Use this as the front door when a new IP matter arrives with little context and you don't yet know which framework applies. It gathers the minimum facts, names the IP type and goal, and routes to the correct sibling skill so nothing starts in the wrong lane.

**Not for:** running the substantive analysis itself (route to `ipl-clearance`, `ipl-fto-triage`, or the matching skill), setting org-wide default positions (`ipl-customize`), or organizing an already-scoped matter's files and deadlines (`ipl-matter-workspace`).

## Method

1. **Ask the goal in plain words.** What are you trying to do? Map the answer: adopt a name → `ipl-clearance`; demand letter or copycat found → `ipl-infringement-triage`; launching a product → `ipl-fto-triage`; made something new → `ipl-invention-intake`; reviewing a contract → `ipl-ip-clause-review`; using open source → `ipl-oss-review`; content stolen online → `ipl-takedown`; managing existing assets → `ipl-portfolio`.
2. **Capture the frame.** Jurisdiction(s), IP type (patent, trademark, copyright, trade secret), business goal, and any dates.
3. **Screen for hard deadlines.** Note statutory windows, hearing dates, or response deadlines.
4. **Decision point:** which single route best fits the stated goal — if two apply, pick the one blocking the nearest deadline and note the second as a follow-on.
5. **ATTORNEY-ESCALATION GATE:** active litigation, a received lawsuit or demand letter, or any hard legal deadline routes straight to a licensed attorney before any self-serve skill. You assist with intake and routing only — nothing here is legal advice.
6. **Hand off.** Name the chosen skill and pass the captured facts forward.

## Example

Message: "A competitor is selling shirts with our logo." Goal → copycat found. IP type → trademark (possibly copyright). No lawsuit, no deadline. Route: `ipl-infringement-triage`. Captured: US jurisdiction, mark in use since 2021, goal = stop the sales.

## Pitfalls

- **Analyzing instead of routing.** This skill only gathers and directs — resist diagnosing the merits here.
- **Missing a live deadline.** A buried response window can forfeit rights; screen for dates before routing.
- **Forcing one route.** Some matters split into two skills; name the primary and flag the secondary.
- **Skipping the escalation gate.** Litigation and demand letters go to an attorney first, not a self-serve skill.

## Output format

```
NEW MATTER INTAKE
Stated goal: <plain-words description>
IP type(s): patent | trademark | copyright | trade secret
Jurisdiction(s):
Deadlines / dates:
Escalation flag: <none | attorney — litigation/demand/deadline>
Route to: <sibling skill>  | Secondary (if any):
Facts passed forward:
```

## Reference

ROUTING MAP (situation → skill): adopt a name → `ipl-clearance`; demand letter/copycat → `ipl-infringement-triage`; launching a product → `ipl-fto-triage`; made something new → `ipl-invention-intake`; reviewing a contract → `ipl-ip-clause-review`; using open source → `ipl-oss-review`; content stolen online → `ipl-takedown`; managing existing assets → `ipl-portfolio`.

The four IP types are patent, trademark, copyright, and trade secret. The analytical frameworks the sub-plugin relies on are: trademark likelihood-of-confusion factors, patentability bars (§§101/102/103/112), OSS license obligations, and DMCA §512 elements.
