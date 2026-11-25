---
name: emplaw-investigation-memo
version: 1.0.0
description: Draft the formal investigation memorandum with findings and credibility analysis from a completed investigation record.
author: matrixx0070
tags: [employment, investigation, memo, findings, credibility]
capabilities: []
---

## When to use
Use this when an investigation RECORD is substantially complete and you must produce the formal memorandum — allegation-by-allegation findings with a reasoned credibility analysis under the preponderance standard. **Not for:** creating the record (use emplaw-investigation-open); appending items (emplaw-investigation-add); reading state (emplaw-investigation-query); running the full process (emplaw-internal-investigation); a short leadership roll-up (emplaw-investigation-summary); termination decisions (emplaw-termination-review); or the shared matter folder (emplaw-matter-workspace).

## Method
1. Confirm from the record that the respondent was interviewed and gaps are closed. Decision point: if not, return to emplaw-investigation-add/query before drafting.
2. State scope, methodology, and who directed the work (privilege posture).
3. For each allegation, marshal the supporting and contradicting evidence.
4. Apply the EEOC credibility factors witness by witness where accounts conflict.
5. Reach a finding per allegation: substantiated / not substantiated / inconclusive, under the preponderance standard. Decision point: if evidence is evenly balanced, the allegation is not substantiated — state that plainly rather than straining.
6. Recommend remediation proportionate to substantiated findings.
7. Route the draft through counsel before distribution. Decision point: if the memo analyzes legal liability, keep it privileged and counsel-directed.

## Example
For the harassment matter, the memo frames three allegations. Two peers corroborate comments A and B with consistent, detailed accounts; the respondent's account shifts on dates (motive/demeanor factors weigh against him). Comment C has only the reporter's word and no corroboration. Findings: A and B substantiated by a preponderance; C inconclusive. Recommendation: final written warning plus training, with a retaliation-monitoring plan.

## Pitfalls
- **Findings without factor analysis.** "I believe her" is not a finding; show the EEOC factors that drove it.
- **Overstating the standard.** This is preponderance, not beyond reasonable doubt — don't demand certainty.
- **Editorializing.** Keep tone neutral and evidence-anchored; conclusions follow facts, not adjectives.
- **Distributing before counsel review.** Wide circulation can waive privilege — gate distribution through counsel.

## Output format
```
INVESTIGATION MEMORANDUM
Matter id / Date / Prepared by:
Privilege: (counsel-directed? Upjohn given?)
Scope & methodology:
Allegation 1: <statement>
  Evidence for / against:
  Credibility analysis (EEOC factors):
  Finding (preponderance): substantiated | not substantiated | inconclusive
[repeat per allegation]
Recommended remediation:
Anti-retaliation plan:
Distribution (need-to-know):
```

## Reference
General reference, not tailored legal advice. Standard of proof: preponderance of the evidence (more likely than not). EEOC credibility factors: inherent plausibility, demeanor, motive to falsify, corroboration, and past record — apply them explicitly where accounts conflict. Upjohn/attorney-client privilege: a memo prepared at counsel's direction may be privileged; limit distribution to need-to-know and label accordingly. Anti-retaliation obligations continue after findings. Remediation should be proportionate and consistently applied. Attorney-escalation gate: involve counsel to preserve privilege before the memo analyzes legal liability or is distributed beyond the core team — not legal advice.
