---
name: clinic-client-intake
version: 1.0.0
description: Run and document a new-client intake for a legal clinic — eligibility, conflicts, and scope — forming no attorney-client relationship until the supervisor approves.
author: matrixx0070
tags: [legal-clinic, intake, eligibility, conflicts-check, scope, engagement]
capabilities: []
---

## When to use
Use this when a prospective client first approaches the clinic and you need to gather facts, screen eligibility, run a conflicts check, and define a possible scope of representation. Intake is the gate that decides whether the clinic can and should take a matter — done well, it prevents conflicts, sets expectations, and gives the supervising attorney what they need to accept or decline.

**Not for:** logging ongoing contacts once a matter is open (use clinic-client-comms-log), drafting letters to the client (use clinic-client-letter), or standardizing a repeatable procedure (use clinic-build-guide). Critically, intake does not itself create an attorney-client relationship or authorize legal advice — students cannot form the relationship or advise independently (Rule 5.5 / UPL); only the supervising attorney can accept the matter.

## Method
1. Collect prospective-client identity and matter facts, and give a clear non-engagement statement: talking today does not mean the clinic represents you.
2. Screen eligibility against clinic criteria (income, subject matter, jurisdiction, capacity).
3. Run a conflicts check against the clinic's database before discussing substance in depth.
   **Decision point:** if a conflict surfaces or eligibility fails, stop, do not give advice, and escalate to the supervising attorney for a decline/referral decision (Rule 5.5 / UPL).
4. Draft a proposed scope — what the clinic would and would not handle — as a recommendation, not a commitment.
5. Protect confidentiality even at the prospective stage: keep notes in the secure matter file and never enter identifying details into external or AI tools (Rule 1.6; ABA Op. 512).
6. Route the intake packet to the supervising attorney; the relationship forms only on attorney approval and a signed engagement letter.

## Example
> Prospective client "R.K." seeks help contesting a security-deposit withholding. Student confirmed non-engagement upfront, screened income (eligible) and jurisdiction (in-clinic), ran conflicts (none against landlord "Oakview LLC"). Proposed scope: demand letter + small-claims prep; excludes appeals. No advice given. Packet routed to Prof. Lee for accept/decline; engagement letter pending.

## Pitfalls
- Letting the prospective client believe they are represented before attorney approval and a signed engagement letter.
- Giving legal advice during intake — students screen, they do not advise (Rule 5.5).
- Discussing the matter's substance before completing the conflicts check.
- Storing intake notes or names in external or AI tools, breaching prospective-client confidentiality (Rule 1.6).

## Output format
```
NEW-CLIENT INTAKE — CONFIDENTIAL
Date: <YYYY-MM-DD> | Intake by: <student>
Non-engagement statement given: [yes]

Prospective client: <name/initials> | Contact: <...>
Matter summary: <facts>
Eligibility: income [ ] subject [ ] jurisdiction [ ] -> <eligible/ineligible>
Conflicts check: <run against DB> -> <clear / conflict: ...>
Proposed scope: <includes / excludes>
Advice given: none (students do not advise independently)

Routed to: <attorney> | Decision: [ ] accept [ ] decline [ ] refer
Engagement letter: [ ] pending [ ] signed  (relationship forms only when signed)
```

## Reference
- Model Rules 1.6 & 1.18 (confidentiality to clients and prospective clients), 5.5 (UPL — supervision required).
- ABA Formal Opinion 512 — confidentiality and competence when using GenAI in intake.
- Clinic norm: no attorney-client relationship until the supervising attorney approves and the engagement letter is signed.
