---
name: meeting-notes
description: "Transforms raw meeting notes, transcripts, or recordings into structured summaries with decisions captured, action items assigned, open questions tracked, and parking lot items preserved. The single skill every PM uses daily."
category: communication
default_depth: standard
---

# Meeting Notes & Action Items

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Transforms raw meeting notes, transcripts, or recordings into structured summaries with decisions captured, action items assigned, open questions tracked, and parking lot items preserved. The single skill every PM uses daily.

## When to Use

- After any meeting (standup, planning, 1:1, design review, stakeholder sync)
- Processing a meeting transcript or recording
- Before the next meeting, review previous action items
- When someone asks "what did we decide in that meeting?"

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick standup or informal sync with few decisions | TL;DR + Action Items only |
| **Standard** | Regular planning, design review, or stakeholder sync | All sections |
| **Deep** | High-stakes meeting (board, exec review, post-mortem) requiring full audit trail | All sections + verbatim quotes on key decisions, timestamped discussion notes, and explicit dissent record |

**Omit rules:** At Light depth, skip detailed discussion notes and parking lot. Retain the TL;DR, actual decisions with attribution, and action items. If no decision was made, say so; do not invent owners or dates.

## Framework

### Meeting Notes Template

```markdown
# [Meeting Name], [Date]

## Metadata
- **Date & Time:** [date, time, duration]
- **Attendees:** [names, mark who was absent with ~~strikethrough~~]
- **Facilitator:** [name]
- **Note-taker:** [name]
- **Recording:** [link, if available]

---

## Summary (TL;DR)
[2-3 sentences capturing the most important outcomes. If someone reads only this section, they should know what happened.]

---

## Decisions Made

| # | Decision | Context | Decision-Maker | Dissent? |
|---|---|---|---|---|
| D1 | [What was decided] | [Brief context, why this came up] | [Who made the call] | [Any notable disagreement to record] |
| D2 | [What was decided] | [Context] | [Who] | [Dissent] |

---

## Action Items

| # | Action | Owner | Due Date | Status |
|---|---|---|---|---|
| A1 | [Specific, actionable task] | [Single owner, never "the team"] | [Date] | [ ] Open |
| A2 | [Specific task] | [Owner] | [Date] | [ ] Open |
| A3 | [Specific task] | [Owner] | [Date] | [ ] Open |

---

## Discussion Notes

### Topic 1: [Title]
[Key points discussed. Capture the substance, not a transcript. Focus on:]
- Arguments for and against
- Data or evidence cited
- Concerns raised
- Resolution or next step

### Topic 2: [Title]
[Key points discussed]

---

## Open Questions

| # | Question | Owner (to resolve) | Due Date |
|---|---|---|---|
| Q1 | [Unresolved question that needs follow-up] | [Who will answer] | [When] |

---

## Parking Lot
[Items raised but explicitly deferred to a future discussion]
- [Topic 1], Revisit: [when]
- [Topic 2], Revisit: [when]

---

## Previous Action Items (Review)

| # | Action | Owner | Status | Outcome |
|---|---|---|---|---|
| A1 (prev) | [From last meeting] | [Owner] | [Done / In Progress / Blocked] | [Brief outcome] |
```

### Processing Raw Transcripts

When given a raw transcript or brain-dump notes:

**Step 1: Extract decisions**, Scan for language indicating a decision was made:
- "We agreed to..."
- "Let's go with..."
- "The decision is..."
- "We're going to..."

**Step 2: Extract action items**, Look for commitments:
- "[Name] will..."
- "Can you [action] by [date]?"
- "The next step is..."
- "We need someone to..."

**Step 3: Identify open questions**, Unresolved items:
- "We still need to figure out..."
- "I'll check on that"
- "TBD"
- Questions asked but not answered

**Step 4: Synthesize discussion**, Compress to key points:
- Remove small talk, filler, and repeated points
- Preserve disagreements and their resolution
- Capture data points and evidence cited
- Note emotional signals ("there was strong pushback on...")

### Meeting-Type-Specific Templates

**For Sprint Planning:**
Add: Sprint goal, committed stories, capacity breakdown

**For 1:1s:**
Add: Career development items, feedback given/received, personal context

**For Design Reviews:**
Add: Design decision log, feedback by reviewer, next iteration scope

**For Stakeholder Syncs:**
Add: Alignment status, escalation items, communication actions

## Minimum Evidence Bar

**Required inputs:** Raw meeting notes, transcript, or recording, plus attendee list and meeting purpose.

**Acceptable evidence:** Direct quotes from participants, screen-shared data referenced in discussion, stated commitments ("I'll do X by Friday"), explicit decisions ("We're going with option B").

**Insufficient evidence:** If a decision was implied but never explicitly stated, produce a partial artifact with the implied decision marked `[TBD, requires: explicit confirmation from decision-maker]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Decisions Made, Action Items, and the TL;DR must reflect only what was actually said or agreed.
- **Hypotheses:** Inferred sentiment or unstated concerns noted in Discussion Notes, must be labeled as "inferred" or "implied."

## Output Format

Produce structured meeting notes with:
1. **TL;DR**, 2-3 sentence summary
2. **Decisions**, numbered with context and decision-maker
3. **Action Items**, owned, dated, trackable
4. **Discussion Notes**, substance by topic
5. **Open Questions**, assigned and dated
6. **Parking Lot**, deferred items with revisit dates
7. **Previous Action Review**, accountability check

**Shipwright Signature (required closing):**
8. **Decision Frame**, key decision from this meeting, trade-offs discussed, confidence based on evidence cited in-room, decision owner, decision date, revisit trigger
9. **Unknowns & Evidence Gaps**, questions raised but unanswered, data cited but not verified, absent stakeholders whose input is needed
10. **Pass/Fail Readiness**, PASS if decisions are faithfully attributed and agreed actions have owners and dates. Mark missing attribution, ownership or dates as TBD and FAIL for action readiness; an informational meeting with no decisions or actions can PASS as an accurate record.
11. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Transcript, not notes**, Don't capture everything; capture what matters (decisions, actions, key arguments)
- **Unowned action items**, "We should look into X" is not an action item; "[Name] will research X by Friday" is
- **Missing decisions**, If a decision was made, it must be explicitly captured; implicit decisions get relitigated
- **No TL;DR**, People who weren't in the meeting need the summary; they won't read the full notes
- **Never reviewing previous actions**, Without accountability, meeting notes are write-only artifacts

## Weak vs. Strong Output

**Weak:**
> "A1: Look into the analytics issue, Team, ASAP"

No single owner, no specific date, vague task, this will never get done.

**Strong:**
> "A1: Investigate 15% drop in dashboard load time since March deploy, @Sarah, Due: 2025-04-04, Status: Open"

Named owner, specific problem, concrete deadline, trackable and accountable.
