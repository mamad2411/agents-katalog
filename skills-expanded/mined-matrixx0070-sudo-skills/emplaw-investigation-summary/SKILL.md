---
name: emplaw-investigation-summary
version: 1.0.0
description: Produce a concise closure summary or status roll-up of an investigation for leadership.
author: matrixx0070
tags: [employment, investigation, summary, leadership, reporting]
capabilities: []
---

## When to use
Use this when leadership needs a short, decision-ready roll-up of an investigation RECORD — status, headline findings, and next steps — without the full memo's detail. **Not for:** creating the record (use emplaw-investigation-open); appending items (emplaw-investigation-add); reading raw state (emplaw-investigation-query); the full findings document (emplaw-investigation-memo); running the whole process (emplaw-internal-investigation); termination decisions (emplaw-termination-review); or the shared matter folder (emplaw-matter-workspace).

## Method
1. Pull status, findings, and remediation from the record manifest and memo.
2. Decide the audience. Decision point: if the reader lacks need-to-know or the matter is privileged, redact party names and route through counsel before sending.
3. State status in one line (OPEN / findings drafted / CLOSED).
4. Summarize each allegation and its finding in a single clause — no evidence recitation.
5. State remediation taken or recommended and the anti-retaliation follow-up.
6. Flag open risks and decisions leadership must make. Decision point: if a finding creates legal exposure, note "counsel engaged" rather than describing the exposure.
7. Keep it to one screen; link to the full memo for detail.

## Example
For the harassment matter you send leadership: status CLOSED; three allegations, two substantiated, one inconclusive; remediation = final written warning plus training; retaliation monitoring for 90 days; counsel engaged on privilege; no further action required from leadership beyond approving the discipline. Full memo linked.

## Pitfalls
- **Leaking detail up the chain.** Leadership needs outcomes, not verbatim testimony — summarize, don't dump.
- **Naming parties needlessly.** Use roles unless the reader has need-to-know.
- **Editorializing exposure.** Describe legal risk in the memo under privilege, not in a wide summary.
- **Stale status.** A roll-up is a snapshot — timestamp it and mark the record state.

## Output format
```
INVESTIGATION STATUS SUMMARY
Matter id / As-of date:
Status: OPEN | FINDINGS DRAFTED | CLOSED
Allegations & findings (one line each):
Remediation (taken/recommended):
Anti-retaliation follow-up:
Open risks / decisions needed:
Counsel engaged? (privilege):
Full memo: <link>
```

## Reference
General reference, not tailored legal advice. Roll-ups should give leadership enough to decide without waiving privilege or over-sharing. Findings rest on the preponderance-of-evidence standard and EEOC credibility factors; the summary reports outcomes, not the analysis. Upjohn/attorney-client privilege: broad distribution can waive it — limit to need-to-know and keep legal-exposure analysis in the counsel-directed memo. Anti-retaliation obligations continue after closure; note the monitoring plan. Attorney-escalation gate: involve counsel to preserve privilege before summarizing legal exposure or distributing beyond the need-to-know circle — not legal advice.
