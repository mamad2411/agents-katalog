---
name: litig-oc-status
version: 1.0.0
description: Track opposing-counsel contacts, outstanding items, meet-and-confer obligations, negotiation posture, and pending correspondence.
author: matrixx0070
tags: [litigation, opposing-counsel, meet-and-confer, negotiation, discovery]
capabilities: []
---

## When to use
Use this to keep a live picture of your relationship with the other side: who said what, what you owe them, what they owe you, and what is overdue. Reach for it before a meet-and-confer, before sending a discovery deficiency letter, or when a judge asks whether you conferred in good faith. It keeps commitments and deadlines from slipping between calls and emails.

**Not for:** proving your own claim (use litig-claim-chart) or firm-wide matter rollups (use litig-portfolio-status).

## Method
1. Log every contact: date, medium, participants, and a one-line substance summary.
2. Separate outstanding items into "we owe them" and "they owe us," each with a due date and the source obligation (rule, order, or agreement).
3. Track meet-and-confer status per dispute: raised, conferred, impasse, or resolved.
4. **Decision point:** if a meet-and-confer reaches impasse, decide whether to send a final deficiency letter with a deadline or move directly to a motion to compel.
5. **Decision point:** if the other side missed a deadline, decide whether to grant a professional-courtesy extension (document it) or hold them to the date.
6. Note tone and negotiation posture (cooperative, positional, stonewalling) to calibrate your next move.
7. ATTORNEY-ESCALATION gate: route any deficiency letter, extension agreement, or settlement communication to a supervising attorney for review before sending.

## Example
> 2026-07-09, email, Nguyen (OC): agreed to produce ESI by 7/23. WE OWE: privilege log by 7/16 (per 7/1 order). THEY OWE: RFP set 2 responses, overdue since 7/2 → conferred 7/8, impasse. Posture: positional. Next: final deficiency letter, 5-day deadline, then motion to compel.

## Pitfalls
- **Undocumented oral agreements.** Confirm every phone commitment in a follow-up email the same day.
- **Vague meet-and-confer records.** Courts require a genuine, itemized effort; log specifics, not "we conferred."
- **Missing your own deadlines while tracking theirs.** Keep the "we owe" column as sharp as the "they owe" column.
- **Overreacting to tone.** Posture informs strategy but should not drive premature motion practice.

## Output format
```
MATTER: <caption>  OC: <name/firm>  As of: <date>
CONTACT LOG: <date | medium | substance>
WE OWE: <item | due | source>
THEY OWE: <item | due | status>
MEET-AND-CONFER: <dispute | status>
POSTURE: <cooperative/positional/stonewalling>
NEXT ACTION: <step | owner | date>
```

## Reference
Under Fed. R. Civ. P. 37(a)(1), a motion to compel must certify a good-faith meet-and-confer; many districts (e.g., C.D. Cal. L.R. 37-1) require a formal joint-stipulation or letter process first, and some judges' standing orders demand a pre-motion conference. Fed. R. Civ. P. 26(c) applies the same conferral requirement to protective orders. Document conferral contemporaneously — the certification is scrutinized. Local rules and standing orders vary widely by district and judge; confirm the applicable requirements. General guidance, not legal advice.
