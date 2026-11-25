---
name: litig-matter-briefing
version: 1.0.0
description: Produce a briefing that brings a colleague or new attorney up to speed on a litigation matter quickly.
author: matrixx0070
tags: [litigation, briefing, handoff, case-management, strategy]
capabilities: []
---

## When to use
Use this when someone new joins the matter, when you are handing off, or before a strategy meeting where everyone needs shared context. Use it to compress the file into a fast, accurate orientation without making the reader dig through the docket. Aim for something a busy attorney can absorb in a few minutes.

**Not for:** logging a single event (see litig-matter-update) or opening the file (see litig-matter-intake).

## Method
1. Open with a one-paragraph posture summary: who is suing whom, over what, and where things stand.
2. Lay out the parties and their counsel.
3. Summarize the claims, defenses, and the current procedural posture.
4. Give the key upcoming deadlines and the near-term calendar. **Decision point:** if the next deadline is inside two weeks, lead with it.
5. Summarize strengths, weaknesses, and open strategic questions. **Decision point:** if the record is thin on a pivotal fact, flag it as an evidence gap rather than papering over it.
6. List immediate next actions and open items.
7. ATTORNEY-ESCALATION gate: because the briefing includes strategic assessment, route it to the supervising attorney for review before circulating beyond the internal team.

## Example
> A senior associate is added to a products-liability defense on the eve of a mediation. You produce a briefing: posture (design-defect claim, discovery closed), parties and counsel, the summary-judgment motion pending, the mediation in nine days (lead item), a strengths/weaknesses read, and the open question of whether to retain a second expert — flagged for the supervising attorney.

## Pitfalls
- **Narrative without posture:** the reader needs the procedural stage first, not a chronology.
- **Overclaiming strength:** present weaknesses honestly; a rosy briefing misleads strategy.
- **Stale deadlines:** pull dates from the current docket, not memory.
- **Burying the lede:** the nearest deadline and biggest risk belong at the top.

## Output format
```
MATTER: <name> | No: <matter#>
POSTURE: <one paragraph>
PARTIES & COUNSEL: <list>
CLAIMS / DEFENSES / STAGE: <summary>
CALENDAR: <next deadlines, soonest first>
STRENGTHS / WEAKNESSES / OPEN QUESTIONS: <bullets>
NEXT ACTIONS: <list>
STATUS: pending attorney review
```

## Reference
Procedural posture is the reader's anchor: pre-answer, pleadings, discovery, dispositive motions (FRCP 56 summary judgment), pretrial (FRCP 16 conference and order), trial, or appeal. In a handoff, confirm the operative complaint and answer, any pending motions, the current scheduling order, and outstanding discovery. Note the litigation-hold status and any privilege log obligations. Mediation and settlement posture matter for staffing. Work-product and privilege protections attach to your candid assessment (attorney work product under FRCP 26(b)(3)); mark the briefing privileged and confidential. This is general practice guidance; specifics vary by jurisdiction and should be confirmed with the supervising attorney.
