---
name: emplaw-investigation-open
version: 1.0.0
description: Open and initialize a new investigation record with complaint intake, allegation framing, scope, interim measures, and privilege setup.
author: matrixx0070
tags: [employment, investigation, intake, hr, privilege]
capabilities: []
---

## When to use
Use this when a complaint arrives and you need to create the persisted investigation RECORD — a tracked folder with a manifest that later steps append to. This is the "new file" step of the record lifecycle. **Not for:** running the whole investigation in one pass (use emplaw-internal-investigation); appending evidence or interviews to a record that already exists (emplaw-investigation-add); reading the record back (emplaw-investigation-query); drafting the memo (emplaw-investigation-memo); leadership roll-ups (emplaw-investigation-summary); termination decisions (emplaw-termination-review); or provisioning the shared matter folder itself (emplaw-matter-workspace).

## Method
1. Assign a matter id and create the record manifest (parties, dates, channel, status=OPEN).
2. Record the complaint verbatim; note whether reporter requests anonymity.
3. Frame each allegation as a discrete, testable statement with the policy or law it implicates.
4. Define scope and out-of-scope items. Decision point: if allegations reach senior leadership or possible criminal conduct, escalate to counsel and mark the record privileged before framing further.
5. Decide interim measures. Decision point: if there is safety or tampering risk, impose separation/leave now and log it; else record "none — rationale."
6. Set the privilege posture (who directs the work; Upjohn warnings planned).
7. Seed the witness/evidence stub list and issue a preservation hold. Save the manifest.

## Example
An engineer emails HR alleging his lead retaliated after he reported safety violations. You open matter EMP-2026-014, log the email verbatim, frame two allegations (retaliation; unsafe-condition report), scope out an unrelated pay dispute, impose no separation but issue a preservation hold on Slack and email, mark the record counsel-directed, and stub three witnesses. Status: OPEN.

## Pitfalls
- **Vague allegation framing.** "Hostile behavior" is untestable; break it into dated, specific acts.
- **Opening without a hold.** Evidence walks — issue preservation at open, not at findings.
- **Guessing the privilege posture.** Decide up front whether counsel directs the work; retrofitting privilege rarely holds.
- **Over-scoping.** A sprawling scope stalls the investigation; state out-of-scope items explicitly.

## Output format
```
INVESTIGATION RECORD — OPEN
Matter id:
Opened / By:
Reporter (anonymity?):
Respondent(s):
Complaint (verbatim):
Allegations (framed + policy/law):
Scope / Out-of-scope:
Interim measures (or none + rationale):
Preservation hold issued:
Privilege posture (counsel-directed?):
Witness/evidence stubs:
Status: OPEN
```

## Reference
General reference, not tailored legal advice. Intake should be prompt and impartial. Allegations must be discrete and testable so findings map cleanly. Interim measures: separation of parties, schedule/reporting change, or paid administrative leave — proportionate to risk. Preservation: issue a litigation hold at open to prevent spoliation. Upjohn/attorney-client privilege: if counsel directs the investigation it may be privileged; plan Upjohn warnings. Anti-retaliation obligations attach the moment a protected report is made. Attorney-escalation gate: involve counsel to preserve privilege before framing allegations that touch legal exposure, leadership, or criminal conduct — not legal advice.
