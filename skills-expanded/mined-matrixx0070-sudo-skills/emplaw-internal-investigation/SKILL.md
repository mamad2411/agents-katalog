---
name: emplaw-internal-investigation
version: 1.0.0
description: Run a workplace internal investigation end-to-end, from complaint intake through interviews, evidence, findings, and remediation.
author: matrixx0070
tags: [employment, investigation, hr, compliance, workplace]
capabilities: []
---

## When to use
Use this when you need to drive an entire workplace investigation as one continuous process — a complaint has landed and you must go from intake to closed findings without pausing to manage a persisted record. **Not for:** initializing a standalone tracked record (use emplaw-investigation-open); logging one interview or exhibit into an existing record (emplaw-investigation-add); reading back the state of a record (emplaw-investigation-query); drafting the formal memo alone (emplaw-investigation-memo); leadership roll-ups (emplaw-investigation-summary); assessing a firing decision (emplaw-termination-review); or standing up the shared matter folder (emplaw-matter-workspace).

## Method
1. Intake the complaint verbatim; capture reporter, respondent, date, and channel.
2. Frame each allegation as a discrete testable statement. Decision point: if an allegation implicates senior leadership or potential criminal conduct, involve counsel before proceeding — do not self-clear.
3. Assess interim measures (separation of parties, schedule change, paid leave). Decision point: if there is a safety or evidence-tampering risk, impose measures now; else document why none are needed.
4. Build a witness list and evidence map; issue litigation-hold/preservation notices.
5. Interview reporter, then witnesses, then respondent last. Decision point: if a union employee requests representation, honor Weingarten rights before continuing.
6. Weigh evidence against the preponderance standard using the EEOC credibility factors.
7. Write findings, recommend remediation, and close with anti-retaliation follow-up.

## Example
A sales rep alleges her manager made repeated sexual comments. You log the intake, frame three allegations, move the rep to a different reporting line as an interim measure, interview two peers who corroborate two comments, then interview the manager. Peers' consistent detail plus the manager's shifting timeline tips credibility. You find two allegations substantiated by a preponderance and recommend discipline plus a retaliation-monitoring check-in.

## Pitfalls
- **Interviewing the respondent first.** You telegraph the case and invite alibi-shaping; take the respondent last.
- **Promising absolute confidentiality.** You cannot; promise discretion on a need-to-know basis only.
- **Skipping the privilege gate.** Casual notes can waive privilege — route sensitive analysis through counsel under Upjohn.
- **Forgetting retaliation.** The complaint is not closed until you have monitored for and warned against retaliation.

## Output format
```
INTERNAL INVESTIGATION — <matter id>
Reporter / Respondent:
Allegations (framed):
Interim measures:
Witnesses interviewed:
Evidence collected:
Findings (per allegation, preponderance):
Credibility notes:
Remediation recommended:
Anti-retaliation follow-up:
Counsel involved? (privilege):
```

## Reference
General reference, not tailored legal advice. Best-practice checklist: prompt, impartial, thorough, documented. Standard of proof: preponderance of the evidence (more likely than not). EEOC credibility factors: inherent plausibility, demeanor, motive to falsify, corroboration, and past record. Weingarten rights: union employees may request representation in investigatory interviews that could lead to discipline. Upjohn/attorney-client privilege: internal investigations directed by counsel may be privileged; give Upjohn warnings ("I represent the company, not you"). Anti-retaliation: protect participants from adverse action. Interim measures: separation of parties, schedule/reporting change, or paid administrative leave. Attorney-escalation gate: involve counsel to preserve privilege before analyzing legal exposure or interviewing on potential criminal conduct — not legal advice.
