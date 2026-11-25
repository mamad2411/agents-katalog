---
name: clinic-customize
version: 1.0.0
description: Adapt a clinic template, precedent, or form to a specific client matter while tracking every change and the reason for it.
author: matrixx0070
tags: [legal-clinic, template, precedent, customization, jurisdiction, supervision]
capabilities: []
---

## When to use
Use this when you have a starting document — a clinic template, a prior client's precedent, or an official court form — and you need to make it fit the client in front of you. The value is in the discipline: change deliberately, record what you changed, and explain why, so your supervisor can verify the fit fast.

**Not for:** collecting the facts in the first place (use clinic-cold-start-interview), writing a document from scratch (use clinic-draft), or setting the dates and filing windows the customized document must meet (use clinic-deadlines).

## Method
1. Identify the source document's origin, jurisdiction, and vintage. A precedent from another state or an old form may carry stale law.
2. Map the template's variables and boilerplate against this matter's facts and forum.
3. Edit one section at a time; for each change, log the old value, the new value, and the reason.
4. Strip any residual identifying data from the source precedent — a prior client's name in a reused document is a Rule 1.6 breach.
   **Decision point:** if a clause's fit depends on a legal judgment you are not competent or authorized to make (e.g., which cause of action applies), do NOT resolve it yourself — flag it for the supervising attorney. Choosing the theory is legal advice under Rule 5.5.
5. Verify every citation, defined term, and cross-reference still resolves after editing.
6. Deliver the redline plus a change log to your supervisor before anything reaches the client or court.

## Example
> Small-business clinic: you adapt a template operating agreement for a two-member LLC. You change member names, capital contributions, and the governing-law clause from Delaware to the client's home state — logging each edit. You flag "buy-sell trigger events — confirm these match client's stated intent" for supervisor review rather than guessing.

## Pitfalls
- Find-and-replace that misses a name or dollar figure buried in boilerplate.
- Carrying over a prior client's identifying details — Rule 1.6 violation.
- Leaving citations or statutory references that were correct in the source jurisdiction but wrong here.
- Pasting the template into an external GenAI tool with client facts to "just clean it up" — ABA Op. 512 confidentiality and competence duties; verify anything a tool suggests.

## Output format
```
SOURCE DOC: <name / origin / jurisdiction / date>
TARGET MATTER: <matter id / forum>
CHANGE LOG:
  - [section] old: ... -> new: ...  | reason: ...
CARRY-OVER DATA REMOVED: [ ]
CITATIONS RE-VERIFIED: [ ]
FLAGGED FOR SUPERVISOR: ...
SUPERVISOR REVIEW: [ ] pending
```

## Reference
- Model Rule 1.1 (competence — right jurisdiction and current law), 5.5 (UPL — no independent choice of legal theory).
- Rule 1.6 (confidentiality); ABA Formal Opinion 512 — verify GenAI output, protect client data.
- Clinic norm: customized documents ship only after supervising-attorney sign-off.
