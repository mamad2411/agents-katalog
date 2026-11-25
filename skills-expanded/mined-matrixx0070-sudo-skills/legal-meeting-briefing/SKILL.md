---
name: legal-meeting-briefing
version: 1.0.0
description: Prepare an attendee for a legally-relevant meeting and capture the decisions, commitments, and action items that come out of it.
author: matrixx0070
tags: [legal, meeting, briefing, action-items, preparation, negotiation]
capabilities: []
---

## When to use
Use this before a meeting with legal stakes — a negotiation, a regulator call, a board matter, a dispute discussion, a vendor sign-off — and again after it to capture what was decided. The attendee walks in prepared and walks out with tracked commitments.

**Not for:** routine internal meetings with no legal exposure, drafting the agreement itself (use `legal-review-contract`), or giving the attendee legal advice on positions (attorney-set red lines only).

## Method
1. **State purpose and desired outcome.** What decision or agreement should exist when the meeting ends.
2. **Profile the parties.** Who attends, their interests, likely positions. Note privilege or confidentiality boundaries.
3. **Assemble the record.** Relevant contracts, prior correspondence, open issues, and each item's status. Flag anything still under attorney review.
4. **Prepare positions.** For each contested point: our position, acceptable range, fallback, walk-away. Mark red lines. *Decision point:* red lines and settlement authority are set by counsel, not the attendee — confirm them in advance.
5. **List questions to ask** and commitments to avoid making without counsel.
6. **Capture outcomes.** During/after, record decisions, who committed to what, deadlines, and items deferred to counsel.
7. **Log action items** with owner, due date, and status.

## Example
Meeting: renewal negotiation with a key vendor. Desired outcome: agreed price and a mutual liability cap. Parties: vendor CSM (wants multi-year lock-in) + our procurement. Positions — price: target 5% cut, range 0-8%, walk-away above list; liability: red line = must be mutual and ≥ 12 months fees (counsel-set). Question to ask: "Will you accept a 30-day termination-for-convenience?" Defer: any indemnity change → counsel. Post-meeting decision: 4% cut agreed, cap deferred to legal. Action item: send redline of cap clause (owner: procurement, by Wed).

## Pitfalls
- **Walking in without a walk-away.** Without a defined floor, the attendee concedes under pressure.
- **Committing on the spot to counsel-only terms.** Indemnity, liability, and IP get deferred, not agreed live.
- **No post-meeting capture.** Verbal commitments evaporate; write them down while fresh.
- **Action items with no owner or date.** Follow-through dies in the gap.

## Output format
```
Meeting / purpose / desired outcome:
Attendees & interests:
Key documents & status:
Positions:
  | Point | Our stance | Range | Red line |
Questions to ask:
Commitments to defer to counsel:
Decisions made (post-meeting):
Action items:
  | Item | Owner | Due | Status |
```

## Negotiation position framework
Walk in with a ladder for every contested point, not a single number. The ladder has four rungs: **Target** (your opening ask, ambitious but defensible), **Acceptable range** (the band you can settle inside without further approval), **Fallback** (the less-good but still-workable position you retreat to under pressure), and **Walk-away / BATNA** (the point past which no deal beats the best alternative away from the table).

| Point | Target | Acceptable range | Fallback | Walk-away (BATNA) |
|-------|--------|------------------|----------|-------------------|
| Price | 8% reduction | 3-8% reduction | List price flat | Above list → use alternate vendor |
| Liability cap | 24 months' fees, mutual | 12-24 months, mutual | 12 months, mutual | Unilateral or uncapped → no deal |
| Termination rights | 30-day termination for convenience | 30-60 day notice | Termination for cause only | Locked multi-year, no exit → no deal |

**Red lines and settlement authority are set by counsel, not by the attendee.** The attendee negotiates inside a mandate; they do not invent the floor in the room. Confirm the walk-away and the dollar/term authority in writing before the meeting, and if the conversation pushes past it, defer rather than concede.

## Meeting-type playbook
Different meetings carry different legal traps. Match your prep to the type.

| Meeting type | Prep focus | Live traps to avoid |
|--------------|-----------|---------------------|
| Vendor / commercial negotiation | Position ladder, prior terms, budget authority | Agreeing to liability, indemnity, or IP terms on the spot |
| Regulator call | Exact facts, what has been produced, counsel's script | Speculating, volunteering scope, admitting fault or non-compliance |
| Board / committee matter | Materials in advance, decision framing, minutes plan | Discussing privileged advice in front of non-privileged attendees |
| Dispute / settlement discussion | Authority range, key facts, privilege posture | Naming settlement figures without authority; admitting liability |
| Partnership / BD | Deal shape, exclusivity limits, IP ownership stance | Committing to exclusivity or IP assignment live |

Privilege reminders: keep counsel on privileged threads so the advice stays protected, do not create bad documents (write as if opposing counsel will read it), and let counsel — not the attendee — decide when a "Privileged & Confidential" header actually applies. **Never commit live to:** indemnity, liability allocation, IP ownership or license grants, admissions of fault, or settlement figures.

## Commitments-to-defer
Route these to counsel rather than agreeing in the room, even under pressure to "just close it":

- [ ] Indemnification obligations (scope, caps, carve-outs)
- [ ] Limitation-of-liability and liability caps
- [ ] IP ownership, assignments, and license grants
- [ ] Confidentiality and data-processing terms
- [ ] Governing law, jurisdiction, and dispute-resolution clauses
- [ ] Termination rights and exit/wind-down obligations
- [ ] Exclusivity, non-compete, or most-favored-nation terms
- [ ] Any settlement figure or admission touching a dispute
- [ ] Warranties and representations beyond the standard set
- [ ] Pricing outside your approved authority

## Post-meeting capture
Record decisions, commitments, and action items while they are fresh — verbal commitments evaporate within hours. When capturing:

- **Distinguish a decision from a discussion.** "We agreed to a 4% cut" is a decision; "we talked about pricing" is not. Write only what was actually resolved as resolved, and mark the rest as open.
- **Attribute commitments.** Who committed to what, by when. Unowned commitments do not happen.
- **Flag for privilege or correction.** If anything said in the room may need privilege review, or if the attendee misspoke or over-committed, flag it immediately so counsel can correct the record before it hardens.

**Anti-trust / competitor sensitivities:** if the meeting involves a competitor (industry group, benchmarking, partnership talks), do not discuss price, output, market allocation, or customers. These conversations carry serious anti-trust exposure — keep to the stated, lawful agenda and route anything sensitive to counsel before, not after.
