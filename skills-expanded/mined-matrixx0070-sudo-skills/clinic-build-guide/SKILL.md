---
name: clinic-build-guide
version: 1.0.0
description: Build a reusable, supervisor-approved runbook that standardizes a recurring legal-clinic task or matter type for other students to follow.
author: matrixx0070
tags: [legal-clinic, runbook, template, supervision, workflow, standardization]
capabilities: []
---

## When to use
Use this when your clinic keeps handling the same kind of matter — expungement petitions, tenant demand letters, name-change filings — and each student reinvents the process. You are capturing a stable, repeatable procedure so the next student starts from a vetted baseline instead of a blank page. Write the guide when you have run the task at least once and understand its real steps, dependencies, and jurisdiction-specific quirks.

**Not for:** documenting facts of a single live client matter (use clinic-client-intake and clinic-client-comms-log), drafting anything a client will read (use clinic-client-letter), or publishing legal positions as settled advice. A build guide is internal process scaffolding, not legal advice to any person, and never a substitute for the supervising attorney's judgment on a specific case.

## Method
1. Name the matter type and the exact trigger that starts it. Keep scope narrow enough that steps stay concrete.
2. List prerequisites: forms, filing fees, deadlines, court/agency contacts, and which clinic templates feed in.
3. Write the steps in order, each as a single action with the artifact it produces.
   **Decision point:** if any step requires interpreting law or advising a client, mark it "ATTORNEY REVIEW REQUIRED" — students execute process, they do not independently render legal advice (Rule 5.5 / UPL).
4. Add a confidentiality note: strip client identifiers from any example; never paste real client data into external drafting or AI tools (Rule 1.6; ABA Op. 512).
5. Route the draft to the supervising attorney for sign-off before circulation.
6. Version and date it; flag a review interval so the guide does not silently go stale against changed law or local rules.

## Example
> Guide: "Misdemeanor Expungement Petition (State X)". Trigger: client eligible under §XX after intake approval. Steps: (1) confirm eligibility checklist [ATTORNEY REVIEW REQUIRED], (2) pull certified disposition, (3) populate Petition template EX-1, (4) prepare proposed order, (5) attorney reviews packet, (6) file with clerk, (7) calendar hearing. Sample records anonymized as "Client A."

## Pitfalls
- Baking in a legal conclusion as if settled — law and local rules drift; mark interpretive steps for attorney review.
- Embedding real client names or facts as examples, exposing confidential info (Rule 1.6).
- Circulating the guide before the supervising attorney signs off.
- Writing steps so abstract they smuggle unsupervised judgment past the reader.

## Output format
```
# Build Guide: <Matter Type> (<Jurisdiction>)
Version: 1.0.0 | Date: <YYYY-MM-DD> | Author: <student> | Approved by: <attorney>
Review by: <YYYY-MM-DD>

Trigger: <what starts this matter>
Prerequisites: <forms / fees / deadlines / templates>

Steps:
1. <action> -> <artifact>   [ATTORNEY REVIEW REQUIRED?]
...

Confidentiality note: <anonymization / no external tools with client data>
```

## Reference
- ABA Formal Opinion 512 — competence and confidentiality duties when using GenAI in legal work.
- Model Rules 1.1 (competence), 1.6 (confidentiality), 5.5 (UPL — student work under supervision only).
- Clinic norm: no process guide circulates without supervising-attorney sign-off.
