---
name: clinic-semester-handoff
version: 1.0.0
description: Transfer live clinic matters between student cohorts at semester end so status, deadlines, and client expectations carry over with nothing dropped.
author: matrixx0070
tags: [handoff, clinic, continuity, deadlines, confidentiality, supervision]
capabilities: []
---

## When to use
Use this at semester transition when live matters move from a departing student to an incoming one. It captures current posture, imminent deadlines, next steps, client expectations, and confidentiality boundaries so the new student can pick up without re-discovering the file, and so the supervising attorney can confirm continuity and that no deadline was missed.

**Not for:** kicking off research on a new legal issue (use clinic-research-start), the recurring status update for rounds (use clinic-status), or staging drafts for attorney review (use clinic-supervisor-review-queue). A handoff is an internal transfer, not client-facing work — the supervising attorney must confirm it, and neither the departing nor incoming student may give independent legal advice (Model Rule 5.5); both act only under supervision.

## Method
1. List every live matter with current posture in one line each: what stage, who is opposing, what is the theory.
2. Extract all deadlines — statutes of limitation, filing/response dates, hearings — and flag anything due within the transition window.
   **Decision point:** if any deadline falls at or near the gap between cohorts, escalate it to the supervising attorney now; do not assume the incoming student will catch it in time.
3. Record the immediate next steps and any half-finished work product with its location.
4. Capture client expectations and last communication date (Rule 1.4), noting anything you promised the client.
5. Preserve confidentiality: transfer files only through clinic-approved channels; keep client-identifying data out of external or GenAI tools (Rule 1.6).
6. Route the packet to the supervising attorney for continuity sign-off before the departing student's access ends.

## Example
> Matter H-14 (asylum): master hearing set for Feb 3 (during winter break). I-589 drafted, evidence index at 60%. Client last spoke Dec 8, expects a call before the hearing. Flag: hearing is inside the cohort gap — supervisor must assign coverage now.

## Pitfalls
- Handing off a matter without surfacing a deadline that lands during the break.
- Vague "next steps" that force the new student to reconstruct the file from scratch.
- Losing the client's expectations and last-contact date, so a promised update is dropped (Rule 1.4).
- Emailing files or client identifiers through personal or external tools instead of clinic-approved channels (Rule 1.6).

## Output format
```
MATTER: <id / short name>          COHORT: <out student> -> <in student>
POSTURE: <one-line stage + theory>
DEADLINES: <date | event | in-gap? Y/N>
NEXT STEPS: <ordered actions>
WORK PRODUCT: <what exists | location>
CLIENT EXPECTATIONS: <last contact | promises>
CONFIDENTIALITY: <transfer channel confirmed>
SUPERVISOR CONTINUITY SIGN-OFF: <name | date | pending>
```

## Reference
- Model Rules 1.3 (diligence), 1.4 (communication), 1.6 (confidentiality), 5.5 (supervision/UPL).
- ABA Formal Opinion 512: keep client-identifying data out of GenAI tools during transfer.
- Clinic norm: supervising attorney confirms every handoff; no missed deadlines across cohorts.
