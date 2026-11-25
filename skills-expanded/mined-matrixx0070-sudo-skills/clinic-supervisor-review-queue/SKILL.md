---
name: clinic-supervisor-review-queue
version: 1.0.0
description: Assemble and prioritize student work items awaiting supervising-attorney review so nothing goes to a client or court unreviewed.
author: matrixx0070
tags: [review-queue, clinic, supervision, prioritization, deadlines, work-product]
capabilities: []
---

## When to use
Use this to build the queue of student work items waiting on supervising-attorney review, ordered by deadline and risk, with each item made review-ready. This is the enforcement point for the clinic's core rule: no work product leaves for a client or court until a supervising attorney has reviewed and approved it (Model Rule 5.5).

**Not for:** starting research (use clinic-research-start), reporting a single matter's status (use clinic-status), or transferring matters between cohorts (use clinic-semester-handoff). The queue does not itself approve anything — approval is the attorney's act. Students prepare and stage work here but cannot give independent legal advice or release output on their own signature.

## Method
1. Collect every item awaiting review across matters: memos, drafts, letters, filings, client communications.
2. For each item, attach the draft and state what it is, the specific ask of the reviewer, and the deadline.
   **Decision point:** if an item is bound for a client or court, it cannot be sent until the attorney approves — mark it BLOCKED-UNTIL-REVIEW regardless of how tight the deadline is.
3. Order the queue by deadline, then by risk (irreversible filings, limitations dates, client-relied-upon advice first).
4. Confirm each draft is review-ready: citations Shepardized/KeyCited and read, GenAI-sourced material verified, not just accepted (ABA Op. 512).
5. Flag confidentiality: ensure drafts and the queue itself do not expose client identifiers to external or GenAI tools (Rule 1.6).
6. Note the reviewer assigned and leave an approval field the attorney fills — never pre-mark an item approved.

## Example
> Queue, week of Mar 3:
> 1. [BLOCKED-UNTIL-REVIEW] Motion to dismiss reply — court filing due Mar 6 (HIGH risk). Ask: confirm the two cited cases and the tone of section II.
> 2. Client update letter, Matter B-02 — due Mar 8. Ask: approve before send; client waiting since Feb 20.

## Pitfalls
- Letting a student send a client letter or file with a court before the attorney signs off.
- Ordering by convenience rather than deadline and risk, so a limitations-date filing slips.
- Queueing a draft with unread or unverified GenAI citations, pushing verification onto the reviewer.
- Including client-identifying detail in a shared queue or external tool (Rule 1.6).

## Output format
```
REVIEW QUEUE — WEEK OF <date>
# | MATTER | ITEM | ASK OF REVIEWER | DEADLINE | RISK | DRAFT ATTACHED | STATUS
- STATUS = BLOCKED-UNTIL-REVIEW | IN REVIEW | APPROVED (attorney fills)
- Order: deadline, then risk (irreversible/limitations/client-relied first)
REVIEWER: <attorney name>     APPROVAL (attorney only): <sign/date>
```

## Reference
- Model Rule 5.5: student work product is released only after supervising-attorney review — the queue enforces it.
- ABA Formal Opinion 512: verify GenAI-derived content before it enters the review queue (competence/candor).
- Model Rules 1.3 (diligence), 1.6 (confidentiality); clinic norm: nothing goes out unreviewed.
